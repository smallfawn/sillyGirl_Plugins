# [title: m116_今视频]
# [name: m116JinShiPin]
# [language: python]
# [class: 任务]
# [author: mrconli]
# [version: v1.0.2]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^今视频(.*)|(.*)今视频$]
# [cron: 46 8,18 * * *]
# [icon: http://img.jxdown.com/upload/2026-4/2026429923454752.jpg]
# [description: 无脚本提供；支持扫码登录和抓包批量登录，ck提交青龙，格式：token]
# [depe: ["requests","urllib3"]]

import asyncio as _sg_asyncio
import os as _sg_os
import time as _sg_time
import types as _sg_types
import json as _sg_json
from threading import Thread as _sg_Thread
from sillygirl import Adapter as _SGAdapter, Bucket as _SGBucket, Sender as _SGSender, sender as _sg_sender, plugin
calculate_auth_time = lambda *args, **kwargs: "2099-12-31"
try: import ast as _sg_ast
except Exception: _sg_ast=None
try: import decimal as decimal
except Exception: decimal=None

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
    "enable": plugin.Form.boolean().title("是否启用").default(True),
    'mrconli_jinshipin_bind': plugin.Form.string().title('登录方式').default('').description('0：所有方式，1：仅扫码登录，2：仅CK登录'),
    'mrconli_jinshipin_ql_config': plugin.Form.string().title('对接青龙').default('').description('|'),
    'mrconli_jinshipin_var_name': plugin.Form.string().title('环境变量名').default('').description('青龙容器内的变量名，默认为：m_jinshipin'),
    'mrconli_jinshipin_is_proxy': plugin.Form.boolean().title('是否启用代理').default(False).description('开启代理就勾选，其实不需要代理'),
    'mrconli_jinshipin_proxy_pool': plugin.Form.string().title('代理池地址').default('').description('代理API服务地址'),
})
_CONFIG_FIELD_MAP = {
    ('mrconli', 'jinshipin.bind'): 'mrconli_jinshipin_bind',
    ('mrconli', 'jinshipin.ql_config'): 'mrconli_jinshipin_ql_config',
    ('mrconli', 'jinshipin.var_name'): 'mrconli_jinshipin_var_name',
    ('mrconli', 'jinshipin.is_proxy'): 'mrconli_jinshipin_is_proxy',
    ('mrconli', 'jinshipin.proxy_pool'): 'mrconli_jinshipin_proxy_pool',
}

batch_size = 50     #  每页账号数量
scripts_name =  "今视频"
full_scripts_name =  "今视频"
bucket_prefix = "mrconli.jinshipin"

from decimal import Decimal  # 处理浮点数
import requests  # 处理http请求
import time  # 处理时间
import json  # 处理json数据
import re
from datetime import datetime
import uuid

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

senderID = sg.getSenderID()  # 获取发送者QQ号
sender = sg.Sender(senderID)  # 获取发送者对象
userid = sender.getUserID()  # 存储当前发送者的用户 ID，与 senderID 类似，但通常用于内部标识
uservalue = sg.bucketGet(bucket=f'{bucket_prefix}.user', key=userid)
today_date = datetime.now().date()
today_time = str(today_date)

MAX_RETRIES = 5  # 最大重试次数
IS_PROXY = sg.bucketGet(bucket_prefix, 'is_proxy')  # 是否启用代理True
PROXY_API = sg.bucketGet(bucket_prefix, 'proxy_pool') or "http://mrconli.com:12306"
proxy = None  # 初始化全局代理变量

def update_proxy():
    global proxy
    try:
        if not IS_PROXY or IS_PROXY == "false":
            proxy = None
            return
        response = requests.get(PROXY_API, timeout=15)
        ip = response.text.strip()
        if "请先添加白名单" in ip:
            raise ValueError("请配置代理白名单")
        proxy = {
            'http': ip,
            'https': ip,
        }
    except Exception as e:
        sender.reply(f"❌ 代理获取失败: {str(e)}")
        proxy = None

