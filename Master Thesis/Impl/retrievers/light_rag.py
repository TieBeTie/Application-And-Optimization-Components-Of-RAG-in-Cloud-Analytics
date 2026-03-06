import time

import requests

from .base import BaseRetriever, RAGResult, RetrievalResult


class LightRAGRetriever(BaseRetriever):
    def __init__(self, lightrag_api_url: str, mode: str = "hybrid"):
        self.url = lightrag_api_url.rstrip("/")
        self.mode = mode

    def query(self, query: str, k: int = 5) -> RAGResult:
        t0 = time.perf_counter()

        resp = requests.post(
            f"{self.url}/query",
            json={
                "query": query,
                "mode": self.mode,
                "include_references": True,
                "include_chunk_content": True,
                "top_k": k,
            },
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()

        answer = data.get("response", "")
        chunks = [
            chunk
            for ref in data.get("references", [])
            for chunk in ref.get("content", [])
        ]
        total_ms = (time.perf_counter() - t0) * 1000

        return RAGResult(
            retrieval=RetrievalResult(chunks=chunks, scores=[], latency_ms=total_ms),
            answer=answer,
            total_latency_ms=total_ms,
        )
