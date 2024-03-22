'''
主功能文件
Powered By MicroPython
Version 1.0.0
'''

from lib.service.service import server
from libs import ap,global_var
import gc,re,machine,socket,math,uctypes,time,uzlib,json,urandom
from lib.service import led
from machine import Pin,Timer