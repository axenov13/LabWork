from serial import *
from time import *
from Tkinter import *

ser = Serial(port='COM3', baudrate=9600, timeout=0)

print("I Got to GIT!!!")
print("How do I commit this shit?")

i = 1000

while(True):
    ser.write(b'start')
    sleep(0.05)
    line = ser.readline()
    print(line)
    i -= 1
    if (i == 0):
        i = 1000