import os
from datetime import datetime
import socket
import cv2
from flask import Flask, render_template, Response

app = Flask(__name__)

# Variabili globali per il tracking
tracking_enabled = False
tracked_person_rect = (0, 0, 0, 0)  # Formato: (x, y, width, height)

# Funzione per il tracking delle persone
def track_person(frame):
    global tracking_enabled, tracked_person_rect

    # Utilizza un classificatore preaddestrato per il riconoscimento delle persone (HOG)
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    # Rileva persone nell'immagine
    rects, weights = hog.detectMultiScale(frame, winStride=(8, 8), padding=(4, 4), scale=1.05)

    # Salva l'intera immagine quando una persona viene rilevata
    if len(rects) > 0:
        save_snapshot(frame)

    # Se vengono rilevate persone, prendi la posizione della prima persona
    if len(rects) > 0:
        tracked_person_rect = tuple(rects[0])

    # Disegna il rettangolo verde intorno alla persona rilevata
    if tracking_enabled:
        (x, y, w, h) = tracked_person_rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Funzione per catturare il flusso video dalla telecamera
def generate_frames():
    camera = cv2.VideoCapture(0)  # Puoi regolare il parametro a seconda della tua telecamera

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Applica le ottimizzazioni
            frame = optimize_frame(frame)

            # Ruota il frame di 90 gradi a sinistra
            frame = cv2.transpose(frame)
            frame = cv2.flip(frame, 180)

            if tracking_enabled:
                track_person(frame)

            # Invia il frame ottimizzato
            ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Funzione per applicare ottimizzazioni al frame
def optimize_frame(frame):
    # Riduci la risoluzione del frame
    frame = cv2.resize(frame, (640, 480))
    return frame

# Funzione per salvare un'immagine istantanea
def save_snapshot(frame):
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f'/cam/photos/{socket.gethostname()}-{timestamp}.jpg'

    # Crea la directory se non esiste
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Salva l'immagine
    cv2.imwrite(filename, frame)

# Route principale per la pagina web
@app.route('/')
def index():
    return render_template('index.html', tracking_enabled=tracking_enabled)

# Route per il controllo del tracking
@app.route('/control/<action>')
def control(action):
    global tracking_enabled
    if action == 'start':
        tracking_enabled = True
    elif action == 'stop':
        tracking_enabled = False
    return 'OK'

# Route per il video in tempo reale
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
