from serial import *
from time import *
from tkinter import *
from math import *

ser = Serial(port='COM4', baudrate=9600, timeout=0)

class GaussLight:
    def __init__(self, canv, sigma):
        self.canv = canv
        self.sigma = sigma
        self.factor = 255 * sigma - 1
        self.x = self.canv.winfo_width()/2
        self.y = self.canv.winfo_height()/2
        self.circles = []
        i = 0
        while True:
            if round(self.gauss(i)) != 0:
                i+=1
            else:
                break
        while i > 0:
            color_dec = self.gauss(i)
            color_hex = hex(round(color_dec))
            if len(color_hex) == 4:
                color_hex_correct = color_hex[2:4]
            else:
                color_hex_correct = "0" + color_hex[2:3]
            full_color_hex = "#" + 3*color_hex_correct
            self.circles.append(self.canv.create_oval(self.x-i, self.y-i, self.x+i, self.y+i,
                                                   fill=full_color_hex, width=0))
            i-=1

    def set_coords(self, x, y):
        for circle in self.circles:
            self.canv.move(circle, x, y)

    def move(self, x, y, v):
        passed_x = 0
        passed_y = 0
        delta_t = 0.01
        if abs(x) > 0:
            delta_x = v*delta_t/sqrt(1+(y/x)*(y/x))
            if x < 0:
                delta_x *= -1
            delta_y = y*delta_x/x
        else:
            delta_x = 0
            if abs(y) > 0:
                delta_y = v*delta_t
                if y < 0:
                    delta_y *= -1
            else:
                delta_y = 0
        begin = -1
        while passed_x < abs(x) or passed_y < abs(y):
            end = time()
            if end - begin > delta_t:
                begin = time()
                for circle in self.circles:
                    self.canv.move(circle, delta_x, delta_y)
                passed_x += abs(delta_x)
                passed_y += abs(delta_y)
                self.canv.update()

    def gauss(self, r):
        return self.factor*exp(-r*r/(2*self.sigma*self.sigma))/self.sigma

def get_signal(ser, number):
    sum = 0
    for i in range(number):
        line = ser.readline()
        if len(line) != 0:
            sum += int(line.strip('\0'))
        else:
            i-=1
    return sum/number

def scan(ser, canv, number):
    width = 20
    height = 20
    list = []
    for i in range(38):
        list1 = []
        for j in range(55):
            rect = canv.create_rectangle(j*width, i*height, j*width + width, i*height + height, fill="white")
            canv.update()
            sleep(0.02)
            signal = get_signal(ser, number)
            canv.delete(rect)
            list1.append(signal)
        list.append(list1)
    return list

def output(canv, list):
    width = 20
    height = 20
    for i in range(38):
        for j in range(55):
            n = list[i][j]
            if n > 99:
                n = 99
            col = 'gray' + str(n)
            canv.create_rectangle(j*width, i*height, j*width + width, i*height + height, fill=col)
            canv.update()
            sleep(1000)
    return 0
       

root = Tk()
def callback():
    b.pack_forget()
    root.update()
    ser.write("GO")
    l = scan(ser, w, 100)
    output(w, l)

b = Button(root, text="start", command=callback)
b.pack(anchor=CENTER)
w = Canvas(root, width=1024, height=768, bg="black")
w.pack()





mainloop()


#while True:
#    line = ser.readline()
#    if not line.strip():
#        continue
#    print(line)