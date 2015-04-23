import sys

from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

import SerialCommunication as serial



class Window(QtGui.QDialog):
        def __init__(self, parent=None):
                super(Window, self).__init__(parent)

                #Variables Init
                self.num_rows = 7
                self.num_cols = 4

                self.sensor_num =self.num_rows*self.num_cols
                self.figure = plt.figure()
                 self.canvas = FigureCanvas(self.figure)
                
                global ax, mat, ser, Array, data
                
                Matrix = np.zeros((self.num_rows, self.num_cols))
                Array = bytearray(self.num_rows*self.num_cols)
                ser = serial.sensorInit()
                ax = self.figure.add_subplot(111)
                self.toolbar = NavigationToolbar(self.canvas, self)
                self.toolbar.hide()
                mat = ax.matshow(np.zeros((self.num_rows,self.num_cols)))
                # Start Button
                self.button = QtGui.QPushButton('Start')
                self.button.clicked.connect(self.plot)
                #self.button1 = QtGui.QPushButton('Record')
                #self.button.clicked.connect(self.plot)

                # set the layout
                layout = QtGui.QVBoxLayout()
                layout.addWidget(self.canvas)
                layout.addWidget(self.button)
                self.setLayout(layout)
                
                
        #recieves information from the Arduino
        def generate_data(self):
                #gets stuck at this line???
                Array = serial.readSensors(ser, self.sensor_num)
                data = serial.matrixConvert(Array, self.num_rows, self.num_cols)
                return data

        #updates mat, which should be spit out onto the figure
        def update(self, data):
                print("updating")
                mat.set_data(data)
                return mat

        #gets the data argument to be passed into update()
        def data_gen(self):
                print("data_gen")
                yield self.generate_data()

        def plot(self):
                print("bruh!")
                self.ani = animation.FuncAnimation(self.figure, self.update, self.data_gen, interval = 1, save_count = 50, blit=True)

if __name__ == '__main__':
        app = QtGui.QApplication(sys.argv)

        main = Window()
        main.setWindowTitle('PressMat')
        main.show()

        sys.exit(app.exec_())
