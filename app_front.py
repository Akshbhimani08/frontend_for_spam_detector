import streamlit as st
import requests

# Page Config
st.set_page_config(
    page_title="Spam Email Detector",
    page_icon="📧",
    layout="centered"
)

# Custom CSS for modern UI
st.markdown("""
    <style>
        .main {
            padding-top: 2rem;
        }

        .stTextArea textarea {
            font-size: 14px !important;
        }

        .stButton>button {
            width: 100%;
            border-radius: 8px;
            height: 40px;
            font-weight: 600;
        }

        .result-box {
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-size: 15px;
            font-weight: 500;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h2 style='text-align:center;'>📧 Spam Email Detection</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:14px;'>Check whether your email is Spam or Not Spam</p>", unsafe_allow_html=True)

st.divider()

# Input Box
email_text = st.text_area(
    "Email Content",
    height=150,
    placeholder="Paste your email content here..."
)

# Predict Button
if st.button("🔍 Analyze Email"):

    if email_text.strip() == "":
        st.warning("Please enter email content.")
    else:
        try:
            response = requests.post(
            "http://localhost:8000/predict",
            data=email_text,
            headers={"Content-Type": "text/plain"}
            )

            if response.status_code == 200:
                result = response.json()["Message"]

                # Extract confidence
                confidence = float(result.split(":")[-1].replace("%", "").strip())

                if "Not Spam" in result:
                    st.markdown(
                        f"<div class='result-box' style='background-color:#1f3a2a; color:#00d084;'>✅ Not Spam<br>Confidence: {confidence}%</div>",
                        unsafe_allow_html=True
                    )
                elif "Spam" in result:
                    st.markdown(
                        f"<div class='result-box' style='background-color:#3a1f1f; color:#ff4b4b;'>🚨 Spam Detected<br>Confidence: {confidence}%</div>",
                        unsafe_allow_html=True
                    )

                st.progress(confidence / 100)

            else:
                st.error("Backend error. Check FastAPI server.")

        except:
            st.error("Cannot connect to backend. Is FastAPI running?")


st.markdown("""
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 10px;
    width: 100%;
    text-align: center;
    font-size: 14px;
    color: #888;
}
</style>

<div class="footer">
    Built with ❤️ by <span style='color:#4ea8de;'>Aksh Bhimani</span>
</div>
""", unsafe_allow_html=True)
