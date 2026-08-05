# [title: 牛卡福司机]
# [name: niuKaFuSiJi]
# [language: python]
# [class: 任务]
# [author: rujingxianghai]
# [version: v3.5]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(牛卡福|nkf)(登录|登陆)$|^登(录|陆)(牛卡福|nkf)$|^(牛卡福|nkf)(查询|管理|检测|教程|一键更新)$]
# [cron: 0 8 * * *]
# [icon: https://api.iconify.design/lucide:apple.svg]
# [description: 牛卡福插件v3；兼容青龙与呆呆面板；短信验证码登录 + 滑块识别]
# [depe: ["pycryptodome","requests"]]


import asyncio as _sg_asyncio, os as _sg_os, time as _sg_time, types as _sg_types, json as _sg_json, re as _sg_re, urllib.parse as _sg_urlparse
from threading import Thread as _sg_Thread
from sillygirl import Adapter as _SGAdapter, Bucket as _SGBucket, Sender as _SGSender, sender as _sg_sender, container as _sg_container, form
try: import ast as _sg_ast
except Exception: _sg_ast=None
try: import decimal as decimal
except Exception: decimal=None

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
    's_nkfsj_qlname': form.string().title('设置对接容器').default('').description('面板容器参数（兼容青龙与呆呆面板），不填则使用默认配置'),
    's_nkfsj_use_dumbpanel': form.boolean().title('使用DumbPanel').default(False).description('勾选使用DumbPanel面板，不勾选使用青龙面板'),
    's_nkfsj_panel_group': form.string().title('DumbPanel分组').default('').description('填写后新增/更新变量时同步写入group字段，留空则不处理'),
    's_nkfsj_osname': form.string().title('青龙变量名').default('').description('青龙容器内的变量名'),
    's_nkfsj_notify': form.string().title('通知渠道').default('').description('检测通知推送渠道'),
    's_nkfsj_proxy_url': form.string().title('代理地址').default('').description('登录请求代理，支持两种模式：1)API形式(http开头的URL，GET请求返回ip:port文本) 2)代理池形式(直接填写ip:port)'),
    's_nkfsj_rsa_private_key': form.string().title('RSA签名私钥Base64').default('').description('牛卡福接口签名私钥，留空则不执行需要签名的登录请求'),
})
_CONFIG_FIELD_MAP = {
    ('s_nkfsj', 'qlname'): 's_nkfsj_qlname',
    ('s_nkfsj', 'use_dumbpanel'): 's_nkfsj_use_dumbpanel',
    ('s_nkfsj', 'panel_group'): 's_nkfsj_panel_group',
    ('s_nkfsj', 'osname'): 's_nkfsj_osname',
    ('s_nkfsj', 'notify'): 's_nkfsj_notify',
    ('s_nkfsj', 'proxy_url'): 's_nkfsj_proxy_url',
    ('s_nkfsj', 'rsa_private_key'): 's_nkfsj_rsa_private_key',
}

import os
import json
import time
import hashlib
import random
import string
import requests
import base64
import uuid
from datetime import datetime


from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.Cipher import PKCS1_v1_5


SLIDER_API_URL = "https://slider-verification.vzvv.de/solve"


def get_proxy_config():
    """获取代理配置，返回 proxies 字典或 None"""
    proxy_url = sg.bucketGet('s_nkfsj', 'proxy_url') or ''
    proxy_url = proxy_url.strip()
    if not proxy_url:
        return None

    try:
        if proxy_url.lower().startswith('http'):
            resp = requests.get(proxy_url, timeout=10)
            proxy_text = resp.text.strip()
            if not proxy_text or ':' not in proxy_text:
                print(f"代理API返回格式异常: {proxy_text}")
                return None
            proxy_ip_port = proxy_text.splitlines()[0].strip()
            proxy_addr = f"http://{proxy_ip_port}"
        else:
            if ':' not in proxy_url:
                print(f"代理地址格式异常: {proxy_url}")
                return None
            proxy_addr = f"http://{proxy_url}"

        proxies = {
            'http': proxy_addr,
            'https': proxy_addr
        }
        print(f"使用代理: {proxy_addr}")
        return proxies
    except Exception as e:
        print(f"获取代理失败: {e}")
        return None


senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()
uservalue = sg.bucketGet(bucket='s_nkfsj_user', key=userid)

PLUGIN_CONFIG = {'bucket': 's_nkfsj', 'coin_key': 'dd_sign_points', 'name': '牛卡福司机'}


DEVICE_MODELS = [
    "Xiaomi 14 Ultra", "Xiaomi 14 Pro", "Xiaomi 14", "Xiaomi 13 Ultra", "Xiaomi 13 Pro",
    "Xiaomi 12S Ultra", "Xiaomi 12 Pro", "Redmi K70 Pro", "Redmi K60 Pro", "Redmi Note 13 Pro",
    "HUAWEI Mate 60 Pro", "HUAWEI Mate 60", "HUAWEI P60 Pro", "HUAWEI nova 12 Ultra",
    "OPPO Find X7 Ultra", "OPPO Find X6 Pro", "OPPO Reno11 Pro", "OPPO A3 Pro",
    "vivo X100 Pro", "vivo X100", "vivo X90 Pro+", "vivo S18 Pro", "iQOO 12 Pro",
    "HONOR Magic6 Pro", "HONOR Magic5 Pro", "HONOR 100 Pro", "HONOR X50",
    "OnePlus 12", "OnePlus 11", "OnePlus Ace 3",
    "Samsung Galaxy S24 Ultra", "Samsung Galaxy S24+", "Samsung Galaxy S23 Ultra",
    "realme GT5 Pro", "realme GT Neo5", "realme 12 Pro+",
]

