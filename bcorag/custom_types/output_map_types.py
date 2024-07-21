""" The output map custom types.
"""

from .. import __version__
from typing import TypedDict, Optional


class OutputTrackerGitFilter(TypedDict):
    """Parsed git filter TypedDict used for output map formatting.

    Attributes
    ----------
    filter : tuple[str, list[str]]
        Tuple representing the filter type (include or exclude) and the filter values.
    """

    filter: tuple[str, list[str]]


def create_output_tracker_git_filter(
    filter: tuple[str, list[str]]
) -> OutputTrackerGitFilter:
    """Constructor for the `OutputTrackerGitFilter` TypedDict.

    Parameters
    ----------
    filter : tuple[str, list[str]]

    Returns
    -------
    OutputTrackerGitFilter
    """
    return_data: OutputTrackerGitFilter = {"filter": filter}
    return return_data


class OutputTrackerParamSet(TypedDict):
    """Parameter set for a run.

    Attributes
    ----------
    loader : str
        The data loader used for the run.
    vector_store : str
        The vector store used for the run.
    llm : str
        The LLM name used for the run.
    embedding_model : str
        The embedding model used for the run.
    similarity_top_k : int
        The similarity top k value used for the run.
    chunking_config : str
        The chunking strategy used for the run.
    git_user : Optional[str]
        The user who owns the github repository included in the document ingestion for the run (if applicable).
    git_repo : Optional[str]
        The github repository included in the document ingestion for the run (if applicable).
    git_branch : Optional[str]
        The github repository branch indexed during the document ingestion for the run (if applicable).
    directory_git_filter : Optional[OutputTrackerGitFilter]
        The directory filter used for indexing the github repository (if applicable).
    file_ext_git_filter : Optional[OutputTrackerGitFilter]
        The file extension filter used for indexing the github repository (if applicable).
    """

    loader: str
    vector_store: str
    llm: str
    embedding_model: str
    similarity_top_k: int
    chunking_config: str
    git_user: Optional[str]
    git_repo: Optional[str]
    git_branch: Optional[str]
    directory_git_filter: Optional[OutputTrackerGitFilter]
    file_ext_git_filter: Optional[OutputTrackerGitFilter]


def create_output_tracker_param_set(
    loader: str,
    vector_store: str,
    llm: str,
    embedding_model: str,
    similarity_top_k: int,
    chunking_config: str,
    git_user: Optional[str],
    git_repo: Optional[str],
    git_branch: Optional[str],
    directory_git_filter: Optional[OutputTrackerGitFilter] = None,
    file_ext_git_filter: Optional[OutputTrackerGitFilter] = None,
) -> OutputTrackerParamSet:
    """Constructor for the `OutputTrackerParamSet` TypedDict.

    Parameters
    ----------
    loader : str
        The data loader used for the run.
    vector_store : str
        The vector store used for the run.
    llm : str
        The LLM name used for the run.
    embedding_model : str
        The embedding model used for the run.
    similarity_top_k : int
        The similarity top k value used for the run.
    chunking_config : str
        The chunking strategy used for the run.
    git_user : Optional[str]
        The user who owns the github repository included in the document ingestion for the run (if applicable).
    git_repo : Optional[str]
        The github repository included in the document ingestion for the run (if applicable).
    git_branch : Optional[str]
        The github repository branch indexed during the document ingestion for the run (if applicable).
    directory_git_filter : Optional[OutputTrackerGitFilter], optional
        The directory filter used for indexing the github repository (if applicable).
    file_ext_git_filter : Optional[OutputTrackerGitFilter], optional
        The file extension filter used for indexing the github repository (if applicable).

    Returns
    -------
    OutputTrackerParamSet
    """
    return_data: OutputTrackerParamSet = {
        "loader": loader,
        "vector_store": vector_store,
        "llm": llm,
        "embedding_model": embedding_model,
        "similarity_top_k": similarity_top_k,
        "chunking_config": chunking_config,
        "git_user": git_user,
        "git_repo": git_repo,
        "git_branch": git_branch,
        "directory_git_filter": directory_git_filter,
        "file_ext_git_filter": file_ext_git_filter,
    }
    return return_data


class OutputTrackerRunsEntry(TypedDict):
    """Specific file data under a parameter set.

    Attributes
    ----------
    index : int
        The index for the run (the index represents the run number for that specific domain parameter set).
    timestamp : str
        The timestamp for the run.
    txt_file : str
        File path to the raw output dump text file.
    json_file : str
        File path to the JSON output file.
    source_node_file : str
        File path to the source node text file.
    elapsed_time : float
        The elapsed time (in seconds) for how long the domain generation took.
    version : str
        The version of the bcorag tool used.
    """

    index: int
    timestamp: str
    txt_file: str
    json_file: str
    source_node_file: str
    elapsed_time: float
    version: str


