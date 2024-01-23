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
        |---devmode.py: 开发者模式
    |---service
        |---service:系统服务文件(core)
        |---led.py: 用于控制led灯
        |---system: 用于pyshell

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