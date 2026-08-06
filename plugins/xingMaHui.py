# [title: 星妈会]
# [name: xingMaHui]
# [language: python]
# [class: 任务]
# [author: sky2022]
# [version: v1.0.5]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^星妈会(登录|登陆|查询|管理|一键运行|后台|教程)$|^(登录|登陆|查询|管理)星妈会$]
# [cron: 0 8,15 * * *]
# [icon: https://tg.96218.xyz/file/BQACAgUAAxkDAAIHCmm-LiuIplV2-MijHZDPMGWzMIqcAAIzHAACNG7wVX3FrlyGxlWhOgQ.png]
# [description: 此插件出自徒弟：huawei；合并版【星妈会】插件，内置飞鹤项目与星妈会项目，插件内置运行；指令：星妈会登录、星妈会查询、星妈会管理、星妈会一键运行、星妈会后台、星妈会教程]
# [depe: ["requests","urllib3"]]
import asyncio as _sg_asyncio
import os as _sg_os
import time as _sg_time
import types as _sg_types
from threading import Thread as _sg_Thread
from sillygirl import Adapter as _SGAdapter, Bucket as _SGBucket, Sender as _SGSender, sender as _sg_sender, plugin

_runtime_config = plugin.Form({
    "enable": plugin.Form.boolean().title("是否启用").default(True),
})
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
    if _sg_loop is not None and not _sg_loop.is_closed(): return _sg_loop
    box = {}
    def runner():
        loop = _sg_asyncio.new_event_loop(); _sg_asyncio.set_event_loop(loop); box["loop"] = loop; loop.run_forever()
    _sg_Thread(target=runner, daemon=True).start()
    while "loop" not in box: _sg_time.sleep(0.01)
    _sg_loop = box["loop"]; return _sg_loop

def _sg_run(value):
    if not _sg_asyncio.iscoroutine(value): return value
    return _sg_asyncio.run_coroutine_threadsafe(value, _sg_get_loop()).result()

def _sg_sender_sync(uuid=""):
    s = _SGSender(uuid or _sg_os.environ.get("SENDER_ID", "")); call = lambda name,*a,**k: _sg_run(getattr(s,name)(*a,**k))
    def wait(timeout=60000,*a,**k):
        try:
            reply = call("listen", {"timeout": int(timeout or 0)}); return _sg_run(reply.getContent()) if reply else ""
        except Exception: return ""
    return _sg_types.SimpleNamespace(getUserID=lambda:call("getUserId"),getUserId=lambda:call("getUserId"),getMessage=lambda:call("getContent"),getContent=lambda:call("getContent"),getUserName=lambda:call("getUserName"),getNickname=lambda:call("getUserName"),getChatID=lambda:call("getChatId"),getChatId=lambda:call("getChatId"),getImtype=lambda:call("getPlatform"),getPlatform=lambda:call("getPlatform"),getMessageID=lambda:call("getMessageId"),getPluginName=lambda:_sg_os.environ.get("PLUGIN_NAME",""),getPluginVersion=lambda:_sg_os.environ.get("PLUGIN_VERSION",""),isAdmin=lambda:bool(call("isAdmin")),reply=lambda m="":call("reply",str(m)),replyImage=lambda u="":call("reply",str(u) if str(u).startswith("[") else f"[CQ:image,file={u}]"),listen=wait,input=wait,waitInput=wait,setContinue=lambda *a,**k:call("continue_"),breakIn=lambda *a,**k:call("continue_"))

def _sg_bucket_get(bucket=None,key=None,default="",**kw):
    try:
        value=_SGBucket(str(kw.get("bucket",bucket) or ""))[str(kw.get("key",key) or "")]; return default if value in (None,"") and default not in (None,"") else (value if value is not None else "")
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
    item=a[0] if a and isinstance(a[0],dict) else {}; platform=item.get("imType") or item.get("platform") or kw.get("platform") or (a[0] if a else ""); group=item.get("groupCode") or item.get("group_id") or kw.get("group_id") or (a[1] if len(a)>1 else ""); user=item.get("userID") or item.get("user_id") or kw.get("userID") or (a[2] if len(a)>2 else ""); title=item.get("title") or kw.get("title") or (a[3] if len(a)>3 else ""); message=item.get("content") or item.get("message") or kw.get("content") or (a[4] if len(a)>4 else title); return _sg_run(_SGAdapter(str(platform or "")).push({"group_id":str(group or ""),"user_id":str(user or ""),"title":str(title or ""),"content":str(message or "")}))
def _sg_notify(message,channels=None,*a,**k): return _sg_run(_sg_sender.pushAdmin(str(message),{"platforms":list(channels or [])} if channels else {}))
class _SGFacade:
    Sender=staticmethod(_sg_sender_sync); getSenderID=staticmethod(lambda:_sg_os.environ.get("SENDER_ID","")); getPluginName=staticmethod(lambda:_sg_os.environ.get("PLUGIN_NAME","")); bucketGet=staticmethod(_sg_bucket_get); bucketSet=staticmethod(_sg_bucket_set); bucketDel=staticmethod(_sg_bucket_del); bucketDelete=staticmethod(_sg_bucket_del); bucketAllKeys=staticmethod(_sg_bucket_keys); bucketKeys=staticmethod(_sg_bucket_keys); bucketAll=staticmethod(_sg_bucket_all); notifyMasters=staticmethod(_sg_notify); pushAdmin=staticmethod(_sg_notify); push=staticmethod(_sg_push); Push=staticmethod(_sg_push); reply=staticmethod(lambda m="":_sg_sender_sync().reply(m)); get=staticmethod(lambda k,default="":_sg_bucket_get(*(str(k).split(".",1) if "." in str(k) else ["otto",k]),default=default)); getParam=get; version=staticmethod(lambda:{"sn":_sg_os.environ.get("SILLYGIRL_VERSION","3.0.0"),"version":_sg_os.environ.get("SILLYGIRL_VERSION","3.0.0")}); port=staticmethod(lambda:_sg_os.environ.get("SILLYGIRL_PORT","8080")); sleep=staticmethod(lambda sec:_sg_time.sleep(float(sec or 0)))
