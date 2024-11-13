import streamlit as st
from flowise import Flowise, PredictionData
import json

# Flowise app base url
base_url = st.secrets["https://qa-admin.precisionai-portal.bayer.com:8510/chatbot/05d59e9b-376a-41be-bff7-764baf8737a8"] or "https://qa-admin.precisionai-portal.bayer.com:8510/chatbot/05d59e9b-376a-41be-bff7-764baf8737a8"

# Chatflow/Agentflow ID
flow_id = st.secrets["abc"] or "abc"

# Show title and description.
st.title("💬 Flowise Streamlit Chat")
st.write(
    "This is a simple chatbot that uses Flowise Python SDK"
)

# Create a Flowise client.
client = Flowise(base_url=base_url)

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def generate_response(prompt: str):
    print('generating response')
    completion = client.create_prediction(
        PredictionData(
            chatflowId=flow_id,
            question=prompt,
            overrideConfig={
                "sessionId": "session1234"
            },
            streaming=True
        )
    )

    for chunk in completion:
        print(chunk)
        parsed_chunk = json.loads(chunk)
        if (parsed_chunk['event'] == 'token' and parsed_chunk['data'] != ''):
            yield str(parsed_chunk['data'])

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("What is up?"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Stream the response to the chat using `st.write_stream`, then store it in 
    # session state.
    with st.chat_message("assistant"):
        response = generate_response(prompt)
        full_response = st.write_stream(response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
