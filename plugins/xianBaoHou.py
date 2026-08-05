# [title: 线报猴]
# [name: xianBaoHou]
# [language: python]
# [class: 任务]
# [author: authook]
# [version: v1.0.1]
# [public: true]
# [disable: false]
# [admin: true]
# [rule: ^线报猴$]
# [cron: 0/15 * * * * *]
# [icon: https://iehou.com/view/img/favicon.ico]
# [description: 线报推送 xbh]
# [depe: ["beautifulsoup4","colorlog","requests"]]


import asyncio as _sg_asyncio
import os as _sg_os
import time as _sg_time
import types as _sg_types
from threading import Thread as _sg_Thread
from sillygirl import Adapter as _SGAdapter, Bucket as _SGBucket, Sender as _SGSender, sender as _sg_sender
try:
    import ast as _sg_ast
except Exception:
    _sg_ast = None
try:
    import decimal as decimal
except Exception:
    decimal = None

_sg_loop = None

def _sg_get_loop():
    global _sg_loop
    if _sg_loop is not None and not _sg_loop.is_closed():
        return _sg_loop
    box = {}
    def runner():
        loop = _sg_asyncio.new_event_loop()
        _sg_asyncio.set_event_loop(loop)
        box["loop"] = loop
        loop.run_forever()
    t = _sg_Thread(target=runner, daemon=True)
    t.start()
    while "loop" not in box:
        _sg_time.sleep(0.01)
    _sg_loop = box["loop"]
    return _sg_loop

def _sg_run(coro):
    if not _sg_asyncio.iscoroutine(coro):
        return coro
    loop = _sg_get_loop()
    future = _sg_asyncio.run_coroutine_threadsafe(coro, loop)
    return future.result()


def _sg_sender_sync(uuid=""):
    s=_SGSender(uuid or _sg_os.environ.get("SENDER_ID", ""))
    def call(name,*a,**k): return _sg_run(getattr(s,name)(*a,**k))
    def listen(timeout=60000,*a,**k):
        try:
            r=call("listen", {"timeout": int(timeout or 0)})
            return _sg_run(r.getContent()) if r else ""
        except Exception: return ""
    return _sg_types.SimpleNamespace(
        getUserID=lambda:call("getUserId"), getUserId=lambda:call("getUserId"), getMessage=lambda:call("getContent"), getContent=lambda:call("getContent"),
        getUserName=lambda:call("getUserName"), getNickname=lambda:call("getUserName"), getChatID=lambda:call("getChatId"), getChatId=lambda:call("getChatId"),
        getImtype=lambda:call("getPlatform"), getPlatform=lambda:call("getPlatform"), getMessageID=lambda:call("getMessageId"), getPluginName=lambda:_sg_os.environ.get("PLUGIN_NAME",""), getPluginVersion=lambda:_sg_os.environ.get("PLUGIN_VERSION",""),
        isAdmin=lambda:bool(call("isAdmin")), reply=lambda msg="":call("reply", str(msg)), replyImage=lambda url="":call("reply", str(url) if str(url).startswith("[") else f"[CQ:image,file={url}]"),
        listen=listen, input=listen, waitInput=listen, setContinue=lambda *a,**k:call("continue_"), breakIn=lambda *a,**k:call("continue_"))

def _sg_bucket_get(bucket=None,key=None,default="",**kw):
    try:
        v=_SGBucket(str(kw.get("bucket",bucket) or ""))[str(kw.get("key",key) or "")]
        return default if v in (None,"") and default not in (None,"") else (v if v is not None else "")
    except Exception: return default or ""
def _sg_bucket_set(bucket=None,key=None,value=None,**kw):
    try: _SGBucket(str(kw.get("bucket",bucket) or ""))[str(kw.get("key",key) or "")]=kw.get("value",value); return True
    except Exception: return False
def _sg_bucket_del(bucket=None,key=None,**kw): return _sg_bucket_set(kw.get("bucket",bucket),kw.get("key",key),None)
def _sg_bucket_keys(bucket=None,**kw):
    try: return _sg_run(_SGBucket(str(kw.get("bucket",bucket) or "")).keys())
    except Exception: return []
def _sg_bucket_all(bucket=None,**kw):
    try: return _sg_run(_SGBucket(str(kw.get("bucket",bucket) or "")).getAll()) or {}
    except Exception: return {}
