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
        self.grid[0,0] = 1000
        self.start()

    def start(self):
        self.setWindowTitle('PressMat')
        gridLayout = QtGui.QGridLayout()    
        self.setLayout(gridLayout)
        
        #button
        restart = QtGui.QPushButton("Start")
        restart.clicked.connect(self.plot)

        #checkbox
        self.record = QtGui.QCheckBox('Record', self)
        

        gridLayout.addWidget(self.canvas,0,0)
        gridLayout.addWidget(restart, 1,0)
        gridLayout.addWidget(self.record, 2,0)
        self.show()

    def plot(self):
        #Figure and subplot

        ax = self.figure.add_subplot(111)
        self.mat = ax.matshow(self.grid, interpolation='bicubic')
        plt.axis('off')
            
        ani = animation.FuncAnimation(self.figure, self.update, interval=3, save_count=500)

        if (self.record.checkState() != 0):
            ani.save('bruh.mp4', writer="ffmpeg")
            
        self.canvas.draw()
        
    def update(self, data):
        #print('Updating')
        newGrid = self.grid.copy()
        Array = serial.readSensors(ser, sensor_num)
        newGrid = serial.matrixConvert(Array, num_rows, num_cols)
        self.mat.set_data(newGrid)
        self.grid = newGrid

    #simply restarts data
    def restart_animation(self, ax, figure):
        self.grid = np.zeros((num_rows,num_cols))
        self.mat = ax.matshow(self.grid)


def main():
    app = QtGui.QApplication(sys.argv)
    widget = Press_Mat()
    #widget can be implement in other layout
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
