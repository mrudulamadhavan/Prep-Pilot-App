import json

from config import MODEL_NAME
from core.llm import get_client

from tools.filler_words import detect_filler_words
from tools.star_structure import check_star_structure
from tools.relevance import score_relevance

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "detect_filler_words",
            "description": "Detect common filler words in a candidate's interview answer.",
            "parameters": {
                "type": "object",
                "properties": {
                    "answer": {
                        "type": "string",
                        "description": "The candidate's answer."
                    }
                },
                "required": ["answer"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_star_structure",
            "description": "Check whether an interview answer contains Situation, Task, Action, and Result components.",
            "parameters": {
                "type": "object",
                "properties": {
                    "answer": {
                        "type": "string",
                        "description": "The candidate's answer."
                    }
                },
                "required": ["answer"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "score_relevance",
            "description": "Score how relevant the candidate's answer is to the interview question using expected keywords.",
            "parameters": {
                "type": "object",
                "properties": {
                    "answer": {
                        "type": "string",
                        "description": "The candidate's answer."
                    },
                    "expected_keywords": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Keywords expected in a relevant answer."
                    }
                },
                "required": [
                    "answer",
                    "expected_keywords"
                ]
            }
        }
    }
]

def evaluate_answer(
    question: str,
    answer: str,
    expected_keywords: list[str]
) -> dict:

    messages = [
        {
            "role": "system",
            "content": """
You are an encouraging interview evaluator.

Evaluate the candidate's answer using the available tools.

Use the available tools to assess:
- filler words
- STAR structure
- relevance

You may call multiple tools. Continue evaluating until you
have enough information.

After all required tool calls are complete, provide short,
encouraging feedback.

Mention:
1. Strengths
2. One area for improvement

Do not make a tool call if you are ready to provide final feedback.
"""
        },
        {
            "role": "user",
            "content": f"""
Interview question:
{question}

Candidate answer:
{answer}

Expected relevance keywords:
{expected_keywords}
"""
        }
    ]

    tool_results = {}

    while True:

        response = get_client().chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=TOOLS
        )

        assistant_message = response.choices[0].message

        messages.append(assistant_message)

        # If there are no more tool calls,
        # the model has finished evaluating.
        if not assistant_message.tool_calls:

            feedback = assistant_message.content

            return {
                "tool_results": tool_results,
                "feedback": feedback
            }

        # Execute every tool requested by the model
        for tool_call in assistant_message.tool_calls:

            function_name = tool_call.function.name

            function_args = json.loads(
                tool_call.function.arguments
            )

            print(f"\nCalling tool: {function_name}")

            if function_name == "detect_filler_words":

                result = detect_filler_words(
                    **function_args
                )

            elif function_name == "check_star_structure":

                result = check_star_structure(
                    **function_args
                )

            elif function_name == "score_relevance":

                result = score_relevance(
                    **function_args
                )

            else:
                result = {
                    "error": "Unknown tool"
                }

            tool_results[function_name] = result

            print(f"Result: {result}")

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                }
            )