import streamlit as st
import json
from datetime import datetime

from econ_mode import load_career_paths, score_paths
from decision_engine import (
    get_top_paths,
    get_tradeoffs,
    get_reality_check,
    get_main_warning,
    get_path_strategy_profile,
    get_result_reveal,
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

st.subheader("Clarity Mode")

response_mode = st.selectbox(
    "How do you want ClarityFlow to guide you?",
    [
        "Direct Mode — clear answer fast",
        "Coach Mode — supportive and steady",
        "Analyst Mode — explain the tradeoffs",
        "Checklist Mode — action steps only",
    ],
    help=(
        "This changes how the AI explains the decision map. "
        "The scoring engine stays the same."
    ),
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

    reveal = get_result_reveal(top_path["path"])

    st.markdown(
        f"""
        <div style="
            border-radius: 18px;
            padding: 28px;
            margin-top: 20px;
            margin-bottom: 20px;
            background: linear-gradient(135deg, #f4f7ff, #ffffff);
            border: 1px solid #d9e2ff;
            box-shadow: 0 4px 18px rgba(0,0,0,0.08);
            text-align: center;
        ">
            <div style="font-size: 54px;">{reveal["icon"]}</div>
            <div style="font-size: 18px; font-weight: 600; color: #555;">
                Your Starting Direction
            </div>
            <div style="font-size: 42px; font-weight: 800; margin-top: 6px; color: #111;">
                {reveal["title"]}
            </div>
            <div style="font-size: 18px; margin-top: 12px; color: #444;">
                {reveal["message"]}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Your Starting Plan")

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

    path_strategy_profile = get_path_strategy_profile(top_path["path"])

    ai_summary = generate_ai_summary(
        career_goal,
        decision_question,
        top_path,
        backup_path,
        results,
        path_strategy_profile,
        response_mode,
    )

    st.markdown(ai_summary)

    st.write("### Reality Check")
    st.warning(get_reality_check(top_path["path"]))

    st.caption(
        "This ranking is based on general pathway assumptions and your current priority sliders. "
        "It does not guarantee income, job placement, program quality, or future success."
    )

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

        st.dataframe(display_results, width="stretch", hide_index=True)

    st.divider()

    st.write("### Report Wrong or Harmful Output")

    st.caption(
        "Use this after reviewing the result. If the plan feels unsafe, biased, "
        "unrealistic, confusing, incorrect, or too confident, you can create a report."
    )

    with st.expander("Report this output"):
        st.warning(
            "Do not include private details, addresses, passwords, medical records, "
            "or emergency information. If this is an emergency, contact local emergency "
            "services or a trusted human support professional."
        )

        report_type = st.selectbox(
            "What kind of issue did you notice?",
            [
                "Wrong recommendation",
                "Unsafe advice",
                "Biased or unfair output",
                "Too confident",
                "Confusing explanation",
                "Checklist not realistic",
                "Other",
            ],
        )

        report_severity = st.selectbox(
            "How serious is the issue?",
            [
                "Low - wording issue",
                "Medium - could confuse someone",
                "High - could cause harm if followed",
            ],
        )

        report_notes = st.text_area(
            "Describe what felt wrong or harmful.",
            placeholder=(
                "Example: The app recommended an expensive path even though "
                "the user had a very tight budget."
            ),
            height=120,
        )

        report_data = {
            "timestamp": datetime.now().isoformat(),
            "reported_issue_type": report_type,
            "severity": report_severity,
            "user_decision_question": decision_question,
            "career_goal": career_goal,
            "top_path": top_path["path"],
            "backup_path": backup_path["path"] if backup_path is not None else "None",
            "overall_match": float(top_path["fit_percent"]),
            "confidence_level": top_path["confidence_level"],
            "decision_clarity": top_path["decision_clarity_level"],
            "life_pressure_level": top_path["pressure_level"],
            "cost_stress": float(top_path["affordability_stress"]),
            "risk_exposure": float(top_path["risk_exposure"]),
            "report_notes": report_notes,
        }

        st.download_button(
            label="Download Report File",
            data=json.dumps(report_data, indent=2),
            file_name="clarityflow_output_report.json",
            mime="application/json",
        )

        st.markdown(
            """
            After downloading the report file, email it to:

            **clarityflow.reports@example.com**

            [Open email draft](mailto:clarityflow.reports@example.com?subject=ClarityFlow%20Output%20Report&body=Please%20attach%20the%20downloaded%20clarityflow_output_report.json%20file%20to%20this%20email.)
            """
        )

        st.caption(
            "Prototype note: In a full version, this report would go to a human review queue. "
            "For this demo, the user downloads the report and emails it for review."
        )