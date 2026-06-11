import html
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.append(
    str(
        Path(__file__).resolve().parent.parent
    )
)

from src.recommender import CareerRecommender
from src.roadmap_generator import RoadmapGenerator
from src.skill_gap import SkillGapAnalyzer


st.set_page_config(
    page_title="CareerCompass AI | Career Readiness & Recommendation System",
    page_icon="CC",
    layout="wide"
)


def inject_styles():
    st.markdown(
        """
        <style>
            :root {
                --bg: #0b1020;
                --panel: #111827;
                --panel-soft: #162033;
                --border: rgba(148, 163, 184, 0.18);
                --text: #f8fafc;
                --muted: #94a3b8;
                --cyan: #22d3ee;
                --blue: #60a5fa;
                --green: #34d399;
                --amber: #fbbf24;
                --red: #fb7185;
            }

            .stApp {
                background:
                    radial-gradient(circle at top left, rgba(34, 211, 238, 0.14), transparent 34rem),
                    radial-gradient(circle at top right, rgba(96, 165, 250, 0.12), transparent 30rem),
                    var(--bg);
                color: var(--text);
            }

            section[data-testid="stSidebar"] {
                background:
                    linear-gradient(180deg, rgba(15, 23, 42, 0.98), rgba(8, 13, 26, 1));
                border-right: 1px solid var(--border);
            }

            section[data-testid="stSidebar"] h1,
            section[data-testid="stSidebar"] h2,
            section[data-testid="stSidebar"] h3,
            section[data-testid="stSidebar"] label,
            section[data-testid="stSidebar"] p {
                color: var(--text);
            }

            .block-container {
                max-width: 1180px;
                padding-top: 2rem;
                padding-bottom: 3rem;
            }

            h1, h2, h3 {
                letter-spacing: 0;
            }

            div[data-testid="stMetric"] {
                background: linear-gradient(180deg, rgba(17, 24, 39, 0.98), rgba(15, 23, 42, 0.96));
                border: 1px solid var(--border);
                border-radius: 8px;
                padding: 1rem;
                box-shadow: 0 18px 44px rgba(0, 0, 0, 0.20);
            }

            div[data-testid="stMetricLabel"] p {
                color: var(--muted);
                font-size: 0.86rem;
            }

            div[data-testid="stMetricValue"] {
                color: var(--text);
            }

            .hero {
                border: 1px solid var(--border);
                border-radius: 8px;
                padding: 1.9rem 2rem;
                background:
                    linear-gradient(135deg, rgba(34, 211, 238, 0.12), rgba(96, 165, 250, 0.08)),
                    rgba(17, 24, 39, 0.82);
                box-shadow: 0 24px 70px rgba(0, 0, 0, 0.30);
                margin-bottom: 1.15rem;
            }

            .eyebrow {
                color: var(--cyan);
                font-size: 0.78rem;
                font-weight: 700;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                margin-bottom: 0.65rem;
            }

            .hero h1 {
                color: var(--text);
                font-size: 3rem;
                line-height: 1.05;
                margin: 0 0 0.75rem 0;
            }

            .hero p {
                color: #cbd5e1;
                font-size: 1.04rem;
                line-height: 1.6;
                max-width: 760px;
                margin: 0;
            }

            .badge-row {
                display: flex;
                flex-wrap: wrap;
                gap: 0.65rem;
                margin-top: 1.35rem;
            }

            .badge {
                border: 1px solid rgba(34, 211, 238, 0.28);
                border-radius: 999px;
                color: #dbeafe;
                background: rgba(15, 23, 42, 0.72);
                padding: 0.42rem 0.72rem;
                font-size: 0.84rem;
            }

            .section-title {
                color: var(--text);
                font-size: 1.18rem;
                font-weight: 750;
                margin: 0.4rem 0 0.8rem;
            }

            .muted {
                color: var(--muted);
            }

            .empty-state,
            .card,
            .recommendation-card,
            .timeline-card,
            .callout {
                border: 1px solid var(--border);
                border-radius: 8px;
                background: rgba(17, 24, 39, 0.88);
                box-shadow: 0 18px 44px rgba(0, 0, 0, 0.20);
            }

            .empty-state {
                padding: 1.5rem;
                color: #cbd5e1;
            }

            .card {
                padding: 1rem;
                margin-bottom: 0.8rem;
            }

            .card.strength-card {
                border-left: 3px solid var(--green);
            }

            .card.gap-card {
                border-left: 3px solid var(--amber);
            }

            .recommendation-card {
                border-left: 3px solid var(--cyan);
                padding: 1.1rem 1.15rem;
                margin-bottom: 0.9rem;
            }

            .rec-top {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 1rem;
                margin-bottom: 0.65rem;
            }

            .rank {
                color: var(--cyan);
                font-size: 0.82rem;
                font-weight: 800;
                text-transform: uppercase;
            }

            .role {
                color: var(--text);
                font-size: 1.08rem;
                font-weight: 760;
                margin-top: 0.15rem;
            }

            .score {
                color: var(--cyan);
                font-size: 1.22rem;
                font-weight: 800;
                white-space: nowrap;
            }

            .bar {
                width: 100%;
                height: 0.56rem;
                border-radius: 999px;
                background: rgba(148, 163, 184, 0.16);
                overflow: hidden;
                margin: 0.7rem 0;
            }

            .bar-fill {
                height: 100%;
                border-radius: 999px;
                background: linear-gradient(90deg, var(--cyan), var(--blue));
            }

            .reason {
                color: #cbd5e1;
                font-size: 0.92rem;
                line-height: 1.45;
                margin: 0;
            }

            .pill-list {
                display: flex;
                flex-wrap: wrap;
                gap: 0.55rem;
                margin-bottom: 1.05rem;
            }

            .pill {
                border-radius: 999px;
                padding: 0.42rem 0.7rem;
                font-size: 0.85rem;
                border: 1px solid var(--border);
                background: rgba(15, 23, 42, 0.78);
            }

            .pill.good {
                color: #bbf7d0;
                border-color: rgba(52, 211, 153, 0.36);
                background: rgba(20, 83, 45, 0.18);
            }

            .pill.gap {
                color: #fde68a;
                border-color: rgba(251, 191, 36, 0.38);
                background: rgba(120, 53, 15, 0.18);
            }

            .timeline-card {
                padding: 1rem 1rem 1rem 1.2rem;
                margin-bottom: 0.85rem;
                border-left: 3px solid var(--blue);
            }

            .timeline-card h4 {
                color: var(--text);
                margin: 0 0 0.7rem;
                font-size: 1rem;
            }

            .task {
                color: #cbd5e1;
                padding: 0.34rem 0;
                border-top: 1px solid rgba(148, 163, 184, 0.10);
            }

            .task:first-of-type {
                border-top: 0;
            }

            .callout {
                padding: 1rem;
                color: #dbeafe;
                background: rgba(30, 41, 59, 0.86);
            }

            .stTabs [data-baseweb="tab-list"] {
                gap: 0.4rem;
                margin-top: 0.8rem;
            }

            .stTabs [data-baseweb="tab-panel"] {
                padding-top: 1.05rem;
            }

            .stTabs [data-baseweb="tab"] {
                background: rgba(17, 24, 39, 0.82);
                border: 1px solid var(--border);
                border-radius: 8px;
                color: var(--muted);
                padding: 0.7rem 1rem;
            }

            .stTabs [aria-selected="true"] {
                color: var(--text);
                border-color: rgba(34, 211, 238, 0.42);
                background: rgba(34, 211, 238, 0.10);
            }

            div.stButton > button {
                width: 100%;
                border-radius: 8px;
                border: 1px solid rgba(34, 211, 238, 0.42);
                color: #06111f;
                background: linear-gradient(90deg, var(--cyan), var(--blue));
                font-weight: 800;
            }

            div.stButton > button:hover {
                border-color: rgba(248, 250, 252, 0.7);
                color: #06111f;
            }

            .kpi-spacer {
                margin: 0.35rem 0 1.05rem;
            }

            .sidebar-panel-title {
                color: var(--text);
                font-size: 1.08rem;
                font-weight: 800;
                margin: 0.1rem 0 0.25rem;
            }

            .sidebar-panel-caption {
                color: var(--muted);
                font-size: 0.84rem;
                line-height: 1.45;
                margin-bottom: 1rem;
            }

            .sidebar-section {
                color: var(--cyan);
                font-size: 0.76rem;
                font-weight: 800;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                margin: 1.15rem 0 0.45rem;
                padding-top: 0.78rem;
                border-top: 1px solid rgba(148, 163, 184, 0.16);
            }

            .sidebar-section.first {
                border-top: 0;
                padding-top: 0;
                margin-top: 0.55rem;
            }

            section[data-testid="stSidebar"] .stSlider {
                padding-bottom: 0.15rem;
            }

            section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] label {
                color: #dbeafe;
                font-weight: 650;
            }
        </style>
        """,
        unsafe_allow_html=True
    )


