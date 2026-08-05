# [title: 新江北]
# [name: xinJiangBei]
# [language: python]
# [class: 任务]
# [author: rujingxianghai]
# [version: v1.1.3]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(新江北|xjb)(登录|登陆)$|^登(录|陆)(新江北|xjb)$|^(新江北|xjb)(查询|管理)$|^(查询|管理)(新江北|xjb)$|^新江北清理$|^新江北检测$|^新江北$|^新江北教程$]
# [icon: https://api.iconify.design/lucide:apple.svg]
# [description: 1.0.0：基础版本]
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
    's_xjb_config_xjb_qlname': form.string().title('设置对接容器').default('').description('你的变量需要添加到的容器？参数用丨分割'),
    's_xjb_config_xjb_osname': form.string().title('提交到青龙的变量名').default('').description('青龙容器内新江北的变量名'),
    's_xjb_config_notify': form.string().title('通知渠道').default('').description('检测功能的通知渠道，多个渠道用逗号分隔'),
})
_CONFIG_FIELD_MAP = {
    ('s_xjb_config', 'xjb_qlname'): 's_xjb_config_xjb_qlname',
    ('s_xjb_config', 'xjb_osname'): 's_xjb_config_xjb_osname',
    ('s_xjb_config', 'notify'): 's_xjb_config_notify',
}

import os
import json
import time
import random
import requests
from datetime import datetime
import hashlib
import hmac
import base64
import uuid
from urllib.parse import quote
import re
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()
uservalue = sg.bucketGet(bucket='s_xjb_user', key=userid)


PLUGIN_CONFIG = {
    'bucket': 's_xjb_config',
    'coin_key': 'dd_sign_points',
    'name': '新江北'
}

PAYMENT_CONFIG = {
    'zsm': sg.bucketGet('s_xjb_config', 'zsm') or '',  # 赞赏码链接
    'ma_pay_switch': '2099-12-31' or 'false',  # 在线处理开关
    'ma_pay_gateway': '2099-12-31' or '',  # 从卡密系统获取支付网关
    'ma_pay_pid': '2099-12-31' or '',  # 从卡密系统获取商户ID
    'ma_pay_key': '2099-12-31' or '',  # 从卡密系统获取商户密钥
    'ma_pay_type': '2099-12-31' or 'alipay,wxpay',  # 从卡密系统获取支付方式
    'ma_pay_notify_url': '2099-12-31' or 'http://localhost/notify',  # 从卡密系统获取异步通知地址
    'ma_pay_return_url': '2099-12-31' or 'http://localhost/return',  # 从卡密系统获取跳转通知地址
    'pid': '',  # 将在后面初始化
    'key': '',  # 将在后面初始化
    'gateway': '',  # 将在后面初始化
    'notify_url': '',  # 将在后面初始化
    'return_url': ''  # 将在后面初始化
}

PAYMENT_CONFIG['pid'] = PAYMENT_CONFIG['ma_pay_pid']
PAYMENT_CONFIG['key'] = PAYMENT_CONFIG['ma_pay_key']
PAYMENT_CONFIG['gateway'] = PAYMENT_CONFIG['ma_pay_gateway']
PAYMENT_CONFIG['notify_url'] = PAYMENT_CONFIG['ma_pay_notify_url']
PAYMENT_CONFIG['return_url'] = PAYMENT_CONFIG['ma_pay_return_url']

PAY_TYPE_NAMES = {
    'alipay': '支付宝',
    'wxpay': '微信支付',
    'qqpay': 'QQ钱包',
}

payment_status = {}

A = "102"  # X-TENANT-ID
B = "10050"  # client_id
C = "FR*r!isE5W"  # 签名密钥

def get_user_content():
    """获取用户配置内容"""
    xjb_osname = sg.bucketGet('s_xjb_config', 'xjb_osname') or 'S_XJB'
    xjb_qlname = sg.bucketGet('s_xjb_config', 'xjb_qlname') or ''
    xjb_managecommand = sg.bucketGet('s_xjb_config', 'xjb_managecommand') or '新江北管理'
    xjb_querycommand = sg.bucketGet('s_xjb_config', 'xjb_querycommand') or '新江北查询'
    xjb_signcommand = sg.bucketGet('s_xjb_config', 'xjb_signcommand') or '新江北登录'

    randommanagecommand = xjb_managecommand
    randomquerycommand = xjb_querycommand
    randomsigncommand = xjb_signcommand

    xjbVipmoney = float(sg.bucketGet('s_xjb_config', 'xjbVipmoney') or '1')

    xjbcoin = sg.bucketGet(PLUGIN_CONFIG['bucket'], PLUGIN_CONFIG['coin_key'])
    if not xjbcoin:
        xjbcoin = sg.bucketGet('s_xjb_config', 'xjbcoin') or '0'
    xjbcoin = int(xjbcoin)

    return (xjb_osname, xjb_qlname, randommanagecommand,
            randomquerycommand, randomsigncommand, xjbVipmoney, xjbcoin)

def mask_phone(phone):
    """手机号脱敏处理"""
    if not phone or len(phone) != 11:
        return phone
    return f"{phone[:3]}****{phone[7:]}"

def get_random_user_agent():
    """获取随机UA"""
    backup_ua_list = [
        'Mozilla/5.0 (Linux; Android 15; 2210132C Build/AQ3A.240812.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/135.0.7049.37 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 14; Pixel 6 Build/UQ1A.240605.004; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/133.0.6638.41 Mobile Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1'
    ]
    return random.choice(backup_ua_list)

def generate_uuid():
    """生成UUID"""
    return str(uuid.uuid4())

def generate_device_info():
    """生成设备信息"""
    version = "1.7.0"
    device_uuid = generate_uuid()

    devices = [
        "M1903F2A", "M2001J2E", "M2001J2C", "M2001J1E", "M2001J1C",
        "M2002J9E", "M2011K2C", "M2102K1C", "M2101K9C", "2107119DC",
        "2201123C", "2112123AC", "2201122C", "2211133C", "2210132C",
        "2304FPN6DC", "23127PN0CC", "24031PN0DC", "23090RA98C",
        "2312DRA50C", "2312CRAD3C", "2312DRAABC", "22101316UCP", "22101316C"
    ]

    device = random.choice(devices)
    device_name = f"Xiaomi {device}"
    android_version = "11"
    os_name = "Android"

    ua = f"{os_name.upper()};{android_version};{B};{version};1.0;null;{device}"
    common_ua = f"{version};{device_uuid};{device_name};{os_name};{android_version};6.9.0"

    return ua, common_ua, device_uuid

def get_signature(path, session_id="", request_uuid=""):
    """生成API签名"""
    timestamp = int(time.time() * 1000)
    if not request_uuid:
        request_uuid = generate_uuid()

    if "?" in path:
        path = path.split("?")[0]

    sign_string = f"{path}&&{session_id}&&{request_uuid}&&{timestamp}&&{C}&&{A}"

    signature = hashlib.sha256(sign_string.encode()).hexdigest()

    return {
        'uuid': request_uuid,
        'timestamp': timestamp,
        'signature': signature
    }