def generate_random_device_name():
    """生成随机设备名称"""
    return random.choice(DEVICE_MODELS)


def format_red_envelope_details(records, limit=5):
    """格式化红包明细"""
    if not records:
        return ""

    lines = [f"🧧 红包明细(前{limit}条):"]
    for record in records[:limit]:
        raw_amount = record.get('rewardAmount')
        try:
            amount = f"{float(raw_amount):.2f}"
        except Exception:
            amount = "0.00"

        create_time = record.get('createTime')
        win_date = '未知日期'
        try:
            ts = int(str(create_time))
            if ts > 10 ** 12:
                ts = ts / 1000
            win_date = datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
        except Exception:
            pass

        status_desc = str(record.get('rewardStatusDesc') or '')
        status_raw = str(record.get('rewardStatus') or '')
        arrival_status = '已到' if ('已到账' in status_desc or status_raw == 'DISTRIBUTED') else '未到'

        lines.append(f"🧧 {amount} {win_date} {arrival_status}")

    return "\n".join(lines)


class NucarfAPI:
    """牛卡福司机端API"""

    X_OFFSET = 3

    RSA_PRIVATE_KEY = ""

    AES_KEY = "ef4d4f8e73cc1b84"
    AES_IV = "1234567812345678"

    def __init__(self, device_id=None, device_name=None, use_proxy=False):
        self.base_url = "https://unify-driver.nucarf.net/api"
        self.activity_base_url = "https://driver-activity.nucarf.net/api"
        self.device_id = device_id or self.generate_device_id()
        self.device_name = device_name or generate_random_device_name()
        self.token = None
        self.unify_id = None
        self.proxies = get_proxy_config() if use_proxy else None

    def generate_device_id(self):
        """生成随机设备ID"""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))

    def get_headers(self, use_encrypt=False):
        """获取请求头"""
        common_headers_dict = {
            "ip": "192.168.124.153",
            "deviceid": self.device_id,
            "uid": "",
            "platform": "android",
            "appid": "com.nucarf.member",
            "ver": "5.9.0",
            "lon": 116.397499,
            "lat": 39.908722,
            "network": "wifi",
            "session_id": str(uuid.uuid4()),
            "channel": "xiaomi",
            "url": "",
            "imei": self.device_id,
            "identity": "0",
            "user_agent": "Dalvik/2.1.0 (Linux; U; Android 16; 2210132C Build/BP2A.250605.031.A3)"
        }

        headers = {
            'User-Agent': 'okhttp/3.14.9',
            'Accept-Encoding': 'gzip',
            'common-headers': json.dumps(common_headers_dict, separators=(',', ':')),
            'x-access-token': self.token or '',
            'x-request-id': str(uuid.uuid4()),
            'x-access-token-d': '',
            'token': self.token or '',
            'x-apptype': 'APP',
            'x-appversion': '5.9.0',
            'x-device-id': self.device_id,
            'x-device-type': 'ANDROID',
            'x-device-name': self.device_name,
            'x-device-ip': '192.168.124.153',
            'x-driver-id': '',
            'x-term-id': '24427455',
            'x-driver-unifyid': self.unify_id or '',
            'content-type': 'application/json; charset=UTF-8',
            'Cookie': ''
        }

        if use_encrypt:
            headers['x-app-encrypt'] = 'encryptedData'

        return headers

    def get_simple_headers(self):
        """获取简单请求头（用于密码登录后的接口）"""
        return {
            "X-Request-Id": str(uuid.uuid4()),
            "X-AppType": "APP",
            "X-Device-Id": self.device_id,
            "X-Device-Name": self.device_name,
            "X-Device-Type": "ANDROID",
            "X-AppVersion": "5.9.0",
            "X-Driver-UnifyId": self.unify_id or '',
            "X-Access-Token": self.token or ''
        }

    def encrypt_data_cbc(self, data):
        """使用AES/CBC加密数据（URL-safe Base64）"""
        key = self.AES_KEY.encode('utf-8')
        iv = self.AES_IV.encode('utf-8')

        cipher = AES.new(key, AES.MODE_CBC, iv)
        json_data = json.dumps(data, separators=(',', ':'))
        padded_data = pad(json_data.encode('utf-8'), AES.block_size)
        encrypted = cipher.encrypt(padded_data)

        encrypted_base64 = base64.b64encode(encrypted).decode('utf-8')
        return encrypted_base64.replace('+', '-').replace('/', '_').replace('=', '')

    def decrypt_data_cbc(self, encrypted_str):
        """使用AES/CBC解密数据（URL-safe Base64）"""
        try:
            key = self.AES_KEY.encode('utf-8')
            iv = self.AES_IV.encode('utf-8')

            b64_str = encrypted_str.replace('-', '+').replace('_', '/')
            padding_needed = 4 - (len(b64_str) % 4)
            if padding_needed != 4:
                b64_str += '=' * padding_needed

            encrypted_bytes = base64.b64decode(b64_str)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)
            return json.loads(decrypted.decode('utf-8'))
        except Exception as e:
            print(f"解密失败: {e}")
            return None

    def generate_sign(self, data_md5):
        """生成 RSA 签名"""
        try:
            private_key_text = sg.bucketGet('s_nkfsj', 'rsa_private_key') or self.RSA_PRIVATE_KEY
            if not private_key_text:
                raise ValueError('未配置RSA签名私钥')
            private_key = RSA.import_key(base64.b64decode(private_key_text))
            h = SHA256.new(data_md5.encode('utf-8'))
            signature = pkcs1_15.new(private_key).sign(h)
            signature_base64 = base64.b64encode(signature).decode('utf-8')
            timestamp = int(time.time() * 1000)
            return f"{signature_base64}_{timestamp}"
        except Exception as e:
            print(f"生成签名失败: {e}")
            return None

    def encrypt_aes_ecb(self, data, key):
        """AES ECB PKCS7 加密（标准Base64）"""
        try:
            key_bytes = key.encode('utf-8')
            cipher = AES.new(key_bytes, AES.MODE_ECB)
            padded_data = pad(data.encode('utf-8'), AES.block_size)
            encrypted = cipher.encrypt(padded_data)
            return base64.b64encode(encrypted).decode('utf-8')
        except Exception as e:
            print(f"AES加密异常: {e}")
            return None

    def get_captcha(self):
        """获取滑块验证码"""
        url = f"{self.base_url}/driver/captcha/getCaptcha"
        payload = {
            "clientUid": self.device_id,
            "captchaType": "blockPuzzle",
            "ts": str(int(time.time() * 1000))
        }

        try:
            response = requests.post(url, headers=self.get_headers(), json=payload, proxies=self.proxies, timeout=30)
            result = response.json()
            if result.get('code') == 200:
                return result.get('data')
            return None
        except Exception as e:
            print(f"获取验证码异常: {e}")
            return None

    def solve_captcha(self, bg_base64, slide_base64):
        """使用远程API识别滑块验证码"""
        try:
            resp = requests.post(SLIDER_API_URL, json={
                "bg": bg_base64,
                "slide": slide_base64,
                "offset": self.X_OFFSET
            }, timeout=30, proxies=self.proxies)
            result = resp.json()
            if result.get('success'):
                x = result['data']['x']
                print(f"滑块识别成功: x={x}, 置信度={result['data'].get('confidence', 'N/A')}")
                return x
            else:
                print(f"滑块识别失败: {result.get('error')}")
                return None
        except Exception as e:
            print(f"滑块识别API调用异常: {e}")
            return None

    def check_captcha(self, token, x_pos, secret_key):
        """验证滑块验证码"""
        url = f"{self.base_url}/driver/captcha/checkCaptcha"

        point_data = {"x": float(x_pos), "y": 5.0}
        point_json_str = json.dumps(point_data, separators=(',', ':'))

        encrypted_point_json = self.encrypt_aes_ecb(point_json_str, secret_key)
        if not encrypted_point_json:
            return None

        payload = {
            "clientUid": self.device_id,
            "pointJson": encrypted_point_json,
            "captchaType": "blockPuzzle",
            "token": token
        }

        try:
            response = requests.post(url, headers=self.get_headers(), json=payload, proxies=self.proxies, timeout=30)
            result = response.json()

            if result.get('code') == 200:
                verification_raw = f"{token}---{point_json_str}"
                return self.encrypt_aes_ecb(verification_raw, secret_key)
            return None
        except Exception as e:
            print(f"验证异常: {e}")
            return None

    def send_sms_code(self, mobile, captcha_verification=""):
        """发送短信验证码"""
        url = f"{self.base_url}/driver/app/common/sendSmsCode"

        data = {
            "captchaSource": "1",
            "captchaVerification": captcha_verification,
            "clientUid": self.device_id,
            "codeType": "LOGIN",
            "mobile": mobile
        }

        encrypted_data = self.encrypt_data_cbc(data)
        payload = {"encryptedData": encrypted_data}

        data_md5 = hashlib.md5(encrypted_data.encode('utf-8')).hexdigest()
        sign = self.generate_sign(data_md5)

        headers = self.get_headers(use_encrypt=True)
        headers['sign'] = sign

        try:
            response = requests.post(url, headers=headers, json=payload, proxies=self.proxies, timeout=30)
            return response.json()
        except Exception as e:
            print(f"发送短信异常: {e}")
            return None

    def login_with_sms(self, mobile, sms_code):
        """使用短信验证码登录"""
        url = f"{self.base_url}/driver/app/auth/login"

        data = {
            "deviceIp": "192.168.124.153",
            "deviceType": "ANDROID",
            "loginType": "MOBILE_CODE",
            "username": mobile,
            "verificationCode": sms_code
        }

        encrypted_data = self.encrypt_data_cbc(data)
        payload = {"encryptedData": encrypted_data}

        data_md5 = hashlib.md5(encrypted_data.encode('utf-8')).hexdigest()
        sign = self.generate_sign(data_md5)

        headers = self.get_headers(use_encrypt=True)
        headers['sign'] = sign

        try:
            response = requests.post(url, headers=headers, json=payload, proxies=self.proxies, timeout=30)
            result = response.json()

            if result.get('code') == 200:
                data = result.get('data')
                if isinstance(data, str):
                    data = self.decrypt_data_cbc(data)

                if data:
                    self.token = data.get('token')
                    self.unify_id = data.get('unifyId')
                    return True, data, "登录成功"

            return False, None, result.get('message', '登录失败')
        except Exception as e:
            return False, None, str(e)

    def get_pub_key(self):
        """获取 RSA 公钥"""
        url = f"{self.base_url}/driver/app/unify/common/getPubKey"
        try:
            response = requests.get(url, proxies=self.proxies, timeout=30)
            data = response.json()
            if data['code'] == 200:
                return data['data']['pubKeyId'], data['data']['pubKey']
            return None, None
        except Exception as e:
            print(f"获取公钥异常: {e}")
            return None, None

    def encrypt_password(self, password, pub_key_pem):
        """使用 RSA 公钥加密密码"""
        try:
            key = RSA.importKey(pub_key_pem)
            cipher = PKCS1_v1_5.new(key)
            ciphertext = cipher.encrypt(password.encode('utf-8'))
            return base64.b64encode(ciphertext).decode('utf-8')
        except Exception:
            return None

    def set_password(self, password):
        """设置登录密码（首次设置）"""
        pub_key_id, pub_key = self.get_pub_key()
        if not pub_key:
            return False, "获取公钥失败"

        encrypted_password = self.encrypt_password(password, pub_key)
        if not encrypted_password:
            return False, "密码加密失败"

        url = f"{self.base_url}/driver/app/user/v2/setPassword"
        payload = {
            "password": encrypted_password,
            "pubKeyId": pub_key_id,
            "oldPassword": "NEW_SET_PASSWORD",
            "destroyAllToken": True,
            "setPwdType": "NEW_SET_PASSWORD",
            "force": True
        }

        try:
            response = requests.post(url, headers=self.get_headers(), json=payload, proxies=self.proxies, timeout=30)
            result = response.json()
            if result.get('code') == 200:
                return True, result.get('data', '密码设置成功')
            else:
                return False, result.get('message', '设置密码失败')
        except Exception as e:
            return False, str(e)

    def login_with_password(self, username, password):
        """账密登录"""
        pub_key_id, pub_key = self.get_pub_key()
        if not pub_key:
            return False, None, "获取公钥失败"

        encrypted_password = self.encrypt_password(password, pub_key)
        if not encrypted_password:
            return False, None, "密码加密失败"

        url = f"{self.base_url}/driver/app/auth/login"
        headers = {
            "x-request-id": str(uuid.uuid4()),
            "x-apptype": "APP",
            "x-appversion": "5.9.0",
            "x-device-id": self.device_id,
            "x-device-type": "ANDROID",
            "x-device-name": self.device_name,
            "Content-Type": "application/json"
        }
        payload = {
            "deviceIp": "192.168.124.153",
            "deviceType": "ANDROID",
            "loginType": "MOBILE_PASSWORD",
            "pubKeyId": pub_key_id,
            "username": username,
            "verificationCode": encrypted_password
        }

        try:
            response = requests.post(url, headers=headers, json=payload, proxies=self.proxies, timeout=30)
            data = response.json()
            if data['code'] == 200:
                self.token = data['data']['token']
                self.unify_id = data['data']['unifyId']
                return True, data['data'], "登录成功"
            else:
                return False, None, data.get('message', '登录失败')
        except Exception as e:
            return False, None, str(e)

    def get_points_info(self):
        """获取积分信息"""
        if not self.token or not self.unify_id:
            return None

        url = f"{self.base_url}/points/account/getAccountInfo"
        payload = {
            "unifyId": self.unify_id,
            "platformType": "NUCARF_DRIVER"
        }

        try:
            response = requests.post(url, headers=self.get_simple_headers(), json=payload, proxies=self.proxies, timeout=30)
            data = response.json()
            if data.get('code') == 200 and data.get('data'):
                return data['data'].get('totalPoints', '0')
            return None
        except Exception as e:
            print(f"获取积分异常: {e}")
            return None

    def get_wallet_balance(self):
        """获取钱包余额"""
        if not self.token or not self.unify_id:
            return None

        url = f"{self.base_url}/driver/app/middle/wallet/entrance"

        try:
            response = requests.get(url, headers=self.get_simple_headers(), proxies=self.proxies, timeout=30)
            data = response.json()
            if data.get('code') == 200 and data.get('data'):
                return data['data'].get('walletBalance', '0')
            return None
        except Exception as e:
            print(f"获取余额异常: {e}")
            return None

    def get_red_envelope_records(self, page_no=1, page_size=10):
        """获取红包中奖记录并扁平化返回"""
        if not self.token or not self.unify_id:
            return []

        url = f"{self.activity_base_url}/driver/app/unify/activity/instantgrab/myWinningRecordByActivity"
        payload = {
            "pageNo": page_no,
            "pageSize": page_size
        }

        headers = self.get_simple_headers()
        headers['Content-Type'] = 'application/json'

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=15, proxies=self.proxies)
            data = response.json()
            if data.get('code') != 200:
                return []

            activity_list = data.get('data') or []
            records = []
            for activity in activity_list:
                for record in (activity.get('recordList') or []):
                    records.append(record)
            return records
        except Exception as e:
            print(f"获取红包明细异常: {e}")
            return []


