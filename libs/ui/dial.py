'''
版本：v2.0
日期：2024.3
'''

#导入相关模块
import time, math
from libs import global_var
from lib.service.service import server
# 构建1.5寸LCD对象并初始化
d = global_var.LCD
# 定义常用颜色
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
def background():
    # 绘制表盘外圆蓝色边框
    d.drawCircle(120, 120, 120, BLUE, border=5)
    
    # 绘制时钟的刻度
    for i in range(12):
        # 每一个小时的角度
        angle = math.radians(i * 30)
        
        # 刻度的起始和结束位置
        inner_x = 120 + int(105 * math.sin(angle))
        inner_y = 120 - int(105 * math.cos(angle))
        outer_x = 120 + int(115 * math.sin(angle))
        outer_y = 120 - int(115 * math.cos(angle))
        
        # 绘制刻度线
        d.drawLine(outer_x, outer_y, inner_x, inner_y, WHITE)

# 绘制指针
def draw_hand(time_value, length, time_scale, color):
    angle = math.radians(time_value * time_scale)
    end_x = 120 + int(length * math.sin(angle))
    end_y = 120 - int(length * math.cos(angle))
    d.drawLine(120, 120, end_x, end_y, color)

# 清除指针，用于秒针和分针的连续移动
def clear_hand(time_value, length, time_scale, color):
    angle = math.radians(time_value * time_scale)
    end_x = 120 + int(length * math.sin(angle))
    end_y = 120 - int(length * math.cos(angle))
    d.drawLine(120, 120, end_x, end_y, color)

def datetime_display(datetime):
    # 获取时、分、秒
    second = datetime[6]
    minute = datetime[5]
    hour = datetime[4] % 12 # 12小时制
    
    # 绘制时针
    clear_hand((hour * 5 + minute // 12) - 1, 70, 30, BLACK)
    draw_hand((hour * 5 + minute // 12), 70, 30, RED)
    # 绘制分针
    clear_hand(minute - 1, 85, 6, BLACK)
    draw_hand(minute, 85, 6, GREEN)
    # 绘制秒针
    clear_hand(second - 1, 100, 6, BLACK)
    draw_hand(second, 100, 6, WHITE)
    d.drawCircle(120, 120, 3, WHITE, border=10)
    time.sleep(0.1)

def UI_Display(datetime):
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