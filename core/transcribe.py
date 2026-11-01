from config import STT_MODEL
from core.llm import get_client

# A short prompt nudges Whisper to keep spoken fillers (um, uh, like) in the
# transcript instead of silently cleaning them up, so the filler-word
# detector still has something to find.
_PROMPT = "Um, uh, so, like, you know, basically, actually, I mean."


def transcribe_audio(audio_bytes: bytes, filename: str = "answer.wav") -> str:
    """Transcribe recorded speech to text using Groq's Whisper endpoint."""
    response = get_client().audio.transcriptions.create(
        model=STT_MODEL,
        file=(filename, audio_bytes, "audio/wav"),
        language="en",
        prompt=_PROMPT,
        response_format="text",
    )
    # response_format="text" returns a plain string; other formats return an object
    text = response if isinstance(response, str) else getattr(response, "text", "")
    return text.strip()
