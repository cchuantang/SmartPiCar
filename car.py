import RPi.GPIO as GPIO
import time

IN1 = 31
IN2 = 33
IN3 = 35
IN4 = 37

T   = 38
R   = 40

def init():
    if(GPIO.getmode!=10):
        GPIO.setmode(GPIO.BOARD)     
    GPIO.setup(IN1,GPIO.OUT)
    GPIO.setup(IN2,GPIO.OUT)
    GPIO.setup(IN3,GPIO.OUT)
    GPIO.setup(IN4,GPIO.OUT)
    GPIO.setup(T,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(R,GPIO.IN)
    cl()
    
def cl():
    GPIO.output(IN1,False)
    GPIO.output(IN2,False)
    GPIO.output(IN3,False)
    GPIO.output(IN4,False)
    GPIO.output(T,False)
    
def sign(t):
    f = open('car.txt','a')
    f.write(t)
    f.close()

def checkdist():
    
    GPIO.output(T,True)
   
    time.sleep(0.000015)
    GPIO.output(T,False)
    while not GPIO.input(R):
            pass
    
    t1 = time.time()
    while GPIO.input(R):
            pass
    
    t2 = time.time()
    
    return (float)(t2-t1)*340/2
    
def go(sleep_time):
    if(checkdist()>0.1):
        GPIO.output(IN1,True)
        GPIO.output(IN2,False)
        GPIO.output(IN3,True)
        GPIO.output(IN4,False)
        time.sleep(sleep_time)
        sign('d')
    cl()
    
def bk(sleep_time):
    GPIO.output(IN1,False)
    GPIO.output(IN2,True)
    GPIO.output(IN3,False)
    GPIO.output(IN4,True)
    time.sleep(sleep_time)
    cl()

def left(sleep_time):
    GPIO.output(IN1,True)
    GPIO.output(IN2,False)
    GPIO.output(IN3,False)
    GPIO.output(IN4,True)
    time.sleep(sleep_time)
    cl()

def right(sleep_time):
    GPIO.output(IN1,False)
    GPIO.output(IN2,True)
    GPIO.output(IN3,True)
    GPIO.output(IN4,False)
    time.sleep(sleep_time)
    cl()



def cleanup():
    GPIO.cleanup()
    f = open('car.txt','w')
    f.write('')
    f.close()

def go_way(way):
    print(way)
    if(way=='w'):
        go(0.2)
    else:
        if(way=='d'):
            bk(0.2)
            sign('w')
        else:
            if(way=='r'):
                right(0.2)
                sign('l')
            else:
                if(way=='l'):
                    left(0.2)
                    sign('r')
                else:
                    if(way=='b'):
                        go_back()
                    else:
                        cl()

def go_back():
    f=open('car.txt','r')
    s=f.read()
    s=s[::-1]
    while len(s):
        go_way(s[0:1])
        s=s[1:]
           
