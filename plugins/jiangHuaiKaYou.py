# [title: 江淮卡友]
# [name: jiangHuaiKaYou]
# [language: python]
# [class: 任务]
# [author: rujingxianghai]
# [version: v1.7.0]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(江淮|jh)(登录|登陆)$|^登(录|陆)(江淮|jh)$|^(江淮|jh)(查询|管理|检测|教程|迁移)$|^(查询|管理|检测|教程|迁移)(江淮|jh)$]
# [cron: 0 9 * * *]
# [icon: https://y.gtimg.cn/music/photo_new/T053M000001NYort1rZecQ.png]
# [description: 。]
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
    's_jh_osname': form.string().title('青龙变量名').default('').description('青龙容器内的变量名'),
    's_jh_qlname': form.string().title('设置对接容器').default('').description('面板容器参数，不填则使用默认配置'),
    's_jh_use_daipanel': form.boolean().title('使用呆呆面板').default(False).description('勾选使用呆呆面板，不勾选使用青龙面板'),
    's_jh_panel_group': form.string().title('呆呆面板分组').default('').description('填写后新增/更新变量时同步写入group字段，留空则不处理'),
    's_jh_notify': form.string().title('通知渠道').default('').description('检测通知推送渠道'),
})
_CONFIG_FIELD_MAP = {
    ('s_jh', 'osname'): 's_jh_osname',
    ('s_jh', 'qlname'): 's_jh_qlname',
    ('s_jh', 'use_daipanel'): 's_jh_use_daipanel',
    ('s_jh', 'panel_group'): 's_jh_panel_group',
    ('s_jh', 'notify'): 's_jh_notify',
}

import json
import time
import base64
import hashlib
import random
import requests
from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5



senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()
uservalue = sg.bucketGet(bucket='s_jh_user', key=userid)

base_url = 'https://jacwxmp.starnetah.com'
base_url2 = 'http://jacwxmp.starnetah.com'

PLUGIN_CONFIG = {'bucket': 's_jh', 'coin_key': 'dd_sign_points', 'name': '江淮卡友'}

BUCKET_USER = 's_jh_user'
BUCKET_TOKEN = 's_jh_token'
BUCKET_AUTH = 's_jh_auth'
BUCKET_CONFIG = 's_jh'


def get_user_content():
    osname = sg.bucketGet(BUCKET_CONFIG, 'osname') or 'S_JHKY'
    qlname = sg.bucketGet(BUCKET_CONFIG, 'qlname') or ''
    use_daipanel = sg.bucketGet(BUCKET_CONFIG, 'use_daipanel') or ''
    panel_group = sg.bucketGet(BUCKET_CONFIG, 'panel_group') or ''
    Vipmoney = float(sg.bucketGet(BUCKET_CONFIG, 'Vipmoney') or '1')
    coin = int(sg.bucketGet(BUCKET_CONFIG, 'coin') or '0')
    return osname, qlname, use_daipanel, panel_group, Vipmoney, coin


osname, qlname, use_daipanel, panel_group, Vipmoney, coin = get_user_content()
panel_client = None


def get_panel_client():
    global panel_client
    if panel_client is not None:
        return panel_client
    if use_daipanel and use_daipanel.lower() in ('true', '1', 'on'):
        panel_client = DumbPanelClient(osname, qlname if qlname else None)
    else:
        panel_client = QingLongClient(osname, qlname if qlname else None)
    return panel_client


def get_random_user_agent():
    ua_list = [
        'Mozilla/5.0 (Linux; Android 15; 2210132C Build/AQ3A.240812.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/135.0.7049.37 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 14; Pixel 6 Build/UQ1A.240605.004; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/133.0.6638.41 Mobile Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1'
    ]
    return random.choice(ua_list)


def generate_sign(phone):
    try:
        public_key_str = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDIj9Wu0HmxAazAeXaERwuuirtc
