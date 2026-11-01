# PrepPilot

An AI-powered interview practice app built with Streamlit. Answer interview
questions, get instant structured feedback, chat with an AI coach, and receive a
final performance report.

## Features

- AI evaluation of every answer with encouraging, actionable feedback
- STAR structure detection (Situation, Task, Action, Result)
- Filler word detection
- Keyword-based relevance scoring
- Welcome screen with a spoken greeting and a Start button
- Questions are read aloud (browser text-to-speech); you type your answers. Toggle and speed in the sidebar
- Live scorecard in the sidebar
- Ask-the-coach chat that uses your whole session history
- Final report with AI coaching summary and Markdown download

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # then open .env and paste your key after GROQ_API_KEY=
streamlit run app.py
```

Get a free API key at https://console.groq.com. Your `.env` should look like this
(no spaces or quotes needed):

```text
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxx
```

No `.env`? You can also paste the key into the sidebar when the app starts, or
add it to `.streamlit/secrets.toml` as `GROQ_API_KEY = "gsk_..."`.

## Project structure

```text
preppilot/
├── app.py                  # Streamlit UI
├── config.py               # App name, tagline, model
├── voice.py                # Read-aloud (text-to-speech) for questions
├── interview_bank.py       # Questions and expected keywords
├── requirements.txt
├── .env.example
├── .streamlit/config.toml
├── core/
│   ├── llm.py              # Lazy Groq client
│   ├── evaluator_agent.py  # Tool-calling answer evaluator
│   ├── agent.py            # Ask-the-coach agent
│   ├── final_coach.py      # Final coaching report
│   ├── report.py           # Session metrics aggregation
│   └── session_manager.py  # In-memory session history
└── tools/
    ├── filler_words.py
    ├── relevance.py
    └── star_structure.py
```

## Voice

Questions are read aloud using your browser's built-in speech engine, so there is
nothing to install. Use the **Voice** section in the sidebar to switch it off or change
the speaking speed. If a question doesn't play automatically (some browsers block
audio until you click on the page), press **🔊 Listen to question**. Works best in
Chrome, Edge and Safari.


## Customising

- **Rename the app:** edit `APP_NAME` in `config.py`.
- **Change questions:** edit `interview_bank.py`.
- **Change model:** edit `MODEL_NAME` in `config.py`.