def _get_ql_client():
    """获取面板客户端，根据开关决定使用青龙或DumbPanel"""
    osname = sg.bucketGet('s_nkfsj', 'osname') or 'S_NKF'
    qlname = sg.bucketGet('s_nkfsj', 'qlname') or ''
    use_dp = str(sg.bucketGet('s_nkfsj', 'use_dumbpanel') or '').lower() == 'true'

    if use_dp:
        if qlname:
            return DumbPanelClient(osname, qlname)
        return DumbPanelClient(osname)
    else:
        if qlname:
            return QingLongClient(osname, qlname)
        return QingLongClient(osname)


def _normalize_panel_account_info(username, account_info):
    """兼容字符串/字典两种账号信息，统一提取面板同步所需字段。"""
    if isinstance(account_info, str):
        raw = account_info.strip()
        if not raw:
            return '', '', ''
        if raw.startswith('{'):
            try:
                account_info = json.loads(raw)
            except Exception:
                return '', '', ''
        else:
            parts = raw.split('#')
            if len(parts) >= 3:
                return parts[0].strip() or username, parts[1].strip(), parts[2].strip()
            return username, '', ''

    if not isinstance(account_info, dict):
        return '', '', ''

    phone = (
        account_info.get('phone')
        or account_info.get('mobile')
        or account_info.get('username')
        or username
    )
    token = account_info.get('token') or account_info.get('accessToken') or ''
    unify_id = account_info.get('unifyId') or account_info.get('unify_id') or ''
    return str(phone).strip(), str(token).strip(), str(unify_id).strip()


