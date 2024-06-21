"""Parameter search base class.
"""

from bcorag.bcorag import BcoRag, supress_stdout_stderr
import tqdm
from bcorag.custom_types import UserSelections, create_user_selections, GitData, DomainKey
from .custom_types import SearchSpace
from typing import Optional, get_args


class _BcoParameterSearch:
    """Parent class that lays the foundation for the specific parameter
    search classes. This class shouldn't be instantiated directly.
    """

    def __init__(self, search_space: SearchSpace):

        self._files = search_space["filenames"]
        self._loaders = search_space["loader"]
        self._chunking_configs = search_space["chunking_config"]
        self._embedding_models = search_space["embedding_model"]
        self._vector_stores = search_space["vector_store"]
        self._similarity_top_k = search_space["similarity_top_k"]
        self._llms = search_space["llm"]
        self._git_data = search_space["git_data"]

    def generate_domains(self, bcorag: BcoRag):
        
        domain: DomainKey
        for domain in get_args(DomainKey):
            with supress_stdout_stderr():
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
