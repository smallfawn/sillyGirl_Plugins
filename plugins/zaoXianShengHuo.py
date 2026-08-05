# [title: 早纤生活]
# [name: zaoXianShengHuo]
# [language: python]
# [class: 任务]
# [author: rujingxianghai]
# [version: v2.3]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(早纤|早纤生活)(登录|登陆)$|^登(录|陆)(早纤|早纤生活)$|^(早纤|早纤生活)(查询|管理|检测|提醒|教程)$|^(查询|管理|检测|提醒|教程)(早纤|早纤生活)$]
# [cron: 5 8 * * *]
# [icon: https://api.iconify.design/lucide:apple.svg]
# [description: 早纤生活插件；必须走邀请才有活动界面：https://img-upload.example.invalid/9ea8306e7362734cccd4151c38947333.jpeg]
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
    's_zx_qlname': form.string().title('设置对接容器').default('').description('青龙容器参数用丨分割'),
    's_zx_osname': form.string().title('青龙变量名').default('').description('青龙容器内早纤的变量名'),
    's_zx_notify': form.string().title('通知渠道').default('').description('检测通知推送渠道'),
    's_zx_default_version': form.string().title('默认APP版本号').default('').description('用户登录时自动使用的版本号'),
    's_zx_proxy_api': form.string().title('代理API地址').default('').description('返回格式 ip:port'),
    's_zx_invite_phone': form.string().title('邀请人手机号').default('').description('用户登录后需要验证邀请人信息'),
})
_CONFIG_FIELD_MAP = {
    ('s_zx', 'qlname'): 's_zx_qlname',
    ('s_zx', 'osname'): 's_zx_osname',
    ('s_zx', 'notify'): 's_zx_notify',
    ('s_zx', 'default_version'): 's_zx_default_version',
    ('s_zx', 'proxy_api'): 's_zx_proxy_api',
    ('s_zx', 'invite_phone'): 's_zx_invite_phone',
}

import os
import json
import time
import hashlib
import random
import re
import base64
import requests
from datetime import datetime, timedelta

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()
uservalue = sg.bucketGet(bucket='s_zx_user', key=userid)

PLUGIN_CONFIG = {'bucket': 's_zx', 'coin_key': 'dd_sign_points', 'name': '早纤生活'}
BASE_HOST = 'gw.yyzqsh.cn'
BASE_URL = f'http://{BASE_HOST}'
API = {
    "pwd_login": f"{BASE_URL}/api/web/auth/pwdLogin",
    "member_info": f"{BASE_URL}/api/web/member/getMemberInfo",
    "member_center": f"{BASE_URL}/api/web/member/getMemberCenterInfo",
    "contrib_detail": f"https://{BASE_HOST}/api/web/member/contributDetail/list",
    "ip_detail": f"https://{BASE_HOST}/api/web/member/ipDetail/page",
}
PAY_TYPE_NAMES = {'alipay': '支付宝', 'wxpay': '微信支付', 'qqpay': 'QQ钱包'}


def get_user_content():
    osname = sg.bucketGet('s_zx', 'osname') or 'S_ZXSH'
    qlname = sg.bucketGet('s_zx', 'qlname') or ''
    Vipmoney = float(sg.bucketGet('s_zx', 'Vipmoney') or '1')
    coin = sg.bucketGet(PLUGIN_CONFIG['bucket'], PLUGIN_CONFIG['coin_key'])
    if not coin:
        coin = sg.bucketGet('s_zx', 'coin') or '0'
    default_version = sg.bucketGet('s_zx', 'default_version') or '1.2.8'
    proxy_api = sg.bucketGet('s_zx', 'proxy_api') or ''
    invite_phone = sg.bucketGet('s_zx', 'invite_phone') or ''
    invite_reward_days = int(sg.bucketGet('s_zx', 'invite_reward_days') or '7')
    return osname, qlname, '早纤管理', '早纤查询', '早纤登录', Vipmoney, int(coin), default_version, proxy_api, invite_phone, invite_reward_days

def mask_account(account):
    if not account or len(account) < 4:
        return account
    if account.isdigit() and len(account) == 11:
        return f"{account[:3]}****{account[7:]}"
    if len(account) <= 16:
        return f"{account[:4]}****{account[-4:]}"
    return f"{account[:8]}****{account[-8:]}"

def md5_hash(text):
    return hashlib.md5(text.encode()).hexdigest().upper()

def generate_android_ua(version):
    build_number = random.randint(100, 200)
    android_version = f"{random.randint(12, 15)}.{random.randint(0, 1)}.0"
    return f"GZHealth/{version} (cn.yyzqsh.android; build:{build_number}; Android {android_version}) okhttp/4.10."

