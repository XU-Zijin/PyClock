'''
指示灯控制文件
Version 1.0.0
'''

from machine import Pin
def on():
    LED=Pin(2,Pin.OUT)
    LED.value(1)
def off():
    LED=Pin(2,Pin.OUT)
    LED.value(0)