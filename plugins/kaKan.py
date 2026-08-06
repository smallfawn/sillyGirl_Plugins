# [title: 卡看]
# [name: kaKan]
# [language: python]
# [class: 任务]
# [author: dandan8]
# [version: v1.0.2]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^卡看(教程|登录|管理|查询|刷进度)$]
# [icon: https://api.iconify.design/lucide:apple.svg]
# [description: 卡看账号登录、查询、进度任务、面板同步与管理]
# [depe: ["pycryptodome","requests","urllib3"]]
import asyncio as _sg_asyncio
import os as _sg_os
import time as _sg_time
import types as _sg_types
import json as _sg_json
from threading import Thread as _sg_Thread
from sillygirl import Adapter as _SGAdapter, Bucket as _SGBucket, Sender as _SGSender, sender as _sg_sender, plugin
try: import ast as _sg_ast
except Exception: _sg_ast=None

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
    'dd_kakan_config_Qinglong': plugin.Form.string().title('青龙面板配置').default('').description('青龙面板地址、应用ID、应用密钥，用中文丨分隔'),
    'dd_kakan_config_env_name': plugin.Form.string().title('青龙变量名').default('').description('青龙容器内卡看的环境变量名'),
    'dd_kakan_config_admin_ids': plugin.Form.string().title('管理员ID列表').default('').description('管理员ID，逗号分隔'),
    'dd_kakan_config_proxy_url': plugin.Form.string().title('代理提取链接').default('').description('查询时使用的代理提取链接，不填则不使用代理'),
})
_CONFIG_FIELD_MAP = {
    ('dd_kakan_config', 'Qinglong'): 'dd_kakan_config_Qinglong',
    ('dd_kakan_config', 'env_name'): 'dd_kakan_config_env_name',
    ('dd_kakan_config', 'admin_ids'): 'dd_kakan_config_admin_ids',
    ('dd_kakan_config', 'proxy_url'): 'dd_kakan_config_proxy_url',
}

"""
卡看插件 - 青龙面板对接版本
支持账号管理、查询、进度任务和青龙同步
任务在青龙中执行，插件只负责账号管理
"""

import requests
import json
import time
import random
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
from urllib.parse import quote_plus, urlparse, parse_qs, unquote
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print('卡看助手 v1.0.0 加载中...')

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()
username = sender.getUserName() or "未知用户"

CANCEL_KEY = 'q'
TOKEN_CACHE_TIME = 23 * 3600
DEFAULT_COIN_BUCKET = 'dd_sign_points'

RSA_PRIVATE_KEY_B64 = "MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCWLxnotIP3pNK4Vb/MEvm205lz1gRyFuXS0Td1v2cDfkJibxwWBRGtkP5LjmhxH/6TuFaoKGrEqBKqpfNuMcOG8l6FRTO7XgqMr6QfCb47I/FHsg3j4UNGy8cMzA3Ei/PpM9SxeTImIclvJ7zBXlJZjQyZ8jMClEfm+AnzXb4dXJe/tjd+iLnms15+2T2HjOCI9+EsBdbtHZ482F/G+nO1OL7J2/MmEkwnjhm+WcXm3fu5MjXIUHBKL11vYMYSvIh0+w0xI85hDiuz1Q6lYS7AdIaEGWtA0wfGT0iYQNQc+cDU3Ev9PMyTowdfOeTcnfwq6+BkOcW0AwZOzPQA++8BAgMBAAECggEAK0X0FbCZy8vSqamPg5o+GJdcwls62bLOUtHUxJk7ce656wnv0kpwnw3Fr/ifEGVzIZY+ZeKLbRGumzwI6cnt+F6yrHzVnJnKuWHMjOLuTLUdCxb7WJtqGqaRupa7KtRWme3EzcRJlmIq29vbz+3BFauGI399gjM+iocSuuxaYLQBenDu0xlI2a3bYH4zxV8kJ4pKc4qu+jmM84csc/sFoGkEFOQ5im6TJubNQ+PVdHSpSAitR/E7Sq57Nyw5IFkbZxX5R0XequX8f4XDt6lOmg5dBu/mouBMEPhGvnbY/5YpD0TGTi1BcAWWbMDjqhHX6L0WV/e1bQqwlBK5faO8pwKBgQDTBYW5AJfLVRcv6UJNPD5U5+stDTy2FGdZaaEW+AytbPT6xkDl8MVoey6zV5G6gDn8wOGwhW3YoJCchwT34jCR9rYlhCIxRRX7aaRAzqyiXM7B3ZACLVSfaCkiPA/7tYAlReaKKOIRXRVlmRKy5KKvEHzqkIPAGc6Z/e2ZmgD3AwKBgQC2MfOUa29DAEc9s8QXwc0hvAIRgjPjTn/8KNUQyhwVSRb5Xj/GRuAMII4dUGsKR1DnME4CHixRZhjEJwTeS04BPb2Mgnu9s/Wl7A/pd+3lm8Qzux+uDmP6vmlJe4hsPfm5axPOCAMGI0gq5YM01GiRwPqYIpjuL7UrpXg5wmJQqwKBgFVSDElK5hT+aIukonwb+Y/W3Y2vpnZwNYE/ZjSlQmr0fPDQK/lMqmSeObmllHR11/xL+HSo3ksSUKYZKXcYa075E5iDnleReVvX0OOrLL3RDH/yF4Hp1idFtCv1YPkC37cyVg5SjWU736TeiWLvcp+Z6QfmOn73cENvGhxa2j0FAoGBAITLPaVE9PBZyJMRbnB+Ydwfo0ZNpzIa6i/JNxqopPVis2sIJeWHjQ9pvwtgrNPuDOqki4cBpP2jM5PseKDpNC61aG18QWKQQxAvUZ2yOuPqt4OY9MsxU+/TTvwvHM0AEv7xK5s0vbeAib4yUIJ1+s2ZYUz3ko2wmhT44vr+UhhHAoGBALeia7zaiLQWr5h+X+DQfIaMWX2FrFwx16UXxKPAlTSdrj0UGQDZsG9uk7KIMZVs/LFnasAhflWRwX6gYADssXyPGeeOSWkOk7fTSZduj7KXXKMQYIl5OQ9nnCaqJNVHh/7xt+0avU2DlcUSrjSFxeF4cd6tO/kWcnPlWqp9M9OB"

