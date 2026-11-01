import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# Always load the .env that sits next to app.py, regardless of the
# directory the app was launched from.
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

_client = None
_client_key = None


def get_api_key() -> str:
    return (os.getenv("GROQ_API_KEY") or "").strip().strip('"').strip("'")


def get_client() -> OpenAI:
    """Create the Groq client lazily so the app can start without a key."""
    global _client, _client_key
    api_key = get_api_key()
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set.")
    if _client is None or api_key != _client_key:
        _client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
        _client_key = api_key
    return _client