def decode_jwt_token(token):
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return {}
        payload_str = parts[1]
        padding = 4 - len(payload_str) % 4
        if padding != 4:
            payload_str += '=' * padding
        payload_bytes = base64.urlsafe_b64decode(payload_str)
        return json.loads(payload_bytes.decode('utf-8'))
    except:
        return {}

def get_proxy(proxy_api, max_retries=3):
    if not proxy_api:
        return None
    for attempt in range(max_retries):
        try:
            resp = requests.get(proxy_api, timeout=8)
            if resp.status_code == 200:
                proxy_text = resp.text.strip()
                if proxy_text.startswith('http'):
                    return {'http': proxy_text, 'https': proxy_text}
                return {'http': f'http://{proxy_text}', 'https': f'http://{proxy_text}'}
        except:
            pass
        time.sleep(1 + attempt)
    return None


def zx_pwd_login(phone, password):
    """账密登录"""
    _, _, _, _, _, _, _, _, proxy_api, _, _ = get_user_content()

    for attempt in range(3):
        try:
            headers = {
                "User-Agent": "okhttp/4.10.0",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "version": "v1.2.8",
                "platform": "Android",
                "Content-Type": "application/json; charset=UTF-8"
            }

            proxies = get_proxy(proxy_api) if proxy_api else None
            login_data = {"phone": phone, "password": md5_hash(password)}
            resp = requests.post(API["pwd_login"], headers=headers, json=login_data, timeout=10, proxies=proxies)
            result = resp.json()

            if result.get("code") != 200:
                return False, None, None, result.get("message", "登录失败")

            token = result.get("result", {}).get("token")
            if not token:
                return False, None, None, "获取Token失败"

            headers["Authorization"] = token
            resp = requests.post(API["member_info"], headers=headers, timeout=10, proxies=proxies)
            result = resp.json()

            if result.get("code") != 200:
                return False, token, None, result.get("message", "获取会员信息失败")

            return True, token, result.get("result", {}), None

        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            if attempt < 2:
                continue
            return False, None, None, "网络波动，请稍后重试"
        except:
            return False, None, None, "登录失败，请稍后重试"

    return False, None, None, "网络波动，请稍后重试"

def zx_get_basic_member_info(authorization, user_agent):
    """获取会员基本信息（phone, invitePhone等）"""
    try:
        _, _, _, _, _, _, _, _, proxy_api, _, _ = get_user_content()

        version_match = re.search(r'GZHealth/(\d+\.\d+\.\d+)', user_agent)
        platform_match = re.search(r'(iOS|Android) \d+\.\d+\.\d+', user_agent)

        if not version_match or not platform_match:
            return {"error": "UA格式错误"}

        headers = {
            "Host": BASE_HOST,
            "platform": platform_match.group(1),
            "version": version_match.group(1),
            "Authorization": authorization,
            "User-Agent": user_agent,
            "Content-Type": "application/json",
        }

        proxies = get_proxy(proxy_api) if proxy_api else None
        resp = requests.post(API['member_info'], headers=headers, json={}, timeout=20, proxies=proxies)

        if resp is None:
            return {"error": "请求失败，请重试"}

        data = resp.json()
        if data and data.get('success') and data.get('code') == 200:
            return data.get('result') or {}
        return {"error": data.get('message', '获取会员信息失败')}
    except Exception as e:
        return {"error": str(e)}

def zx_get_member_info(authorization, user_agent):
    """获取会员中心信息"""
    try:
        _, _, _, _, _, _, _, _, proxy_api, _, _ = get_user_content()

        version_match = re.search(r'GZHealth/(\d+\.\d+\.\d+)', user_agent)
        platform_match = re.search(r'(iOS|Android) \d+\.\d+\.\d+', user_agent)

        if not version_match or not platform_match:
            return {"error": "UA格式错误"}

        headers = {
            "Host": BASE_HOST,
            "platform": platform_match.group(1),
            "version": version_match.group(1),
            "Authorization": authorization,
            "User-Agent": user_agent,
            "Content-Type": "application/json",
        }

        proxies = get_proxy(proxy_api) if proxy_api else None
        resp = requests.post(API['member_center'], headers=headers, json={}, timeout=20, proxies=proxies)

        if resp is None:
            return {"error": "请求失败，请重试"}

        data = resp.json()
        if data and data.get('success') and data.get('code') == 200:
            return data.get('result') or {}
        return {"error": data.get('message', '获取会员信息失败')}
    except Exception as e:
        return {"error": str(e)}

