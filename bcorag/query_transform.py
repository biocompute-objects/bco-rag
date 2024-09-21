from llama_index.core.indices.query.query_transform.base import BaseQueryTransform
from llama_index.core.schema import QueryBundle
from llama_index.core.prompts.mixin import PromptMixinType, PromptDictType


class CustomQueryTransform(BaseQueryTransform):

    def __init__(self, delimiter: str):
        self.delimiter = delimiter

    def _run(self, query_bundle: QueryBundle, metadata: dict) -> QueryBundle:
        retrieval_query = query_bundle.query_str
        if self.delimiter in retrieval_query:
            retrieval_query = retrieval_query.split(self.delimiter)[0].strip()
        new_query_bundle = QueryBundle(
            query_str=retrieval_query,
            custom_embedding_strs=query_bundle.custom_embedding_strs,
            embedding=query_bundle.embedding,
        )
        return new_query_bundle

    def _get_prompts(self) -> PromptDictType:
        return {}

    def _get_prompt_modules(self) -> PromptMixinType:
        return {}

    def _update_prompts(self, prompts_dict: PromptDictType) -> None:
        """Update prompts."""
