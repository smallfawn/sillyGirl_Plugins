# [title: 联通云盘]
# [name: lianTongYunPan]
# [language: python]
# [class: 任务]
# [author: sky2022]
# [version: v1.5]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^联通云盘(登录|登陆|查询|管理|后台|教程)$]
# [cron: 0 8 * * *]
# [icon: https://uapis.cn/static/uploads/9b25f4d581_5gbszuxm7Mt8.webp]
# [description: V1.5:此版本更新适配了呆呆面板丨联通云盘抽奖和联通权益插件，支持验证码/账密登录]
# [depe: ["pycryptodome", "requests"]]


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
    'dd_ltyp_ql_config': form.string().title('设置对接容器').default('').description('青龙配置,用丨分割'),
    'dd_ltyp_var_name': form.string().title('青龙变量名').default('').description('提交到青龙的变量名'),
    'dd_ltyp_ql_format': form.string().title('青龙变量格式').default('').description('1=手机号#token_online 2=token_online 3=手机号#ecs_token'),
    'dd_ltyp_use_daidai': form.boolean().title('使用呆呆面板').default(False).description('是否使用呆呆面板管理变量（开启后将使用呆呆面板替代青龙）'),
    'dd_ltyp_dd_ltyp_ddname': form.string().title('呆呆面板配置').default('').description('呆呆面板配置,用丨分割: 面板地址丨AppKey丨AppSecret'),
})
_CONFIG_FIELD_MAP = {
    ('dd_ltyp', 'ql_config'): 'dd_ltyp_ql_config',
    ('dd_ltyp', 'var_name'): 'dd_ltyp_var_name',
    ('dd_ltyp', 'ql_format'): 'dd_ltyp_ql_format',
    ('dd_ltyp', 'use_daidai'): 'dd_ltyp_use_daidai',
    ('dd_ltyp', 'dd_ltyp_ddname'): 'dd_ltyp_dd_ltyp_ddname',
}

import os
import re
import json
import time
import base64
import hashlib
import random
import asyncio
from datetime import datetime, timedelta
import requests
import httpx
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()
uservalue = sg.bucketGet(bucket='dd_ltyp_user', key=userid)

PLUGIN_CONFIG = {
    'bucket': 'dd_ltyp',
    'coin_key': 'ltypcoin',
    'name': '联通云盘'
}

PUBLIC_KEY_BASE64 = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDc+CZK9bBA9IU+gZUOc6FUGu7yO9WpTNB0PzmgFBh96Mg1WrovD1oqZ+eIF4LjvxKXGOdI79JRdve9NPhQo07+uqGQgE4imwNnRx7PFtCRryiIEcUoavuNtuRVoBAm6qdB0SrctgaqGfLgKvZHOnwTjyNqjBUxzMeQlEC2czEMSwIDAQAB"
DEFAULT_SPLIT = "#PART#"
MAX_BLOCK_SIZE = 117
LOGIN_URL = "https://m.client.10010.com/mobileService/login.htm"
LOGIN_APP_ID = "44fd964cef7a8ced082d577f9b8d6b2e4440b3365caa7f55c9dbb89f2bb937ffb6edbf14685c46dc3cb09713d0ee6c4d40024d30b1c641b50acbd438906c2e7130b971868dd96077b1852c03c7eb0dfe8942d033f902d9af6d471afb6bf955cd"


def get_config():
    """获取插件配置"""
    var_name = sg.bucketGet('dd_ltyp', 'var_name') or 'LTYPCookie'
    ql_config = sg.bucketGet('dd_ltyp', 'ql_config') or ''
    ql_format = sg.bucketGet('dd_ltyp', 'ql_format') or '1'
    return var_name, ql_config, ql_format

def get_daidai_config():
    """获取呆呆面板配置"""
    use_daidai = sg.bucketGet('dd_ltyp', 'use_daidai') or 'false'
    use_daidai = use_daidai.lower() == 'true'
    dd_ltyp_ddname = sg.bucketGet('dd_ltyp', 'dd_ltyp_ddname') or ''
    return use_daidai, dd_ltyp_ddname


def get_full_config():
    """获取完整插件配置"""
    from decimal import Decimal
    var_name = sg.bucketGet('dd_ltyp', 'var_name') or 'LTYPCookie'
    ql_config = sg.bucketGet('dd_ltyp', 'ql_config') or ''
    zsm = sg.bucketGet('dd_ltyp', 'zsm') or ''
    vip_money = Decimal(sg.bucketGet('dd_ltyp', 'vip_money') or '0')
    vip_coin = int(sg.bucketGet('dd_ltyp', 'vip_coin') or '0')
    use_ma_pay = '2099-12-31' or 'false'
    use_ma_pay = use_ma_pay.lower() == 'true'
    return var_name, ql_config, zsm, vip_money, vip_coin, use_ma_pay


def get_payment_config():
    return {}


def generate_qrcode(url):
    """生成二维码图片"""
    try:
        import urllib.parse
        encoded_url = urllib.parse.quote(url, safe='')
        return f"https://api.qrtool.cn/?text={encoded_url}"
    except Exception as e:
        print(f"生成二维码失败: {str(e)}")
        return None


def send_qrcode_image(sender, qrcode_url, pay_type):
    """发送二维码图片"""
    pay_type_names = {'alipay': '支付宝', 'wxpay': '微信', 'qqpay': 'QQ钱包'}
    pay_type_name = pay_type_names.get(pay_type, pay_type)

    try:
        sender.replyImage(qrcode_url)
        if pay_type == 'qqpay':
            sender.reply(f"请使用【{pay_type_name}】扫描上方二维码完成支付\nQQ支付打开图片若是黑屏，长按屏幕进行\"识别二维码\"即可！\n支付过程中输入'q'可取消支付")
        else:
            sender.reply(f"请使用【{pay_type_name}】扫描上方二维码完成支付\n支付过程中输入'q'可取消支付")
    except:
        if pay_type == 'qqpay':
            pay_msg = f'请使用【{pay_type_name}】扫描下方二维码完成支付，支付过程中输入"q"可取消支付:\nQQ支付打开图片若是黑屏，长按屏幕进行"识别二维码"即可！\n[CQ:image,file={qrcode_url}]'
        else:
            pay_msg = f'请使用【{pay_type_name}】扫描下方二维码完成支付，支付过程中输入"q"可取消支付:\n[CQ:image,file={qrcode_url}]'
        sender.reply(pay_msg)


def empower(empowertime, me_as_int):
    """授权时间计算"""
    today_date = datetime.now().date()
    today_time = str(today_date)
    day = me_as_int * 30
    if len(empowertime) == 0 or empowertime <= today_time:
        delayed_date = today_date + timedelta(days=day)
    elif empowertime > today_time:
        empower_date = datetime.strptime(empowertime, "%Y-%m-%d")
        delayed_date = empower_date + timedelta(days=day)
        delayed_date = delayed_date.date()
    else:
        return None
    return str(delayed_date)


def get_auth_status(account_vip, today_time):
    return '2099-12-31'


def parse_payment_result(ddzf):
    return True


def mask_phone(phone):
    """手机号脱敏"""
    if isinstance(phone, str) and len(phone) >= 11:
        return phone[:3] + "****" + phone[-4:]
    return phone


class SMSEncrypt:
    """RSA加密类 - 用于短信验证码登录"""
    def __init__(self):
        self.k = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDc+CZK9bBA9IU+gZUOc6FUGu7y
