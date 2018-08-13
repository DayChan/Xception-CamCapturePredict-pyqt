#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2018年1月29日
@author: Irony."[讽刺]
@site: http://alyl.vip, http://orzorz.vip, https://coding.net/u/892768447, https://github.com/892768447
@email: 892768447@qq.com
@file: OpencvWidget
@description: 
'''
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import cv2  # @UnresolvedImport 
import numpy
from Xception_predict_video import get_result,WIDTH,HEIGHT



class OpencvWidget(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(OpencvWidget, self).__init__(*args, **kwargs)
        self.fps = 24
        self.createUI()
        

    def createUI(self):
        self.resize(800, 600)
        self.setWindowTitle("Classifier")
        self.videoView = QLabel("稍候，正在初始化数据和摄像头。。。")
        self.videoView.setAlignment(Qt.AlignCenter)
        self.text_result = QLabel("")
        self.text_result.setAlignment(Qt.AlignCenter)
        self.vlayout = QVBoxLayout()
        self.vlayout.addWidget(self.videoView)
        self.vlayout.addWidget(self.text_result)
        self.widget = QWidget()
        self.widget.setLayout(self.vlayout)
        self.setCentralWidget(self.widget)


    def start(self):
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap or not self.cap.isOpened():
                return QMessageBox.critical(self, "错误", "打开摄像头失败")
            # 开启定时器定时捕获
            self.timer = QTimer(self, timeout=self.onCapture)
            self.timer.start(1000 / self.fps)
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))

    def closeEvent(self, event):
        if hasattr(self, "timer"):
            self.timer.stop()
            self.timer.deleteLater()
            self.cap.release()
            del self.predictor, self.detector, self.cascade, self.cap
        super(OpencvWidget, self).closeEvent(event)
        self.deleteLater()

    def onCapture(self):
        _, frame = self.cap.read()

        minisize = (WIDTH, HEIGHT)
        tmpframe = cv2.resize(frame, minisize)

        index,prop = get_result(tmpframe)
        del tmpframe
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3, QImage.Format_RGB888)
        del frame

        self.videoView.setPixmap(QPixmap.fromImage(img))
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
    # 5秒后启动
    QTimer.singleShot(5000, w.start)
    sys.exit(app.exec_())
