# [title: 大潮]
# [name: daChao]
# [language: python]
# [class: 任务]
# [author: rujingxianghai]
# [version: v1.4]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(大潮|dc)(登录|登陆)$|^登(录|陆)(大潮|dc)$|^(大潮|dc)(查询|管理)$|^(查询|管理)(大潮|dc)$|^大潮$|^大潮检测$|^大潮红包推送$|^大潮教程$]
# [cron: 0 9 * * *]
# [icon: https://api.iconify.design/lucide:apple.svg]
# [description: 大潮现金毛，概率0.2~1；1.0.3:增加备注功能，推送显示对应备注]
# [depe: ["requests"]]


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
    's_dc_qlname': form.string().title('设置对接容器').default('').description('面板容器参数，不填则使用默认配置'),
    's_dc_use_daipanel': form.boolean().title('使用呆呆面板').default(False).description('勾选使用呆呆面板，不勾选使用青龙面板'),
    's_dc_panel_group': form.string().title('呆呆面板分组').default('').description('填写后新增/更新变量时同步写入group字段，留空则不处理'),
    's_dc_osname': form.string().title('提交到青龙的变量名').default('').description('青龙容器内大潮的变量名'),
    's_dc_notify': form.string().title('通知渠道').default('').description('配置检测通知推送渠道'),
})
_CONFIG_FIELD_MAP = {
    ('s_dc', 'qlname'): 's_dc_qlname',
    ('s_dc', 'use_daipanel'): 's_dc_use_daipanel',
    ('s_dc', 'panel_group'): 's_dc_panel_group',
    ('s_dc', 'osname'): 's_dc_osname',
    ('s_dc', 'notify'): 's_dc_notify',
}

import json
import time
import hashlib
import random
import base64
import requests
import uuid
from datetime import datetime

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()
uservalue = sg.bucketGet(bucket='s_dc_user', key=userid)

PLUGIN_CONFIG = {
    'bucket': 's_dc',
    'coin_key': 'dd_sign_points',
    'name': '大潮'
}

TENANT_ID = "94"
CLIENT_ID = "10048"


def get_user_content():
    """获取用户配置内容"""
    osname = sg.bucketGet('s_dc', 'osname') or 'S_DC'
    qlname = sg.bucketGet('s_dc', 'qlname') or ''
    Vipmoney = float(sg.bucketGet('s_dc', 'Vipmoney') or '1')
    coin = int(sg.bucketGet('s_dc', 'coin') or '0')
    return osname, qlname, Vipmoney, coin


def generate_random_uuid():
    """生成随机UUID"""
    return str(uuid.uuid4())

def generate_random_device_id():
    """生成随机设备ID"""
    return ''.join(random.choices('0123456789abcdef', k=32))

def generate_signature_md5(raw_str: str) -> str:
    """生成MD5签名"""
    try:
        return hashlib.md5(raw_str.encode(), usedforsecurity=True).hexdigest()
    except TypeError:
        return hashlib.md5(raw_str.encode()).hexdigest()

def generate_random_ua():
    """生成随机UA"""
    version = "14.1.6"
    uuid_str = generate_random_uuid()
    device_models = ["M1903F2A", "M2001J2E", "M2001J2C", "M2001J1E", "M2001J1C",
                    "M2002J9E", "M2011K2C", "M2102K1C", "M2101K9C", "2107119DC",
                    "2201123C", "2112123AC", "2201122C", "2211133C", "2210132C",
                    "2304FPN6DC", "23127PN0CC", "24031PN0DC", "23090RA98C",
                    "2312DRA50C", "2312CRAD3C", "2312DRAABC", "22101316UCP", "22101316C"]

    device_model = random.choice(device_models)
    device_name = f"Xiaomi {device_model}"
    os_name = "Android"

    ua = f"{os_name.upper()};11;{CLIENT_ID};{version};1.0;null;{device_model}"
    common_ua = f"{version};{uuid_str};{device_name};{os_name};11;6.11.0"

    return {
        'ua': ua,
        'commonUa': common_ua,
        'uuid': uuid_str
    }


def get_session_id():
    """获取sessionId"""
    init_url = "https://vapp.tmuyun.com/api/account/init"
    device_id = generate_random_device_id()
    ua_info = generate_random_ua()

    init_headers = {
        "Connection": "keep-alive",
        "Cache-Control": "no-cache",
        "Accept-Encoding": "gzip",
        "user-agent": ua_info['commonUa'],
        "X-TENANT-ID": TENANT_ID,
        "Content-Type": "application/json;charset=utf-8"
    }

    try:
        init_response = requests.post(init_url, headers=init_headers, json={}, timeout=10)
        time.sleep(1)

        if init_response.status_code != 200:
            return None, None, None, None

        init_result = init_response.json()

        if 'data' in init_result and 'session' in init_result['data']:
            session_id = init_result['data']['session']['id']
            return session_id, device_id, ua_info['ua'], ua_info['commonUa']
        else:
            return None, None, None, None

    except Exception as e:
        sender.reply(f"获取sessionId异常: {str(e)}")
        return None, None, None, None

