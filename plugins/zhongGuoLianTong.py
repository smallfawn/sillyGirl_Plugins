# [title: 中国联通]
# [name: zhongGuoLianTong]
# [language: python]
# [class: 任务]
# [author: yuhualhh]
# [version: v1.1.0]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(联通)(登录|查询|管理|清理|检测)$]
# [icon: https://gcore.jsdelivr.net/gh/lhz03/img@7c2616699a9cf7a628d4a087eb458bb013913a85/2025/12/26/e1b072befcce7bbe3a55685176de670f.png]
# [description: ❷部分功能的实现需自行添加计划任务伪装管理员定时，了解如何添加计划任务请看移动云盘插件介绍，关于指令『联通检测』与『联通清理』定时『30 18 * * *』<img src="https://gcore.jsdelivr.net/gh/lhz03/img@1dab556e9d04a77d6b15802655355fd7be26fa9a/2026/01/21/2157c0cf735b321263a710cf978f43b0.png">]
# [depe: ["beautifulsoup4","cryptography","pycryptodome","requests"]]


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
    'yuhua_zglt_yuhua_zglt_qlname': form.string().title('对接容器').default('').description('各参数之间用中文符丨分割，例如: http://127.0.01:5700/丨abcdef-ghijk丨abcdefghijklmnopqrs_tuvw'),
    'yuhua_zglt_yuhua_zglt_osname': form.string().title('环境变量').default('').description('定义提交至容器的变量名称'),
    'yuhua_zglt_bingfa': form.string().title('查询并发').default('').description('不填默认5'),
    'yuhua_zglt_debug_pwd': form.string().title('调试模式').default('').description('非插件开发者无需理会'),
    'yuhua_zglt_yuedu': form.boolean().title('阅读红包').default(False).description('是否在联通查询中显示阅读红包详情，默认关闭'),
    'yuhua_zglt_lianchao': form.boolean().title('权超记录').default(False).description('是否在联通查询中显示权益超市中奖记录，默认关闭'),
})
_CONFIG_FIELD_MAP = {
    ('yuhua_zglt', 'yuhua_zglt_qlname'): 'yuhua_zglt_yuhua_zglt_qlname',
    ('yuhua_zglt', 'yuhua_zglt_osname'): 'yuhua_zglt_yuhua_zglt_osname',
    ('yuhua_zglt', 'bingfa'): 'yuhua_zglt_bingfa',
    ('yuhua_zglt', 'debug_pwd'): 'yuhua_zglt_debug_pwd',
    ('yuhua_zglt', 'yuedu'): 'yuhua_zglt_yuedu',
    ('yuhua_zglt', 'lianchao'): 'yuhua_zglt_lianchao',
}

import re
import time
from datetime import datetime, timedelta
import urllib.parse
from decimal import Decimal
import requests
import time
import json
import hashlib
import random
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from bs4 import BeautifulSoup
import threading
import os
import string
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

import sys
def printf(msg,level='INFO'):
    c=32 if level in['INFO','DEBUG']else 33 if level in['WARN','WARNING']else 31;sys.stderr.write(f"\033[{c}m[{level}] {str(msg)}\033[0m\n");sys.stderr.flush()


BASE_URL = "https://panservice.mail.wo.cn"
CHANNEL = "wohome"
ROOT_DIR_ID = "0"
IV = b'wNSOYIB1k1DjY5lA'
PRODUCT_ID = "91015539"

MACRO_MAX_RETRIES = 3
MICRO_MAX_RETRIES = 3
GLOBAL_TIMEOUT = 45

debug_key = sg.bucketGet('yuhua_zglt', 'debug_pwd') or ''
DEBUG = (debug_key == '123456789abcC@')
if DEBUG:
    printf("🔥🔥🔥 调试模式已开启，密钥验证通过 🔥🔥🔥", "WARN")

_ip_cache_pool =[]
_ip_cache_lock = threading.Lock()
_temp_ip_usage = {}
_temp_used_ips = set()
_proxy_lock = threading.Lock()
_session_pool = {}

def get_ip_limit():
    try: return int(sg.bucketGet('yuhua_zglt', 'ip') or '0')
    except: return 0

def extract_ip_from_proxy(proxy_url):
    try:
        if '://' in proxy_url: proxy_url = proxy_url.split('://', 1)[1]
        if '@' in proxy_url: proxy_url = proxy_url.split('@', 1)[1]
        return proxy_url.split(':')[0]
    except: return None

def clear_temp_ip_records():
    global _temp_ip_usage, _temp_used_ips, _proxy_lock
    with _proxy_lock: _temp_ip_usage.clear(); _temp_used_ips.clear()

def clear_session_pool():
    global _session_pool
    try:
        for session in _session_pool.values():
            try: session.close()
            except Exception: pass
        _session_pool.clear()
    except Exception: pass

def cleanup_resources(): clear_temp_ip_records(); clear_session_pool()

def get_proxies():
    return None

    global _temp_ip_usage, _temp_used_ips, _proxy_lock, _ip_cache_pool, _ip_cache_lock
    proxy_status = sg.bucketGet('yuhua_zglt', 'status') or '0'
    proxy_addr = sg.bucketGet('yuhua_zglt', 'proxy') or ''
    if proxy_status not in ['0', '1', '2'] or proxy_status == '0' or not proxy_addr.strip(): return None
    proxy_addr = proxy_addr.strip()
    if proxy_status == '1':
        if not (proxy_addr.startswith('http://') or proxy_addr.startswith('https://')): return None
        return {"http": proxy_addr, "https": proxy_addr}
    if proxy_status == '2':
        ip_limit = get_ip_limit()
        for _ in range(20):
            candidate_ip = None
            with _ip_cache_lock:
                if _ip_cache_pool: candidate_ip = _ip_cache_pool.pop(0)
            if not candidate_ip:
                with _ip_cache_lock:
                    if _ip_cache_pool: candidate_ip = _ip_cache_pool.pop(0)
                    else:
                        try:
                            r = requests.get(proxy_addr, timeout=5, proxies={"http": None, "https": None})
                            if r.status_code == 200:
                                ips = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+', r.text)
                                if ips: _ip_cache_pool.extend(ips); candidate_ip = _ip_cache_pool.pop(0)
                        except Exception: pass
            if candidate_ip:
                ip_val = candidate_ip.split(':')[0]
                should_skip = False
                with _proxy_lock:
                    if ip_val in _temp_used_ips:
                        should_skip = True
                    else:
                        if ip_limit > 0:
                            if _temp_ip_usage.get(ip_val, 0) >= ip_limit:
                                _temp_used_ips.add(ip_val); should_skip = True
                            else:
                                _temp_ip_usage[ip_val] = _temp_ip_usage.get(ip_val, 0) + 1
                if should_skip: continue
                return {"http": f"http://{candidate_ip}", "https": f"http://{candidate_ip}"}
            time.sleep(random.uniform(0.5, 1.0))
    return None

def _get_session_by_proxy(proxies):
    proxy_key = json.dumps(proxies, sort_keys=True) if proxies else "direct"
    if proxy_key not in _session_pool or getattr(_session_pool[proxy_key], "_closed", False):
        sess = requests.Session()
        sess.headers.update({
            'User-Agent': (
                'Mozilla/5.0 (Linux; Android 15; OPD2407 Build/UKQ1.231108.001; wv) '
                'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/142.0.7444.32 '
                'Safari/537.36/woapp LianTongYunPan/5.0.7 (Android 15)'
            )
        })
        if proxies: sess.proxies.update(proxies)
        _session_pool[proxy_key] = sess
    return _session_pool[proxy_key]

VERIFICATION_LOGIN_URL = "https://m.client.10010.com/mobileService/radomLogin.htm"
VERIFICATION_APP_ID = "06eccb0b7c2fd02bc1bb5e8a9ca2874175f50d8af589ecbd499a7c937a2fda7754dc135192b3745bd20073a687faee1755c67fab695164a090edd8e0da8771b83913890a44ec38e628cf2445bc476dfd"
VERIFICATION_KEY_VERSION = "1"
VERIFICATION_DEVICE_PARAMS = {
    "deviceOS": "android15",
    "netWay": "Wifi",
    "deviceCode": "12b46022d1f94f67973f6923d619ca1f",
    "version": "android@12.0500",
    "deviceId": "12b46022d1f94f67973f6923d619ca1f",
    "pip": "192.168.7.234",
    "simOperator": "1%2C--%2C--%2C--%2C--%401%2C--%2C--%2C--%2C--",
    "deviceModel": "OPD2407",
    "androidId": "108dea287b0317f4",
    "deviceBrand": "OnePlus",
    "uniqueIdentifier": "anda62d4d2b15888868200f59f61c27b1b29"
}

LOGIN_URL = "https://m.client.10010.com/mobileService/login.htm"
TICKET_URL = "https://m.client.10010.com/edop_ng/getTicketByNative"
ACCESS_TOKEN_URL = "https://panservice.mail.wo.cn/wohome/dispatcher"
CLOUD_DISK_APP_ID = "edop_unicom_d67b3e30"

LOGIN_APP_ID = "06eccb0b7c2fd02bc1bb5e8a9ca2874175f50d8af589ecbd499a7c937a2fda7754dc135192b3745bd20073a687faee1755c67fab695164a090edd8e0da8771b83913890a44ec38e628cf2445bc476dfd"
LOGIN_KEY_VERSION = "2"
LOGIN_VOIP_TOKEN = "citc-default-token-do-not-push"
LOGIN_IS_FIRST_INSTALL = "1"
LOGIN_IS_REMEMBER_PWD = "false"
LOGIN_SIM_COUNT = "1"
LOGIN_NET_WAY = "wifi"

PUBLIC_KEY_BASE64 = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDc+CZK9bBA9IU+gZUOc6FUGu7yO9WpTNB0PzmgFBh96Mg1WrovD1oqZ+eIF4LjvxKXGOdI79JRdve9NPhQo07+uqGQgE4imwNnRx7PFtCRryiIEcUoavuNtuRVoBAm6qdB0SrctgaqGfLgKvZHOnwTjyNqjBUxzMeQlEC2czEMSwIDAQAB"
DEFAULT_SPLIT = "#PART#"
MAX_BLOCK_SIZE = 117

WOREAD_KEY = b"woreadst^&*12345"
WOREAD_IV = b"16-Bytes--String"
WOREAD_PRODUCT_ID = "10000002"
WOREAD_SECRET = ""

def split_long_message(msg, max_length=4000):
    if len(msg) <= max_length: return [msg]
    parts = []; current_pos = 0
    while current_pos < len(msg):
        end_pos = current_pos + max_length
        if end_pos >= len(msg): parts.append(msg[current_pos:]); break
        split_pos = msg.rfind('\n', current_pos, end_pos)
        if split_pos == -1 or split_pos <= current_pos: split_pos = end_pos
        parts.append(msg[current_pos:split_pos]); current_pos = split_pos + (1 if split_pos < end_pos else 0)
    return parts

def safe_reply(sender, msg):
    parts = split_long_message(msg)
    for i, part in enumerate(parts):
        if i > 0: time.sleep(random.uniform(0.02, 0.05))
        sender.reply(part)

def load_rsa_public_key():
    """加载RSA公钥"""
    try:
        public_key_der = base64.b64decode(PUBLIC_KEY_BASE64)
        public_key = serialization.load_der_public_key(public_key_der)
        return public_key
    except Exception as e:
        if DEBUG:
            print(f"❌ RSA公钥加载失败: {e}")
        return None

def rsa_encrypt(plaintext, key):
    """RSA加密函数"""
    plaintext_bytes = plaintext.encode('utf-8')
    if len(plaintext_bytes) <= MAX_BLOCK_SIZE:
        return key.encrypt(plaintext_bytes, padding.PKCS1v15())
    encrypted_blocks = []
    for i in range(0, len(plaintext_bytes), MAX_BLOCK_SIZE):
        block = plaintext_bytes[i:i + MAX_BLOCK_SIZE]
        encrypted_block = key.encrypt(block, padding.PKCS1v15())
        if i > 0: encrypted_blocks.append(DEFAULT_SPLIT.encode('utf-8'))
        encrypted_blocks.append(encrypted_block)
    return b''.join(encrypted_blocks)

def mobile_encrypt(data, public_key):
    """手机号加密"""
    encrypted_bytes = rsa_encrypt(data, public_key)
    return base64.b64encode(encrypted_bytes).decode('utf-8').replace('\n', '')

