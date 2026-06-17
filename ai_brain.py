import streamlit as st
from openai import OpenAI


def generate_ai_summary(career_goal, decision_question, top_path, backup_path, results):
    """
    Uses AI to explain the ECON Mode result in a clear, practical voice.
    The AI does not change the score. It only explains the ranked result.
    """

    api_key = st.secrets.get("OPENAI_API_KEY")

    if not api_key:
        return (
            "AI summary is not enabled yet. Add your OpenAI API key in "
            ".streamlit/secrets.toml to turn on the extra brain."
        )

    client = OpenAI(api_key=api_key)

    backup_name = backup_path["path"] if backup_path is not None else "None"

    top_results = results[["rank", "path", "score", "notes"]].head(3).to_dict(
        orient="records"
    )

    prompt = f"""
You are ClarityFlow AI, a practical life decision simulator for career crossroads.

Your job:
Turn messy career uncertainty into a clear, completed decision plan.

Tone:
- calm
- direct
- logical
- supportive without being cheesy
- practical
- no vague motivation
- no final life commands

Important behavior:
- Do NOT leave the user with unanswered questions as the main output.
- If something is unclear, make a reasonable assumption and clearly label it.
- Give the user a complete plan they can act on immediately.
- You may include a short "Verify This" section, but do not make the whole answer depend on the user doing more research.
- Do not say "I need more information" unless absolutely necessary.
- Do not make final life decisions for the user.
- Explain this is decision support, not guaranteed career advice.

User career goal:
{career_goal}

User decision question:
{decision_question}

Top recommended path from ECON Mode:
{top_path["path"]}

Backup path:
{backup_name}

Top scored results:
{top_results}

Write the response with these sections:

1. Clean Read
Give the most likely meaning of the user's situation in plain language.

2. Best Starting Direction
Recommend the strongest starting direction based on the ECON result and user input.
Use wording like "appears to fit best" instead of "you must."

3. Why This Direction Fits
Explain cost, time, risk, flexibility, current background, and likely payoff.

4. Completed 7-Day Checklist
Give a specific 7-day checklist the user can act on immediately.
Format each day as a checkbox using Markdown:
- [ ] Day 1: ...
- [ ] Day 2: ...
- [ ] Day 3: ...
- [ ] Day 4: ...
- [ ] Day 5: ...
- [ ] Day 6: ...
- [ ] Day 7: ...

Do not include a 30-day plan.
Do not make the user create the plan.
Keep it realistic, low-pressure, and focused on testing the next step.

5. What To Avoid
List mistakes that could waste time, money, or confidence.

6. Verify Before Committing
Give 3-5 things the user should verify before making a major decision.

7. Confidence Boost
Give a grounded, realistic confidence boost based on the plan.
"""

    try:
        response = client.responses.create(
            model="gpt-5.4-mini",
            input=prompt,
        )
        return response.output_text

    except Exception as error:
        return (
            "AI Strategy Summary is temporarily unavailable.\n\n"
            "The local decision map still works because the ECON scoring runs in Python. "
            "The AI explanation layer could not complete this request.\n\n"
            f"Technical note: {error}"
        )