
import os
import json
import re

from groq import Groq


MODEL_NAME = "openai/gpt-oss-20b"


def _get_groq_client():
    """Create a Groq client using the configured API key."""
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is missing. Set it in the PowerShell "
            "terminal used to launch Streamlit."
        )

    return Groq(api_key=api_key)


def _validate_insights(insights):
    """Validate that exactly five EDA insights are provided."""
    if not isinstance(insights, (list, tuple)) or len(insights) != 5:
        raise ValueError("Please provide exactly five EDA insights.")

    if any(
        not isinstance(item, str) or not item.strip()
        for item in insights
    ):
        raise ValueError("Every EDA insight must contain text.")


def generate_executive_summary(insights):
    """Generate an evidence-based executive summary."""
    _validate_insights(insights)
    client = _get_groq_client()

    prompt = f"""
You are a senior business data analyst writing for business leaders.

Write an executive summary of approximately 200 words based only
on the five EDA insights below.

Cover:
1. Key findings.
2. Possible business implications.
3. Data-quality risks.
4. Practical next steps.

Rules:
- Never invent facts, numbers, causes, or relationships.
- Distinguish observed findings from possible implications.
- Do not interpret identifier statistics as business trends.
- Do not claim outliers, skewness, or low variability without
  sufficient statistical evidence.
- Explain that conclusions from small datasets are limited.
- Do not claim that zero missing values or duplicates proves
  the entire dataset is error-free.
- Use professional language and short paragraphs.

EDA INSIGHTS:
{chr(10).join(f"- {insight}" for insight in insights)}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful business data analyst. "
                    "Use only the supplied evidence. Never invent facts "
                    "or present unsupported assumptions as conclusions."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        max_completion_tokens=1200,
        reasoning_effort="low",
    )

    summary = response.choices[0].message.content

    if not summary or not summary.strip():
        raise RuntimeError(
            "Groq returned an empty executive summary. Please try again."
        )

    return summary.strip()


def generate_business_recommendations(insights):
    """Generate five cautious, evidence-based recommendations."""
    _validate_insights(insights)
    client = _get_groq_client()

    prompt = f"""
You are a senior business data analyst preparing recommendations
for an executive report.

DATASET FINDINGS:
{chr(10).join(f"- {insight}" for insight in insights)}

Generate exactly five distinct recommendations as a JSON array
of five strings.

IMPORTANT EVIDENCE RULES:
- Treat findings from small datasets as preliminary.
- A city's frequency does not prove it is the best market.
- Do not assume rows represent customers unless the evidence says so.
- Do not recommend marketing campaigns, loyalty programmes,
  expansion, or sales targets based only on city frequency or
  the difference between mean and median.
- Mean and median alone do not establish low variability,
  outliers, forecast accuracy, or data reliability.
- Zero missing cells and zero duplicates do not guarantee
  overall data quality.
- Do not invent numbers, customer behaviour, causes, or trends.
- Prioritize validation, larger samples, comparisons across cities,
  and useful fields such as transaction date, product category,
  and cost where appropriate.
- Each recommendation must explain a practical next action.
- Clearly identify when further evidence is needed.
- Avoid repeating the same action in different words.

Return only a valid JSON array with exactly five non-empty strings.
Do not include Markdown fences or text outside the JSON.
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a cautious, evidence-based data analyst. "
                    "Never turn a small-sample observation into an "
                    "unsupported business conclusion. Return only "
                    "a JSON array containing exactly five strings."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        max_completion_tokens=1200,
        reasoning_effort="low",
    )

    result = response.choices[0].message.content

    if not result or not result.strip():
        raise RuntimeError(
            "Groq returned empty business recommendations."
        )

    cleaned = result.strip()

    # Remove optional Markdown code fences.
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)

    try:
        recommendations = json.loads(cleaned)
    except json.JSONDecodeError:
        # Recover the JSON array if extra text surrounds it.
        start = cleaned.find("[")
        end = cleaned.rfind("]")

        if start == -1 or end <= start:
            raise RuntimeError(
                "Groq did not return a valid JSON array. Please retry."
            )

        try:
            recommendations = json.loads(cleaned[start:end + 1])
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "Groq returned invalid recommendation data. Please retry."
            ) from exc

    if (
        not isinstance(recommendations, list)
        or len(recommendations) != 5
        or any(
            not isinstance(item, str) or not item.strip()
            for item in recommendations
        )
    ):
        raise RuntimeError(
            "Groq must return exactly five non-empty recommendations. "
            "Please try again."
        )

    return [item.strip() for item in recommendations]
