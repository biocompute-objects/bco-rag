# In-Progress Report Documentation

The BCO standard describes comprehensive documentation on the complete specifications of a bioinformatics workflow. Unfortunately, this makes it difficult to create BCOs while work is still in progress. If a full paper describing the complete workflow for the project has not yet been completed, the `in-progress` mode can be used to create in progress documentation using the `Aggregator` tool. The `Aggregator` tool leverages the OpenAI `gpt-4o-mini` model to generate a plain text summary that follows a similar structure to the domains of a BioCompute Object (BCO). 

The in progress documentation aggregator can be run from the `main.py` entrypoint using the `in-progress` positional argument and the `--path` option. The available options for the in progress mode are as follows:

- `--path`: The path to the directory to process (required).
- `--include`: Comma delimited list of glob patterns to include (optional).
- `--exclude`: Comma delimited list of glob patterns to exclude (optional).
- `--exclude-from-tree`: Whether to exclude non-included files in the source tree (optional, store true argument).
- `--include-priority`: Whether to prioritize include or exclude patterns in the case of conflict (optional, store false argument).

Here's an example output from the `Aggregator` tool when run on this project:

> # BioCompute Object Documentation for the BCO-RAG Project
> 
> ## Usability Domain
> The BCO-RAG project aims to provide an automated assistant for generating BioCompute Objects (BCOs) from existing biological research publications. This tool allows researchers to easily convert their publications into a standardized format, thus enhancing reproducibility and transparency in biological data analysis workflows. The primary use case is to reduce the overhead of retroactively documenting existing workflows used in research, making it easier for users to adhere to BCO standards while leveraging advanced language models for generation.
> 
> ## IO Domain
> ### Input Files:
> - High resolution measurement PDF file located in `bco-rag/test_papers/High resolution measurement.pdf`.
> 
> ### Output Files:
> - Output directory structure will be created under `output/high_resolution_measurement/` containing:
>   - `generated_domains/` subdirectory with generated domain files.
>       - JSON and TXT files for each domain generated (e.g., `usability-1-{hash}.json`, `io-1-{hash}.txt`).
>   - `reference_sources/` subdirectory for tracking source references.
>   - `output_map.json` and `output_map.tsv` files that track generated domains and parameter sets.
> 
> ## Description Domain
> ### Keywords:
> - BCO-RAG, BioCompute Object, automation, reproducibility, biological data analysis, retrieval-augmented generation, documentation standardization.
> 
> ### Workflow Steps:
> 1. **Load the PDF**: Use PDF or directory reader to ingest the publication.
> 2. **Generate Domain**: Execute `perform_query` for each BCO domain including usability, IO, description, execution, parametric, and error domains.
> 3. **Store Outputs**: Save generated outputs to the specified output directory.
> 4. **Log Data**: Keep track of input/output files and their relationships in `output_map.json`.
> 
> ## Execution Domain
> The BCO-RAG requires the following setup for execution:
> - **Dependencies**: Users must have Python 3.10 or higher installed.
> - **Required Packages**: Install dependencies specified in `requirements.txt` using `pip install -r requirements.txt`.
> - **Environment Configuration**: 
>    - Set the OpenAI API key in a `.env` file.
>    - Set the Github personal access token if using Github options.
> 
> ### Run Instructions:
> - Run the main script with:
>   ```bash
>   python main.py one-shot
>   ```
> - For in-progress documentation:
>   ```bash
>   python main.py in-progress --path <directory_path>
>   ```
> 
> ## Parametric Domain
> The following parameters affect the computational workflow:
> - **loader** (str): Data loader used (e.g., `PDFReader`).
> - **chunking_config** (str): Configuration for chunking strategy (e.g., `1024 chunk size/20 chunk overlap`).
> - **embedding_model** (str): Model used for embeddings (e.g., `text-embedding-3-large`).
> - **vector_store** (str): Name of the vector store used (e.g., `VectorStoreIndex`).
> - **similarity_top_k** (int): Number of top entries to retrieve during similarity search.
> - **llm** (str): Language model choice (e.g., `gpt-4-turbo`).
> - **git_data** (Optional[GitData]): Includes repository info if GitHub is used.
> 
> ### Examples of Parameters:
> - Sample settings might include: LLM as `gpt-4`, embedding model as `text-embedding-3-large`, similarity_top_k as `3`, etc.
> 
> ## Error Domain
> The project tracks potential errors in the generated domains:
> - **Inferred Knowledge Errors**: Errors related to information that require inference based on external conditions not stated in the source material.
> - **External Knowledge Errors**: Errors arising from insufficient context provided for the domain's connections to external references.
> - **JSON Formatting Errors**: Issues arising if the generated output is not valid JSON.
> - **Miscellaneous Errors**: Any other discrepancies consistently tracked for documentation purposes. 
> 
> ### Evaluation:
> For each output generated, the tool logs potential errors and evaluations of the output quality, ensuring that all relevant data is captured in the final documentation.
> 
> ### Overall Functionality:
> The BCO-RAG project automates the generation of a structured and standardized representation of computational research workflows, significantly aiding in data sharing and reproducibility within the biological research community.
