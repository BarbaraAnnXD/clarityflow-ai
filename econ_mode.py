import pandas as pd


def load_career_paths(file_path="data/career_paths.csv"):
    """
    Loads the career path data from the CSV file.
    """
    return pd.read_csv(file_path)


def score_paths(career_paths, user_weights):
    """
    Scores each career path based on the user's priorities.

    Higher score = better fit for the user's current situation.
    """

    scored_paths = career_paths.copy()

    scored_paths["score"] = (
        scored_paths["income_speed"] * user_weights["income_urgency"]
        + (6 - scored_paths["cost_level"]) * user_weights["budget_sensitivity"]
        + scored_paths["flexibility"] * user_weights["flexibility_need"]
        + (6 - scored_paths["risk_level"]) * user_weights["risk_aversion"]
        + scored_paths["credential_strength"] * user_weights["credential_importance"]
    )

    scored_paths = scored_paths.sort_values(by="score", ascending=False)
    scored_paths["rank"] = range(1, len(scored_paths) + 1)

    return scored_paths