O9WpTNB0PzmgFBh96Mg1WrovD1oqZ+eIF4LjvxKXGOdI79JRdve9NPhQo07+uqGQ
gE4imwNnRx7PFtCRryiIEcUoavuNtuRVoBAm6qdB0SrctgaqGfLgKvZHOnwTjyNq
jBUxzMeQlEC2czEMSwIDAQAB
-----END PUBLIC KEY-----"""

    def rsa(self, d):
        try:
            from Crypto.PublicKey import RSA
            from Crypto.Cipher import PKCS1_v1_5
            from base64 import b64encode
            d = d.encode('utf-8')
            l = len(d)
            dl = 117
            p = RSA.import_key(self.k)
            c = PKCS1_v1_5.new(p)
            r = []
            for i in range(0, l, dl):
                r.append(c.encrypt(d[i:i+dl]))
            return b64encode(b''.join(r)).decode()
        except:
            return ""


class UnicomSMS:
    """联通短信验证码登录"""
    def __init__(self, phone):
        self.phone = phone
        self.e = SMSEncrypt()
        self.did = hashlib.md5(phone.encode()).hexdigest()
        self.s = requests.Session()
        self.ua = f"Mozilla/5.0 (Linux; Android 13; M2007J3SC Build/TKQ1.220829.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/107.0.5304.141 Mobile Safari/537.36; unicom{{version:android@11.0800,desmobile:{phone}}};devicetype{{deviceBrand:Xiaomi,deviceModel:M2007J3SC}};{{yw_code:}}"

    def post(self, url, data):
        try:
            h = {
                'Host': 'm.client.10010.com',
                'User-Agent': self.ua,
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Requested-With': 'com.sinovatech.unicom.ui'
            }
            r = self.s.post(url, headers=h, data=data, timeout=15, verify=False)
            try:
                return r.json()
            except:
                return {"code": "Err", "msg": f"HTML响应(IP被风控): {r.text[:60]}..."}
        except Exception as e:
            return {"code": "Err", "msg": f"请求异常: {str(e)}"}

    def login(self, code):
        """使用短信验证码登录"""
        from urllib.parse import quote
        u = "https://m.client.10010.com/mobileService/radomLogin.htm"
        t = datetime.now().strftime('%Y%m%d%H%M%S')
        d = f"isFirstInstall=1&simCount=1&yw_code=&loginStyle=0&isRemberPwd=true&deviceOS=android13&mobile={quote(self.e.rsa(self.phone))}&netWay=Wifi&version=android@11.0800&deviceId={self.did}&password={quote(self.e.rsa(code))}&keyVersion=&provinceChanel=general&appId=06eccb0b7c2fd02bc1bb5e8a9ca28741239c3b50f82256263d117f58676ffba6021b5e1ab481056d6ce70c6c98f775d65728b662f8a9da9cc4fa96e0f73a3ff3b0a6b93b73787d84970d3c2e78a15179&deviceModel=M2007J3SC&androidId={self.did[:16]}&deviceBrand=Xiaomi&timestamp={t}"
        res = self.post(u, d)

        if str(res.get("code")) in ["0", "0000"]:
            token_online = res.get('token_online', '')
            ecs_token = res.get('ecs_token', '')
            if token_online:
                return {"status": "success", "token_online": token_online, "ecs_token": ecs_token}
        return {"status": "fail", "msg": f"登录失败: {res.get('desc', res.get('msg', '未知错误'))} [Code:{res.get('code')}]"}


def rsa_encrypt(plaintext, public_key_base64):
    """RSA 公钥加密函数"""
    public_key_bytes = base64.b64decode(public_key_base64)
    public_key_b64 = base64.b64encode(public_key_bytes).decode('utf-8')
    pem_lines = [public_key_b64[i:i+64] for i in range(0, len(public_key_b64), 64)]
    pem_public_key = "-----BEGIN PUBLIC KEY-----\n" + "\n".join(pem_lines) + "\n-----END PUBLIC KEY-----"
    public_key = serialization.load_pem_public_key(pem_public_key.encode('utf-8'))
    plaintext_bytes = plaintext.encode('utf-8')
    if len(plaintext_bytes) <= MAX_BLOCK_SIZE:
        encrypted = public_key.encrypt(plaintext_bytes, padding.PKCS1v15())
        return encrypted
    encrypted_blocks = []
    for i in range(0, len(plaintext_bytes), MAX_BLOCK_SIZE):
        block = plaintext_bytes[i:i + MAX_BLOCK_SIZE]
        encrypted_block = public_key.encrypt(block, padding.PKCS1v15())
        if i > 0:
            encrypted_blocks.append(DEFAULT_SPLIT.encode('utf-8'))
        encrypted_blocks.append(encrypted_block)
    return b''.join(encrypted_blocks)


def mobile_encrypt(data):
    """手机号加密函数"""
    encrypted_bytes = rsa_encrypt(data, PUBLIC_KEY_BASE64)
    return base64.b64encode(encrypted_bytes).decode('utf-8').replace('\n', '')


def password_encrypt(password, random_str="000000"):
    """密码加密函数"""
    combined = password + random_str
    return mobile_encrypt(combined)


def handle_risk_verification(base_url, mobile_encrypted, session):
    """处理风控验证"""
    try:
        from urllib.parse import urlencode, urlparse
        parsed = urlparse(base_url)
        full_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        params = {"channel": "antiBrushing", "mobile": mobile_encrypted}
        full_url_with_params = f"{full_url}?{urlencode(params)}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 12; Redmi K30 Pro Build/SKQ1.220303.001) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        }
        response = session.get(full_url_with_params, headers=headers, timeout=15)
        return True
    except Exception as e:
        return False


def perform_login(mobile, password, retry_count=0, max_retries=2):
    """账密登录获取token_online"""
    try:
        session = requests.Session()
        mobile_encrypted = mobile_encrypt(mobile)
        password_encrypted = password_encrypt(password)
        device_id = hashlib.md5(mobile.encode()).hexdigest()
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        android_id = device_id[:16]

        payload = {
            "isFirstInstall": "1",
            "simCount": "0",
            "yw_code": "",
            "deviceOS": "android12",
            "mobile": mobile_encrypted,
            "netWay": "Wifi",
            "deviceCode": device_id,
            "isRemberPwd": "true",
            "version": "android@11.0702",
            "deviceId": device_id,
            "pushPlatform": "XIAOMI",
            "password": password_encrypted,
            "platformToken": "",
            "keyVersion": "",
            "pip": "192.168.3.24",
            "provinceChanel": "general",
            "appId": LOGIN_APP_ID,
            "simOperator": "5,中国联通,460,01,cn@5,--,460,01,cn",
            "deviceModel": "Redmi K30 Pro",
            "androidId": android_id,
            "deviceBrand": "Xiaomi",
            "uniqueIdentifier": f"and{device_id}",
            "timestamp": timestamp
        }
        headers = {
            "Host": "m.client.10010.com",
            "Accept-Encoding": "gzip",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 12; Redmi K30 Pro Build/SKQ1.220303.001);unicom{version:android@11.0702}",
        }
        response = session.post(LOGIN_URL, data=payload, headers=headers, timeout=10)
        data = response.json()

        if data.get("code") == "ECS99999" and data.get("url"):
            risk_url = data.get("url")
            if retry_count < max_retries:
                encrypted_mobile_from_resp = data.get("mobile", "")
                if handle_risk_verification(risk_url, encrypted_mobile_from_resp, session):
                    time.sleep(3)
                    return perform_login(mobile, password, retry_count + 1, max_retries)
            return None, "触发风控验证，请稍后重试"

        if data.get("code") in ["0", "0000"]:
            token_online = data.get("token_online", "")
            if token_online:
                return token_online, None
            return None, "未获取到token_online"
        else:
            return None, data.get('dsc', data.get('msg', '登录失败'))
    except Exception as e:
        return None, str(e)


def get_ql_token(url, client_id, client_secret):
    """获取青龙token"""
    try:
        r = requests.get(f'{url}/open/auth/token?client_id={client_id}&client_secret={client_secret}')
        if r.status_code != 200:
            raise Exception(f"请求失败: {r.status_code}")
        data = r.json()
        if "token" not in data.get('data', {}):
            raise Exception("获取token失败")
        return data['data']['token']
    except Exception as e:
        raise Exception(f"获取token失败: {str(e)}")


def dd_get_token(dd_url, app_key, app_secret):
    """获取呆呆面板Token"""
    try:
        url = f'{dd_url}/api/open-api/token'
        data = {"app_key": app_key, "app_secret": app_secret}
        response = requests.post(url, json=data)
        if response.status_code != 200:
            raise Exception(f"请求失败: {response.status_code}")
        result = response.json()
        access_token = result.get('data', {}).get('access_token')
        if access_token:
            return access_token
        raise Exception("获取Token失败")
    except Exception as e:
        raise Exception(f"获取呆呆面板Token失败: {str(e)}")


def init_qinglong():
    """初始化面板连接（支持青龙/呆呆面板）"""
    use_daidai, dd_ltyp_ddname = get_daidai_config()
    var_name, ql_config, ql_format = get_config()

    if use_daidai:
        if not dd_ltyp_ddname:
            return None, None, None, None
        ddlist = dd_ltyp_ddname.split('丨')
        if len(ddlist) != 3:
            return None, None, None, None
        dd_url = ddlist[0].strip()
        app_key = ddlist[1].strip()
        app_secret = ddlist[2].strip()
        if not all([dd_url, app_key, app_secret]):
            return None, None, None, None
        try:
            token = dd_get_token(dd_url, app_key, app_secret)
            return dd_url, token, var_name, ql_format
        except:
            return None, None, None, None

    if not ql_config:
        return None, None, None, None
    ql_params = ql_config.split('丨')
    if len(ql_params) != 3:
        return None, None, None, None
    ql_url = ql_params[0].strip()
    client_id = ql_params[1].strip()
    client_secret = ql_params[2].strip()
    if not all([ql_url, client_id, client_secret]):
        return None, None, None, None
    try:
        token = get_ql_token(ql_url, client_id, client_secret)
        return ql_url, token, var_name, ql_format
    except:
        return None, None, None, None


def add_to_qinglong(ql_url, ql_token, var_name, token_online, phone, remark, ql_format='1', ecs_token=None, expire_time=None):
    """添加变量到面板（支持青龙/呆呆面板）
    ql_format: 1=手机号#token_online 2=token_online 3=手机号#ecs_token
    expire_time: 授权到期时间
    """
    use_daidai, _ = get_daidai_config()

    if ql_format == '1':
        env_value = f"{phone}#{token_online}"
    elif ql_format == '2':
        env_value = token_online
    elif ql_format == '3':
        if ecs_token:
            env_value = f"{phone}#{ecs_token}"
        else:
            env_value = f"{phone}#{token_online}"
    else:
        env_value = f"{phone}#{token_online}"

    account_remark = remark
    if not account_remark:
        account_data = sg.bucketGet('dd_ltyp_token', phone)
        if account_data:
            try:
                account_remark = json.loads(account_data).get('remark', '')
            except:
                account_remark = ''

    remarks_parts = [f"手机:{phone}"]
    remarks_parts.append(f"备注:{account_remark or ''}")
    if expire_time:
        remarks_parts.append(f"到期:{expire_time}")
    remarks_parts.append(f"用户:{userid}")

    if use_daidai:
        try:
            headers = {
                "Authorization": f"Bearer {ql_token}",
                "accept": "application/json",
                "Content-Type": "application/json"
            }
            params = {"keyword": str(phone), "page_size": 100}
            response = requests.get(f"{ql_url}/api/envs", headers=headers, params=params).json()
            exists_id = None
            data_list = response.get('data', [])
            if isinstance(data_list, list):
                for env in data_list:
                    if env.get('name') == var_name and str(phone) in (env.get('remarks') or ''):
                        exists_id = env['id']
                        break

            data = {
                "value": env_value,
                "name": var_name,
                "remarks": "丨".join(remarks_parts)
            }

            if exists_id:
                response = requests.put(f"{ql_url}/api/envs/{exists_id}", headers=headers, json=data)
            else:
                response = requests.post(f"{ql_url}/api/envs", headers=headers, json=data)

            return response.status_code in (200, 201)
        except:
            return False
    else:
        try:
            url = f"{ql_url}/open/envs"
            headers = {
                "Authorization": f"Bearer {ql_token}",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                raise Exception("获取变量失败")

            exists_id = None
            for env in response.json().get('data', []):
                if env['name'] == var_name and phone in env.get('remarks', ''):
                    exists_id = env['id']
                    break

            data = {
                "name": var_name,
                "value": env_value,
                "remarks": "丨".join(remarks_parts)
            }

            if exists_id:
                data['id'] = exists_id
                response = requests.put(url, headers=headers, json=data)
            else:
                response = requests.post(url, headers=headers, json=[data])

            if response.status_code != 200:
                raise Exception("提交变量失败")
            return True
        except Exception as e:
            return False


def delete_from_qinglong(ql_url, ql_token, var_name, phone):
    """从面板删除变量（支持青龙/呆呆面板）"""
    use_daidai, _ = get_daidai_config()

    if use_daidai:
        try:
            headers = {
                "Authorization": f"Bearer {ql_token}",
                "accept": "application/json",
                "Content-Type": "application/json"
            }
            params = {"keyword": str(phone), "page_size": 100}
            response = requests.get(f"{ql_url}/api/envs", headers=headers, params=params).json()
            data_list = response.get('data', [])
            if isinstance(data_list, list):
                for env in data_list:
                    if env.get('name') == var_name and str(phone) in (env.get('remarks') or ''):
                        requests.delete(f"{ql_url}/api/envs/{env['id']}", headers=headers)
                        break
            return True
        except:
            return False
    else:
        try:
            url = f"{ql_url}/open/envs"
            headers = {"Authorization": f"Bearer {ql_token}"}
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                return False
            env_id = None
            for env in response.json().get('data', []):
                if env['name'] == var_name and phone in env.get('remarks', ''):
                    env_id = env['id']
                    break
            if env_id:
                requests.delete(url, headers=headers, json=[env_id])
            return True
        except:
            return False


def encrypt_aes(text, key, iv='wNSOYIB1k1DjY5lA'):
    """AES加密"""
    key_bytes = key[:16].encode('utf-8')
    iv_bytes = iv.encode('utf-8')
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
    padded_text = pad(text.encode('utf-8'), AES.block_size)
    encrypted_bytes = cipher.encrypt(padded_text)
    return base64.b64encode(encrypted_bytes).decode('utf-8')


async def get_ecstoken(session, token_online):
    """获取ecs_token和手机号"""
    try:
        url = "https://m.client.10010.com/mobileService/onLine.htm"
        payload = {
            'isFirstInstall': "1",
            'version': "android@11.0702",
            'token_online': token_online
        }
        headers = {
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 12; leijun Pro Build/SKQ1.22013.001);unicom{version:android@11.0702}",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'Content-Type': "application/x-www-form-urlencoded",
        }
        response = await session.post(url, data=payload, headers=headers)
        response_text = response.text
        try:
            data = json.loads(response_text)
        except:
            return None, None, f"返回非JSON: {response_text[:200]}"
        if data.get("code") == "9999" or data.get("code") == "ECS99999":
            return None, None, "token已失效，请重新登录"
        desmobile = data.get("desmobile")
        ecs_token = data.get("ecs_token")
        if not ecs_token:
            return None, None, data.get("dsc", "获取ecs_token失败")
        return desmobile, ecs_token, None
    except Exception as e:
        return None, None, str(e)


async def get_ticket(session, ecs_token):
    """获取ticket"""
    try:
        url = "https://m.client.10010.com/mobileService/openPlatform/openPlatLineNew.htm?to_url=https://contact.bol.wo.cn/market"
        headers = {
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 12; leijun Pro Build/SKQ1.22013.001);unicom{version:android@11.0702}",
            'Cookie': f'ecs_token={ecs_token}',
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
        }
        response = await session.get(url, headers=headers, follow_redirects=False)
        if response.status_code in (301, 302, 303, 307, 308):
            location = response.headers.get('Location')
            if location:
                from urllib.parse import urlparse, parse_qs
                parsed_url = urlparse(location)
                query_params = parse_qs(parsed_url.query)
                ticket = query_params.get('ticket', [None])[0]
                return ticket, None
        return None, f"状态码:{response.status_code}"
    except Exception as e:
        return None, str(e)


async def get_cloud_token(session, ticket):
    """获取云盘token"""
    try:
        url = "https://panservice.mail.wo.cn/wohome/dispatcher"
        timestamp = str(int(time.time() * 1000))
        result = random.randint(123456, 199999)
        key = "HandheldHallAutoLogin"
        channel = "100002"
        client_id = "1001000035"

        string_to_hash = key + timestamp + str(result) + channel
        md5_hash = hashlib.md5()
        md5_hash.update(string_to_hash.encode('utf-8'))
        md5Hash = md5_hash.hexdigest()

        payload = {
            "header": {
                "key": key,
                "resTime": timestamp,
                "reqSeq": result,
                "channel": channel,
                "version": "",
                "sign": md5Hash
            },
            "body": {
                "clientId": client_id,
                "ticket": ticket
            }
        }
        headers = {
            'User-Agent': "LianTongYunPan/5.0.8 (Android 12)",
            'Content-Type': "application/json",
        }
        response = await session.post(url, headers=headers, json=payload)
        data = response.json()
        rsp_data = data.get("RSP", {}).get("DATA")
        if isinstance(rsp_data, dict):
            return rsp_data.get("token")
        return None
    except:
        return None


async def get_market_user_token(session, ecs_token):
    """获取权益超市userToken（用于抽奖记录查询，与脚本一致）"""
    try:
        from urllib.parse import urlparse, parse_qs
        url = "https://m.client.10010.com/mobileService/openPlatform/openPlatLineNew.htm?to_url=https://contact.bol.wo.cn/market"
        headers = {
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 12; leijun Pro Build/SKQ1.22013.001);unicom{version:android@11.0702}",
            'Cookie': f'ecs_token={ecs_token}',
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
        }
        response = await session.get(url, headers=headers, follow_redirects=False)
        if response.status_code not in (301, 302, 303, 307, 308):
            return None

        location = response.headers.get('Location')
        if not location:
            return None

        parsed_url = urlparse(location)
        query_params = parse_qs(parsed_url.query)
        ticket = query_params.get('ticket', [None])[0]
        if not ticket:
            return None

        login_url = f"https://backward.bol.wo.cn/prod-api/auth/marketUnicomLogin?ticket={ticket}"
        login_headers = {
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 12; leijun Pro Build/SKQ1.22013.001);unicom{version:android@11.0702}",
        }
        login_resp = await session.post(login_url, headers=login_headers)
        login_result = login_resp.json()
        return login_result.get("data", {}).get("token")
    except Exception as e:
        print(f"get_market_user_token error: {e}")
        return None


async def query_raffle_records(session, user_token):
    """查询权益超市抽奖中奖记录（与脚本getMyPrize接口一致）"""
    try:
        url = "https://backward.bol.wo.cn/prod-api/promotion/home/raffleActivity/getMyPrize"
        headers = {
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 12; leijun Pro Build/SKQ1.22013.001);unicom{version:android@11.0702}",
            'Content-Type': "application/json",
            'Authorization': f'Bearer {user_token}',
        }
        payload = {
            "id": 12,
            "type": 0,
            "page": 1,
            "limit": 100
        }
        response = await session.post(url, headers=headers, json=payload)
        data = response.json()
        if data.get("code") == 200:
            records = []
            for item in data.get("data", {}).get("list", []):
                records.append({
                    'id': item.get('id'),
                    'name': item.get('prizesName'),
                    'time': item.get('createTime'),
                    'deadline': item.get('deadline'),
                    'status': '已领取' if item.get('status') == 1 else '待领取',
                })
            return records
        return []
    except Exception as e:
        print(f"query_raffle_records error: {e}")
        return []


async def query_cloud_lottery_records(session, cloud_token, activity_id):
    """查询云盘抽奖中奖记录（与20251210联通云盘抽奖.py脚本一致）"""
    try:
        url = "https://panservice.mail.wo.cn/activity/lottery/recordList"
        headers = {
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 12; leijun Pro Build/SKQ1.22013.001);unicom{version:android@11.0702}",
            'Accept': "application/json, text/plain, */*",
            'requestTime': str(int(time.time() * 1000)),
            'clientId': "1001000165",
            'X-YP-Client-Id': "1001000165",
            'source-type': "woapi",
            'X-YP-Access-Token': cloud_token,
            'token': cloud_token,
        }
        params = {'activityId': f'{activity_id}='}
        response = await session.get(url, headers=headers, params=params)
        data = response.json()
        if data.get("meta", {}).get("code") == "200":
            records = []
            for item in data.get("result", []):
                records.append({
                    'name': item.get('prizeName'),
                    'time': item.get('createTime'),
                })
            return records
        return []
    except Exception as e:
        print(f"query_cloud_lottery_records error: {e}")
        return []


async def query_sign_telephone(session, ecs_token):
    """查询签到区话费红包总额"""
    try:
        url = "https://act.10010.com/SigninApp/convert/getTelephone"
        headers = {
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 12; leijun Pro Build/SKQ1.22013.001);unicom{version:android@11.0702}",
            'Cookie': f'ecs_token={ecs_token}',
            'Content-Type': "application/x-www-form-urlencoded",
        }
        response = await session.post(url, headers=headers, data={})
        data = response.json()
        if data.get("status") == "0000" and data.get("data"):
            telephone_val = data["data"].get("telephone", 0)
            try:
                telephone = float(telephone_val) if telephone_val else 0.0
            except (ValueError, TypeError):
                telephone = 0.0
            return telephone
        return None
    except Exception as e:
        print(f"query_sign_telephone error: {e}")
        return None


async def query_ttlxj_available(session, ecs_token, mobile):
    """查询天天领现金-可用立减金"""
    try:
        target_url = "https://epay.10010.com/ci-mps-st-web/?webViewNavIsHidden=webViewNavIsHidden"
        open_url = f"https://m.client.10010.com/mobileService/openPlatform/openPlatLineNew.htm?to_url={target_url}"
        open_headers = {
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 12; leijun Pro Build/SKQ1.22013.001);unicom{version:android@11.0702}",
            'Cookie': f'ecs_token={ecs_token}',
        }
        open_resp = await session.get(open_url, headers=open_headers, follow_redirects=False)
        if open_resp.status_code not in (301, 302, 303, 307, 308):
            return None

        location = open_resp.headers.get('Location', '')
        if not location:
            return None

        from urllib.parse import urlparse, parse_qs
        parsed = urlparse(location)
        params = parse_qs(parsed.query)
        ticket = params.get('ticket', [None])[0]
        st_type = params.get('type', ['02'])[0]

        if not ticket:
            return None

        import secrets
        auth_url = "https://epay.10010.com/woauth2/v2/authorize"
        auth_headers = {
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 12; leijun Pro Build/SKQ1.22013.001);unicom{version:android@11.0702}",
            'Content-Type': "application/json",
            'Origin': "https://epay.10010.com",
            'Referer': location,
        }
        auth_payload = {
            "response_type": "rptid",
            "client_id": "73b138fd-250c-4126-94e2-48cbcc8b9cbe",
            "redirect_uri": "https://epay.10010.com/ci-mps-st-web/",
            "login_hint": {
                "credential_type": "st_ticket",
                "credential": ticket,
                "st_type": st_type,
                "force_logout": True,
                "source": "app_sjyyt"
            },
            "device_info": {
                "token_id": f"chinaunicom-pro-{int(time.time()*1000)}-{secrets.token_hex(6)}",
                "trace_id": secrets.token_hex(16)
            }
        }
        auth_resp = await session.post(auth_url, headers=auth_headers, json=auth_payload)
        auth_data = auth_resp.json()
        if auth_data.get("status") != 200:
            return None

        biz_info = json.dumps({
            "bizChannelCode": "225",
            "disriBiz": "party",
            "unionSessionId": "",
            "stType": "",
            "stDesmobile": "",
            "source": "",
            "rptId": "",
            "ticket": "",
            "tongdunTokenId": "",
            "xindunTokenId": ""
        })

        check_url = "https://epay.10010.com/ps-pafs-auth-front/v1/auth/check"
        check_headers = {
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 12; leijun Pro Build/SKQ1.22013.001);unicom{version:android@11.0702}",
            'bizchannelinfo': biz_info,
        }
        check_resp = await session.post(check_url, headers=check_headers)
        check_data = check_resp.json()

        session_id = ""
        token_id = ""

        if check_data.get("code") == "0000":
            auth_info_data = check_data.get("data", {}).get("authInfo", {})
            session_id = auth_info_data.get("sessionId", "")
            token_id = auth_info_data.get("tokenId", "")
        elif check_data.get("code") == "2101000100":
            login_url_base = check_data.get("data", {}).get("woauth_login_url", "")
            if login_url_base:
                full_login_url = f"{login_url_base}https://epay.10010.com/ci-mcss-party-web/clockIn/?bizFrom=225&bizChannelCode=225"
                login_headers = {
                    'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 12; leijun Pro Build/SKQ1.22013.001);unicom{version:android@11.0702}",
                }
                login_resp = await session.get(full_login_url, headers=login_headers, follow_redirects=False)
                if login_resp.status_code in (301, 302, 303, 307, 308):
                    login_location = login_resp.headers.get('Location', '')
                    if 'rptid=' in login_location:
                        parsed_login = urlparse(login_location)
                        login_params = parse_qs(parsed_login.query)
                        rpt_id = login_params.get('rptid', [''])[0]

                        biz_info = json.dumps({
                            "bizChannelCode": "225",
                            "disriBiz": "party",
                            "unionSessionId": "",
                            "stType": "",
                            "stDesmobile": "",
                            "source": "",
                            "rptId": rpt_id,
                            "ticket": "",
                            "tongdunTokenId": "",
                            "xindunTokenId": ""
                        })

                        check_headers2 = {
                            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 12; leijun Pro Build/SKQ1.22013.001);unicom{version:android@11.0702}",
                            'bizchannelinfo': biz_info,
                        }
                        check_resp2 = await session.post(check_url, headers=check_headers2)
                        check_data2 = check_resp2.json()
                        if check_data2.get("code") == "0000":
                            auth_info_data = check_data2.get("data", {}).get("authInfo", {})
                            session_id = auth_info_data.get("sessionId", "")
                            token_id = auth_info_data.get("tokenId", "")

        if not session_id or not token_id:
            return None

        query_url = "https://epay.10010.com/ci-mcss-party-front/v1/ttlxj/queryAvailable"
        auth_info = json.dumps({
            "mobile": "",
            "sessionId": session_id,
            "tokenId": token_id,
            "userId": ""
        })
        query_headers = {
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 12; leijun Pro Build/SKQ1.22013.001);unicom{version:android@11.0702}",
            'bizchannelinfo': biz_info,
            'authinfo': auth_info,
        }
        query_resp = await session.post(query_url, headers=query_headers)
        query_data = query_resp.json()
        if query_data.get("code") == "0000" and str(query_data.get("data", {}).get("returnCode")) == "0":
            available_amount = int(query_data["data"].get("availableAmount", 0))
            return available_amount / 100  # 转换为元
        return None
    except Exception as e:
        print(f"query_ttlxj_available error: {e}")
        return None


async def query_woread_balance(session, token_online):
    """查询阅读区话费红包余额"""
    try:
        import hashlib as hl
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import pad

        default_password = "woreadst^&*12345"
        iv_string = "16-Bytes--String"
        product_id = "10000002"
        secret_key = "7k1HcDL8RKvc"

        def encode_woread_hex(data):
            """AES加密并返回hex再base64"""
            key_bytes = default_password[:16].encode('utf-8')
            iv_bytes = iv_string.encode('utf-8')
            cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
            if isinstance(data, dict):
                json_str = json.dumps(data)
            else:
                json_str = str(data)
            padded = pad(json_str.encode('utf-8'), AES.block_size)
            encrypted = cipher.encrypt(padded)
            hex_str = encrypted.hex()
            return base64.b64encode(hex_str.encode('utf-8')).decode('utf-8')

        timestamp = int(time.time() * 1000)
        sign_str = f"{product_id}{secret_key}{timestamp}"
        md5_hash = hl.md5(sign_str.encode()).hexdigest()

        date_str = datetime.now().strftime('%Y%m%d%H%M%S')
        crypt_text = {"timestamp": date_str}
        encoded_sign = encode_woread_hex(crypt_text)

        auth_url = f"https://10010.woread.com.cn/ng_woread_service/rest/app/auth/{product_id}/{timestamp}/{md5_hash}"
        auth_headers = {
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 12; leijun Pro Build/SKQ1.22013.001);unicom{version:android@11.0702}",
            'Content-Type': "application/json",
        }
        auth_resp = await session.post(auth_url, headers=auth_headers, json={"sign": encoded_sign})
        auth_data = auth_resp.json()
        if auth_data.get("code") != "0000":
            return None

        access_token = auth_data.get("data", {}).get("accesstoken")
        if not access_token:
            return None

        def encode_woread_str(text):
            """单字符串加密"""
            key_bytes = default_password[:16].encode('utf-8')
            iv_bytes = iv_string.encode('utf-8')
            cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
            padded = pad(text.encode('utf-8'), AES.block_size)
            encrypted = cipher.encrypt(padded)
            hex_str = encrypted.hex()
            return base64.b64encode(hex_str.encode('utf-8')).decode('utf-8')

        token_enc = encode_woread_str(token_online)
        phone_enc = encode_woread_str("13800000000")
        login_timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

        inner_json = json.dumps({
            "tokenOnline": token_enc,
            "phone": phone_enc,
            "timestamp": login_timestamp
        })
        login_sign = encode_woread_str(inner_json)

        login_url = "https://10010.woread.com.cn/ng_woread_service/rest/account/login"
        login_headers = {
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 12; leijun Pro Build/SKQ1.22013.001);unicom{version:android@11.0702}",
            'Content-Type': "application/json",
            'accesstoken': access_token,
        }
        login_resp = await session.post(login_url, headers=login_headers, json={"sign": login_sign})
        login_data = login_resp.json()
        if login_data.get("code") != "0000":
            return None

        woread_token = login_data.get("data", {}).get("token")
        woread_userid = login_data.get("data", {}).get("userid")
        woread_userindex = login_data.get("data", {}).get("userindex")
        woread_verifycode = login_data.get("data", {}).get("verifycode")

        if not woread_token:
            return None

        query_param = {
            "timestamp": datetime.now().strftime('%Y%m%d%H%M%S'),
            "token": woread_token,
            "userid": woread_userid,
            "userId": woread_userid,
            "userIndex": woread_userindex,
            "userAccount": "",
            "verifyCode": woread_verifycode
        }
        query_sign = encode_woread_hex(query_param)
        query_url = "https://10010.woread.com.cn/ng_woread_service/rest/phone/vouchers/queryTicketAccount"
        query_headers = {
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 12; leijun Pro Build/SKQ1.22013.001);unicom{version:android@11.0702}",
            'Content-Type': "application/json",
            'accesstoken': access_token,
        }
        query_resp = await session.post(query_url, headers=query_headers, json={"sign": query_sign})
        query_data = query_resp.json()
        if query_data.get("code") == "0000":
            usable_num = query_data.get("data", {}).get("usableNum", 0)
            return usable_num / 100  # 转换为元
        return None
    except Exception as e:
        print(f"query_woread_balance error: {e}")
        return None


async def query_watering_progress(session, user_token):
    """查询权益超市浇花进度"""
    try:
        url = "https://backward.bol.wo.cn/prod-api/promotion/activityTask/getMultiCycleProcess?activityId=13"
        headers = {
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 12; leijun Pro Build/SKQ1.22013.001);unicom{version:android@11.0702}",
            'Authorization': f'Bearer {user_token}',
        }
        response = await session.get(url, headers=headers)
        data = response.json()
        if data.get("code") == 200 and data.get("data"):
            triggered_time = data["data"].get("triggeredTime", 0)
            trigger_time = data["data"].get("triggerTime", 0)
            return triggered_time, trigger_time
        return None, None
    except Exception as e:
        print(f"query_watering_progress error: {e}")
        return None, None


async def query_cloud_points(session, ecs_token):
    """查询云盘任务积分（完整流程）"""
    try:
        ticket_url = f"https://m.client.10010.com/edop_ng/getTicketByNative?appId=edop_unicom_d67b3e30&token={ecs_token}"
        ticket_headers = {
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 12; leijun Pro Build/SKQ1.22013.001);unicom{version:android@11.0702}",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
        }
        ticket_resp = await session.get(ticket_url, headers=ticket_headers)
        ticket_data = ticket_resp.json()
        ticket = ticket_data.get("ticket")
        if not ticket:
            return None, None

        timestamp = str(int(time.time() * 1000))
        result_num = random.randint(123456, 199999)
        string_to_hash = f"HandheldHallAutoLoginV2{timestamp}{result_num}wohome"
        md5_hash = hashlib.md5(string_to_hash.encode('utf-8')).hexdigest()

        dispatcher_url = "https://panservice.mail.wo.cn/wohome/dispatcher"
        dispatcher_payload = {
            "header": {
                "key": "HandheldHallAutoLoginV2",
                "resTime": timestamp,
                "reqSeq": result_num,
                "channel": "wohome",
                "version": "",
                "sign": md5_hash
            },
            "body": {
                "clientId": "1001000003",
                "ticket": ticket
            }
        }
        dispatcher_headers = {
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 12; leijun Pro Build/SKQ1.22013.001);unicom{version:android@11.0702}",
            'Content-Type': "application/json",
        }
        dispatcher_resp = await session.post(dispatcher_url, headers=dispatcher_headers, json=dispatcher_payload)
        dispatcher_data = dispatcher_resp.json()
        user_token = dispatcher_data.get("RSP", {}).get("DATA", {}).get("token")
        if not user_token:
            return None, None

        userticket_url = "https://panservice.mail.wo.cn/api-user/api/user/ticket"
        userticket_headers = {
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 12; leijun Pro Build/SKQ1.22013.001);unicom{version:android@11.0702}",
            'Content-Type': 'application/json',
            'X-YP-Access-Token': user_token,
            'accesstoken': user_token,
            'token': user_token,
            'clientId': "1001000003",
            'X-YP-Client-Id': "1001000003",
            'source-type': "woapi",
            'app-type': "unicom"
        }
        userticket_resp = await session.post(userticket_url, headers=userticket_headers, json={})
        userticket_data = userticket_resp.json()
        user_ticket = userticket_data.get("result", {}).get("ticket")
        if not user_ticket:
            return None, None

        userinfo_url = "https://m.jf.10010.com/jf-external-application/jftask/userInfo"
        userinfo_headers = {
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 12; leijun Pro Build/SKQ1.22013.001);unicom{version:android@11.0702}",
            'Content-Type': 'application/json;charset=UTF-8',
            'ticket': user_ticket,
            'partnersid': "1649",
            'origin': "https://m.jf.10010.com",
            'clienttype': "yunpan_android",
            'x-requested-with': "com.sinovatech.unicom.ui"
        }
        userinfo_resp = await session.post(userinfo_url, headers=userinfo_headers, json={})
        userinfo_data = userinfo_resp.json()

        if userinfo_data.get("data"):
            all_earn_score = userinfo_data["data"].get("allEarnScore", 0)
            available_score = userinfo_data["data"].get("availableScore", 0)
            return all_earn_score, available_score
        return None, None
    except Exception as e:
        print(f"query_cloud_points error: {e}")
        return None, None


async def query_cloud_records(token_online):
    """查询账号信息（包含各类余额和中奖记录）"""
    try:
        async with httpx.AsyncClient(timeout=30, verify=False) as session:
            phone, ecs_token, err = await get_ecstoken(session, token_online)
            if not ecs_token:
                return None, err or "获取ecs_token失败"

            result = {
                'phone': phone,
                'market_records': [],
                'cloud_records': [],
                'sign_telephone': None,  # 签到区话费红包
                'ttlxj_available': None,  # 天天领现金-立减金
                'woread_balance': None,  # 阅读区话费红包余额
                'watering_progress': None,  # 浇花进度
                'cloud_all_score': None,  # 云盘已赚积分
                'cloud_available_score': None,  # 云盘可用积分
            }

            sign_telephone = await query_sign_telephone(session, ecs_token)
            result['sign_telephone'] = sign_telephone

            ttlxj_available = await query_ttlxj_available(session, ecs_token, phone)
            result['ttlxj_available'] = ttlxj_available

            woread_balance = await query_woread_balance(session, token_online)
            result['woread_balance'] = woread_balance

            user_token = await get_market_user_token(session, ecs_token)
            if user_token:
                market_records = await query_raffle_records(session, user_token)
                result['market_records'] = market_records

                triggered, trigger = await query_watering_progress(session, user_token)
                if triggered is not None and trigger is not None:
                    result['watering_progress'] = f"{triggered}/{trigger}"

            all_score, available_score = await query_cloud_points(session, ecs_token)
            result['cloud_all_score'] = all_score
            result['cloud_available_score'] = available_score

            ticket, _ = await get_ticket(session, ecs_token)
            if ticket:
                cloud_token = await get_cloud_token(session, ticket)
                if cloud_token:
                    activity_ids = ['MTg', 'MTk', 'MjU']
                    all_cloud_records = []
                    for aid in activity_ids:
                        records = await query_cloud_lottery_records(session, cloud_token, aid)
                        all_cloud_records.extend(records)
                    result['cloud_records'] = all_cloud_records

            return result, None
    except Exception as e:
        return None, str(e)


def bind_account():
    """绑定联通云盘账号"""
    guide = """
