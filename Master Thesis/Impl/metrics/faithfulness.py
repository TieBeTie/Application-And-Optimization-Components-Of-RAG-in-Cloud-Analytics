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
) -> dict:
    if not anchors:
        return {"verified": 0, "total": 0, "score": None}

    chunks_text = "\n---\n".join(chunks)
    anchors_text = "\n".join(f"- {a}" for a in anchors)

    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": _PROMPT.format(
                        chunks=chunks_text, answer=answer, anchors=anchors_text
                    ),
                }
            ],
            temperature=0.0,
        )
        text = resp.choices[0].message.content.strip()
        if text.startswith("```"):
            text = "\n".join(text.split("\n")[1:-1])
        return json.loads(text)
    except Exception as e:
        return {"verified": 0, "total": len(anchors), "score": 0.0, "error": str(e)}