AQRFnYq6ZA/inXdgHB8DVmwYTG8PWsDsDoZjbzmxe7j8uMrmev0q6oOh3nJRuF+3
J4oTtTP5Pp5t+Y8L5xuqYbdN4PL0hHf3omarX0sMeIpXtn2KiKYybHUR67oFv/R4
eOty05luqQfTKyhfEQIDAQAB
-----END PUBLIC KEY-----"""
        public_key = RSA.import_key(public_key_str)
        cipher = PKCS1_v1_5.new(public_key)
        data = f"jac+{phone}"
        encrypted = cipher.encrypt(data.encode('utf-8'))
        return base64.b64encode(encrypted).decode('utf-8')
    except Exception as e:
        print(f"生成签名失败: {str(e)}")
        return None


def login_with_password(phone, password):
    try:
        login_url = f"{base_url2}:18280/v2driver/v2/login"
        headers = {
            'User-Agent': get_random_user_agent(),
            'Accept-Encoding': 'gzip',
            'Content-Type': 'application/json',
            'Host': 'jacwxmp.starnetah.com:18280',
            'deviceType': '1',
            'deviceModal': 'iPhone',
            'Referer': 'http://jacwxmp.starnetah.com:9201/',
            'Origin': 'http://jacwxmp.starnetah.com:9201',
            'osName': 'iOS 16.6.1',
            'versionType': '2'
        }
        md5_password = hashlib.md5(password.encode('utf-8')).hexdigest()
        sign = generate_sign(phone)
        if not sign:
            return {"success": False, "message": "生成签名失败"}
        data = {
            "appType": "0",
            "deviceType": "1",
            "password": md5_password,
            "phone": phone,
            "sendMessageKey": "default",
            "sign": sign
        }
        response = requests.post(login_url, headers=headers, json=data, timeout=10)
        result = response.json()
        if result.get('resultCode') == 200:
            return {
                "success": True,
                "message": "登录成功",
                "token": result.get('data', {}).get('token', ''),
                "userId": result.get('data', {}).get('id', ''),
                "phone": phone
            }
        else:
            return {"success": False, "message": result.get('message', '登录失败，请检查账号密码')}
    except Exception as e:
        print(f"账密登录失败: {str(e)}")
        return {"success": False, "message": str(e)}


def verify_account(login_body):
    try:
        phone = ""
        try:
            data = json.loads(login_body)
            if data.get("login_type") == "password":
                phone = data.get("phone", "")
                password = data.get("password", "")
                return login_with_password(phone, password)
            phone = data.get("phone", "")
            login_url = f"{base_url}:19000/v2driver/v4/login"
            headers = {
                'User-Agent': get_random_user_agent(),
                'Accept-Encoding': 'gzip',
                'Content-Type': 'application/json',
                'appType': '0'
            }
            response = requests.post(login_url, headers=headers, json=data, timeout=10)
        except json.JSONDecodeError:
            login_url = f"{base_url}:19000/v2driver/v4/login"
            headers = {
                'User-Agent': get_random_user_agent(),
                'Accept-Encoding': 'gzip',
                'Content-Type': 'application/json',
                'appType': '0'
            }
            response = requests.post(login_url, headers=headers, data=login_body, timeout=10)
        result = response.json()
        if result.get('resultCode') == 200:
            return {
                "success": True,
                "message": "登录成功",
                "token": result.get('data', {}).get('token', ''),
                "userId": result.get('data', {}).get('userId', ''),
                "phone": phone
            }
        else:
            return {"success": False, "message": result.get('message', '登录失败，请检查请求体')}
    except Exception as e:
        print(f"验证账号失败: {str(e)}")
        return {"success": False, "message": str(e)}


def get_user_info(token, user_id):
    try:
        headers = {
            'User-Agent': get_random_user_agent(),
            'Accept-Encoding': 'gzip',
            'Content-Type': 'application/json',
            'appType': '0',
            'token': token
        }
        data = {"uc_id": user_id}
        response = requests.post(f"{base_url}:19000/v2driver/getUserInfo",
                                headers=headers, json=data, timeout=10)
        result = response.json()
        if result.get('resultCode') == 200:
            return {"success": True, "data": result.get('data', {})}
        else:
            return {"success": False, "message": result.get('message', '获取用户信息失败')}
    except Exception as e:
        print(f"获取用户信息失败: {str(e)}")
        return {"success": False, "message": str(e)}


def get_points(token, user_id):
    try:
        headers = {
            'User-Agent': get_random_user_agent(),
            'Accept-Encoding': 'gzip',
            'Content-Type': 'application/json',
            'appType': '0',
            'token': token
        }
        data = {"uc_id": user_id}
        response = requests.post(f"{base_url}:19000/v2driver/queryIntegral",
                                headers=headers, json=data, timeout=10)
        result = response.json()
        if result.get('resultCode') == 200:
            return {"success": True, "points": result.get('data', {}).get('integralCounts', 0)}
        else:
            return {"success": False, "message": result.get('message', '获取积分信息失败')}
    except Exception as e:
        print(f"获取积分信息失败: {str(e)}")
        return {"success": False, "message": str(e)}


def update_ql_env(phone, account_info):
    remark = account_info.get('remark', phone)
    login_body = account_info.get('login_body', '')
    enable_comment = account_info.get('enable_comment', False)
    enable_post = account_info.get('enable_post', False)
    if not login_body:
        print(f"更新青龙变量失败: 没有有效的登录请求体")
        return False
    env_value = f"{remark}#{login_body}#{str(enable_comment).lower()}#{str(enable_post).lower()}"
    client = get_panel_client()
    if not client.is_configured():
        print("面板未配置")
        return False
    remark_str = f"江淮：{phone}"
    return client.update_env(phone, env_value, remark=remark_str, group=panel_group or '')


def delete_ql_env(phone):
    client = get_panel_client()
    if not client.is_configured():
        return False
    return client.delete_env(phone)


def pay_order(project, months, money):
    return True


def handle_auth_result(phone, account_info, months, money):
    def ql_callback(acc, info):
        return update_ql_env(acc, info)
    success = process_authorization(sender, BUCKET_AUTH, phone, account_info, months, update_ql_callback=ql_callback)
    if success:
        new_expire = '2099-12-31' or ''
        sender.reply(f"""
