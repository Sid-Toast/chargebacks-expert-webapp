import streamlit as st
import requests
import json

# --- Configuration ---
API_URL = "https://ghctsltbp2.execute-api.eu-north-1.amazonaws.com/prod/ask"
API_HEADERS = {"Content-Type": "application/json"}

# --- Streamlit App ---

st.set_page_config(page_title="Chargebacks Expert", page_icon="🤖", layout="centered")

st.title("🤖 Chargebacks Expert")
st.caption("Your personal AI assistant, powered by Slack conversations.")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "How can I help you today?"})

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask a question about chargebacks..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")

        try:
            # Prepare the data to send to the API
            payload = json.dumps({"prompt": prompt})

            # Call the API
            response = requests.post(API_URL, headers=API_HEADERS, data=payload)
            response.raise_for_status()  # Raise an exception for bad status codes

            # The response body is a JSON string, so we need to parse it twice.
            # 1. Parse the main response body
            # 2. Get the 'body' key, which is also a JSON string, and parse that
            api_response_body = response.json()
            answer_data = json.loads(api_response_body.get("body", "{}"))
            
            full_response = answer_data.get("answer", "I could not find an answer.")
            message_placeholder.markdown(full_response)

        except requests.exceptions.RequestException as e:
            full_response = f"Error: Could not connect to the API. {e}"
            message_placeholder.markdown(full_response)
        except (json.JSONDecodeError, KeyError) as e:
            full_response = f"Error: Could not parse the API response. {e}"
            message_placeholder.markdown(full_response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response}) 