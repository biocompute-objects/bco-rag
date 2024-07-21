"""Entry point for a singular, manual run."""

from llama_index.readers.github import GithubRepositoryReader  # type: ignore
from bcorag import misc_functions as misc_fns
from bcorag import option_picker as op
from bcorag.bcorag import BcoRag
from parameter_search.grid_search import BcoGridSearch
from parameter_search.random_search import BcoRandomSearch
from bcorag.custom_types.core_types import (
    GitFilter,
    GitFilters,
    create_git_data,
    create_git_filters,
)
from parameter_search.custom_types import (
    SearchSpace,
    create_git_data_file_config,
    init_search_space,
)
from evaluator.frontend.app import App
import argparse
import os


def _create_search_space() -> SearchSpace:
    """Creates a search space for parameter testing."""
    filenames = ["./bcorag/test_papers/High resolution measurement.pdf"]
    loaders = "SimpleDirectoryReader"
    chunking_config = [
        "1024 chunk size/20 chunk overlap",
        "2048 chunk size/50 chunk overlap",
    ]
    embedding_model = "text-embedding-3-large"
    vector_store = "VectorStoreIndex"
    similarity_top_k = [2, 3, 4]
    llms = ["gpt-3.5-turbo", "gpt-4-turbo"]

    github_url = "https://github.com/dpastling/plethora"
    git_info = misc_fns.extract_repo_data(github_url)
    if git_info is None:
        misc_fns.graceful_exit(1, "Error parsing github URL.")

    git_filters: list[GitFilters] = []
    directory_filter = create_git_filters(
        filter_type=GithubRepositoryReader.FilterType.EXCLUDE,
        filter=GitFilter.DIRECTORY,
        value=["logs", "fastq", "data"],
    )
    git_filters.append(directory_filter)

    file_ext_filter = create_git_filters(
        filter_type=GithubRepositoryReader.FilterType.EXCLUDE,
        filter=GitFilter.FILE_EXTENSION,
        value=[".txt", ".gz", ".bed"],
    )
    git_filters.append(file_ext_filter)

    git_data = create_git_data(
        user=git_info[0], repo=git_info[1], branch="master", filters=git_filters
    )

    git_file_data = create_git_data_file_config(
        os.path.basename(filenames[0]), git_data
    )

    search_space = init_search_space(
        filenames=filenames,
        loader=loaders,
        chunking_config=chunking_config,
        embedding_model=embedding_model,
        vector_store=vector_store,
        similarity_top_k=similarity_top_k,
        llm=llms,
        git_data=[git_file_data],
    )
    return search_space


def main() -> None:

    parser = argparse.ArgumentParser(prog="main.py")
    parser.add_argument(
        "run_mode",
        default="one-shot",
        nargs="?",
        choices=["one-shot", "grid-search", "random-search", "evaluate"],
        help="one-shot/grid-search/random-search/evaluate",
    )
    options = parser.parse_args()
    run_mode = options.run_mode.lower().strip()

    match run_mode:

        case "one-shot":

            logger = misc_fns.setup_root_logger("./logs/bcorag.log")
            logger.info(
                "################################## RUN START ##################################"
            )

            user_choices = op.initialize_picker()
            if user_choices is None:
                misc_fns.graceful_exit()

            bco_rag = BcoRag(user_choices)
            while True:
                domain = bco_rag.choose_domain()
                if domain is None or isinstance(domain, tuple):
                    misc_fns.graceful_exit()
                _ = bco_rag.perform_query(domain)
                print(f"Successfully generated the {domain} domain.\n")

        case "grid-search":

            grid_search = BcoGridSearch(_create_search_space())
            grid_search.train()

            misc_fns.graceful_exit()

        case "random-search":

            random_search = BcoRandomSearch(_create_search_space(), subset_size=5)
            random_search.train()

            misc_fns.graceful_exit()

        case "evaluate":

            app = App()
            app.start()

        case _:

            misc_fns.graceful_exit(1, "Unsupported run mode.")


if __name__ == "__main__":
    main()
