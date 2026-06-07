import pandas as pd


CAREER_SKILLS = {
    "AI Engineer": {
        "AI_ML_Skill_Level": "Machine Learning & Deep Learning",
        "DSA_Problems_Solved": "Data Structures & Algorithms",
        "Projects_Count": "AI/ML Projects",
        "System_Design_Knowledge": "System Design"
    },

    "Data Scientist": {
        "AI_ML_Skill_Level": "Machine Learning",
        "Projects_Count": "Data Science Projects",
        "Aptitude_Test_Score": "Statistics & Analytics",
        "Communication_Skills": "Business Communication"
    },

    "Software Engineer": {
        "DSA_Problems_Solved": "Data Structures & Algorithms",
        "Projects_Count": "Software Projects",
        "GitHub_Contributions": "Open Source Contributions",
        "System_Design_Knowledge": "System Design"
    },

    "Business Analyst": {
        "Communication_Skills": "Communication Skills",
        "Resume_Score": "Professional Profile",
        "Mock_Interview_Score": "Interview Readiness",
        "Aptitude_Test_Score": "Analytical Thinking"
    }
}


LEARNING_RESOURCES = {
    "AI_ML_Skill_Level":
        "Study Machine Learning, Deep Learning and AI fundamentals",

    "DSA_Problems_Solved":
        "Practice DSA daily on LeetCode and Codeforces",

    "Projects_Count":
        "Build 2-3 portfolio projects and publish them on GitHub",

    "System_Design_Knowledge":
        "Learn System Design basics and scalability concepts",

    "Communication_Skills":
        "Practice public speaking, presentations and mock interviews",

    "Resume_Score":
        "Improve resume, LinkedIn profile and project descriptions",

    "Mock_Interview_Score":
        "Attend mock interviews and behavioral interview practice",

    "Aptitude_Test_Score":
        "Strengthen quantitative aptitude and logical reasoning",

    "GitHub_Contributions":
        "Contribute to open-source projects regularly"
}


class SkillGapAnalyzer:

    def __init__(self, data_path):
        self.df = pd.read_csv(data_path)

    def analyze_skill_gap(self, student, target_role):

        required_skills = CAREER_SKILLS[target_role]

        strengths = []
        gaps = []

        for column, display_name in required_skills.items():

            value = student[column]

            if value >= 60:
                strengths.append(display_name)

            else:
                gaps.append(display_name)

        return strengths, gaps

    def get_skill_gap_report(self, student, target_role):

        strengths, gaps = self.analyze_skill_gap(
            student,
            target_role
        )

        total_skills = len(strengths) + len(gaps)

        readiness = round(
            (len(strengths) / total_skills) * 100,
            1
        )

        learning_plan = []

        for column, display_name in CAREER_SKILLS[target_role].items():

            if display_name in gaps:

                if column in LEARNING_RESOURCES:

                    learning_plan.append(
                        LEARNING_RESOURCES[column]
                    )

        if readiness >= 80:

            next_action = (
                "Focus on advanced projects and internships."
            )

        elif readiness >= 50:

            next_action = (
                "Improve the identified gaps and build more projects."
            )

        else:

            next_action = (
                "Strengthen core skills before targeting this role."
            )

        return {
            "target_role": target_role,
            "readiness": readiness,
            "strengths": strengths,
            "gaps": gaps,
            "learning_plan": learning_plan,
            "next_action": next_action
        }


if __name__ == "__main__":

    analyzer = SkillGapAnalyzer(
        "data/engineered_data.csv"
    )

    student = analyzer.df.iloc[0]

    report = analyzer.get_skill_gap_report(
        student,
        "AI Engineer"
    )

    print("\nSKILL GAP REPORT\n")

    print(
        f"Target Role: {report['target_role']}"
    )

    print(
        f"Readiness: {report['readiness']}%"
    )

    print("\nStrengths:")

    for item in report["strengths"]:
        print("-", item)

    print("\nGaps:")

    for item in report["gaps"]:
        print("-", item)

    print("\nLearning Plan:")

    for item in report["learning_plan"]:
        print("-", item)