def _sg_push(*a,**kw):
    i=a[0] if a and isinstance(a[0],dict) else {}; platform=i.get("imType") or i.get("platform") or kw.get("platform") or (a[0] if a else ""); group=i.get("groupCode") or i.get("group_id") or kw.get("group_id") or (a[1] if len(a)>1 else ""); user=i.get("userID") or i.get("user_id") or kw.get("userID") or (a[2] if len(a)>2 else ""); title=i.get("title") or kw.get("title") or (a[3] if len(a)>3 else ""); content=i.get("content") or i.get("message") or kw.get("content") or (a[4] if len(a)>4 else title)
    return _sg_run(_SGAdapter(str(platform or "")).push({"group_id":str(group or ""),"user_id":str(user or ""),"title":str(title or ""),"content":str(content or "")}))
def _sg_notify(msg,channels=None,*a,**k): return _sg_run(_sg_sender.pushAdmin(str(msg), {"platforms":list(channels or [])} if channels else {}))
class _SGFacade:
    Sender=staticmethod(_sg_sender_sync); getSenderID=staticmethod(lambda:_sg_os.environ.get("SENDER_ID","")); getPluginName=staticmethod(lambda:_sg_os.environ.get("PLUGIN_NAME","")); bucketGet=staticmethod(_sg_bucket_get); bucketSet=staticmethod(_sg_bucket_set); bucketDel=staticmethod(_sg_bucket_del); bucketDelete=staticmethod(_sg_bucket_del); bucketAllKeys=staticmethod(_sg_bucket_keys); bucketKeys=staticmethod(_sg_bucket_keys); bucketAll=staticmethod(_sg_bucket_all); notifyMasters=staticmethod(_sg_notify); pushAdmin=staticmethod(_sg_notify); push=staticmethod(_sg_push); Push=staticmethod(_sg_push); reply=staticmethod(lambda msg="":_sg_sender_sync().reply(msg)); get=staticmethod(lambda key,default="":_sg_bucket_get(*(str(key).split(".",1) if "." in str(key) else ["otto",key]), default=default)); getParam=get; version=staticmethod(lambda:{"sn":_sg_os.environ.get("SILLYGIRL_VERSION","3.0.0"),"version":_sg_os.environ.get("SILLYGIRL_VERSION","3.0.0")}); port=staticmethod(lambda:_sg_os.environ.get("SILLYGIRL_PORT","8080")); sleep=staticmethod(lambda sec:_sg_time.sleep(float(sec or 0)))
sg=_SGFacade(); Sender=sg.Sender; getSenderID=sg.getSenderID; bucketGet=sg.bucketGet; bucketSet=sg.bucketSet; bucketAllKeys=sg.bucketAllKeys; notifyMasters=sg.notifyMasters


config = None
_CONFIG_FIELD_MAP = {}


import datetime
import json
import logging
import re
import time

import colorlog
import requests
from bs4 import BeautifulSoup