def get_passport_signature(body_params, signature_key, request_uuid=""):
    """生成passport API签名"""
    if not request_uuid:
        request_uuid = generate_uuid()

    sign_string = f"post%%/web/oauth/credential_auth?{body_params}%%{request_uuid}%%"

    signature = hmac.new(
        signature_key.encode(),
        sign_string.encode(),
        hashlib.sha256
    ).hexdigest()

    return {
        'uuid': request_uuid,
        'signature': signature
    }

def encrypt_password(password):
    """使用RSA加密密码"""
    try:
        public_key_str = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQD6XO7e9YeAOs+cFqwa7ETJ+WXi
zPqQeXv68i5vqw9pFREsrqiBTRcg7wB0RIp3rJkDpaeVJLsZqYm5TW7FWx/iOiXF
c+zCPvaKZric2dXCw27EvlH5rq+zwIPDAJHGAfnn1nmQH7wR3PCatEIb8pz5GFlT
HMlluw4ZYmnOwg+thwIDAQAB
-----END PUBLIC KEY-----"""

        public_key = RSA.importKey(public_key_str)
        cipher = PKCS1_v1_5.new(public_key)

        encrypted_password = cipher.encrypt(password.encode('utf-8'))
        encrypted_password_b64 = base64.b64encode(encrypted_password).decode('utf-8')

        return encrypted_password_b64
    except Exception as e:
        print(f"❌ RSA加密失败: {e}")
        return password  # 如果加密失败，返回原始密码

def request_passport_api(path, ua):
    """请求passport API"""
    url = f"https://passport.tmuyun.com{path}"

    headers = {
        "Connection": "Keep-Alive",
        "Cache-Control": "no-cache",
        "X-REQUEST-ID": generate_uuid(),
        "Accept-Encoding": "gzip",
        "user-agent": ua
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        return response.json()
    except Exception as e:
        print(f"❌ passport API请求失败: {e}")
        return None

def request_passport_post(path, data, ua, signature_key):
    """发送passport POST请求"""
    url = f"https://passport.tmuyun.com{path}"

    sig_info = get_passport_signature(data, signature_key)

    headers = {
        "Connection": "Keep-Alive",
        "X-REQUEST-ID": sig_info['uuid'],
        "X-SIGNATURE": sig_info['signature'],
        "Cache-Control": "no-cache",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Accept-Encoding": "gzip",
        "user-agent": ua
    }

    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        return response.json()
    except Exception as e:
        print(f"❌ passport POST请求失败: {e}")
        return None

def request_vapp_api(path, session_id, account_id, common_ua, method='GET', data=None):
    """请求vapp API"""
    url = f"https://vapp.tmuyun.com{path}"

    sig_info = get_signature(path, session_id)

    headers = {
        "Connection": "Keep-Alive",
        "X-TIMESTAMP": str(sig_info['timestamp']),
        "X-SESSION-ID": session_id,
        "X-REQUEST-ID": sig_info['uuid'],
        "X-SIGNATURE": sig_info['signature'],
        "X-TENANT-ID": A,
        "X-ACCOUNT-ID": account_id,
        "Cache-Control": "no-cache",
        "Accept-Encoding": "gzip",
        "user-agent": common_ua
    }

    if method.upper() == 'POST':
        headers["Content-Type"] = "application/x-www-form-urlencoded;charset=UTF-8"

    try:
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers, timeout=10)
        else:
            if data is None:
                data = ""
            response = requests.post(url, headers=headers, data=data, timeout=10)

        time.sleep(1)  # 避免请求过快
        return response.json()
    except Exception as e:
        print(f"❌ API请求失败: {e}")
        return None

def get_user_info(account_info):
    """获取用户信息和积分"""
    try:
        phone = account_info.get('phone', '')
        password = account_info.get('password', '')

        if not phone or not password:
            return {"success": False, "message": "账号信息不完整"}

        ua, common_ua, device_uuid = generate_device_info()

        result = request_vapp_api("/api/account/init", "", "", common_ua, 'POST')
        if not result or not result.get('data') or not result['data'].get('session'):
            return {"success": False, "message": "获取sessionId失败"}

        session_id = result['data']['session']['id']

        result = request_passport_api(f"/web/init?client_id={B}", ua)
        if not result or not result.get('data') or not result['data'].get('client'):
            return {"success": False, "message": "获取signature_key失败"}

        signature_key = result['data']['client']['signature_key']

        encrypted_password = encrypt_password(password)

        encoded_password = quote(encrypted_password)

        data = f"client_id={B}&password={encoded_password}&phone_number={phone}"

        result = request_passport_post("/web/oauth/credential_auth", data, ua, signature_key)
        if not result or not result.get('data') or not result['data'].get('authorization_code'):
            return {"success": False, "message": f"获取授权码失败: {result.get('message', '未知错误')}"}

        auth_code = result['data']['authorization_code']['code']

        data = f"check_token=&code={auth_code}&token=&type=-1&union_id="
        result = request_vapp_api("/api/zbtxz/login", session_id, "", common_ua, 'POST', data)

        if not result or not result.get('data') or not result['data'].get('session'):
            return {"success": False, "message": "登录失败"}

        account_id = result['data']['session']['account_id']
        session_id = result['data']['session']['id']

        result = request_vapp_api("/api/user_mumber/account_detail", session_id, account_id, common_ua)

        if result and result.get('data') and result['data'].get('rst'):
            integral = result['data']['rst'].get('total_integral', 0)
            return {
                "success": True,
                "integral": str(integral),
                "account_id": account_id,
                "session_id": session_id
            }
        else:
            return {"success": False, "message": "查询积分失败"}

    except Exception as e:
        return {"success": False, "message": str(e)}

def bind_account():
    """绑定新江北账号"""
    phone_guide_lines = [
        "请输入手机号码",
        "------------------",
        "回复\"q\"退出操作"
    ]
    sender.reply(format_message("账号绑定", phone_guide_lines))

    phone = sender.input(120000, 1, False)
    if not phone or phone.lower() == 'q':
        sender.reply("✅ 已取消绑定")
        return None

    if not phone.isdigit() or len(phone) != 11:
        sender.reply("❌ 手机号格式错误，请输入11位数字")
        return None

    password_guide_lines = [
        f"📱 手机号: {mask_phone(phone)}",
        "------------------",
        "请输入密码",
        "回复\"q\"退出操作"
    ]
    sender.reply(format_message("输入密码", password_guide_lines))

    password = sender.input(120000, 1, False)
    if not password or password.lower() == 'q':
        sender.reply("✅ 已取消绑定")
        return None

    alipay_name_guide_lines = [
        f"📱 手机号: {mask_phone(phone)}",
        "------------------",
        "请输入支付宝姓名",
        "💡 提示: 填写支付宝实名姓名",
        "回复\"q\"退出操作"
    ]
    sender.reply(format_message("输入支付宝姓名", alipay_name_guide_lines))

    alipay_name = sender.input(120000, 1, False)
    if not alipay_name or alipay_name.lower() == 'q':
        sender.reply("✅ 已取消绑定")
        return None

    alipay_account_guide_lines = [
        f"📱 手机号: {mask_phone(phone)}",
        "------------------",
        "请输入支付宝账号",
        "💡 提示: 可以是手机号或邮箱",
        "回复\"q\"退出操作"
    ]
    sender.reply(format_message("输入支付宝账号", alipay_account_guide_lines))

    alipay_account = sender.input(120000, 1, False)
    if not alipay_account or alipay_account.lower() == 'q':
        sender.reply("✅ 已取消绑定")
        return None

    session_id_guide_lines = [
        f"📱 手机号: {mask_phone(phone)}",
        f"💳 支付宝账号: {alipay_account}",
        "------------------",
        "请输入SessionID（可选）",
        "💡 提示: 留空可自动获取",
        "直接回复\"n\"跳过",
        "回复\"q\"退出操作"
    ]
    sender.reply(format_message("输入SessionID（可选）", session_id_guide_lines))

    session_id = sender.input(120000, 1, False)
    if session_id and session_id.lower() == 'q':
        sender.reply("✅ 已取消绑定")
        return None

    if session_id.strip() == "n":
        session_id = ""

    sender.reply("🔄 正在验证账号...")
    account_info = {
        'phone': phone,
        'password': password,
        'alipay_name': alipay_name,
        'alipay_account': alipay_account,
        'session_id': session_id  # 添加sessionid字段
    }

    login_info = {
        'phone': phone,
        'password': password
    }

    user_info = get_user_info(login_info)
    if not user_info.get("success"):
        sender.reply(f"❌ 账号验证失败: {user_info.get('message', '未知错误')}")
        return None

    if not uservalue:
        sg.bucketSet('s_xjb_user', userid, str([phone]))
    else:
        accounts = _sg_literal(uservalue)
        if phone not in accounts:
            accounts.append(phone)
            sg.bucketSet('s_xjb_user', userid, str(accounts))

    sg.bucketSet('s_xjb_token', phone, json.dumps(account_info))

    success_lines = [
        f"📱 手机号: {mask_phone(phone)}",
        f"💳 支付宝账号: {alipay_account}",
        f"💰 积分: {user_info.get('integral', '0')}"
    ]

    if session_id:
        success_lines.append(f"🔑 SessionID: {session_id[:20]}...")
    else:
        success_lines.append("🔑 SessionID: 自动获取")

    sender.reply(format_message("绑定成功", success_lines))

    dqsj = datetime.now().strftime("%Y-%m-%d")
    accountVip = '2099-12-31'  # 使用手机号作为key

    if accountVip and accountVip > dqsj:
        ql_result = update_ql_env(phone, account_info)
        auth_result = f"""
