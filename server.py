from flask import Flask, render_template, request
from flask_socketio import SocketIO, send
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(msg):
    # 1. Calculate payload size in bytes
    payload_size = len(msg.encode('utf-8'))
    
    # 2. Generate precise timestamp
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    
    # 3. Package the metadata with the text
    packet = {
        "text": msg,
        "sender": request.sid,
        "size": payload_size,
        "time": timestamp
    }
    
    # 4. Print raw routing log to your laptop's terminal
    print(f"[ROUTER] Time: {timestamp} | Node: {request.sid[:6]}... | Payload: {payload_size} Bytes | Status: Broadcasted")
    
    send(packet, broadcast=True)

if __name__ == '__main__':
    print("[SYSTEM] DCN WebSocket Server Initialized on Port 5000")
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)
