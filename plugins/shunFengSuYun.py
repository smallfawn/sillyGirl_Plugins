# [title: 顺丰速运]
# [name: shunFengSuYun]
# [language: python]
# [class: 任务]
# [author: sky2022]
# [version: v1.7.2]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^顺丰(登录|登陆|查询|管理|教程|Token刷新|刷新|快递查询|同步)$|^登(录|陆)顺丰$|^(查询|管理)顺丰$]
# [cron: 56 8,15 * * *]
# [icon: https://api.iconify.design/lucide:apple.svg]
# [description: 顺丰登录、查询、物流、账号管理、Token刷新与面板同步]
# [depe: ["requests"]]

import asyncio as _sg_asyncio
import os as _sg_os
import time as _sg_time
import types as _sg_types
from threading import Thread as _sg_Thread
from sillygirl import Adapter as _SGAdapter, Bucket as _SGBucket, Sender as _SGSender, sender as _sg_sender, plugin

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
    'dd_sf_panel_type': plugin.Form.string().title('对接面板类型').default('').description('填写你当前使用的面板类型，支持：青龙、青龙面板、QL、呆呆、呆呆面板、Daidai'),
    'dd_sf_panel_config': plugin.Form.string().title('对接面板配置').default('').description('统一填写面板对接参数。青龙：Host丨ClientID丨ClientSecret；呆呆：Host丨AppKey丨AppSecret；分隔符使用中文丨'),
    'dd_sf_panel_group': plugin.Form.string().title('对接面板分组').default('').description('仅呆呆面板生效。填写后新增或更新变量时会同步写入 group 字段；留空则不处理分组'),
    'dd_sf_dd_sf_osname': plugin.Form.string().title('面板变量名').default('').description('提交到面板中的顺丰变量名'),
    'dd_sf_show_other_coupons': plugin.Form.boolean().title('显示其他优惠券').default(False).description('是否显示除免单券外的其他优惠券(仅显示10元以上)'),
})
_CONFIG_FIELD_MAP = {
    ('dd_sf', 'panel_type'): 'dd_sf_panel_type',
    ('dd_sf', 'panel_config'): 'dd_sf_panel_config',
    ('dd_sf', 'panel_group'): 'dd_sf_panel_group',
    ('dd_sf', 'dd_sf_osname'): 'dd_sf_dd_sf_osname',
    ('dd_sf', 'show_other_coupons'): 'dd_sf_show_other_coupons',
}

import re
import ast
import hmac as _hmac
from datetime import datetime
import urllib.parse
import requests
import time
import json
import hashlib
import uuid
import random
import string

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()
uservalue = sg.bucketGet(bucket='dd_sf_user', key=userid)

SF_CAPTCHA_SEND_PATH = '/api/v1/sf/send-captcha'
SF_CAPTCHA_LOGIN_PATH = '/api/v1/sf/login'
SF_CAPTCHA_API_BASE_URL = 'http://115.190.238.245:17666'
SF_CAPTCHA_API_KEY = ''
SF_CAPTCHA_API_SECRET = ''
MOBILE_PATTERN = re.compile(r'^1[3-9]\d{9}$')
CAPTCHA_PATTERN = re.compile(r'^\d{4,8}$')

def format_message(title, content, status="info"):
    status_icons = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌",
        "loading": "⏳"
    }
    icon = status_icons.get(status, "ℹ️")
    return f"{icon} {title}\n{content}"

def format_account_info(login_mobile, _status="", _legacy_time="", **kwargs):
    lines = ["=====================", f"📱 账号: {login_mobile}"]
    labels = (("coin", "💎 总计积分"), ("today_coin", "🎯 今日积分"), ("account_status", "📈 账号检测"), ("express_count", "🚚 快递数量"), ("coupons", "🎫 大额优惠券"))
    lines.extend(f"{label}: {kwargs[key]}" for key, label in labels if key in kwargs)
    return "\n".join(lines + ["====================="])

def validate_input(value, max_count, field_name="输入"):
    try:
        value = int(value)
        if value > max_count or value == 0:
            sender.reply(format_message("输入无效", f"请输入 1-{max_count} 之间的数字", "error"))
            exit(0)
        return value
    except ValueError:
        sender.reply(format_message("输入无效", f"{field_name}必须是数字", "error"))
        exit(0)

def get_user_choice(prompt, timeout=120000, allow_quit=True):
    choice = sender.input(timeout, 1, False)
    if choice is None or choice == 'timeout':
        sender.reply('⏰ 操作超时,已退出')
        exit(0)
    elif allow_quit and (choice == 'q' or choice == 'Q'):
        sender.reply('✅ 已退出操作')
        exit(0)
    return choice

def mask_phone(phone):
    if len(phone) >= 11:
        return phone[:3] + '*' * 4 + phone[7:]
    return phone

def _build_captcha_auth_headers(path, body_bytes):
    ts = str(int(time.time()))
    nonce = uuid.uuid4().hex
    body_md5 = hashlib.md5(body_bytes).hexdigest()
    sign_str = f"{SF_CAPTCHA_API_KEY}|{ts}|{nonce}|{path}|{body_md5}"
    signature = _hmac.new(SF_CAPTCHA_API_SECRET.encode('utf-8'), sign_str.encode('utf-8'), hashlib.sha256).hexdigest()
    return {
        'X-API-Key': SF_CAPTCHA_API_KEY,
        'X-Timestamp': ts,
        'X-Nonce': nonce,
        'X-Signature': signature,
    }

def call_captcha_api(path, payload, timeout=30):
    base_url = str(SF_CAPTCHA_API_BASE_URL or '').rstrip('/')
    body_bytes = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    headers.update(_build_captcha_auth_headers(path, body_bytes))
    try:
        response = requests.post(
            f"{base_url}{path}",
            data=body_bytes,
            headers=headers,
            timeout=timeout,
            verify=False
        )
    except requests.RequestException as exc:
        raise ValueError('请求验证码接口失败') from exc

    if response.status_code >= 400:
        try:
            err = response.json()
            msg = err.get('message') or err.get('code') or f'HTTP {response.status_code}'
        except Exception:
            msg = f'HTTP {response.status_code}'
        raise ValueError(f'验证码接口请求失败: {msg}')

    try:
        result = response.json()
    except ValueError as exc:
        raise ValueError('验证码接口返回的不是 JSON') from exc

    if not isinstance(result, dict):
        raise ValueError('验证码接口返回格式异常')

    return result

def send_sf_sms_captcha(mobile):
    result = call_captcha_api(SF_CAPTCHA_SEND_PATH, {'mobile': mobile})
    if not result.get('success'):
        raise ValueError(result.get('message') or '验证码发送失败')
    return result.get('message')

def build_sms_token_data(account, mobile, data):
    return json.dumps(
        {
            'userId': data.get('userId', '') or data.get('memberId', '') or data.get('login_user_id', ''),
            'memNo': data.get('memNo', ''),
            'mobile': mobile,
            'sign': data.get('sign', ''),
            'deviceId': data.get('deviceId', ''),
            'srcDeviceGuid': data.get('srcDeviceGuid', ''),
            'clientVersion': data.get('clientVersion', ''),
            'ck': data.get('ck', ''),
            'appToken': data.get('token', '') or data.get('appToken', ''),
        },
        ensure_ascii=False,
    )

def login_with_sms_api(mobile, captcha):
    result = call_captcha_api(SF_CAPTCHA_LOGIN_PATH, {'mobile': mobile, 'captcha': captcha})
    if not result.get('success'):
        raise ValueError(result.get('message') or '验证码登录失败')

    data = result.get('data') or {}
    if not isinstance(data, dict):
        raise ValueError('验证码登录接口返回格式异常')

    ck = str(data.get('ck', '')).strip()
    if not ck:
        raise ValueError('验证码登录接口未返回 CK')

    account = str(data.get('login_mobile') or data.get('mobile') or mobile).strip()
    if not account:
        raise ValueError('验证码登录接口未返回账号手机号')

    token_data = build_sms_token_data(account, account, data)
    return token_data, account, mask_phone(account)

def parse_accounts(account_data):
    if not account_data:
        return []
    try:
        if isinstance(account_data, (list, tuple, set)):
            accounts = list(account_data)
        elif isinstance(account_data, str):
            normalized = account_data.strip()
            if not normalized or normalized in ('{}', '[]'):
                return []
            try:
                parsed = ast.literal_eval(normalized)
            except Exception:
                return [normalized]
            if isinstance(parsed, (list, tuple, set)):
                accounts = list(parsed)
            elif parsed is None:
                return []
            else:
                accounts = [str(parsed)]
        else:
            accounts = [str(account_data)]

        return list(dict.fromkeys(str(item) for item in accounts if item))
    except Exception:
        return []

