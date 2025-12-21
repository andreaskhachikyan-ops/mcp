import json
from typing import Any
from Dto import AnalyzedRequest
from LLMRequest import request_to_lmm


SYSTEM_PROMPT = """
You are a decision module in a Model Context Protocol (MCP) system.

Your task is NOT to answer the user's question.

Your task is to decide whether the language model requires
additional external information in order to answer the user's request
accurately and reliably.

External information includes:
- real-time or recent data
- factual verification (dates, numbers, current status)
- information outside general world knowledge
- proprietary, local, or user-specific data

The model DOES NOT require external information if:
- the question is conceptual or explanatory
- the answer relies on general knowledge or reasoning
- no factual verification is needed

You must output a JSON object with the following fields ONLY:
- requires_external_information: true or false
- reason: a brief explanation (one sentence)
- search_query: an optimized search string to find the missing information (return an empty string if requires_external_information is false)

Do not answer the user's question.
Do not add any extra text.
"""


def analyze_request(query: str) -> AnalyzedRequest:
    response = request_to_lmm(SYSTEM_PROMPT, query)

    raw_content = response.choices[0].message.content
    data: dict = json.loads(raw_content)

    requires_external = data.get("requires_external_information")
    search_query = data.get("search_query")
    reason = data.get("reason")

    return AnalyzedRequest(
        query=query,
        reason=reason,
        time_sensitive=requires_external,
        requires_external_knowledge=requires_external,
        search_query=search_query
    )
