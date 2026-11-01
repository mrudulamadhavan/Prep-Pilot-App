class SessionManager:

    def __init__(self):
        self.history = []

    def add_evaluation(
        self,
        question: str,
        answer: str,
        tool_results: dict,
        feedback: str
    ):

        evaluation = {
            "question": question,
            "answer": answer,
            "tool_results": tool_results,
            "feedback": feedback
        }

        self.history.append(evaluation)

    def get_history(self) -> list:
        return self.history

    def get_session_summary(self) -> dict:

        return {
            "questions_answered": len(self.history),
            "history": self.history
        }

    def clear_session(self):
        self.history = []