import serial
import string

#from matplotlib import *
import numpy as np

def sensorInit():
    ser = serial.Serial('/dev/cu.usbmodemfa131', 115200, bytesize=serial.EIGHTBITS)
    return ser

def readSensors(ser, sensor_num):
    #while True: 
        #Input = ser.read(sensor_num)
        #ByteArray = bytearray(Input)
    try: 
        Line = ser.readline()
        Line = Line.split(',')
        Line.pop()
        Line.pop()
#        print(Line)
        return Line
    except:
        print("Failed reading Serial")

def matrixConvert(Array, num_rows, num_cols):
    matrix = np.zeros((num_rows, num_cols))
    #print(matrix)
    for i in range(0, num_rows):
        for j in range(0, num_cols):
            matrix[i,j] = Array[i*num_cols + j]
           # print(i, j, i*num_cols + j)
    return matrix
