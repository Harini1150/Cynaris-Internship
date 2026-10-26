
import os
from groq import Groq


def generate_executive_summary(insights):
    """Generate an evidence-based executive summary from five EDA insights."""

    if len(insights) != 5:
        raise ValueError("Please provide exactly five EDA insights.")

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is missing. Set it in the PowerShell "
            "terminal used to launch Streamlit."
        )

    client = Groq(api_key=api_key)

    prompt = f"""
You are a senior business data analyst writing for business leaders.

Write an executive summary of approximately 200 words based only
on the five EDA insights below.

Explain:
1. The key findings.
2. Their possible business implications.
3. Data-quality risks.
4. Practical next steps.

Do not invent facts, numbers, causes, or relationships.
Clearly distinguish observed findings from possible implications.
Use professional language and short paragraphs.

EDA INSIGHTS:
{chr(10).join(f"- {insight}" for insight in insights)}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful business data analyst. "
                    "Use only the supplied evidence and never invent facts."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        max_completion_tokens=1000,
        reasoning_effort="low",
    )

    summary = response.choices[0].message.content

    if not summary or not summary.strip():
        raise RuntimeError(
            "Groq returned an empty executive summary. Please try again."
        )

    return summary.strip()