=====授权成功=====
📱 手机号: {mask_account(phone)}
⏰ 时长: {months}个月
📅 到期: {new_expire}
💰 金额: {money}元
==================""")
    return success


def batch_bind_account():
    sender.reply("""
=====批量账号登录=====
请输入账号信息，每行一个账号
格式：备注#手机号#密码#发帖开关#回帖开关
------------------
说明：
• 发帖开关和回帖开关可选，默认false
• 开关值：true/false 或 1/0
• 开启发帖或回帖封号几率大，谨慎开启
------------------
示例：
张三#13800138000#123456#true#false
王五#13700137000#abc123
------------------
回复"q"退出操作
==================""")

    batch_data = sender.input(120000, 1, False)
    if not batch_data:
        sender.reply("⏰ 操作超时,已退出")
        return
    elif batch_data.lower() == 'q':
        sender.reply("✅ 已取消登录")
        return

    lines = batch_data.strip().split('\n')
    total_count = len(lines)
    success_count = 0
    failed_accounts = []

    current_uservalue = sg.bucketGet(bucket=BUCKET_USER, key=userid)
    accounts = _sg_literal(current_uservalue) if current_uservalue else []

    sender.reply(f"⏳ 开始处理 {total_count} 个账号...")

    for index, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
        parts = line.split('#')
        if len(parts) < 3:
            failed_accounts.append({
                "line": index,
                "remark": parts[0] if len(parts) > 0 else f"账号{index}",
                "reason": "格式错误，至少需要：备注#手机号#密码"
            })
            continue

        remark = parts[0].strip()
        phone = parts[1].strip()
        password = parts[2].strip()
        enable_post = parts[3].strip().lower() in ('true', '1', 'yes', 'on') if len(parts) > 3 else False
        enable_comment = parts[4].strip().lower() in ('true', '1', 'yes', 'on') if len(parts) > 4 else False

        sender.reply(f"⏳ [{index}/{total_count}] 正在验证：{remark}...")
        login_result = login_with_password(phone, password)

        if not login_result.get('success'):
            failed_accounts.append({
                "line": index,
                "remark": remark,
                "phone": mask_account(phone),
                "reason": login_result.get('message', '登录失败')
            })
            continue

        try:
            login_body = json.dumps({"phone": phone, "password": password, "login_type": "password"})
            if phone not in accounts:
                accounts.append(phone)
            account_info = {
                "phone": phone, "remark": remark,
                "token": login_result.get('token', ''),
                "userId": login_result.get('userId', ''),
                "login_body": login_body,
                "enable_comment": enable_comment,
                "enable_post": enable_post
            }
            sg.bucketSet(BUCKET_TOKEN, phone, json.dumps(account_info))
            success_count += 1
            sender.reply(f"✅ [{index}/{total_count}] {remark} 绑定成功")
        except Exception as e:
            failed_accounts.append({
                "line": index, "remark": remark,
                "phone": mask_account(phone),
                "reason": f"保存失败：{str(e)}"
            })

    if success_count > 0:
        sg.bucketSet(BUCKET_USER, userid, str(accounts))

    result_msg = f"""
