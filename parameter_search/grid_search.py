"""Grid search class implementation.
"""

from .parameter_search import BcoParameterSearch
from .custom_types import SearchSpace
from bcorag.custom_types.core_types import (
    UserSelections,
    create_git_data,
    create_user_selections,
)
from bcorag.misc_functions import setup_root_logger, check_dir
from itertools import product
from logging import Logger
import os


class BcoGridSearch(BcoParameterSearch):
    """BCO grid search class. Subclass of `BcoParameterSearch`."""

    def __init__(self, search_space: SearchSpace):
        """Constructor.

        Parameters
        ----------
        search_space : SearchSpace
            The parameter search space.
        """
        super().__init__(search_space)

    def _setup_logger(self, path: str = "./logs", name: str = "grid-search") -> Logger:
        """Sets up the logger.

        Parameters
        ----------
        path : str, optional
            File path for the logger.
        name : str, optional
            Name for the logger output.

        Returns
        -------
        Logger
            The grid search logger.
        """
        check_dir(path)
        if not name.endswith(".log"):
            name = f"{name}.log"
        return setup_root_logger(os.path.join(path, name))

    def _create_param_sets(self) -> list[UserSelections]:
        """Creates a cartesian product of the parameter space.

        Returns
        -------
        list[UserSelections]
            Every comination of the parameter search space.
        """
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

            if self._other_docs is None:
                base_selections["other_docs"] = None
            else:
                for paper, other_docs in self._other_docs.items():
                    if paper == os.path.basename(str(filepath)):
                        base_selections["other_docs"] = other_docs

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
                base_selections["other_docs"],
            )
            param_sets.append(user_selections)

        return param_sets
