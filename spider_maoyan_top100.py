import re
import time
import random
import csv
from spider import SpiderBase
from tools import get_headers
from loguru import logger
from lxml import etree


# 定义一个爬虫类
class MaoyanSpider(SpiderBase):
    # 初始化
    # 定义初始页面url
    def __init__(self):
        self.base = "https://www.maoyan.com/board/4"

    # def get(self, params):
    #     req = requests.Request("GET", self.base, headers=headers, params=params)
    #     r = req.prepare()
    #     print("start scraping...:", r.url)
    #     sess = requests.Session()
    #     rsp = sess.send(r, allow_redirects=False)
    #     if rsp.status_code != 200:
    #         print("req.url:", req.url)
    #         print("res.request.url:", rsp.request.url)
    #         raise RuntimeError(f"{rsp.ok}, {rsp.status_code}, {rsp.content}")
    #     return rsp

    # 解析函数
    def parse_html(self, html):
        # 正则表达式
        re_bds = '<div class="movie-item-info">.*?title="(.*?)".*?<p class="star">(.*?)</p>.*?class="releasetime">(.*?)</p>'
        # 生成正则表达式对象
        pattern = re.compile(re_bds, re.S)
        # r_list: [('我不是药神','徐峥,周一围,王传君','2018-07-05'),...] 列表元组
        r_list = pattern.findall(html)
        return r_list

    # 保存数据函数，使用python内置csv模块
    def print_films(self, films):
        for r in films:
            name = r[0].strip()
            star = r[1].strip()[3:]
            time = r[2].strip()[5:15]
            L = [name, star, time]
            print(name, time, star)

    def fetch_one_batch(self):
        url = "https://www.maoyan.com/board/4?offset=0"
        h = get_headers(url)
        h["Cookie"] = (
            "_csrf=2c5813abd19aa460c5497fab0d18c4fc4f0acc06121d33d675a89acac8f9dba3; uuid=352F69C000AC11F08A64AD70B6989449FE99F5099BB7448BAD902216F0385753; uuid_n_v=v1"
        )
        rsp = self.get(url, headers=h)
        if rsp.ok:
            p = etree.HTML(rsp.text)
        dd_list = p.xpath('//dl[@class="board-wrapper"]/dd')
        for dd in dd_list:
            name = dd.xpath('.//p[@class="name"]/a/text()')[0].strip()
            star = dd.xpath('.//p[@class="star"]/text()')[0].strip()
            release_time = dd.xpath('.//p[@class="releasetime"]/text()')[0].strip()
            L = [name, star, release_time]
            print(L)

    # 主函数
    def run(self):
        # 抓取第一页数据
        for offset in range(0, 100, 10):
            params = {"offset": offset}
            logger.debug(get_headers(self.base))
            # resp = self.get(self.base, headers=get_headers(self.base), params=params)
            # # 直接调用解析函数
            # r_list = self.parse_html(resp.text)
            # self.print_films(r_list)
            # # 生成1-2之间的浮点数
            # time.sleep(random.random())


# 以脚本方式启动
if __name__ == "__main__":
    # 捕捉异常错误
    try:
        spider = MaoyanSpider()
        # spider.run()
    except Exception as e:
        print("错误:", e)
