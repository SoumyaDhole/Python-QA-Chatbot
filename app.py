"""Streamlit interface for the Personal Python Question-Answering Chatbot."""

import streamlit as st

from chatbot import clear_conversation_state, context_after_answer, get_answer


st.set_page_config(
    page_title="Python Assistant",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;600;700&display=swap');
    :root {
        --page: #F8FAFC;
        --surface: #FFFFFF;
        --surface-soft: #F1F5F9;
        --ink: #0F172A;
        --muted: #64748B;
        --blue: #2563EB;
        --blue-hover: #1D4ED8;
        --blue-soft: #EFF6FF;
        --line: #E2E8F0;
        --focus: #93C5FD;
    }
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; color: var(--ink); }
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] { background: var(--page) !important; color: var(--ink); }
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] {
        background: var(--page) !important;
        color: var(--ink) !important;
    }
    [data-testid="stSidebar"] { background: var(--surface-soft); border-right: 1px solid var(--line); }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] * { color: var(--ink); }
    [data-testid="stMainBlockContainer"] { max-width: 980px; padding: 1.5rem 1.5rem 6rem; }
    h1, h2, h3, h4, p, label, [data-testid="stMarkdownContainer"] { color: var(--ink); }
    .app-title { color: var(--ink); font: 700 2rem/1.15 'DM Sans', sans-serif; margin: 0; }
    .app-subtitle { color: var(--muted); font-size: 0.98rem; margin: 0.35rem 0 0.8rem; }
    .welcome-title { color: var(--ink); font-size: 1.35rem; font-weight: 600; margin: 1.4rem 0 0.25rem; }
    .welcome-copy { color: var(--muted); margin: 0 0 1rem; }
    .section-label { color: var(--muted); font-size: 0.78rem; font-weight: 600; text-transform: uppercase; }
    [data-testid="stAlert"] { border: 1px solid #BFDBFE; border-radius: 8px; background: var(--blue-soft); }
    [data-testid="stAlert"] [data-testid="stMarkdownContainer"] * { color: #1E3A8A; }
    [data-testid="stChatMessage"] { border: 1px solid var(--line); border-radius: 12px; padding: 0.75rem 0.95rem; background: var(--surface); color: var(--ink); }
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) { background: var(--blue-soft); border-color: #BFDBFE; }
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] * { color: var(--ink); }
    [data-testid="stChatMessage"] pre {
        max-width: 100%;
        overflow-x: auto;
        border: 1px solid var(--line);
        border-radius: 8px;
        background: var(--surface-soft) !important;
        color: var(--ink) !important;
    }
    [data-testid="stChatMessage"] pre > div { background: var(--surface-soft) !important; }
    [data-testid="stChatMessage"] pre code,
    [data-testid="stChatMessage"] pre code span,
    [data-testid="stChatMessage"] pre code .token { color: var(--ink) !important; }
    [data-testid="stChatMessage"] pre code .token.keyword,
    [data-testid="stChatMessage"] pre code .token.boolean { color: #7C2D92 !important; }
    [data-testid="stChatMessage"] pre code .token.string { color: #166534 !important; }
    [data-testid="stChatMessage"] pre code .token.number { color: #0F766E !important; }
    [data-testid="stChatMessage"] pre code .token.function,
    [data-testid="stChatMessage"] pre code .token.builtin { color: #1D4ED8 !important; }
    [data-testid="stChatMessage"] pre code .token.operator,
    [data-testid="stChatMessage"] pre code .token.punctuation { color: #475569 !important; }
    [data-testid="stChatMessage"] pre code .token.comment { color: #64748B !important; }
    [data-testid="stChatMessage"] p code,
    [data-testid="stChatMessage"] li code {
        padding: 0.12rem 0.3rem;
        border: 1px solid var(--line);
        border-radius: 4px;
        background: var(--surface-soft) !important;
        color: #1E3A8A !important;
        font-size: 0.9em;
    }
    [data-testid="stBottom"], [data-testid="stBottom"] > div, [data-testid="stBottom"] > div > div {
        background: var(--page) !important;
    }
    [data-testid="stChatInput"] { border: 1px solid #CBD5E1; border-radius: 12px; background: var(--surface) !important; box-shadow: 0 4px 16px #0F172A0A; }
    [data-testid="stChatInput"] > div { background: var(--surface) !important; }
    [data-testid="stChatInput"] textarea { color: var(--ink); background: var(--surface) !important; caret-color: var(--blue); }
    [data-testid="stChatInput"] textarea::placeholder { color: var(--muted); opacity: 1; }
    [data-testid="stChatInputSubmitButton"] { border-radius: 8px; background: var(--blue); color: #FFFFFF; }
    [data-testid="stChatInputSubmitButton"]:hover { background: var(--blue-hover); color: #FFFFFF; }
    [data-testid="stChatInput"]:focus-within { border-color: var(--blue); box-shadow: 0 0 0 3px #93C5FD55; }
    [data-testid="stBottom"] { background: var(--page); }
    .stButton > button { min-height: 2.55rem; border: 1px solid var(--line); border-radius: 9px; background: var(--surface); color: var(--ink); font-weight: 500; text-align: left; transition: border-color 120ms ease, background-color 120ms ease, color 120ms ease; }
    .stButton > button:hover { border-color: var(--blue); background: var(--blue-soft); color: #1D4ED8; }
    .stButton > button:focus-visible { outline: 3px solid var(--focus); outline-offset: 2px; }
    .stButton > button[kind="primary"] { border-color: var(--blue); background: var(--blue); color: #FFFFFF; text-align: center; }
    .stButton > button[kind="primary"]:hover { border-color: var(--blue-hover); background: var(--blue-hover); color: #FFFFFF; }
    [data-testid="stExpander"] { border-color: var(--line); border-radius: 8px; background: var(--surface); color: var(--ink); }
    [data-testid="stExpander"] details,
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] { background: var(--surface); color: var(--ink); }
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] summary [data-testid="stIconMaterial"] { color: var(--ink) !important; }
    [data-testid="stSidebar"] [data-testid="stExpander"] details,
    [data-testid="stSidebar"] [data-testid="stExpander"] [data-testid="stExpanderDetails"] { background: var(--surface-soft); }
    [data-testid="stSidebar"] .stButton > button { min-height: 2.25rem; font-size: 0.88rem; }
    @media (max-width: 640px) {
        [data-testid="stMainBlockContainer"] { padding: 1rem 0.8rem 5rem; }
        .app-title { font-size: 1.7rem; }
        [data-testid="stChatMessage"] { padding: 0.6rem 0.7rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_context" not in st.session_state:
    st.session_state.conversation_context = None


def queue_question(question):
    st.session_state.pending_question = question
    st.rerun()


st.sidebar.markdown("### Python Assistant")
st.sidebar.caption("Curated answers, retrieved locally.")

sidebar_topics = {
    "Python basics": ["What is Python?", "Where is Python used?"],
    "Collections": ["Explain lists", "How do I access dictionary values?"],
    "Functions": ["What is a function?", "How do I set a default function argument?"],
    "Data and ML": ["How do I read a CSV file with pandas?", "What is overfitting in machine learning?"],
}
for topic, prompts in sidebar_topics.items():
    with st.sidebar.expander(topic):
        for index, prompt in enumerate(prompts):
            if st.button(prompt, key=f"sidebar_{topic}_{index}", use_container_width=True):
                queue_question(prompt)

st.sidebar.divider()
if st.sidebar.button("Clear conversation", key="clear_conversation", use_container_width=True):
    clear_conversation_state(st.session_state)
    st.rerun()
st.sidebar.caption("No external model or API is used.")

st.markdown('<h1 class="app-title">Python Assistant</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="app-subtitle">Ask a Python question. Answers come from a curated knowledge base, with follow-ups tied to the current topic.</p>',
    unsafe_allow_html=True,
)
st.info("Knowledge-base retrieval uses TF-IDF and cosine similarity; it is not a generative AI model.")

with st.container(height=470, border=False):
    if st.session_state.messages:
        for index, message in enumerate(st.session_state.messages):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if message.get("source"):
                    with st.expander("Answer source"):
                        st.caption(message["source"])
    else:
        st.markdown('<div class="welcome-title">What would you like to learn?</div>', unsafe_allow_html=True)
        st.markdown('<div class="welcome-copy">Pick a starter question or ask in your own words.</div>', unsafe_allow_html=True)
        starter_prompts = [
            ("Python basics", "What is Python?"),
            ("Lists", "How do I add an item to a list?"),
            ("Functions", "What is a function in Python?"),
            ("Dictionaries", "How do I access dictionary values?"),
            ("Pandas", "How do I read a CSV file with pandas?"),
            ("Machine learning", "What is overfitting in machine learning?"),
        ]
        for row_start in range(0, len(starter_prompts), 2):
            left, right = st.columns(2, gap="small")
            for column, item in zip((left, right), starter_prompts[row_start : row_start + 2]):
                with column:
                    topic, prompt = item
                    st.caption(topic)
                    if st.button(prompt, key=f"starter_{row_start}_{topic}", use_container_width=True):
                        queue_question(prompt)

question = st.chat_input("Ask a Python question...")
pending_question = st.session_state.pop("pending_question", None)
if question is None:
    question = pending_question

if question is not None:
    if not question.strip():
        st.warning("Enter a question before sending.")
    else:
        st.session_state.messages.append({"role": "user", "content": question})
        try:
            with st.spinner("Searching the Python knowledge base..."):
                result = get_answer(question, context=st.session_state.conversation_context)
            st.session_state.conversation_context = context_after_answer(result)
            if result is None:
                response = (
                    "I couldn't find a sufficiently relevant answer in the Python knowledge base. "
                    "Try rephrasing your question or choose a topic from the sidebar."
                )
                source = None
            else:
                response = result["answer"]
                source = result.get("matched_question")
        except Exception:
            st.session_state.conversation_context = None
            response = "I couldn't complete that search just now. Please try asking again."
            source = None

        st.session_state.messages.append(
            {"role": "assistant", "content": response, "source": source}
        )
        st.rerun()