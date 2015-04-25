from PyQt4 import QtGui,QtCore
import sys, time, cv
from psychopy import visual, event, core
#import Image, time, pylab, cv, numpy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

import SerialCommunication as serial

#constants
num_rows = 10
num_cols = 5
sensor_num = num_rows*num_cols

ser = serial.sensorInit()
for i in range (4):
    Array = serial.readSensors(ser, 28)

from functools import partial 

class CamWorker(QtCore.QThread): 
    def __init__(self): 
        super(CamWorker, self).__init__() 
        self.cap = cv.CaptureFromCAM(0)
        capture_size = (640,480)
        cv.SetCaptureProperty(self.cap, cv.CV_CAP_PROP_FRAME_WIDTH, capture_size[0])
        cv.SetCaptureProperty(self.cap, cv.CV_CAP_PROP_FRAME_HEIGHT, capture_size[1])
 
    def run(self):
        while 1:
            time.sleep(0.01)
            frame = cv.QueryFrame(self.cap)
            im = QtGui.QImage(frame.tostring(), frame.width, frame.height, QtGui.QImage.Format_RGB888).rgbSwapped()	
            self.emit(QtCore.SIGNAL('webcam_frame(QImage)'), im)


class Press_Mat(QtGui.QWidget):
    def __init__(self):
        super(Press_Mat, self).__init__()


        self.figure = plt.figure()
        self.resize(1500,650)
        self.scene = QtGui.QGraphicsScene(self)
        self.view  = QtGui.QGraphicsView(self.scene)

        self.canvas = FigureCanvas(self.figure)
        self.grid = serial.matrixConvert(Array, num_rows, num_cols)
        self.grid[0,0] = 1000
        
        self.setWindowTitle('PressMat')
        gridLayout = QtGui.QGridLayout()
        self.setLayout(gridLayout)
        
        #button
        restart = QtGui.QPushButton("Start")
        restart.clicked.connect(self.plot)

        #checkbox
        self.record = QtGui.QCheckBox('Record', self)


        gridLayout.addWidget(self.canvas,1,0)
        gridLayout.addWidget(restart, 2,0)
        gridLayout.addWidget(self.record, 2,1)
        gridLayout.addWidget(self.view,1,1)
        self.show()
        #self.start()

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
        gridLayout.addwidget(self.view,3,0)
        self.show()

    def plot(self):
        #Figure and subplot

        ax = self.figure.add_subplot(111)
        self.mat = ax.matshow(self.grid)
        plt.axis('off')
            
        ani = animation.FuncAnimation(self.figure, self.update, interval=3, save_count=500)

#        if (self.record.checkState() != 0):
#            ani.save('bruh.mp4', writer="ffmpeg")
            
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
        
    def Frame(self, im):
        pix = QtGui.QPixmap(im)
        self.scene.clear()
        self.scene.addPixmap(pix)

def main():
    app = QtGui.QApplication(sys.argv)
    widget = Press_Mat()
    camWorker = CamWorker()
    QtCore.QObject.connect(camWorker, QtCore.SIGNAL("webcam_frame(QImage)"), widget.Frame)
    camWorker.start()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
