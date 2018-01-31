#coding:utf-8
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys,os
import math
import threading
import time

#导入其他模块
gRootDir = os.path.join(os.getcwd(), "..")#得到当前脚本工作目录
sys.path.append(gRootDir)#添加到系统
from Radar_Data import gPI#导入模块参数
from Radar_Data import g1Deg#导入模块参数
from Radar_Data import gRadarScale#导入模块参数
from Radar_Data import gShipLegendLen#导入模块参数
from Radar_Data import gRangeTable#导入模块参数
from Radar_Data import gEchoLineCountAFrame#导入模块参数
from Radar_Data import gRotate

from Radar_Echoline import RadarEcholine
'''
圆形窗口
'''
class RadarImage(QWidget):
    """docstring for RadarImage"""
    def __init__(self, parent = None):
        super(RadarImage, self).__init__(parent)
        screen = QDesktopWidget().screenGeometry()
        self.setMinimumSize(screen.width()/1.618,screen.height())
        self.setStyleSheet("background-color:#696969;")#背景色
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)#微件可以自行放大或缩小
        self.setSizePolicy(sizePolicy)

        center = QPoint(self.width()/2,self.height()/2)
        radius = 0
        if self.width() < self.height():
            radius = self.width()
        radius = self.height()
        radius /= 2

        self.SetCenter(center)
        self.SetRadius(radius)
        
        self.mHdt = 0#船首线
        self.mth = 0.0
        self.rotationangle = 0#扫描线旋转角

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(500)#画面刷新时间

    #************************************************************************
        '''self.pushButton = QPushButton("test")
        #self.pushButton.setGeometry(QRect(150, 160, 112, 34))
        Rgridlayout = QGridLayout()#右侧网格布局
        Rgridlayout.addWidget(self.pushButton)
        self.setLayout(Rgridlayout)

        self.pushButton.clicked.connect(self.__DrawESLine)'''

    #************************************************************************
    #窗体大小变化时，刷新
    def resizeEvent(self,event):
        center = QPoint(self.width()/2, self.height()/2)
        radius = 0
        if self.width() < self.height():
            radius = self.width()
        radius = self.height()
        radius /= 2
        self.SetCenter(center)
        self.SetRadius(radius)

    def paintEvent(self, event): 
        #先画背景
        painter = QPainter(self)
        brush = QBrush(QColor(0, 0, 0))
        painter.setBrush(brush)
        painter.setRenderHint(QPainter.Antialiasing)#反走样，圆滑
        side=min(self.width(),self.height())/2*gRadarScale#保证与最外圈半径相同
        painter.drawEllipse((self.width()/2-side), (self.height()/2-side),side*2, side*2)

        #再画其他图
        painterToPixmap = QPainter(self)
        self.Draw(painterToPixmap)

    # 绘制时的圆心坐标
    def SetCenter(self, center):
        self.mCenter = center;#微调圆心

    # 绘制半径
    def SetRadius(self, radius):
        self.mRadius = radius * gRadarScale

    # 绘制
    def Draw(self, p): 
        self.__DrawESLine(p)#扫描线
        self.__DrawDisCircleIn(p)#里圈1
        self.__DrawScaleLine(p)#刻度2
        self.__DrawShipHeadLine(p)#船首线3
        self.__DrawRangeLine(p)#刻度线4
        self.__DrawSysInfo(p)
        self.__UpdateAngle()
        
    # 绘制系统信息
    def __DrawSysInfo(self, p):
        pen = QPen(QColor(0, 255, 0))
        p.setFont(QFont("仿宋",11))
        p.setPen(pen)
        time = QTime.currentTime()
        text = time.toString("hh:mm:ss")

        #左上
        p.drawText(-370, -300, "时间: ".decode('utf-8') + text)
        p.drawText(-370, -320, "角度: ".decode('utf-8') + str(self.rotationangle) + "°".decode('utf-8'))
        #右上
        p.drawText(280, -300, "经度: ".decode('utf-8') + str(self.mHdt) + "°".decode('utf-8'))
        p.drawText(280, -320, "纬度: ".decode('utf-8') + str(self.mHdt) + "°".decode('utf-8'))

    #绘制距表圈
    def __DrawDisCircleIn(self, p):
        pen = QPen(QColor(0, 255, 0),1.5,Qt.SolidLine)#颜色、线宽、线型
        p.setPen(pen)
        p.setBrush(Qt.NoBrush)
        p.setRenderHint(QPainter.Antialiasing)#反走样，圆滑

        r = self.mRadius
        self.__DrawCircle(p, self.mCenter, r)         #最外圈n
        #self.__DrawCircle(p, self.mCenter, r*1.02)     #刻度圈
        self.__DrawCircle(p, self.mCenter, 0.2 * r)         
        self.__DrawCircle(p, self.mCenter, 0.4 * r)      
        self.__DrawCircle(p, self.mCenter, 0.6 * r)      
        self.__DrawCircle(p, self.mCenter, 0.8 * r)    
        #self.__DrawCircle(p, self.mCenter, 0.01 * r)    #圆心

    def __DrawCircle(self, p, center, r):
        x = center.x() - r 
        y = center.y() - r

        width = 2 * r
        height = 2 * r
        p.drawEllipse(x , y, width, height)#校准圆心

    # 绘制0线
    def __DrawShipHeadLine(self, p):
        #绘制船首线
        pen = QPen(QColor(0, 255, 0), 1, Qt.DashLine)#颜色、线宽、线型
        p.setPen(pen)
        p.setRenderHint(QPainter.Antialiasing)#反走样，圆滑

        angle = self.mHdt - 90 * g1Deg #g1Deg=3.1415926535898/180
        xStart = int(self.mCenter.x())
        yStart = int(self.mCenter.y())
        xEnd = int(self.mRadius * math.cos(angle) + xStart)
        yEnd = int(self.mRadius * math.sin(angle) + yStart)
        p.drawLine(xStart, yStart, xEnd, yEnd)

        #首线三角标
        pen = QPen(QColor(255,0,0))
        p.setPen(pen)
        brush = QBrush(QColor(255, 0, 0), Qt.SolidPattern)
        p.setBrush(brush);

        angle = self.mHdt + 90 * g1Deg
        ang = angle - 30 * g1Deg;
        cos_a = math.cos(ang);
        sin_a = math.sin(ang);
        x1 = xEnd + gShipLegendLen * cos_a;
        y1 = yEnd - gShipLegendLen * sin_a;

        ang = angle + 30 * g1Deg;
        cos_a = math.cos(ang);
        sin_a = math.sin(ang);
        x2 = xEnd + gShipLegendLen * cos_a;
        y2 = yEnd - gShipLegendLen * sin_a;

        p1 = QPointF(xEnd+1, yEnd)
        p2 = QPointF(x1+1, y1*1.5)#三角对称
        p3 = QPointF(x2+1, y2*1.5)
        p.drawPolygon(p1, p2, p3); 

    #绘制45°、135°、180°、225°、270°、315°、360°刻度线
    def __DrawScaleLine(self, p):
        pen = QPen(QColor(0,255,0), 1, Qt.DashLine)#颜色、线宽、线型
        p.setPen(pen)
        p.setRenderHint(QPainter.Antialiasing)#反走样，圆滑

        angleBox = [0,45,90,135,180,225,315]
        for angleX in angleBox:            
            angleL = self.mHdt + angleX * g1Deg
            xStart = int(self.mCenter.x())
            yStart = int(self.mCenter.y())
            xEndL = int(self.mRadius * math.cos(angleL) + xStart)
            yEndL = int(self.mRadius * math.sin(angleL) + yStart)
            p.drawLine(xStart,yStart, xEndL, yEndL)

    #表盘刻度、度数
    def __DrawRangeLine(self, p):
        pen = QPen(QColor(0, 255, 0),1.5,Qt.SolidLine)#颜色、线宽、线型
        p.setPen(pen)
        p.setBrush(Qt.NoBrush)
        p.setFont(QFont("仿宋",11))#字体,QFont.Bold
        p.setRenderHint(QPainter.Antialiasing)#反走样，圆滑

        side=min(self.width(),self.height())
        p.setViewport((self.width()-side)/2,(self.height()-side)/2, side, side)
        p.setWindow(0, 0, 700, 700)##初始值不用更改
        p.translate(350, 350)#不用更改

        #刻度计算算法不完善，但基本可实现
        m_startAngle = 180    #m_startAngle是起始角度
        m_endAngle =-180      #m_endAngle是结束角度
        m_scaleMajor = 36     #m_scaleMajor在一个量程中需要绘制的刻度总个数
        m_maxValue = 360      #预绘制刻度最大值
        m_minValue = 0        #预绘制刻度最小值
        fm = QFontMetricsF(QFont("Times",24))
        p.save()
        startRad = (270 - m_startAngle) * g1Deg
        deltaRad = (360 - m_startAngle - m_endAngle) * g1Deg / m_scaleMajor

        for i in range(0,m_scaleMajor):
            sina = math.sin(startRad - i * deltaRad)
            cosa = math.cos(startRad - i * deltaRad)

            ScaleV = 1.0 * i *((m_maxValue - m_minValue) / m_scaleMajor) + m_minValue
            if ScaleV == 0:
                str = '00'+ QString.number(ScaleV)
            elif ScaleV < 100:
                str = '0'+ QString.number(ScaleV)
            else:
                str = QString.number(ScaleV)
            w = fm.size(Qt.TextSingleLine,str).width()
            h = fm.size(Qt.TextSingleLine,str).height()
            x = 332 * cosa - w / 2
            y = -326 * sina + h / 4
            p.drawText(x+12, y-4, str)#函数的前两个参数是显示的坐标位置，后一个是显示的内容，是字符类型""
        p.restore()

        for i in range(0,360):
            p.save()
            p.rotate(i)
            if (i % 10 == 0):
                p.drawLine(0,-313,0,-306)
            elif (i % 5 ==0):
                p.drawLine(0,-311,0,-306)
            else:
                p.drawLine(0,-308,0,-306)
            p.restore()

    def __UpdateAngle(self):
        if self.rotationangle < 360:
            self.rotationangle += 1
        else:
            self.rotationangle = 0
        self.update()
    #扫描线
    def __DrawESLine(self, p):
        xStart = int(self.mCenter.x())
        yStart = int(self.mCenter.y())

        pen = QPen(QColor(0,255,0), 2)#颜色、线宽、线型
        p.setPen(pen)
        p.setRenderHint(QPainter.Antialiasing)#反走样，圆滑，但是吃CPU
        xEnd = int(self.mRadius * math.cos(self.rotationangle*g1Deg) + xStart)
        yEnd = int(self.mRadius * math.sin(self.rotationangle*g1Deg) + yStart)        
        p.drawLine(xStart,yStart, xEnd, yEnd)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = RadarImage()
    win.show()
    sys.exit(app.exec_())


        
