from serial import *
from time import *
from Tkinter import *
from math import *
from __builtin__ import round
from PIL import Image
from PIL import ImageTk
from random import random

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

    def set_x_blocksize(self, size):
        self.x_blocksize=size
        return 0
    def set_y_blocksize(self, size):
        self.y_blocksize=size
        return 0

    def init_gauss_cmatrix(self, sigma1, sigma2='E'):
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
    def find_initial_matrix(self, convolution):
        initial = []
        return initial

def create_matrix_image(matrix):
    cmatrix_image = Image.new("L", (len(matrix), len(matrix[0])), "black")
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            cmatrix_image.putpixel((i, j), int(matrix[i][j]))
    return cmatrix_image

cim = ConvolutionImageMaster(None, None)
im = create_matrix_image(cim.init_gauss_cmatrix(100))

#ser = Serial(port='COM4', baudrate=9600, timeout=10)
#sleep(1)

root = Tk()
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

imgTk = ImageTk.PhotoImage(im)
canv = Canvas(root, width = root.winfo_width(), height = root.winfo_height(), background="black", borderwidth=0)
canv.pack(fill = BOTH, expand = 1)
root.update()
imgCv = canv.create_image( (0,0), image=imgTk)
canv.update()

print(canv.winfo_width())

x_blocksize = 20
y_blocksize = 50
latency = 0.1

convolution = []
m = 0
for i in range(canv.winfo_height()/y_blocksize + 1):
    convolution.append([])
    for j in range(canv.winfo_width()/x_blocksize + 1):
        convolution[i].append(get_signal1(100000000000, 1))
        canv.move(imgCv, x_blocksize, 0)
        
        canv.update()
        sleep(latency)
        m=j
    canv.move(imgCv, -j*x_blocksize, y_blocksize)
    canv.update()
    sleep(latency)

cim.set_x_blocksize(x_blocksize)
cim.set_y_blocksize(y_blocksize)    
result = cim.find_initial_matrix(convolution)

resultIm = create_matrix_image(result)
resultIm.show()

mainloop()