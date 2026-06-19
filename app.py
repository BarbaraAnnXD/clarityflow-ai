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
    get_priority_impact,
    get_option_aware_paths,
    detect_critical_situation,
)

from ai_brain import generate_ai_summary

st.set_page_config(
    page_title="ClarityFlow AI",
    page_icon="🧠",
    layout="wide"
)

st.markdown(
    """
    <style>
    /* Cyberpunk ClarityFlow theme */
    html, body, [class*="css"] {
        font-family: "Inter", "Segoe UI", Arial, sans-serif;
    }

    /* Main app background */
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(0, 255, 255, 0.12), transparent 28%),
            radial-gradient(circle at top right, rgba(255, 0, 200, 0.14), transparent 30%),
            linear-gradient(135deg, #070711 0%, #0b1020 45%, #120019 100%);
        color: #f5f7ff;
    }

    /* Custom app title */
    .app-title {
        font-size: 3.2rem;
        font-weight: 900;
        color: #ffffff;
        margin-top: 0.5rem;
        margin-bottom: 1.6rem;
        letter-spacing: 0.03em;
        text-shadow:
            0 0 14px rgba(0, 255, 255, 0.65),
            0 0 24px rgba(255, 0, 212, 0.25);
    }

    .app-subtitle {
        font-size: 1.6rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 1.4rem;
        text-shadow: 0 0 10px rgba(0, 245, 255, 0.35);
    }

    /* Main page titles and section labels */
    h1 {
        color: #ffffff;
        font-size: 2.7rem;
        line-height: 1.15;
        letter-spacing: 0.02em;
        text-shadow: 0 0 14px rgba(0, 255, 255, 0.55);
    }

    h2 {
        color: #ffffff;
        font-size: 2rem;
        line-height: 1.25;
        letter-spacing: 0.02em;
    }

    h3 {
        color: #7df9ff;
        font-size: 1.45rem;
        line-height: 1.3;
        margin-top: 1.4rem;
        margin-bottom: 0.6rem;
        letter-spacing: 0.02em;
    }

    /* Strong intro text */
    strong {
        font-size: 1.18rem;
        line-height: 1.6;
    }

    /* Regular text */
    p, li, label, span {
        color: #f5f7ff;
        font-size: 1.08rem;
        line-height: 1.65;
    }

    /* Captions and helper text */
    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] p {
        font-size: 1.12rem;
        line-height: 1.65;
        color: #d7e8ff;
    }

    /* Form labels */
    [data-testid="stWidgetLabel"] label,
    [data-testid="stWidgetLabel"] p {
        font-size: 1.25rem;
        font-weight: 800;
        color: #ffffff;
    }

    /* Slider text */
    [data-testid="stSlider"] label,
    [data-testid="stSlider"] p,
    [data-testid="stSlider"] span {
        font-size: 1.08rem;
    }

    /* Expander text */
    [data-testid="stExpander"] p,
    [data-testid="stExpander"] li,
    [data-testid="stExpander"] span {
        font-size: 1.06rem;
        line-height: 1.6;
    }

    /* Info / warning boxes */
    [data-testid="stAlert"] {
        border-radius: 16px;
        border: none;
        box-shadow: 0 0 18px rgba(0, 255, 255, 0.10);
        padding: 1rem 1.1rem;
    }

    /* Alert text size */
    [data-testid="stAlert"] p,
    [data-testid="stAlert"] div,
    [data-testid="stAlert"] span {
        font-size: 1.08rem;
        line-height: 1.6;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #00f5ff, #ff00d4);
        color: #050510;
        border: none;
        border-radius: 18px;
        font-size: 1.35rem;
        font-weight: 900;
        letter-spacing: 0.04em;
        padding: 1rem 2rem;
        min-height: 64px;
        box-shadow: 0 0 22px rgba(255, 0, 212, 0.45);
        transition: 0.2s ease-in-out;
    }

    /* Button text */
    .stButton > button p,
    .stButton > button span,
    .stButton > button div {
        font-size: 1.35rem !important;
        font-weight: 900 !important;
        color: #050510 !important;
        line-height: 1.2 !important;
    }

    /* Section title labels */
    .section-title {
        font-size: 1.75rem;
        font-weight: 900;
        color: #7df9ff;
        margin-top: 2rem;
        margin-bottom: 0.85rem;
        letter-spacing: 0.02em;
        text-shadow: 0 0 12px rgba(0, 245, 255, 0.45);
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 0 26px rgba(0, 245, 255, 0.55);
    }

    /* Inputs */
    textarea, input {
        background-color: #0d1224 !important;
        color: #ffffff !important;
        border: 1px solid rgba(125, 249, 255, 0.45) !important;
        border-radius: 12px !important;
    }

    textarea:focus, input:focus {
        border-color: #ff00d4 !important;
        box-shadow: 0 0 12px rgba(255, 0, 212, 0.35) !important;
    }

    /* Select boxes */
    [data-baseweb="select"] > div {
        background-color: #0d1224;
        border-color: rgba(125, 249, 255, 0.45);
        color: #ffffff;
        border-radius: 12px;
    }

    /* Sliders */
    [data-testid="stSlider"] {
        color: #7df9ff;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: rgba(13, 18, 36, 0.72);
        border: 1px solid rgba(125, 249, 255, 0.24);
        border-radius: 16px;
        padding: 16px;
        box-shadow: 0 0 16px rgba(0, 255, 255, 0.08);
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.85rem;
        font-weight: 700;
        color: #7df9ff;
    }

    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 800;
        line-height: 1.1;
        color: #ffffff;
        text-shadow: 0 0 12px rgba(255, 0, 212, 0.35);
    }

    /* Expanders */
    [data-testid="stExpander"] {
        background: rgba(13, 18, 36, 0.55);
        border: 1px solid rgba(125, 249, 255, 0.20);
        border-radius: 14px;
        box-shadow: 0 0 14px rgba(0, 245, 255, 0.06);
    }

    /* Dataframes */
    [data-testid="stDataFrame"] {
        margin-top: 0.5rem;
        border-radius: 14px;
        box-shadow: 0 0 18px rgba(0, 255, 255, 0.08);
    }

    /* AI Strategy Plan text size */
    .ai-strategy-text {
        font-size: 1.15rem;
        line-height: 1.7;
    }

    .ai-strategy-text p,
    .ai-strategy-text li {
        font-size: 1.15rem;
        line-height: 1.7;
    }

    .ai-strategy-text h3 {
        font-size: 1.35rem;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
        color: #7df9ff;
        text-shadow: 0 0 10px rgba(0, 245, 255, 0.35);
    }

    @media (max-width: 768px) {
        .ai-strategy-text,
        .ai-strategy-text p,
        .ai-strategy-text li {
            font-size: 1.15rem;
            line-height: 1.7;
        }

        .ai-strategy-text h3 {
            font-size: 1.45rem;
        }

        [data-testid="stMetricValue"] {
            font-size: 1.7rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="app-title">ClarityFlow AI</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">Turn career noise into a clear next step.</div>', unsafe_allow_html=True)

st.write(
    "You do not need to know the perfect career answer before using this. "
    "Start messy. ClarityFlow helps organize the options, tradeoffs, risks, "
    "and first steps."
)

st.info(
    "Responsible AI note: ClarityFlow is a decision-support prototype. "
    "It does not make final life or career commitments for the user, and it does not "
    "verify live salary, school, job-market, financial aid, or hiring data. "
    "Before acting, check trusted sources such as schools, employers, workforce offices, "
    "official program pages, advisors, mentors, counselors, or other trusted humans."
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

st.subheader("What matters most right now?")
st.caption(
    "Move the sliders based on your real life right now. "
    "There are no perfect answers — this just helps ClarityFlow compare your options."
)

col1, col2 = st.columns(2)

with col1:
    income_urgency = st.slider(
        "How quickly do you need your next paycheck?",
        1,
        10,
        5,
        help="1 = Money is not urgent, 10 = I need income as soon as possible"
    )

    budget_sensitivity = st.slider(
        "How tight is your budget?",
        1,
        10,
        5,
        help="1 = I can spend/invest money, 10 = I need the lowest-cost option"
    )

    flexibility_need = st.slider(
        "How much control do you need over your schedule?",
        1,
        10,
        5,
        help=(
            "1 = I can follow a fixed schedule, "
            "10 = I need control around work, family, transportation, or childcare"
        )
    )

with col2:
    risk_aversion = st.slider(
        "How much do you want to avoid risk?",
        1,
        10,
        5,
        help="1 = I can handle uncertainty, 10 = I need the option with less risk"
    )

    credential_importance = st.slider(
        "How much do you need a degree or certificate?",
        1,
        10,
        5,
        help="1 = skills/projects matter more, 10 = formal proof matters a lot"
    )

st.markdown('<div class="section-title">Clarity Mode</div>', unsafe_allow_html=True)

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

    critical_alert = detect_critical_situation(
        f"{decision_question} {career_goal}"
    )

    if critical_alert["is_critical"]:
        categories = ", ".join(critical_alert["categories"])

        st.warning("Stability-first notice")

        st.info(
            "Your message may involve an urgent stability or safety concern: "
            f"{categories}. Your career goals still matter, but immediate stability "
            "should come first."
        )

        st.warning(
            "ClarityFlow will keep this plan small, realistic, and focused. "
            "Before making major commitments like quitting a job, moving, enrolling, "
            "taking on debt, or accepting risky work, consider connecting with a trusted "
            "human, shelter or housing support, clinic, benefits office, school counselor, "
            "workforce center, or emergency service if you are in immediate danger."
        )

        st.caption(
            "This does not stop the decision map. It helps keep the next steps safer "
            "and more realistic for high-pressure situations."
        )

    career_paths = load_career_paths()

    user_weights = {
        "income_urgency": income_urgency,
        "budget_sensitivity": budget_sensitivity,
        "flexibility_need": flexibility_need,
        "risk_aversion": risk_aversion,
        "credential_importance": credential_importance,
    }

    option_awareness = get_option_aware_paths(decision_question)
    relevant_paths = option_awareness["relevant_paths"]

    if len(relevant_paths) >= 2:
        scoring_paths = career_paths[career_paths["path"].isin(relevant_paths)]
    else:
        scoring_paths = career_paths

    results = score_paths(scoring_paths, user_weights)
    top_path, backup_path = get_top_paths(results)

    reveal = get_result_reveal(top_path["path"])

    card_html = f"""<div style="
border-radius: 22px;
padding: 32px;
margin-top: 24px;
margin-bottom: 24px;
background:
    linear-gradient(135deg, rgba(13, 18, 36, 0.96), rgba(28, 0, 45, 0.94)),
    radial-gradient(circle at top left, rgba(0, 245, 255, 0.25), transparent 32%),
    radial-gradient(circle at bottom right, rgba(255, 0, 212, 0.22), transparent 35%);
border: 1px solid rgba(125, 249, 255, 0.55);
box-shadow:
    0 0 30px rgba(0, 245, 255, 0.20),
    inset 0 0 22px rgba(255, 0, 212, 0.08);
text-align: center;
position: relative;
overflow: hidden;
">
<div style="
font-size: 13px;
color: #7df9ff;
letter-spacing: 0.22em;
text-transform: uppercase;
margin-bottom: 14px;
text-shadow: 0 0 10px rgba(0, 245, 255, 0.55);
">
ClarityFlow Decision Scan
</div>

<div style="
font-size: 58px;
margin-bottom: 8px;
filter: drop-shadow(0 0 12px rgba(255, 0, 212, 0.45));
">
{reveal["icon"]}
</div>

<div style="
font-size: 17px;
font-weight: 700;
color: #7df9ff;
margin-top: 4px;
text-shadow: 0 0 10px rgba(0, 245, 255, 0.45);
">
Your Starting Direction
</div>

<div style="
font-size: 46px;
font-weight: 900;
margin-top: 8px;
color: #ffffff;
text-shadow:
    0 0 14px rgba(0, 245, 255, 0.45),
    0 0 22px rgba(255, 0, 212, 0.25);
">
{reveal["title"]}
</div>

<div style="
font-size: 18px;
margin-top: 14px;
color: #f5f7ff;
max-width: 760px;
margin-left: auto;
margin-right: auto;
line-height: 1.6;
">
{reveal["message"]}
</div>

<div style="
margin-top: 22px;
height: 3px;
width: 72%;
margin-left: auto;
margin-right: auto;
border-radius: 999px;
background: linear-gradient(90deg, transparent, #00f5ff, #ff00d4, transparent);
box-shadow: 0 0 16px rgba(0, 245, 255, 0.55);
"></div>
</div>"""

    st.markdown(card_html, unsafe_allow_html=True)

    st.subheader("Your Starting Plan")

    if backup_path is not None:
        st.info(f"Backup path to compare: **{backup_path['path']}**")

    st.write("### Decision Snapshot")

    st.caption(
        "This snapshot explains why this path surfaced. "
        "It combines your priorities with the career path data."
    )

    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

    with metric_col1:
        st.metric("Overall Match", f"{top_path['fit_percent']}%")

    with metric_col2:
        st.metric("Confidence", top_path["confidence_level"])

    with metric_col3:
        st.metric("Life Pressure", top_path["pressure_level"])

    with metric_col4:
        st.metric("Risk Exposure", top_path["risk_exposure"])

    with st.expander("Why did I get this result?"):
        st.write("### Options Detected")

        if option_awareness["detected_options"]:
            for detected_option in option_awareness["detected_options"]:
                matched_paths = ", ".join(detected_option["matched_paths"])
                st.info(
                    f"**{detected_option['option']}** appears connected to: {matched_paths}"
                )
        elif relevant_paths:
            st.info(
                "The app detected career signals in your decision question: "
                + ", ".join(relevant_paths)
            )
        else:
            st.caption(
                "No specific option keywords were detected, so the app used the full career path comparison."
            )

        st.write("### What Your Priorities Changed")

        for impact in get_priority_impact(user_weights):
            st.write(f"- {impact}")

        st.write("### Overall Match Breakdown")

        st.caption(
            "This shows which priority factors had the strongest effect on the top recommendation."
        )

        breakdown_data = [
            {
                "Factor": "Income speed",
                "Impact": top_path["income_impact"],
                "Score contribution": top_path["income_contribution"],
            },
            {
                "Factor": "Budget fit",
                "Impact": top_path["budget_impact"],
                "Score contribution": top_path["budget_contribution"],
            },
            {
                "Factor": "Flexibility fit",
                "Impact": top_path["flexibility_impact"],
                "Score contribution": top_path["flexibility_contribution"],
            },
            {
                "Factor": "Risk safety",
                "Impact": top_path["risk_impact"],
                "Score contribution": top_path["risk_contribution"],
            },
            {
                "Factor": "Credential match",
                "Impact": top_path["credential_impact"],
                "Score contribution": top_path["credential_contribution"],
            },
        ]

        st.dataframe(breakdown_data, width="stretch", hide_index=True)

    with st.expander("View advanced decision metrics"):
        adv_col1, adv_col2, adv_col3, adv_col4 = st.columns(4)

        with adv_col1:
            st.metric("Decision Clarity", top_path["decision_clarity_level"])

        with adv_col2:
            st.metric("Momentum", top_path["momentum_level"])

        with adv_col3:
            st.metric("Multiplier Score", top_path["momentum_multiplier"])

        with adv_col4:
            st.metric("Cost Stress", top_path["affordability_stress"])

        st.markdown(
            """
            **Overall Match** shows how well the top path matches your current priorities.

            **Confidence** shows how far ahead the top path is compared to the backup path.

            **Decision Clarity** checks whether one path clearly stands out or whether the top options are close.

            **Momentum** estimates how much career movement a path may create compared to cost, time, and risk.

            **Life Pressure** reflects income urgency, budget pressure, flexibility needs, and risk concerns.

            **Risk Exposure** shows how risky this path may feel under your current income and budget pressure.
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

    st.markdown(
        f"""
        <div class="ai-strategy-text">
        {ai_summary}
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("Reality Check"):
        st.warning(get_reality_check(top_path["path"]))

        st.caption(
            "This ranking is based on general pathway assumptions and your current priority sliders. "
            "It does not guarantee income, job placement, program quality, or future success."
        )

    st.write("### Human Review Before Committing")

    st.warning(
        "ClarityFlow can help compare options and create a decision map, but it should not "
        "make final life or career commitments for the user. Before quitting a job, moving, "
        "enrolling in a paid program, taking on debt, accepting a job, or making a major "
        "change, review the plan with a mentor, advisor, counselor, workforce worker, "
        "or trusted human."
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
                "confidence_gap_percent",
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