def create_output_tracker_runs_entry(
    index: int,
    timestamp: str,
    txt_file: str,
    json_file: str,
    source_node_file: str,
    elapsed_time: float,
    version: str = __version__,
) -> OutputTrackerRunsEntry:
    """Constructor for the `OutputTrackerRunsEntry` TypedDict.

    Parameters
    ----------
    index : int
        The index for the run (the index represents the run number for that specific domain parameter set).
    timestamp : str
        The timestamp for the run.
    txt_file : str
        File path to the raw output dump text file.
    json_file : str
        File path to the JSON output file.
    source_node_file : str
        File path to the source node text file.
    elapsed_time : float
        The elapsed time (in seconds) for how long the domain generation took.
    version : str, optional
        The version of the `bcorag` tool used.
    """
    return_data: OutputTrackerRunsEntry = {
        "index": index,
        "timestamp": timestamp,
        "txt_file": txt_file,
        "json_file": json_file,
        "source_node_file": source_node_file,
        "elapsed_time": elapsed_time,
        "version": version,
    }
    return return_data


class OutputTrackerEntry(TypedDict):
    """Entry in the output map under a specific domain hash string.

    Attributes
    ----------
    curr_index : int
        The most recent run index.
    params : OutputTrackerParamSet
        The parameter set for the run.
    runs : list[OutputTrackerRunsEntry]
        The list of runs for this parameter set.
    """

    curr_index: int
    params: OutputTrackerParamSet
    runs: list[OutputTrackerRunsEntry]


def create_output_tracker_entry(
    curr_index: int, params: OutputTrackerParamSet, runs: list[OutputTrackerRunsEntry]
) -> OutputTrackerEntry:
    """Constructor for the `OutputTrackerEntry` TypedDict.

    Parameters
    ----------
    curr_index : int
        The most recent run index.
    params : OutputTrackerParamSet
        The parameter set for the run.
    runs : list[OutputTrackerRunsEntry]
        The list of runs for this parameter set.

    Returns
    -------
    OutputTrackerEntry
    """
    return_data: OutputTrackerEntry = {
        "curr_index": curr_index,
        "params": params,
        "runs": runs,
    }
    return return_data


class OutputTrackerDomainEntry(TypedDict):
    """Entry for a specific domain.

    *Note*: this isn't the most ideal way to do this. Ideally
    the hash string itself for the parameter set would be the
    key instead of forcing the OutputTrackerDomainField to be
    kept as a list of objects. However, there doesn't seem to
    be a good way to do this in a pythonic way while enforcing
    type safety with static type checkers. As they currently
    exist, TypedDict's require all keys are specified at the
    time of creating the definition. I would rather not specify
    regular dictionaries with extensive and verbose type annotations
    and I expect these map output files are likely to be small enough
    that serious linear runtime complexity won't cause issues.

    Attributes
    ----------
    hash_str : str
        The hash of the parameter set used for run collision identification.
    entries : OutputTrackerEntry
        The run objects.
    """

    hash_str: str
    entries: OutputTrackerEntry


def create_output_tracker_domain_entry(
    hash_str: str, entries: OutputTrackerEntry
) -> OutputTrackerDomainEntry:
    """Constructor for the `OutputTrackerDomainEntry` TypedDict.

    Parameters
    ----------
    hash_str : str
        The hash of the parameter set used for run collision identification.
    entries : OutputTrackerEntry
        The run objects.

    Returns
    -------
    OutputTrackerDomainEntry
    """
    return_data: OutputTrackerDomainEntry = {"hash_str": hash_str, "entries": entries}
    return return_data


class OutputTrackerFile(TypedDict):
    """Top level schema for the output file.

    Attributes
    ----------
    usability : list[OutputTrackerDomainEntry]
        The output map for the usability domain.
    io : list[OutputTrackerDomainEntry]
        The output map for the io domain.
    description : list[OutputTrackerDomainEntry]
        The output map for the description domain.
    execution : list[OutputTrackerDomainEntry]
        The output map for the execution domain.
    parametric : list[OutputTrackerDomainEntry]
        The output map for the parametric domain.
    error : list[OutputTrackerDomainEntry]
        The output map for the error domain.
    """

    usability: list[OutputTrackerDomainEntry]
    io: list[OutputTrackerDomainEntry]
    description: list[OutputTrackerDomainEntry]
    execution: list[OutputTrackerDomainEntry]
    parametric: list[OutputTrackerDomainEntry]
    error: list[OutputTrackerDomainEntry]


def default_output_tracker_file() -> OutputTrackerFile:
    """Creates an empty, default output tracker file instance.

    Returns
    -------
    OutputTrackerFile
    """
    return_data: OutputTrackerFile = {
        "usability": [],
        "io": [],
        "description": [],
        "execution": [],
        "parametric": [],
        "error": [],
    }
    return return_data
