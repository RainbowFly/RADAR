#coding:utf-8
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys

'''
雷达界面初始化
'''

class RadarWidget(QWidget):
    """docstring for RadarWidget"""
    def __init__(self, parent = None):
        super(RadarWidget, self).__init__(parent)
        self.setWindowIcon(QIcon('Radar.ICO'))#设置窗口图标
        self.setWindowTitle("Radar-Simulator".decode('utf-8'))
        self.setFont(QFont("Roman times",10.5))#font
        #窗口居中
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry() #此处的geometry()首字母必须要小写，否则无法测试通过。
        self.move((screen.width()-size.width())/2,(screen.height()-size.height())/2)

        self.showMaximized()#窗口最大化显示
        self.setStyleSheet("background-color:#7A7A7A;")#背景色
        #隐藏标题栏
        #self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        #只显示关闭按钮
        #self.setWindowFlags(Qt.CustomizeWindowHint| Qt.WindowCloseButtonHint )

        '''gridlayout = QGridLayout()
        self.RButton1 = QPushButton("关闭系统".decode('utf-8'))
        gridlayout.addWidget(self.RButton1,0,0)
        self.connect(self.RButton1,SIGNAL('clicked()'),self.close)
        self.setLayout(gridlayout)

    def close(self):
        sys.exit()'''

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = RadarWidget()
    win.show()
    sys.exit(app.exec_())
