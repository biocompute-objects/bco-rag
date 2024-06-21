import os
from typing import TypedDict, Optional
from bcorag.custom_types import GitData, OptionKey
from bcorag.misc_functions import load_config_data, graceful_exit, get_file_list

config_object = load_config_data("./bcorag/conf.json")
if config_object is None:
    graceful_exit(1, "Error loading bcorag config object in custom type load.")
_options = config_object["options"]


class _AvailFilters(TypedDict):
    """Internal class for the available parameter set."""

    loader: list[str]
    chunking_config: list[str]
    embedding_model: list[str]
    vector_store: list[str]
    similarity_top_k: list[int]
    llm: list[str]
    mode: list[str]


_avail_options: _AvailFilters = {
    "loader": _options["loader"]["list"],
    "chunking_config": _options["chunking_config"]["list"],
    "embedding_model": _options["embedding_model"]["list"],
    "vector_store": _options["vector_store"]["list"],
    "similarity_top_k": [int(k) for k in _options["similarity_top_k"]["list"]],
    "llm": _options["llm"]["list"],
    "mode": _options["mode"]["list"],
}


class GitDataFileConfig:
    """Git data instance for a file."""

    filename: str
    git_info: GitData


class SearchSpace(TypedDict):
    """Search space used for hyperparameter search."""

    filenames: list[str]
    loader: list[str]
    chunking_config: list[str]
    embedding_model: list[str]
    vector_store: list[str]
    similarity_top_k: list[int]
    llm: list[str]
    git_data: Optional[list[GitDataFileConfig]]


def init_search_space(
    filenames: Optional[list[str] | str] = None,
    loader: Optional[list[str] | str] = None,
    chunking_config: Optional[list[str] | str] = None,
    embedding_model: Optional[list[str] | str] = None,
    vector_store: Optional[list[str] | str] = None,
    similarity_top_k: Optional[list[int] | int] = None,
    llm: Optional[list[str] | str] = None,
    git_data: Optional[list[GitDataFileConfig]] = None,
) -> SearchSpace:
    """Creates a search space instance.

    Parameters
    ----------
    filenames : list[str], str, or None (default: None)
        The filenames to test over for the search space (if None,
        defaults to all the filenames in the `bcorag/test_papers/`
        directory). Note, many files can increase run time
        significantly as a full parameter search will be executed
        on each paper sequentially.
    loader : list[str], str, or None (default: None)
        The data loaders for the search space (if None, defaults to
        the full list as defined in the conf.json list).
    chunking_config : list[str], str, or None (default: None)
        The chunking strategies for the search space (if None, defaults
        to the full list as defined in the conf.json list).
    embedding_model : list[str], str, or None (default: None)
        The embedding model for the search space (if None, defaults
        to the full list as defined in the conf.json list).
    vector_store : list[str], str, or None (default: None)
        The vector store for the search space (if None, defaults
        to the full list as defined in the conf.json list).
    similarity_top_k : list[int], int, or None (default: None)
        The similarity top k for the search space (if None, defaults
        to the full list as defined in the conf.json list).
    llm : list[str], str, or None (default: None)
        The llm for the search space (if None, defaults
        to the full list as defined in the conf.json list).
    git_data : list[GitDataFileConfig], GitDataFileConfig or None (default: None)
        The git data for each file (if None, assumes no git data for
        any files).

    Returns
    -------
    SearchSpace
        The search space grid.
    """

    def _validate_options(
        option: OptionKey, option_list: list[str] | list[int]
    ) -> bool:
        if not set(option_list) <= set(_avail_options[option]):
            return False
        return True

    match filenames:
        case list():
            filenames_space: list[str] = filenames
        case str():
            filenames_space = [filenames]
        case None:
            filenames_space = get_file_list("./bcorag/test_papers", "*.pdf")
        case _:
            graceful_exit(1, "Invalid type for filenames")
    for file in filenames_space:
        if not os.path.isfile(file):
            graceful_exit(1, f"Invalid file `{file}`")

    match loader:
        case list():
            loader_space: list[str] = loader
            if not _validate_options("loader", loader_space):
                graceful_exit(1, "Invalid or undefined loader in search space")
        case str():
            loader_space = [loader]
            if not _validate_options("loader", loader_space):
                graceful_exit(1, "Invalid or undefined loader in search space")
        case None:
            loader_space = _avail_options["loader"]
        case _:
            graceful_exit(1, "Invalid type specified for loader")

    match chunking_config:
        case list():
            chunking_space: list[str] = chunking_config
            if not _validate_options("chunking_config", chunking_space):
                graceful_exit(
                    1, "Invalid or undefined chunking strategy in search space"
                )
        case str():
            chunking_space = [chunking_config]
            if not _validate_options("chunking_config", chunking_space):
                graceful_exit(
                    1, "Invalid or undefined chunking strategy in search space"
                )
        case None:
            chunking_space = _avail_options["chunking_config"]
        case _:
            graceful_exit(1, "Invalid type specified for chunking_config")

    match embedding_model:
        case list():
            embedding_model_space: list[str] = embedding_model
            if not _validate_options("embedding_model", embedding_model_space):
                graceful_exit(1, "Invalid or undefined embedding model in search space")
        case str():
            embedding_model_space = [embedding_model]
            if not _validate_options("embedding_model", embedding_model_space):
                graceful_exit(1, "Invalid or undefined embedding model in search space")
        case None:
            embedding_model_space = _avail_options["embedding_model"]
        case _:
            graceful_exit(1, "Invalid type specified for embedding_model")

    match vector_store:
        case list():
            vector_store_space: list[str] = vector_store
            if not _validate_options("vector_store", vector_store_space):
                graceful_exit(1, "Invalid or undefined vector store in search space")
        case str():
            vector_store_space = [vector_store]
            if not _validate_options("vector_store", vector_store_space):
                graceful_exit(1, "Invalid or undefined vector store in search space")
        case None:
            vector_store_space = _avail_options["vector_store"]
        case _:
            graceful_exit(1, "Invalid type specified for vector_store")

    match similarity_top_k:
        case list():
            similarity_top_k_space: list[int] = similarity_top_k
        case int():
            similarity_top_k_space = [similarity_top_k]
        case None:
            similarity_top_k_space = _avail_options["similarity_top_k"]
        case _:
            graceful_exit(1, "Invalid type for similarity top k")

    match llm:
        case list():
            llm_space: list[str] = llm
            if not _validate_options("llm", llm_space):
                graceful_exit(1, "Invalid or undefined llm in search space")
        case str():
            llm_space = [llm]
            if not _validate_options("llm", llm_space):
                graceful_exit(1, "Invalid or undefined llm in search space")
        case None:
            llm_space = _avail_options["llm"]
        case _:
            graceful_exit(1, "Invalid type for llm")

    match git_data:
        case list():
            git_data_space: list[GitDataFileConfig] | None = git_data
        case None:
            git_data_space = None

    return_data: SearchSpace = {
        "filenames": filenames_space,
        "loader": loader_space,
        "chunking_config": chunking_space,
        "embedding_model": embedding_model_space,
        "vector_store": vector_store_space,
        "similarity_top_k": similarity_top_k_space,
        "llm": llm_space,
        "git_data": git_data_space,
    }

    return return_data
