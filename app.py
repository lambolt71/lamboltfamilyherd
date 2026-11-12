import random
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Common Ground",
    page_icon="🐄",
    layout="centered",
)

st.title("🐄 Common Ground")
st.caption("A party game about guessing what everyone else will say.")

QUESTION_FILE = Path(__file__).parent / "questions.csv"

@st.cache_data
def load_questions(file_path: str, modified_time: float) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    required = {"question", "category", "difficulty"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"questions.csv is missing columns: {', '.join(sorted(missing))}")

    df = df.dropna(subset=["question", "category", "difficulty"]).copy()
    for col in required:
        df[col] = df[col].astype(str).str.strip()
    df = df[df["question"] != ""]
    df = df.drop_duplicates(subset=["question"], keep="first").reset_index(drop=True)
    return df

if not QUESTION_FILE.exists():
    st.error("Could not find questions.csv. Upload it to the same GitHub folder as app.py.")
    st.stop()

try:
    questions = load_questions(str(QUESTION_FILE), QUESTION_FILE.stat().st_mtime)
except Exception as exc:
    st.error(f"Could not load questions.csv: {exc}")
    st.stop()

if questions.empty:
    st.error("The question bank is empty.")
    st.stop()

if "used_ids" not in st.session_state:
    st.session_state.used_ids = []
if "current_id" not in st.session_state:
    st.session_state.current_id = None
if "history" not in st.session_state:
    st.session_state.history = []
if "flagged" not in st.session_state:
    st.session_state.flagged = []

with st.sidebar:
    st.header("Game settings")
    categories = ["All categories"] + sorted(questions["category"].unique().tolist())
    selected_category = st.selectbox("Category", categories)
    difficulties = ["All levels"] + sorted(questions["difficulty"].unique().tolist())
    selected_difficulty = st.selectbox("Difficulty", difficulties)

    st.divider()
    st.metric("Questions available", f"{len(questions):,}")
    st.metric("Used this session", len(st.session_state.used_ids))
    st.metric("Flagged this session", len(st.session_state.flagged))

    if st.button("Reset session", use_container_width=True):
        st.session_state.used_ids = []
        st.session_state.current_id = None
        st.session_state.history = []
        st.session_state.flagged = []
        st.rerun()

filtered = questions.copy()
if selected_category != "All categories":
    filtered = filtered[filtered["category"] == selected_category]
if selected_difficulty != "All levels":
    filtered = filtered[filtered["difficulty"] == selected_difficulty]

st.markdown(
    """
    **How to play**
    1. Read the question aloud.
    2. Everyone writes down the answer they think most other players will give.
    3. Reveal answers together and award points for matching the group.
    """
)

def get_next_question():
    eligible = filtered[~filtered.index.isin(st.session_state.used_ids)]
    if eligible.empty:
        # Start a fresh cycle for the currently selected filters.
        st.session_state.used_ids = []
        eligible = filtered
    if eligible.empty:
        return None
    chosen_id = int(random.choice(eligible.index.tolist()))
    return chosen_id

col1, col2 = st.columns(2)
with col1:
    if st.button("🎲 Get a question", type="primary", use_container_width=True):
        if st.session_state.current_id is not None:
            st.session_state.history.append(st.session_state.current_id)
        new_id = get_next_question()
        st.session_state.current_id = new_id
        if new_id is not None and new_id not in st.session_state.used_ids:
            st.session_state.used_ids.append(new_id)

with col2:
    if st.button("↩ Previous question", use_container_width=True):
        if st.session_state.history:
            st.session_state.current_id = st.session_state.history.pop()

if st.session_state.current_id is None:
    st.info("Choose your settings and click **Get a question**.")
else:
    current = questions.loc[st.session_state.current_id]
    st.markdown(
        f"""
        <div style="
            border: 1px solid rgba(128,128,128,.35);
            border-radius: 18px;
            padding: 2rem 1.5rem;
            margin: 1rem 0;
            text-align: center;
        ">
            <div style="font-size: .85rem; opacity: .7; margin-bottom: 1rem;">
                {current['category']} · {current['difficulty']}
            </div>
            <div style="font-size: 1.65rem; font-weight: 650; line-height: 1.35;">
                {current['question']}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("🚩 Flag this question", use_container_width=True):
        if st.session_state.current_id not in st.session_state.flagged:
            st.session_state.flagged.append(st.session_state.current_id)
        st.success("Flagged for review during this session.")

with st.expander("Browse question bank"):
    browse_category = st.selectbox("Category to browse", categories, key="browse_category")
    browse = questions if browse_category == "All categories" else questions[questions["category"] == browse_category]
    st.caption(f"{len(browse)} questions")
    for number, row in enumerate(browse.itertuples(index=False), start=1):
        st.write(f"{number}. {row.question}")

if st.session_state.flagged:
    with st.expander("Flagged questions"):
        for question_id in st.session_state.flagged:
            st.write(f"- {questions.loc[question_id, 'question']}")
        st.caption("Flags are kept for this session only; they are not written back to GitHub.")