def update_ql_env(username, account_info):
    """更新青龙环境变量"""
    phone, token, unify_id = _normalize_panel_account_info(username, account_info)
    if not phone or not token or not unify_id:
        return False
    env_value = f"{phone}#{token}#{unify_id}"
    auth_time = '2099-12-31' or '未授权'
    panel_group = (sg.bucketGet('s_nkfsj', 'panel_group') or '').strip()
    ql = _get_ql_client()
    return ql.update_env(
        username,
        env_value,
        f"牛卡福司机:{username}|到期:{auth_time}",
        group=panel_group,
    )


def delete_ql_env(username):
    """删除青龙环境变量"""
    ql = _get_ql_client()
    return ql.delete_env(username)


def bind_account():
    """绑定账号 - 短信验证码登录"""
    sender.reply(
        "=====牛卡福登录=====\n"
        "📱 请输入手机号:\n"
        "------------------\n"
        "回复\"q\"退出操作\n"
        "=================="
    )

    mobile = sender.input(120000, 1, False)
    if not mobile:
        sender.reply("⏰ 操作超时")
        return
    if mobile.lower() == 'q':
        sender.reply("✅ 已取消")
        return

    if not mobile.isdigit() or len(mobile) != 11:
        sender.reply("❌ 手机号格式错误，请输入11位手机号")
        return

    api = NucarfAPI(use_proxy=True)

    sender.reply("🔄 正在发送验证码...")

    res = api.send_sms_code(mobile)

    if not res:
        sender.reply("❌ 请求失败，请稍后重试")
        return

    if res.get('code') == 4001:
        captcha_data = api.get_captcha()
        if not captcha_data:
            sender.reply("❌ 获取验证码失败")
            return

        token = captcha_data.get('token')
        secret_key = captcha_data.get('secretKey')

        x_pos = api.solve_captcha(
            captcha_data.get('originalImageBase64'),
            captcha_data.get('jigsawImageBase64')
        )

        if x_pos is None:
            sender.reply("❌ 滑块识别失败")
            return

        captcha_verification = api.check_captcha(token, x_pos, secret_key)

        if not captcha_verification:
            sender.reply("❌ 滑块验证失败")
            return

        res = api.send_sms_code(mobile, captcha_verification)

        if not res or res.get('code') != 200:
            fail_msg = (res or {}).get('message', '未知错误')
            sender.reply(f"❌ 发送验证码失败: {fail_msg}")
            return

    elif res.get('code') != 200:
        sender.reply(f"❌ 发送验证码失败: {res.get('message', '未知错误')}")
        return

    sender.reply(
        "✅ 验证码已发送\n"
        "📲 请输入短信验证码:\n"
        "------------------\n"
        "回复\"q\"退出\n"
        "=================="
    )

    sms_code = sender.input(120000, 1, False)
    if not sms_code:
        sender.reply("⏰ 操作超时")
        return
    if sms_code.lower() == 'q':
        sender.reply("✅ 已取消")
        return

    sender.reply("🔄 正在登录...")

    success, login_data, msg = api.login_with_sms(mobile, sms_code)

    if not success:
        sender.reply(f"❌ 登录失败: {msg}")
        return

    sender.reply(
        f"✅ 短信登录成功！\n"
        f"📱 手机号: {mask_account(mobile)}\n"
        f"------------------\n"
        f"🔐 是否已设置登录密码？\n"
        f"已设置 → 直接输入密码\n"
        f"需设置 → 回复 y\n"
        f"回复 q 退出\n"
        f"=================="
    )

    pwd_input = sender.input(120000, 1, False)
    if not pwd_input:
        sender.reply("⏰ 操作超时")
        return
    if pwd_input.lower() == 'q':
        sender.reply("✅ 已取消")
        return

    if pwd_input.lower() == 'y':
        sender.reply(
            "🔐 请输入要设置的登录密码：\n"
            "（用于后续脚本自动登录）\n"
            "------------------\n"
            "回复\"q\"退出\n"
            "=================="
        )

        password = sender.input(120000, 1, False)
        if not password:
            sender.reply("⏰ 操作超时")
            return
        if password.lower() == 'q':
            sender.reply("✅ 已取消")
            return

        sender.reply("🔄 正在设置密码...")

        set_success, set_msg = api.set_password(password)
        if not set_success:
            sender.reply(f"❌ 设置密码失败: {set_msg}")
            return

        sender.reply(f"✅ 密码设置成功！")
    else:
        password = pwd_input

    sender.reply("🔄 正在验证密码...")

    verify_api = NucarfAPI(api.device_id, api.device_name, use_proxy=True)
    pwd_success, pwd_data, pwd_msg = verify_api.login_with_password(mobile, password)

    if not pwd_success:
        sender.reply(f"❌ 密码验证失败: {pwd_msg}\n请确保输入的是正确的登录密码")
        return

    current_value = sg.bucketGet('s_nkfsj_user', userid)
    if not current_value:
        sg.bucketSet('s_nkfsj_user', userid, str([mobile]))
    else:
        accounts = _sg_literal(current_value)
        if mobile not in accounts:
            accounts.append(mobile)
            sg.bucketSet('s_nkfsj_user', userid, str(accounts))

    account_info = {
        "phone": mobile,
        "password": password,
        "device_id": verify_api.device_id,
        "device_name": verify_api.device_name,
        "token": verify_api.token,
        "unifyId": verify_api.unify_id
    }
    sg.bucketSet('s_nkfsj_token', mobile, json.dumps(account_info))

    sender.reply(
        f"=====绑定成功=====\n"
        f"📱 账号: {mask_account(mobile)}\n"
        f"🔑 设备ID: {verify_api.device_id[:8]}...\n"
        f"📱 设备名: {verify_api.device_name}\n"
        f"=================="
    )

    dqsj = datetime.now().strftime("%Y-%m-%d")
    accountVip = '2099-12-31'

    if accountVip and accountVip >= dqsj:
        sender.reply(f"📱 {mask_account(mobile)} 已授权，到期: {accountVip}")
        update_ql_env(mobile, account_info)
    else:
        sender.reply(f"\n📋 账号需要授权，发送\"牛卡福管理\"进行授权")


