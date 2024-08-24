import pytest
from deepeval import assert_test  # type: ignore
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric  # type: ignore
from deepeval.test_case import LLMTestCase  # type: ignore
from bcorag.bcorag import BcoRag
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.readers.github import GithubRepositoryReader  # type: ignore
from bcorag.custom_types.core_types import (
    create_git_data,
    create_user_selections,
    create_git_filters,
    GitFilter,
    GitFilters,
)
from bcorag.prompts import DOMAIN_MAP
from bcorag.misc_functions import extract_repo_data, graceful_exit
import os


@pytest.fixture
def setup_bcorag() -> BcoRag:

    github_url = "https://github.com/dpastling/plethora"
    git_info = extract_repo_data(github_url)
    if git_info is None:
        graceful_exit(1, "Error parsing github URL.")

    git_filters: list[GitFilters] = []

    directory_filter = create_git_filters(
        filter_type=GithubRepositoryReader.FilterType.EXCLUDE,
        filter=GitFilter.DIRECTORY,
        value=["logs", "fastq", "data"],
    )
    file_ext_filter = create_git_filters(
        filter_type=GithubRepositoryReader.FilterType.EXCLUDE,
        filter=GitFilter.FILE_EXTENSION,
        value=[".txt", ".gz", ".bed"],
    )

    git_filters.append(directory_filter)
    git_filters.append(file_ext_filter)
    git_data = create_git_data(
        user=git_info[0], repo=git_info[1], branch="master", filters=git_filters
    )

    user_selection = create_user_selections(
        llm="gpt-4-turbo",
        embedding_model="text-embedding-3-small",
        filename="High resolution measurement.pdf",
        filepath=os.path.join(
            os.path.dirname(__file__),
            "bcorag",
            "test_papers",
            "High resolution measurement.pdf",
        ),
        vector_store="VectorStoreIndex",
        loader="SimpleDirectoryReader",
        mode="debug",
        similarity_top_k=5,
        chunking_config="1024 chunk size/20 chunk overlap",
        git_data=git_data,
        other_docs=None,
    )

    bcorag_instance = BcoRag(user_selections=user_selection)
    return bcorag_instance


def test_answer_relevancy(setup_bcorag):

    domain_key = "usability"
    query_prompt = DOMAIN_MAP[domain_key]["prompt"]
    query_response = setup_bcorag.perform_query(domain_key)

    retrieval_context = [
        "The usability domain describes the scientific use case and purpose of the paper, similar to content in sections like an abstract, background, etc."
    ]

    answer_relevancy_metric = AnswerRelevancyMetric(threshold=0.5)
    faithfulness_metric = FaithfulnessMetric(threshold=0.5)

    test_case = LLMTestCase(
        input=query_prompt,
        actual_output=query_response,
        retrieval_context=retrieval_context,
    )

    assert_test(test_case, [answer_relevancy_metric, faithfulness_metric])
