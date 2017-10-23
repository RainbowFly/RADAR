#coding:utf-8
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys,os
import math

#导入其他模块
gRootDir = os.path.join(os.getcwd(), "..")#得到当前脚本工作目录
sys.path.append(gRootDir)#添加到系统
from Radar_radardraw import RadarData
'''
圆形窗口
'''

class RadarImage(QWidget):
    """docstring for RadarImage"""
    def __init__(self, parent = None):
        super(RadarImage, self).__init__(parent)
        self.resize(700,700)
        self.setStyleSheet("background-color:#7A7A7A;")#背景色
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)#微件可以自行放大或缩小
        self.setSizePolicy(sizePolicy)
        self.mRadar_data = RadarData()

        center = QPoint(self.width()/2,self.height()/2)
        radius = 0
        radius = min(self.height(),self.width())
        radius /= 2

        self.mRadar_data.SetCenter(center)
        self.mRadar_data.SetRadius(radius)

    #窗体大小变化时，刷新
    def resizeEvent(self,event):
        center = QPoint(self.width()/2, self.height()/2)
        radius = 0
        radius = min(self.height(),self.width())
        radius /= 2
        self.mRadar_data.SetCenter(center)
        self.mRadar_data.SetRadius(radius)

    def paintEvent(self, event): 
        #先画背景
        painter = QPainter(self)
        brush = QBrush(QColor(0, 0, 0))
        painter.setBrush(brush)
        side=min(self.width(),self.height())
        painter.drawEllipse((self.width()-side)/2, (self.height()-side)/2,side, side)

        #再画其他图
        painterToPixmap = QPainter(self)
        self.mRadar_data.Draw(painterToPixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = RadarImage()
    win.show()
    sys.exit(app.exec_())

        
