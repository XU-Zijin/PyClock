from libs.urllib import urequest
import ujson

def get_ip_info():
    # IP定位服务提供商的URL
    url = 'http://ip-api.com/json/?lang=zh-CN'
    # 发送请求并获取响应对象
    response = urequest.urlopen(url)
    # 读取响应的内容
    response_content = response.read()
    # 转换JSON字符串为Python字典
    ip_info = ujson.loads(response_content)
    city = ip_info.get('city', '').replace('市', '')
    print('您所在的城市是：', city)
    response.close()
    return city

# 调用函数，输出IP信息
#get_ip_info()