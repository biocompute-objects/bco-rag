# Parameter Search

- [Search Space]()
- [Grid Search]()
- [Random Search]()

---

If wanting to test multiple parameter sets and/or papers, the BcoRag tool has an accompanying wrapper tool that implements a similar concept to hyperparameter tuning, offering parameter set grid and random searches.

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