=====联通云盘登录=====
[1] 📱 验证码登录
[2] 🔑 账密登录
[3] 🎫 Token登录
------------------
回复数字选择登录方式
回复"q"退出
=================="""
    sender.reply(guide)

    choice = sender.input(60000, 1, False)
    if not choice:
        sender.reply("⏰ 操作超时,已退出")
        return
    elif choice.lower() == 'q':
        sender.reply("✅ 已取消登录")
        return

    if choice == '1':
        login_by_sms()
    elif choice == '2':
        login_by_password()
    elif choice == '3':
        login_by_token()
    else:
        sender.reply("❌ 无效选择，请输入1、2或3")


def login_by_sms():
    """短信验证码登录"""
    sender.reply("""
=====验证码登录=====
📱 格式: 手机号#验证码
📝 示例: 13800138000#123456
------------------
💡 支持批量登录(换行分割)
回复"q"退出
==================""")

    user_input = sender.input(120000, 1, False)
    if not user_input:
        sender.reply("⏰ 操作超时,已退出")
        return
    elif user_input.lower() == 'q':
        sender.reply("✅ 已取消登录")
        return

    lines = [line.strip() for line in user_input.split('\n') if line.strip() and '#' in line]
    if not lines:
        sender.reply("❌ 格式错误\n请输入: 手机号#验证码")
        return

    total = len(lines)
    success_count = 0
    fail_count = 0

    if total > 1:
        sender.reply(f"🔄 检测到 {total} 个账号，开始批量登录...")

    for line in lines:
        parts = line.split('#', 1)
        if len(parts) < 2:
            fail_count += 1
            continue

        phone = parts[0].strip()
        code = parts[1].strip()

        if not phone.isdigit() or len(phone) != 11:
            sender.reply(f"❌ {phone} 手机号格式错误")
            fail_count += 1
            continue

        if not code:
            sender.reply(f"❌ {mask_phone(phone)} 验证码不能为空")
            fail_count += 1
            continue

        sender.reply(f"🔄 正在验证 {mask_phone(phone)}...")

        u = UnicomSMS(phone)
        result = u.login(code)

        if result.get("status") != "success":
            sender.reply(f"❌ {mask_phone(phone)} 登录失败: {result.get('msg', '未知错误')}")
            fail_count += 1
            continue

        token_online = result.get("token_online", "")
        ecs_token = result.get("ecs_token", "")

        if not ecs_token:
            try:
                async def fetch_ecs_token():
                    async with httpx.AsyncClient(verify=False, timeout=30) as session:
                        _, ecs, _ = await get_ecstoken(session, token_online)
                        return ecs
                ecs_token = asyncio.run(fetch_ecs_token())
            except Exception as e:
                print(f"获取ecs_token失败: {str(e)}")

        _save_sms_account(phone, token_online, ecs_token)
        success_count += 1
        sender.reply(f"✅ {mask_phone(phone)} 登录成功 [{success_count + fail_count}/{total}]")

    if total > 1:
        sender.reply(f"=====批量登录完成=====\n✅ 成功: {success_count}\n❌ 失败: {fail_count}\n==================")


def _save_sms_account(phone, token_online, ecs_token):
    """保存验证码登录的账号信息"""
    global uservalue

    if not uservalue:
        sg.bucketSet('dd_ltyp_user', userid, str([phone]))
    else:
        accounts = _sg_literal(uservalue)
        if phone not in accounts:
            accounts.append(phone)
            sg.bucketSet('dd_ltyp_user', userid, str(accounts))

    account_info = {
        "phone": phone,
        "password": "",  # 验证码登录没有密码
        "remark": "验证码登录",
        "token_online": token_online,
        "ecs_token": ecs_token,
        "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    sg.bucketSet('dd_ltyp_token', phone, json.dumps(account_info))

    today_time = str(datetime.now().date())
    account_vip = '2099-12-31'

    if account_vip and account_vip > today_time:
        ql_url, ql_token, var_name, ql_format = init_qinglong()
        if ql_url and ql_token:
            add_to_qinglong(ql_url, ql_token, var_name, token_online, phone, '验证码登录', ql_format, ecs_token, account_vip)


def login_by_token():
    """Token登录"""
    sender.reply("""
