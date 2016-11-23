from serial import *
from time import *

ser = Serial(port='COM4', baudrate=9600, timeout=10)
sleep(2)

while True:
    ser.write('w')
    line = ser.readline()
    if not line.strip():
        continue
    n = int(line)
    print(n)
    if n < 10:
        print("WOOOW")
#    sleep(0.01)