from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import time
import threading

app = Flask(__name__)

# Imposta la porta GPIO per il servo motore
servo_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

# Imposta il PWM per il servo motore
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)

# Variabili per gestire il movimento fluido del servo
current_angle = 90
target_angle = 90
transition_time = 1.0  # Tempo di transizione in secondi
movement_lock = threading.Lock()

# Funzione per il movimento fluido del servo
def move_servo():
    global current_angle, target_angle, transition_time

    start_angle = current_angle
    end_angle = target_angle

    for angle in range(int(start_angle), int(end_angle), 1 if start_angle < end_angle else -1):
        duty_cycle = angle / 18.0 + 2.5
        pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(transition_time / abs(end_angle - start_angle))

    pwm.ChangeDutyCycle(0)
    current_angle = target_angle

# Pagina principale
@app.route('/')
def index():
    return render_template('index.html')

# API per controllare il servo motore
@app.route('/control', methods=['POST'])
def control():
    global target_angle, movement_lock

    angle = int(request.form['angle'])
    
    with movement_lock:
        target_angle = angle
        threading.Thread(target=move_servo).start()

    return "OK"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')