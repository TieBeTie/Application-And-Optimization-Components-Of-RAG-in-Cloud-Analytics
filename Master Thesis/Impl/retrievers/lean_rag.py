import os
import sys
import time
import pymysql

from .base import BaseRetriever, RAGResult, RetrievalResult

# Absolute path to the LeanRAG package
_LEAN_RAG_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "RAG", "LeanRAG")
)

# Import query_graph with CWD set to LeanRAG dir (config.yaml is read at module level)
_orig_cwd = os.getcwd()
os.chdir(_LEAN_RAG_DIR)
sys.path.insert(0, _LEAN_RAG_DIR)
from dotenv import load_dotenv
load_dotenv(os.path.join(_LEAN_RAG_DIR, ".env"))
from groq_adapter import GroqAdapter, embedding_func
from query_graph import query_graph as _query_graph
os.chdir(_orig_cwd)

_WORKING_DIR = os.path.join(_LEAN_RAG_DIR, "exp", "thesis")
_CHUNKS_FILE = os.path.join(_LEAN_RAG_DIR, "datasets", "thesis", "thesis_chunk.json")


def _extract_text_units(describe: str) -> list[str]:
    """Pull the text_units section out of LeanRAG's describe string."""
    marker = "text_units:"
    idx = describe.find(marker)
    if idx == -1:
        return [describe]
    text_block = describe[idx + len(marker):].strip()
    chunks = [c.strip() for c in text_block.split("\n\n") if c.strip()]
    return chunks if chunks else [text_block]


class LeanRAGRetriever(BaseRetriever):
    def __init__(self):
        self._adapter = GroqAdapter()
        self._db = pymysql.connect(
            host="localhost", user="root", port=4321,
            passwd="123", charset="utf8mb4"
        )
        self._global_config = {
            "chunks_file": _CHUNKS_FILE,
            "embeddings_func": embedding_func,
            "working_dir": _WORKING_DIR,
            "topk": 5,
            "level_mode": 1,
            "use_llm_func": self._adapter.generate_text,
        }

    def query(self, query: str, k: int = 5) -> RAGResult:
        self._global_config["topk"] = k
        t0 = time.perf_counter()

        describe, answer = _query_graph(self._global_config, self._db, query)

        retrieval_ms = (time.perf_counter() - t0) * 1000
        chunks = _extract_text_units(describe)

        return RAGResult(
            retrieval=RetrievalResult(chunks=chunks, scores=[], latency_ms=retrieval_ms),
            answer=answer or "",
            total_latency_ms=retrieval_ms,
        )