def normalize_panel_type(panel_type_value, legacy_use_daidai_value='false'):
    value = str(panel_type_value or '').strip().lower()

    if value in ('呆呆', '呆呆面板', 'daidai', 'dd'):
        return 'daidai'
    if value in ('青龙', '青龙面板', 'qinglong', 'ql'):
        return 'qinglong'
    if value:
        return ''

    legacy_value = str(legacy_use_daidai_value or '').strip().lower()
    if legacy_value == 'true':
        return 'daidai'
    return 'qinglong'

def getusercontent():
    panel_type = normalize_panel_type(sg.bucketGet('dd_sf', 'panel_type'))
    return (
        sg.bucketGet('dd_sf', 'dd_sf_osname') or 'sfsyUrl', sg.bucketGet('dd_sf', 'panel_config'),
        '顺丰管理', '顺丰查询', '顺丰登录', None, None,
        sg.bucketGet('dd_sf', 'show_point_status') != 'false',
        sg.bucketGet('dd_sf', 'show_other_coupons') == 'true', None,
        panel_type == 'daidai', sg.bucketGet('dd_sf', 'ddname'), sg.bucketGet('dd_sf', 'panel_group') or '',
    )


def seekql():
    try:
        if not dd_sf_qlname:
            sender.reply(format_message("配置错误",
                "未配置青龙面板信息\n请在插件配置中填写:\n• 对接面板类型: 青龙\n• 对接面板配置: Host丨ClientID丨ClientSecret\n• 使用中文丨分隔\n• 示例:\nhttp://ql.example.com丨abcd丨1234", "error"))
            exit(0)

        qllist = dd_sf_qlname.split('丨')
        if len(qllist) != 3:
            sender.reply(format_message("格式错误",
                f"青龙面板配置格式错误\n当前格式: {dd_sf_qlname}\n正确格式:\nHost丨ClientID丨ClientSecret", "error"))
            exit(0)

        QLurl = qllist[0].strip()
        ClientID = qllist[1].strip()
        ClientSecret = qllist[2].strip()

        if not all([QLurl, ClientID, ClientSecret]):
            sender.reply(format_message("参数错误",
                "青龙面板配置参数不完整\n请确保以下参数都已填写:\n• 青龙面板地址(Host)\n• 应用ID(ClientID)\n• 应用密钥(ClientSecret)", "error"))
            exit(0)

        if not QLurl.startswith(('http://', 'https://')):
            sender.reply(format_message("地址错误",
                f"青龙地址格式错误\n当前地址: {QLurl}\n正确格式:\n• http://qinglong.example.com\n• https://ql.example.com:5700", "error"))
            exit(0)

        try:
            qltoken = QLtoken(QLurl=QLurl, ClientID=ClientID, ClientSecret=ClientSecret)
            return QLurl, qltoken
        except Exception as e:
            raise Exception(f"获取Token失败: {str(e)}")

    except Exception as e:
        sender.reply(format_message("连接失败",
            f"无法连接青龙面板\n请检查:\n1. 青龙面板是否运行\n2. 网络是否正常\n3. 配置是否正确\n4. 错误信息: {str(e)}\n\n当前配置:\n• 地址: {QLurl if 'QLurl' in locals() else '未设置'}\n• 应用ID: {ClientID[:4] + '****' if 'ClientID' in locals() else '未设置'}", "error"))
        exit(0)

def get_ql_headers(content_type="application/json"):
    return {
        "Authorization": f"Bearer {qltoken}",
        "accept": "application/json",
        "Content-Type": content_type
    }

def delenvs(id):
    if use_daidai:
        dd_delenvs(id)
        return
    if id is None:
        return
    url = f"{QLurl}/open/envs"
    headers = get_ql_headers()
    data = [id]
    requests.delete(url, headers=headers, json=data).json()

def allenvs(osname, account):
    if use_daidai:
        return dd_allenvs(osname, account)
    url = f"{QLurl}/open/envs"
    headers = get_ql_headers()
    response = requests.get(url=url, headers=headers).json()

    if response['code'] == 200:
        envslist = response['data']
        for envs in envslist:
            envname = envs['name']
            remarks = envs['remarks']
            if remarks is None:
                continue
            if osname == envname and str(account) in remarks:
                return envs['id']
        return None
    else:
        sender.reply(format_message("连接失败", "连接青龙获取变量失败", "error"))
        exit(0)

def Addenvs(osname, value, account, phone, target_userid=None, expire_time=None):
    phone = mask_phone(phone)
    target_userid if target_userid else userid

    if use_daidai:
        env_id = dd_allenvs(osname, account)
        if env_id is None:
            DDcreate(osname, value, account, phone, target_userid, expire_time)
        else:
            DDupdate(osname, value, account, env_id, phone, target_userid, expire_time)
        return

    qlid = allenvs(osname, account)

    if qlid is None:
        QLzt(osname, value, account, phone, target_userid, expire_time)
    else:
        QLupdate(osname, value, account, qlid, phone, target_userid, expire_time)

