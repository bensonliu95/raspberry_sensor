#!/usr/bin/env python
from Adafruit_PWM_Servo_Driver import PWM
import RPi.GPIO as GPIO
import time
import sys

PWMA   = 18
AIN1   = 22
AIN2   = 27

PWMB   = 23
BIN1   = 25
BIN2   = 24

BtnPin  = 19
Gpin    = 5
Rpin    = 6

TRIG = 20
ECHO = 21

#右紅外線
SensorRight = 16
#左紅外線
SensorLeft  = 12
# Initialise the PWM device using the default address
# bmp = PWM(0x40, debug=True)
pwm = PWM(0x40,debug = False)

servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096

#  --------------------------------蜂鳴器
Buzzer = 17

CL = [0, 131, 147, 165, 175, 196, 211, 248]		# Frequency of Low C notes

CM = [0, 262, 294, 330, 350, 393, 441, 495]		# Frequency of Middle C notes

CH = [0, 525, 589, 661, 700, 786, 882, 990]		# Frequency of High C notes

song_1 = [	CM[3], CM[5], CM[6], CM[3], CM[2], CM[3], CM[5], CM[6], # Notes of song1
			CH[1], CM[6], CM[5], CM[1], CM[3], CM[2], CM[2], CM[3], 
			CM[5], CM[2], CM[3], CM[3], CL[6], CL[6], CL[6], CM[1],
			CM[2], CM[3], CM[2], CL[7], CL[6], CM[1], CL[5]	]

beat_1 = [	1, 1, 3, 1, 1, 3, 1, 1, 			# Beats of song 1, 1 means 1/8 beats
			1, 1, 1, 1, 1, 1, 3, 1, 
			1, 3, 1, 1, 1, 1, 1, 1, 
			1, 2, 1, 1, 1, 1, 1, 1, 
			1, 1, 3	]

song_2 = [	CM[1], CM[1], CM[1], CL[5], CM[3], CM[3], CM[3], CM[1], # Notes of song2
			CM[1], CM[3], CM[5], CM[5], CM[4], CM[3], CM[2], CM[2], 
			CM[3], CM[4], CM[4], CM[3], CM[2], CM[3], CM[1], CM[1], 
			CM[3], CM[2], CL[5], CL[7], CM[2], CM[1]	]

beat_2 = [	1, 1, 2, 2, 1, 1, 2, 2, 			# Beats of song 2, 1 means 1/8 beats
			1, 1, 2, 2, 1, 1, 3, 1, 
			1, 2, 2, 1, 1, 2, 2, 1, 
			1, 2, 2, 1, 1, 3 ]
#  --------------------------------------------------------------------------------------------------------



def setServoPulse(channel, pulse):
  pulseLength = 1000000.0                   # 1,000,000 us per second
  pulseLength /= 50.0                       # 60 Hz
  #print ("%d us per period" % pulseLength)
  pulseLength /= 4096.0                     # 12 bits of resolution
  #print ("%d us per bit" % pulseLength)
  pulse *= 1000.0
  pulse /= (pulseLength*1.0)
# pwmV=int(pluse)
#   print ("pluse: %f  " % (pulse))
  pwm.setPWM(channel, 0, int(pulse))

#Angle to PWM
def write(servonum,x):
  y=x/90.0+0.5
  y=max(y,0.5)
  y=min(y,2.5)
  setServoPulse(servonum,y)
  
def t_up(speed,t_time):
        L_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2,False)#AIN2
        GPIO.output(AIN1,True) #AIN1

        R_Motor.ChangeDutyCycle(speed)
        GPIO.output(BIN2,False)#BIN2
        GPIO.output(BIN1,True) #BIN1
        time.sleep(t_time)
        
def t_stop(t_time):
        L_Motor.ChangeDutyCycle(0)
        GPIO.output(AIN2,False)#AIN2
        GPIO.output(AIN1,False) #AIN1

        R_Motor.ChangeDutyCycle(0)
        GPIO.output(BIN2,False)#BIN2
        GPIO.output(BIN1,False) #BIN1
        time.sleep(t_time)
        
def t_down(speed,t_time):
        L_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2,True)#AIN2
        GPIO.output(AIN1,False) #AIN1

        R_Motor.ChangeDutyCycle(speed)
        GPIO.output(BIN2,True)#BIN2
        GPIO.output(BIN1,False) #BIN1
        time.sleep(t_time)