sg=_SGFacade(); Sender=sg.Sender; getSenderID=sg.getSenderID; bucketGet=sg.bucketGet; bucketSet=sg.bucketSet; bucketAllKeys=sg.bucketAllKeys; notifyMasters=sg.notifyMasters

config = None
_CONFIG_FIELD_MAP = {}

import hashlib
import json
import re
import time
import random
from datetime import datetime

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PROJECT_NAME = "星妈会"
BUCKET_USER = "dd_xmyx_user"
BUCKET_TOKEN = "dd_xmyx_token"
BUCKET_AUTH = "dd_xmyx_auth"
BUCKET_CONFIG = "dd_xmyx_config"
MOMCLUB_BASE_URL = "https://momclub.feihe.com/capis/c"
FEIHE_API_APP_ID = "xmyx"
PAY_TIMEOUT = 600000
PAY_POLL_TIMES = 60
PAY_POLL_INTERVAL_MS = 5000

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()

def has_bucket_value(value):
    return value is not None and str(value).strip() != ""

def bucket_get_first(primary_bucket, key, legacy_buckets=None, default=""):
    value = sg.bucketGet(primary_bucket, key)
    if has_bucket_value(value):
        return value
    return default

def bucket_set_primary(primary_bucket, key, value):
    sg.bucketSet(primary_bucket, key, value)

def bucket_del_all(primary_bucket, key, legacy_buckets=None):
    sg.bucketDel(primary_bucket, key)

def bucket_all_keys_merged(primary_bucket, legacy_buckets=None):
    merged = []
    for bucket_name in (primary_bucket,):
        for item in sg.bucketAllKeys(bucket_name) or []:
            if item not in merged:
                merged.append(item)
    return merged

def parse_bucket_phone_list(raw):
    text = str(raw or "").strip()
    if not text:
        return []
    try:
        data = json.loads(text)
        if isinstance(data, list):
            return [str(item).strip() for item in data if str(item).strip()]
        if isinstance(data, str):
            text = data
    except Exception:
        pass
    phones = []
    for part in str(text).replace("\r\n", "\n").replace("&", ",").split(","):
        current = str(part).strip()
        if current:
            phones.append(current)
    return list(dict.fromkeys(phones))

FEIHE_API_APP_KEY = str(bucket_get_first(BUCKET_CONFIG, "appKey") or "").strip() or "TwUQ01lKS1Km5zlV2f7amsZc5EQYkTbv"

class MomClubClient:
    def __init__(self, authorization):
        self.authorization = str(authorization or "").strip()
        self.phone = None
        self.nickname = None
        self.user_label = "未登录"

    def _headers(self):
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf2541022) XWEB/16467",
            "authorization": self.authorization,
            "content-type": "application/json",
            "locale": "zh_CN",
            "referer": "https://servicewechat.com/wxc83b55d61c7fc51d/75/page-frame.html",
        }

    def _update_user_label(self):
        self.user_label = mask_phone(self.phone) or self.nickname or "未命名账号"

    def get_member_info(self):
        if not self.authorization:
            return None
        try:
            response = requests.get(
                "{}/user/memberInfo".format(MOMCLUB_BASE_URL),
                headers=self._headers(),
                timeout=(5, 20),
                verify=False,
            )
            result = response.json()
            data = result.get("data")
            if result.get("success") and data:
                self.phone = str(data.get("mobile") or data.get("phone") or "").strip() or self.phone
                self.nickname = str(data.get("nickname") or data.get("name") or "").strip() or self.nickname
                self._update_user_label()
                return data
        except Exception:
            return None
        return None

    def get_todo_list(self):
        if not self.authorization:
            return None
        try:
            response = requests.get(
                "{}/activity/todo/list".format(MOMCLUB_BASE_URL),
                headers=self._headers(),
                params={"mockTime": int(time.time() * 1000)},
                timeout=(5, 20),
                verify=False,
            )
            result = response.json()
            data = result.get("data")
            if result.get("success") and data:
                return data
        except Exception:
            return None
        return None

    def checkin(self, checkin_data):
        try:
            activity_id = checkin_data.get("id")
            extra = checkin_data.get("checkInExtra", {}) or {}
            join_record = extra.get("joinRecord", []) or []
            today_record = next((record for record in join_record if record.get("today")), None)

            if today_record and today_record.get("joined"):
                return {"success": True, "credits": today_record.get("credits", 0), "already_done": True}

            payload = {"activityId": activity_id, "mockTime": int(time.time() * 1000)}
            response = requests.post(
                "{}/activity/todo/checkIn".format(MOMCLUB_BASE_URL),
                headers=self._headers(),
                json=payload,
                timeout=(5, 30),
                verify=False,
            )
            result = response.json()
            if result.get("success"):
                return {"success": True, "credits": result.get("data", {}).get("credits", 0), "already_done": False}
            return {"success": False, "message": result.get("message") or result.get("msg") or "签到失败"}
        except Exception as exc:
            return {"success": False, "message": str(exc)}

    def complete_task(self, task):
        task_name = task.get("name", "未知任务")
        try:
            activity_id = task.get("id")
            extra = task.get("taskTodoExtra", {}) or {}
            credits = extra.get("credits", 0)
            payload = {"activityId": activity_id, "mockTime": int(time.time() * 1000)}

            receive_response = requests.post(
                "{}/activity/todo/receive".format(MOMCLUB_BASE_URL),
                headers=self._headers(),
                json=payload,
                timeout=(5, 30),
                verify=False,
            )
            receive_result = receive_response.json()
            if not receive_result.get("success"):
                return {"success": False, "message": receive_result.get("message") or "{} 领取失败".format(task_name)}

            time.sleep(random.randint(3, 6))
            payload["mockTime"] = int(time.time() * 1000)
            complete_response = requests.post(
                "{}/activity/todo/complete".format(MOMCLUB_BASE_URL),
                headers=self._headers(),
                json=payload,
                timeout=(5, 30),
                verify=False,
            )
            complete_result = complete_response.json()
            if complete_result.get("success"):
                return {"success": True, "task_name": task_name, "credits": credits}
            return {"success": False, "message": complete_result.get("message") or "{} 完成失败".format(task_name)}
        except Exception as exc:
            return {"success": False, "message": "{} 异常: {}".format(task_name, exc)}

    def run_all_tasks(self):
        completed = 0
        messages = []
        todo_data = self.get_todo_list()
        if not todo_data:
            return {"completed": 0, "messages": ["任务列表获取失败"]}

        checkin_data = todo_data.get("checkInTodo")
        if checkin_data:
            checkin_result = self.checkin(checkin_data)
            if checkin_result.get("success"):
                completed += 1
                if checkin_result.get("already_done"):
                    messages.append("今日已签到")
                else:
                    messages.append("签到成功(+{}积分)".format(checkin_result.get("credits", 0)))
            else:
                messages.append("签到失败: {}".format(checkin_result.get("message") or "未知错误"))
            time.sleep(random.randint(1, 3))

        skip_types = {"Perfect", "AddQw", "FirstOrder"}
        for task in todo_data.get("taskTodo", []) or []:
            extra = task.get("taskTodoExtra", {}) or {}
            task_type = extra.get("type", "")
            task_name = task.get("name", "未知任务")
            status = extra.get("status", "")
            complete_count = extra.get("completeCount", 0)
            complete_limit = extra.get("completeLimit", 1)

            if task_type in skip_types:
                messages.append("跳过任务: {}".format(task_name))
                continue
            if status == "3" or complete_count >= complete_limit:
                messages.append("任务已完成: {}".format(task_name))
                continue

            task_result = self.complete_task(task)
            if task_result.get("success"):
                completed += 1
                messages.append("任务完成: {} (+{}积分)".format(task_name, task_result.get("credits", 0)))
            else:
                messages.append("任务失败: {}".format(task_result.get("message") or task_name))
            time.sleep(random.randint(2, 4))

        return {"completed": completed, "messages": messages}

