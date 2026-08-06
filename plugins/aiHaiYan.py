# [title: 爱海盐]
# [name: aiHaiYan]
# [language: python]
# [class: 任务]
# [author: 8165799]
# [version: v1.3.1]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^爱海盐(登录|登陆|查询|管理|教程)?$|^登(录|陆)爱海盐$|^(查询|管理)爱海盐$]
# [icon: https://api.iconify.design/lucide:bot.svg]
# [description: 爱海盐账号登录、查询、面板同步与管理]
# [depe: ["pycryptodome","requests"]]
import asyncio as _sg_asyncio
import os as _sg_os
import time as _sg_time
import types as _sg_types
from threading import Thread as _sg_Thread
from sillygirl import Adapter as _SGAdapter, Bucket as _SGBucket, Sender as _SGSender, sender as _sg_sender, plugin

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

config = plugin.Form({
    'aihaiyan_panel_type': plugin.Form.string().title('对接面板类型').default('').description('qinglong=青龙面板 daidai=呆呆面板'),
    'aihaiyan_aihaiyan_qlname': plugin.Form.string().title('对接系统配置').default('').description('青龙:URL丨ID丨Secret 呆呆:URL丨Key丨Secret'),
    'aihaiyan_aihaiyan_osname': plugin.Form.string().title('系统变量名').default('').description('系统容器内变量名(默认为AiHaiYan)'),
    'aihaiyan_enable_remark': plugin.Form.boolean().title('启用备注功能').default(False).description('是否启用账号备注功能'),
    'aihaiyan_auth_appkey': plugin.Form.string().title('H5 AppKey').default('').description('爱海盐H5接口签名AppKey'),
    'aihaiyan_h5_sign_secret': plugin.Form.string().title('H5 SignSecret').default('').description('爱海盐H5接口签名Secret'),
})
_CONFIG_FIELD_MAP = {
    ('aihaiyan', 'panel_type'): 'aihaiyan_panel_type',
    ('aihaiyan', 'aihaiyan_qlname'): 'aihaiyan_aihaiyan_qlname',
    ('aihaiyan', 'aihaiyan_osname'): 'aihaiyan_aihaiyan_osname',
    ('aihaiyan', 'enable_remark'): 'aihaiyan_enable_remark',
    ('aihaiyan', 'auth_appkey'): 'aihaiyan_auth_appkey',
    ('aihaiyan', 'h5_sign_secret'): 'aihaiyan_h5_sign_secret',
}

import re
import ast
from datetime import datetime, timedelta
import urllib.parse
import gzip
import requests
import time
import hashlib
import hmac
import logging
import base64
import warnings
import random
import uuid
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.error import HTTPError, URLError
from urllib.request import Request, build_opener

warnings.filterwarnings('ignore', message='Unverified HTTPS request')
requests.packages.urllib3.disable_warnings()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('aihaiyan_plugin')

REQUEST_TIMEOUT = 30
MAINTENANCE_CK_MAX_WORKERS = 8

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = str(sender.getUserID())
usermessage = sender.getMessage()

_RUNTIME_BUCKET = "plugin_push_runtime"
_RUNTIME_KEY = "爱海盐"
try:
    current_imtype = str(sender.getImtype() or "")
except:
    current_imtype = ""
if current_imtype and current_imtype.lower() not in ["fake", "cron"]:
    try: sg.bucketSet(_RUNTIME_BUCKET, _RUNTIME_KEY + "_sender", str(senderID))
    except: pass
    try: sg.bucketSet(_RUNTIME_BUCKET, _RUNTIME_KEY + "_imtype", current_imtype)
    except: pass

def getusercontent():
    panel=(sg.bucketGet('aihaiyan','panel_type') or 'qinglong').lower();raw=sg.bucketGet('aihaiyan','aihaiyan_qlname') or ''
    if not raw:
        sender.reply('❌ 请先配置青龙或呆呆面板信息');raise SystemExit
    return {'panel_type':panel,'env_name':sg.bucketGet('aihaiyan','aihaiyan_osname') or 'AiHaiYan','env_qlconfig':raw,'randommanagecommand':'爱海盐管理','randomquerycommand':'爱海盐查询','randomsigncommand':'爱海盐登录','enable_remark':str(sg.bucketGet('aihaiyan','enable_remark') or 'false').lower()=='true'}

config = getusercontent()






def mask_account(account):
    account = str(account)
    return account[:3] + "****" + account[-3:] if len(account) >= 11 else account

def get_account_display(account, remark=""):
    remark = str(remark or "").strip()
    return remark if remark else mask_account(account)

def parse_aihaiyan_credential(raw, default_remark=""):
    text = str(raw or "").strip()
    if not text or "#" not in text:
        return "", "", "", "格式错误: 应为 手机号#密码"

    parts = [part.strip() for part in text.split("#")]
    if len(parts) >= 3 and re.fullmatch(r"\d{11}", parts[1] or ""):
        remark = parts[0] or default_remark
        phone = parts[1]
        password = "#".join(parts[2:]).strip()
    else:
        remark = default_remark
        phone, password = text.split("#", 1)
        phone = phone.strip()
        password = password.strip()

    if not re.fullmatch(r"\d{11}", phone or ""):
        return "", "", "", "格式错误: 手机号应为11位数字"
    if not password:
        return "", "", "", "格式错误: 密码为空"
    return phone, password, str(remark or "").strip()[:20], ""

def is_definitive_auth_failure(message):
    msg = str(message or "").lower()
    keywords = [
        "账号或密码", "密码错误", "用户名或密码", "手机号或密码",
        "credential", "invalid password", "invalid account", "unauthorized"
    ]
    return any(key.lower() in msg for key in keywords)

def get_lottery_record_data():
    key = sg.bucketGet('aihaiyan', 'record_key') or 'aihaiyan_lottery_record'
    raw = sg.bucketGet('aihaiyan_lottery_record', key) or '{}'
    try:
        data = json.loads(raw)
        return data if isinstance(data, dict) else {}
    except Exception as e:
        logger.warning(f"读取爱海盐抽奖记录桶失败 {key}: {e}")
        return {}

def normalize_prize_text(prize):
    text = str(prize or "").strip()
    if not text:
        return ""
    if "：" in text:
        text = text.split("：", 1)[1].strip()
    elif ":" in text:
        text = text.split(":", 1)[1].strip()
    return text