=====批量登录完成=====
📊 总计: {total_count} 个账号
✅ 成功: {success_count} 个
❌ 失败: {len(failed_accounts)} 个
=================="""
    if failed_accounts:
        result_msg += "\n\n失败详情：\n"
        for fail in failed_accounts:
            phone_info = f" ({fail['phone']})" if 'phone' in fail else ""
            result_msg += f"• [{fail['line']}] {fail['remark']}{phone_info}\n  原因: {fail['reason']}\n"
    sender.reply(result_msg)


def bind_account():
    sender.reply("""
=====江淮卡友登录=====
请选择登录方式：
[1] 账号密码登录
[2] 抓包请求体登录
------------------
回复数字选择登录方式
回复"q"退出操作
==================""")

    login_type = sender.input(120000, 1, False)
    if not login_type:
        sender.reply("⏰ 操作超时,已退出")
        return
    elif login_type.lower() == 'q':
        sender.reply("✅ 已取消登录")
        return

    phone = ""
    login_body = ""
    login_result = None

    if login_type == '1':
        sender.reply("""
=====账号密码登录=====
请选择登录模式：
[1] 单个账号登录
[2] 批量账号登录
------------------
回复数字选择模式
回复"q"退出操作
==================""")
        mode = sender.input(120000, 1, False)
        if not mode:
            sender.reply("⏰ 操作超时,已退出")
            return
        elif mode.lower() == 'q':
            sender.reply("✅ 已取消登录")
            return
        if mode == '2':
            batch_bind_account()
            return
        elif mode != '1':
            sender.reply("❌ 无效的选择")
            return

        sender.reply("=====账号密码登录=====\n请输入手机号：\n==================")
        phone_input = sender.input(120000, 1, False)
        if not phone_input:
            sender.reply("⏰ 操作超时,已退出")
            return
        elif phone_input.lower() == 'q':
            sender.reply("✅ 已取消登录")
            return
        phone = phone_input.strip()

        sender.reply("=====账号密码登录=====\n请输入密码：\n==================")
        password = sender.input(120000, 1, False)
        if not password:
            sender.reply("⏰ 操作超时,已退出")
            return
        elif password.lower() == 'q':
            sender.reply("✅ 已取消登录")
            return

        sender.reply("⏳ 正在验证账号...")
        login_result = login_with_password(phone, password)
        if login_result.get('success'):
            login_body = json.dumps({"phone": phone, "password": password, "login_type": "password"})
        else:
            sender.reply(f"=====登录失败=====\n❌ 原因: {login_result.get('message', '未知错误')}\n请检查账号密码\n==================")
            return

    elif login_type == '2':
        sender.reply("""=====抓包请求体登录=====
