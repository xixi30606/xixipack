##seperate window
##interactive file

##main window
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QColorDialog, QFontDialog, QTextEdit, QFileDialog, QLabel
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen
from PyQt5.QtCore import QCoreApplication ,Qt
import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtWidgets,QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QInputDialog, QGridLayout, QLabel, QPushButton, QFrame
import os
class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):

        self.setGeometry(500, 500, 800, 500)
        self.setWindowTitle('svplot.dspec')

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.tx = QTextEdit(self)
        self.tx.setGeometry(20, 20, 300, 270)

        self.bt1 = QPushButton('Open the measurement set',self)
        self.bt1.move(550,20)
        self.bt2 = QPushButton('Make the dynamic spectrum',self)
        self.bt2.move(550,70)
        self.bt3 = QPushButton('Display the dynamic spectrum',self)
        self.bt3.move(550,120)
        self.bt4 = QPushButton('Quit', self)
        self.bt4.clicked.connect(QCoreApplication.instance().quit)
        self.bt4.resize(70,30)
        self.bt4.move(550, 450)

        self.bt1.clicked.connect(self.openfile)
        self.bt2.clicked.connect(self.mkds)
        self.show()
    def openfile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open the file','./',("Measuremet set (*.ms *npz)"))
        if fname[0]:
            self.tx.setText(fname[0]) 
    def mkds(self):
        fig= plt.figure(figsize=(10, 6))
        ax = plt.subplot()
        plt.show()
    def handle_click(self):
        if not self.isVisible():
            self.show()