class FeiHeAuto:
    def __init__(self, access_token):
        self.token = str(access_token or "").strip()
        self.headers = {
            "Host": "www.feihevip.com",
            "token": self.token,
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.48(0x1800302b) NetType/4G Language/zh_CN",
            "Referer": "https://servicewechat.com/wx4205ec55b793245e/215/page-frame.html",
            "fhAppid": FEIHE_API_APP_ID,
            "source": "1",
        }

    def get_timestamp(self):
        return int(str(int(time.time() * 1000))[:10])

    def get_nonce(self, config=None):
        config = config or {}
        length = config.get("length", 16)
        use_numeric = config.get("numeric", True)
        use_letters = config.get("letters", True)
        use_special = config.get("special", False)
        exclude = config.get("exclude", []) if isinstance(config.get("exclude", []), list) else []
        char_pool = ""
        if use_numeric:
            char_pool += "0123456789"
        if use_letters:
            char_pool += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        if use_special:
            char_pool += "!$%^&*()_+|~-=`{}[]:;<>?,./"
        for excluded_char in exclude:
            char_pool = char_pool.replace(excluded_char, "")
        result = ""
        for _ in range(length):
            result += random.choice(char_pool)
        return result

    def get_signature(self):
        fh_nonce_str = self.get_nonce({"length": 16})
        fh_timestamp = self.get_timestamp()
        sign_string = "fhAppid{}fhNonceStr{}fhTimestamp{}{}{}".format(
            FEIHE_API_APP_ID,
            fh_nonce_str,
            fh_timestamp,
            "{}",
            FEIHE_API_APP_KEY,
        )
        return {
            "fhNonceStr": fh_nonce_str,
            "fhTimestamp": str(fh_timestamp),
            "fhSign": hashlib.md5(sign_string.encode("utf-8")).hexdigest().upper(),
        }

    def get_refresh_signature(self):
        fh_nonce_str = self.get_nonce({"length": 16})
        fh_timestamp = self.get_timestamp()
        sign_string = "fhAppidxmhfhNonceStr{}fhTimestamp{}98d9fe9b613a479dbcb111ca261e3ce1".format(
            fh_nonce_str,
            fh_timestamp,
        )
        return {
            "fhNonceStr": fh_nonce_str,
            "fhTimestamp": str(fh_timestamp),
            "fhSign": hashlib.md5(sign_string.encode("utf-8")).hexdigest().upper(),
        }

    def get_user_info(self):
        try:
            signature = self.get_signature()
            response = requests.post(
                "https://www.feihevip.com/api/starMember/getMemberInfo",
                headers={**self.headers, **signature},
                json={},
                timeout=(5, 30),
            )
            result = response.json()
            if result.get("code") == "200" and result.get("data"):
                return result.get("data")
        except Exception:
            return None
        return None

    def get_task_list(self):
        for _ in range(3):
            try:
                signature = self.get_signature()
                response = requests.get(
                    "https://www.feihevip.com/api/member/signin/getTaskList",
                    headers={**self.headers, **signature},
                    json={},
                    timeout=(5, 30),
                )
                result = response.json()
                if result.get("code") == "200" and len(result.get("data", [])) > 0:
                    return result["data"]
            except Exception:
                pass
            time.sleep(2)
        return []

    def signin(self):
        for _ in range(3):
            try:
                signature = self.get_signature()
                response = requests.post(
                    "https://www.feihevip.com/api/member/signin/sign",
                    headers={**self.headers, **signature},
                    json={},
                    timeout=(5, 30),
                )
                result = response.json()
                if result.get("code") == "200":
                    return True
            except Exception:
                pass
            time.sleep(2)
        return False

    def tofinish(self, task_type):
        for _ in range(2):
            try:
                signature = self.get_signature()
                response = requests.get(
                    "https://www.feihevip.com/api/member/signin/tofinish?taskType={}".format(task_type),
                    headers={**self.headers, **signature},
                    json={},
                    timeout=(5, 30),
                )
                result = response.json()
                if result.get("code") == "200":
                    return True
            except Exception:
                pass
            time.sleep(2)
        return False

    def complete_task(self, task_type):
        for _ in range(3):
            try:
                signature = self.get_signature()
                response = requests.get(
                    "https://www.feihevip.com/api/member/signin/completeTask?taskType={}".format(task_type),
                    headers={**self.headers, **signature},
                    json={},
                    timeout=(5, 30),
                )
                result = response.json()
                if result.get("code") == "200":
                    return True
            except Exception:
                pass
            time.sleep(2)
        return False

    def refresh_token(self):
        try:
            signature = self.get_refresh_signature()
            response = requests.get(
                "https://mom.feihe.com/program/token/refreshToken",
                headers={
                    "Host": "mom.feihe.com",
                    "token": self.token,
                    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.48(0x1800302b) NetType/4G Language/zh_CN",
                    "Referer": "https://servicewechat.com/wx4205ec55b793245e/215/page-frame.html",
                    "fhAppid": "xmh",
                    "source": "1",
                    **signature,
                },
                timeout=(5, 30),
            )
            result = response.json()
            new_token = result.get("data")
            if new_token:
                self.token = str(new_token).strip()
                self.headers["token"] = self.token
                return self.token
        except Exception:
            return None
        return None

