import json

from config import MODEL_NAME
from core.llm import get_client

def generate_coaching_report(
    session_history: list,
    final_report: dict
) -> str:

    prompt = f"""
You are an expert interview coach.

Review the complete interview session below.

SESSION METRICS:
{json.dumps(final_report, indent=2)}

SESSION HISTORY:
{json.dumps(session_history, indent=2)}

Provide a concise overall coaching report.

Include:

1. Overall performance
2. Key strengths
3. Recurring areas for improvement
4. Specific practical recommendations

Be encouraging but honest.
Do not invent weaknesses that are not supported by the
session data.
"""

    response = get_client().chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert interview coach who "
                    "analyses performance across multiple "
                    "interview answers."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content