=====账号已授权=====
📱 手机号: {mask_phone(phone)}
💰 积分: {user_info.get('integral', '0')}
📅 到期时间: {accountVip}
------------------
🔄 青龙更新: {'成功' if ql_result else '失败'}
=================="""
        sender.reply(auth_result)
    else:
        auth_guide = """
=====授权提示=====
❓ 是否需要立即授权账号？
------------------
[1] 立即授权
[2] 暂不授权
------------------
回复数字选择
=================="""
        sender.reply(auth_guide)

        choice = sender.input(120000, 1, False)
        if choice == '1':
            authorize_account(phone, account_info)
        else:
            sender.reply("""
=====提示=====
✅ 账号已绑定成功
❗ 您可以稍后使用"新江北管理"命令进行授权
==================""")

def query_accounts():
    """查询账号信息"""
    if not uservalue:
        sender.reply(format_message("未绑定账号", [
            "❌ 未找到任何账号信息",
            f"💡 发送 新江北登录 绑定"
        ]))
        return

    accounts = _sg_literal(uservalue)
    account_list_lines = ["[0] 全部账号"]

    for i, account in enumerate(accounts, 1):
        account_info_str = sg.bucketGet('s_xjb_token', account)
        if not account_info_str:
            continue

        auth_time = '2099-12-31'

        if not auth_time:
            auth_status = '未授权'
        elif auth_time < str(datetime.now().date()):
            auth_status = '已过期'
        else:
            auth_status = f'{auth_time}'

        account_list_lines.append(f"[{i}]{mask_phone(account)}({auth_status})")

    account_list_lines.append("=====================")
    account_list_lines.append("支持多选，用英文逗号分隔")
    account_list_lines.append("例如: 1,2,3")
    account_list_lines.append("回复\"q\"退出操作")
    account_list_lines.append("=====================")

    sender.reply(format_message("选择账号", account_list_lines))

    choice = sender.input(120000, 1, False)
    if not choice or choice.lower() == 'q':
        sender.reply("✅ 已退出查询")
        return

    try:
        selected_accounts = []

        if choice == '0':
            selected_accounts = accounts.copy()
        else:
            indices = choice.split(',')
            for idx in indices:
                idx = idx.strip()
                if not idx.isdigit():
                    continue

                index = int(idx) - 1
                if 0 <= index < len(accounts):
                    selected_accounts.append(accounts[index])

        if not selected_accounts:
            sender.reply("❌ 未选择有效账号")
            return

        sender.reply(f"✅ 已选择 {len(selected_accounts)} 个账号，正在查询...")

        query_count = 0
        for account in selected_accounts:
            try:
                account_info_str = sg.bucketGet('s_xjb_token', account)
                if not account_info_str:
                    sender.reply(show_error("账号不存在", "未找到账号信息", f"📱 账号: {account}"))
                    continue

                account_info = json.loads(account_info_str)

                user_info = get_user_info(account_info)
                if not user_info.get("success"):
                    sender.reply(show_error("获取信息失败", user_info.get("message", "未知错误"), f"📱 账号: {account}"))
                    continue

                auth_time = '2099-12-31'
                if not auth_time:
                    auth_status = '到期: 未授权'
                elif auth_time < str(datetime.now().date()):
                    auth_status = '到期: 已过期'
                else:
                    auth_status = f'到期: {auth_time}'

                info_lines = [
                    f"📱 账号: {mask_phone(account)}",
                    f"💰 积分: {user_info.get('integral', '0')}",
                    f"📅 {auth_status}"
                ]

                try:
                    account_info.get('alipay_name', '')
                    alipay_account = account_info.get('alipay_account', '')
                    session_id = account_info.get('session_id', '')

                    if alipay_account:
                        if '@' in alipay_account:  # 邮箱格式
                            masked_alipay = alipay_account[:3] + '***' + alipay_account[alipay_account.find('@'):]
                        elif len(alipay_account) == 11:  # 手机号格式
                            masked_alipay = mask_phone(alipay_account)
                        else:
                            masked_alipay = alipay_account[:3] + '***'
                        info_lines.append(f"💳 支付宝账号: {masked_alipay}")

                    if session_id:
                        info_lines.append(f"🔑 SessionID: {session_id[:20]}...")
                    else:
                        info_lines.append("🔑 SessionID: 未绑定")

                except Exception:
                    pass  # 如果获取信息出错，不影响其他信息显示

                try:
                    red_packet_result = get_red_packet_details(user_info)
                    if red_packet_result.get("success") and red_packet_result.get("data") and red_packet_result["data"].get("records"):
                        records = red_packet_result["data"]["records"]
                        if records:
                            red_packet_details = format_red_packet_details(records)
                            info_lines.append("-------------------")
                            info_lines.extend(red_packet_details)
                except Exception as e:
                    print(f"获取红包明细失败: {str(e)}")

                sender.reply(format_message(f"账号信息[{query_count+1}/{len(selected_accounts)}]", info_lines))
                query_count += 1

                if query_count < len(selected_accounts) and len(selected_accounts) > 3:
                    time.sleep(0.5)

            except Exception as e:
                sender.reply(show_error(f"查询异常[{query_count+1}/{len(selected_accounts)}]", str(e), f"📱 账号: {account}"))
                query_count += 1

    except Exception as e:
        sender.reply(f"❌ 查询失败: {str(e)}")

def format_message(title, content_lines):
    """
    格式化消息，统一处理消息格式
    title: 消息标题
    content_lines: 消息内容行的列表
    """
    message = f"""
