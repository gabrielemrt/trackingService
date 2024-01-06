from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import time
import threading

app = Flask(__name__, static_url_path='/static', static_folder='static')

# Imposta la porta GPIO per il servo motore sull'asse X
servo_x_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_x_pin, GPIO.OUT)
pwm_x = GPIO.PWM(servo_x_pin, 50)
pwm_x.start(0)

# Imposta la porta GPIO per il servo motore sull'asse Y
servo_y_pin = 19
GPIO.setup(servo_y_pin, GPIO.OUT)
pwm_y = GPIO.PWM(servo_y_pin, 50)
pwm_y.start(0)

# Variabili per gestire il movimento fluido dei servomotori
current_angle_x = 90
target_angle_x = 90
current_angle_y = 90
target_angle_y = 90
transition_time = 1.0  # Tempo di transizione in secondi
movement_lock = threading.Lock()

# Funzione per il movimento fluido dei servomotori
def move_servos():
    global current_angle_x, target_angle_x, current_angle_y, target_angle_y

    start_angle_x = current_angle_x
    end_angle_x = target_angle_x

    for angle_x in range(int(start_angle_x), int(end_angle_x), 1 if start_angle_x < end_angle_x else -1):
        duty_cycle_x = angle_x / 18.0 + 2.5
        pwm_x.ChangeDutyCycle(duty_cycle_x)
        time.sleep(transition_time / abs(end_angle_x - start_angle_x))

    pwm_x.ChangeDutyCycle(0)
    current_angle_x = target_angle_x

    # Ripeti lo stesso processo per l'asse Y
    start_angle_y = current_angle_y
    end_angle_y = target_angle_y

    for angle_y in range(int(start_angle_y), int(end_angle_y), 1 if start_angle_y < end_angle_y else -1):
        duty_cycle_y = angle_y / 18.0 + 2.5
        pwm_y.ChangeDutyCycle(duty_cycle_y)
        time.sleep(transition_time / abs(end_angle_y - start_angle_y))

    pwm_y.ChangeDutyCycle(0)
    current_angle_y = target_angle_y

# Pagina principale
@app.route('/')
def index():
    return render_template('index.html')

# API per controllare i servomotori
@app.route('/control', methods=['POST'])
def control():
    global target_angle_x, target_angle_y, movement_lock

    angle_x = int(request.form['angle_x'])
    angle_y = int(request.form['angle_y'])

    with movement_lock:
        target_angle_x = angle_x
        target_angle_y = angle_y
        threading.Thread(target=move_servos).start()

    return "OK"

# API per il movimento di 10° negli assi X e Y
@app.route('/move_10', methods=['POST'])
def move_10():
    global target_angle_x, target_angle_y, movement_lock

    direction = request.form['direction']

    with movement_lock:
        if direction == 'up':
            target_angle_y += 10
        elif direction == 'down':
            target_angle_y -= 10
        elif direction == 'left':
            target_angle_x -= 10
        elif direction == 'right':
            target_angle_x += 10

        threading.Thread(target=move_servos).start()

    return "OK"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
