import pandas as pd
import numpy as np


def load_career_paths(file_path="data/career_paths.csv"):
    """
    Loads the career path data from the CSV file.
    """
    return pd.read_csv(file_path)


def get_pressure_level(pressure_score):
    """
    Converts the user's pressure score into a simple label.
    """
    if pressure_score >= 7:
        return "High"
    elif pressure_score >= 4:
        return "Moderate"
    else:
        return "Low"


def get_confidence_level(confidence_gap_percent):
    """
    Converts the percent gap between the top two paths into a confidence label.
    A small percent gap means the user should compare both paths carefully.
    """
    if confidence_gap_percent >= 25:
        return "Strong"
    elif confidence_gap_percent >= 10:
        return "Moderate"
    else:
        return "Low"


def calculate_gini(values):
    """
    Calculates a Gini-style score spread.

    Traditional Gini measures inequality in a distribution.
    Here, we adapt the idea to measure how spread out the career path scores are.

    Low Gini = career paths are close together, so the decision is less clear.
    High Gini = one or more paths clearly stand out, so the decision is clearer.
    """
    values = np.array(values, dtype=float)

    if len(values) == 0:
        return 0

    if np.amin(values) < 0:
        values = values - np.amin(values)

    if np.sum(values) == 0:
        return 0

    values = np.sort(values)
    n = len(values)
    index = np.arange(1, n + 1)

    gini = (2 * np.sum(index * values)) / (n * np.sum(values)) - (n + 1) / n

    return round(gini, 3)


def get_decision_clarity_level(gini_score):
    """
    Converts the Gini-style score spread into a user-friendly clarity label.
    """
    if gini_score >= 0.18:
        return "High"
    elif gini_score >= 0.08:
        return "Moderate"
    else:
        return "Low"

def get_momentum_level(momentum_multiplier):
    """
    Converts the Momentum Multiplier into a user-friendly label.
    """

    if momentum_multiplier >= 1.5:
        return "High"
    elif momentum_multiplier >= 1.0:
        return "Moderate"
    else:
        return "Low"

def get_factor_impact_label(value):
    """
    Converts a factor contribution into a simple user-facing impact label.
    """

    if value >= 40:
        return "Very high impact"
    elif value >= 25:
        return "High impact"
    elif value >= 12:
        return "Moderate impact"
    elif value > 0:
        return "Low impact"
    else:
        return "No impact"


