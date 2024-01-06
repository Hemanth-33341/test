import threading
import json
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import random_gw as r


from datetime import datetime
import importlib
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(5, GPIO.OUT, initial=GPIO.LOW)

delay_main = 2
delay_internet_off = 3600
delay_compressor_off = 1800
delay_mail = 5
delay_current = 1800

def main():
    while True:
        with open("status.txt",'r') as f:
            status = f.read()
        s = status
        if s == "True":
            GPIO.output(6, GPIO.HIGH)
            print("Load ON")
        else:
            print("Load off")
            GPIO.output(6, GPIO.LOW)
        #importlib.reload(m)
        time.sleep(delay_main)

def internet():
    last_internet_off = time.time()
    while True:
        now = time.time()
        if now - last_internet_off >= delay_internet_off:
            GPIO.output(5, GPIO.LOW)
            print("Internet is OFF")  
            time.sleep(3)
            last_internet_off = time.time()
        else:
            GPIO.output(5, GPIO.HIGH)
            print("Internet is ON")
        time.sleep(1)

def compressor():
    last_compressor_off = time.time()
    while True:
        now = time.time()
        if now - last_compressor_off >= delay_compressor_off:
            GPIO.output(23, GPIO.LOW)
            print("Compressor is OFF")
            time.sleep(1800)
            last_compressor_off = time.time()
  
        else:
            GPIO.output(23, GPIO.HIGH)
            print("Compressor is ON")
        time.sleep(1)
        
def mail():
    while True:
        #importlib.reload(m)
        with open("status.txt",'r') as f:
            status = f.read()
        s = status
        print(s)
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
        current1, current2 = r.generate_values()
        #print(current2)
        #print(current1)
        if  s == "True":
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
        time.sleep(1800)
    
threading.Thread(target=main).start()
threading.Thread(target=internet).start()
threading.Thread(target=compressor).start()
threading.Thread(target=mail).start()