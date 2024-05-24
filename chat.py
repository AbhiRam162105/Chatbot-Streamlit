import streamlit as st
import os
import google.generativeai as ggi

st.title("Shopping Assistant")

# Access the environment variable
api_key = os.environ.get('FETCHEED_API_KEY')
print(api_key)

if not api_key:
    st.error("API Key not found. Please set the FETCHEED_API_KEY environment variable.")
else:
    ggi.configure(api_key=api_key)

model = ggi.GenerativeModel("gemini-pro")
chat = model.start_chat()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = chat.send_message(prompt, stream=True)
        responses = []
        stream.resolve()
        for candidate in stream.candidates:
            for part in candidate.content.parts:
                responses.append(part.text)

        # Join all responses into a single string
        response_text = "\n".join(responses)
        st.session_state.messages.append({"role": "assistant", "content": response_text})

        # Display the response
        st.write(response_text)
