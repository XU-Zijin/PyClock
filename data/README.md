## 代码结构
boot.py ：启动参数配置，可以不用。
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
        |---ip.py: 根据IP地址自动获取天气

libs: 项目Micropython库
    urllib: urequest库
        |---urequest.py: 爬虫库
    
    |---ap.py: AP热点配网
    |---global_var.py：全局变量定义
    |---mode.py: 开发者模式程序
    
    ui：UI主题库 
        |---dial.py: 极简表盘
        |---default.py: 默认表盘