def query_accounts():
    """查询账号信息"""
    if not uservalue:
        sender.reply(f"=====未绑定账号=====\n❌ 未找到账号\n💡 发送 牛卡福登录 绑定\n==================")
        return

    accounts = _sg_literal(uservalue)
    account_list = "\n========选择账号=======\n[0] 全部账号"
    for i, username in enumerate(accounts, 1):
        auth_time = '2099-12-31'
        if not auth_time:
            auth_status = '未授权'
        elif auth_time < str(datetime.now().date()):
            auth_status = '已过期'
        else:
            auth_status = f'到期:{auth_time}'
        account_list += f"\n[{i}]{mask_account(username)}({auth_status})"
    account_list += "\n=====================\n支持多选，用逗号分隔\n回复\"q\"退出\n====================="
    sender.reply(account_list)

    choice = sender.input(120000, 1, False)
    if not choice or choice.lower() == 'q':
        sender.reply("✅ 已退出")
        return

    try:
        if choice == '0':
            selected = accounts.copy()
        else:
            selected = [
                accounts[int(idx.strip()) - 1]
                for idx in choice.split(',')
                if idx.strip().isdigit() and 0 <= int(idx.strip()) - 1 < len(accounts)
            ]

        if not selected:
            sender.reply("❌ 未选择有效账号")
            return

        sender.reply(f"✅ 已选择 {len(selected)} 个账号，正在查询...")

        for i, username in enumerate(selected, 1):
            try:
                account_info = json.loads(sg.bucketGet('s_nkfsj_token', username))
                auth_time = '2099-12-31'

                if auth_time and auth_time >= str(datetime.now().date()):
                    auth_status = '已授权'
                else:
                    auth_status = '未授权'

                api = NucarfAPI(
                    account_info.get('device_id'),
                    account_info.get('device_name'),
                    use_proxy=True
                )
                login_success, _, login_msg = api.login_with_password(
                    account_info.get('phone'),
                    account_info.get('password')
                )

                points = "N/A"
                balance = "N/A"
                red_envelope_text = ""
                "✓" if login_success else "✗"

                if login_success:
                    points = api.get_points_info() or "N/A"
                    balance = api.get_wallet_balance() or "N/A"
                    red_records = api.get_red_envelope_records(page_no=1, page_size=10)
                    red_envelope_text = format_red_envelope_details(red_records, limit=5)

                sender.reply(
                    f"=====账号信息[{i}/{len(selected)}]=====\n"
                    f"📱 账号: {mask_account(username)}\n"
                    f"🏷 授权: {auth_status}\n"
                    f"📅 到期: {auth_time or '未授权'}\n"
                    f"💰 积分: {points}\n"
                    f"💵 余额: {balance} 元\n"
                    f"{red_envelope_text + chr(10) if red_envelope_text else ''}"
                    f"=================="
                )
            except Exception as e:
                sender.reply(f"=====查询失败=====\n❌ 错误: {str(e)}\n==================")

        sender.reply(f"✅ 查询完成")
    except Exception as e:
        sender.reply(f"❌ 查询失败: {str(e)}")


