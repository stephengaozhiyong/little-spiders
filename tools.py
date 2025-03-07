import os
from requests import Response
from pathlib import Path
from fake_useragent import UserAgent
from dotted_dict import DottedDict

headers = DottedDict({"User-Agent": None})
root = Path(os.getcwd())
html_folder = root / "html_folder"


def save_html(res: Response, path: str):
    with open(html_folder / path, "wb") as f:
        f.write(res.content)


def get_ua():
    ua = UserAgent()
    return ua.random
