import random
import streamlit as st

st.set_page_config(
    page_title="Common Ground",
    page_icon="🐄",
    layout="centered",
)

# Original prompts inspired by the broad social mechanic of consensus-answer
# party games. No questions or text are copied from Herd Mentality.
TOPICS = {
    "Food & drink": [
        "a typical breakfast",
        "a food people often eat for lunch",
        "a popular takeaway meal",
        "a classic pizza topping",
        "food served at a barbecue",
        "something people put in a sandwich",
        "a common flavour of ice cream",
        "a food people eat at the cinema",
        "something people dip chips into",
        "a popular hot drink",
    ],
    "Home & everyday life": [
        "something people keep in a kitchen drawer",
        "an item people often lose at home",
        "something people do as soon as they get home",
        "an object found in most living rooms",
        "something people forget to switch off",
        "a chore people tend to put off",
        "something people keep beside their bed",
        "an item people use every day",
        "something that commonly needs replacing at home",
        "a reason someone might ring the doorbell",
    ],
    "Work & school": [
        "something people keep on their desk",
        "a common excuse for being late",
        "something people do during a boring meeting",
        "an item people take to school",
        "something people often forget to bring to work",
        "a job children commonly say they want",
        "something people write on a sticky note",
        "a reason someone might call in sick",
        "something people do during a coffee break",
        "an object found in a classroom",
    ],
    "Travel & transport": [
        "something people pack for a holiday",
        "an item people often forget when travelling",
        "a popular holiday destination",
        "something people do during a long car journey",
        "a reason a flight might be delayed",
        "something people buy at an airport",
        "an object found in a car",
        "a common form of public transport",
        "something people take to the beach",
        "a place people stop on a road trip",
    ],
    "Entertainment & hobbies": [
        "a film genre lots of people enjoy",
        "a popular board game",
        "something people watch on television",
        "an instrument people learn to play",
        "a hobby people take up in retirement",
        "something people do at a concert",
        "a well-known type of dance",
        "a video game genre",
        "something people collect",
        "an activity people do on a rainy day",
    ],
    "People & relationships": [
        "a quality people look for in a friend",
        "a common nickname for a parent",
        "something people argue about at home",
        "a gift people buy for a birthday",
        "a reason someone might cancel plans",
        "something people do when they are nervous",
        "a topic people make small talk about",
        "a quality people admire in a colleague",
        "something people say when meeting someone new",
        "a reason people throw a party",
    ],
    "Shopping & money": [
        "something people buy every week",
        "an item people often buy impulsively",
        "something people save money for",
        "a shop found in most town centres",
        "something people compare before buying",
        "an item people buy as a present",
        "something people tend to buy in bulk",
        "a reason someone might return a purchase",
        "something people keep in a wallet",
        "an expense people often complain about",
    ],
    "Nature & weather": [
        "something people do on a sunny day",
        "an animal people commonly see in a garden",
        "something people associate with winter",
        "a type of weather people dislike",
        "a flower people can easily name",
        "something people take on a walk in the countryside",
        "an animal people are likely to see at a zoo",
        "something that grows in a vegetable garden",
        "a sound people hear outdoors",
        "a popular outdoor activity in summer",
    ],
    "Health & personal care": [
        "something people do to stay healthy",
        "an item found in a bathroom cabinet",
        "something people use in the shower",
        "a reason someone might visit a doctor",
        "something people do before going to bed",
        "an item people take to the gym",
        "a common minor everyday complaint",
        "something people use to clean their teeth",
        "a reason someone might have trouble sleeping",
        "something people do when they have a cold",
    ],
    "Celebrations & occasions": [
        "something people do on New Year's Eve",
        "a food served at Christmas",
        "something people bring to a housewarming",
        "a popular wedding gift",
        "something people do on their birthday",
        "an item associated with Halloween",
        "something people decorate for a celebration",
        "a reason people give someone a card",
        "something people do at a family gathering",
        "a common party game",
    ],
}

