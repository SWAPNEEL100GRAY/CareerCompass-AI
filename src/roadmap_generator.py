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

    def generate_roadmap(self, career):

        roadmap = self.ROADMAPS.get(career)

        if not roadmap:
            print("Roadmap not available.")
            return

        print("\n" + "=" * 60)
        print("90 DAY CAREER ROADMAP")
        print("=" * 60)

        print(f"\nTarget Career: {career}")

        for month, tasks in roadmap.items():

            print(f"\n{month}")
            print("-" * 30)

            for i, task in enumerate(tasks, start=1):
                print(f"{i}. {task}")

        print("\nFinal Goal:")
        print("Build a portfolio project and prepare for interviews.")

        print("\n" + "=" * 60)


if __name__ == "__main__":

    career = "AI Engineer"

    generator = RoadmapGenerator()

    generator.generate_roadmap(career)