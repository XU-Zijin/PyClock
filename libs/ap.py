#AP配网
from lib.service.service import server
from lib.service import ip
from libs import global_var
import os,json,gc,re
from machine import Pin

import network
import socket
import ure
import time

########################
# 构建1.5寸LCD对象并初始化
########################
d = global_var.LCD

#定义常用颜色
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW = (255,255,0)
DEEPGREEN = (1,179,105)

wlan_ap = network.WLAN(network.AP_IF)
wlan_sta = network.WLAN(network.STA_IF)

server_socket = None

def send_header(conn, status_code=200, content_length=None ):
    conn.sendall("HTTP/1.0 {} OK\r\n".format(status_code))
    conn.sendall("Content-Type: text/html\r\n")
    if content_length is not None:
      conn.sendall("Content-Length: {}\r\n".format(content_length))
    conn.sendall("\r\n")

def send_response(conn, payload, status_code=200):
    content_length = len(payload)
    send_header(conn, status_code, content_length)
    if content_length > 0:
        conn.sendall(payload)
    conn.close()

#WiFi配置页面
def config_page():
    return b"""
<!DOCTYPE html>
<html>
<head>
  <title>PyClock WiFi 配置</title>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {
      background-color: #303030;
      color: #fff;
      font-family: Arial, sans-serif;
      text-align: center;
    }

    .wrapper {
      margin: auto;
      max-width: 500px;
      padding: 20px;
      border-radius: 5px;
    }

    h1 {
      margin-bottom: 2rem;
    }

    label,
    input,
    button {
      display: block;
      width: calc(100% - 20px);
      margin-bottom: 1rem;
      padding: 10px;
    }

    input,
    button {
      background: #424242;
      border: 1px solid #576574;
      border-radius: 5px;
      color: #fff;
    }

    button {
      cursor: pointer;
      background-color: #1fa3ec;
    }

    button:disabled {
      opacity: 0.5;
    }
  </style>
</head>
<body>
  <div class="wrapper">
    <h1>PyClock WiFi配置</h1>
    <form action="configure" method="post">
      <div>
        <label for="ssid">WiFi账号：</label>
        <input type="text" id="ssid" name="ssid" />
      </div>
      <div>
        <label for="password">WiFi密码：</label>
        <input type="password" id="password" name="password" />
      </div>
      <button type="submit">连接</button>
    </form>
  </div>
</body>
</html>"""

def connect_sucess(new_ip):
    return b"""
<!DOCTYPE html>
<html>
<head>
  <title>连接成功!</title>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {
      margin: 0;
      padding: 0;
      background-color: #303030;
      color: #fff;
      font-family: Arial, sans-serif;
      text-align: center;
      display: flex;
      flex-direction: column;
      justify-content: center;
      min-height: 100vh;
    }

    p {
      margin: 15px 0;
    }

    a {
      display: inline-block;
      margin: 15px;
      padding: 15px 25px;
      background-color: #1fa3ec;
      color: #fff;
      border-radius: 5px;
      text-decoration: none;
      transition: background 0.2s ease-in-out;
    }

    a:hover,
    a:focus {
      background-color: #0e7ac4;
    }

    /* 媒体查询，针对不同尺寸的设备进行样式调整 */
    @media (max-width: 600px) {
      a {
        padding: 10px 20px;
      }
    }

    @media (max-width: 400px) {
      a {
        padding: 8px 15px;
        font-size: 0.9em;
      }
    }
  </style>
</head>
<body>
  <div>
    <p>WiFi连接成功</p>
    <p>IP地址：%s</p> <!-- 后端代码替换 %s -->
    <a href="http://%s">首页</a> <!-- 后端代码替换 %s -->
    <a href="/disconnect">断开连接</a>
  </div>
</body>
</html>""" % (new_ip, new_ip)

#中文转字节字符串
_hextobyte_cache = None

def unquote(string):
    """unquote('abc%20def') -> b'abc def'."""
    global _hextobyte_cache

    # Note: strings are encoded as UTF-8. This is only an issue if it contains
    # unescaped non-ASCII characters, which URIs should not.
    if not string:
        return b''

    if isinstance(string, str):
        string = string.encode('utf-8')

    bits = string.split(b'%')
    if len(bits) == 1:
        return string

    res = [bits[0]]
    append = res.append

    # Build cache for hex to char mapping on-the-fly only for codes
    # that are actually used
    if _hextobyte_cache is None:
        _hextobyte_cache = {}

    for item in bits[1:]:
        try:
            code = item[:2]
            char = _hextobyte_cache.get(code)
            if char is None:
                char = _hextobyte_cache[code] = bytes([int(code, 16)])
            append(char)
            append(item[2:])
        except KeyError:
            append(b'%')
            append(item)

    return b''.join(res)

