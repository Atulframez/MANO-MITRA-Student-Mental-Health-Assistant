import streamlit as st
import requests
from PIL import Image
import io

API_URL = st.secrets.get("api_url", "http://localhost:8000")

st.set_page_config(page_title="MANO-MITRA", layout="wide")
st.title("MANO-MITRA — Student Mental Health Assistant")

# --- Simple local auth (for prototype only)
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# Login / main UI
if not st.session_state.user_id:
    with st.form("login"):
        uid = st.text_input("Enter your student id (email)")
        submitted = st.form_submit_button("Start")
        if submitted and uid:
            st.session_state.user_id = uid
            st.experimental_rerun()
else:
    st.sidebar.write("Logged in as: " + st.session_state.user_id)
    tab = st.sidebar.radio(
        "Go to",
        ["Chatbot", "Emotion Check (webcam/image)", "Dashboard", "Mock Smartwatch"],
    )

    if tab == "Chatbot":
        st.header("Talk to MANO-MITRA")
        txt = st.text_area("How are you feeling?")
        if st.button("Send") and txt.strip():
            try:
                r = requests.post(
                    API_URL + "/chat",
                    json={"user_id": st.session_state.user_id, "text": txt},
                    timeout=10,
                )
                if r.ok:
                    st.success(r.json().get("reply", "No reply"))
                else:
                    st.error("Error: " + r.text)
            except requests.exceptions.RequestException as e:
                st.error(f"Network error: {e}")

    if tab == "Emotion Check (webcam/image)":
        st.header("Emotion detection")
        img_file = st.file_uploader("Upload a face photo", type=["png", "jpg", "jpeg"])
        if img_file is not None:
            try:
                # prepare file payload
                files = {"file": (img_file.name, img_file.read(), "image/jpeg")}
                r = requests.post(
                    API_URL + "/emotion?user_id=" + st.session_state.user_id,
                    files=files,
                    timeout=20,
                )
                if r.ok:
                    st.json(r.json())
                else:
                    st.error("Error: " + r.text)
            except requests.exceptions.RequestException as e:
                st.error(f"Network error: {e}")

    if tab == "Mock Smartwatch":
        st.header("Simulate smartwatch data (prototype)")
        hr = st.slider("Heart rate", 40, 140, 72)
        steps = st.number_input("Steps today", 0, 50000, 1200)
        if st.button("Send smartwatch data"):
            # In real system you'd POST to an endpoint that ingests smartwatch data
            st.info(
                "Smartwatch data sent (simulated). If heart rate > 110 an alert would be considered."
            )

    if tab == "Dashboard":
        st.header("Recent sessions (prototype)")
        st.info(
            "This dashboard is a placeholder. Connect to MongoDB to show real user data."
        )

    if st.button("Logout"):
        st.session_state.user_id = None
        st.experimental_rerun()