=====Token登录=====
📱 格式: 备注#online_token
📝 示例: 张三#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
------------------
💡 支持批量登录(换行分割)
回复"q"退出
==================""")

    user_input = sender.input(120000, 1, False)
    if not user_input:
        sender.reply("⏰ 操作超时,已退出")
        return
    elif user_input.lower() == 'q':
        sender.reply("✅ 已取消登录")
        return

    lines = [line.strip() for line in user_input.split('\n') if line.strip() and '#' in line]
    if not lines:
        sender.reply("❌ 格式错误\n请输入: 备注#online_token")
        return

    total = len(lines)
    success_count = 0
    fail_count = 0

    for line in lines:
        parts = line.split('#', 1)
        if len(parts) < 2:
            fail_count += 1
            continue

        remark = parts[0].strip()
        token_online = parts[1].strip()

        if not remark:
            sender.reply("❌ 备注不能为空")
            fail_count += 1
            continue

        if not token_online:
            sender.reply(f"❌ {remark} 的Token不能为空")
            fail_count += 1
            continue

        try:
            async def verify_token():
                async with httpx.AsyncClient(verify=False, timeout=30) as session:
                    try:
                        url = "https://m.client.10010.com/mobileService/onLine.htm"
                        payload = {
                            'isFirstInstall': "1",
                            'version': "android@11.0702",
                            'token_online': token_online
                        }
                        headers = {
                            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 12; leijun Pro Build/SKQ1.22013.001);unicom{version:android@11.0702}",
                            'Connection': "Keep-Alive",
                            'Accept-Encoding': "gzip",
                            'Content-Type': "application/x-www-form-urlencoded",
                        }
                        response = await session.post(url, data=payload, headers=headers)
                        response_text = response.text

                        try:
                            data = json.loads(response_text)
                        except:
                            return None, None, f"返回非JSON格式: {response_text[:100]}"

                        code = data.get("code")
                        if code == "9999" or code == "ECS99999":
                            return None, None, f"Token已失效 [code:{code}]"

                        desmobile = data.get("desmobile")
                        ecs_token = data.get("ecs_token")

                        if not ecs_token:
                            error_msg = data.get("dsc") or data.get("msg") or "未返回ecs_token,可能Token已经失效了"
                            return None, None, f"{error_msg} [code:{code}]"

                        if not desmobile:
                            return None, None, f"未返回手机号 [code:{code}]"

                        return desmobile, ecs_token, None
                    except Exception as e:
                        return None, None, f"请求异常: {str(e)}"

            phone, ecs_token, error = asyncio.run(verify_token())

            if error or not phone:
                sender.reply(f"❌ {remark} Token验证失败\n原因: {error or 'Token无效或已过期'}")
                fail_count += 1
                continue

            _save_token_account(phone, token_online, ecs_token, remark)
            success_count += 1
            sender.reply(f"✅ {remark} ({mask_phone(phone)}) 登录成功 [{success_count + fail_count}/{total}]")

        except Exception as e:
            sender.reply(f"❌ {remark} 登录异常\n错误: {str(e)}")
            fail_count += 1
            continue

    if total > 1:
        sender.reply(f"=====批量登录完成=====\n✅ 成功: {success_count}\n❌ 失败: {fail_count}\n==================")


def _save_token_account(phone, token_online, ecs_token, remark):
    """保存Token登录的账号信息"""
    global uservalue

    if not uservalue:
        sg.bucketSet('dd_ltyp_user', userid, str([phone]))
    else:
        accounts = _sg_literal(uservalue)
        if phone not in accounts:
            accounts.append(phone)
            sg.bucketSet('dd_ltyp_user', userid, str(accounts))

    account_info = {
        "phone": phone,
        "password": "",
        "remark": remark,
        "token_online": token_online,
        "ecs_token": ecs_token,
        "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    sg.bucketSet('dd_ltyp_token', phone, json.dumps(account_info))

    today_time = str(datetime.now().date())
    account_vip = '2099-12-31'

    if account_vip and account_vip > today_time:
        ql_url, ql_token, var_name, ql_format = init_qinglong()
        if ql_url and ql_token:
            add_to_qinglong(ql_url, ql_token, var_name, token_online, phone, remark, ql_format, ecs_token, account_vip)


def login_by_password():
    """账密登录"""
    sender.reply("""