def score_paths(career_paths, user_weights):
    """
    Scores each career path based on the user's priorities.

    This is the ECON-style decision engine.

    Higher fit_score = better fit for the user's current situation.
    The AI does not create this score. The score is calculated here using
    transparent weighted logic.
    """

    scored_paths = career_paths.copy()

    # Convert raw path traits into easier-to-understand decision factors.
    # The CSV uses 1-5 scores.
    # For cost, time, and risk: lower is usually better.
    scored_paths["affordability_score"] = 6 - scored_paths["cost_level"]
    scored_paths["speed_score"] = 6 - scored_paths["time_to_result"]
    scored_paths["safety_score"] = 6 - scored_paths["risk_level"]

    # Main fit score.
    # User sliders are 1-10.
    # Each contribution shows how much that factor affected the overall match.
    scored_paths["income_contribution"] = (
        scored_paths["income_speed"] * user_weights["income_urgency"]
    )

    scored_paths["budget_contribution"] = (
        scored_paths["affordability_score"] * user_weights["budget_sensitivity"]
    )

    scored_paths["flexibility_contribution"] = (
        scored_paths["flexibility"] * user_weights["flexibility_need"]
    )

    scored_paths["risk_contribution"] = (
        scored_paths["safety_score"] * user_weights["risk_aversion"]
    )

    scored_paths["credential_contribution"] = (
        scored_paths["credential_strength"] * user_weights["credential_importance"]
    )

    scored_paths["fit_score"] = (
        scored_paths["income_contribution"]
        + scored_paths["budget_contribution"]
        + scored_paths["flexibility_contribution"]
        + scored_paths["risk_contribution"]
        + scored_paths["credential_contribution"]
    )

    scored_paths["income_impact"] = scored_paths["income_contribution"].apply(
        get_factor_impact_label
    )
    scored_paths["budget_impact"] = scored_paths["budget_contribution"].apply(
        get_factor_impact_label
    )
    scored_paths["flexibility_impact"] = scored_paths[
        "flexibility_contribution"
    ].apply(get_factor_impact_label)
    scored_paths["risk_impact"] = scored_paths["risk_contribution"].apply(
        get_factor_impact_label
    )
    scored_paths["credential_impact"] = scored_paths[
        "credential_contribution"
    ].apply(get_factor_impact_label)

    # Maximum possible fit score:
    # each career path factor maxes at 5, and each user slider maxes at 10.
    max_possible_score = 5 * (
        user_weights["income_urgency"]
        + user_weights["budget_sensitivity"]
        + user_weights["flexibility_need"]
        + user_weights["risk_aversion"]
        + user_weights["credential_importance"]
    )

    scored_paths["fit_percent"] = (
        scored_paths["fit_score"] / max_possible_score * 100
    ).round(1)

    # User pressure score.
    # This shows whether the user has urgent life constraints.
    pressure_score = (
        user_weights["income_urgency"]
        + user_weights["budget_sensitivity"]
        + user_weights["flexibility_need"]
        + user_weights["risk_aversion"]
    ) / 4

    scored_paths["pressure_score"] = round(pressure_score, 1)
    scored_paths["pressure_level"] = get_pressure_level(pressure_score)

    # Affordability stress:
    # expensive path + tight budget = higher stress.
    scored_paths["affordability_stress"] = (
        scored_paths["cost_level"] * user_weights["budget_sensitivity"]
    )

    # Risk exposure:
    # risky path + income/budget pressure = higher exposure.
    financial_pressure = (
        user_weights["income_urgency"]
        + user_weights["budget_sensitivity"]
    ) / 2

    scored_paths["risk_exposure"] = (
        scored_paths["risk_level"] * financial_pressure
    ).round(1)

    # Gini-inspired Decision Clarity Index:
    # Measures how spread out all path scores are.
    # This helps show whether there is a clear winner or a crowded/tied decision.
    decision_clarity_index = calculate_gini(scored_paths["fit_score"])
    decision_clarity_level = get_decision_clarity_level(decision_clarity_index)

    scored_paths["decision_clarity_index"] = decision_clarity_index
    scored_paths["decision_clarity_level"] = decision_clarity_level

    # Momentum Multiplier:
    # Inspired by the macroeconomic multiplier idea.
    # Instead of GDP change / spending change, this estimates:
    # expected career movement / initial burden.
    #
    # Higher multiplier = more possible movement for less cost, time, and risk.
    expected_impact = (
        scored_paths["income_speed"]
        + scored_paths["credential_strength"]
        + scored_paths["flexibility"]
        + scored_paths["speed_score"]
    )

    initial_burden = (
        scored_paths["cost_level"]
        + scored_paths["time_to_result"]
        + scored_paths["risk_level"]
    )

    scored_paths["momentum_multiplier"] = (
        expected_impact / initial_burden
    ).round(2)

    scored_paths["momentum_level"] = scored_paths["momentum_multiplier"].apply(
        get_momentum_level
    )

    # Sort strongest path first.
    scored_paths = scored_paths.sort_values(by="fit_score", ascending=False)
    scored_paths["rank"] = range(1, len(scored_paths) + 1)

    # Confidence level:
    # based on the percent gap between the top path and backup path.
    # This is better than raw difference because a 10-point gap means
    # different things depending on how large the top score is.
    if len(scored_paths) > 1:
        top_score = scored_paths.iloc[0]["fit_score"]
        second_score = scored_paths.iloc[1]["fit_score"]

        confidence_gap = top_score - second_score

        if top_score > 0:
            confidence_gap_percent = (confidence_gap / top_score) * 100
        else:
            confidence_gap_percent = 0
    else:
        confidence_gap = 0
        confidence_gap_percent = 0

    scored_paths["confidence_gap"] = round(confidence_gap, 1)
    scored_paths["confidence_gap_percent"] = round(confidence_gap_percent, 1)
    scored_paths["confidence_level"] = get_confidence_level(confidence_gap_percent)

    # Keep old "score" column so the rest of the app does not break.
    scored_paths["score"] = scored_paths["fit_score"]

    return scored_paths