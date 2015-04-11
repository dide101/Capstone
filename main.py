#!/usr/bin/python
#import serial

from SerialCommunication import *
#from Plot_Functions import *

import numpy as np

import matplotlib.pyplot as plt

Array = bytearray(64)
num_rows = 8
num_cols = 8
Matrix = np.zeros((8,8))

ser = sensorInit()
fig = plt.figure()

for i in range (0, 10): 
    Array = readSensors(ser)
    Matrix = matrixConvert(Array, num_rows, num_cols)
    plt.imshow(Matrix, interpolation = 'nearest', cmap=plt.cm.ocean)
    plt.show()




    
