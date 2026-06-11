class RoadmapGenerator:

    ROADMAPS = {

        "AI Engineer": {
            "Month 1": [
                "Python for AI",
                "Statistics Basics",
                "Machine Learning Fundamentals",
                "Mini ML Project"
            ],

            "Month 2": [
                "Deep Learning",
                "Neural Networks",
                "TensorFlow / PyTorch",
                "AI Project"
            ],

            "Month 3": [
                "System Design Basics",
                "Docker Fundamentals",
                "Model Deployment",
                "Mock Interviews"
            ]
        },

        "Machine Learning Engineer": {
            "Month 1": [
                "Python for ML",
                "Statistics & Probability",
                "Supervised Learning",
                "Regression / Classification Project"
            ],

            "Month 2": [
                "Feature Engineering",
                "Model Evaluation",
                "Scikit-learn Pipelines",
                "End-to-End ML Project"
            ],

            "Month 3": [
                "Deep Learning Basics",
                "Experiment Tracking",
                "Model Deployment Basics",
                "ML Interview Preparation"
            ]
        },

        "Data Scientist": {
            "Month 1": [
                "Python",
                "Pandas",
                "NumPy",
                "Data Cleaning Project"
            ],

            "Month 2": [
                "Statistics",
                "Machine Learning",
                "Data Visualization",
                "Dashboard Project"
            ],

            "Month 3": [
                "Feature Engineering",
                "Advanced ML",
                "Case Studies",
                "Interview Preparation"
            ]
        },

        "Data Analyst": {
            "Month 1": [
                "Excel / Spreadsheets",
                "SQL Fundamentals",
                "Python for Data Analysis",
                "Data Cleaning Project"
            ],

            "Month 2": [
                "Pandas",
                "Data Visualization",
                "Statistics Basics",
                "Exploratory Analysis Project"
            ],

            "Month 3": [
                "Dashboard Building",
                "Business Metrics",
                "Case Study Presentation",
                "Portfolio Polish"
            ]
        },

        "Software Engineer": {
            "Month 1": [
                "DSA",
                "OOP",
                "Git & GitHub",
                "Mini Project"
            ],

            "Month 2": [
                "Backend Development",
                "Databases",
                "APIs",
                "Full Stack Project"
            ],

            "Month 3": [
                "System Design",
                "Deployment",
                "Mock Interviews",
                "Portfolio Building"
            ]
        },

        "Business Analyst": {
            "Month 1": [
                "Excel",
                "SQL",
                "Communication Skills",
                "Business Case Studies"
            ],

            "Month 2": [
                "Power BI",
                "Tableau",
                "Data Analysis",
                "Dashboard Project"
            ],

            "Month 3": [
                "Stakeholder Communication",
                "Presentation Skills",
                "Interview Preparation",
                "Portfolio Building"
            ]
        }
    }

    def get_roadmap(self, career):

        roadmap = self.ROADMAPS.get(career)

        if not roadmap:

            return {
                "career": career,
                "roadmap": {},
                "goal": "Roadmap not available."
            }

        return {
            "career": career,
            "roadmap": roadmap,
            "goal": "Build a portfolio project and prepare for interviews."
        }


if __name__ == "__main__":

    generator = RoadmapGenerator()

    report = generator.get_roadmap(
        "AI Engineer"
    )

    print("\nROADMAP REPORT\n")

    print(
        f"Career: {report['career']}"
    )

    for month, tasks in report["roadmap"].items():

        print(f"\n{month}")

        for task in tasks:
            print("-", task)

    print(
        f"\nGoal: {report['goal']}"
    )