class TOOL:
    def __init__(self):
        self.plugin_pre = "jd_3c"
        self.remark = ""
        self.platform_arr = self.platformArr()
        self.cut_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.logger = logging.getLogger()
        self.color_formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(levelname)s: %(message)s',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        self.logger = self._configure_logger()
        self.debug = False

    def _configure_logger(self):
        logger = logging.getLogger(self.plugin_pre)
        logger.setLevel(logging.DEBUG)  # 设置日志默认最低级别

        if not any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers):
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)  # 控制台日志最低级别
            console_handler.setFormatter(self.color_formatter)
            logger.addHandler(console_handler)

        return logger

    def log(self, level, message):
        if level == logging.INFO:
            self.logger.info(message)
        elif level == logging.ERROR:
            self.logger.error(message)
        elif level == logging.WARNING:
            self.logger.warning(message)
        elif level == logging.DEBUG:
            self.logger.debug(message)
        elif level == logging.CRITICAL:
            self.logger.critical(message)

    def log_debug(self, message):
        if self.debug:
            self.log(logging.DEBUG, message)

    def log_info(self, message):
        self.log(logging.INFO, message)

    def log_err(self, message):
        self.log(logging.ERROR, message)

    def log_warn(self, message):
        if self.debug:
            self.log(logging.WARNING, message)

    def platformArr(self):
        plat_arr = []
        for p in ["qq", "wx", "wb", "qb", "bt", "tg"]:
            t = {"platform": f"{p}", "imType": p}
            plat_arr.append(t)
        return plat_arr

    def pushMsg(self, userId, chatId, imType, title, content):
        now = datetime.datetime.now()
        formatted_datetime = now.strftime('%Y-%m-%d %H:%M:%S')
        self.remark = ""
        return sg.push(imType, chatId, userId, title, f"{formatted_datetime}\n{content}")

    def pushGroup(self, imtype, groupCode, content):
        self.pushMsg(0, groupCode, imtype, "", content)


    def replyMsg(self, content):
        return sender.reply(content)

    def pushMaster(self, content):
        arr = ["qq", "wx", "tg", "qb", 'wb']
        for p in arr:
            masters = sender.bucketGet(p, "masters")
            if masters:
                masters_arr = masters.split(",") if "," in masters else masters.split("&")
                for m in masters_arr:
                    sg.push(p, "", m, "", content)

    def qls(self):
        qls = []
        ql_id_arr = sender.bucketAllKeys("qls")
        if not ql_id_arr:
            return []
        for ql_id in ql_id_arr:
            value = sender.bucketGet("qls", ql_id)
            if value:
                qls.append(json.loads(value))
        return qls


    def listen_quiet(self, timeout):
        value = sender.listen(timeout)
        if value and value.lower() in ["q","Q","error"]:
            sender.reply("已退出！")
            exit()


class XBH:
    def __init__(self):
        self.black_words = sender.bucketGet("authook","xbh_black_words")
        self.status = sender.bucketGet("authook","xbh_status") or "n"
        self.push_groups = (sender.bucketGet("authook","xbh_push_groups") or "").split(",")
        self.headers = {
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2007J20CG Build/QKQ1.200419.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/88.0.4324.93 Mobile Safari/537.36"
        }
        self.host = "https://iehou.com/index.htm"

    def push_msg(self,msg):
        for group in self.push_groups:
            sg.push(group[:2], group[3:], "", "",f"{msg}")

    def get_url(self):
        res = requests.get(self.host, headers=self.headers)
        if res.status_code == 200:
            url_list = []
            soup = BeautifulSoup(res.text, "html.parser")
            for a in soup.find_all("a"):
                url = a.get("href")
                if "https://iehou.com/xianbao-" not in url:
                    continue
                if sender.bucketGet("xhb_url",url):
                    continue
                url_list.append(url)
            if not url_list:
                tool.log_info("暂无新线报")
                return
            for url in url_list:
                sender.bucketSet("xhb_url",url,"1")
                self.get_content(url)


    def get_content(self,url):
        r = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(r.text, "html.parser")
        div = soup.find_all("div", class_="thread-content message break-all")
        for d in div:
            for br in d.find_all('br'):
                br.replace_with('\n')
            text = d.get_text()
            if not text:
                tool.log_info("内容为空")
                continue
            if self.black_words and any(word in text for word in self.black_words.split(",")):
                tool.log_info("包含黑名单词汇")
                continue
            a_href_list = [a['href'] for a in d.find_all('a', href=True) if "u.jd" not in a['href']]
            if a_href_list:
                text += '\n'.join(a_href_list)
            self.mp_reg = re.compile(r'#小程序://[^/]+/[\w-]{15}')
            text = re.sub(self.mp_reg, lambda m: m.group(0) + " \n", text)
            content = f"【原帖】：{url}"
            content += f"\n【时间】：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            content += f"\n【内容】：{text}"
            self.push_msg(content)
            img_list = [a['src'] for a in d.find_all('img', src=True)]
            if img_list:
                for img in img_list:
                    self.push_msg(f"[CQ:image,file={img}]")


    def run(self):
        if self.status == "true":
            self.get_url()
        else:
            sender.reply("未开启线报猴")


if __name__ == "__main__":
    sender = sg.Sender(sg.getSenderID())
    plugin_ver = sender.getPluginVersion()
    plugin_name = sender.getPluginName()
    msg = sender.getMessage().strip('"')
    imType = "fake" if sender.getImtype() == "cron" else sender.getImtype()
    chatId = sender.getChatID()
    userId = sender.getUserID()
    isAdmin = sender.isAdmin()
    username = sender.getUserName()
    tool = TOOL()
    xbh = XBH()
    xbh.run()
