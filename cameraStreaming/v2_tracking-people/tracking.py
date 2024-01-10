from flask import Flask, render_template, Response
import cv2
import threading

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
            # Ruota il frame di 90 gradi a sinistra
            frame = cv2.transpose(frame)
            frame = cv2.flip(frame, 180)
            
            if tracking_enabled:
                track_person(frame)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Route principale per la pagina web
@app.route('/')
def index():
    return render_template('index.html')

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