def QLupdate(osname, value, account, qlid, phone, target_userid=None, expire_time=None):
    actual_userid = target_userid if target_userid else userid
    expire_info = f'丨到期:{expire_time}' if expire_time else ''
    qlurl = f"{QLurl}/open/envs"

    data = {
        "value": value,
        "name": osname,
        "remarks": f'顺丰:{account}丨用户:{actual_userid}丨手机:{phone}{expire_info}丨顺丰管理',
        "id": qlid
    }

    headers = get_ql_headers()
    response = requests.put(qlurl, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_json = response.json()
        data = response_json['data']
        if data is None:
            exit(0)
        return data['id'], data['createdAt']
    else:
        sender.reply(format_message("更新失败", "更新变量失败,请稍后重试", "error"))
        exit(0)

def QLzt(osname, value, account, phone, target_userid=None, expire_time=None):
    try:
        actual_userid = target_userid if target_userid else userid
        expire_info = f'丨到期:{expire_time}' if expire_time else ''
        qlurl = f"{QLurl}/open/envs"

        data = [{
            "value": value,
            "name": osname,
            "remarks": f'顺丰:{account}丨用户:{actual_userid}丨手机:{phone}{expire_info}丨顺丰管理'
        }]

        headers = get_ql_headers()
        response = requests.post(qlurl, headers=headers, json=data)

        if response.status_code != 200:
            sender.reply(format_message("添加变量失败", f"请求失败\n状态码: {response.status_code}", "error"))
            exit(0)

        result = response.json()
        if result.get('code') != 200:
            sender.reply(format_message("添加变量失败", f"青龙返回错误\n错误信息: {result.get('message')}", "error"))
            exit(0)

        if "value must be unique" in response.text:
            return

        data = result.get('data')
        if not data or not isinstance(data, list) or len(data) == 0:
            sender.reply(format_message("添加变量失败", "青龙返回数据异常", "error"))
            exit(0)

        return data[0].get('id')

    except Exception as e:
        sender.reply(format_message("系统错误", f"添加青龙变量失败\n错误信息: {str(e)}", "error"))
        exit(0)

def QLtoken(QLurl, ClientID, ClientSecret):
    try:
        url = f'{QLurl}/open/auth/token?client_id={ClientID}&client_secret={ClientSecret}'
        response = requests.get(url)

        if response.status_code != 200:
            sender.reply(format_message("请求失败",
                f"青龙API请求失败\n状态码: {response.status_code}\n请检查:\n• API地址是否正确\n• 面板是否正常运行", "error"))
            exit(0)

        result = response.json()
        if "token" in result.get('data', {}):
            return result['data']['token']
        else:
            sender.reply(format_message("认证失败",
                "获取Token失败\n请检查:\n• ClientID是否正确\n• ClientSecret是否正确\n• 应用是否有权限", "error"))
            exit(0)

    except requests.exceptions.RequestException as e:
        sender.reply(format_message("网络错误",
            f"连接青龙面板失败\n请检查:\n• 青龙地址是否正确\n• 网络是否正常\n• 错误信息: {str(e)}", "error"))
        exit(0)
    except Exception as e:
        sender.reply(format_message("系统错误",
            f"处理请求时出错\n请检查:\n• 配置格式是否正确\n• 错误信息: {str(e)}", "error"))
        exit(0)

def seekdd():
    try:
        if not dd_sf_ddname:
            sender.reply(format_message("配置错误",
                "未配置呆呆面板信息\n请在插件配置中填写:\n• 对接面板类型: 呆呆\n• 对接面板配置: Host丨AppKey丨AppSecret\n• 使用中文丨分隔", "error"))
            exit(0)

        ddlist = dd_sf_ddname.split('丨')
        if len(ddlist) != 3:
            sender.reply(format_message("格式错误",
                f"呆呆面板配置格式错误\n当前格式: {dd_sf_ddname}\n正确格式:\nHost丨AppKey丨AppSecret", "error"))
            exit(0)

        DDurl = ddlist[0].strip()
        AppKey = ddlist[1].strip()
        AppSecret = ddlist[2].strip()

        if not all([DDurl, AppKey, AppSecret]):
            sender.reply(format_message("参数错误",
                "呆呆面板配置参数不完整\n请确保以下参数都已填写:\n• 面板地址(Host)\n• AppKey\n• AppSecret", "error"))
            exit(0)

        if not DDurl.startswith(('http://', 'https://')):
            sender.reply(format_message("地址错误",
                f"呆呆面板地址格式错误\n当前地址: {DDurl}\n正确格式:\n• http://panel.example.com\n• https://panel.example.com", "error"))
            exit(0)

        try:
            ddtoken = DDtoken(DDurl=DDurl, AppKey=AppKey, AppSecret=AppSecret)
            return DDurl, ddtoken
        except Exception as e:
            raise Exception(f"获取Token失败: {str(e)}")

    except SystemExit:
        raise
    except Exception as e:
        sender.reply(format_message("连接失败",
            f"无法连接呆呆面板\n请检查:\n1. 面板是否运行\n2. 网络是否正常\n3. 配置是否正确\n4. 错误信息: {str(e)}\n\n当前配置:\n• 地址: {DDurl if 'DDurl' in locals() else '未设置'}\n• AppKey: {AppKey[:4] + '****' if 'AppKey' in locals() else '未设置'}", "error"))
        exit(0)

def DDtoken(DDurl, AppKey, AppSecret):
    try:
        url = f'{DDurl}/api/open-api/token'
        data = {"app_key": AppKey, "app_secret": AppSecret}
        response = requests.post(url, json=data)

        if response.status_code != 200:
            sender.reply(format_message("请求失败",
                f"呆呆面板API请求失败\n状态码: {response.status_code}\n请检查:\n• API地址是否正确\n• 面板是否正常运行", "error"))
            exit(0)

        result = response.json()
        access_token = result.get('data', {}).get('access_token')
        if access_token:
            return access_token
        else:
            sender.reply(format_message("认证失败",
                "获取Token失败\n请检查:\n• AppKey是否正确\n• AppSecret是否正确\n• 应用是否有权限", "error"))
            exit(0)

    except requests.exceptions.RequestException as e:
        sender.reply(format_message("网络错误",
            f"连接呆呆面板失败\n请检查:\n• 面板地址是否正确\n• 网络是否正常\n• 错误信息: {str(e)}", "error"))
        exit(0)
    except SystemExit:
        raise
    except Exception as e:
        sender.reply(format_message("系统错误",
            f"处理请求时出错\n请检查:\n• 配置格式是否正确\n• 错误信息: {str(e)}", "error"))
        exit(0)

def get_dd_headers(content_type="application/json"):
    return {
        "Authorization": f"Bearer {panel_token}",
        "accept": "application/json",
        "Content-Type": content_type
    }

def dd_allenvs(osname, account):
    url = f"{panel_url}/api/envs"
    headers = get_dd_headers()
    params = {"keyword": str(account), "page_size": 100}
    response = requests.get(url=url, headers=headers, params=params).json()

    data_list = response.get('data', [])
    if isinstance(data_list, list):
        for envs in data_list:
            envname = envs.get('name', '')
            remarks = envs.get('remarks', '')
            if remarks is None:
                continue
            if osname == envname and str(account) in remarks:
                return envs['id']
        return None
    else:
        sender.reply(format_message("连接失败", "连接呆呆面板获取变量失败", "error"))
        exit(0)

def dd_delenvs(id):
    if id is None:
        return
    url = f"{panel_url}/api/envs/{id}"
    headers = get_dd_headers()
    requests.delete(url, headers=headers)

def DDcreate(osname, value, account, phone, target_userid=None, expire_time=None):
    try:
        actual_userid = target_userid if target_userid else userid
        expire_info = f'丨到期:{expire_time}' if expire_time else ''
        url = f"{panel_url}/api/envs"

        data = {
            "value": value,
            "name": osname,
            "remarks": f'顺丰:{account}丨用户:{actual_userid}丨手机:{phone}{expire_info}丨顺丰管理'
        }
        if panel_group:
            data["group"] = panel_group

        headers = get_dd_headers()
        response = requests.post(url, headers=headers, json=data)

        if response.status_code not in (200, 201):
            sender.reply(format_message("添加变量失败", f"请求失败\n状态码: {response.status_code}", "error"))
            exit(0)

        result = response.json()
        resp_data = result.get('data')
        if resp_data:
            return resp_data.get('id')

    except SystemExit:
        raise
    except Exception as e:
        sender.reply(format_message("系统错误", f"添加变量失败\n错误信息: {str(e)}", "error"))
        exit(0)

def DDupdate(osname, value, account, env_id, phone, target_userid=None, expire_time=None):
    actual_userid = target_userid if target_userid else userid
    expire_info = f'丨到期:{expire_time}' if expire_time else ''
    url = f"{panel_url}/api/envs/{env_id}"

    data = {
        "value": value,
        "name": osname,
        "remarks": f'顺丰:{account}丨用户:{actual_userid}丨手机:{phone}{expire_info}丨顺丰管理'
    }
    if panel_group:
        data["group"] = panel_group

    headers = get_dd_headers()
    response = requests.put(url, headers=headers, json=data)

    if response.status_code == 200:
        return env_id, None
    else:
        sender.reply(format_message("更新失败", "更新变量失败,请稍后重试", "error"))
        exit(0)

def session_ids(url_or_ck):
    if not url_or_ck:
        sender.reply(format_message("输入无效", "输入内容无效，请重新输入！", "error"))
        exit(0)

    if url_or_ck.startswith(('http://', 'https://')):
        try:
            response = requests.get(url_or_ck, allow_redirects=False)
            cookie_str = str(response.headers)
        except requests.exceptions.RequestException as e:
            sender.reply(format_message("网络错误", f"网络请求失败: {str(e)}", "error"))
            exit(0)
    else:
        cookie_str = url_or_ck

    try:
        session_id_pattern = r'sessionId=([^;]+)'
        login_mobile_pattern = r'_login_mobile_=([^;]+)'

        session_id_match = re.search(session_id_pattern, cookie_str)
        login_mobile_match = re.search(login_mobile_pattern, cookie_str)

        if not session_id_match or not login_mobile_match:
            sender.reply(format_message("获取失败", "无法从输入中获取用户信息，请检查CK是否正确！", "error"))
            exit(0)

        session_id = session_id_match.group(1)
        login_mobile = login_mobile_match.group(1)

        if url_or_ck.startswith(('http://', 'https://')) and '用户手机号校验未通过' in response.text:
            sender.reply(format_message("校验失败", "用户手机号校验未通过，请检查账号状态！", "error"))
            exit(0)

        return session_id, login_mobile

    except requests.exceptions.RequestException as e:
        sender.reply(format_message("网络错误", f"网络请求失败: {str(e)}", "error"))
        exit(0)
    except Exception as e:
        sender.reply(format_message("处理错误", f"处理用户信息时出错: {str(e)}", "error"))
        exit(0)

def query_user_info(session_id):
    url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberIntegral~userInfoService~queryUserInfo"

    headers = {
        "Cookie": f"sessionId={session_id}",
        "Content-Type": "application/json",
        "syscode": "MCS-MIMP-CORE"
    }

    data = {
        "sysCode": "ESG-CEMP-CORE",
        "optionalColumns": ["usablePoint", "cycleSub", "leavePoint"],
        "token": "zeTLTYeG0bLetfRk"
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        if result.get('success'):
            obj = result.get('obj', {})
            usable_point = obj.get('usablePoint', 0)
            cycle_add = obj.get('cycleAdd', 0)
            point_clear_cycle = obj.get('pointClearCycle', '')
            expiring_points = usable_point - cycle_add if cycle_add else usable_point
            if point_clear_cycle:
                try:
                    original_date = datetime.strptime(point_clear_cycle, "%Y-%m-%d")
                    next_year_date = original_date.replace(year=original_date.year + 1)
                    point_clear_cycle = next_year_date.strftime("%Y-%m-%d")
                except ValueError:
                    pass

            return {
                'usable_point': usable_point,
                'cycle_add': cycle_add,
                'expiring_points': max(0, expiring_points),
                'point_clear_cycle': point_clear_cycle
            }
    except Exception as e:
        print(f"查询用户信息失败: {str(e)}")
        return None

    return None

def todaycoin(session_id):
    pageNo = 1
    coin = 0
    user_info = query_user_info(session_id)

    while True:
        url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberIntegral~memberPoint~queryMemberPointDetail"

        headers = {
            "Cookie": f"sessionId={session_id}"
        }

        data = {
            "type": "ALL",
            "pageNo": pageNo,
            "pageSize": 10
        }

        response = requests.post(url, headers=headers, json=data).json()
        success = response['success']
        data = response['obj']['data']
        if len(data) < 1:
            return 0, '0', user_info
        if success:
            allcoin = response['obj']['usablePoint']
            for coinjson in data:
                createTm = coinjson['createTm']
                datetime_obj = datetime.strptime(createTm, "%Y-%m-%d %H:%M:%S")
                date_str = datetime_obj.strftime("%Y-%m-%d")
                if date_str < str(today_time):
                    break
                else:
                    opCode = coinjson['opCode']
                    pointVal = coinjson['pointVal']
                    if opCode == 'ADD':
                        coin = coin + int(pointVal)
                    else:
                        continue
            createTm = data[-1]['createTm']
            datetime_obj = datetime.strptime(createTm, "%Y-%m-%d %H:%M:%S")
            date_str = datetime_obj.strftime("%Y-%m-%d")
            if date_str >= str(today_time):
                pageNo = pageNo + 1
            else:
                break
    return coin, allcoin, user_info

def sytTokens(payload, deviceId):
    t = int(time.time() * 1000)
    datamd5 = generate_md5(payload + '&080R3MAC57J2{A19!$3:WO{I<1N$31BI')
    deviceidmd5 = generate_md5(
        deviceId + f'{t}' + '9.77.02NBF+BE4{@P:@X${Q9BAE>{PAK!D:N*^CNsc' + datamd5 + '705088894ad6ef475bdf4875c9d533b8&2NBF+BE4{@P:@X${Q9BAE>{PAK!D:N*^')

    sytToken = generate_md5(deviceidmd5 + '&0HQ%H91K&AA{DH$*XV>XR)VKL:QFE{&%')
    return sytToken, t

def generate_md5(input_string):
    md5_hash = hashlib.md5()
    md5_hash.update(input_string.encode('utf-8'))
    md5_digest = md5_hash.hexdigest()

    return md5_digest

def build_token_url(sign):
    encoded_string = urllib.parse.quote(sign)
    return f'https://mcs-mimp-web.sf-express.com/mcs-mimp/share/app/shareRedirect?sign={encoded_string}&source=SFAPP&bizCode=647@RnlvejM1R3VTSVZ6d3BNaXJxRFpOUVVtQkp0ZnFpNDBKdytobm5TQWxMeHpVUXVrVzVGMHVmTU5BVFA1bXlwcw=='

def get_ck_from_url(token_url):
    try:
        session = requests.Session()
        session.get(token_url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090551) XWEB/6945 Flue',
        }, timeout=15)
        cookies = session.cookies.get_dict()
        session_id = cookies.get('sessionId', '')
        login_mobile = cookies.get('_login_mobile_', '')
        login_user_id = cookies.get('_login_user_id_', '')
        if session_id and login_mobile:
            return f'sessionId={session_id};_login_mobile_={login_mobile};_login_user_id_={login_user_id}'
        return None
    except Exception as e:
        print(f"获取CK失败: {str(e)}")
        return None

