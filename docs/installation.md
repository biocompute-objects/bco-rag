# Installation and Setup

- [Prerequisites](#prerequisites)
- [Quickstart](#quickstart)
  - [Virtual Environment](#virtual-environment)
  - [Create Log Directory](#create-log-directory)
  - [OpenAI API Key](#openai-api-key)

## Prerequisites

This directory requires at least Python 3.10 to setup. The code in this directory makes extensive use of an [alternate way](https://peps.python.org/pep-0604/) to indicate union type annotations as `X | Y` instead of `Union[X, Y]` from the `Typing` library.

## Quickstart

Getting started with the BCO-RAG assistant requires minimal setup. From a high level, this guide will walk you through:

1. Getting the code on your local machine.
2. Setting up a virtual environment and downloading the project dependencies.
3. Required environment variable(s).
4. Starting up the assistant in its primary usage form.

### Clone the repository

First, clone the repository to your machine:

```bash
git clone git@github.com:biocompute-objects/bco-rag.git
```

This example uses the ssh method, replace with HTTPS URL as needed.

### Virtual Environment

Create a virtual environment from with the `bco-rag/` root directory:

```bash
virtualenv env
```

This example uses [`virtualenv`](https://virtualenv.pypa.io/en/latest/) to create the virtual environment, replace with [`venv`](https://docs.python.org/3/library/venv.html) or your preferred virtual environment handler as needed.

To activate the virtual environment on Windows:

```bash
env/Scripts/activate
```

To activate the virtual environment on MacOS/Linux:

```bash
source env/bin/activate
```

Then install the project dependencies:

```bash
(env) pip install -r requirements.txt
```

### OpenAI API Key

Create your `.env` file and add your OpenAI API key and Github personal access token (if using Github option). For example:

```.env
OPENAI_API_KEY=<KEY>
GITHUB_TOKEN=<TOKEN>
```

If you are not planning on including Github repositories in the data ingestion process, you don't need to include a Github personal access token in your `.env` file.

Additional information on obtaining API keys/tokens:

- [OpenAI API Key](https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key)
- [Github Personal Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

### Create log Directory

Within the root of the project, create the log directory:

```bash
mkdir logs/
```

### Basic Usage

The base `one-shot` approach can be run like so:

```bash
(env) python main.py
```

or

```bash
(env) python main.py one-shot
```

On startup, you will be prompted to choose the paper generate the BCO domains for. You can place any `.pdf` paper in the `./bco-rag/bcorag/test_papers` directory for it to be included in this menu. The arrow keys or `j`/`k` can be used to navigate the menus. Press `Enter` to choose an option.

```
 Please choose the PDF file to index:

 -> High resolution measurement.pdf
    Exit
```

After choosing the paper to index, you'll be prompted for the data loader to use. On any configuration menu step, there will be a link that will direct you to detailed documentation on the differences, strengths, and weaknesses between each of the options.

```
 Please choose one of the following Loaders.
 Documentation can be found at:
 https://biocompute-objects.github.io/bco-rag/options/#data-loader.

 -> SimpleDirectoryReader (default)
    PDFReader
    PDFMarker
    Exit
```

After choosing the data loader, the chunking strategy has to be chosen:

```
 Please choose one of the following Chunking Configs.
 Documentation can be found at:
 https://biocompute-objects.github.io/bco-rag/options/#chunking-strategy.

 -> 256 chunk size/20 chunk overlap
    512 chunk size/50 chunk overlap
    1024 chunk size/20 chunk overlap (default)
    2048 chunk size/50 chunk overlap
    semantic
    Exit
```

After choosing the chunking strategy, the embedding model has to be chosen:

```
 Please choose one of the following Embedding Models.
 Documentation can be found at:
 https://biocompute-objects.github.io/bco-rag/options/#embedding-model.

 -> text-embedding-3-small (default)
    text-embedding-3-large
    text-embedding-ada-002
    Exit
```

After choosing the embedding model, the vector store has to be chosen:

```
 Please choose one of the following Vector Stores.
 Documentation can be found at:
 https://biocompute-objects.github.io/bco-rag/options/#vector-store.

 -> VectorStoreIndex (default)
    Exit
```

After choosing the vector store, the similarity top k value has to be chosen:

```
 Please choose one of the following Similarity Top Ks.
 Documentation can be found at:
 https://biocompute-objects.github.io/bco-rag/options/#similarity-top-k.

 -> 1 (default)
    2
    3
    4
    5
    Exit
```

After choosing the similarity top k value, the LLM has to be chosen:

```
 Please choose one of the following Llms.
 Documentation can be found at:
 https://biocompute-objects.github.io/bco-rag/options/#llm-model.

 -> gpt-3.5-turbo
    gpt-4-turbo (default)
    gpt-4-turbo-preview
    gpt-4
    Exit
```

Next, choose the run mode. The run mode will control the verbosity of the logging for each generated domain. Choosing `debug` mode will include an extensive logging of everything that is happening under the hood during ewach run. Choosing `production` mode will only include the minimum necessary logging, wuch as the user options and return responses.

```
 Please choose one of the following Modes.
 Documentation can be found at:
 https://biocompute-objects.github.io/bco-rag/options/#mode.

 -> debug
    production (default)
    Exit
```

Next, you will be prompted to include a Github repository to include as supplemental knowledge for the retrieval step. In this example, we have pasted the URL to the repository for this project. If you have included a Github repository, you will then be prompted for more granular configuration options regarding how the repository will be ingested. These configuration options include which repository branch to index and optional directory/file extension filters. In this example, we are indexing the repository's `main` branch, excluding the `output/`, `logs/`, `parameter_search/`, `output/`, and `evaluator/` directories. We are also excluding any files with the file extensions of `.txt`, `.log`, and `.md`.

```
If you would like to include a Github repository enter the URL below. Enter "x" to exit or leave blank to skip.
> https://github.com/biocompute-objects/bco-rag
Repo branch to index (case sensitive):
> main
Would you like to include a directory filter?
Enter a list of comma-delimited directories to either conditionally exclude or inclusively include. Or leave blank to skip.
> output, logs, parameter_search, output, evaluator
Enter "include" or "exclude" for the directory filter.
> exclude
Would you like to include a file extension filter?
Enter a list of comma-delimited file extensions to either conditionally exclude or inclusively include. Or leave blank to skip.
> .txt, .log, .md
Enter "include" or "exclude" for the file extension filter.
> exclude
```

More extensive documentation that goes past this quick start guide can be found on the [usage](https://biocompute-objects.github.io/bco-rag/options/) page.

Once the configuration steps are completed, you can select which domains to generate. You can enter the shorthand code, denoted inside the `[]` brackets, or the full domain name and then pressing `Enter`.

```
Which domain would you like to generate? Supported domains are:
    [u]sability
    [i]o
    [d]escription
    [e]xecution
    [p]arametric
    [err]or
    E[x]it

>
```
