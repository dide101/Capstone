import sys
from PyQt4 import QtGui

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

import numpy as np


class Monitor(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)

        # the file is 5 float values separated by spaces on every line, like this:
        #0.28 0.18 0.18 0.18 0.18
        #0.352 0.162 0.162 0.162 0.162
        #0.4168 0.1458 0.1458 0.1458 0.1458
        #0.37512 0.23122 0.13122 0.13122 0.13122
        self.data = [np.array(map(float, line.strip().split())) for line in open('data.txt').readlines()]
        self.counter = 1

        # the width of the bars
        self.width = 0.8

        # the locations of the bars
        self.locs = np.arange(len(self.data[0]))

        # the first set of bars
        self.bars = self.ax.bar(self.locs, self.data[0], self.width, color='#6a7ea6')

        # set up the lables for the bars
        self.ax.set_xticks(self.locs+0.5)
        self.ax.set_xticklabels(['Red', 'Green', 'Black', 'Orange', 'Yellow'])

        # set the limit for the x and y
        self.ax.set_xlim(0., len(self.data[0]))
        self.ax.set_ylim(0., 1.,)

        # draw the canvas
        self.fig.canvas.draw()

        # start the timer
        self.timer = self.startTimer(1000)


    def timerEvent(self, evt):
        # update the height of the bars, one liner is easier
        [bar.set_height(self.data[self.counter][i]) for i,bar in enumerate(self.bars)]

        # force the redraw of the canvas
        self.fig.canvas.draw()

        # update the data row counter
        self.counter += 1

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    w = Monitor()
    w.setWindowTitle("Convergence")
    w.show()
    sys.exit(app.exec_())
