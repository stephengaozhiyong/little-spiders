import json
import os, glob, re
from loguru import logger
from hashlib import md5
from spider import SpiderBase
from tools import get_headers


class SpiderImage(SpiderBase):
    finger_path = "data/images_fingers.text"

    def reset(self):
        with open(self.finger_path, "w") as f:
            pass

        files = glob.glob("images/*")
        for f in files:
            os.remove(f)

    def cal_finger(self, string: str):
        s = md5()
        s.update(string.encode())
        finger = s.hexdigest()
        return finger

    def get_all_fingers(self):
        with open(self.finger_path, "r") as f:
            return [x.rstrip() for x in f.readlines()]

    def already_get(self, finger):
        fingers_all = self.get_all_fingers()
        if finger in fingers_all:
            return True
        return False

    def save_finger(self, finger):
        _all = self.get_all_fingers()
        if finger in _all:
            return

        with open(self.finger_path, "a") as f:
            f.write(f"{finger}\n")

    def replace_invalid_char(self, s: str):
        return re.sub(r"[\s\/]", "", s)

    def fetch_one_batch(self, data):
        for item in data:
            try:
                title = self.replace_invalid_char(item["fromPageTitle"])
                img_url = item["hoverURL"]
            except KeyError as e:
                if not item:
                    continue
                logger.error(e)
                logger.error(item)
            logger.debug(f"titile: {title}")
            logger.debug(f"img_url: {img_url}")
            finger = self.cal_finger(img_url)
            if self.already_get(finger):
                logger.debug(f"already get {img_url}")
                continue
            res = self.get(img_url, headers=get_headers(img_url))
            if res.ok:
                save_path = f"images/{title}.jpg"
                logger.debug(f"save image to {save_path}")
                with open(save_path, "wb") as img:
                    img.write(res.content)
                self.save_finger(finger)

    def run(self):
        for i in range(3):
            rn = 30
            pn = i * rn
            url = f"https://image.baidu.com/search/acjson?tn=resultjson_com&logid=8973787188171475396&ipn=rj&ct=201326592&is=&fp=result&fr=&word=python&queryWord=python&cl=2&lm=&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&expermode=&nojc=&isAsync=&pn={pn}&rn={rn}&gsm=5a&17419"
            rsp = self.get(url, headers=get_headers(url))
            try:
                res = rsp.json()
                data = res["data"]
            except json.decoder.JSONDecodeError as e:
                logger.debug(e)
                s = rsp.text.replace("\\", "\\\\")
                data = json.loads(s)["data"]
                logger.debug(r"load successfully after replate \\")
            self.fetch_one_batch(data)


if __name__ == "__main__":
    sp = SpiderImage()
    # sp.reset()
    sp.run()