def get_signature_key(user_agent):
    """获取signature_key"""
    passport_url = f"https://passport.tmuyun.com/web/init?client_id={CLIENT_ID}"
    passport_headers = {
        "Connection": "Keep-Alive",
        "Cache-Control": "no-cache",
        "X-REQUEST-ID": generate_random_uuid(),
        "Accept-Encoding": "gzip",
        "user-agent": user_agent
    }

    try:
        passport_response = requests.get(passport_url, headers=passport_headers, timeout=10)
        if passport_response.status_code != 200:
            return None

        passport_result = passport_response.json()

        if 'data' in passport_result and 'client' in passport_result['data'] and 'signature_key' in passport_result['data']['client']:
            return passport_result['data']['client']['signature_key']
        else:
            return None

    except Exception as e:
        sender.reply(f"获取signature_key异常: {str(e)}")
        return None

def get_authorization_code(phone, password, signature_key, user_agent, device_id):
    return '2099-12-31'

def login_account(auth_code, session_id, device_id, common_ua):
    """登录账号"""
    uuid_str = generate_random_uuid()
    timestamp = str(int(time.time() * 1000))

    path = "/api/zbtxz/login"
    sign_str = f"{path}&&{session_id}&&{uuid_str}&&{timestamp}&&FR*r!isE5W&&{TENANT_ID}"
    signature = hashlib.sha256(sign_str.encode()).hexdigest()

    login_url = "https://vapp.tmuyun.com/api/zbtxz/login"
    login_data = f"check_token=&code={auth_code}&token=&type=-1&union_id="

    login_headers = {
        "Connection": "Keep-Alive",
        "X-SESSION-ID": session_id,
        "X-TENANT-ID": TENANT_ID,
        "Cache-Control": "no-cache",
        "Accept-Encoding": "gzip",
        "user-agent": common_ua,
        "Content-Type": "application/x-www-form-urlencoded",
        "X-SIGNATURE": signature,
        "X-REQUEST-ID": uuid_str,
        "X-TIMESTAMP": timestamp
    }

    try:
        response = requests.post(login_url, headers=login_headers, data=login_data, timeout=10)
        time.sleep(1)

        if response.status_code != 200:
            return None, None

        try:
            result = response.json()
        except json.JSONDecodeError:
            return None, None

        if result.get('code') != 0:
            return None, None

        if 'data' not in result or 'session' not in result['data']:
            return None, None

        session_data = result['data']['session']
        if 'account_id' not in session_data or 'id' not in session_data:
            return None, None

        account_id = session_data['account_id']
        new_session_id = session_data['id']
        return account_id, new_session_id

    except Exception as e:
        sender.reply(f"登录异常: {str(e)}")
        return None, None

def bind_account():
    """绑定大潮账号"""
    sender.reply("""
=====大潮登录=====
请按照提示依次输入账号信息
回复"q"退出
==================""")

    sender.reply("请输入手机号（大潮登录账号）:")
    username = sender.input(120000, 1, False)
    if not username:
        sender.reply("⏰ 操作超时")
        return
    elif username.lower() == 'q':
        sender.reply("✅ 已取消登录")
        return

    if not username.isdigit() or len(username) != 11:
        sender.reply("""
=====格式错误=====
❌ 手机号格式不正确
------------------
请输入11位数字手机号
==================""")
        return

    sender.reply("请输入密码:")
    password = sender.input(120000, 1, False)
    if not password:
        sender.reply("⏰ 操作超时")
        return
    elif password.lower() == 'q':
        sender.reply("✅ 已取消登录")
        return

    sender.reply("🔄 正在登录...")

    try:
        session_id, device_id, user_agent, common_ua = get_session_id()
        if not session_id:
            sender.reply("❌ 获取会话失败")
            return

        signature_key = get_signature_key(user_agent)
        if not signature_key:
            sender.reply("❌ 获取签名密钥失败")
            return

        auth_code = get_authorization_code(username, password, signature_key, user_agent, device_id)
        if not auth_code:
            sender.reply("❌ 账号或密码错误")
            return

        account_id, new_session_id = login_account(auth_code, session_id, device_id, common_ua)
        if not account_id:
            sender.reply("❌ 登录失败")
            return

        if not uservalue:
            sg.bucketSet('s_dc_user', userid, str([username]))
        else:
            accounts = _sg_literal(uservalue)
            if username not in accounts:
                accounts.append(username)
                sg.bucketSet('s_dc_user', userid, str(accounts))

        account_info = {
            "username": username,
            "password": password,
            "enable_redpack_push": False  # 默认不推送红包
        }
        sg.bucketSet('s_dc_token', username, json.dumps(account_info))

        success_msg = f"""
=====绑定成功=====
📱 手机号: {mask_account(username)}
=================="""
        sender.reply(success_msg)

        sender.reply("""
=====红包推送设置=====
是否开启红包链接推送功能？
------------------
回复 y 开启推送
回复 n 不开启
==================""")

        push_choice = sender.input(120000, 1, False)
        if push_choice and push_choice.lower() == 'y':
            account_info['enable_redpack_push'] = True
            sg.bucketSet('s_dc_token', username, json.dumps(account_info))
            sender.reply("✅ 已开启红包推送功能")
        else:
            sender.reply("✅ 未开启红包推送功能")

        dqsj = datetime.now().strftime("%Y-%m-%d")
        accountVip = '2099-12-31'

        if accountVip and accountVip > dqsj:
            sender.reply(f"""
=====账号已授权=====
📅 到期时间: {accountVip}
------------------
正在更新账号信息...
==================""")

            if update_ql_env(username, account_info):
                sender.reply("✅ 账号信息更新成功")
            else:
                sender.reply("❌ 账号信息更新失败")
        else:
            authorize_multiple_accounts([username])

    except Exception as e:
        sender.reply(f"""
=====绑定异常=====
❌ 错误: {str(e)}
请重试或检查配置
==================""")


