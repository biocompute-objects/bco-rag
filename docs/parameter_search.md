# Parameter Search

- [Search Space](#search-space)
- [Grid Search](#grid-search)
- [Random Search](#random-search)

---

If wanting to test multiple parameter sets and/or papers, the BcoRag tool has an accompanying wrapper tool that implements a similar concept to hyperparameter tuning, offering grid and random parameter set search capabilities.

## Search Space

The parameter search tool uses a custom data type called a `SearchSpace`, which is defined as such:

```python
class SearchSpace(TypedDict):
    """Search space used for parameter searches."""

    filenames: list[str]
    loader: list[str]
    chunking_config: list[str]
    embedding_model: list[str]
    vector_store: list[str]
    similarity_top_k: list[str]
    llm: list[str]
    git_data: Optional[list[GitDataFileConfig]]
```

The `SearchSpace` type has a corresponding initialization function to help with creating a search space. The `init_search_space` function is defined as such:

```python
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
    # initialization function
```

## Grid Search

A grid search can be run from the `main.py` entrypoint using the `grid-search` positional argument like so: 

```bash
(env) python main.py grid-search
```

This will run a grid search with the default parameter search space defined in the `_create_search_space` function.

## Random Search

A random search can be run from the `main.py` entrypoint using the `random-search` positional argument like so:

```bash
(env) python main.py random-search
```

This will run a random search with the default parameter search space defined in the `_create_search_space` function using a parameter subset value of `5`.