def zx_get_contrib_detail(authorization, user_agent, page_size=5):
    """获取贡献值明细"""
    try:
        _, _, _, _, _, _, _, _, proxy_api, _, _ = get_user_content()

        version_match = re.search(r'GZHealth/(\d+\.\d+\.\d+)', user_agent)
        platform_match = re.search(r'(iOS|Android) \d+\.\d+\.\d+', user_agent)

        if not version_match or not platform_match:
            return []

        headers = {
            "Host": BASE_HOST,
            "platform": platform_match.group(1),
            "version": version_match.group(1),
            "Authorization": authorization,
            "User-Agent": user_agent,
            "Content-Type": "application/json",
        }

        url = f"{API['contrib_detail']}?pageNum=1&pageSize={page_size}&contributionType=1"
        proxies = get_proxy(proxy_api) if proxy_api else None
        resp = requests.get(url, headers=headers, timeout=20, proxies=proxies)

        data = resp.json()
        if data and data.get('success') and data.get('code') == 200:
            records = data.get('result', {}).get('records', [])
            return records[:page_size]
        return []
    except:
        return []

def zx_get_ip_detail(authorization, user_agent, page_size=5):
    """获取兑换值明细"""
    try:
        _, _, _, _, _, _, _, _, proxy_api, _, _ = get_user_content()

        version_match = re.search(r'GZHealth/(\d+\.\d+\.\d+)', user_agent)
        platform_match = re.search(r'(iOS|Android) \d+\.\d+\.\d+', user_agent)

        if not version_match or not platform_match:
            return []

        headers = {
            "Host": BASE_HOST,
            "platform": platform_match.group(1),
            "version": version_match.group(1),
            "Authorization": authorization,
            "User-Agent": user_agent,
            "Content-Type": "application/json",
        }

        proxies = get_proxy(proxy_api) if proxy_api else None
        date_month = datetime.now().strftime("%Y%m")
        request_body = {
            "dateMonth": date_month,
            "transactionTypeList": [1, 3],
            "pageNum": 1,
            "pageSize": page_size
        }
        resp = requests.post(API['ip_detail'], headers=headers, json=request_body, timeout=20, proxies=proxies)

        data = resp.json()
        if data and data.get('success') and data.get('code') == 200:
            records = data.get('result', {}).get('records', [])
            return records[:page_size]
        return []
    except:
        return []


