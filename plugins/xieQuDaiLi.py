# [title: 携趣代理]
# [name: xieQuDaiLi]
# [language: python]
# [class: 任务]
# [author: funyhook]
# [version: v1.0.0]
# [public: true]
# [disable: false]
# [admin: true]
# [rule: ^携趣$|^携趣删白$|^携趣余量$|^携趣管理$|^携趣配置$|^xqfk$]
# [cron: 2 0 * * *]
# [icon: https://www.xiequ.cn/Home/img/logo.png]
# [description: 。]
# [depe: ["colorlog","requests","urllib3"]]


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
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool

import colorlog
import urllib3
import time
urllib3.disable_warnings()
import requests



class TOOL:
    def __init__(self):
        self.plugin_pre = 'vhook_xiequ_'
        self.plat = ["qq", "wx", "wb", "qb", "bt", "tg"]

        self.plugin_auth_ver = "2.5.5"
        self.auth_ver = sg.version()['sn']
        self.sender = sg.Sender(sg.getSenderID())
        self.plugin_ver = self.sender.getPluginVersion()
        self.plugin_name = self.sender.getPluginName()
        self.platform_arr = self.platformArr()

        self.msg = self.sender.getMessage().strip('"')
        self.imType = "fake" if self.sender.getImtype() == "cron" else self.sender.getImtype()
        self.chatId = self.sender.getChatID()
        self.userId = self.sender.getUserID()
        self.isAdmin = self.sender.isAdmin()
        self.username = self.sender.getUserName()
        self.remark = ""
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
        self.content_msg=""
        self.conf = {
            "white_type": self.bucketGet(f"{self.plugin_pre}conf", "white_type") or "1",
            "white_ip_list": self.bucketGet(f"{self.plugin_pre}conf", "white_ip_list") or "",
        }

    def get_log(self, level=logging.INFO):
        self.logger.setLevel(level)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(self.color_formatter)
        for handler in self.logger.handlers:
            self.logger.removeHandler(handler)
        self.logger.addHandler(console_handler)

    def log_info(self, message):
        self.get_log(logging.INFO)
        return self.logger.info(f"【{self.plugin_name}】: {message}")

    def log_err(self, message):
        self.get_log(logging.ERROR)
        return self.logger.error(f"【{self.plugin_name}】: {message}")

    def log_warn(self, message):
        self.get_log(logging.WARN)
        return self.logger.warning(f"【{self.plugin_name}】: {message}")

    def platformArr(self):
        plat_arr = []
        for p in self.plat:
            t = {"platform": f"{self.plugin_pre}{p}", "imType": p}
            plat_arr.append(t)
        return plat_arr

    def pushMsg(self, userId, chatId, imType, title, content):
        now = datetime.datetime.now()
        formatted_datetime = now.strftime('%Y-%m-%d %H:%M:%S')
        self.remark = ""
        sg.push(imType, chatId, userId, title,
                        f"****{self.msg}****\n【运行时间】：{formatted_datetime}\n{content}")
        return
    def pushErr2Master(self, content):
        sg.notifyMasters(
            f"【插件】：{self.plugin_title}\n {content}",
            ['qq', 'tg', 'wx', 'wb', ])


    def pushGroup(self, imtype, groupCode, content):
        self.pushMsg(0, groupCode, imtype, "", content)

    def replyMsg(self, content):
        return self.sender.reply(content)

    def pushMaster(self, content):
        arr=["qq","wx","tg","qb",'wb']
        for p in arr:
            masters = self.bucketGet(p,"masters")
            if masters:
                masters_arr = masters.split(",") if "," in masters else masters.split("&")
                for m in masters_arr:
                     self.log_info(f"{p}:::{m}")
                     sg.push(p,"",m,"",content)

    def bucketGet(self, bucket, key):
        if self.auth_ver >= self.plugin_auth_ver:
            return self.sender.bucketGet(bucket, key)
        else:
            return sg.bucketGet(bucket, key)

    def bucketKeys(self, bucket, value):
        if self.auth_ver >= self.plugin_auth_ver:
            return self.sender.bucketKeys(bucket, value)
        else:
            return sg.bucketKeys(bucket, value)

    def bucketAllKeys(self, bucket):
        if self.auth_ver >= self.plugin_auth_ver:
            return self.sender.bucketAllKeys(bucket)
        else:
            return sg.bucketAllKeys(bucket)

    def bucketSet(self, bucket, key, value):
        if self.auth_ver >= self.plugin_auth_ver:
            return self.sender.bucketSet(bucket, key, value)
        else:
            return sg.bucketSet(bucket, key, value)

    def bucketDel(self, bucket, key):
        if self.auth_ver >= self.plugin_auth_ver:
            return self.sender.bucketDel(bucket, key)
        else:
            return sg.bucketDel(bucket, key)


    def check_user_plugin(self, title, cloud_name):
        pass

    def hide_phone_number(self, text):
        if not text:
            return text
        if len(text) > 11:
            return text
        return re.sub(r'(\d{3})\d{4}(\d{4})', r'\1****\2', text)

    def get_ip(self):
        urls = [
            "http://myip.ipip.net/json",
            "https://whois.pconline.com.cn/ipJson.jsp?json=true",
            "https://2024.ipchaxun.com",
            "https://searchplugin.csdn.net/api/v1/ip/get",
            "https://ip.useragentinfo.com/json"
        ]

        headers = {
            "Content-Type": "application/json"
        }

        for url in urls:
            try:
                res = requests.get(url=url, headers=headers)
                if res.status_code == 200:
                    rj = res.json()
                    if 'ip' in rj:
                        return rj['ip']
                    elif 'data' in rj and 'ip' in rj['data']:
                        return rj['data']['ip']
            except Exception as e:
                self.log_info(f"Failed to get IP from {url}: {e}")
                continue

        return None  # Return None if all attempts fail



    def edit_conf(self):
        conf = {
            "white_type": self.bucketGet(f"{self.plugin_pre}conf", "white_type") or "1",
            "white_ip_list": self.bucketGet(f"{self.plugin_pre}conf", "white_ip_list") or "",
        }
        options = [
            {"text": "加白方式", "key": "white_type", "tips": "加白方式（1：自动获取IP，2：自定义IP）"},
            {"text": "自定义IP", "key": "white_ip_list", "tips": "自定义IP（多个ip请用英文逗号分隔）"},
        ]
        content = "配置如下，请在【60】秒内输入对应序号编辑（q:退出）：\n"
        for i, option in enumerate(options, 1):
            content += f"{i}、{option['text']}：{conf[option['key']]}\n"
        content+=f"\n\n------\n插件版本：V{self.plugin_ver}"
        self.replyMsg(content)

        value = tool.sender.listen(60000)
        if not value or value == "q" or value == "error":
            self.replyMsg("已退出！")
            exit()

        option = options[int(value) - 1]
        if option:
            self.replyMsg(f"请输入{option['tips']}：")
            value = tool.sender.listen(60000)
            if not value or value == "q" or value == "error":
                self.replyMsg("已退出！")
                exit()
            conf[option["key"]] = value
            self.bucketSet(f"{tool.plugin_pre}conf",option['key'],value)
            self.sender.breakIn(tool.msg)
        else:
            self.replyMsg("请输入正确的序号")
            self.sender.breakIn(tool.msg)


