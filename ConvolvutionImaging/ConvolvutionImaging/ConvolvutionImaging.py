from serial import Serial
import time
from Tkinter import *
from math import exp, log
from __builtin__ import round
from PIL import Image
from PIL import ImageTk
from random import random
import numpy as np
import scipy as scp

#ser = Serial(port='COM4', baudrate=9600, timeout=10)
#time.sleep(1)
#ser.flush()


def get_signal(ser, number):
    sum = 0
    for i in range(number):
        ser.write('w')
        time.sleep(0.005)
        line = ser.readline()
        if not line.strip():
            i-=1
            continue
        sum += int(line)
    return float(sum)/number

def get_signal1(ser, number):
    return 100*random()

def gauss(r, sigma):
        return 15*exp(-r*r/(sigma*sigma))

class ConvolutionImageMaster:

    def __init__(self, x_blocksize=1, y_blocksize=1):
        self.cmatrix = []
        self.imatrix = []
        self.convolution = []
        self.x_blocksize = x_blocksize
        self.y_blocksize = y_blocksize
        self.cmatrix_image = None
        self.cmatrix_type = None
        self.imatrix_image = None

    def _get_average_in_zone(self, x1, y1, x2, y2):
        sum = 0
        for i in range(0, x2 -x1):
            for j in range(0, y2 -y1):
                sum += self.cmatrix[i][j]
        return sum/( (x2-x1)*(y2-y1) )
    def set_x_blocksize(self, size):
        self.x_blocksize=size
        return 0
    def set_y_blocksize(self, size):
        self.y_blocksize=size
        return 0
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
                for j in range(int(len(self.cmatrix[0])/self.y_blocksize) + 1):
                    x = self._get_average_in_zone(self.x_blocksize*i, self.y_blocksize*j, self.x_blocksize*(i+1), self.y_blocksize*(j+1))
                    new[i].append(x)
        return new            
    def _extand_matrix_to_square(self, matrix, size):
        while len(matrix) < size:
            matrix.append([])
        for i in range(len(matrix)):
            while len(matrix[i]) < size:
                matrix[i].append(0)
        return matrix

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
    def init_convolution(self, convolution):
        self.convolution = convolution
        return self.convolution
    def init_imatrix(self):
        self.imatrix = []
        hmatrix = self.convolution
        cmatrix = self.cmatrix

# H COLUMN INIZIALIZATION
        convcolumn = []
        for i in xrange( len(hmatrix) ):
            for j in xrange( len(hmatrix[i]) ):
                convcolumn.append(hmatrix[i][j])
            for j in xrange( len(cmatrix[0])-1 ):
                convcolumn.append(0.)
        for i in xrange( (len(cmatrix) - 1)*(len(hmatrix[0])+len(cmatrix[0])-1) ):
            convcolumn.append(0.)

# END OF H COLUMN INIZIALIZATION

##### GMATRIX INIZIALIZATION
        firstrow = []
        for j in xrange( len(cmatrix) ):
            for i in xrange( len(cmatrix[j]) ):
                firstrow.append(cmatrix[j][i])
            for i in xrange( len(hmatrix[0])-1 ):
                firstrow.append(0.)
        l = len(firstrow)
        for j in xrange( len(convcolumn)-l ):
            firstrow.append(0.)

        Gmatrix = []
        k = 0
        for i in xrange( len(hmatrix) ):
            for j in xrange( len(hmatrix[0]) ):
                Gmatrix.append(list(firstrow))
                firstrow.reverse()
                firstrow.pop(0)
                firstrow.append(0.)
                firstrow.reverse()
                k+=1
            for j in xrange( len(cmatrix[0])-1 ):
                firstrow.reverse()
                firstrow.pop(0)
                firstrow.append(0.)
                firstrow.reverse()
                marker = (len(convcolumn)-1)*[0.]
                marker.insert(k, 1.)
                k+=1
                Gmatrix.append(marker)
        for i in xrange( (len(cmatrix)-1)*(len(hmatrix[0])+len(cmatrix[0])-1) ):
            marker = (len(convcolumn)-1)*[0.]
            marker.insert(k, 1.)
            k+=1
            Gmatrix.append(marker)

#END OF GMATRIX INIZIALIZATION

# SOLVING
        f = linalg.solve(Gmatrix, convcolumn)
        f = array(f).reshape( ( len(hmatrix) + len(cmatrix) - 1, len(hmatrix[0])+len(cmatrix[0])-1 ) )

# END

        self.imatrix = f
        return self.imatrix
        
    def create_cmatrix_image(self):
        self.cmatrix_image = Image.new("L", (len(self.cmatrix), len(self.cmatrix[0])), "black")
        for i in range(len(self.cmatrix)):
            for j in range(len(self.cmatrix[0])):
                self.cmatrix_image.putpixel((i, j), int(self.cmatrix[i][j]))
        return self.cmatrix_image
    def create_imatrix_image(self):
        self.imatrix_image = Image.new("L", (len(self.imatrix), len(self.imatrix[0])), "black")
        for i in range(len(self.imatrix)):
            for j in range(len(self.imatrix[0])):
                self.imatrix_image.putpixel((i, j), int(self.imatrix[i][j].real))
        return self.imatrix_image

    def get_imatrix_image(self):
        return self.imatrix_image
    def get_cmatrix_image(self):
        return self.cmatrix_image
    def get_cmatrix_type(self):
        return self.cmatrix_type

class DiodMaster:
    def __init__(self, canvas_, serial_name='COM4', baudrate1=9600, timeout1=10):
        self.value = 1
        self.serial = Serial(port=serial_name, baudrate=baudrate1, timeout=timeout1)
        time.sleep(1)
        self.canvas = canvas_

    def go():
        return 0


cim = ConvolutionImageMaster(None, None)
cim.init_gauss_cmatrix(50)
cim.create_cmatrix_image()

root = Tk()
root.geometry("{0}x{1}+0+0".format(1024, 768)) #Run big window

imgTk = ImageTk.PhotoImage(cim.get_cmatrix_image())
canv = Canvas(root, width =1000, height = 750, background="black", borderwidth=0)
canv.pack(fill = BOTH, expand = 1)
root.update()
imgCv = canv.create_image( (0,0), image=imgTk)
canv.update() #putting image on canvas (0, 0) coords

x_blocksize = 200    #setting step
y_blocksize = 200    #for x and y
latency = 0.001      #and latency for diod to react
convolution = []
m = 0
time.clock()
while(True):
    if(time.clock() > 3):
        break
    time.sleep(0.02)
    canv.update()

for i in range(canv.winfo_width()/x_blocksize + 1):
    convolution.append([])
    for j in range(canv.winfo_height()/y_blocksize + 1):
        convolution[i].append(get_signal1(0, 0)) #ERRRRORRORORORORRORORORO HERE
        canv.move(imgCv, 0, y_blocksize)
        canv.update()
        time.sleep(latency)
    canv.move(imgCv, x_blocksize, -(canv.winfo_height()/y_blocksize + 1)*y_blocksize)
    canv.update()
    time.sleep(latency)

cim.set_x_blocksize(x_blocksize) #this sets up the size of convolution matrix????
cim.set_y_blocksize(y_blocksize)  
cim.init_convolution(convolution)  
result = cim.init_imatrix()
cim.create_imatrix_image()
resultIm = cim.get_imatrix_image()
resultIm.show()
time.sleep(5)

mainloop()