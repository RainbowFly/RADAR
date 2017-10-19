#coding:utf-8
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys,os
import math

#导入其他模块
gRootDir = os.path.join(os.getcwd(), "..")#得到当前脚本工作目录
sys.path.append(gRootDir)#添加到系统
from Radar_Data import gPI#导入模块参数
from Radar_Data import g1Deg#导入模块参数
from Radar_Data import gRadarEchoScale#导入模块参数
from Radar_Data import gEchoLineCountAFrame#导入模块参数
from Radar_Data import gShipLegendLen#导入模块参数
from Radar_Data import gRangeTable#导入模块参数

'''
圆形窗口
'''

class RadarImage(QWidget):
    """docstring for RadarImage"""
    def __init__(self, parent = None):
        super(RadarImage, self).__init__(parent)
        #self.setStyleSheet("background-color:#7A7A7A;")#背景色
        self.resize(600,600)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)#微件可以自行放大或缩小
        self.setSizePolicy(sizePolicy)

        self.mPixmap = QPixmap(self.width(), self.height())
        self.mPixmap.fill(Qt.black)
        self.mRadar_data = RadarData()

        center = QPoint(self.width()/2,self.height()/2)
        radius = 0
        if self.width() <self.height():
            radius = self.width()
        radius = self.height()
        radius /= 2

        self.mRadar_data.SetCenter(center)
        self.mRadar_data.SetRadius(radius)

    def paintEvent(self, event): 
        # 回波绘制 绘制到后台缓存
        painterToPixmap = QPainter(self.mPixmap)
        self.mRadar_data.Draw(painterToPixmap)

        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.width(), self.height(), self.mPixmap)
 