def validate_ck(ck):
    if not ck:
        return False
    try:
        session_id_match = re.search(r'sessionId=([^;]+)', ck)
        if not session_id_match:
            return False
        session_id = session_id_match.group(1)
        url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberIntegral~memberPoint~queryMemberPointDetail"
        headers = {
            "Cookie": f"sessionId={session_id}",
            "Content-Type": "application/json"
        }
        data = {"type": "ALL", "pageNo": 1, "pageSize": 1}
        response = requests.post(url, headers=headers, json=data, timeout=10)
        result = response.json()
        return result.get('success', False)
    except:
        return False

def get_ck_with_fallback(account):
    td = parse_token_data(account)
    if not td:
        return None

    saved_ck = td.get('ck', '')
    if saved_ck and validate_ck(saved_ck):
        return saved_ck

    sign = td.get('sign', '')
    userId = td.get('userId', '')
    memNo = td.get('memNo', '')
    mobile = td.get('mobile', '')
    deviceId = td.get('deviceId', '')

    if sign:
        token_url = build_token_url(sign)
        new_ck = get_ck_from_url(token_url)
        if new_ck and validate_ck(new_ck):
            save_token_data(account, userId, memNo, mobile, sign, deviceId, new_ck)
            return new_ck

        if userId and memNo and mobile:
            new_sign = refresh_sign(userId, memNo, mobile, deviceId)
            if new_sign:
                new_url = build_token_url(new_sign)
                new_ck = get_ck_from_url(new_url)
                if new_ck and validate_ck(new_ck):
                    save_token_data(account, userId, memNo, mobile, new_sign, deviceId, new_ck)
                    return new_ck
                save_token_data(account, userId, memNo, mobile, new_sign, deviceId, '')
                return new_ck

    if userId and memNo and mobile:
        new_sign = refresh_sign(userId, memNo, mobile, deviceId)
        if new_sign:
            new_url = build_token_url(new_sign)
            new_ck = get_ck_from_url(new_url)
            save_token_data(account, userId, memNo, mobile, new_sign, deviceId, new_ck or '')
            if new_ck and validate_ck(new_ck):
                return new_ck

    raw = sg.bucketGet(bucket='dd_sf_token', key=account)
    if raw and raw.startswith('http'):
        new_ck = get_ck_from_url(raw)
        return new_ck

    return None

def parse_token_data(account):
    raw = sg.bucketGet(bucket='dd_sf_token', key=account)
    if not raw:
        return None
    raw_text = str(raw).strip()
    try:
        data = json.loads(raw_text)
        if isinstance(data, dict):
            data.setdefault('sign', '')
            data.setdefault('mobile', account)
            data.setdefault('userId', '')
            data.setdefault('memNo', '')
            data.setdefault('deviceId', '')
            data.setdefault('srcDeviceGuid', '')
            data.setdefault('clientVersion', '')
            data.setdefault('ck', '')
            data.setdefault('appToken', '')
            return data
    except (json.JSONDecodeError, TypeError):
        pass

    result = {'sign': '', 'mobile': account, 'userId': '', 'memNo': '', 'deviceId': '', 'srcDeviceGuid': '', 'clientVersion': '', 'ck': '', 'appToken': ''}
    if 'sessionId=' in raw_text:
        result['ck'] = raw_text
        login_mobile_match = re.search(r'_login_mobile_=([^;]+)', raw_text)
        if login_mobile_match:
            result['mobile'] = login_mobile_match.group(1)
        return result

    try:
        parsed = urllib.parse.urlparse(raw_text)
        params = urllib.parse.parse_qs(parsed.query)
        if 'sign' in params:
            result['sign'] = urllib.parse.unquote(params['sign'][0])
    except Exception:
        pass
    return result

def save_token_data(account, userId, memNo, mobile, sign, deviceId='', ck='', appToken='', srcDeviceGuid='', clientVersion=''):
    old_data = parse_token_data(account) or {}
    appToken = appToken or old_data.get('appToken', '')
    srcDeviceGuid = srcDeviceGuid or old_data.get('srcDeviceGuid', '')
    clientVersion = clientVersion or old_data.get('clientVersion', '')
    data = json.dumps(
        {
            'userId': userId,
            'memNo': memNo,
            'mobile': mobile,
            'sign': sign,
            'deviceId': deviceId,
            'srcDeviceGuid': srcDeviceGuid,
            'clientVersion': clientVersion,
            'ck': ck,
            'appToken': appToken,
        },
        ensure_ascii=False,
    )
    sg.bucketSet(bucket='dd_sf_token', key=account, value=data)

