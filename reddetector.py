from re import A
from tkinter import W, Image
from PyQt5.QtWidgets import *
#from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
#from PyQt5.QtGui import QImage
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys
import cv2
import numpy as nu
#from sympy import cancel, capture, false, re, true

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        uic.loadUi("untitled.ui", self)

        self.radio = self.findChild(QRadioButton, "radioButton")
        self.stream = self.findChild(QLabel, "label")
        self.label = self.findChild(QLabel, "label_2")

        self.show()

        self.radio.clicked.connect(self.start)
        self.live = live()

        self.radio.setText("Mulai")

    def start(self):
        if self.radio.isChecked():
            self.radio.setText("Mati")
            self.live.start()
            self.live.image_up.connect(self.imgup)
        else:
            self.radio.setText("Mulai")
            self.live.stop()


    def imgup(self, Image):
        self.stream.setPixmap(QPixmap.fromImage(Image))

class live(QThread):
    image_up = pyqtSignal(QImage)
    def run(self):
        self.ThreadActive = True

        self.label = self.findChild(QLabel, "label_2")

        cam = cv2.VideoCapture(0)
        #if cam.isOpened():
            #self.label.setText("Kamera Terdeteksi")

        while self.ThreadActive:
            ret, frame = cam.read()
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                #Flip = cv2.flip(Image, 1)

                low = nu.array([1, 155, 84])
                up = nu.array([5, 255, 255])

                red_mask = cv2.inRange(Image, low, up)
                red = cv2.bitwise_and(frame, frame, mask=red_mask)

                turnred = cv2.cvtColor(red, cv2.COLOR_RGB2BGR)


                qtform = QImage(turnred.data, turnred.shape[1], turnred.shape[0], QImage.Format_RGB888)

                gambar = qtform.scaled(1121, 641, Qt.KeepAspectRatio)
                self.image_up.emit(gambar)

    def stop(self):
        self.ThreadActive = False
        self.quit()
         



app = QApplication(sys.argv)
Window = UI()
app.exec_()