def manage_account():
    """管理账号"""
    if not uservalue:
        sender.reply("=====未绑定账号=====\n❌ 未找到账号\n==================")
        return

    accounts = _sg_literal(uservalue)
    sender.reply(
        "=====账号管理=====\n"
        "[1] 授权账号\n"
        "[2] 删除账号\n"
        "[3] 提交青龙\n"
        "------------------\n"
        "回复数字选择\n"
        "回复\"q\"退出\n"
        "=================="
    )
    choice = sender.input(120000, 1, False)
    if not choice or choice.lower() == 'q':
        sender.reply("✅ 已退出")
        return

    account_list = "\n========选择账号=======\n[0] 全部账号"
    for i, username in enumerate(accounts, 1):
        auth_time = '2099-12-31'
        if not auth_time:
            auth_status = '未授权'
        elif auth_time < str(datetime.now().date()):
            auth_status = '已过期'
        else:
            auth_status = f'到期:{auth_time}'
        account_list += f"\n[{i}]{mask_account(username)}({auth_status})"
    account_list += "\n=====================\n支持多选，用逗号分隔\n回复\"q\"退出\n====================="
    sender.reply(account_list)

    account_choice = sender.input(120000, 1, False)
    if not account_choice or account_choice.lower() == 'q':
        sender.reply("✅ 已退出")
        return

    if account_choice == '0':
        selected = accounts.copy()
    else:
        selected = [
            accounts[int(idx.strip()) - 1]
            for idx in account_choice.split(',')
            if idx.strip().isdigit() and 0 <= int(idx.strip()) - 1 < len(accounts)
        ]

    if not selected:
        sender.reply("❌ 未选择有效账号")
        return

    sender.reply(f"✅ 已选择 {len(selected)} 个账号")

    if choice == '1':
        authorize_multiple_accounts(selected)
    elif choice == '2':
        sender.reply("=====确认删除=====\n⚠️ 此操作不可恢复\n回复 y 确认删除\n==================")
        if sender.input(120000, 1, False).lower() == 'y':
            for username in selected:
                if username in accounts:
                    accounts.remove(username)
                sg.bucketDel('s_nkfsj_token', username)
                True
                delete_ql_env(username)

            if accounts:
                sg.bucketSet('s_nkfsj_user', userid, str(accounts))
            else:
                sg.bucketDel('s_nkfsj_user', userid)
            sender.reply(f"✅ 已删除 {len(selected)} 个账号")
        else:
            sender.reply("✅ 已取消")
    elif choice == '3':
        success = 0
        for username in selected:
            try:
                account_info = json.loads(sg.bucketGet('s_nkfsj_token', username))
                auth_time = '2099-12-31'
                if auth_time and auth_time >= str(datetime.now().date()):
                    if update_ql_env(username, account_info):
                        success += 1
            except:
                pass
        sender.reply(
            f"=====提交结果=====\n"
            f"✅ 成功: {success}个\n"
            f"❌ 失败: {len(selected) - success}个\n"
            f"=================="
        )


