from . import __version__
from typing import TypedDict, Optional, Literal

### General literals

DomainKey = Literal[
    "usability", "io", "description", "execution", "parametric", "error"
]

OptionKey = Literal[
    "loader",
    "chunking_config",
    "embedding_model",
    "vector_store",
    "similarity_top_k",
    "llm",
    "mode",
]

### User parameter selection schemas


class GitData(TypedDict):
    """Typed dict for the optional git repo information."""

    user: str
    repo: str
    branch: str


def create_git_data(user: str, repo: str, branch: str) -> GitData:
    """Constructor for the GitData TypedDict."""
    return_data: GitData = {"user": user, "repo": repo, "branch": branch}
    return return_data


class UserSelections(TypedDict):
    """Types dict for the user selections."""

    llm: str
    embedding_model: str
    filename: str
    filepath: str
    vector_store: str
    loader: str
    mode: str
    similarity_top_k: int
    chunking_config: str
    git_data: Optional[GitData]


def create_user_selections(
    llm: str,
    embedding_model: str,
    filename: str,
    filepath: str,
    vector_store: str,
    loader: str,
    mode: str,
    similarity_top_k: int,
    chunking_config: str,
    git_data: Optional[GitData],
) -> UserSelections:
    """Constructor for the UserSelections TypedDict."""
    return_data: UserSelections = {
        "llm": llm,
        "embedding_model": embedding_model,
        "filename": filename,
        "filepath": filepath,
        "vector_store": vector_store,
        "loader": loader,
        "mode": mode,
        "similarity_top_k": similarity_top_k,
        "chunking_config": chunking_config,
        "git_data": git_data,
    }
    return return_data


### Output map file schemas
# Note: TypedDict's technically aren't real types but more like meta-types,
# because of this the constructors have to be separate independent functions
# instead of class methods. From PEP 589: "Methods are not allowed, since the
# runtime type of a TypedDict object will always be just dict (it is never
# a subclass of dict)."


class OutputTrackerParamSet(TypedDict):
    """Parameter set for a run."""

    loader: str
    vector_store: str
    llm: str
    embedding_model: str
    similarity_top_k: int
    chunking_config: str
    git_user: Optional[str]
    git_repo: Optional[str]
    git_branch: Optional[str]


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
) -> OutputTrackerParamSet:
    """Constructor for the OutputTrackerParamSet TypedDict."""
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
    }
    return return_data


class OutputTrackerRunsEntry(TypedDict):
    """Specific file data under a parameter set."""

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
    """Constructor for the OutputTrackerRunsEntry TypedDict."""
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
    """Entry in the output map under a specific domain hash string."""

    curr_index: int
    params: OutputTrackerParamSet
    runs: list[OutputTrackerRunsEntry]


def create_output_tracker_entry(
    curr_index: int, params: OutputTrackerParamSet, runs: list[OutputTrackerRunsEntry]
) -> OutputTrackerEntry:
    """Constructor for the OutputTrackerEntry TypedDict."""
    return_data: OutputTrackerEntry = {
        "curr_index": curr_index,
        "params": params,
        "runs": runs,
    }
    return return_data


class OutputTrackerDomainEntry(TypedDict):
    """Entry for a specific domain.

    Note: this isn't the most ideal way to do this. Ideally
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
    """

    hash_str: str
    entries: OutputTrackerEntry


def create_output_tracker_domain_entry(
    hash_str: str, entries: OutputTrackerEntry
) -> OutputTrackerDomainEntry:
    """Constructor for the OutputTrackerDomainEntry TypedDict."""
    return_data: OutputTrackerDomainEntry = {"hash_str": hash_str, "entries": entries}
    return return_data


class OutputTrackerFile(TypedDict):
    """Schema for the output file."""

    usability: list[OutputTrackerDomainEntry]
    io: list[OutputTrackerDomainEntry]
    description: list[OutputTrackerDomainEntry]
    execution: list[OutputTrackerDomainEntry]
    parametric: list[OutputTrackerDomainEntry]
    error: list[OutputTrackerDomainEntry]


def default_output_tracker_file() -> OutputTrackerFile:
    """Creates an empty, default output tracker file instance."""
    return_data: OutputTrackerFile = {
        "usability": [],
        "io": [],
        "description": [],
        "execution": [],
        "parametric": [],
        "error": [],
    }
    return return_data


### Domain map prompting schemas


class IndividualDomainMapEntry(TypedDict):
    """Entry for an individual domain."""

    prompt: str
    top_level: bool
    user_prompt: str
    code: str


class DomainMap(TypedDict):
    """Domain map for processing user input."""

    usability: IndividualDomainMapEntry
    io: IndividualDomainMapEntry
    description: IndividualDomainMapEntry
    execution: IndividualDomainMapEntry
    parametric: IndividualDomainMapEntry
    error: IndividualDomainMapEntry


### conf.json schema


class OptionSchema(TypedDict):
    """Schema for a config object option entry."""

    list: list[str]
    default: str
    documentation: str


class ConfigObjectOptions(TypedDict):
    """Schema for the options in the config JSON."""

    loader: OptionSchema
    chunking_config: OptionSchema
    embedding_model: OptionSchema
    vector_store: OptionSchema
    similarity_top_k: OptionSchema
    llm: OptionSchema
    mode: OptionSchema


class ConfigObject(TypedDict):
    """Config JSON schema."""

    paper_directory: str
    options: ConfigObjectOptions
