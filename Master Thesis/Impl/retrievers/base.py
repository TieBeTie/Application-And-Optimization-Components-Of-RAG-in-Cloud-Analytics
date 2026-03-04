from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class RetrievalResult:
    chunks: list[str]
    scores: list[float]
    latency_ms: float


@dataclass
class RAGResult:
    retrieval: RetrievalResult
    answer: str
    total_latency_ms: float
    prompt_tokens: int | None = None  # exact count from resp.usage, None if unavailable


class BaseRetriever(ABC):
    @abstractmethod
    def query(self, query: str, k: int = 5) -> RAGResult:
        ...
