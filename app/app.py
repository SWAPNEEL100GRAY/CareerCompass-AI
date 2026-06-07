import streamlit as st

st.set_page_config(
    page_title="CareerCompass AI",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 CareerCompass AI")
st.subheader("AI-Powered Career Guidance Platform")

st.markdown("---")

st.header("Student Profile")

col1, col2 = st.columns(2)

with col1:
    cgpa = st.slider("CGPA", 0.0, 10.0, 8.0)
    dsa = st.slider("DSA Problems Solved", 0, 1000, 200)
    internships = st.slider("Internships", 0, 10, 1)
    projects = st.slider("Projects", 0, 20, 3)

with col2:
    communication = st.slider("Communication Skills", 0, 100, 70)
    resume = st.slider("Resume Score", 0, 100, 70)
    ai_ml = st.slider("AI/ML Skill Level", 0, 100, 50)

career = st.selectbox(
    "Target Career",
    [
        "AI Engineer",
        "Data Scientist",
        "Software Engineer",
        "Business Analyst"
    ]
)

if st.button("Analyze Career"):

    readiness = round(
        (
            cgpa * 10 +
            communication +
            resume +
            ai_ml
        ) / 4,
        1
    )

    st.markdown("---")

    st.header("📊 Results")

    st.metric(
        "Career Readiness Score",
        f"{readiness}%"
    )

    st.subheader("🎯 Recommended Career")

    st.success(career)

    st.subheader("💪 Strengths")

    strengths = []

    if dsa > 200:
        strengths.append("Strong DSA")

    if projects > 3:
        strengths.append("Project Experience")

    if communication > 70:
        strengths.append("Communication Skills")

    if ai_ml > 60:
        strengths.append("AI/ML Knowledge")

    for item in strengths:
        st.write("✅", item)

    st.subheader("📈 Areas To Improve")

    improvements = []

    if dsa < 200:
        improvements.append("Practice DSA")

    if projects < 3:
        improvements.append("Build More Projects")

    if communication < 70:
        improvements.append("Improve Communication")

    if ai_ml < 60:
        improvements.append("Learn Machine Learning")

    for item in improvements:
        st.write("⚠️", item)

    st.subheader("🗺️ 90-Day Roadmap")

    st.write("Month 1: Fundamentals")
    st.write("Month 2: Intermediate Projects")
    st.write("Month 3: Advanced Projects & Interview Prep")