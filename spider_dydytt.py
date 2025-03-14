"""
爬取多级页面，
用md5把爬取过的url生成hash，实现增量式爬虫。
"""

# -*- coding: utf-8 -*-
from urllib import request
import re
import time
import random
from hashlib import md5
import sys
import json
from loguru import logger

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Cookie": "__mta=140885517.1741655259068.1741684011331.1741684013790.18; uuid_n_v=v1; uuid=411861E0FE1511EF95CE179E06884450E3E2A645CEA44A55BAAE2E0354AE28D5; _csrf=0abb44a2eca28e6c85e7f77260b87e7e09e311a1273fe15f6f7019ad644aefb8; Hm_lvt_e0bacf12e04a7bd88ddbd9c74ef2b533=1741655258; HMACCOUNT=222C4C737AA4B431; _lxsdk_cuid=19582be339ec8-0f0901b998f804-26011d51-144000-19582be339ec8; _ga=GA1.1.101381580.1741655259; __mta=140885517.1741655259068.1741682566986.1741682570528.7; theme=moviepro; _lxsdk=411861E0FE1511EF95CE179E06884450E3E2A645CEA44A55BAAE2E0354AE28D5; Hm_lpvt_e0bacf12e04a7bd88ddbd9c74ef2b533=1741684014; _ga_WN80P4PSY7=GS1.1.1741682545.3.1.1741684120.0.0.0; _lxsdk_s=195845e8b1b-0cf-e07-625%7C%7C53",
    "Host": "dydytt.net",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    "Referer": "https://dydytt.net/index.htm",
}
from spider import SpiderBase


class MovieSkySpider(SpiderBase):
    def __init__(self):
        self.url = "https://www.dydytt.net/html/gndy/dyzz/list_23_{}.html"

    # 2.正则解析函数
    def re_func(self, re_bds, html):
        pattern = re.compile(re_bds, re.S)
        r_list = pattern.findall(html)
        return r_list

    # 3.提取数据函数
    def parse_html(self, one_url):
        # 调用请求函数，获取一级页面
        one_html = self.get(one_url, headers=headers).text
        re_bds = '<table width="100%".*?<td width="5%".*?<a href="(.*?)".*?ulink">.*?</table>'
        # 获取二级页面链接
        # link_list: ['/html//html/gndy/dyzz/20210226/61131.html','/html/xxx','','']
        link_list = self.re_func(re_bds, one_html)
        print(link_list)
        for link in link_list:
            # 判断是否需要爬取此链接
            # 1.获取指纹
            # 拼接二级页面url
            two_url = "https://www.dydytt.net" + link
            s = md5()
            # 加密url，需要是字节串
            s.update(two_url.encode())
            # 生成指纹，获取十六进制加密字符串，
            finger = s.hexdigest()
            # 2.通过函数判断指纹在数据库中是否存在
            if self.is_hold_on(finger):
                # 抓取二级页面数据
                self.save_html(two_url, finger)
                time.sleep(random.random())
            else:
                logger.debug(f"{two_url} already in dytt.json, continue...")
                # sys.exit("更新完成")

    # 4.判断链接是否已经抓取过
    def is_hold_on(self, finger):
        with open("data/dytt.json", "r") as f:
            data = json.load(f)
            if finger in data.keys():
                # 已经抓取过了
                return False
        # 还没有被抓取过
        return True

    # 5.解析二级页面，获取数据（名称与下载链接）
    def save_html(self, two_url, finger):
        rsp = self.get(two_url)
        text = rsp.content.decode("gb2312", "ignore")
        _match = re.search("<title>(.*?)</title>", text)
        title = _match.groups()[0] if _match else None

        _match = re.search('<a .*? target="_blank" href="(.*?)">', text)
        download_link = _match.groups()[0] if _match else None
        print(title, download_link)
        with open("data/dytt.json", "r+") as f:
            try:
                data = json.load(f)
            except json.decoder.JSONDecodeError as e:
                data = {}
            logger.info(f"before write: {data}")
            data[finger] = [title, download_link]
            logger.info(f"after write: {data}")
            f.seek(0)
            json.dump(data, f, indent=4, ensure_ascii=False, sort_keys=True)

    # 主函数
    def run(self):
        # 二级页面后四页的正则表达式略有不同，需要重新分析
        for i in range(1, 4):
            url = self.url.format(i)
            self.parse_html(url)


if __name__ == "__main__":
    spider = MovieSkySpider()
    html = spider.run()