=====账密登录=====
请输入账号信息
格式: 手机号#密码#备注
示例: 13812345678#abc123#张三
------------------
回复"q"退出
==================""")

    user_input = sender.input(120000, 1, False)
    if not user_input:
        sender.reply("⏰ 操作超时,已退出")
        return
    elif user_input.lower() == 'q':
        sender.reply("✅ 已取消登录")
        return

    try:
        parts = user_input.split('#')
        if len(parts) != 3:
            sender.reply("""
=====格式错误=====
❌ 输入格式不正确
------------------
正确格式: 手机号#密码#备注
例如: 13812345678#abc123#张三
==================""")
            return

        phone, password, remark = parts

        if not phone.isdigit() or len(phone) != 11:
            sender.reply("""
=====格式错误=====
❌ 手机号格式不正确
------------------
请输入11位手机号
==================""")
            return
        token_online, error = perform_login(phone, password)
        if not token_online:
            sender.reply(f"""
=====登录失败=====
❌ 原因: {error}
请检查账号密码是否正确
==================""")
            return

        ecs_token = None
        try:
            async def fetch_ecs_token():
                async with httpx.AsyncClient(verify=False, timeout=30) as session:
                    _, ecs, _ = await get_ecstoken(session, token_online)
                    return ecs
            ecs_token = asyncio.run(fetch_ecs_token())
        except Exception as e:
            print(f"获取ecs_token失败: {str(e)}")

        if not uservalue:
            sg.bucketSet('dd_ltyp_user', userid, str([phone]))
        else:
            accounts = _sg_literal(uservalue)
            if phone not in accounts:
                accounts.append(phone)
                sg.bucketSet('dd_ltyp_user', userid, str(accounts))

        account_info = {
            "phone": phone,
            "password": password,
            "remark": remark,
            "token_online": token_online,
            "ecs_token": ecs_token,
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        sg.bucketSet('dd_ltyp_token', phone, json.dumps(account_info))

        today_time = str(datetime.now().date())
        account_vip = '2099-12-31'
        ql_status = "⏳ 待授权后提交"

        if account_vip and account_vip > today_time:
            ql_url, ql_token, var_name, ql_format = init_qinglong()
            if ql_url and ql_token:
                if add_to_qinglong(ql_url, ql_token, var_name, token_online, phone, remark, ql_format, ecs_token, account_vip):
                    ql_status = "✅ 已提交青龙"
                else:
                    ql_status = "❌ 提交青龙失败"
            else:
                ql_status = "❌ 未配置青龙"

        success_msg = f"""
