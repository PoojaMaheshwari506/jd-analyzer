import streamlit as st
import requests

st.set_page_config(
    page_title="JD Analyzer",
    layout="centered",
    page_icon="📄"
)

st.title("📄 Job Description Analyzer")
st.caption("Analyze job descriptions using AI to extract role, skills & complexity")

jd_text = st.text_area(
    "Paste Job Description here",
    height=250,
    placeholder="Paste the job description here..."
)
uploaded_file = st.file_uploader(
    "Upload JD (PDF or Image)",
    type=["pdf", "png", "jpg", "jpeg"]
)
if st.button("Analyze JD"):
    if not jd_text.strip() and uploaded_file is None:
        st.warning("Please paste a job description or upload a file.")
    else:
        with st.spinner("Analyzing JD..."):
            try:
                # -------- CASE 1: File uploaded --------
                if uploaded_file is not None:
                    response = requests.post(
                        "https://jd-analyzer-pfb3.onrender.com-file",
                        files={"file": uploaded_file},
                        timeout=60
                    )

                # -------- CASE 2: Text pasted --------
                else:
                    response = requests.post(
                        "https://jd-analyzer-pfb3.onrender.com",
                        json={"jd_text": jd_text},
                        timeout=30
                    )

                if response.status_code == 200:
                    result = response.json()

                    st.subheader("🔍 Analysis Result")

                    st.markdown(f"**Role:** `{result.get('role', 'N/A')}`")
                    st.markdown(f"**Seniority:** `{result.get('seniority', 'N/A')}`")

                    # -------- Required Skills --------
                    st.markdown("### ✅ Required Skills")
                    req_skills = result.get("required_skills", [])

                    if req_skills:
                        for skill in req_skills:
                            st.write("•", skill)
                    else:
                        st.info("No strong required skills detected.")

                    # -------- Nice to Have --------
                    nice_skills = result.get("nice_to_have", [])

                    if nice_skills:
                        st.markdown("### 🌱 Nice to Have")
                        for skill in nice_skills:
                            st.write("•", skill)

                    # -------- Complexity --------
                    st.markdown(
                        f"### ⚙️ JD Complexity: `{result.get('complexity', 'N/A')}`"
                    )

                else:
                    st.error("Backend error. Please try again.")

            except requests.exceptions.RequestException as e:
                st.error("Unable to connect to backend.")
                st.caption(str(e))
