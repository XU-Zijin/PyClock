import time, math
from libs import global_var
# 构建1.5寸LCD对象并初始化
d = global_var.LCD
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
DEEPGREEN = (1, 179, 105)
YOU = (156,202,127)
LIANG = (249,218,101) 
QINGDU = (242,159,57)
ZHONGDU = (219,85,94)
ZDU = (186,55,121)
YANZHONG = (136,11,32)
# 屏幕中央坐标
center_x = 120
center_y = 120
# 表盘半径
radius = 120
def background():
    # 绘制表盘外圆蓝色边框
    d.drawCircle(120, 120, 120, DEEPGREEN, border=5)
    # 绘制时钟的刻度
    for i in range(12):
        angle = math.radians(i * 30)
        mark_length = 10 if i % 3 else 15  # 每三个小时一个较长的标记
        mark_width = 4 if i % 3 else 2
        inner_x = center_x + (radius - mark_length) * math.sin(angle)
        inner_y = center_y - (radius - mark_length) * math.cos(angle)
        outer_x = center_x + radius * math.sin(angle)
        outer_y = center_y - radius * math.cos(angle)
        d.drawLine(int(inner_x), int(inner_y), int(outer_x), int(outer_y), WHITE)

def datetime_display(datetime):
    second = datetime[6]
    minute = datetime[5]
    hour = datetime[4]
    # 显示时间文字
    time_str = "{:02d}:{:02d}".format(hour, minute, second)
    d.printStr(time_str, center_x - 30, center_y + 50, WHITE, size=2)
    #秒钟处理
    #清除上一帧
    x0 = 120+round(100*math.sin(math.radians(second*6-6)))
    y0 = 120-round(100*math.cos(math.radians(second*6-6)))
    d.drawLine(x0, y0, 120, 120, BLACK)
    #显示
    x1 = 120+round(100*math.sin(math.radians(second*6)))
    y1 = 120-round(100*math.cos(math.radians(second*6)))
    d.drawLine(x1, y1, 120, 120, ZHONGDU)
    #分钟处理
    #清除上一帧
    x0 = 120+round(85*math.sin(math.radians(minute*6-6)))
    y0 = 120-round(85*math.cos(math.radians(minute*6-6)))
    d.drawLine(x0, y0, 120, 120, BLACK)
    #显示
    x1 = 120+round(85*math.sin(math.radians(minute*6)))
    y1 = 120-round(85*math.cos(math.radians(minute*6)))
    d.drawLine(x1, y1, 120, 120, GREEN)  
    #时钟处理
    #清除上一帧
    x0 = 120+round(75*math.sin(math.radians(hour*30+int(minute/12)*6-6)))
    y0 = 120-round(75*math.cos(math.radians(hour*30+int(minute/12)*6-6)))
    d.drawLine(x0, y0, 120, 120, BLACK)
    #显示
    x1 = 120+round(75*math.sin(math.radians(hour*30+int(minute/12)*6)))
    y1 = 120-round(75*math.cos(math.radians(hour*30+int(minute/12)*6)))
    d.drawLine(x1, y1, 120, 120, QINGDU)
    d.drawCircle(120, 120, 4, YELLOW, border=10)
def draw_clock(datetime):
    if global_var.UI_Change: #首次画表盘
        global_var.UI_Change = 0        
        d.fill(BLACK) #清屏
        background()
    f = open('/data/file/set.txt','r',encoding = "utf-8")
    s = f.read()
    f.close()
    if s=='1':
        global_var.UI_Change = 0        
        d.fill(BLACK) #清屏
        background()
        f = open('/data/file/set.txt','w',encoding = "utf-8")
        f.write("simple")
        f.close()
    datetime_display(datetime)
    
#draw_clock(datetime)