=====绑定成功=====
👤 备注: {remark}
📱 手机号: {mask_phone(phone)}
🔑 Token: 已获取
☁️ 青龙: {ql_status}
💡 提示: 请发送"联通云盘管理"进行授权
=================="""
        sender.reply(success_msg)

    except Exception as e:
        sender.reply(f"""
=====绑定异常=====
❌ 错误: {str(e)}
请重试或检查配置
==================""")


def manage_account():
    """账号管理功能"""
    from decimal import Decimal

    if not uservalue:
        sender.reply("""
=====未绑定账号=====
❌ 未找到任何账号信息
💡 发送 云盘登录 绑定账号
==================""")
        return

    accounts = _sg_literal(uservalue)
    today_time = str(datetime.now().date())

    var_name, ql_config, zsm, vip_money, vip_coin, use_ma_pay = get_full_config()

    account_list = """
=====我的云盘账号=====
[0] 🎯 批量授权所有账号"""

    for i, phone in enumerate(accounts, 1):
        account_data = sg.bucketGet('dd_ltyp_token', phone)
        account_vip = '2099-12-31'
        auth_status, auth_time = get_auth_status(account_vip, today_time)

        if account_data:
            account_info = json.loads(account_data)
            remark = account_info.get('remark', phone)
        else:
            remark = phone

        account_list += f"""