AES_KEY = b'5d5e2890a7e84598'
AES_IV = b'5d5e2890a7e84598'

BASE_URL = 'https://welfare-user.palmestore.com'
DURATION_URL = 'https://kakan-api.zhangyue.com'
WELFARE_URL = 'https://kakan-welfare.zhangyue.com'

def format_number(num):
    return f"{num:,}"

class SignatureManager:
    _rsa_key = None

    X_SIG_VER = "v1.1"

    DEFAULT_HEADERS = {
        'X-AppId': 'zya3c0e0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'Keep-Alive'
    }

    @staticmethod
    def generate_user_agent(device_info: dict, api_path: str = '', base_url: str = '') -> str:
        android_ver = device_info.get('p22', '15')
        device_model = device_info.get('p16', 'PHK110')
        build_id = device_info.get('build_id', 'AP3A.240617.008')

        if base_url in [DURATION_URL, WELFARE_URL] or api_path.startswith('/taiji_user/'):
            return f"Dalvik/2.1.0 (Linux; U; Android {android_ver}; {device_model} Build/{build_id})"

        channel = device_info.get('p2', '731006')
        app_id = device_info.get('p29', 'zya3c0e0')

        chrome_ver = f"{random.randint(80, 120)}.0.{random.randint(4000, 6000)}.{random.randint(100, 200)}"

        ua = (f"Mozilla/5.0 (Linux; Android {android_ver}; {device_model} Build/V417IR; wv) "
              f"AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/{chrome_ver} "
              f"Mobile Safari/537.36 zyHybridVer/2.3.1 zyApp/kakan zyVersion/1.2.0.1 "
              f"zyChannel/{channel} zyAppid/{app_id}")
        return ua

    @classmethod
    def _get_rsa_key(cls):
        if cls._rsa_key is None:
            cls._rsa_key = RSA.import_key(base64.b64decode(RSA_PRIVATE_KEY_B64))
        return cls._rsa_key

    @staticmethod
    def aes_encrypt(plain_text: str) -> str:
        cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
        padded_data = pad(plain_text.encode('utf-8'), AES.block_size)
        encrypted = cipher.encrypt(padded_data)
        return base64.urlsafe_b64encode(encrypted).decode('ascii').rstrip('=')

    @staticmethod
    def _timestamp_xor_key(timestamp):
        tmp = int(timestamp)
        key = []
        for _ in range(4):
            key.append(tmp % 10)
            tmp //= 10
        return key

    @classmethod
    def make_x_sig_sec(cls, env_info=None, timestamp=None):
        if timestamp is None:
            timestamp = cls.get_timestamp()
        obj = {}
        if env_info is not None:
            obj["ne"] = env_info
        obj["zy"] = "d0"
        plain = json.dumps(obj, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        key = cls._timestamp_xor_key(timestamp)
        raw = bytearray(b"\x00\x01")
        for i, b in enumerate(plain):
            raw.append(b ^ key[i & 3])
        return base64.b64encode(bytes(raw)).decode("ascii")

    @staticmethod
    def build_params_string(params: dict, for_signature: bool = True) -> str:
        sorted_params = sorted(params.items(), key=lambda x: x[0])
        parts = []
        for k, v in sorted_params:
            if v is None or str(v).strip() == "":
                continue
            text = str(v)
            if for_signature:
                text = quote_plus(text, safe="*-._")
            if text.strip() == "":
                continue
            parts.append(f"{k}={text}")
        return "&".join(parts)

    @staticmethod
    def build_origin(post_body: str, query_params, path: str, timestamp: str) -> str:
        if isinstance(query_params, str):
            query_string = query_params
        elif query_params:
            query_string = SignatureManager.build_params_string(query_params, for_signature=True)
        else:
            query_string = ""
        return f"{post_body or ''}&{query_string}&{path}&{timestamp}"

    @classmethod
    def generate_signature(cls, params: dict, timestamp: str, api_path: str, sig_sec: str) -> str:
        params_str = cls.build_params_string(params, for_signature=True)
        origin = cls.build_origin(params_str, {}, api_path, timestamp)
        sign_input = origin.encode("utf-8") + b"&" + sig_sec.encode("utf-8")

        key = cls._get_rsa_key()
        h = SHA256.new(sign_input)
        signature = pkcs1_15.new(key).sign(h)
        return base64.b64encode(signature).decode('utf-8')

    @staticmethod
    def get_timestamp() -> str:
        return str(int(time.time() * 1000))

    @classmethod
    def get_base_url(cls, url: str) -> str:
        if url.startswith(BASE_URL):
            return BASE_URL
        elif url.startswith(WELFARE_URL):
            return WELFARE_URL
        return DURATION_URL

class KaKanAPI:

    def __init__(self):
        self.session = requests.Session()

    def _send_request(self, method: str, url: str, params: dict = None,
                     data: dict = None, extra_headers: dict = None, device_info: dict = None, proxy: dict = None) -> dict:
        base_url = SignatureManager.get_base_url(url)
        sign_path = url.replace(base_url, '')
        request_params = params or data or {}

        timestamp = SignatureManager.get_timestamp()
        sig_sec = SignatureManager.make_x_sig_sec("d0", timestamp)
        signature = SignatureManager.generate_signature(request_params, timestamp, sign_path, sig_sec)

        headers = SignatureManager.DEFAULT_HEADERS.copy()
        if device_info:
            headers['User-Agent'] = SignatureManager.generate_user_agent(device_info, sign_path, base_url)
        headers.update({
            'X-SIG-Sign': signature,
            'X-SIG-Alg': 'RSA-SHA256',
            'X-SIG-Timestamp': timestamp,
            'X-SIG-Ver': SignatureManager.X_SIG_VER,
            'X-SIG-Sec': sig_sec
        })
        if extra_headers:
            headers.update(extra_headers)

        try:
            if method.upper() == 'GET':
                response = self.session.get(url, params=request_params, headers=headers, timeout=20, verify=False, proxies=proxy)
            else:
                params_str = SignatureManager.build_params_string(request_params, for_signature=True)
                response = self.session.post(url, data=params_str, headers=headers, timeout=20, verify=False, proxies=proxy)

            return response.json()
        except Exception as e:
            print(f"API请求异常: {str(e)}")
            return {'code': -1, 'msg': str(e)}

    def _build_common_params(self, device_info: dict, session_info: dict = None) -> dict:
        params = {
            'p1': device_info.get('p1', ''),
            'p16': device_info.get('p16', ''),
            'p2': device_info.get('p2', '731001'),
            'p21': device_info.get('p21', '3'),
            'p22': device_info.get('p22', '13'),
            'p24': device_info.get('p24', '0'),
            'p25': device_info.get('p25', '12030'),
            'p28': device_info.get('p28', ''),
            'p29': device_info.get('p29', 'zya3c0e0'),
            'p3': device_info.get('p3', '101200017'),
            'p31': device_info.get('p31', ''),
            'p33': device_info.get('p33', 'com.zhangyue.app.shortplay.kakandj'),
            'p34': device_info.get('p34', 'navigationbar_is_min'),
            'p4': device_info.get('p4', '501617'),
            'p5': device_info.get('p5', '16'),
            'p7': device_info.get('p7', device_info.get('p28', '')),
            'p9': device_info.get('p9', '2'),
            'pc': device_info.get('pc', '10'),
            'zyeid': device_info.get('zyeid', '')
        }

        if session_info:
            params['usr'] = session_info.get('encrypt_user_id') or session_info.get('user_id', '')
            params['zysid'] = session_info.get('session_id', '')

        return params

    def send_sms_code(self, phone: str, device_info: dict) -> tuple:
        plain_data = json.dumps({'phone': phone}, separators=(',', ':'))
        encrypt_data = SignatureManager.aes_encrypt(plain_data)

        url = f"{DURATION_URL}/taiji_user/sms/sendSms"
        params = self._build_common_params(device_info)
        params.update({
            'app_id': 'zya3c0e0',
            'data': encrypt_data,
            'flag': '1',
            'usr': device_info.get('usr', ''),
            'zyeid': device_info.get('zyeid', '')
        })
        response = self._send_request('POST', url, params=params, device_info=device_info)

        if isinstance(response, dict) and response.get('code') == 0:
            body = response.get('body', {})
            remains = body.get('remains', '未知')
            interval = body.get('interval', '未知')
            return True, remains, interval
        else:
            error_msg = response.get('msg', '未知错误') if isinstance(response, dict) else str(response)
            return False, error_msg, None

    def login_by_phone(self, phone: str, code: str, device_info: dict) -> tuple:
        plain_data = json.dumps({'phone': phone}, separators=(',', ':'))
        encrypt_data = SignatureManager.aes_encrypt(plain_data)

        url = f"{DURATION_URL}/taiji_user/login/loginByPhone"
        params = self._build_common_params(device_info)
        params.update({
            'app_id': 'zya3c0e0',
            'data': encrypt_data,
            'device_no': device_info.get('p1', ''),
            'p_code': code,
            'usr': device_info.get('usr', ''),
            'visitor_id': device_info.get('visitor_id', device_info.get('usr', '')),
            'zyeid': device_info.get('zyeid', '')
        })
        response = self._send_request('POST', url, params=params, device_info=device_info)

        if isinstance(response, dict) and response.get('code') == 0:
            user_info = response.get('body', {})
            return True, user_info
        else:
            error_msg = response.get('msg', '未知错误') if isinstance(response, dict) else str(response)
            return False, {'error': error_msg}

    def get_user_info(self, device_info: dict, session_info: dict, proxy: dict = None) -> tuple:
        params = self._build_common_params(device_info, session_info)

        url = f"{BASE_URL}/api/user/info"
        response = self._send_request('GET', url, params=params, device_info=device_info, proxy=proxy)

        if isinstance(response, dict) and response.get('code') == 0:
            return True, response.get('body', {})
        return False, None

    def get_gold_account(self, device_info: dict, session_info: dict, proxy: dict = None) -> tuple:
        params = self._build_common_params(device_info, session_info)
        params['gold_type'] = '3'

        url = f"{BASE_URL}/api/user/gold_account"
        response = self._send_request('GET', url, params=params, device_info=device_info, proxy=proxy)

        if isinstance(response, dict) and response.get('code') == 0:
            return True, response.get('body', {})
        return False, None

    def get_task_user_info(self, device_info: dict, session_info: dict, task_ids: str = '3119,3801,3014') -> tuple:
        params = self._build_common_params(device_info, session_info)
        params['act_id'] = '1021'
        params['task_ids'] = task_ids

        url = f"{BASE_URL}/api/task/task/user_info/by_user"
        response = self._send_request('GET', url, params=params, device_info=device_info)

        if isinstance(response, dict) and response.get('code') == 0:
            return True, response.get('body', {})
        return False, None

    def get_bind_info(self, device_info: dict, session_info: dict) -> tuple:
        params = self._build_common_params(device_info, session_info)
        params['extract_type'] = '2'

        url = f"{BASE_URL}/api/user/withdraw/schedule"
        response = self._send_request('GET', url, params=params, device_info=device_info)

        if isinstance(response, dict) and response.get('code') == 0:
            body = response.get('body', {})
            bind_info = body.get('bind_info', {})
            return True, bind_info
        return False, None

    def receive_task(self, device_info: dict, session_info: dict, task_id: int,
                     receive_type: str = '4', act_id: int = 1021,
                     sub_task_id: str = None, proxy: dict = None) -> tuple:
        params = self._build_common_params(device_info, session_info)
        params['task_id'] = str(task_id)
        params['receive_type'] = receive_type
        params['act_id'] = str(act_id)
        if sub_task_id:
            params['sub_task_id'] = sub_task_id

        url = f"{BASE_URL}/api/task/task/receive"
        response = self._send_request('POST', url, params=params, device_info=device_info, proxy=proxy)

        if isinstance(response, dict) and response.get('code') == 0:
            return True, response.get('body', {})
        else:
            error_msg = response.get('msg', '未知错误') if isinstance(response, dict) else str(response)
            return False, {'error': error_msg}

    def complete_ad_task(self, device_info: dict, session_info: dict, task_type: int = 106) -> bool:
        params = self._build_common_params(device_info, session_info)
        params['task_type'] = str(task_type)

        url = f"{BASE_URL}/api/task/done"
        response = self._send_request('POST', url, params=params, device_info=device_info)

        if isinstance(response, dict) and response.get('code') == 0:
            return True
        return False

class DeviceManager:

    DEVICE_MODELS = [
        ('PHK110', '15', 'OnePlus', 'PHK110'),
        ('PTP-AN70', '15', 'Huawei', '23117RK66C'),
        ('VOG-AL00', '12', 'Huawei', 'VOG-AL00'),
        ('ELE-AL00', '11', 'Huawei', 'ELE-AL00'),
        ('SEA-AL10', '10', 'Huawei', 'SEA-AL10'),
        ('PAR-AL00', '9', 'Huawei', 'PAR-AL00'),
        ('Redmi K50', '12', 'Xiaomi', '22041211AC'),
        ('Redmi Note 11', '11', 'Xiaomi', '2201117TI'),
        ('OPPO Find X', '11', 'OPPO', 'PAFM00'),
        ('vivo X80', '12', 'vivo', 'V2145A'),
        ('OnePlus 9', '11', 'OnePlus', 'LE2110'),
    ]

    NAV_PROPS = ['navigationbar_is_min', 'force_fsg_nav_bar', 'notch']

    @staticmethod
    def generate_shumei_id() -> str:
        p35_bytes = bytes([random.choice([0x06, 0x07])])
        p35_bytes += bytes([random.randint(0, 255) for _ in range(16)])
        p35_bytes += bytes([random.randint(0, 255) for _ in range(48)])
        return base64.b64encode(p35_bytes).decode('utf-8')

    @staticmethod
    def generate_p28() -> str:
        prefix = ''.join(random.choices('0123456789ABCDEF', k=32))
        suffix = ''.join(random.choices('0123456789abcdef', k=32))
        return prefix + suffix

    @staticmethod
    def generate_oaid() -> str:
        return ''.join(random.choices('0123456789abcdef', k=16))

    @staticmethod
    def generate_imei() -> str:
        return ''.join(random.choices('0123456789', k=15))

    @staticmethod
    def generate_android_id() -> str:
        return ''.join(random.choices('0123456789abcdef', k=16))

    @staticmethod
    def generate_device_info(url_params: dict = None, phone: str = None) -> dict:
        seed = ''.join(random.choices('0123456789abcdef', k=32))
        android_release = random.choice(["12", "13", "14"])
        model = random.choice(["Pixel6", "Pixel7", "Mi10", "V2241A", "PDEM30"])
        build_id = ''.join(random.choices('0123456789ABCDEF', k=8))
        oaid = ''.join(random.choices('0123456789abcdef', k=32))
        android_id = ''.join(random.choices('0123456789abcdef', k=16))
        visitor_id = "tj" + ''.join(random.choices('0123456789', k=16))
        p1 = str(int(time.time() * 1000)) + ''.join(random.choices('0123456789', k=6))

        device_info = {
            'p1': p1,
            'p16': model,
            'p31': android_id,
            'p28': oaid,
            'p2': '731001',
            'p21': '3',
            'p22': android_release,
            'p24': '0',
            'p25': '12030',
            'p29': 'zya3c0e0',
            'p3': '101200017',
            'p33': 'com.zhangyue.app.shortplay.kakandj',
            'p34': 'navigationbar_is_min',
            'p4': '501617',
            'p5': '16',
            'p7': oaid,
            'p9': '2',
            'pc': '10',
            'build_id': build_id,
            'brand': 'Google',
            'device': model,
            'model': model,
            'product': model.lower(),
            'manufacturer': 'Google',
            'android_version': android_release,
            'network_type': '3',
            'sim_type': '2',
            'device_info_prop': 'navigationbar_is_min',
            'lang': 'zh_CN',
            'timezone': 'Asia/Shanghai',
            'oaid': oaid,
            'android_id': android_id,
            'usr': visitor_id,
            'visitor_id': visitor_id,
            'zyeid': hashlib.md5(seed.encode('ascii')).hexdigest(),
            'user_agent': f"Dalvik/2.1.0 (Linux; U; Android {android_release}; {model} Build/{build_id})",
            'createTime': time.strftime('%Y-%m-%d %H:%M:%S')
        }

        if url_params:
            for key, value in url_params.items():
                device_info[key] = value

        if phone:
            if 'usr' not in device_info or not device_info.get('usr'):
                device_info['usr'] = visitor_id
            if 'zyeid' not in device_info or not device_info.get('zyeid'):
                device_info['zyeid'] = hashlib.md5(seed.encode('ascii')).hexdigest()
            if 'zysid' not in device_info or not device_info.get('zysid'):
                device_info['zysid'] = ''.join(random.choices('0123456789abcdef', k=32))

        return device_info

    @staticmethod
    def parse_url_params(url: str) -> dict:
        try:
            parsed = urlparse(url.strip())
            params = parse_qs(parsed.query)

            extracted = {}
            for key, values in params.items():
                extracted[key] = unquote(values[0])

            return extracted
        except:
            return {}

_proxy_cache = {'proxy': None, 'expire_time': 0, 'info': '本地'}

def get_proxy(proxy_url: str) -> tuple:

    if not proxy_url:
        return {}, '本地'

    if _proxy_cache['proxy'] and time.time() < _proxy_cache['expire_time']:
        return _proxy_cache['proxy'], _proxy_cache['info']

    try:
        response = requests.get(proxy_url, timeout=10)
        proxy_text = response.text.strip()

        if ':' in proxy_text:
            parts = proxy_text.split(':')
            if len(parts) >= 2:
                host = parts[0]
                port = parts[1]
                proxy = {
                    'http': f'http://{host}:{port}',
                    'https': f'http://{host}:{port}'
                }
                proxy_info = f"{host}:{port}"
                _proxy_cache['proxy'] = proxy
                _proxy_cache['expire_time'] = time.time() + 55
                _proxy_cache['info'] = proxy_info
                print(f"✅ 获取代理成功: {host}:{port}")
                return proxy, proxy_info
    except Exception as e:
        print(f"⚠️ 获取代理失败: {str(e)}")

    return {}, '本地'

def get_plugin_config():
    raw=sg.bucketGet('dd_kakan_config','Qinglong') or ''
    parts=[x.strip() for x in raw.split('丨')]
    if len(parts)!=3 or not all(parts):
        sender.reply('❌ 请配置青龙面板：Host丨ClientID丨ClientSecret')
        raise SystemExit
    if not parts[0].startswith(('http://','https://')):
        sender.reply('❌ 青龙地址格式错误')
        raise SystemExit
    return (*parts,sg.bucketGet('dd_kakan_config','env_name') or 'kakan',sg.bucketGet('dd_kakan_config','proxy_url') or '')

class QingLongAPI:

    def __init__(self, base_url: str, client_id: str, client_secret: str):
        self.base_url = base_url.rstrip('/')
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None
        self.token_expire_time = 0

    def _get_token(self):
        try:
            if self.token and time.time() < self.token_expire_time:
                return self.token

            url = f"{self.base_url}/open/auth/token"
            params = {
                'client_id': self.client_id,
                'client_secret': self.client_secret
            }

            response = requests.get(url, params=params, timeout=10)
            result = response.json()

            if result.get('code') == 200:
                self.token = result['data']['token']
                self.token_expire_time = time.time() + TOKEN_CACHE_TIME
                return self.token
            else:
                print(f"获取token失败: {result.get('message', '未知错误')}")
                return None

        except Exception as e:
            print(f"获取token异常: {str(e)}")
            return None

    def _request(self, method: str, endpoint: str, data=None, params=None):
        token = self._get_token()
        if not token:
            return None

        try:
            url = f"{self.base_url}/open/{endpoint}"
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            response = None
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=30)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=data, timeout=30)
            elif method.upper() == 'PUT':
                response = requests.put(url, headers=headers, json=data, timeout=30)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=headers, json=data, timeout=30)
            else:
                return None

            result = response.json()
            return result if result.get('code') == 200 else None

        except Exception as e:
            print(f"API请求异常: {str(e)}")
            return None

    def get_envs(self, search_value=None):
        params = {}
        if search_value:
            params['searchValue'] = search_value

        result = self._request('GET', 'envs', params=params)
        if result and result.get('data'):
            return result['data']
        return []

    def find_env_by_remark(self, env_name: str, remark: str):
        envs = self.get_envs(search_value=env_name)
        for env in envs:
            if env.get('name') == env_name:
                remarks = env.get('remarks', '')
                if f'卡看:{remark}丨' in remarks or f'备注:{remark}' in remarks:
                    return env
        return None

    def add_env(self, name: str, value: str, remarks: str = '') -> bool:
        data = [{
            'name': name,
            'value': value,
            'remarks': remarks
        }]
        result = self._request('POST', 'envs', data=data)
        return result is not None

    def update_env(self, env_id: int, name: str, value: str, remarks: str = '') -> bool:
        data = {
            'id': env_id,
            'name': name,
            'value': value,
            'remarks': remarks
        }
        result = self._request('PUT', 'envs', data=data)
        return result is not None

    def delete_env(self, env_ids: list) -> bool:
        result = self._request('DELETE', 'envs', data=env_ids)
        return result is not None

    def disable_env(self, env_ids: list) -> bool:
        result = self._request('PUT', 'envs/disable', data=env_ids)
        return result is not None

    def enable_env(self, env_ids: list) -> bool:
        result = self._request('PUT', 'envs/enable', data=env_ids)
        return result is not None

