import streamlit as st
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
st.set_page_config(page_title="BMI Calculator", layout="centered", page_icon="⚖️")

# ------------- SESSION STATE -----------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# ------------- DARK MODE TOGGLE ----------
dark_mode = st.toggle("🌙 Enable Dark Mode", value=st.session_state.dark_mode)
st.session_state.dark_mode = dark_mode

# ------------- CSS STYLING ----------------
def inject_styles(dark_mode: bool):
    bg_url = (
        "https://images.unsplash.com/photo-1588776814546-ec7a3c86eb1c?auto=format&fit=crop&w=1350&q=80"
        if not dark_mode else
        "https://images.unsplash.com/photo-1588776814780-47edbcf6c2ab?auto=format&fit=crop&w=1350&q=80"
    )

    text_color = "#ffffff" if dark_mode else "#0d1b2a"

    st.markdown(
        f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
            html, body, [class*="css"] {{
                font-family: 'Poppins', sans-serif;
                background-image: url('{bg_url}');
                background-size: cover;
                background-attachment: fixed;
                background-position: center;
                color: {text_color};
            }}
            h1, h2, h3, h4 {{
                font-size: 2rem !important;
                font-weight: 600 !important;
            }}
            label, .stNumberInput input {{
                font-size: 1.2rem !important;
            }}
            .stButton > button {{
                font-size: 1.1rem;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 123, 255, 0.3);
                transition: 0.3s ease-in-out;
                padding: 0.6rem 1.5rem;
            }}
            .stButton > button:hover {{
                box-shadow: 0 0 14px rgba(0, 123, 255, 0.6);
            }}
            .result-card {{
                padding: 1.8rem;
                border-radius: 12px;
                text-align: center;
                margin-top: 1.5rem;
                color: white;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

inject_styles(dark_mode)

# ------------------ UI ------------------
st.title("BMI Calculator")
st.subheader("Calculate your Body Mass Index instantly")

weight = st.number_input("Enter your weight (kg)", min_value=1.0, max_value=300.0, step=0.1)
height_cm = st.number_input("Enter your height (cm)", min_value=50.0, max_value=250.0, step=0.1)

# ------------------ LOGIC ------------------
def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    height_m = height_cm / 100
    return weight_kg / (height_m ** 2)

def classify_bmi(bmi: float) -> tuple[str, str]:
    if bmi < 18.5:
        return "Underweight", "#4fc3f7"
    if bmi < 25:
        return "Normal", "#66bb6a"
    if bmi < 30:
        return "Overweight", "#ffa726"
    return "Obese", "#ef5350"

# ------------------ CHART ------------------
def render_bmi_chart(bmi_value: float):
    categories = ["Underweight", "Normal", "Overweight", "Obese"]
    thresholds = [18.5, 25, 30]
    colors = ["#4fc3f7", "#66bb6a", "#ffa726", "#ef5350"]

    fig, ax = plt.subplots(figsize=(8, 1.5))
    bars = [16, 6.5, 5, 10]  # Segment widths for visual range

    start = 10
    for width, color in zip(bars, colors):
        ax.barh(0, width, left=start, color=color)
        start += width

    ax.axvline(bmi_value, color="black", linewidth=2)
    ax.text(bmi_value + 0.2, 0.2, f"Your BMI: {bmi_value}", fontsize=10)

    ax.set_xlim(10, 47)
    ax.set_yticks([])
    ax.set_xticks([10, 18.5, 25, 30, 40])
    ax.set_xticklabels(["10", "18.5", "25", "30", "40+"])
    ax.set_title("BMI Classification Chart", fontsize=12)
    st.pyplot(fig)

# ------------------ OUTPUT ------------------
if st.button("Calculate BMI"):
    bmi = round(calculate_bmi(weight, height_cm), 2)
    category, color = classify_bmi(bmi)

    st.markdown(
        f"""
        <div class="result-card" style="background-color: {color};">
            <h2>Your BMI: {bmi}</h2>
            <h3>Category: {category}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    interpretation = {
        "Underweight": "You are below the normal weight range. Consider speaking with a health professional.",
        "Normal": "You are within the healthy weight range. Keep up the good lifestyle!",
        "Overweight": "You are above the normal weight range. A balanced diet and activity may help.",
        "Obese": "You are significantly above the normal weight range. Medical advice is recommended."
    }

    st.markdown(f"**Note:** {interpretation[category]}")
    render_bmi_chart(bmi)
