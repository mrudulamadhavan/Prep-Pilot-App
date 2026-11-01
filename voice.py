"""
Voice helpers for PrepPilot.

Reads interview questions aloud using the browser's built-in Web Speech API
(speechSynthesis). Nothing is sent to a server and no API key is needed.
"""

import json

import streamlit as st


def speak_question(
    text: str,
    rate: float = 1.0,
    autoplay: bool = True,
    key: str = "",
    label: str = "🔊 Listen to question",
):
    """Render Listen / Stop buttons and (optionally) speak the question automatically.

    The widget is re-created whenever `text`, `rate` or `autoplay` change, so a new
    question is read automatically when you move to it. Re-runs that don't change
    these values do not repeat the speech.
    """
    payload = json.dumps({"text": text, "rate": rate, "autoplay": autoplay}).replace("</", "<\\/")

    html = f"""
    <div style="font-family: sans-serif; display: flex; gap: 8px; align-items: center;">
      <button id="listen" style="padding: 6px 14px; border-radius: 8px; border: 1px solid #c9ccd3;
              background: #f4f5f8; color: #262730; cursor: pointer; font-size: 14px;">
        {label}
      </button>
      <button id="stop" style="padding: 6px 14px; border-radius: 8px; border: 1px solid #c9ccd3;
              background: #f4f5f8; color: #262730; cursor: pointer; font-size: 14px;">
        ⏹ Stop
      </button>
      <span id="msg" style="font-size: 12px; color: #888;"></span>
    </div>
    <!-- {key} -->
    <script>
      const cfg = {payload};
      const msg = document.getElementById("msg");
      const synth = window.speechSynthesis;

      function pickVoice() {{
        const voices = synth.getVoices();
        return voices.find(v => v.lang === "en-US" && /Google|Natural|Samantha|Aria|Jenny/i.test(v.name))
            || voices.find(v => v.lang.startsWith("en"))
            || null;
      }}

      function speak() {{
        if (!synth) {{ msg.textContent = "Speech is not supported in this browser."; return; }}
        synth.cancel();
        const u = new SpeechSynthesisUtterance(cfg.text);
        const voice = pickVoice();
        if (voice) u.voice = voice;
        u.lang = (voice && voice.lang) || "en-US";
        u.rate = cfg.rate;
        u.onstart = () => msg.textContent = "Speaking...";
        u.onend = () => msg.textContent = "";
        u.onerror = (e) => {{
          msg.textContent = (e.error === "not-allowed")
            ? "Click “Listen” to hear the question." : "";
        }};
        synth.speak(u);
      }}

      document.getElementById("listen").onclick = speak;
      document.getElementById("stop").onclick = () => {{ synth.cancel(); msg.textContent = ""; }};

      if (synth) {{
        synth.cancel();  // stop any previous question
        if (cfg.autoplay) {{
          // Voices load asynchronously in some browsers
          if (synth.getVoices().length) {{ speak(); }}
          else {{ synth.onvoiceschanged = () => {{ synth.onvoiceschanged = null; speak(); }}; setTimeout(speak, 400); }}
        }}
      }} else {{
        msg.textContent = "Speech is not supported in this browser.";
      }}
    </script>
    """
    html = html.strip()
    if hasattr(st, "iframe"):
        # Newer Streamlit: st.components.v1.html is deprecated in favour of st.iframe
        st.iframe(html, height=48)
    else:
        import streamlit.components.v1 as components

        components.html(html, height=48)
