# Automated Testing

The `test_bco_rag.py` script contains a suite of tests designed to evaluate the functionality of the BcoRag tool using the `pytest` framework and the open source LLM evaluation framework [DeepEval](https://docs.confident-ai.com/).

## Test Cases

There is one test case for each domain:

- `test_usability`
- `test_io`
- `test_description`
- `test_execution`
- `test_parametric`
- `test_error`

## Test Metrics

The test suite evaluates two different metrics:

**Answer Relevancy**:

The answer relevancy metric is used to evaluate how relevant the finalized generated output (in our case, the generated domain) is to the original input prompt. It attempts to evaluate relevancy (does the generated content directly relate to the question at hand), appropriateness (is the content appropriate given the context of the input) and focus (does the content stay on topic).

> The answer relevancy metric measures the quality of your RAG pipeline's generator by evaluating how relevant the `actual_output` of your LLM application is compared to the provided input.

- Source: https://docs.confident-ai.com/docs/metrics-answer-relevancy

**Faithfulness**:

The faithfulness metric assesses how accurate and truthful the finalized generated output (in our case, the generated domain) is concerning the source material (the retrieved content). It attempts to ensure that the content is relevant, factual, and does not contradict the information gathered from the retrieval step.

> The faithfulness metric measures the quality of your RAG pipeline's generator by evaluating whether the `actual_output` factually aligns with the contents of your `retrieval_context`.

- Source: https://docs.confident-ai.com/docs/metrics-faithfulness

## Running The Tests

It is not recommended to run all the tests at once. The test suite uses `gpt-4o` in the backend to evaluate the above metrics.

To run one test at a time:

`deepeval test run test_bco_rag.py::test_{domain}`

To run all the tests at once:

`deepeval test run test_bco_rag.py`
