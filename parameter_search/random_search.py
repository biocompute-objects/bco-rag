"""Random search class.
"""

from .parameter_search import BcoParameterSearch
from .custom_types import SearchSpace
from bcorag.custom_types import UserSelections, create_git_data, create_user_selections
from itertools import product
import os
import random


class BcoRandomSearch(BcoParameterSearch):
    """BCO random search class. Subclass of
    BcoParameterSearch.
    """

    def __init__(self, search_space: SearchSpace, subset_size: int = 5):
        """Constructor.

        Parameters
        ----------
        search_space : SearchSpace
            The parameter search space.
        subset_size : int (default: 5)
            The number of parameter sets to search.
        """
        super().__init__(search_space)
        self.subset_size = subset_size

    def _create_param_sets(self) -> list[UserSelections]:
        """Creates a random subset of the parameter space."""
        param_sets: list[UserSelections] = []

        for (
            llm,
            embedding_model,
            filepath,
            loader,
            chunking_config,
            vector_store,
            similarity_top_k,
        ) in product(
            self._llms,
            self._embedding_models,
            self._files,
            self._loaders,
            self._chunking_configs,
            self._vector_stores,
            self._similarity_top_k,
        ):
            base_selections = {
                "llm": llm,
                "embedding_model": embedding_model,
                "filename": os.path.basename(str(filepath)),
                "filepath": filepath,
                "vector_store": vector_store,
                "loader": loader,
                "mode": "production",
                "similarity_top_k": similarity_top_k,
                "chunking_config": chunking_config,
            }

            if self._git_data is None:
                base_selections["git_data"] = None
            else:
                for git_data in self._git_data:
                    if git_data["filename"] == filepath or git_data[
                        "filename"
                    ] == os.path.basename(str(filepath)):
                        base_selections["git_data"] = create_git_data(
                            user=git_data["git_info"]["user"],
                            repo=git_data["git_info"]["repo"],
                            branch=git_data["git_info"]["branch"],
                            filters=git_data["git_info"]["filters"],
                        )
            user_selections = create_user_selections(
                base_selections["llm"],
                base_selections["embedding_model"],
                base_selections["filename"],
                base_selections["filepath"],
                base_selections["vector_store"],
                base_selections["loader"],
                base_selections["mode"],
                base_selections["similarity_top_k"],
                base_selections["chunking_config"],
                base_selections["git_data"],
            )
            param_sets.append(user_selections)

        if self.subset_size > len(param_sets):
            self.subset_size = len(param_sets)

        param_subset = random.sample(param_sets, self.subset_size)

        return param_subset
