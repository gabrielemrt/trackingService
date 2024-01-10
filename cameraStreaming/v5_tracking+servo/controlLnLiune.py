from flask import Flask, render_template, request, Response
import cv2
import threading
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

# Configurazione dei pin GPIO per i servomotori
X_AXIS_PIN = 17
Y_AXIS_PIN = 18

# Inizializzazione dei pin GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(X_AXIS_PIN, GPIO.OUT)
GPIO.setup(Y_AXIS_PIN, GPIO.OUT)

# Inizializzazione degli oggetti PWM per i servomotori
x_axis_pwm = GPIO.PWM(X_AXIS_PIN, 50)
y_axis_pwm = GPIO.PWM(Y_AXIS_PIN, 50)

# Avvio dei servomotori
x_axis_pwm.start(0)
y_axis_pwm.start(0)

# Variabili globali per la posizione dei servomotori
x_position = 0
y_position = 0

# Funzione per muovere il servomotore sull'asse X
def move_x_axis(position):
    duty = float(position) / 18.0 + 2.5
    x_axis_pwm.ChangeDutyCycle(duty)

# Funzione per muovere il servomotore sull'asse Y
def move_y_axis(position):
    duty = float(position) / 18.0 + 2.5
    y_axis_pwm.ChangeDutyCycle(duty)

# Funzione per catturare il flusso video dalla telecamera
def generate_frames():
    camera = cv2.VideoCapture(0, cv2.CAP_V4L2)  # Utilizza il backend V4L2

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Ruota il frame di 90 gradi a sinistra
            frame = cv2.transpose(frame)
            frame = cv2.flip(frame, 180)
            
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Route principale per la pagina web
@app.route('/')
def index():
    return render_template('index.html')

# Route per controllare i servomotori
@app.route('/control', methods=['POST'])
def control():
    global x_position, y_position

    x_position = int(request.form['x_position'])
    y_position = int(request.form['y_position'])

    move_x_axis(x_position)
    move_y_axis(y_position)

    return 'OK'

# Route per il video in tempo reale
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