====={title}=====
"""
    for line in content_lines:
        message += f"{line}\n"
    return message

def show_error(title, error_msg, extra_info=None):
    """显示统一格式的错误消息"""
    content = [f"❌ {error_msg}"]
    if extra_info:
        content.append("------------------")
        if isinstance(extra_info, list):
            content.extend(extra_info)
        else:
            content.append(extra_info)

    return format_message(title, content)

def get_ql_config():
    """获取青龙配置信息"""
    try:
        qlconfig = sg.bucketGet('s_xjb_config', 'xjb_qlname')
        if not qlconfig:
            return {"code": 400, "msg": "未配置青龙信息", "data": None}

        qlconfig = qlconfig.replace('|', '丨')
        configs = qlconfig.split('丨')
        if len(configs) < 3:
            return {"code": 400, "msg": "青龙配置格式错误", "data": None}

        return {
            "code": 200,
            "msg": "获取成功",
            "data": {
                "url": configs[0].strip(),
                "client_id": configs[1].strip(),
                "client_secret": configs[2].strip()
            }
        }
    except Exception as e:
        return {"code": 500, "msg": f"获取青龙配置发生异常: {str(e)}", "data": None}

def get_ql_token(host, client_id, client_secret):
    """获取青龙 token"""
    try:
        url = f'{host}/open/auth/token?client_id={client_id}&client_secret={client_secret}'
        response = requests.get(url, timeout=10)
        data = response.json()
        if data.get('code') == 200 and data.get('data') and data['data'].get('token'):
            return data['data']['token']
        else:
            print(f"获取青龙token失败: {data.get('message', '未知错误')}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"请求青龙token异常: {str(e)}")
        return None
    except Exception as e:
        print(f"获取青龙token异常: {str(e)}")
        return None

def update_ql_env(phone, account_info):
    """更新青龙环境变量"""
    try:
        print(f"开始更新青龙变量: {phone}")

        ql_config = get_ql_config()
        if ql_config['code'] != 200:
            print(f"获取青龙配置失败: {ql_config['msg']}")
            return False

        host = ql_config['data'].get('url', '')
        client_id = ql_config['data'].get('client_id', '')
        client_secret = ql_config['data'].get('client_secret', '')

        if not host or not client_id or not client_secret:
            print("青龙配置信息不完整")
            return False

        print(f"青龙地址: {host}")

        token = get_ql_token(host, client_id, client_secret)
        if not token:
            print("获取青龙token失败")
            return False

        print("青龙token获取成功")

        env_name = sg.bucketGet('s_xjb_config', 'xjb_osname') or 'S_XJB'
        print(f"变量名: {env_name}")

        password = account_info.get('password', '')
        alipay_name = account_info.get('alipay_name', '')
        alipay_account = account_info.get('alipay_account', '')
        session_id = account_info.get('session_id', '')  # 可选的sessionid

        if not password:
            print(f"账号信息不完整: {phone}")
            return False

        if session_id:
            value = f"{phone}#{password}#{alipay_name}#{alipay_account}#{session_id}"
            print(f"变量值: {phone}#***#{alipay_name}#{alipay_account[:3] if alipay_account else ''}***#{session_id[:20] if session_id else ''}...")
        else:
            value = f"{phone}#{password}#{alipay_name}#{alipay_account}"
            print(f"变量值: {phone}#***#{alipay_name}#{alipay_account[:3] if alipay_account else ''}***")

        auth_time = '2099-12-31' or '未授权'
        remark = f"新江北:{phone}丨到期:{auth_time}"
        print(f"变量备注: {remark}")

        headers = {'Authorization': f'Bearer {token}'}

        try:
            print("正在获取环境变量列表...")
            response = requests.get(f'{host}/open/envs', headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"获取环境变量失败: {response.text}")
                return False

            envs = response.json().get('data', [])
            if not envs:
                envs = []  # 确保envs不为None
            print(f"找到 {len(envs)} 个环境变量")
            env_id = None

            for env in envs:
                if not env:  # 跳过None或空值
                    continue
                env_remarks = env.get('remarks', '') or ''  # 确保不为None
                env_name_val = env.get('name', '') or ''    # 确保不为None
                if env_name_val == env_name and f"新江北:{phone}" in env_remarks:
                    env_id = env.get('_id') or env.get('id')
                    print(f"找到已存在的变量，ID: {env_id}")
                    break

            env_data = {
                "name": env_name,
                "value": value,
                "remarks": remark
            }

            if env_id:
                print("正在更新已存在的变量...")
                env_data["id"] = env_id
                response = requests.put(f'{host}/open/envs', headers=headers, json=env_data, timeout=10)
                if response.status_code != 200:
                    print(f"更新环境变量失败: {response.text}")
                    return False

                try:
                    requests.put(f'{host}/open/envs/enable', headers=headers, json=[env_id], timeout=10)
                    print("变量已启用")
                except Exception as e:
                    print(f"启用变量异常: {str(e)}")
            else:
                print("正在添加新变量...")
                response = requests.post(f'{host}/open/envs', headers=headers, json=[env_data], timeout=10)
                if response.status_code != 200:
                    print(f"添加环境变量失败: {response.text}")
                    return False

                result = response.json()
                print(f"添加变量响应: {result}")
                if result.get('code') == 200:
                    new_id = None
                    if result.get('data') and len(result['data']) > 0:
                        new_id = result['data'][0].get('_id') or result['data'][0].get('id')
                    if new_id:
                        try:
                            requests.put(f'{host}/open/envs/enable', headers=headers, json=[new_id], timeout=10)
                            print("新变量已启用")
                        except Exception as e:
                            print(f"启用变量异常: {str(e)}")
                else:
                    print(f"添加变量失败，响应码: {result.get('code')}")
                    return False

            print(f"青龙变量更新成功: {phone}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"请求青龙API异常: {str(e)}")
            return False
    except Exception as e:
        print(f"更新青龙变量异常: {str(e)}")
        return False

def delete_ql_env(phone):
    """删除青龙环境变量"""
    try:
        env_name = sg.bucketGet('s_xjb_config', 'xjb_osname') or 'S_XJB'

        ql_config = get_ql_config()
        if ql_config['code'] != 200:
            print(ql_config['msg'])
            return False

        host = ql_config['data'].get('url', '')
        client_id = ql_config['data'].get('client_id', '')
        client_secret = ql_config['data'].get('client_secret', '')

        if not host or not client_id or not client_secret:
            print("青龙配置信息不完整")
            return False

        token = get_ql_token(host, client_id, client_secret)
        if not token:
            print("获取青龙token失败")
            return False

        headers = {'Authorization': f'Bearer {token}'}
        try:
            response = requests.get(f'{host}/open/envs', headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"获取环境变量失败: {response.text}")
                return False

            envs = response.json().get('data', [])

            deleted = False
            for env in envs:
                if not env:  # 跳过None或空值
                    continue
                env_remarks = env.get('remarks', '') or ''  # 确保不为None
                env_name_val = env.get('name', '') or ''    # 确保不为None
                if env_name_val == env_name and f"新江北:{phone}" in env_remarks:
                    env_id = env.get('_id') or env.get('id')
                    if not env_id:
                        continue

                    try:
                        response = requests.delete(
                            f'{host}/open/envs',
                            headers=headers,
                            json=[env_id],
                            timeout=10
                        )
                        if response.status_code == 200:
                            deleted = True
                            print(f"删除青龙变量成功: {env_id}")
                        else:
                            print(f"删除青龙变量失败: {response.text}")
                    except Exception as e:
                        print(f"删除变量请求异常: {str(e)}")

            return deleted
        except requests.exceptions.RequestException as e:
            print(f"请求青龙API异常: {str(e)}")
            return False
    except Exception as e:
        print(f"删除青龙变量异常: {str(e)}")
        return False

def manage_account():
    """账号管理功能"""
    if not uservalue:
        sender.reply(format_message("未绑定账号", [
            "❌ 未找到任何账号信息",
            f"💡 发送 新江北登录 绑定"
        ]))
        return

    accounts = _sg_literal(uservalue)

    menu_lines = [
        "[1] 授权账号",
        "[2] 删除账号",
        "[3] 提交青龙",
        "[4] 更新支付宝信息",
        "[5] 更新SessionID",
        "------------------",
        "回复数字选择功能",
        "回复\"q\"退出操作"
    ]
    sender.reply(format_message("账号管理", menu_lines))

    choice = sender.input(120000, 1, False)
    if not choice or choice.lower() == 'q':
        sender.reply("✅ 已退出操作")
        return

    account_list_lines = ["[0] 全部账号"]

    for i, account in enumerate(accounts, 1):
        account_info_str = sg.bucketGet('s_xjb_token', account)
        if not account_info_str:
            continue

        auth_time = '2099-12-31'

        if not auth_time:
            auth_status = '未授权'
        elif auth_time < str(datetime.now().date()):
            auth_status = '已过期'
        else:
            auth_status = f'{auth_time}'

        account_list_lines.append(f"[{i}]{mask_phone(account)}({auth_status})")

    account_list_lines.extend([
        "=====================",
        "支持多选，用英文逗号分隔",
        "例如: 1,2,3",
        "回复\"q\"退出操作"
    ])

    sender.reply(format_message("选择账号", account_list_lines))

    account_choice = sender.input(120000, 1, False)
    if not account_choice or account_choice.lower() == 'q':
        sender.reply("✅ 已退出操作")
        return

    try:
        selected_accounts = []

        if account_choice == '0':
            selected_accounts = accounts.copy()
        else:
            indices = account_choice.split(',')
            for idx in indices:
                idx = idx.strip()
                if not idx.isdigit():
                    continue

                index = int(idx) - 1
                if 0 <= index < len(accounts):
                    selected_accounts.append(accounts[index])

        if not selected_accounts:
            sender.reply("❌ 未选择有效账号")
            return

        sender.reply(f"✅ 已选择 {len(selected_accounts)} 个账号")

        if choice == '1':
            authorize_multiple_accounts(selected_accounts)

        elif choice == '2':
            confirm_lines = [
                "⚠️ 此操作不可恢复",
                "------------------",
                "回复 y 确认删除",
                "回复 n 取消操作"
            ]
            sender.reply(format_message("确认删除", confirm_lines))

            confirm = sender.input(120000, 1, False)
            if confirm.lower() == 'y':
                success_count = 0
                for account in selected_accounts:
                    try:
                        if account in accounts:
                            accounts.remove(account)

                        sg.bucketDel('s_xjb_token', account)
                        True

                        delete_ql_env(account)
                        success_count += 1
                    except Exception as e:
                        print(f"删除账号失败: {account}, 错误: {str(e)}")

                if accounts:
                    sg.bucketSet('s_xjb_user', userid, str(accounts))
                else:
                    sg.bucketDel('s_xjb_user', userid)

                sender.reply(f"✅ 已成功删除 {success_count}/{len(selected_accounts)} 个账号")
            else:
                sender.reply("✅ 已取消删除")

        elif choice == '3':
            success_count = 0
            for account in selected_accounts:
                try:
                    account_info_str = sg.bucketGet('s_xjb_token', account)
                    if not account_info_str:
                        continue

                    account_info = json.loads(account_info_str)

                    auth_time = '2099-12-31'
                    if auth_time and auth_time >= str(datetime.now().date()):
                        if update_ql_env(account, account_info):
                            success_count += 1
                    else:
                        print(f"账号未授权或已过期: {account}")
                except Exception as e:
                    print(f"提交青龙失败: {account}, 错误: {str(e)}")

            result_lines = [
                f"📊 选择账号: {len(selected_accounts)}个",
                f"✅ 提交成功: {success_count}个",
                f"❌ 提交失败: {len(selected_accounts) - success_count}个",
                "------------------",
                "💡 提示: 未授权账号无法提交"
            ]
            sender.reply(format_message("提交结果", result_lines))
        elif choice == '4':
            update_alipay_info(selected_accounts)
        elif choice == '5':
            update_session_id(selected_accounts)
        else:
            sender.reply("❌ 无效的选择")

    except Exception as e:
        sender.reply(f"❌ 操作失败: {str(e)}")

def show_tutorial():
    """显示新江北教程"""
    tutorial_url = sg.bucketGet('s_xjb_config', 'tutorial_url') or 'https://example.com/tutorial'

    tutorial = f"""
