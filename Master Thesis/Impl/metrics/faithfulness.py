import json

from openai import OpenAI

_PROMPT = """\
You are checking whether an answer is faithful to the retrieved source chunks.

Retrieved chunks:
{chunks}

Answer:
{answer}

Anchors (key facts that must appear in the answer AND be supported by at least one chunk):
{anchors}

For each anchor verify:
1. Is it present (or paraphrased) in the answer?
2. Is it supported by at least one retrieved chunk?

An anchor passes only if BOTH conditions hold.

Output ONLY valid JSON:
{{
    "verified": <number of anchors that pass>,
    "total": <total anchors>,
    "score": <verified / total, float 0-1>
}}\
"""


def faithfulness(
    answer: str,
    chunks: list[str],
    anchors: list[str],
    client: OpenAI,
    model: str,
    n_runs: int = 1,
) -> dict:
    """
    Fraction of anchors that are (a) present or paraphrased in the answer
    AND (b) supported by at least one retrieved chunk.

    n_runs > 1 averages across multiple judge calls (use with temperature > 0
    for genuine variance reduction; at temperature=0 all runs are identical).
    """
    if not anchors:
        return {"verified": 0, "total": 0, "score": None}

    chunks_text = "\n---\n".join(chunks)
    anchors_text = "\n".join(f"- {a}" for a in anchors)
    prompt = _PROMPT.format(chunks=chunks_text, answer=answer, anchors=anchors_text)

    verified_runs = []
    for _ in range(n_runs):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
            )
            text = resp.choices[0].message.content.strip()
            if text.startswith("```"):
                text = "\n".join(text.split("\n")[1:-1])
            result = json.loads(text)
            verified_runs.append(result.get("verified", 0))
        except Exception as e:
            return {"verified": 0, "total": len(anchors), "score": 0.0, "error": str(e)}

    verified = round(sum(verified_runs) / len(verified_runs))
    total = len(anchors)
    return {"verified": verified, "total": total, "score": round(verified / total, 3)}
