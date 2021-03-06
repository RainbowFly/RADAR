# -*- coding: utf-8 -*-

gPI = 3.1415926535898
g1Deg = gPI / 180

gRadarScale = 0.86#调节雷达图大小
gEchoLineCountAFrame = 2048
gShipLegendLen = 12
gRotate = 350


gRangeTable = {
    "50 m":      (50,    0.12),
    "75 m":      (75,    0.18),  
    "100 m":     (100,   0.24),  
    "1/8 nm":    (231.5, 0.73),  
    "1/4 nm":    (463.0, 0.85),  
    "1/2 nm":    (926,   1.69),  
    "3/4 nm":    (1389,  1.69),  
    "1 nm":      (1852,  1.69),  
    "1.5 nm":    (2778,  2.44),  
    "2 nm":      (3704,  2.44),  
    "3 nm":      (5556,  7.93),  
    "4 nm":      (7408,  8.55),  
    "6 nm":      (11112, 8.55),  
    "8 nm":      (14816, 12.82), 
    "12 nm":     (22224, 12.82), 
    "16 nm":     (29632, 12.82), 
    "24 nm":     (44448, 12.82), 
    "32 nm":     (59264, 12.82) 
}

def PrintVal():
	print('gPI:',gPI)
	

if __name__ == '__main__':
	PrintVal()