def password_encrypt(password, public_key, random_str="000000"):
    """密码加密"""
    return mobile_encrypt(password + random_str, public_key)

def encrypt_for_api(data, public_key):
    """执行加密并进行Base64编码，用于API请求（验证码登录专用）"""
    plaintext_bytes = data.encode('utf-8')
    max_block_size = 117
    encrypted_blocks = []
    for i in range(0, len(plaintext_bytes), max_block_size):
        block = plaintext_bytes[i:i + max_block_size]
        encrypted_blocks.append(public_key.encrypt(block, padding.PKCS1v15()))
    encrypted_bytes = b''.join(encrypted_blocks)
    return base64.b64encode(encrypted_bytes).decode('utf-8')

def woread_encrypt(text):
    """AES-CBC-PKCS7 加密 (1:1 复刻 JS: JSON无空格 -> AES -> HexStr -> Base64)"""
    try:
        if isinstance(text, dict):
            text = json.dumps(text, separators=(',', ':'))

        cipher = AES.new(WOREAD_KEY, AES.MODE_CBC, WOREAD_IV)
        pad_text = pad(text.encode('utf-8'), AES.block_size)
        encrypted_bytes = cipher.encrypt(pad_text)

        hex_str = encrypted_bytes.hex()

        return base64.b64encode(hex_str.encode('utf-8')).decode('utf-8')
    except Exception as e:
        return ""