def get_today_prize_record(phone):
    today_key = time.strftime("%Y-%m-%d")
    phone = str(phone or "").strip()
    data = get_lottery_record_data()
    today_data = data.get(today_key, {})
    try:
        if isinstance(today_data, dict):
            acc_data = today_data.get(phone)
            if not isinstance(acc_data, dict):
                return None
            prizes = [str(x).strip() for x in (acc_data.get("prizes") or []) if str(x).strip()]
            if not prizes:
                prizes = [normalize_prize_text(x) for x in (acc_data.get("lottery_results") or []) if normalize_prize_text(x)]
            return {"path": "bucket:aihaiyan_lottery_record", "read_done": acc_data.get("read_done", 0), "sign": acc_data.get("sign", ""), "prizes": prizes}
        if isinstance(today_data, list) and phone in today_data:
            return {"path": "bucket:aihaiyan_lottery_record", "read_done": 0, "sign": "", "prizes": []}
    except Exception as e:
        logger.warning(f"读取爱海盐抽奖记录失败: {e}")
    return None


def encrypt_token(token):
    try:
        return base64.b64encode(token.encode()).decode()
    except:
        return token

def decrypt_token(encrypted_token):
    try:
        return base64.b64decode(encrypted_token.encode()).decode()
    except:
        return encrypted_token

CLIENT_ID = "10018"
PASSPORT_HOST = "https://passport.tmuyun.com"
VAPP_HOST = "https://vapp.tmuyun.com"
H5_API_HOST = "https://ya.iyunxh.com/api"
H5_API_FALLBACK_HOST = "https://yapi.y-h5.iyunxh.com/api"
H5_ORIGIN = "https://haiyan.y-h5.iyunxh.com"
TENANT_ID = "60"
AUTH_APPKEY = ""
H5_SIGN_SECRET = ""
AIHAIYAN_PRIZE_ACTIVITY_ID = "d45e103026692d01667e08"
AIHAIYAN_PRIZE_MODULE_ID = "40602"
RSA_PUBLIC_KEY = (
    "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQD6XO7e9YeAOs+cFqwa7ETJ+WXizPqQeXv68i5vqw9pFREsrqiBTRcg7wB0"
    "RIp3rJkDpaeVJLsZqYm5TW7FWx/iOiXFc+zCPvaKZric2dXCw27EvlH5rq+zwIPDAJHGAfnn1nmQH7wR3PCatEIb8pz5GFlTHMlluw4ZYmnOwg+thwIDAQAB"
)

def now_ms():
    return int(time.time() * 1000)

def md5(value):
    return hashlib.md5(str(value).encode()).hexdigest()

def randstr(length=32):
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    return "".join(random.choice(chars) for _ in range(length))

def js_quote(value):
    value = str(value)
    return (
        urllib.parse.quote(value, safe="")
        .replace("+", "+")
        .replace("~", "%7E")
        .replace("!", "%21")
        .replace("'", "%27")
        .replace("(", "%28")
        .replace(")", "%29")
        .replace("*", "%2A")
    )

def form_string(params):
    return "&".join(f"{key}={js_quote(value)}" for key, value in params.items())