def get_user_accounts(user_id: str) -> list:
    uservalue = sg.bucketGet(bucket='dd_kakan_user', key=user_id)
    if uservalue:
        try:
            return _sg_literal(uservalue)
        except:
            return []
    return []

def save_user_accounts(user_id: str, accounts: list):
    if accounts:
        sg.bucketSet(bucket='dd_kakan_user', key=user_id, value=str(accounts))
    else:
        sg.bucketDel(bucket='dd_kakan_user', key=user_id)

def get_account_data(remark: str) -> dict:
    data = sg.bucketGet(bucket='dd_kakan_token', key=remark)
    if data:
        try:
            return json.loads(data)
        except:
            return None
    return None

def save_account_data(remark: str, value: dict):
    sg.bucketSet(bucket='dd_kakan_token', key=remark, value=json.dumps(value, ensure_ascii=False))

def delete_account_data(remark: str):
    sg.bucketDel(bucket='dd_kakan_token', key=remark)
    True



def get_unique_remark(base_remark: str, user_id: str) -> str:
    user_accounts = get_user_accounts(user_id)

    if base_remark not in user_accounts:
        existing_data = get_account_data(base_remark)
        if existing_data is None:
            return base_remark

    counter = 1
    while True:
        new_remark = f"{base_remark}_{counter}"
        if new_remark not in user_accounts:
            existing_data = get_account_data(new_remark)
            if existing_data is None:
                return new_remark
        counter += 1
        if counter > 100:
            return f"{base_remark}_{int(time.time())}"

