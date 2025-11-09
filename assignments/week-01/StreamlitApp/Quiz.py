import time
import csv
import io
from dataclasses import dataclass
from typing import List, Dict, Optional
import streamlit as st

# -------------------------------
# Page setup
# -------------------------------
st.set_page_config(page_title="Quiz App", page_icon="📝", layout="centered")

# -------------------------------
# Data structures
# -------------------------------
@dataclass
class Question:
    q: str
    options: List[str]  # exactly 4 options
    answer_idx: int     # 0..3
    explanation: str = ""

# -------------------------------
# Default questions (sample bank)
# -------------------------------
DEFAULT_QUESTIONS = [
    Question(
        q="What is the capital of Australia?",
        options=["Sydney", "Melbourne", "Canberra", "Perth"],
        answer_idx=2,
        explanation="Canberra is the capital; Sydney is the largest city."
    ),
    Question(
        q="Which one is not a Python data structure?",
        options=["List", "Tuple", "Dictionary", "Pointer"],
        answer_idx=3,
        explanation="Python doesn't have raw pointers like C/C++."
    ),
    Question(
        q="What does HTTP stand for?",
        options=["HyperText Transfer Protocol", "High-Time Transfer Path", "HyperTool Text Protocol", "Host Transfer Text Protocol"],
        answer_idx=0,
        explanation="HTTP = HyperText Transfer Protocol."
    ),
    Question(
        q="Which library is used for building web apps quickly in Python?",
        options=["NumPy", "Streamlit", "Matplotlib", "Pandas"],
        answer_idx=1,
        explanation="Streamlit is designed for quick data/web apps."
    ),
]

# -------------------------------
# Helpers
# -------------------------------
def parse_csv(file) -> List[Question]:
    """
    CSV columns required:
    question, option_a, option_b, option_c, option_d, answer (A/B/C/D or 0-3), explanation
    """
    text = file.read().decode("utf-8", errors="ignore")
    reader = csv.DictReader(io.StringIO(text))
    qs: List[Question] = []
    for i, row in enumerate(reader, 1):
        try:
            q = row.get("question", "").strip()
            opts = [row.get("option_a",""), row.get("option_b",""), row.get("option_c",""), row.get("option_d","")]
            opts = [o.strip() for o in opts]
            ans_raw = (row.get("answer","") or "").strip().upper()
            if ans_raw in ("A","B","C","D"):
                ans_idx = "ABCD".index(ans_raw)
            else:
                ans_idx = int(ans_raw)
            exp = (row.get("explanation","") or "").strip()
            if not q or len(opts) != 4:
                continue
            qs.append(Question(q=q, options=opts, answer_idx=ans_idx, explanation=exp))
        except Exception:
            st.warning(f"Skipping invalid row {i}.")
    return qs

def init_state():
    if "questions" not in st.session_state:
        st.session_state.questions: List[Question] = DEFAULT_QUESTIONS.copy()
    if "order" not in st.session_state:
        st.session_state.order = list(range(len(st.session_state.questions)))
    if "idx" not in st.session_state:
        st.session_state.idx = 0
    if "answers" not in st.session_state:
        st.session_state.answers: Dict[int, int] = {}  # question_index -> chosen_idx
    if "submitted" not in st.session_state:
        st.session_state.submitted: Dict[int, bool] = {}
    if "start_time" not in st.session_state:
        st.session_state.start_time = None
    if "time_left" not in st.session_state:
        st.session_state.time_left = None
    if "timer_on" not in st.session_state:
        st.session_state.timer_on = False
    if "total_seconds" not in st.session_state:
        st.session_state.total_seconds = 0

def start_timer(total_seconds: int):
    st.session_state.timer_on = True
    st.session_state.total_seconds = total_seconds
    st.session_state.start_time = time.time()
    st.session_state.time_left = total_seconds

def tick_timer():
    if not st.session_state.timer_on or st.session_state.start_time is None:
        return
    elapsed = int(time.time() - st.session_state.start_time)
    st.session_state.time_left = max(0, st.session_state.total_seconds - elapsed)
    if st.session_state.time_left == 0:
        # Auto-submit current question if not yet submitted
        qi = st.session_state.order[st.session_state.idx]
        if qi not in st.session_state.submitted:
            st.session_state.submitted[qi] = True

def reset_quiz(keep_bank=False):
    if not keep_bank:
        st.session_state.questions = DEFAULT_QUESTIONS.copy()
    st.session_state.order = list(range(len(st.session_state.questions)))
    st.session_state.idx = 0
    st.session_state.answers = {}
    st.session_state.submitted = {}
    st.session_state.start_time = None
    st.session_state.time_left = None
    st.session_state.timer_on = False
    st.session_state.total_seconds = 0

def score_summary():
    correct = 0
    for qi, q in enumerate(st.session_state.questions):
        if qi in st.session_state.answers and qi in st.session_state.submitted:
            if st.session_state.answers[qi] == q.answer_idx:
                correct += 1
    total = len(st.session_state.questions)
    return correct, total

# -------------------------------
# Sidebar (settings)
# -------------------------------
init_state()
st.sidebar.header("⚙️ Settings")

