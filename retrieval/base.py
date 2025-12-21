from abc import ABC, abstractmethod
from typing import List


class RetrievalResult:
    def __init__(self, source: str, content: str):
        self.source = source
        self.content = content

    def __str__(self):
        return f"{self.source}: {self.content}"


class BaseRetriever(ABC):

    @staticmethod
    @abstractmethod
    async def retrieve(query: str) -> List[RetrievalResult]:
        """
        Retrieve external information relevant to the query.
        Must return raw factual content.
        """
        pass