QUESTION_STYLES = [
    "What is the first thing that comes to mind when you think of {topic}?",
    "Name one thing most people associate with {topic}.",
    "If you asked 100 people about {topic}, what answer do you think would come up most often?",
    "What would be the most obvious answer when someone mentions {topic}?",
    "Which single thing best represents {topic}?",
    "What is a very common example of {topic}?",
    "What would an average person immediately think of for {topic}?",
    "What is the most familiar thing connected with {topic}?",
    "Give the answer you think the majority of people would choose for {topic}.",
    "What common answer would you expect people to give about {topic}?",
]

@st.cache_data
def build_question_bank():
    questions = []
    for category, topics in TOPICS.items():
        for topic in topics:
            for style in QUESTION_STYLES:
                questions.append({
                    "question": style.format(topic=topic),
                    "category": category,
                })
    # Stable ordering; random selection happens separately.
    return questions

QUESTIONS = build_question_bank()
CATEGORIES = ["All categories"] + list(TOPICS.keys())

def available_indices(category):
    return [
        i for i, item in enumerate(QUESTIONS)
        if category == "All categories" or item["category"] == category
    ]

def pick_next(category):
    candidates = available_indices(category)
    unused = [i for i in candidates if i not in st.session_state.used]
    if not unused:
        # Start a fresh cycle for this category if all its questions were used.
        st.session_state.used = [
            i for i in st.session_state.used if i not in candidates
        ]
        unused = candidates
    if not unused:
        return None
    chosen = random.choice(unused)
    st.session_state.used.append(chosen)
    return chosen

if "used" not in st.session_state:
    st.session_state.used = []
if "current" not in st.session_state:
    st.session_state.current = None
if "history" not in st.session_state:
    st.session_state.history = []

st.title("🐄 Common Ground")
st.caption("A quick-fire party game about guessing what everyone else will say.")

with st.sidebar:
    st.header("Game settings")
    category = st.selectbox("Question category", CATEGORIES)
    st.divider()
    st.metric("Questions in the bank", f"{len(QUESTIONS):,}")
    st.metric("Used this session", len(st.session_state.used))
    st.caption(
        "Questions are original prompts designed for common, everyday answers. "
        "There is no single official answer."
    )
    if st.button("Reset used questions", use_container_width=True):
        st.session_state.used = []
        st.session_state.current = None
        st.session_state.history = []
        st.rerun()

st.markdown(
    """
    **How to play**
    1. Show everyone the question.
    2. Each player writes down the answer they think most other players will give.
    3. Reveal answers together. Award points when answers match.
    """
)

left, right = st.columns([1, 1])
with left:
    if st.button("🎲 Get a question", type="primary", use_container_width=True):
        if st.session_state.current is not None:
            st.session_state.history.append(st.session_state.current)
        st.session_state.current = pick_next(category)
with right:
    if st.button("↩ Previous question", use_container_width=True):
        if st.session_state.history:
            st.session_state.current = st.session_state.history.pop()

if st.session_state.current is None:
    st.info("Choose a category and click **Get a question** to begin.")
else:
    item = QUESTIONS[st.session_state.current]
    st.markdown(
        f"""
        <div style="
            border: 1px solid rgba(128,128,128,.35);
            border-radius: 18px;
            padding: 2rem 1.5rem;
            margin: 1rem 0;
            text-align: center;
            min-height: 190px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        ">
            <div style="font-size: .85rem; opacity: .7; margin-bottom: 1rem;">
                {item["category"]}
            </div>
            <div style="font-size: 1.65rem; font-weight: 650; line-height: 1.35;">
                {item["question"]}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("There is no right answer — the aim is to match the group.")

with st.expander("Browse the question bank"):
    selected = st.selectbox(
        "Browse category",
        CATEGORIES,
        key="browse_category",
    )
    browse = [
        q for q in QUESTIONS
        if selected == "All categories" or q["category"] == selected
    ]
    st.caption(f"{len(browse)} questions")
    for number, item in enumerate(browse, start=1):
        st.write(f"{number}. {item['question']}")