def bind_account():
    osname, _, _, _, _, _, _, default_version, _, _, _ = get_user_content()

    sender.reply(
        "=====早纤生活登录=====\n"
        "[1] 账密登录\n"
        "[2] CK登录\n"
        "------------------\n"
        "请选择登录方式\n"
        "回复\"q\"退出\n"
        "=================="
    )
    login_type = sender.input(120000, 1, False)
    if not login_type:
        sender.reply("⏰ 操作超时")
        return
    if login_type.lower() == 'q':
        sender.reply("✅ 已取消")
        return

    if login_type == '1':
        sender.reply(
            "=====账密登录=====\n"
            "格式: 手机号#密码\n"
            "示例: 13800138000#123456\n"
            "------------------\n"
            "支持批量登录(换行分割)\n"
            "回复\"q\"退出\n"
            "=================="
        )
        input_text = sender.input(120000, 1, False)
        if not input_text:
            sender.reply("⏰ 操作超时")
            return
        if input_text.lower() == 'q':
            sender.reply("✅ 已取消")
            return

        lines = [line.strip() for line in input_text.split('\n') if line.strip() and '#' in line]
        if not lines:
            sender.reply("❌ 格式错误\n请输入: 手机号#密码")
            return

        total = len(lines)
        success_count = 0
        fail_count = 0
        need_auth_accounts = []  # 需要授权的账号列表

        if total > 1:
            sender.reply(f"🔄 检测到 {total} 个账号，开始批量登录...")

        for line in lines:
            parts = line.split('#', 1)
            if len(parts) < 2 or not parts[0].strip() or not parts[1].strip():
                fail_count += 1
                continue

            phone = parts[0].strip()
            password = parts[1].strip()

            if not phone.isdigit() or len(phone) != 11:
                sender.reply(f"❌ {phone} 手机号格式错误")
                fail_count += 1
                continue

            sender.reply(f"🔄 正在登录 {mask_account(phone)}... [{success_count + fail_count + 1}/{total}]")

            success, token, member_info, error_msg = zx_pwd_login(phone, password)
            if not success:
                sender.reply(f"❌ {mask_account(phone)} 登录失败: {error_msg}")
                fail_count += 1
                continue

            need_auth = _save_account(phone, token, member_info, batch_mode=(total > 1))
            if need_auth:
                need_auth_accounts.append(phone)
            success_count += 1

        if total > 1:
            sender.reply(f"=====批量登录完成=====\n✅ 成功: {success_count}\n❌ 失败: {fail_count}\n==================")
            if need_auth_accounts:
                sender.reply(f"📋 共 {len(need_auth_accounts)} 个账号需要授权")
                authorize_multiple_accounts(need_auth_accounts)

    elif login_type == '2':
        sender.reply(
            "=====CK登录=====\n"
            "格式: Authorization\n"
            "示例: eyJhbGci...\n"
            "------------------\n"
            "支持批量登录(换行分割)\n"
            "自动获取手机号作为备注\n"
            "回复\"q\"退出\n"
            "=================="
        )
        input_text = sender.input(120000, 1, False)
        if not input_text:
            sender.reply("⏰ 操作超时")
            return
        if input_text.lower() == 'q':
            sender.reply("✅ 已取消")
            return

        lines = [line.strip() for line in input_text.split('\n') if line.strip()]
        if not lines:
            sender.reply("❌ 格式错误\n请输入: Authorization")
            return

        total = len(lines)
        success_count = 0
        fail_count = 0
        need_auth_accounts = []  # 需要授权的账号列表

        if total > 1:
            sender.reply(f"🔄 检测到 {total} 个账号，开始批量登录...")

        for idx, authorization in enumerate(lines):
            if not authorization:
                fail_count += 1
                continue

            user_agent = generate_android_ua(default_version)

            sender.reply(f"🔄 正在验证第 {idx + 1} 个CK... [{success_count + fail_count + 1}/{total}]")

            member_info = zx_get_basic_member_info(authorization, user_agent)
            if 'error' in member_info:
                sender.reply(f"❌ 第 {idx + 1} 个CK校验失败: {member_info['error']}")
                fail_count += 1
                continue

            phone = member_info.get('phone', '')
            if not phone:
                sender.reply(f"❌ 第 {idx + 1} 个CK无法获取手机号")
                fail_count += 1
                continue


            need_auth = _save_ck_account(phone, authorization, user_agent, member_info, batch_mode=(total > 1))
            if need_auth:
                need_auth_accounts.append(phone)
            success_count += 1

        if total > 1:
            sender.reply(f"=====批量登录完成=====\n✅ 成功: {success_count}\n❌ 失败: {fail_count}\n==================")
            if need_auth_accounts:
                sender.reply(f"📋 共 {len(need_auth_accounts)} 个账号需要授权")
                authorize_multiple_accounts(need_auth_accounts)
    else:
        sender.reply("❌ 请选择 1 或 2")

def _save_account(phone, token, member_info, batch_mode=False):
    """保存账密登录的账号
    batch_mode: 批量模式，不处理授权，返回是否需要授权
    """
    osname, qlname, _, _, _, _, _, default_version, _, invite_phone_config, invite_reward_days = get_user_content()

    sender.reply(member_info)

    current_value = sg.bucketGet('s_zx_user', userid)
    if not current_value:
        sg.bucketSet('s_zx_user', userid, str([phone]))
    else:
        accounts = _sg_literal(current_value)
        if phone not in accounts:
            accounts.append(phone)
            sg.bucketSet('s_zx_user', userid, str(accounts))

    user_agent = generate_android_ua(default_version)
    account_info = {
        "phone": phone,
        "token": token,
        "user_agent": user_agent
    }
    sg.bucketSet('s_zx_token', phone, json.dumps(account_info))


    dqsj = datetime.now().strftime("%Y-%m-%d")
    accountVip = '2099-12-31'
    if accountVip and accountVip > dqsj:
        sender.reply(f"📱 {mask_account(phone)} 已授权，到期: {accountVip}")
        update_ql_env(phone, account_info)
        return False  # 不需要授权

    if invite_phone_config:
        invite_phone_actual = member_info.get('invitePhone', '') if member_info else ''
        if invite_phone_actual == invite_phone_config:
            free_phones = sg.bucketGet('s_zx_free_phone', userid) or ''
            free_phone_list = [p.strip() for p in free_phones.split(',') if p.strip()]

            if phone not in free_phone_list:
                today_date = datetime.now().date()
                new_vip = str(today_date + timedelta(days=invite_reward_days))
                True

                free_phone_list.append(phone)
                sg.bucketSet('s_zx_free_phone', userid, ','.join(free_phone_list))

                update_ql_env(phone, account_info)

                sender.reply(
                    f"=====邀请验证通过=====\n"
                    f"📱 账号: {mask_account(phone)}\n"
                    f"🎁 已赠送{invite_reward_days}天授权\n"
                    f"📅 到期: {new_vip}\n"
                    f"=================="
                )
                return False  # 不需要授权
        else:
            sender.reply(
                f"=====邀请人验证失败=====\n"
                f"❌ 邀请人手机号不匹配\n"
                f"📱 配置邀请人: {mask_account(invite_phone_config)}\n"
                f"📱 实际邀请人: {mask_account(invite_phone_actual) if invite_phone_actual else '无'}\n"
                f"=================="
            )
            if batch_mode:
                return True  # 需要授权
            sender.reply(f"📋 {mask_account(phone)} 需要授权")
            authorize_multiple_accounts([phone])
            return False

    if batch_mode:
        return True  # 需要授权
    sender.reply(f"📋 {mask_account(phone)} 需要授权")
    authorize_multiple_accounts([phone])
    return False

