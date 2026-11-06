from flask import Flask, Response, render_template_string, request
from collections import deque

app = Flask(__name__)

# Guarda los últimos frames en memoria
frames = deque(maxlen=1)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AUDITORY // LIVE CAM</title>
    <style>
        body { background: #000; color: #0f0; text-align: center; font-family: monospace; margin: 0; padding: 0; overflow: hidden; }
        h1 { margin: 10px; font-size: 20px; }
        img { width: 100vw; height: 100vh; object-fit: contain; }
    </style>
</head>
<body>
    <h1>AUDITORY LIVE STREAM</h1>
    <img src="/video_feed" />
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/video_feed')
def video_feed():
    def generate():
        while True:
            if frames:
                frame = frames[-1]
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/upload_frame', methods=['POST'])
def upload_frame():
    frame_data = request.data
    if frame_data:
        frames.append(frame_data)
    return "OK"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
