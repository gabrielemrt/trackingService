from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import time
import threading

app = Flask(__name__)

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

    start_angle_y = current_angle_y
    end_angle_y = target_angle_y

    steps = 100  # Numero di passaggi per la transizione
    delay = transition_time / steps

    for step in range(steps + 1):
        # Calcola l'angolazione corrente in base al passo della transizione
        current_angle_x = start_angle_x + (end_angle_x - start_angle_x) * step / steps
        current_angle_y = start_angle_y + (end_angle_y - start_angle_y) * step / steps

        # Calcola i cicli di lavoro per i servo motori
        duty_cycle_x = current_angle_x / 18.0 + 2.5
        duty_cycle_y = current_angle_y / 18.0 + 2.5

        # Assicurati che i valori di duty cycle siano nel range corretto
        duty_cycle_x = max(0, min(duty_cycle_x, 100))
        duty_cycle_y = max(0, min(duty_cycle_y, 100))

        # Imposta i cicli di lavoro sui servo motori solo se sono validi
        if 0 <= duty_cycle_x <= 100:
            pwm_x.ChangeDutyCycle(duty_cycle_x)
        if 0 <= duty_cycle_y <= 100:
            pwm_y.ChangeDutyCycle(duty_cycle_y)

        time.sleep(delay)

    # Fai in modo che l'angolazione attuale corrisponda all'angolazione finale
    current_angle_x = target_angle_x
    current_angle_y = target_angle_y

    # Arresta i servo motori
    pwm_x.ChangeDutyCycle(0)
    pwm_y.ChangeDutyCycle(0)



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
