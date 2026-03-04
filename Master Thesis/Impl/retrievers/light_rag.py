import time

import requests
from openai import OpenAI

from .base import BaseRetriever, RAGResult, RetrievalResult

# LightRAG REST API (run via: docker compose up lightrag)
# POST /query  body: {"query": "...", "mode": "hybrid"}
# Response:    {"response": "..."}
#
# LightRAG does not return source chunks in its default API response,
# so chunks = [] and recall@k / faithfulness / groundedness will be None.
# This is a known limitation of the current LightRAG REST interface.


class LightRAGRetriever(BaseRetriever):
    def __init__(
        self,
        lightrag_api_url: str,
        mode: str = "hybrid",
    ):
        self.url = lightrag_api_url.rstrip("/")
        self.mode = mode

    def query(self, query: str, k: int = 5) -> RAGResult:
        t0 = time.perf_counter()

        resp = requests.post(
            f"{self.url}/query",
            json={"query": query, "mode": self.mode},
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        answer = data.get("response", "")
        total_ms = (time.perf_counter() - t0) * 1000

        return RAGResult(
            retrieval=RetrievalResult(chunks=[], scores=[], latency_ms=total_ms),
            answer=answer,
            total_latency_ms=total_ms,
        )