请输入获取到的请求体：
(通过抓包获取，URL为: http://jacwxmp.starnetah.com:19000/v2driver/v4/login)
==================""")
        login_body = sender.input(120000, 1, False)
        if not login_body:
            sender.reply("⏰ 操作超时,已退出")
            return
        elif login_body.lower() == 'q':
            sender.reply("✅ 已取消登录")
            return
        try:
            body_data = json.loads(login_body)
            if "phone" not in body_data:
                sender.reply("=====格式错误=====\n❌ 请求体中缺少phone字段\n==================")
                return
            phone = body_data.get("phone", "")
        except json.JSONDecodeError:
            sender.reply("=====提示=====\n⚠️ 检测到加密格式的请求体\n==================")

        sender.reply("⏳ 正在验证账号...")
        login_result = verify_account(login_body)
        if not login_result.get('success'):
            sender.reply(f"=====验证失败=====\n❌ 原因: {login_result.get('message', '未知错误')}\n==================")
            return
        result_phone = login_result.get('phone', '') or phone
        if not result_phone:
            sender.reply("=====输入手机号=====\n检测到加密格式，请手动输入手机号：\n==================")
            result_phone = sender.input(120000, 1, False)
            if not result_phone or result_phone.lower() == 'q':
                sender.reply("✅ 已取消登录")
                return
        phone = result_phone
    else:
        sender.reply("❌ 无效的选择")
        return

    if not login_result or not login_result.get('success'):
        sender.reply("=====登录失败=====\n❌ 账号验证失败\n请重试或检查配置\n==================")
        return

    sender.reply("=====发帖功能=====\n是否开启发帖功能？(封号概率大，谨慎开启)\n回复\"y\"开启\n==================")
    enable_post_input = sender.input(120000, 1, False)
    if not enable_post_input:
        sender.reply("⏰ 操作超时,已退出")
        return
    enable_post = enable_post_input.lower() == "y"

    sender.reply("=====回帖功能=====\n是否开启回帖功能？(封号概率大，谨慎开启)\n回复\"y\"开启\n==================")
    enable_comment_input = sender.input(120000, 1, False)
    if not enable_comment_input:
        sender.reply("⏰ 操作超时,已退出")
        return
    enable_comment = enable_comment_input.lower() == "y"

    sender.reply("=====账号备注=====\n请输入账号备注：\n==================")
    remark = sender.input(120000, 1, False)
    if not remark:
        sender.reply("⏰ 操作超时,已退出")
        return
    elif remark.lower() == 'q':
        sender.reply("✅ 已取消登录")
        return

    try:
        if not uservalue:
            sg.bucketSet(BUCKET_USER, userid, str([phone]))
        else:
            accounts = _sg_literal(uservalue)
            if phone not in accounts:
                accounts.append(phone)
                sg.bucketSet(BUCKET_USER, userid, str(accounts))

        account_info = {
            "phone": phone, "remark": remark,
            "token": login_result.get('token', ''),
            "userId": login_result.get('userId', ''),
            "login_body": login_body,
            "enable_comment": enable_comment,
            "enable_post": enable_post
        }
        sg.bucketSet(BUCKET_TOKEN, phone, json.dumps(account_info))

        sender.reply(f"""
=====绑定成功=====
👤 备注: {remark}
📱 手机号: {mask_account(phone)}
🔄 回复功能: {'已开启' if enable_comment else '未开启'}
📝 发帖功能: {'已开启' if enable_post else '未开启'}
==================""")

        auth_time = '2099-12-31'
        current_date = datetime.now().strftime("%Y-%m-%d")

        if auth_time and auth_time >= current_date:
            if update_ql_env(phone, account_info):
                ql_flag = "✅ 青龙变量更新成功"
            else:
                ql_flag = "❌ 青龙变量更新失败"
            sender.reply(f"""
=====账号已授权=====
📅 到期时间: {auth_time}
📅 当前时间: {current_date}
------------------
{ql_flag}
==================""")
        else:
            if auth_time and auth_time < current_date:
                sender.reply(f"⚠️ 账号授权已过期（到期:{auth_time}），需要重新授权")
            else:
                sender.reply("⚠️ 账号未授权，需要进行授权")
            sender.reply("正在为您开始授权流程...")
            authorize_account(phone, account_info)

    except Exception as e:
        sender.reply(f"=====绑定异常=====\n❌ 错误: {str(e)}\n==================")


def authorize_account(phone, account_info):
    return True


def authorize_multiple_accounts(phones):
    return True


def query_accounts():
    if not uservalue:
        sender.reply("=====未绑定账号=====\n❌ 未找到任何账号信息\n💡 发送 江淮登录 绑定\n==================")
        return

    _sg_literal(uservalue)
    accounts_list, selected = select_accounts(sender, BUCKET_USER, userid, BUCKET_AUTH, '江淮卡友')
    if not accounts_list or not selected:
        return

    sender.reply(f"✅ 已选择 {len(selected)} 个账号，正在查询...")
    query_count = 0
    for phone in selected:
        try:
            account_info = json.loads(sg.bucketGet(BUCKET_TOKEN, phone))
            if 'login_body' not in account_info:
                sender.reply(f"=====账号已过期=====\n📱 手机号: {mask_account(phone)}\n❌ 状态: 账号信息已过期，请重新绑定\n==================")
                continue
            login_result = verify_account(account_info.get('login_body', ''))
            if login_result.get('success'):
                account_info['token'] = login_result.get('token', '')
                account_info['userId'] = login_result.get('userId', '')
                sg.bucketSet(BUCKET_TOKEN, phone, json.dumps(account_info))
                auth_time = '2099-12-31'
                current_date = datetime.now().strftime("%Y-%m-%d")
                auth_status = '已授权' if auth_time and auth_time >= current_date else '未授权'
                get_user_info(account_info.get('token', ''), account_info.get('userId', ''))
                points_info = get_points(account_info.get('token', ''), account_info.get('userId', ''))
                points = points_info.get('points', 0) if points_info.get('success') else 0
                sender.reply(f"""
=====账号信息[{query_count+1}/{len(selected)}]=====
📱 手机号: {mask_account(phone)}
👤 备注: {account_info.get('remark')}
🔐 授权状态: {auth_status}
💰 当前积分: {points}
🔄 回复功能: {'已开启' if account_info.get('enable_comment') else '未开启'}
📝 发帖功能: {'已开启' if account_info.get('enable_post') else '未开启'}
==================""")
                query_count += 1
                if query_count < len(selected) and len(selected) > 3:
                    time.sleep(0.5)
            else:
                sender.reply(f"=====查询失败[{query_count+1}/{len(selected)}]=====\n📱 手机号: {mask_account(phone)}\n❌ 状态: {login_result.get('message', '账号验证失败')}\n==================")
                query_count += 1
        except Exception as e:
            sender.reply(f"=====查询异常[{query_count+1}/{len(selected)}]=====\n📱 手机号: {mask_account(phone)}\n❌ 错误: {str(e)}\n==================")
            query_count += 1

    if query_count > 0:
        sender.reply(f"✅ 查询完成，共查询了 {query_count} 个账号")


def manage_account():
    if not uservalue:
        sender.reply("=====未绑定账号=====\n❌ 未找到任何账号信息\n💡 发送 江淮登录 绑定\n==================")
        return

    accounts = _sg_literal(uservalue)
    menu = """
=====账号管理=====
[1] 授权账号
[2] 删除账号
[3] 提交面板
------------------
回复数字选择功能
回复"q"退出操作
=================="""
    sender.reply(menu)
    choice = sender.input(120000, 1, False)
    if not choice or choice.lower() == 'q':
        sender.reply("✅ 已退出操作")
        return

    accounts_list, selected = select_accounts(sender, BUCKET_USER, userid, BUCKET_AUTH, '江淮卡友')
    if not accounts_list or not selected:
        return

    sender.reply(f"✅ 已选择 {len(selected)} 个账号")

    if choice == '1':
        authorize_multiple_accounts(selected)

    elif choice == '2':
        sender.reply("=====确认删除=====\n⚠️ 此操作不可恢复\n回复 y 确认\n==================")
        confirm = sender.input(120000, 1, False)
        if confirm and confirm.lower() == 'y':
            success_count = 0
            for phone in selected:
                try:
                    if phone in accounts:
                        accounts.remove(phone)
                    sg.bucketDel(BUCKET_TOKEN, phone)
                    True
                    delete_ql_env(phone)
                    success_count += 1
                except Exception as e:
                    print(f"删除账号失败: {phone}, 错误: {str(e)}")
            if accounts:
                sg.bucketSet(BUCKET_USER, userid, str(accounts))
            else:
                sg.bucketDel(BUCKET_USER, userid)
            sender.reply(f"✅ 已成功删除 {success_count}/{len(selected)} 个账号")
        else:
            sender.reply("✅ 已取消删除")

    elif choice == '3':
        success_count = 0
        failed_accounts = []
        for phone in selected:
            try:
                account_info = json.loads(sg.bucketGet(BUCKET_TOKEN, phone))
                auth_time = '2099-12-31'
                current_date = datetime.now().strftime("%Y-%m-%d")
                if auth_time and auth_time >= current_date:
                    if update_ql_env(phone, account_info):
                        success_count += 1
                    else:
                        failed_accounts.append(f"{mask_account(phone)}(提交失败)")
                else:
                    failed_accounts.append(f"{mask_account(phone)}(未授权)")
                    sender.reply(f"⚠️ {mask_account(phone)} 未授权或已过期")
            except Exception as e:
                failed_accounts.append(f"{mask_account(phone)}(异常)")
                sender.reply(f"❌ {mask_account(phone)} 提交异常: {str(e)}")

        result_msg = f"""
=====提交结果=====
📊 选择账号: {len(selected)}个
✅ 提交成功: {success_count}个
❌ 提交失败: {len(failed_accounts)}个"""
        if failed_accounts:
            result_msg += "\n------------------\n失败账号:"
            for acc in failed_accounts:
                result_msg += f"\n• {acc}"
        result_msg += "\n=================="
        sender.reply(result_msg)
    else:
        sender.reply("❌ 无效的选择")


def show_tutorial():
    tutorial = """
=====江淮卡友使用教程=====
🔍 基础功能:
1. 江淮登录 - 绑定账号
2. 江淮查询 - 查看账号信息
3. 江淮管理 - 管理绑定账号
4. 江淮检测 - 检测并清理(管理员)
5. 江淮授权 - 按天数授权(管理员)
6. 江淮迁移 - 迁移旧数据桶(管理员)
==================
⚠️ 检测逻辑:
• 剩余天数>提前天数: 不提醒
• 剩余天数≤提前天数: 推送提醒
• 剩余天数≤0: 自动清理
• 每天9点自动执行检测
==================
❓ 遇到问题请检查配置
=================="""
    sender.reply(tutorial)


def migrate_data():
    """迁移旧数据桶到新数据桶"""
    if not sender.isAdmin():
        sender.reply("❌ 此功能仅限管理员使用")
        return

    BUCKET_MAPPING = {
        'jh_user': 's_jh_user',
        'jh_token': 's_jh_token',
        'jh_auth': 's_jh_auth',
        'jh_config': 's_jh',
        'jh_order': 's_jh_order',
    }

    sender.reply("""
=====数据迁移工具=====
⚠️ 此操作将把旧数据桶迁移到新数据桶
旧桶: jh_user, jh_token, jh_auth, jh_config, jh_order
新桶: s_jh_user, s_jh_token, s_jh_auth, s_jh, s_jh_order

回复 y 确认迁移
回复 q 取消操作
==================""")

    confirm = sender.input(120000, 1, False)
    if not confirm or confirm.lower() != 'y':
        sender.reply("✅ 已取消迁移")
        return

    sender.reply("⏳ 开始迁移数据...")
    migration_results = []

    for old_bucket, new_bucket in BUCKET_MAPPING.items():
        try:
            old_data = sg.bucketAll(old_bucket)

            if not old_data:
                migration_results.append(f"• {old_bucket} → {new_bucket}: 无数据")
                continue

            success_count = 0
            fail_count = 0
            len(old_data)

            for key, value in old_data.items():
                try:
                    sg.bucketSet(new_bucket, key, value)
                    success_count += 1
                except Exception as e:
                    fail_count += 1
                    print(f"迁移失败 {old_bucket}[{key}]: {str(e)}")

            result_msg = f"• {old_bucket} → {new_bucket}: 成功{success_count}条"
            if fail_count > 0:
                result_msg += f", 失败{fail_count}条"
            migration_results.append(result_msg)

        except Exception as e:
            migration_results.append(f"• {old_bucket} → {new_bucket}: 迁移异常 - {str(e)}")

    report = "=====迁移完成=====\n"
    report += "\n".join(migration_results)
    report += "\n=================="
    sender.reply(report)

    sender.reply("""
=====清理旧数据=====
是否清理旧数据桶？
⚠️ 清理后无法恢复！
回复 y 确认清理
回复 n 保留旧数据
==================""")

    clean_confirm = sender.input(120000, 1, False)
    if clean_confirm and clean_confirm.lower() == 'y':
        clean_results = []
        for old_bucket in BUCKET_MAPPING.keys():
            try:
                sg.bucketClear(old_bucket)
                clean_results.append(f"• {old_bucket}: 已清理")
            except Exception as e:
                clean_results.append(f"• {old_bucket}: 清理失败 - {str(e)}")

        clean_report = "=====清理完成=====\n"
        clean_report += "\n".join(clean_results)
        clean_report += "\n=================="
        sender.reply(clean_report)
    else:
        sender.reply("✅ 已保留旧数据")


def check_order(order_id):
    data = sg.bucketGet('s_jh_order', order_id)
    if not data:
        return '订单不存在'
    try:
        data = json.loads(data)
        status = {'pending': '待支付', 'success': '已完成', 'failed': '已取消'}.get(data['status'], '未知')
        msg = f"""
=====订单详情=====
📝 订单号: {order_id}
💰 金额: {data['amount']}元
⏰ 时长: {data['months']}月
📊 状态: {status}"""
        if data['status'] == 'success':
            msg += f"\n💵 实付: {data.get('paid_amount', 0)}元\n⌚ 支付时间: {data.get('pay_time', '')}"
        return msg
    except:
        return '查询失败'


def do_check_auth_status():
    try:
        sender.reply('该管理项已取消，账号直接运行')
    except Exception:
        pass
    return None
def do_admin_auth():
    return True


def main():
    imtype = sender.getImtype()
    usermessage = sender.getMessage()

    if '登录' in usermessage or '登陆' in usermessage:
        bind_account()
    elif '管理' in usermessage:
        manage_account()
    elif '查询' in usermessage:
        query_accounts()
    elif '教程' in usermessage:
        show_tutorial()
    elif '授权' in usermessage:
        do_admin_auth()
    elif '检测' in usermessage:
        if not sender.isAdmin():
            sender.reply("❌ 此功能仅限管理员使用")
        else:
            sender.reply("🔍 正在检测...")
            result = do_check_auth_status()
            sender.reply(result)
    elif '迁移' in usermessage:
        migrate_data()
    elif usermessage.startswith('JH_'):
        msg = check_order(usermessage)
        sender.reply(msg)
    elif imtype == 'fake':
        try:
            sg.notifyMasters(do_check_auth_status())
        except:
            pass
    else:
        sender.setContinue()


if __name__ == "__main__":
    main()
