import requests
from tools import save_html, headers, get_ua
from urllib import parse

headers["User-Agent"] = get_ua()
HOME = "http://www.baidu.com/"


def get(url=None, params={}, save=False, save_path="baidu-home-page.html"):
    if not url:
        url = HOME

    req = requests.Request("GET", url, headers=headers, params=params)
    r = req.prepare()
    print("start scraping...:")
    print(f"url: {r.url}")
    s = requests.Session()
    res = s.send(r)
    # res = requests.get(url, headers=headers, params=params, timeout=3)
    print(f"ok? {res.ok}")
    if save and res.ok:
        save_html(res, save_path)
        print(f"html is saved to {save_path}")
    return res


if __name__ == "__main__":
    params = {"wd": "爬虫"}
    url = f"{HOME}s"
    res = get(url, save=True, params=params, save_path="百度爬虫.html")