def _save_ck_account(phone, authorization, user_agent, member_info=None, batch_mode=False):
    """保存CK登录的账号
    member_info: 会员信息（包含phone, invitePhone等）
    batch_mode: 批量模式，不处理授权，返回是否需要授权
    """
    _, _, _, _, _, _, _, _, _, invite_phone_config, invite_reward_days = get_user_content()

    account_key = phone

    current_value = sg.bucketGet('s_zx_user', userid)
    if not current_value:
        sg.bucketSet('s_zx_user', userid, str([account_key]))
    else:
        accounts = _sg_literal(current_value)
        if account_key not in accounts:
            accounts.append(account_key)
            sg.bucketSet('s_zx_user', userid, str(accounts))

    account_info = {
        "phone": phone,
        "token": authorization,
        "user_agent": user_agent
    }
    sg.bucketSet('s_zx_token', account_key, json.dumps(account_info))


    dqsj = datetime.now().strftime("%Y-%m-%d")
    accountVip = '2099-12-31'
    if accountVip and accountVip > dqsj:
        sender.reply(f"📱 {mask_account(phone)} 已授权，到期: {accountVip}")
        update_ql_env(account_key, account_info)
        return False  # 不需要授权

    if invite_phone_config and member_info:
        invite_phone_actual = member_info.get('invitePhone', '')
        if invite_phone_actual == invite_phone_config:
            free_phones = sg.bucketGet('s_zx_free_phone', userid) or ''
            free_phone_list = [p.strip() for p in free_phones.split(',') if p.strip()]

            if phone not in free_phone_list:
                today_date = datetime.now().date()
                new_vip = str(today_date + timedelta(days=invite_reward_days))
                True

                free_phone_list.append(phone)
                sg.bucketSet('s_zx_free_phone', userid, ','.join(free_phone_list))

                update_ql_env(account_key, account_info)

                sender.reply(
                    f"=====邀请验证通过=====\n"
                    f"📱 账号: {mask_account(phone)}\n"
                    f"🎁 已赠送{invite_reward_days}天授权\n"
                    f"📅 到期: {new_vip}\n"
                    f"=================="
                )
                return False  # 不需要授权
        else:
            sender.reply(
                f"=====邀请人验证失败=====\n"
                f"❌ 邀请人手机号不匹配\n"
                f"📱 配置邀请人: {mask_account(invite_phone_config)}\n"
                f"📱 实际邀请人: {mask_account(invite_phone_actual) if invite_phone_actual else '无'}\n"
                f"=================="
            )
            if batch_mode:
                return True  # 需要授权
            sender.reply(f"📋 {mask_account(phone)} 需要授权")
            authorize_multiple_accounts([account_key])
            return False

    if batch_mode:
        return True  # 需要授权
    sender.reply(f"📋 {mask_account(phone)} 需要授权")
    authorize_multiple_accounts([account_key])
    return False


