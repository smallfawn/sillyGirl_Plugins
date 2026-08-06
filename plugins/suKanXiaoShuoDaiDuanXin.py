# [title: 速看小说带短信]
# [name: suKanXiaoShuoDaiDuanXin]
# [language: python]
# [class: 任务]
# [author: 8165799]
# [version: v1.6.1]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^速看(登录|登陆|查询|管理|教程)$|^登(录|陆)速看$|^(查询|管理)速看$]
# [icon: https://api.iconify.design/lucide:bot.svg]
# [description: 速看小说账号登录、查询、备注与青龙变量同步]
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
    'dd_sk_rsa_private_key': plugin.Form.string().title('RSA签名私钥PEM').default('').description('速看接口签名私钥，留空则短信登录不可用'),
    'dd_sk_dd_sk_qlname': plugin.Form.string().title('青龙连接').default('').description('格式：地址丨ClientID丨ClientSecret；留空仅本地保存'),
    'dd_sk_dd_sk_osname': plugin.Form.string().title('变量名').default('S_SUKAN'),
    'dd_sk_enable_proxy': plugin.Form.boolean().title('启用代理').default(False),
    'dd_sk_proxy_pool_url': plugin.Form.string().title('代理地址').default(''),
})
_CONFIG_FIELD_MAP = {
    ('dd_sk', 'rsa_private_key'): 'dd_sk_rsa_private_key',
    ('dd_sk', 'dd_sk_qlname'): 'dd_sk_dd_sk_qlname',
    ('dd_sk', 'dd_sk_osname'): 'dd_sk_dd_sk_osname',
    ('dd_sk', 'enable_proxy'): 'dd_sk_enable_proxy',
    ('dd_sk', 'proxy_pool_url'): 'dd_sk_proxy_pool_url',
}

import re
import ast
from datetime import datetime
import urllib.parse
import requests
import time
import json
import logging
import base64
import warnings
import random
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
    from Crypto.Cipher import DES
    from Crypto.Signature import PKCS1_v1_5 as Signature_PKCS1_v1_5
    from Crypto.Hash import SHA
    from Crypto.Util.Padding import pad
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

warnings.filterwarnings('ignore', message='Unverified HTTPS request')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('su_kan')

REQUEST_TIMEOUT = 30  # 常规请求超时

