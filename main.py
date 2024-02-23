'''
主文件
Powered By MicroPython
Version 6.1.8
By XZJ
'''
print('Powered By XZJ')
print('Version 6.1.8')
#导入相关模块
from libs.ui import default
#from libs.ui import dial
#导入server
from lib.service.service import server
from lib.service import led
import time,os,machine,gc
f = open('/data/file/mode.txt','w',encoding = "utf-8")
f.write("boot")
f.close()

f = open('/data/file/set.txt','w',encoding = "utf-8")
f.write("simple")
f.close()

from libs import ap
from machine import Pin,WDT,Timer
sys=0#系统状态，0为boot，1为run
count=0
c=0
button_pressed_time = None  # 记录上一次按键时间
# 定义多次点击的间隔阈值（毫秒）
mct = 500  
# 定义一个定时器，在没有按键活动时重置计数器
timer=Timer(-1)  
#按键    
KEY=Pin(9,Pin.IN,Pin.PULL_UP) #构建KEY对象
#按键中断触发
def key(KEY):
    global sys,count,button_pressed_time,c
    current_time = time.ticks_ms()
    time.sleep_ms(10) #消除抖动
    if KEY.value() == 0: #确认按键被按下
        if button_pressed_time is None or time.ticks_diff(current_time, button_pressed_time) > mct:
            c = 1
            button_pressed_time = current_time
            # 重置定时器，指定时间后如果没有新的按键动作则重置计数器
            timer.init(mode=Timer.ONE_SHOT, period=mct, callback=lambda t:reset_count())
            if sys == 1:
                if count == 0:
                    server.screen()
                    f = open('/data/file/set.txt','w',encoding = "utf-8")
                    f.write('0')
                    f.close()
                    count += 1
                elif count == 1:
                    f = open('/data/file/set.txt','w',encoding = "utf-8")
                    f.write('1')
                    f.close()
                    count = 0
                    print('screen on')
            elif sys == 0:
                from lib.develop import devmode
                f = open('/data/file/set.txt','w',encoding = "utf-8")
                f.write("dev")
                f.close()
                mode.run()
            gc.collect()
        elif time.ticks_diff(current_time, button_pressed_time) < mct:
            c+=1
            button_pressed_time = current_time
            print('yes')
            
        #print('Button pressed count:', count)
        #长按
        start = time.ticks_ms()
        while KEY.value() == 0:
            if time.ticks_ms() - start >5000: #长按按键5秒   
                led.on() #指示灯亮
                print("Factory Mode!")
                cwu = 0
                try:
                    os.remove('/data/file/wifi.txt')
                    os.remove('/data/file/mode.txt')
                    os.remove('/data/file/set.txt')
                    os.remove('/data/city.txt')
                    print('Remove wifi.txt')
                    print('Remove mode.txt')
                    print('Remove set.txt')
                    print('Remove city.txt')
                except:
                    print('no wifi.txt')
                print('Rebooting!')
                machine.reset() #重启开发板
# 配置按钮的中断，下降沿触发
KEY.irq(key, Pin.IRQ_FALLING)
def reset_count():
    global c
    c=0
################
#    主程序    #
################
#没有WiFi配置文件,出厂模式
while 'wifi.txt' not in os.listdir('/data/file/'):
    os.remove('/data/file/mode.txt')
    os.remove('/data/file/set.txt')
    ap.startAP() #启动AP配网模式
    f = open('/data/file/mode.txt','w',encoding = "utf-8")
    f.write("boot")
    f.close()
    f = open('/data/file/set.txt','w',encoding = "utf-8")
    f.write("simple")
    f.close()
#启动看门狗，超时30秒。
#wdt = WDT(timeout=30000)
#连接WiFi
while not server.WIFI_Connect()==True: #等待wifi连接             
    pass
#wdt.feed() #喂狗
#同步网络时钟
server.sync_ntp()
#获取城市名称和编码
server.city_get()
city=server.re('city')
datetime = server.re('rtc')
server.weather_get(datetime)
weather=server.re('weather')
server.info_print()
server.check()
gc.collect()
sys=1
tick = 61 #每秒刷新标志位
print("start")
if sys==1: 
    while True:
        #获取时间
        datetime = server.re('rtc')
        #15分钟在线获取一次天气信息,顺便检测wifi是否掉线
        if datetime[5]%15 == 0 and datetime[6] == 0:
            led.on()
            server.WIFI_Connect() #检查WiFi，掉线的话自动重连
            server.weather_get(datetime)
            weather=server.re('weather')
            server.info_print()
            gc.collect()
            led.off()
        #每秒刷新一次UI
        if tick != datetime[6]:
            tick = datetime[6]
            #wdt.feed() #喂狗
            #wst = server.re('wst')
            ntpst = server.re('ts')
            f = open('/data/file/set.txt','r',encoding = "utf-8")
            s = f.read()
            f.close()
            if s=='1' or s=='simple':
                #dial.UI_Display(datetime) #极简表盘
                default.UI_Display(city,weather,datetime)
    #        print('gc2:',gc.mem_free()) #内存监测
            #if wst==0:
                #server.weather_get(datetime)
                #weather=server.re('weather')
            if ntpst==0:
                server.sync_ntp()
                datetime = server.re('rtc')
        time.sleep_ms(200) 