class AiHaiYanClient:
    def __init__(self, token_str):
        self.token = token_str.strip()
        self.phone = ""
        self.password = ""
        self.uid = ""
        self.aliases = []
        self.session = requests.Session()
        self.session_id = ""
        self.account_id = ""
        self.account_info = {}
        self.api_dt = ""
        self.access_token = ""
        self.access_user_id = "0"
        self.h5_api_host = H5_API_HOST
        self.app_ua = "Mozilla/5.0 (Linux; Android 11; 21091116AC Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.85 Mobile Safari/537.36;xsb_aihaiyan;xsb_aihaiyan;3.0.61.0;native_app;6.12.0"
        self.common_ua = f"3.0.61.0;{uuid.uuid4()};Xiaomi M2011K2C;Android;11;Release;6.12.0"
        self._parse_token()

    def _parse_token(self):
        parts = self.token.split('#')
        if len(parts) >= 2:
            self.phone = parts[-2].strip()
            self.password = parts[-1].strip()
        else:
            self.phone = self.token
        self.uid = self.phone

    def _http_json(self, method, url, headers=None, body_str=None, timeout=10):
        payload = body_str.encode("utf-8") if body_str else None
        req = Request(url=url, data=payload, method=method.upper())
        if headers:
            for k, v in headers.items():
                req.add_header(k, v)
        opener = build_opener()
        with opener.open(req, timeout=timeout) as response:
            raw = response.read()
            if response.headers.get("Content-Encoding", "").lower() == "gzip":
                raw = gzip.decompress(raw)
            return json.loads(raw.decode("utf-8", errors="replace"))

    def rsa_encrypt_b64(self, value):
        from Crypto.Cipher import PKCS1_v1_5
        from Crypto.PublicKey import RSA
        key = RSA.import_key(base64.b64decode(RSA_PUBLIC_KEY))
        cipher = PKCS1_v1_5.new(key)
        return base64.b64encode(cipher.encrypt(value.encode())).decode()

    def login(self):
        try:
            pass
        except ImportError:
            return False, "缺少依赖，请检查配置执行: pip3 install pycryptodome"

        try:
            init_data = self.vapp_post("/api/account/init")
            self.session_id = (init_data or {}).get("data", {}).get("session", {}).get("id", "")
            if not self.session_id:
                return False, "获取session失败"

            init_res = self._requests_json(
                "GET",
                f"{PASSPORT_HOST}/web/init?client_id={CLIENT_ID}",
                headers={
                    "Connection": "Keep-Alive",
                    "Cache-Control": "no-cache",
                    "X-REQUEST-ID": str(uuid.uuid4()),
                    "Accept-Encoding": "gzip",
                    "user-agent": self.app_ua,
                },
            )

            signature_key = init_res.get("data", {}).get("client", {}).get("signature_key", "")
            if not signature_key:
                return False, "获取signature_key失败"

            encrypted_password = self.rsa_encrypt_b64(self.password)
            req_id = str(uuid.uuid4())
            sign_body = f"client_id={CLIENT_ID}&password={encrypted_password}&phone_number={self.phone}"
            sign_text = f"post%%/web/oauth/credential_auth?{sign_body}%%{req_id}%%"
            signature = hmac.new(signature_key.encode(), sign_text.encode(), hashlib.sha256).hexdigest()
            body = f"client_id={CLIENT_ID}&password={urllib.parse.quote(encrypted_password, safe='')}&phone_number={self.phone}"

            headers = {
                "X-REQUEST-ID": req_id,
                "X-SIGNATURE": signature,
                "Cache-Control": "no-cache",
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                "Accept-Encoding": "gzip",
                "user-agent": self.app_ua
            }

            auth = self._requests_json("POST", f"{PASSPORT_HOST}/web/oauth/credential_auth", headers=headers, data=body)
            if not auth or not auth.get("data"):
                return False, auth.get("message", "账号或密码错误")

            code = auth["data"]["authorization_code"]["code"]

            login_data = self.vapp_post("/api/zbtxz/login", f"check_token=&code={code}&token=&type=-1&union_id=")
            account_info = login_data.get("data", {}).get("account", {})
            session_info = login_data.get("data", {}).get("session", {})
            self.account_info = account_info
            self.session_id = session_info.get("id", self.session_id)
            self.account_id = str(session_info.get("account_id", "") or account_info.get("id", ""))
            if not self.session_id:
                return False, "登录未返回session"
            nickname = account_info.get("nick_name", f"用户_{self.phone[-4:]}")
            return True, nickname
        except (HTTPError, URLError, TimeoutError, requests.RequestException) as e:
            return None, f"网络异常: {e}"
        except Exception as e:
            return False, str(e)

    def _requests_json(self, method, url, headers=None, data=None, json_data=None, timeout=15):
        response = self.session.request(
            method.upper(),
            url,
            headers=headers or {},
            data=data,
            json=json_data,
            timeout=timeout,
            verify=False,
        )
        text = response.text
        if response.status_code >= 400:
            raise RuntimeError(f"HTTP {response.status_code}: {text[:120]}")
        return response.json()

    def h5_signature(self):
        nonce = randstr(32)
        timestamp = now_ms()
        sign_secret = sg.bucketGet("aihaiyan", "h5_sign_secret") or H5_SIGN_SECRET
        if not sign_secret:
            raise RuntimeError("未配置爱海盐H5 SignSecret")
        signature = md5(f"haiyan{nonce}{timestamp}{sign_secret}")
        return f"haiyan;{nonce};{timestamp};{signature}"

    def h5_headers(self, authed=True, json_body=False):
        headers = {
            "Connection": "keep-alive",
            "Access-T-Id-In": "69",
            "User-Agent": self.app_ua,
            "Access-Api-Unique-Token": "1",
            "Access-Api-Dt": self.api_dt or str(now_ms()),
            "Access-T-Id": "69",
            "Accept": "*/*",
            "Origin": H5_ORIGIN,
            "X-Requested-With": "com.hoge.android.app.haiyan",
            "Referer": H5_ORIGIN + "/",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }
        if authed:
            headers.update({
                "Access-User-Id": self.access_user_id,
                "Access-Api-Signature": self.h5_signature(),
                "Access-Wxclient-Type": "wx_app",
                "Access-Token": self.access_token,
            })
        if json_body:
            headers["Content-Type"] = "application/json"
        return headers

    def vapp_signature(self, path):
        req_id = str(uuid.uuid4())
        timestamp = str(now_ms())
        sign_path = path.split("?", 1)[0]
        raw = f"{sign_path}&&{self.session_id}&&{req_id}&&{timestamp}&&FR*r!isE5W&&{TENANT_ID}"
        return req_id, timestamp, hashlib.sha256(raw.encode()).hexdigest()

    def vapp_get(self, path):
        req_id, timestamp, signature = self.vapp_signature(path)
        headers = {
            "Connection": "Keep-Alive",
            "X-TIMESTAMP": timestamp,
            "X-SESSION-ID": self.session_id,
            "X-REQUEST-ID": req_id,
            "X-SIGNATURE": signature,
            "X-TENANT-ID": TENANT_ID,
            "X-ACCOUNT-ID": self.account_id,
            "Cache-Control": "no-cache",
            "Accept-Encoding": "gzip",
            "user-agent": self.common_ua,
        }
        return self._requests_json("GET", VAPP_HOST + path, headers=headers)

    def vapp_post(self, path, body=None):
        req_id, timestamp, signature = self.vapp_signature(path)
        headers = {
            "Connection": "Keep-Alive",
            "X-TIMESTAMP": timestamp,
            "X-SESSION-ID": self.session_id,
            "X-REQUEST-ID": req_id,
            "X-SIGNATURE": signature,
            "X-TENANT-ID": TENANT_ID,
            "X-ACCOUNT-ID": self.account_id,
            "Cache-Control": "no-cache",
            "Accept-Encoding": "gzip",
            "user-agent": self.common_ua,
        }
        if body is not None:
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        return self._requests_json("POST", VAPP_HOST + path, headers=headers, data=body)

    def h5_request(self, method, path, authed=True, json_body=False, json_data=None, data=None):
        hosts = []
        for host in [self.h5_api_host, H5_API_HOST, H5_API_FALLBACK_HOST]:
            if host and host not in hosts:
                hosts.append(host)
        last_error = None
        for host in hosts:
            try:
                result = self._requests_json(
                    method,
                    host + path,
                    headers=self.h5_headers(authed=authed, json_body=json_body),
                    data=data,
                    json_data=json_data,
                )
                self.h5_api_host = host
                return result
            except Exception as e:
                last_error = e
                continue
        raise last_error or RuntimeError("H5请求失败")

    def h5_get(self, path):
        return self.h5_request("GET", path)

    def find_buoy_id(self, pattern):
        data = self.vapp_get("/api/buoy/list")
        text = json.dumps(data or {}, ensure_ascii=False, separators=(",", ":"))
        match = re.search(pattern, text)
        return match.group(1) if match else ""

    def init_h5(self):
        if self.access_token and self.access_user_id != "0":
            return True
        if not self.session_id:
            return False

        dt = self.h5_request("GET", "/aosbase/_auth_dt", authed=False)
        dt_data = (dt or {}).get("data", "")
        self.api_dt = str(dt_data)[32:68]
        if not self.api_dt:
            return False

        account_info = self.account_info or {}
        payload = {
            "app_user_token": self.session_id,
            "appid": "haiyan",
            "noncestr": randstr(6),
            "phone": self.phone,
            "portrait_url": account_info.get("image_url", ""),
            "timestamp": str(int(time.time())),
            "user_id": account_info.get("id", self.account_id),
            "user_name": account_info.get("nick_name", ""),
            "wx_openid": "",
            "wx_unionid": "",
        }
        auth_appkey = sg.bucketGet("aihaiyan", "auth_appkey") or AUTH_APPKEY
        if not auth_appkey:
            raise RuntimeError("未配置爱海盐H5 AppKey")
        payload["signature"] = md5(form_string(payload) + f"&appkey={auth_appkey}")
        auth_user = self.h5_request("POST", "/aosbase/_auth_appuserinit", json_body=True, json_data=payload)
        auth_data = (auth_user or {}).get("data", {})
        self.access_token = auth_data.get("access_token", "")
        self.access_user_id = str(auth_data.get("data", {}).get("user_id", "0"))
        return bool(self.access_token and self.access_user_id != "0")

    def get_lottery_query_targets(self):
        if not self.init_h5():
            return []
        targets = []
        seen = set()

        def add_target(lottery_id, label):
            lottery_id = str(lottery_id or "").strip()
            if not lottery_id or lottery_id in seen:
                return
            seen.add(lottery_id)
            module_id = ""
            try:
                detail = self.h5_get(f"/aoslottery/_ac_detail?id={lottery_id}") or {}
                module_id = str((detail.get("data") or {}).get("m_id") or "")
            except Exception as e:
                logger.warning(f"获取爱海盐{label}详情失败: {e}")
            targets.append({
                "activity_id": lottery_id,
                "module_id": module_id or AIHAIYAN_PRIZE_MODULE_ID,
                "label": label,
            })

        try:
            study_id = self.find_buoy_id(r"/module-study/home/home\?hide_back=1&id=([a-zA-Z0-9]+)")
            if study_id:
                detail = self.h5_get(f"/aoslearnfoot/_ac_detail?id={study_id}") or {}
                other_set = (detail.get("data") or {}).get("other_set", "{}")
                lottery_id = json.loads(other_set or "{}").get("lottery", {}).get("id")
                add_target(lottery_id, "阅读抽奖")
        except Exception as e:
            logger.warning(f"动态获取阅读抽奖ID失败: {e}")

        try:
            sign_id = self.find_buoy_id(r"/module-signin/home/home\?hide_back=1&id=([a-zA-Z0-9]+)")
            if sign_id:
                detail = self.h5_get(f"/aossignin/_ac_detail?id={sign_id}") or {}
                text = json.dumps(detail or {}, ensure_ascii=False, separators=(",", ":"))
                match = re.search(r"/module-lottery/home/home\?hide_back=1&id=([a-zA-Z0-9]+)", text)
                if match:
                    add_target(match.group(1), "签到抽奖")
        except Exception as e:
            logger.warning(f"动态获取签到抽奖ID失败: {e}")

        if not targets:
            activity_id = sg.bucketGet('aihaiyan', 'prize_activity_id') or AIHAIYAN_PRIZE_ACTIVITY_ID
            module_id = sg.bucketGet('aihaiyan', 'prize_module_id') or AIHAIYAN_PRIZE_MODULE_ID
            targets.append({"activity_id": activity_id, "module_id": module_id, "label": "抽奖"})
        return targets

    def query_today_prizes(self):
        today = datetime.now().strftime("%Y-%m-%d")
        prizes = []
        errors = []
        targets = self.get_lottery_query_targets()
        if not targets:
            return None, "未获取到抽奖活动"
        for target in targets:
            try:
                path = (
                    f"/aoslottery/act_user"
                    f"?offset=0&count=50&activity_id={target['activity_id']}&module_id={target['module_id']}"
                )
                data = self.h5_get(path)
                if not isinstance(data, dict):
                    errors.append(f"{target['label']}响应异常")
                    continue
                rows = data.get("data") or []
                if not isinstance(rows, list):
                    errors.append(data.get("msg") or f"{target['label']}数据异常")
                    continue
                for row in rows:
                    if not isinstance(row, dict):
                        continue
                    created_at = str(row.get("created_at") or row.get("createdAt") or "")
                    if created_at and not created_at.startswith(today):
                        continue
                    title = str(row.get("title") or row.get("goods_title") or "").strip()
                    if not title:
                        value = str(row.get("value") or "").strip()
                        title = f"{value}积分" if value else ""
                    if title:
                        prizes.append(title)
            except Exception as e:
                errors.append(f"{target.get('label', '抽奖')}:{str(e)[:30]}")
        if errors and not prizes:
            return None, "；".join(errors[:2])
        return prizes, ""

    def verify_ck(self):
        success, msg = self.login()
        if success is None:
            return True
        if success:
            return True
        return not is_definitive_auth_failure(msg)

    def get_info(self):
        prize_record = get_today_prize_record(self.phone)
        if prize_record:
            prizes = prize_record.get("prizes") or []
            prize_str = "、".join(prizes) if prizes else "无"
            record_msg = f"✅ 青龙记录已匹配\n🎁 今日奖品: {prize_str}"
            return True, True, f"用户_{self.phone[-4:]}", record_msg

        success, result = self.login()
        if success is None:
            return False, True, "未知", result
        if success:
            record_msg = "✅ 登录验证成功"
            try:
                prizes, prize_err = self.query_today_prizes()
                if prizes is not None:
                    prize_str = "、".join(prizes) if prizes else "无"
                    record_msg += f"\n🎁 今日奖品: {prize_str}"
                else:
                    record_msg += f"\nℹ️ 今日奖品: 查询失败({str(prize_err)[:30]})"
            except Exception as e:
                prize_record = get_today_prize_record(self.phone)
                if prize_record:
                    prizes = prize_record.get("prizes") or []
                    prize_str = "、".join(prizes) if prizes else "无"
                    record_msg += f"\n🎁 今日奖品: {prize_str}"
                else:
                    record_msg += f"\nℹ️ 今日奖品: 查询异常({str(e)[:30]})"
            return True, True, result, record_msg
        else:
            return True, False, "未知", f"登录失败: {result}"

    def check_info(self):
        safe_phone = mask_account(self.phone)
        nickname = f"海盐_{safe_phone}"
        final_token = f"{self.phone}#{self.password}"

        return {
            "nickname": nickname,
            "phone": self.phone,
            "acc_key": self.phone,
            "acc_type": "phone",
            "aliases": [self.phone],
            "legacy_key": hashlib.md5(self.token.encode()).hexdigest()[:8],
            "final_token": final_token
        }