def get_token_as_ck(account):
    return get_ck_with_fallback(account)

def refresh_sign(userId, memNo, mobile, deviceId=''):
    try:
        if not deviceId:
            deviceId = str(uuid.uuid4())
        url = "https://ccsp-egmas.sf-express.com/cx-app-member/member/app/user/universalSign"
        payload = json.dumps({
            "mobile": mobile,
            "userId": userId,
            "memNo": memNo,
            "name": "mcs-mimp-web.sf-express.com",
            "extra": "",
            "needReqTime": "1"
        })
        sytToken, t = sytTokens(payload, deviceId)
        headers = {
            'User-Agent': "okhttp/4.9.1",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'Content-Type': "application/json",
            'jsbundle': "705088894ad6ef475bdf4875c9d533b8",
            'clientVersion': "9.77.0",
            'languageCode': "sc",
            'systemVersion': "13",
            'deviceId': deviceId,
            'regionCode': "CN",
            'carrier': "unknown",
            'screenSize': "1080x2400",
            'sytToken': sytToken,
            'timeInterval': f"{t}",
            'model': "MEIZU 20",
            'mediaCode': "AndroidML"
        }
        response = requests.post(url, data=payload, headers=headers)
        new_sign = response.json()['obj']['sign']
        return new_sign
    except Exception as e:
        print(f"刷新sign失败: {str(e)}")
        return None

def get_token_url_auto_refresh(account):
    token_data = parse_token_data(account)
    if not token_data:
        return None, False
    sign = token_data.get('sign', '')
    userId = token_data.get('userId', '')
    memNo = token_data.get('memNo', '')
    mobile = token_data.get('mobile', '')
    deviceId = token_data.get('deviceId', '')
    if not sign:
        if userId and memNo and mobile:
            new_sign = refresh_sign(userId, memNo, mobile, deviceId)
            if new_sign:
                new_url = build_token_url(new_sign)
                new_ck = get_ck_from_url(new_url)
                save_token_data(account, userId, memNo, mobile, new_sign, deviceId, new_ck or '')
                return new_url, True
        raw = sg.bucketGet(bucket='dd_sf_token', key=account)
        if raw and raw.startswith('http'):
            return raw, False
        return None, False
    token_url = build_token_url(sign)
    try:
        response = requests.get(token_url, allow_redirects=False, timeout=10)
        session_id_match = re.search(r'sessionId=([^;]+);', str(response.headers))
        if session_id_match:
            return token_url, False
    except:
        pass
    if not userId or not memNo or not mobile:
        return token_url, False
    new_sign = refresh_sign(userId, memNo, mobile, deviceId)
    if new_sign:
        new_url = build_token_url(new_sign)
        new_ck = get_ck_from_url(new_url)
        save_token_data(account, userId, memNo, mobile, new_sign, deviceId, new_ck or '')
        return new_url, True
    return token_url, False

def refresh_all_signs():
    if not sender.isAdmin():
        sender.reply("❌ 您没有权限执行此操作!")
        exit(0)
    users = sg.bucketAllKeys(bucket='dd_sf_user')
    if not users:
        sender.reply(format_message("刷新结果", "未找到任何绑定账号", "error"))
        return
    sender.reply(format_message("开始刷新", f"共找到: {len(users)}个用户\n⏳ 刷新中请稍候...", "loading"))
    success_count = 0
    fail_count = 0
    skip_count = 0
    for user in users:
        try:
            accountlist = sg.bucketGet(bucket='dd_sf_user', key=user)
            if not accountlist:
                continue
            accounts = parse_accounts(accountlist)
            for account in accounts:
                try:
                    token_data = parse_token_data(account)
                    if not token_data:
                        fail_count += 1
                        continue
                    userId = token_data.get('userId', '')
                    memNo = token_data.get('memNo', '')
                    mobile = token_data.get('mobile', '')
                    deviceId = token_data.get('deviceId', '')
                    if not userId or not memNo or not mobile:
                        skip_count += 1
                        continue
                    new_sign = refresh_sign(userId, memNo, mobile, deviceId)
                    if new_sign:
                        new_url = build_token_url(new_sign)
                        new_ck = get_ck_from_url(new_url)
                        save_token_data(account, userId, memNo, mobile, new_sign, deviceId, new_ck or '')
                        accountVip = '2099-12-31'
                        if accountVip and accountVip > today_time:
                            try:
                                ck = new_ck or get_ck_from_url(new_url)
                                if ck:
                                    phone = mask_phone(account)
                                    Addenvs(osname=dd_sf_osname, value=ck, account=account, phone=phone, target_userid=user, expire_time=accountVip)
                            except:
                                pass
                        success_count += 1
                    else:
                        fail_count += 1
                except Exception as e:
                    print(f"刷新账号 {account} 失败: {str(e)}")
                    fail_count += 1
        except Exception as e:
            print(f"处理用户 {user} 时出错: {str(e)}")
            continue
    result_msg = f"""=====登录态刷新完成=====
✅ 刷新成功: {success_count}个账号
⏭️ 跳过(无法刷新): {skip_count}个账号
❌ 刷新失败: {fail_count}个账号
=================="""
    sender.reply(result_msg)

def sf_captcha_login(sender):
    guide = """
=====短信验证码登录=====
请输入顺丰绑定手机号
------------------
回复"q"可随时退出
=================="""
    sender.reply(guide)

    mobile = get_user_choice('请输入手机号')
    mobile = str(mobile or '').strip()
    if not MOBILE_PATTERN.match(mobile):
        sender.reply(format_message('登录失败', '手机号格式错误，请输入 11 位大陆手机号', 'error'))
        exit(0)

    try:
        send_sf_sms_captcha(mobile)
    except ValueError as exc:
        sender.reply(format_message('发送失败', str(exc), 'error'))
        exit(0)

    sender.reply(format_message('发送成功', '\n请输入收到的短信验证码', 'success'))

    retry_count = 3
    while retry_count > 0:
        captcha = get_user_choice('请输入验证码')
        captcha = str(captcha or '').strip()
        if not CAPTCHA_PATTERN.match(captcha):
            retry_count -= 1
            if retry_count == 0:
                sender.reply(format_message('登录失败', '验证码格式错误次数过多，请重新执行顺丰登录', 'error'))
                exit(0)
            sender.reply(format_message('输入有误', f'验证码格式错误，请重新输入\n剩余次数: {retry_count}', 'warning'))
            continue

        try:
            return login_with_sms_api(mobile, captcha)
        except ValueError as exc:
            retry_count -= 1
            if retry_count == 0:
                sender.reply(format_message('登录失败', f'{exc}\n请重新执行顺丰登录', 'error'))
                exit(0)
            sender.reply(format_message('校验失败', f'{exc}\n剩余次数: {retry_count}', 'warning'))

    sender.reply(format_message('登录失败', '验证码重试次数已耗尽，请重新执行顺丰登录', 'error'))
    exit(0)

