from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

# Configurar SocketIO con eventlet para producción
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AUDITORY // LIVE</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <style>
        body { background: #000; color: #0f0; text-align: center; font-family: monospace; margin: 0; padding: 0; overflow: hidden; }
        h1 { margin: 10px; font-size: 20px; }
        img { width: 100vw; height: 100vh; object-fit: contain; }
    </style>
</head>
<body>
    <h1>AUDITORY LIVE STREAM</h1>
    <img id="video" src="" />
    <script>
        var socket = io();
        socket.on('video_frame', function(msg) {
            document.getElementById('video').src = 'data:image/jpeg;base64,' + msg.data;
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@socketio.on('video_frame')
def handle_frame(data):
    # Reenviar el frame a todos los clientes conectados (tu navegador)
    emit('video_frame', data, broadcast=True)

if __name__ == "__main__":
    # Render asigna un puerto dinámico en la variable de entorno PORT
    port = int(os.environ.get("PORT", 10000))
    socketio.run(app, host='0.0.0.0', port=port)
