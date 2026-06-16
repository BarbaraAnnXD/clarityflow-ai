import streamlit as st

from econ_mode import load_career_paths, score_paths


st.set_page_config(
    page_title="ClarityFlow AI",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 ClarityFlow AI")
st.subheader("Life Decision Simulator for Career Crossroads")

st.write(
    "ClarityFlow AI helps you compare career paths using cost, time, risk, "
    "flexibility, credential value, and income urgency."
)

st.info(
    "Responsible AI note: This tool supports decision-making, but it does not make "
    "final life decisions for you. Review major choices with a mentor, advisor, "
    "or trusted person."
)

st.divider()

career_goal = st.text_input(
    "What career or direction are you aiming for?",
    placeholder="Example: cybersecurity, data analytics, nursing, business owner..."
)

decision_question = st.text_area(
    "What path are you stuck between?",
    placeholder="Example: I don't know if I should finish my degree, do a bootcamp, self-teach, or get a job now."
)

st.subheader("ECON Mode: What matters most right now?")

col1, col2 = st.columns(2)

with col1:
    income_urgency = st.slider("How soon do you need income?", 1, 5, 3)
    budget_sensitivity = st.slider("How limited is your budget?", 1, 5, 3)
    flexibility_need = st.slider("How much flexibility do you need?", 1, 5, 3)

with col2:
    risk_aversion = st.slider("How much do you want to avoid risk?", 1, 5, 3)
    credential_importance = st.slider("How important is a formal credential?", 1, 5, 3)

st.divider()

if st.button("Simulate My Career Paths"):
    career_paths = load_career_paths()

    user_weights = {
        "income_urgency": income_urgency,
        "budget_sensitivity": budget_sensitivity,
        "flexibility_need": flexibility_need,
        "risk_aversion": risk_aversion,
        "credential_importance": credential_importance,
    }

    results = score_paths(career_paths, user_weights)

    top_path = results.iloc[0]

    st.subheader("Recommended Starting Path")
    st.success(f"Your strongest fit right now appears to be: **{top_path['path']}**")

    st.write("### Why this path ranked highest")
    st.write(top_path["notes"])

    st.write("### ECON Mode Comparison")
    st.dataframe(
        results[
            [
                "rank",
                "path",
                "score",
                "cost_level",
                "time_to_result",
                "risk_level",
                "flexibility",
                "credential_strength",
                "income_speed",
                "notes",
            ]
        ],
        use_container_width=True,
    )

    st.write("### Reality Check")
    st.warning(
        "This ranking is based on general pathway assumptions and your current priority sliders. "
        "It does not guarantee income, job placement, program quality, or future success."
    )

    st.write("### First 7-Day Plan")
    st.markdown(
        f"""
        **Day 1:** Write down the exact career role you want to test: `{career_goal or "your target role"}`  
        **Day 2:** Find 5 real job posts and list the skills they repeat.  
        **Day 3:** Compare those skills against your top path: **{top_path['path']}**.  
        **Day 4:** Identify one low-cost action you can take this week.  
        **Day 5:** Ask a mentor, advisor, instructor, or trusted person to review your plan.  
        **Day 6:** Check the cost, time, and risk assumptions again.  
        **Day 7:** Decide whether to continue, adjust, or test a backup path.
        """
    )