def sf_login(sender):
    try:
        scan_msg = """
=====微信扫码登录=====
⌛ 正在加载二维码...
⏳ 请稍候...
=================="""
        sender.reply(scan_msg)

        url_getQr = 'https://wxsm.linzixuan.top/api/getQr'
        url_checkQr = 'https://wxsm.linzixuan.top/api/checkQr'
        response = requests.post(url_getQr, json={'project': 'sf'})
        response_data = response.json()
        if not response_data.get('data') or 'uuid' not in response_data['data']:
            sender.reply('❌ 获取二维码失败!')
            exit(0)

        QRcode = response_data['data']['uuid']
        QRcodeImg = response_data['data']['img_url']

        sender.replyImage(QRcodeImg)

        scan_guide = """
=====登录说明=====
📱 请使用微信扫描二维码登录
------------------
⚠️ 注意事项:
1. 请确保已用微信登录过顺丰APP和微信小程序
2. 如果登录失败,请先下载顺丰APP和登录小程序
3. 扫码后请等待5分钟内完成授权
=================="""
        sender.reply(scan_guide)

        retry = 150
        check_interval = 2
        while True:
            time.sleep(check_interval)
            data = {'project': 'sf', 'uuid': QRcode}
            try:
                response = requests.post(url_checkQr, json=data, timeout=10)
                response_data = response.json()

                if response_data.get('code') == 0 and response_data.get('data', {}).get('code'):
                    code = response_data['data']['code']
                    break
                elif response_data.get('code') == 2:
                    sender.reply('❌ 二维码已过期,请重新尝试!')
                    exit(0)
                else:
                    retry -= 1
                    if retry == 0:
                        sender.reply('❌ 扫码超时,请重新尝试!')
                        exit(0)
            except requests.exceptions.Timeout:
                retry -= 1
                if retry == 0:
                    sender.reply('❌ 网络请求超时,请检查网络后重试!')
                    exit(0)
            except Exception as e:
                retry -= 1
                if retry == 0:
                    sender.reply(f'❌ 检查扫码状态失败: {str(e)}')
                    exit(0)

        deviceId = str(uuid.uuid4())
        url = "https://ccsp-egmas.sf-express.com/cx-app-member/member/app/weixin/getAccessTokenByCode"
        payload = json.dumps({"code": code})
        sytToken, t = sytTokens(payload, deviceId)
        headers = {
            'User-Agent': "okhttp/4.9.1",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'Content-Type': "application/json",
            'jsbundle': "705088894ad6ef475bdf4875c9d533b8",
            'clientVersion': "9.77.0",
            'languageCode': "sc",
            'systemVersion': "13",
            'deviceId': deviceId,
            'regionCode': "CN",
            'carrier': "unknown",
            'screenSize': "1080x2400",
            'sytToken': sytToken,
            'timeInterval': f"{t}",
            'model': "MEIZU 20",
            'mediaCode': "AndroidML"
        }
        response = requests.post(url, data=payload, headers=headers)
        wx_login_obj = response.json().get('obj', {})
        url = "https://ccsp-egmas.sf-express.com/cx-app-member/member/app/user/universalSign"
        account = wx_login_obj['memInfos'][0]['userId']
        memNo = wx_login_obj['memInfos'][0]['memNo']
        mobile = wx_login_obj['memInfos'][0]['mobile']
        wx_app_token = wx_login_obj.get('token', '')

        payload = json.dumps({
            "mobile": mobile,
            "userId": account,
            "memNo": memNo,
            "name": "mcs-mimp-web.sf-express.com",
            "extra": "",
            "needReqTime": "1"
        })
        sytToken, t = sytTokens(payload, deviceId)
        headers['sytToken'] = sytToken
        headers['timeInterval'] = str(t)
        response = requests.post(url, data=payload, headers=headers)
        sign = response.json()['obj']['sign']
        Token = build_token_url(sign)

        try:
            web_headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 13; MEIZU 20 Build/TKQ1.220829.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/122.0.6261.120 Mobile Safari/537.36 XWEB/1220133 MMWEBSDK/20231202 MMWEBID/2247 MicroMessenger/8.0.47.2560(0x28002F30) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive'
            }
            requests.get(Token, headers=web_headers, allow_redirects=True, timeout=10)
        except Exception as e:
            print(f"访问Web端URL时出现异常(可忽略): {str(e)}")

        login_ck = get_ck_from_url(Token)
        token_data = json.dumps(
            {
                'userId': account,
                'memNo': memNo,
                'mobile': mobile,
                'sign': sign,
                'deviceId': deviceId,
                'srcDeviceGuid': '',
                'clientVersion': '9.77.0',
                'ck': login_ck or '',
                'appToken': wx_app_token,
            },
            ensure_ascii=False,
        )
        account = mobile
        mobile = mobile[:3] + '*' * 4 + mobile[7:]

        return token_data, str(account), mobile
    except Exception:
        sender.reply('❌ 获取Token失败，请仔细查看注意事项！')
        exit(0)

def bindaccount():
    sender.reply("=====顺丰速运登录=====\n[1] 验证码登录\n[2] 微信扫码登录\n==================")
    choice = get_user_choice('请选择登录方式')
    if choice == '1': token, account, mobile = sf_captcha_login(sender)
    elif choice == '2': token, account, mobile = sf_login(sender)
    else: sender.reply('❌ 输入错误'); return
    if not token or not account: return
    accounts = list(dict.fromkeys(parse_accounts(uservalue) + [account]))
    sg.bucketSet('dd_sf_user', userid, str(accounts)); sg.bucketSet('dd_sf_token', account, token)
    try:
        value = get_token_as_ck(account) or token
        Addenvs(dd_sf_osname, value, account, mask_phone(mobile or account), target_userid=userid, expire_time='')
        sync = '已同步面板'
    except Exception as exc: sync = f'面板同步失败：{exc}'
    sender.reply(f'=====顺丰账号绑定=====\n📱 {mask_phone(mobile or account)}\n✅ 绑定成功，{sync}\n==================')

def meituanmanage():
    accounts = parse_accounts(uservalue)
    if not accounts:
        sender.reply(f'❌ 未绑定账号，请先发送 {dd_signcommand}'); return
    sender.reply('=====顺丰账号管理=====\n' + '\n'.join(f'[{i}] {mask_phone(x)}' for i, x in enumerate(accounts, 1)) + '\n==================')
    choice = get_user_choice('', 120000, True)
    if not choice or choice.lower() == 'q': return
    if not choice.isdigit() or not 1 <= int(choice) <= len(accounts): sender.reply('❌ 序号无效'); return
    account = accounts[int(choice)-1]
    sender.reply('[1] 查询账号\n[2] 删除账号')
    action = get_user_choice('', 120000, True)
    if action == '1': query_accounts([account])
    elif action == '2':
        sender.reply('确认删除请回复 y')
        if get_user_choice('', 120000, True).lower() != 'y': return
        accounts.remove(account); sg.bucketDel('dd_sf_token', account)
        if accounts: sg.bucketSet('dd_sf_user', userid, str(accounts))
        else: sg.bucketDel('dd_sf_user', userid)
        try:
            env_id = allenvs(dd_sf_osname, account)
            if env_id: delenvs(env_id)
        except Exception: pass
        sender.reply('✅ 删除成功')

def cx_by_session(session_id):
    coin, allcoin, user_info = todaycoin(session_id)
    large_coupons = query_large_coupons(session_id, show_other_coupons)
    return coin, allcoin, large_coupons, user_info

def get_session_from_ck(ck):
    if not ck:
        return None
    match = re.search(r'sessionId=([^;]+)', ck)
    if match:
        return match.group(1)
    return None

def _sf_express_headers_to_lower(headers):
    key_map = {
        "srcDeviceGuid": "srcdeviceguid",
        "clientVersion": "clientversion",
        "languageCode": "languagecode",
        "systemVersion": "systemversion",
        "deviceId": "deviceid",
        "regionCode": "regioncode",
        "screenSize": "screensize",
        "sytToken": "syttoken",
        "timeInterval": "timeinterval",
        "mediaCode": "mediacode",
        "memberId": "memberid",
    }
    return {key_map.get(k, k): v for k, v in headers.items()}

def _sf_express_post(url, body_obj, app_token, member_id, extra_headers=None, device_id="", ck="", lowercase_headers=False):
    if not device_id:
        return {"success": False, "errorMessage": "快递查询缺少登录设备信息，请重新登录后再试"}

    cfg = {
        "clientVersion": "9.77.0",
        "languageCode": "sc",
        "systemVersion": "13",
        "deviceId": device_id,
        "regionCode": "CN",
        "carrier": "unknown",
        "screenSize": "1080x2400",
        "model": "MEIZU 20",
        "mediaCode": "AndroidML",
        "jsbundle": "705088894ad6ef475bdf4875c9d533b8",
        "srcDeviceGuid": "".join(random.choices(string.ascii_letters + string.digits + "_", k=38)),
    }
    body_str = json.dumps(body_obj, separators=(",", ":"), ensure_ascii=False)
    ts = str(int(time.time() * 1000))
    body_md5 = generate_md5(body_str + "&080R3MAC57J2{A19!$3:WO{I<1N$31BI")
    mix = cfg["deviceId"] + ts + cfg["clientVersion"] + "2NBF+BE4{@P:@X${Q9BAE>{PAK!D:N*^" + "CN" + cfg["languageCode"] + body_md5 + cfg["jsbundle"]
    computed_syt = generate_md5(generate_md5(mix + "&2NBF+BE4{@P:@X${Q9BAE>{PAK!D:N*^") + "&0HQ%H91K&AA{DH$*XV>XR)VKL:QFE{&%")
    headers = {
        "User-Agent": "okhttp/4.9.1",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/json",
        "jsbundle": cfg["jsbundle"],
        "srcDeviceGuid": cfg["srcDeviceGuid"],
        "clientVersion": cfg["clientVersion"],
        "languageCode": cfg["languageCode"],
        "systemVersion": cfg["systemVersion"],
        "deviceId": cfg["deviceId"],
        "regionCode": cfg["regionCode"],
        "carrier": cfg["carrier"],
        "screenSize": cfg["screenSize"],
        "sytToken": computed_syt,
        "timeInterval": ts,
        "model": cfg["model"],
        "mediaCode": cfg["mediaCode"],
        "token": app_token,
        "memberId": member_id,
    }
    if ck:
        headers["Cookie"] = ck
    if extra_headers:
        headers.update(extra_headers)
    if lowercase_headers:
        headers = _sf_express_headers_to_lower(headers)
    return requests.post(url, headers=headers, data=body_str.encode("utf-8"), timeout=15).json()

