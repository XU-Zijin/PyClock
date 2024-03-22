# PyClock
一个基于esp32的micropython项目

这是一个开源项目,原项目地址 https://github.com/01studio-lab/pyClock

我重写了这个开源项目的软件部分(不包括固件)PS: 代码水平不高，有意见可以直接指出，有优化和bug的地方请指出

## 代码结构
boot.py ：启动参数配置，可以不用

main.py：主函数代码

data: 数据

    |---Fonts : 字库文件
    |---picture：主题图片素材
    |---CityCode.txt：全国城市编码
    file: 用于存放系统文件
        |---wifi.txt: 记录WiFi账户密码
        |---mode.txt: 系统状态文件
        |---set.txt: 系统状态文件
		|---ui.txt: 记录上次关机时的表盘

lib: 服务

    |---service
        |---service.py:系统服务(core)
        |---led.py: 用于控制led灯
        |---ip.py: 自动获取城市

libs: 项目Micropython库

    urllib: urequest库
        |---urequest.py: 爬虫库
    |---ap.py: AP热点配网
    |---global_var.py：全局变量定义
    ui：UI主题库 
        |---default.py: 默认表盘
		|---dial.py: 极简表盘

其中service.py是相当于这个程序的核心，大部分功能从这里调用

## 代码分析

### 结构分析

首先`data`文件夹用于存放主题图片、字库、编码以及系统运行时所需的文件。

而`libs`里面就是各种所需的库了，还有表盘，也就是UI。

### 功能介绍

这个天气时钟的主要功能：

* 查看天气
* 查看温湿度
* 查看时间
* 可以息屏
* 可以切换表盘
* 开机自动校准时间
* 手机web配网
* 自动获取城市
* 表盘记忆

### service.py和led.py文件的调用说明

使用`from lib.service import led`从而调用led.py，使用`led.on()`即可开启板子上自带的led指示灯，使用`led.off()`即可关闭。

使用`from lib.service.service import server`导入server库

`server.WIFI_Connect()`用于联网      

`server.sync_ntp()`用于同步网络时钟

`server.city_get()`获取城市编码

`city=server.re('city')`返回城市编码

`datetime = server.re('rtc')`返回rtc时间

`server.weather_get(datetime)`获取天气

`weather=server.re('weather')`返回天气

`server.info_print()`打印天气到调试台

`server.check()`自检

注：main.py默认开启看门狗功能

## 如何使用

首次开机按照屏幕上显示的步骤进行配网，然后首次开机会进入到默认的太空人表盘，若不是首次开机，则会进入上次关机时的表盘，短按切换表盘，目前有两个表盘，按2秒息屏，长按5秒进入出厂设置。

## 版本说明

V2.1.0修复3个已知bug，修改dial表盘，添加表盘记忆功能，添加自动调节CPU频率功能，增加运行稳定性

V2.0.1删除掉一些调试代码

V2.0.0修改默认表盘，修改AP配网文件，可以自动检测城市，新增加两个功能：短按切换表盘、按两秒息屏

V1.0.0开源，重写主要代码（除表盘，AP配网）