import eventlet
from flask import Flask, render_template_string
import socketio

# Create a Socket.IO server
sio = socketio.Server(cors_allowed_origins='*')

# Create a Flask app
flask_app = Flask(__name__)

# Serve an HTML page at the root using Flask
@flask_app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.socket.io/4.5.0/socket.io.min.js"></script>
        <script>
            const socket = io();
            socket.on('connect', () => {
                console.log('Connected to server');
            });
            socket.on('message', (data) => {
                console.log('Message from server:', data);
            });
            function sendMessage() {
                const message = document.getElementById('message').value;
                socket.emit('message', message);
            }
        </script>
    </head>
    <body>
        <h1>Socket.IO Server</h1>
        <input type="text" id="message" placeholder="Type a message">
        <button onclick="sendMessage()">Send</button>
    </body>
    </html>
    """)

# Wrap Flask app with Socket.IO server
app = socketio.WSGIApp(sio, flask_app)

# Define Socket.IO events
@sio.event
def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.event
def message(sid, data):
    print(f"Message from {sid}: {data}")
    sio.emit('message', data, skip_sid=sid)

# Run the combined server
if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
