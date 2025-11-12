import os
import streamlit as st
from dotenv import load_dotenv

# Optional: silence benign gRPC logs like "ALTS creds ignored"
os.environ.setdefault("GRPC_VERBOSITY", "ERROR")
os.environ.setdefault("GLOG_minloglevel", "2")

import google.generativeai as genai

# -----------------------------
# Page config (must be early)
# -----------------------------
st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# Load API key from .env
# -----------------------------
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("❌ GOOGLE_API_KEY not found. Create a .env with `GOOGLE_API_KEY=...`")
    st.stop()

genai.configure(api_key=api_key)

# -----------------------------
# Helpers
# -----------------------------
def list_available_models():
    """
    Return a list of model ids (strings) that support generateContent.
    Falls back to a safe static list if listing fails.
    """
    fallback = [
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
        "gemini-2.5-pro",
        "gemini-flash-latest",
    ]
    try:
        models = genai.list_models()
        names = []
        for m in models:
            methods = getattr(m, "supported_generation_methods", []) or []
            if "generateContent" in methods:
                # API returns names like "models/gemini-2.5-flash"
                names.append(m.name.split("/")[-1])
        # Prefer a sensible order; keep any others at the end
        prefs = ["gemini-2.5-flash", "gemini-2.5-flash-lite", "gemini-2.5-pro", "gemini-flash-latest"]
        ordered = [m for m in prefs if m in names] + [m for m in names if m not in prefs]
        return ordered or fallback
    except Exception:
        return fallback

def ensure_chat(model_name: str):
    """
    (Re)create a chat session if needed or if the model changed.
    """
    if "chat_model_name" not in st.session_state or st.session_state.chat_model_name != model_name:
        st.session_state.chat_model_name = model_name
        st.session_state.model = genai.GenerativeModel(model_name=model_name)
        st.session_state.chat = st.session_state.model.start_chat(history=[])
        # Keep user-visible markdown history separately
        st.session_state.messages = []

# -----------------------------
# Sidebar (settings)
# -----------------------------
with st.sidebar:
    st.header("🤖 AI Chat Settings")

    model_options = list_available_models()
    default_index = 0 if model_options else None
    model_choice = st.selectbox("Select AI Model", model_options, index=default_index)

    temperature = st.slider("Creativity Level", 0.0, 1.0, 0.7, 0.1)

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            if "chat" in st.session_state:
                # Reset the actual chat session history, too
                st.session_state.chat = st.session_state.model.start_chat(history=[])
            st.rerun()
    with col_b:
        st.caption(f"Model: `{model_choice}`")

# Make sure chat session exists for the selected model
ensure_chat(model_choice)

# -----------------------------
# Styles
# -----------------------------
st.markdown(
    """
    <style>
        .stApp { background-color: #1f1e1e; }
        .chat-message { padding: 10px; border-radius: 10px; margin-bottom: 10px; }
        .user-message { background-color: #e6f3ff; text-align: right; }
        .assistant-message { background-color: #f0f0f0; text-align: left; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Main UI
# -----------------------------
st.title("🤖 AI Chat Assistant")

# Initialize message history (for UI rendering)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render prior turns
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Ask me anything...")
if prompt:
    # Show & store user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.chat.send_message(
                    prompt,
                    generation_config={
                        "temperature": float(temperature),
                        "max_output_tokens": 2048,
                    },
                )
                reply = response.text
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"An error occurred: {e}\n\nTip: try switching to another model in the sidebar.")

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown("Powered by Google Gemini AI • Built with ❤️ in Brampton, ON")