def query_accounts():
    if not uservalue:
        sender.reply(
            "=====未绑定账号=====\n"
            "❌ 未找到账号\n"
            "💡 发送 早纤登录 绑定\n"
            "=================="
        )
        return

    accounts = _sg_literal(uservalue)
    osname, _, _, _, _, _, _, default_version, _, _, _ = get_user_content()

    account_list = "\n========选择账号=======\n[0] 全部账号"
    for i, account in enumerate(accounts, 1):
        auth_time = '2099-12-31'
        if not auth_time:
            auth_status = '未授权'
        elif auth_time < str(datetime.now().date()):
            auth_status = '已过期'
        else:
            auth_status = f'到期:{auth_time}'

        try:
            token_data = sg.bucketGet('s_zx_token', account)
            if token_data:
                info = json.loads(token_data)
                display_name = info.get('remark') or mask_account(info.get('phone') or account)
            else:
                display_name = mask_account(account)
        except:
            display_name = mask_account(account)

        account_list += f"\n[{i}]{display_name}({auth_status})"
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

        for i, account in enumerate(selected, 1):
            try:
                token_data = sg.bucketGet('s_zx_token', account)
                if not token_data:
                    sender.reply(f"=====账号信息[{i}/{len(selected)}]=====\n📱 账号: {mask_account(account)}\n❌ 账号数据丢失，请重新登录\n==================")
                    continue

                account_info = json.loads(token_data)
                auth_time = '2099-12-31'

                if auth_time and auth_time >= str(datetime.now().date()):
                    auth_status = '已授权'
                else:
                    auth_status = '未授权'

                token = account_info.get('token', '')
                user_agent = account_info.get('user_agent') or generate_android_ua(default_version)
                display_name = account_info.get('remark') or mask_account(account_info.get('phone') or account)

                member_info_text = ""
                record_text = ""

                if token:
                    info = zx_get_member_info(token, user_agent)
                    if 'error' not in info:
                        member_info_text = (
                            f"\n📊 贡献值: {info.get('contribution', 0)}"
                            f"\n💎 兑换值: {info.get('ipValue', 0)}"
                        )

                    contrib_records = zx_get_contrib_detail(token, user_agent, 5)
                    if contrib_records:
                        record_text += "\n------------------\n📋 贡献值明细:"
                        for rec in contrib_records[:3]:
                            contrib_val = rec.get('contribution', 0)
                            create_time = rec.get('createTime', '')
                            record_text += f"\n  +{contrib_val} {create_time}"

                sender.reply(
                    f"=====账号信息[{i}/{len(selected)}]=====\n"
                    f"📱 账号: {display_name}\n"
                    f"🏷 状态: {auth_status}\n"
                    f"📅 到期: {auth_time or '未授权'}{member_info_text}"
                    f"{record_text}\n"
                    f"=================="
                )
            except Exception as e:
                sender.reply(f"=====查询失败=====\n❌ 错误: {str(e)}\n==================")

        sender.reply("✅ 查询完成")
    except Exception as e:
        sender.reply(f"❌ 查询失败: {str(e)}")


def manage_account():
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
    for i, account in enumerate(accounts, 1):
        auth_time = '2099-12-31'
        if not auth_time:
            auth_status = '未授权'
        elif auth_time < str(datetime.now().date()):
            auth_status = '已过期'
        else:
            auth_status = f'到期:{auth_time}'

        try:
            info = json.loads(sg.bucketGet('s_zx_token', account))
            display_name = info.get('remark') or mask_account(info.get('phone') or account)
        except:
            display_name = mask_account(account)

        account_list += f"\n[{i}]{display_name}({auth_status})"
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
            for account in selected:
                if account in accounts:
                    accounts.remove(account)
                sg.bucketDel('s_zx_token', account)
                True
                delete_ql_env(account)

            if accounts:
                sg.bucketSet('s_zx_user', userid, str(accounts))
            else:
                sg.bucketDel('s_zx_user', userid)
            sender.reply(f"✅ 已删除 {len(selected)} 个账号")
        else:
            sender.reply("✅ 已取消")
    elif choice == '3':
        success = 0
        for account in selected:
            try:
                account_info = json.loads(sg.bucketGet('s_zx_token', account))
                auth_time = '2099-12-31'
                if auth_time and auth_time >= str(datetime.now().date()):
                    if update_ql_env(account, account_info):
                        success += 1
            except:
                pass
        sender.reply(
            f"=====提交结果=====\n"
            f"✅ 成功: {success}个\n"
            f"❌ 失败: {len(selected) - success}个\n"
            f"=================="
        )


def authorize_multiple_accounts(accounts):
    return True


def generate_iframe_url(url):
    """将URL通过base64编码生成iframe页面链接"""
    try:
        encoded = base64.b64encode(url.encode('utf-8')).decode('utf-8')
        iframe_url = f"https://metwhale.github.io?u={encoded}"
        return iframe_url
    except:
        return url

def generate_qrcode(url):
    """生成二维码图片"""
    QRCODE_API_URL = "https://qrcode.example.invalid/api/qrcode/generate"
    QRCODE_API_KEY = ""

    try:
        response = requests.post(
            QRCODE_API_URL,
            json={"content": url},
            headers={"X-API-Key": QRCODE_API_KEY},
            timeout=10
        )
        if response.status_code == 200:
            result = response.json()
            if result.get('success') and result.get('data', {}).get('url'):
                return result['data']['url']
    except:
        pass

    try:
        encoded_url = requests.utils.quote(url)
        return f"https://api.qrtool.cn/?text={encoded_url}&size=300&level=M"
    except:
        return None

