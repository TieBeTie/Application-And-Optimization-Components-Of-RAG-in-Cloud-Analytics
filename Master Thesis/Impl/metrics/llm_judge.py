import json
import statistics

from openai import OpenAI

_SYSTEM = (
    "You are an expert evaluator. Evaluate the given answer strictly and objectively."
)

_PROMPT = """\
Evaluate the following answer to the question on four criteria. Score each from 1 to 10.

Criteria:
- Comprehensiveness: does the answer cover all aspects of the question?
- Empowerment: does the answer help the reader make informed judgments?
- Diversity: does the answer provide varied perspectives and insights?
- Overall: combined quality across all criteria.

Question: {query}

Answer: {answer}

Output ONLY valid JSON, no extra text:
{{
    "Comprehensiveness": {{"score": <int>}},
    "Empowerment": {{"score": <int>}},
    "Diversity": {{"score": <int>}},
    "Overall": {{"score": <int>}}
}}\
"""

_KEYS = ("Comprehensiveness", "Empowerment", "Diversity", "Overall")


def _parse(content: str) -> dict[str, float] | None:
    try:
        text = content.strip()
        if text.startswith("```"):
            text = "\n".join(text.split("\n")[1:-1])
        parsed = json.loads(text)
        return {k: float(parsed[k]["score"]) for k in _KEYS if k in parsed}
    except Exception:
        return None


def judge(query: str, answer: str, client: OpenAI, model: str, n_runs: int = 5) -> dict[str, float]:
    runs: list[dict[str, float]] = []
    for _ in range(n_runs):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": _SYSTEM},
                    {"role": "user", "content": _PROMPT.format(query=query, answer=answer)},
                ],
                temperature=0.0,
            )
            result = _parse(resp.choices[0].message.content)
            if result:
                runs.append(result)
        except Exception:
            continue

    if not runs:
        return {}
    return {k: round(statistics.mean(r[k] for r in runs if k in r), 3) for k in _KEYS}
