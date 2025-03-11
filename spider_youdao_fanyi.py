# coding:utf8
import random
import time
from hashlib import md5
import requests


class YoudaoSpider(object):
    def __init__(self):
        # url一定要写抓包时抓到的POST请求的提交地址，但是还需要去掉 url中的“_o”，
        # “_o”这是一种url反爬策略，做了页面跳转，若直接访问会返回{"errorCode":50}
        self.url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        }

    # 获取lts时间戳,salt加密盐,sign加密签名
    def get_lts_salt_sign(self, word):
        lts = str(int(time.time() * 1000))
        salt = lts + str(random.randint(0, 9))
        string = "fanyideskweb" + word + salt + "Tbh5E8=q6U3EXe+&L[4c@"
        s = md5()
        s.update(string.encode())
        sign = s.hexdigest()
        print(lts, salt, sign)
        return lts, salt, sign

    def attack_yd(self, word):
        lts, salt, sign = self.get_lts_salt_sign(word)

        # 构建form表单数据
        data = {
            "i": word,
            "from": "AUTO",
            "to": "AUTO",
            "smartresult": "dict",
            "client": "fanyideskweb",
            "salt": salt,
            "sign": sign,
            "lts": lts,
            "bv": "cda1e53e0c0eb8dd4002cefc117fa588",
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_REALTlME",
        }
        # 使用 reqeusts.post()方法提交请求
        res = requests.post(
            url=self.url,
            data=data,
            headers=self.headers,
        )
        # res.json() 将json格式的字符串转为python数据类型
        # 客户端与服务器数据交互以json字符串传递，因此需要将它转换为python数据类型
        html = res.json()
        print(html)
        # 查看响应结果response  html:{"translateResult":[[{"tgt":"hello","src":"你好"}]],"errorCode":0,"type":"zh-CHS2en"}
        result = html["translateResult"][0][0]["tgt"]
        print("翻译结果:", result)

    def run(self):
        try:
            word = input("请输入要翻译的单词：")
            self.attack_yd(word)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    spider = YoudaoSpider()
    spider.run()