def handle_mapay_order(project, months, money, pay_type=None):
    return True

def pay_order(project, months, money):
    return True


def get_ql_token(host, client_id, client_secret):
    try:
        url = f'{host}/open/auth/token?client_id={client_id}&client_secret={client_secret}'
        resp = requests.get(url, timeout=10).json()
        if resp.get('code') == 200:
            return resp['data']['token']
        return None
    except:
        return None

def update_ql_env(account, account_info):
    token = account_info.get('token', '')
    user_agent = account_info.get('user_agent', '')
    if not token:
        return False

    version_match = re.search(r'GZHealth/(\d+\.\d+\.\d+)', user_agent)
    version = version_match.group(1) if version_match else ''
    env_value = f"{token}#{version}" if version else token

    qlconfig = sg.bucketGet('s_zx', 'qlname')
    if not qlconfig:
        return False

    configs = qlconfig.replace('|', '丨').split('丨')
    if len(configs) < 3:
        return False

    host, client_id, client_secret = [x.strip() for x in configs]

    try:
        ql_token = get_ql_token(host, client_id, client_secret)
        if not ql_token:
            return False

        headers = {'Authorization': f'Bearer {ql_token}'}
        osname = sg.bucketGet('s_zx', 'osname') or 'S_ZXSH'
        auth_time = '2099-12-31' or '未授权'
        display_name = account_info.get('remark') or mask_account(account_info.get('phone') or account)

        masked_account = mask_account(account)
        envs = requests.get(
            f'{host}/open/envs?searchValue={masked_account}',
            headers=headers,
            timeout=10
        ).json().get('data', [])
        env_id = next((e.get('id') for e in envs if e['name'] == osname), None)

        env_data = {
            'name': osname,
            'value': env_value,
            'remarks': f"早纤：{display_name}|用户:{userid}|到期:{auth_time}"
        }

        if env_id:
            env_data['id'] = env_id
            requests.put(f'{host}/open/envs', headers=headers, json=env_data, timeout=10)
            requests.put(f'{host}/open/envs/enable', headers=headers, json=[env_id], timeout=10)
        else:
            resp = requests.post(f'{host}/open/envs', headers=headers, json=[env_data], timeout=10).json()
            if resp.get('data'):
                new_id = resp['data'][0].get('_id') or resp['data'][0].get('id')
                if new_id:
                    requests.put(f'{host}/open/envs/enable', headers=headers, json=[new_id], timeout=10)
        return True
    except:
        return False

def delete_ql_env(account):
    qlconfig = sg.bucketGet('s_zx', 'qlname')
    if not qlconfig:
        return False

    configs = qlconfig.replace('|', '丨').split('丨')
    if len(configs) < 3:
        return False

    host, client_id, client_secret = [x.strip() for x in configs]

    try:
        ql_token = get_ql_token(host, client_id, client_secret)
        if not ql_token:
            return False

        headers = {'Authorization': f'Bearer {ql_token}'}
        osname = sg.bucketGet('s_zx', 'osname') or 'S_ZXSH'
        envs = requests.get(f'{host}/open/envs', headers=headers, timeout=10).json().get('data', [])

        for env in envs:
            if env['name'] == osname and account in env.get('remarks', ''):
                env_id = env.get('_id') or env.get('id')
                requests.delete(f'{host}/open/envs', headers=headers, json=[env_id], timeout=10)
                return True
        return False
    except:
        return False