=====新江北使用教程=====
🔍 基础功能:
1. 新江北登录 - 绑定账号
2. 新江北查询 - 查看账号信息
3. 新江北管理 - 管理绑定账号
==================
⚠️ 注意事项:
• 账号失效请及时更新
• 请勿泄露账号信息
==================
💡 登录方式:
• 账号密码登录 - 使用手机号和密码登录
==================
❓ 遇到问题请检查配置
=================="""
    sender.reply(tutorial)

class MaPay_Api:
    def __init__(self, config):
        """初始化在线处理API类"""
        self.config = config
        self.pay_type_names = {
            'alipay': '支付宝',
            'wxpay': '微信支付',
            'qqpay': 'QQ钱包',
        }

    def calculate_md5(self, text):
        """计算字符串的MD5值"""
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    def sort_dict_by_key(self, data):
        """对字典按照键名排序"""
        return dict(sorted(data.items(), key=lambda x: x[0]))

    def create_payment(self, amount, out_trade_no, name, user_id, pay_type=None, sitename=""):
        return True

    def query_order(self, order_no, order_type=2):
        """查询订单状态"""
        try:
            query_url = self.config['gateway']
            if query_url.endswith('/'):
                query_url = query_url[:-1]
            query_url = f"{query_url}/api/findorder"

            params = {
                "order_no": order_no,  # 订单号
                "type": order_type     # 订单号类型
            }

            response = requests.get(query_url, params=params, timeout=10)

            if response.status_code != 200:
                return False, None, f"查询订单失败，HTTP状态码: {response.status_code}"

            try:
                result = response.json()
            except:
                return False, None, "查询订单失败，返回数据格式错误"

            code = result.get('code', 0)
            result.get('msg', '未知状态')
            data = result.get('data', {})

            if code == 200:  # 在线处理API返回的成功状态码是200
                order_status = data.get('status')
                if order_status == 1:  # 假设1表示支付成功
                    return True, data, "支付成功"
                else:
                    return True, data, "订单未支付"
            else:
                return True, data, "未找到订单数据"

        except Exception as e:
            return False, None, f"查询订单异常: {str(e)}"

class PaymentCallbackHandler(BaseHTTPRequestHandler):
    """支付回调处理器"""
    def do_GET(self):
        try:
            parsed_url = urlparse(self.path)
            path = parsed_url.path.strip('/')
            order_no = path

            payment_status[order_no] = {'paid': True, 'time': time.time()}

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Payment received')

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f'Error: {str(e)}'.encode())

    def log_message(self, format, *args):
        pass

def start_payment_server(order_no, callback_url, port):
    return True

def poll_mapi_payment_status(order_no, max_tries=30):
    return True

def generate_qrcode(url):
    """生成二维码图片

    Args:
        url: 要生成二维码的URL

    Returns:
        str: 二维码API的URL
    """
    try:
        encoded_url = quote(url)
        api_url = f"https://api.qrtool.cn/?text={encoded_url}&size=300&level=M"
        return api_url
    except Exception as e:
        return None

def poll_mapi_payment_status(order_no, max_tries=30):
    return True

def authorize_account(phone, account_info):
    return True

def authorize_multiple_accounts(accounts):
    return True


def process_coin_exchange(phone, account_info, months, xjbcoin):
    """处理积分兑换"""
    try:
        if not xjbcoin or int(xjbcoin) <= 0:
            sender.reply(f"""
