# coding:utf8
import requests
import time
import random
import re
import json

# from ua_info import ua_list
from tools import get_ua


class DoubanSpider(object):
    def __init__(self):
        self.url = "https://movie.douban.com/j/chart/top_list?"
        self.i = 0

    # 获取随机headers
    def get_headers(self):
        # headers = {"User-Agent": random.choice(ua_list)}
        headers = {"User-Agent": get_ua()}
        return headers

    # 获取页面
    def get_page(self, params):
        # 将json转换为 python 数据类型，并返回
        html = requests.get(
            url=self.url, params=params, headers=self.get_headers()
        ).text
        html = json.loads(html)
        self.parse_page(html)

    # 解析并保存数据
    def parse_page(self, html):
        item = {}
        # html列表类型： [{电影1},{电影2},{电影3}...]
        for one in html:
            # 名称 + 评分
            item["name"] = one["title"].strip()
            item["score"] = float(one["score"].strip())
            print(item)
            self.i += 1

    # 获取电影总数
    def total_number(self, type_number):
        # F12抓包抓到的地址，type表示电影类型
        url = "https://movie.douban.com/j/chart/top_list_count?type={}&interval_id=100%3A90".format(
            type_number
        )
        headers = self.get_headers()
        html = requests.get(url=url, headers=headers).json()
        total = int(html["total"])
        return total

    # 获取所有电影的类型和对应type值
    def get_all_type_films(self):
        # 获取类型与类型码
        url = "https://movie.douban.com/chart"
        headers = self.get_headers()
        html = requests.get(url=url, headers=headers).text
        re_bds = r"<a href=.*?type_name=(.*?)&type=(.*?)&.*?</a>"
        pattern = re.compile(re_bds, re.S)
        r_list = pattern.findall(html)
        # 存放所有类型和对应类型码大字典
        type_dict = {}
        # 定义一个选择电影类型的菜单
        menu = ""
        for r in r_list:
            type_dict[r[0].strip()] = r[1].strip()
            # 获取input的菜单，显示所有电影类型
            menu += r[0].strip() + "|"

        return type_dict, menu

    # 主程序入口函数
    def main(self):
        # 获取type的值
        type_dict, menu = self.get_all_type_films()
        menu = menu + "\n你想了解什么类型电影:"
        name = input(menu)
        type_number = type_dict[name]
        # 获取电影总数
        total = self.total_number(type_number)
        total = 100
        for start in range(0, (total + 1), 20):
            # 构建查询参数
            params = {
                "type": type_number,
                "interval_id": "100:90",
                "action": "",
                "start": str(start),
                "limit": "20",
            }
            # 调用函数,传递params参数
            self.get_page(params)
            # 随机休眠1-3秒
            time.sleep(random.randint(1, 3))
        print("电影总数量:%d部" % self.i)


if __name__ == "__main__":
    spider = DoubanSpider()
    spider.main()
