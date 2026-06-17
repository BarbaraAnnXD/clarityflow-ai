def get_top_paths(results):
    """
    Returns the top recommended path and backup path.
    """
    top_path = results.iloc[0]
    backup_path = results.iloc[1] if len(results) > 1 else None
    return top_path, backup_path


def get_tradeoffs(path_name):
    """
    Provides path-specific hidden tradeoffs.
    """
    tradeoffs = {
        "Degree": [
            "Strong credential value, but higher cost and longer time before payoff.",
            "May open doors for roles requiring formal education.",
            "Can delay income if the user needs money quickly."
        ],
        "Bootcamp": [
            "Faster than a degree, but program quality varies a lot.",
            "Can build focused skills quickly if the user has time and discipline.",
            "May create debt without guaranteeing job placement."
        ],
        "Self-Taught": [
            "Low cost and flexible, but the user must prove skills through projects.",
            "Works best for users who can stay consistent without external structure.",
            "May be harder for employers to trust without certifications, portfolio work, or experience."
        ],
        "Job Now": [
            "Fastest income path, but may slow long-term skill-building.",
            "Can reduce financial pressure while the user builds skills on the side.",
            "Risk: the user may get stuck in survival mode and delay the career transition."
        ],
        "Graduate School": [
            "Strong advanced credential, but high cost and delayed income.",
            "Best when the target career truly requires advanced education.",
            "Risk: taking on debt without a clear role outcome."
        ],
        "Startup": [
            "High freedom and upside, but unstable income and high uncertainty.",
            "Works best when the user has a clear problem, support system, and runway.",
            "Risk: burnout or financial stress if the idea is not validated early."
        ],
    }

    return tradeoffs.get(path_name, ["This path has tradeoffs that should be reviewed before making a final decision."])


def get_reality_check(path_name):
    """
    Gives a direct risk warning based on the top path.
    """
    checks = {
        "Degree": "Verify total cost, financial aid, time to graduation, and whether your target role truly requires a degree.",
        "Bootcamp": "Check job placement claims, reviews, refund policies, total cost, and whether employers in your field respect the program.",
        "Self-Taught": "Make sure you have a project plan, accountability system, and proof of skills. Self-taught paths require visible evidence.",
        "Job Now": "Protect time for skill-building. Immediate income helps, but the long-term career goal can stall without a weekly learning plan.",
        "Graduate School": "Confirm that graduate school is required or strongly rewarded for your target role before taking on more cost or debt.",
        "Startup": "Validate the idea with real users before investing too much time or money. Freedom is high, but stability is low."
    }

    return checks.get(path_name, "Review assumptions with a trusted human before making a major decision.")


def get_confidence_boost(path_name):
    """
    Gives a grounded confidence boost without fake hype.
    """
    return (
        f"You do not need perfect certainty to move forward. "
        f"The goal is to test **{path_name}** for the next 7 days, gather evidence, "
        f"and adjust before making a bigger commitment."
    )

def get_main_warning(top_path):
    """
    Gives the user one clear warning based on the strongest risk signal.
    This keeps the recommendation responsible and prevents overconfident advice.
    """

    if top_path["decision_clarity_level"] == "Low":
        return (
            "The career path scores are close together, so there is not one obvious winner yet. "
            "Compare the top path and backup path carefully before making a major commitment."
        )

    if top_path["confidence_level"] == "Low":
        return (
            "The top path and backup path are close. Treat this as a comparison, "
            "not a final decision. Test both before committing."
        )

    if top_path["affordability_stress"] >= 35:
        return (
            "This path may create high cost stress based on your budget priorities. "
            "Review costs, debt, and payment commitments before moving forward."
        )

    if top_path["risk_exposure"] >= 35:
        return (
            "This path has high risk exposure based on your income and budget pressure. "
            "Avoid major commitments until you verify the real-world risks."
        )

    if top_path["pressure_level"] == "High":
        return (
            "Your life pressure level is high, so avoid big irreversible decisions right now. "
            "Focus on a small 7-day test step before making a major change."
        )

    return (
        "No major danger signal is standing out, but this should still be treated as "
        "decision support, not a guaranteed outcome."
    )