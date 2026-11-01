def generate_final_report(history: list) -> dict:
    """
    Aggregate all interview evaluations into
    one session-level report.
    """

    total_questions = len(history)

    if total_questions == 0:
        return {
            "questions_answered": 0,
            "average_relevance": 0,
            "total_filler_words": 0,
            "star_components": {
                "situation": 0,
                "task": 0,
                "action": 0,
                "result": 0
            },
            "weakest_question": None,
            "weakest_score": 0
        }

    relevance_scores = []
    total_filler_words = 0

    weakest_question = None
    weakest_score = None

    star_components = {
        "situation": 0,
        "task": 0,
        "action": 0,
        "result": 0
    }

    for evaluation in history:

        tool_results = evaluation["tool_results"]

        # -------------------------
        # Relevance
        # -------------------------

        relevance_result = tool_results.get(
            "score_relevance",
            {}
        )

        if "score" in relevance_result:

            score = relevance_result["score"]

            relevance_scores.append(score)

            if (
                weakest_score is None
                or score < weakest_score
            ):
                weakest_score = score
                weakest_question = evaluation["question"]

        # -------------------------
        # Filler Words
        # -------------------------

        filler_result = tool_results.get(
            "detect_filler_words",
            {}
        )

        total_filler_words += filler_result.get(
            "count",
            0
        )

        # -------------------------
        # STAR Structure
        # -------------------------

        star_result = tool_results.get(
            "check_star_structure",
            {}
        )

        for component in star_components:

            if star_result.get(component):
                star_components[component] += 1

    # -------------------------
    # Average Relevance
    # -------------------------

    average_relevance = 0

    if relevance_scores:
        average_relevance = round(
            sum(relevance_scores)
            / len(relevance_scores)
        )

    # If no relevance score was produced
    if weakest_score is None:
        weakest_score = 0

    return {
        "questions_answered": total_questions,
        "average_relevance": average_relevance,
        "total_filler_words": total_filler_words,
        "star_components": star_components,
        "weakest_question": weakest_question,
        "weakest_score": weakest_score
    }