def authorize_multiple_accounts(usernames):
    return True


def process_mapay_payment(project, months, money, pay_type='alipay'):
    return True


def process_qrcode_payment(project, months, money):
    return True


def ks_auth():
    return True


def batch_update_tokens():
    """一键更新所有已授权且有密码账号的token和unifyId到青龙变量"""
    if not sender.isAdmin():
        sender.reply("❌ 仅限管理员")
        return

    try:
        all_users = sg.bucketAllKeys('s_nkfsj_user')
        if not all_users:
            sender.reply("❌ 没有找到任何用户(bucketAllKeys返回空)")
            return

        if isinstance(all_users, str):
            all_users = [k.strip() for k in all_users.split(',') if k.strip()]

        total_accounts = 0
        success_count = 0
        fail_count = 0
        skip_no_password = 0
        skip_not_auth = 0

        current_date = str(datetime.now().date())

        accounts_to_update = []
        for raw_user_id in all_users:
            user_id = str(raw_user_id).strip()
            user_accounts_str = sg.bucketGet('s_nkfsj_user', user_id)

            if not user_accounts_str:
                sender.reply(f"⚠️ 用户 {user_id[:8]}... 数据为空(key={repr(raw_user_id)})")
                continue
            try:
                accounts = _sg_literal(user_accounts_str)
            except Exception as e:
                sender.reply(f"⚠️ 用户 {user_id[:8]}... 解析失败: {str(e)[:30]}")
                continue
            if not isinstance(accounts, list):
                sender.reply(f"⚠️ 用户 {user_id[:8]}... 格式错误: {type(accounts)}")
                continue

            for phone in accounts:
                token_data = sg.bucketGet('s_nkfsj_token', phone)
                if not token_data:
                    skip_no_password += 1
                    continue

                try:
                    account_info = json.loads(token_data)
                except Exception:
                    skip_no_password += 1
                    continue

                auth_time = '2099-12-31'

                if not auth_time or auth_time < current_date:
                    skip_not_auth += 1
                    continue

                if not account_info.get('password'):
                    skip_no_password += 1
                    continue

                accounts_to_update.append({
                    'phone': phone,
                    'account_info': account_info
                })
                total_accounts += 1

        if not accounts_to_update:
            sender.reply(
                f"❌ 没有找到符合条件的账号\n"
                f"⏭️ 跳过: {skip_not_auth} 个(未授权/已过期)\n"
                f"⏭️ 跳过: {skip_no_password} 个(无密码/无数据)"
            )
            return

        sender.reply(
            f"📊 找到 {total_accounts} 个已授权账号，开始更新...\n"
            f"⏭️ 跳过: {skip_not_auth} 个(未授权/已过期)"
        )

        for acc in accounts_to_update:
            phone = acc['phone']
            account_info = acc['account_info']

            try:
                api = NucarfAPI(
                    account_info.get('device_id'),
                    account_info.get('device_name'),
                    use_proxy=True
                )
                login_success, _, login_msg = api.login_with_password(
                    phone,
                    account_info.get('password')
                )

                if not login_success:
                    sender.reply(f"❌ {mask_account(phone)} 登录失败: {login_msg}")
                    fail_count += 1
                    continue

                account_info['token'] = api.token
                account_info['unifyId'] = api.unify_id

                sg.bucketSet('s_nkfsj_token', phone, json.dumps(account_info))

                if not update_ql_env(phone, account_info):
                    sender.reply(f"⚠️ {mask_account(phone)} Token更新成功，但青龙同步失败")

                success_count += 1

            except Exception as e:
                sender.reply(f"❌ {mask_account(phone)} 更新异常: {str(e)}")
                fail_count += 1

        sender.reply(
            f"=====更新完成=====\n"
            f"✅ 成功: {success_count} 个\n"
            f"❌ 失败: {fail_count} 个\n"
            f"⏭️ 跳过: {skip_not_auth} 个(未授权/已过期)\n"
            f"⏭️ 跳过: {skip_no_password} 个(无密码)\n"
            f"=================="
        )

    except Exception as e:
        sender.reply(f"❌ 一键更新失败: {str(e)}")


