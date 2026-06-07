import pandas as pd


CAREER_SKILLS = {
    "AI Engineer": {
        "AI_ML_Skill_Level": "Machine Learning & Deep Learning",
        "DSA_Problems_Solved": "Data Structures & Algorithms",
        "Projects_Count": "AI/ML Projects",
        "System_Design_Knowledge": "System Design",
    },

    "Data Scientist": {
        "AI_ML_Skill_Level": "Machine Learning",
        "Projects_Count": "Data Science Projects",
        "Aptitude_Test_Score": "Statistics & Analytics",
        "Communication_Skills": "Business Communication",
    },

    "Software Engineer": {
        "DSA_Problems_Solved": "Data Structures & Algorithms",
        "Projects_Count": "Software Projects",
        "GitHub_Contributions": "Open Source Contributions",
        "System_Design_Knowledge": "System Design",
    },

    "Business Analyst": {
        "Communication_Skills": "Communication Skills",
        "Resume_Score": "Professional Profile",
        "Mock_Interview_Score": "Interview Readiness",
        "Aptitude_Test_Score": "Analytical Thinking",
    }
}


LEARNING_RESOURCES = {
    "AI_ML_Skill_Level": "Study Machine Learning, Deep Learning and AI fundamentals",

    "DSA_Problems_Solved": "Practice DSA daily on LeetCode and Codeforces",

    "Projects_Count": "Build 2-3 portfolio projects and publish them on GitHub",

    "System_Design_Knowledge": "Learn System Design basics and scalability concepts",

    "Communication_Skills": "Practice public speaking, presentations and mock interviews",

    "Resume_Score": "Improve resume, LinkedIn profile and project descriptions",

    "Mock_Interview_Score": "Attend mock interviews and behavioral interview practice",

    "Aptitude_Test_Score": "Strengthen quantitative aptitude and logical reasoning",

    "GitHub_Contributions": "Contribute to open-source projects regularly"
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
                gaps.append((display_name, column))

        return strengths, gaps

    def generate_report(self, student, target_role):

        strengths, gaps = self.analyze_skill_gap(
            student,
            target_role
        )

        total_skills = len(strengths) + len(gaps)

        readiness = round(
            (len(strengths) / total_skills) * 100,
            1
        )

        print("\n" + "=" * 60)
        print("CAREER SKILL GAP ANALYSIS REPORT")
        print("=" * 60)

        print(f"\nTarget Career: {target_role}")

        print(f"\nCareer Readiness Score: {readiness}%")

        print("\nCurrent Strengths:")

        if strengths:
            for skill in strengths:
                print(f"✓ {skill}")
        else:
            print("No major strengths identified yet.")

        print("\nPriority Skills To Improve:")

        if gaps:
            for i, (skill_name, _) in enumerate(gaps, start=1):
                print(f"{i}. {skill_name}")
        else:
            print("No major skill gaps detected.")

        print("\nRecommended Learning Plan:")

        if gaps:
            for _, column_name in gaps:

                if column_name in LEARNING_RESOURCES:
                    print(
                        f"- {LEARNING_RESOURCES[column_name]}"
                    )

        print("\nNext Action:")

        if readiness >= 80:
            print(
                "You are close to being industry-ready. Focus on advanced projects and internships."
            )

        elif readiness >= 50:
            print(
                "You have a solid foundation. Improve the identified gaps and build more projects."
            )

        else:
            print(
                "Focus on strengthening core skills before targeting this role."
            )

        print("\n" + "=" * 60)


if __name__ == "__main__":

    analyzer = SkillGapAnalyzer(
        "data/engineered_data.csv"
    )

    student = analyzer.df.iloc[0]

    target_role = "AI Engineer"

    analyzer.generate_report(
        student,
        target_role
    )