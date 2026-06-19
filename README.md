# ClarityFlow AI

ClarityFlow AI is a web-based career decision simulator that helps students, young professionals, and career changers turn career confusion into a clear starting direction.

Instead of giving generic AI advice, ClarityFlow combines a transparent ECON-inspired scoring engine with an AI explanation layer. The scoring engine ranks possible career paths first, then the AI explains the result, compares the user’s real options, and creates a practical 7-day evidence-gathering plan.

## Track and Challenge

**Track:** Undergraduate Track — AI for Life & Work
**Mission Lane:** Productivity
**Challenge Direction:** Direction A: Life Decision Simulator

ClarityFlow AI helps students, early professionals, and career changers compare major career paths by modeling tradeoffs, surfacing hidden considerations, and showing likely next steps before they make major commitments.

## Problem

Many people experience decision paralysis when choosing a career direction. They may be stuck between multiple options, worried about money, unsure whether to pursue school or work, or afraid of choosing the wrong path.

General AI chatbots can give advice, but the advice may feel too open-ended, too generic, or hard to audit.

ClarityFlow AI helps users organize their decision into a structured decision map.

## Solution

The user enters what they are stuck between, adjusts priority sliders, and chooses how they want the AI to respond.

ClarityFlow then compares possible paths using structured data and transparent scoring. The app returns:

* A result reveal card
* Strongest starting direction
* Backup path
* Decision snapshot
* Decision Paralysis Breaker
* AI Strategy Plan
* 7-day evidence-gathering checklist
* Main warning
* Reality check
* Optional decision map and scoring details
* Report wrong or harmful output option

## Career Paths Compared

The current prototype compares:

* Degree
* Bootcamp
* Self-Taught
* Job Now
* Graduate School
* Startup

These paths are stored in:

`data/career_paths.csv`

## Data Sources

ClarityFlow AI currently uses a small CSV-based prototype dataset stored in `data/career_paths.csv`. The dataset contains structured career-path options and comparison factors such as cost level, time to result, flexibility, credential strength, risk level, and income speed.

The data is prototype/simulated career-path data created for the hackathon demo, not a live labor-market dataset. The app does not currently use PostgreSQL, Supabase, Firebase, external job APIs, or saved user data.


## Key Features

### Result Reveal Card

After the user clicks **Build My Plan**, ClarityFlow shows a visual result card with the user’s starting direction.

Example:

`Your Starting Direction: Self-Taught`

This helps the result feel clear and memorable.

### Priority Check

Users adjust sliders for:

* Income urgency
* Budget sensitivity
* Flexibility need
* Risk aversion
* Credential importance

These sliders affect the scoring engine and help the app compare tradeoffs.

### Clarity Mode

Users can choose how they want the AI to guide them:

* Direct Mode — clear answer fast
* Coach Mode — supportive and steady
* Analyst Mode — explain the tradeoffs
* Checklist Mode — action steps only

The scoring result stays the same, but the AI explanation adapts to the user’s preferred support style.

### Decision Paralysis Breaker

The Decision Paralysis Breaker identifies the real options the user typed and helps them choose one option to investigate first.

It includes:

* Real options the app sees
* Primary option to investigate first
* Backup option
* Why the tie breaks
* Switch point

This helps the app avoid generic advice and focus on the user’s actual stuck decision.

### 7-Day Evidence-Gathering Checklist

The checklist is not meant to force the user into a major commitment.

Instead, it helps the user collect evidence before making a bigger decision.

The checklist should not require quitting, moving, enrolling, paying money, or accepting a job. It is designed to help users compare options safely before committing.

### Decision Snapshot

The app shows decision metrics such as:

* Overall Match
* Recommendation Confidence
* Decision Clarity
* Momentum Multiplier
* Life Pressure Level
* Cost Stress
* Risk Exposure

These metrics help users understand why a path surfaced.

## ECON-Inspired Decision Engine

The scoring engine is located in:

`econ_mode.py`

It calculates several decision metrics.

### Overall Match

Shows how well the top path matches the user’s current priorities.

Code field:

`fit_percent`

### Recommendation Confidence

Compares the top path against the backup path. If the top two options are close, confidence is lower.

Code field:

`confidence_level`

### Life Pressure Level

Estimates how much pressure the user may be under based on:

* Income urgency
* Budget sensitivity
* Flexibility needs
* Risk concerns

Code fields:

* `pressure_score`
* `pressure_level`

### Cost Stress

Estimates how financially stressful a path may be based on the path cost and the user’s budget pressure.

Code field:

`affordability_stress`

### Risk Exposure