def clamp_score(score):
    return max(0, min(float(score), 100))


def render_hero():
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">AI-Powered Career Readiness & Recommendation System</div>
            <h1>CareerCompass AI</h1>
            <p>
                A professional student career dashboard that turns academic, technical,
                and professional signals into ranked career matches, skill gaps, and a
                focused 90-day learning roadmap.
            </p>
            <div class="badge-row">
                <span class="badge">Career Recommendations</span>
                <span class="badge">Skill Gap Analysis</span>
                <span class="badge">90-Day Roadmap</span>
                <span class="badge">Portfolio-Ready Dashboard</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_recommendation_card(rank, recommendation):
    role = html.escape(recommendation["role"])
    reason = html.escape(recommendation["reason"])
    match = clamp_score(recommendation["match"])

    st.markdown(
        f"""
        <div class="recommendation-card">
            <div class="rec-top">
                <div>
                    <div class="rank">Rank {rank}</div>
                    <div class="role">{role}</div>
                </div>
                <div class="score">{match:.1f}%</div>
            </div>
            <div class="bar">
                <div class="bar-fill" style="width: {match:.1f}%"></div>
            </div>
            <p class="reason">{reason}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_pills(items, class_name, empty_text):
    empty_card_class = "strength-card" if class_name == "good" else "gap-card"

    if not items:
        st.markdown(
            f'<div class="card {empty_card_class} muted">{html.escape(empty_text)}</div>',
            unsafe_allow_html=True
        )
        return

    pills = "".join(
        f'<span class="pill {class_name}">{html.escape(item)}</span>'
        for item in items
    )
    st.markdown(
        f'<div class="pill-list">{pills}</div>',
        unsafe_allow_html=True
    )


def render_learning_plan(items):
    if not items:
        st.markdown(
            '<div class="card gap-card muted">No learning gaps detected for this role.</div>',
            unsafe_allow_html=True
        )
        return

    for item in items:
        st.markdown(
            f'<div class="card gap-card">{html.escape(item)}</div>',
            unsafe_allow_html=True
        )


def render_roadmap(roadmap):
    for month, tasks in roadmap["roadmap"].items():
        task_rows = "".join(
            f'<div class="task">{html.escape(task)}</div>'
            for task in tasks
        )

        st.markdown(
            f"""
            <div class="timeline-card">
                <h4>{html.escape(month)}</h4>
                {task_rows}
            </div>
            """,
            unsafe_allow_html=True
        )


inject_styles()
render_hero()

st.sidebar.markdown(
    '<div class="sidebar-panel-title">Student Profile</div>',
    unsafe_allow_html=True
)
st.sidebar.markdown(
    '<div class="sidebar-panel-caption">Adjust profile signals and run the career analysis.</div>',
    unsafe_allow_html=True
)

st.sidebar.markdown(
    '<div class="sidebar-section first">Academic & Technical</div>',
    unsafe_allow_html=True
)

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

projects = st.sidebar.slider(
    "Projects",
    0,
    20,
    3
)

ai_ml = st.sidebar.slider(
    "AI/ML Skill Level",
    0,
    100,
    50
)

st.sidebar.markdown(
    '<div class="sidebar-section">Professional Readiness</div>',
    unsafe_allow_html=True
)

internships = st.sidebar.slider(
    "Internships",
    0,
    10,
    1
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

recommender = CareerRecommender(
    "data/engineered_data.csv"
)

skill_gap = SkillGapAnalyzer(
    "data/engineered_data.csv"
)

roadmap_generator = RoadmapGenerator()

if not analyze:
    st.markdown(
        """
        <div class="empty-state">
            <div class="section-title">Dashboard Ready</div>
            <p>
                Use the sidebar to define a student profile, then select
                <strong>Analyze Career</strong> to generate role recommendations,
                skill gaps, and a 90-day roadmap.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

if analyze:
    employability = round(
        (
            cgpa * 10 * 0.20 +
            dsa / 10 * 0.15 +
            internships * 10 * 0.15 +
            projects * 5 * 0.10 +
            resume * 0.15 +
            communication * 0.10 +
            ai_ml * 0.15
        ),
        2
    )

    technical = round(
        (
            dsa / 10 * 0.40 +
            ai_ml * 0.40 +
            projects * 5 * 0.20
        ),
        2
    )

    professional = round(
        (
            communication * 0.40 +
            resume * 0.30 +
            internships * 10 * 0.30
        ),
        2
    )

    activity = round(
        (
            projects * 10 * 0.60 +
            internships * 10 * 0.40
        ),
        2
    )

    student = pd.Series(
        {
            "Technical_Strength_Score": technical,
            "Professional_Readiness_Score": professional,
            "Activity_Score": activity,
            "Employability_Score": employability,

            "AI_ML_Skill_Level": ai_ml,
            "DSA_Problems_Solved": dsa,
            "Projects_Count": projects,
            "System_Design_Knowledge": 50,

            "Communication_Skills": communication,
            "Resume_Score": resume,
            "Mock_Interview_Score": 60,
            "Aptitude_Test_Score": 60,
            "GitHub_Contributions": 50
        }
    )

    report = recommender.get_career_report(
        student
    )

    best_career = report[
        "recommendations"
    ][0]["role"]

    skill_report = (
        skill_gap.get_skill_gap_report(
            student,
            best_career
        )
    )

    roadmap = (
        roadmap_generator.get_roadmap(
            best_career
        )
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Career Readiness",
            f"{report['career_readiness']}%"
        )

    with col2:
        st.metric(
            "Best Match",
            best_career
        )

    with col3:
        st.metric(
            "Projects",
            projects
        )

    with col4:
        st.metric(
            "Internships",
            internships
        )

    st.markdown(
        '<div class="kpi-spacer"></div>',
        unsafe_allow_html=True
    )

    tab1, tab2, tab3 = st.tabs(
        [
            "Recommendations",
            "Skill Gaps",
            "Roadmap"
        ]
    )

    with tab1:
        st.markdown(
            '<div class="section-title">Top Career Matches</div>',
            unsafe_allow_html=True
        )

        for index, rec in enumerate(
            report["recommendations"],
            start=1
        ):
            render_recommendation_card(
                index,
                rec
            )

    with tab2:
        st.markdown(
            f"""
            <div class="card">
                <div class="rank">Target Role</div>
                <div class="role">{html.escape(best_career)}</div>
                <p class="reason">Skill readiness for the strongest recommended path.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        readiness = clamp_score(skill_report["readiness"])
        st.markdown(
            f"""
            <div class="card">
                <div class="rec-top">
                    <div class="section-title">Role Readiness</div>
                    <div class="score">{readiness:.1f}%</div>
                </div>
                <div class="bar">
                    <div class="bar-fill" style="width: {readiness:.1f}%"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        left, right = st.columns(2)

        with left:
            st.markdown(
                '<div class="section-title">Current Strengths</div>',
                unsafe_allow_html=True
            )
            render_pills(
                skill_report["strengths"],
                "good",
                "No major strengths detected yet."
            )

        with right:
            st.markdown(
                '<div class="section-title">Priority Skill Gaps</div>',
                unsafe_allow_html=True
            )
            render_pills(
                skill_report["gaps"],
                "gap",
                "No major gaps detected for this role."
            )

        st.markdown(
            '<div class="section-title">Learning Plan</div>',
            unsafe_allow_html=True
        )
        render_learning_plan(
            skill_report["learning_plan"]
        )

        st.markdown(
            f'<div class="callout">{html.escape(skill_report["next_action"])}</div>',
            unsafe_allow_html=True
        )

    with tab3:
        st.markdown(
            f'<div class="section-title">90-Day Roadmap for {html.escape(best_career)}</div>',
            unsafe_allow_html=True
        )

        render_roadmap(
            roadmap
        )

        st.markdown(
            f'<div class="callout">{html.escape(roadmap["goal"])}</div>',
            unsafe_allow_html=True
        )