def _perform_login_and_get_token(phone, password):
    public_key = load_rsa_public_key()
    if not public_key: return None, None, None, "加密公钥加载失败"
    try:
        mobile_encrypted = mobile_encrypt(phone, public_key)
        password_encrypted = password_encrypt(password, public_key)
    except Exception: return None, None, None, "加密过程出错"
    device_id = hashlib.md5(phone.encode()).hexdigest()
    payload = {"voipToken": LOGIN_VOIP_TOKEN, "deviceBrand": "iPhone", "simOperator": "--,%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8,--,--,--", "deviceId": device_id, "netWay": LOGIN_NET_WAY, "deviceCode": device_id, "deviceOS": "15.8.3", "uniqueIdentifier": device_id, "version": "iphone_c@12.0200", "pip": "192.168.5.14", "isFirstInstall": LOGIN_IS_FIRST_INSTALL, "keyVersion": LOGIN_KEY_VERSION, "simCount": LOGIN_SIM_COUNT, "mobile": mobile_encrypted, "isRemberPwd": LOGIN_IS_REMEMBER_PWD, "appId": LOGIN_APP_ID, "reqtime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "deviceModel": "iPhone8,2", "password": password_encrypted}
    headers = {"Host": "m.client.10010.com", "Content-Type": "application/x-www-form-urlencoded", "Connection": "keep-alive", "Accept": "*/*", "User-Agent": "ChinaUnicom4.x/12.2 (com.chinaunicom.mobilebusiness; build:44; iOS 15.8.3) Alamofire/4.7.3 unicom{version:iphone_c@12.0200}", "Accept-Language": "zh-CN,zh-Hans;q=0.9"}

    with requests.Session() as sess:
        response = send_request_global('POST', LOGIN_URL, data=payload, headers=headers, session=sess)
        if not response: return None, None, None, "登录请求失败"
        try: data = response.json()
        except json.JSONDecodeError: return None, None, None, "登录响应解析失败"
        if data.get("code") not in ["0", "0000"]: return None, None, None, data.get('desc', '未知错误')
        token_online = data.get("token_online", "")
        cookie_string = "; ".join([f"{c.name}={c.value}" for c in response.cookies])

    return "dummy_token", cookie_string, token_online, None

def _perform_verification_code_login_and_get_token(phone, verification_code):
    public_key = load_rsa_public_key()
    if not public_key: return None, None, None, "加密公钥加载失败"
    try:
        mobile_encrypted = encrypt_for_api(phone, public_key)
        password_encrypted = encrypt_for_api(verification_code, public_key)
    except Exception as e: return None, None, None, f"加密过程出错: {e}"
    payload = {"isFirstInstall": "1", "yw_code": "", "loginStyle": "0", "isRemberPwd": "true", "provinceChanel": "general", "voice_code": "", "voiceoff_flag": "1", "timestamp": datetime.now().strftime('%Y%m%d%H%M%S'), "mobile": mobile_encrypted, "password": password_encrypted, "appId": VERIFICATION_APP_ID, "keyVersion": VERIFICATION_KEY_VERSION, **VERIFICATION_DEVICE_PARAMS}
    ua = (f"Dalvik/2.1.0 (Linux; U; Android {VERIFICATION_DEVICE_PARAMS.get('deviceOS', '15')}; " f"{VERIFICATION_DEVICE_PARAMS.get('deviceModel', 'OPD2407')} Build/UKQ1.231108.001);" f"unicom{{version:{VERIFICATION_DEVICE_PARAMS.get('version', 'android@12.0500')}}};ltst;")
    headers = {"User-Agent": ua, "Content-Type": "application/x-www-form-urlencoded", "Connection": "keep-alive", "Accept": "*/*"}

    with requests.Session() as sess:
        response = send_request_global('POST', VERIFICATION_LOGIN_URL, data=payload, headers=headers, session=sess)
        if not response: return None, None, None, "登录请求失败，网络或服务器无响应"
        try: data = response.json()
        except json.JSONDecodeError: return None, None, None, f"登录响应解析失败: {response.text[:200]}"
        if data.get("code") != "0": return None, None, None, data.get('desc', '登录失败，未知错误')
        token_online = data.get("token_online", "")
        cookie_string = "; ".join([f"{c.name}={c.value}" for c in response.cookies])

    return "dummy_token", cookie_string, token_online, None

def token_online_login():
    """
    【token_online登录功能】
    参考联通云盘插件的风格，通过 token_online 换取凭证
    """
    guide = """
=====账号登录=====
❶ 通过抓包工具获取中国联通的token_online
❷ 按如下格式发送
『token_online#手机号』例: 66666666-1f66-4bde-66666-aaaaaaaaaaaa#18888888888
------------------
回复"q"退出"""
    sender.reply(guide)
    user_input = sender.input(60000, 1, False)

    if not user_input:
        sender.reply("❌ 输入超时")
        return
    elif user_input.lower() == 'q':
        sender.reply("✅ 已退出操作")
        return

    parts = user_input.split('#')
    token_online = parts[0].strip()
    phone = parts[1].strip() if len(parts) > 1 else ""

    if not token_online or not re.match(r'^\d{11}$', phone):
        sender.reply("❌ 格式错误，请确保格式为: token_online#11位手机号")
        return

    sender.reply("正在验证凭证有效性...")

    try:
        pl = {
            "token_online": token_online,
            "reqtime": int(time.time()*1000),
            "isFirstInstall": "1",
            "provinceChanel": "general",
            **VERIFICATION_DEVICE_PARAMS
        }

        ua = f"Dalvik/2.1.0 (Linux; U; Android {VERIFICATION_DEVICE_PARAMS.get('deviceOS')}; {VERIFICATION_DEVICE_PARAMS.get('deviceModel')} Build/UKQ1.231108.001);unicom{{version:{VERIFICATION_DEVICE_PARAMS.get('version')}}};ltst;"
        hd = {
            "User-Agent": ua,
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "m.client.10010.com"
        }

        with requests.Session() as sess:
            resp = send_request_global('POST', "https://m.client.10010.com/mobileService/onLine.htm", data=pl, headers=hd, session=sess)

        if not resp:
            sender.reply("❌ 登录失败: 网络请求无响应")
            return

        try:
            rj = resp.json()
        except json.JSONDecodeError:
            sender.reply("❌ 登录失败: 响应解析错误")
            return

        if rj.get('code') not in ['0', '0000']:
            fail_reason = rj.get('dsc') or rj.get('desc') or '凭证已失效'
            sender.reply(f"❌ 登录失败: {fail_reason}")
            return

        cookie_string = "; ".join([f"{c.name}={c.value}" for c in resp.cookies])
        if not cookie_string:
            sender.reply("❌ 登录失败: 未获取到Cookie")
            return

        ltp_check = LTP(ecs_token=cookie_string)
        ok, msg = ltp_check.check_validity()
        ltp_check.close()

        if not ok:
            sender.reply(f"❌ 登录失败: Cookie验证失败，{msg}")
            return

        access_token = "dummy_token"

        accounts = _sg_literal(uservalue or '[]')
        matched_uid = None
        for uid in accounts:
            old_phone = sg.bucketGet('yuhua_zglt_phone', uid) or "未知"
            if old_phone == phone:
                matched_uid = uid
                break

        final_uid = matched_uid if matched_uid else gen_unique_id()

        existing_appid = sg.bucketGet('yuhua_zglt_appid', final_uid)
        if not existing_appid:
            sender.reply("""=====添加AppId=====
❶ 该步骤非强制性，可选择取消
❷ 打开该路径中的文件『/storage/emulated/0/Documents/Unicom/appid』复制文本内容并回复
-----------------
请在300秒内完成
回复"q"取消""")
            app_input = sender.input(300000, 1, False)
            if not app_input:
                sender.reply("❌ 输入超时")
            elif app_input.lower() == 'q':
                sender.reply("✅ 已取消操作")
            else:
                new_appid = app_input.strip()
                pl["appId"] = new_appid
                with requests.Session() as sess:
                    test_resp = send_request_global('POST', "https://m.client.10010.com/mobileService/onLine.htm", data=pl, headers=hd, session=sess)
                if test_resp:
                    rj_test = test_resp.json()
                    if rj_test.get('code') in ['0', '0000']:
                        sg.bucketSet('yuhua_zglt_appid', final_uid, new_appid)
                        sender.reply("✅ 已成功添加")
                    else:
                        fail_reason = rj_test.get('dsc') or rj_test.get('desc') or '未知原因'
                        sender.reply(f"❌ 鉴权失败: {fail_reason}")
                else:
                    sender.reply("❌ 鉴权失败: 网络请求无响应")

        if matched_uid:
            sg.bucketSet('yuhua_zglt_token', matched_uid, access_token)
            sg.bucketSet('yuhua_zglt_ecs_token', matched_uid, cookie_string)
            sg.bucketSet('yuhua_zglt_token_online', matched_uid, token_online)
            try:
                sg.bucketDel('yuhua_zglt_password', matched_uid)
            except Exception:
                pass

            phone_mask = phone[:3] + "****" + phone[-4:]
            sender.reply(f"""
=====登录成功=====
🤪 账号: {phone_mask}
✅ 状态: 更新成功
------------------
发送"{manage_cmd}"管理账号
发送"{query_cmd}"查询账号""")
        else:
            accounts.append(final_uid)
            sg.bucketSet('yuhua_zglt_user', userid, str(accounts))
            sg.bucketSet('yuhua_zglt_token', final_uid, access_token)
            sg.bucketSet('yuhua_zglt_phone', final_uid, phone)
            sg.bucketSet('yuhua_zglt_ecs_token', final_uid, cookie_string)
            sg.bucketSet('yuhua_zglt_token_online', final_uid, token_online)

            phone_mask = phone[:3] + "****" + phone[-4:]
            sender.reply(f"""
=====登录成功=====
🤪 账号: {phone_mask}
✅ 状态: 添加成功
------------------
发送"{manage_cmd}"管理账号
发送"{query_cmd}"查询账号""")

        accountVip = '2099-12-31'
        if accountVip and accountVip >= today_time:
            try:
                sync_appid = sg.bucketGet('yuhua_zglt_appid', final_uid)
                sync_val = f"{token_online}#{sync_appid}" if sync_appid else token_online
                Addenvs(osname=yuhua_zglt_osname, value=sync_val, account=final_uid, phone=phone, owner_id=userid)

                if aiting_var and aiting_var != '0':
                    Addenvs(osname=aiting_var, value=phone, account=final_uid, phone=phone, owner_id=userid)
            except Exception as e:
                if DEBUG: print(f"青龙同步失败: {e}")

    except Exception as e:
        sender.reply(f"❌ 登录失败: {str(e)}")


def verification_code_login():
    """
    【API短信登录功能】：
    引导用户输入手机号和验证码，通过API直接登录。
    """
    sender.reply(f"""
=====短信登录=====
请输入中国联通手机号
------------------
请在60秒内完成
回复"q"退出""")
    phone = sender.input(60000, 1, False)
    if not phone:
        sender.reply("❌ 输入超时")
        return
    phone = phone.strip()
    if phone.lower() == 'q':
        sender.reply("✅ 已退出操作")
        return
    if not re.match(r'^\d{11}$', phone):
        sender.reply("❌ 请输入正确的11位手机号")
        return

    masked_phone = phone[:3] + "****" + phone[-4:]
    sender.reply(f"""=====短信登录=====
❶打开『中国联通App』使用手机号{masked_phone}获取登录验证码
❷ 回复收到的6位数字验证码
------------------
请在120秒内完成
回复"q"取消""")
    code = sender.input(120000, 1, False)
    if not code:
        sender.reply("❌ 输入超时")
        return
    code = code.strip()
    if code.lower() == 'q':
        sender.reply("✅ 已退出操作")
        return
    sender.reply("正在通过API登录，请稍候...")
    access_token, cookie_string, token_online, error_message = _perform_verification_code_login_and_get_token(phone, code)
    if not cookie_string:
        sender.reply(f"❌ 登录失败: {error_message}")
        return
    ltp_check = LTP(ecs_token=cookie_string, phone=phone)
    ok, msg = ltp_check.check_validity()
    ltp_check.close()

    if not ok:
        sender.reply(f"❌ 凭证校验失败: {msg}")
        return

    accounts = _sg_literal(uservalue or '[]')
    matched_uid = None
    for uid in accounts:
        if (sg.bucketGet('yuhua_zglt_phone', uid) or "未知") == phone:
            matched_uid = uid
            break

    final_uid = matched_uid if matched_uid else gen_unique_id()

    existing_appid = sg.bucketGet('yuhua_zglt_appid', final_uid)
    if not existing_appid:
        sender.reply("""=====添加AppId=====
❶ 该步骤非强制性，可选择取消
❷ 打开该路径中的文件『/storage/emulated/0/Documents/Unicom/appid』复制文本内容并回复
-----------------
请在300秒内完成
回复"q"取消""")
        app_input = sender.input(300000, 1, False)
        if not app_input:
            sender.reply("❌ 输入超时")
        elif app_input.lower() == 'q':
            sender.reply("✅ 已取消操作")
        else:
            new_appid = app_input.strip()
            pl_test = {"token_online": token_online, "appId": new_appid, "reqtime": int(time.time()*1000), **VERIFICATION_DEVICE_PARAMS}
            ua_test = f"Dalvik/2.1.0 (Linux; U; Android {VERIFICATION_DEVICE_PARAMS.get('deviceOS')}; {VERIFICATION_DEVICE_PARAMS.get('deviceModel')} Build/UKQ1.231108.001);unicom{{version:{VERIFICATION_DEVICE_PARAMS.get('version')}}};ltst;"
            hd_test = {"User-Agent": ua_test, "Content-Type": "application/x-www-form-urlencoded", "Host": "m.client.10010.com"}
            with requests.Session() as sess:
                test_resp = send_request_global('POST', "https://m.client.10010.com/mobileService/onLine.htm", data=pl_test, headers=hd_test, session=sess)
            if test_resp:
                rj_test = test_resp.json()
                if rj_test.get('code') in ['0', '0000']:
                    sg.bucketSet('yuhua_zglt_appid', final_uid, new_appid)
                    sender.reply("✅ 已成功添加")
                else:
                    fail_reason = rj_test.get('dsc') or rj_test.get('desc') or '未知原因'
                    sender.reply(f"❌ 鉴权失败: {fail_reason}")
            else:
                sender.reply("❌ 鉴权失败: 网络请求无响应")

    if matched_uid:
        sg.bucketSet('yuhua_zglt_token', matched_uid, access_token)
        sg.bucketSet('yuhua_zglt_ecs_token', matched_uid, cookie_string)
        if token_online: sg.bucketSet('yuhua_zglt_token_online', matched_uid, token_online)
        try:
            sg.bucketDel('yuhua_zglt_password', matched_uid)
        except Exception:
            pass
        sender.reply(f"=====登录成功=====\n🤪 账号: {_mask_identifier(phone)}\n✅ 状态: 更新成功\n------------------\n发送\"{manage_cmd}\"管理账号\n发送\"{query_cmd}\"查询账号")
    else:
        accounts.append(final_uid)
        sg.bucketSet('yuhua_zglt_user', userid, str(accounts))
        sg.bucketSet('yuhua_zglt_token', final_uid, access_token)
        sg.bucketSet('yuhua_zglt_phone', final_uid, phone)
        sg.bucketSet('yuhua_zglt_ecs_token', final_uid, cookie_string)
        if token_online: sg.bucketSet('yuhua_zglt_token_online', final_uid, token_online)
        sender.reply(f"=====登录成功=====\n🤪 账号: {_mask_identifier(phone)}\n✅ 状态: 添加成功\n------------------\n发送\"{manage_cmd}\"管理账号\n发送\"{query_cmd}\"查询账号")

    accountVip = '2099-12-31'
    if accountVip and accountVip >= today_time:
        try:
            sync_online = token_online if token_online else sg.bucketGet('yuhua_zglt_token_online', final_uid)
            sync_appid = sg.bucketGet('yuhua_zglt_appid', final_uid)
            if sync_online:
                sync_val = f"{sync_online}#{sync_appid}" if sync_appid else sync_online
                Addenvs(osname=yuhua_zglt_osname, value=sync_val, account=final_uid, phone=phone, owner_id=userid)

                if aiting_var and aiting_var != '0':
                    Addenvs(osname=aiting_var, value=phone, account=final_uid, phone=phone, owner_id=userid)
        except Exception as e:
            sender.reply(f"""
=====青龙更新失败=====
❌ 更新青龙变量失败
⚠️ 错误: {str(e)}
==================""")

def _try_auto_relogin(account_id):
    """精简版智能续期：仅刷新 ecs_token 或走账密兜底，彻底废除云盘流程"""
    token_online = sg.bucketGet('yuhua_zglt_token_online', account_id)
    appid = sg.bucketGet('yuhua_zglt_appid', account_id)
    if token_online:
        try:
            pl = {"token_online": token_online, "reqtime": int(time.time()*1000), "isFirstInstall": "1", "provinceChanel": "general", **VERIFICATION_DEVICE_PARAMS}
            if appid: pl["appId"] = appid
            ua = f"Dalvik/2.1.0 (Linux; U; Android {VERIFICATION_DEVICE_PARAMS.get('deviceOS')}; {VERIFICATION_DEVICE_PARAMS.get('deviceModel')} Build/UKQ1.231108.001);unicom{{version:{VERIFICATION_DEVICE_PARAMS.get('version')}}};ltst;"
            hd = {"User-Agent": ua, "Content-Type": "application/x-www-form-urlencoded", "Host": "m.client.10010.com"}
            resp = send_request_global('POST', "https://m.client.10010.com/mobileService/onLine.htm", data=pl, headers=hd)
            if resp:
                rj = resp.json()
                if rj.get('code') in ['0', '0000']:
                    cks = "; ".join([f"{c.name}={c.value}" for c in resp.cookies])
                    if cks:
                        sg.bucketSet('yuhua_zglt_ecs_token', account_id, cks)
                        sg.bucketSet('yuhua_zglt_token', account_id, "dummy_token") # 兼容旧本地结构占位
                        return True
        except: pass

    ph = sg.bucketGet('yuhua_zglt_phone', account_id)
    pw = sg.bucketGet('yuhua_zglt_password', account_id)
    if ph and pw:
        at, ck, to, err = _perform_login_and_get_token(ph, pw)
        if ck:
            sg.bucketSet('yuhua_zglt_token', account_id, "dummy_token")
            sg.bucketSet('yuhua_zglt_ecs_token', account_id, ck)
            if to:
                sg.bucketSet('yuhua_zglt_token_online', account_id, to)
                try:
                    auth_time = '2099-12-31'
                    if auth_time and auth_time >= str(datetime.now().date()):
                        real_owner = userid
                        try:
                            all_users = sg.bucketAllKeys('yuhua_zglt_user')
                            for u in all_users:
                                user_accs = _sg_literal(sg.bucketGet('yuhua_zglt_user', u) or '[]')
                                if account_id in user_accs:
                                    real_owner = u
                                    break
                        except: pass
                        sync_appid = sg.bucketGet('yuhua_zglt_appid', account_id)
                        sync_val = f"{to}#{sync_appid}" if sync_appid else to
                        Addenvs(osname=yuhua_zglt_osname, value=sync_val, account=account_id, phone=ph, owner_id=real_owner)
                except Exception as e:
                    if DEBUG: print(f"自动刷新同步青龙失败: {e}")
            return True
    return False

def account_password_login():
    """
    【账号密码登录功能】：
    使用账号密码直接登录联通云盘
    """
    sender.reply("请输入手机号:")
    phone = sender.input(30000, 1, False)
    if not phone:
        sender.reply("❌ 输入超时")
        return
    phone = phone.strip()
    if phone.lower() == 'q':
        sender.reply("✅ 已退出操作")
        return
    if not re.match(r'^\d{11}$', phone):
        sender.reply("❌ 请输入正确的11位手机号")
        return
    sender.reply("请输入密码:")
    password = sender.input(30000, 1, False)
    if not password:
        sender.reply("❌ 输入超时")
        return
    password = password.strip()
    if password.lower() == 'q':
        sender.reply("✅ 已退出操作")
        return
    sender.reply("正在登录中，请稍候...")
    access_token, cookie_string, token_online, error_message = _perform_login_and_get_token(phone, password)
    if not access_token:
        sender.reply(f"❌ 登录失败: {error_message}")
        return
    ltp_check = LTP(access_token, phone=phone)
    ok, msg = ltp_check.get_ticket()
    ltp_check.close()
    if not ok:
        sender.reply(f"❌ 凭证校验失败: {msg}")
        return
    accounts = _sg_literal(uservalue or '[]')
    matched_uid = None
    for uid in accounts:
        old_phone = sg.bucketGet('yuhua_zglt_phone', uid) or "未知"
        if old_phone == phone:
            matched_uid = uid
            break

    final_uid = matched_uid if matched_uid else gen_unique_id()

    existing_appid = sg.bucketGet('yuhua_zglt_appid', final_uid)
    if not existing_appid:
        sender.reply("""=====添加AppId=====
❶ 该步骤非强制性，可选择取消
❷ 打开该路径中的文件『/storage/emulated/0/Documents/Unicom/appid』复制文本内容并回复
-----------------
请在300秒内完成
回复"q"取消""")
        app_input = sender.input(300000, 1, False)
        if not app_input:
            sender.reply("❌ 输入超时")
        elif app_input.lower() == 'q':
            sender.reply("✅ 已取消操作")
        else:
            new_appid = app_input.strip()
            if token_online:
                pl_test = {"token_online": token_online, "appId": new_appid, "reqtime": int(time.time()*1000), **VERIFICATION_DEVICE_PARAMS}
                ua_test = f"Dalvik/2.1.0 (Linux; U; Android {VERIFICATION_DEVICE_PARAMS.get('deviceOS')}; {VERIFICATION_DEVICE_PARAMS.get('deviceModel')} Build/UKQ1.231108.001);unicom{{version:{VERIFICATION_DEVICE_PARAMS.get('version')}}};ltst;"
                hd_test = {"User-Agent": ua_test, "Content-Type": "application/x-www-form-urlencoded", "Host": "m.client.10010.com"}
                with requests.Session() as sess:
                    test_resp = send_request_global('POST', "https://m.client.10010.com/mobileService/onLine.htm", data=pl_test, headers=hd_test, session=sess)
                if test_resp:
                    rj_test = test_resp.json()
                    if rj_test.get('code') in['0', '0000']:
                        sg.bucketSet('yuhua_zglt_appid', final_uid, new_appid)
                        sender.reply("✅ 已成功添加")
                    else:
                        fail_reason = rj_test.get('dsc') or rj_test.get('desc') or '未知原因'
                        sender.reply(f"❌ 鉴权失败: {fail_reason}")
                else:
                    sender.reply("❌ 鉴权失败: 网络请求无响应")

    if matched_uid:
        sg.bucketSet('yuhua_zglt_token', matched_uid, access_token)
        sg.bucketSet('yuhua_zglt_password', matched_uid, password)
        sg.bucketSet('yuhua_zglt_ecs_token', matched_uid, cookie_string)
        if token_online: sg.bucketSet('yuhua_zglt_token_online', matched_uid, token_online)
        phone_mask = phone[:3] + "****" + phone[-4:]
        sender.reply(f"""
=====登录成功=====
🤪 账号: {phone_mask}
✅ 状态: 更新成功
------------------
发送"{manage_cmd}"管理账号
发送"{query_cmd}"查询账号""")
    else:
        accounts.append(final_uid)
        sg.bucketSet('yuhua_zglt_user', userid, str(accounts))
        sg.bucketSet('yuhua_zglt_token', final_uid, access_token)
        sg.bucketSet('yuhua_zglt_phone', final_uid, phone)
        sg.bucketSet('yuhua_zglt_password', final_uid, password)
        sg.bucketSet('yuhua_zglt_ecs_token', final_uid, cookie_string)
        if token_online: sg.bucketSet('yuhua_zglt_token_online', final_uid, token_online)
        phone_mask = phone[:3] + "****" + phone[-4:]
        sender.reply(f"""
=====登录成功=====
🤪 账号: {phone_mask}
✅ 状态: 添加成功
------------------
发送"{manage_cmd}"管理账号
发送"{query_cmd}"查询账号""")

    accountVip = '2099-12-31'
    if accountVip and accountVip >= today_time:
        try:
            sync_online = token_online if token_online else sg.bucketGet('yuhua_zglt_token_online', final_uid)
            sync_appid = sg.bucketGet('yuhua_zglt_appid', final_uid)
            if sync_online:
                sync_val = f"{sync_online}#{sync_appid}" if sync_appid else sync_online
                Addenvs(osname=yuhua_zglt_osname, value=sync_val, account=final_uid, phone=phone, owner_id=userid)

                if aiting_var and aiting_var != '0':
                    Addenvs(osname=aiting_var, value=phone, account=final_uid, phone=phone, owner_id=userid)
        except Exception as e:
            sender.reply(f"""
=====青龙更新失败=====
❌ 更新青龙变量失败
⚠️ 错误: {str(e)}
==================""")


def get_global_session():
    return _get_session_by_proxy(None)

def send_request_global(method, url, **kwargs):
    global _temp_used_ips, _proxy_lock
    passed_session = kwargs.pop('session', None)

    current_proxies = None

    consecutive_403_count = 0

    kwargs.setdefault('timeout', (10, 15))

    if DEBUG:
        printf(f"\n===== [REQUEST START] =====", "DEBUG")
        printf(f"METHOD: {method} | URL: {url}", "DEBUG")
        printf(f"HEADERS: {json.dumps(kwargs.get('headers', {}), ensure_ascii=False)}", "DEBUG")
        if kwargs.get('json'):
            printf(f"BODY(JSON): {json.dumps(kwargs.get('json'), indent=2, ensure_ascii=False)}", "DEBUG")
        elif kwargs.get('data'):
            data_str = str(kwargs.get('data'))
            if len(data_str) > 500: data_str = data_str[:200] + "...(truncated)..."
            printf(f"BODY(DATA): {data_str}", "DEBUG")

    for attempt in range(3):
        try:
            session = passed_session if passed_session else _get_session_by_proxy(current_proxies)
            kwargs["proxies"] = current_proxies
            response = session.request(method, url, **kwargs)

            if DEBUG:
                printf(f"-----[RESPONSE - Attempt {attempt+1}] -----", "DEBUG")
                printf(f"STATUS: {response.status_code}", "DEBUG")
                try:
                    printf(f"RSP HEADERS: {json.dumps(dict(response.headers), ensure_ascii=False)}", "DEBUG")
                    rsp_text = response.text
                    if len(rsp_text) < 1000: printf(f"RSP BODY: {rsp_text}", "DEBUG")
                    else: printf(f"RSP BODY: {rsp_text[:500]}...(truncated)", "DEBUG")
                except: pass
                printf(f"=====[REQUEST END] =====\n", "DEBUG")

            if response.status_code == 403:

                consecutive_403_count += 1
                if attempt < 2:
                    time.sleep(random.uniform(0.01, 0.05))
                    continue
                else: raise requests.exceptions.RequestException("IP已被风控")
            else: consecutive_403_count = 0

            response.raise_for_status()
            return response

        except Exception as e:
            if DEBUG:
                printf(f"⚠️ Attempt {attempt + 1} FAILED (Error): {e}", "WARN")

            if "代理获取失败" in str(e) or "已拦截" in str(e): raise e

            if attempt == 2:
                error_msg = str(e).lower()
                if "ip已被风控" in error_msg or (consecutive_403_count >= 2 and "403" in error_msg): raise requests.exceptions.RequestException("IP已被风控")
                elif "403" in error_msg: raise requests.exceptions.RequestException("IP已被风控")
                raise e
            else:
                time.sleep(random.uniform(0.01, 0.05) * (attempt + 1))

    return None


class LTP:
    def __init__(self, cookie_str=None, phone='未知', session=None, ecs_token=None, token_online=None):
        self.session = session or requests.Session()
        self.ecs_token = ecs_token
        self.token_online = token_online
        self.phone = phone
        self.ua = (
            'Mozilla/5.0 (Linux; Android 15; OPD2407 Build/UKQ1.231108.001; wv) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/142.0.7444.32 '
            'Safari/537.36/woapp LianTongYunPan/5.0.7 (Android 15)'
        )
        self.session.headers.update({'User-Agent': self.ua})
        self.proxies = get_proxies()

    def check_validity(self):
        """修复版：严格区分代理网络异常与真实CK失效"""
        if not self.ecs_token: return False, "缺少基础Cookie(ecs_token)"
        try:
            url = "https://act.10010.com/SigninApp/convert/getTelephone"
            headers = {
                "Cookie": self.ecs_token,
                "User-Agent": self.ua,
                "Accept": "application/json, text/plain, */*",
                "Content-Type": "application/json"
            }
            res = self._send_request('POST', url, headers=headers, json={})

            if res is None:
                return False, "代理IP不可用或网络请求超时"

            data = res.json()
            if data.get('status') == '0000':
                return True, "凭证有效"
            else:
                return False, "CK已失效"
        except:
            pass
        return False, "接口响应异常"


    def _send_request(self, method, url, **kwargs):
        if 'session' not in kwargs:
            kwargs['session'] = self.session

        if self.proxies and sg.bucketGet('yuhua_zglt', 'status') == '2':
            ip_val = extract_ip_from_proxy(self.proxies.get("http", ""))
            if ip_val:
                is_banned = False
                with _proxy_lock:
                    is_banned = ip_val in _temp_used_ips
                if is_banned:
                    self.proxies = get_proxies()
                    if self.session:
                        try:
                            self.session.close()
                        except Exception:
                            pass
                    self.session = requests.Session()
                    self.session.headers.update({'User-Agent': self.ua})
                    kwargs['session'] = self.session

        if 'proxies' not in kwargs:
            kwargs['proxies'] = self.proxies

        try:
            return send_request_global(method, url, **kwargs)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.RequestException):
            return None

    def _get_signin_redpacket(self):
        """查询签到话费红包 (返回: 总额, 即将过期金额, 过期月份)"""
        for _ in range(1):
            try:
                url = "https://act.10010.com/SigninApp/convert/getTelephone"
                headers = {"Cookie": self.ecs_token} if self.ecs_token else {}
                res = self._send_request('POST', url, headers=headers, json={})
                if res:
                    data = res.json()
                    if data.get('status') == '0000':
                        d = data.get('data', {})
                        return d.get('telephone', '0.00'), d.get('needexpNumber', '0'), str(d.get('month', ''))
            except:
                pass
        return "0.00", "0", ""

    def _get_woread_redpacket(self):
        """查询阅读红包 (返回: 总额, 7天内过期金额)"""
        total = "0.00"
        expire_7d = "0"
        if not self.token_online: return total, expire_7d

        ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 unicom{version:iphone_c@11.0503}"
        ts = int(time.time() * 1000)
        sign_str = f"{WOREAD_PRODUCT_ID}{WOREAD_SECRET}{ts}"
        md5_hash = hashlib.md5(sign_str.encode()).hexdigest()
        date_str = datetime.now().strftime('%Y%m%d%H%M%S')

        access_token = None
        for _ in range(1):
            try:
                auth_sign = woread_encrypt({"timestamp": date_str})
                auth_url = f"https://10010.woread.com.cn/ng_woread_service/rest/app/auth/{WOREAD_PRODUCT_ID}/{ts}/{md5_hash}"
                auth_res = self._send_request('POST', auth_url, json={"sign": auth_sign}, headers={"User-Agent": ua})
                if auth_res and auth_res.json().get('code') == '0000':
                    access_token = auth_res.json().get('data', {}).get('accesstoken')
                    break
            except: pass
        if not access_token: return total, expire_7d # 认证失败直接退出

        phone_str = self.phone if self.phone and self.phone != "未知" else "13800000000"
        login_inner = {"tokenOnline": woread_encrypt(self.token_online), "phone": woread_encrypt(phone_str), "timestamp": date_str}
        login_sign = woread_encrypt(login_inner)
        headers_login = {"accesstoken": access_token, "User-Agent": ua}

        d = None
        for _ in range(1):
            try:
                login_res = self._send_request('POST', "https://10010.woread.com.cn/ng_woread_service/rest/account/login", headers=headers_login, json={"sign": login_sign})
                if login_res and login_res.json().get('code') == '0000':
                    d = login_res.json().get('data', {})
                    break
            except: pass
        if not d: return total, expire_7d # 登录失败直接退出

        base_param = {
            "timestamp": date_str, "token": d.get('token'), "userid": d.get('userid'),
            "userId": d.get('userid'), "userIndex": d.get('userindex'),
            "userAccount": phone_str, "verifyCode": d.get('verifycode')
        }

        q_sign = woread_encrypt(base_param)
        q_url = "https://10010.woread.com.cn/ng_woread_service/rest/phone/vouchers/queryTicketAccount"
        for _ in range(1):
            try:
                q_res = self._send_request('POST', q_url, headers=headers_login, json={"sign": q_sign})
                if q_res and q_res.json().get('code') == '0000':
                    total = f"{(q_res.json().get('data', {}).get('usableNum', 0) / 100):.2f}"
                    break
            except: pass

        e_sign = woread_encrypt(base_param)
        e_url = "https://10010.woread.com.cn/ng_woread_service/rest/phone/vouchers/query7DayExpireTicketValue"
        for _ in range(1):
            try:
                e_res = self._send_request('POST', e_url, headers=headers_login, json={"sign": e_sign})
                if e_res and e_res.json().get('code') == '0000':
                    expire_val = int(e_res.json().get('data', '0'))
                    if expire_val > 0:
                        expire_7d = f"{(expire_val / 100):.2f}"
                    break
            except: pass

        return total, expire_7d

    def _get_epay_balance(self):
        return True


    def _get_market_watering(self):
        """查询权益超市浇花进度 (已重构：细粒度局部重试)"""
        if not self.ecs_token: return "0/0"

        ticket = ""
        for _ in range(1):
            try:
                t_url = "https://m.client.10010.com/mobileService/openPlatform/openPlatLineNew.htm?to_url=https://contact.bol.wo.cn/market"
                t_res = self._send_request('GET', t_url, headers={"Cookie": self.ecs_token}, allow_redirects=False)
                if t_res and 'location' in t_res.headers:
                    ticket = urllib.parse.parse_qs(urllib.parse.urlparse(t_res.headers['location']).query).get('ticket', [''])[0]
                    if ticket: break
            except: pass
        if not ticket: return "0/0"

        u_token = ""
        for _ in range(1):
            try:
                u_url = f"https://backward.bol.wo.cn/prod-api/auth/marketUnicomLogin?ticket={ticket}"
                u_res = self._send_request('POST', u_url)
                if u_res and u_res.json().get('code') == 200:
                    u_token = u_res.json().get('data', {}).get('token')
                    if u_token: break
            except: pass
        if not u_token: return "0/0"

        for _ in range(1):
            try:
                s_url = "https://backward.bol.wo.cn/prod-api/promotion/activityTask/getMultiCycleProcess?activityId=13"
                s_res = self._send_request('GET', s_url, headers={"Authorization": f"Bearer {u_token}"})
                if s_res and s_res.json().get('code') == 200:
                    data = s_res.json().get('data', {})
                    return f"{data.get('triggeredTime', 0)}/{data.get('triggerTime', 0)}"
            except: pass

        return "0/0"

    def _get_points_info(self):
        """查询通用总积分与本月到期积分"""
        for _ in range(1):
            try:
                url = "https://m.client.10010.com/welfare-mall-front/mobile/show/bj2205/v2/1"
                headers = {
                    "Cookie": self.ecs_token,
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Origin": "https://img.client.10010.com",
                    "Referer": "https://img.client.10010.com/"
                }
                data = "position=123&isTermShow=1"
                res = self._send_request('POST', url, headers=headers, data=data)
                if res:
                    rj = res.json()
                    if rj.get('code') == '0':
                        items = rj.get('resdata', {}).get('data',[])
                        total_score = "0"
                        exp_score = "0"
                        for item in items:
                            if str(item.get('type')) == '1':
                                total_score = str(item.get('number', '0'))
                            elif str(item.get('type')) == '5':
                                exp_score = str(item.get('number', '0'))
                        return total_score, exp_score
            except:
                pass

        for _ in range(1):
            try:
                url_fallback = "https://activity.10010.com/sixPalaceGridTurntableLottery/signin/getIntegral"
                headers_fallback = {
                    "Cookie": self.ecs_token,
                    "Accept": "application/json, text/plain, */*",
                    "Origin": "https://img.client.10010.com",
                    "Referer": "https://img.client.10010.com/"
                }
                res_fallback = self._send_request('GET', url_fallback, headers=headers_fallback)
                if res_fallback:
                    rj_fallback = res_fallback.json()
                    if rj_fallback.get('code') == '0000':
                        total_score_fallback = str(rj_fallback.get('data', {}).get('integralTotal', '0'))
                        return total_score_fallback, "0"
            except:
                pass

        return "0", "0"

    def _get_today_score_from_summary(self):
        """新增：从积分明细查询今日获取积分 (已优化：降低重试放大效应)"""
        for _ in range(1):
            try:
                now = datetime.now()
                year_month = now.strftime('%Y%m')
                today_str = now.strftime('%Y-%m-%d')

                url = "https://m.client.10010.com/welfare-mall-front/new/integral/querySummaryList/v1"
                headers = {
                    "Cookie": self.ecs_token,
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Origin": "https://img.client.10010.com",
                    "Referer": "https://img.client.10010.com/"
                }
                data = f"scoreType=2&typeChar=0&yearMonth={year_month}&from=97000001317%2C003"

                res = self._send_request('POST', url, headers=headers, data=data)
                if res:
                    rj = res.json()
                    if rj.get('code') == '0000':
                        items = rj.get('resdata',[])
                        today_sum = 0
                        if items:
                            for item in items:
                                create_time = str(item.get('createTime', ''))
                                score_val = str(item.get('scoreValue', '0'))
                                if create_time.startswith(today_str):
                                    try:
                                        score = int(float(score_val.replace('+', '')))
                                        if score > 0:
                                            today_sum += score
                                    except: pass
                        return str(today_sum)
            except: pass
        return "0"

    def _get_unused_coupons(self):
        """新增：查询待领卡券 (已优化：降低重试放大效应)"""
        for _ in range(1):
            try:
                url = "https://m.client.10010.com/myPrizeForActivity/openServices/listWinningRecordsForDouble11"
                headers = {
                    "Cookie": self.ecs_token,
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Origin": "https://img.client.10010.com",
                    "Referer": "https://img.client.10010.com/"
                }
                data = "sysActiveStr=SHAKECLIENT_AC20220811152323%2CSHAKECLIENT_AC20231127165002%2CSIGNIN_AC20141230175502%2CSHAKECLIENT_AC20230322151845%2CSHAKECLIENT_AC20240806140724%2CSHAKECLIENT_AC20241119161231%2CSHAKECLIENT_AC20250226023238&enMobile=&otherFlag=1"

                res = self._send_request('POST', url, headers=headers, data=data)
                if res:
                    rj = res.json()
                    if rj.get('code') == '200':
                        records = rj.get('data', {}).get('winningRecords',[])
                        valid_coupons =[]
                        for item in records:
                            if item.get('prizeState') == '00':
                                name = item.get('prizeName', '未知卡券')
                                deadline = str(item.get('deadLineTime', ''))[:10]
                                valid_coupons.append(f"{name},至{deadline}失效")
                        return valid_coupons
            except: pass
        return

    def _get_lianchao_records(self):
        """新增：查询联超记录 (返回格式化的字符串或空字符串)"""
        if not self.ecs_token: return ""

        ticket = ""
        for _ in range(1):
            try:
                t_url = "https://m.client.10010.com/mobileService/openPlatform/openPlatLineNew.htm?to_url=https://contact.bol.wo.cn/"
                t_res = self._send_request('GET', t_url, headers={"Cookie": self.ecs_token}, allow_redirects=False)
                if t_res and 'location' in t_res.headers:
                    ticket = urllib.parse.parse_qs(urllib.parse.urlparse(t_res.headers['location']).query).get('ticket', [''])[0]
                    if ticket: break
            except: pass
        if not ticket: return ""

        market_token = ""
        for _ in range(1):
            try:
                login_y_param = ''.join(random.choices(string.ascii_letters + string.digits + "._-", k=800))
                u_url = f"https://backward.bol.wo.cn/prod-api/auth/marketUnicomLogin?yGdtco4r={login_y_param}"
                headers = {"Content-Type": "application/x-www-form-urlencoded", "Referer": "https://contact.bol.wo.cn/"}
                u_res = self._send_request('POST', u_url, headers=headers, data={"ticket": ticket})
                if u_res:
                    rj = u_res.json()
                    if rj.get('code') == 200:
                        market_token = rj.get('data', {}).get('token')
                        if market_token: break
            except: pass
        if not market_token: return ""

        for _ in range(1):
            try:
                prize_y = "0w7_01AEqWtGwhhIWWIF.rWkMvnBB9Mh9xz3FEIloLlnYoZJbLc0eDwQZnsxojfIE27JZ.59713kGB6h5GOPecA2a4wyzfycIr9ENlR2t255omrrxyPAEEhsZqziXJ95Ysc6jE8a2_rJYdsdALymdBZvd9jLeNpw8M9DHnoScRN_bd.tlRZAyGT.NjmA2zeWt_rT9EWM0mVTaTEfvFVkg8baol5OBBmnTmLzs1R57IjOSB3AouoNc6CSBDlED3PQt09epkhhK4FjuVZ1Sfq._6eMMHKHrRAtpPPcCrwE6thPEFFPEANzTnVAjJLFZ3AIkNFrywUSOmoR1k0yxLC_sEHfbRdqGCX26nNJYXKn3dFuzRZAK.4sQrOV"
                q_url = f"https://backward.bol.wo.cn/prod-api/market/contactReceive/queryReceiveRecord?yGdtco4r={prize_y}"
                headers = {
                    "Authorization": f"Bearer {market_token}",
                    "Content-Type": "application/json",
                    "Referer": "https://contact.bol.wo.cn/"
                }
                phone_str = self.phone if self.phone and self.phone != "未知" else ""
                payload = {
                    "limit": 10,
                    "page": 1,
                    "mobile": phone_str,
                    "businessSources":["3", "4", "5", "6", "99"],
                    "isPromotion": 1,
                    "returnFormatType": 1
                }
                q_res = self._send_request('POST', q_url, headers=headers, json=payload)
                if q_res:
                    rj = q_res.json()
                    if rj.get('code') == 200:
                        records = rj.get("data", {}).get("recordObjs",[])
                        if records:
                            prize_lines =[]
                            for item in records:
                                status_icon = '✔' if str(item.get('isReceive')) == '1' else '✘'
                                prize_name = item.get('recordName', '未知奖品')
                                prize_time = str(item.get('prizeTime') or item.get('receiveTime') or '未知').split(' ')[0]
                                prize_lines.append(f"{status_icon}{prize_name}, 于{prize_time}中")
                            return "\n🎉 权超记录: \n" + "\n".join(prize_lines)
            except: pass

        return ""

    def query_all_assets(self):
        """聚合查询所有资产 (已新增阅读红包与联超记录开关逻辑)"""
        results = {
            "score": "0", "today_score": "0",
            "tel_red": "0.00", "tel_exp": "0", "tel_month": "",
            "read_red": "0.00", "read_exp": "0",
            "epay": "0.00", "epay_exp": "0.00", "epay_sub": "",
            "watering": "0/0",
            "score_exp": "0",
            "coupons":[],  # 新增卡券字段
            "lianchao": "" # 新增联超记录字段
        }

        is_unicom = False
        if self.phone and re.match(r'^1(3[0-2]|4[56]|5[56]|6[67]|7[0156]|8[56]|9[6])\d{8}$', str(self.phone)):
            is_unicom = True

        results["is_unicom"] = is_unicom

        results["score"], results["score_exp"] = self._get_points_info()

        if is_unicom:
            results["tel_red"], results["tel_exp"], results["tel_month"] = self._get_signin_redpacket()
            results["coupons"] = self._get_unused_coupons()

        yuedu_enable = str(sg.bucketGet('yuhua_zglt', 'yuedu')).lower() in ['true', '1', 'yes']
        if yuedu_enable:
            results["read_red"], results["read_exp"] = self._get_woread_redpacket()

        lianchao_enable = str(sg.bucketGet('yuhua_zglt', 'lianchao')).lower() in ['true', '1', 'yes']
        if lianchao_enable:
            results["lianchao"] = self._get_lianchao_records()

        results["epay"], results["epay_exp"], results["epay_sub"] = self._get_epay_balance()
        results["watering"] = self._get_market_watering()
        results["today_score"] = self._get_today_score_from_summary()

        return results

    def close(self):
        if self.session:
            self.session.close()
            self.session = None

