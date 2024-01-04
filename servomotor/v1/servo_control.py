from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

# Imposta la porta GPIO per il servo motore
servo_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

# Imposta il PWM per il servo motore
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)

# Pagina principale
@app.route('/')
def index():
    return render_template('index.html')

# API per controllare il servo motore
@app.route('/control', methods=['POST'])
def control():
    angle = int(request.form['angle'])
    duty_cycle = angle / 18.0 + 2.5
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(1)
    pwm.ChangeDutyCycle(0)
    return "OK"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
