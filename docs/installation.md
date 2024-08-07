# Installation and Setup

- [Prerequisites](#prerequisites)
- [Virtual Environment](#virtual-environment)
- [Create Log Directory](#create-log-directory)
- [OpenAI API Key](#openai-api-key)

## Prerequisites

This directory requires at least Python 3.10 to setup. The code in this directory makes extensive use of an alternate way to indicate union type annotations as `X | Y` instead of `Union[X, Y]` from the `Typing` library.

## Clone the repository

First, clone the repository to your machine: 

```bash
git clone git@github.com:biocompute-objects/bco-rag.git
```

This example uses the ssh method, replace with HTTPS URL as needed.

## Virtual Environment

Create a virtual environment from with the `bco-rag/` root directory:

```bash
virtualenv env
```

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

## OpenAI API Key

Create your `.env` file and add your OpenAI API key and Github personal access token (if using Github option). For example:

```.env
OPENAI_API_KEY=<KEY>
GITHUB_TOKEN=<TOKEN>
```

References:  
- [OpenAI API Key](https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key)  
- [Github Personal Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

## Create log Directory

Within the root of the project, create the log directory:

```bash
mkdir logs/
```

## Basic Usage

The base `one-shot` approach can be run like so: 

```bash
(env) python main.py
```

or 

```bash
(env) python main.py one-shot
```
