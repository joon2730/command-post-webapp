import streamlit as st
import time
import command_post.config as config
from command_post.context_builder import generate_context_prompt
from command_post.domain import determine_domain, SPINNER_MSG
from command_post.ollama_binding import ollama_generate

# App title
st.set_page_config(page_title="Command-Post: Loyal Assistant", page_icon="☕", layout="wide")

@st.cache_data
def load_config():
    return config.Config()

# Load configuration
base_config = load_config()

# Initialize session state
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
if "config" not in st.session_state.keys():
    st.session_state.config = {'language': 'en', 'command_post_model': base_config.command_post_model}

session_config = st.session_state.config

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
if prompt := st.chat_input("Ask me about today's news..."):
    # User query
    st.session_state.messages.append({"role": "user", "content": prompt}) # Save user message
    with st.chat_message("user"):
        st.markdown(prompt)     # Display user message

    # Assistant response
    with st.chat_message("assistant"): 
        with st.spinner("Categorizing the Request..."):
            domain = determine_domain(prompt, session_config) # Determine domain of the request
        
        with st.spinner(SPINNER_MSG[domain]):
            prompt, data = generate_context_prompt(prompt, domain, session_config) # Retrieve real-time context
    
        with st.spinner("Formulating Response..."):
            response = ollama_generate(session_config['command_post_model'], prompt)  # Get response from the model
        
        # Display response with typing effect
        placeholder = st.empty()
        full_response = ''
        for item in response.split(' '): # Simulate typing effect
            full_response += item + ' '
            placeholder.markdown(full_response)
            time.sleep(0.03)

    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": response})