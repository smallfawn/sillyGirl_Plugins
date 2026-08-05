# [title: 速看小说带短信]
# [name: suKanXiaoShuoDaiDuanXin]
# [language: python]
# [class: 任务]
# [author: 8165799]
# [version: v3.6]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(速看)(登录|登陆)$|^登(录|陆)(速看)$|^(速看)(查询|管理)$|^(查询|管理)(速看)$|^速看清理$|^速看$|^速看教程$|^清理速看$|^速看广播 ?(.*)$|^速看通知 ?(.*)$]
# [cron: 56 9,19 * * *]
# [icon: https://api.iconify.design/lucide:bot.svg]
# [description: 速看小说代挂提交插件，支持抓包完整URL整段提交和短信登录；1. 严格执行整段提交：用户发送的完整URL直接存入青龙，不进行任何参数分割或重组；2. 修复因缺失签名参数导致的脚本运行失败问题；3.支持青龙/呆呆变量同步]
# [depe: ["pycryptodome", "requests"]]
# [staticmethod: def _get_env_identity(env_ref):]


import asyncio as _sg_asyncio, os as _sg_os, time as _sg_time, types as _sg_types, json as _sg_json, re as _sg_re, urllib.parse as _sg_urlparse
from threading import Thread as _sg_Thread
from sillygirl import Adapter as _SGAdapter, Bucket as _SGBucket, Sender as _SGSender, sender as _sg_sender, container as _sg_container, form
try: import ast as _sg_ast
except Exception: _sg_ast=None
try: import decimal as decimal
except Exception: decimal=None

def _sg_run(coro):
    try: _sg_asyncio.get_running_loop(); running=True
    except RuntimeError: running=False
    if not running: return _sg_asyncio.run(coro)
    box={}
    def r():
        try: box["v"]=_sg_asyncio.run(coro)
        except BaseException as e: box["e"]=e
    t=_sg_Thread(target=r,daemon=True); t.start(); t.join()
    if "e" in box: raise box["e"]
    return box.get("v")

def _sg_literal(v, default=None):
    if isinstance(v,(list,dict,tuple,set,int,float,bool)) or v is None: return v if v is not None else ([] if default is None else default)
    t=str(v or "").strip()
    if not t: return [] if default is None else default
    for p in (_sg_json.loads, (_sg_ast.literal_eval if _sg_ast else None)):
        if p:
            try: return p(t)
            except Exception: pass
    return [] if default is None else default

def _sg_sender_sync(uuid=""):
    s=_SGSender(uuid or _sg_os.environ.get("SENDER_ID","")); c=lambda n,*a,**k:_sg_run(getattr(s,n)(*a,**k))
    def wait(timeout=60000,*a,**k):
        try:
            r=c("listen",{"timeout":int(timeout or 0)}); return _sg_run(r.getContent()) if r else ""
        except Exception: return ""
    return _sg_types.SimpleNamespace(getUserID=lambda:c("getUserId"),getUserId=lambda:c("getUserId"),getMessage=lambda:c("getContent"),getContent=lambda:c("getContent"),getUserName=lambda:c("getUserName"),getNickname=lambda:c("getUserName"),getChatID=lambda:c("getChatId"),getChatId=lambda:c("getChatId"),getImtype=lambda:c("getPlatform"),getPlatform=lambda:c("getPlatform"),getMessageID=lambda:c("getMessageId"),getPluginName=lambda:_sg_os.environ.get("PLUGIN_NAME",""),getPluginVersion=lambda:_sg_os.environ.get("PLUGIN_VERSION",""),isAdmin=lambda:bool(c("isAdmin")),reply=lambda m="":c("reply",str(m)),replyImage=lambda u="":c("reply",str(u) if str(u).startswith("[") else f"[CQ:image,file={u}]"),listen=wait,input=wait,waitInput=wait,setContinue=lambda *a,**k:c("continue_"),breakIn=lambda *a,**k:c("continue_"))

def _sg_bucket_get(bucket=None,key=None,default="",**kw):
    try:
        v=_SGBucket(str(kw.get("bucket",bucket) or ""))[str(kw.get("key",key) or "")]; return default if v in (None,"") and default not in (None,"") else (v if v is not None else "")
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
    i=a[0] if a and isinstance(a[0],dict) else {}; pf=i.get("imType") or i.get("platform") or kw.get("platform") or (a[0] if a else ""); g=i.get("groupCode") or i.get("group_id") or kw.get("group_id") or (a[1] if len(a)>1 else ""); u=i.get("userID") or i.get("user_id") or kw.get("userID") or (a[2] if len(a)>2 else ""); title=i.get("title") or kw.get("title") or (a[3] if len(a)>3 else ""); m=i.get("content") or i.get("message") or kw.get("content") or (a[4] if len(a)>4 else title); return _sg_run(_SGAdapter(str(pf or "")).push({"group_id":str(g or ""),"user_id":str(u or ""),"title":str(title or ""),"content":str(m or "")}))
def _sg_notify(m,channels=None,*a,**k): return _sg_run(_sg_sender.pushAdmin(str(m),{"platforms":list(channels or [])} if channels else {}))
class _SGFacade:
    Sender=staticmethod(_sg_sender_sync); getSenderID=staticmethod(lambda:_sg_os.environ.get("SENDER_ID","")); getPluginName=staticmethod(lambda:_sg_os.environ.get("PLUGIN_NAME","")); bucketGet=staticmethod(_sg_bucket_get); bucketSet=staticmethod(_sg_bucket_set); bucketDel=staticmethod(_sg_bucket_del); bucketDelete=staticmethod(_sg_bucket_del); bucketAllKeys=staticmethod(_sg_bucket_keys); bucketKeys=staticmethod(_sg_bucket_keys); bucketAll=staticmethod(_sg_bucket_all); notifyMasters=staticmethod(_sg_notify); pushAdmin=staticmethod(_sg_notify); push=staticmethod(_sg_push); Push=staticmethod(_sg_push); reply=staticmethod(lambda m="":_sg_sender_sync().reply(m)); get=staticmethod(lambda k,default="":_sg_bucket_get(*(str(k).split(".",1) if "." in str(k) else ["otto",k]),default=default)); getParam=get; version=staticmethod(lambda:{"sn":_sg_os.environ.get("SILLYGIRL_VERSION","3.0.0"),"version":_sg_os.environ.get("SILLYGIRL_VERSION","3.0.0")}); port=staticmethod(lambda:_sg_os.environ.get("SILLYGIRL_PORT","8080")); sleep=staticmethod(lambda sec:_sg_time.sleep(float(sec or 0)))
sg=_SGFacade(); Sender=sg.Sender; getSenderID=sg.getSenderID; bucketGet=sg.bucketGet; bucketSet=sg.bucketSet; bucketAllKeys=sg.bucketAllKeys; notifyMasters=sg.notifyMasters
mask_account=lambda v: (str(v or "") if len(str(v or ""))<=7 else str(v or "")[:3]+"***"+str(v or "")[-4:])
def generate_qrcode_url(t): return "https://api.qrserver.com/v1/create-qr-code/?size=260x260&data="+_sg_urlparse.quote(str(t or ""))
def get_pay_config(): return {}
class MaPayClient:
    def create_order(self,*a,**k): return {"error":"","status":True,"data":None}
    def is_paid(self,*a,**k): return True
calculate_auth_time=lambda *a,**k:"2099-12-31"; check_auth_status=lambda *a,**k:"账号默认可用"; _check_auth_status=check_auth_status
process_authorization=lambda *a,**k: True; process_coin_payment=lambda *a,**k: True; admin_auth_all_accounts=lambda *a,**k: True; admin_auth_by_user=lambda *a,**k: True
def select_accounts(sender,user_bucket,user_id,*a,**k):
    raw=sg.bucketGet(user_bucket,user_id,[]); raw=_sg_literal(raw,[]) if isinstance(raw,str) else raw; raw=(list(raw.keys()) or list(raw.values())) if isinstance(raw,dict) else raw; return (raw if isinstance(raw,list) else []),(raw if isinstance(raw,list) else [])
def get_user_points(user_id=None,bucket="dd_sign_points"):
    try: return int(sg.bucketGet(bucket,user_id or sg.getSenderID()) or 0)
    except Exception: return 0
def update_user_points(user_id=None,points=0,bucket="dd_sign_points"): return sg.bucketSet(bucket,user_id or sg.getSenderID(),str(points))
def _sg_panel_id(config=None):
    if isinstance(config,dict): config=config.get("id") or config.get("ID") or config.get("index") or config.get("name")
    m=_sg_re.search(r"\d+",str(config or "")); return int(m.group(0)) if m else 1