def sync_to_qinglong(api, env_name, remark, account_data, user_id):
    value=json.dumps(account_data,ensure_ascii=False)
    remarks=f'卡看:{remark}丨用户:{user_id}'
    old=api.find_env_by_remark(env_name,remark)
    if old:
        env_id=old.get('id');ok=api.update_env(env_id,env_name,value,remarks)
        if ok:api.enable_env([env_id])
        return ok
    return api.add_env(env_name,value,remarks)



def parse_batch_selection(input_str: str, max_count: int) -> list:
    input_str = input_str.strip()

    if input_str == '0':
        return list(range(max_count))

    indices = set()

    if '-' in input_str and ',' not in input_str:
        try:
            parts = input_str.split('-')
            if len(parts) == 2:
                start = int(parts[0].strip())
                end = int(parts[1].strip())
                for i in range(start, end + 1):
                    if 1 <= i <= max_count:
                        indices.add(i - 1)
        except:
            pass
    else:
        try:
            for item in input_str.replace('，', ',').split(','):
                item = item.strip()
                if '-' in item:
                    parts = item.split('-')
                    if len(parts) == 2:
                        start = int(parts[0].strip())
                        end = int(parts[1].strip())
                        for i in range(start, end + 1):
                            if 1 <= i <= max_count:
                                indices.add(i - 1)
                elif item:
                    idx = int(item)
                    if 1 <= idx <= max_count:
                        indices.add(idx - 1)
        except:
            pass

    return sorted(list(indices))

