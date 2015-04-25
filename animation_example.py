import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
from SerialCommunication import *

FFMPEG_BIN="ffmpeg"

ser = sensorInit()
num_rows = 10
num_cols = 5
toggle = 0
Matrix = np.zeros((num_rows, num_cols))
#Matrix[0,0] = 1500
for i in range (4):
	Array = readSensors(ser, 28)
Matrix[0,0] = 1500

Array = bytearray(num_rows*num_cols)
sensor_num = 28


def generate_data():
	Array = readSensors(ser, sensor_num)
	Matrix = matrixConvert(Array, num_rows, num_cols)
	#print(Array)
	return Matrix

def update(data):
	mat.set_data(data)
	#print("Doing update")
	return mat 

def data_gen():
	while True:
	    #print("Doing Data_gen")
	    yield generate_data()       

fig, ax = plt.subplots()
mat = ax.matshow(Matrix)
plt.colorbar(mat)
ani = animation.FuncAnimation(fig, update, data_gen, interval=3, 
blit=False)
#ani.save('blah.mp4', writer="ffmpeg", fps=15)

plt.show()