=====兑换失败=====
❌ 未配置积分价格
------------------
请检查配置配置积分兑换功能
==================""")
            return False

        required_coins = months * int(xjbcoin)

        user_coins = sg.bucketGet('dd_sign_points', userid) or '0'
        user_coins = int(user_coins)

        if user_coins < required_coins:
            sender.reply(f"""
=====积分不足=====
❌ 积分余额不足
------------------
💰 当前积分: {user_coins}
🔢 需要积分: {required_coins}
🔍 差额: {required_coins - user_coins}
==================""")
            return False

        new_coins = user_coins - required_coins
        sg.bucketSet('dd_sign_points', userid, str(new_coins))

        success = process_authorization(phone, account_info, months)

        if success:
            sender.reply(f"""
=====积分兑换成功=====
✅ 已扣除积分: {required_coins}
💰 剩余积分: {new_coins}
------------------
授权已处理完成
==================""")
            return True
        else:
            sg.bucketSet('dd_sign_points', userid, str(user_coins))
            sender.reply(f"""
=====积分退还=====
⚠️ 授权处理失败，已退还积分
------------------
💰 当前积分: {user_coins}
==================""")
            return False
    except Exception as e:
        try:
            original_coins = sg.bucketGet('dd_sign_points', userid) or '0'
            original_coins = int(original_coins)
            if original_coins < user_coins:
                sg.bucketSet('dd_sign_points', userid, str(user_coins))
        except:
            pass

        error_msg = f"""
=====兑换异常=====
❌ 积分兑换过程出错
------------------
错误: {str(e)}
=================="""
        print(f"积分兑换异常: {phone}, 错误: {str(e)}")
        sender.reply(error_msg)
        return False

def pay_order(project, months, money):
    return True

def handle_mapay_order(project, months, money, pay_type=None):
    return True

def xjb_auth():
    return True

def update_alipay_info(accounts):
    """更新账号支付宝信息"""
    success_count = 0

    for phone in accounts:
        try:
            account_info_str = sg.bucketGet('s_xjb_token', phone)
            if not account_info_str:
                sender.reply(f"❌ 账号 {mask_phone(phone)} 信息不存在")
                continue

            account_info = json.loads(account_info_str)

            account_info.get('alipay_name', '')
            has_alipay_account = account_info.get('alipay_account', '')

            alipay_name_guide_lines = [
                f"📱 手机号: {mask_phone(phone)}",
                "------------------",
                "请输入新的支付宝姓名",
                "💡 提示: 填写支付宝实名姓名",
                "回复\"s\"跳过此账号",
                "回复\"q\"退出操作"
            ]
            sender.reply(format_message("更新支付宝姓名", alipay_name_guide_lines))

            alipay_name = sender.input(120000, 1, False)
            if not alipay_name or alipay_name.lower() == 'q':
                sender.reply("✅ 已退出更新")
                return
            elif alipay_name.lower() == 's':
                continue

            alipay_account_guide_lines = [
                f"📱 手机号: {mask_phone(phone)}",
                f"💳 当前支付宝账号: {has_alipay_account or '未设置'}",
                "------------------",
                "请输入新的支付宝账号",
                "💡 提示: 可以是手机号或邮箱",
                "回复\"s\"跳过此账号",
                "回复\"q\"退出操作"
            ]
            sender.reply(format_message("更新支付宝账号", alipay_account_guide_lines))

            alipay_account = sender.input(120000, 1, False)
            if not alipay_account or alipay_account.lower() == 'q':
                sender.reply("✅ 已退出更新")
                return
            elif alipay_account.lower() == 's':
                continue

            account_info['alipay_name'] = alipay_name
            account_info['alipay_account'] = alipay_account

            sg.bucketSet('s_xjb_token', phone, json.dumps(account_info))

            auth_time = '2099-12-31'
            if auth_time and auth_time >= str(datetime.now().date()):
                update_ql_env(phone, account_info)
                sender.reply(f"""
