def score_relevance(
    answer: str,
    expected_keywords: list[str]
) -> dict:
    """
    Score how relevant an answer is based on
    expected keywords.
    """

    answer_lower = answer.lower()

    matched_keywords = []

    for keyword in expected_keywords:
        if keyword.lower() in answer_lower:
            matched_keywords.append(keyword)

    if not expected_keywords:
        score = 0
    else:
        score = (
            len(matched_keywords)
            / len(expected_keywords)
        ) * 100

    return {
        "score": round(score),
        "matched_keywords": matched_keywords,
        "total_expected_keywords": len(expected_keywords)
    }