class ACCOUNT:
    def __init__(self):
        self.attr_arr = [
            {
                "title": "uid(官网-白名单-白名单获取地址里面的参数uid的值)",
                "key": "uid",
                "timeOut": 60000
            },
            {
                "title": "ukey(官网-白名单-白名单获取地址里面的参数key的值)",
                "key": "ukey",
                "timeOut": 60000
            },
            {
                "title": "备注",
                "key": "name",
                "timeOut": 60000
            },
            {
                "title": "是否禁用账号（y/n）",
                "key": "disable",
                "timeOut": 60000
            }

        ]

    def setVal(self, item, title, key, timeOut):
        print(self)
        tool.replyMsg(f"{tool.plugin_name}-请输入{title}：")
        value = tool.sender.listen(timeOut)
        tool.log_info(f"{key}==={value}")
        if not value or value == "error":
            tool.replyMsg("输入有误/超时，已退出！")
            exit()
        if value == "q":
            tool.replyMsg("已退出！")
            exit()
        item[key] = value
        return True


    def addCount(self):
        tool.replyMsg("注册地址：https://www.xiequ.cn/index.html?b611237a")
        item = {}
        for attr in self.attr_arr:
            self.setVal(item, attr['title'], attr['key'], attr['timeOut'])
        item_arr = []
        item_str = sg.bucketGet(f"{tool.plugin_pre}{tool.imType}", tool.userId)
        if item_str:
            item_arr = json.loads(item_str)
        item_arr.append(item)
        sg.bucketSet(f"{tool.plugin_pre}{tool.imType}", tool.userId, json.dumps(item_arr))
        tool.replyMsg("数据已管理完成，指令：携趣加白/携趣删白/携趣管理")


    def editCount(self, item_arr, no):
        item = item_arr[no]
        content = "请在【2分钟】内输入 序号，编辑对应的属性（q：保存并退出）"
        content += "\n--------------------"
        content += "\n输入数字：0 删除此账号！"
        content += "\n--------------------"
        for index, attr in enumerate(self.attr_arr):
            content += f"\n{index + 1}.【{attr['title']}】：{tool.hide_phone_number(item[attr['key']])}"
        tool.replyMsg(content)
        value = tool.sender.listen(120000)
        if value == "q" or value == "error":
            sg.bucketSet(f"{tool.plugin_pre}{tool.imType}", tool.userId, json.dumps(item_arr))
            return tool.replyMsg("已退出！")
        if not value.isdigit():
            return self.editCount(item_arr, no)
        if 0 < int(value) <= len(self.attr_arr):
            attr = self.attr_arr[int(value) - 1]
            if self.setVal(item, attr['title'], attr['key'], 12000):
                item_arr[no] = item
                self.editCount(item_arr, no)
        elif value == "0":
            item_arr.pop(no)
            if len(item_arr) == 0:
                sg.bucketDel(f"{tool.plugin_pre}{tool.imType}", tool.userId)
            else:
                sg.bucketSet(f"{tool.plugin_pre}{tool.imType}", tool.userId, json.dumps(item_arr))
            return tool.replyMsg(f"已删除第{no + 1}个账号信息！请重新发送：携趣管理 ！")
        else:
            return self.editCount(item_arr, no)

    def accoount_manager(self):
        item_str = sg.bucketGet(f"{tool.plugin_pre}{tool.imType}", tool.userId)
        if not item_str or item_str == "":
            tool.replyMsg(f"[{tool.plugin_name}]:未配置账号，请发送：携趣加白")
            exit(1)
        item_arr = json.loads(item_str)
        content = f"[{tool.plugin_name}]请选择要账号查看详情：（0增加， q退出）\n"
        for index, item in enumerate(item_arr):
            status = "禁用" if item['disable'] == "y" else "启用"
            content = "".join([content, f"\n{index + 1}、{item['name']} （{status}）"])
        tool.replyMsg(content)
        value = tool.sender.listen(60000)
        if value == "q" or value == "error":
            tool.replyMsg("输入有误，已退出！")
        elif value == "0":
            self.addCount()
        elif value.isdigit() and 0 < int(value) <= len(item_arr):
            self.editCount(item_arr, int(value) - 1)
        else:
            tool.replyMsg(f"[{tool.plugin_name}]:输入有误,请重新发送:携趣管理，并输入正确的序号！")

    def cron_account_arr(self):
        print(self)
        account_arr = []
        for plat in tool.platformArr():
            p = plat["platform"]
            user_id_arr = sg.bucketAllKeys(p)
            if not user_id_arr:
                continue
            for index, user_id in enumerate(user_id_arr):
                user_data_str = sg.bucketGet(p, user_id)
                if not user_data_str or user_id == '':
                    continue
                user_data_arr_temp = json.loads(user_data_str)
                for n, account_data in enumerate(user_data_arr_temp):
                    account_data["push_user_id"] = user_id
                    account_data["push_im_type"] = plat["imType"]
                    account_data['index'] = n + 1
                    account_data['total'] = len(user_data_arr)
                    account_arr.append(account_data)
        return account_arr

    def account_task(self, item, no):
        print(self)
        read = XIEQU(item)
        read.run()