class RadarData(QWidget):
    """docstring for RadarData"""
    def __init__(self, parent = None):
        super(RadarData, self).__init__(parent)
        self.mCenter = QPoint(0,0)
        self.mRadius = 0
        
        self.SetCenter(QPoint(0,0))
        self.SetRadius(0)
        self.SetHdt(0)

    # 绘制时的圆心坐标
    def SetCenter(self, center):
        self.mCenter = center;

    # 绘制半径
    def SetRadius(self, radius):
        self.mRadius = radius * gRadarEchoScale

    #船首线
    def SetHdt(self,hdt):
        self.mHdt = 0

    # 绘制
    def Draw(self, p): 
        self.__DrawShipHeadLine(p)#船首线
        self.__DrawScaleLine(p)#刻度线
        self.__DrawScale(p)#绘制刻度
        self.__DrawDisCircle(p)

    # 绘制距标圈
    def __DrawDisCircle(self, p):
        pen = QPen(QColor(0, 150, 0),2,Qt.SolidLine)#颜色、线宽、线型
        p.setPen(pen)
        p.setBrush(Qt.NoBrush)

        r = self.mRadius
        rHalf = 0.2 * r#修改半径
        rHalfOne = 0.4 * r
        rHalfTwo = 0.6 * r
        rHalfThree = 0.8 * r
        rHalfcenter = 0.01 * r
        self.__DrawCircle(p, self.mCenter, r)         #最外圈n
        self.__DrawCircle(p, self.mCenter, rHalf)         #
        self.__DrawCircle(p, self.mCenter, rHalfOne)      #
        self.__DrawCircle(p, self.mCenter, rHalfTwo)      #
        self.__DrawCircle(p, self.mCenter, rHalfThree)    #
        self.__DrawCircle(p, self.mCenter, rHalfcenter)

    # 绘制船艏线
    def __DrawShipHeadLine(self, p):
        #绘制船首线
        pen = QPen(QColor(0, 150, 0), 1, Qt.DashLine)#颜色、线宽、线型
        p.setPen(pen)

        angle = self.mHdt - 90 * g1Deg #g1Deg=3.1415926535898/180
        xStart = int(self.mCenter.x())
        yStart = int(self.mCenter.y())
        xEnd = int(self.mRadius * math.cos(angle) + xStart)
        yEnd = int(self.mRadius * math.sin(angle) + yStart)
        p.drawLine(xStart, yStart, xEnd, yEnd)

        #船首线三角标
        pen = QPen(QColor(255,255,255))
        p.setPen(pen)
        brush = QBrush(QColor(255, 255, 255), Qt.SolidPattern);
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

        p1 = QPointF(xEnd, yEnd)
        p2 = QPointF(x1, y1)
        p3 = QPointF(x2, y2)
        p.drawPolygon(p1, p2, p3); 

    #绘制45°、135°、180°、225°、270°、315°、360°刻度线
    def __DrawScaleLine(self, p):
        pen = QPen(QColor(0,150,0), 1, Qt.DashLine)#颜色、线宽、线型
        p.setPen(pen)

        angleBox = [0,45,90,135,180,225,315]
        for angleX in angleBox:            
            angleL = self.mHdt + angleX * g1Deg
            xStart = int(self.mCenter.x())
            yStart = int(self.mCenter.y())
            xEndL = int(self.mRadius * math.cos(angleL) + xStart)
            yEndL = int(self.mRadius * math.sin(angleL) + yStart)
            p.drawLine(xStart,yStart, xEndL, yEndL)

    #刻度绘制
    def __DrawScale(self, p):
        pen = QPen(QColor(0,255,0))#颜色、线宽
        p.setPen(pen)
        xStart = int(self.mCenter.x())
        yStart = int(self.mCenter.y())

        angle0 = self.mHdt - 90 * g1Deg   #0°
        xEnd0 = int(self.mRadius * math.cos(angle0) + xStart)
        yEnd0 = int(self.mRadius * math.sin(angle0) + yStart)
        p.drawText(xEnd0-2, yEnd0-12, "0°".decode('utf-8'))

        angle1 = self.mHdt - 45 * g1Deg   #45°
        xEnd1 = int(self.mRadius * math.cos(angle1) + xStart)
        yEnd1 = int(self.mRadius * math.sin(angle1) + yStart)
        p.drawText(xEnd1+2, yEnd1-3, "45°".decode('utf-8'))

        angle2 = self.mHdt - g1Deg   #90°
        xEnd2 = int(self.mRadius * math.cos(angle2) + xStart)
        yEnd2 = int(self.mRadius * math.sin(angle2) + yStart)
        p.drawText(xEnd2+5, yEnd2+9, "90°".decode('utf-8'))

        angle3 = self.mHdt + 45*g1Deg   #135°
        xEnd3 = int(self.mRadius * math.cos(angle3) + xStart)
        yEnd3 = int(self.mRadius * math.sin(angle3) + yStart)
        p.drawText(xEnd3+5, yEnd3+12, "135°".decode('utf-8'))

        angle4 = self.mHdt + 90*g1Deg   #180°
        xEnd4 = int(self.mRadius * math.cos(angle4) + xStart)
        yEnd4 = int(self.mRadius * math.sin(angle4) + yStart)
        p.drawText(xEnd4-8, yEnd4+14, "180°".decode('utf-8'))

        angle5 = self.mHdt + 135*g1Deg   #225°
        xEnd5 = int(self.mRadius * math.cos(angle5) + xStart)
        yEnd5 = int(self.mRadius * math.sin(angle5) + yStart)
        p.drawText(xEnd5-26, yEnd5+12, "225°".decode('utf-8'))

        angle6 = self.mHdt + 180*g1Deg   #270°
        xEnd6 = int(self.mRadius * math.cos(angle6) + xStart)
        yEnd6 = int(self.mRadius * math.sin(angle6) + yStart)
        p.drawText(xEnd6-26, yEnd6+4, "270°".decode('utf-8'))

        angle7 = self.mHdt + 225*g1Deg   #315°
        xEnd7 = int(self.mRadius * math.cos(angle7) + xStart)
        yEnd7 = int(self.mRadius * math.sin(angle7) + yStart)
        p.drawText(xEnd7-20, yEnd7-4, "315°".decode('utf-8'))

    def __DrawCircle(self, p, center, r):
        x = center.x() - r
        y = center.y() - r

        width = 2 * r
        height = 2 * r
        p.drawEllipse(x, y, width, height)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = RadarImage()
    win.show()
    sys.exit(app.exec_())

        
