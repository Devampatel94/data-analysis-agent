import streamlit as st
from agent import DataAgent
from src.file_upload import load_file_from_upload

# Streamlit app
st.set_page_config(page_title="Data Analyst Agent", layout="wide")
st.title("🧠 Smart Data Analyst Agent")

if "agent" not in st.session_state:
    st.session_state.agent = DataAgent()
    st.session_state.file_uploaded = False

uploaded_file = st.file_uploader("📤 Upload a file", type=["csv", "xlsx", "txt","pdf","docx", "jpg", "jpeg", "png"])

if uploaded_file and not st.session_state.file_uploaded:
    file_type, content = load_file_from_upload(uploaded_file)
    st.session_state.agent.load(file_type, content)
    st.session_state.file_uploaded = True
    st.success("✅ File processed!")

if st.session_state.file_uploaded:
    query = st.text_input("💬 Ask a question or request a chart:")
    if query:
        with st.spinner("Thinking..."):
            response, fig = st.session_state.agent.ask(query)
        st.markdown(f"**🤖 Agent:** {response}")
        if fig:
            st.pyplot(fig)