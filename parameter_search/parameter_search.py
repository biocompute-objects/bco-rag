"""Parameter search base class.
"""

from bcorag.bcorag import BcoRag, supress_stdout
from bcorag.custom_types import UserSelections, create_user_selections, GitData, DomainKey
from .custom_types import GitDataFileConfig, SearchSpace
from typing import Optional, get_args


class BcoParameterSearch:
    """Parent class that lays the foundation for the specific parameter
    search classes. This class shouldn't be instantiated directly.
    """

    def __init__(self, search_space: SearchSpace, verbose: bool = True):
        """Constructor.

        Parameters
        ----------
        search_space : SearchSpace
            The parameter search space.
        verbose : bool (default: True)
            The verbosity level. False for no output, True for running output.
        """

        self._files: list[str] = search_space["filenames"]
        self._loaders: list[str] = search_space["loader"]
        self._chunking_configs: list[str] = search_space["chunking_config"]
        self._embedding_models: list[str] = search_space["embedding_model"]
        self._vector_stores: list[str] = search_space["vector_store"]
        self._similarity_top_k: list[int] = search_space["similarity_top_k"]
        self._llms: list[str] = search_space["llm"]
        self._git_data: Optional[list[GitDataFileConfig]] = search_space["git_data"]
        self._verbose: bool = verbose

    def _generate_domains(self, bcorag: BcoRag):
        
        domain: DomainKey
        for domain in get_args(DomainKey):
            with supress_stdout():
                bcorag.perform_query(domain)

    def _create_bcorag(
        self,
        llm: str,
        embedding_model: str,
        filename: str,
        filepath: str,
        vector_store: str,
        loader: str,
        similarity_top_k: int,
        chunking_config: str,
        git_data: Optional[GitData],
        mode: str = "production",
        evaluation_mode: bool = False
    ) -> BcoRag:
        """Creates the user selections set for the BcoRag."""
        user_selections: UserSelections = create_user_selections(
            llm,
            embedding_model,
            filename,
            filepath,
            vector_store,
            loader,
            mode,
            similarity_top_k,
            chunking_config,
            git_data,
        )
        bcorag = BcoRag(user_selections, evaluation_metrics=evaluation_mode)
        return bcorag
