import json

from openai import OpenAI

_PROMPT = """\
You are checking whether an answer is grounded in the retrieved source chunks.

Retrieved chunks:
{chunks}

Answer:
{answer}

Instructions:
1. Extract each distinct factual claim from the answer (numbers, dates, names, factual statements).
2. For each claim, check whether it is supported by at least one retrieved chunk.
3. A claim is grounded only if the chunk explicitly contains or directly implies it.

Output ONLY valid JSON:
{{
    "verified": <number of claims supported by at least one chunk>,
    "total": <total number of claims extracted from the answer>,
    "score": <verified / total, float 0-1, or null if total is 0>
}}\
"""


def groundedness(answer: str, chunks: list[str], client: OpenAI, model: str) -> dict:
    """
    Groundedness: fraction of factual claims in the answer that are
    supported by at least one retrieved chunk.

    Complements faithfulness (which validates pre-defined anchors).
    Groundedness audits the answer itself for unsupported claims.
    """
    if not chunks:
        return {"verified": 0, "total": 0, "score": None}

    chunks_text = "\n---\n".join(chunks[:10])

    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": _PROMPT.format(chunks=chunks_text, answer=answer),
                }
            ],
            temperature=0.0,
        )
        text = resp.choices[0].message.content.strip()
        if text.startswith("```"):
            text = "\n".join(text.split("\n")[1:-1])
        return json.loads(text)
    except Exception as e:
        return {"verified": None, "total": None, "score": None, "error": str(e)}