class RemarkManager:
    @staticmethod
    def get_account_remark(user_id, account_id):
        try:
            remark_data = sg.bucketGet(bucket='aihaiyan_remarks', key=f'{user_id}_{account_id}')
            return str(remark_data) if remark_data else ""
        except: return ""

    @staticmethod
    def set_account_remark(user_id, account_id, remark):
        try:
            remark_clean = str(remark).strip()[:20]
            if remark_clean:
                sg.bucketSet(bucket='aihaiyan_remarks', key=f'{user_id}_{account_id}', value=remark_clean)
                return remark_clean
            return ""
        except: return ""

    @staticmethod
    def get_all_remarks(user_id):
        try:
            accounts = AccountManager.get_accounts(user_id)
            remarks = {}
            for account in accounts:
                remark = RemarkManager.get_account_remark(user_id, account)
                if remark: remarks[str(account)] = remark
            return remarks
        except: return {}

    @staticmethod
    def delete_account_remark(user_id, account_id):
        try:
            sg.bucketDel(bucket='aihaiyan_remarks', key=f'{user_id}_{account_id}')
            return True
        except: return False

class AccountManager:
    @staticmethod
    def get_accounts(user_id):
        try:
            value = sg.bucketGet(bucket='aihaiyan_user', key=str(user_id))
            if not value: return []
            if value.startswith('[') and value.endswith(']'):
                try:
                    accounts = ast.literal_eval(value)
                    if isinstance(accounts, (list, tuple, set)):
                        return [str(x) for x in list(dict.fromkeys(accounts))]
                except: pass
            return [str(value)]
        except: return []

    @staticmethod
    def add_account(user_id, account):
        try:
            account = str(account)
            accounts = AccountManager.get_accounts(user_id)
            if account not in accounts:
                accounts.append(account)
                sg.bucketSet(bucket='aihaiyan_user', key=str(user_id), value=str(accounts))
                return True
            return False
        except: return False

    @staticmethod
    def remove_account(user_id, account):
        try:
            account = str(account)
            accounts = AccountManager.get_accounts(user_id)
            if account in accounts:
                accounts.remove(account)
                if accounts:
                    sg.bucketSet(bucket='aihaiyan_user', key=str(user_id), value=str(accounts))
                else:
                    sg.bucketDel(bucket='aihaiyan_user', key=str(user_id))
                return True
            return False
        except: return False

    @staticmethod
    def update_account_token(account, token):
        try:
            encrypted_token = encrypt_token(str(token))
            sg.bucketSet(bucket='aihaiyan_token', key=str(account), value=encrypted_token)
            return True
        except: return False

    @staticmethod
    def get_token(account):
        try:
            enc = sg.bucketGet(bucket='aihaiyan_token', key=str(account))
            return decrypt_token(enc) if enc else None
        except: return None

    @staticmethod
    def get_all_users():
        try:
            users = sg.bucketAllKeys(bucket='aihaiyan_user')
            user_list = []
            for user in users:
                accounts = AccountManager.get_accounts(user)
                if accounts: user_list.append(str(user))
            return user_list
        except: return []

    @staticmethod
    def migrate_account(user_id, old_account, new_account, new_token, remark=""):
        try:
            old_account = str(old_account)
            new_account = str(new_account)
            if not old_account or not new_account or old_account == new_account:
                return False

            accounts = AccountManager.get_accounts(user_id)
            if old_account not in accounts:
                return False

            old_vip = '2099-12-31'
            new_vip = '2099-12-31'
            if old_vip and (not new_vip or str(old_vip) > str(new_vip)):
                True

            old_bind_date = sg.bucketGet(bucket='aihaiyan_bind_date', key=old_account)
            if old_bind_date and not sg.bucketGet(bucket='aihaiyan_bind_date', key=new_account):
                sg.bucketSet(bucket='aihaiyan_bind_date', key=new_account, value=old_bind_date)

            if config['enable_remark']:
                old_remark = RemarkManager.get_account_remark(user_id, old_account)
                final_remark = remark or old_remark
                if final_remark:
                    RemarkManager.set_account_remark(user_id, new_account, final_remark)
                RemarkManager.delete_account_remark(user_id, old_account)

            new_accounts = []
            for acc in accounts:
                if acc == old_account:
                    acc = new_account
                if acc not in new_accounts:
                    new_accounts.append(acc)
            sg.bucketSet(bucket='aihaiyan_user', key=str(user_id), value=str(new_accounts))

            AccountManager.update_account_token(new_account, new_token)
            try: sg.bucketDel(bucket='aihaiyan_token', key=old_account)
            except: pass
            try:
                pass
            except: pass
            return True
        except Exception as e:
            logger.error(f"Account migrate failed: {e}")
            return False

    @staticmethod
    def find_migration_source(user_id, new_account, aliases=None, acc_type="", legacy_key=""):
        try:
            new_account = str(new_account)
            legacy_key = str(legacy_key or "")
            aliases = [str(x) for x in (aliases or []) if str(x)]

            new_ids = set(aliases)
            if acc_type != "token_md5":
                new_ids.add(new_account)
            if legacy_key:
                new_ids.discard(legacy_key)

            for old_account in AccountManager.get_accounts(user_id):
                old_account = str(old_account)
                if old_account == new_account:
                    continue
                if old_account in new_ids:
                    return old_account

                old_token = AccountManager.get_token(old_account)
                if not old_token:
                    continue

                old_client = AiHaiYanClient(old_token)
                old_info = old_client.check_info()
                old_ids = set(old_info.get('aliases', []))
                if old_info.get('acc_type') != "token_md5":
                    old_ids.add(str(old_info.get('acc_key', "")))
                old_legacy = str(old_info.get('legacy_key', ""))
                if old_legacy:
                    old_ids.discard(old_legacy)

                if new_ids and old_ids and (new_ids & old_ids):
                    return old_account
            return ""
        except Exception as e:
            logger.error(f"Find migration source failed: {e}")
            return ""

