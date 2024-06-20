# Output Structure

- [Output Directory](#output-directory)
- [Generated Content](#generated-content)
- [Output Maps](#output-maps)

## Output Directory

All output files and sub-directories will be placed within the `output/` directory at the root of this repository. When starting up a run for a PDF file, a new subdirectory will be created with the name of the PDF file. For example, if the file being indexed is named `High resolution measurement.pdf`, the output directory created will be at the path `output/high_resolution_measurement/` (whitespaces replaced with underscores). Within that sub-directory will be two more sub-directories, `generated_domains/` and `reference_sources/`, and two files, `output_map.json` and `output_map.json`.

## Generated Content

Output filenames contain three components:

1. `Domain` - the corresponding BioCompute domain.
2. `Index` - the run number for the domain under that parameter set (used to delineate between hash collisions).
3. `Parameter Set Hash` - used to uniquely identify parameter sets for a run.

The filename formats are as follows:

```
{domain}-{index}-{parameter set hash}.json
{domain}-{index}-{parameter set hash}.txt
```

When generating a domain, the LLM generated domain response will be attempted to be serialized into a valid JSON object. If successful, a JSON file will be created within the `generated_domains/` sub-directory. Whether or not the JSON serialization is successful, the raw response message will be dumped into a text file in the `generated_domains/` sub-directory.

A key component of any RAG pipeline is the retrieval process. In order to accurately capture the state of the tool when generating a domain, we capture the referenced sources that were retrieved based on the standardized domain queries. These are stored in the `referernce_sources/` sub-directory and follow the same filename format as the output text files.

## Output Maps

Along with the generated content output, an `output_map.json` file is generated (or updated) to keep track of the parameter sets for each run. As a convenience for human-readability, the JSON output map is also dumped as a TSV file (however, the TSV file is not used for tracking at all by the code).

### Map Structure

```json
{
  "{domain}": [
    {
      "hash_str": "{parameter set hash}",
      "entries": {
        "curr_index": "{current run index}",
        "params": {
          "loader": "{data loader used}",
          "vector_store": "{vector store used}",
          "llm": "{llm used}",
          "embedding_model": "{embedding model used}",
          "similarity_top_k": "{similarity top k selected}",
          "chunking_config": "{chunking strategy used for node parsing}",
          "git_user": "{github user (or org) that owns the github repo used (if applicable)}",
          "git_repo": "{github repo indexed (if applicable)}",
          "git_branch": "{github branch to index (if applicable)}"
        },
        "runs": [
          {
            "index": "{index for this run}",
            "timestamp": "{timestamp of the run}",
            "txt_file": "{filepath to the raw txt dump}",
            "json_file": "{filepath to the serialized JSON response (if applicable)}",
            "source_node_file": "{filepath to the retrieved nodes file}",
            "version": "{version of the tool that was used}"
          }
        ]
      }
    }
  ]
}
```