def show_tutorial():
    """显示插件使用教程"""
    tutorial = """
=====牛卡福司机教程=====
📱 用户指令:
• 牛卡福登录 - 短信验证码登录绑定账号
• 牛卡福查询 - 查询账号状态、积分、余额
• 牛卡福管理 - 授权/删除/提交青龙
• 牛卡福教程 - 查看本教程
------------------
🔧 管理员指令:
• 牛卡福授权 - 管理员按天数授权
• 牛卡福检测 - 检测过期账号并清理
• 牛卡福一键更新 - 更新所有账号Token到青龙
------------------
💡 登录说明:
📝 使用短信验证码登录
📝 登录后设置密码用于一键更新Token
📝 青龙变量格式: 手机号#token#unifyId
------------------
📋 功能说明:
🎁 支持抢红包脚本
💰 查询显示积分和余额
==================
"""
    sender.reply(tutorial.strip())


def main():
    """主入口"""
    msg = sender.getMessage()

    if '登录' in msg or '登陆' in msg:
        bind_account()
    elif '教程' in msg and ('牛卡福' in msg or 'nkf' in msg.lower()):
        show_tutorial()
    elif '查询' in msg and ('牛卡福' in msg or 'nkf' in msg.lower()):
        query_accounts()
    elif '管理' in msg and ('牛卡福' in msg or 'nkf' in msg.lower()):
        manage_account()
    elif '牛卡福授权' in msg or 'nkf授权' in msg.lower():
        ks_auth()
    elif '牛卡福一键更新' in msg or 'nkf一键更新' in msg.lower():
        batch_update_tokens()
    elif '牛卡福检测' in msg or 'nkf检测' in msg.lower():
        if not sender.isAdmin():
            sender.reply("❌ 仅限管理员")
            return
        sender.reply("🔍 正在检测...")
        result = check_auth_status('s_nkfsj', 's_nkfsj_user', 's_nkfsj_auth', 's_nkfsj_token', '牛卡福', delete_ql_callback=delete_ql_env)
        sender.reply(result)
    elif sender.getImtype() == 'fake':
        try:
            result = check_auth_status('s_nkfsj', 's_nkfsj_user', 's_nkfsj_auth', 's_nkfsj_token', '牛卡福', delete_ql_callback=delete_ql_env)
            sg.notifyMasters(result)
        except:
            pass
    else:
        sender.setContinue()


if __name__ == "__main__":
    main()