class XIEQU:
    def __init__(self, ac):
        self.uid = ac['uid']
        self.ukey = ac['ukey']
        self.name = ac['name']
        self.push_user_id = ac['push_user_id']
        self.push_im_type = ac['push_im_type']
        self.msg = ""
        self.balance = 0


    def pushMsg(self, msg):
        content = f'{msg}'
        tool.pushMsg(self.push_user_id, "", self.push_im_type, "", content)

    def pushGroups(self, content):
        groups = sg.get("wxyd__notify_groups")
        if groups:
            group_arr = groups.split(",")
            for group in group_arr:
                tool.log_info(group)
                imType = group.split(":")[0][:2]
                chatId = group.split(":")[1]
                msg = f"\n【账号备注】：{self.en_mobile}"
                msg += f'\n{content}'
                tool.pushGroup(imType, chatId, msg)

    def log_info(self, msg):
        tool.log_info(f"【账号备注】：{self.en_mobile} ：{msg}")


    def delAll(self):
        url = f'http://op.xiequ.cn/IpWhiteList.aspx?uid={self.uid}&ukey={self.ukey}&act=del&ip=all'
        res = requests.get(url)
        tool.log_info(f"XIEQU delAll res {res.text}")
        self.msg += f"\n【删白名单】：{res.text}"

    def set_white_ip(self, ip):
        white_ip_list = []
        msg = ""
        if tool.conf['white_type'] == "1":
            white_ip_list.append(ip)
        if tool.conf['white_type'] == "2":
            if tool.conf['white_ip_list']:
                white_ip_list = tool.conf['white_ip_list'].split(",")
        if white_ip_list:
            for index,ip in enumerate(white_ip_list):
                if index>0:
                    time.sleep(5)
                url = f"http://op.xiequ.cn/IpWhiteList.aspx?uid={self.uid}&ukey={self.ukey}&act=add&ip={ip}"
                res = requests.get(url)
                tool.log_info(f"XIEQU set_white_ip [{ip}] res {res.text}")
                msg += f"\n【加白IP】：{ip}：{res.text}"
            self.msg += f"\n【白名单IP】：{','.join(white_ip_list)}"
            self.msg += f"\n【加白名单】：{res.text}"
        return msg


    def info(self):
        url = f"http://op.xiequ.cn/ApiUser.aspx?act=suitdt&uid={self.uid}&ukey={self.ukey}"
        res = requests.get(url)
        tool.log_info(res.text)
        if "ERR#Null" in res.text:
            self.balance = 0
            return
        if res.status_code == 200:
            rj = res.json()
            if rj['success']:
                for item in rj['data']:
                    self.msg += f"\n【{item['type']}余量】：{int(item['num'])-int(item['use'])}"
                    self.balance = int(item['num'])-int(item['use'])

    def all_balance(self):
        self.info()
        tool.content_msg +=f"\n【账号】：{self.uid}，剩余ip：{self.balance}"


    def run(self):
        self.msg += f"【携趣账号】：{self.uid}"
        self.msg += f"\n【携趣备注】：{self.name}"
        self.info()
        ip = tool.getIP()
        if tool.msg == "携趣删白":
            self.delAll()
            self.pushMsg(self.msg)
        else:
            if self.balance>0:
                self.msg+="\n【温馨提示】ip余额充足，执行删白加白"
                self.delAll()
                self.set_white_ip(ip)
                self.pushMsg(self.msg)
                exit(1)
            else:
                self.msg+="\n【温馨提示】，ip用完了，自动删除全部白名单，开始下个账号加白"
                self.delAll()
                self.pushMsg(self.msg)

