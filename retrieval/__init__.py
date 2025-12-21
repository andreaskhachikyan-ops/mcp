from typing import List
from retrieval.retrievers import WebRetriever, WikipediaRetriever, TavilyRetriever, ArXivRetriever
from retrieval.base import RetrievalResult


async def retrieve_external_information(query: str) -> List[RetrievalResult]:
    """

    :rtype: object
    """
    retrievers = [
        WebRetriever(),
        WikipediaRetriever(),
        TavilyRetriever(),
        ArXivRetriever(),
    ]

    results: List[RetrievalResult] = []

    for retriever in retrievers:
        retrieved = await retriever.retrieve(query=query)
        results.extend(retrieved)
        try:
            retrieved = await retriever.retrieve(query)
            results.extend(retrieved)
        except Exception:
            print("Something went wrong...")
            print(retriever)
            continue

    return results