#从配置网页获取WiFi账号密码
def get_wifi_conf(request):
    match = ure.search("ssid=([^&]*)&password=(.*)", request)
    if match is None:
        return None

    try:
        ssid = match.group(1).decode("utf-8").replace("%3F", "?").replace("%21", "!")
        password = match.group(2).decode("utf-8").replace("%3F", "?").replace("%21", "!")
    except Exception:
        ssid = match.group(1).replace("%3F", "?").replace("%21", "!")
        password = match.group(2).replace("%3F", "?").replace("%21", "!")
        
    if len(ssid) == 0: #wifi名称为空。
        return None
    return (ssid.replace('+',' '), password)

def check_wlan_connected():
    if wlan_sta.isconnected():
        return True
    else:
        return False

def read_profiles():
    with open(NETWORK_PROFILES) as f:
        lines = f.readlines()
    profiles = {}
    for line in lines:
        ssid, password = line.strip("\n").split(";")
        profiles[ssid] = password
    return profiles


def write_profiles(profiles):
    lines = []
    for ssid, password in profiles.items():
        lines.append("%s;%s\n" % (ssid, password))
    with open(NETWORK_PROFILES, "w") as f:
        f.write(''.join(lines))

#停止Socket服务
def stop():
    global server_socket

    if server_socket:
        server_socket.close()
        server_socket = None
        
    
def startAP():
    
    global server_socket
    
    stop() #停止Socket服务
    
    print('Connect pyClock AP to Config WiFi.')

    #启动热点，名称问pyClock，不加密。
    wlan_ap.active(True)
    wlan_ap.config(essid='pyClock',authmode=0)

    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 80))
    server_socket.listen(10)

    d.Picture(0,0,"/data/picture/Step1.jpg") #步骤1，连接AP热点。

    while not wlan_ap.isconnected(): #等待AP接入
        
        pass
    
    d.Picture(0,0,"/data/picture/Step2.jpg") #步骤2，登录192.168.4.1进行配网。
 
    while not wlan_sta.isconnected(): #开发板没连上路由器
        
        #等待配网设备接入
        conn, addr = server_socket.accept()
        print('Connection: %s ' % str(addr))

        try:
            conn.settimeout(3)
            request = b""

            try:
                while "\r\n\r\n" not in request:
                    request += conn.recv(2048) #增大适配多种浏览器
                
                print(request)
                    
                # url process
                try:
                    url = ure.search("(?:GET|POST) /(.*?)(?:\\?.*?)? HTTP", request).group(1).decode("utf-8").rstrip("/")
                except Exception:
                    url = ure.search("(?:GET|POST) /(.*?)(?:\\?.*?)? HTTP", request).group(1).rstrip("/")
                    pass
                
                print("URL is {}".format(url))

                #收到内容为空时，发送配置页面。
                if url == "": 
                    print("send config web!")
                    response = config_page()
                    send_response(conn, response)              
                    
                elif url == "configure":
                    #获取配置信息，SSID,PASSWORD
                    ret = get_wifi_conf(request)
                    print(ret)
                    if ret != None: #获取信息成功   
                        #SSID带中文和特殊字符处理
                        if '%' in ret[0]:
                            print('wifi chinese')
                            SSID = unquote(ret[0]).decode("gbk")
                        else:
                            SSID = ret[0]
                            
                        #PASSWORD带中文和特殊字符处理
                        if '%' in ret[1]:
                            print('wifi chinese')
                            PASSWORD = unquote(ret[1]).decode("gbk")
                        else:
                            PASSWORD = ret[1]
                            
                        d.fill(BLACK)
                        d.printStr('Connecting...', 10, 50, RED, size=2)
                        d.printStr(SSID, 10, 110, WHITE, size=2)
                        #print(ret_ip)
                        while not server.WIFI_Connect(SSID,PASSWORD)==True: #等待wifi连接             
                            pass
                        try:
                            CITY = ip.get_ip_info()
                            #保存WiFi信息到/data/file/wifi.txt,字典格式。
                            wifi_info = {'SSID':'','PASSWORD':''}
                            wifi_info['SSID'] = SSID
                            wifi_info['PASSWORD'] = PASSWORD
                            wifi_info['CITY'] = CITY
                            print(wifi_info)
                            f = open('/data/file/wifi.txt', 'w') #以写的方式打开一个文件，没有该文件就自动新建
                            f.write(json.dumps(wifi_info)) #写入数据
                            f.close() #每次操作完记得关闭文件    
                            response = web_page()
                            send_response(conn, response)  
                        except:#连接失败
                            response = config_page()
                            send_response(conn, response)
                            d.Picture(0,0,"/data/picture/error2.jpg") #步骤2，登录192.168.4.1进行配网
                            
                    else : #获取信息不成功
                        response = config_page()
                        send_response(conn, response)
                        d.Picture(0,0,"/data/picture/error3.jpg") #步骤2，登录192.168.4.1进行配网
                    
                elif url == "disconnect":
                    wlan_sta.disconnect()

            except OSError:
                pass

        finally:
            conn.close()
    wlan_ap.active(False)
    stop()
    print('ap exit')