def relogin_account(username, password):
    """重新登录获取session信息"""
    try:
        session_id, device_id, user_agent, common_ua = get_session_id()
        if not session_id:
            return None

        signature_key = get_signature_key(user_agent)
        if not signature_key:
            return None

        auth_code = get_authorization_code(username, password, signature_key, user_agent, device_id)
        if not auth_code:
            return None

        account_id, new_session_id = login_account(auth_code, session_id, device_id, common_ua)
        if not account_id:
            return None

        return {
            'session_id': new_session_id,
            'account_id': account_id,
            'device_id': device_id,
            'user_agent': user_agent,
            'common_ua': common_ua
        }

    except Exception as e:
        sender.reply(f"重新登录异常: {str(e)}")
        return None

def get_member_token(username, password):
    """获取member_token用于红包API"""
    try:
        login_info = relogin_account(username, password)
        if not login_info:
            return None, None

        session_id = login_info['session_id']
        account_id = login_info['account_id']
        common_ua = login_info['common_ua']

        if not session_id or not account_id:
            return None

        uuid_str = generate_random_uuid()
        timestamp = str(int(time.time() * 1000))
        path = "/api/user_mumber/account_detail"
        sign_str = f"{path}&&{session_id}&&{uuid_str}&&{timestamp}&&FR*r!isE5W&&{TENANT_ID}"
        signature = hashlib.sha256(sign_str.encode()).hexdigest()

        headers = {
            "Connection": "Keep-Alive",
            "X-SESSION-ID": session_id,
            "X-REQUEST-ID": uuid_str,
            "X-SIGNATURE": signature,
            "X-TIMESTAMP": timestamp,
            "X-TENANT-ID": TENANT_ID,
            "X-ACCOUNT-ID": account_id,
            "Cache-Control": "no-cache",
            "Accept-Encoding": "gzip",
            "user-agent": common_ua
        }

        response = requests.get("https://vapp.tmuyun.com/api/user_mumber/account_detail", headers=headers, timeout=10)

        if response.status_code != 200:
            return None

        result = response.json()
        if result.get('code') != 0 or 'data' not in result:
            return None

        user_data = result['data'].get('rst', {})

        timestamp_sec = int(time.time())
        signature_str = f" &id&mobile&nick_name&&{timestamp_sec}&&KO>N<O5&3^L1%23YH0H1#G91*2H"
        signature_hash = hashlib.sha256(signature_str.encode()).hexdigest()

        signature_data = {
            "accountId": account_id,
            "signature": signature_hash,
            "mobile": "1",
            "sessionId": session_id,
            "login": "1",
            "user": {
                "realName": "",
                "image_url": user_data.get('image_url', ''),
                "nick_name": user_data.get('nick_name', ''),
                "is_face_verify": 0,
                "idcard": "",
                "id": account_id
            },
            "timestamp": str(timestamp_sec),
            "sign": "xsb_hn"
        }

        member_response = requests.post(
            "https://m.aihoge.com/api/memberhy/tm/signature",
            json=signature_data,
            headers={
                "Content-Type": "application/json;charset=UTF-8",
                "Connection": "keep-alive",
                "X-DEVICE-SIGN": "xsb_hn",
                "X-CLIENT-VERSION": "1314",
                "accept": "application/json, text/plain, */*",
                "user-agent": "Mozilla/5.0 (Linux; Android 11; 21091116AC Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.85 Mobile Safari/537.36;xsb_hn;xsb_hn;14.1.6;native_app;6.11.0",
                "HTTP-X-H5-VERSION": "1",
                "Limit": "default",
                "sessionId": session_id,
                "X-DEVICE-ID": "000",
                "accountId": account_id,
                "x-requested-with": "com.hoge.android.app.dachao",
                "sec-fetch-site": "same-origin",
                "sec-fetch-mode": "cors",
                "sec-fetch-dest": "empty",
                "accept-encoding": "gzip, deflate",
                "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
            },
            timeout=10
        )

        if member_response.status_code != 200:
            return None

        member_result = member_response.json()
        if not member_result:
            return None

        member_token = json.dumps({
            "id": member_result.get('id', ''),
            "black": 0,
            "btoken": member_result.get('btoken', ''),
            "expire": member_result.get('expire', ''),
            "token": member_result.get('token', ''),
            "source": "xsb_hn",
            "mobile": member_result.get('mobile', ''),
            "mark": member_result.get('mark', ''),
            "mtoken": member_result.get('mtoken', ''),
            "stoken": member_result.get('stoken', ''),
            "nick_name": requests.utils.quote(member_result.get('nick_name', '')),
            "avatar": member_result.get('avatar', '')
        })

        return member_token, login_info

    except Exception as e:
        sender.reply(f"获取member_token异常: {str(e)}")
        return None