uploaded = st.sidebar.file_uploader("Upload CSV (optional)", type=["csv"])
if uploaded:
    custom = parse_csv(uploaded)
    if custom:
        st.session_state.questions = custom
        st.session_state.order = list(range(len(custom)))
        st.session_state.idx = 0
        st.session_state.answers = {}
        st.session_state.submitted = {}
        st.sidebar.success(f"Loaded {len(custom)} questions.")
    else:
        st.sidebar.error("No valid questions found in the CSV.")

shuffle = st.sidebar.checkbox("Shuffle questions", value=True)
if shuffle and st.sidebar.button("Reshuffle"):
    import random
    random.shuffle(st.session_state.order)
    st.session_state.idx = 0

with st.sidebar.expander("⏱️ Timer (optional)"):
    use_timer = st.checkbox("Enable per-quiz timer", value=False, key="use_timer_key")
    minutes = st.number_input("Minutes", min_value=0, value=1, step=1)
    seconds = st.number_input("Seconds", min_value=0, value=0, step=5)
    total_seconds = int(minutes) * 60 + int(seconds)
    if use_timer and not st.session_state.timer_on and st.button("Start timer"):
        if total_seconds <= 0:
            st.warning("Please set a positive duration.")
        else:
            start_timer(total_seconds)

st.sidebar.button("🔁 Restart quiz", on_click=reset_quiz)

# -------------------------------
# Header / progress
# -------------------------------
st.title("📝 Quiz App")
q_count = len(st.session_state.questions)
current = st.session_state.idx + 1
st.progress(current / q_count, text=f"Question {current} of {q_count}")

# Timer display
col_t1, col_t2 = st.columns([1, 3])
with col_t1:
    if st.session_state.timer_on:
        tick_timer()
        m, s = divmod(st.session_state.time_left, 60)
        st.metric("Time left", f"{m:02d}:{s:02d}")
        if st.session_state.time_left == 0:
            st.warning("⏰ Time is up for this quiz.")
            # Allow navigation/review but auto-submitted where needed.

# -------------------------------
# Question card
# -------------------------------
qi = st.session_state.order[st.session_state.idx]
q = st.session_state.questions[qi]

st.subheader(q.q)
options = q.options

# Preserve previously selected choice if any
prev = st.session_state.answers.get(qi, None)
choice = st.radio("Select one:", range(4), format_func=lambda i: options[i], index=prev if prev is not None else 0, key=f"radio_{qi}")

# Actions
c1, c2, c3 = st.columns(3)
submit_clicked = c1.button("✅ Submit", use_container_width=True, disabled=qi in st.session_state.submitted)
next_clicked   = c2.button("➡️ Next", use_container_width=True)
prev_clicked   = c3.button("⬅️ Previous", use_container_width=True)

# Handle submit
if submit_clicked:
    st.session_state.answers[qi] = int(choice)
    st.session_state.submitted[qi] = True

# Auto-save selection even if not submitted
st.session_state.answers[qi] = int(choice)

# Feedback
if qi in st.session_state.submitted:
    is_correct = st.session_state.answers[qi] == q.answer_idx
    if is_correct:
        st.success("✅ Correct!")
    else:
        st.error(f"❌ Incorrect. Correct answer: {q.options[q.answer_idx]}")
    if q.explanation:
        st.info(f"ℹ️ {q.explanation}")

# Navigation
if next_clicked:
    if st.session_state.idx < q_count - 1:
        st.session_state.idx += 1
        st.rerun()
if prev_clicked:
    if st.session_state.idx > 0:
        st.session_state.idx -= 1
        st.rerun()

# -------------------------------
# Completion + Review
# -------------------------------
all_done = len(st.session_state.submitted) == q_count
st.divider()
if all_done:
    correct, total = score_summary()
    st.header(f"🏁 Quiz Complete: {correct}/{total} correct")

    # Review table
    rows = []
    for i in range(total):
        QQ = st.session_state.questions[i]
        your = st.session_state.answers.get(i, None)
        rows.append({
            "Q#": i + 1,
            "Question": QQ.q,
            "Your Answer": "" if your is None else QQ.options[your],
            "Correct Answer": QQ.options[QQ.answer_idx],
            "Result": "Correct" if your == QQ.answer_idx else "Wrong",
        })
    st.dataframe(rows, use_container_width=True, hide_index=True)

    # Export results
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["Q#", "Question", "Your Answer", "Correct Answer", "Result"])
    for r in rows:
        w.writerow([r["Q#"], r["Question"], r["Your Answer"], r["Correct Answer"], r["Result"]])
    st.download_button("⬇️ Download Results (CSV)", data=buf.getvalue().encode("utf-8"),
                       file_name="quiz_results.csv", mime="text/csv")

    st.button("🔄 Restart", on_click=lambda: reset_quiz(keep_bank=True))

# Footer hint
st.caption("Tip: Upload a CSV to use your own questions. Required headers: "
           "`question, option_a, option_b, option_c, option_d, answer, explanation` (answer A/B/C/D or 0-3).")
