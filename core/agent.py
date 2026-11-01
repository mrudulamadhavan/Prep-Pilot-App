import json

from config import MODEL_NAME
from core.llm import get_client

def ask_agent(
    user_question: str,
    session_history: list
) -> str:

    if not session_history:
        return (
            "You have not completed any interview questions yet. "
            "Answer at least one question first, and then I can "
            "give you feedback based on your performance."
        )

    prompt = f"""
You are an AI interview coach.

The candidate is currently in the middle of an interview
practice session.

Use the COMPLETE session history below to answer the
candidate's question.

SESSION HISTORY:
{json.dumps(session_history, indent=2)}

CANDIDATE QUESTION:
{user_question}

Important rules:

- Base your answer only on the session history provided.
- Consider performance across the entire interview so far.
- Do not analyse only the most recent answer.
- Be concise and practical.
- Be encouraging but honest.
- If the candidate asks about their weakest area, identify
  it using evidence from the session history.
"""

    response = get_client().chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful and honest AI interview "
                    "coach. You answer questions about the "
                    "candidate's performance using the complete "
                    "session history."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content