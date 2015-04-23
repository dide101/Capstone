import sys
#import time

from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

import SerialCommunication as serial

num_rows = 7
num_cols = 4
Array = bytearray(num_rows*num_cols)
sensor_num =num_rows*num_cols
figure = plt.figure()
ax = figure.add_subplot(111)
mat = ax.matshow(np.zeros((num_rows,num_cols)))
ser = serial.sensorInit()



def generate_data():
        #gets stuck at this line???
        Array = serial.readSensors(ser, sensor_num)
        data = serial.matrixConvert(Array, num_rows, num_cols)
        return data

#updates mat, which should be spit out onto the figure
def update(data):
        print("updating")
        mat.set_data(data)
        return mat

#gets the data argument to be passed into update()
def data_gen():
        print("data_gen")
        
        yield generate_data()

def plot():
        print("bruh!")
        ani = animation.FuncAnimation(figure, update, data_gen, interval = 1000, save_count = 50, blit=True)
        plt.show()

class Window(QtGui.QDialog):
        def __init__(self, parent=None):
                super(Window, self).__init__(parent)
                #Variables Init
                canvas = FigureCanvas(figure)

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
        
                
        #recieves information from the Arduino
        
        


# def generate_data(self):
#       Array = readSensors(self.ser, self.sensor_num)
#       data= matrixConvert(Array, self.num_rows, self.num_cols)
#       return data

# def update(self, data, mat):
#       mat.set_data(data)
#       return mat

# def animate(self, mat):
#       ani = animation.FuncAnimation(self.figure, self.update(data, mat), self.generate_data, interval = 33, save_count = 50, blit=True)
#       return ani
# def plot(self):
#       mat = ax.matshow(self.generate_data())
#       while True:
#               self.animate(mat)
#               self.canvas.draw()      
#       #plt.show()
#       #ani.save('blah.mp4', clear_temp=False)

if __name__ == '__main__':
        app = QtGui.QApplication(sys.argv)

        main = Window()
        main.setWindowTitle('PressMat')
        main.show()

        sys.exit(app.exec_())
