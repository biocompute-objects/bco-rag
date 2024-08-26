import pytest
from deepeval import assert_test  # type: ignore
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric, BaseMetric, BaseConversationalMetric  # type: ignore
from deepeval.test_case import LLMTestCase  # type: ignore
from bcorag.bcorag import BcoRag
from llama_index.readers.github import GithubRepositoryReader  # type: ignore
from bcorag.custom_types.core_types import (
    create_git_data,
    create_user_selections,
    create_git_filters,
    GitFilter,
    GitFilters,
)
from bcorag.misc_functions import extract_repo_data, graceful_exit
import os

DOMAIN_PARAMS = {
    "usability": {"verbose": True, "async": False},
    "io": {"verbose": True, "async": False},
    "description": {"verbose": True, "async": False},
    "execution": {"verbose": True, "async": False},
    "parametric": {"verbose": True, "async": False},
    "error": {"verbose": True, "async": False},
}
THRESHOLD = 0.9


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


def strip_json_schema(prompt: str) -> str:
    """Strips the JSON schema portion of the prompt.

    Parameters
    ----------
    prompt : str
        The prompt to strip the JSON schema from.

    Returns
    -------
    str
        The cleaned prompt.
    """
    schema_start = prompt.find("The JSON schema is as follows:")
    return prompt[:schema_start]


def create_metrics(
    verbose_mode: bool, async_mode: bool
) -> list[BaseMetric | BaseConversationalMetric]:
    """Creates a BaseMetric list.

    Parameters
    ----------
    verbose_mode : bool
        Whether to create the metrics with verbose mode on.
    async_mode : bool
        Whether to create the metrics with async mode on.

    Returns
    -------
    list[BaseMetric | BaseConversationalMetric]
        The list of metrics.
    """
    answer_relevancy_metric = AnswerRelevancyMetric(
        threshold=THRESHOLD, verbose_mode=verbose_mode, async_mode=async_mode
    )
    faithfulness_metric = FaithfulnessMetric(
        threshold=THRESHOLD, verbose_mode=verbose_mode, async_mode=async_mode
    )
    return [answer_relevancy_metric, faithfulness_metric]


def test_usability(setup_bcorag):

    domain_key = "usability"
    verbose_mode = DOMAIN_PARAMS[domain_key]["verbose"]
    async_mode = DOMAIN_PARAMS[domain_key]["async"]
    setup_bcorag.perform_query(domain_key)

    retrieval_context = [
        node["content"] for node in setup_bcorag.domain_content["last_source_nodes"]
    ]

    metrics = create_metrics(verbose_mode, async_mode)

    test_case = LLMTestCase(
        input=strip_json_schema(setup_bcorag._domain_map[domain_key]["prompt"]),
        actual_output=setup_bcorag.domain_content[domain_key],
        retrieval_context=retrieval_context,
    )

    assert_test(test_case=test_case, run_async=async_mode, metrics=metrics)


def test_io(setup_bcorag):

    domain_key = "io"
    verbose_mode = DOMAIN_PARAMS[domain_key]["verbose"]
    async_mode = DOMAIN_PARAMS[domain_key]["async"]
    setup_bcorag.perform_query(domain_key)

    retrieval_context = [
        node["content"] for node in setup_bcorag.domain_content["last_source_nodes"]
    ]

    metrics = create_metrics(verbose_mode, async_mode)

    test_case = LLMTestCase(
        input=strip_json_schema(setup_bcorag._domain_map[domain_key]["prompt"]),
        actual_output=setup_bcorag.domain_content[domain_key],
        retrieval_context=retrieval_context,
    )

    assert_test(test_case=test_case, run_async=async_mode, metrics=metrics)


def test_description(setup_bcorag):

    domain_key = "description"
    verbose_mode = DOMAIN_PARAMS[domain_key]["verbose"]
    async_mode = DOMAIN_PARAMS[domain_key]["async"]
    setup_bcorag.perform_query(domain_key)

    retrieval_context = [
        node["content"] for node in setup_bcorag.domain_content["last_source_nodes"]
    ]

    metrics = create_metrics(verbose_mode, async_mode)

    test_case = LLMTestCase(
        input=strip_json_schema(setup_bcorag._domain_map[domain_key]["prompt"]),
        actual_output=setup_bcorag.domain_content[domain_key],
        retrieval_context=retrieval_context,
    )

    assert_test(test_case=test_case, run_async=async_mode, metrics=metrics)


def test_execution(setup_bcorag):

    domain_key = "execution"
    verbose_mode = DOMAIN_PARAMS[domain_key]["verbose"]
    async_mode = DOMAIN_PARAMS[domain_key]["async"]
    setup_bcorag.perform_query(domain_key)

    retrieval_context = [
        node["content"] for node in setup_bcorag.domain_content["last_source_nodes"]
    ]

    metrics = create_metrics(verbose_mode, async_mode)

    test_case = LLMTestCase(
        input=strip_json_schema(setup_bcorag._domain_map[domain_key]["prompt"]),
        actual_output=setup_bcorag.domain_content[domain_key],
        retrieval_context=retrieval_context,
    )

    assert_test(test_case=test_case, run_async=async_mode, metrics=metrics)


def test_parametric(setup_bcorag):

    domain_key = "parametric"
    verbose_mode = DOMAIN_PARAMS[domain_key]["verbose"]
    async_mode = DOMAIN_PARAMS[domain_key]["async"]
    setup_bcorag.perform_query(domain_key)

    retrieval_context = [
        node["content"] for node in setup_bcorag.domain_content["last_source_nodes"]
    ]

    metrics = create_metrics(verbose_mode, async_mode)

    test_case = LLMTestCase(
        input=strip_json_schema(setup_bcorag._domain_map[domain_key]["prompt"]),
        actual_output=setup_bcorag.domain_content[domain_key],
        retrieval_context=retrieval_context,
    )

    assert_test(test_case=test_case, run_async=async_mode, metrics=metrics)


def test_error(setup_bcorag):

    domain_key = "error"
    verbose_mode = DOMAIN_PARAMS[domain_key]["verbose"]
    async_mode = DOMAIN_PARAMS[domain_key]["async"]
    setup_bcorag.perform_query(domain_key)

    retrieval_context = [
        node["content"] for node in setup_bcorag.domain_content["last_source_nodes"]
    ]

    metrics = create_metrics(verbose_mode, async_mode)

    test_case = LLMTestCase(
        input=strip_json_schema(setup_bcorag._domain_map[domain_key]["prompt"]),
        actual_output=setup_bcorag.domain_content[domain_key],
        retrieval_context=retrieval_context,
    )

    assert_test(test_case=test_case, run_async=async_mode, metrics=metrics)
