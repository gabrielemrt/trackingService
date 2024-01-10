from flask import Flask, render_template, Response, request
import cv2
import os
from datetime import datetime
import socket


app = Flask(__name__)

# Percorso per le immagini catturate
capture_path = "/cam/capture"

# Inizializza la telecamera
cap = cv2.VideoCapture(0)  # 0 indica la telecamera predefinita

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture', methods=['POST'])
def capture():
    if request.method == 'POST':
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d-%H-%M")
        filename = f"{socket.gethostname()}-{timestamp}.jpg"
        filepath = os.path.join(capture_path, filename)

        success, frame = cap.read()
        if success:
            cv2.imwrite(filepath, frame)
            return "Immagine catturata e salvata con successo!"
        else:
            return "Errore durante la cattura e il salvataggio dell'immagine."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