def sf_query_express_list(app_token, member_id, mobile, data_type=0, page_no=1, device_id="", ck=""):
    body = {
        "pageRows": 10,
        "orderType": "1",
        "payTypeList": [],
        "accountMobile": mobile,
        "pageNo": page_no,
        "dataType": data_type,
        "orderStatusList": [],
        "mobile": mobile,
        "memberId": member_id,
        "timeRange": "",
        "queryLastRouter": True,
        "supportWaybillStatusNew": True,
        "userInfos": [],
        "selectedFamily": False,
    }
    url = "https://ccsp-egmas.sf-express.com/cx-app-query/query/app/waybill/queryMultAccountBillListComplex"
    return _sf_express_post(url, body, app_token, member_id, device_id=device_id, ck=ck)

def sf_query_express_detail(app_token, member_id, waybill_no, device_id="", ck=""):
    body = {"waybillNo": waybill_no, "mediaCode": "AndroidML"}
    url = "https://ucmp.sf-express.com/cx-wechat-query/query/newWaybill/search"
    extra = {"cxgw-appid": "sfapp-valid-a85073uy"}
    return _sf_express_post(url, body, app_token, member_id, extra, device_id=device_id, ck=ck, lowercase_headers=True)

def get_app_query_context(account):
    td = parse_token_data(account)
    if not td:
        return None, None, None, None, None
    app_token = td.get("appToken", "")
    member_id = td.get("userId", "")
    mobile = td.get("mobile", account)
    device_id = td.get("deviceId", "")
    ck = td.get("ck", "")
    return app_token, member_id, mobile, device_id, ck

def format_express_detail(detail_obj):
    if not detail_obj:
        return "❌ 无法获取快递详情"

    def short_text(text, limit=46):
        text = str(text or "").strip()
        if len(text) <= limit:
            return text
        return text[:limit] + "..."

    waybill_no = detail_obj.get("waybillNo", "")
    sender_name = detail_obj.get("consignorContName", "")
    sender_mobile = detail_obj.get("consignorMobile", "")
    sender_addr = detail_obj.get("consignorAddr", "")
    receiver_name = detail_obj.get("addresseeContName", "")
    receiver_mobile = detail_obj.get("addresseeMobile", "")
    receiver_addr = detail_obj.get("addresseeAddr", "")
    product_name = detail_obj.get("productDisplayName", "") or detail_obj.get("limitTypeName", "")
    status_msg = detail_obj.get("waybillStatusMessage", "")
    consigned_tm = detail_obj.get("consignedTm", "")
    signed_tm = detail_obj.get("signinTm", "")
    weight = detail_obj.get("meterageWeightQty", "")
    fee = detail_obj.get("transportFeeAmt", "")
    goods_name = detail_obj.get("consNames", "")

    lines = [
        "=====快递详情=====",
        f"📦 单号: {waybill_no}",
        f"📊 状态: {status_msg}｜{product_name}",
        f"📤 寄件: {sender_name} {sender_mobile}",
        f"📍 {short_text(sender_addr)}",
        f"📥 收件: {receiver_name} {receiver_mobile}",
        f"📍 {short_text(receiver_addr)}",
    ]

    extra_parts = []
    if goods_name:
        extra_parts.append(f"物品: {goods_name}")
    if weight:
        extra_parts.append(f"重量: {weight}kg")
    if fee:
        extra_parts.append(f"运费: ¥{fee}")
    if extra_parts:
        lines.append("｜".join(extra_parts))

    if consigned_tm:
        lines.append(f"🕐 揽收: {consigned_tm}")
    if signed_tm and status_msg == "已签收":
        lines.append(f"🕐 签收: {signed_tm}")

    bar_list = detail_obj.get("barNewList", [])
    if bar_list:
        display_bars = bar_list
        if len(bar_list) > 5:
            display_bars = [bar_list[0]] + bar_list[-4:]

        lines.append("------------------")
        lines.append(f"🚚 关键轨迹({len(display_bars)}/{len(bar_list)}):")
        for bar in display_bars:
            scan_date = bar.get("barScanDt", "")
            scan_time = bar.get("barScanTm", "")
            remark = bar.get("remark", "")
            pkg_msg = bar.get("cxPackageMessage", "")
            if remark:
                time_str = f"{scan_date} {scan_time}"
                lines.append(f"  [{pkg_msg}] {time_str}")
                lines.append(f"  {short_text(remark, 72)}")
        if len(bar_list) > len(display_bars):
            lines.append(f"  已省略 {len(bar_list) - len(display_bars)} 条中间轨迹")

    lines.append("==================")
    return "\n".join(lines)

def sf_express_interactive_query():
    if not uservalue:
        sender.reply(format_message("未绑定账号", f"未找到任何账号信息\n💡 发送 {dd_signcommand} 绑定", "error"))
        return

    accounts = parse_accounts(uservalue)
    if not accounts:
        sender.reply(format_message("账号错误", "账号数据格式异常", "error"))
        return

    selected_account = None
    if len(accounts) == 1:
        selected_account = accounts[0]
    else:
        msg_lines = ["=====选择查询账号====="]
        for i, acc in enumerate(accounts):
            msg_lines.append(f"[{i + 1}] {mask_phone(acc)}")
        msg_lines.append("------------------")
        msg_lines.append('回复序号选择，回复"q"退出')
        msg_lines.append("=" * 22)
        sender.reply("\n".join(msg_lines))
        choice = get_user_choice("选择账号")
        if choice is None or choice == "q":
            exit(0)
        idx = validate_input(choice, len(accounts), "序号")
        selected_account = accounts[idx - 1]

    app_token, member_id, mobile, device_id, ck = get_app_query_context(selected_account)
    if not app_token or not member_id or not device_id:
        sender.reply(format_message("需要重新登录", f"快递查询需要重新登录以获取授权\n💡 请发送 {dd_signcommand} 重新登录", "warning"))
        return

    sender.reply("""=====顺丰快递查询=====
[1] 📤 寄件快递
[2] 📥 收件快递
------------------
回复序号选择，回复"q"退出
======================""")
    type_choice = get_user_choice("选择类型")
    if type_choice is None or type_choice == "q":
        exit(0)
    if type_choice not in ("1", "2"):
        sender.reply("❌ 输入错误，请回复1或2")
        return

    data_type = 0 if type_choice == "1" else 1
    type_name = "寄件" if data_type == 0 else "收件"

    sender.reply(f"⏳ 正在查询{type_name}快递...")
    try:
        result = sf_query_express_list(app_token, member_id, mobile, data_type, device_id=device_id, ck=ck)
    except Exception as e:
        sender.reply(format_message("查询失败", f"网络请求异常: {str(e)}", "error"))
        return

    if not result.get("success"):
        sender.reply(format_message("查询失败", result.get("errorMessage", "未知错误"), "error"))
        return

    obj = result.get("obj", {})
    data_list = obj.get("dataList", [])
    send_total = obj.get("mySendTotal", 0)
    recv_total = obj.get("myReceiveTotal", 0)

    if not data_list:
        sender.reply(format_message("查询结果", f"暂无{type_name}快递记录\n📤 寄件: {send_total}件  📥 收件: {recv_total}件", "info"))
        return

    msg_lines = [
        f"====={type_name}快递列表=====",
        f"📤 寄件: {send_total}件  📥 收件: {recv_total}件",
        "-" * 24,
    ]
    for i, item in enumerate(data_list):
        origin = item.get("originateContacts", "")
        dest = item.get("destinationContacts", "")
        origin_city = item.get("originateCityName", "")
        dest_city = item.get("destinationCityName", "")
        waybill = item.get("waybillno", "")
        status = item.get("waybillStatusMessage", "")
        product = item.get("productDisplayName", "")
        recv_time = item.get("receivedTime", "")[:10] if item.get("receivedTime") else ""
        msg_lines.append(f"[{i + 1}] {origin}→{dest}")
        msg_lines.append(f"    {origin_city}→{dest_city} | {product}")
        msg_lines.append(f"    单号: {waybill}")
        msg_lines.append(f"    状态: {status} | {recv_time}")
        if i < len(data_list) - 1:
            msg_lines.append("")

    msg_lines.append("-" * 24)
    msg_lines.append('回复序号查看详情，回复"q"退出')
    msg_lines.append("=" * 24)
    sender.reply("\n".join(msg_lines))

    detail_choice = get_user_choice("选择快递")
    if detail_choice is None or detail_choice == "q":
        exit(0)
    detail_idx = validate_input(detail_choice, len(data_list), "序号")
    selected_item = data_list[detail_idx - 1]
    waybill_no = selected_item.get("waybillno", "")

    sender.reply(f"⏳ 正在查询 {waybill_no} 的详细信息...")
    try:
        detail_result = sf_query_express_detail(app_token, member_id, waybill_no, device_id=device_id, ck=ck)
    except Exception as e:
        sender.reply(format_message("查询失败", f"网络请求异常: {str(e)}", "error"))
        return

    if not detail_result.get("success"):
        sender.reply(format_message("查询失败", detail_result.get("errorMessage", "未知错误"), "error"))
        return

    detail_obj = detail_result.get("obj", {})
    sender.reply(format_express_detail(detail_obj))

