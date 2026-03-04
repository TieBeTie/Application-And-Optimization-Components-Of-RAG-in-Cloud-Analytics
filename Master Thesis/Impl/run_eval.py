"""
Run evaluation for one retriever over the query dataset.

Usage:
    python run_eval.py --retriever naive_rag --output results/naive_rag.jsonl
    python run_eval.py --retriever light_rag --output results/light_rag.jsonl

Reads:
    .env               — LLM_JUDGE_API_KEY, RAG_API_URL, LIGHTRAG_API_URL, TOP_K, N_JUDGE_RUNS
    file_ids.json      — {filename: file_id} produced by ingest.py
    datasets/queries.jsonl
"""
import argparse
import json
import os
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from dotenv import load_dotenv
from openai import OpenAI

from metrics.computational_cost import context_tokens
from metrics.faithfulness import faithfulness
from metrics.groundedness import groundedness
from metrics.llm_judge import judge
from metrics.recall import recall_at_k
from retrievers.light_rag import LightRAGRetriever
from retrievers.naive_rag import NaiveRAGRetriever

load_dotenv()

RAG_API_URL = os.getenv("RAG_API_URL", "http://localhost:8000")
LIGHTRAG_API_URL = os.getenv("LIGHTRAG_API_URL", "http://localhost:9621")

RAG_GENERATOR_API_KEY = os.getenv("RAG_GENERATOR_API_KEY")
RAG_GENERATOR_BASE_URL = os.getenv("RAG_GENERATOR_BASE_URL", "https://api.groq.com/openai/v1")
RAG_GENERATOR_MODEL = os.getenv("RAG_GENERATOR_MODEL", "llama-3.3-70b-versatile")

LLM_JUDGE_API_KEY = os.getenv("LLM_JUDGE_API_KEY")
LLM_JUDGE_BASE_URL = os.getenv("LLM_JUDGE_BASE_URL", "https://api.groq.com/openai/v1")
LLM_JUDGE_MODEL = os.getenv("LLM_JUDGE_MODEL", "llama-3.3-70b-versatile")
TOP_K = int(os.getenv("TOP_K", "5"))
N_JUDGE_RUNS = int(os.getenv("N_JUDGE_RUNS", "5"))

RETRIEVERS = {
    "naive_rag": NaiveRAGRetriever,
    "light_rag": LightRAGRetriever,
}


def build_retriever(name: str, gen_client: OpenAI, file_ids: list[str]):
    if name == "naive_rag":
        return NaiveRAGRetriever(
            rag_api_url=RAG_API_URL, file_ids=file_ids, client=gen_client, model=RAG_GENERATOR_MODEL
        )
    if name == "light_rag":
        return LightRAGRetriever(lightrag_api_url=LIGHTRAG_API_URL)
    raise ValueError(f"Unknown retriever: {name}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--retriever", default="naive_rag", choices=list(RETRIEVERS))
    parser.add_argument("--queries", default="datasets/queries.jsonl")
    parser.add_argument("--file-ids", default="file_ids.json")
    parser.add_argument("--output", default=None)
    parser.add_argument("--k", type=int, default=TOP_K)
    parser.add_argument("--n-runs", type=int, default=N_JUDGE_RUNS)
    args = parser.parse_args()

    output = args.output or f"results/{args.retriever}.jsonl"
    Path(output).parent.mkdir(exist_ok=True)

    judge_client = OpenAI(api_key=LLM_JUDGE_API_KEY, base_url=LLM_JUDGE_BASE_URL)
    gen_client = OpenAI(api_key=RAG_GENERATOR_API_KEY, base_url=RAG_GENERATOR_BASE_URL)

    with open(args.file_ids, encoding="utf-8") as f:
        file_ids_data = json.load(f)
    # file_ids.json is {filename: file_id}; retriever needs list of ids
    file_ids = list(file_ids_data.values()) if isinstance(file_ids_data, dict) else file_ids_data

    retriever = build_retriever(args.retriever, gen_client, file_ids)

    with open(args.queries, encoding="utf-8") as f:
        queries = [json.loads(line) for line in f if line.strip()]

    results = []
    for i, item in enumerate(queries):
        query = item["query"]
        anchors = item.get("anchors", [])
        print(f"[{i+1}/{len(queries)}] {query[:70]}")

        try:
            rag = retriever.query(query, k=args.k)
        except Exception as e:
            print(f"  ERROR: {e}")
            continue

        judge_scores = judge(query, rag.answer, judge_client, LLM_JUDGE_MODEL, n_runs=args.n_runs)
        faith = faithfulness(rag.answer, rag.retrieval.chunks, anchors, judge_client, LLM_JUDGE_MODEL, n_runs=args.n_runs)
        gnd = groundedness(rag.answer, rag.retrieval.chunks, judge_client, LLM_JUDGE_MODEL)
        rec = recall_at_k(rag.retrieval.chunks, anchors, k=args.k)
        ctx_tokens = context_tokens(rag.retrieval.chunks)

        result = {
            "id": item.get("id", i),
            "query": query,
            "anchors": anchors,
            "answer": rag.answer,
            "chunks": rag.retrieval.chunks,
            "scores": rag.retrieval.scores,
            "latency_retrieval_ms": round(rag.retrieval.latency_ms, 1),
            "latency_total_ms": round(rag.total_latency_ms, 1),
            "judge": judge_scores,
            "faithfulness": faith,
            "groundedness": gnd,
            "recall_at_k": rec,
            "context_tokens": ctx_tokens,
        }
        results.append(result)

        print(
            f"  Overall={judge_scores.get('Overall', '?')} "
            f"Faith={faith.get('score', '?')} "
            f"Gnd={gnd.get('score', '?')} "
            f"Recall@{args.k}={rec} "
            f"CtxTokens={ctx_tokens} "
            f"Latency={result['latency_total_ms']}ms"
        )

    with open(output, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"\nSaved {len(results)} results -> {output}")


if __name__ == "__main__":
    main()
