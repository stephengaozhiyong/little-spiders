from urllib import request
from tools import save_html, headers
import requests
from urllib import request

url = "http://httpbin.org/get"  # 向测试网站发送请求

req = request.Request(url=url, headers=headers)
# 2、发送请求，获取响应对象
res = request.urlopen(req)
# 3、提取响应内容
html = res.read().decode("utf-8")
print(html)
