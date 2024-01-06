import time
import busio
import board
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from datetime import datetime
import RPi.GPIO as GPIO
import client as c
import json
from datetime import datetime
try:
    i2c=busio.I2C(board.SCL,board.SDA)
    adc=ADS.ADS1115(i2c)
    chan=AnalogIn(adc,ADS.P0)
    chan1=AnalogIn(adc,ADS.P1)
except Exception as e:
    print(e)

GPIO.setwarnings(False)
GPIO.setup(5,GPIO.OUT)
time.sleep(2)
def callibrate():
        global fvalue
        with open('Cal.txt', 'r') as cal:
            a = float(cal.read())
        print(f"Previous Calibration Value = {a}")
        print("above values")
        values=[]
        for i in range (10):
            for j in range (100):
                print("inside the loop")
                value = chan.value
                print("-------------value")
                print(value)
                v = value * (a / 32767)
                if v>2.5000:
                  a=a-0.0001
                elif v<2.5000:
                  a=a+0.0001
                elif v==2.5000:
                  a=a
                values.append(value)
            a=round(a,4)
            print(f'Calibrating  {10-i}....      cal={a}')
        with open('Cal.txt', 'w') as cal:
            cal.write(str(a))
        fvalue=sum(values)/len(values)
        values.clear()
def callibrate1():
        global fvalue1
        with open('Cal1.txt', 'r') as cal1:
            a1 = float(cal1.read())
        print(f"Previous Calibration Value = {a1}")
        values1=[]
        for i in range (10):
            for j in range (100):
                value1 = chan1.value
                print(f"chan2 value@@@@@@@@ {value1}")
                v1 = value1 * (a1 / 32767)
                if v1>2.5000:
                  a1=a1-0.0001
                elif v1<2.5000:
                  a1=a1+0.0001
                elif v1==2.5000:
                  a1=a1
                values1.append(value1)
            a1=round(a1,4)
            print(f'Calibrating  {10-i}....      cal={a1}')
        with open('Cal1.txt', 'w') as cal1:
            cal1.write(str(a1))
        fvalue1=sum(values1)/len(values1)
        values1.clear()
def sensor():
        offsetVoltage = 2.5
        sensitivity =0.066
        global current1
        global current1_time
        current=[]
        values=[]
        with open('Cal.txt','r') as cal:
            a=float(cal.read())
        for i in range (100):
              print("-------------------------->sensor<---------------------------------------")
              value = chan.value
              print(f"sensor chan val-->{value}")
              if fvalue>value:
                 value=fvalue+(fvalue-value)
              else:
                 value=value
              v = value * (a / 32767)
              cur = (v - offsetVoltage) / sensitivity
              values.append(value)
              current.append(cur)
              time.sleep(.0001)
        current1_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        current1=round(float(sum(current)/len(current)),2)
        print(current1)
        values.clear()
        current.clear()
        time.sleep(1)
def sensor1():
        offsetVoltage = 2.5
        sensitivity =0.066
        global current2
        global current2_time
        current1 =[]
        values1=[]
        with open('Cal1.txt','r') as cal1:
            a1=float(cal1.read())
        for i in range (100):
              value1 = chan1.value
              if fvalue1>value1:
                 value1=fvalue1+(fvalue1-value1)
              else:
                 value1=value1
              v1 = value1 * (a1 / 32767)
              cur1 = (v1 - offsetVoltage) / sensitivity
              values1.append(value1)
              current1.append(cur1)
              time.sleep(.0001)
        current2_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        current2=round(float(sum(current1)/len(current1)),2)
        print(current2)
        values1.clear()
        current1.clear()
        time.sleep(1)
try:
   callibrate()
   callibrate1()
except Exception as e:
   print(e)
while True:
    try:
        print("starting")
        with open("gw.json", 'r') as s1:
            data = json.load(s1)

        t1 = datetime.now().minute

        if data["Status"]:
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

            if 0 <= t1 < 15 or 16 <= t1 < 35 or 36 <= t1 < 58:
                sensor()
                sensor1()
                GPIO.output(5, GPIO.HIGH)
                data["Current1"] = current1
                data["Current2"] = current2
                data["current1_time"] = current1_time
                data["current2_time"] = current2_time
                data["Status_time"] = formatted_time
                print("Done")
                with open("gw.json", "w") as d2:
                    json.dump(data, d2)
                    d2.flush()
                with open("gw.json", "r") as s1:
                    data = json.load(s1)
                print("Running loop")
            elif 15 <= t1 < 16 or 35 <= t1 < 36 or 58 <= t1 < 60:
                sensor()
                sensor1()
                GPIO.output(5, GPIO.LOW)
                print("Stopped Loop ")
            else:
                print("Not in Any loop")
        elif not data["Status"]:
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
            data["Current1"] = 0.0
            data["Current2"] = 0.0
            time.sleep(1)
            print("Device Off")
            data["current1_time"] = formatted_time
            data["current2_time"] = formatted_time
            data["Status_time"] = formatted_time
            with open("gw.json", "w") as d2:
                json.dump(data, d2)
                d2.flush()  # Flush the buffer to ensure immediate write
            # Reopen the file for reading
            with open("gw.json", "r") as s1:
                data = json.load(s1)

    except Exception as e:
        print(e)

    print("ending")
    time.sleep(1.5)