##Window 2 display dynamic spectrum
##Need to do:1.complete state bar 2: do the interactive box
class Display(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(Display,self).__init__(parent)
        self.resize(800, 659)
        self.menu = QtWidgets.QMenu("Plot")
        self.menu_action = QtWidgets.QAction("Open Specfile and Plot",self.menu)
        self.menu.addAction(self.menu_action)
        self.menuBar().addMenu(self.menu)
        self.menu_action.triggered.connect(self.plot_)
        self.menu2 = QtWidgets.QMenu("Clean")
        self.menu2_action1 = QtWidgets.QAction("Clean Box",self.menu)
        self.menu2.addAction(self.menu2_action1)
        self.menuBar().addMenu(self.menu2)
        self.menu2_action1.triggered.connect(self.plot_)
        self.menu2_action2 = QtWidgets.QAction("Parameter Clean",self.menu)
        self.menu2.addAction(self.menu2_action2)
        self.menuBar().addMenu(self.menu2)
        self.menu3 = QtWidgets.QMenu("Quit")
        self.menu3_action = QtWidgets.QAction("Back",self.menu)
        self.menu3.addAction(self.menu3_action)
        self.menuBar().addMenu(self.menu3)
        self.setCentralWidget(QtWidgets.QWidget())
        self.statusBar().showMessage('statesbar')

    def handle_click(self):
        if not self.isVisible():
            self.show()


    def plot_(self):
        specfile = QFileDialog.getOpenFileName(self, 'Open the file','./',("specfile (*.npz)"))
        plt.cla()
        fig = plt.figure()
        data=np.load(specfile[0])
        spec = data['spec']
        spec_plt = (spec[0, 0, :, :] + spec[1, 0, :, :]) / 2
        tim = data['tim']
        freq = data['freq']
        plt.pcolormesh(tim, freq, spec_plt, cmap='jet')
        cavans = FigureCanvas(fig)
        self.setCentralWidget(cavans)

##Window 3 clean
##Need to do:1.fix the stokes 2. check the clean para
class Clean(QWidget):
    def __init__(self):       
        super(Clean,self).__init__()
        self.initUi()

    def initUi(self):
        self.setWindowTitle("Clean")
        self.setGeometry(600,600,500,450)

        label1=QLabel("Imagename:")
        label2=QLabel("Spw:")
        label3=QLabel("Timerange:")
        label4=QLabel("Phasecenter:")
        label5=QLabel("Stokes:")
        label6=QLabel("Confirm")

        self.nameLable = QLabel("read from specfile")
        self.nameLable.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        self.spwLable = QLabel(":''")
        self.spwLable.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        self.numberLable = QLabel(":''")
        self.numberLable.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        self.TimeLable = QLabel(":''")
        self.TimeLable.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        self.PhaLable = QLabel("I")
        self.PhaLable.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        self.stoLable = QLabel("I")
        self.stoLable.setFrameStyle(QFrame.Panel|QFrame.Sunken)

        nameButton=QPushButton("Input")
        nameButton.clicked.connect(self.Imagename)
        styleButton=QPushButton("Input")
        styleButton.clicked.connect(self.SelectSpw)
        numberButton=QPushButton("Input")
        numberButton.clicked.connect(self.SelectTimerange)
        costButton=QPushButton("Input")
        costButton.clicked.connect(self.Phasecenter)
        introductionButton=QPushButton("Input")
        introductionButton.clicked.connect(self.Stokes)
        self.OkButton=QPushButton("Ok",self)
        self.OkButton.clicked.connect(self.Con)
        self.CancelButton=QPushButton("Back",self)

        mainLayout=QGridLayout()
        mainLayout.addWidget(label1,0,0)
        mainLayout.addWidget(self.nameLable,0,1)
        mainLayout.addWidget(nameButton,0,2)
        mainLayout.addWidget(label2,1,0)
        mainLayout.addWidget(self.spwLable,1,1)
        mainLayout.addWidget(styleButton,1,2)
        mainLayout.addWidget(label3,2,0)
        mainLayout.addWidget(self.TimeLable,2,1)
        mainLayout.addWidget(numberButton,2,2)
        mainLayout.addWidget(label4,3,0)
        mainLayout.addWidget(self.PhaLable,3,1)
        mainLayout.addWidget(costButton,3,2)
        mainLayout.addWidget(label5,4,0)
        mainLayout.addWidget(self.stoLable,4,1)
        mainLayout.addWidget(introductionButton,4,2)
        mainLayout.addWidget(label6,5,0)
        mainLayout.addWidget(self.OkButton,5,1)
        mainLayout.addWidget(self.CancelButton,5,2)

        self.setLayout(mainLayout)



    def Imagename(self):
        name,ok = QInputDialog.getText(self,"Imagename","Input imagename:",
                                       QLineEdit.Normal,self.nameLable.text())
        if ok and (len(name)!=0):
            self.nameLable.setText(name)
    def SelectSpw(self):
        spw,ok = QInputDialog.getText(self,"Spw","Input spw:",
                                       QLineEdit.Normal,self.spwLable.text())
        if ok :
            self.spwLable.setText(spw)

    def SelectTimerange(self):
        timerange,ok = QInputDialog.getText(self,"Timerange","Input timerange:",
                                       QLineEdit.Normal,self.TimeLable.text())
        if ok :
            self.TimeLable.setText(timerange)

    def Phasecenter(self):
        pha,ok = QInputDialog.getText(self,"Phasecenter","Input Phasecenter:",
                                       QLineEdit.Normal,self.PhaLable.text())
        if ok :
            self.PhaLable.setText(pha)

    def Stokes(self):
        list = ["I","V","RR","LL","RRLL","IV"]
        style,ok = QInputDialog.getItem(self,"Stokes","Select the Stokes",list)
        if ok :
            self.stoLable.setText(style)

    def handle_click(self):
        if not self.isVisible():
            self.show()

    def Con(self):
        os.system('rm -rf cleanpa.npz')
        try:
            #np.savez('cleanpa.npz',imagename=str(self.nameLable.text()),spw=str(self.spwLable.text()),timerange=str(self.TimeLable.text()),\
            #pha=str(self.PhaLable.text()),sto=str(QInputDialog.getItem(self.introductionButton())))
            np.savez('cleanpa.npz',imagename=str(self.nameLable.text()),spw=str(self.spwLable.text()),timerange=str(self.TimeLable.text()),pha=str(self.PhaLable.text()))
        except:
            QMessageBox.information(self,"Information","No clean parameters created",QMessageBox.Yes)
        if os.path.exists('cleanpa.npz'):
            QMessageBox.information(self,"Information","Save the clean parameters successfully!",QMessageBox.Yes)




if __name__ == "__main__":
    App = QApplication(sys.argv)
    ma = Main()
    s = Display()
    c = Clean()
    ma.bt3.clicked.connect(s.handle_click)
    ma.bt3.clicked.connect(ma.hide)
    s.menu3_action.triggered.connect(s.hide)
    s.menu3_action.triggered.connect(ma.handle_click)
    s.menu2_action2.triggered.connect(s.hide)
    s.menu2_action2.triggered.connect(c.handle_click)
    c.CancelButton.clicked.connect(c.hide)
    c.CancelButton.clicked.connect(s.handle_click)
    ma.show()
    sys.exit(App.exec_())



class Example(QWidget):
    distance_from_center = 0
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setMouseTracking(True)
    def initUI(self):
        self.setGeometry(200, 200, 1000, 500)
        self.setWindowTitle('interactive window')
        self.label = QLabel(self)
        self.label.resize(500, 40)
        self.show()
        self.pos = None

    def mouseMoveEvent(self, event):
        distance_from_center = round(((event.y() - 250)**2 + (event.x() - 500)**2)**0.5)
        self.label.setText('location: ( x: %d ,y: %d )' % (event.x(), event.y()) + " dist: " + str(distance_from_center))       
        self.pos = event.pos()
        self.update()

    def paintEvent(self, event):
        if self.pos:
            q = QPainter(self)
            q.drawLine(0, 0, self.pos.x(), self.pos.y())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())










































