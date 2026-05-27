# MCP Service Layer

A Model Context Protocol (MCP) intermediary service that intelligently routes user queries through an AI-powered decision system, retrieves external information when needed, and generates contextually-aware responses using LLM.

## Overview

This service acts as an intelligent middleware layer between clients and language models. It analyzes incoming queries to determine if external knowledge is required, retrieves relevant information from multiple sources, and generates enhanced responses with proper context.

## Features

- **Intelligent Query Analysis**: Automatically determines if a query requires external information
- **Multi-Source Retrieval**: Fetches data from multiple sources including:
  - Web search (DuckDuckGo)
  - Academic papers (arXiv)
  - Wikipedia
  - Tavily Search API
- **Context-Aware Responses**: Enhances LLM responses with retrieved external information
- **RESTful API**: Simple FastAPI-based interface
- **Async Architecture**: Non-blocking I/O for efficient retrieval operations

## Architecture

```
User Query → Analyzer → [Need External Info?]
                              ↓
                         Retrievers (Web, arXiv, Wikipedia, Tavily)
                              ↓
                         LLM Request (with context)
                              ↓
                         Response to User
```

## Installation

### Prerequisites

- Python 3.8+
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/andreaskhachikyan-ops/mcp.git
cd mcp
```

2. Install dependencies:
```bash
pip install fastapi uvicorn pydantic groq httpx arxiv wikipedia-api
```

3. Configure API keys in your environment or update the following files:
   - `LLMRequest.py`: Set your Groq API key
   - `retrievers.py`: Set your Tavily API key (if using Tavily retriever)

## Usage

### Starting the Server

Run the FastAPI server:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Making Requests

**Endpoint:** `POST /ask`

**Request Body:**
```json
{
  "query": "What is the latest news about quantum computing?"
}
```

**Response:**
```json
{
  "response": "Received query: [LLM generated response with context]",
  "context_used": true
}
```

### Example with cURL

```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"query": "Explain quantum entanglement"}'
```

### Example with Python

```python
import requests

response = requests.post(
    "http://localhost:8000/ask",
    json={"query": "What are the latest developments in AI?"}
)

result = response.json()
print(result["response"])
print(f"External context used: {result['context_used']}")
```

## Project Structure

```
mcp/
├── main.py                 # FastAPI application entry point
├── requestHandler.py       # Main request processing logic
├── analyzer.py            # Query analysis module
├── LLMRequest.py          # LLM communication layer
├── Dto.py                 # Data transfer objects (Pydantic models)
├── retrieval/
│   ├── __init__.py        # Retrieval orchestration
│   ├── base.py            # Base retriever interface
│   └── retrievers.py      # Concrete retriever implementations
└── README.md
```

## Components

### Query Analyzer
Determines whether a query requires external information by:
- Checking if the question needs real-time data
- Identifying if factual verification is required
- Assessing if the query is beyond general knowledge
- Generating optimized search queries for retrieval

### Retrievers
Multiple retrieval sources work in parallel:
- **WebRetriever**: General web search via DuckDuckGo
- **ArXivRetriever**: Academic papers and research
- **WikipediaRetriever**: Encyclopedia articles
- **TavilyRetriever**: Advanced search API

### LLM Integration
Uses Groq's API with the `kimi-k2-instruct` model for:
- Query analysis
- Response generation with retrieved context

## Configuration

### Environment Variables (Recommended)

Instead of hardcoding API keys, use environment variables:

```python
# LLMRequest.py
import os
api_key = os.getenv("GROQ_API_KEY")

# retrievers.py
api_key = os.getenv("TAVILY_API_KEY")
```

Set them in your environment:
```bash
export GROQ_API_KEY="your_groq_api_key"
export TAVILY_API_KEY="your_tavily_api_key"
```

## Development

### Running Tests

```bash
# Add your test commands here
pytest tests/
```

### Code Style

This project follows PEP 8 style guidelines. Format code using:

```bash
black .
flake8 .
```

## Limitations

- API rate limits depend on your Groq and Tavily subscription tiers
- WebRetriever uses simple HTML parsing and may be fragile
- Maximum token limit set to 80 in LLM requests (configurable)

## Future Enhancements
Lightweight Local Model for Query Analysis

Currently, the service uses the same high-capability Groq model for both:

Query analysis/routing
Final response generation

A more efficient architecture would separate these responsibilities by introducing a lightweight local model for the analysis stage.
