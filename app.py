"""Main application entry point"""
import streamlit as st
from modules.initialization.session import init_session_state
from modules.initialization.components import init_components
from modules.initialization.signals import setup_signal_handlers

def main():
    """Main application function"""
    st.set_page_config(
        page_title="RAGify Chat",
        page_icon="💬",
        layout="wide"
    )
    
    # Initialize application
    init_session_state()
    init_components()
    setup_signal_handlers()
    
    st.title("RAGify Chat")
    
    # Layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.session_state.chat_interface.display_chat()
        st.session_state.chat_interface.message_input()

    with col2:
        st.session_state.file_handler.upload_section()
        st.session_state.rag_engine.display_context()

if __name__ == "__main__":
    main()