from LLMRequest import request_to_lmm
from Dto import UserRequest, MCPResponse
from analyzer import analyze_request
from retrieval import retrieve_external_information


async def handle_request(request: UserRequest) -> MCPResponse:
    query = request.query
    analyzed_request = analyze_request(query)
    need_extended_info = analyzed_request.requires_external_knowledge
    request_content = ""

    if need_extended_info:
        search_query = analyzed_request.search_query
        retrieval_results = await retrieve_external_information(search_query)
        request_content = "/n".join([res.__str__() for res in retrieval_results])

    final_response = request_to_lmm(request_content, query)
    response_content = final_response.choices[0].message.content

    return MCPResponse(
        response=f"Received query: {response_content}",
        context_used=need_extended_info
    )
