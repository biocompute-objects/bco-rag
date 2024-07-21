""" The core logic custom types.

Type Aliases
------------
- ```DomainKey = Literal["usability", "io", "description", "execution", "parametric", "error"]```
- ```OptionKey = Literal[
        "loader",
        "chunking_config",
        "embedding_model",
        "vector_store",
        "similarity_top_k",
        "llm",
        "mode"]```
"""

from typing import TypedDict, Optional, Literal
from enum import Enum
from llama_index.readers.github import GithubRepositoryReader  # type: ignore

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

### Core logic types


class GitFilter(Enum):
    """Enum delineating between the directory and file extension filters.

    Attributes
    ----------
    DIRECTORY : int
        A git directory filter, represented by the value 1.
    FILE_EXTENSION : int
        A file extension filter, represented by the value 2.
    """

    DIRECTORY = 1
    FILE_EXTENSION = 2


class GitFilters(TypedDict):
    """Typed dict for github loader filters.

    Attributes
    ----------
    filter_type : GithubRepositoryReader.FilterType
        The type of github filter (whether it is an include or exclude filter).
    filter : GitFilter
        The filter enum specification.
    value : list[str]
        The values to filter on.
    """

    filter_type: GithubRepositoryReader.FilterType
    filter: GitFilter
    value: list[str]


def create_git_filters(
    filter_type: GithubRepositoryReader.FilterType, filter: GitFilter, value: list[str]
) -> GitFilters:
    """Constructor for the `GitFilters` TypedDict.

    Parameters
    ----------
    filter_type : GithubRepositoryReader.FilterType
        The type of github filter (whether it is an include or exclude filter).
    filter : GitFilter
        The filter enum specification.
    value : list[str]
        The values to filter on.

    Returns
    -------
    GitFilters
    """
    sorted_values = sorted(value)
    return_data: GitFilters = {
        "filter_type": filter_type,
        "filter": filter,
        "value": sorted_values,
    }
    return return_data


class GitData(TypedDict):
    """Typed dict for the optional git repo information.

    Attributes
    ----------
    user : str
        The github repo owner.
    repo : str
        The repo name.
    branch : str
        The repo branch to index.
    filters : list[GitFilters]
        The list of filters to apply.
    """

    user: str
    repo: str
    branch: str
    # TODO : can we refactor this for a tuple?
    filters: list[GitFilters]


def create_git_data(
    user: str, repo: str, branch: str, filters: list[GitFilters] = []
) -> GitData:
    """Constructor for the `GitData` TypedDict.

    Parameters
    ----------
    user : str
        The github repo owner.
    repo : str
        The repo name.
    branch : str
        The repo branch to index.
    filters : list[GitFilters]
        The list of filters to apply.

    Returns
    -------
    GitData
    """
    return_data: GitData = {
        "user": user,
        "repo": repo,
        "branch": branch,
        "filters": filters,
    }
    return return_data


class UserSelections(TypedDict):
    """Types dict for the user selections.

    Attributes
    ----------
    llm : str
        The LLM to use.
    embedding_model : str
        The embedding model to use.
    filename : str
        The file name of the paper being processed.
    filepath : str
        The file path to the paper being processed.
    vector_store : str
        The vector store to use.
    loader : str
        The data loader to ingest the paper with.
    mode : str
        The run mode.
    similarity_top_k : int
        The base integer used to calculate the similarity_top_k and top_n values.
    chunking_config : str
        The chunking configuration to use during node parsing.
    git_data : Optional[GitData]
        The optional github repository information to include in the documents.
    """

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
    """Constructor for the `UserSelections` TypedDict.

    Parameters
    ----------
    llm : str
        The LLM to use.
    embedding_model : str
        The embedding model to use.
    filename : str
        The file name of the paper being processed.
    filepath : str
        The file path to the paper being processed.
    vector_store : str
        The vector store to use.
    loader : str
        The data loader to ingest the paper with.
    mode : str
        The run mode.
    similarity_top_k : int
        The base integer used to calculate the similarity_top_k and top_n values.
    chunking_config : str
        The chunking configuration to use during node parsing.
    git_data : Optional[GitData]
        The optional github repository information to include in the documents.

    Returns
    -------
    UserSelections
    """
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


### Domain map prompting schemas


class IndividualDomainMapEntry(TypedDict):
    """Information for one domain to prompt and process the user domain choice.

    Attributes
    ----------
    prompt : str
        The prompt to use for querying the RAG pipeline for a specific domain generation.
    top_level : bool
        Whether the specified domain includes object's defined in the top level JSON schema.
    user_prompt : str
        The prompt string to display to the user.
    code : str
        The short hand code for choosing the domain.
    """

    prompt: str
    top_level: bool
    user_prompt: str
    code: str


class DomainMap(TypedDict):
    """Domain map for processing user input. Maps the user input for 
    the domain prompt to the prompt to use for querying the RAG pipeline.

    Attributes
    ----------
    usability : IndividualDomainMapEntry
    io: IndividualDomainMapEntry
    description: IndividualDomainMapEntry
    execution: IndividualDomainMapEntry
    parametric: IndividualDomainMapEntry
    error: IndividualDomainMapEntry
    """

    usability: IndividualDomainMapEntry
    io: IndividualDomainMapEntry
    description: IndividualDomainMapEntry
    execution: IndividualDomainMapEntry
    parametric: IndividualDomainMapEntry
    error: IndividualDomainMapEntry


### conf.json schema


class OptionSchema(TypedDict):
    """Schema for a config object option entry in the config JSON file.

    Attributes
    ----------
    list : list[str]
        The list of options to choose from.
    default : str
        The option to use as the default.
    documentation : str
        The link to the documentation for the option.
    """

    list: list[str]
    default: str
    documentation: str


class ConfigObjectOptions(TypedDict):
    """Schema for the supported options.

    Attributes
    ----------
    loader : OptionSchema
    chunking_config : OptionSchema
    embedding_model: OptionSchema
    vector_store: OptionSchema
    similarity_top_k: OptionSchema
    llm: OptionSchema
    mode: OptionSchema
    """

    loader: OptionSchema
    chunking_config: OptionSchema
    embedding_model: OptionSchema
    vector_store: OptionSchema
    similarity_top_k: OptionSchema
    llm: OptionSchema
    mode: OptionSchema


class ConfigObject(TypedDict):
    """Config JSON schema.

    Attributes
    ----------
    paper_directory : str
        The file path to the paper's directory.
    options : ConfigObjectOptions
        The supported configuration options.
    """

    paper_directory: str
    options: ConfigObjectOptions
