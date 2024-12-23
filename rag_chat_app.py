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
    st.rerun()  # Updated to st.rerun()

def main():
    st.title("RAG Chat System")
    user = st.text_input("Enter your username")

    if user:
        # Connect to SocketIO server
        if not sio.connected:
            try:
                print("Connecting to SocketIO server...")
                sio.connect('http://localhost:5000')
                print("Connected to SocketIO server")
            except Exception as e:
                st.error(f"Failed to connect to SocketIO server: {e}")
                print(f"Error connecting to SocketIO: {e}")

        # Chat interface
        st.subheader("Chat")
        
        # Display chat messages
        messages = db.get_messages()
        print(f"Messages retrieved: {messages}")
        for idx, msg in enumerate(reversed(messages)):
            message(msg['message'], is_user=msg['user'] == user, key=f"msg_{idx}_{msg['user']}")
        
        # Input for new message
        new_message = st.text_input("Type your message")
        if st.button("Send"):
            print(f"Sending message: {new_message}")
            try:
                # Save message to database
                db.save_message(user, new_message, time.time())
                
                # Send message via SocketIO
                sio.emit('message', {'user': user, 'message': new_message})
                
                # Get AI response
                ai_response = rag.query(new_message)
                print(f"AI Response: {ai_response}")
                db.save_message("AI", ai_response, time.time())
                
                # Clear input
                st.rerun()
            except Exception as e:
                print(f"Error sending message or getting AI response: {e}")
                st.error(f"An error occurred while processing your message: {e}")
        
        # File upload
        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            try:
                file_contents = uploaded_file.read()
                db.save_file(uploaded_file.name, file_contents, user)
                st.success(f"File {uploaded_file.name} uploaded successfully!")
            except Exception as e:
                print(f"Error uploading file: {e}")
                st.error(f"Failed to upload file: {e}")

if __name__ == "__main__":
    main()
