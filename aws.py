from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
#from __future__ import division
import time
import logging
import argparse
import json
import car
import temp
import Adafruit_PCA9685
import os
host = "a2upnp1nbdxe41.iot.us-west-2.amazonaws.com"
rootCAPath = "./CA/root-CA.crt"
certificatePath = "./CA/SMC.cert.pem"
privateKeyPath = "./CA/SMC.private.key"
clientId = "basicPubSub"
testmod=0;



pwm = Adafruit_PCA9685.PCA9685()

servo_min = 200  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096

def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)


pwm.set_pwm_freq(60)

def servo(ch,ser):
    pwm.set_pwm(ch,ch, servo_max)
# Custom MQTT message callback
def customCallback(client, userdata, message):
#    print("Received a new message: ")
    m=str(message.payload)
    print(m)
    
    f=m.find('$')+1
    e=m.find('*')
    way=m[f:f+1]
    print(way)
    car.go_way(way)
    
def Callback1(client, userdata, message):
    m=str(message.payload)
    print(m)
    f=m.find('$')+1
    e=m.find(',')
    way=int(m[f:e])
    print(way)
    
    if(way>servo_max):
        way=servo_max
    if(way<servo_min):
        way=servo_min
    pwm.set_pwm(0, 0,way)
    f=e+1
    e=m.find('.')
    way=int(m[f:e])
    print(way)
    if(way>servo_max):
        way=servo_max
    if(way<servo_min):
        way=servo_min
    pwm.set_pwm(1, 1,way)
    f=e+1
    e=m.find('*')
    way=int(m[f:e])
    print(way)
    if(way>servo_max):
        way=servo_max
    if(way<servo_min):
        way=servo_min
    pwm.set_pwm(2, 2,way)
def Callback2(client, userdata, message):
#    print("Received a new message: ")

    
    m=str(message.payload)
    print(m)
    f=m.find('$')+1
    e=m.find('*')
    way=m[f:f+1]
    print(way)

    if(way=='p'):
        os.system("fswebcam --no-banner -r 640x480 ./cam/1.jpg")
        os.system("python up.py")
def test_init():
    # Configure logging   
    logger = logging.getLogger("AWSIoTPythonSDK.core")
    logger.setLevel(logging.DEBUG)
    streamHandler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)
   
def init():
    car.init()
    if(testmod==1):
        test_init()

init()
pwm = Adafruit_PCA9685.PCA9685()
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe('topic/smc', 1, customCallback)
myAWSIoTMQTTClient.subscribe('topic/cam', 1, Callback2)
myAWSIoTMQTTClient.subscribe('topic/servo', 1, Callback1)
time.sleep(2)


    
try:
    while True:
        message = {}
        message['temp'] =temp.get()
        messageJson = json.dumps(message)
        myAWSIoTMQTTClient.publish('topic/temp',messageJson,1)
        print(messageJson)
        message = {}
        message['distance'] =car.checkdist()
        messageJson = json.dumps(message)
        myAWSIoTMQTTClient.publish('topic/distance',messageJson,1)
        print(messageJson)
        
except KeyboardInterrupt:
        car.cleanup()
        
        