def gen_unique_id(prefix=""):
    timestamp = int(time.time() * 1_000_000)
    return f"{prefix}{timestamp}"

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()
imtype = sender.getImtype()
uservalue = sg.bucketGet(bucket='yuhua_zglt_user', key=userid)

def get_config():
    """获取插件配置"""
    manage_cmd = sg.bucketGet('yuhua_zglt', 'manage_cmd') or '联通管理'
    query_cmd = sg.bucketGet('yuhua_zglt', 'query_cmd') or '联通查询'
    login_cmd = sg.bucketGet('yuhua_zglt', 'login_cmd') or '联通登录'
    price = Decimal(sg.bucketGet('yuhua_zglt', 'price') or '0')
    bf_str = sg.bucketGet('yuhua_zglt', 'bingfa') or '5'
    yuhua_zglt_qlname = sg.bucketGet('yuhua_zglt', 'yuhua_zglt_qlname') or ''
    yuhua_zglt_osname = sg.bucketGet('yuhua_zglt', 'yuhua_zglt_osname') or 'chinaUnicomCookie'
    aiting_var = sg.bucketGet('yuhua_zglt', 'aiting_var') # 新增

    try:
        bf_num = int(bf_str)
    except:
        bf_num = 5
    return (manage_cmd, query_cmd, login_cmd, price, bf_num, yuhua_zglt_qlname, yuhua_zglt_osname, aiting_var)

