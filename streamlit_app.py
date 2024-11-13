import streamlit as st

st.title("🎈 Maik new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."    
)

import streamlit as requests
st.title("🎈 Chatbot")
API_URL = "https://qa-admin.precisionai-portal.bayer.com:8510/api/v1/prediction/05d59e9b-376a-41be-bff7-764baf8737a8"

def query(payload):
    response = requests.post(API_URL, json=payload)
    return response.json()
    
output = query({
    "question": "Hey, how are you?",
})
