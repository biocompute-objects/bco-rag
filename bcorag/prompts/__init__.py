from bcorag.custom_types.core_types import DomainMap
from .retrieval import (
    RETRIEVAL_PROMPT,
    USABILITY_DOMAIN_RETRIEVAL,
    IO_DOMAIN_RETRIEVAL,
    DESCRIPTION_DOMAIN_RETRIEVAL,
    EXECUTION_DOMAIN_RETRIEVAL,
    PARAMETRIC_DOMAIN_RETRIEVAL,
    ERROR_DOMAIN_RETRIEVAL,
)
from .llm_prompts import (
    LLM_PROMPT,
    USABILITY_DOMAIN_LLM,
    IO_DOMAIN_LLM,
    DESCRIPTION_DOMAIN_LLM,
    EXECUTION_DOMAIN_LLM,
    PARAMETRIC_DOMAIN_LLM,
    ERROR_DOMAIN_LLM,
    SUPPLEMENT_PROMPT
)

DELIMITER = "|;"

LLM_PROMPT_TEMPLATE = """
Below is some excerpts from a bioinformatics project. The information is from the project's publication and could also contain some information from the project's code repository.

{context_str}

---------\n

{query_str}
"""


PROMPT_DOMAIN_MAP: DomainMap = {
    "usability": {
        "retrieval_prompt": USABILITY_DOMAIN_RETRIEVAL,
        "llm_prompt": USABILITY_DOMAIN_LLM,
        "top_level": False,
        "user_prompt": "[u]sability",
        "code": "u",
        "dependencies": [],
    },
    "io": {
        "retrieval_prompt": IO_DOMAIN_RETRIEVAL,
        "llm_prompt": IO_DOMAIN_LLM,
        "top_level": True,
        "user_prompt": "[i]o",
        "code": "i",
        "dependencies": [],
    },
    "description": {
        "retrieval_prompt": DESCRIPTION_DOMAIN_RETRIEVAL,
        "llm_prompt": DESCRIPTION_DOMAIN_LLM,
        "top_level": True,
        "user_prompt": "[d]escription",
        "code": "d",
        "dependencies": [],
    },
    "execution": {
        "retrieval_prompt": EXECUTION_DOMAIN_RETRIEVAL,
        "llm_prompt": EXECUTION_DOMAIN_LLM,
        "top_level": True,
        "user_prompt": "[e]xecution",
        "code": "e",
        "dependencies": [],
    },
    "parametric": {
        "retrieval_prompt": PARAMETRIC_DOMAIN_RETRIEVAL,
        "llm_prompt": PARAMETRIC_DOMAIN_LLM,
        "top_level": False,
        "user_prompt": "[p]arametric",
        "code": "p",
        "dependencies": ["description"],
    },
    "error": {
        "retrieval_prompt": ERROR_DOMAIN_RETRIEVAL,
        "llm_prompt": ERROR_DOMAIN_LLM,
        "top_level": False,
        "user_prompt": "[err]or",
        "code": "err",
        "dependencies": [],
    },
}
