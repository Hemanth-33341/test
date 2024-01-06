import os
import sys
sys.path.append('/home/pi')
import time
from threading import *
import RPi.GPIO as GPIO
from time import sleep
import threading
from datetime import datetime
import client as c
import json
import random
from paho.mqtt.client import Client
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
mqtt = c.iotMQTT()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(5, GPIO.OUT, initial=GPIO.LOW)

delay_random = 1800
last_random_off = time.time()
status = True

def generate_values():
    current1 = round(random.uniform(2.20, 2.48), 2)
    current2 = round(random.uniform(1.08, 1.5), 2)
    return current1, current2
    
def main():
    while True:
        global status
        if status:
            GPIO.output(6, GPIO.HIGH)
            print("Load ON")
        else:
            print("Load off")
            GPIO.output(6, GPIO.LOW)
        #importlib.reload(m)
        time.sleep(2)

def internet():
    while True:
        GPIO.output(5, GPIO.HIGH)
        print("Internet is ON")
        time.sleep(60)
        
        GPIO.output(5, GPIO.LOW)
        print("Internet is OFF")  
        time.sleep(10)



def compressor():
    while True:
        GPIO.output(23, GPIO.HIGH)
        print("Compressor is ON")
        time.sleep(150)
        
        GPIO.output(23, GPIO.LOW)
        print("Compressor is OFF")
        time.sleep(30)


        
def mail():
    while True:
        #importlib.reload(m)
        global status
        email_user = "care.bariflolabs@gmail.com"
        email_password = "ifln keco pdbc hqts"
        # email_send = "data.bariflolabs@gmail.com"
        #email_send = "mrityunjay.sahu@bariflolabs.com"
        email_send = "gandupallihemanth86@gmail.com"
        subject = "IWMS Status"

        msg = MIMEMultipart()
        msg["From"] = email_user
        msg["To"] = email_send
        msg["Subject"] = subject
        #print("hai")
        current1, current2 = generate_values()
        #print(current2)
        #print(current1)
        if  status:
            print("t")
            current1 = current1
            current2= current2
            body = f"GW_Status:ON  Aeration:On  CompCurrVal:{current1} Amp  AerationCurrVal:{current2} Amp"
        else:
            print("f")
            body = "GW_status:ON Aeration Device :OFF"


        msg.attach(MIMEText(body,"plain"))

        text = msg.as_string()
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(email_user,email_password)


        server.sendmail(email_user,email_send,text)
        server.quit()
        time.sleep(30)
threading.Thread(target=main).start()
threading.Thread(target=internet).start()
threading.Thread(target=compressor).start()
threading.Thread(target=mail).start()


def doFeed():
    if __name__ == "__main__":
        threading.Timer(5.0,doFeed).start()
    with open('config.json') as json_file:
        did = json.load(json_file)
    now = time.time()
    global status
    global last_random_off
    if now - last_random_off >= delay_random:
        current1, current2 = 0,0
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{current1}")
        print(f"{current2}")
        if now-delay_random - last_random_off >= delay_random:
            last_random_off = now
    else:
        if status:
            current_datetime = datetime.now()
            current1, current2 = generate_values()
            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{current1}")
            print(f"{current2}")
        else:
            current1, current2 = 0,0
            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            print(current1)
            print(current2)        
    for i in did["deviceCommuncationId"]:
        if i == "746770045049742":
            mqtt.postDataFeed({"dataPoint": formatted_datetime, "paramType": 'Sensor1', "paramValue": current1},i) 
            mqtt.postDataFeed({"dataPoint": formatted_datetime, "paramType": 'Sensor2', "paramValue": current2},i)

sleep(.6)
if __name__ == "__main__":
    threading.Timer(5.0,doFeed).start()
def anotherFunction():
    broker_address = "4.240.114.7"
    broker_port = 1883
    username = "BarifloLabs"
    password = "Bfl@123"
    topics = ["746770045049742","495888677862344","910366006590890"]
    def on_connect(client, userdata, flags, rc):
            if rc == 0:
                for topic in topics:
                    client.subscribe(topic)
            else:
                pass           

    def on_message(client, userdata, message):
        global status
        data = json.loads(message.payload.decode('utf-8'))
        status = data[0]["status"]
        print(f"Received message: {data}")
        print(f"status val :---{status}")
        with open ("status.txt",'w') as f:
            f.write(str(data[0]["status"]))

    from paho.mqtt.client import Client
    while True:
        if __name__ == "__main__":
            mqtt_client = Client()
            mqtt_client.on_connect = on_connect
            mqtt_client.on_message = on_message
            mqtt_client.username_pw_set(username, password)
            mqtt_client.connect(broker_address, broker_port)
            mqtt_client.loop_start()
        try: 
            while True:
                pass
        except KeyboardInterrupt:
            mqtt_client.loop_stop()
            
if __name__ == "__main__":
    threading.Timer(5.0,anotherFunction).start()
    mqtt.lp()
    
    
    
    
    