def t_left(speed,t_time):
        L_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2,True)#AIN2
        GPIO.output(AIN1,False) #AIN1

        R_Motor.ChangeDutyCycle(speed)
        GPIO.output(BIN2,False)#BIN2
        GPIO.output(BIN1,True) #BIN1
        time.sleep(t_time)

def t_right(speed,t_time):
        L_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2,False)#AIN2
        GPIO.output(AIN1,True) #AIN1

        R_Motor.ChangeDutyCycle(speed)
        GPIO.output(BIN2,True)#BIN2
        GPIO.output(BIN1,False) #BIN1
        time.sleep(t_time)
        
def keysacn():
    print('keysacn start')
    val = GPIO.input(BtnPin)
    while GPIO.input(BtnPin) == False:
        val = GPIO.input(BtnPin)
       # print('GPIO.input(BtnPin) == False:')
    while GPIO.input(BtnPin) == True:
       # print('GPIO.input(BtnPin) == True:')
        time.sleep(0.01)
        val = GPIO.input(BtnPin)
        if val == True:
            GPIO.output(Rpin,1)
            while GPIO.input(BtnPin) == False:
                GPIO.output(Rpin,0)
        else:
            GPIO.output(Rpin,0)
            
def setup():
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(TRIG, GPIO.OUT)
        GPIO.setup(ECHO, GPIO.IN)
        
        GPIO.setup(Gpin, GPIO.OUT)     # Set Green Led Pin mode to output
        GPIO.setup(Rpin, GPIO.OUT)     # Set Red Led Pin mode to output
        GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)

        GPIO.setup(AIN2,GPIO.OUT)
        GPIO.setup(AIN1,GPIO.OUT)
        GPIO.setup(PWMA,GPIO.OUT)
        
        GPIO.setup(BIN1,GPIO.OUT)
        GPIO.setup(BIN2,GPIO.OUT)
        GPIO.setup(PWMB,GPIO.OUT)
        pwm.setPWMFreq(50)           # Set frequency to 60 Hz
        #紅外線setup
        GPIO.setup(SensorRight,GPIO.IN)
        GPIO.setup(SensorLeft,GPIO.IN)
        #蜂鳴器
        GPIO.setup(Buzzer, GPIO.OUT)	# Set pins' mode is output
        global Buzz			# Assign a global variable to replace GPIO.PWM
        Buzz = GPIO.PWM(Buzzer, 440)	# 440 is initial frequency.
        Buzz.start(50)			# Start Buzzer pin with 50% duty ration
        
def distance():
    GPIO.output(TRIG, 0)
    time.sleep(0.000002)

    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)

    
    while GPIO.input(ECHO) == 0:
        a = 0
    time1 = time.time()
    while GPIO.input(ECHO) == 1:
        a = 1
    time2 = time.time()

    during = time2 - time1
    return during * 340 / 2 * 100

def front_detection():
        write(0,110)
        time.sleep(0.5)
        dis_f = distance()
        return dis_f

def left_detection():
        write(0, 175)
        time.sleep(1)
        dis_l = distance()
        return dis_l
        
def right_detection():
        write(0,45)
        time.sleep(1)
        dis_r = distance()
        return dis_r
     
# def loop():
#         while True:
#                 dis1 = front_detection()
#                 if (dis1 < 40) == True:
#                         t_stop(0.2)
#                         t_down(30,0.5)
#                         t_stop(0.2)
#                         dis_left = left_detection()
#                         dis_right = right_detection()
#                         print("front:" + str(dis1)+ ' -- 左邊：'+str(dis_left)+ '-- 右邊：'+str(dis_right))
#                         if (dis_left < 40) == True and (dis_right < 40) == True:
#                                 print('左右都沒路，回轉 (左轉1秒)')
#                                 t_left(30,1)
#                         elif (dis_left > dis_right) == True:
#                                 print(' 左邊比較空， 左轉0.3秒')
#                                 t_left(30,0.3)
#                                 t_stop(0.1)
#                         else:
#                                 print(' 右邊比較空， 右轉0.3秒')
#                                 t_right(30,0.3)
#                                 t_stop(0.1)
#                 else:
#                         print('直走')
#                         t_up(40,0)
#               #  print dis1, 'cm'
#                # print ''

