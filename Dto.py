from pydantic import BaseModel


class UserRequest(BaseModel):
    query: str


class AnalyzedRequest(BaseModel):
    query: str
    reason: str
    time_sensitive: bool
    requires_external_knowledge: bool
    search_query: str


class MCPResponse(BaseModel):
    response: str
    context_used: bool
