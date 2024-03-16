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
d.fill(BLACK)
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
# 画表盘的函数
def draw_clock():
    if global_var.UI_Change: #首次画表盘
        global_var.UI_Change = 0        
        d.fill(BLACK) #清屏
        d.drawCircle(center_x, center_y, radius, DEEPGREEN, border=5)
        # 绘制时刻标记（每小时一个标记）
        for i in range(12):
            angle = math.radians(i * 30)
            mark_length = 10 if i % 3 else 15  # 每三个小时一个较长的标记
            mark_width = 4 if i % 3 else 2
            inner_x = center_x + (radius - mark_length) * math.sin(angle)
            inner_y = center_y - (radius - mark_length) * math.cos(angle)
            outer_x = center_x + radius * math.sin(angle)
            outer_y = center_y - radius * math.cos(angle)
            d.drawLine(int(inner_x), int(inner_y), int(outer_x), int(outer_y), WHITE)
        # 画表盘中心圆
        d.drawCircle(center_x, center_y, 4, YELLOW, border=10)
    f = open('/data/file/set.txt','r',encoding = "utf-8")
    s = f.read()
    f.close()
    if s=='1':
        global_var.UI_Change = 0        
        d.fill(BLACK) #清屏
        d.drawCircle(center_x, center_y, radius, DEEPGREEN, border=5)
        # 绘制时刻标记（每小时一个标记）
        for i in range(12):
            angle = math.radians(i * 30)
            mark_length = 10 if i % 3 else 15  # 每三个小时一个较长的标记
            mark_width = 4 if i % 3 else 2
            inner_x = center_x + (radius - mark_length) * math.sin(angle)
            inner_y = center_y - (radius - mark_length) * math.cos(angle)
            outer_x = center_x + radius * math.sin(angle)
            outer_y = center_y - radius * math.cos(angle)
            d.drawLine(int(inner_x), int(inner_y), int(outer_x), int(outer_y), WHITE)
        # 画表盘中心圆
        d.drawCircle(center_x, center_y, 4, YELLOW, border=10)
        f = open('/data/file/set.txt','w',encoding = "utf-8")
        f.write("simple")
        f.close()
    # 获取当前时间
    local_time = time.localtime()
    hour, minute, second = local_time[3], local_time[4], local_time[5]
    # 确保小时在12小时制范围内
    hours = hour % 12
    # 绘制时针
    clear_hand((hours * 5 + minute // 12) - 1, 70, 30, BLACK)
    draw_hand((hours * 5 + minute // 12), 70, 30, QINGDU)
    # 绘制分针
    clear_hand(minute - 1, 85, 6, BLACK)
    draw_hand(minute, 85, 6, GREEN)
    # 绘制秒针
    clear_hand(second - 1, 100, 6, BLACK)
    draw_hand(second, 100, 6, ZHONGDU)
    # 显示时间文字
    time_str = "{:02d}:{:02d}".format(hour, minute, second)
    d.printStr(time_str, center_x - 30, center_y + 50, WHITE, size=2)

#draw_clock()