def get_redpack_list(account_info):
    """获取未领取红包列表"""
    try:
        username = account_info.get('username', '')
        password = account_info.get('password', '')

        if not username or not password:
            return None, "账号信息不完整"

        member_token, login_info = get_member_token(username, password)
        if not member_token or not login_info:
            return None, "获取member_token失败"

        session_id = login_info['session_id']
        account_id = login_info['account_id']

        url = "https://axh5.aihoge.com/api/lotteryhy/api/client/cj/member/prize/info?prize_type=3&page=1&count=20"

        headers = {
            "Connection": "keep-alive",
            "X-DEVICE-SIGN": "xsb_hn",
            "X-CLIENT-VERSION": "1314",
            "accept": "application/json, text/plain, */*",
            "user-agent": "Mozilla/5.0 (Linux; Android 11; 21091116AC Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.85 Mobile Safari/537.36;xsb_hn;xsb_hn;14.1.6;native_app;6.11.0",
            "HTTP-X-H5-VERSION": "1",
            "member": member_token,
            "Limit": "default",
            "sessionId": session_id,
            "X-DEVICE-ID": "000",
            "accountId": account_id,
            "x-requested-with": "com.hoge.android.app.dachao",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "Referer": "https://axh5.aihoge.com/winningList?refresh_times=1641284795642",
            "accept-encoding": "gzip, deflate",
            "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return None, f"请求失败，状态码: {response.status_code}"

        result = response.json()

        if not result or 'data' not in result:
            return None, "获取红包列表失败"

        data = result.get('data', [])

        redpacks = []

        for prize in data:
            status = prize.get('status', 0)

            if status != 2 and status != 6:
                prize_info_str = prize.get('prize_info', '{}')
                try:
                    prize_info = json.loads(prize_info_str)
                    code = prize_info.get('code', '')
                except:
                    code = ''

                link = f"https://m.aihoge.com/lottery/rotor/drawRedPacket?CHECK_CODE={code}"

                end_time = prize.get('end_time', 0)
                if end_time > 0:
                    expire_time_str = datetime.fromtimestamp(end_time).strftime("%Y-%m-%d %H:%M")
                else:
                    expire_time_str = "未知"

                redpacks.append({
                    'id': prize.get('id', ''),
                    'amount': prize.get('prize_content', '未知'),
                    'link': link,
                    'expire_time': expire_time_str,
                    'activity_name': prize.get('activity_name', ''),
                    'code': code,
                    'status_name': prize.get('status_name', '未知')
                })

        return redpacks, "获取成功"

    except Exception as e:
        return None, f"获取红包列表异常: {str(e)}"

def query_accounts():
    """查询账号信息"""
    if not uservalue:
        sender.reply(f"""
=====未绑定账号=====
❌ 未找到账号
💡 发送 大潮登录 绑定
==================""")
        return

    accounts = _sg_literal(uservalue)
    account_list = "\n========选择账号=======\n[0] 全部账号"

    for i, username in enumerate(accounts, 1):
        account_info = json.loads(sg.bucketGet('s_dc_token', username))
        auth_time = '2099-12-31'

        if not auth_time:
            auth_status = '未授权'
        elif auth_time < str(datetime.now().date()):
            auth_status = '已过期'
        else:
            auth_status = f'到期:{auth_time}'

        remark = account_info.get('remark', '')
        remark_display = f", {remark}" if remark else ""

        account_list += f"\n[{i}]{mask_account(username)}({auth_status}{remark_display})"

    account_list += "\n=====================\n支持多选，用逗号分隔\n回复\"q\"退出\n====================="

    sender.reply(account_list)

    choice = sender.input(120000, 1, False)
    if not choice or choice.lower() == 'q':
        sender.reply("✅ 已退出")
        return

    try:
        if choice == '0':
            selected_accounts = accounts.copy()
        else:
            selected_accounts = [
                accounts[int(idx.strip()) - 1]
                for idx in choice.split(',')
                if idx.strip().isdigit() and 0 <= int(idx.strip()) - 1 < len(accounts)
            ]

        if not selected_accounts:
            sender.reply("❌ 未选择有效账号")
            return

        sender.reply(f"✅ 已选择 {len(selected_accounts)} 个账号，正在查询...")

        query_count = 0
        for username in selected_accounts:
            try:
                account_info = json.loads(sg.bucketGet('s_dc_token', username))

                auth_time = '2099-12-31'
                auth_status = '已授权' if auth_time and auth_time >= str(datetime.now().date()) else '未授权'

                push_status = "已开启" if account_info.get('enable_redpack_push', False) else "未开启"

                remark = account_info.get('remark', '')

                redpacks, msg = get_redpack_list(account_info)

                redpack_info = ""
                if redpacks:
                    redpack_info = "=================="
                    redpack_info += f"\n🎁 待领红包: {len(redpacks)}个"
                    for i, pack in enumerate(redpacks[:5], 1):  # 最多显示5个
                        short_link = shorten_url(pack.get('link', '无链接'))
                        redpack_info += f"\n  [{i}] {pack.get('amount', '未知')}"
                        redpack_info += f"\n      🔗 {short_link}"
                        redpack_info += f"\n      ⏰ 过期：{pack.get('expire_time', '未知')}"
                    if len(redpacks) > 5:
                        redpack_info += f"\n  ... 还有{len(redpacks)-5}个红包"
                else:
                    redpack_info = "\n🎁 待领红包: 0个"

                remark_info = f"\n📝 备注: {remark}" if remark else ""
                account_info_msg = f"""
=====账号信息[{query_count+1}/{len(selected_accounts)}]=====
📱 手机号: {mask_account(username)}
🏷 状态: {auth_status}
💰 红包推送: {push_status}{remark_info}{redpack_info}
=================="""
                sender.reply(account_info_msg)
                query_count += 1

                if query_count < len(selected_accounts) and len(selected_accounts) > 3:
                    time.sleep(0.5)

            except Exception as e:
                sender.reply(f"""
=====查询失败[{query_count+1}/{len(selected_accounts)}]=====
📱 手机号: {mask_account(username)}
❌ 状态: 账号信息查询失败
❌ 错误: {str(e)}
==================""")
                query_count += 1

        if query_count > 0:
            sender.reply("✅ 查询完成")

    except Exception as e:
        sender.reply(f"❌ 查询失败: {str(e)}")

def push_redpack_links():
    """推送红包链接给用户（管理员功能）"""
    if not sender.isAdmin():
        sender.reply("❌ 仅限管理员")
        return

    sender.reply("🔍 正在检查红包...")

    all_users = sg.bucketAllKeys('s_dc_user')
    if not all_users:
        sender.reply("❌ 没有用户")
        return

    total_users = 0
    total_accounts = 0
    total_redpacks = 0
    pushed_users = 0

    for user_id in all_users:
        try:
            user_accounts = _sg_literal(sg.bucketGet('s_dc_user', user_id) or '[]')
            if not user_accounts:
                continue

            total_users += 1
            user_redpacks = []  # 该用户的所有红包

            for username in user_accounts:
                try:
                    total_accounts += 1
                    account_info = json.loads(sg.bucketGet('s_dc_token', username))

                    if not account_info.get('enable_redpack_push', False):
                        continue

                    auth_time = '2099-12-31'
                    if not auth_time or auth_time < str(datetime.now().date()):
                        continue

                    redpacks, msg = get_redpack_list(account_info)

                    if redpacks and len(redpacks) > 0:
                        user_redpacks.append({
                            'username': username,
                            'redpacks': redpacks
                        })

                except Exception as e:
                    print(f"检查账号异常: {username}, 错误: {str(e)}")
                    continue

            if user_redpacks:
                push_msg = "=====红包提醒=====\n"

                for account_data in user_redpacks:
                    username = account_data['username']
                    redpacks = account_data['redpacks']

                    try:
                        account_info = json.loads(sg.bucketGet('s_dc_token', username))
                        remark = account_info.get('remark', '')
                    except:
                        remark = ''

                    if remark:
                        push_msg += f"\n📱 账号: {mask_account(username)}({remark})\n"
                    else:
                        push_msg += f"\n📱 账号: {mask_account(username)}\n"

                    push_msg += f"🎁 待领红包: {len(redpacks)}个\n"
                    push_msg += "------------------\n"

                    for i, pack in enumerate(redpacks, 1):
                        short_link = shorten_url(pack.get('link', '无链接'))
                        push_msg += f"[{i}] {pack.get('amount', '未知')}\n"
                        push_msg += f"🔗 {short_link}\n"
                        push_msg += f"⏰ 过期: {pack.get('expire_time', '未知')}\n"

                        total_redpacks += 1

                    push_msg += "\n"

                push_msg += "------------------\n"
                push_msg += "请及时领取红包\n"
                push_msg += "=================="

                try:
                    notify_channels = sg.bucketGet('s_dc', 'notify') or 'qq'
                    channels = [channel.strip() for channel in notify_channels.split(',') if channel.strip()]

                    for channel in channels:
                        try:
                            sg.push(
                                imType=channel,
                                groupCode='',
                                userID=user_id,
                                title="",
                                content=push_msg
                            )
                        except Exception as e:
                            print(f"推送失败: {channel}, 用户: {user_id}, 错误: {str(e)}")
                            continue

                    pushed_users += 1

                except Exception as e:
                    print(f"推送给用户失败: {user_id}, 错误: {str(e)}")
                    continue

        except Exception as e:
            print(f"处理用户异常: {user_id}, 错误: {str(e)}")
            continue

    sender.reply(f"""
=====推送完成=====
👥 检查用户: {total_users}个
📱 检查账号: {total_accounts}个
✅ 推送用户: {pushed_users}个
🎁 红包总数: {total_redpacks}个
==================""")


def manage_account():
    """账号管理功能"""
    if not uservalue:
        sender.reply(f"""
=====未绑定账号=====
❌ 未找到账号
💡 发送 大潮登录 绑定
==================""")
        return

    accounts = _sg_literal(uservalue)

    menu = """
=====账号管理=====
[1] 授权账号
[2] 删除账号
[3] 提交青龙
[4] 红包推送设置
[5] 添加备注
------------------
回复数字选择
回复"q"退出
=================="""
    sender.reply(menu)

    choice = sender.input(120000, 1, False)
    if not choice or choice.lower() == 'q':
        sender.reply("✅ 已退出")
        return

    account_list = """
========选择账号=======
[0] 全部账号"""

    for i, username in enumerate(accounts, 1):
        account_info = json.loads(sg.bucketGet('s_dc_token', username))
        auth_time = '2099-12-31'

        if not auth_time:
            auth_status = '未授权'
        elif auth_time < str(datetime.now().date()):
            auth_status = '已过期'
        else:
            auth_status = f'到期:{auth_time}'

        push_status = "推送✓" if account_info.get('enable_redpack_push', False) else "推送✗"

        remark = account_info.get('remark', '')
        remark_display = f", {remark}" if remark else ""

        account_list += f"""
[{i}]{mask_account(username)}({auth_status}, {push_status}{remark_display})"""

    account_list += """
=====================
支持多选，用逗号分隔
回复"q"退出
====================="""

    sender.reply(account_list)

    account_choice = sender.input(120000, 1, False)
    if not account_choice or account_choice.lower() == 'q':
        sender.reply("✅ 已退出")
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
            confirm = """
=====确认删除=====
⚠️ 此操作不可恢复
------------------
回复 y 确认删除
回复 n 取消操作
=================="""
            sender.reply(confirm)

            confirm = sender.input(120000, 1, False)
            if confirm and confirm.lower() == 'y':
                success_list = []
                fail_list = []
                for username in selected_accounts:
                    try:
                        if username in accounts:
                            accounts.remove(username)

                        sg.bucketDel('s_dc_token', username)
                        True

                        delete_ql_env(username)
                        success_list.append(mask_account(username))
                    except Exception as e:
                        fail_list.append(f"{mask_account(username)} {str(e)}")

                if accounts:
                    sg.bucketSet('s_dc_user', userid, str(accounts))
                else:
                    sg.bucketDel('s_dc_user', userid)

                result = "=====删除完成=====\n"
                result += f"✅ 成功: {len(success_list)}个\n"
                if success_list:
                    result += "、".join(success_list) + "\n"
                if fail_list:
                    result += f"❌ 失败: {len(fail_list)}个\n"
                    result += "\n".join(fail_list) + "\n"
                result += "=================="
                sender.reply(result)
            else:
                sender.reply("✅ 已取消删除")

        elif choice == '3':
            success_list = []
            fail_list = []
            for username in selected_accounts:
                try:
                    raw = sg.bucketGet('s_dc_token', username)
                    if not raw:
                        fail_list.append(f"{mask_account(username)} 无账号数据")
                        continue
                    account_info = json.loads(raw)

                    auth_time = '2099-12-31'
                    if auth_time and auth_time >= str(datetime.now().date()):
                        if update_ql_env(username, account_info):
                            success_list.append(mask_account(username))
                        else:
                            fail_list.append(f"{mask_account(username)} 提交失败")
                    else:
                        fail_list.append(f"{mask_account(username)} 未授权/已过期")
                except Exception as e:
                    fail_list.append(f"{mask_account(username)} {str(e)}")

            result = "=====提交完成=====\n"
            result += f"✅ 成功: {len(success_list)}个\n"
            if success_list:
                result += "、".join(success_list) + "\n"
            if fail_list:
                result += f"❌ 失败: {len(fail_list)}个\n"
                result += "\n".join(fail_list) + "\n"
            result += "=================="
            sender.reply(result)

        elif choice == '4':
            sender.reply("""
=====红包推送设置=====
请选择操作:
[1] 开启推送
[2] 关闭推送
------------------
回复数字选择
回复"q"退出
==================""")

            push_choice = sender.input(120000, 1, False)
            if not push_choice or push_choice.lower() == 'q':
                sender.reply("✅ 已退出")
                return

            if push_choice == '1':
                enable_push = True
                action_text = "开启"
            elif push_choice == '2':
                enable_push = False
                action_text = "关闭"
            else:
                sender.reply("❌ 无效的选择")
                return

            success_list = []
            fail_list = []
            for username in selected_accounts:
                try:
                    account_info = json.loads(sg.bucketGet('s_dc_token', username))
                    account_info['enable_redpack_push'] = enable_push
                    sg.bucketSet('s_dc_token', username, json.dumps(account_info))
                    success_list.append(mask_account(username))
                except Exception as e:
                    fail_list.append(f"{mask_account(username)} {str(e)}")

            result = "=====设置完成=====\n"
            result += f"✅ 已{action_text}: {len(success_list)}个\n"
            if success_list:
                result += "、".join(success_list) + "\n"
            if fail_list:
                result += f"❌ 失败: {len(fail_list)}个\n"
                result += "\n".join(fail_list) + "\n"
            result += "=================="
            sender.reply(result)

        elif choice == '5':
            sender.reply("""
=====添加备注=====
请输入备注内容:
------------------
回复"q"退出
==================""")

            remark_text = sender.input(120000, 1, False)
            if not remark_text or remark_text.lower() == 'q':
                sender.reply("✅ 已退出")
                return

            success_list = []
            fail_list = []
            for username in selected_accounts:
                try:
                    account_info = json.loads(sg.bucketGet('s_dc_token', username))
                    account_info['remark'] = remark_text
                    sg.bucketSet('s_dc_token', username, json.dumps(account_info))
                    success_list.append(mask_account(username))
                except Exception as e:
                    fail_list.append(f"{mask_account(username)} {str(e)}")

            result = "=====备注添加完成=====\n"
            result += f"✅ 成功: {len(success_list)}个\n"
            if success_list:
                result += "、".join(success_list) + "\n"
            if fail_list:
                result += f"❌ 失败: {len(fail_list)}个\n"
                result += "\n".join(fail_list) + "\n"
            result += f"📝 备注: {remark_text}\n"
            result += "=================="
            sender.reply(result)
        else:
            sender.reply("❌ 无效的选择")

    except Exception as e:
        sender.reply(f"❌ 操作失败: {str(e)}")


def authorize_multiple_accounts(usernames):
    return True

def generate_iframe_url(url):
    """将URL通过base64编码生成iframe页面链接"""
    try:
        encoded = base64.b64encode(url.encode('utf-8')).decode('utf-8')
        iframe_url = f"https://metwhale.github.io?u={encoded}"
        return iframe_url
    except Exception as e:
        return url

def shorten_url(long_url):
    """缩短链接"""
    try:
        encoded_url = requests.utils.quote(long_url)
        headers = {
            'sec-ch-ua-platform': 'Windows',
            'sec-ch-ua': '"Microsoft Edge";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'sec-ch-ua-mobile': '?0',
            'Origin': 'https://www.mrw.so',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.mrw.so/',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
        }
        data = {
            'urlStr': encoded_url,
            'domain': 'mrw.so',
            'expireType': '1',
            'key': '5d7798c491d2c423c8c33d2d@631d0a6ffd3fbca7c2728bebc6602f98',
            'random': str(int(time.time() * 1000))
        }
        response = requests.post('https://create.mrw.so/pageHome/createBySingle.htm', headers=headers, data=data, timeout=10)
        short_url = response.json().get('data')
        if short_url:
            return short_url
        return long_url
    except:
        return long_url

def process_mapay_payment(project, months, money, pay_type='alipay'):
    return True


def process_qrcode_payment(project, months, money):
    return True


def update_ql_env(username, account_info):
    """更新青龙环境变量"""
    phone = account_info.get('username', '')
    password = account_info.get('password', '')

    if not phone or not password:
        sender.reply(f"更新青龙变量失败: 账号信息不完整")
        return False

    env_value = f"{phone}#{password}"

    auth_time = '2099-12-31' or '未授权'
    panel_group = (sg.bucketGet('s_dc', 'panel_group') or '').strip()
    ql = _get_ql_client()
    return ql.update_env(
        username,
        env_value,
        f"大潮:{mask_account(username)}|到期:{auth_time}",
        group=panel_group,
    )

def delete_ql_env(username):
    """删除面板环境变量（青龙/呆呆面板 通用）"""
    ql = _get_ql_client()
    return ql.delete_env(username)


def _get_ql_client():
    """获取面板客户端，根据开关决定使用青龙或DumbPanel"""
    osname = sg.bucketGet('s_dc', 'osname') or 'S_DC'
    qlname = sg.bucketGet('s_dc', 'qlname') or ''
    use_dp = str(sg.bucketGet('s_dc', 'use_daipanel') or '').lower() == 'true'

    if use_dp:
        if qlname:
            return DumbPanelClient(osname, qlname)
        return DumbPanelClient(osname)
    else:
        if qlname:
            return QingLongClient(osname, qlname)
        return QingLongClient(osname)



def ks_auth():
    return True


def show_tutorial():
    """显示大潮教程"""
    sender.reply(
        '=====大潮教程=====\n'
        '用户指令:\n'
        '1. 大潮登录 - 绑定账号\n'
        '2. 大潮查询 - 查询账号状态和红包\n'
        '3. 大潮管理 - 授权、删除、提交面板\n'
        '4. 大潮教程 - 查看说明\n'
        '------------------\n'
        '管理员指令:\n'
        '1. 大潮授权 - 批量授权\n'
        '2. 大潮检测 - 检测过期并清理\n'
        '3. 大潮红包推送 - 推送红包链接\n'
        '------------------\n'
        '绑定输入:\n'
        '按提示依次输入手机号和密码\n'
        '登录成功后可选择开启红包推送\n'
        '------------------\n'
        '使用流程:\n'
        '1. 发送"大潮登录"绑定账号\n'
        '2. 发送"大潮查询"查看状态\n'
        '3. 发送"大潮管理"授权账号\n'
        '4. 选择时长并完成支付\n'
        '=================='
    )


def main():
    """主入口"""
    msg = sender.getMessage()

    if ('登录' in msg or '登陆' in msg) and ('大潮' in msg or 'dc' in msg.lower()):
        bind_account()
    elif '查询' in msg and ('大潮' in msg or 'dc' in msg.lower()):
        query_accounts()
    elif '管理' in msg and ('大潮' in msg or 'dc' in msg.lower()):
        manage_account()
    elif '大潮授权' in msg:
        ks_auth()
    elif '大潮检测' in msg:
        if not sender.isAdmin():
            sender.reply("❌ 此功能仅限管理员使用")
            return

        sender.reply("🔍 正在检测所有账号状态...")
        result = check_auth_status()
        sender.reply(result)
    elif '大潮红包推送' in msg or '红包推送' in msg:
        push_redpack_links()
    elif '教程' in msg and ('大潮' in msg or 'dc' in msg.lower()):
        show_tutorial()
    elif sender.getImtype() == 'fake':
        try:
            sg.notifyMasters(check_auth_status())
        except:
            pass
    elif msg.startswith('S_DC_'):  # 查询订单
        try:
            order_info = sg.bucketGet('s_dc_order', msg)
            if not order_info:
                sender.reply("""
=====查询结果=====
❌ 未找到订单信息
------------------
请确认订单号是否正确
==================""")
            else:
                order_data = json.loads(order_info)
                sender.reply(f"""
=====订单详情=====
🔖 订单号: {msg}
💰 金额: {order_data.get('amount', '未知')}元
⏱️ 时长: {order_data.get('months', '未知')}个月
📊 状态: {'已支付' if order_data.get('status') == 'success' else '未支付'}
==================""")
        except Exception as e:
            sender.reply(f"""
=====查询异常=====
❌ 错误: {str(e)}
==================""")
    else:
        sender.setContinue()

if __name__ == "__main__":
    main()
