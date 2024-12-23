import streamlit as st
from streamlit_chat import message
import socketio
from database import Database
from rag_model import RAGModel
import time
import eventlet
from multiprocessing import Process

# Initialize database and RAG model
db = Database()
rag = RAGModel()

# SocketIO server setup
sio_server = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio_server)

@sio_server.event
def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio_server.event
def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio_server.event
def message(sid, data):
    print(f"Message from {sid}: {data}")
    sio_server.emit('message', data, skip_sid=sid)

# SocketIO client setup
sio_client = socketio.Client()

@sio_client.event
def connect():
    print("Connected to SocketIO server")

@sio_client.event
def disconnect():
    print("Disconnected from SocketIO server")

@sio_client.on('message')
def on_message(data):
    st.experimental_rerun()

# Streamlit app
def streamlit_app():
    st.title("RAG Chat System")

    # User authentication (simplified)
    user = st.text_input("Enter your username")

    if user:
        # Connect to SocketIO server
        if not sio_client.connected:
            sio_client.connect('http://localhost:5000')

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
            sio_client.emit('message', {'user': user, 'message': new_message})
            
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

def run_socketio_server():
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)

if __name__ == "__main__":
    # Start SocketIO server in a separate process
    server_process = Process(target=run_socketio_server)
    server_process.start()

    # Run Streamlit app
    import streamlit.web.bootstrap as bootstrap
    bootstrap.run(streamlit_app, '', [], flag_options={})

    # Wait for the server process to finish
    server_process.join()