# Common Ground — Streamlit party game

A party game where players try to predict the answer most other people will give.

## Files

- `app.py` — Streamlit application
- `questions.csv` — editable question bank
- `requirements.txt` — Python dependencies

## Run locally

```bash
python -m venv .venv
```

Activate the environment, then:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Upload `app.py`, `questions.csv`, `requirements.txt`, and `README.md` to the same folder in your GitHub repository.
2. In Streamlit Community Cloud, create an app from that repository.
3. Set `app.py` as the app entry point.
4. Deploy.

## Editing questions

Edit `questions.csv` directly in GitHub. Keep the three columns:

`question,category,difficulty`

Allowed difficulty labels are `Easy` and `Medium`, but you can add your own labels. The app reads the CSV at startup and caches it based on the file's modification time.

## Current bank

1089 individually authored questions across 11 categories.

The questions are original prompts inspired by the broad consensus-answer party-game format. They are not copied from Herd Mentality.