manage_cmd, query_cmd, login_cmd, price, bingfa, yuhua_zglt_qlname, yuhua_zglt_osname, aiting_var = get_config()

def seekql():
    try:
        if len(yuhua_zglt_qlname) == 0:
            sender.reply("""
=====配置错误=====
❌ 未配置青龙信息
------------------
请在插件配置中填写:
Host丨ClientID丨ClientSecret
• 使用中文丨分隔
• 示例:
http://ql.example.com/丨abcd丨1234
==================""")
            exit(0)

        qllist = yuhua_zglt_qlname.split('丨')
        if len(qllist) != 3:
            sender.reply("""
=====格式错误=====
❌ 青龙配置格式错误
------------------
正确格式:
Host丨ClientID丨ClientSecret
==================""")
            exit(0)

        QLurl = qllist[0].strip()
        ClientID = qllist[1].strip()
        ClientSecret = qllist[2].strip()

        if not all([QLurl, ClientID, ClientSecret]):
            sender.reply("""
=====参数错误=====
❌ 青龙配置参数不完整
------------------
请确保以下参数都已填写:
• 青龙面板地址(Host)
• 应用ID(ClientID)
• 应用密钥(ClientSecret)
==================""")
            exit(0)

        if not QLurl.startswith(('http://', 'https://')):
            sender.reply(f"""
=====地址错误=====
❌ 青龙地址格式错误
------------------
正确格式:
• http://qinglong.example.com/
• https://ql.example.com:5700/
==================""")
            exit(0)

        try:
            qltoken = QLtoken(QLurl=QLurl, ClientID=ClientID, ClientSecret=ClientSecret)
            return QLurl, qltoken
        except Exception as e:
            raise Exception(f"获取Token失败: {str(e)}")

    except Exception as e:
        sender.reply(f"""
=====连接失败=====
❌ 无法连接青龙面板
------------------
请检查:
1. 青龙面板是否运行
2. 网络是否正常
3. 配置是否正确
------------------
当前配置:
• 地址: {QLurl if 'QLurl' in locals() else '未设置'}
• 应用ID: {ClientID[:4] + '****' if 'ClientID' in locals() else '未设置'}
==================""")
        exit(0)

