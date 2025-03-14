import os
from requests import Response
from pathlib import Path
from fake_useragent import UserAgent
from dotted_dict import DottedDict
from urllib import parse


headers = {
    "Accept": "*/*",
    "Accept-Encoding": "deflate",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Cookie": "BAIDUID=552757DE4EC43FBF843033DB8E6270D5:FG=1; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; BIDUPSID=552757DE4EC43FBF62384A78019CBD2C; H_WISE_SIDS=62035_62325_62345_62328_62420_62423_62480_62499",
    "Host": None,
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": None,
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    "Referer": None,
}

root = Path(os.getcwd())
html_folder = root / "html_folder"


def save_html(res: Response, path: str):
    with open(html_folder / path, "wb") as f:
        f.write(res.content)


def get_ua():
    ua = UserAgent()
    return ua.random


def get_headers(url):
    r = parse.urlparse(url)
    if r.hostname:
        headers["Host"] = r.hostname
        headers["User-Agent"] = get_ua()
        headers["Referer"] = f"{r.scheme}://{r.netloc}{r.path}"
    return headers


def text_to_dict():
    raw = {}  # headers 文本形式
    headers = {}
    for one in raw.split("\n"):
        _a = one.split(":")
        if len(_a) == 2:
            k, v = _a
            headers.update({k.strip(): v.strip()})
        else:
            print(_a)
    headers.update(
        {
            "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            "Referer": "https://www.maoyan.com/board/4?offset=20",
        }
    )
    return headers


if __name__ == "__main__":
    pass