class SystemAPI:
    def __init__(self):
        self.enabled = False
        self.panel_type = config.get('panel_type', 'qinglong')
        ql_config = config['env_qlconfig']
        try:
            if not ql_config: raise ValueError("对接配置为空")
            qllist = ql_config.split('丨')
            if len(qllist) != 3: raise ValueError("对接配置格式错误")
            self.QLurl = qllist[0].strip().rstrip('/')
            self.ClientID = qllist[1].strip()
            self.ClientSecret = qllist[2].strip()

            if self.panel_type == 'daidai':
                self.access_token = self._get_daidai_token()
            else:
                self.qltoken = self._get_ql_token()
            self.enabled = True
        except Exception as e:
            logger.error(f"系统初始化失败: {e}")

    def _get_ql_token(self):
        try:
            url = f"{self.QLurl}/open/auth/token?client_id={self.ClientID}&client_secret={self.ClientSecret}"
            response = requests.get(url, timeout=10, verify=False)
            if response.status_code == 200:
                return response.json()['data']['token']
            raise Exception("获取青龙Token失败")
        except Exception: raise

    def _get_daidai_token(self):
        try:
            url = f"{self.QLurl}/api/open-api/token"
            data = {"app_key": self.ClientID, "app_secret": self.ClientSecret}
            response = requests.post(url, json=data, timeout=10, verify=False)
            if response.status_code == 200:
                return response.json()['data']['access_token']
            raise Exception("获取呆呆Token失败")
        except Exception: raise

    def get_all_envs(self):
        if not self.enabled: return []
        try:
            if self.panel_type == 'daidai':
                url = f"{self.QLurl}/api/envs?keyword={config['env_name']}&page_size=9999"
                headers = {"Authorization": f"Bearer {self.access_token}", "accept": "application/json"}
                response = requests.get(url, headers=headers, timeout=10, verify=False)
                if response.status_code == 200:
                    return response.json().get('data', [])
                return []
            else:
                url = f"{self.QLurl}/open/envs"
                headers = {"Authorization": f"Bearer {self.qltoken}", "accept": "application/json"}
                response = requests.get(url, headers=headers, timeout=10, verify=False)
                if response.status_code == 200:
                    return response.json()['data']
                return []
        except: return []

    def _env_id(self, env):
        return env.get('id') if env.get('id') is not None else env.get('_id')

    def _env_value_tokens(self, value):
        return [x.strip() for x in re.split(r'[&\n]+', str(value or '')) if x.strip()]

    def _is_aggregate_value(self, value):
        return len(self._env_value_tokens(value)) > 1

    def _phone_from_token(self, token):
        token = str(token or '').strip()
        return token.split('#', 1)[0].strip() if token else ''

    def _env_matches_account(self, env, phone='', token='', include_aggregate=False):
        value = str(env.get('value') or '').strip()
        remarks = str(env.get('remarks') or env.get('remark') or '')
        phone = str(phone or '').strip()
        token = str(token or '').strip()
        tokens = self._env_value_tokens(value)

        if not include_aggregate and len(tokens) > 1:
            return False
        if token and (value == token or (include_aggregate and token in tokens)):
            return True
        if phone:
            if len(tokens) <= 1 and self._phone_from_token(value) == phone:
                return True
            if f"账号:{phone}" in remarks or f"账号：{phone}" in remarks:
                return True
        return False

    def find_env(self, phone=None, token=None):
        if not self.enabled: return None
        try:
            for env in self.get_all_envs():
                if env.get('name') != config['env_name']:
                    continue
                if self._env_matches_account(env, phone=phone, token=token):
                    return self._env_id(env)
            return None
        except: return None

    def _delete_env_id(self, env_id):
        if env_id is None:
            return False
        if self.panel_type == 'daidai':
            url = f"{self.QLurl}/api/envs/{env_id}"
            headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
            requests.delete(url, headers=headers, timeout=10, verify=False)
        else:
            url = f"{self.QLurl}/open/envs"
            headers = {"Authorization": f"Bearer {self.qltoken}", "Content-Type": "application/json"}
            requests.delete(url, headers=headers, json=[env_id], timeout=10, verify=False)
        return True

    def _cleanup_duplicate_envs(self, keep_id=None):
        try:
            keep_id = str(keep_id) if keep_id is not None else ""
            for env in self.get_all_envs():
                if env.get('name') != config['env_name']:
                    continue
                env_id = self._env_id(env)
                if keep_id and str(env_id) == keep_id:
                    continue
                self._delete_env_id(env_id)
        except Exception as e:
            logger.warning(f"清理重复面板变量失败: {e}")

    def _cleanup_envs(self, active_items=None, delete_phones=None):
        active_items = active_items or {}
        delete_phones = {str(x) for x in (delete_phones or []) if str(x)}
        kept_phones = set()
        try:
            for env in self.get_all_envs():
                if env.get('name') != config['env_name']:
                    continue
                env_id = self._env_id(env)
                value = str(env.get('value') or '').strip()
                matched_phone = ''

                for phone, item in active_items.items():
                    if self._env_matches_account(env, phone=phone, token=item.get('token', '')):
                        matched_phone = str(phone)
                        break

                should_delete = False
                if self._is_aggregate_value(value):
                    should_delete = True
                elif any(self._env_matches_account(env, phone=phone, include_aggregate=True) for phone in delete_phones):
                    should_delete = True
                elif active_items and not matched_phone:
                    should_delete = True
                elif matched_phone:
                    if matched_phone in kept_phones:
                        should_delete = True
                    else:
                        kept_phones.add(matched_phone)
                elif not active_items and not delete_phones:
                    should_delete = True

                if should_delete:
                    self._delete_env_id(env_id)
        except Exception as e:
            logger.warning(f"清理面板变量失败: {e}")

    def _collect_env_items(self, extra=None, exclude_phone=""):
        items = {}
        exclude_phone = str(exclude_phone or "")
        for user in AccountManager.get_all_users():
            try:
                remarks = RemarkManager.get_all_remarks(user) if config['enable_remark'] else {}
                for account in AccountManager.get_accounts(user):
                    account = str(account)
                    if account == exclude_phone:
                        continue
                    token = AccountManager.get_token(account)
                    if not token:
                        continue
                    items[account] = {
                        "token": str(token).strip(),
                        "remark": remarks.get(account, ""),
                    }
            except Exception:
                continue

        if extra:
            phone = str(extra.get("phone") or "")
            token = str(extra.get("token") or "").strip()
            if phone and phone != exclude_phone and token:
                items[phone] = {
                    "token": token,
                    "remark": str(extra.get("remark") or ""),
                }
        return items

    def _build_single_env_remark(self, phone, item):
        remark = str(item.get("remark") or "").strip()
        bits = [f"账号:{phone}"]
        if remark:
            bits.append(f"备注:{remark}")
        bits.append(f"更新:{datetime.now().strftime('%m-%d %H:%M')}")
        bits.append("爱海盐提交")
        return "丨".join(bits)

    def _upsert_single_env(self, phone, item):
        ql_value = str(item.get("token") or "").strip()
        if not ql_value:
            return False, None
        final_remark = self._build_single_env_remark(phone, item)
        env_id = self.find_env(phone=phone, token=ql_value)
        if self.panel_type == 'daidai':
            headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
            if env_id is not None:
                url = f"{self.QLurl}/api/envs/{env_id}"
                data = {"name": config['env_name'], "value": ql_value, "remarks": final_remark}
                res = requests.put(url, headers=headers, json=data, timeout=10, verify=False)
                if res.status_code == 200:
                    try: requests.put(f"{self.QLurl}/api/envs/{env_id}/enable", headers=headers, timeout=5, verify=False)
                    except: pass
                else: return False, env_id
            else:
                url = f"{self.QLurl}/api/envs"
                data = {"name": config['env_name'], "value": ql_value, "remarks": final_remark}
                res = requests.post(url, headers=headers, json=data, timeout=10, verify=False)
                if res.status_code != 200: return False, env_id
                try:
                    env_id = self._env_id((res.json().get("data") or {}))
                except Exception:
                    env_id = self.find_env(phone=phone, token=ql_value)
        else:
            headers = {"Authorization": f"Bearer {self.qltoken}", "Content-Type": "application/json"}
            url = f"{self.QLurl}/open/envs"
            if env_id is not None:
                data = {"value": ql_value, "name": config['env_name'], "remarks": final_remark}
                if isinstance(env_id, int) or str(env_id).isdigit():
                    data["id"] = env_id
                else:
                    data["_id"] = env_id
                res = requests.put(url, headers=headers, json=data, timeout=10, verify=False)
                if res.status_code == 200:
                    try: requests.put(f"{self.QLurl}/open/envs/enable", headers=headers, json=[env_id], timeout=5, verify=False)
                    except: pass
                else: return False, env_id
            else:
                data = [{"value": ql_value, "name": config['env_name'], "remarks": final_remark}]
                res = requests.post(url, headers=headers, json=data, timeout=10, verify=False)
                if res.status_code != 200: return False, env_id
                env_id = self.find_env(phone=phone, token=ql_value)
        return True, env_id

    def _sync_env_items(self, items):
        if not items:
            self._cleanup_envs()
            return True
        success = True
        for phone in sorted(items.keys()):
            ok, _ = self._upsert_single_env(phone, items[phone])
            if not ok:
                success = False
        if success:
            self._cleanup_envs(active_items=items)
        return success

    def delete_env(self, phone):
        if not self.enabled: return False
        phone = str(phone)
        try:
            items = self._collect_env_items(exclude_phone=phone)
            ok = self._sync_env_items(items)
            self._cleanup_envs(active_items=items, delete_phones=[phone])
            return ok
        except Exception as e:
            logger.error(f"Delete Env Error: {e}")
            return False

    def sync_env(self, token, phone, remark="", owner_user_id=None):
        if not self.enabled: return False
        phone = str(phone)
        try:
            items = self._collect_env_items({
                "phone": phone,
                "token": token,
                "remark": remark,
            })
            if not items:
                return False
            return self._sync_env_items(items)
        except Exception as e:
            logger.error(f"Sync Env Error: {e}")
            return False