class QingLongClient:
    def __init__(self,env_name="",config=None,*a,**k): self.env_name=str(env_name or ""); self.client=_sg_container.QingLong({"id":_sg_panel_id(config)})
    def get_envs(self,search=""): return _sg_run(self.client.getEnvs(search or "")) or []
    all_envs=search_envs=envGet=get_envs
    def add_envs(self,envs): return _sg_run(self.client.createEnv(envs if isinstance(envs,list) else [envs]))
    def add_env(self,name,value="",remarks=""): return self.add_envs({"name":name,"value":value,"remarks":remarks})
    def update_env(self,env): return _sg_run(self.client.updateEnv(env))
    def delete_env(self,name_or_id,*a,**k): return _sg_run(self.client.deleteEnvs([name_or_id]))
    envSet=add_envs; envUpdate=update_env; envDel=delete_env
class DadaiPanelClient(QingLongClient):
    def __init__(self,env_name="",config=None,*a,**k): self.env_name=str(env_name or ""); self.client=_sg_container.DaiDai({"id":_sg_panel_id(config)})
DumbPanelClient=DadaiPanelClient

config = form({
    'dd_sk_rsa_private_key': form.string().title('RSA签名私钥PEM').default('').description('速看接口签名私钥，留空则短信/签名登录不可用'),
})
_CONFIG_FIELD_MAP = {
    ('dd_sk', 'rsa_private_key'): 'dd_sk_rsa_private_key',
}

