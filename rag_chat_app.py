import streamlit as st
from streamlit_chat import message
import socketio
from database import Database
from rag_model import RAGModel
import time

# Initialize database and RAG model
db = Database()
rag = RAGModel()

# SocketIO client setup
sio = socketio.Client()

@sio.event
def connect():
    print("Connected to SocketIO server")

@sio.event
def disconnect():
    print("Disconnected from SocketIO server")

@sio.on('message')
def on_message(data):
    st.experimental_rerun()

# Streamlit app
def main():
    st.title("RAG Chat System")

    # User authentication (simplified)
    user = st.text_input("Enter your username")

    if user:
        # Connect to SocketIO server
        if not sio.connected:
            try:
                sio.connect('http://localhost:5000')
            except Exception as e:
                st.error(f"Failed to connect to SocketIO server: {e}")

        # Chat interface
        st.subheader("Chat")
        
        # Display chat messages
        messages = db.get_messages()
        for msg in reversed(messages):
            message(msg['message'], is_user=msg['user'] == user)

        # Input for new message
        new_message = st.text_input("Type your message")
        if st.button("Send"):
            # Save message to database
            db.save_message(user, new_message, time.time())
            
            # Send message via SocketIO
            sio.emit('message', {'user': user, 'message': new_message})
            
            # Get AI response
            ai_response = rag.query(new_message)
            db.save_message("AI", ai_response, time.time())
            
            # Clear input
            st.experimental_rerun()

        # File upload
        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            # Save file to database
            file_contents = uploaded_file.read()
            db.save_file(uploaded_file.name, file_contents, user)
            st.success(f"File {uploaded_file.name} uploaded successfully!")

if __name__ == "__main__":
    main()