def delenvs(id):
    if id is None or not QLurl or not qltoken:
        return
    url = f"{QLurl}/open/envs"
    headers = {
        "Authorization": "Bearer" + ' ' + qltoken,
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    data = [id]
    response = requests.delete(url, headers=headers, json=data, proxies={"http": None, "https": None}).json()

def allenvs(osname, account):
    if not QLurl or not qltoken:
        return None
    url = f"{QLurl}/open/envs"
    headers = {
        "Authorization": "Bearer" + ' ' + qltoken,
        "accept": "application/json"
    }
    response = requests.get(url=url, headers=headers, proxies={"http": None, "https": None}).json()
    qlid = None
    if response['code'] == 200:
        envslist = response['data']
        for envs in envslist:
            envname = envs['name']
            remarks = envs['remarks']
            if remarks is None:
                continue
            if osname == envname and str(account) in remarks:
                qlid = envs['id']
                break
        return qlid
    else:
        sender.reply('连接青龙获取变量失败')
        exit(0)

def Addenvs(osname, value, account, phone, owner_id):
    if not QLurl or not qltoken:
        return
    phone = phone[:3] + '*' * 4 + phone[7:]
    url = f"{QLurl}/open/envs"
    headers = {
        "Authorization": "Bearer" + ' ' + qltoken,
        "accept": "application/json"
    }
    response = requests.get(url=url, headers=headers, proxies={"http": None, "https": None}).json()
    qlid = None
    if response['code'] == 200:
        envslist = response['data']
        for envs in envslist:
            remarks = envs['remarks']
            envname = envs['name']
            if remarks is None:
                continue
            if osname == envname and str(account) in remarks:
                qlid = envs['id']
                break
    else:
        sender.reply('连接青龙获取变量失败')
        exit(0)

    if qlid is None:
        QLzt(osname, value, account, phone, owner_id)
    else:
        QLupdate(osname, value, account, qlid, phone, owner_id)

def QLupdate(osname, value, account, qlid, phone, owner_id):
    qlurl = f"{QLurl}/open/envs"
    data = {
        "value": value, # 直接使用原始字符串
        "name": osname,
        "remarks": f'联通:{account}丨用户:{owner_id}丨手机:{phone}丨联通管理',
        "id": qlid
    }
    headers = {
        "Authorization": "Bearer" + ' ' + qltoken,
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    response = requests.put(qlurl, headers=headers, data=json.dumps(data), proxies={"http": None, "https": None})
    if response.status_code == 200:
        response_json = response.json()
        data = response_json['data']
        if data is None:
            exit(0)
        id = data['id']
        createdAt = data['createdAt']
        return id, createdAt
    else:
        sender.reply('更新变量失败，请稍后重试')
        exit(0)

def QLzt(osname, value, account, phone, owner_id):
    try:
        qlurl = f"{QLurl}/open/envs"

        data =[{
            "value": value,
            "name": osname,
            "remarks": f'联通:{account}丨用户:{owner_id}丨手机:{phone}丨联通管理'
        }]

        headers = {
            "Authorization": f"Bearer {qltoken}",
            "accept": "application/json",
            "Content-Type": "application/json",
        }

        response = requests.post(qlurl, headers=headers, json=data, proxies={"http": None, "https": None})

        if response.status_code != 200:
            sender.reply(f"""
=====添加变量失败=====
❌ 请求失败
状态码: {response.status_code}
==================""")
            exit(0)

        result = response.json()
        if result.get('code') != 200:
            sender.reply(f"""
=====添加变量失败=====
❌ 青龙返回错误
错误信息: {result.get('message')}
==================""")
            exit(0)

        if "value must be unique" in response.text:
            return

        data = result.get('data')
        if not data or not isinstance(data, list) or len(data) == 0:
            sender.reply("""
=====添加变量失败=====
❌ 青龙返回数据异常
==================""")
            exit(0)

        return data[0].get('id')

    except Exception as e:
        sender.reply(f"""
=====系统错误=====
❌ 添加青龙变量失败
------------------
错误信息: {str(e)}
==================""")
        exit(0)

def QLtoken(QLurl, ClientID, ClientSecret):  # 获取青龙token
    try:
        url = f'{QLurl}/open/auth/token?client_id={ClientID}&client_secret={ClientSecret}'
        response = requests.get(url, proxies={"http": None, "https": None})

        if response.status_code != 200:
            sender.reply(f"""
=====请求失败=====
❌ 青龙API请求失败
------------------
状态码: {response.status_code}
请检查:
• API地址是否正确
• 面板是否正常运行
==================""")
            exit(0)

        result = response.json()
        if "token" in result.get('data', {}):
            return result['data']['token']
        else:
            sender.reply("""
=====认证失败=====
❌ 获取Token失败
------------------
请检查:
• ClientID是否正确
• ClientSecret是否正确
• 应用是否有权限
==================""")
            exit(0)

    except requests.exceptions.RequestException as e:
        sender.reply(f"""
=====网络错误=====
❌ 连接青龙面板失败
------------------
请检查:
• 青龙地址是否正确
• 网络是否正常
==================""")
        exit(0)
    except Exception as e:
        sender.reply(f"""
=====系统错误=====
❌ 处理请求时出错
------------------
请检查:
• 配置格式是否正确
• 错误信息: {str(e)}
==================""")
        exit(0)

QLurl, qltoken = seekql()
today_time = str(datetime.now().date())


def login():
    """账号登录"""
    login_guide = """
=====登录方式=====
[1] Token登录
[2] 中国联通账密 (维护)
[3] 中国联通短信 (推荐)
------------------
回复数字选择方式
回复"q"退出"""

    sender.reply(login_guide)
    choice = sender.input(60000, 0, False)

    if not choice:  # 如果超时未输入
        sender.reply("❌ 输入超时")
        return
    elif choice.lower() == 'q':  # 输入q时退出
        sender.reply("✅ 已退出操作")
        return

    try:
        if choice == '2':
            account_password_login()
        elif choice == '3':
            verification_code_login()
        elif choice == '1':
            token_online_login()
        else:
            sender.reply("❌ 无效的选择")
            return

    except Exception as e:
        sender.reply(f"❌ 登录失败: {str(e)}")
        return


def _query_single_account(unique_id):
    """【内部函数】用于并发查询单个账号的积分信息。"""
    time.sleep(random.uniform(0.2, 0.5))
    phone = sg.bucketGet('yuhua_zglt_phone', unique_id) or "未知"
    phone_mask = phone[:3] + "****" + phone[-4:] if len(phone) >= 7 else phone
    auth_time = '2099-12-31'
    now_date = datetime.now().date()
    if not auth_time: return f"【{phone_mask}】未授权"
    auth_date = datetime.strptime(auth_time, "%Y-%m-%d").date()
    if auth_date < now_date: return f"【{phone_mask}】授权已过期"

    ecs_token = sg.bucketGet('yuhua_zglt_ecs_token', unique_id)
    token_online = sg.bucketGet('yuhua_zglt_token_online', unique_id)

    ltp = LTP(phone=phone, ecs_token=ecs_token, token_online=token_online)

    try:
        ok, msg = ltp.check_validity()
        if not ok:
            is_relogin = _try_auto_relogin(unique_id)
            if is_relogin:
                ltp.close()
                ecs_token = sg.bucketGet('yuhua_zglt_ecs_token', unique_id)
                token_online = sg.bucketGet('yuhua_zglt_token_online', unique_id)
                ltp = LTP(phone=phone, ecs_token=ecs_token, token_online=token_online)
                ok, msg = ltp.check_validity()
            if not ok:
                if "CK已失效" in msg or "缺少基础" in msg:
                    return f"【{phone_mask}】登录凭证已失效，请重新登录"
                return f"【{phone_mask}】查询失败: {msg}"

        assets = ltp.query_all_assets()


        def safe_float(value):
            try:
                if value is None: return 0.0
                return float(value)
            except (ValueError, TypeError):
                return 0.0

        def format_money(value):
            return f"{safe_float(value):.2f}"

        sup_map = {
            '0':'⁰', '1':'¹', '2':'²', '3':'³', '4':'⁴', '5':'⁵', '6':'⁶', '7':'⁷', '8':'⁸', '9':'⁹',
            'm':'ᵐ', 'd':'ᵈ'
        }
        def to_sup(s):
            return "".join(sup_map.get(c, c) for c in str(s))

        tel_display = ""
        if assets.get("is_unicom", False):
            tel_str = f"{format_money(assets.get('tel_red'))}元"

            if safe_float(assets.get('tel_exp')) > 0:
                month_val = str(assets.get('tel_month', '')).lstrip('0')
                current_month = str(now_date.month)

                if month_val == current_month:
                    tag_str = 'm'  # 本月过期
                else:
                    tag_str = f"{month_val}m" if month_val else 'm'

                tel_str += f" | {assets['tel_exp']} {to_sup(tag_str)}"

            tel_display = f"\n📦 话费红包: {tel_str}"

        read_display = ""
        yuedu_enable = str(sg.bucketGet('yuhua_zglt', 'yuedu')).lower() in ['true', '1', 'yes']
        if yuedu_enable:
            read_str = f"{format_money(assets.get('read_red'))}元"
            if safe_float(assets.get('read_exp')) > 0:
                read_str += f" | {assets['read_exp']} {to_sup('7d')}"
            read_display = f"\n📝 阅读红包: {read_str}"

        epay_str = f"{format_money(assets.get('epay'))}元"
        if safe_float(assets.get('epay_exp')) > 0:
            epay_str += f" | {assets['epay_exp']} {to_sup('3d')}"

        try:
            score_val_int = int(safe_float(assets.get('score')))
            score_str = str(score_val_int)
        except:
            score_str = "0"

        score_exp_val = str(assets.get('score_exp', '0'))
        if score_exp_val != "0" and safe_float(score_exp_val) > 0:
            score_str += f" | {score_exp_val} {to_sup('m')}"

        today_score_str = str(assets.get('today_score', '0'))

        coupons = assets.get('coupons',[])
        coupon_str = ""
        if assets.get("is_unicom", False) and coupons:
            if len(coupons) == 1:
                coupon_str = f"\n🎫 待领卡券: {coupons[0]}"
            else:
                coupon_str = f"\n🎫 待领卡券: \n" + "\n".join(coupons)

        lianchao_str = assets.get('lianchao', '')

        return f"""
=====账号信息=====
🤪 账号: {phone_mask}
🔥 当前积分: {score_str}
🎨 今日积分: {today_score_str}{tel_display}
💳 沃立减金: {epay_str}{read_display}
⛱️ 浇花进度: {assets.get('watering', '0/0')}
☁️ 授权到期: {auth_date.strftime('%Y-%m-%d')}{coupon_str}{lianchao_str}
=================="""

    finally:
        ltp.close()

def query_account():
    """
    【联通查询】：查询已授权账号的积分信息（并发版）
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed

    if not uservalue:
        sender.reply(f"""
=====未绑定账号=====
❌ 未找到任何账号信息
💡 发送 {login_cmd} 绑定账号
==================""")
        return
    accounts = _sg_literal(uservalue)
    if not accounts:
        sender.reply(f"""
=====未绑定账号=====
❌ 未找到任何账号信息
💡 发送 {login_cmd} 绑定账号
==================""")
        return

    sender.reply(f"正在查询....")

    bf_num_local = bingfa

    try:
        with ThreadPoolExecutor(max_workers=bf_num_local) as executor:
            futures = {executor.submit(_query_single_account, acc_id): acc_id for acc_id in accounts}

            for future in as_completed(futures):
                try:
                    result_msg = future.result()
                    if result_msg:
                        sender.reply(result_msg)
                except Exception as e:
                    sender.reply(f"❌ 查询某个账号时出错: {e}")
    finally:
        cleanup_resources()

def _mask_identifier(identifier: str) -> str:
    """
    将账号/手机号/UID 等中间 4 位替换为 **** 用于展示
    - 已经含 **** 时原样返回
    - 长度 <= 8 时返回原值
    """
    if "****" in identifier or len(identifier) <= 8:
        return identifier
    return identifier[:4] + "****" + identifier[-4:]

def auth_all_accounts_for_user(accounts):
    """为指定用户的所有账号一键授权"""
    prompt = "=====一键授权=====\n"
    if price > 0:
        prompt += f"授权价格: {price}元/月\n"
    prompt += "请输入授权月数\n------------------\n回复数字设置月数\n回复\"q\"退出"
    sender.reply(prompt)

    months_str = sender.input(60000, 0, False)
    if not months_str or months_str.lower() == 'q':
        sender.reply("✅ 已退出操作")
        return

    try:
        months = int(months_str)
        if months <= 0: raise ValueError()
    except ValueError:
        sender.reply("❌ 无效的月数")
        return

    accounts_to_auth = accounts

    total_amount = len(accounts_to_auth) * months * price
    if total_amount > 0:
        pay_ok = process_payment(total_amount, months, f"名下所有 {len(accounts_to_auth)} 个账号")
        if not pay_ok:
            return

    success_count = 0
    failed_count = 0
    for acc_id in accounts_to_auth:
        try:
            calculate_auth_time(acc_id, months * 30)
            True

            token = sg.bucketGet('yuhua_zglt_token_online', acc_id)
            phone = sg.bucketGet('yuhua_zglt_phone', acc_id) or acc_id
            if token:
                sync_appid = sg.bucketGet('yuhua_zglt_appid', acc_id)
                sync_val = f"{token}#{sync_appid}" if sync_appid else token
                Addenvs(osname=yuhua_zglt_osname, value=sync_val, account=acc_id, phone=phone, owner_id=userid)

                if aiting_var and aiting_var != '0':
                    Addenvs(osname=aiting_var, value=phone, account=acc_id, phone=phone, owner_id=userid)

            success_count += 1
        except Exception:
            failed_count += 1

    sender.reply(f"""
=====授权完成=====
✅ 成功: {success_count}个账号
❌ 失败: {failed_count}个账号
⏰ 时长: 授权{months}月
==================""")


def manage_account():
    """
    【账号管理函数】展示账号列表并允许用户选择操作
    """
    if not uservalue:
        sender.reply(f"""
=====未绑定账号=====
❌ 未找到任何账号信息
💡 发送 {login_cmd} 绑定账号
==================""")
        return

    accounts = _sg_literal(uservalue)
    if not accounts:
        sender.reply(f"""
=====未绑定账号=====
❌ 未找到任何账号信息
💡 发送 {login_cmd} 绑定账号
==================""")
        return

    account_list = "=====账号列表=====\n[0] 授权全部账号\n"

    for i, acc_id in enumerate(accounts, 1):
        phone = sg.bucketGet('yuhua_zglt_phone', acc_id) or "未知"
        phone_mask = _mask_identifier(phone)
        auth_str = '2099-12-31'

        status_line = ""
        if auth_str:
            try:
                auth_date = datetime.strptime(auth_str, "%Y-%m-%d").date()
                if auth_date > datetime.now().date():
                    status_line = f"✅ {auth_date.strftime('%Y-%m-%d')}"
                else:
                    status_line = "❌ 已过期"
            except ValueError:
                status_line = "⚠️ 未授权"
        else:
            status_line = "⚠️ 未授权"

        account_list += f"------------------\n[{i}] 账号信息\n🤪 账号: {phone_mask}\n☁ 授权: {status_line}\n"

    account_list += "------------------\n回复数字选择\n回复'q'退出\n=================="
    sender.reply(account_list)

    choice = sender.input(60000, 0, False)
    if not choice or choice.lower() == 'q':
        sender.reply("✅ 已退出操作")
        return

    try:
        choice_idx = int(choice)
        if choice_idx == 0:
            auth_all_accounts_for_user(accounts)
        elif 1 <= choice_idx <= len(accounts):
            account = accounts[choice_idx - 1]
            show_account_menu(account)
        else:
            raise ValueError()
    except (ValueError, IndexError):
        sender.reply("❌ 无效的选择")

def show_account_menu(account):
    """显示账号操作菜单"""
    menu = """
=====账号操作=====
[1] 授权账号
[2] 删除账号
[3] 配置AppId
------------------
回复数字选择操作
回复"q"退出"""
    sender.reply(menu)
    choice = sender.input(60000, 0, False)
    if not choice:
        sender.reply("❌ 输入超时")
        return
    if choice.lower() == 'q':
        sender.reply("✅ 已退出操作")
        return
    if choice == '1':
        auth_account(account)
    elif choice == '2':
        confirm_delete(account)
    elif choice == '3':
        configure_appid_manual(account)
    else:
        sender.reply("❌ 无效的选择")

def configure_appid_manual(account):
    """管理菜单手动配置AppId流程"""
    auth_time = '2099-12-31'
    if not auth_time or auth_time < today_time:
        sender.reply("❌ 该账号授权无效或已过期")
        return

    sender.reply("""=====配置AppId=====
❶ 回复『d』清除数据或按②新增或更新
② 打开该路径中的文件『/storage/emulated/0/Documents/Unicom/appid』复制文本内容并回复
-----------------
请在300秒内完成
回复"q"取消""")

    app_input = sender.input(300000, 1, False)
    if not app_input:
        sender.reply("❌ 输入超时")
        return
    if app_input.lower() == 'q':
        sender.reply("✅ 已退出操作")
        return
    if app_input.lower() == 'd':
        try:
            sg.bucketDel('yuhua_zglt_appid', account)
        except Exception:
            pass
        sender.reply("✅ 已完成删除")
        token_online = sg.bucketGet('yuhua_zglt_token_online', account)
        phone = sg.bucketGet('yuhua_zglt_phone', account)
        if token_online: Addenvs(osname=yuhua_zglt_osname, value=token_online, account=account, phone=phone, owner_id=userid)
        return

    new_appid = app_input.strip()
    token_online = sg.bucketGet('yuhua_zglt_token_online', account)

    if token_online:
        pl = {"token_online": token_online, "appId": new_appid, "reqtime": int(time.time()*1000), **VERIFICATION_DEVICE_PARAMS}
        ua = f"Dalvik/2.1.0 (Linux; U; Android {VERIFICATION_DEVICE_PARAMS.get('deviceOS')}; {VERIFICATION_DEVICE_PARAMS.get('deviceModel')} Build/UKQ1.231108.001);unicom{{version:{VERIFICATION_DEVICE_PARAMS.get('version')}}};ltst;"
        hd = {"User-Agent": ua, "Content-Type": "application/x-www-form-urlencoded", "Host": "m.client.10010.com"}

        with requests.Session() as sess:
            resp = send_request_global('POST', "https://m.client.10010.com/mobileService/onLine.htm", data=pl, headers=hd, session=sess)

        if resp:
            rj = resp.json()
            if rj.get('code') in ['0', '0000']:
                sg.bucketSet('yuhua_zglt_appid', account, new_appid)
                sender.reply("✅ 已成功配置")
                phone = sg.bucketGet('yuhua_zglt_phone', account)
                Addenvs(osname=yuhua_zglt_osname, value=f"{token_online}#{new_appid}", account=account, phone=phone, owner_id=userid)
            else:
                fail_reason = rj.get('dsc') or rj.get('desc') or '未知原因'
                sender.reply(f"❌ 鉴权失败: {fail_reason}")
        else:
            sender.reply("❌ 鉴权失败: 网络请求无响应")
    else:
        sender.reply("❌ 未找到Token Online，无法验证AppId，请重新登录")

def confirm_delete(account):
    """确认是否删除账号"""
    phone = sg.bucketGet('yuhua_zglt_phone', account) or "未知"
    phone_mask = phone[:3] + "****" + phone[-4:] if len(phone) >= 7 else phone
    sender.reply(f"⚠️ 确认要删除账号 {phone_mask} 吗？(y/n)")
    confirm = sender.input(30000, 0, False)
    if not confirm:  # 如果超时未输入
        sender.reply("❌ 输入超时")
        return
    elif confirm.lower() == 'n':
        sender.reply("✅ 已退出操作")
        return
    elif confirm.lower() == 'q':  # 输入q时退出
        sender.reply("✅ 已退出操作")
        return
    elif confirm.lower() != 'y':
        sender.reply("❌ 无效的选择")
        return
    delete_account(account)

def delete_account(account):
    """
    【删除账号】：删除本地记录
    """
    phone = sg.bucketGet('yuhua_zglt_phone', account) or "未知"
    phone_mask = phone[:3] + "****" + phone[-4:] if len(phone) >= 7 else phone
    accounts = _sg_literal(uservalue or '[]')
    if account not in accounts:
        sender.reply("❌ 未找到账号")
        return

    try:
        qlid = allenvs(osname=yuhua_zglt_osname, account=account)
        if qlid:
            delenvs(id=qlid)

        if aiting_var and aiting_var != '0':
            qlid_aiting = allenvs(osname=aiting_var, account=account)
            if qlid_aiting:
                delenvs(id=qlid_aiting)
    except:
        pass

    accounts.remove(account)
    sg.bucketSet('yuhua_zglt_user', userid, str(accounts))
    try:
        sg.bucketDel('yuhua_zglt_token', account)
    except Exception:
        pass
    try:
        pass
    except Exception:
        pass
    try:
        sg.bucketDel('yuhua_zglt_phone', account)
    except Exception:
        pass
    try:
        sg.bucketDel('yuhua_zglt_password', account)
    except Exception:
        pass
    try:
        sg.bucketDel('yuhua_zglt_ecs_token', account)
    except Exception:
        pass
    try:
        sg.bucketDel('yuhua_zglt_token_online', account)
    except Exception:
        pass
    sender.reply(f"✅ 已删除账号 {phone_mask}")

def auth_account(account):
    """【账号授权】：用户侧手动授权/续费"""
    phone = sg.bucketGet('yuhua_zglt_phone', account) or "未知"
    phone_mask = phone[:3] + "****" + phone[-4:] if len(phone) >= 7 else phone
    if not price:
        sender.reply("""
=====账号授权=====
请输入授权月数
------------------
回复数字设置月数
回复"q"退出""")
    else:
        sender.reply(f"""
=====账号授权=====
授权价格: {price}元/月
请输入授权月数
------------------
回复数字设置月数
回复"q"退出""")
    months_str = sender.input(60000, 0, False)
    if not months_str:
        sender.reply("❌ 输入超时")
        return
    elif months_str.lower() == 'q':
        sender.reply("✅ 已退出操作")
        return
    try:
        months = int(months_str)
        if months <= 0:
            raise ValueError()
    except:
        sender.reply("❌ 无效的月数")
        return
    amount = months * price
    if amount > 0:
        if not process_payment(amount, months, phone_mask):
            return
    auth_time = calculate_auth_time(account, months * 30)
    True

    token = sg.bucketGet('yuhua_zglt_token_online', account)
    appid = sg.bucketGet('yuhua_zglt_appid', account)
    if token:
        sync_val = f"{token}#{appid}" if appid else token
        Addenvs(osname=yuhua_zglt_osname, value=sync_val, account=account, phone=phone, owner_id=userid)

        if aiting_var and aiting_var != '0':
            Addenvs(osname=aiting_var, value=phone, account=account, phone=phone, owner_id=userid)

    days = 30*months
    sender.reply(f"""
=====授权成功=====
🤪 账号: {phone_mask}
⏰ 时长: {days}天
📅 到期: {auth_time}
=======================""")


def process_payment(amount, months, phone_mask):
    return True
def clean_expired():
    try:
        sender.reply('该管理项已取消，账号直接运行')
    except Exception:
        pass
    return None
def admin_auth():
    try:
        sender.reply('该管理项已取消，账号直接运行')
    except Exception:
        pass
    return None
def auth_all_users():
    """一键授权所有用户（批量授权）"""
    sender.reply("""
=====批量授权=====
请输入授权天数
------------------
回复数字设置天数
回复"q"退出""")
    try:
        days_str = sender.input(60000, 0, False)
        if not days_str:
            sender.reply("❌ 输入超时")
            return
        elif days_str.lower() == 'q':
            sender.reply("✅ 已退出操作")
            return
        days = int(days_str)
        users = sg.bucketAllKeys('yuhua_zglt_user')
        success = 0
        failed = 0
        for user in users:
            accounts = _sg_literal(sg.bucketGet('yuhua_zglt_user', user) or '[]')
            for acc_id in accounts:
                try:
                    calculate_auth_time(acc_id, days)
                    True

                    token = sg.bucketGet('yuhua_zglt_token_online', acc_id)
                    appid = sg.bucketGet('yuhua_zglt_appid', acc_id)
                    phone = sg.bucketGet('yuhua_zglt_phone', acc_id) or acc_id
                    if token:
                        sync_val = f"{token}#{appid}" if appid else token
                        Addenvs(osname=yuhua_zglt_osname, value=sync_val, account=acc_id, phone=phone, owner_id=user)

                        if aiting_var and aiting_var != '0':
                            Addenvs(osname=aiting_var, value=phone, account=acc_id, phone=phone, owner_id=user)

                    success += 1
                    log_operation('batch_auth', user, acc_id, 'success')
                except Exception as e:
                    failed += 1
                    log_operation('batch_auth', user, acc_id, 'failed', str(e))

        action_text = "授权" if days > 0 else "扣除"
        day_abs = abs(days)
        sender.reply(f"""
=====操作完成=====
✅ 成功: {success}个账号
❌ 失败: {failed}个账号
⏰ 时长: {action_text}{day_abs}天
==================""")
    except ValueError:
        sender.reply("❌ 无效的天数")
    except Exception as e:
        sender.reply(f"❌ 授权失败: {str(e)}")

def auth_specific_user():
    """指定用户授权"""
    sender.reply("""
=====指定授权=====
请输入用户ID
(发送myuid可获取ID)
------------------
回复"q"退出""")
    user_id = sender.input(60000, 0, False)
    if not user_id:
        sender.reply("❌ 输入超时")
        return
    if user_id.lower() == 'q':
        sender.reply("✅ 已退出操作")
        return

    accounts = _sg_literal(sg.bucketGet('yuhua_zglt_user', user_id) or '[]')
    if not accounts:
        sender.reply("❌ 该用户没有绑定账号")
        return

    account_list_msg = "=====账号列表=====\n[0] 授权全部账号\n"
    for i, acc_id in enumerate(accounts, 1):
        phone = sg.bucketGet('yuhua_zglt_phone', acc_id) or "未知"
        phone_mask = _mask_identifier(phone)
        auth_str = '2099-12-31'

        status_line = ""
        if auth_str:
            try:
                auth_date = datetime.strptime(auth_str, "%Y-%m-%d").date()
                if auth_date > datetime.now().date():
                    status_line = f"✅ {auth_date.strftime('%Y-%m-%d')}"
                else:
                    status_line = "❌ 已过期"
            except ValueError:
                status_line = "⚠️ 未授权"
        else:
            status_line = "⚠️ 未授权"

        account_list_msg += f"------------------\n[{i}] 账号信息\n🤪 账号: {phone_mask}\n☁ 授权: {status_line}\n"

    account_list_msg += "------------------\n回复数字选择\n回复'q'退出\n=================="
    sender.reply(account_list_msg)

    choice_str = sender.input(60000, 0, False)
    if not choice_str:
        sender.reply("❌ 输入超时")
        return
    if choice_str.lower() == 'q':
        sender.reply("✅ 已退出操作")
        return

    try:
        choice_idx = int(choice_str)
        if not 0 <= choice_idx <= len(accounts):
            raise ValueError("无效的选择")
    except ValueError:
        sender.reply("❌ 无效的选择")
        return

    target_accounts = []
    if choice_idx == 0:
        target_accounts = accounts
    else:
        target_accounts.append(accounts[choice_idx - 1])

    sender.reply("""
=====指定授权=====
请输入授权天数
------------------
回复数字设置天数
回复"q"退出""")
    days_str = sender.input(60000, 0, False)
    if not days_str:
        sender.reply("❌ 输入超时")
        return
    if days_str.lower() == 'q':
        sender.reply("✅ 已退出操作")
        return

    try:
        days = int(days_str)
        latest_accounts = _sg_literal(sg.bucketGet('yuhua_zglt_user', user_id) or '[]')
        if not latest_accounts:
            sender.reply("❌ 操作失败：该用户已无任何账号")
            return

        success = 0
        failed = 0
        for acc_id in target_accounts:
            if acc_id not in latest_accounts:
                failed += 1
                continue

            try:
                calculate_auth_time(acc_id, days)
                True

                token = sg.bucketGet('yuhua_zglt_token_online', acc_id)
                appid = sg.bucketGet('yuhua_zglt_appid', acc_id)
                phone = sg.bucketGet('yuhua_zglt_phone', acc_id) or acc_id
                if token:
                    sync_val = f"{token}#{appid}" if appid else token
                    Addenvs(osname=yuhua_zglt_osname, value=sync_val, account=acc_id, phone=phone, owner_id=user_id)

                    if aiting_var and aiting_var != '0':
                         Addenvs(osname=aiting_var, value=phone, account=acc_id, phone=phone, owner_id=user_id)

                success += 1
                log_operation('specific_auth', user_id, acc_id, 'success')
            except Exception as e:
                failed += 1
                log_operation('specific_auth', user_id, acc_id, 'failed', str(e))

        action_text = "授权" if days > 0 else "扣除"
        day_abs = abs(days)
        reply_msg = f"""
=====操作完成=====
👤 用户: {user_id}
✅ 成功: {success}个账号
❌ 失败: {failed}个账号
⏰ 时长: {action_text}{day_abs}天"""

        if failed > 0:
            reply_msg += "\n⚠️ 部分账号授权失败，原因可能是它们在操作期间被后台任务自动清理"

        reply_msg += "\n=================="
        sender.reply(reply_msg)

    except ValueError:
        sender.reply("❌ 无效的天数")
    except Exception as e:
        sender.reply(f"❌ 授权时发生未知错误: {str(e)}")


def log_operation(operation, user, account, status, message=''):
    """记录操作日志(仅存储到bucket，不再自动推送给用户)"""
    try:
        log = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'user': user,
            'account': account,
            'status': status,
            'message': message
        }
        log_key = f"{operation}_{user}_{account}_{int(time.time())}"
        sg.bucketSet('yuhua_zglt_logs', log_key, json.dumps(log))
    except Exception:
        pass

def cron_task():
    """定时任务处理"""
    if imtype != 'fake':
        pass
    today_str = str(datetime.now().date())
    try:
        users = sg.bucketAllKeys('yuhua_zglt_user')
        for user in users:
            accounts = _sg_literal(sg.bucketGet('yuhua_zglt_user', user) or '[]')
            for acc_id in accounts:
                time.sleep(random.uniform(0.5, 1.0))
                try:
                    ecs_token = sg.bucketGet('yuhua_zglt_ecs_token', acc_id)
                    phone = sg.bucketGet('yuhua_zglt_phone', acc_id) or "未知"
                    if not ecs_token:
                        notify_user(user, acc_id, "未找到登录凭证")
                        continue

                    ltp = LTP(ecs_token=ecs_token, phone=phone)
                    ok, msg = ltp.check_validity()
                    ltp.close()

                    if not ok:
                        if not _try_auto_relogin(acc_id):
                            if "CK已失效" in msg:
                                notify_user(user, acc_id, "登录凭证已过期且自动刷新失败，请重新登录")
                            else:
                                print(f"定时检测账号 {acc_id} 失败(不推送): {msg}")
                        continue

                    auth_time = '2099-12-31'
                    if not auth_time or auth_time <= today_str:
                        notify_user(user, acc_id, "授权已过期，请及时续费")
                except Exception as e:
                    print(f"处理账号 {acc_id} 出错: {str(e)}")
                    continue

    except Exception as e:
            print(f"定时任务出错: {str(e)}")
    finally:
        cleanup_resources()

notified_accounts = set()
def notify_user(user, account, message):
    """发送用户通知"""
    try:
        if account in notified_accounts:
            return
        phone = sg.bucketGet('yuhua_zglt_phone', account) or "未知"
        phone_mask = phone[:3] + "****" + phone[-4:] if len(phone) >= 7 else phone
        notify_msg = f"""
=====联通通知=====
🤪 账号: {phone_mask}
📢 消息: {message}
=================="""
        sg.push('qq', '', user, '', notify_msg)
        sg.push('qb', '', user, '', notify_msg)
        sg.push('wx', '', user, '', notify_msg)
        sg.push('gw', '', user, '', notify_msg)
        sg.push('sb', '', user, '', notify_msg)
        sg.push('wb', '', user, '', notify_msg)
        sg.push('tg', '', user, '', notify_msg)
        sg.push('tb', '', user, '', notify_msg)
        sg.push('qx', '', user, '', notify_msg)
        sg.push('xy', '', user, '', notify_msg)
        sg.push('ip', '', user, '', notify_msg)
        notified_accounts.add(account)
    except Exception as e:
        print(f"发送通知失败: {str(e)}")


def _perform_maintenance_check() -> bool:
    url = "https://yuhualhh.250666.xyz/shouquan"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache"
    }
    for attempt in range(3):
        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=(5, 10),
                verify=True,
                allow_redirects=True,
                proxies={"http": None, "https": None}
            )
            response.raise_for_status()
            response.encoding = 'UTF-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            content_div = soup.find('div', class_='note-content')
            if content_div:
                return "服务正常中" in content_div.get_text(strip=True)
            return any("服务正常中" in tag.get_text() for tag in soup.find_all(['div', 'p']))
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            if attempt < 2:
                time.sleep(2)
                continue
            return False
        except Exception:
            if attempt < 2:
                time.sleep(2)
                continue
            return False
    return False
def check_maintenance_page() -> bool:
    import os, base64, hashlib, json
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    cache_bucket = "time"
    cache_key = "status_cache"
    ttl_seconds = 1 * 3600
    try:
        salt = b'\x8a\x9b\x1f\xe3\x7d\x4c\x5b\x6a\x01\x23\x45\x67\x89\xab\xcd\xef'
        identifier = "yuhua888"
        key = hashlib.sha256(salt + identifier.encode('utf-8')).digest()
        aesgcm = AESGCM(key)
        cached_data_str = sg.bucketGet(cache_bucket, cache_key)
        if cached_data_str:
            decoded_data = base64.b64decode(cached_data_str.encode('utf-8'))
            nonce = decoded_data[:12]
            ciphertext = decoded_data[12:]
            decrypted_bytes = aesgcm.decrypt(nonce, ciphertext, None)
            cached_data = json.loads(decrypted_bytes.decode('utf-8'))
            if (time.time() - cached_data.get("timestamp", 0)) < ttl_seconds and cached_data.get("status") is True:
                return True
    except Exception:
        pass
    live_status = _perform_maintenance_check()
    new_cache_payload = {
        "status": live_status,
        "timestamp": time.time()
    }
    try:
        salt = b'\x8a\x9b\x1f\xe3\x7d\x4c\x5b\x6a\x01\x23\x45\x67\x89\xab\xcd\xef'
        identifier = "yuhua888"
        key = hashlib.sha256(salt + identifier.encode('utf-8')).digest()
        aesgcm = AESGCM(key)
        nonce = os.urandom(12)
        plaintext = json.dumps(new_cache_payload).encode('utf-8')
        ciphertext = aesgcm.encrypt(nonce, plaintext, None)
        base64.b64encode(nonce + ciphertext).decode('utf-8')
        True
    except Exception as e:
        pass
    return live_status
def main():
    """主函数"""
    try:
        if not check_maintenance_page():
            sender.reply("❌ 服务端无法连通, 插件停止运行")
            return
        message = sender.getMessage().strip()
        if '登录' in message:
            login()
        elif '管理' in message:
            manage_account()
        elif '查询' in message:
            query_account()
        elif message == '联通清理':
            clean_expired()
        elif message == '联通授权':
            if not sender.isAdmin():
                sender.reply("❌ 需要管理员权限")
                return
            admin_auth()
        elif message == '联通检测':
            if not sender.isAdmin():
                sender.reply("❌ 需要管理员权限")
                return
            sender.reply("正在检测....")
            cron_task()
            sender.reply("✅ 已执行联通检测推送任务")
        else:
            sender.setContinue()
    except Exception as e:
        sender.reply(f"❌ 运行出错: {str(e)}")

if __name__ == "__main__":
    try:
        manage_cmd, query_cmd, login_cmd, price, bingfa, yuhua_zglt_qlname, yuhua_zglt_osname, aiting_var = get_config()
        today = str(datetime.now().date())
        if imtype == 'fake':
            pass
        else:
            main()
    except Exception as e:
        sender.reply(f"❌ 运行出错: {str(e)}")
