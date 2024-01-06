import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import json
import time
import main3 as m
import random_gw as r
import importlib

 

delay_mail = 1800
time.sleep(2)
while True:
    try:
        #importlib.invalidate_caches(m)
        importlib.reload(m)
        with open("status.txt",'r') as f:
            status = f.read()
        s = status
        print(s)
        email_user = "care.bariflolabs@gmail.com"
        email_password = "ifln keco pdbc hqts"
        # email_send = "data.bariflolabs@gmail.com"
        #email_send = "mrityunjay.sahu@bariflolabs.com"
        email_send = "gandupallihemanth86@gmail.com"
        #email_send = "g"
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
            #print("t")
            current1 = current1
            current2= current2
            body = f"GW_Status:ON  Aeration:On  CompCurrVal:{current1} Amp  AerationCurrVal:{current2} Amp"
        else:
            #print("f")
            body = "GW_status:ON Aeration Device :OFF"


        msg.attach(MIMEText(body,"plain"))

        text = msg.as_string()
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(email_user,email_password)


        server.sendmail(email_user,email_send,text)
        server.quit()


    except Exception as e:
        pass
    time.sleep(delay_mail)