def cmd_help():
    sender.reply('=====卡看教程=====\n卡看登录：短信验证码登录\n卡看查询：查询金币与余额\n卡看管理：同步或删除账号\n卡看刷进度：执行攒钱罐任务\n==================')

def mask_phone(phone: str) -> str:
    if len(phone) == 11:
        return f"{phone[:3]}****{phone[7:]}"
    return phone[:3] + "****" + phone[-4:] if len(phone) > 7 else phone

def cmd_login():
    sender.reply('请输入手机号；q 退出')
    phone=(sender.input(180000,1000,False) or '').strip()
    if phone.lower()=='q':return
    if len(phone)!=11 or not phone.isdigit():
        sender.reply('❌ 手机号格式错误')
        return
    url,cid,secret,env_name,_=get_plugin_config();api=KaKanAPI();device=DeviceManager.generate_device_info(phone=phone)
    ok,result,_=api.send_sms_code(phone,device)
    if not ok:
        sender.reply(f'❌ 验证码发送失败：{result}')
        return
    sender.reply('验证码已发送，请输入验证码')
    code=(sender.input(60000,5000,False) or '').strip()
    if not code or code.lower()=='q':return
    ok,user=api.login_by_phone(phone,code,device)
    if not ok or not user:
        sender.reply(f'❌ 登录失败：{user.get("error","未知错误") if isinstance(user,dict) else user}')
        return
    device['usr']=user.get('user_id',device.get('usr',''));device.update({k:user[k] for k in ('zyeid',) if k in user})
    remark=get_unique_remark(mask_phone(phone),userid)
    data={'user_id':user.get('user_id'),'encrypt_user_id':user.get('encrypt_user_id'),'session_id':user.get('session_id'),'device_info':device,'name':user.get('name',''),'login_time':time.strftime('%Y-%m-%d %H:%M:%S'),'login_type':'sms'}
    save_account_data(remark,data);accounts=get_user_accounts(userid)
    if remark not in accounts:accounts.append(remark);save_user_accounts(userid,accounts)
    synced=sync_to_qinglong(QingLongAPI(url,cid,secret),env_name,remark,data,userid)
    sender.reply(f'✅ {remark} 登录成功；面板'+('已同步' if synced else '同步失败'))

