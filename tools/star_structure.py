STAR_KEYWORDS = {
    "situation": [
        "situation",
        "when",
        "during",
        "project",
        "problem",
        "issue",
    ],
    "task": [
        "task",
        "responsible",
        "responsibility",
        "needed to",
        "had to",
        "goal",
    ],
    "action": [
        "action",
        "i decided",
        "i implemented",
        "i investigated",
        "i fixed",
        "i worked",
        "i created",
    ],
    "result": [
        "result",
        "as a result",
        "outcome",
        "improved",
        "reduced",
        "increased",
        "resolved",
    ],
}


def check_star_structure(answer: str) -> dict:
    """
    Check whether an answer contains the four
    components of the STAR framework.
    """

    answer = answer.lower()

    result = {}

    for component, keywords in STAR_KEYWORDS.items():
        result[component] = any(
            keyword in answer
            for keyword in keywords
        )

    return result