def run_feihe_task_list(task_list, client):
    completed = 0
    for task in task_list or []:
        task_name = str(task.get("taskName") or "").strip()
        task_type = str(task.get("taskType") or "").strip()
        if not task_name or not task_type:
            continue
        if re.search(r"使用任意商品", task_name):
            continue
        client.tofinish(task_type)
        time.sleep(random.randint(2, 5))
        if client.complete_task(task_type):
            completed += 1
        time.sleep(1)
        time.sleep(random.randint(3, 6))
    return completed

def fetch_feihe_snapshot(access_token):
    client = FeiHeAuto(access_token)
    try:
        client.refresh_token()
    except Exception:
        pass
    user_info = client.get_user_info()
    if not user_info:
        return None
    base_info = user_info.get("baseInfo") or {}
    member_points = user_info.get("memberPoints") or {}
    phone = str(base_info.get("mobile") or base_info.get("fullName") or base_info.get("openId") or "").strip()
    if not phone:
        return None
    return {
        "phone": phone,
        "display_name": sanitize_text(base_info.get("nickName") or mask_phone(phone)),
        "points": member_points.get("scoreBalance", 0),
        "grade_name": sanitize_text(base_info.get("memberLevelName") or user_info.get("memberLevelName") or "飞鹤会员"),
        "new_token": client.token,
    }

def run_feihe_account(access_token):
    client = FeiHeAuto(access_token)
    user_info_before = client.get_user_info() or {}
    if not user_info_before:
        return {
            "success": False,
            "sign_success": False,
            "completed_tasks": 0,
            "earned_points": 0,
            "points_before": 0,
            "points_after": 0,
            "new_token": "",
        }
    member_points_before = user_info_before.get("memberPoints") or {}
    score_before = safe_int(member_points_before.get("scoreBalance") or 0, 0)
    sign_success = client.signin()
    task_list = client.get_task_list() or []
    completed_tasks = run_feihe_task_list(task_list, client) if task_list else 0
    new_token = client.refresh_token() or ""
    time.sleep(1)
    user_info_after = client.get_user_info() or {}
    member_points_after = user_info_after.get("memberPoints") or {}
    score_after = safe_int(member_points_after.get("scoreBalance"), score_before)
    return {
        "success": bool(sign_success or completed_tasks > 0 or score_after >= score_before),
        "sign_success": sign_success,
        "completed_tasks": completed_tasks,
        "earned_points": max(0, score_after - score_before),
        "points_before": score_before,
        "points_after": score_after,
        "new_token": new_token,
    }

def run_momclub_account(authorization):
    client = MomClubClient(authorization)
    member_info_before = client.get_member_info()
    if not member_info_before:
        return {"success": False, "message": "authorization 无效或已过期", "earned_points": 0, "completed_tasks": 0}

    points_before = safe_int(member_info_before.get("points") or 0, 0)
    run_result = client.run_all_tasks()
    time.sleep(2)
    member_info_after = client.get_member_info() or member_info_before
    points_after = safe_int(member_info_after.get("points") or points_before, points_before)
    return {
        "success": True,
        "earned_points": max(0, points_after - points_before),
        "completed_tasks": safe_int(run_result.get("completed") or 0, 0),
        "messages": run_result.get("messages") or [],
        "points_before": points_before,
        "points_after": points_after,
    }

def safe_int(value, default=0):
    try:
        return int(str(value).strip())
    except Exception:
        return default

def sanitize_text(value):
    text = str(value or "").strip()
    return text.replace("#", "-").replace("|", "-").replace("丨", "-").replace("\r", " ").replace("\n", " ")

def mask_phone(phone):
    phone = str(phone or "").strip()
    if len(phone) < 7:
        return phone
    return "{}****{}".format(phone[:3], phone[-4:])

def today_date():
    return datetime.now().date()

def read_input(prompt="", timeout=120000):
    if prompt:
        sender.reply(prompt)
    value = sender.input(timeout, 1, False)
    if value is None:
        return None
    text = str(value).strip()
    if text.lower() == "q":
        return None
    return text

def get_user_phones(user_id=None):
    user_id = user_id or userid
    raw = sg.bucketGet(BUCKET_USER, user_id) or ""
    return parse_bucket_phone_list(raw)

