import streamlit as st
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

# --- HARD-CODED OPENAI API KEY ---
client = OpenAI(api_key="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")

# Streamlit setup
st.set_page_config(page_title="Chatbot", layout="centered")
st.title("🤖 Simple AI Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    role_label = "🧑 You" if msg["role"] == "user" else "🤖 Bot"
    with st.chat_message(role_label):
        st.markdown(msg["content"], unsafe_allow_html=True)

# User input
user_input = st.chat_input("Type your message and press Enter...")

if user_input:
    # Show user message
    st.chat_message("🧑 You").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        # Prepare messages for the API
        formatted_messages: list[ChatCompletionMessageParam] = [
            {"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages
        ]

        # Call OpenAI Chat API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=formatted_messages
        )

        reply = response.choices[0].message.content
        st.chat_message("🤖 Bot").markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
