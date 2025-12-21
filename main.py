from fastapi import FastAPI
from Dto import UserRequest, MCPResponse
from requestHandler import handle_request

app = FastAPI(
    title="MCP Service Layer",
    description="Model Context Protocol intermediary between client and LLM",
    version="0.1.0"
)


@app.post("/ask", response_model=MCPResponse)
async def ask_mcp(request: UserRequest):
    return await handle_request(request)
