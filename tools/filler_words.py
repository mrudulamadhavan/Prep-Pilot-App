FILLER_WORDS = [
    "um",
    "uh",
    "like",
    "basically",
    "actually",
]


def detect_filler_words(answer: str) -> dict:
    """
    Detect common filler words in a candidate's answer.
    """

    words = answer.lower().split()

    detected = []

    for word in words:
        cleaned_word = word.strip(".,!?;:")

        if cleaned_word in FILLER_WORDS:
            detected.append(cleaned_word)

    return {
        "count": len(detected),
        "words": detected
    }