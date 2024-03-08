'''
主功能文件
Version 3.2.0
'''
print("boot")
print('core 3.2.0')
#定义常用颜色
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW = (255,255,0)
DEEPGREEN = (1,179,105)
#导入相关模块
from tftlcd import LCD15
########################
# 构建1.5寸LCD对象并初始化
########################
d = LCD15(portrait=1)
d.fill(BLACK)
d.printStr('Powered by',60,185,color=WHITE,size=1)
d.printStr('Micropython',60,205,color=WHITE,size=2)
d.printStr('PyClock',60,85,color=WHITE,size=3)
from machine import RTC,Pin,Timer
import time,math,ntptime,network,re,json,machine,gc,os,tftlcd
from libs.urllib import urequest
from lib.service import led
os.uname()
led.on()
# 初始化 RTC
rtc = RTC()
city=['','']
weather = ['']*9
total = 0
lost = 0 
state=0#系统状态，0为boot,1为wifi,2为time,3为city，4为weather
weather_state=0#天气状态，连上为1反之为0
time_state=0#时间状态，连上为1反之为0
class server:
    datetime=rtc.datetime()
    def __init__(self,city):
        self.city=['','']
    #WIFI连接函数
    def WIFI_Connect(ssid,password):
        global state
        wlan = network.WLAN(network.STA_IF) #STA模式
        wlan.active(True)                   #激活接口
        start_time=time.time()              #记录时间做超时判断
        if ssid=='p' or password=='p':
            if not wlan.isconnected():
                print('Connecting to network...')
                f = open('/data/file/wifi.txt', 'r',encoding = "utf-8") #获取账号密码
                info = json.loads(f.read())
                f.close()
                print(info)
                try:
                    wlan.connect(info['SSID'], info['PASSWORD']) #WIFI账号密码
                    return True
                except:           
                    print('error')
                    led.on()
                    time.sleep_ms(300)
                    led.off()
                    time.sleep_ms(300)
                    #超时判断,15秒没连接成功判定为超时
                    if time.time()-start_time > 25:             
                        wlan.active(False)
                        #点亮led表示没连接上WiFi
                        led.on()
                        print('WIFI Connected Timeout!')
                        return False 
        else:
            try:
                wlan.connect(ssid, password) #WIFI账号密码
                return True
            except:           
                print('error')
                led.on()
                time.sleep_ms(300)
                led.off()
                time.sleep_ms(300)
                #超时判断,15秒没连接成功判定为超时
                if time.time()-start_time > 25:             
                    wlan.active(False)
                    #点亮led表示没连接上WiFi
                    led.on()
                    print('WIFI Connected Timeout!')
                    return False
        #连接成功，熄灭led
        led.off()
        #串口打印信息
        state+=1
        print('network information:', wlan.ifconfig())
        return True
    
    # 同步时间
    def sync_ntp():
        global state,time_state
        ntptime.NTP_DELTA = 3155644800   # 可选 UTC+8偏移时间（秒），不设置就是UTC0
        ntptime.host = 'ntp1.aliyun.com'  # 可选，ntp服务器，默认是"pool.ntp.org"
        print("ntptime.host = 'ntp1.aliyun.com'")
        try:
            ntptime.settime()   # 修改设备时间,到这就已经设置好了
            print('同步成功')
            print(rtc.datetime())
            print("同步后本地时间：%s" %str(time.localtime()))
            led.off()
            state+=1
            time_state=1
            return True
        except:
            for i in range(6):
                led.on()              #turn off 0是亮
                time.sleep(0.1)
                led.off()             
                time.sleep(0.1)
            print('同步失败')
            print(rtc.datetime())
            print("未同步网络时间","正在使用本地时间：%s" %str(time.localtime()))
            time_state=0
            return False
    #获取城市信息
    def city_get():
        global city,state
        #获取城市编码
        f = open('/data/file/wifi.txt', 'r',encoding = "utf-8") #获取账号密码
        info = json.loads(f.read())
        f.close()
        city[0] = info['CITY'] 
        #获取城市名称
        f = open('/data/CityCode.txt', 'r',encoding = "utf-8")
        num = 0
        while True:   
            text = f.readline()   
            if city[0] in text: 
                if city[0] == re.match(r'"(.+?)"',text).group(1): #城市名称完全一样
                    city[1] = re.match(r'"(.+?)"',text.split(': ')[1]).group(1) #"获取城市编码"
                    break 
            elif '}' in text: #结束，没这个城市。
                print('No City Name!')
                break  
            num = num + 1
            if num == 300:
                gc.collect() #内存回收
                num = 0  
        f.close()
        city_node = 0
        #city.txt文件存在,判断文件是否已经有当前城市字库
        if 'city.txt' in os.listdir('/data/'): 
            f = open('/data/city.txt', 'r',encoding = "utf-8")
            city_text = f.read()
            for i in range(len(city[0])):
                if city[0][i] in city_text:      
                    if i == len(city[0])-1: #全部字体都有         
                        city_node = 1 #标记字符信息正常
            f.close()
        #城市字库正常，无需制作
        if city_node == 1:
            pass       
        else: #获取字库文件并保存
            #生成城市字模文件
            city_font= {}   
            for i in range(len(city[0])): 
                f = open('/data/Fonts/fonts_city.py', 'r') 
                while True:    
                    text = f.readline()
                    if city[0][i] in text: 
                        while True:  
                            text = text + f.readline()
                            if ')' in text:
                                a = re.search('[(]' + '(.*?)' + '[)]',text).group(1).replace('\r\n','').replace(' ','').split(',')
                                for j in range(len(a)):
                                    a[j] = int(a[j])
                                city_font[city[0][i]] = a
                                break
                        break
                    if not text: #读完
                        print("No City Fonts.")
                        break
                f.close()
            f = open('/data/city.txt', 'w',encoding = "utf-8") #以写的方式打开一个文件，没有该文件就自动新建
            f.write((json.dumps(city_font))) #写入数据
            f.close() #每次操作完记得关闭文件
            gc.collect() #内存回收
            state+=1
            return True
        
    #网页获取天气数据
    def weather_get(datetime):
        global weather,lost,total,city,state,weather_state
        for i in range(1):#失败会重试(为满足main.py中的代码，把5次改成1次）
            try:      
                myURL = urequest.urlopen("http://www.weather.com.cn/weather1d/"+city[1]+".shtml")
                text = myURL.read(39000+100*i).decode('utf-8') #抓取约前4W个字符，节省内存
                #获取当日天气、高低温
                text1=re.search('id="hidden_title" value="' + '(.*?)' + '°C',text).group(1)
                weather[0] = text1.split()[2] #当日天气
                weather[1] = str(min(list(map(int,text1.split()[3].split('/'))))) #当天最低温
                weather[2] = str(max(list(map(int,text1.split()[3].split('/'))))) #当天最高温
                #获取实时天气
                text2 = json.loads(re.search('var hour3data=' + '(.*?)' + '</script>',text).group(1))
                for i in range(len(text2['1d'])): 
                    if int(text2['1d'][i].split(',')[0].split('日')[0]) == datetime[2]:#日期相同
                        if datetime[4] <= int(text2['1d'][i].split(',')[0].split('日')[1].split('时')[0]): #小时
                            if i == 0 or datetime[4] == int(text2['1d'][i].split(',')[0].split('日')[1].split('时')[0]):
                                weather[3] = text2['1d'][i].split(',')[2] #实时天气
                            else:
                                weather[3] = text2['1d'][i-1].split(',')[2] #实时天气
                            break
                #获取实时空气质量、风向风力、温湿度
                text3 = json.loads(re.search('var observe24h_data = ' + '(.*?)' + ';',text).group(1))
                for i in range(len(text3['od']['od2'])):
                    weather[4] = text3['od']['od2'][i]['od28'] #空气质量
                    if weather[4] != '':
                        break
                for i in range(len(text3['od']['od2'])):
                    weather[5] = text3['od']['od2'][i]['od24'] #实时风向
                    if weather[5] != '':
                        break
                if '风' in weather[5]:#获取的是风向
                    pass
                else: #获取失败，从另外一个地方获取
                    text2 = json.loads(re.search('var hour3data=' + '(.*?)' + '</script>',text).group(1))
                    for i in range(len(text2['1d'])):
                        if int(text2['1d'][i].split(',')[0].split('日')[0]) == datetime[2]:#日期相同
                            if datetime[4] <= int(text2['1d'][i].split(',')[0].split('日')[1].split('时')[0]): #小时
                                if i == 0 or datetime[4] == int(text2['1d'][i].split(',')[0].split('日')[1].split('时')[0]):
                                    weather[5] = text2['1d'][i].split(',')[4] #实时风向
                                else:
                                    weather[5] = text2['1d'][i-1].split(',')[4] #实时风向
                                break
                for i in range(len(text3['od']['od2'])):
                    weather[6] = text3['od']['od2'][i]['od25'] #实时风力级数
                    if weather[6] != '':
                        break
                for i in range(len(text3['od']['od2'])):
                    weather[8] = text3['od']['od2'][i]['od27'] #相对湿度
                    if weather[8] != '':
                        break
                for i in range(len(text3['od']['od2'])):
                    weather[7] = text3['od']['od2'][i]['od22'] #温度
                    if weather[7] != '':
                        break 
                total = total+1
                weather_state=1
                return None
            except:
                print("Can not get weather!",i)
                lost = lost + 1
                weather_state=0
                gc.collect() #内存回收
            state+=1
            time.sleep_ms(1000)
    
    def re(server):
        global city,weather,weather_state,time_state,state
        datetime = rtc.datetime()
        if server=='city':
            return city
        elif server=='weather':
            return weather
        elif server=='wst':
            return weather_state
        elif server=='rtc':
            return datetime
        elif server=='ts':
            return time_state
        elif server=='state':
            return state
        else:
            return False
    
    def screen():
        tftlcd.LCD15(portrait=1)
        print('screen off')
        time.sleep(0.1)
        d.fill(BLACK)
        tftlcd.LCD15(portrait=1)
    
    def check():
        global state
        if state==4:
            f = open('/data/file/mode.txt','w',encoding = "utf-8")
            f.write("run")
            f.close()
            
    def info_print():
        global city,weather
        print(rtc.datetime())
        print('城市:',city[0],city[1])
        print('当日天气:',weather[0])
        print('当日最低温:',weather[1])
        print('当日最高温:',weather[2])
        print('实时天气:',weather[3])
        print('实时空气质量:',weather[4])
        print('实时风向:',weather[5])
        print('实时风力级数:',weather[6])
        print('实时温度:',weather[7])
        print('实时湿度:',weather[8])
        print('total:',total)
        print('lost:',lost)
        