def _send_request(method, url, **kwargs):
    global proxy
    attempts = 0
    while attempts < MAX_RETRIES:
        try:
            if IS_PROXY:
                proxy = proxy if 'proxy' in globals() else None
                if not proxy:
                    update_proxy()
            kwargs['timeout'] = kwargs.get('timeout', 15)  # 默认超时时间 15 秒
            response = requests.request(
                method=method,
                url=url,
                proxies=proxy if IS_PROXY and proxy else None,
                verify=False,
                **kwargs
            )
            response.raise_for_status()
            return response
        except (requests.exceptions.ProxyError, requests.exceptions.Timeout) as e:
            print(f"⚠️ 代理异常: {str(e)}")
            if IS_PROXY:
                update_proxy()
                attempts += 1
                print(f"🔄 重试请求 ({attempts}/{MAX_RETRIES})")
                time.sleep(2)
        except requests.exceptions.RequestException as e:
            print(f"🚨 请求失败: {str(e)}")
            raise
    raise Exception(f"请求失败，超过最大重试次数: {MAX_RETRIES}")

def mask_phone(phone):
    if not phone or len(phone) != 11:
        return phone
    return f"{phone[:3]}****{phone[7:]}"

APPID = "wx9b368dd31bb430c3"  # App的微信AppID
BUNDLEID = "com.jxtv.jinshipin"  # App的BundleID
UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 18_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Html5Plus/1.0 (Immersed/20) uni-app"
DEFAULT_UA = "Mozilla/5.0 (Linux; Android 15; 2210132C Build/AQ3A.240812.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/130.0.6723.103 Mobile Safari/537.36 XWEB/1300473 MMWEBSDK/20250201 MMWEBID/9172 MicroMessenger/8.0.57.2820(0x28003939) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64"

def get_user_info(token):
    headers = {
        'User-Agent': "okhttp/4.9.2",
        'Accept-Encoding': "gzip",
        'appversion': "6.1.2",
        'channeltype': "jinshipin",
        'authorization': f"Bearer {token}",
        'os': "Android"
    }
    url = "https://app.jxgdw.com/api/v2/app/tab/template/list"
    params = {'tabId': "10113"}
    resp = _send_request('GET', url, params=params, headers=headers)
    data = resp.json()
    print(data)
    if 'result' not in data or len(data['result']) == 0:
        print("获取用户信息失败")
        return False, None, None, None
    user_info = data['result'][0]['userInfo']
    phone = user_info['phone']
    nickname = user_info['nickname']
    beans = user_info['jspBeanCount']
    return True, phone, nickname, beans

def get_qr_code():
    url = "https://open.weixin.qq.com/connect/app/qrconnect"
    params = {
        'appid': APPID,
        'bundleid': BUNDLEID,
        'scope': 'snsapi_userinfo',
        'state': 'wx_oauth_authorization_state',
        'pass_ticket': str(uuid.uuid4())
    }
    headers = {
        'User-Agent': DEFAULT_UA,
        'Referer': "https://open.weixin.qq.com/"
    }
    try:
        response = _send_request('GET', url, params=params, headers=headers)
        if response.status_code == 200:
            match = re.search(r'uuid\: *"(\w+)"', response.text)
            if match:
                return match.group(1)
    except Exception as e:
        print(f'获取二维码失败：{e}')
    return None

def check_scan_status(uuid_str):
    url = "https://long.open.weixin.qq.com/connect/l/qrconnect"
    params = {
        'uuid': uuid_str,
        'f': 'url',
        '_': int(time.time() * 1000)
    }
    headers = {
        'User-Agent': DEFAULT_UA,
        'Referer': "https://open.weixin.qq.com/"
    }
    try:
        response = _send_request('GET', url, params=params, headers=headers)
        if response.status_code == 200:
            print(response.text)
            if 'window.wx_errcode=405' in response.text:
                code_pattern = r'oauth\?code=([^&]+)&state='
                code_match = re.search(code_pattern, response.text)
                nickname_match = re.search(r"window\.wx_nickname='([^']+)'", response.text)
                if code_match:
                    code = code_match.group(1)
                    nickname = nickname_match.group(1) if nickname_match else "未知用户"
                    return {"code": code, "nickname": nickname}
            elif 'window.wx_errcode=408' in response.text:
                return {"status": "waiting"}
            elif 'window.wx_errcode=404' in response.text:
                return {"status": "expired"}
            else:
                return {"status": "unknown"}
    except Exception as e:
        print(f'检查扫码状态失败：{e}')
    return {"status": "error"}