def sf_query_express_count(app_token, member_id, mobile, device_id="", ck=""):
    try:
        result = sf_query_express_list(app_token, member_id, mobile, data_type=0, page_no=1, device_id=device_id, ck=ck)
        if result.get("success"):
            obj = result.get("obj", {})
            return obj.get("mySendTotal", 0), obj.get("myReceiveTotal", 0)
    except:
        pass
    return None, None

def query_accounts(accounts=None):
    accounts = accounts or parse_accounts(uservalue)
    if not accounts:
        sender.reply(f'❌ 未绑定账号，请先发送 {dd_signcommand}'); return
    for account in accounts:
        mobile = mask_phone(account)
        try:
            ck = get_ck_with_fallback(account)
            session_id = get_session_from_ck(ck) if ck and validate_ck(ck) else None
            if not session_id:
                url, _ = get_token_url_auto_refresh(account)
                if not url: raise ValueError('登录态失效，请重新登录')
                ck = get_ck_from_url(url) or ck; session_id, _ = session_ids(url)
            today_points, total_points, coupons, info = cx_by_session(session_id)
            extra = {}
            try:
                token, member_id, member_mobile, device_id, app_ck = get_app_query_context(account)
                send_count, receive_count = sf_query_express_count(token, member_id, member_mobile, device_id, app_ck)
                if send_count is not None: extra['express_count'] = f'{send_count}寄件, {receive_count}收件'
            except Exception: pass
            sender.reply(format_account_info(mobile, coin=total_points, today_coin=today_points, account_status='✅ 正常', coupons=coupons, **extra))
            if ck: Addenvs(dd_sf_osname, ck, account, mobile, target_userid=userid, expire_time='')
        except Exception as exc:
            sender.reply(format_account_info(mobile, account_status=f'❌ {exc}', coupons='查询失败'))

def cxs():
    query_accounts()

def sync_to_panel(quiet=False):
    success = failed = 0
    for user in sg.bucketAllKeys('dd_sf_user') or []:
        for account in parse_accounts(sg.bucketGet('dd_sf_user', user)):
            try:
                token = get_token_as_ck(account)
                if not token: raise ValueError('无有效 CK')
                Addenvs(dd_sf_osname, token, account, mask_phone(account), target_userid=user, expire_time='')
                success += 1
            except Exception: failed += 1
    if not quiet: sender.reply(f'=====同步完成=====\n✅ 成功：{success}\n❌ 失败：{failed}\n==================')
    return success, failed

def query_large_coupons(session_id, show_other_coupons=False):
    url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/coupon/available/list"

    headers = {
        "Cookie": f"sessionId={session_id}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
    }

    data = {
        "couponType": "",
        "pageNo": 1,
        "pageSize": 100
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        if not result.get('success'):
            return "优惠券查询失败"

        coupons = result.get('obj', [])
        if not coupons:
            return "暂无优惠券"

        free_coupons = []
        other_coupons = []

        for coupon in coupons:
            try:
                coupon_name = coupon.get('couponName', '未知优惠券')
                expire_time = coupon.get('invalidTm', '')
                coupon_value = coupon.get('discountPrice', 0)
                coupon_num = coupon.get('couponNum', 1)
                coupon_amount = 0
                try:
                    coupon_amount = float(coupon_value)
                except (TypeError, ValueError):
                    pass
                if coupon_amount <= 0:
                    amount_match = re.match(r'^(\d+)元', coupon_name)
                    if amount_match:
                        coupon_amount = int(amount_match.group(1))
                if '寄件' in coupon_name and coupon_amount >= 12:
                    if coupon_num > 1:
                        coupon_info = f"{coupon_name} (共{coupon_num}张), 过期时间: {expire_time}"
                    else:
                        coupon_info = f"{coupon_name}, 过期时间: {expire_time}"
                    free_coupons.append(coupon_info)
                elif show_other_coupons:
                    try:
                        if isinstance(coupon_value, (int, float)) and coupon_value >= 10:
                            if coupon_num > 1:
                                coupon_info = f"{coupon_name} (共{coupon_num}张), 面额: {coupon_value}元, 过期时间: {expire_time}"
                            else:
                                coupon_info = f"{coupon_name}, 面额: {coupon_value}元, 过期时间: {expire_time}"
                            other_coupons.append(coupon_info)
                        else:
                            amount_match = re.search(r'(\d+)元', coupon_name)
                            if amount_match:
                                amount = int(amount_match.group(1))
                                if amount >= 10:
                                    if coupon_num > 1:
                                        coupon_info = f"{coupon_name} (共{coupon_num}张), 过期时间: {expire_time}"
                                    else:
                                        coupon_info = f"{coupon_name}, 过期时间: {expire_time}"
                                    other_coupons.append(coupon_info)
                    except:
                        continue

            except Exception as e:
                print(f"处理优惠券出错: {str(e)}")
                continue

        result_lines = []
        if free_coupons:
            result_lines.extend(free_coupons)

        if show_other_coupons and other_coupons:
            if free_coupons:
                result_lines.append("------------------")
                result_lines.append("🎫 其他大额优惠券:")
            result_lines.extend(other_coupons)

        if not result_lines:
            return "无"

        return '\n'.join(result_lines)

    except Exception as e:
        print(f"优惠券查询异常: {str(e)}")
        return "无"

def show_tutorial():
    sender.reply("""=====顺丰插件教程=====
顺丰登录：验证码或微信扫码绑定账号
顺丰查询：查询积分、优惠券和快递数量
顺丰快递查询：查询物流轨迹
顺丰管理：查询或删除账号
顺丰刷新：刷新登录态
顺丰同步：同步全部账号到面板
==================""")

dd_sf_osname, dd_sf_qlname, dd_managecommand, dd_querycommand, dd_signcommand, _, _, show_point_status, show_other_coupons, _, use_daidai, dd_sf_ddname, panel_group = getusercontent()
if use_daidai: QLurl, qltoken = seekdd()
else: QLurl, qltoken = seekql()
panel_url, panel_token = QLurl, qltoken
imtype = sender.getImtype(); today_time = str(datetime.now().date()); usermessage = sender.getMessage()
if '登录' in usermessage or '登陆' in usermessage: bindaccount()
elif '管理' in usermessage:
    if uservalue: meituanmanage()
    else: sender.reply(f'❌ 未绑定账号，请先发送 {dd_signcommand}')
elif '快递查询' in usermessage: sf_express_interactive_query()
elif '查询' in usermessage: cxs()
elif usermessage in ('顺丰刷新', '顺丰Token刷新'): refresh_all_signs()
elif usermessage == '顺丰同步':
    if sender.isAdmin(): sync_to_panel()
elif usermessage == '顺丰教程': show_tutorial()
elif imtype == 'fake': sync_to_panel(quiet=True)
else: sender.setContinue()
