"""
Interview question bank: 50 questions, ordered from Basic to Advanced.

Each question has:
  - level:             "Basic", "Intermediate" or "Advanced"
  - star:              True if the question calls for the STAR method (Situation,
                       Task, Action, Result). False for open questions such as
                       "Tell me about yourself", where STAR is not used.
  - question:          the interview question shown to the candidate
  - expected_keywords: word stems used for relevance scoring. Matching is
                       substring-based, so "investigat" matches "investigated",
                       "investigating", "investigation", etc.
"""

LEVELS = ["Basic", "Intermediate", "Advanced"]


def _q(level, question, keywords, star=True):
    return {
        "level": level,
        "question": question,
        "expected_keywords": keywords,
        "star": star,
    }


INTERVIEW_QUESTIONS = [

    # ==========================================================
    # BASIC (1-15): foundations, teamwork, communication
    # ==========================================================

    _q("Basic",
       "Tell me about yourself and what led you to your current career path.",
       ["experience", "skills", "background", "role", "goal", "passion"],
       star=False),

    _q("Basic",
       "Why do you want to work for this company, and what attracts you to this role?",
       ["company", "role", "values", "skills", "contribute", "growth"],
       star=False),

    _q("Basic",
       "Tell me about a time you had to learn a new skill or tool quickly.",
       ["learn", "tutorial", "practice", "documentation", "applied", "quickly"]),

    _q("Basic",
       "Describe a time you worked successfully as part of a team.",
       ["team", "collaborat", "responsib", "communicat", "goal", "result"]),

    _q("Basic",
       "Tell me about a time you received constructive feedback. How did you respond?",
       ["feedback", "listen", "improv", "applied", "learn", "result"]),

    _q("Basic",
       "How do you prioritize your work when several tasks are due at the same time?",
       ["prioriti", "deadline", "urgent", "impact", "plan", "communicat"],
       star=False),

    _q("Basic",
       "Tell me about a time you helped a colleague who was struggling with their work.",
       ["help", "support", "explain", "colleague", "together", "result"]),

    _q("Basic",
       "Tell me about a time you made a mistake at work. How did you handle it?",
       ["mistake", "identif", "responsib", "correct", "learn", "improv"]),

    _q("Basic",
       "Describe a time you had to explain something technical to a non-technical person.",
       ["explain", "simple", "analogy", "audience", "understand", "clear"]),

    _q("Basic",
       "Tell me about a goal you set for yourself and how you achieved it.",
       ["goal", "plan", "steps", "progress", "achiev", "result"]),

    _q("Basic",
       "Describe a time you had to adapt quickly to a change at work.",
       ["change", "adapt", "flexible", "adjust", "learn", "outcome"]),

    _q("Basic",
       "Tell me about a time you went above and beyond what was expected of you.",
       ["extra", "initiative", "beyond", "impact", "effort", "result"]),

    _q("Basic",
       "Describe a time you took the initiative to start something without being asked.",
       ["initiative", "noticed", "proposed", "started", "owner", "impact"]),

    _q("Basic",
       "Tell me about a time you needed to ask for help. What did you do?",
       ["help", "asked", "stuck", "mentor", "learn", "resolved"]),

    _q("Basic",
       "How do you stay organized and manage your time on a busy day?",
       ["organiz", "schedule", "list", "prioriti", "track", "deadline"],
       star=False),

    # ==========================================================
    # INTERMEDIATE (16-34): ownership, conflict, trade-offs
    # ==========================================================

    _q("Intermediate",
       "Tell me about a time you had to debug a difficult production issue.",
       ["investigat", "logs", "issue", "implement", "fix", "service"]),

    _q("Intermediate",
       "Describe a situation where you disagreed with a teammate. How did you handle it?",
       ["disagree", "listen", "explain", "review", "agree", "solution"]),

    _q("Intermediate",
       "Tell me about a challenging project you worked on. What was your role?",
       ["project", "responsib", "challenge", "implement", "collaborat", "result"]),

    _q("Intermediate",
       "Describe a time you had to manage competing requests from multiple stakeholders.",
       ["stakeholder", "prioriti", "negotiat", "expectation", "communicat", "agreed"]),

    _q("Intermediate",
       "Tell me about a time you improved an existing process or system.",
       ["improv", "process", "identif", "automat", "reduced", "result"]),

    _q("Intermediate",
       "Describe a time you had to work with a difficult coworker.",
       ["difficult", "conversation", "understand", "boundar", "professional", "resolved"]),

    _q("Intermediate",
       "Tell me about a time you met a tight deadline with limited resources.",
       ["deadline", "scope", "prioriti", "resources", "delivered", "trade-off"]),

    _q("Intermediate",
       "Tell me about a code review where you disagreed with the feedback you received.",
       ["review", "feedback", "reason", "discuss", "evidence", "agreed"]),

    _q("Intermediate",
       "Describe a time you caught a serious bug or risk before it reached customers.",
       ["bug", "testing", "caught", "risk", "customer", "prevent"]),

    _q("Intermediate",
       "Tell me about a project that failed or did not meet its goals. What did you learn?",
       ["fail", "cause", "learn", "retrospective", "changed", "improv"]),

    _q("Intermediate",
       "Describe a time you had to deliver on unclear or constantly changing requirements.",
       ["requirement", "clarif", "assum", "ambigu", "stakeholder", "iterat"]),

    _q("Intermediate",
       "Tell me about a time you pushed back on a request from your manager or a client.",
       ["push back", "concern", "explain", "alternative", "risk", "agreed"]),

    _q("Intermediate",
       "Tell me about a time you used data to make or influence a decision.",
       ["data", "analy", "metric", "decision", "evidence", "impact"]),

    _q("Intermediate",
       "Describe a time you mentored or onboarded a new team member.",
       ["mentor", "onboard", "guided", "feedback", "growth", "independent"]),

    _q("Intermediate",
       "Tell me about a time you had to balance quality against speed of delivery.",
       ["quality", "speed", "trade-off", "testing", "scope", "decision"]),

    _q("Intermediate",
       "Describe a time you collaborated with another team to deliver something.",
       ["cross", "team", "dependenc", "align", "communicat", "delivered"]),

    _q("Intermediate",
       "Tell me about a time you handled an unhappy customer or stakeholder.",
       ["customer", "upset", "listen", "empath", "solution", "follow"]),

    _q("Intermediate",
       "Describe a time you improved the performance of a slow application, query or process.",
       ["performance", "bottleneck", "profil", "optimiz", "measured", "faster"]),

    _q("Intermediate",
       "Tell me about a time you wrote documentation or built automation that saved your team time.",
       ["document", "automat", "script", "time", "team", "adopted"]),

    # ==========================================================
    # ADVANCED (35-50): leadership, strategy, high stakes
    # ==========================================================

    _q("Advanced",
       "Tell me about a project you led from start to finish. How did you keep it on track?",
       ["led", "plan", "milestone", "stakeholder", "risk", "delivered"]),

    _q("Advanced",
       "Describe a high-stakes decision you made with incomplete information.",
       ["decision", "information", "risk", "assum", "weigh", "outcome"]),

    _q("Advanced",
       "Tell me about a time you led the response to a major outage or incident.",
       ["incident", "outage", "coordinat", "communicat", "root cause", "postmortem"]),

    _q("Advanced",
       "Describe a significant architectural or technical trade-off you had to make. How did you decide?",
       ["architect", "trade-off", "scalab", "option", "evaluat", "decision"]),

    _q("Advanced",
       "Tell me about a time you convinced senior leadership to adopt your proposal.",
       ["proposal", "leadership", "business", "case", "persuad", "approved"]),

    _q("Advanced",
       "Describe a time you had to manage an underperforming team member.",
       ["expectation", "feedback", "support", "plan", "performance", "improv"]),

    _q("Advanced",
       "Tell me about a time you had to deliver bad news to a senior stakeholder or client.",
       ["bad news", "transparent", "impact", "options", "plan", "trust"]),

    _q("Advanced",
       "Describe a large migration or refactor you led while keeping the system running.",
       ["migrat", "refactor", "rollout", "rollback", "downtime", "tested"]),

    _q("Advanced",
       "Tell me about a time you had to cut scope to hit a critical deadline. How did you decide what to drop?",
       ["scope", "prioriti", "cut", "impact", "stakeholder", "deadline"]),

    _q("Advanced",
       "Describe a time you identified a security vulnerability or compliance risk and drove the fix.",
       ["security", "vulnerab", "risk", "mitigat", "patch", "compliance"]),

    _q("Advanced",
       "Tell me about a time you scaled a system or team to handle rapid growth.",
       ["scal", "growth", "capacity", "hiring", "bottleneck", "process"]),

    _q("Advanced",
       "Describe a time you resolved a conflict between two senior colleagues or teams.",
       ["conflict", "mediat", "perspective", "common", "resolution", "relationship"]),

    _q("Advanced",
       "Tell me about a time you challenged the status quo and drove organizational change.",
       ["change", "status quo", "buy-in", "vision", "adoption", "impact"]),

    _q("Advanced",
       "Tell me about a failure you were accountable for that hurt the business. How did you recover?",
       ["accountab", "failure", "impact", "recover", "prevent", "learned"]),

    _q("Advanced",
       "Describe a time you had to balance paying down technical debt against delivering new features.",
       ["technical debt", "feature", "prioriti", "business", "trade-off", "roadmap"]),

    _q("Advanced",
       "Tell me about the toughest strategic decision you have made. How did you measure whether it worked?",
       ["strategy", "decision", "metric", "stakeholder", "outcome", "review"]),
]