RSA_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDFxo8kt6ftwFZ5QSXuVUOrQvYp
4fLVQb3uK/sgYwuR0A+rYdp97UsrjVWGjUQBUhKvjhDcJ8MIY22FJ4y1m/qmbHAe
NytfuP1pSnb34MEFV5tGUNvozAX/teuVARBLrlk9lql3ipJFKj0LWuZa7eHhX26O
dyXDjuA+Xw0hkEuW2QIDAQAB
-----END PUBLIC KEY-----"""

RSA_PRIVATE_KEY = ""

SK_DEVICE_CONFIG = {
    "device": "V2359A",
    "firm": "vivo",
    "channelId": "801002",
    "versionId": "80002056",
    "p2": "801002",
    "p3": "80002056",
    "p4": "501656",
    "p5": "19",
    "p9": "0",
    "p16": "V2359A",
    "p21": "99",
    "p22": "14",
    "p25": "80002056",
    "p26": "34",
    "p29": "zycb1bdb",
    "p33": "com.chaozh.xincao.only.sk",
    "p34": "vivo",
    "p36": "a",
    "d1": "8.0.2",
    "pc": "10",
    "rgt": "7",
}

SK_SMS_DEVICE_CONFIG = {
    "device": "Redmi Note 11",
    "firm": "Xiaomi",
    "channelId": "731001",
    "versionId": "101200017",
    "p2": "731001",
    "p3": "101200017",
    "p4": "501617",
    "p5": "16",
    "p9": "2",
    "p16": "Redmi Note 11",
    "p21": "3",
    "p22": "11",
    "p25": "12030",
    "p26": "36",
    "p29": "zya3c0e0",
    "p33": "com.zhangyue.app.shortplay.kakandj",
    "p34": "navigationbar_is_min",
    "p36": "a",
    "d1": "8.0.2",
    "pc": "10",
    "rgt": "7",
}

SK_DEVICE_PROFILES = [
    dict(SK_DEVICE_CONFIG),
    {
        "device": "PLQ110",
        "firm": "OnePlus",
        "channelId": "801001",
        "versionId": "80002056",
        "p2": "801001",
        "p3": "80002056",
        "p4": "501656",
        "p5": "19",
        "p9": "0",
        "p16": "PLQ110",
        "p21": "99",
        "p22": "16",
        "p25": "80002056",
        "p26": "36",
        "p29": "zycb1bdb",
        "p33": "com.chaozh.xincao.only.sk",
        "p34": "OnePlus",
        "p36": "a",
        "d1": "8.0.2",
        "pc": "10",
        "rgt": "7",
    },
    {
        "device": "M2007J3SC",
        "firm": "Xiaomi",
        "channelId": "801004",
        "versionId": "80002056",
        "p2": "801004",
        "p3": "80002056",
        "p4": "501656",
        "p5": "19",
        "p9": "0",
        "p16": "M2007J3SC",
        "p21": "99",
        "p22": "12",
        "p25": "80002056",
        "p26": "34",
        "p29": "zycb1bdb",
        "p33": "com.chaozh.xincao.only.sk",
        "p34": "Xiaomi",
        "p36": "a",
        "d1": "8.0.2",
        "pc": "10",
        "rgt": "7",
    },
]

SK_SMS_DEVICE_PROFILES = [
    dict(SK_SMS_DEVICE_CONFIG),
]

SK_API_BASE = "https://dj.palmestore.com"
SK_API_SEND_SMS = f"{SK_API_BASE}/dj_user/out/sms/sendSms/V2"
SK_API_LOGIN = f"{SK_API_BASE}/dj_user/out/login/loginByPhoneV3"

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()
usermessage = sender.getMessage()  # 这里提前获取

_RUNTIME_BUCKET = "plugin_push_runtime"
_RUNTIME_KEY = "速看"
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
    return {
        'dd_sk_osname':sg.bucketGet('dd_sk','dd_sk_osname') or 'S_SUKAN',
        'dd_sk_qlname':sg.bucketGet('dd_sk','dd_sk_qlname') or '',
        'randommanagecommand':'速看管理','randomquerycommand':'速看查询','randomsigncommand':'速看登录',
        'enable_proxy':str(sg.bucketGet('dd_sk','enable_proxy') or 'false').lower()=='true',
        'proxy_pool_url':sg.bucketGet('dd_sk','proxy_pool_url') or '',
        'enable_remark':True,
    }


config = getusercontent()

def get_owner_user_id(account, fallback_userid=None):
    account = str(account or "")
    try:
        if fallback_userid and account in [str(x) for x in AccountManager.get_accounts(str(fallback_userid))]:
            return str(fallback_userid)
    except:
        pass
    try:
        for frame_info in __import__('inspect').stack()[1:6]:
            local_vars = frame_info.frame.f_locals
            for key in ['owner_user_id', 'target_userid', 'target_qq', 'target_user', 'user', 'uid']:
                candidate = local_vars.get(key)
                if not candidate:
                    continue
                candidate = str(candidate)
                try:
                    if account in [str(x) for x in AccountManager.get_accounts(candidate)]:
                        return candidate
                except:
                    pass
    except:
        pass
    try:
        for owner in sg.bucketAllKeys(bucket='dd_sk_user'):
            try:
                if account in [str(x) for x in AccountManager.get_accounts(owner)]:
                    return str(owner)
            except:
                pass
    except:
        pass
    try:
        if not sender.isAdmin() and str(userid):
            return str(userid)
    except:
        pass
    return


def extract_sukan_device_profile(full_data):
    try:
        text = str(full_data or "").strip()
        if not text:
            return {}
        query_str = text.split('?', 1)[1] if '?' in text else text
        params = dict(urllib.parse.parse_qsl(query_str))
        profile = {
            "device": params.get("p16") or params.get("device") or "",
            "firm": params.get("firm") or params.get("p34") or "",
            "channelId": params.get("p2") or "",
            "versionId": params.get("p3") or "",
            "p2": params.get("p2") or "",
            "p3": params.get("p3") or "",
            "p4": params.get("p4") or "",
            "p5": params.get("p5") or "",
            "p9": params.get("p9") or "",
            "p16": params.get("p16") or "",
            "p21": params.get("p21") or "",
            "p22": params.get("p22") or "",
            "p25": params.get("p25") or "",
            "p26": params.get("p26") or "",
            "p29": params.get("p29") or "",
            "p33": params.get("p33") or "",
            "p34": params.get("p34") or "",
            "p36": params.get("p36") or "",
            "d1": params.get("d1") or "",
            "pc": params.get("pc") or "",
            "rgt": params.get("rgt") or "",
        }
        return {k: v for k, v in profile.items() if str(v).strip()}
    except Exception as e:
        logger.warning(f"提取速看设备画像失败: {e}")
        return {}

def save_sukan_device_profile(full_data):
    profile = extract_sukan_device_profile(full_data)
    if not profile:
        return
    try:
        merged = dict(SK_DEVICE_CONFIG)
        merged.update(profile)
        sg.bucketSet('dd_sk_runtime', 'sms_device_profile', json.dumps(merged, ensure_ascii=False))
        logger.info(f"已保存速看设备画像: {merged.get('device')} / {merged.get('channelId')}")
    except Exception as e:
        logger.warning(f"保存速看设备画像失败: {e}")

def is_sukan_sms_profile(profile):
    if not isinstance(profile, dict):
        return False
    return (
        profile.get("p2") == "731001"
        or profile.get("p3") == "101200017"
        or profile.get("p29") == "zya3c0e0"
        or profile.get("p33") == "com.zhangyue.app.shortplay.kakandj"
    )

def get_sukan_sms_device_profile():
    try:
        saved = sg.bucketGet('dd_sk_runtime', 'sms_device_profile')
        data = safe_json_loads(saved, {})
        merged = dict(SK_SMS_DEVICE_CONFIG)
        if is_sukan_sms_profile(data):
            merged.update({k: v for k, v in data.items() if str(v).strip()})
        return merged
    except Exception:
        return dict(SK_SMS_DEVICE_CONFIG)

def rsa_encrypt(data):
    if not CRYPTO_AVAILABLE:
        return ""
    key = RSA.import_key(RSA_PUBLIC_KEY)
    cipher = Cipher_PKCS1_v1_5.new(key)
    encrypted = cipher.encrypt(data.encode('utf-8'))
    return base64.b64encode(encrypted).decode('utf-8')

def rsa_sign(data):
    if not CRYPTO_AVAILABLE:
        return ""
    private_key_text = sg.bucketGet("dd_sk", "rsa_private_key") or RSA_PRIVATE_KEY
    if not private_key_text:
        raise RuntimeError("未配置速看RSA签名私钥")
    key = RSA.import_key(private_key_text)
    h = SHA.new(data.encode('utf-8'))
    signer = Signature_PKCS1_v1_5.new(key)
    signature = signer.sign(h)
    return base64.b64encode(signature).decode('utf-8')

def des_encrypt(data, key):
    if not CRYPTO_AVAILABLE:
        return ""
    key_bytes = key.encode('utf-8')[:8].ljust(8, b'\0')
    cipher = DES.new(key_bytes, DES.MODE_CBC, key_bytes)
    encrypted = cipher.encrypt(pad(data.encode('utf-8'), DES.block_size))
    return base64.b64encode(encrypted).decode('utf-8')

def generate_des_key():
    return ''.join([str(random.randint(0, 9)) for _ in range(8)])

def generate_pinfo(phone, code):
    des_key = generate_des_key()
    encrypted_des_key = rsa_encrypt(des_key)
    data_json = json.dumps({"phone": phone, "pCode": code}, separators=(',', ':'))
    encrypted_data = des_encrypt(data_json, des_key)
    pinfo = json.dumps({
        "DesKey": encrypted_des_key,
        "Data": encrypted_data
    }, separators=(',', ':'))
    return pinfo, encrypted_des_key

def generate_sign_content(params):
    sorted_keys = sorted(params.keys())
    return "&".join([f"{k}={params[k]}" for k in sorted_keys if params[k] != ""])

class SukanSMSLoginAPI:
    def __init__(self):
        self.device_config = get_sukan_sms_device_profile()
        self.session = requests.Session()
        self.session.verify = False
        self.session.headers.update({
            'User-Agent': f"Dalvik/2.1.0 (Linux; U; Android {self.device_config.get('p22', '14')}; {self.device_config.get('device', 'V2359A')} Build/BP2A.250605.015)",
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept-Encoding': 'gzip',
        })
        self.zyeid = str(uuid.uuid4())
        self.imei = "____" + uuid.uuid4().hex[:16]
        self.p7 = "__" + uuid.uuid4().hex[:16]
        self.p28 = uuid.uuid4().hex.upper() + uuid.uuid4().hex[:32]
        self.guest_usr = f"j{int(time.time())}{random.randint(100, 999)}"
        self.p1 = ""
        self.usr = self.guest_usr
        self.ku = self.guest_usr
        self.kt = ""
        self.p35 = ""

    def get_base_params(self):
        current_usr = self.ku or self.usr or self.guest_usr
        return {
            "zyeid": self.zyeid,
            "usr": current_usr,
            "rgt": self.device_config["rgt"],
            "p1": self.p1,
            "ku": current_usr,
            "pc": self.device_config["pc"],
            "p2": self.device_config["p2"],
            "p3": self.device_config["p3"],
            "p4": self.device_config["p4"],
            "p5": self.device_config["p5"],
            "p7": self.p7,
            "p9": self.device_config["p9"],
            "p12": "",
            "p16": self.device_config["p16"],
            "p21": self.device_config["p21"],
            "p22": self.device_config["p22"],
            "p25": self.device_config["p25"],
            "p26": self.device_config["p26"],
            "p28": self.p28,
            "p29": self.device_config["p29"],
            "p30": "",
            "p31": self.p7,
            "p33": self.device_config["p33"],
            "p34": self.device_config["p34"],
            "p36": self.device_config["p36"],
            "firm": self.device_config["firm"],
            "d1": self.device_config["d1"],
        }

    def send_sms(self, phone):
        timestamp = str(int(time.time() * 1000))
        encrypted_phone = rsa_encrypt(phone)
        sign_params = {
            "channelId": self.device_config["channelId"],
            "device": self.device_config["device"],
            "flag": "1",
            "imei": self.imei,
            "phone": encrypted_phone,
            "sendType": "0",
            "times": "1",
            "timestamp": timestamp,
            "versionId": self.device_config["versionId"],
        }
        sign = rsa_sign(generate_sign_content(sign_params))
        url = f"{SK_API_SEND_SMS}?{urllib.parse.urlencode(self.get_base_params())}"
        data = {
            "versionId": self.device_config["versionId"],
            "device": self.device_config["device"],
            "flag": "1",
            "imei": self.imei,
            "sign": sign,
            "timestamp": timestamp,
            "phone": encrypted_phone,
            "times": "1",
            "sendType": "0",
            "channelId": self.device_config["channelId"],
        }
        response = self.session.post(url, data=data, timeout=30)
        result = response.json()
        if result.get("code") == 0 or result.get("msg") == "success":
            return True, "验证码发送成功"
        logger.warning(f"速看短信发送失败: {result}")
        return False, result.get("msg", "未知错误")

    def login(self, phone, code):
        timestamp = str(int(time.time() * 1000))
        encrypted_phone = rsa_encrypt(phone)
        pinfo, encrypted_des_key = generate_pinfo(phone, code)
        sign_params = {
            "channelId": self.device_config["channelId"],
            "device": self.device_config["device"],
            "imei": self.imei,
            "phone": encrypted_phone,
            "timestamp": timestamp,
            "versionId": self.device_config["versionId"],
        }
        sign = rsa_sign(generate_sign_content(sign_params))
        url_params = self.get_base_params()
        url_params["p35"] = encrypted_des_key
        url = f"{SK_API_LOGIN}?{urllib.parse.urlencode(url_params)}"
        data = {
            "smboxid": encrypted_des_key,
            "versionId": self.device_config["versionId"],
            "device": self.device_config["device"],
            "userName": url_params.get("usr", ""),
            "imei": self.imei,
            "sign": sign,
            "timestamp": timestamp,
            "pInfo": pinfo,
            "phone": encrypted_phone,
            "utdId": self.p1 or "",
            "loginSource": "我的_马上登录",
            "channelId": self.device_config["channelId"],
        }
        response = self.session.post(url, data=data, timeout=30)
        result = response.json()
        if result.get("code") == 0:
            body = result.get("body", {})
            self.kt = body.get("token", "") or body.get("kt", "")
            self.p1 = body.get("utdId", "") or body.get("signUser", "") or body.get("p1", "")
            self.usr = body.get("userName", "") or body.get("usr", "")
            self.ku = body.get("signUser", "") or body.get("ku", "") or self.usr
            self.p35 = encrypted_des_key
            return True, body, "登录成功"
        logger.warning(f"速看短信登录失败: {result}")
        return False, None, result.get("msg", "未知错误")

    def generate_welfare_url(self):
        if not self.kt:
            return ""
        task_profile = dict(SK_DEVICE_CONFIG)
        task_profile["p16"] = self.device_config.get("p16") or self.device_config.get("device") or task_profile["p16"]
        task_profile["p22"] = self.device_config.get("p22") or task_profile["p22"]
        task_profile["p34"] = self.device_config.get("firm") or self.device_config.get("p34") or task_profile["p34"]
        task_profile["firm"] = self.device_config.get("firm") or self.device_config.get("p34") or task_profile["firm"]
        params = {
            "zyeid": self.zyeid,
            "rgt": task_profile["rgt"],
            "p1": self.p1,
            "kt": self.kt,
            "source": "welfare",
            "showContentInStatusBar": "1",
            "ecpmMix": "0.0",
            "ecpmVideo": "0.0",
            "mcTacid": "",
            "pc": task_profile["pc"],
            "p2": task_profile["p2"],
            "p3": task_profile["p3"],
            "p4": task_profile["p4"],
            "p5": task_profile["p5"],
            "p7": self.p7,
            "p9": task_profile["p9"],
            "p12": "",
            "p16": task_profile["p16"],
            "p21": task_profile["p21"],
            "p22": task_profile["p22"],
            "p25": task_profile["p25"],
            "p26": task_profile["p26"],
            "p28": self.p28,
            "p29": task_profile["p29"],
            "p30": "",
            "p31": self.p7,
            "p33": task_profile["p33"],
            "p34": task_profile["p34"],
            "p36": task_profile["p36"],
            "firm": task_profile["firm"],
            "d1": task_profile["d1"],
            "pca": "channel-visit",
            "p35": self.p35,
            "usr": self.ku,
            "ku": self.ku,
        }
        base_url = "https://welfare-user.palmestore.com/sukanread/welfare-package/sudu/welfare.html"
        return f"{base_url}?{urllib.parse.urlencode(params)}"



class ProxyManager:

    def __init__(self, enable_proxy=False, proxy_pool_url=''):
        self.enable_proxy = enable_proxy
        self.proxy_pool_url = proxy_pool_url
        self.current_proxy = None
        self.last_fetch_time = 0
        self.proxy_cache_time = 300  # 代理缓存5分钟

    def get_proxy(self):
        if not self.enable_proxy or not self.proxy_pool_url:
            return None

        current_time = time.time()
        if self.current_proxy and (current_time - self.last_fetch_time) < self.proxy_cache_time:
            return self.current_proxy

        try:
            logger.info("从代理池获取代理: " + self.proxy_pool_url)
            response = requests.get(self.proxy_pool_url, timeout=10)

            if response.status_code == 200:
                proxy_data = response.json()

                if isinstance(proxy_data, dict):
                    proxy = proxy_data.get('proxy')
                    if proxy:
                        self.current_proxy = proxy
                        self.last_fetch_time = current_time
                        logger.info("获取代理成功: " + proxy)
                        return proxy

                    http_proxy = proxy_data.get('http') or proxy_data.get('https')
                    if http_proxy:
                        self.current_proxy = http_proxy
                        self.last_fetch_time = current_time
                        logger.info("获取代理成功: " + http_proxy)
                        return http_proxy

                elif isinstance(proxy_data, str):
                    self.current_proxy = proxy_data
                    self.last_fetch_time = current_time
                    logger.info("获取代理成功: " + proxy_data)
                    return proxy_data

                elif isinstance(proxy_data, list) and proxy_data:
                    proxy = proxy_data[0]
                    self.current_proxy = proxy
                    self.last_fetch_time = current_time
                    logger.info("获取代理成功: " + proxy)
                    return proxy

                logger.warning("代理池返回格式不支持: " + str(proxy_data))
                return None

        except Exception as e:
            logger.error("获取代理失败: " + str(e))
            return None

    def rotate_proxy(self):
        self.current_proxy = None
        self.last_fetch_time = 0
        return self.get_proxy()

    def get_proxy_dict(self):
        proxy = self.get_proxy()
        if not proxy:
            return None

        return {
            'http': proxy,
            'https': proxy
        }

class RemarkManager:

    @staticmethod
    def get_account_remark(user_id, account_id):
        try:
            remark_data = sg.bucketGet(bucket='dd_sk_remarks', key=f'{user_id}_{account_id}')
            if remark_data:
                return remark_data
            return ""
        except Exception as e:
            logger.error("获取备注失败: " + str(user_id) + " - " + str(account_id) + " - " + str(e))
            return ""

    @staticmethod
    def set_account_remark(user_id, account_id, remark):
        try:
            remark_clean = remark.strip()[:20]  # 限制20字符
            if remark_clean:
                sg.bucketSet(bucket='dd_sk_remarks', key=f'{user_id}_{account_id}', value=remark_clean)
                logger.info("设置备注: " + str(user_id) + " - " + str(account_id) + " - " + remark_clean)
                return remark_clean
            return ""
        except Exception as e:
            logger.error("设置备注失败: " + str(user_id) + " - " + str(account_id) + " - " + str(e))
            return ""

    @staticmethod
    def get_all_remarks(user_id):
        try:
            accounts = AccountManager.get_accounts(user_id)
            remarks = {}
            for account in accounts:
                remark = RemarkManager.get_account_remark(user_id, account)
                if remark:
                    remarks[account] = remark
            return remarks
        except Exception as e:
            logger.error("获取所有备注失败: " + str(user_id) + " - " + str(e))
            return {}

    @staticmethod
    def delete_account_remark(user_id, account_id):
        try:
            sg.bucketDel(bucket='dd_sk_remarks', key=f'{user_id}_{account_id}')
            logger.info("删除备注: " + str(user_id) + " - " + str(account_id))
            return True
        except Exception as e:
            logger.error("删除备注失败: " + str(user_id) + " - " + str(account_id) + " - " + str(e))
            return False

def safe_request(method, url, **kwargs):
    try:
        if 'timeout' not in kwargs:
            kwargs['timeout'] = REQUEST_TIMEOUT

        if 'verify' not in kwargs:
             kwargs['verify'] = False

        if config['enable_proxy'] and config['proxy_pool_url']:
            proxy_manager = ProxyManager(enable_proxy=True, proxy_pool_url=config['proxy_pool_url'])
            proxies = proxy_manager.get_proxy_dict()
            if proxies:
                kwargs['proxies'] = proxies
                logger.debug("使用代理请求: " + str(proxies))

        logger.debug("发送请求: " + method + " " + url)
        response = requests.request(method, url, **kwargs)

        if response.status_code >= 400:
            logger.error("请求失败: " + url + " - 状态码: " + str(response.status_code))
            if response.status_code in [403, 407, 408, 429] and config['enable_proxy']:
                logger.info("代理可能失效，尝试更换代理重试...")
                proxy_manager = ProxyManager(enable_proxy=True, proxy_pool_url=config['proxy_pool_url'])
                proxy_manager.rotate_proxy()
                proxies = proxy_manager.get_proxy_dict()
                if proxies:
                    kwargs['proxies'] = proxies

                    try:
                        logger.info("使用新代理重试请求")
                        response = requests.request(method, url, **kwargs)
                        if response.status_code >= 400:
                            raise Exception("请求失败，状态码: " + str(response.status_code))
                    except Exception as retry_e:
                        raise Exception("代理重试失败: " + str(retry_e))
            else:
                     raise Exception("请求失败，状态码: " + str(response.status_code))

        return response
    except requests.exceptions.Timeout:
        logger.error("请求超时: " + url)
        raise Exception("请求超时: " + url)
    except requests.exceptions.SSLError as e:
        logger.error("SSL错误: " + url + " - " + str(e))
        try:
            logger.warning("尝试跳过SSL验证: " + url)
            kwargs['verify'] = False
            response = requests.request(method, url, **kwargs)
            return response
        except Exception:
            raise Exception("SSL验证失败: " + str(e))
    except requests.exceptions.RequestException as e:
        logger.error("请求失败: " + url + " - " + str(e))
        raise Exception("请求失败: " + str(e))
    except Exception as e:
        logger.error("请求异常: " + url + " - " + str(e))
        raise Exception("请求异常: " + str(e))

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

def safe_json_loads(raw, default=None):
    try:
        return json.loads(raw) if raw else (default if default is not None else {})
    except:
        return default if default is not None else {}

def detect_phone_candidates(*values):
    candidates = []
    for value in values:
        if value is None:
            continue
        text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
        for phone in re.findall(r'(?<!\d)1[3-9]\d{9}(?!\d)', text):
            if phone not in candidates:
                candidates.append(phone)
    return candidates

def get_account_meta(account_key):
    return safe_json_loads(sg.bucketGet(bucket='dd_sk_meta', key=str(account_key)), {})

def set_account_meta(account_key, meta):
    try:
        merged = get_account_meta(account_key)
        merged.update({k: v for k, v in (meta or {}).items() if v not in [None, ""]})
        sg.bucketSet(bucket='dd_sk_meta', key=str(account_key), value=json.dumps(merged, ensure_ascii=False))
        return merged
    except Exception as e:
        logger.error(f"保存账号元信息失败 {account_key}: {e}")
        return meta or {}

def remove_account_meta(account_key):
    try:
        sg.bucketDel(bucket='dd_sk_meta', key=str(account_key))
    except:
        pass

def find_account_by_phone(user_id, phone):
    phone = str(phone or "").strip()
    if not phone:
        return None
    for account in AccountManager.get_accounts(user_id):
        meta = get_account_meta(account)
        if str(meta.get('phone') or "").strip() == phone:
            return str(account)
        if str(account).strip() == phone:
            return str(account)
    return None

def migrate_account_binding_if_needed(user_id, old_account_key, new_account_key):
    old_account_key = str(old_account_key or "").strip()
    new_account_key = str(new_account_key or "").strip()
    if not old_account_key or not new_account_key or old_account_key == new_account_key:
        return
    try:
        old_token = sg.bucketGet(bucket='dd_sk_token', key=old_account_key)
        new_token = sg.bucketGet(bucket='dd_sk_token', key=new_account_key)
        if old_token and not new_token:
            sg.bucketSet(bucket='dd_sk_token', key=new_account_key, value=old_token)

        old_auth = '2099-12-31'
        new_auth = '2099-12-31'
        if old_auth and not new_auth:
            True

        old_remark = sg.bucketGet(bucket='dd_sk_remarks', key=f'{user_id}_{old_account_key}')
        new_remark = sg.bucketGet(bucket='dd_sk_remarks', key=f'{user_id}_{new_account_key}')
        if old_remark and not new_remark:
            sg.bucketSet(bucket='dd_sk_remarks', key=f'{user_id}_{new_account_key}', value=old_remark)

        old_meta = get_account_meta(old_account_key)
        if old_meta:
            merged = dict(old_meta)
            merged.setdefault("migrated_from", old_account_key)
            set_account_meta(new_account_key, merged)

        AccountManager.remove_account(user_id, old_account_key)
        sg.bucketDel(bucket='dd_sk_token', key=old_account_key)
        True
        sg.bucketDel(bucket='dd_sk_remarks', key=f'{user_id}_{old_account_key}')
        remove_account_meta(old_account_key)

        try:
            remove_account_env_from_system(old_account_key)
        except Exception:
            pass

        logger.info(f"账号已合并迁移: {old_account_key} -> {new_account_key}")
    except Exception as e:
        logger.error(f"账号迁移失败 {old_account_key} -> {new_account_key}: {e}")

class AccountManager:

    @staticmethod
    def get_accounts(user_id):
        try:
            value = sg.bucketGet(bucket='dd_sk_user', key=user_id)
            if not value:
                return []

            if value.startswith('[') and value.endswith(']'):
                try:
                    accounts = ast.literal_eval(value)
                    if isinstance(accounts, (list, tuple, set)):
                        accounts = [str(x) for x in list(dict.fromkeys(accounts))]
                        return accounts
                except:
                    pass
            return [str(value)]
        except Exception as e:
            logger.error("获取账号列表失败: " + str(user_id) + " - " + str(e))
            return []

    @staticmethod
    def add_account(user_id, account):
        try:
            accounts = AccountManager.get_accounts(user_id)
            if account not in accounts:
                accounts.append(account)
                sg.bucketSet(bucket='dd_sk_user', key=user_id, value=str(accounts))
                logger.info("用户 " + str(user_id) + " 添加账号: " + account)
            return True
        except Exception as e:
            logger.error("添加账号失败: " + str(user_id) + " - " + account + " - " + str(e))
            return False

    @staticmethod
    def remove_account(user_id, account):
        try:
            accounts = AccountManager.get_accounts(user_id)
            if account in accounts:
                accounts.remove(account)
                if accounts:
                    sg.bucketSet(bucket='dd_sk_user', key=user_id, value=str(accounts))
                else:
                    sg.bucketDel(bucket='dd_sk_user', key=user_id)
                logger.info("用户 " + str(user_id) + " 移除账号: " + account)
                return True
            return False
        except Exception as e:
            logger.error("移除账号失败: " + str(user_id) + " - " + account + " - " + str(e))
            return False

    @staticmethod
    def update_account_credentials(account_key, full_credential):
        try:
            encrypted = encrypt_token(full_credential)
            sg.bucketSet(bucket='dd_sk_token', key=account_key, value=encrypted)
            return True
        except Exception as e:
            logger.error("更新凭证失败: " + str(e))
            return False

    @staticmethod
    def get_all_users():
        try:
            users = sg.bucketAllKeys(bucket='dd_sk_user')
            user_list = []
            for user in users:
                accounts = AccountManager.get_accounts(user)
                if accounts:
                    user_list.append(user)
            return user_list
        except Exception as e:
            logger.error("获取用户列表失败: " + str(e))
            return []

class QingLongAPI:

    def __init__(self):
        ql_config = config['dd_sk_qlname']
        try:
            if not ql_config:
                raise ValueError("对接配置为空")

            qllist = ql_config.split('丨')
            if len(qllist) != 3:
                raise ValueError("对接配置格式错误，应使用'丨'分隔")

            self.QLurl = qllist[0].strip()
            self.ClientID = qllist[1].strip()
            self.ClientSecret = qllist[2].strip()

            if not all([self.QLurl, self.ClientID, self.ClientSecret]):
                raise ValueError("对接配置参数不完整")

            if not self.QLurl.startswith(('http://', 'https://')):
                raise ValueError("对接地址格式错误，必须以http://或https://开头")

            self.qltoken = self._get_token()

        except Exception as e:
            logger.error("系统初始化失败: " + str(e))
            raise

    def _get_token(self):
        try:
            url = self.QLurl + '/open/auth/token?client_id=' + self.ClientID + '&client_secret=' + self.ClientSecret
            response = safe_request("GET", url, timeout=REQUEST_TIMEOUT)

            if response.status_code != 200:
                raise Exception("对接API请求失败，状态码: " + str(response.status_code))

            result = response.json()
            token_data = result.get('data', {})
            if "token" in token_data:
                return token_data['token']
            else:
                raise Exception("获取Token失败")

        except Exception as e:
            logger.error("获取系统Token失败: " + str(e))
            raise

    def get_all_envs(self):
        try:
            url = self.QLurl + "/open/envs"
            headers = {
                "Authorization": "Bearer" + ' ' + self.qltoken,
                "accept": "application/json"
            }
            response = safe_request("GET", url, headers=headers)
            result = response.json()

            if result.get('code') == 200:
                return result.get('data', [])
            else:
                raise Exception("获取变量失败: " + str(result.get('message')))

        except Exception as e:
            logger.error("获取系统变量失败: " + str(e))
            raise

    @staticmethod
    def _get_env_identity(env_ref):
        if not env_ref:
            return None, None

        if isinstance(env_ref, dict):
            if env_ref.get('id') is not None:
                return 'id', env_ref.get('id')
            if env_ref.get('_id') is not None:
                return '_id', env_ref.get('_id')

        return 'id', env_ref

    def find_env_by_account(self, value_snippet, user_id=None):
        try:
            envs = self.get_all_envs()
            f"{value_snippet}"
            target_uid_str = f"ID:{user_id}" if user_id else None

            for env in envs:
                if env.get('name') != config['dd_sk_osname']:
                    continue

                remarks = env.get('remarks', '')
                if target_uid_str and remarks and target_uid_str in remarks:
                    return env

                current_value = env.get('value', '')
                if user_id and str(user_id) in current_value:
                    return env

            return None
        except Exception as e:
            logger.error("查找系统变量失败: " + str(e))
            return None

    def delete_env(self, env_id):
        _, env_value = self._get_env_identity(env_id)
        if not env_value:
            return False

        try:
            url = self.QLurl + "/open/envs"
            headers = {
                "Authorization": "Bearer" + ' ' + self.qltoken,
                "accept": "application/json",
                "Content-Type": "application/json",
            }
            data = [env_value]
            response = safe_request("DELETE", url, headers=headers, json=data)
            return response.status_code == 200
        except Exception as e:
            logger.error("删除系统变量失败: " + str(e))
            return False

    def add_env(self, full_value, user_id, nickname, remark="", auth_time="", owner_user_id=None):
        try:
            url = self.QLurl + "/open/envs"
            value = full_value

            remarks_parts = [f'速看:{nickname}']

            if remark:
                remarks_parts.append(f'备注:{remark}')

            owner_user = get_owner_user_id(locals().get('account') or locals().get('phone') or locals().get('user_id') or '', owner_user_id if 'owner_user_id' in locals() else None)
            if not owner_user:
                raise Exception("无法确认账号真实归属，已阻止写入面板备注，避免青龙数据错乱")
            remarks_parts.extend([f'用户:{owner_user}', f'ID:{user_id}', '速看管理'])

            data = [{
                "value": value,
                "name": config['dd_sk_osname'],
                "remarks": '丨'.join(remarks_parts)
            }]

            headers = {
                "Authorization": "Bearer " + self.qltoken,
                "accept": "application/json",
                "Content-Type": "application/json",
            }

            response = safe_request("POST", url, headers=headers, json=data)

            if response.status_code != 200:
                raise Exception("请求失败，状态码: " + str(response.status_code))

            result = response.json()
            if result.get('code') != 200:
                raise Exception("系统返回错误: " + str(result.get('message')))

            return True
        except Exception as e:
            logger.error("添加系统变量失败: " + str(e))
            raise

    def update_env(self, env_id, full_value, user_id, nickname, remark="", auth_time="", owner_user_id=None):
        try:
            env_field, env_value = self._get_env_identity(env_id)
            if not env_value:
                raise Exception("系统变量ID为空")

            url = self.QLurl + "/open/envs"
            value = full_value

            remarks_parts = [f'速看:{nickname}']

            if remark:
                remarks_parts.append(f'备注:{remark}')

            owner_user = get_owner_user_id(locals().get('account') or locals().get('phone') or locals().get('user_id') or '', owner_user_id if 'owner_user_id' in locals() else None)
            if not owner_user:
                raise Exception("无法确认账号真实归属，已阻止写入面板备注，避免青龙数据错乱")
            remarks_parts.extend([f'用户:{owner_user}', f'ID:{user_id}', '速看管理'])

            data = {
                "value": value,
                "name": config['dd_sk_osname'],
                "remarks": '丨'.join(remarks_parts)
            }
            data[env_field] = env_value

            headers = {
                "Authorization": "Bearer" + ' ' + self.qltoken,
                "accept": "application/json",
                "Content-Type": "application/json",
            }

            response = safe_request("PUT", url, headers=headers, data=json.dumps(data))

            if response.status_code != 200:
                raise Exception("更新失败，状态码: " + str(response.status_code))

            return True
        except Exception as e:
            logger.error("更新系统变量失败: " + str(e))
            raise

try:
    ql_api = QingLongAPI() if config['dd_sk_qlname'] else None
except Exception as e:
    sender.reply("❌ 系统连接失败: " + str(e))
    exit(0)



def remove_account_env_from_system(account_key):
    env_ref = ql_api.find_env_by_account(account_key, account_key)
    if not env_ref:
        return False
    return ql_api.delete_env(env_ref)

def sync_account_env(account_key,full_cred,nickname,remark=''):
    if not ql_api:return 'local_only'
    env_ref=ql_api.find_env_by_account(account_key,account_key)
    if env_ref:ql_api.update_env(env_ref,full_cred,account_key,nickname,remark,'');return 'updated'
    ql_api.add_env(full_cred,account_key,nickname,remark,'');return 'added'




class NN:
    def __init__(self, full_data=""):
        self.full_data = full_data.strip()
        self.kt = ""
        self.zyeid = ""
        self.user_id = None
        self.nickname = "速看用户"
        self.user_url = 'https://welfare-user.palmestore.com' # 用户信息用
        self.proxy_manager = ProxyManager(config['enable_proxy'], config['proxy_pool_url'])
        self.request_params = {} # 存储解析后的完整参数

        self.parse_input()

    def getRandomUA(self):
        try:
            androidVersions = ['10', '11', '12', '13']
            models = ['M2007J3SC', 'M2012K11C', '22041211AC', '23049RAD8C', 'V2055A', 'V2185A', 'PCDM10', 'PDEM30', 'Redmi K40', 'Mi 10']
            model = random.choice(models)
            androidVer = random.choice(androidVersions)
            buildId = 'SP1A.' + str(random.randint(100000, 999999)) + '.0' + str(random.randint(10, 99))
            return f"Mozilla/5.0 (Linux; Android {androidVer}; {model} Build/{buildId}; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/{random.randint(90, 99)}.0.4951.61 Safari/537.36 zyApp/SuKanRead zyVersion/8.0.2 zyChannel/801004"
        except:
            return "Mozilla/5.0 (Linux; Android 12; M2007J3SC Build/SP1A.123456.012; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/99.0.4951.61 Safari/537.36 zyApp/SuKanRead zyVersion/8.0.2 zyChannel/801004"

    def parse_input(self):
        if not self.full_data: return

        try:
            query_str = ""
            if '?' in self.full_data:
                query_str = self.full_data.split('?', 1)[1]
            else:
                query_str = self.full_data

            params_list = urllib.parse.parse_qsl(query_str)
            self.request_params = dict(params_list)

            self.kt = self.request_params.get('kt') or self.request_params.get('token')
            self.zyeid = self.request_params.get('zyeid') or self.request_params.get('zyeId')

            if not self.kt and self.full_data.startswith('{'):
                try:
                    json_data = json.loads(self.full_data)
                    body = json_data.get('body', {})
                    self.kt = body.get('token') or body.get('kt')
                    self.zyeid = body.get('zyeid') or body.get('zyeId')
                    self.request_params = {'kt': self.kt, 'zyeid': self.zyeid, 'source': 'welfare'}
                except: pass

        except Exception as e:
            logger.error(f"参数解析失败: {e}")

        if self.zyeid:
            self.user_id = self.zyeid

    def get_headers(self):
        return {
            'Host': 'welfare-user.palmestore.com',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://welfare-user.palmestore.com',
            'X-Requested-With': 'com.chaozh.xincao.only.sk',
            'Referer': 'https://welfare-user.palmestore.com/sukanread/welfare-package/sudu/welfare.html',
            'User-Agent': self.getRandomUA()
        }

    def user_info(self):
        try:
            if not self.kt or not self.zyeid:
                return None

            url = f"{self.user_url}/api/user/info"

            params = self.request_params

            if 'source' not in params:
                params['source'] = 'welfare'

            headers = self.get_headers()
            proxies = self.proxy_manager.get_proxy_dict() if config['enable_proxy'] else None

            res = safe_request("GET", url, headers=headers, params=params, proxies=proxies, timeout=10)

            try:
                rj = res.json()
            except:
                return None

            if str(rj.get('code')) == '0':
                body = rj.get('body', {})
                total_coin = body.get('total_coin', 0)
                phone_candidates = detect_phone_candidates(body, self.full_data)
                phone = phone_candidates[0] if phone_candidates else ""

                return {
                    "nickname": "速看用户",
                    "coin": total_coin,
                    "money": 0,
                    "user_id": self.zyeid,
                    "phone": phone,
                    "zyeid": self.zyeid,
                    "token": self.full_data
                }
            return None

        except Exception as e:
            logger.error(f"速看验证失败: {e}")
            return None

def nn_session_ids(input_str):
    try:
        logger.info(f"验证速看数据: {input_str[:30]}...")
        nn = NN(input_str)
        info = nn.user_info()

        if info:
            logger.info("账号验证成功: " + str(info['user_id']))
            submission_str = info['token']
            return {
                "submission_str": submission_str,
                "device_id": info.get('zyeid') or info['user_id'],
                "user_id": info['user_id'],
                "nickname": info['nickname'],
                "phone": info.get('phone', ''),
                "zyeid": info.get('zyeid') or info['user_id'],
            }
        else:
            sender.reply('❌ 验证失败：链接可能已过期或签名无效')
            exit(0)
    except Exception as e:
        logger.error("账号验证失败: " + str(e))
        sender.reply("❌ 验证账号失败: " + str(e))
        exit(0)



def cx(credential):
    try:
        info = NN(credential).user_info()
        return {'nickname': info.get('nickname', '速看用户'), 'coin': info.get('coin', 0)} if info else None
    except Exception as error:
        logger.error('速看查询失败: %s', error)
        return None


def process_single_account(account, index, total, remarks):
    token = sg.bucketGet('dd_sk_token', account)
    credential = decrypt_token(token) if token else ''
    if not credential:
        return f'{index}/{total} {account}：凭证不存在，请重新登录'
    data = cx(credential)
    remark = f"（{remarks[account]}）" if remarks.get(account) else ''
    return f"{index}/{total} {account}{remark}：金币 {data['coin']}" if data else f'{index}/{total} {account}：查询失败'


def cxs():
    try:
        accounts = AccountManager.get_accounts(userid)

        if not accounts:
            sender.reply(f"""
