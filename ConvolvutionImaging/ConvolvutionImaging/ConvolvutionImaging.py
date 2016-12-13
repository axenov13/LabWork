from serial import Serial
from time import sleep
from Tkinter import *
from math import exp, log
from __builtin__ import round
from PIL import Image
from PIL import ImageTk
from random import random
import numpy as np

def get_signal(ser, number):
    sum = 0
    for i in range(number):
        ser.write('w')
        sleep(0.005)
        line = ser.readline()
        if not line.strip():
            i+=1
            continue
        sum += int(line)
    return float(sum)/number

def get_signal1(ser, number):
    return 100*random()

def gauss(r, sigma):
        return 15*exp(-r*r/(sigma*sigma))

class ConvolutionImageMaster:

    def __init__(self, __serial, __canvas, x_blocksize=1, y_blocksize=1):
        self.ser = __serial
        self.canv = __canvas
        self.cmatrix = []
        self.rmatrix = []
        self.x_blocksize = x_blocksize
        self.y_blocksize = y_blocksize
        self.cmatrix_image = []
        self.cmatrix_type = None

    def set_x_blocksize(self, size):
        self.x_blocksize=size
        return 0
    def set_y_blocksize(self, size):
        self.y_blocksize=size
        return 0
    def _get_average_in_zone(self, x1, y1, x2, y2):
        sum = 0
        for i in range(x1, x2):
            for j in range(y1, y2):
                sum += self.cmatrix[i][j]
        return sum/( (x2-x1)*(y2-y1)
    def _resized_cmatrix(self):
        new = []
        if self.cmatrix_type == 'block':
            for i in range(int(len(self.cmatrix)/self.x_blocksize) + 1):
                new.append([])
                for j in range(int(self.cmatrix[0]/self.y_blocksize) + 1):
                     new[i].append(1)
        else:
            for i in range(int(len(self.cmatrix)/self.x_blocksize) + 1):
                new.append([])
                for j in range(int(self.cmatrix[0]/self.y_blocksize) + 1):
                    x = _get_average_in_zone(self.x_blocksize*i, self.y_blocksize*j, self.x_blocksize*(i+1), self.y_blocksize*(j+1))
                    new[i].append(x)
        return new            

    def init_gauss_cmatrix(self, sigma1, sigma2='E'):
        self.cmatrix = []
        self.cmatrix_type = 'gauss'
        if sigma2 == 'E':
            sigma2 = sigma1

        width = int(round(2*sigma1*log(15)))
        height = int(round(2*sigma2*log(15)))
        
        i0 = int(round(width/2))
        j0 = int(round((height/2)))
        i = 0
        j = 0
        for i in range(width):
            self.cmatrix.append([])
            for j in range(height):
                self.cmatrix[i].append(round(gauss(float(i-i0), float(sigma1))*gauss(float(j-j0), float(sigma2))))
        return self.cmatrix
    def init_block_cmatrix(self, x, y):
        self.cmatrix = []
        self.cmatrix_type = 'block'
        for i in range(x):
            self.cmatrix.append([])
            for j in range(y):
                self.cmatrix[i].append(1)
        return self.cmatrix
    def init_cmatrix(self, matrix):
        self.cmatrix = matrix
        self.cmatrix_type = 'manual'
        return self.cmatrix

    def find_initial_matrix(self, convolution):
        initial = []
        return initial

    def create_cmatrix_image(self):
        self.cmatrix_image = Image.new("L", (len(self.cmatrix), len(self.cmatrix[0])), "black")
        for i in range(len(self.cmatrix)):
            for j in range(len(self.cmatrix[0])):
                self.cmatrix_image.putpixel((i, j), int(self.cmatrix[i][j]))
        return self.cmatrix_image
    def get_cmatrix_image(self):
        return self.cmatrix_image
    def get_cmatrix_type(self):
        return self.cmatrix_type

cim = ConvolutionImageMaster(None, None)
cim.init_gauss_cmatrix(50)
cim.create_cmatrix_image()

#ser = Serial(port='COM4', baudrate=9600, timeout=10)
#sleep(1)

root = Tk()
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight())) #Run big window

imgTk = ImageTk.PhotoImage(cim.get_cmatrix_image())
canv = Canvas(root, width = root.winfo_width(), height = root.winfo_height(), background="black", borderwidth=0)
canv.pack(fill = BOTH, expand = 1)
root.update()
imgCv = canv.create_image( (0,0), image=imgTk)
canv.update() #putting image on canvas (0, 0) coords

x_blocksize = 1    #setting step
y_blocksize = 1    #for x and y
latency = 0.02       #and latency for diod to react

convolution = []
m = 0
for i in range(canv.winfo_height()/y_blocksize + 1):
    convolution.append([])
    for j in range(canv.winfo_width()/x_blocksize + 1):
        convolution[i].append(get_signal1(100000000000, 1)) #here is a mistake (signal1 -> signal)
        canv.move(imgCv, x_blocksize, 0)
        canv.update()
        sleep(latency)
        m=j
    canv.move(imgCv, -j*x_blocksize, y_blocksize)
    canv.update()
    sleep(latency)

cim.set_x_blocksize(x_blocksize) #this sets up the size of convolution matrix????
cim.set_y_blocksize(y_blocksize)    
result = cim.find_initial_matrix(convolution)

resultIm = create_matrix_image(result)
resultIm.show()

mainloop()