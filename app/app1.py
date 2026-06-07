import streamlit as st

st.set_page_config(
    page_title="CareerCompass AI",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 CareerCompass AI")
st.caption("AI-Powered Career Intelligence Platform")

st.markdown("---")

st.sidebar.header("Student Profile")

cgpa = st.sidebar.slider(
    "CGPA",
    0.0,
    10.0,
    8.0
)

dsa = st.sidebar.slider(
    "DSA Problems Solved",
    0,
    1000,
    200
)

internships = st.sidebar.slider(
    "Internships",
    0,
    10,
    1
)

projects = st.sidebar.slider(
    "Projects",
    0,
    20,
    3
)

communication = st.sidebar.slider(
    "Communication Skills",
    0,
    100,
    70
)

resume = st.sidebar.slider(
    "Resume Score",
    0,
    100,
    70
)

ai_ml = st.sidebar.slider(
    "AI/ML Skill Level",
    0,
    100,
    50
)

domain = st.sidebar.selectbox(
    "Preferred Domain",
    [
        "AI & Data",
        "Software Development",
        "Business & Product",
        "Management",
        "Undecided"
    ]
)

analyze = st.sidebar.button(
    "Analyze Career"
)

if analyze:

    readiness = round(
        (
            cgpa * 10 +
            communication +
            resume +
            ai_ml
        ) / 4,
        1
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Career Readiness",
            f"{readiness}%"
        )

    with col2:
        st.metric(
            "Projects",
            projects
        )

    with col3:
        st.metric(
            "Internships",
            internships
        )

    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(
        [
            "🎯 Recommendations",
            "📈 Skill Gaps",
            "🗺️ Roadmap"
        ]
    )

    with tab1:

        st.subheader("Top Career Matches")

        if domain == "AI & Data":

            careers = [
                "AI Engineer",
                "Machine Learning Engineer",
                "Data Scientist",
                "Data Analyst",
                "BI Analyst"
            ]

        elif domain == "Software Development":

            careers = [
                "Software Engineer",
                "Backend Developer",
                "Frontend Developer",
                "Full Stack Developer",
                "DevOps Engineer"
            ]

        elif domain == "Business & Product":

            careers = [
                "Business Analyst",
                "Product Analyst",
                "Product Manager",
                "Operations Analyst"
            ]

        else:

            careers = [
                "Technology Consultant",
                "Project Coordinator",
                "Project Manager"
            ]

        for i, career in enumerate(
            careers[:5],
            start=1
        ):
            st.success(
                f"{i}. {career}"
            )

    with tab2:

        st.subheader(
            "Current Strengths"
        )

        if dsa > 200:
            st.write(
                "✅ Strong DSA"
            )

        if projects > 3:
            st.write(
                "✅ Good Project Experience"
            )

        if communication > 70:
            st.write(
                "✅ Good Communication"
            )

        if ai_ml > 60:
            st.write(
                "✅ AI/ML Knowledge"
            )

        st.subheader(
            "Areas To Improve"
        )

        if dsa < 200:
            st.warning(
                "Practice DSA"
            )

        if projects < 3:
            st.warning(
                "Build More Projects"
            )

        if communication < 70:
            st.warning(
                "Improve Communication Skills"
            )

        if ai_ml < 60:
            st.warning(
                "Learn Machine Learning"
            )

    with tab3:

        st.subheader(
            "90-Day Learning Roadmap"
        )

        st.write(
            "Month 1 → Fundamentals"
        )

        st.write(
            "Month 2 → Intermediate Projects"
        )

        st.write(
            "Month 3 → Advanced Projects & Interviews"
        )