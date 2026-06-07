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

    def recommend_careers(self, student):

        scores = self.calculate_scores(student)

        careers = {
            "AI Engineer":
                scores["technical"] * 0.60 +
                scores["activity"] * 0.20 +
                scores["employability"] * 0.20,

            "Machine Learning Engineer":
                scores["technical"] * 0.55 +
                scores["activity"] * 0.25 +
                scores["professional"] * 0.20,

            "Data Scientist":
                scores["technical"] * 0.50 +
                scores["professional"] * 0.30 +
                scores["employability"] * 0.20,

            "Data Analyst":
                scores["technical"] * 0.40 +
                scores["professional"] * 0.40 +
                scores["employability"] * 0.20,

            "Business Analyst":
                scores["professional"] * 0.50 +
                scores["employability"] * 0.30 +
                scores["activity"] * 0.20
        }

        ranked = sorted(
            careers.items(),
            key=lambda x: x[1],
            reverse=True
        )

        max_score = ranked[0][1]

        recommendations = []

        for role, score in ranked:

            match_percent = round(
                (score / max_score) * 100,
                1
            )

            if "AI" in role or "Machine Learning" in role:
                reason = "Strong technical and AI profile"

            elif "Data" in role:
                reason = "Good analytical and problem-solving ability"

            elif "Business" in role:
                reason = "Strong communication and professional readiness"

            else:
                reason = "Balanced profile"

            recommendations.append(
                {
                    "role": role,
                    "match": match_percent,
                    "reason": reason
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