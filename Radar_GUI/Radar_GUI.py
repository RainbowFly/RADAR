#coding:utf-8
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys,os

#导入其他模块
gRootDir = os.path.join(os.getcwd(), "..")#得到当前脚本工作目录
sys.path.append(gRootDir)#添加到系统
from Radar_radarwin.Radar_radarWin import RadarImage
from Radar_Infor.Radar_information import RadarInfor
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
        '''screen = QDesktopWidget().screenGeometry()
        size = self.geometry() #此处的geometry()首字母必须要小写，否则无法测试通过。
        self.move((screen.width()-size.width())/2,(screen.height()-size.height())/2)'''

        self.showMaximized()#窗口最大化显示
        self.setStyleSheet("background-color:#7A7A7A;")#背景色
        #隐藏标题栏
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        #只显示关闭按钮
        #self.setWindowFlags(Qt.CustomizeWindowHint| Qt.WindowCloseButtonHint )

        Hlayout = QHBoxLayout()#总布局
        
        self.radarWinL = RadarImage()
        Lgridlayout = QGridLayout()#左侧网格布局
        Lgridlayout.addWidget(self.radarWinL)

        self.radarWinR = RadarInfor()
        Rgridlayout = QGridLayout()#右侧网格布局
        Rgridlayout.addWidget(self.radarWinR)

        Hlayout.addLayout(Lgridlayout)#顺序
        Hlayout.addLayout(Rgridlayout)
        self.setLayout(Hlayout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = RadarWidget()
    win.show()
    sys.exit(app.exec_())
    
