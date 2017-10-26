#coding:utf-8
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys,os

#导入其他模块
gRootDir = os.path.join(os.getcwd(), "..")#得到当前脚本工作目录
sys.path.append(gRootDir)#添加到系统

class RadarInfor(QWidget):
    """docstring for RadarInfor"""
    def __init__(self, parent=None):
        super(RadarInfor, self).__init__(parent)
        screen = QDesktopWidget().screenGeometry()
        self.setMinimumSize(screen.width()-screen.width()/1.618,screen.height())
        self.setStyleSheet("background-color:#5F9EA0;")#背景色
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)#微件可以自行放大或缩小
        self.setSizePolicy(sizePolicy)
        
        self.RButton1 = QPushButton("运行".decode('utf-8'))
        self.RButton2 = QPushButton("停止".decode('utf-8'))

        self.RButton3 = QPushButton("退出".decode('utf-8'))
        self.RButton3.clicked.connect(self.close)

        Rgridlayout = QGridLayout()#右侧网格布局
        Rgridlayout.addWidget(self.RButton1,0,0)
        Rgridlayout.addWidget(self.RButton2,0,1)
        Rgridlayout.addWidget(self.RButton3,0,2)
        self.setLayout(Rgridlayout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = RadarInfor()
    win.show()
    sys.exit(app.exec_())
