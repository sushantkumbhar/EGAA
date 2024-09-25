
import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import time


print("Starting Streamlit_app.py")
from appv3 import invoke_llm_with_user_question, Agent_Executor_Class
print("Finished importing from appv2.py")
# initialize_resources()
# Set page config

st.set_page_config(
    page_title="EGAA",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Custom CSS to make it fancy
st.markdown("""
<style>
    .reportview-container {
        background: linear-gradient(to right, #1a2980, #26d0ce);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(to bottom, #1a2980, #26d0ce);
    }
    .st-bb {
        background-color: rgba(255,255,255,0.1);
    }
    .st-at {
        background-color: #1a2980;
    }
    .st-cc {
        color: white !important;
    }
  .custom-loader {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 9999;
    width: 100px;
    height: 100px;
    border: 8px solid #f3f3f3;
    border-top: 8px solid #3498db;
    border-radius: 50%;
    animation: spin 2s linear infinite;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
</style>
""", unsafe_allow_html=True)

# Check if the app has finished loading
if 'loaded' not in st.session_state:
    # Show loader
    with st.spinner('Loading...'):
        time.sleep(2)
    # Set the loaded state to True
    st.session_state.loaded = True

if 'obj' not in st.session_state:

    obj = Agent_Executor_Class()
    st.session_state['obj'] = obj
    st.success("AI agent initialized successfully!")
else:
    print('Agent already initialized')
# Initialize chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Only show the main content if the app has finished loading
if st.session_state.get('loaded', True):
    # Sidebar
    st.sidebar.header("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Insights", "About Us"])

    # Add document upload feature
    st.sidebar.header("Upload Document")
    uploaded_file = st.sidebar.file_uploader("Choose a file", type=["pdf", "docx", "txt"])
    if uploaded_file is not None:
        st.sidebar.success(f"File {uploaded_file.name} uploaded successfully!")

    # Title and description
    st.title("🌟 EGAA - Empowering Growth and Accelerating Achievements")
    st.markdown("Welcome to the EGAA dashboard, your one-stop solution for financial insights and loan management.")

    # Display chatbot information above the input box
    st.info("I'm your AI assistant for loan and financial inquiries. Feel free to ask me anything!")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me anything about loans or financial insights:"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.spinner("Thinking..."):
            # Process the user input and generate a response using the imported function
            response = invoke_llm_with_user_question(st.session_state.obj.agent_executor, prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})


    elif page == "About Us":
        st.header("About EGAA")
        st.write("EGAA is committed to providing cutting-edge financial solutions.")
        
        # Team info
        st.subheader("Our Team")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.image("https://via.placeholder.com/150", caption="John Doe - CEO")
        with col2:
            st.image("https://via.placeholder.com/150", caption="Jane Smith - CTO")
        with col3:
            st.image("https://via.placeholder.com/150", caption="Bob Johnson - CFO")

    # Footer
    # st.markdown("---")
    # st.markdown("© 2024 EGAA. All rights reserved.")
