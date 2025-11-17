import streamlit as st
import base64

# --- Configuration ---
st.set_page_config(page_title="Greeting App", layout="centered")

# Function to inject local image as background using Base64 encoding
def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        img_bytes = f.read()
    encoded_string = base64.b64encode(img_bytes).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded_string}");
            background-size: cover;
            background-attachment: fixed;
            color: white; /* Make text readable on potentially dark background */
            text-shadow: 1px 1px 2px black; /* Add shadow to text for better contrast */
        }}
        /* Optional: adjust header and sidebar for transparency if needed */
        [data-testid="stHeader"] {{
            background-color: rgba(0, 0, 0, 0.2);
        }}
        [data-testid="stSidebar"] {{
            background-color: rgba(0, 0, 0, 0.4);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# --- Apply Background ---
# NOTE: Make sure 'background.jpg' is in the same directory as your Python script
try:
    add_bg_from_local('background.jpg')
except FileNotFoundError:
    st.warning("Background image 'background.jpg' not found. App running without a custom background.")

st.title("Personalized Greeting Form")

# --- Form Inputs (moved to a container for better visibility) ---
with st.container(border=True):
    # Text input for the name
    name = st.text_input("Enter your name:")

    # Slider for the age (range 0 to 100, default 25)
    age = st.slider("Select your age:", min_value=0, max_value=100, value=25)

    # --- Button and Output Logic ---
    # A button to process the input
    if st.button("Show Greeting and Celebrate!"):
        if name:
            # Display the greeting message
            st.success(f"Hello, {name}! You are {age} years old.")
            # Trigger the balloon animation
            st.balloons()
        else:
            # Display a warning if the name is empty
            st.warning("Please enter your name.")

