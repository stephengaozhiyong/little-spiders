import requests, json
from loguru import logger


class SpiderBase:
    # 4.判断链接是否已经抓取过
    def is_hold_on(self, finger):
        raise NotImplementedError("to be implemented by children...")

    def get(self, url, headers={}, params={}):
        req = requests.Request("GET", url, headers=headers, params=params)
        r = req.prepare()
        logger.info(f"start scraping...: {r.url}")
        sess = requests.Session()
        try:
            rsp = sess.send(r, allow_redirects=False)
        except Exception:
            raise RuntimeError("sess send failed!!!")
        if rsp.status_code != 200:
            logger.error("some thing error occured!!!")
            logger.error(
                f"req.url: {req.url}",
            )
            logger.error(
                f"res.request.url: {rsp.request.url}",
            )
            raise RuntimeError(f"{rsp.ok}, {rsp.status_code}, {rsp.content}")
        return rsp
