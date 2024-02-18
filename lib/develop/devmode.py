'''
开发者模式配置文件
Powered By MicroPython
Version 1.1.14
By XZJ
'''

#导入相关模块
from libs import global_var
d = global_var.LCD
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW = (255,255,0)
DEEPGREEN = (1,179,105)
import time,os,machine,gc
from machine import Pin
f = open('/data/file/mode.txt','w',encoding = "utf-8")
f.write("boot")
f.close()
f = open('/data/file/set.txt','w',encoding = "utf-8")
f.write("dev")
f.close()
sys=0#系统状态，0为boot，1为run
#按键    
KEY=Pin(9,Pin.IN,Pin.PULL_UP) #构建KEY对象 
#按键中断触发
def key(KEY):
    time.sleep_ms(10) #消除抖动
    if KEY.value() == 0: #确认按键被按下 
        gc.collect()
        #长按
        start = time.ticks_ms()
        while KEY.value() == 0:
            if time.ticks_ms() - start >3000: #长按按键3秒
                pass
KEY.irq(key,Pin.IRQ_FALLING) #定义中断，下降沿触发
################
#    主程序    #
################
sys=1
print('start')
d.fill(BLACK)
d.printStr('Login:',0,0,color=WHITE,size=2)
print('Login:')
user_name='root'
user_login=input()
d.printStr(user_login,75,0,color=GREEN,size=2)
passward='123'
d.printStr('Passward:',0,25,color=WHITE,size=2)
print('Passward:')
user_passward=input()
if user_passward==passward and user_login==user_name:
    print('welcome!')
    d.fill(BLACK)
    d.printStr('>>> ',0,0,color=GREEN,size=2)
    print('Type "help()" for more information.')
    
else:
    count=1
    while True:
        d.printStr('passward wrong',0,50,color=RED,size=2)
        print("passward wrong")
        d.printStr('Passward:',0,25,color=WHITE,size=2)
        print('Passward:')
        user_passward=input()
        if user_passward==passward and user_login==user_name:
            break
        else:
            count+=1
    print('welcome!')
    d.fill(BLACK)
    d.printStr('>>> ',0,0,color=GREEN,size=2)
    print('Type "help()" for more information.')
    
