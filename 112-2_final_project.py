import RPi.GPIO as GPIO
import time as time
from firebase import firebase

url='https://aiot-final-project-default-rtdb.firebaseio.com/'
firebase = firebase.FirebaseApplication(url, None)

Relay_pin=5

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER=2
GPIO_ECHO=3

GPIO.setup(GPIO_TRIGGER,GPIO.OUT)
GPIO.setup(GPIO_ECHO,GPIO.IN)
GPIO.setup(Relay_pin,GPIO.OUT,initial=GPIO.LOW)
state=0
counter=0
temp_state=0

def distance():
      GPIO.output(GPIO_TRIGGER,True)
      time.sleep(0.00001)
      GPIO.output(GPIO_TRIGGER,False)
      start_time=time.time()
      stop_time=time.time()
      
      while GPIO.input(GPIO_ECHO)==0:
            start_time=time.time()
      
      while GPIO.input(GPIO_ECHO)==1:
            stop_time=time.time()
      
      time_elapsed=stop_time-start_time
      distance=(time_elapsed*34300)/2
      return  distance
      
if __name__ == '__main__':
      try:
            while True:
                  temp_state=state
                  
                  dist=distance()
                  if dist<=200:
                        GPIO.output(Relay_pin,GPIO.HIGH)
                        print("人來了",end="\n")
                        firebase.put_async('/data','state',"人來了")
                        state=1
                  else:
                        GPIO.output(Relay_pin,GPIO.LOW)
                        print("沒人",end="\n")
                        firebase.put_async('/data','state',"沒人")
                        state=0
                  if temp_state>state:
                        counter=counter+1
                  print(counter)
                  firebase.put_async('/data','counter',counter)     
                  time.sleep(1)
      except KeyboardInterrupt:
            print("Measurement stopped by User")
            GPIO.cleanup()
            