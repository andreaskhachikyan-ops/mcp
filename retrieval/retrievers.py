import httpx
from retrieval.base import BaseRetriever, RetrievalResult
from typing import List
import arxiv
import wikipedia


class WebRetriever(BaseRetriever):
    @staticmethod
    async def retrieve(query: str) -> List[RetrievalResult]:
        url = "https://duckduckgo.com/html/"
        params = {"q": query}

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url, params=params)

        if response.status_code != 200:
            return []

        # Very naive extraction (raw text)
        text = response.text

        # Truncate to avoid massive payloads
        snippet = text[:2000]

        return [
            RetrievalResult(
                source="duckduckgo",
                content=snippet
            )
        ]


class TavilyRetriever(BaseRetriever):
    api_key = "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"
    url = "https://api.tavily.com/search"

    @staticmethod
    async def retrieve(query: str) -> List[RetrievalResult]:
        payload = {
            "api_key": TavilyRetriever.api_key,
            "query": query,
            "search_depth": "basic",
            "include_answer": False
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(TavilyRetriever.url, json=payload)

        if response.status_code != 200:
            return []

        data = response.json()
        return [
            RetrievalResult(
                source="tavily_search",
                content=result["content"]
            ) for result in data.get("results", [])
        ]


class ArXivRetriever(BaseRetriever):
    @staticmethod
    async def retrieve(query: str) -> List[RetrievalResult]:
        search = arxiv.Search(
            query=query,
            max_results=2,
            sort_by=arxiv.SortCriterion.Relevance
        )

        results = []
        for result in search.results():
            content = f"Title: {result.title}\nAuthors: {result.authors}\nAbstract: {result.summary}"
            results.append(RetrievalResult(source="arxiv", content=content))

        return results


class WikipediaRetriever(BaseRetriever):
    @staticmethod
    async def retrieve(query: str) -> List[RetrievalResult]:
        try:
            # Search for the most relevant page titles
            search_results = wikipedia.search(query, results=1)
            if not search_results:
                return []

            # Fetch the summary of the top result
            page = wikipedia.summary(search_results[0], sentences=5)

            return [
                RetrievalResult(
                    source="wikipedia",
                    content=f"Title: {search_results[0]}\n\n{page}"
                )
            ]
        except Exception:
            return []