=====更新成功=====
📱 手机号: {mask_phone(phone)}
💳 支付宝账号: {alipay_account}
🔄 已同步到青龙
==================""")
            else:
                sender.reply(f"""
=====更新成功=====
📱 手机号: {mask_phone(phone)}
💳 支付宝账号: {alipay_account}
==================""")

            success_count += 1

        except Exception as e:
            sender.reply(f"❌ 更新账号 {mask_phone(phone)} 失败: {str(e)}")

    if success_count > 0:
        sender.reply(f"✅ 已成功更新 {success_count} 个账号的支付宝信息")

def update_session_id(accounts):
    """更新SessionID"""
    success_count = 0

    for phone in accounts:
        try:
            account_info_str = sg.bucketGet('s_xjb_token', phone)
            if not account_info_str:
                sender.reply(f"❌ 账号 {mask_phone(phone)} 信息不存在")
                continue

            account_info = json.loads(account_info_str)

            has_session_id = account_info.get('session_id', '')

            session_id_guide_lines = [
                f"📱 手机号: {mask_phone(phone)}",
                f"🔑 当前SessionID: {has_session_id[:20] + '...' if has_session_id and len(has_session_id) > 20 else has_session_id or '未设置'}",
                "------------------",
                "请输入新的SessionID",
                "💡 提示: 留空则清除SessionID",
                "回复\"s\"跳过此账号",
                "回复\"q\"退出操作"
            ]
            sender.reply(format_message("更新SessionID", session_id_guide_lines))

            new_session_id = sender.input(120000, 1, False)
            if not new_session_id:
                new_session_id = ""  # 处理None情况

            if new_session_id.lower() == 'q':
                sender.reply("✅ 已退出更新")
                return
            elif new_session_id.lower() == 's':
                continue
            elif new_session_id == '':
                account_info['session_id'] = ''
                display_session_id = "已清除"
            else:
                account_info['session_id'] = new_session_id.strip()
                display_session_id = f"{new_session_id.strip()[:20]}..." if len(new_session_id.strip()) > 20 else new_session_id.strip()

            sg.bucketSet('s_xjb_token', phone, json.dumps(account_info))

            auth_time = '2099-12-31'
            if auth_time and auth_time >= str(datetime.now().date()):
                update_ql_env(phone, account_info)
                sender.reply(f"""
=====更新成功=====
📱 手机号: {mask_phone(phone)}
🔑 SessionID: {display_session_id}
🔄 已同步到青龙
==================""")
            else:
                sender.reply(f"""