------------------
[{i}] 账号信息
📱 手机号: {mask_phone(phone)}
👤 备注: {remark}
⏰ 授权: {auth_status}"""

    account_list += """
==================
回复数字选择账号
回复"q"退出操作"""

    sender.reply(account_list)

    choice = sender.input(120000, 1, False)
    if not choice or choice.lower() == 'q':
        sender.reply("✅ 已退出管理")
        return

    try:
        me_as_int = int(choice)
        if me_as_int < 0 or me_as_int > len(accounts):
            sender.reply("❌ 无效的选择")
            return

        if me_as_int == 0:
            batch_auth_guide = """
=====批量授权设置=====
请输入授权月数(如:1)
------------------
回复数字设置月数
回复"q"退出操作
=================="""
            sender.reply(batch_auth_guide)

            mes = sender.input(120000, 1, False)
            if not mes or mes.lower() == 'q':
                sender.reply("✅ 已取消操作")
                return

            try:
                mes = int(mes)
                if mes <= 0:
                    sender.reply("❌ 月数必须大于0")
                    return
            except ValueError:
                sender.reply("❌ 请输入正确的数字")
                return

            total_money = Decimal(mes) * vip_money * len(accounts)

            confirm_msg = f"""
=====批量授权确认=====
📊 账号数量: {len(accounts)}个
⏰ 授权时长: {mes}月/每个账号
💰 总计金额: {total_money}元
------------------
确认批量授权？
[y] 确认授权
[n] 取消操作
=================="""
            sender.reply(confirm_msg)

            confirm = sender.input(60000, 1, False)
            if confirm and confirm.lower() == 'y':
                batch_payment(accounts=accounts, months=mes, total_money=total_money)
            else:
                sender.reply("✅ 已取消批量授权")
        else:
            phone = accounts[me_as_int - 1]
            show_account_menu(phone, accounts)

    except ValueError:
        sender.reply("❌ 无效的选择")


def show_account_menu(phone, accounts):
    """显示账号操作菜单"""
    from decimal import Decimal

    today_time = str(datetime.now().date())
    account_vip = '2099-12-31'
    auth_status, auth_time = get_auth_status(account_vip, today_time)

    menu = f"""
=====账号管理=====
📱 手机号: {mask_phone(phone)}
🔐 授权: {auth_status}
------------------
[1] 授权账号
[2] 刷新Token
[3] 提交青龙
[4] 查询中奖
[5] 删除账号
------------------
回复数字选择功能
回复"q"退出操作
=================="""
    sender.reply(menu)

    choice = sender.input(120000, 1, False)
    if not choice or choice.lower() == 'q':
        return

    account_data = sg.bucketGet('dd_ltyp_token', phone)
    if not account_data:
        sender.reply("❌ 账号信息不存在")
        return
    account_info = json.loads(account_data)

    if choice == '1':
        var_name, ql_config, zsm, vip_money, vip_coin, use_ma_pay = get_full_config()

        auth_guide = """
=====设置授权时长=====
请输入授权月数(如:1)
------------------
回复数字设置月数
回复"q"退出操作
=================="""
        sender.reply(auth_guide)

        mes = sender.input(120000, 1, False)
        if not mes or mes.lower() == 'q':
            sender.reply("✅ 已取消操作")
            return

        try:
            mes = int(mes)
            if mes <= 0:
                sender.reply("❌ 月数必须大于0")
                return
        except ValueError:
            sender.reply("❌ 请输入正确的数字")
            return

        money = Decimal(mes) * vip_money
        token_online = account_info.get('token_online')
        ecs_token = account_info.get('ecs_token')

        process_payment(
            project='联通云盘授权',
            me_as_int=mes,
            account_vip=account_vip or '',
            token=token_online,
            phone=phone,
            account=phone,
            money=money,
            vip_money=vip_money,
            vip_coin=vip_coin,
            ecs_token=ecs_token
        )

    elif choice == '2':
        sender.reply("🔄 正在刷新Token...")
        password = account_info.get('password')
        if not password:
            sender.reply("❌ 未保存密码，无法刷新")
            return

        token_online, error = perform_login(phone, password)
        if token_online:
            account_info['token_online'] = token_online
            account_info['update_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            ecs_token = None
            try:
                import httpx
                async def fetch_ecs_token():
                    async with httpx.AsyncClient(verify=False, timeout=30) as session:
                        _, ecs, _ = await get_ecstoken(session, token_online)
                        return ecs
                ecs_token = asyncio.run(fetch_ecs_token())
                account_info['ecs_token'] = ecs_token
            except Exception as e:
                print(f"获取ecs_token失败: {str(e)}")

            sg.bucketSet('dd_ltyp_token', phone, json.dumps(account_info))

            account_vip = '2099-12-31'
            if account_vip and account_vip > today_time:
                ql_url, ql_token, var_name, ql_format = init_qinglong()
                if ql_url and ql_token:
                    add_to_qinglong(ql_url, ql_token, var_name, token_online, phone, account_info.get('remark', ''), ql_format, ecs_token, account_vip)

            sender.reply(f"""
=====刷新成功=====
📱 手机号: {mask_phone(phone)}
🔑 Token: 已更新
🕐 时间: {account_info['update_time']}
==================""")
        else:
            sender.reply(f"""
=====刷新失败=====
📱 手机号: {mask_phone(phone)}
❌ 原因: {error}
==================""")

    elif choice == '3':
        account_vip = '2099-12-31'
        if not account_vip or account_vip <= today_time:
            sender.reply("❌ 账号未授权或已过期，请先授权")
            return

        ql_url, ql_token, var_name, ql_format = init_qinglong()
        if not ql_url:
            sender.reply("❌ 未配置青龙信息")
            return

        token_online = account_info.get('token_online')
        ecs_token = account_info.get('ecs_token')
        if not token_online:
            sender.reply("❌ 未获取到Token，请先刷新")
            return

        if add_to_qinglong(ql_url, ql_token, var_name, token_online, phone, account_info.get('remark', ''), ql_format, ecs_token, account_vip):
            sender.reply(f"""
=====提交成功=====
📱 手机号: {mask_phone(phone)}
✅ 已同步到青龙
==================""")
        else:
            sender.reply(f"""
=====提交失败=====
📱 手机号: {mask_phone(phone)}
❌ 青龙操作失败
==================""")

    elif choice == '4':
        token_online = account_info.get('token_online')
        if not token_online:
            sender.reply("❌ 未获取到Token，请先刷新")
            return

        result, error = asyncio.run(query_cloud_records(token_online))
        if error:
            sender.reply(f"""
=====查询失败=====
📱 手机号: {mask_phone(phone)}
❌ 原因: {error}
==================""")
            return

        market_records = result.get('market_records', [])
        cloud_records = result.get('cloud_records', [])

        msg = f"""
=====中奖记录=====
📱 手机号: {mask_phone(phone)}
------------------
🎰 权益超市({len(market_records)}条):"""

        if market_records:
            for r in market_records[:5]:
                name = r.get('name', '未知')
                prize_time = r.get('time', '')[:10] if r.get('time') else ''
                status = r.get('status', '')
                msg += f"\n🎁 {name}"
                if status:
                    msg += f" [{status}]"
                if prize_time:
                    msg += f" {prize_time}"
        else:
            msg += "\n暂无记录"

        msg += f"""
------------------
☁️ 云盘抽奖({len(cloud_records)}条):"""

        if cloud_records:
            for r in cloud_records[:5]:
                name = r.get('name', '未知')
                prize_time = r.get('time', '')[:10] if r.get('time') else ''
                msg += f"\n🎁 {name}"
                if prize_time:
                    msg += f" {prize_time}"
        else:
            msg += "\n暂无记录"

        msg += "\n=================="
        sender.reply(msg)

    elif choice == '5':
        confirm = """
=====确认删除=====
⚠️ 此操作不可恢复
------------------
回复 y 确认删除
回复 n 取消操作
=================="""
        sender.reply(confirm)

        confirm_input = sender.input(60000, 1, False)
        if confirm_input and confirm_input.lower() == 'y':
            accounts.remove(phone)
            if accounts:
                sg.bucketSet('dd_ltyp_user', userid, str(accounts))
            else:
                sg.bucketDel('dd_ltyp_user', userid)

            sg.bucketDel('dd_ltyp_token', phone)
            True

            ql_url, ql_token, var_name, ql_format = init_qinglong()
            if ql_url and ql_token:
                delete_from_qinglong(ql_url, ql_token, var_name, phone)

            sender.reply("✅ 账号已删除")
        else:
            sender.reply("✅ 已取消删除")

    else:
        sender.reply("❌ 无效的选择")


def process_payment(project, me_as_int, account_vip, token, phone, account, money, vip_money, vip_coin, ecs_token=None):
    return True
def batch_payment(accounts, months, total_money):
    return True


def query_account():
    """查询账号信息"""
    if not uservalue:
        sender.reply("""