=====未绑定账号=====
❌ 未找到任何账号信息
💡 发送 {config['randomsigncommand']} 绑定
==================""")
            return

        account_remarks = {}
        if config['enable_remark']:
            account_remarks = RemarkManager.get_all_remarks(userid)

        total_count = len(accounts)
        logger.info("用户 " + str(userid) + " 开始批量查询 " + str(total_count) + " 个账号")

        sender.reply(f"🚀 正在并发查询 {total_count} 个账号，请稍候...")

        max_workers = min(10, total_count)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_account = {}
            for index, account in enumerate(accounts, 1):
                future = executor.submit(process_single_account, account, index, total_count, account_remarks)
                future_to_account[future] = account

            for future in as_completed(future_to_account):
                result_msg = future.result()
                if result_msg:
                    sender.reply(result_msg)

    except Exception as e:
        logger.error("批量查询失败: " + str(e))
        sender.reply(f"""
=====查询系统错误=====
❌ 批量查询失败
错误: {str(e)}
==================""")

def get_user_input(timeout=60):
    try:
        logger.info("等待用户输入，超时: " + str(timeout) + "秒")
        response = sender.listen(timeout * 1000)

        if response is None or response == '':
            logger.warning("用户输入超时或为空")
            return None

        response = response.strip()
        logger.info("收到用户输入: " + response)

        if response.lower() in ['q', 'quit', 'exit', '退出', 'cancel']:
            return 'q'

        return response

    except Exception as e:
        logger.error("获取用户输入失败: " + str(e))
        return None

def bindaccount():
    try:
        logger.info("用户 " + str(userid) + " 开始绑定账号")

        remark = ""
        if config['enable_remark']:
            remark_guide = """