def save_user_phones(phones, user_id=None):
    user_id = user_id or userid
    normalized = [str(phone).strip() for phone in phones if str(phone).strip()]
    normalized = list(dict.fromkeys(normalized))
    if normalized:
        bucket_set_primary(BUCKET_USER, user_id, ",".join(normalized))
    else:
        bucket_del_all(BUCKET_USER, user_id)

def add_user_phone(phone, user_id=None):
    phones = get_user_phones(user_id)
    if phone not in phones:
        phones.append(phone)
        save_user_phones(phones, user_id)

def remove_user_phone(phone, user_id=None):
    phones = get_user_phones(user_id)
    if phone in phones:
        phones.remove(phone)
        save_user_phones(phones, user_id)

def get_token_info(phone):
    raw = bucket_get_first(BUCKET_TOKEN, phone) or ""
    parts = str(raw).split("#", 1)
    feihe_token = str(parts[0] if len(parts) > 0 else "").strip()
    authorization = str(parts[1] if len(parts) > 1 else "").strip()
    return {
        "feihe_token": feihe_token,
        "authorization": authorization,
        "display_name": mask_phone(phone),
    }

def save_project_tokens(phone, feihe_token=None, authorization=None):
    current = get_token_info(phone)
    new_feihe_token = str(current.get("feihe_token") or "").strip()
    new_authorization = str(current.get("authorization") or "").strip()
    if feihe_token is not None:
        new_feihe_token = str(feihe_token or "").strip()
    if authorization is not None:
        new_authorization = str(authorization or "").strip()
    if not new_feihe_token and not new_authorization:
        bucket_del_all(BUCKET_TOKEN, phone)
        return
    bucket_set_primary(BUCKET_TOKEN, phone, "{}#{}".format(new_feihe_token, new_authorization))

def get_owner_of_phone(phone):
    users = bucket_all_keys_merged(BUCKET_USER) or []
    for user_id in users:
        if phone in get_user_phones(user_id):
            return user_id
    return None

def get_feihe_token(phone):
    return str(get_token_info(phone).get("feihe_token") or "").strip()

def save_feihe_token(phone, access_token):
    save_project_tokens(phone, feihe_token=access_token)

def get_today_earned(phone):
    key = "{}_{}".format(phone, today_date().strftime("%Y%m%d"))
    return safe_int(sg.bucketGet("dd_xmyx_daily", key) or 0, 0)

def add_today_earned(phone, points):
    if points <= 0:
        return
    key = "{}_{}".format(phone, today_date().strftime("%Y%m%d"))
    current = get_today_earned(phone)
    sg.bucketSet("dd_xmyx_daily", key, str(current + points))

def has_project_binding(phone, project_name):
    project = str(project_name or "").strip().lower()
    token_info = get_token_info(phone)
    if project == "feihe":
        return bool(str(token_info.get("feihe_token") or "").strip())
    if project == "momclub":
        return bool(str(token_info.get("authorization") or "").strip())
    return False

def parse_bind_line(raw_text):
    text = str(raw_text or "").strip()
    if not text:
        return None
    if "#" in text:
        feihe_token, authorization = text.split("#", 1)
        feihe_token = feihe_token.strip()
        authorization = authorization.strip()
        if not feihe_token and not authorization:
            return None
        return {
            "project": "combined",
            "feihe_token": feihe_token,
            "authorization": authorization,
        }
    return {"project": "auto", "credential": text}

def is_valid_bind_item(item):
    if not item:
        return False
    if str(item.get("project") or "").strip().lower() == "combined":
        return bool(str(item.get("feihe_token") or "").strip() or str(item.get("authorization") or "").strip())
    return bool(str(item.get("credential") or "").strip())

def parse_bind_inputs(raw_text):
    items = []
    for line in str(raw_text or "").splitlines():
        item = parse_bind_line(line)
        if is_valid_bind_item(item):
            items.append(item)
    if not items:
        item = parse_bind_line(raw_text)
        if is_valid_bind_item(item):
            items.append(item)

    unique_items = []
    seen = set()
    for item in items:
        key = (
            item.get("project"),
            item.get("credential"),
            item.get("feihe_token"),
            item.get("authorization"),
        )
        if key in seen:
            continue
        seen.add(key)
        unique_items.append(item)
    return unique_items

def fetch_momclub_snapshot(authorization):
    member_info = MomClubClient(authorization).get_member_info()
    if not member_info:
        return None
    phone = str(member_info.get("mobile") or member_info.get("phone") or "").strip()
    if not phone:
        return None
    return {
        "member_id": str(member_info.get("memberId") or member_info.get("id") or member_info.get("userId") or phone),
        "phone": phone,
        "grade_name": sanitize_text(member_info.get("gradeName") or "未知等级"),
        "points": member_info.get("points", 0),
    }

def bind_or_update_momclub_account(raw_text, old_phone=None):
    authorization = str(raw_text or "").strip()
    if not authorization:
        return False, "请输入 authorization"
    snapshot = fetch_momclub_snapshot(authorization)
    if not snapshot:
        return False, "authorization 无效或已过期，请重新抓包"
    phone = snapshot["phone"]
    existing_owner = get_owner_of_phone(phone)
    if existing_owner and existing_owner != userid:
        if not old_phone or phone != old_phone:
            return False, "该账号已被其他用户绑定，请稍后重试"
    if old_phone and old_phone != phone:
        old_feihe_token = get_feihe_token(old_phone)
        bucket_del_all(BUCKET_TOKEN, old_phone)
        remove_user_phone(old_phone, userid)
        if old_feihe_token and not get_feihe_token(phone):
            save_feihe_token(phone, old_feihe_token)
    display_name = mask_phone(phone)
    existed = has_project_binding(phone, "momclub")
    save_project_tokens(phone, authorization=authorization)
    add_user_phone(phone, userid)
    return True, {
        "phone": phone,
        "display_name": display_name,
        "grade_name": snapshot["grade_name"],
        "points": snapshot["points"],
        "existed": existed,
        "sync_message": "",
    }