if __name__ == "__main__":
    tool = TOOL()
    account = ACCOUNT()
    if tool.msg == '携趣配置':
        tool.edit_conf()
        exit("携趣配置退出")
    if tool.msg == '携趣管理':
        account.accoount_manager()
        exit(1)
    user_data_arr = []
    if tool.imType == 'fake' or tool.msg =="xqfk":
        user_data_arr = account.cron_account_arr()
    else:
        user_str = sg.bucketGet(f"{tool.plugin_pre}{tool.imType}", tool.userId)
        if not user_str or user_str == "":
            account.addCount()
            exit(1)
        user_data_arr = json.loads(user_str)
        tool.log_info(user_str)
        for i, user_data in enumerate(user_data_arr):
            user_data["push_user_id"] = tool.userId
            user_data["push_im_type"] = tool.imType
            user_data['index'] = i + 1
            user_data['total'] = len(user_data_arr)
    num_of_accounts = len(user_data_arr)
    tool.log_info(f"获取到 {num_of_accounts} 个账号,多线程并发任务")
    if tool.msg == "携趣余量":
        for item in user_data_arr:
            XIEQU(item).all_balance()
        tool.pushMsg(tool.userId,"",tool.imType,"",tool.content_msg)
        exit()
    if tool.msg == "携趣加白":
        white_ip = tool.get_ip()
        for item in user_data_arr:
            xq = XIEQU(item)
            xq.delAll()
            xq.info()
            if xq.balance>0:
                msg = f"【携趣账号】：{xq.uid}"
                msg += f"\n【携趣备注】：{xq.name}"
                msg += "\n【温馨提示】ip余额充足，执行删白加白"
                msg += xq.set_white_ip(white_ip)
                tool.pushMsg(item['push_user_id'],"",item['push_im_type'],"",msg)
                break
        exit()
    with Pool() as pool:
        thread_pool = ThreadPool(1)
        thread_pool.starmap(account.account_task, [(account, i) for i, account in enumerate(user_data_arr, start=1)])
    exit(1)
