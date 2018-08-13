#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PIL import Image
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import cv2  # @UnresolvedImport
import numpy

from Xception_predict import get_result,WIDTH,HEIGHT



DOWNSCALE = 4


class OpencvWidget(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(OpencvWidget, self).__init__(*args, **kwargs)
        self.createUI()

        

    def createUI(self):
        self.resize(800, 600)
        self.setWindowTitle("Classifier")
        self.imageView = QLabel("add a image file")
        self.imageView.setAlignment(Qt.AlignCenter)
        self.btn_open = QPushButton("open")
        self.btn_open.clicked.connect(self.on_btn_open_clicked)
        self.text_result = QLabel("")
        self.text_result.setAlignment(Qt.AlignCenter)
        self.vlayout = QVBoxLayout()
        self.vlayout.addWidget(self.btn_open)
        self.vlayout.addWidget(self.imageView)
        self.vlayout.addWidget(self.text_result)
        self.widget = QWidget()
        self.widget.setLayout(self.vlayout)
        
        self.setCentralWidget(self.widget)
        self.createMenu()

    def on_btn_open_clicked(self, checked):
        self.filename = QFileDialog.getOpenFileName(self, "OpenFile", ".", "Image Files(*.jpg *.jpeg *.png)")[0]
        self.onPredict()
        
    def createMenu(self):
        
        menubar = self.menuBar()
        menu = menubar.addMenu("选择图片(F)")
        menu.addAction(QAction("打开", self, triggered=self.on_btn_open_clicked))
    

        
    def onPredict(self):
        img = cv2.imread(self.filename)
        scale = img.shape[0]/500
        img = cv2.resize(img, (int(img.shape[1]/scale), int(img.shape[0]/scale)), interpolation=cv2.INTER_CUBIC)
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3, QImage.Format_RGB888)
        img = QPixmap(img)
        self.imageView.setPixmap(img)


        index,prop = get_result(self.filename)
        if (index is not 0 and prop > 0.90):
            if(index is 0):
                self.text_result.setText("The result is: ballon")
            elif(index is 1):
                self.text_result.setText("The result is: UAV")
            elif(index is 2):
                self.text_result.setText("The result is: missile")
            elif(index is 3):
                self.text_result.setText("The result is: plane")
            elif(index is 4):
                self.text_result.setText("The result is: helicopter")
    
        elif (prop >= 0.995):
            self.text_result.setText("The result is: ballon")
        else:
            self.text_result.setText("The result is: other")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OpencvWidget()
    w.show()
    sys.exit(app.exec_())