def get_token_by_code(code):
    device_id = str(uuid.uuid4()).upper()
    url = "https://app.jxgdw.com/api/auth/wechat-login"
    headers = {
        'device': device_id,
        'Connection': 'keep-alive',
        'Accept-Encoding': 'br;q=1.0, gzip;q=0.9, deflate;q=0.8',
        'Content-Type': 'application/json',
        'os': 'iOS',
        'User-Agent': 'GVideo/6.1.2 (com.sobey.JiangXiTV; build:6.1.14; iOS 26.2.0) Alamofire/5.7.1',
        'Host': 'app.jxgdw.com',
        'appVersion': '6.1.2',
        'Accept-Language': 'zh-Hans-US;q=1.0',
        'Accept': '*/*'
    }
    body = json.dumps({"code": code})

    try:
        response = _send_request('POST', url, headers=headers, data=body)
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 0:
                phone = data.get('result', {}).get('userTokenVO', {}).get('user', {}).get('phone')
                token = data.get('result', {}).get('userTokenVO', {}).get('token')
                return True, phone, token
            else:
                print(f"登录失败！状态码: {response.status_code}")
                print(f"错误信息: {response.text}")
                return False, None, None
        else:
            print(f"登录失败！状态码: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False, None, None
    except Exception as e:
        print(f"请求异常: {e}")
        return False, None, None

def bind():
    login_guide = """
=====登录方式=====
[1] 扫码登录
[2] 抓包登录（支持批量）
------------------
回复数字选择方式
回复"q"退出"""
    sender.reply(login_guide)
    choice = sender.input(60000, recallDuration=60000, forGroup=False)
    if not choice:
        sender.reply('❌ 输入超时！')
        return
    if choice == 'q' or choice == 'Q':
        sender.reply('❌ 已退出登录操作！')
        return
    try:
        if choice == '1':
            scan_login()
        elif choice == '2':
            batch_login()
        else:
            sender.reply("❌ 无效的选择")
            return
    except Exception as e:
        sender.reply(f"❌ 登录失败: {str(e)}")
        return

def sms_send():
    sender.reply("短信登录暂不可用，请使用扫码登录或抓包登录")
    return None, None, None, None, None

def sms_login():
    account, u_token, uuid, oaid, device_id = sms_send()
    if account is None or u_token is None or oaid is None or device_id is None:
        sender.reply('❌ 登录失败，无法获取账户信息')
        return
    token = f"{u_token}#{device_id}"
    try:
        try:
            accounts = _sg_literal(uservalue or '[]')
        except (json.JSONDecodeError, TypeError):
            return
        auth = '2099-12-31'
        auth_status = "✅ 已授权" if auth and auth > today else "❌ 未授权"
        if account not in accounts:
            dlzt = "登录"
            accounts.append(account)
            sg.bucketSet(f'{bucket_prefix}.user', userid, json.dumps(accounts))
        else:
            dlzt = "更新"
            if not auth or auth < today_time:
                sender.reply("⚠️ 账号未授权或授权已过期，环境变量未提交青龙...")
            else:
                add_to_qinglong(token, account, userid)
        sg.bucketSet(f'{bucket_prefix}.token', account, token)
        sg.bucketSet(f'{bucket_prefix}.oaid', account, oaid)
        sg.bucketSet(f'{bucket_prefix}.uuid', account, uuid)
        if auth and auth > today:
            success_msg = f"""
=====星芽{dlzt}成功=====
📱 手机号: {mask_phone(account)}
🔐 授权状态: {auth_status}
⏰ 授权到期: {auth}
------------------
发送"{manage_cmd}"管理账号
发送"{query_cmd}"查询账号
"""
        else:
            success_msg = f"""
=====星芽{dlzt}成功=====
📱 手机号: {mask_phone(account)}
🔐 授权状态: {auth_status}
------------------
发送"{manage_cmd}"管理账号
发送"{query_cmd}"查询账号
"""
        sender.reply(success_msg)
    except Exception as e:
        sender.reply(f"❌ 处理登录失败: {str(e)}")
        return

def scan_login():
    uuid_str = get_qr_code()
    if not uuid_str:
        sender.reply("❌ 获取登录二维码失败，请稍后再试")
        return False
    qr_url = f"https://open.weixin.qq.com/connect/qrcode/{uuid_str}"
    sender.reply("请使用微信扫描下方二维码登录")
    sender.replyImage(qr_url)
    sender.replyImage("扫码后请在微信中点击「确认登录」\n等待扫码中...\n回复'q'取消操作")
    retry_count = 0
    max_retries = 90  # 最多等待90秒
    while retry_count < max_retries:
        try:
            message = sender.listen(1000)  # 等待1秒
            if message == 'q' or message == 'Q':
                sender.reply("❌ 已取消扫码登录")
                exit(0)
        except:
            pass
        result = check_scan_status(uuid_str)
        if isinstance(result, dict):
            if 'code' in result:
                code = result['code']
                nickname = result.get('nickname', '未知用户')
                sender.reply(f"{nickname} 扫码成功，正在处理登录...")
                break
            elif result.get('status') == 'waiting':
                pass
            elif result.get('status') == 'unknown':
                sender.reply("❌ 扫码出现未知状态，请重新尝试")
                return False, None, None
            elif result.get('status') == 'error':
                sender.reply("❌ 扫码出现错误，请重新尝试")
                return False, None, None
        retry_count += 1
        time.sleep(1)
    if max_retries <= retry_count:
        sender.reply("❌ 扫码超时，请重新尝试")
        exit(0)
    success, phone, token = get_token_by_code(code)
    if success:
        phone = str(phone)
        sg.bucketSet(f'{bucket_prefix}.token', phone, token)
        current_accounts = _sg_literal(sg.bucketGet(f'{bucket_prefix}.user', userid) or '[]')
        if phone not in current_accounts:
            status = f"{scripts_name}登录成功"
            accountVip = '2099-12-31'
            if not accountVip or accountVip < today_time:
                accountVip = "❌ 未授权"
            current_accounts.append(phone)
            sg.bucketSet(f'{bucket_prefix}.user', userid, json.dumps(current_accounts, ensure_ascii=False))
        else:
            status = f"{scripts_name}更新成功"
            accountVip = '2099-12-31'
            if not accountVip or accountVip < today_time:
                accountVip = "❌ 未授权"
                sender.reply("⚠️ 账号未授权或授权已过期，环境变量未提交青龙...")
            else:
                add_to_qinglong(token, phone, userid)
        sender.reply(f"""
====={status}=====
📱 账号: {mask_phone(phone)}
⏰ 授权到期：{accountVip}
==================""")
    else:
        sender.reply(f"❌ {nickname} 登录失败，请稍后重试")

def batch_login():
    global uservalue
    sender.reply(
        f"======={login_cmd}=======\n"
        "📝 请输入ck参数: token\n"
        "说明:\n"
        "  1. 支持批量，一个账号一行\n"
        "  2.不带Bearer前缀\n"
        "=====================\n"
        "⭐ 输入q退出操作\n"
    )
    success_count = 0
    add_count = 0
    update_count = 0
    fail_count = 0
    error_reasons = []

    accounts_str = sender.input(120000, 1, False)
    if accounts_str == 'q':
        sender.reply('❌ 已退出登录操作！')
        return
    if not accounts_str:
        sender.reply('❌ 输入超时！')
        return
    accounts = [line.strip() for line in accounts_str.split('\n') if line.strip()]

    total = len(accounts)
    if total == 0:
        sender.reply("❌ 未检测到有效账号信息")
        return

    sender.reply(f"🔍 共检测到 {total} 个账号，开始批量登录...")

    for index, account in enumerate(accounts, 1):
        try:

            success, phone, nickname, beans = get_user_info(account)
            if success:
                phone = str(phone)
                success_count += 1
                sg.bucketSet(f'{bucket_prefix}.token', phone, account)
                current_accounts = _sg_literal(sg.bucketGet(f'{bucket_prefix}.user', userid) or '[]')
                if phone not in current_accounts:
                    add_count += 1
                    status = f"✅ {mask_phone(phone)} 登录成功"
                    current_accounts.append(phone)
                    sg.bucketSet(f'{bucket_prefix}.user', userid, json.dumps(current_accounts, ensure_ascii=False))
                else:
                    update_count += 1
                    status = f"✅ {mask_phone(phone)} 更新成功"
                    accountVip = '2099-12-31'
                    if not accountVip or accountVip < today_time:
                        sender.reply("⚠️ 账号未授权或授权已过期，环境变量未提交青龙...")
                    else:
                        add_to_qinglong(account, phone, userid)
            else:
                print("登录失败")
                fail_count += 1
                error_reasons.append(f"❌ {account} 登录认证失败")
                continue

            uservalue = json.dumps(current_accounts)

            progress = f"[{index}/{total}] {status}"
            sender.reply(progress)
        except Exception as e:
            fail_count += 1
            error_msg = f"无效账号: {account}：{e}"
            error_reasons.append(error_msg)
            sender.reply(f"⚠️ 第{index}个账号处理失败: {error_msg}")
        time.sleep(2)

    report = (
        f"📊 登录完成\n"
        f"✅ 执行成功: {success_count} 个\n"
        f"➕ 添加: {add_count} 个\n"
        f"🔄 更新: {update_count} 个\n"
        f"✖️ 失败: {fail_count} 个\n"
        f"------------------------\n"
        f"发送“{manage_cmd}”管理账号\n"
        f"发送“{query_cmd}”查询账号\n"
    )

    if error_reasons:
        report += "\n❌ 失败原因:\n" + "\n".join(error_reasons[:5])
        if len(error_reasons) > 5:
            report += f"\n...等{len(error_reasons)-5}个错误"
    sender.reply(report)

def query():
    accounts = _sg_literal(uservalue or '[]')
    if not accounts:
        sender.reply(
            f'\n==={query_cmd}===\n❌ 未找到任何账号\n------------------\n💡 发送"{login_cmd}"绑定账号\n===================')
        return
    if len(accounts) > 1:
        total_pages = (len(accounts) + batch_size - 1) // batch_size
        for page in range(total_pages):
            start_idx = page * batch_size
            end_idx = min((page + 1) * batch_size, len(accounts))
            menu = f"==请选择查询账号(第{page + 1}/{total_pages}页)==\n[0] 查询全部账号\n------------------\n"
            for idx in range(start_idx, end_idx):
                acc = accounts[idx]
                menu += f"[{idx + 1}] {mask_phone(acc)} \n"
            menu += "====================\n⚠️ 请回复数字序号(输入q退出)\n💡 支持多选，如：1,3,4,7\n💡 支持范围选择，如：1-3,5-6,8"
            if total_pages > 1:
                menu += f"\n📊 当前页：{start_idx + 1}-{end_idx}，共{len(accounts)}个账号"
            sender.reply(menu)

        choice = sender.input(30000, 1, False)
        if not choice:
            sender.reply('❌ 输入超时！')
            return
        if choice.lower() == 'q':
            sender.reply('已取消查询')
            return

        if '-' in choice:
            ranges = [r.strip() for r in choice.split(',')]
            target_accounts = []

            for range_str in ranges:
                if '-' in range_str:
                    range_parts = range_str.split('-')
                    if len(range_parts) != 2:
                        sender.reply('❌ 范围格式错误，请使用如"1-3"的格式')
                        return

                    start_str, end_str = range_parts[0].strip(), range_parts[1].strip()
                    if not start_str.isdigit() or not end_str.isdigit():
                        sender.reply('❌ 范围格式错误，起始和结束必须是数字')
                        return

                    start_num, end_num = int(start_str), int(end_str)
                    if start_num < 1 or end_num > len(accounts) or start_num > end_num:
                        sender.reply(f'❌ 范围超出有效范围：1-{len(accounts)}')
                        return

                    for i in range(start_num, end_num + 1):
                        target_accounts.append(accounts[i - 1])
                else:
                    if not range_str.isdigit():
                        sender.reply(f'❌ 输入格式错误："{range_str}"不是有效数字')
                        return

                    c_num = int(range_str)
                    if c_num == 0:
                        target_accounts = accounts
                        break
                    elif 1 <= c_num <= len(accounts):
                        target_accounts.append(accounts[c_num - 1])
                    else:
                        sender.reply(f'❌ 选择超出范围：{c_num}')
                        return

            if target_accounts == accounts:
                sender.reply(f'正在查询全部{scripts_name}账号...')
            else:
                sender.reply(f'正在查询选中的{len(target_accounts)}个账号...')
        elif ',' in choice or '，' in choice:
            choices = [c.strip() for c in choice.split(',')]
            target_accounts = []

            for c in choices:
                if not c.isdigit():
                    sender.reply(f'❌ 输入格式错误："{c}"不是有效数字')
                    return

                c_num = int(c)
                if c_num == 0:
                    target_accounts = accounts
                    break
                elif 1 <= c_num <= len(accounts):
                    target_accounts.append(accounts[c_num - 1])
                else:
                    sender.reply(f'❌ 选择超出范围：{c_num}')
                    return

            if target_accounts == accounts:
                sender.reply(f'正在查询全部{scripts_name}账号...')
            else:
                sender.reply(f'正在查询选中的{len(target_accounts)}个账号...')
        else:
            if not choice.isdigit():
                sender.reply('输入格式错误，请回复数字')
                return

            choice_num = int(choice)
            if choice_num < 0 or choice_num > len(accounts):
                sender.reply('选择超出范围，已取消查询')
                return

            if choice_num == 0:
                target_accounts = accounts
                sender.reply(f'正在查询全部{scripts_name}账号...')
            else:
                target_accounts = [accounts[choice_num - 1]]
    else:
        target_accounts = accounts

    for account in target_accounts:
        try:
            accountVip = '2099-12-31'
            token = sg.bucketGet(f'{bucket_prefix}.token', account)
            if not token:
                sender.reply(f'❌ 【{mask_phone(account)}】ck获取失败')
                continue
            if not accountVip:
                sender.reply(f'❌ 【{mask_phone(account)}】账号未授权')
            elif accountVip < today_time:
                sender.reply(f'❌ 【{mask_phone(account)}】云授权过期')
            else:
                success, phone, nickname, beans = get_user_info(token)
                if not success:
                    sender.reply(f'❌ 【{mask_phone(account)}】查询失败')
                    continue
                sender.reply(f"""
===={scripts_name}账号详情====
📱 账号：{mask_phone(phone)}
👤 昵称：{nickname}
🫘 豆子：{beans}
⏰ 授权到期：{accountVip}
==================""")
        except Exception as e:
            sender.reply(f'❌ 【{mask_phone(account)}】查询出错: {str(e)}')

def cron_task():
    if imtype != 'fake':
        return
    try:
        users = sg.bucketAllKeys(f'{bucket_prefix}.user')
        for user in users:
            accounts = _sg_literal(sg.bucketGet(f'{bucket_prefix}.user', user) or '[]')
            for account in accounts:
                try:
                    auth = '2099-12-31'
                    sg.bucketGet(f'{bucket_prefix}.token', account)
                    if auth and auth <= today:
                        delete_from_qinglong(account)
                        notify_user(user, account, "授权已过期,环境变量已删除,请及时续费")
                        continue

                except Exception as e:
                    print(f"处理账号 {account} 出错: {str(e)}")
                    continue
    except Exception as e:
        print(f"定时任务出错: {str(e)}")

def notify_user(user, account, message):
    try:
        notify_msg = f"""
====={full_scripts_name}账号通知=====
📱 账号: {account}
📢 消息: {message}
=================="""
        sg.push('qq', '', user, '', notify_msg)
        sg.push('wx', '', user, '', notify_msg)
        sg.push('tg', '', user, '', notify_msg)
        sg.push('qx', '', user, '', notify_msg)
        sg.push('ipad', '', user, '', notify_msg)
    except Exception as e:
        print(f"发送通知失败: {str(e)}")

def get_config():
    try:
        var_name = sg.bucketGet(bucket_prefix, 'var_name') or "m_jinshipin"
        if not var_name:
            print("未配置变量名，使用默认值: m_jinshipin")
            var_name = 'm_jinshipin'
            sg.bucketSet(bucket_prefix, 'var_name', var_name)
        ql_config = sg.bucketGet(bucket_prefix, 'ql_config')
        if not ql_config:
            raise ValueError("青龙配置未设置")
        ql_params = ql_config.split('丨')
        if len(ql_params) != 3:
            raise ValueError("青龙配置格式错误，应为 地址丨ClientID丨ClientSecret")
        if len(ql_params) == 3:
            ql_host = ql_params[0]
            ql_client_id = ql_params[1]
            ql_client_secret = ql_params[2]
        else:
            print("青龙配置不完整，请检查配置")
        manage_cmd = sg.bucketGet(bucket_prefix, 'manage_cmd') or f'{scripts_name}管理'
        query_cmd = sg.bucketGet(bucket_prefix, 'query_cmd') or f'{scripts_name}查询'
        login_cmd = sg.bucketGet(bucket_prefix, 'login_cmd') or f'{scripts_name}登录'
        try:
            price = Decimal(sg.bucketGet(bucket_prefix, 'price') or '1')
            if price < 0:
                raise ValueError("价格不能为负数")
        except (ValueError, decimal.InvalidOperation):
            print("价格配置无效，使用默认值: 1")
            price = Decimal('1')
            sg.bucketSet(bucket_prefix, 'price', '1')
        try:
            coin_price = int(sg.bucketGet(bucket_prefix, 'coin') or '0')
            if coin_price < 0:
                raise ValueError("积分不能为负数")
        except ValueError:
            print("积分配置无效，使用默认值: 0")
            coin_price = 0
            sg.bucketSet(bucket_prefix, 'coin', '0')
        return (var_name, ql_host, ql_client_id, ql_client_secret, manage_cmd, query_cmd, login_cmd, price, coin_price)
    except Exception as e:
        error_msg = f"获取配置失败: {str(e)}"
        print(error_msg)
        sender.reply(f"❌ {error_msg}")
        raise

def init_qinglong():
    try:
        ql_config = sg.bucketGet(bucket_prefix, 'ql_config')
        if not ql_config:
            raise ValueError("青龙配置未设置")
        ql_host, ql_client_id, ql_client_secret = ql_config.split('丨')
        if not ql_host or not ql_client_id or not ql_client_secret:
            print("青龙配置不完整，请检查配置")
            exit(0)
        if not ql_host.endswith('/'):
            ql_host += '/'
        token = get_ql_token(ql_host, ql_client_id, ql_client_secret)
        return ql_host, token
    except Exception as e:
        sender.reply(f"❌ 连接青龙失败: {str(e)}")
        exit(0)

def get_ql_token(url, client_id, client_secret):
    try:
        if not url.endswith('/'):
            url += '/'
        r = requests.get(f'{url}open/auth/token?client_id={client_id}&client_secret={client_secret}')
        if r.status_code != 200:
            raise Exception(f"请求失败: {r.status_code}")
        data = r.json()
        if "token" not in data.get('data', {}):
            raise Exception("获取token失败")
        return data['data']['token']
    except Exception as e:
        raise Exception(f"获取token失败: {str(e)}")

def add_to_qinglong(token, account, username):
    try:
        url = f"{ql_host}/open/envs"
        headers = {
            "Authorization": f"Bearer {ql_token}",
            "Content-Type": "application/json"
        }

        existing_ids = []
        duplicate_vars = []
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            for env in response.json().get('data', []):
                if env['name'] == var_name and env.get('remarks', '') and account in env.get('remarks', ''):
                    existing_ids.append(env['id'])
                elif env['value'] == token:  # 新增重复值检测
                    duplicate_vars.append(env['id'])

        if duplicate_vars:
            del_response = requests.delete(url, json=duplicate_vars, headers=headers)
            if del_response.status_code != 200:
                raise Exception(f"删除冲突变量失败: {del_response.text}")

        if existing_ids:
            del_response = requests.delete(url, json=existing_ids, headers=headers)
            if del_response.status_code != 200:
                raise Exception(f"删除旧变量失败: {del_response.text}")

        auth_time = '2099-12-31'
        data = {
            "name": var_name,
            "value": token,
            "remarks": f"{full_scripts_name}账号:{account}丨用户:{username}丨授权时间:{auth_time}",
        }

        max_retries = 3
        for attempt in range(max_retries):
            response = requests.post(url, headers=headers, json=[data])
            if response.status_code == 200:
                new_ids = [item['id'] for item in response.json().get('data', [])]
                sg.bucketSet(f'{bucket_prefix}.env_id', account, json.dumps(new_ids))
                return True
            elif response.status_code == 500 and "SequelizeUniqueConstraintError" in response.text:
                print(f"🔄 检测到唯一性冲突，正在重试 ({attempt+1}/{max_retries})")
                time.sleep(1)

        error_detail = response.json().get('message') or response.text
        raise Exception(f"操作失败：多次尝试后仍存在唯一性冲突 | {error_detail} [HTTP {response.status_code}]")

    except Exception as e:
        error_msg = f"青龙操作失败: {str(e)}"
        print(error_msg)
        sender.reply(f"❌ {error_msg}")
        return False

def delete_from_qinglong(account):
    try:
        url = f"{ql_url}/open/envs"
        headers = {
            "Authorization": f"Bearer {ql_token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception("获取变量失败")
        env_id = None
        for env in response.json()['data']:
            if env['name'] == var_name and env.get('remarks', '') and account in env.get('remarks', ''):
                env_id = env['id']
                break
        if env_id:
            response = requests.delete(url, headers=headers, json=[env_id])
            if response.status_code != 200:
                raise Exception("删除变量失败")
        return True
    except Exception as e:
        sender.reply(f"❌ 青龙操作失败: {str(e)}")
        return False

def manage_accounts():
    accounts = _sg_literal(uservalue or "[]")
    if not accounts:
        sender.reply(f'❌ 未绑定账号，请先发送“{login_cmd}”')
        return
    menu = "=====账号管理=====\n" + "\n".join(
        f"[{i}] {mask_phone(account)}" for i, account in enumerate(accounts, 1)
    ) + "\n==================\n回复序号，输入 q 退出"
    sender.reply(menu)
    choice = sender.input(30000, 1, False).strip()
    if not choice or choice.lower() == "q":
        return
    if not choice.isdigit() or not 1 <= int(choice) <= len(accounts):
        sender.reply("❌ 账号序号无效")
        return
    show_account_menu(accounts[int(choice) - 1])

def show_account_menu(account):
    sender.reply(f"=====账号操作=====\n📱 {mask_phone(account)}\n[1] 查看 CK\n[2] 删除账号\n==================")
    choice = sender.input(30000, 1, False).strip()
    if choice == "1":
        show_ck(account)
    elif choice == "2":
        delete_account(account)

def log_operation(operation, user, account, status, message=''):
    try:
        log = {
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'operation': operation,
            'user': user,
            'account': account,
            'status': status,
            'message': message
        }
        logs = _sg_literal(sg.bucketGet(f'{bucket_prefix}.logs', 'operations') or '[]')
        logs.append(log)
        if len(logs) > 1000:  # 只保留最近1000条
            logs = logs[-1000:]
        sg.bucketSet(f'{bucket_prefix}.logs', 'operations', str(logs))
    except Exception as e:
        print(f"记录日志失败: {str(e)}")

def delete_account(account):
    try:
        if not delete_from_qinglong(account):
            raise Exception("从青龙删除变量失败")
        sg.bucketDel(f'{bucket_prefix}.token', account)
        True
        sg.bucketDel(f'{bucket_prefix}.env_id', account)

        try:
            accounts = _sg_literal(uservalue or "[]")
        except (json.JSONDecodeError, TypeError) as e:
            print(f"用户列表解析失败: {str(e)}")

        if account in accounts:
            accounts.remove(account)
            try:
                sg.bucketSet(f'{bucket_prefix}.user', userid, json.dumps(accounts, ensure_ascii=False))
            except Exception as e:
                raise Exception(f"用户列表更新失败: {str(e)}")
        sender.reply(f"""
=====删除成功=====
📱 账号: {mask_phone(account)}
✅ 状态: 已删除
==================""")
        log_operation('delete_account', userid, account, 'success')
        return True
    except Exception as e:
        error_msg = f"删除账号失败: {str(e)}"
        sender.reply(f"❌ {error_msg}")
        log_operation('delete_account', userid, account, 'failed', str(e))
        return False

def show_ck(account):
    token = sg.bucketGet(f'{bucket_prefix}.token', account)
    if token:
        sender.reply(f"""
====={full_scripts_name}账号ck=====
📱 账号: {mask_phone(account)}
🔑 CK: {token}
====================""")
    else:
        sender.reply(f"❌ {full_scripts_name}账号未绑定ck")

def tutorial():
    sender.reply(
        f"====={full_scripts_name}教程=====\n"
        f"1. {scripts_name}登录 - 绑定或更新账号\n"
        f"2. {scripts_name}查询 - 查询账号数据\n"
        f"3. {scripts_name}管理 - 查看 CK 或删除账号\n"
        "=================="
    )

def main():
    message = sender.getMessage()
    if any(word in message for word in ("登录", "登陆", "上车")):
        bind_choice = sg.bucketGet(bucket_prefix, "bind") or "0"
        if bind_choice in ("0", "所有方式"):
            bind()
        elif bind_choice in ("1", "仅短信登录"):
            sms_login()
        else:
            batch_login()
    elif "管理" in message:
        manage_accounts()
    elif "查询" in message:
        query()
    elif "教程" in message:
        tutorial()


if __name__ == "__main__":
    try:
        var_name, ql_host, ql_client_id, ql_client_secret, manage_cmd, query_cmd, login_cmd, price, coin_price = get_config()
        ql_url, ql_token = init_qinglong()
        imtype = sender.getImtype()
        today = str(datetime.now().date())
        if imtype == 'fake':
            cron_task()
        else:
            main()
    except Exception as e:
        sender.reply(f"❌ 运行出错: {str(e)}")
