import pandas as pd


class CareerRecommender:

    def __init__(self, data_path):
        self.df = pd.read_csv(data_path)

    def calculate_scores(self, student):

        return {
            "technical": student["Technical_Strength_Score"],
            "professional": student["Professional_Readiness_Score"],
            "activity": student["Activity_Score"],
            "employability": student["Employability_Score"]
        }

    def normalize_student_profile(self, student):

        return {
            "ai_ml": student["AI_ML_Skill_Level"],
            "system_design": student["System_Design_Knowledge"],
            "communication": student["Communication_Skills"],
            "resume": student["Resume_Score"],
            "aptitude": student["Aptitude_Test_Score"],
            "technical": student["Technical_Strength_Score"],
            "professional": student["Professional_Readiness_Score"],
            "dsa": min(student["DSA_Problems_Solved"] / 500 * 100, 100),
            "projects": min(student["Projects_Count"] / 10 * 100, 100),
            "github": min(student["GitHub_Contributions"] / 100 * 100, 100),
            "internships": min(student.get("Internships", 0) / 3 * 100, 100)
        }

    def recommend_careers(self, student):

        profile = self.normalize_student_profile(student)

        careers = {
            "AI Engineer":
                profile["ai_ml"] * 0.35 +
                profile["system_design"] * 0.20 +
                profile["projects"] * 0.20 +
                profile["github"] * 0.15 +
                profile["dsa"] * 0.10,

            "Machine Learning Engineer":
                profile["ai_ml"] * 0.30 +
                profile["dsa"] * 0.25 +
                profile["projects"] * 0.20 +
                profile["github"] * 0.15 +
                profile["technical"] * 0.10,

            "Data Scientist":
                profile["ai_ml"] * 0.25 +
                profile["aptitude"] * 0.25 +
                profile["projects"] * 0.20 +
                profile["communication"] * 0.15 +
                profile["technical"] * 0.15,

            "Data Analyst":
                profile["aptitude"] * 0.30 +
                profile["communication"] * 0.25 +
                profile["resume"] * 0.20 +
                profile["projects"] * 0.15 +
                profile["professional"] * 0.10,

            "Business Analyst":
                profile["communication"] * 0.35 +
                profile["aptitude"] * 0.25 +
                profile["resume"] * 0.20 +
                profile["professional"] * 0.15 +
                profile["internships"] * 0.05
        }

        ranked = sorted(
            careers.items(),
            key=lambda x: x[1],
            reverse=True
        )

        recommendations = []

        reasons = {
            "AI Engineer":
                "Best fit for strong AI/ML, system design, projects, and GitHub activity",

            "Machine Learning Engineer":
                "Best fit for strong ML, DSA, project implementation, and coding practice",

            "Data Scientist":
                "Best fit for ML, analytical thinking, data projects, and communication",

            "Data Analyst":
                "Best fit for aptitude, communication, resume strength, and analysis projects",

            "Business Analyst":
                "Best fit for communication, business readiness, aptitude, and professional profile"
        }

        for role, score in ranked:

            match_percent = round(
                score,
                1
            )

            recommendations.append(
                {
                    "role": role,
                    "match": match_percent,
                    "reason": reasons[role]
                }
            )

        return recommendations

    def get_career_report(self, student):

        scores = self.calculate_scores(student)

        career_readiness = round(
            (
                scores["technical"] +
                scores["professional"] +
                scores["activity"] +
                scores["employability"]
            ) / 4,
            2
        )

        recommendations = self.recommend_careers(student)

        strengths = []

        if scores["technical"] >= 60:
            strengths.append("Strong Technical Skills")

        if scores["professional"] >= 60:
            strengths.append("Good Communication & Interview Readiness")

        if scores["activity"] >= 60:
            strengths.append("Active Project Portfolio")

        improvements = []

        if scores["technical"] < 60:
            improvements.append("Improve technical skills")

        if scores["professional"] < 60:
            improvements.append("Improve communication and interview skills")

        if scores["activity"] < 60:
            improvements.append("Build more projects and participate in hackathons")

        return {
            "career_readiness": career_readiness,
            "recommendations": recommendations,
            "strengths": strengths,
            "improvements": improvements,
            "scores": scores
        }


if __name__ == "__main__":

    recommender = CareerRecommender(
        "data/engineered_data.csv"
    )

    student = recommender.df.iloc[0]

    report = recommender.get_career_report(
        student
    )

    print("\nCAREER REPORT\n")

    print(
        f"Career Readiness: {report['career_readiness']}%"
    )

    print("\nTop Recommendations:\n")

    for rec in report["recommendations"]:

        print(
            f"{rec['role']} ({rec['match']}%)"
        )
