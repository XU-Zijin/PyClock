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
		|---ui.txt: 记录上次关机表盘
		|---datetime.txt: 存储rtc时间
		|---weather.txt: 存储天气数据

lib: 服务

    |---develop
        |---devmode.py: 开发者模式(正在开发中)
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
        |---dial.py: 极简表盘
        |---default.py: 默认表盘
		|---ticlock.py: 极简时钟表盘

其中service.py是相当于这个程序的核心，大部分功能从这里调用

`注：因为devmode.py文件里的功能尚未开发完，使用时可以删除，不影响现有功能及稳定性`

## 代码分析

### 结构分析

首先`data`文件夹用于存放主题图片、字库、编码以及系统运行时所需的文件。

`lib`文件夹中就是用于调试的`devmode.py`文件及用于系统大部分基础功能`service.py`文件，还有控制led的文件，我打算用`devmode.py`这个文件在PyClock这个板子上实现一个终端功能，也就是pyshell。

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
* 离线使用（仅限天气，原理是把上次联网时获取的天气存储，离线时读取使用）

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

## 怎么使用

首次开机按照屏幕上显示的步骤进行配网，然后首次开机会进入到默认的太空人表盘，若不是首次开机，则会进入上次关机时的表盘，短按切换表盘，目前有两个表盘，按2秒息屏，长按5秒进入出厂设置。

## 版本说明

V2.3.1修复2个bug，添加串口输出内存剩余情况、CPU频率、WiFi信号强度、表盘使用情况等方便的调试功能

V2.3.0支持离线使用（原理是把上次联网时获取的天气和时间存储，离线时读取使用，所以数据并不准确，只是一个demo），把开机画面写入函数，只有调用时才显示开机画面；加快开机速度，提速10%，把开机画面提前；只导入需要的表盘，开机时不导入其他表盘，使用时再导入，增加开机速度；增加稳定性

V2.2.0修复1个已知bug，添加表盘记忆功能，新增1个表盘

V2.1.0修复已知的3个bug，添加新的表盘，删除不必要文件，在息屏超过15分钟时CPU频率为80MHz

V2.0.1添加自动调整esp32的CPU频率以节省功耗，在正常情况下CPU频率为160MHz，在息屏时为80MHz，在息屏超过15分钟时为20MHz

V2.0.0修改默认表盘，修改AP配网文件，可以自动检测城市，新增加两个功能：短按切换表盘、按两秒息屏

V1.0.0开源，重写主要代码（除表盘，AP配网）