=====未绑定账号=====
❌ 未找到任何账号信息
💡 发送 云盘登录 绑定账号
==================""")
        return

    accounts = _sg_literal(uservalue)
    today_time = str(datetime.now().date())

    account_list_msg = "=====选择查询账号=====\n"
    account_list_msg += "[0] 全部查询\n"

    for idx, phone in enumerate(accounts, 1):
        account_data = sg.bucketGet('dd_ltyp_token', phone)
        account_vip = '2099-12-31'
        auth_status, _ = get_auth_status(account_vip, today_time)

        if account_data:
            account_info = json.loads(account_data)
            remark = account_info.get('remark', phone)
        else:
            remark = phone

        account_list_msg += f"[{idx}] {mask_phone(phone)}\n"

    account_list_msg += "------------------\n"
    account_list_msg += "回复序号选择账号\n"
    account_list_msg += "回复\"q\"退出\n"
    account_list_msg += "=================="
    sender.reply(account_list_msg)

    user_choice = sender.input(60000, 1, False)
    if not user_choice:
        sender.reply("⏰ 操作超时,已退出")
        return
    elif user_choice.lower() == 'q':
        sender.reply("✅ 已取消查询")
        return

    try:
        choice_num = int(user_choice)
        if choice_num < 0 or choice_num > len(accounts):
            sender.reply("❌ 序号无效，请输入正确的序号")
            return
    except ValueError:
        sender.reply("❌ 请输入数字序号")
        return

    if choice_num == 0:
        query_phones = accounts
    else:
        query_phones = [accounts[choice_num - 1]]

    for phone in query_phones:
        account_data = sg.bucketGet('dd_ltyp_token', phone)
        account_vip = '2099-12-31'
        auth_status, auth_time = get_auth_status(account_vip, today_time)

        if not account_data:
            continue

        account_info = json.loads(account_data)
        token_online = account_info.get('token_online')
        remark = account_info.get('remark', phone)

        if not token_online:
            sender.reply(f"""
=====账号信息=====
📱 手机号: {mask_phone(phone)}
👤 备注: {remark}
🔐 授权: {auth_status}
📅 到期: {auth_time}
❌ Token未获取
==================""")
            continue

        result, error = asyncio.run(query_cloud_records(token_online))
        if error:
            sender.reply(f"""
=====账号信息=====
📱 手机号: {mask_phone(phone)}
👤 备注: {remark}
🔐 授权: {auth_status}
📅 到期: {auth_time}
❌ 查询失败: {error}
==================""")
            continue

        market_records = result.get('market_records', [])
        cloud_records = result.get('cloud_records', [])

        sign_telephone = result.get('sign_telephone')
        ttlxj_available = result.get('ttlxj_available')
        woread_balance = result.get('woread_balance')
        watering_progress = result.get('watering_progress')
        cloud_all_score = result.get('cloud_all_score')
        cloud_available_score = result.get('cloud_available_score')

        msg = f"""
=====账号信息=====
📱 手机号: {mask_phone(phone)}
👤 备注: {remark}
📅 到期: {auth_time}
------------------
💰 资产信息:
🔴 话费红包: {f'{sign_telephone:.2f}元' if sign_telephone is not None else '查询失败'}
🟡 阅读红包: {f'{woread_balance:.2f}元' if woread_balance is not None else '查询失败'}
🟢 沃立减金: {f'{ttlxj_available:.2f}元' if ttlxj_available is not None else '查询失败'}
🌸 浇花进度: {watering_progress if watering_progress else '查询失败'}
☁️ 云盘积分: {f'{cloud_available_score}' if cloud_all_score is not None else '查询失败'}
------------------
🎰 权益超市({len(market_records)}条):"""

        if market_records:
            for r in market_records[:5]:
                name = r.get('name', '未知')
                prize_time = r.get('time', '')[:10] if r.get('time') else ''
                status = r.get('status', '')
                msg += f"\n🎁 {name}"
                if status:
                    msg += f" [{status}]"
                if prize_time:
                    msg += f" {prize_time}"
        else:
            msg += "\n暂无记录"

        msg += f"""
------------------
☁️ 云盘抽奖({len(cloud_records)}条):"""

        if cloud_records:
            for r in cloud_records[:3]:
                name = r.get('name', '未知')
                prize_time = r.get('time', '')[:10] if r.get('time') else ''
                msg += f"\n🎁 {name}"
                if prize_time:
                    msg += f" {prize_time}"
        else:
            msg += "\n暂无记录"

        msg += "\n=================="
        sender.reply(msg)


def admin_auth():
    return True
def backend_manage():
    """后台管理功能"""
    if not sender.isAdmin():
        sender.reply("❌ 您没有权限执行此操作!")
        return

    backend_menu = """=====云盘后台管理=====
[1] 清理过期账号
[2] 同步青龙变量
------------------
回复数字选择功能
回复"q"退出
=================="""
    sender.reply(backend_menu)
    xz = sender.listen(60000)

    if xz == 'q' or xz == 'Q':
        sender.reply("✅ 已退出后台管理")
        return
    elif xz is None:
        sender.reply("⏰ 操作超时,已退出")
        return
    elif xz == '1':
        clean_expired_accounts()
    elif xz == '2':
        sync_to_qinglong()
    else:
        sender.reply("❌ 输入错误,请重新选择")
        return


def clean_expired_accounts():
    """清理过期的云盘账号"""
    users = sg.bucketAllKeys('dd_ltyp_user')

    if not users:
        sender.reply("❌ 未找到任何绑定账号")
        return

    sender.reply(f"⏳ 共找到: {len(users)}个用户\n清理中请稍候...")

    cleaned_count = 0
    today_time = str(datetime.now().date())

    for user in users:
        try:
            accountlist = sg.bucketGet('dd_ltyp_user', user)
            if not accountlist:
                continue

            accounts = _sg_literal(accountlist)
            valid_accounts = []

            for account in accounts:
                account_vip = '2099-12-31'

                if not account_vip or account_vip <= today_time:
                    try:
                        ql_url, ql_token, var_name, ql_format = init_qinglong()
                        if ql_url and ql_token:
                            delete_from_qinglong(ql_url, ql_token, var_name, account)
                    except:
                        pass

                    sg.bucketDel('dd_ltyp_token', account)
                    True
                    cleaned_count += 1
                else:
                    valid_accounts.append(account)

            valid_accounts = list(dict.fromkeys(valid_accounts))

            if valid_accounts:
                sg.bucketSet('dd_ltyp_user', user, str(valid_accounts))
            else:
                sg.bucketDel('dd_ltyp_user', user)

        except Exception as e:
            print(f"处理用户 {user} 时出错: {str(e)}")
            continue

    sender.reply(f"""
=====清理完成=====
✅ 已清理: {cleaned_count}个过期账号
==================""")


def sync_to_qinglong():
    """同步已授权账号到青龙"""
    users = sg.bucketAllKeys('dd_ltyp_user')

    if not users:
        sender.reply("❌ 未找到任何绑定账号")
        return

    sender.reply(f"⏳ 共找到: {len(users)}个用户\n同步中请稍候...")

    success_count = 0
    skip_count = 0
    fail_count = 0
    today_time = str(datetime.now().date())

    for user in users:
        try:
            accountlist = sg.bucketGet('dd_ltyp_user', user)
            if not accountlist:
                continue

            accounts = _sg_literal(accountlist)

            for account in accounts:
                try:
                    account_vip = '2099-12-31'

                    if not account_vip or account_vip <= today_time:
                        skip_count += 1
                        continue

                    account_data = sg.bucketGet('dd_ltyp_token', account)
                    account_json = json.loads(account_data) if account_data else {}
                    token = account_json.get('token_online')
                    ecs_token = account_json.get('ecs_token')
                    if not token:
                        fail_count += 1
                        continue

                    ql_url, ql_token, var_name, ql_format = init_qinglong()
                    if ql_url and ql_token:
                        add_to_qinglong(ql_url, ql_token, var_name, token, account, '', ql_format, ecs_token, account_vip)
                    success_count += 1

                except Exception as e:
                    print(f"同步账号 {account} 失败: {str(e)}")
                    fail_count += 1
                    continue

        except Exception as e:
            print(f"处理用户 {user} 时出错: {str(e)}")
            continue

    result_msg = f"""=====同步完成=====
✅ 成功同步: {success_count}个账号
⏭️ 跳过未授权: {skip_count}个账号
❌ 同步失败: {fail_count}个账号
=================="""
    sender.reply(result_msg)


def show_tutorial():
    """显示云盘插件使用教程"""
    tutorial = """📚 联通云盘插件教程

🔰 基础功能指令:
1️⃣ 联通云盘登录 - 绑定联通云盘账号(账密登录)
2️⃣ 联通云盘查询 - 查看账号中奖记录
3️⃣ 联通云盘管理 - 管理已绑定账号([0]批量授权 [1-N]单个账号)

🔧 管理员功能:
• 云盘授权 - 管理员授权用户
• 云盘后台 - 清理过期账号/同步青龙

💡 授权说明:
• 选择[0]可批量授权所有账号
• 自动计算总金额和所需积分
• 支持微信、在线处理、积分支付

⚠️ 注意事项:
1. 首次使用请先登录绑定
2. 定期查看账号状态
3. 及时处理授权到期
4. 登录格式: 手机号#密码#备注"""
    sender.reply(tutorial)


def main():
    """主函数"""
    message = sender.getMessage()

    if '联通云盘登录' in message or '联通云盘登陆' in message:
        bind_account()
    elif '联通云盘管理' in message:
        manage_account()
    elif '联通云盘查询' in message:
        query_account()
    elif message == '联通云盘授权':
        admin_auth()
    elif message == '联通云盘后台':
        backend_manage()
    elif message == '联通云盘教程':
        show_tutorial()
    else:
        sender.setContinue()


if __name__ == "__main__":
    try:
        imtype = sender.getImtype()
        main()
    except Exception as e:
        sender.reply(f"❌ 运行出错: {str(e)}")
