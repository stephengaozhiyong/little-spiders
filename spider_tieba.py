"""
抓取失败了，
初次登录tieba的时候有个滑动窗口验证，
暂时还不会解决这个问题，
先放一下吧，
后面再说
"""

import requests, os
from tools import get_ua
from pathlib import Path

root = Path(os.getcwd())
html_folder = root / "html_folder"


class TiebaSpider:
    def get_html(self, url):
        req = requests.Request(
            "GET",
            url,
            headers={
                "User-Agent": get_ua(),
                "Cookie": "TIEBA_USERTYPE=7a4a7b31c9c979705ea62058",
            },
        )
        r = req.prepare()
        print("start scraping...:")
        print(f"url: {r.url}")
        s = requests.Session()
        res = s.send(r)
        return res

    def save_html(self, f_path, html):
        with open(f_path, "w") as f:
            f.write(html)


if __name__ == "__main__":
    spider = TiebaSpider()
    res = spider.get_html(url="https://tieba.baidu.com/f?kw=ubuntu&ie=utf-8&pn=50")
    if res.ok:
        f_path = html_folder / "temp_tieba.html"
        spider.save_html(f_path, res.text)
        print(f"saved to {f_path} successfully.")