try:
    sys_api = SystemAPI()
    if not sys_api.enabled and sender.getImtype() != 'fake':
        sender.reply("⚠️ 系统API初始化失败，青龙/呆呆同步功能不可用，请检查配置。")
except:
    sys_api = type('obj', (object,), {'enabled': False, 'sync_env': lambda *a, **k: None, 'delete_env': lambda *a, **k: None})()
    if sender.getImtype() != 'fake':
        sender.reply("⚠️ 系统API初始化异常，青龙/呆呆同步功能不可用，请检查配置。")

def process_single_account_query(account,index=0,total_count=0,account_remarks=None):
    account=str(account);token=AccountManager.get_token(account) or '';remark=(account_remarks or {}).get(account,'') if config['enable_remark'] else '';display=get_account_display(account,remark)
    if len(token)<10:return f'❌ {display}: 凭证不存在'
    try:
        client=AiHaiYanClient(token);client.check_info();net,valid,nick,msg=client.get_info()
        if not net:return f'⚠️ {display}: 网络异常：{str(msg)[:60]}'
        if not valid:return f'⚠️ {display}: 登录失效：{str(msg)[:60]}'
        return f'=====爱海盐=====\n👤 {display}\n✅ 当前登录: {nick}\n{msg}\n=================='
    except Exception as e:return f'❌ {display}: {str(e)[:80]}'

