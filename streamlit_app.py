import requests
import streamlit as st

st.set_page_config(
    page_title="Phishing Email Detector", page_icon="🛡️", layout="centered"
)

st.title("🛡️ Phishing Email Detector")
st.write("Email ka text niche enter karein aur check karein ke yeh safe hai ya phishing.")

# User input text
email_text = st.text_area("Email Content:", height=150, placeholder="Paste email text here...")

# Backend API URL (Render deployment ke baad yahan Render ka URL aayega)
API_URL = "http://127.0.0.1:8000/predict"

if st.button("Analyze Email", type="primary"):
    if email_text.strip():
        with st.spinner("Analyzing text..."):
            try:
                response = requests.post(API_URL, json={"text": email_text})
                if response.status_code == 200:
                    result = response.json()

                    st.divider()

                    # Result Display
                    pred = result.get("prediction")
                    conf = result.get("confidence", 0) * 100

                    if pred == "Phishing":
                        st.error(f"⚠️ **Result: Phishing Detected!**")
                    else:
                        st.success(f"✅ **Result: Safe Email**")

                    st.metric(label="Confidence Score", value=f"{conf:.2f}%")

                    # Word Impact Scores Display
                    impacts = result.get("word_impact_scores", {})
                    if impacts:
                        st.subheader("Top Influential Words")
                        st.json(impacts)

                else:
                    st.error("API se error aaya hai. Dobaara try karein.")
            except Exception as e:
                st.error(f"Backend Server se connect nahi ho saka: {e}")
    else:
        st.warning("Please enter some text first!")