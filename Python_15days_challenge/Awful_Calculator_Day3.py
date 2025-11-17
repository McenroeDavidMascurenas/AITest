import streamlit as st
import pandas as pd

# -------------------------------
# Page config
# -------------------------------
st.set_page_config(
    page_title="VIVID CALCULATOR",
    page_icon="🧮",
    layout="centered"
)

# -------------------------------
# Session State Init (History)
# -------------------------------
if "history" not in st.session_state:
    st.session_state.history = []  # list of dicts: {"a":..,"b":..,"op":..,"res":..}


# -------------------------------
# Dark / Light Toggle
# -------------------------------
mode = st.toggle("🌗 Dark mode", value=True)

# -------------------------------
# Base + Theme CSS (Animated + Neon + Holographic)
# -------------------------------
base_css = """
<style>
/* Animated gradient background */
body {
    margin: 0;
    padding: 0;
    background: linear-gradient(-45deg, #0f172a, #1f2937, #2dd4bf, #ec4899);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
    font-family: "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
}
@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Main app container holographic card */
.main {
    padding: 2rem;
}

.vivid-card {
    max-width: 800px;
    margin: 1.5rem auto;
    padding: 2rem 2.5rem;
    border-radius: 32px;
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    background: radial-gradient(circle at top, rgba(255,255,255,0.20), rgba(15,23,42,0.95));
    border: 2px solid rgba(255,255,255,0.18);
    box-shadow:
        0 0 40px rgba(56,189,248,0.4),
        0 0 70px rgba(236,72,153,0.35),
        0 0 100px rgba(129,140,248,0.4);
}

/* Title – holographic 3D */
.app-title {
    font-size: 3.5rem;
    font-weight: 900;
    text-align: center;
    margin-bottom: 1.5rem;
    letter-spacing: 0.06em;
    background: linear-gradient(120deg,#a855f7,#22d3ee,#f97316,#ec4899);
    -webkit-background-clip: text;
    color: transparent;
    text-shadow:
        0 0 12px rgba(59,130,246,0.8),
        0 0 30px rgba(236,72,153,0.8);
}

/* Subtitle */
.subtitle {
    text-align: center;
    font-size: 1.1rem;
    margin-bottom: 1.5rem;
    color: #e5e7eb;
}

/* Labels */
.stTextInput label, .stSelectbox label {
    font-size: 1.3rem !important;
    font-weight: 700 !important;
}

/* Text inputs */
.stTextInput input {
    font-size: 1.2rem !important;
    font-weight: 600 !important;
    border-radius: 999px !important;
    border: 1px solid rgba(148,163,184,0.8) !important;
    background: rgba(15,23,42,0.75) !important;
    color: #e5e7eb !important;
}

/* Select box */
.stSelectbox div[data-baseweb="select"] > div {
    font-size: 1.2rem !important;
    font-weight: 600 !important;
}

/* Neon glow button */
.stButton > button {
    width: 100%;
    font-size: 1.7rem !important;
    font-weight: 800 !important;
    border-radius: 999px !important;
    padding: 0.8rem 1.2rem !important;
    border: 2px solid #22d3ee !important;
    color: #0f172a !important;
    background: radial-gradient(circle at top left, #f97316, #ec4899, #22d3ee) !important;
    box-shadow:
        0 0 20px rgba(56,189,248,0.9),
        0 0 40px rgba(236,72,153,0.7);
    transition: transform 0.15s ease, box-shadow 0.15s ease, filter 0.15s ease;
}
.stButton > button:hover {
    transform: translateY(-2px) scale(1.02);
    box-shadow:
        0 0 30px rgba(56,189,248,1),
        0 0 60px rgba(236,72,153,0.9);
    filter: brightness(1.1);
}

/* Result box */
.result-box {
    margin-top: 1.5rem;
    padding: 1.6rem;
    border-radius: 24px;
    border: 1px solid rgba(148,163,184,0.8);
    background: radial-gradient(circle at top, rgba(34,197,94,0.25), rgba(15,23,42,0.9));
    text-align: center;
    font-size: 1.7rem;
    color: #e5e7eb;
    font-weight: 700;
}
.result-num {
    font-size: 2.7rem;
    font-weight: 900;
    color: #bbf7d0;
    text-shadow:
        0 0 8px rgba(74,222,128,0.9),
        0 0 18px rgba(34,197,94,0.8);
}

/* History title */
.history-title {
    font-size: 1.5rem;
    font-weight: 800;
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
    color: #e5e7eb;
}

/* Voice box */
.voice-card {
    margin-top: 2rem;
    padding: 1.2rem 1.4rem;
    border-radius: 22px;
    border: 1px solid rgba(129,140,248,0.8);
    background: radial-gradient(circle at top, rgba(129,140,248,0.25), rgba(15,23,42,0.95));
    color: #e5e7eb;
}
.voice-title {
    font-weight: 800;
    font-size: 1.3rem;
    margin-bottom: 0.4rem;
}

/* Voice button */
.voice-btn {
    border-radius: 999px;
    padding: 0.5rem 1.1rem;
    border: 2px solid #f97316;
    background: radial-gradient(circle,#f97316,#ec4899);
    color: #0f172a;
    font-weight: 800;
    cursor: pointer;
    font-size: 1rem;
    box-shadow:
        0 0 10px rgba(249,115,22,0.8),
        0 0 24px rgba(236,72,153,0.9);
}
.voice-btn:hover {
    transform: translateY(-1px) scale(1.03);
}

/* Dark / Light mode variants */
body.dark-mode {
    color: #e5e7eb;
}
body.light-mode {
    background: linear-gradient(-45deg,#f9fafb,#e5e7eb,#bfdbfe,#fed7aa);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
}
body.light-mode .vivid-card {
    background: radial-gradient(circle at top, rgba(255,255,255,0.95), rgba(248,250,252,0.9));
    border-color: rgba(148,163,184,0.5);
    box-shadow:
        0 0 20px rgba(148,163,184,0.4),
        0 0 50px rgba(191,219,254,0.7);
}
body.light-mode .subtitle,
body.light-mode .history-title,
body.light-mode .voice-card {
    color: #111827;
}
body.light-mode .voice-card {
    background: radial-gradient(circle at top, rgba(191,219,254,0.85), rgba(248,250,252,0.98));
}
</style>
"""