def cmd_manage():
    accounts=get_user_accounts(userid)
    if not accounts:
        sender.reply('❌ 暂无账号，请先发送 卡看登录')
        return
    sender.reply('=====卡看管理=====\n'+'\n'.join(f'[{i}] {a}' for i,a in enumerate(accounts,1))+'\n回复序号；q退出')
    choice=sender.input(120000,5000,False)
    if not str(choice).isdigit():return
    i=int(choice)-1
    if i not in range(len(accounts)):return
    remark=accounts[i];data=get_account_data(remark)
    sender.reply('[1] 同步面板 [2] 查看配置 [3] 删除账号')
    action=sender.input(120000,5000,False)
    url,cid,secret,env_name,_=get_plugin_config();api=QingLongAPI(url,cid,secret)
    if action=='1':sender.reply('✅ 同步成功' if data and sync_to_qinglong(api,env_name,remark,data,userid) else '❌ 同步失败')
    elif action=='2':sender.reply(json.dumps(data,ensure_ascii=False) if data else '❌ 数据不存在')
    elif action=='3':
        sender.reply('确认删除请回复 y')
        if (sender.input(60000,5000,False) or '').lower()=='y':
            old=api.find_env_by_remark(env_name,remark)
            if old:api.delete_env([old.get('id')])
            accounts.remove(remark);save_user_accounts(userid,accounts);delete_account_data(remark);sender.reply('✅ 已删除')











