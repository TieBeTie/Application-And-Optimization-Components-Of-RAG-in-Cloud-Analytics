import time

import requests
from openai import OpenAI

from .base import BaseRetriever, RAGResult, RetrievalResult

SYSTEM_PROMPT = "Answer the question based only on the provided context. Be precise and factual."


def _parse_chunks(raw: list) -> tuple[list[str], list[float]]:
    chunks, scores = [], []
    for item in raw:
        if isinstance(item, dict):
            chunks.append(item.get("page_content", ""))
            scores.append(float(item.get("score", 0.0)))
        elif isinstance(item, (list, tuple)) and len(item) == 2:
            doc, score = item
            text = doc.get("page_content", "") if isinstance(doc, dict) else str(doc)
            chunks.append(text)
            scores.append(float(score))
    return chunks, scores


class NaiveRAGRetriever(BaseRetriever):
    def __init__(
        self,
        rag_api_url: str,
        file_ids: list[str],
        client: OpenAI,
        model: str,
    ):
        self.url = rag_api_url.rstrip("/")
        self.file_ids = file_ids
        self.client = client
        self.model = model

    def query(self, query: str, k: int = 5) -> RAGResult:
        t0 = time.perf_counter()

        resp = requests.post(
            f"{self.url}/query_multiple",
            json={"query": query, "file_ids": self.file_ids, "k": k},
            timeout=30,
        )
        resp.raise_for_status()
        chunks, scores = _parse_chunks(resp.json())
        retrieval_ms = (time.perf_counter() - t0) * 1000

        context = "\n\n---\n\n".join(chunks)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": f"{SYSTEM_PROMPT}\n\nContext:\n{context}"},
                {"role": "user", "content": query},
            ],
            temperature=0.0,
        )
        answer = response.choices[0].message.content
        total_ms = (time.perf_counter() - t0) * 1000

        return RAGResult(
            retrieval=RetrievalResult(chunks=chunks, scores=scores, latency_ms=retrieval_ms),
            answer=answer,
            total_latency_ms=total_ms,
        )