# def loopV2():
        while True:
                dis1 = front_detection()
                SR_2 = GPIO.input(SensorRight)#讀取红外訊號
                SL_2 = GPIO.input(SensorLeft)#讀取红外訊號
                dis_left = left_detection()
                dis_right = right_detection()
                if (dis1 > 70) == True and SL_2 == True and SR_2 == True:
                        print('直走', dis1)
                        t_up(30,0)
                elif (dis1 < 70):
                        print("前方阻礙", dis1)
                        t_down(40,1)
                        t_right(30,1)
                elif SR_2 == False:
                        print("右方阻礙")
                        t_down(40,1)
                        t_right(30,1)
                elif SL_2 == False:
                        print("左方阻礙")
                        t_down(40,1)
                        t_left(30,1)
                else:
                        print("else")
                        music2()
                        t_down(40,1)

def loopV3():
        print("loopV3")
        while True:
                dis1 = front_detection()
                # dis_left = left_detection()
                # dis_right = right_detection()
                SR_2 = GPIO.input(SensorRight)#讀取红外訊號
                SL_2 = GPIO.input(SensorLeft)#讀取红外訊號
                if (dis1 > 50) == True and SL_2 == True and SR_2 == True:
                        print('直走', dis1)
                        t_up(30,0)
                elif (dis1 < 50):
                        print("前方阻礙", dis1)
                        t_stop(1)
                        dis_left2 = left_detection()
                        dis_right2 = right_detection()
                        print("左側距離是" + str(dis_left2) + "          右側距離是" + str(dis_right2))
                        #如果左右放距離都 > 50 
                        if dis_left2 > 50 and dis_right2 > 50:
                                #判斷那邊距離較遠
                                if dis_left2 > dis_right2:
                                        t_left(30,1)
                                else:
                                        t_right(30,1)
                        elif dis_right2 > 50:
                                t_right(30,1)
                        elif dis_left2 > 50:
                                t_left(30,1)
                        else:
                                print("music")
                                #music2()
                                t_stop(100)
                elif SR_2 == False:
                        print("右方阻礙")
                        t_down(40,1)
                        t_right(30,1)
                elif SL_2 == False:
                        print("左方阻礙")
                        t_down(40,1)
                        t_left(30,1)
                else:
                        print("else")
                        t_down(40,1)

# 攝影機 
# /mjpg-streamer/mjpg-streamer-experimental 
# ./mjpg_streamer -i "./input_uvc.so" -o "./output_http.so -w ./www"  
# mjpg-streamer/mjpg-streamer-experimental/mjpg_streamer -i "mjpg-streamer/mjpg-streamer-experimental/input_uvc.so" -o "mjpg-streamer/mjpg-streamer-experimental/output_http.so -w /mjpg-streamer/mjpg-streamer-experimental/www"
# 瀏覽器瀏覽 localhost:8080
# 
# music
# def music1():
#         print ('\n    Playing song 1...')
#         for i in range(1, len(song_1)):
#                 Buzz.ChangeFrequency(song_1[i])	# Change the frequency along the song note
#                 time.sleep(beat_1[i] * 0.5)		# delay a note for beat * 0.5s	

def music2():       
        print ('\n\n    Playing song 2...')
        for i in range(1, len(song_2)):     # Play song 1
                Buzz.ChangeFrequency(song_2[i]) # Change the frequency along the song note
                time.sleep(beat_2[i] * 0.5)     # delay a note for beat * 0.5s

def destroy():
        Buzz.stop()					# Stop the buzzer
        GPIO.output(Buzzer, 1)
        GPIO.cleanup()

if __name__ == "__main__":
        
        print('start')
        setup()
        print('finish Setup()')
        L_Motor= GPIO.PWM(PWMA,100) 
        L_Motor.start(0)
        print('finish GPIO.PWM(PWMA,100)')
        R_Motor = GPIO.PWM(PWMB,100)
        R_Motor.start(0)
        print('finish GPIO.PWM(PWMB,100)')
        keysacn()
        print('finish keysacn()')
        try:
                Buzz.stop()	
                print('start loop()')
                loopV3()
        except KeyboardInterrupt:
                destroy()
