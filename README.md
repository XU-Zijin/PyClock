# PyClock
一个基于micropython的esp32项目

这是一个开源项目,原项目地址 https://github.com/01studio-lab/pyClock

我重写了这个开源项目的软件部分(不包括表盘、联网程序、获取天气以及固件)PS: 代码水平不高，有意见可以直接指出，有优化和bug的地方请指出

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
        |---set.txt: 系统状态文件(use for ui)
        |---state.txt: 系统状态记录

lib: 服务

    |---develop
        |---devmode.py: 开发者模式(还没开发完)
    |---service
        |---service.py:系统服务(core)
        |---led.py: 用于控制led灯
        |---system.py: 用于pyshell(待开发)

libs: 项目Micropython库

    urllib: urequest库
        |---parse.py
        |---urequest.py: 爬虫库
    |---ap.py: AP热点配网
    |---global_var.py：全局变量定义
    ui：UI主题库 
        |---dial.py: 极简表盘
        |---default.py: 默认表盘

其中service.py是相当于这个程序的核心，大部分功能从这里调用

`注：因为system.py和devmode.py文件里的功能尚未开发或未开发完，使用时可以删除，不影响现有功能及稳定性，dial.py也可以删除，这是个表盘，如果要用这个表盘我后面会讲如何更换表盘`

## 代码分析

### 结构分析

首先`data`文件夹用于存放主题图片、字库、编码以及系统运行时所需的文件。

`lib`文件夹中就是用于调试的`devmode.py`文件及用于系统大部分基础功能`service.py`文件，还有控制led的文件，最后还有一个是计划开发的`system.py`文件，我打算再这个开源硬件PyClock这个板子上实现一个终端功能，也就是pyshell。

而`libs`里面就是各种所需的库了，还有表盘，也就是UI。

### 功能介绍

这个天气时钟的主要功能：

* 查看天气
* 查看温湿度
* 查看时间
* 可以熄屏
* 开机自动校准时间（把原项目的获取时间优化了）
* 手机web配网

### service.py和led.py文件的调用说明

使用`from lib.service import led`从而调用led.py，使用`led.on()`即可开启板子上自带的led指示灯，使用`led.off()`即可关闭。

