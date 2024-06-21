""" Handles the RAG implementation using the llama-index library.
"""

from typing import Optional, get_args
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    Settings,
    download_loader,
    get_response_synthesizer,
    Response,
)
from llama_index.core.callbacks import CallbackManager, TokenCountingHandler
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.evaluation import FaithfulnessEvaluator, RelevancyEvaluator
from llama_index.llms.openai import OpenAI  # type: ignore
from llama_index.embeddings.openai import OpenAIEmbedding  # type: ignore
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.readers.github import GithubRepositoryReader, GithubClient  # type: ignore
from dotenv import load_dotenv
import tiktoken
import time
from pathlib import Path
from hashlib import md5
import os
from contextlib import contextmanager, redirect_stdout
import json
from . import EVALUATION_LLM
from .custom_types import (
    GitData,
    create_output_tracker_param_set,
    create_output_tracker_runs_entry,
    create_output_tracker_entry,
    create_output_tracker_domain_entry,
    default_output_tracker_file,
    UserSelections,
    DomainKey,
)
import bcorag.misc_functions as misc_fns
from .prompts import DOMAIN_MAP, QUERY_PROMPT, SUPPLEMENT_PROMPT


@contextmanager
def supress_stdout():
    """Context manager that redirects stdout and stderr to devnull."""
    with open(os.devnull, "w") as f, redirect_stdout(f):
            yield


