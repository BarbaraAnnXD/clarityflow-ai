# ClarityFlow AI

ClarityFlow AI is a web-based career decision simulator that helps students, young professionals, and career changers turn career confusion into a clear starting plan.

Instead of giving generic AI advice, ClarityFlow combines a transparent ECON-inspired scoring engine with an AI explanation layer. The scoring engine calculates the recommendation first, then the AI explains the result and turns it into a practical 7-day checklist.

## Problem

Many people face career decision overload. They may have too many options, unclear tradeoffs, fear of choosing wrong, budget pressure, family responsibilities, or uncertainty about whether to pursue school, work, self-learning, a bootcamp, graduate school, or a startup.

ClarityFlow AI helps users organize those choices into a clearer decision map.

## Solution

The user enters what they are stuck between and adjusts priority sliders based on their current situation.

The app then compares multiple career paths using structured data and an explainable scoring model. It returns:

* Strongest starting path
* Backup path
* Decision snapshot
* Main warning
* AI-generated strategy plan
* 7-day checklist
* Optional decision map and scoring details

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

## How It Works

ClarityFlow uses a layered decision pipeline:

1. User enters a messy career decision.
2. User adjusts priority sliders.
3. The ECON engine calculates decision metrics using Pandas and NumPy.
4. The decision engine ranks career paths.
5. The AI explanation layer explains the result and creates a 7-day checklist.

The AI does not secretly choose the recommendation. The recommendation is calculated first using transparent scoring logic.

## ECON-Inspired Decision Engine

The ECON engine is located in:

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

* income urgency
* budget sensitivity
* flexibility needs
* risk concerns

Code fields:

* `pressure_score`
* `pressure_level`

### Cost Stress

Estimates how financially stressful a path may be based on the path cost and the user’s budget pressure.

Code field:

`affordability_stress`

### Risk Exposure

Estimates how risky a path may be based on the path risk level and the user’s income/budget pressure.

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
* High life pressure warnings
* Optional decision map for transparency

The AI explanation layer is used to explain the calculated result, not to secretly invent the recommendation.

## Tech Stack

* Python
* Streamlit
* Pandas
* NumPy
* OpenAI API
* CSV data layer
* GitHub

## Main Files

* `app.py` — Streamlit web app interface
* `econ_mode.py` — ECON-inspired scoring engine
* `decision_engine.py` — tradeoffs, warnings, confidence boost, and decision logic
* `ai_brain.py` — AI-generated explanation and 7-day checklist
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

## Team Roles

### Barbara

Main app build, Streamlit interface, AI flow, ECON engine implementation, GitHub setup, responsible AI structure.

### Jana

Data Analytics + Model Evaluation Lead. Jana will review the dataset, scoring logic, Pandas/NumPy use, ECON-inspired metrics, bias risks, and test cases.

### Ahmed

Project coordination, pitch support, Devpost/project submission support, and team organization.

## Current Status

The prototype is working locally and includes:

* Priority sliders
* Career path scoring
* AI-generated strategy plan
* 7-day checklist
* Optional decision map
* Decision snapshot
* Gini-inspired Decision Clarity
* Momentum Multiplier
* Main warning logic
* Responsible AI safeguards