def cxs():
    accounts=[str(x) for x in AccountManager.get_accounts(userid)]
    if not accounts:
        sender.reply('❌ 暂无账号，请先发送 爱海盐登录');return
    remarks=RemarkManager.get_all_remarks(userid) if config['enable_remark'] else {}
    sender.reply('=====爱海盐查询=====\n'+'\n'.join(f'[{i}] {get_account_display(a,remarks.get(a,""))}' for i,a in enumerate(accounts,1))+'\n[a] 全部；支持1,2或3-6')
    choice=get_user_input(60)
    if not choice or choice.lower()=='q':return
    indexes=list(range(1,len(accounts)+1)) if choice.lower()=='a' else parse_index_selection(choice,len(accounts),False)[0]
    if not indexes:return
    with ThreadPoolExecutor(max_workers=min(8,len(indexes))) as pool:
        futures=[pool.submit(process_single_account_query,accounts[i-1],i,len(accounts),remarks) for i in indexes]
        for f in as_completed(futures):sender.reply(f.result())


def get_user_input(timeout=60):
    try:
        response = sender.listen(timeout * 1000)
        if not response: return None
        response = response.strip()
        if response.lower() in ['q', 'quit', 'exit', '退出', 'cancel']: return 'q'
        return response
    except: return None

def parse_index_selection(text, total_count, allow_all=True):
    try:
        if text is None:
            return [], []
        raw = str(text).strip()
        if not raw:
            return [], []
        if allow_all and raw.lower() in ['a', 'all', '全部', '全选']:
            return list(range(1, total_count + 1)), []

        selected = []
        invalid = []
        parts = re.split(r'[,\s，、;；]+', raw)
        for part in parts:
            part = part.strip()
            if not part:
                continue

            range_match = re.match(r'^(\d+)\s*(?:-|~|到|至)\s*(\d+)$', part)
            if range_match:
                start = int(range_match.group(1))
                end = int(range_match.group(2))
                if start > end:
                    start, end = end, start
                start = max(1, start)
                end = min(total_count, end)
                if start <= end:
                    selected.extend(range(start, end + 1))
                else:
                    invalid.append(part)
                continue

            if part.isdigit():
                idx = int(part)
                if 1 <= idx <= total_count:
                    selected.append(idx)
                else:
                    invalid.append(part)
                continue

            invalid.append(part)

        return list(dict.fromkeys(selected)), invalid
    except:
        return [], [str(text)]

def bindaccount():
    try:
        remark = ""
        if config['enable_remark']:
            sender.reply("""
=====账号备注设置=====
🎯 请输入账号备注名
(批量提交时此备注将应用到所有账号)
------------------
回复备注名继续
回复"n"跳过备注
回复"q"退出操作
==================""")
            remark_input = get_user_input(timeout=120)
            if remark_input == 'q':
                sender.reply("✅ 已取消")
                return
            elif remark_input != 'n' and remark_input:
                remark = remark_input.strip()[:20]

        sender.reply("""
=====爱海盐 登录=====
当前模式: 🌐 提交至面板
------------------
👉 请直接发送账号配置，格式如下(一行一个)：
手机号#密码
或带备注:
备注#手机号#密码
------------------
⚠️ 绑定后根据手机号无损覆盖旧数据，不会重复!
------------------
回复"q"退出操作
==================""")

        input_str = get_user_input(timeout=120)
        if not input_str or input_str.lower() == 'q':
            sender.reply("✅ 已取消")
            return

        token_lines = []
        raw_lines = [line.strip() for line in input_str.split('\n') if line.strip()]
        for line in raw_lines:
            token_lines.append(line.strip())

        if not token_lines:
            sender.reply("❌ 内容为空")
            return

        sender.reply(f"⏳ 正在处理 {len(token_lines)} 个账号，请稍候...")
        bind_stats = {"success": 0, "fail": 0, "new": 0, "update": 0, "migrate": 0}
        fail_msgs = []

        for line in token_lines:
            try:
                phone, pwd, line_remark, parse_err = parse_aihaiyan_credential(line, remark)
                if parse_err:
                    bind_stats["fail"] += 1
                    fail_msgs.append(parse_err)
                    if len(token_lines) == 1:
                        sender.reply(f"❌ {parse_err}")
                    continue

                final_token_str = f"{phone}#{pwd}"

                client = AiHaiYanClient(final_token_str)
                info_res = client.check_info()

                nick = info_res['nickname']
                final_token_str = info_res['final_token']
                acc_id = info_res['acc_key']
                aliases = info_res.get('aliases', [])
                acc_type = info_res.get('acc_type', '')
                legacy_key = info_res.get('legacy_key', '')

                bind_result = process_account_binding(final_token_str, acc_id, nick, line_remark, aliases, acc_type, legacy_key, silent=(len(token_lines) > 1))
                if bind_result.get("ok"):
                    bind_stats["success"] += 1
                    bind_stats[bind_result.get("action", "update")] += 1
                    if bind_result.get("migrated"):
                        bind_stats["migrate"] += 1
                else:
                    bind_stats["fail"] += 1
                    fail_msgs.append(bind_result.get("msg", "处理失败"))
            except Exception as ex:
                bind_stats["fail"] += 1
                fail_msgs.append(str(ex)[:30])
                if len(token_lines) == 1:
                    sender.reply(f"❌ 登录处理失败: {str(ex)}")

        if len(token_lines) > 1:
            fail_text = ""
            if fail_msgs:
                fail_text = "\n❌ 失败原因: " + "；".join(list(dict.fromkeys(fail_msgs))[:3])
            sender.reply(f"""=====爱海盐登录汇总=====
✅ 成功: {bind_stats['success']} 个
🆕 新增: {bind_stats['new']} 个
🔄 更新: {bind_stats['update']} 个
🔁 承接旧账号: {bind_stats['migrate']} 个
❌ 失败: {bind_stats['fail']} 个{fail_text}
==================""")

    except Exception as e:
        logger.error(f"绑定失败: {e}")
        sender.reply(f"❌ 绑定失败: {e}")

