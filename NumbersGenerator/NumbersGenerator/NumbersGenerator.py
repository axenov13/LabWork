from serial import *
from time import *
from math import *
from __builtin__ import round
from PIL import Image

def gauss(r, sigma):
        x = float(r)
        s = float(sigma)
        return 15*exp(-(x*x)/(s*s))

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

        width = int(round(2*sigma1*log(99)))
        height = int(round(2*sigma2*log(99)))
        
        i0 = int(round(width/2))
        j0 = int(round(height/2))
        i = 0
        j = 0
        for i in range(width):
            self.cmatrix.append([])
            for j in range(height):
                self.cmatrix[i].append(round(gauss(i-i0, sigma1)*gauss(j-j0, sigma2)))
        return 0
    
    def create_cmatrix_image(self):
        cmatrix_image = Image.new("L", (len(self.cmatrix), len(self.cmatrix[0])), "black")
        for i in range(len(self.cmatrix)):
            for j in range(len(self.cmatrix[0])):
                cmatrix_image.putpixel((i, j), 5*int(self.cmatrix[i][j]))
        return cmatrix_image

cim = ConvolutionImageMaster(None, None)
cim.init_gauss_cmatrix(100)
im = cim.create_cmatrix_image()
im.show()


