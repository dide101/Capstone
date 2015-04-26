import sys
import numpy as np
from PyQt4 import QtGui

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

import SerialCommunication as serial

#constants
num_rows = 10
num_cols = 5
frames = 400
i = 0

SaveArray = [[0]*50]*(frames+1)

sensor_num = num_rows*num_cols

ser = serial.sensorInit()

from functools import partial 

class Press_Mat(QtGui.QWidget):
    def __init__(self):
        super(Press_Mat, self).__init__()
        for i in range (4):
            Array = serial.readSensors(ser, 28)

        self.figure = plt.figure()
    
        self.canvas = FigureCanvas(self.figure)
        self.grid = serial.matrixConvert(Array, num_rows, num_cols)
 #       self.grid[0,0] = 1000
        self.start()

    def start(self):
        self.setWindowTitle('PressMat')
        gridLayout = QtGui.QGridLayout()    
        self.setLayout(gridLayout)
        
        #button
        restart = QtGui.QPushButton("Start")
        restart.clicked.connect(self.plot)

        save = QtGui.QPushButton("Save")
        save.clicked.connect(self.restart_animation)

        #checkbox
        self.record = QtGui.QCheckBox('Record', self)
        

        gridLayout.addWidget(self.canvas,0,0)
        gridLayout.addWidget(restart, 1,0)
        gridLayout.addWidget(self.record, 2,0)
        gridLayout.addWidget(save, 3,0)
        self.show()

    def plot(self):
        #Figure and subplot

        ax = self.figure.add_subplot(111)
        self.mat = ax.matshow(self.grid,  vmin=0, vmax=1000, interpolation='bilinear')
        plt.axis('off')
            
        ani = animation.FuncAnimation(self.figure, self.update, interval=3, save_count=500)

        self.canvas.draw()
        
    def update(self, data):
        #print('Updating')
        global i
        newGrid = self.grid.copy()
        Array = serial.readSensors(ser, sensor_num)
        
        if (self.record.checkState() != 0):
            if (i < frames):
                SaveArray[i] = Array
                i=i+1
                #print(i)
        #print(SaveArray)
        newGrid = serial.matrixConvert(Array, num_rows, num_cols)
        self.mat.set_data(newGrid)
        self.grid = newGrid

    def new_update(self, data):
        #print('Updating')
 #       newGrid = self.grid.copy()
        global i
        Array = SaveArray[i] #serial.readSensors(ser, sensor_num)
        #print(i)
        i=i+1
        newGrid = serial.matrixConvert(Array, num_rows, num_cols)
        self.mat.set_data(newGrid)
        self.grid = newGrid
        


    #simply restarts data
        
    def restart_animation(self):
    #if (self.record.checkState() != 0);
        global i
        i = 0
        #for i=0 to 500
        #Array2
        #ani.save('bruh.mp4', fps=30)
        
        #if (self.record.checkState() != 0):
 #       self.grid[0,0] = 1000
#        self.grid[0,1] = 0
        ax = self.figure.add_subplot(111)
        self.mat = ax.matshow(self.grid, vmin=0, vmax=1000, interpolation='bilinear')

        #delete after debugging
        plt.colorbar(self.mat)
        ani = animation.FuncAnimation(self.figure, self.new_update, save_count=frames)
        ani.save('PressMat.mp4',fps=30, bitrate=333)
        sys.exit()
##        self.grid = np.zeros((num_rows,num_cols))
##        self.mat = ax.matshow(self.grid)
##

def main():
    app = QtGui.QApplication(sys.argv)
    widget = Press_Mat()
    #widget can be implement in other layout
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
