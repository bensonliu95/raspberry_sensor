import RPi.GPIO as GPIO
import time
import random

GPIO.setmode(GPIO.BCM)
RED_LED_PIN = 2
BLUE_LED_PIN = 3
GREEN_LED_PIN = 4
PWM_FREQ = 200

GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_LED_PIN, GPIO.OUT)
GPIO.setup(BLUE_LED_PIN, GPIO.OUT)
GPIO.setup(GREEN_LED_PIN, GPIO.OUT)

red_pwm = GPIO.PWM(RED_LED_PIN, PWM_FREQ)
red_pwm.start(0)
blue_pwm = GPIO.PWM(BLUE_LED_PIN, PWM_FREQ)
blue_pwm.start(0)
green_pwm = GPIO.PWM(GREEN_LED_PIN, PWM_FREQ)
green_pwm.start(0)

def setColor(r=0, g=0, b=0):
    red_pwm.ChangeDutyCycle(100-int(r/255*100))
    blue_pwm.ChangeDutyCycle(100-int(b/255*100))
    green_pwm.ChangeDutyCycle(100-int(g/255*100))

def light_01():
    try:
        while True:
            print('按下 Ctrl-C 可停止程式')
            print('自動展示開始')
            print('紅色')
            setColor(255, 0, 0)
            time.sleep(3)
            print('綠色')
            setColor(0, 255, 0)
            time.sleep(3)
            print('藍色')
            setColor(0, 0, 255)
            time.sleep(3)
            print('熄滅')
            setColor(0, 0, 0)
            time.sleep(3)
            print('白色')
            setColor(255, 255, 255)
            time.sleep(3)
            break
    except KeyboardInterrupt:
        print('關閉程式')
    finally:
        red_pwm.stop()
        blue_pwm.stop()
        green_pwm.stop()
        GPIO.cleanup()