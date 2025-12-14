import streamlit as st
import google.generativeai as genai

# ===============================
# 🔐 CONFIGURATION
# ===============================

# ✅ Use Streamlit secrets (DO NOT hardcode keys)
API_KEY="AIzaSyDn3tDPYJRMv9TuBVjloPBdPpWd-QHaWSo"
genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-pro"

# Domain-specific system prompts
SYSTEM_PROMPTS = {
    "home": "You are a friendly home AI assistant. Answer general questions clearly and helpfully.",
    "cybersecurity": "You are a cybersecurity expert. Provide technical, accurate security guidance.",
    "data_science": "You are a data science expert. Help with analysis, statistics, and visualization.",
    "it_ops": "You are an IT operations expert. Troubleshoot systems and optimize IT workflows."
}

# ===============================
# 🧠 SESSION STATE INIT
# ===============================

if "messages" not in st.session_state:
    st.session_state.messages = {}

if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

if "model" not in st.session_state:
    st.session_state.model = genai.GenerativeModel(
        model_name=MODEL_NAME,
        generation_config={
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 2048,
        },
    )

# ===============================
# 💬 AI CHAT FUNCTION
# ===============================

def ai_chat(domain: str):
    # Init domain history
    if domain not in st.session_state.messages:
        st.session_state.messages[domain] = []

    # Render chat history
    for msg in st.session_state.messages[domain]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input(f"Ask about {domain.replace('_', ' ').title()}...")

    if not user_input:
        return

    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.messages[domain].append({
        "role": "user",
        "content": user_input
    })

    # -------------------------------
    # Build Gemini-compatible history
    # -------------------------------

    chat_history = []

    # ✅ Inject system prompt as first message
    system_prompt = SYSTEM_PROMPTS.get(domain, "You are a helpful assistant.")
    chat_history.append({
        "role": "user",
        "parts": [system_prompt]
    })

    # Add recent messages (limit context)
    for msg in st.session_state.messages[domain][-6:]:
        if msg["role"] == "user":
            chat_history.append({"role": "user", "parts": [msg["content"]]})
        else:
            chat_history.append({"role": "model", "parts": [msg["content"]]})

    # -------------------------------
    # Generate response
    # -------------------------------

    with st.chat_message("assistant"):
        response_box = st.empty()
        full_response = ""

        try:
            chat = st.session_state.model.start_chat(history=chat_history)
            response = chat.send_message(user_input, stream=True)

            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    response_box.markdown(full_response)

            st.session_state.messages[domain].append({
                "role": "assistant",
                "content": full_response
            })

        except Exception as e:
            st.error(f"AI Error: {e}")

# ===============================
# 🧭 SIDEBAR NAVIGATION
# ===============================

with st.sidebar:
    st.header("Navigation")

    page_map = {
        "Home": "home",
        "Cybersecurity": "cybersecurity",
        "Data Science": "data_science",
        "IT Operations": "it_ops",
    }

    selection = st.radio("Go to:", list(page_map.keys()))
    st.session_state.current_page = page_map[selection]

    st.divider()

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages[st.session_state.current_page] = []
        st.rerun()

    st.divider()
    st.caption("Powered by Google Gemini 1.5 Pro")

# ===============================
# 🖥️ PAGE RENDERING
# ===============================

PAGE_TITLES = {
    "home": "🏠 Home AI Assistant",
    "cybersecurity": "🔒 Cybersecurity Assistant",
    "data_science": "📊 Data Science Assistant",
    "it_ops": "🖥️ IT Operations Assistant",
}

PAGE_DESCRIPTIONS = {
    "home": "Ask me anything!",
    "cybersecurity": "Security threats, best practices, and analysis.",
    "data_science": "Statistics, ML, visualization, and insights.",
    "it_ops": "System troubleshooting and IT operations help.",
}

page = st.session_state.current_page

st.title(PAGE_TITLES[page])
st.caption(PAGE_DESCRIPTIONS[page])
st.divider()

ai_chat(page)
