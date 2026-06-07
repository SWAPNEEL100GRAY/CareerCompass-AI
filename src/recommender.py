import pandas as pd


class CareerRecommender:

    def __init__(self, data_path):
        self.df = pd.read_csv(data_path)

    def calculate_scores(self, student):

        technical = (
            student["Technical_Strength_Score"]
        )

        professional = (
            student["Professional_Readiness_Score"]
        )

        activity = (
            student["Activity_Score"]
        )

        employability = (
            student["Employability_Score"]
        )

        return {
            "technical": technical,
            "professional": professional,
            "activity": activity,
            "employability": employability
        }

    def recommend_careers(self, student):

        scores = self.calculate_scores(student)

        careers = {}

        careers["Data Scientist"] = (
            scores["technical"] * 0.5 +
            scores["professional"] * 0.3 +
            scores["employability"] * 0.2
        )

        careers["AI Engineer"] = (
            scores["technical"] * 0.6 +
            scores["activity"] * 0.2 +
            scores["employability"] * 0.2
        )

        careers["Machine Learning Engineer"] = (
            scores["technical"] * 0.55 +
            scores["activity"] * 0.25 +
            scores["professional"] * 0.2
        )

        careers["Data Analyst"] = (
            scores["professional"] * 0.4 +
            scores["technical"] * 0.4 +
            scores["employability"] * 0.2
        )

        careers["Business Analyst"] = (
            scores["professional"] * 0.5 +
            scores["employability"] * 0.3 +
            scores["activity"] * 0.2
        )

        ranked = sorted(
            careers.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return ranked[:5]


if __name__ == "__main__":

    recommender = CareerRecommender(
        "data/engineered_data.csv"
    )

    student = recommender.df.iloc[0]

recommendations = recommender.recommend_careers(student)

scores = recommender.calculate_scores(student)

career_readiness = round(
    (
        scores["technical"] +
        scores["professional"] +
        scores["activity"] +
        scores["employability"]
    ) / 4,
    2
)

best_domain = recommendations[0][0]

print("\n" + "=" * 50)
print("CAREER RECOMMENDATION REPORT")
print("=" * 50)

print(f"\nCareer Readiness Score: {career_readiness}%")

print(f"\nBest Match: {best_domain}")

print("\nTop Career Recommendations:\n")

max_score = recommendations[0][1]

for idx, (role, score) in enumerate(recommendations, start=1):

    match_percent = round(
        (score / max_score) * 100,
        1
    )

    print(f"{idx}. {role}")
    print(f"   Match: {match_percent}%")

    if "AI" in role or "Machine Learning" in role:
        reason = "Strong technical and AI-related profile"

    elif "Data" in role:
        reason = "Good analytical and problem-solving ability"

    elif "Business" in role:
        reason = "Strong professional readiness and communication"

    else:
        reason = "Balanced overall profile"

    print(f"   Reason: {reason}\n")

print("Top Strengths:")
print(f"- Technical Strength: {round(scores['technical'],2)}")
print(f"- Professional Readiness: {round(scores['professional'],2)}")
print(f"- Employability: {round(scores['employability'],2)}")

print("\nAreas to Improve:")

if scores["technical"] < 60:
    print("- Improve technical skills")

if scores["professional"] < 60:
    print("- Improve communication and interview skills")

if scores["activity"] < 60:
    print("- Build more projects and participate in hackathons")

print("\nSuggested Next Step:")
print("- Continue building portfolio projects")
print("- Add internships and certifications")
print("- Improve domain-specific skills")