=====账号备注设置=====
🎯 请输入账号备注名
------------------
例如: 我的主账号、备用账号等
(可选，最多20个字符)
------------------
回复备注名继续
回复"n"跳过备注
回复"q"退出操作
=================="""
            sender.reply(remark_guide)

            remark_input = get_user_input(timeout=120)
            if remark_input is None:
                sender.reply("⏰ 操作超时，已退出")
                return
            elif remark_input.lower() == 'q':
                sender.reply("✅ 已取消登录")
                return
            elif remark_input.lower() != 'n':
                remark = remark_input.strip()[:20]
                logger.info("用户设置备注: " + remark)

        sender.reply("""
=====速看登录=====
[1] CK登录
[2] 短信登录
------------------
回复对应数字继续
回复"q"退出
==================""")

        login_type = get_user_input(timeout=120)
        if not login_type or login_type == 'q':
            sender.reply("✅ 已退出")
            return

        if login_type.strip() == '1':
            sender.reply("""
=====CK登录=====
请发送抓包的【整段链接】
------------------
包含 https://... 和所有参数
不要删减任何内容
------------------
直接发送数据即可
回复"q"退出
==================""")

            instr = get_user_input(180)
            if not instr or instr == 'q':
                sender.reply("✅ 已退出")
                return

            try:
                login_info = nn_session_ids(instr)
                if login_info and login_info.get("submission_str") and login_info.get("user_id"):
                    save_sukan_device_profile(login_info["submission_str"])
                    process_account_binding(
                        login_info["submission_str"],
                        login_info["device_id"],
                        login_info["user_id"],
                        login_info["nickname"],
                        remark,
                        phone=login_info.get("phone", ""),
                        login_type="ck"
                    )
            except Exception as e:
                sender.reply(f"❌ 验证失败: {e}")
            return

        if login_type.strip() == '2':
            if not CRYPTO_AVAILABLE:
                sender.reply("❌ 当前环境缺少 pycryptodome，无法使用短信登录")
                return

            sender.reply("""