def bind_or_update_feihe_account(raw_text, old_phone=None):
    access_token = str(raw_text or "").strip()
    if not access_token:
        return False, "请输入飞鹤 access_token"
    snapshot = fetch_feihe_snapshot(access_token)
    if not snapshot:
        return False, "飞鹤 access_token 无效或已过期"
    phone = snapshot["phone"]
    existing_owner = get_owner_of_phone(phone)
    if existing_owner and existing_owner != userid:
        return False, "该账号已被其他用户绑定，请稍后重试"
    if old_phone and phone != old_phone:
        old_token_info = get_token_info(old_phone)
        old_auth = old_token_info.get("authorization") or ""
        bucket_del_all(BUCKET_TOKEN, old_phone)
        remove_user_phone(old_phone, userid)
        if old_auth and not get_token_info(phone).get("authorization"):
            save_project_tokens(phone, authorization=old_auth)
    existed = bool(get_feihe_token(phone))
    save_feihe_token(phone, snapshot.get("new_token") or access_token)
    add_user_phone(phone, userid)
    return True, {
        "phone": phone,
        "display_name": snapshot["display_name"] or mask_phone(phone),
        "grade_name": snapshot["grade_name"],
        "points": snapshot["points"],
        "existed": existed,
        "sync_message": "",
    }

def bind_combined_account(feihe_token, authorization, old_phone=None):
    feihe_token = str(feihe_token or "").strip()
    authorization = str(authorization or "").strip()
    if not feihe_token and not authorization:
        return False, "未提供有效的飞鹤 token 或星妈会 authorization"

    feihe_snapshot = fetch_feihe_snapshot(feihe_token) if feihe_token else None
    if feihe_token and not feihe_snapshot:
        return False, "飞鹤 access_token 无效或已过期"

    momclub_snapshot = fetch_momclub_snapshot(authorization) if authorization else None
    if authorization and not momclub_snapshot:
        return False, "星妈会 authorization 无效或已过期"

    phones = [item["phone"] for item in (feihe_snapshot, momclub_snapshot) if item]
    if not phones:
        return False, "未识别到有效账号"
    if len(set(phones)) > 1:
        return False, "飞鹤和星妈会凭证对应的手机号不一致，无法合并绑定"

    phone = phones[0]
    existing_owner = get_owner_of_phone(phone)
    if existing_owner and existing_owner != userid:
        return False, "该账号已被其他用户绑定，请稍后重试"

    existed = bool(get_feihe_token(phone) or get_token_info(phone).get("authorization"))
    if old_phone and old_phone != phone:
        bucket_del_all(BUCKET_TOKEN, old_phone)
        remove_user_phone(old_phone, userid)

    effective_feihe_token = (feihe_snapshot.get("new_token") if feihe_snapshot else None) or feihe_token or None
    save_project_tokens(phone, feihe_token=effective_feihe_token, authorization=authorization or None)
    add_user_phone(phone, userid)

    grade_name = "未知"
    points = 0
    if momclub_snapshot:
        grade_name = momclub_snapshot["grade_name"]
        points = momclub_snapshot["points"]
    elif feihe_snapshot:
        grade_name = feihe_snapshot["grade_name"]
        points = feihe_snapshot["points"]

    return True, {
        "phone": phone,
        "display_name": mask_phone(phone),
        "grade_name": grade_name,
        "points": points,
        "existed": existed,
        "sync_message": "",
    }

def bind_project_item(item, old_phone=None):
    project = str(item.get("project") or "auto").strip().lower()
    credential = str(item.get("credential") or "").strip()
    if project == "combined":
        ok, result = bind_combined_account(item.get("feihe_token"), item.get("authorization"), old_phone=old_phone)
        feihe_token = str(item.get("feihe_token") or "").strip()
        authorization = str(item.get("authorization") or "").strip()
        if feihe_token and authorization:
            project_name = "飞鹤+星妈会"
        elif feihe_token:
            project_name = "飞鹤"
        else:
            project_name = "星妈会"
        return ok, result, project_name

    if not credential:
        return False, "未提供有效凭证", ""

    if project == "momclub":
        ok, result = bind_or_update_momclub_account(credential, old_phone=old_phone)
        return ok, result, "星妈会"
    if project == "feihe":
        ok, result = bind_or_update_feihe_account(credential, old_phone=old_phone)
        return ok, result, "飞鹤"

    ok, result = bind_or_update_momclub_account(credential, old_phone=old_phone)
    if ok:
        return True, result, "星妈会"
    ok, feihe_result = bind_or_update_feihe_account(credential, old_phone=old_phone)
    if ok:
        return True, feihe_result, "飞鹤"
    return False, "未识别到有效的星妈会 authorization 或飞鹤 token", ""