def daily_checkin_reminder():
    """每日提醒已授权的账号登录APP点击"今日打卡"进行VX绑定"""
    notify = sg.bucketGet('s_zx', 'notify') or ''
    if not notify:
        return "❌ 未配置通知渠道"

    channels = [c.strip() for c in notify.split(',') if c.strip()]
    all_users = sg.bucketAllKeys('s_zx_user')
    if not all_users:
        return "❌ 没有用户"

    current_date = str(datetime.now().date())
    total_accounts, notified_users = 0, 0

    for user_id in all_users:
        try:
            accounts = _sg_literal(sg.bucketGet('s_zx_user', user_id) or '[]')

            authorized_accounts = []
            for acc in accounts:
                auth_time = '2099-12-31'
                if auth_time and auth_time >= current_date:
                    try:
                        info = json.loads(sg.bucketGet('s_zx_token', acc))
                        display_name = info.get('remark') or mask_account(info.get('phone') or acc)
                    except:
                        display_name = mask_account(acc)

                    authorized_accounts.append({
                        'name': display_name,
                        'auth_time': auth_time
                    })

            total_accounts += len(authorized_accounts)

            if authorized_accounts:
                account_list = "\n".join([
                    f"📱 {a['name']} (到期:{a['auth_time']})"
                    for a in authorized_accounts
                ])
                msg = (
                    f"=====🔔 早纤打卡提醒=====\n"
                    f"👋 早上好！别忘了打卡哦~\n"
                    f"------------------\n"
                    f"📋 您的账号:\n{account_list}\n"
                    f"------------------\n"
                    f"📲 请登录APP点击【今日打卡】\n"
                    f"🔗 完成微信绑定，才可打卡获取收益！\n"
                    f"===================="
                )
                for ch in channels:
                    try:
                        sg.push(
                            imType=ch,
                            groupCode='',
                            userID=user_id,
                            title="",
                            content=msg
                        )
                        notified_users += 1
                    except:
                        pass
        except:
            pass

    return f"✅ 打卡提醒完成，共 {total_accounts} 个有效账号，发送 {notified_users} 条通知"

def calculate_auth_time_by_days(account, days):
    return '2099-12-31'

def ks_auth():
    return True


def show_tutorial():
    """显示早纤生活教程"""
    tutorial = """=====早纤生活教程=====
📱 用户指令:
• 早纤登录 - 绑定早纤生活账号
• 早纤查询 - 查询账号状态和收益
• 早纤管理 - 授权/删除/提交青龙
• 早纤教程 - 查看本教程
------------------
🔧 管理员指令:
• 早纤授权 - 管理员按天数授权
• 早纤检测 - 检测过期账号并清理
• 早纤提醒 - 发送打卡提醒
------------------
💡 登录格式:
[1] 账密登录
📝 格式: 手机号#密码
📝 示例: 13812345678#password123
💡 账密登录会顶掉已登录的APP

[2] CK登录
📝 格式: Authorization
📝 示例: eyJhbGci...
💡 支持批量登录，每行一个CK
------------------
📝 账号获取方式:
1. 必须通过邀请链接才有活动页面，可检查配置获取
2. 使用手机号注册账号
3. 设置登录密码
------------------
💰 功能说明:
• 账号绑定: 保存账号信息到系统
• 状态查询: 查看贡献值、兑换值等
• 授权管理: 付费使用插件功能
• 青龙提交: 自动提交到青龙容器
• 过期检测: 到期前提醒，过期自动清理
• 打卡提醒: 每日提醒已授权用户打卡
------------------
🎯 使用流程:
1. 发送"早纤登录"绑定账号
2. 发送"早纤查询"查看账号状态
3. 发送"早纤管理"选择授权账号
4. 选择授权时长并完成支付
5. 系统自动提交到青龙容器
6. 每日登录APP点击"今日打卡"
------------------
⚠️ 注意事项:
• 授权后才能使用自动任务
• 过期账号会被自动清理
• 支持微信支付和积分兑换
• 必须通过邀请进入活动页面
• 每日需手动打卡绑定微信
=================="""
    sender.reply(tutorial)

def main():
    msg = sender.getMessage()

    if '登录' in msg or '登陆' in msg:
        bind_account()
    elif '查询' in msg and ('早纤' in msg or '早纤生活' in msg):
        query_accounts()
    elif '管理' in msg and ('早纤' in msg or '早纤生活' in msg):
        manage_account()
    elif '教程' in msg and ('早纤' in msg or '早纤生活' in msg):
        show_tutorial()
    elif '早纤授权' in msg or '早纤生活授权' in msg:
        ks_auth()
    elif ('检测' in msg or '清理' in msg) and ('早纤' in msg or '早纤生活' in msg):
        if not sender.isAdmin():
            sender.reply("❌ 仅限管理员")
            return
        sender.reply("🔍 正在检测...")
        sender.reply(check_auth_status())
    elif '提醒' in msg and ('早纤' in msg or '早纤生活' in msg):
        if not sender.isAdmin():
            sender.reply("❌ 仅限管理员")
            return
        sender.reply("🔔 正在发送打卡提醒...")
        sender.reply(daily_checkin_reminder())
    elif sender.getImtype() == 'fake':
        try:
            sg.notifyMasters(check_auth_status())
            daily_checkin_reminder()
        except:
            pass
    else:
        sender.setContinue()


if __name__ == "__main__":
    main()
