# Common Ground — Streamlit party-question app

A simple party game built around everyday questions. Players try to predict the
answer that most other people in the group will give.

## Run locally

```bash
python -m venv .venv
```

Activate the environment, then:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy from GitHub

1. Create a GitHub repository.
2. Upload `app.py`, `requirements.txt`, and this `README.md`.
3. In Streamlit Community Cloud, choose **New app**.
4. Select the repository, branch, and `app.py` as the entry point.
5. Deploy.

## What's included

- 1,000 original question prompts across 10 everyday categories.
- Random question selection.
- No-repeat selection until the current category's questions have been used.
- Previous-question navigation.
- A browsable question bank.
- Reset button for a new session.

The question bank is generated from 100 everyday topics and 10 alternative
prompt styles. The questions are not copied from Herd Mentality.