def process_account_binding(full_token,unique_id,nickname,remark='',aliases=None,acc_type='',legacy_key='',silent=False):
    account=str(unique_id)
    try:
        is_new=AccountManager.add_account(userid,account);AccountManager.update_account_token(account,full_token)
        if config['enable_remark'] and remark:RemarkManager.set_account_remark(userid,account,remark)
        synced=sys_api.sync_env(full_token,account,remark,owner_user_id=userid)
        if not silent:sender.reply(f'✅ {nickname or account} 已保存；面板'+('同步成功' if synced else '未同步'))
        return {'ok':True,'account':account,'action':'new' if is_new else 'update','migrated':False}
    except Exception as e:
        if not silent:sender.reply(f'❌ 入库失败：{e}')
        return {'ok':False,'msg':str(e)}

def xy_manage():
    accounts = [str(x) for x in AccountManager.get_accounts(userid)]
    if not accounts:
        sender.reply(f"❌ 未找到账号，请发送 {config['randomsigncommand']} 绑定")
        return
    sender.reply("=====账号管理=====\n" + "\n".join(
        f"[{i}] {account}" for i, account in enumerate(accounts, 1)
    ) + "\n[d] 删除多个账号\n[q] 退出\n==================")
    choice = get_user_input()
    if not choice or choice.lower() == "q":
        return
    if choice.lower() == "d":
        sender.reply("请输入账号序号，多个用逗号分隔：")
        selected, _ = parse_index_selection(get_user_input(), len(accounts), allow_all=False)
        if selected:
            batch_delete_selected([accounts[i - 1] for i in selected])
        return
    selected, _ = parse_index_selection(choice, len(accounts), allow_all=False)
    if len(selected) == 1:
        manage_single_account(accounts[selected[0] - 1], {})
    elif selected:
        manage_multiple_accounts([accounts[i - 1] for i in selected], {})
    else:
        sender.reply("❌ 序号无效")

def manage_multiple_accounts(selected_accs, account_remarks=None):
    sender.reply(f"确认删除选中的 {len(selected_accs)} 个账号请回复 y")
    if get_user_input().lower() == "y":
        batch_delete_selected(selected_accs)

def manage_single_account(account,account_remarks=None):
    token=AccountManager.get_token(account) or ''
    sender.reply(f'=====账号操作=====\n📱 {account}\n[1] 修改备注 [2] 查看配置 [3] 同步面板 [4] 删除账号')
    choice=get_user_input()
    if choice=='1' and config['enable_remark']:
        sender.reply('请输入新备注：');remark=get_user_input()
        if remark and remark.lower()!='q':RemarkManager.set_account_remark(userid,account,remark);sender.reply('✅ 备注已更新')
    elif choice=='2':sender.reply(token or '❌ 未保存配置')
    elif choice=='3':sender.reply('✅ 同步成功' if token and sys_api.sync_env(token,account,RemarkManager.get_account_remark(userid,account),owner_user_id=userid) else '❌ 同步失败')
    elif choice=='4':
        sender.reply('确认删除请回复 y')
        if get_user_input().lower()=='y':AccountManager.remove_account(userid,account);RemarkManager.delete_account_remark(userid,account);sys_api.delete_env(account);sender.reply('✅ 已删除')

def batch_delete_selected(accounts):
    preview = []
    account_remarks = RemarkManager.get_all_remarks(userid) if config['enable_remark'] else {}
    for account in accounts[:5]:
        account = str(account)
        preview.append(get_account_display(account, account_remarks.get(account, "")))
    more = f"\n...等 {len(accounts)} 个账号" if len(accounts) > 5 else ""
    sender.reply(f"=====确认批量删除=====\n已选择 {len(accounts)} 个账号\n{chr(10).join(preview)}{more}\n------------------\n确认删除请回复【确认删除】\n回复 q 取消\n==================")
    if get_user_input() == "确认删除":
        today_date = datetime.now().date()
        for account in accounts:
            try:
                 account = str(account)
                 AccountManager.remove_account(userid, account)
                 try: sg.bucketDel(bucket='aihaiyan_token', key=account)
                 except: pass
                 try:
                     pass
                 except: pass
                 if config['enable_remark']: RemarkManager.delete_account_remark(userid, account)
                 sys_api.delete_env(account)
                 for d in range(config['reminder_days'] + 1):
                     remind_key = f"{userid}_{account}_{today_date - timedelta(days=d)}"
                     try: sg.bucketDel('aihaiyan_remind_log', remind_key)
                     except: pass
            except: pass
        sender.reply("✅ 批量删除完成")


def show_tutorial():
    sender.reply('=====爱海盐教程=====\n爱海盐登录：提交 手机号#密码\n爱海盐查询：查询账号状态与记录\n爱海盐管理：备注、同步或删除账号\n==================')

try:
    if '登录' in usermessage or '登陆' in usermessage:bindaccount()
    elif '管理' in usermessage:xy_manage()
    elif '查询' in usermessage:cxs()
    elif '教程' in usermessage or usermessage=='爱海盐':show_tutorial()
except Exception as e:
    logger.error(f'Error: {e}');sender.reply(f'❌ 系统错误: {e}')
