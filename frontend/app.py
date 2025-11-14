import streamlit as st
import requests

# ---------------- Config ----------------
BACKEND_URL = "http://127.0.0.1:8000/query"

st.set_page_config(page_title="💬 Customer FAQ Chatbot", layout="wide")

# ---------------- Session State ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- Title ----------------
st.title("💬 Customer FAQ Chatbot (RAG-powered)")

# ---------------- Chat History ----------------
for msg in st.session_state.messages:
    # Use the new chat message element
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("sources"):
            with st.expander("📚 Sources used"):
                for s in msg["sources"]:
                    st.write(f"- {s}")

# ---------------- Input ----------------
user_input = st.chat_input("Type your question here...")

if user_input:
    # Append user message to history and display
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    try:
        resp = requests.post(BACKEND_URL, json={"question": user_input})
        if resp.status_code == 200:
            data = resp.json()
            bot_answer = data.get("answer", "⚠️ No answer found.")

            # Collect sources, including the score for more context
            sources = []
            if data.get("source_question"):
                score = data.get("score")
                sources.append(f"Q: {data['source_question']} (Score: {score:.2f})")
            if data.get("suggestion"):
                sources.append(f"Suggested: {data['suggestion']}")

            # Save bot response
            st.session_state.messages.append({
                "role": "assistant", # Changed from "bot" to "assistant"
                "content": bot_answer,
                "sources": sources
            })

            # Display bot response
            with st.chat_message("assistant"):
                st.write(bot_answer)
                if sources:
                    with st.expander("📚 Sources used"):
                        for s in sources:
                            st.write(f"- {s}")
        else:
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"⚠️ Error: {resp.status_code} - {resp.text}"
            })
            with st.chat_message("assistant"):
                st.write(f"⚠️ Error: {resp.status_code} - {resp.text}")
    except Exception as e:
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"⚠️ Backend not reachable. {e}"
        })
        with st.chat_message("assistant"):
            st.write(f"⚠️ Backend not reachable. {e}")