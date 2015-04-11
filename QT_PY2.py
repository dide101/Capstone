import sys
import time

from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import matplotlib.pyplot as plt

from SerialCommunication import *



class Window(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
 
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
 
         
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.hide()
 
##        # Start Button
##        self.button = QtGui.QPushButton('Start')
##        self.button.clicked.connect(self.plot)
##        
        # set the layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.canvas)
##        layout.addWidget(self.button)
        self.setLayout(layout)

        global ser, Array, num_rows, num_cols, Matrix, count, sensor_num
        ser = sensorInit()
        num_rows = 7
        num_cols = 4
        Array = bytearray(num_rows*num_cols)
        Matrix = np.zeros((num_cols,num_rows))
        
        count = 33
        sensor_num = 24
        #timer info
        self.timer = QtCore.QBasicTimer()
        self.timer.start(count, self)
        self.step = 0

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.update()
            Array = readSensors(ser, sensor_num)
            Matrix = matrixConvert(Array, num_rows, num_cols)
            ax = self.figure.add_subplot(111)
            ax.imshow(Matrix, interpolation='nearest', cmap='Spectral')
            self.canvas.draw()
            super(Window, self).timerEvent(event)
                        
         
##    def plot(self):
##        #while(1):
##        Array = readSensors(ser)
##        Matrix = matrixConvert(Array, num_rows, num_cols)
##        #time.sleep(1)
##        ax = self.figure.add_subplot(111)
##        ax.imshow(Matrix, interpolation='nearest', cmap=plt.cm.ocean)
##        self.canvas.draw()
            
            

 
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
 
    main = Window()
    main.setWindowTitle('Press Mat')
    main.show()
 
    sys.exit(app.exec_())
    ser.close()