def cmd_query():
    accounts=get_user_accounts(userid)
    if not accounts:
        sender.reply('❌ 暂无账号，请先发送 卡看登录')
        return
    selected=accounts
    if len(accounts)>1:
        sender.reply('=====卡看查询=====\n'+'\n'.join(f'[{i}] {a}' for i,a in enumerate(accounts,1))+'\n[0] 全部')
        choice=sender.input(120000,5000,False)
        indexes=parse_batch_selection(choice,len(accounts))
        if not indexes:return
        selected=[accounts[i] for i in indexes]
    *_,proxy_url=get_plugin_config();proxy,proxy_info=get_proxy(proxy_url);api=KaKanAPI();results=[]
    for remark in selected:
        data=get_account_data(remark) or {};device=data.get('device_info',{});session={k:data.get(k) for k in ('user_id','encrypt_user_id','session_id')}
        ok,user=api.get_user_info(device,session,proxy=proxy)
        if not ok:
            results.append(f'❌ {remark}: 登录失效');continue
        _,gold=api.get_gold_account(device,session,proxy=proxy)
        results.append(f'📱 {remark}\n💰 金币: {format_number((user or {}).get("total_coin",0))}\n💵 余额: {(user or {}).get("total_cash",0)}元\n🎯 金币账户: {format_number((gold or {}).get("total_gold_num",0))}')
    sender.reply('=====查询结果=====\n'+'\n------------------\n'.join(results)+f'\n🌐 代理: {proxy_info}')

