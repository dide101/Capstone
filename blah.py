import serial
import time
import string

from matplotlib import *
import numpy as np

def sensorInit():
    ser = serial.Serial('/dev/cu.usbmodemfd121', 9600, bytesize=serial.EIGHTBITS)
    return ser

def readSensors(ser, sensor_num):
    Input = ser.read(sensor_num)
    ByteArray = bytearray(Input)
    return ByteArray

def matrixConvert(Array, num_rows, num_cols):
    matrix = np.zeros((num_cols, num_rows))
    for i in range(0, num_rows):
        for j in range(0, num_rows):
            matrix[i,j] = Array[i*num_rows + j]
    return matrix
