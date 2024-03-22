'''
主文件
Powered By MicroPython
Version 6.3.3
By XZJ
'''
print('Powered By XZJ')
print('Version 6.3.3')
#导入相关模块
from libs.ui import default
from libs.ui import dial
from libs.ui import ticlock
#导入server
from lib.service.service import server
server.start_screen()
from lib.service import led
import time,os,machine,gc
machine.freq(160000000)
print("boot")
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
ui_count=3
#按键    
KEY=Pin(9,Pin.IN,Pin.PULL_UP) #构建KEY对象
#按键中断触发
def key(KEY):
    global sys,count,ui,ui_count
    time.sleep_ms(10) #消除抖动server.WIFI_Connect('p','p')
    if KEY.value() == 0: #确认按键被按下
        machine.freq(160000000)
        if sys == 1:
            ui+=1
            f = open('/data/file/set.txt','w',encoding = "utf-8")
            f.write("1")
            f.close()
            if ui>2:
                ui=0
        elif sys == 0:
            from lib.develop import devmode
            f = open('/data/file/set.txt','w',encoding = "utf-8")
            f.write("dev")
            f.close()
            mode.run()
        gc.collect()
        #长按
        start = time.ticks_ms()
        while KEY.value() == 0:
            if time.ticks_ms() - start >2000:
                if sys==1:
                    if count == 0:
                        server.screen_off()
                        f = open('/data/file/set.txt','w',encoding = "utf-8")
                        f.write('0')
                        f.close()
                        count += 1
                        machine.freq(80000000)
                        print('screen off')
                        server.screen_off()
                    elif count == 1:
                        machine.freq(160000000)
                        f = open('/data/file/set.txt','w',encoding = "utf-8")
                        f.write('1')
                        f.close()
                        count = 0
                        print('screen on')
            if time.ticks_ms() - start >5000: #长按按键5秒恢复出厂设置  
                led.on() #指示灯亮
                machine.freq(160000000)
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
                #machine.reset() #重启开发板
                import main #方便调试
KEY.irq(key,Pin.IRQ_FALLING) #定义中断，下降沿触发
################
#    主程序    #
################
#没有WiFi配置文件,出厂模式
while 'wifi.txt' not in os.listdir('/data/file/'):
    sys=2
    f = open('/data/file/mode.txt','w',encoding = "utf-8")
    f.write("ap")
    f.close()
    f = open('/data/file/set.txt','w',encoding = "utf-8")
    f.write("simple")
    f.close()
    ap.startAP() #启动AP配网模式
#启动看门狗，超时30秒。
#wdt = WDT(timeout=30000)
#连接WiFi
while not server.WIFI_Connect('p','p')==True: #等待wifi连接             
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
#weather=['\u591a\u4e91', '19', '27', '\u591a\u4e91', '58', '\u5317\u98ce', '1', '21.1', '98']
server.info_print()
server.check()
gc.collect()
sys=1
tick = 61 #每秒刷新标志位
if 'ui.txt' not in os.listdir('/data/file/'):
    f = open('/data/file/ui.txt','w',encoding = "utf-8")
    f.write('default')
    f.close()
    ui=0
f = open('/data/file/ui.txt','r',encoding = "utf-8")#读取上次关机时的表盘
k=f.read()
f.close()
if len(k)==0:
    ui=0
else:
    if k=='default':
        ui=0#默认表盘
    elif k=='dial':
        ui=1
    elif k=='ticlock':
        ui=2
f = open('/data/file/mode.txt','w',encoding = "utf-8")
f.write("run")
print("start")
if sys==1: 
    while True:
        #获取时间
        datetime = server.re('rtc')
        #15分钟在线获取一次天气信息,顺便检测wifi是否掉线
        if datetime[5]%15 == 0 and datetime[6] == 0:
            led.on()
            server.WIFI_Connect('p','p') #检查WiFi，掉线的话自动重连
            server.weather_get(datetime)
            weather=server.re('weather')
            #weather=['\u591a\u4e91', '19', '27', '\u591a\u4e91', '58', '\u5317\u98ce', '1', '21.1', '98']
            server.info_print()
            gc.collect()
            led.off()
        #每秒刷新一次UI
        if tick != datetime[6]:
            tick = datetime[6]
            #wdt.feed() #喂狗
            ntpst = server.re('ts')
            f = open('/data/file/set.txt','r',encoding = "utf-8")
            s = f.read()
            f.close()
            if s=='1' or s=='simple':
                if ui==0:
                    default.UI_Display(city,weather,datetime)
                    f = open('/data/file/ui.txt','w',encoding = "utf-8")#读取上次关机时的表盘
                    f.write('default')
                    f.close()
                elif ui==1:
                    dial.UI_Display(datetime) #极简表盘
                    f = open('/data/file/ui.txt','w',encoding = "utf-8")#读取上次关机时的表盘
                    f.write('dial')
                    f.close()
                elif ui==2:
                    ticlock.draw_clock(datetime)
                    f = open('/data/file/ui.txt','w',encoding = "utf-8")#读取上次关机时的表盘
                    f.write('ticlock')
                    f.close()
    #        print('gc2:',gc.mem_free()) #内存监测
            if ntpst==0:
                server.sync_ntp()
                datetime = server.re('rtc')