import re
import ast
from datetime import datetime, timedelta
import urllib.parse
from decimal import Decimal
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
    """获取插件完整配置"""
    dd_sk_osname = sg.bucketGet('dd_sk', 'dd_sk_osname') or 'S_SUKAN'
    dd_sk_qlname = sg.bucketGet('dd_sk', 'dd_sk_qlname') or ''
    dd_managecommand = sg.bucketGet('dd_sk', 'dd_managecommand') or '速看管理'
    dd_querycommand = sg.bucketGet('dd_sk', 'dd_querycommand') or '速看查询'
    dd_signcommand = sg.bucketGet('dd_sk', 'dd_signcommand') or '速看登录'
    zsm = sg.bucketGet('dd_sk', 'zsm') or ''

    enable_proxy = sg.bucketGet('dd_sk', 'enable_proxy') or 'false'
    enable_proxy = enable_proxy.lower() == 'true'
    proxy_pool_url = sg.bucketGet('dd_sk', 'proxy_pool_url') or ''

    points_bucket = sg.bucketGet('dd_sk', 'points_bucket') or 'dd_sign_points'

    enable_remark = sg.bucketGet('dd_sk', 'enable_remark') or 'false'
    enable_remark = enable_remark.lower() == 'true'

    randommanagecommand = dd_managecommand
    randomquerycommand = dd_querycommand
    randomsigncommand = dd_signcommand

    try:
        skVipmoney = Decimal(sg.bucketGet('dd_sk', 'skVipmoney') or '1')
    except:
        skVipmoney = Decimal('1')

    try:
        skcoin = int(sg.bucketGet('dd_sk', 'skcoin') or '0')
    except:
        skcoin = 0

    show_point_status = sg.bucketGet('dd_sk', 'show_point_status') or 'false'
    show_point_status = show_point_status.lower() == 'true'

    use_ma_pay = '2099-12-31' or 'false'
    use_ma_pay = use_ma_pay.lower() == 'true'

    epay_url = '2099-12-31' or ''
    epay_pid = '2099-12-31' or ''
    epay_key = '2099-12-31' or ''
    epay_alipay = ('2099-12-31' or 'true').lower() == 'true'
    epay_wxpay = ('2099-12-31' or 'false').lower() == 'true'
    epay_qqpay = ('2099-12-31' or 'false').lower() == 'true'

    try:
        reminder_days = int(sg.bucketGet('dd_sk', 'reminder_days') or '2')
    except:
        reminder_days = 2

    if not dd_sk_qlname:
        sender.reply("❌ 对接系统配置未设置")
        exit(0)

    if not dd_sk_osname:
        sender.reply("❌ 变量名称未设置")
        exit(0)

    return {
        'dd_sk_osname': dd_sk_osname,
        'dd_sk_qlname': dd_sk_qlname,
        'dd_managecommand': dd_managecommand,
        'dd_querycommand': dd_querycommand,
        'dd_signcommand': dd_signcommand,
        'randommanagecommand': randommanagecommand,
        'randomquerycommand': randomquerycommand,
        'randomsigncommand': randomsigncommand,
        'zsm': zsm,
        'enable_proxy': enable_proxy,
        'proxy_pool_url': proxy_pool_url,
        'points_bucket': points_bucket,
        'enable_remark': enable_remark,
        'skVipmoney': skVipmoney,
        'skcoin': skcoin,
        'show_point_status': show_point_status,
        'use_ma_pay': use_ma_pay,
        'epay_url': epay_url,
        'epay_pid': epay_pid,
        'epay_key': epay_key,
        'epay_alipay': epay_alipay,
        'epay_wxpay': epay_wxpay,
        'epay_qqpay': epay_qqpay,
        'reminder_days': reminder_days
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

def send_user_notice(user_id, msg, title="速看小说通知"):
    user_id = str(user_id or "").strip()
    if not user_id:
        return False
    imtype = ""
    try:
        imtype = str(sender.getImtype() or "")
    except:
        pass
    if not imtype or imtype.lower() in ["fake", "cron"]:
        imtype = sg.bucketGet(_RUNTIME_BUCKET, _RUNTIME_KEY + "_imtype") or ""
    try:
        if imtype:
            sg.Push(imtype, "", user_id, title, msg)
            return True
    except Exception as e:
        logger.warning(f"Push发送失败 {user_id}: {e}")
    return False

def safe_send_message(user_id, msg, log_context=""):
    ok = send_user_notice(user_id, msg)
    if not ok:
        logger.warning(f"消息发送失败 {log_context}")
    return ok


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


def get_sukan_sms_device_profiles():
    profiles = []
    learned = get_sukan_sms_device_profile()
    if learned:
        profiles.append(learned)
    for profile in SK_SMS_DEVICE_PROFILES:
        candidate = dict(profile)
        if not any(candidate == existing for existing in profiles):
            profiles.append(candidate)
    return profiles


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


def empower(empowertime, days):
    """授权时间计算 - 按天计算"""
    try:
        today_date = datetime.now().date()
        if len(empowertime) == 0 or empowertime <= str(today_date):
            delayed_date = today_date + timedelta(days=days)
        elif empowertime > str(today_date):
            empower_date = datetime.strptime(empowertime, "%Y-%m-%d")
            delayed_date = empower_date + timedelta(days=days)
            delayed_date = delayed_date.date()
        else:
            raise Exception('时间计算出错！')
        return str(delayed_date)
    except Exception as e:
        logger.error("授权时间计算失败: " + str(e))
        raise Exception("授权时间计算失败: " + str(e))

def _build_epay_sign(params_dict, key, exclude_keys=('sign', 'sign_type')):
    return True

def _create_epay_qr(out_trade_no, channel, project_name, money_str):
    return True

def process_epay_pay(amount, months, channel, order_prefix="SK"):
    return True


class ProxyManager:
    """代理管理器"""

    def __init__(self, enable_proxy=False, proxy_pool_url=''):
        self.enable_proxy = enable_proxy
        self.proxy_pool_url = proxy_pool_url
        self.current_proxy = None
        self.last_fetch_time = 0
        self.proxy_cache_time = 300  # 代理缓存5分钟

    def get_proxy(self):
        """获取代理"""
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
        """强制更换代理"""
        self.current_proxy = None
        self.last_fetch_time = 0
        return self.get_proxy()

    def get_proxy_dict(self):
        """获取requests格式的代理字典"""
        proxy = self.get_proxy()
        if not proxy:
            return None

        return {
            'http': proxy,
            'https': proxy
        }


class RemarkManager:
    """账号备注管理器"""

    @staticmethod
    def get_account_remark(user_id, account_id):
        """获取账号备注"""
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
        """设置账号备注"""
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
        """获取用户所有账号的备注"""
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
        """删除账号备注"""
        try:
            sg.bucketDel(bucket='dd_sk_remarks', key=f'{user_id}_{account_id}')
            logger.info("删除备注: " + str(user_id) + " - " + str(account_id))
            return True
        except Exception as e:
            logger.error("删除备注失败: " + str(user_id) + " - " + str(account_id) + " - " + str(e))
            return False


def safe_request(method, url, **kwargs):
    """安全的请求包装函数，支持代理"""
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
        except Exception as retry_e:
            raise Exception("SSL验证失败: " + str(e))
    except requests.exceptions.RequestException as e:
        logger.error("请求失败: " + url + " - " + str(e))
        raise Exception("请求失败: " + str(e))
    except Exception as e:
        logger.error("请求异常: " + url + " - " + str(e))
        raise Exception("请求异常: " + str(e))


def encrypt_token(token):
    """简单加密Token (这里用于加密凭证)"""
    try:
        return base64.b64encode(token.encode()).decode()
    except:
        return token

def decrypt_token(encrypted_token):
    """解密Token (这里用于解密凭证)"""
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
    """账号管理类"""

    @staticmethod
    def get_accounts(user_id):
        """获取用户账号列表"""
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
        """添加账号（去重）"""
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
        """移除账号"""
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
        """更新账号的凭证 (Token/URL)"""
        try:
            encrypted = encrypt_token(full_credential)
            sg.bucketSet(bucket='dd_sk_token', key=account_key, value=encrypted)
            return True
        except Exception as e:
            logger.error("更新凭证失败: " + str(e))
            return False

    @staticmethod
    def get_all_users():
        """获取所有绑定了速看账号的用户"""
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
    """系统对接API封装"""

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
        """获取系统Token"""
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
        """获取所有环境变量"""
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
        """兼容青龙不同版本的 id / _id 字段"""
        if not env_ref:
            return None, None

        if isinstance(env_ref, dict):
            if env_ref.get('id') is not None:
                return 'id', env_ref.get('id')
            if env_ref.get('_id') is not None:
                return '_id', env_ref.get('_id')

        return 'id', env_ref

    def find_env_by_account(self, value_snippet, user_id=None):
        """
        根据Token片段或用户ID查找环境变量
        优先匹配用户ID(ID:xxxxx)防止变量重复
        """
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
        """删除环境变量"""
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
        """添加环境变量"""
        try:
            url = self.QLurl + "/open/envs"
            value = full_value

            remarks_parts = [f'速看:{nickname}']

            if auth_time:
                remarks_parts.append(f'到期:{auth_time}')
            else:
                remarks_parts.append('到期:未授权')

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
        """更新环境变量"""
        try:
            env_field, env_value = self._get_env_identity(env_id)
            if not env_value:
                raise Exception("系统变量ID为空")

            url = self.QLurl + "/open/envs"
            value = full_value

            remarks_parts = [f'速看:{nickname}']

            if auth_time:
                remarks_parts.append(f'到期:{auth_time}')
            else:
                remarks_parts.append('到期:未授权')

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
    ql_api = QingLongAPI()
except Exception as e:
    sender.reply("❌ 系统连接失败: " + str(e))
    exit(0)


def parse_auth_date(auth_time):
    return '2099-12-31'


def get_account_auth_status(account_key):
    return '2099-12-31'


def remove_account_env_from_system(account_key):
    """按账号ID兜底删除青龙变量"""
    env_ref = ql_api.find_env_by_account(account_key, account_key)
    if not env_ref:
        return False
    return ql_api.delete_env(env_ref)


def sync_account_env(account_key, full_cred, nickname, remark=""):
    """根据授权状态决定是否同步到青龙"""
    auth_time, _, is_authorized = get_account_auth_status(account_key)
    env_ref = ql_api.find_env_by_account(account_key, account_key)

    if not is_authorized:
        if env_ref:
            ql_api.delete_env(env_ref)
            return 'removed'
        return 'local_only'

    if not full_cred:
        raise Exception(f"账号 {account_key} 凭证不存在，无法同步到系统")

    if env_ref:
        ql_api.update_env(env_ref, full_cred, account_key, nickname, remark, auth_time)
        return 'updated'

    ql_api.add_env(full_cred, account_key, nickname, remark, auth_time)
    return 'added'


def parse_sukan_env_remarks(remarks):
    """解析速看青龙备注中的关键字段"""
    if not remarks:
        return {}

    info = {}
    for part in remarks.split('丨'):
        part = part.strip()
        if not part or ':' not in part:
            continue
        key, value = part.split(':', 1)
        info[key.strip()] = value.strip()
    return info


def clean_expired_envs_from_qinglong(today_date):
    """兜底清理青龙中已过期的速看变量，防止本地账密缺失导致残留"""
    cleaned_count = 0

    try:
        envs = ql_api.get_all_envs()
    except Exception as e:
        logger.error(f"获取青龙变量列表失败，无法执行兜底清理: {str(e)}")
        return 0

    for env in envs:
        try:
            if env.get('name') != config['dd_sk_osname']:
                continue

            remarks = env.get('remarks', '') or ''
            is_sukan_env = ('速看管理' in remarks) or ('速看:' in remarks and '到期:' in remarks)
            if not is_sukan_env:
                continue

            info = parse_sukan_env_remarks(remarks)
            expire_str = info.get('到期', '')
            if not expire_str or expire_str == '未授权':
                continue

            expire_date = parse_auth_date(expire_str)
            if not expire_date or expire_date >= today_date:
                continue

            if ql_api.delete_env(env):
                cleaned_count += 1
                account_key = info.get('ID', '')
                if account_key:
                    sg.bucketDel(bucket='dd_sk_token', key=account_key)
                    True
                logger.info(f"青龙兜底清理已过期变量成功: {account_key or remarks}")
            else:
                logger.error(f"青龙兜底清理已过期变量失败: {remarks}")
        except Exception as e:
            logger.error(f"处理青龙速看变量兜底清理失败: {str(e)}")

    return cleaned_count


class NN:
    """速看(SuKan) 核心类"""
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
        """参考脚本生成随机UA"""
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
        """解析抓包数据 - 提取完整参数，不做任何阉割"""
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
        """获取速看专用Header"""
        return {
            'Host': 'welfare-user.palmestore.com',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://welfare-user.palmestore.com',
            'X-Requested-With': 'com.chaozh.xincao.only.sk',
            'Referer': 'https://welfare-user.palmestore.com/sukanread/welfare-package/sudu/welfare.html',
            'User-Agent': self.getRandomUA()
        }

    def user_info(self):
        """获取用户信息 (全参校验)"""
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
    """验证速看数据有效性"""
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


def cx(full_credential):
    """速看查询功能"""
    try:
        nn = NN(full_credential)
        info = nn.user_info()

        if not info:
            return {
                "nickname": "速看用户",
                "coin": "❓失效需更新",
                "money": 0
            }

        return {
            "nickname": info.get("nickname", "未知用户"),
            "coin": info.get("coin", 0),
            "money": 0
        }

    except Exception as e:
        logger.error("速看查询失败: " + str(e))
        return None

def process_single_account(account_key, index, total_count, account_remarks):
    """处理单个账号查询"""
    try:
        enc_cred = sg.bucketGet(bucket='dd_sk_token', key=f'{account_key}')
        full = decrypt_token(enc_cred) if enc_cred else None

        accountVip = '2099-12-31'

        remark = ""
        remark_display = ""
        if config['enable_remark']:
            remark = account_remarks.get(account_key, "")
            remark_display = f"\n📝 备注: {remark}" if remark else ""

        today_time = str(datetime.now().date())
        if not accountVip:
            auth_status = "⚠️ 未授权"
            auth_time = "无"
        elif accountVip <= today_time:
            auth_status = "❌ 已过期"
            auth_time = accountVip
        else:
            auth_status = "✅ 已授权"
            auth_time = accountVip

        if accountVip and accountVip > today_time and full:
            try:
                data = cx(full)

                if not data:
                    return None

                point_status_info = ""
                if config['show_point_status']:
                    point_status_info = f"\n📊 状态: {'✅ 有效' if data['coin'] != '❓失效需更新' else '❌ 需更新'}"

                account_info = f"""
=====速看账号详情({index}/{total_count})=====
🔑 ID: {account_key}{remark_display}
🔐 授权状态: {auth_status}
📅 到期时间: {auth_time}
💰 当前金币: {data['coin']}{point_status_info}
=================="""
                return account_info

            except Exception as e:
                logger.error("账号 " + account_key + " 查询失败: " + str(e))
                return f"""
=====速看查询失败=====
🔑 ID: {account_key}
❌ 错误: {str(e)[:50]}...
=================="""
        else:
            logger.warning("账号 " + account_key + " 未授权或凭证无效")
            return f"""
=====速看授权过期=====
🔑 ID: {account_key}{remark_display}
🔐 授权状态: {auth_status}
📅 到期时间: {auth_time}
=================="""
    except Exception as e:
        logger.error(f"处理账号 {account_key} 失败: {str(e)}")
        return None

def cxs():
    """速看批量查询"""
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
    """获取用户输入"""
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
    """绑定速看账号 - 支持CK登录和短信登录"""
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


def process_account_binding(submission_str, device_id, user_id, nickname, remark="", phone="", login_type="ck"):
    """处理账号绑定逻辑"""
    account_key = str(phone or user_id).strip() # 优先使用手机号归一化，兼容旧zyeid
    full_cred = submission_str # 存入完整的 Query String (包含所有p参数)

    try:
        old_account_key = None
        if phone:
            old_account_key = find_account_by_phone(userid, phone)
            if not old_account_key and str(user_id) != account_key:
                old_account_key = str(user_id)
        elif str(user_id) != account_key:
            old_account_key = str(user_id)

        if old_account_key and old_account_key != account_key:
            migrate_account_binding_if_needed(userid, old_account_key, account_key)

        vip, _, is_authorized = get_account_auth_status(account_key)

        if is_authorized:
            auth_status = f'✅ 已授权 ({vip})'
            next_step = f'发送 {config["randommanagecommand"]} 可管理账号'
        else:
            auth_status = '⚠️ 未授权'
            next_step = f'发送 {config["randommanagecommand"]} 进行授权以自动激活'

        remark_info = f"\n📝 备注: {remark}" if remark else ""

        exists = account_key in AccountManager.get_accounts(userid)
        if exists:
            AccountManager.update_account_credentials(account_key, full_cred)
            logger.info("更新已存在账号的凭证: " + account_key)
        else:
            AccountManager.add_account(userid, account_key)
            enc = encrypt_token(full_cred)
            sg.bucketSet(bucket='dd_sk_token', key=account_key, value=enc)
            logger.info("添加新账号: " + account_key)

        set_account_meta(account_key, {
            "phone": str(phone or "").strip(),
            "zyeid": str(user_id or "").strip(),
            "device_id": str(device_id or "").strip(),
            "login_type": str(login_type or "ck").strip(),
            "last_login_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })

        if config['enable_remark'] and remark:
            RemarkManager.set_account_remark(userid, account_key, remark)

        ql_msg = ""
        try:
            sync_result = sync_account_env(account_key, full_cred, nickname, remark)
            if sync_result == 'updated':
                ql_msg = "\n🔄 状态: ✅ 已同步到系统"
            elif sync_result == 'added':
                ql_msg = "\n🔄 状态: ✅ 已添加到系统"
            elif sync_result == 'removed':
                ql_msg = "\n🔄 状态: ⏸️ 未授权，已从系统移除，仅保留本地"
            else:
                ql_msg = "\n🔄 状态: ⏸️ 未授权，仅保留本地"
        except Exception as e:
            logger.error("更新系统变量失败: " + str(e))
            ql_msg = "\n🔄 状态: ❌ 系统同步失败"

        success_msg = f"""
=====速看账号绑定=====
✅ 绑定成功!
🔑 ID: {account_key}{remark_info}
🔐 授权: {auth_status}{ql_msg}
⏰ 下一步操作:
   {next_step}
=================="""

        sender.reply(success_msg)
        logger.info(f"用户 {userid} 绑定账号成功: {account_key}, 备注: {remark}")

    except Exception as e:
        logger.error("处理账号绑定失败: " + str(e))
        raise


def process_payment(project, months, accountVip, full_credential, nickname, account_key, remark=""):
    return True
def process_wechat_pay(project, amount, months):
    """处理微信支付"""
    try:
        if False:
            sender.reply('⚠️ 当前有人正在支付,请稍后再试！')
            return False

        pay_msg = f"""
=====微信扫在线处理====
🎫 商品: {project}
📅 时长: {months}月
💰 金额: {amount}元
------------------
请使用微信扫在线处理
回复"q"取消支付
=================="""
        sender.reply(pay_msg)
        sender.replyImage(config['zsm'])

        payment_result = False

        if str(payment_result) == 'q':
            sender.reply('✅ 已取消支付')
            return False

        money_received = 0
        payer = ""

        if isinstance(payment_result, dict):
            if payment_result.get('Type') in ['微信赞赏', '微信收款']:
                money_received = float(payment_result.get('Money', 0))
                payer = payment_result.get('FromName', '')
            elif payment_result.get('Money'):
                money_received = float(payment_result.get('Money', 0))
                payer = payment_result.get('FromName', '')
            elif payment_result.get('money'):
                money_received = float(payment_result.get('money', 0))
                payer = payment_result.get('fromName', '')
        else:
            try:
                result_data = json.loads(payment_result)
                if result_data.get('Type') in ['微信赞赏', '微信收款']:
                    money_received = float(result_data.get('Money', 0))
                    payer = result_data.get('FromName', '')
                else:
                    money_received = float(result_data.get('Money', 0))
                    payer = result_data.get('FromName', '')
            except:
                sender.reply("❌ 无法解析支付结果")
                return False

        if money_received >= float(amount):
            return True
        else:
            sender.reply(f"""
=====支付金额错误=====
💰 应付: {amount}元
💳 实付: {money_received}元
{f'👤 付款人: {payer}' if payer else ''}

❗ 请稍后核对支付记录！
==================""")
            return False

    except Exception as e:
        logger.error("微信支付失败: " + str(e))
        sender.reply("❌ 支付失败: " + str(e))
        return False


def process_mapay_pay(project, amount, months, ma_pay_config):
    return True


def process_points_pay(points_needed, months):
    """处理积分支付"""
    try:
        user_points = int(sg.bucketGet(config['points_bucket'], userid) or '0')

        if user_points < points_needed:
            sender.reply(f"""
==================
    积分不足
==================
👤 当前积分: {user_points}
📍 需要积分: {points_needed}
==================""")
            return False

        confirm_msg = f"""
==================
    积分支付确认
==================
💫 消耗积分: {points_needed}
⏰ 授权时长: {months}月
------------------
确认请回复【y】
取消请回复【n】
=================="""
        sender.reply(confirm_msg)

        yesorno = get_user_input(timeout=120000)
        if yesorno and yesorno.lower() in ['y', '是', 'yes']:
            new_balance = user_points - points_needed
            sg.bucketSet(config['points_bucket'], userid, str(new_balance))
            logger.info(f"用户 {userid} 消耗积分 {points_needed}，剩余 {new_balance}")
            return True
        else:
            sender.reply("✅ 已取消支付")
            return False

    except Exception as e:
        logger.error("积分支付失败: " + str(e))
        sender.reply("❌ 积分支付失败: " + str(e))
        return False


def xy_manage():
    """速看账号管理"""
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

    count = 1
    account_list = """
======我的速看账号====="""
    today_time = str(datetime.now().date())

    try:
        for account in accounts:
            accountVip = '2099-12-31'
            if not accountVip:
                vip_status = '⚠️ 未授权'
            elif accountVip < today_time:
                vip_status = '❌ 已过期'
            else:
                vip_status = f'✅ {accountVip}'

            remark = ""
            if config['enable_remark']:
                remark = account_remarks.get(account, "")
            remark_display = f" - {remark}" if remark else ""

            account_list += f"""
------------------
[{count}] 账号信息
🔑 ID: {account}{remark_display}
🔐 授权: {vip_status}"""
            count += 1

        account_list += """
------------------
[b] 批量授权所有账号
[d] 批量删除所有账号
[q] 退出管理
=================="""

        sender.reply(account_list)

        response = get_user_input(timeout=60)
        if response is None:
            sender.reply('⏰ 操作超时,已退出')
            return
        elif response == 'q':
            sender.reply('✅ 已退出管理')
            return

        if response.lower() == 'b':
            batch_auth_all_accounts(accounts, account_remarks)
            return
        elif response.lower() == 'd':
            batch_delete_all_accounts(accounts)
            return

        try:
            choice_num = int(response)
            if choice_num < 1 or choice_num >= count:
                sender.reply('❌ 输入的序号无效')
                return
        except ValueError:
            sender.reply('❌ 输入必须是数字')
            return

        manage_single_account(accounts[choice_num - 1], account_remarks)

    except Exception as e:
        logger.error("账号管理失败: " + str(e))
        sender.reply(f"""
=====账号处理错误=====
❌ 账号列表处理失败
⚠️ 错误: {str(e)}
==================""")


def manage_single_account(account, account_remarks):
    """管理单个账号"""
    try:
        encrypted_cred = sg.bucketGet(bucket='dd_sk_token', key=f'{account}')
        full_cred = decrypt_token(encrypted_cred) if encrypted_cred else ""

        accountVip = '2099-12-31'

        remark = ""
        if config['enable_remark']:
            remark = account_remarks.get(account, "")

        today_time = str(datetime.now().date())

        if not accountVip:
            vip_status = '⚠️ 未授权'
        elif accountVip < today_time:
            vip_status = '❌ 已过期'
        else:
            vip_status = f'✅ {accountVip}'

        remark_info = f"\n📝 备注: {remark}" if remark else ""

        account_info = f"""
=====账号详情=====
🔑 ID: {account}{remark_info}
🔐 授权: {vip_status}
=================="""
        sender.reply(account_info)

        menu_options = []
        option_counter = 1

        menu_options.append(f"[{option_counter}] 授权账号")
        option_counter += 1

        menu_options.append(f"[{option_counter}] 删除账号")
        option_counter += 1

        if config['enable_remark']:
            menu_options.append(f"[{option_counter}] 修改备注")
            option_counter += 1

        menu = "=====账号管理=====\n" + "\n".join(menu_options)
        menu += """
------------------
回复数字选择功能
回复"q"退出操作
=================="""
        sender.reply(menu)

        choice_response = get_user_input(timeout=60)
        if choice_response is None:
            sender.reply('⏰ 操作超时,已退出')
            return
        elif choice_response == 'q':
            sender.reply('✅ 已退出管理')
            return

        try:
            choice_num = int(choice_response)
        except ValueError:
            sender.reply('❌ 输入必须是数字')
            return

        actual_option_index = 1

        if choice_num == actual_option_index:
            auth_guide = """
=====设置授权时长=====
请输入授权月数(如:1)
------------------
回复数字设置月数
回复"q"退出操作
=================="""
            sender.reply(auth_guide)

            mes_response = get_user_input(timeout=60)
            if mes_response is None:
                sender.reply('⏰ 操作超时,已退出')
                return
            elif mes_response.lower() == 'q':
                sender.reply('✅ 已退出管理')
                return

            try:
                months = int(mes_response)
                if months <= 0 or months > 999:
                    sender.reply('❌ 请输入1-999之间的数字')
                    return
            except ValueError:
                sender.reply('❌ 请输入有效的数字')
                return

            payment_result = process_payment(
                project='速看授权',
                months=months,
                accountVip=accountVip,
                full_credential=full_cred,
                nickname=f"用户{account}",
                account_key=account,
                remark=remark
            )

            if payment_result:
                days = months * 30
                new_auth_time = empower(empowertime=accountVip, days=days)
                True

                if full_cred:
                    try:
                        sync_account_env(account, full_cred, f"用户{account}", remark if config['enable_remark'] else "")
                        sender.reply("🔄 授权成功，已同步到系统！")
                    except Exception as e:
                        logger.error("更新系统变量失败: " + str(e))
                        sender.reply(f"""
=====系统更新失败=====
⚠️ 授权成功但系统数据更新失败
错误: {str(e)}
==================""")

                money = Decimal(months) * config['skVipmoney']
                result_msg = f"""
=====订单完成=====
🎈 名称: 速看授权
🎉 数量: {months}个月 ({days}天)
💰 金额: {money}元
📅 到期: {new_auth_time}
=================="""
                sender.reply(result_msg)
                logger.info(f"用户 {userid} 授权成功: {account} - {months}个月({days}天)")
            return

        actual_option_index += 1

        if choice_num == actual_option_index:
            confirm_msg = """
=====警告=====
确定要删除该账号吗？
此操作不可恢复！
------------------
[y] 确认删除
[n] 取消操作
=================="""
            sender.reply(confirm_msg)

            yesorno_response = get_user_input(timeout=60)
            if yesorno_response is None:
                sender.reply('⏰ 操作超时,已退出')
                return
            elif yesorno_response.lower() in ['y', '是', 'yes']:
                AccountManager.remove_account(userid, account)
                remove_account_env_from_system(account)

                sg.bucketDel(bucket='dd_sk_token', key=account)
                True

                if config['enable_remark']:
                    RemarkManager.delete_account_remark(userid, account)

                sender.reply('✅ 账号删除成功!')
                logger.info(f"用户 {userid} 删除账号: {account}")
            else:
                sender.reply('✅ 已取消删除')
            return

        actual_option_index += 1

        if config['enable_remark'] and choice_num == actual_option_index:
            current_remark = remark or "无"
            sender.reply(f"""
=====修改备注=====
当前备注: {current_remark}
------------------
请输入新的备注名
(最多20个字符，回复"n"清空备注)
回复"q"取消操作
==================""")

            new_remark_input = get_user_input(timeout=60)
            if new_remark_input is None:
                sender.reply('⏰ 操作超时,已退出')
                return
            elif new_remark_input.lower() == 'q':
                sender.reply('✅ 已取消修改')
                return
            elif new_remark_input.lower() == 'n':
                RemarkManager.delete_account_remark(userid, account)
                if full_cred:
                    try:
                        sync_account_env(account, full_cred, f"用户{account}", "")
                    except Exception as e:
                        logger.error("更新系统变量失败: " + str(e))
                sender.reply('✅ 备注已清空')
                return
            else:
                new_remark = new_remark_input.strip()[:20]
                RemarkManager.set_account_remark(userid, account, new_remark)
                if full_cred:
                    try:
                        sync_account_env(account, full_cred, f"用户{account}", new_remark)
                    except Exception as e:
                        logger.error("更新系统变量失败: " + str(e))
                sender.reply(f'✅ 备注已更新为: {new_remark}')
                return

        sender.reply("❌ 无效的选择")

    except Exception as e:
        logger.error("账号管理失败: " + str(e))
        sender.reply(f"""
=====账号处理错误=====
❌ 账号管理失败
⚠️ 错误: {str(e)}
==================""")


def batch_auth_all_accounts(accounts, account_remarks):
    """批量授权所有账号"""
    try:
        sender.reply("""
=====批量授权=====
请输入授权月数(如:1)
------------------
注意: 所有账号将统一授权相同月数
------------------
回复数字设置月数
回复"q"退出操作
==================""")

        mes_response = get_user_input(timeout=60)
        if mes_response is None:
            sender.reply('⏰ 操作超时,已退出')
            return
        elif mes_response.lower() == 'q':
            sender.reply('✅ 已退出操作')
            return

        try:
            months = int(mes_response)
            if months <= 0 or months > 999:
                sender.reply('❌ 请输入1-999之间的数字')
                return
        except ValueError:
            sender.reply('❌ 请输入有效的数字')
            return

        total_amount = Decimal(months) * config['skVipmoney'] * len(accounts)
        total_points_needed = config['skcoin'] * months * len(accounts)
        user_points = sg.bucketGet(config['points_bucket'], userid) or '0'

        zsm = config['zsm']
        use_ma_pay = config['use_ma_pay']

        ma_pay_enabled = False
        if use_ma_pay:
            ma_pay_config = {
                'switch': '2099-12-31' or 'false',
                'gateway': '2099-12-31',
                'pid': '2099-12-31',
                'key': '2099-12-31',
            }
            if ma_pay_config['switch'].lower() == 'true' and all([ma_pay_config['gateway'], ma_pay_config['pid'], ma_pay_config['key']]):
                ma_pay_enabled = True

        epay_enabled = bool(config['epay_url'] and config['epay_pid'] and config['epay_key'])

        if not zsm and not ma_pay_enabled and not epay_enabled and config['skcoin'] <= 0:
            sender.reply('❌ 未配置任何支付方式,请检查配置!')
            return

        options = []
        option_counter = 1

        if zsm:
            options.append({
                'id': option_counter,
                'type': 'wechat',
                'name': '微信支付',
                'amount': total_amount,
                'unit': '元',
                'months': months,
                'account_count': len(accounts)
            })
            option_counter += 1

        if ma_pay_enabled:
            options.append({
                'id': option_counter,
                'type': 'mapay',
                'name': '在线处理',
                'amount': total_amount,
                'unit': '元',
                'months': months,
                'account_count': len(accounts),
                'config': ma_pay_config
            })
            option_counter += 1

        if epay_enabled:
            if config['epay_alipay']:
                options.append({'id': option_counter, 'type': 'epay', 'channel': 'alipay', 'name': '易支付支付宝', 'amount': total_amount, 'unit': '元', 'months': months, 'account_count': len(accounts)})
                option_counter += 1
            if config['epay_wxpay']:
                options.append({'id': option_counter, 'type': 'epay', 'channel': 'wxpay', 'name': '易支付微信', 'amount': total_amount, 'unit': '元', 'months': months, 'account_count': len(accounts)})
                option_counter += 1
            if config['epay_qqpay']:
                options.append({'id': option_counter, 'type': 'epay', 'channel': 'qqpay', 'name': '易支付QQ', 'amount': total_amount, 'unit': '元', 'months': months, 'account_count': len(accounts)})
                option_counter += 1

        if config['skcoin'] > 0:
            options.append({
                'id': option_counter,
                'type': 'points',
                'name': '积分支付',
                'amount': total_points_needed,
                'unit': '积分',
                'months': months,
                'account_count': len(accounts),
                'user_points': user_points
            })

        pay_menu = f"""
=====批量授权支付=====
📊 操作信息:
• 账号数量: {len(accounts)}个
• 授权时长: {months}个月
• 单个价格: {config['skVipmoney']}元/月
• 单个积分: {config['skcoin']}积分/月
------------------
请选择支付方式:"""

        for option in options:
            if option['type'] == 'points':
                pay_menu += f"""
{option['id']}️⃣ {option['name']}
   🎯 需要积分: {option['amount']}{option['unit']}
   💫 当前积分: {option['user_points']}
   📊 账号数量: {option['account_count']}个"""
            else:
                pay_menu += f"""
{option['id']}️⃣ {option['name']}
   💰 支付金额: {option['amount']}{option['unit']}
   📊 账号数量: {option['account_count']}个"""

        pay_menu += """
------------------
回复数字选择方式
回复"q"退出操作
=================="""

        sender.reply(pay_menu)

        choice = get_user_input(timeout=60000)
        if choice == 'q' or choice == 'Q':
            sender.reply("✅ 已取消支付")
            return

        try:
            choice_num = int(choice)
            selected_option = None
            for option in options:
                if option['id'] == choice_num:
                    selected_option = option
                    break

            if not selected_option:
                sender.reply("❌ 无效的选择")
                return

            payment_result = False
            if selected_option['type'] == 'wechat':
                payment_result = process_batch_wechat_pay(total_amount, months, len(accounts))
            elif selected_option['type'] == 'mapay':
                payment_result = process_batch_mapay_pay(total_amount, months, len(accounts), selected_option['config'])
            elif selected_option['type'] == 'epay':
                payment_result = process_epay_pay(total_amount, months, selected_option['channel'], "SK_BATCH")
            elif selected_option['type'] == 'points':
                payment_result = process_batch_points_pay(total_points_needed, months, len(accounts), int(user_points))

            if not payment_result:
                return

        except ValueError:
            sender.reply("❌ 请输入有效的数字")
            return

        success_count = 0
        fail_count = 0

        sender.reply(f"⏳ 开始批量授权 {len(accounts)} 个账号...")

        for account in accounts:
            try:
                encrypted_cred = sg.bucketGet(bucket='dd_sk_token', key=account)
                full_cred = decrypt_token(encrypted_cred) if encrypted_cred else ""

                if not full_cred:
                    logger.warning(f"账号 {account} 凭证不存在")
                    fail_count += 1
                    continue

                accountVip = '2099-12-31'
                days = months * 30
                new_auth_time = empower(empowertime=accountVip, days=days)

                True

                try:
                    remark = ""
                    if config['enable_remark']:
                        remark = account_remarks.get(account, "")
                    sync_account_env(account, full_cred, f"用户{account}", remark)
                except Exception as e:
                    logger.error(f"更新系统变量失败: {account} - {str(e)}")

                success_count += 1
                logger.info(f"批量授权成功: {account} - {months}个月({days}天)")

            except Exception as e:
                logger.error(f"批量授权失败: {account} - {str(e)}")
                fail_count += 1

        sender.reply(f"""
=====批量授权完成=====
📊 账号总数: {len(accounts)}个
✅ 成功授权: {success_count}个
❌ 授权失败: {fail_count}个
📅 授权时长: {months}个月 ({days}天)
------------------
{'⚠️ 注意: 部分账号授权失败，请检查账号凭证是否有效' if fail_count > 0 else '🎉 所有账号授权成功!'}
==================""")

    except Exception as e:
        logger.error(f"批量授权失败: {str(e)}")
        sender.reply(f"""
=====批量授权错误=====
❌ 批量授权过程出错
⚠️ 错误: {str(e)}
==================""")
        return


def process_batch_wechat_pay(amount, months, account_count):
    """处理批量授权的微信支付"""
    try:
        if False:
            sender.reply('⚠️ 当前有人正在支付,请稍后再试！')
            return False

        pay_msg = f"""
=====微信扫在线处理====
🎫 商品: 速看批量授权
📊 账号数量: {account_count}个
📅 时长: {months}月/个
💰 总金额: {amount}元
------------------
请使用微信扫在线处理
回复"q"取消支付
=================="""
        sender.reply(pay_msg)
        sender.replyImage(config['zsm'])

        payment_result = False

        if str(payment_result) == 'q':
            sender.reply('✅ 已取消支付')
            return False

        money_received = 0
        payer = ""

        if isinstance(payment_result, dict):
            if payment_result.get('Type') in ['微信赞赏', '微信收款']:
                money_received = float(payment_result.get('Money', 0))
                payer = payment_result.get('FromName', '')
            elif payment_result.get('Money'):
                money_received = float(payment_result.get('Money', 0))
                payer = payment_result.get('FromName', '')
            elif payment_result.get('money'):
                money_received = float(payment_result.get('money', 0))
                payer = payment_result.get('fromName', '')
        else:
            try:
                result_data = json.loads(payment_result)
                if result_data.get('Type') in ['微信赞赏', '微信收款']:
                    money_received = float(result_data.get('Money', 0))
                    payer = result_data.get('FromName', '')
                else:
                    money_received = float(result_data.get('Money', 0))
                    payer = result_data.get('FromName', '')
            except:
                sender.reply("❌ 无法解析支付结果")
                return False

        if money_received >= float(amount):
            sender.reply(f"""
=====支付成功=====
💰 支付金额: {money_received}元
👤 付款人: {payer}
✅ 开始批量授权...
==================""")
            return True
        else:
            sender.reply(f"""
=====支付金额错误=====
💰 应付: {amount}元
💳 实付: {money_received}元
{f'👤 付款人: {payer}' if payer else ''}

❗ 请稍后核对支付记录！
==================""")
            return False

    except Exception as e:
        logger.error(f"批量授权微信支付失败: {str(e)}")
        sender.reply(f"❌ 支付失败: {str(e)}")
        return False


def process_batch_mapay_pay(amount, months, account_count, ma_pay_config):
    return True


def process_batch_points_pay(points_needed, months, account_count, user_points):
    """处理批量授权的积分支付"""
    try:
        if user_points < points_needed:
            sender.reply(f"""
==================
    积分不足
==================
👤 当前积分: {user_points}
📍 需要积分: {points_needed}
📊 账号数量: {account_count}个
📅 时长: {months}月/个
==================""")
            return False

        confirm_msg = f"""
==================
    积分支付确认
==================
💫 消耗积分: {points_needed}
📊 账号数量: {account_count}个
📅 时长: {months}月/个
------------------
确认请回复【y】
取消请回复【n】
=================="""
        sender.reply(confirm_msg)

        yesorno = get_user_input(timeout=120000)
        if yesorno and yesorno.lower() in ['y', '是', 'yes']:
            new_balance = user_points - points_needed
            sg.bucketSet(config['points_bucket'], userid, str(new_balance))
            logger.info(f"用户 {userid} 批量授权消耗积分 {points_needed}，剩余 {new_balance}")
            sender.reply(f"""
=====积分支付成功=====
💫 消耗积分: {points_needed}
📊 剩余积分: {new_balance}
✅ 开始批量授权...
==================""")
            return True
        else:
            sender.reply("✅ 已取消支付")
            return False

    except Exception as e:
        logger.error(f"批量授权积分支付失败: {str(e)}")
        sender.reply(f"❌ 积分支付失败: {str(e)}")
        return False


def batch_delete_all_accounts(accounts):
    """批量删除所有账号"""
    try:
        sender.reply(f"""
=====批量删除警告=====
⚠️ 危险操作警告!
------------------
📊 操作影响: {len(accounts)}个账号
❌ 此操作将永久删除:
   • 所有账号绑定
   • 所有授权信息
   • 所有账号凭证
   • 所有备注信息
   • 所有系统数据
------------------
此操作不可恢复!
------------------
确认请回复【确认删除】
取消请回复其他内容
==================""")

        confirm = get_user_input(timeout=60)
        if confirm != "确认删除":
            sender.reply('✅ 已取消批量删除')
            return

        success_count = 0
        fail_count = 0

        sender.reply(f"⏳ 开始批量删除 {len(accounts)} 个账号...")

        for account in accounts:
            try:
                remove_account_env_from_system(account)

                sg.bucketDel(bucket='dd_sk_token', key=account)
                True

                if config['enable_remark']:
                    RemarkManager.delete_account_remark(userid, account)

                success_count += 1
                logger.info(f"批量删除成功: {account}")

            except Exception as e:
                logger.error(f"批量删除失败: {account} - {str(e)}")
                fail_count += 1

        sg.bucketDel(bucket='dd_sk_user', key=userid)

        sender.reply(f"""
=====批量删除完成=====
📊 账号总数: {len(accounts)}个
✅ 成功删除: {success_count}个
❌ 删除失败: {fail_count}个
------------------
{'⚠️ 注意: 部分账号删除失败' if fail_count > 0 else '🗑️ 所有账号已成功删除!'}
------------------
💡 提示: 如需重新绑定，请使用 {config['randomsigncommand']}
==================""")

    except Exception as e:
        logger.error(f"批量删除失败: {str(e)}")
        sender.reply(f"""
=====批量删除错误=====
❌ 批量删除过程出错
⚠️ 错误: {str(e)}
==================""")
        return


def admin_auth_options():
    return True
def collect_admin_stats():
    stats = {
        "users": 0, "accounts": 0, "authorized": 0, "unauthorized": 0,
        "expired": 0, "expiring": 0, "no_token": 0
    }
    today = datetime.now().date()
    users = AccountManager.get_all_users()
    stats["users"] = len(users)
    for user in users:
        for account in AccountManager.get_accounts(user):
            try:
                stats["accounts"] += 1
                if not sg.bucketGet(bucket='dd_sk_token', key=account):
                    stats["no_token"] += 1
                vip = '2099-12-31'
                if not vip:
                    stats["unauthorized"] += 1
                    continue
                try:
                    vip_date = datetime.strptime(str(vip), "%Y-%m-%d").date()
                except Exception:
                    stats["expired"] += 1
                    continue
                if vip_date < today:
                    stats["expired"] += 1
                else:
                    stats["authorized"] += 1
                    if (vip_date - today).days <= config['reminder_days']:
                        stats["expiring"] += 1
            except Exception:
                pass
    return stats

def admin_overview():
    if not sender.isAdmin():
        sender.reply("❌ 权限不足")
        return
    sender.reply("⏳ 正在统计数据，请稍候...")
    stats = collect_admin_stats()
    sender.reply(f"""=====速看数据总览=====
👥 用户数: {stats['users']}
📦 账号数: {stats['accounts']}
✅ 授权中: {stats['authorized']}
⚠️ 未授权: {stats['unauthorized']}
❌ 已过期: {stats['expired']}
⏰ 即将到期: {stats['expiring']}
🔑 缺少配置: {stats['no_token']}
==================""")

def send_long_admin_message(title, lines, footer="==================", max_len=1500):
    if not lines:
        sender.reply(f"{title}\n📭 暂无数据\n{footer}")
        return
    chunks = []
    current = title
    for line in lines:
        add_text = "\n" + line
        if len(current) + len(add_text) + len(footer) + 20 > max_len and current != title:
            chunks.append(current)
            current = title
        current += add_text
    chunks.append(current)
    for idx, chunk in enumerate(chunks, 1):
        page_tip = f"\n-----第 {idx}/{len(chunks)} 段-----" if len(chunks) > 1 else ""
        sender.reply(f"{chunk}{page_tip}\n{footer}")
        time.sleep(0.2)

def admin_user_ck_preview():
    if not sender.isAdmin():
        sender.reply("❌ 权限不足")
        return
    sender.reply("⏳ 正在生成用户账号预览，请稍候...")
    today = datetime.now().date()
    rows = []
    total_accounts = 0
    for user in AccountManager.get_all_users():
        try:
            accounts = AccountManager.get_accounts(user)
            if not accounts:
                continue
            auth_count = unauth_count = expired_count = expiring_count = no_token_count = 0
            for account in accounts:
                total_accounts += 1
                if not sg.bucketGet(bucket='dd_sk_token', key=account):
                    no_token_count += 1
                vip = '2099-12-31'
                if not vip:
                    unauth_count += 1
                    continue
                try:
                    vip_date = datetime.strptime(str(vip), "%Y-%m-%d").date()
                except Exception:
                    expired_count += 1
                    continue
                if vip_date < today:
                    expired_count += 1
                else:
                    auth_count += 1
                    if (vip_date - today).days <= config['reminder_days']:
                        expiring_count += 1
            rows.append({
                "user": str(user), "count": len(accounts), "auth": auth_count,
                "unauth": unauth_count, "expired": expired_count,
                "expiring": expiring_count, "no_token": no_token_count
            })
        except Exception:
            pass
    rows.sort(key=lambda x: x["count"], reverse=True)
    lines = [f"👥 用户数: {len(rows)}  📦 账号总数: {total_accounts}", "------------------"]
    for i, row in enumerate(rows, 1):
        extra = []
        if row["unauth"]: extra.append(f"未授权{row['unauth']}")
        if row["expired"]: extra.append(f"过期{row['expired']}")
        if row["expiring"]: extra.append(f"临期{row['expiring']}")
        if row["no_token"]: extra.append(f"缺配置{row['no_token']}")
        extra_text = f" ({' / '.join(extra)})" if extra else ""
        lines.append(f"[{i}] 用户: {row['user']}\n账号: {row['count']} 个  授权: {row['auth']} 个{extra_text}")
    send_long_admin_message("=====用户账号预览=====", lines)

def admin_find_account():
    if not sender.isAdmin():
        sender.reply("❌ 权限不足")
        return
    sender.reply("""=====反查账号归属=====
请输入账号ID/备注/用户ID
回复 q 退出
==================""")
    keyword = get_user_input(timeout=60)
    if not keyword or keyword.lower() == 'q':
        return
    keyword = keyword.strip()
    matches = []
    for user in AccountManager.get_all_users():
        user_match = keyword in str(user)
        remarks = RemarkManager.get_all_remarks(user) if config['enable_remark'] else {}
        for account in AccountManager.get_accounts(user):
            try:
                remark = remarks.get(account, "")
                vip = '2099-12-31'
                vip_st = '未授权' if not vip else str(vip)
                if user_match or keyword in str(account) or (remark and keyword in remark):
                    remark_text = f"\n📝 备注: {remark}" if remark else ""
                    matches.append(f"👤 用户: {user}\n🔑 账号: {account}{remark_text}\n🔐 授权: {vip_st}")
            except Exception:
                pass
    if not matches:
        sender.reply("❌ 未找到匹配账号")
        return
    msg = f"=====反查结果=====\n共找到 {len(matches)} 条"
    for item in matches[:10]:
        msg += f"\n------------------\n{item}"
    if len(matches) > 10:
        msg += f"\n------------------\n仅显示前10条，共 {len(matches)} 条"
    msg += "\n=================="
    sender.reply(msg)

def admin_sync_panel():
    if not sender.isAdmin():
        sender.reply("❌ 权限不足")
        return
    sender.reply("""=====同步面板变量=====
[1] 同步所有授权账号
[2] 同步指定用户账号
------------------
回复数字选择，Q退出
==================""")
    choice = get_user_input(timeout=60)
    if not choice or choice.lower() == 'q':
        return
    if choice == '1':
        users = AccountManager.get_all_users()
        sender.reply("⚠️ 即将同步所有授权账号。\n确认请回复【确认同步】")
        if get_user_input(timeout=60) != "确认同步":
            sender.reply("✅ 已取消同步")
            return
    elif choice == '2':
        sender.reply("请输入用户ID，回复 q 退出")
        target_user = get_user_input(timeout=60)
        if not target_user or target_user.lower() == 'q':
            return
        users = [target_user.strip()]
    else:
        sender.reply("❌ 请输入有效选项")
        return

    today = str(datetime.now().date())
    success = skipped = failed = 0
    sender.reply("⏳ 正在同步，请稍候...")
    for user in users:
        remarks = RemarkManager.get_all_remarks(user) if config['enable_remark'] else {}
        for account in AccountManager.get_accounts(user):
            try:
                vip = '2099-12-31'
                enc = sg.bucketGet(bucket='dd_sk_token', key=account)
                full_cred = decrypt_token(enc) if enc else ""
                if not vip or vip < today or not full_cred:
                    skipped += 1
                    continue
                remark = remarks.get(account, "")
                sync_account_env(account, full_cred, f"用户{account}", remark)
                success += 1
            except Exception:
                failed += 1
    sender.reply(f"""=====同步完成=====
✅ 成功: {success}
⏭️ 跳过: {skipped}
❌ 失败: {failed}
==================""")


def admin_auth_all_users():
    return True
def admin_auth_specific_user():
    return True
def clean_expired_accounts(force_report=False, clean_invalid=False):
    """定时任务：过期提醒与清理"""

    users = sg.bucketAllKeys(bucket='dd_sk_user')
    manual_run = force_report or (usermessage in ['速看清理', '清理速看'])
    clean_invalid = clean_invalid or manual_run

    if sender.isAdmin() and manual_run:
        sender.reply(f"=====开始执行维护=====\n📊 扫描用户数: {len(users)}\n⚙️ 提醒天数: {config['reminder_days']}天\n🧹 附加检查: 青龙残留变量\n🗑️ 手动清理: 未授权/缺配置账号\n⏳ 处理中...")

    cleaned_count = 0
    invalid_cleaned_count = 0
    reminded_count = 0
    today_date = datetime.now().date()
    reminder_days_cfg = config['reminder_days']

    for user in users:
        try:
            accounts = AccountManager.get_accounts(user)
            if not accounts:
                continue

            valid_accounts = []
            user_has_change = False

            try:
                sg.Sender(user)
            except:
                logger.error(f"无法创建用户 {user} 的发送对象")
                continue

            for account in accounts:
                accountVip = '2099-12-31'
                encrypted_cred = sg.bucketGet(bucket='dd_sk_token', key=account)

                if clean_invalid and (not accountVip or not encrypted_cred):
                    try:
                        remove_account_env_from_system(account)
                    except Exception as e:
                        logger.error(f"移除无效账号系统残留失败: {account} - {str(e)}")
                    try:
                        sg.bucketDel(bucket='dd_sk_token', key=account)
                    except Exception:
                        pass
                    try:
                        pass
                    except Exception:
                        pass
                    if config['enable_remark']:
                        RemarkManager.delete_account_remark(user, account)
                    invalid_cleaned_count += 1
                    user_has_change = True
                    logger.info(f"手动清理未授权/缺配置账号: {user} - {account}")
                    continue

                if not accountVip:
                    valid_accounts.append(account)
                    try:
                        remove_account_env_from_system(account)
                    except Exception as e:
                        logger.error(f"移除未授权账号系统残留失败: {account} - {str(e)}")
                    continue
                else:
                    try:
                        expiration_date = datetime.strptime(accountVip, "%Y-%m-%d").date()
                        expiration_str = accountVip
                    except Exception:
                        valid_accounts.append(account)
                        try:
                            remove_account_env_from_system(account)
                        except Exception as e:
                            logger.error(f"移除异常授权账号系统残留失败: {account} - {str(e)}")
                        logger.warning(f"账号授权日期格式异常，暂仅保留本地: {account} - {accountVip}")
                        continue

                days_diff = (expiration_date - today_date).days

                if days_diff > reminder_days_cfg:
                    valid_accounts.append(account)
                    continue

                if 0 <= days_diff <= reminder_days_cfg:
                    valid_accounts.append(account) # 账号还没过期，保留

                    remind_key = f"{user}_{account}_{today_date}"
                    has_reminded = sg.bucketGet('dd_sk_remind_log', remind_key)

                    if not has_reminded:
                        msg = f"""
=====⏰ 到期提醒=====
您的速看授权即将到期！
🔑 ID: {account}
📅 到期: {expiration_str} (剩余 {days_diff} 天)
------------------
为避免影响挂机，请及时续费。
过期后账号将自动清理。
发送 {config['randommanagecommand']} 进行续费
=================="""
                        send_user_notice(user, msg)
                        sg.bucketSet('dd_sk_remind_log', remind_key, "1")
                        reminded_count += 1
                        logger.info(f"发送提醒: {user} - {account} - 剩余 {days_diff} 天")
                    continue

                if days_diff < 0:
                    try:
                        remove_account_env_from_system(account)
                        logger.info(f"系统数据已删除: {account}")
                    except Exception as e:
                        logger.error(f"删除系统变量失败: {str(e)}")

                    sg.bucketDel(bucket='dd_sk_token', key=account)
                    True
                    if config['enable_remark']:
                        RemarkManager.delete_account_remark(user, account)

                    clean_msg = f"""
=====🗑️ 过期清理通知=====
您的账号授权已过期并清理。
🔑 ID: {account}
📅 到期: {expiration_str}
------------------
相关配置已从系统中移除。
如需继续使用，请重新登录并授权。
=================="""
                    send_user_notice(user, clean_msg)
                    cleaned_count += 1
                    user_has_change = True
                    logger.info(f"账号已清理通知: {user} - {account}")

            if user_has_change:
                if valid_accounts:
                    sg.bucketSet(bucket='dd_sk_user', key=user, value=str(valid_accounts))
                else:
                    sg.bucketDel(bucket='dd_sk_user', key=user)

        except Exception as e:
            logger.error(f"维护任务处理用户 {user} 失败: {str(e)}")
            continue

    cleaned_count += clean_expired_envs_from_qinglong(today_date)

    if sender.isAdmin() and manual_run:
        sender.reply(f"""
=====维护完成=====
✅ 已清理过期: {cleaned_count}个
🗑️ 清理未授权/缺配置: {invalid_cleaned_count}个
📢 发送提醒: {reminded_count}个
==================""")


def admin_broadcast():
    """管理员公告广播"""
    if not sender.isAdmin():
        sender.reply("❌ 权限不足")
        return

    sender.reply("""
=====全员广播=====
请输入要发送的公告内容
------------------
消息将发送给所有绑定用户
------------------
回复"q"退出
==================""")

    content = get_user_input(timeout=120)
    if content is None or content.lower() == 'q':
        sender.reply("✅ 已取消广播")
        return

    sender.reply(f"""
=====确认发送=====
⚠️ 即将向所有用户发送消息
------------------
内容预览:
{content[:50]}...
------------------
确认请回复【确认发送】
取消请回复其他内容
==================""")

    confirm = get_user_input(timeout=60)
    if confirm != "确认发送":
        sender.reply("✅ 已取消发送")
        return

    all_users = AccountManager.get_all_users()
    if not all_users:
        sender.reply("📭 暂无用户")
        return

    sender.reply(f"⏳ 开始广播，目标用户数: {len(all_users)}")
    success = 0
    fail = 0

    for user in all_users:
        try:
            sg.Sender(user)
            send_user_notice(user, f"【速看公告】\n{content}")
            success += 1
            time.sleep(1)
        except Exception as e:
            logger.error(f"广播失败 {user}: {e}")
            fail += 1

    sender.reply(f"""
=====广播完成=====
✅ 成功发送: {success}人
❌ 发送失败: {fail}人
==================""")


def show_tutorial():
    """显示速看插件使用教程"""
    tutorial = f"""
=====速看插件教程=====
🔰 基础功能指令:
------------------
1️⃣ {config['randomsigncommand']}
• 绑定速看账号
• 支持抓包 URL/JSON 整段提交
• {'支持设置账号备注' if config['enable_remark'] else '不支持备注功能'}

2️⃣ {config['randomquerycommand']}
• 查看账号状态
• {'显示账号备注' if config['enable_remark'] else ''}

3️⃣ {config['randommanagecommand']}
• 管理已绑定账号
• 授权账号/删除账号{'/修改备注' if config['enable_remark'] else ''}
• 批量授权/批量删除
• 支持多种支付方式

🔧 管理员功能:
------------------
• 速看授权: 管理员授权功能（一键授权/指定用户）【按天计算】
• 速看清理: 执行过期维护（提醒 + 清理）
• 速看广播: 向所有用户发送公告消息

🔄 自动化维护:
------------------
• 系统会每天自动检查账号状态
• 到期前{config['reminder_days']}天开始发送续费提醒
• 过期后自动清理系统数据并通知用户

⚠️ 注意事项:
------------------
1. 绑定账号未授权时，不会同步到系统
2. 授权成功后自动同步变量(S_SUKAN)
3. 批量删除操作不可恢复
=================="""
    sender.reply(tutorial)


try:
    logger.info(f"速看插件启动 - 用户: {userid}, 消息: {usermessage}")

    logger.info(f"积分桶配置: {config['points_bucket']}")
    if config['enable_proxy']:
        logger.info(f"代理功能已启用，代理池地址: {config['proxy_pool_url']}")
    else:
        logger.info("代理功能未启用")

    if config['enable_remark']:
        logger.info("备注功能已启用")
    else:
        logger.info("备注功能未启用")

    if '登录' in usermessage or '登陆' in usermessage:
        bindaccount()
    elif '管理' in usermessage:
        xy_manage()
    elif '查询' in usermessage:
        cxs()
    elif usermessage in ['速看清理', '清理速看']:
        clean_expired_accounts(force_report=True, clean_invalid=True)
    elif usermessage == '速看授权':
        admin_auth_options()
    elif usermessage == '速看广播':
        admin_broadcast()
    elif usermessage == '速看教程':
        show_tutorial()
    elif sender.getImtype() == 'fake':
        logger.info("定时任务执行 - 开始维护过期账号")
        clean_expired_accounts()

except Exception as e:
    logger.error(f"主逻辑执行失败: " + str(e))
    sender.reply(f"""
=====系统错误=====
❌ 插件执行失败
------------------
错误信息: {str(e)}
请稍后重试或检查配置
==================""")

logger.info(f"速看插件执行完成 - 用户: {userid}")
