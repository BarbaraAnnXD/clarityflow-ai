import streamlit as st

from econ_mode import load_career_paths, score_paths
from decision_engine import (
    get_top_paths,
    get_tradeoffs,
    get_reality_check,
    get_confidence_boost,
    get_main_warning,
)
from ai_brain import generate_ai_summary


st.set_page_config(
    page_title="ClarityFlow AI",
    page_icon="🧠",
    layout="wide"
)

st.title("ClarityFlow AI")
st.subheader("Turn career noise into a clear next step.")

st.write(
    "You do not need to know the perfect career answer before using this. "
    "Start messy. ClarityFlow helps organize the options, tradeoffs, risks, "
    "and first steps."
)

st.info(
    "Responsible AI note: This tool supports decision-making, but it does not make "
    "final life decisions for you. Review major choices with a mentor, advisor, "
    "or trusted person."
)

st.divider()

decision_question = st.text_area(
    "What are you stuck between?",
    placeholder=(
        "Example: I don't know if I should finish my degree, do a bootcamp, "
        "teach myself, get a job now, start a business, or move for work."
    ),
    height=120
)

career_goal = st.text_input(
    "Optional: Do you have a career direction in mind?",
    placeholder=(
        "Example: cybersecurity, data analytics, healthcare, business... "
        "or leave blank if you don't know yet."
    )
)

st.subheader("Priority Check")
st.caption(
    "Move the sliders based on what feels true right now. "
    "ClarityFlow uses these behind the scenes to compare tradeoffs."
)

col1, col2 = st.columns(2)

with col1:
    income_urgency = st.slider(
        "How soon do you need income?",
        1,
        10,
        5,
        help="1 = no rush, 10 = I need income as soon as possible"
    )

    budget_sensitivity = st.slider(
        "How tight is your budget?",
        1,
        10,
        5,
        help="1 = I can invest money, 10 = I need low-cost options"
    )

    flexibility_need = st.slider(
        "How much flexibility do you need?",
        1,
        10,
        5,
        help="1 = I can follow a fixed schedule, 10 = I need flexibility around life/work/family"
    )

with col2:
    risk_aversion = st.slider(
        "How much do you want to avoid risk?",
        1,
        10,
        5,
        help="1 = I can handle uncertainty, 10 = I need the safer path"
    )

    credential_importance = st.slider(
        "How important is a formal credential?",
        1,
        10,
        5,
        help="1 = skills/projects matter more, 10 = degree/certificate proof matters a lot"
    )

st.caption(
    "Behind the scenes: the app compares cost, time, risk, flexibility, "
    "credential strength, and income speed."
)

st.divider()

if st.button("Build My Plan", type="primary"):
    if not decision_question.strip():
        st.warning(
            "Start by typing what you feel stuck between. "
            "It can be messy — that is the point."
        )
        st.stop()

    career_paths = load_career_paths()

    user_weights = {
        "income_urgency": income_urgency,
        "budget_sensitivity": budget_sensitivity,
        "flexibility_need": flexibility_need,
        "risk_aversion": risk_aversion,
        "credential_importance": credential_importance,
    }

    results = score_paths(career_paths, user_weights)
    top_path, backup_path = get_top_paths(results)

    st.subheader("Your Starting Plan")
    st.success(f"Strongest starting path right now: **{top_path['path']}**")

    if backup_path is not None:
        st.info(f"Backup path to compare: **{backup_path['path']}**")

    st.write("### Decision Snapshot")

    st.caption(
        "This snapshot explains why this path surfaced. "
        "It combines your priorities with the career path data."
    )

    metric_col1, metric_col2, metric_col3 = st.columns(3)

    with metric_col1:
        st.metric("Overall Match", f"{top_path['fit_percent']}%")

    with metric_col2:
        st.metric("Recommendation Confidence", top_path["confidence_level"])

    with metric_col3:
        st.metric("Decision Clarity", top_path["decision_clarity_level"])

    metric_col4, metric_col5, metric_col6 = st.columns(3)

    with metric_col4:
        st.metric("Momentum Multiplier", top_path["momentum_level"])

    with metric_col5:
        st.metric("Life Pressure Level", top_path["pressure_level"])

    with metric_col6:
        st.metric("Risk Exposure", top_path["risk_exposure"])

    metric_col7, metric_col8 = st.columns(2)

    with metric_col7:
        st.metric("Multiplier Score", top_path["momentum_multiplier"])

    with metric_col8:
        st.metric("Cost Stress", top_path["affordability_stress"])

    with st.expander("What do these numbers mean?"):
        st.markdown(
            """
            **Overall Match** shows how well the top path matches your current priorities.

            **Recommendation Confidence** shows how far ahead the top path is compared to the backup path.  
            If confidence is low, the top two paths are close and should be compared carefully.

            **Decision Clarity** uses a Gini-inspired score spread to check whether one path clearly stands out across all options.  
            If clarity is low, the path scores are close together and the user should compare options carefully.

            **Momentum Multiplier** is inspired by the economic multiplier idea.  
            Instead of measuring GDP change from spending, ClarityFlow estimates how much career movement a path may create compared to its initial cost, time, and risk.

            **Multiplier Score** is the numeric version of that idea.  
            Higher numbers suggest the path may create more momentum for less initial burden, but it is still an estimate, not a guaranteed outcome.

            **Life Pressure Level** shows how much pressure you may be under based on income urgency, budget, flexibility needs, and risk concerns.

            **Cost Stress** shows how financially stressful this path may be based on the path cost and your budget pressure.  
            Higher numbers mean the path may need more caution around cost, debt, or payment commitments.

            **Risk Exposure** shows how risky this path may feel based on the path risk level and your income/budget pressure.  
            Higher numbers mean the path should be tested carefully before making a major commitment.
            """
        )

    st.write("### Main Warning")
    st.warning(get_main_warning(top_path))

    st.write("### AI Strategy Plan")
    ai_summary = generate_ai_summary(
        career_goal,
        decision_question,
        top_path,
        backup_path,
        results,
    )
    st.markdown(ai_summary)

    st.write("### Reality Check")
    st.warning(get_reality_check(top_path["path"]))

    st.caption(
        "This ranking is based on general pathway assumptions and your current priority sliders. "
        "It does not guarantee income, job placement, program quality, or future success."
    )

    st.write("### Confidence Boost")
    st.info(get_confidence_boost(top_path["path"]))

    with st.expander("Optional: View Decision Map + scoring details"):
        st.write("### Why this path surfaced")
        st.write(top_path["notes"])

        st.write("### Hidden Tradeoffs")
        for tradeoff in get_tradeoffs(top_path["path"]):
            st.write(f"- {tradeoff}")

        st.write("### Path Comparison")

        display_results = results[
            [
                "rank",
                "path",
                "fit_percent",
                "confidence_level",
                "decision_clarity_index",
                "decision_clarity_level",
                "momentum_multiplier",
                "momentum_level",
                "pressure_level",
                "affordability_stress",
                "risk_exposure",
                "cost_level",
                "time_to_result",
                "risk_level",
                "flexibility",
                "credential_strength",
                "income_speed",
                "notes",
            ]
        ].reset_index(drop=True)

        st.dataframe(display_results, use_container_width=True, hide_index=True)