Estimates how risky a path may be based on the path risk level and the user’s income and budget pressure.

Code field:

`risk_exposure`

### Gini-Inspired Decision Clarity

ClarityFlow adapts the idea of a Gini-style spread to measure how separated the career path scores are.

In this app:

* Low clarity means the paths are close together.
* High clarity means one path stands out more clearly.

Code fields:

* `decision_clarity_index`
* `decision_clarity_level`

### Momentum Multiplier

ClarityFlow adapts the macroeconomic multiplier idea.

In economics:

`Multiplier = Change in Real GDP / Initial Change in Spending`

In ClarityFlow:

`Momentum Multiplier = Expected Career Movement / Initial Burden`

This estimates how much career movement a path may create compared to its cost, time, and risk.

Code fields:

* `momentum_multiplier`
* `momentum_level`

This is not a guaranteed return. It is only a comparison tool.

## Responsible AI Safeguards

ClarityFlow is decision support, not final life advice.

The app includes:

* Human review reminders
* Main warning section
* Low-confidence warnings
* Low decision clarity warnings
* Cost stress warnings
* Risk exposure warnings
* High-pressure safety behavior
* Optional decision map for transparency
* Report wrong or harmful output option

## Verification Notice

ClarityFlow AI is a decision-support prototype. It does not verify live salary, school, hiring, financial-aid, or labor-market data. Users are reminded to check trusted sources such as schools, employers, workforce offices, official program pages, advisors, mentors, counselors, or other trusted humans before acting.

### Stability-First Guardrail

If a user describes a high-pressure situation such as homelessness, unsafe housing, medical risk, lack of food, lack of transportation, domestic violence, trafficking risk, no income, or immediate safety concerns, ClarityFlow surfaces a stability-first warning.

The app should avoid pushing users toward risky major commitments such as quitting a job, moving, taking on debt, enrolling in a paid program, or accepting unsafe work without human review.

The goal is not to abandon the user’s career goal. The goal is to keep the next step smaller, safer, and more realistic while encouraging human support from a mentor, advisor, counselor, workforce worker, shelter or housing support, clinic, or trusted human.


### Report Wrong or Harmful Output

Users can report outputs that feel:

* Wrong
* Unsafe
* Biased
* Too confident
* Confusing
* Unrealistic
* Harmful

The prototype creates a downloadable report file that the user can email to the project team.

In a full version, these reports would go to a human review queue.

## Tech Stack

* Python
* Streamlit
* Streamlit Cloud
* Pandas
* NumPy
* OpenAI LLM API
* GPT-5 mini
* CSV data layer
* GitHub
* HTML/CSS styling inside Streamlit
* ChatGPT coding assistance for debugging, UX wording, Responsible AI planning, prompt design, GitHub/Streamlit troubleshooting, and app polish


## Main Files

* `app.py` — Streamlit web app interface
* `econ_mode.py` — ECON-inspired scoring engine
* `decision_engine.py` — tradeoffs, warnings, result reveal, and decision logic
* `ai_brain.py` — AI-generated explanation, Clarity Mode, and Decision Paralysis Breaker
* `data/career_paths.csv` — career path dataset
* `requirements.txt` — required Python packages

## How to Run Locally

Install requirements:

```bash
python -m pip install -r requirements.txt
```

Run the app:

```bash
python -m streamlit run app.py
```

## API Key Setup

Create a file at:

`.streamlit/secrets.toml`

Add your OpenAI API key:

```toml
OPENAI_API_KEY = "your_api_key_here"
```

Do not commit this file to GitHub.

## Team Roles

### Barbara

Main app build, Streamlit interface, AI flow, ECON engine implementation, GitHub setup, responsible AI structure, and project direction.

### Jana

Data Analytics + Model Evaluation Lead. Jana reviews the dataset, scoring logic, Pandas/NumPy use, ECON-inspired metrics, bias risks, and test cases.

### Ahmed

Project coordination, pitch support, Devpost/project submission support, and team organization.

## Current Status

The prototype is working locally and includes:

* Priority sliders
* Clarity Mode
* Result reveal card
* Career path scoring
* Decision Paralysis Breaker
* AI-generated strategy plan
* 7-day evidence-gathering checklist
* Optional decision map
* Decision snapshot
* Gini-inspired Decision Clarity
* Momentum Multiplier
* Main warning logic
* Report wrong or harmful output option
* Responsible AI safeguards

## Future Improvements

Possible next improvements include:

* Downloadable printable plan
* Priority impact summary
* Better chart visualization
* Expanded career path dataset
* More test scenarios
* Human review dashboard for reports
* Deployment version for public testing

