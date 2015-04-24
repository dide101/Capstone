import sys
from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.animation as animation
import matplotlib.figure as Figure
import matplotlib.pyplot as plt
import numpy as np

import SerialCommunication as serial


num_rows = 7
num_cols = 4
Array = bytearray(num_rows*num_cols)
sensor_num =num_rows*num_cols


ser = serial.sensorInit()

#updates mat, which should be spit out onto the figure


def plot(self):
        print("bruh!")
        try:
                ani = animation.FuncAnimation(figure, self.update, interval = 33, save_count = 50, blit=True)
                self.canvas.draw()
        except:
                print("Dropped a frame!")
        

class Window(QtGui.QDialog):
        def __init__(self, parent=None):
                super(Window, self).__init__(parent)

                #Variables Init
                self.figure = plt.figure()
                self.ax = self.figure.add_subplot(111)
                
                canvas = FigureCanvas(self.figure)
                
                self.mat = self.ax.matshow(np.zeros((num_rows,num_cols)))
                
                #global ax, mat, ser, Array, data
                
                toolbar = NavigationToolbar(canvas, self)
                toolbar.hide()

                
                # Start Button
                self.button = QtGui.QPushButton('Start')
                self.button.clicked.connect(plot)
                #self.button1 = QtGui.QPushButton('Record')
                #self.button.clicked.connect(self.plot)

                # set the layout
                layout = QtGui.QVBoxLayout()
                layout.addWidget(canvas)
                layout.addWidget(self.button)
                self.setLayout(layout)

                self.figure.canvas.draw()
                self.timer = self.startTimer(3)
                
        def timerEvent(self, event):
                
                self.ani = animation.FuncAnimation(self.figure, self.update, interval = 3, save_count = 50, blit=False)
                self.figure.canvas.draw()

        def update(self, data):
                #gets stuck at this line???
                Array = serial.readSensors(ser, sensor_num)
                data = serial.matrixConvert(Array, num_rows, num_cols) 
                #return data
                #print("updating")
 #               self.ax.clear()
                #mat.set_data(data)
                self.ax.matshow(data)
                plt.axis('off')
                #return mat
                
        def generate_data(self):
                #gets stuck at this line???
                Array = serial.readSensors(ser, self.sensor_num)
                data = serial.matrixConvert(Array, self.num_rows, self.num_cols)
                return data

if __name__ == '__main__':
        app = QtGui.QApplication(sys.argv)

        main = Window()
        main.setWindowTitle('PressMat')
        main.show()
        sys.exit(app.exec_()) 
