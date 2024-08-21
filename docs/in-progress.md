# In-Progress Report Documentation

The BCO standard describes comprehensive documentation on the complete specifications of a bioinformatics workflow. Unfortunately, this makes it difficult to create BCOs while work is still in progress. If a full paper describing the complete workflow for the project has not yet been completed, the `in-progress` mode can be used to create in progress documentation using the `Aggregator` tool. The `Aggregator` tool leverages the OpenAI `gpt-4o-mini` model to generate a plain text summary that follows a similar structure to the domains of a BioCompute Object (BCO). 

The in progress documentation aggregator can be run from the `main.py` entrypoint using the `in-progress` positional argument and the `--path` option. The available options for the in progress mode are as follows:

- `--path`: The path to the directory to process (required).
- `--include`: Comma delimited list of glob patterns to include (optional).
- `--exclude`: Comma delimited list of glob patterns to exclude (optional).
- `--exclude-from-tree`: Whether to exclude non-included files in the source tree (optional, store true argument).
- `--include-priority`: Whether to prioritize include or exclude patterns in the case of conflict (optional, store false argument).

Here's an example output from the `Aggregator` tool when run on this project:

> ### BioCompute Object (BCO) Documentation Summary for Project `bco-rag`
>
> #### Usability Domain
> The Biocompute Object Retrieval-Augmented Generation Assistant (bco-rag) project aims to automate the process of creating BioCompute Objects (BCOs) from existing research publications. This project addresses the growing need for standardization in the documentation of computational workflows in biological research. By employing large language models (LLMs), bco-rag facilitates the seamless conversion of publications into BCO-compliant formats, thereby enhancing reproducibility and transparency in computational biology.
> 
> #### IO Domain
> **Input Files:**
> - PDF files: Research papers that are indexed for domain generation> .
> 
> **Output Files:**
> - For each domain generated> :
>  - `generated_domains/{domain}-{index}-{parameter set hash}.json`
>  - `generated_domains/{domain}-{index}-{parameter set hash}.txt`
>  - `reference_sources/{domain}-{index}-{parameter set hash}.txt`
>  - `output_map.json`: Maps parameter sets and generated domains.
>  - `output_map.tsv`: Human-readable format of the output map.
>
>#### Description Domain
>- **Keywords:** BCO, BioCompute Objects, automated documentation, computational biology, LLM, reproducibility.
>- **Workflow Steps:**
>  1. Load input paper from specified directory.
>  2. User selects parameters including loader, vector store, and LLM model.
>  3. Create search space for parameter testing.
>  4. Perform query for specific BCO domains (e.g., usability, execution).
>  5. Generate relevant output files and metadata.
>  6. Log results in output map for tracking.
>
>#### Execution Domain
>- **Software Requirements:** Python 3.10 or higher.
>- **Dependencies:**
>  - OpenAI client for LLM interactions.
>  - LLM and vector store libraries (e.g., llama_index).
>- **Installation:**
>  Follow the [Installation and Setup](docs/installation.md) instructions.
>- **Execution:** The project can be started with:
>  ```bash
>  python main.py <mode> --path <directory_path>
>  ```
>  Replacement `<mode>` with options such as `one-shot`, `grid-search`, or `random-search`.
>
>#### Parametric Domain
>- **Parameters:**
>  - `loader`: Type of data reader to use (e.g., PDFReader, SimpleDirectoryReader).
>  - `chunking_config`: Strategy for splitting documents (size and overlap).
>  - `embedding_model`: Specific model version to generate embeddings.
>  - `vector_store`: Choice for database to store vector embeddings.
>  - `similarity_top_k`: Configured top similar documents for retrieval.
>  - Any custom parameters tied to specific workflows can be added as necessary.
>
>#### Error Domain
>The error domain includes validation of generated outputs against expected thresholds. It accounts for:
>- Empirical and algorithmic errors relating to model performance.
>- Statistical confidence levels can be validated based on output data from BCO scores.
>- Tolerance levels for input variations and the maximum acceptable deviations in pipeline executions are to be defined during evaluations.
>
>### Summary
>The `bco-rag` project enables researchers to easily generate, document, and evaluate BCOs from their computational workflows using structured methods combined with modern AI techniques. The various domains of the BioCompute Object provide a comprehensive framework for organizing and validating this research. Detailed documentation and a structured repository of parameters ensure a robust and reproducible research process.