def bind_account():
    raw_text = read_input(
        "=====星妈会登录=====\n"
        "支持绑定【星妈会】和【飞鹤】两个项目\n"
        "------------------\n"
        "提交方式：\n"
        "1. 同时绑定两个项目：飞鹤token#authorization\n"
        "2. 仅绑定飞鹤：飞鹤token#\n"
        "3. 仅绑定星妈会：#authorization\n"
        "4. 批量提交时每行一条，统一使用以上格式\n"
        "------------------\n"
        "回复 q 取消\n"
        "=================="
    )
    if not raw_text:
        sender.reply("✅ 已取消绑定")
        return
    bind_items = parse_bind_inputs(raw_text)
    if not bind_items:
        sender.reply("❌ 请输入有效的【飞鹤token#authorization】格式")
        return
    if len(bind_items) == 1:
        ok, result, project_name = bind_project_item(bind_items[0])
        if not ok:
            sender.reply("❌ {}".format(result))
            return
        sender.reply(
            "✅ {}{}成功\n👤 项目: {}\n📱 手机: {}\n🎖 等级: {}\n🎁 积分: {}\n{}".format(
                project_name,
                "更新" if result["existed"] else "绑定",
                project_name,
                mask_phone(result["phone"]),
                result["grade_name"],
                result["points"],
                result["sync_message"] or "可前往【星妈会管理】继续完善账号",
            )
        )
        return

    success_items = []
    fail_items = []
    for index, item in enumerate(bind_items, 1):
        ok, result, project_name = bind_project_item(item)
        if ok:
            success_items.append({
                "index": index,
                "project": project_name,
                "phone": mask_phone(result["phone"]),
                "action": "更新成功" if result["existed"] else "绑定成功",
            })
        else:
            fail_items.append({
                "index": index,
                "reason": result,
            })
    lines = [
        "=====批量登录完成=====",
        "✅ 成功: {}".format(len(success_items)),
        "❌ 失败: {}".format(len(fail_items)),
        "------------------",
    ]
    for item in success_items:
        lines.append("[{}] [{}] {} {}".format(item["index"], item["project"], item["phone"], item["action"]))
    for item in fail_items:
        lines.append("[{}] 失败: {}".format(item["index"], item["reason"]))
    lines.append("==================")
    sender.reply("\n".join(lines))

def get_momclub_summary(phone):
    token_info = get_token_info(phone)
    authorization = str(token_info.get("authorization") or "").strip()
    if not authorization:
        return {
            "bound": False,
            "display_name": mask_phone(phone),
            "grade_name": "未绑定",
            "points": "未绑定",
            "pending_tasks": "-",
            "token_status": "未绑定",
        }
    client = MomClubClient(authorization)
    member_info = client.get_member_info()
    todo_data = client.get_todo_list()
    pending_tasks = "-"
    if todo_data:
        pending_tasks = 0
        for task in todo_data.get("taskTodo", []) or []:
            extra = task.get("taskTodoExtra") or {}
            if extra.get("status") == "3":
                continue
            if extra.get("completeCount", 0) >= extra.get("completeLimit", 1):
                continue
            pending_tasks += 1
    return {
        "bound": True,
        "display_name": token_info.get("display_name") or mask_phone(phone),
        "grade_name": member_info.get("gradeName") if member_info else "未知",
        "points": member_info.get("points") if member_info else "未知",
        "pending_tasks": pending_tasks,
        "token_status": "正常" if member_info else "可能失效",
    }

def get_feihe_summary(phone):
    access_token = get_feihe_token(phone)
    if not access_token:
        return {
            "bound": False,
            "display_name": mask_phone(phone),
            "grade_name": "未绑定",
            "points": "未绑定",
            "token_status": "未绑定",
        }
    snapshot = fetch_feihe_snapshot(access_token)
    if not snapshot:
        return {
            "bound": True,
            "display_name": mask_phone(phone),
            "grade_name": "未知",
            "points": "未知",
            "token_status": "可能失效",
        }
    new_token = snapshot.get("new_token")
    if new_token and new_token != access_token:
        save_feihe_token(phone, new_token)
    return {
        "bound": True,
        "display_name": snapshot["display_name"] or mask_phone(phone),
        "grade_name": snapshot["grade_name"],
        "points": snapshot["points"],
        "token_status": "正常",
    }

def format_project_binding_text(feihe_bound, momclub_bound):
    return "飞鹤{} ｜ 星妈会{}".format("✅" if feihe_bound else "❌", "✅" if momclub_bound else "❌")

def get_account_summary(phone):
    momclub = get_momclub_summary(phone)
    feihe = get_feihe_summary(phone)
    return {
        "display_name": momclub.get("display_name") or feihe.get("display_name") or mask_phone(phone),
        "phone": mask_phone(phone), "momclub": momclub, "feihe": feihe,
        "projects_text": format_project_binding_text(feihe.get("bound"), momclub.get("bound")),
    }

def get_manage_account_rows():
    return [{
        "phone": phone, "display_phone": mask_phone(phone),
        "project_text": format_project_binding_text(has_project_binding(phone, "feihe"), has_project_binding(phone, "momclub")),
    } for phone in get_user_phones()]

def query_accounts():
    phones = get_user_phones()
    if not phones:
        sender.reply("❌ 您还没有绑定账号，请先发送【星妈会登录】")
        return
    lines = [f"=====星妈会查询=====\n📦 账号: {len(phones)} 个", "------------------"]
    for index, phone in enumerate(phones, 1):
        summary = get_account_summary(phone); momclub = summary["momclub"]; feihe = summary["feihe"]
        points = feihe.get("points") if feihe.get("bound") and feihe.get("points") not in ("未绑定", "未知") else momclub.get("points")
        lines.extend((f"【{index}】{summary['phone']} {summary['projects_text']}", f"├ 积分: {points}", f"└ 今日: +{get_today_earned(phone)}"))
    sender.reply("\n".join(lines + ["=================="]))

def delete_single_account(phone):
    confirm = read_input("=====删除账号确认=====\n📱 手机: {}\n回复 y 确认删除，回复 q 取消\n==================".format(mask_phone(phone)), 60000)
    if not confirm or confirm.lower() != "y":
        sender.reply("✅ 已取消删除")
        return
    bucket_del_all(BUCKET_TOKEN, phone)
    bucket_del_all(BUCKET_AUTH, phone)
    remove_user_phone(phone, userid)
    sender.reply("✅ 账号已删除")

