from serial import *
from time import *
from Tkinter import *
from math import *
from __builtin__ import round

ser = Serial(port='COM4', baudrate=9600, timeout=10)
sleep(1)

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
        ser.write('w')
        sleep(0.005)
        line = ser.readline()
        if not line.strip():
            i+=1
            print "LOL"  
            continue
        sum += int(line)
    return float(sum)/number

def scanBrick(ser, canv, bricksize, number, diod_reaction_time):
    width = bricksize
    height = bricksize
    list = []
    for i in range(canv.winfo_height()/height + 1):
        list1 = []
        for j in range(canv.winfo_width()/width + 1):
            rect = canv.create_rectangle(j*width, i*height, j*width + width, i*height + height, fill="white")
            canv.update()
            sleep(diod_reaction_time)
            signal = get_signal(ser, number)
            canv.delete(rect)
            list1.append(signal)
            print i, j, signal
        list.append(list1)
        canv.update()
    return list

def outBrick(canv, list, bricksize):
    width = bricksize
    height = bricksize
    for i in range(canv.winfo_height()/height + 1):
        for j in range(canv.winfo_width()/width + 1):
            n = list[i][j]
            col = 'gray' + str(int(round(n)))
            canv.create_rectangle(j*width, i*height, j*width + width, i*height + height, fill=col)         
    canv.update()
    return 0

def normalizeBrick(list, max_norm, min_norm, dstep):
    max = 0
    min = 10000
    for i in range(len(list)):
        for j in range(len(list[i])):
            if list[i][j] > max:
                max = list[i][j]
            if list[i][j] < min:
                min = list[i][j]
    k = (max_norm - min_norm)/(max - min)
    b = max_norm - k*max
    dev = k * dstep

    for i in range(len(list)):
        for j in range(len(list[i])):
            list[i][j] = k*list[i][j] + b
            floatstep = list[i][j] / dev
            list[i][j] = round(floatstep)* dev
            if list[i][j] > 100:
                list[i][j] = 100
    return list     

def deleteNoize(list, noize):
    for i in range(len(list)):
        for j in range(len(list[i])):
            list[i][j] -= noize
    return list

def print_list(list):
    for i in range(len(list)):
        for j in range(len(list[i])):
            print round(list[i][j], 1),
        print '\n'
root = Tk()

def getAlanDev(ser, number):
    dev = 0
    x1 = get_signal(ser, 2)
    for i in range(number):
        x2 = get_signal(ser, 2)
        sleep(0.01)
        dev += (x2 - x1)*(x2 - x1)/2
        x1 = x2
    return float(dev)/number

brick = 40
w1idth = 400
h1eight = 300
waitfor = 0
num = 10



w = Canvas(root, width=w1idth, height=h1eight, bg="black")
w.pack()
w.update()
sleep(1)


list = scanBrick(ser, w, brick, num, waitfor)


noize = get_signal(ser, num)
dev = getAlanDev(ser, num)

list = deleteNoize(list, noize)
list = normalizeBrick(list, 99, 0, dev)

outBrick(w, list, brick)

sleep(10000)


mainloop()

