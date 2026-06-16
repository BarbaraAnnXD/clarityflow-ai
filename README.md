# ClarityFlow AI

ClarityFlow AI is a Streamlit-based Life Decision Simulator prototype.

The current skeleton compares career pathway options using an ECON Mode scoring model based on:

- Cost
- Time to result
- Risk
- Flexibility
- Credential strength
- Income speed

## Current Stack

- Python
- Streamlit
- Pandas
- NumPy
- CSV data file

## Current Features

- User input for career goal and decision question
- ECON Mode sliders
- Career path ranking
- Responsible AI note
- Reality check
- First 7-day action plan

## Responsible AI Notes

This prototype is a decision-support tool. It does not make final life decisions for the user. The scoring model uses transparent starting assumptions and should be reviewed before being used for real-world decisions.

The prototype avoids collecting exact income, addresses, legal names, or sensitive personal records.

## Run Locally

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py