st.markdown(base_css, unsafe_allow_html=True)

# JS to flip body class based on toggle
mode_class = "dark-mode" if mode else "light-mode"

st.markdown(
    f"""
    <script>
    document.addEventListener('DOMContentLoaded', function() {{
        document.body.classList.remove('dark-mode','light-mode');
        document.body.classList.add('{mode_class}');
    }});
    </script>
    """,
    unsafe_allow_html=True
)

# -------------------------------
# Layout Card
# -------------------------------
st.markdown('<div class="vivid-card">', unsafe_allow_html=True)

st.markdown('<div class="app-title">VIVID CALCULATOR</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Type numbers, pick an operation, click the neon button. History, dark mode & even a tiny voice helper included.</div>',
    unsafe_allow_html=True
)

# -------------------------------
# Inputs
# -------------------------------
c1, c2 = st.columns(2)

with c1:
    num1_str = st.text_input("🔢 First number", value="0.0")

with c2:
    num2_str = st.text_input("🔢 Second number", value="0.0")

operation = st.selectbox(
    "👉 Choose operation",
    ["+", "-", "×", "÷", "A % of B (A% of B)"]
)

# -------------------------------
# Calculation
# -------------------------------
result = None
error_msg = ""

if st.button("💥 CALCULATE 💥"):
    try:
        a = float(num1_str)
        b = float(num2_str)

        if operation == "+":
            result = a + b
        elif operation == "-":
            result = a - b
        elif operation == "×":
            result = a * b
        elif operation == "÷":
            if b == 0:
                error_msg = "🚫 Division by zero is not allowed."
            else:
                result = a / b
        elif operation.startswith("A % of B"):
            result = (a / 100.0) * b

        if error_msg == "" and result is not None:
            st.session_state.history.append(
                {"First": a, "Op": operation, "Second": b, "Result": result}
            )

    except ValueError:
        error_msg = "⚠️ Please enter valid numbers (decimals like 2.5 are allowed)."

# -------------------------------
# Output
# -------------------------------
if error_msg:
    st.error(error_msg)
elif result is not None:
    st.markdown(
        f'<div class="result-box">Result: <span class="result-num">{result}</span></div>',
        unsafe_allow_html=True
    )

# -------------------------------
# History
# -------------------------------
if st.session_state.history:
    st.markdown('<div class="history-title">📜 Calculation history</div>', unsafe_allow_html=True)
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df, use_container_width=True)

# -------------------------------
# Voice Input Helper (Web Speech API)
# -------------------------------
voice_html = """
<div class="voice-card">
  <div class="voice-title">🎙️ Voice Input Helper (experimental)</div>
  <p style="font-size:0.95rem; margin-bottom:0.6rem;">
    Click <strong>Start voice</strong>, speak a number or expression (like "twenty three point five"),<br>
    then copy the recognized text into the calculator boxes.
  </p>
  <button class="voice-btn" onclick="startDictation()">🎙️ Start voice</button>
  <p id="voice-status" style="margin-top:0.6rem; font-size:0.9rem; opacity:0.9;">Status: idle</p>
  <textarea id="voice-output" rows="2" style="
        width:100%;
        margin-top:0.3rem;
        border-radius:12px;
        border:1px solid rgba(148,163,184,0.8);
        padding:0.4rem 0.6rem;
        background:rgba(15,23,42,0.75);
        color:#e5e7eb;
        font-size:0.95rem;
    " placeholder="Recognized text will appear here..."></textarea>

  <script>
    function startDictation() {{
      if (!('webkitSpeechRecognition' in window)) {{
        document.getElementById('voice-status').innerText = "Status: ❌ Speech recognition not supported in this browser.";
        return;
      }}
      var recognition = new webkitSpeechRecognition();
      recognition.lang = 'en-US';
      recognition.interimResults = false;
      recognition.maxAlternatives = 1;

      document.getElementById('voice-status').innerText = "Status: 🎧 Listening...";

      recognition.onresult = function(event) {{
        var transcript = event.results[0][0].transcript;
        document.getElementById('voice-output').value = transcript;
        document.getElementById('voice-status').innerText = "Status: ✅ Recognized. Copy & paste into the calculator boxes.";
      }};

      recognition.onerror = function(event) {{
        document.getElementById('voice-status').innerText = "Status: ⚠️ Error: " + event.error;
      }};

      recognition.onend = function() {{
        if (document.getElementById('voice-status').innerText.includes("Listening")) {{
          document.getElementById('voice-status').innerText = "Status: ⏹ Stopped. Click again to retry.";
        }}
      }};

      recognition.start();
    }}
  </script>
</div>
"""
st.markdown(voice_html, unsafe_allow_html=True)

# Close main card div
st.markdown("</div>", unsafe_allow_html=True)
