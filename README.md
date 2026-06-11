# CareerCompass AI

**AI-Powered Career Readiness & Recommendation System**

CareerCompass AI is a Streamlit-based career guidance platform that analyzes a student's academic profile, technical preparation, project activity, communication readiness, and AI/ML skill level to recommend suitable career paths. The project combines feature engineering, rule-based recommendation logic, skill gap analysis, and personalized learning roadmaps to help students prepare for internships, placements, and entry-level AI/ML or analytics roles.

---

## Overview

Students often struggle to understand which career path best matches their current skills and what they should improve next. CareerCompass AI addresses this by converting student profile data into interpretable readiness scores and using those scores to recommend roles such as:

- AI Engineer
- Machine Learning Engineer
- Data Scientist
- Data Analyst
- Business Analyst

The system is designed as a practical portfolio project that demonstrates data preprocessing, feature engineering, recommendation logic, career-readiness scoring, and an interactive Streamlit user interface.

---

## Features

- Interactive Streamlit dashboard for student profile input
- Career readiness score calculation
- Career recommendation engine with ranked role suggestions
- Skill gap analysis for the top recommended role
- Personalized learning plan based on missing skills
- 90-day roadmap generator for supported career paths
- Feature engineering pipeline for composite readiness scores
- EDA scripts and saved visualization reports
- Model training and prediction scripts for career readiness experimentation

---

## Architecture Diagram

```text
CareerCompass AI
|
+-- data/
|   +-- Raw student career dataset
|   +-- Engineered feature dataset
|
+-- src/
|   +-- eda.py
|   |   +-- Exploratory analysis and report plots
|   |
|   +-- features.py
|   |   +-- Composite readiness score generation
|   |
|   +-- train.py
|   |   +-- Career readiness model training
|   |
|   +-- predict.py
|   |   +-- Career readiness prediction utility
|   |
|   +-- recommender.py
|   |   +-- Career recommendation engine
|   |
|   +-- skill_gap.py
|   |   +-- Role-specific skill gap analysis
|   |
|   +-- roadmap_generator.py
|       +-- 90-day learning roadmap generation
|
+-- app/
|   +-- app1.py
|       +-- Streamlit user interface
|
+-- models/
|   +-- Saved model artifact
|
+-- reports/
    +-- EDA visualizations
```

---

## Dataset

The project uses a student placement and career success dataset containing academic, technical, professional, and activity-related features.

Example columns include:

- CGPA
- DSA Problems Solved
- Internships
- Certifications
- Projects Count
- Communication Skills
- Aptitude Test Score
- LeetCode Rating
- GitHub Contributions
- Hackathons Participated
- AI/ML Skill Level
- System Design Knowledge
- Resume Score
- Mock Interview Score
- Placement Status
- Salary LPA

The dataset is stored in:

```text
data/student_placement_career_success_dataset_2026.csv
```

The engineered dataset is stored in:

```text
data/engineered_data.csv
```

---

## Feature Engineering

The feature engineering pipeline creates composite scores that summarize student readiness across multiple dimensions.

Generated features include:

- **Employability Score**: combines CGPA, DSA practice, internships, certifications, projects, resume quality, and mock interview performance.
- **Technical Strength Score**: combines DSA, LeetCode rating, GitHub contributions, AI/ML skill level, and system design knowledge.
- **Professional Readiness Score**: combines communication skills, resume score, mock interview performance, and internship experience.
- **Activity Score**: combines projects, hackathons, and GitHub contributions.

These scores help make the recommendation output more interpretable than using raw columns directly.

Run feature engineering:

```bash
python src/features.py
```

---

## Career Recommendation Engine

The recommendation engine ranks career paths based on weighted combinations of the engineered readiness scores.

For example:

- AI Engineer roles prioritize technical strength, activity, and employability.
- Machine Learning Engineer roles prioritize technical strength, project activity, and professional readiness.
- Data Analyst and Business Analyst roles give more importance to communication, analytical ability, and professional readiness.

The output includes:

- Recommended career role
- Match percentage
- Explanation for the recommendation
- Overall career readiness score

Core file:

```text
src/recommender.py
```

---

## Skill Gap Analysis

The skill gap module compares the student's profile against the expected skills for the recommended career path.

It identifies:

- Current strengths
- Missing or weak skills
- Learning actions for improvement
- Next recommended action

Supported roles include:

- AI Engineer
- Machine Learning Engineer
- Data Scientist
- Data Analyst
- Software Engineer
- Business Analyst

Core file:

```text
src/skill_gap.py
```

---

## Roadmap Generator

The roadmap generator creates a 90-day learning plan for the selected career path.

Each roadmap is divided into:

- Month 1: fundamentals and base skills
- Month 2: intermediate learning and portfolio projects
- Month 3: advanced preparation, interview practice, and portfolio polish

Core file:

```text
src/roadmap_generator.py
```

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd CareerCompass-AI
```

Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

Run the Streamlit app:

```bash
streamlit run app/app1.py
```

Run exploratory data analysis:

```bash
python src/eda.py
```

Generate engineered features:

```bash
python src/features.py
```

Train the career readiness model:

```bash
python src/train.py
```

Run prediction on sample input:

```bash
python src/predict.py
```

Run prediction on a custom CSV:

```bash
python src/predict.py --input data/new_students.csv
```

---

## Screenshots

Add screenshots of the Streamlit interface here after running the app.

### Dashboard

```text
screenshots/dashboard.png
```

### Career Recommendations

```text
screenshots/recommendations.png
```

### Skill Gap Analysis

```text
screenshots/skill_gap.png
```

### 90-Day Roadmap

```text
screenshots/roadmap.png
```

---

## Limitations

- The current recommendation engine is primarily rule-based and uses manually defined weights.
- The dataset's placement target may not represent a real-world balanced placement outcome, so model results should be interpreted as career readiness experimentation rather than a definitive hiring outcome.
- Skill thresholds are simple and may need refinement using expert input or real hiring data.
- Roadmaps are static templates and are not yet fully personalized to every individual skill gap.
- The system does not validate whether user-entered scores are based on standardized assessments.

---

## Future Improvements

- Add clearer score explanations for each recommended career.
- Use consistent scoring functions between the feature engineering pipeline and Streamlit app.
- Improve role-specific thresholds for skill gap analysis.
- Personalize roadmaps directly from identified gaps.
- Add model evaluation metrics beyond accuracy, such as precision, recall, F1-score, and confusion matrix.
- Add sample screenshots to improve GitHub presentation.
- Add a short project report explaining methodology, assumptions, and results.

---

## Portfolio Value

CareerCompass AI demonstrates practical skills relevant to internships and entry-level AI/ML roles:

- Python programming
- Data preprocessing
- Feature engineering
- Model training workflow
- Recommendation system logic
- Streamlit application development
- Explainable scoring
- Career-focused product thinking

This project is suitable for showcasing an end-to-end data application that turns student profile data into actionable career guidance.