=====更新成功=====
📱 手机号: {mask_phone(phone)}
🔑 SessionID: {display_session_id}
==================""")

            success_count += 1

        except Exception as e:
            sender.reply(f"❌ 更新账号 {mask_phone(phone)} 失败: {str(e)}")

    if success_count > 0:
        sender.reply(f"✅ 已成功更新 {success_count} 个账号的SessionID")

def get_red_packet_details(user_info):
    """获取红包明细"""
    try:
        session_id = user_info.get('session_id', '')
        account_id = user_info.get('account_id', '')

        if not session_id or not account_id:
            return {"success": False, "message": "缺少sessionId或accountId"}

        auto_login_url = "https://92261.activity-42.m.duiba.com.cn/customActivity/zjtm/autoLogin"
        auto_login_params = {
            "_": str(int(time.time() * 1000)),
            "sessionId": session_id,
            "accountId": account_id,
            "redirectUrl": "https%3A%2F%2F92261.activity-14.m.duiba.com.cn%2Fhdtool%2Findex%3Fid%3D299402208083641%26dbnewopen"
        }

        auto_login_headers = {
            "host": "92261.activity-42.m.duiba.com.cn",
            "sec-ch-ua-platform": "Android",
            "user-agent": "Mozilla/5.0 (Linux; Android 15; 2210132C Build/AQ3A.240812.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/131.0.6778.260 Mobile Safari/537.36;xsb_xinjiangbei;xsb_xinjiangbei;1.7.0;native_app;6.9.0",
            "sec-ch-ua": '"Android WebView";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "accept": "*/*",
            "x-requested-with": "io.pailian.jiangbei",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://92261.activity-42.m.duiba.com.cn/customShare/share?id=6600&dbredirect=https%3A%2F%2F92261.activity-14.m.duiba.com.cn%2Fhdtool%2Findex%3Fid%3D299402208083641%26dbnewopen&gaze_control=01&isNeedLogin=true",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }

        try:
            auto_login_response = requests.get(auto_login_url, params=auto_login_params, headers=auto_login_headers, timeout=10)
            if auto_login_response.status_code != 200:
                return {"success": False, "message": f"获取自动登录链接失败，状态码: {auto_login_response.status_code}"}

            auto_login_result = auto_login_response.json()
            if not auto_login_result.get('success'):
                return {"success": False, "message": "获取自动登录链接失败"}

            login_data_url = auto_login_result.get('data', '')
            if not login_data_url:
                return {"success": False, "message": "自动登录链接为空"}

            if login_data_url.startswith('//'):
                login_data_url = 'https:' + login_data_url

        except Exception as e:
            return {"success": False, "message": f"获取自动登录链接异常: {str(e)}"}

        try:
            login_headers = {
                "user-agent": "Mozilla/5.0 (Linux; Android 15; 2210132C Build/AQ3A.240812.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/131.0.6778.260 Mobile Safari/537.36;xsb_xinjiangbei;xsb_xinjiangbei;1.7.0;native_app;6.9.0",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "accept-encoding": "gzip, deflate, br, zstd",
                "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
            }

            login_response = requests.get(login_data_url, headers=login_headers, allow_redirects=False, timeout=10)

            cookies = {}
            if 'Set-Cookie' in login_response.headers:
                set_cookie_header = login_response.headers['Set-Cookie']
                for cookie_part in set_cookie_header.split(','):
                    if '=' in cookie_part:
                        key_value = cookie_part.split(';')[0].strip()
                        if '=' in key_value:
                            key, value = key_value.split('=', 1)
                            cookies[key.strip()] = value.strip()

            if not cookies:
                cookies = {
                    "_ac": "eyJhaWQiOjkyMjYxLCJjaWQiOjQyODQxMDIzNDZ9",
                    "w_ts": str(int(time.time() * 1000))
                }

        except Exception as e:
            return {"success": False, "message": f"获取cookies异常: {str(e)}"}

        record_url = "https://92261.activity-14.m.duiba.com.cn/crecord/getrecord"
        record_params = {
            "page": "1",
            "_": str(int(time.time() * 1000))
        }

        record_headers = {
            "host": "92261.activity-14.m.duiba.com.cn",
            "sec-ch-ua-platform": "Android",
            "x-requested-with": "XMLHttpRequest",
            "user-agent": "Mozilla/5.0 (Linux; Android 15; 2210132C Build/AQ3A.240812.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/131.0.6778.260 Mobile Safari/537.36;xsb_xinjiangbei;xsb_xinjiangbei;1.7.0;native_app;6.9.0",
            "accept": "application/json",
            "sec-ch-ua": '"Android WebView";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://92261.activity-14.m.duiba.com.cn/crecord/record?dbnewopen&dpm=92261.3.2.0",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }

        try:
            response = requests.get(record_url, params=record_params, headers=record_headers, cookies=cookies, timeout=10)
            if response.status_code != 200:
                return {"success": False, "message": f"查询红包明细失败，状态码: {response.status_code}"}

            result = response.json()
            if not result.get('success'):
                return {"success": False, "message": "获取红包明细失败"}

            return {"success": True, "data": result}
        except Exception as e:
            return {"success": False, "message": f"查询红包明细异常: {str(e)}"}
    except Exception as e:
        return {"success": False, "message": f"获取红包明细失败: {str(e)}"}

def format_red_packet_details(records):
    """格式化红包明细信息"""
    if not records:
        return ["🧧 暂无红包明细"]

    details = ["🧧 近期红包明细:"]

    total_amount = 0
    success_count = 0

    for record in records[:10]:
        title = record.get('title', '未知红包')
        amount = '0.00'
        if '充值' in title and '元' in title:
            try:
                amount = title.split('元')[0].split('充值')[-1]
            except:
                pass
        elif '元' in title:
            try:
                amount = title.split('元')[0]
            except:
                pass

        is_success = False
        status_text = record.get('statusText', '')
        if '成功' in status_text:
            emoji = "🧧"
            is_success = True
        else:
            emoji = "❌"

        create_time = record.get('gmtCreate', '')

        details.append(f"{emoji} {amount}元 {create_time}")

        if is_success:
            try:
                total_amount += float(amount)
                success_count += 1
            except:
                pass

    details.append("-------------------")
    details.append(f"✅ 成功提现: {success_count}笔")
    details.append(f"💰 累计金额: {total_amount:.2f}元")

    return details

def check_xjb_auth_status():
    """检测所有账号的授权状态并通知用户"""
    try:
        notify_channels = sg.bucketGet('s_xjb_config', 'notify') or ''
        if not notify_channels:
            return "❌ 未配置通知渠道，请在插件配置中设置notify参数"

        channels = [channel.strip() for channel in notify_channels.split(',') if channel.strip()]
        if not channels:
            return "❌ 通知渠道配置格式错误"

        all_users = sg.bucketAllKeys('s_xjb_user')
        if not all_users:
            return "❌ 没有找到任何用户绑定的账号"

        current_date = str(datetime.now().date())

        total_checked = 0
        total_notified = 0

        for user_id in all_users:
            try:
                accounts = _sg_literal(sg.bucketGet('s_xjb_user', user_id) or '[]')
                if not accounts:
                    continue
            except:
                continue

            expired_accounts = []  # 授权过期账号

            for account in accounts:
                total_checked += 1

                auth_time = '2099-12-31'
                if not auth_time or auth_time <= current_date:
                    expired_accounts.append({
                        'phone': account,
                        'auth_time': auth_time or '未授权'
                    })

            if expired_accounts:
                notify_msg = "=====新江北账号检测报告====="
                notify_msg += "\n\n🚨 授权过期账号:"
                notify_msg += "\n" + "-" * 25
                for acc in expired_accounts:
                    phone_masked = acc['phone'][:3] + '****' + acc['phone'][-4:] if len(acc['phone']) >= 7 else acc['phone']
                    notify_msg += f"\n📱 {phone_masked} (到期:{acc['auth_time']})"

                notify_msg += "\n" + "-" * 20
                notify_msg += "\n💡 发送\"新江北管理\"进行续费"
                notify_msg += "\n" + "=" * 14

                for channel in channels:
                    try:
                        sg.push(
                            imType=channel,
                            groupCode='',
                            userID=user_id,
                            title="",
                            content=notify_msg
                        )
                        total_notified += 1
                    except Exception as e:
                        print(f"推送通知失败: {channel}, 用户: {user_id}, 错误: {str(e)}")
                        continue

        return f"✅ 检测完成，共检测 {total_checked} 个账号，发送 {total_notified} 条通知"

    except Exception as e:
        return f"❌ 检测失败: {str(e)}"

def clean_xjb_expired():
    """清理过期账号函数"""
    try:
        expired_count = 0
        token_deleted_count = 0
        dqsj = datetime.now().strftime("%Y-%m-%d")

        sender.reply("🧹 开始清理过期账号...")

        expired_accounts = []
        for username in []:
            auth_time = '2099-12-31'
            if auth_time and auth_time < dqsj:
                expired_accounts.append(username)

        if not expired_accounts:
            sender.reply("✅ 没有找到过期账号")
            return

        sender.reply(f"🔍 找到 {len(expired_accounts)} 个过期账号，开始清理...")

        for username in expired_accounts:
            try:
                delete_ql_env(username)

                sg.bucketDel('xjb_token', username)
                token_deleted_count += 1

                True

                sg.bucketDel('xjb_sessionid', username)

                for user_id in sg.bucketAllKeys('xjb_user'):
                    user_accounts = sg.bucketGet('xjb_user', user_id)
                    if user_accounts:
                        try:
                            accounts_list = _sg_literal(user_accounts)
                            if username in accounts_list:
                                accounts_list.remove(username)
                                if accounts_list:
                                    sg.bucketSet('xjb_user', user_id, str(accounts_list))
                                else:
                                    sg.bucketDel('xjb_user', user_id)
                                break
                        except:
                            continue

                True
                expired_count += 1

            except Exception as e:
                print(f"清理账号异常: {username}, 错误: {str(e)}")
                continue

        result_msg = f"""
=====清理完成=====
📊 过期账号: {len(expired_accounts)}个
🗃️ 账号信息: 清理{token_deleted_count}个
🗃️ 青龙变量: 已清理
=================="""
        sender.reply(result_msg)

    except Exception as e:
        sender.reply(f"""
=====清理异常=====
❌ 错误: {str(e)}
==================""")

def main():
    global randommanagecommand, randomquerycommand
    global randomsigncommand, xjbVipmoney, xjbcoin

    (_, _, randommanagecommand, randomquerycommand,
     randomsigncommand, xjbVipmoney, xjbcoin) = get_user_content()

    sender.getImtype()
    usermessage = sender.getMessage()

    if '登录' in usermessage or '登陆' in usermessage:
        bind_account()
    elif '管理' in usermessage:
        manage_account()
    elif '查询' in usermessage:
        query_accounts()
    elif '新江北教程' in usermessage:
        show_tutorial()
    elif '新江北授权' in usermessage:
        xjb_auth()
    elif '新江北检测' in usermessage:
        if not sender.isAdmin():
            sender.reply("❌ 此功能仅限管理员使用")
            return

        sender.reply("🔍 正在检测所有账号状态...")
        result = check_xjb_auth_status()
        sender.reply(result)
    elif '新江北清理' in usermessage:
        if not sender.isAdmin():
            sender.reply("❌ 此功能仅限管理员使用")
            return

        clean_xjb_expired()
    else:
        sender.setContinue()

if __name__ == "__main__":
    main()