class BcoRag:
    """Class to handle the RAG implementation.

    Attributes
    ----------
    _parameter_set_hash : str
        The MD5 hexidecimal hash of the parameter set.
    _domain_map : DomainMap
        Mapping for each domain to its standardized prompt.
    _file_name : str
        The source file (paper) name.
    _file_path : str
        The file path to the source file (paper).
    _output_path_root : str
        Path to the specific document directory to dump the outputs.
    _debug : bool
        Whether in debug mode or not.
    _logger : logging.Logger
        The document specific logger.
    _llm_model_name : str
        The LLM model name.
    _llm_model : OpenAI
        The Open AI LLM model instance.
    _embed_model_name : str
        The embedding model name.
    _embed_model : OpenAIEmbedding
        The embedding model instance.
    _loader : str
        The data loader being used.
    _vector_store : str
        The vector store being used.
    _splitter : SemanticSplitterNodeParser or None
        The node parser (if a non-fixed chunking strategy is chosen).
    _similarity_top_k : int
        The similarity top k retrieval number for node sources.
    _token_counter : TokenCountingHandler or None
        The token counter handler or None if in production mode.
    _token_counts : dict[str, int] or None
        The token counts or None if in production mode.
    _git_data : GitData or None
        The git data or None if no github repo was included.
    _faithfulness_evaluator : Optional[FaithfulnessEvaluator]
        The faithfulness evalauator instance.
    _relevancy_evaluator : Optional[RelevancyEvaluator]
        The relevancy evaluator instance.
    _documents : list[Documents]
        The list of documents (containers for the data source).
    _index : VectorStoreIndex
        The vector store index instance.
    _query_engine : RetrieverQueryEngine
        The query engine.
    """

    def __init__(
        self,
        user_selections: UserSelections,
        output_dir: str = "./output",
        evaluation_metrics: bool = False,
    ):
        """Constructor.

        Parameters
        ---------
        user_selections : UserSelections
            The user configuration selections.
        output_dir : str (default: "./output")
            The directory to dump the outputs (relative to main.py entry point
            in the repo root).
        evaluation_metrics : bool (default: False)
            Whether or not to calculate Faithfulness and Relevancy metrics.
        """
        load_dotenv()

        self._parameter_set_hash = self._user_selection_hash(user_selections)
        self._domain_map = DOMAIN_MAP
        self._file_name = user_selections["filename"]
        self._file_path = user_selections["filepath"]
        self._output_path_root = os.path.join(
            output_dir,
            os.path.splitext(self._file_name.lower().replace(" ", "_").strip())[0],
        )
        self._debug = True if user_selections["mode"] == "debug" else False
        self._logger = misc_fns.setup_document_logger(
            self._file_name.lower().strip().replace(" ", "_")
        )
        self._llm_model_name = user_selections["llm"]
        self._llm_model = OpenAI(model=self._llm_model_name)
        self._embed_model_name = user_selections["embedding_model"]
        self._embed_model = OpenAIEmbedding(model=self._embed_model_name)
        self._loader = user_selections["loader"]
        self._vector_store = user_selections["vector_store"]
        self._splitter = None
        self._similarity_top_k = user_selections["similarity_top_k"]
        self._chunking_config = user_selections["chunking_config"]
        self._token_counter: TokenCountingHandler | None = None
        self._token_counts: dict[str, int] | None = None
        self._git_data: Optional[GitData] = (
            user_selections["git_data"]
            if user_selections["git_data"] is not None
            else None
        )
        self._faithfulness_evaluator: Optional[FaithfulnessEvaluator] = None
        self._relevancy_evaluator: Optional[RelevancyEvaluator] = None
        if evaluation_metrics:
            _evaluation_llm = OpenAI(model=EVALUATION_LLM, temperature=0.0)
            self._faithfulness_evaluator = FaithfulnessEvaluator(llm=_evaluation_llm)
            self._relevancy_evaluator = RelevancyEvaluator(llm=_evaluation_llm)

        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise EnvironmentError("OpenAI API key not found.")

        github_token = os.getenv("GITHUB_TOKEN")
        if self._git_data is not None and not github_token:
            raise EnvironmentError("Github token not found.")

        misc_fns.check_dir(self._output_path_root)
        self._display_info(user_selections, "User selections:")

        Settings.embed_model = self._embed_model
        Settings.llm = self._llm_model

        match self._chunking_config:
            case "semantic":
                self._splitter = SemanticSplitterNodeParser.from_defaults(
                    buffer_size=1,
                    embed_model=self._embed_model,
                    # The percentile of cosin dissimilarity that must be exceeded
                    # between a group of sentences and the next to form a node. The
                    # smaller this number is, the more nodes will be generated.
                    breakpoint_percentile_threshold=90,
                )
            case "256 chunk size/20 chunk overlap":
                Settings.chunk_size = 256
                Settings.chunk_overlap = 50
            case "512 chunk size/50 chunk overlap":
                Settings.chunk_size = 512
                Settings.chunk_overlap = 50
            case "2048 chunk size/50 chunk overlap":
                Settings.chunk_size = 2048
                Settings.chunk_overlap = 50
            case _:
                Settings.chunk_size = 1024
                Settings.chunk_overlap = 20

        if self._debug:
            self._token_counter = TokenCountingHandler(
                tokenizer=tiktoken.encoding_for_model(self._llm_model_name).encode
            )
            Settings.callback_manager = CallbackManager([self._token_counter])
            self._token_counts = {
                "embedding": 0,
                "input": 0,
                "output": 0,
                "total": 0,
            }

        match self._loader:
            case "SimpleDirectoryReader":
                loader = SimpleDirectoryReader(input_files=[self._file_path])
                paper_documents = loader.load_data()
            case "PDFReader":
                with supress_stdout():
                    pdf_loader = download_loader("PDFReader")
                paper_documents = pdf_loader().load_data(file=Path(self._file_path))
        documents = paper_documents  # type: ignore
        if self._git_data is not None:
            github_client = GithubClient(github_token)
            with supress_stdout():
                download_loader("GithubRepositoryReader")
            git_loader = GithubRepositoryReader(
                github_client=github_client,
                owner=self._git_data["user"],
                repo=self._git_data["repo"],
            )
            github_documents = git_loader.load_data(branch=self._git_data["branch"])
            documents += github_documents
            self._logger.info(
                f"Loading repo `{self._git_data['repo']}` from user `{self._git_data['user']}`"
            )
        self._documents = documents

        _chunk_fixed = (
            False if user_selections["chunking_config"] == "semantic" else True
        )
        if self._vector_store == "VectorStoreIndex":
            if _chunk_fixed:
                self._index = VectorStoreIndex.from_documents(self._documents)
            else:
                if self._splitter is not None:
                    nodes = self._splitter.build_semantic_nodes_from_documents(
                        self._documents
                    )
                    self._index = VectorStoreIndex(nodes=nodes)

        retriever = VectorIndexRetriever(
            index=self._index, similarity_top_k=self._similarity_top_k
        )
        response_synthesizer = get_response_synthesizer()
        self._query_engine = RetrieverQueryEngine(
            retriever=retriever, response_synthesizer=response_synthesizer
        )

        if (
            self._debug
            and self._token_counts is not None
            and self._token_counter is not None
        ):
            self._token_counts[
                "embedding"
            ] += self._token_counter.total_embedding_token_count

    def perform_query(self, domain: DomainKey) -> str:
        """Performs a qeury for a specific BCO domain.

        Parameters
        ----------
        domain : DomainKey
            The domain being queried for.

        Returns
        -------
        str
            The generated domain.
        """
        query_start_time = time.time()
        query_prompt = QUERY_PROMPT.format(domain, self._domain_map[domain]["prompt"])
        if self._domain_map[domain]["top_level"]:
            query_prompt += f"\n{SUPPLEMENT_PROMPT}"
        response_object = self._query_engine.query(query_prompt)
        if isinstance(response_object, Response):
            response_object = Response(
                response=response_object.response,
                metadata=response_object.metadata,
                source_nodes=response_object.source_nodes,
            )
        else:
            self._logger.error(
                f"Error parsing response object, expected type Response, got type `{type(response_object)}`."
            )
            print(
                f"Error parsing response object, expected type Response, got type `{type(response_object)}`."
            )
            misc_fns.graceful_exit(1)
        query_response = str(response_object.response)

        source_str = ""
        for idx, source_node in enumerate(response_object.source_nodes):
            source_str += f"\n--------------- Source Node '{idx + 1}/{len(response_object.source_nodes)}' ---------------"
            source_str += f"\nNode ID: '{source_node.node.node_id}'"
            source_str += f"\nSimilarity: '{source_node.score}'"
            source_str += f"\nMetadata String:\n`{source_node.node.get_metadata_str()}`"
            source_str += (
                f"\nMetadata Size: `{len(source_node.node.get_metadata_str())}`"
            )
            source_str += f"\nContent Size: `{len(source_node.node.get_content())}`"
            source_str += (
                f"\nRetrieved Text:\n{source_node.node.get_content().strip()}\n"
            )
            source_str += "\n"

        if self._faithfulness_evaluator and self._relevancy_evaluator:
            for idx, source_node in enumerate(response_object.source_nodes):
                faithfulness_eval = self._faithfulness_evaluator.evaluate(
                    response=response_object.response,
                    contexts=[source_node.get_content()],
                )
                relevancy_eval = self._relevancy_evaluator.evaluate(
                    query=query_prompt,
                    response=response_object.response,
                    contexts=[source_node.get_content()],
                )
                for name, eval in {
                    "faithfulness": faithfulness_eval,
                    "relevancy": relevancy_eval,
                }.items():
                    self._display_info(
                        {
                            "passing": eval.passing,
                            "score": eval.score,
                            "feedback": eval.feedback,
                        },
                        f"{name.title()} Evaluation for node {idx + 1}:",
                    )

        if self._debug:
            self._display_info(query_prompt, f"QUERY PROMPT for the {domain} domain:")
            self._token_counts["input"] += self._token_counter.prompt_llm_token_count  # type: ignore
            self._token_counts["output"] += self._token_counter.completion_llm_token_count  # type: ignore
            self._token_counts["total"] += self._token_counter.total_llm_token_count  # type: ignore
            self._token_counts["embedding"] += self._token_counter.total_embedding_token_count  # type: ignore
            self._display_info(self._token_counts, "Updated token counts:")
            self._display_info(source_str, "Retrieval source(s):")

        query_elapsed_time = time.time() - query_start_time
        self._process_output(
            domain, query_response, source_str, round(query_elapsed_time, 2)
        )

        return query_response

    def choose_domain(
        self, automatic_query: bool = False
    ) -> Optional[tuple[DomainKey, str] | DomainKey]:
        """Gets the user input for the domain the user wants to generate.

        Parameters
        ----------
        automatic_query : bool (default: False)
            Whether to automatically query after the user chooses a domain. If set to
            True this is a shortcut to calling bcorag.perform_query(choose_domain()).

        Returns
        -------
        (DomainKey, str), str or None
            If automatic query is set to True will return a tuple containing the domain
            name and the query response. If automatic query is False will return the user
            chosen domain. None is returned if the user chooses to exit.
        """
        domain_prompt = (
            "Which domain would you like to generate? Supported domains are:"
        )

        domain_user_prompt: DomainKey
        for domain_user_prompt in get_args(DomainKey):
            domain_prompt += (
                f"\n\t{self._domain_map[domain_user_prompt]['user_prompt']}"
            )
        domain_prompt += "\n\tE[x]it\n"
        print(domain_prompt)

        domain_selection = None

        while True:

            domain_selection = input().strip().lower()

            domain: DomainKey
            for domain in get_args(DomainKey):
                if (
                    domain_selection == domain
                    or domain_selection == self._domain_map[domain]["code"]
                ):
                    domain_selection = domain
                    break
            else:
                if domain_selection == "exit" or domain_selection == "x":
                    if self._debug:
                        self._display_info(
                            "User selected 'exit' on the domain selection step."
                        )
                    return None
                else:
                    if self._debug:
                        self._display_info(
                            f"User entered unrecognized input '{domain_selection}' on domain chooser step."
                        )
                    print(
                        f"Unrecognized input {domain_selection} entered, please try again."
                    )
                    continue
            break

        if automatic_query:
            if self._debug:
                self._display_info(
                    f"Automatic query called on domain: '{domain_selection}'."
                )
            return domain_selection, self.perform_query(domain_selection)
        if self._debug:
            self._display_info(
                f"User chose '{domain_selection}' with no automatic query."
            )
        return domain_selection

    def _process_output(
        self, domain: DomainKey, response: str, source_str: str, elapsed_time: float
    ):
        """Attempts to serialize the response into a JSON object and dumps the output.
        Also dumps the raw text regardless if JSON serialization was successful. The
        file dumps are dumped to the `output` directory located in the root of this
        repo. Keeps a TSV file to track all of the domain outputs and what parameter
        set generated the results. Does not overwrite existing domains outputs,

        Parameters
        ----------
        domain : DomainKey
            The domain the response is for.
        response : str
            The generated response to dump.
        source_str : str
            The formatted source string for the query.
        elapsed_time : float
            The query generation elapsed time.
        """

        def dump_json_response(fp: str, response_string: str) -> bool:
            if response_string.startswith("```json\n"):
                response_string = response_string.replace("```json\n", "").replace(
                    "```", ""
                )
            self._display_info(
                response_string, f"QUERY RESPONSE for the `{domain}` domain:"
            )
            try:
                response_json = json.loads(response_string)
                if misc_fns.write_json(fp, response_json):
                    self._logger.info(
                        f"Succesfully serialized JSON response for the `{domain}` domain."
                    )
                    return True
            except Exception as e:
                self._logger.error(
                    f"Failed to serialize the JSON response for the `{domain}` domain.\n{e}"
                )
            return False

        generated_dir = os.path.join(self._output_path_root, "generated_domains")
        misc_fns.check_dir(generated_dir)

        txt_file_unindexed = os.path.join(
            generated_dir, f"{domain}-(index)-{self._parameter_set_hash}.txt"
        )
        json_file_unindexed = os.path.join(
            generated_dir, f"{domain}-(index)-{self._parameter_set_hash}.json"
        )
        source_file_unindexed = os.path.join(
            self._output_path_root,
            "reference_sources",
            f"{domain}-(index)-{self._parameter_set_hash}.txt",
        )

        output_map_json = misc_fns.load_output_tracker(
            os.path.join(self._output_path_root, "output_map.json")
        )

        # Create a new output file if one doesn't exist
        if output_map_json is None:

            txt_file = txt_file_unindexed.replace("(index)", "1")
            json_file = json_file_unindexed.replace("(index)", "1")
            source_file = source_file_unindexed.replace("(index)", "1")
            if not dump_json_response(json_file, response):
                json_file = "NA"

            run_entry = create_output_tracker_runs_entry(
                1,
                misc_fns.create_timestamp(),
                txt_file,
                json_file,
                source_file,
                elapsed_time,
            )

            param_set = create_output_tracker_param_set(
                self._loader,
                self._vector_store,
                self._llm_model_name,
                self._embed_model_name,
                self._similarity_top_k,
                self._chunking_config,
                self._git_data["user"] if self._git_data is not None else None,
                self._git_data["repo"] if self._git_data is not None else None,
                self._git_data["branch"] if self._git_data is not None else None,
            )

            instance_entry = create_output_tracker_entry(1, param_set, [run_entry])

            domain_entry = create_output_tracker_domain_entry(
                self._parameter_set_hash, instance_entry
            )

            output_data = default_output_tracker_file()
            output_data[domain].append(domain_entry)

        # update output map
        else:

            domain_map_entries = output_map_json[domain]

            for domain_map_entry in domain_map_entries:

                # found the collision entry
                if domain_map_entry["hash_str"] == self._parameter_set_hash:

                    new_index = domain_map_entry["entries"]["curr_index"] + 1
                    domain_map_entry["entries"]["curr_index"] = new_index

                    txt_file = txt_file_unindexed.replace("(index)", str(new_index))
                    json_file = json_file_unindexed.replace("(index)", str(new_index))
                    source_file = source_file_unindexed.replace(
                        "(index)", str(new_index)
                    )
                    if not dump_json_response(json_file, response):
                        json_file = "NA"

                    run_entry = create_output_tracker_runs_entry(
                        new_index,
                        misc_fns.create_timestamp(),
                        txt_file,
                        json_file,
                        source_file,
                        elapsed_time,
                    )

                    domain_map_entry["entries"]["runs"].append(run_entry)

                    break

            # first time parameter set run (loop didn't break)
            else:

                txt_file = txt_file_unindexed.replace("(index)", "1")
                json_file = json_file_unindexed.replace("(index)", "1")
                source_file = source_file_unindexed.replace("(index)", "1")
                if not dump_json_response(json_file, response):
                    json_file = "NA"

                run_entry = create_output_tracker_runs_entry(
                    1,
                    misc_fns.create_timestamp(),
                    txt_file,
                    json_file,
                    source_file,
                    elapsed_time,
                )

                param_set = create_output_tracker_param_set(
                    self._loader,
                    self._vector_store,
                    self._llm_model_name,
                    self._embed_model_name,
                    self._similarity_top_k,
                    self._chunking_config,
                    self._git_data["user"] if self._git_data is not None else None,
                    self._git_data["repo"] if self._git_data is not None else None,
                    self._git_data["branch"] if self._git_data is not None else None,
                )

                instance_entry = create_output_tracker_entry(1, param_set, [run_entry])

                domain_entry = create_output_tracker_domain_entry(
                    self._parameter_set_hash, instance_entry
                )

                domain_map_entries.append(domain_entry)

            output_data = output_map_json

        misc_fns.dump_string(txt_file, response)
        misc_fns.dump_string(source_file, source_str)
        # writes the output mapping files
        misc_fns.write_json(
            os.path.join(self._output_path_root, "output_map.json"), output_data
        )
        misc_fns.dump_output_file_map_tsv(
            os.path.join(self._output_path_root, "output_map.tsv"), output_data
        )

    def _display_info(
        self,
        info: Optional[dict | list | str | UserSelections],
        header: Optional[str] = None,
    ):
        """If in debug mode, handles the debug info output to the log file.

        Parameters
        ----------
        info : dict, list, str UserSelections, or None
            The object to log.
        header : str or None (default: None)
            The optional header to log before the info.
        """
        log_str = header if header is not None else ""
        if isinstance(info, dict):
            for key, value in info.items():
                log_str += f"\n\t{key}: '{value}'"
        elif isinstance(info, str):
            log_str += f"{info}" if header is None else f"\n{info}"
        self._logger.info(log_str)

    def _user_selection_hash(self, params: UserSelections) -> str:
        """Generates an MD5 hash of the parameter set.

        Parameters
        ----------
        params : UserSelections
            The user configuration selections.

        Returns
        -------
        str
            The hexidecimal MD5 hash.
        """
        hash_str = ""
        hash_str += params["llm"]
        hash_str += params["embedding_model"]
        hash_str += params["vector_store"]
        hash_str += params["loader"]
        hash_str += str(params["similarity_top_k"])
        hash_str += params["chunking_config"]
        if params["git_data"] is not None:
            user = params["git_data"]["user"]
            repo = params["git_data"]["repo"]
            hash_str += user if user is not None else ""
            hash_str += repo if repo is not None else ""
        hash_hex = md5(hash_str.encode("utf-8")).hexdigest()
        return hash_hex