def execute_single_account_progress(kakan_api, remark, count, proxy):
    data=get_account_data(remark) or {};device=data.get('device_info',{});session={k:data.get(k) for k in ('user_id','encrypt_user_id','session_id')}
    if not device or not session.get('session_id'):return {'remark':remark,'success':False,'msg':'账号数据缺失'}
    success=0;last=''
    for i in range(count):
        try:
            ok,result=kakan_api.receive_task(device,session,task_id=3812,receive_type='4',act_id=1021,proxy=proxy)
            success+=int(ok)
            if not ok:last=(result or {}).get('error','执行失败')
            if i<count-1:time.sleep(random.uniform(2,4))
        except Exception as e:last=str(e)
    return {'remark':remark,'success':success>0,'success_count':success,'fail_count':count-success,'total':count,'msg':last}

def cmd_progress():
    accounts=get_user_accounts(userid)
    if not accounts:
        sender.reply('❌ 暂无账号')
        return
    sender.reply('选择账号序号（0=全部）：\n'+'\n'.join(f'[{i}] {a}' for i,a in enumerate(accounts,1)))
    indexes=parse_batch_selection(sender.input(120000,5000,False),len(accounts))
    if not indexes:return
    selected=[accounts[i] for i in indexes]
    sender.reply('请输入次数（1-100）')
    try:count=int(sender.input(120000,5000,False))
    except:return
    if count not in range(1,101):return
    *_,proxy_url=get_plugin_config();proxy,_=get_proxy(proxy_url);api=KaKanAPI()
    with ThreadPoolExecutor(max_workers=min(10,len(selected))) as pool:
        futures=[pool.submit(execute_single_account_progress,api,a,count,proxy) for a in selected]
        for f in as_completed(futures):
            r=f.result();sender.reply(f'{"✅" if r["success"] else "❌"} {r["remark"]}: {r.get("success_count",0)}/{r.get("total",count)} {r.get("msg","")}')

msg = sender.getMessage()

if '卡看教程' in msg:
    cmd_help()
elif '卡看登录' in msg:
    cmd_login()
elif '卡看查询' in msg:
    cmd_query()
elif '卡看管理' in msg:
    cmd_manage()
elif '卡看刷进度' in msg:
    cmd_progress()
else:
    sender.reply("❌ 未知指令\n💡 发送'卡看教程'查看使用说明")