=====短信登录=====
📱 请输入手机号
------------------
回复"q"退出
==================""")
            phone = get_user_input(timeout=120)
            if not phone or phone == 'q':
                sender.reply("✅ 已退出")
                return

            phone = str(phone).strip()
            if not phone.isdigit() or len(phone) != 11:
                sender.reply("❌ 手机号格式错误，请输入11位手机号")
                return

            sender.reply(f"🔄 正在发送验证码到 {phone[:3]}****{phone[7:]}...")
            api = SukanSMSLoginAPI()
            sms_ok, sms_msg = api.send_sms(phone)
            if not sms_ok:
                sender.reply(f"❌ 发送验证码失败: {sms_msg}")
                return

            sender.reply("""
=====短信登录=====
✅ 验证码已发送
📱 请输入验证码
------------------
回复"q"退出
==================""")
            code = get_user_input(timeout=120)
            if not code or code == 'q':
                sender.reply("✅ 已退出")
                return

            sender.reply("🔄 正在登录并生成CK，请稍候...")
            login_ok, _, login_msg = api.login(phone, str(code).strip())
            if not login_ok:
                sender.reply(f"❌ 登录失败: {login_msg}")
                return

            welfare_url = api.generate_welfare_url()
            if not welfare_url:
                sender.reply("❌ 短信登录成功，但生成CK失败")
                return

            save_sukan_device_profile(welfare_url)
            process_account_binding(
                welfare_url,
                api.zyeid,
                api.zyeid,
                "速看用户",
                remark,
                phone=phone,
                login_type="sms"
            )
            return

        sender.reply("❌ 无效选择，请输入 1 或 2")

    except Exception as e:
        logger.error("绑定账号失败: " + str(e))
        sender.reply("❌ 绑定失败: " + str(e))

def process_account_binding(submission_str,device_id,user_id,nickname,remark='',phone='',login_type='ck'):
    account=str(phone or user_id).strip();old=find_account_by_phone(userid,phone) if phone else None
    if old and old!=account:migrate_account_binding_if_needed(userid,old,account)
    if account in AccountManager.get_accounts(userid):AccountManager.update_account_credentials(account,submission_str)
    else:AccountManager.add_account(userid,account);sg.bucketSet('dd_sk_token',account,encrypt_token(submission_str))
    set_account_meta(account,{'phone':str(phone or ''),'zyeid':str(user_id or ''),'device_id':str(device_id or ''),'login_type':login_type,'last_login_time':datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
    if remark:RemarkManager.set_account_remark(userid,account,remark)
    try:status=sync_account_env(account,submission_str,nickname,remark)
    except Exception as error:logger.error('同步变量失败: %s',error);status='failed'
    sender.reply(f'账号 {account} 绑定成功，变量状态：{status}')



def xy_manage():
    accounts=AccountManager.get_accounts(userid)
    if not accounts:return sender.reply('未绑定账号，请发送【速看登录】')
    remarks=RemarkManager.get_all_remarks(userid);rows=[f'{i}. {account}'+(f' - {remarks[account]}' if remarks.get(account) else '') for i,account in enumerate(accounts,1)]
    sender.reply('速看账号：\n'+'\n'.join(rows)+'\nd. 删除全部；q. 退出')
    choice=get_user_input(60)
    if choice in (None,'q'):return
    if choice.lower()=='d':return batch_delete_all_accounts(accounts)
    try:account=accounts[int(choice)-1]
    except (ValueError,IndexError):return sender.reply('序号无效')
    manage_single_account(account,remarks)


def manage_single_account(account,remarks):
    sender.reply(f'{account}：\n1. 删除账号\n2. 修改备注\n3. 重新同步变量\nq. 退出')
    choice=get_user_input(60)
    if choice=='1':
        sender.reply('回复 y 确认删除')
        if str(get_user_input(60)).lower()=='y':AccountManager.remove_account(userid,account);remove_account_env_from_system(account);sg.bucketDel('dd_sk_token',account);RemarkManager.delete_account_remark(userid,account);sender.reply('账号已删除')
    elif choice=='2':
        sender.reply('请输入新备注，n 清空');remark=get_user_input(60)
        if remark=='n':RemarkManager.delete_account_remark(userid,account);remark=''
        elif remark:RemarkManager.set_account_remark(userid,account,remark[:20])
        else:return
        token=sg.bucketGet('dd_sk_token',account);full=decrypt_token(token) if token else ''
        if full:sync_account_env(account,full,f'用户{account}',remark);sender.reply('备注已更新')
    elif choice=='3':
        token=sg.bucketGet('dd_sk_token',account);full=decrypt_token(token) if token else ''
        if not full:return sender.reply('账号凭证不存在，请重新登录')
        sender.reply(f'同步结果：{sync_account_env(account,full,f"用户{account}",remarks.get(account,""))}')






def batch_delete_all_accounts(accounts):
    sender.reply(f'确认删除全部 {len(accounts)} 个账号？回复 y 确认')
    if str(get_user_input(60)).lower()!='y':return sender.reply('已取消')
    for account in accounts:
        AccountManager.remove_account(userid,account);remove_account_env_from_system(account);sg.bucketDel('dd_sk_token',account);RemarkManager.delete_account_remark(userid,account)
    sender.reply('全部账号已删除')





def show_tutorial():
    sender.reply('【速看登录】绑定账号；【速看查询】查询账号；【速看管理】删除、备注或重新同步变量。')


if '登录' in usermessage or '登陆' in usermessage:
    bindaccount()
elif '管理' in usermessage:
    xy_manage()
elif '查询' in usermessage:
    cxs()
elif usermessage == '速看教程':
    show_tutorial()
else:
    sender.setContinue()