def execute_account_projects(phone):
    result = {
        "phone": phone,
        "display_phone": mask_phone(phone),
        "projects": [],
        "earned_points": 0,
        "success": False,
    }

    feihe_token = get_feihe_token(phone)
    if feihe_token:
        feihe_result = run_feihe_account(feihe_token)
        if feihe_result.get("new_token"):
            save_feihe_token(phone, feihe_result.get("new_token"))
        result["projects"].append({
            "name": "飞鹤",
            "success": feihe_result.get("success", False),
            "earned_points": feihe_result.get("earned_points", 0),
            "detail": "签到{}，任务{}个，积分 +{}".format(
                "成功" if feihe_result.get("sign_success") else "失败",
                feihe_result.get("completed_tasks", 0),
                feihe_result.get("earned_points", 0),
            ),
        })
        result["earned_points"] += safe_int(feihe_result.get("earned_points", 0), 0)

    token_info = get_token_info(phone)
    authorization = str(token_info.get("authorization") or "").strip()
    if authorization:
        momclub_result = run_momclub_account(authorization)
        result["projects"].append({
            "name": "星妈会",
            "success": momclub_result.get("success", False),
            "earned_points": momclub_result.get("earned_points", 0),
            "detail": "完成任务{}个，积分 +{}".format(
                momclub_result.get("completed_tasks", 0),
                momclub_result.get("earned_points", 0),
            ),
        })
        result["earned_points"] += safe_int(momclub_result.get("earned_points", 0), 0)

    result["success"] = any(project.get("success") for project in result["projects"])
    if result["earned_points"] > 0:
        add_today_earned(phone, result["earned_points"])
    return result

def run_single_account(phone):
    if not has_project_binding(phone, "feihe") and not has_project_binding(phone, "momclub"):
        sender.reply("❌ 当前账号未绑定任何项目数据")
        return
    sender.reply("⏳ 正在执行账号任务，请稍候...")
    result = execute_account_projects(phone)
    lines = ["=====运行完成=====", f"📱 手机: {result['display_phone']}", f"💰 总收益: {result['earned_points']} 积分", "------------------"]
    lines.extend(f"• {item['name']}: {item['detail']}" for item in result["projects"])
    sender.reply("\n".join(lines + ["=================="]))

def get_all_authorized_phones():
    phones = []
    for user_id in bucket_all_keys_merged(BUCKET_USER) or []:
        phones.extend(get_user_phones(user_id))
    return list(dict.fromkeys(phones))

def run_all_accounts():
    phones = get_all_authorized_phones() if sender.isAdmin() else get_user_phones()
    if not phones:
        sender.reply("❌ 没有可运行的账号")
        return
    success = failed = earned = 0; details = []
    for phone in phones:
        if not has_project_binding(phone, "feihe") and not has_project_binding(phone, "momclub"):
            failed += 1; continue
        result = execute_account_projects(phone); earned += result["earned_points"]
        success += int(bool(result["success"])); failed += int(not result["success"])
        details.append(f"• {result['display_phone']}：" + " / ".join(f"{x['name']}(+{x['earned_points']})" for x in result["projects"]))
    sender.reply(f"=====星妈会一键运行=====\n✅ 成功: {success}\n❌ 失败: {failed}\n💰 总收益: {earned} 积分\n------------------\n" + "\n".join(details) + "\n==================")

def manage_accounts():
    rows = get_manage_account_rows()
    if not rows:
        sender.reply("❌ 暂无账号")
        return
    sender.reply("=====星妈会管理=====\n" + "\n".join(f"[{i}] {row['display_phone']} {row['project_text']}" for i, row in enumerate(rows, 1)) + "\n==================")
    choice = read_input("请输入账号序号，输入 q 退出")
    if not choice or choice.lower() == "q": return
    if not choice.isdigit() or not 1 <= int(choice) <= len(rows):
        sender.reply("❌ 序号无效"); return
    phone = rows[int(choice)-1]["phone"]
    sender.reply("[1] 运行账号\n[2] 删除账号")
    action = read_input("请选择操作")
    if action == "1": run_single_account(phone)
    elif action == "2": delete_single_account(phone)

def show_tutorial():
    sender.reply("""=====星妈会教程=====
星妈会登录：绑定或更新飞鹤/星妈会账号
星妈会查询：查询积分与项目状态
星妈会管理：运行或删除账号
星妈会一键运行：执行全部账号任务
==================""")

def cron_run_all():
    authorized_phones = get_all_authorized_phones()
    if not authorized_phones:
        return
    total_earned = 0
    success_count = 0
    fail_count = 0
    detail_lines = []
    for phone in authorized_phones:
        if not has_project_binding(phone, "feihe") and not has_project_binding(phone, "momclub"):
            fail_count += 1
            detail_lines.append("• {}：未绑定任何项目".format(mask_phone(phone)))
            continue
        run_result = execute_account_projects(phone)
        total_earned += run_result["earned_points"]
        if run_result["success"]:
            success_count += 1
        else:
            fail_count += 1
        project_labels = []
        for item in run_result["projects"]:
            project_labels.append("{}(+{})".format(item["name"], item["earned_points"]))
        detail_lines.append("• {}：{}".format(run_result["display_phone"], " / ".join(project_labels) or "无可执行项目"))
        time.sleep(random.randint(2, 5))
    sender.reply(
        "=====星妈会定时任务=====\n"
        "⏰ 时间: {}\n"
        "✅ 成功: {}\n"
        "❌ 失败: {}\n"
        "💰 总收益: {} 积分\n"
        "------------------\n"
        "{}\n"
        "==================".format(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            success_count,
            fail_count,
            total_earned,
            "\n".join(detail_lines),
        )
    )

try:
    usermessage = sender.getMessage()
except AttributeError:
    usermessage = ""

try:
    imtype = sender.getImtype()
except AttributeError:
    imtype = ""

if imtype == 'fake':
    cron_run_all()
elif not usermessage:
    sender.setContinue()
elif re.search(r"星妈会登录", usermessage):
    bind_account()
elif re.search(r"星妈会管理", usermessage):
    manage_accounts()
elif re.search(r"星妈会查询", usermessage):
    query_accounts()
elif re.search(r"星妈会一键运行", usermessage):
    run_all_accounts()
elif re.search(r"星妈会教程", usermessage):
    show_tutorial()
else:
    sender.setContinue()
