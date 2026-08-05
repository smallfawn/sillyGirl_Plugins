# [title: 众安健康]
# [name: zhongAnJianKang]
# [language: python]
# [class: 任务]
# [author: 97610325]
# [version: v1.6.0]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^众安管理$|^管理众安$|^众安查询$|^查询众安$|^众安登录$|^登录众安$|^众安$|^众安清理$|^清理众安$]
# [cron: 32 7 * * *]
# [icon: https://nos.netease.com/ysf/82b362badc596b99e5c3ad437973a560.jpg]
# [description: 众安健康插件；指令：众安登录、众安管理、众安查询、众安清理；5.9更新：修复众安查询问题；5.16更新：Token真实有效新检测]
# [depe: ["requests","urllib3"]]


import asyncio as _sg_asyncio
import os as _sg_os
import time as _sg_time
import types as _sg_types
import json as _sg_json
from threading import Thread as _sg_Thread
from sillygirl import Adapter as _SGAdapter, Bucket as _SGBucket, Sender as _SGSender, sender as _sg_sender, form
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

config = form({
    'dd_zajk_config_Qinglong': form.string().title('设置对接容器').default('').description('你的变量需要添加到的容器？参数用丨分割，这个符号是中文的竖线(直接复制)'),
    'dd_zajk_config_osname': form.string().title('青龙变量名').default('').description('青龙面板中众安健康脚本对应的环境变量名称'),
})
_CONFIG_FIELD_MAP = {
    ('dd_zajk_config', 'Qinglong'): 'dd_zajk_config_Qinglong',
    ('dd_zajk_config', 'osname'): 'dd_zajk_config_osname',
}

import time
import random
import requests
import http.client
import json
from datetime import datetime, timedelta
from decimal import Decimal
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

_original_putheader = http.client.HTTPConnection.putheader
def _patched_putheader(self, header, *values):
    encoded_values = []
    for value in values:
        if isinstance(value, str):
            try:
                value.encode('latin-1')
                encoded_values.append(value)
            except UnicodeEncodeError:
                encoded_values.append(value.encode('utf-8'))
        else:
            encoded_values.append(value)
    return _original_putheader(self, header, *encoded_values)
http.client.HTTPConnection.putheader = _patched_putheader


senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()
uservalue = sg.bucketGet(bucket='dd_zajk_user', key=userid)

today_date = datetime.now().date()
today_time = str(today_date)

API_HOST = "ihealth.zhongan.com"
ACTIVITY_CODE = "ONA20220411001"
CHANNEL_CODE = "c20195660470001"

ZA_BASE_HEADERS = {
    "Host": API_HOST,
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.23(0x1800172f) NetType/WIFI Language/zh_CN",
    "Referer": "https://servicewechat.com/wxbac45cc1588a5a75/210/page-frame.html"
}


def clean_cookie(cookie):
    return cookie.strip('\'" ')


def parse_token_cookie(token_cookie_str):
    token_cookie_str = token_cookie_str.strip()
    if '#' not in token_cookie_str:
        return None, None
    parts = token_cookie_str.split('#', 1)
    if len(parts) < 2:
        return None, None
    access_token = parts[0].strip()
    cookie = clean_cookie(parts[1].strip())
    return access_token, cookie


def za_get_headers(access_token, use_cookie=False, cookie=''):
    headers = ZA_BASE_HEADERS.copy()
    headers["Access-Token"] = access_token
    if use_cookie and cookie:
        headers["Cookie"] = cookie
        headers["Origin"] = f"https://{API_HOST}"
        headers["Accept-Language"] = "zh-cn"
        headers["User-Agent"] += " miniProgram/wxbac45cc1588a5a75"
    return headers

def getusercontent():
    dd_zajk_osname = sg.bucketGet('dd_zajk_config', 'osname') or 'zajk'
    dd_zajk_qlname = sg.bucketGet('dd_zajk_config', 'Qinglong')
    dd_managecommand = sg.bucketGet('dd_zajk_config', 'dd_managecommand') or '众安管理'
    dd_querycommand = sg.bucketGet('dd_zajk_config', 'dd_querycommand') or '众安查询'
    dd_signcommand = sg.bucketGet('dd_zajk_config', 'dd_signcommand') or '众安登录'

    randommanagecommand = dd_managecommand
    randomquerycommand = dd_querycommand
    randomsigncommand = dd_signcommand

    zajkVipmoney = Decimal(sg.bucketGet('dd_zajk_config', 'zajkVipmoney') or '0')
    zajkcoin = int(sg.bucketGet('dd_zajk_config', 'zajkcoin') or '0')

    return (dd_zajk_osname, dd_zajk_qlname, dd_managecommand, dd_querycommand,
            dd_signcommand, randommanagecommand, randomquerycommand, randomsigncommand, zajkVipmoney, zajkcoin)

def seekql():
    try:
        if len(dd_zajk_qlname) == 0:
            sender.reply("""=======配置错误=======
❌ 未配置青龙信息
------------------
请在插件配置中填写:
Host丨ClientID丨ClientSecret
• 使用中文丨分隔
• 示例:
http://ql.example.com丨abcd1234丨efgh5678
====================""")
            exit(0)

        qllist = dd_zajk_qlname.split('丨')
        if len(qllist) != 3:
            sender.reply(f"""=======格式错误=======
❌ 青龙配置格式错误
------------------
当前格式: {dd_zajk_qlname}
正确格式:
青龙地址丨ClientID丨ClientSecret
====================""")
            exit(0)

        QLurl = qllist[0].strip()
        ClientID = qllist[1].strip()
        ClientSecret = qllist[2].strip()

        if not all([QLurl, ClientID, ClientSecret]):
            sender.reply("""=======参数错误=======
❌ 青龙配置参数不完整
------------------
请确保以下参数都已填写:
• 青龙面板地址(Host)
• 应用ID(ClientID)
• 应用密钥(ClientSecret)
====================""")
            exit(0)

        if not QLurl.startswith(('http://', 'https://')):
            sender.reply(f"""=======地址错误=======
❌ 青龙地址格式错误
------------------
当前地址: {QLurl}
正确格式:
• http://qinglong.example.com
• https://ql.example.com:5700
====================""")
            exit(0)

        try:
            qltoken = QLtoken(QLurl=QLurl, ClientID=ClientID, ClientSecret=ClientSecret)
            return QLurl, qltoken
        except Exception as e:
            raise Exception(f"获取Token失败: {str(e)}")

    except Exception as e:
        sender.reply(f"""=======网络错误=======
❌ 无法连接青龙面板
------------------
请检查:
1. 青龙面板是否运行
2. 网络是否正常
3. 配置是否正确
4. 错误信息: {str(e)}
------------------
当前配置:
• 地址: {QLurl if 'QLurl' in locals() else '未设置'}
• 应用ID: {ClientID[:4] + '****' if 'ClientID' in locals() else '未设置'}
====================""")
        exit(0)

def QLtoken(QLurl, ClientID, ClientSecret):
    try:
        url = f'{QLurl}/open/auth/token?client_id={ClientID}&client_secret={ClientSecret}'
        response = requests.get(url)

        if response.status_code != 200:
            sender.reply(f"""=======请求失败=======
❌ 青龙API请求失败
------------------
状态码: {response.status_code}
请检查:
• API地址是否正确
• 面板是否正常运行
====================""")
            exit(0)

        result = response.json()
        if "token" in result.get('data', {}):
            return result['data']['token']
        else:
            sender.reply("""=======认证失败=======
❌ 获取Token失败
------------------
请检查:
• ClientID是否正确
• ClientSecret是否正确
• 应用是否有权限
====================""")
            exit(0)

    except requests.exceptions.RequestException as e:
        sender.reply(f"""=======网络错误=======
❌ 连接青龙面板失败
------------------
请检查:
• 青龙地址是否正确
• 网络是否正常
• 错误信息: {str(e)}
====================""")
        exit(0)
    except Exception as e:
        sender.reply(f"""=======系统错误=======
❌ 处理请求时出错
------------------
请检查:
• 配置格式是否正确
• 错误信息: {str(e)}
====================""")
        exit(0)

def QLzt(osname, value, account, username):
    try:
        qlurl = f"{QLurl}/open/envs"
        accountVip = '2099-12-31'
        data = [{
            "value": value,
            "name": osname,
            "remarks": f'众安:{username}丨用户:{userid}丨账号:{account}丨授权时间:{accountVip}丨众安管理'
        }]
        headers = {
            "Authorization": "Bearer" + ' ' + qltoken,
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        r = requests.post(qlurl, headers=headers, data=json.dumps(data))
        r_json = r.json()
        if "value must be unique" in r.text:
            return
        else:
            r_json['data'][0]['id']
            return
    except Exception as e:
        sender.reply(f"""=======添加失败=======
❌ 添加青龙变量失败
------------------
请检查:
• 青龙面板状态
• 变量格式是否正确
• 错误信息: {str(e)}
====================""")
        exit(0)

def QLupdate(osname, value, account, qlid, username):
    try:
        qlurl = f"{QLurl}/open/envs"
        accountVip = '2099-12-31'
        data = {
            "value": value,
            "name": osname,
            "remarks": f'众安:{username}丨用户:{userid}丨账号:{account}丨授权时间:{accountVip}丨众安管理',
            "id": qlid
        }
        headers = {
            "Authorization": "Bearer" + ' ' + qltoken,
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        response = requests.put(qlurl, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            response_json = response.json()
            data = response_json['data']
            if data is None:
                exit(0)
            return data['id'], data['createdAt']
        else:
            sender.reply("""=======更新失败=======
❌ 更新青龙变量失败
------------------
请稍后重试
====================""")
            exit(0)
    except Exception as e:
        sender.reply(f"""=======更新错误=======
❌ 更新变量时出错
------------------
错误信息: {str(e)}
====================""")
        exit(0)

def Addenvs(osname, value, account, username):
    url = f"{QLurl}/open/envs"
    headers = {
        "Authorization": "Bearer" + ' ' + qltoken,
        "accept": "application/json"
    }
    try:
        response = requests.get(url=url, headers=headers).json()
        qlid = None
        username_qlid = None

        if response['code'] == 200:
            envslist = response['data']
            for envs in envslist:
                remarks = envs.get('remarks')
                envname = envs.get('name')
                if not remarks or envname != osname:
                    continue

                if account in remarks:
                    qlid = envs['id']
                    break

                if '众安:' in remarks:
                    try:
                        remark_username = remarks.split('众安:')[1].split('丨')[0]
                        if remark_username == username:
                            username_qlid = envs['id']
                    except:
                        continue

            if not qlid and username_qlid:
                qlid = username_qlid
        else:
            sender.reply("""=======连接失败=======
❌ 连接青龙获取变量失败
====================""")
            exit(0)

        if qlid:
            QLupdate(osname, value, account, qlid, username)
        else:
            QLzt(osname, value, account, username)
    except Exception as e:
        sender.reply(f"""=======操作失败=======
❌ 处理变量时出错
------------------
错误信息: {str(e)}
====================""")
        exit(0)

def allenvs(osname, account):
    url = f"{QLurl}/open/envs"
    headers = {
        "Authorization": f"Bearer {qltoken}",
        "accept": "application/json"
    }

    try:
        response = requests.get(url=url, headers=headers).json()
        qlid = None
        for envs in response['data']:
            if (envs.get('name') == osname and
                envs.get('remarks') and
                str(account) in envs['remarks']):
                qlid = envs['id']
                break
        return qlid
    except:
        return None

def delenvs(id):
    if id is None:
        return

    url = f"{QLurl}/open/envs"
    headers = {
        "Authorization": f"Bearer {qltoken}",
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    data = [id]

    try:
        response = requests.delete(url, headers=headers, json=data)
        if response.status_code != 200:
            return
        result = response.json()
        if result.get('code') != 200:
            return
    except:
        return

def query_zajk_info(token_cookie):
    try:
        access_token, cookie = parse_token_cookie(token_cookie)
        if not access_token or not cookie:
            return {"success": False, "error": "变量格式错误，需Access-Token#Cookie"}

        session = requests.Session()
        session.verify = False
        headers = za_get_headers(access_token, use_cookie=False)

        url = f"https://{API_HOST}/api/lemon/v1/common/activity/homePage"
        body = {
            "activityCode": ACTIVITY_CODE,
            "channelCode": CHANNEL_CODE
        }

        resp = session.post(url, headers=headers, json=body, timeout=15)
        result = resp.json()

        if result.get("code") == "0":
            data = result.get("result", {})
            is_signed = False
            sign_in_info = data.get("signInInfo", {}) or {}
            sign_status = sign_in_info.get("status", "")
            if str(sign_status) == "1" or sign_status == 1:
                is_signed = True
            if not is_signed:
                sign_status2 = sign_in_info.get("signInStatus", "")
                if str(sign_status2) == "1" or sign_status2 == 1:
                    is_signed = True
            if not is_signed:
                direct_status = data.get("signInStatus", "")
                if str(direct_status) == "1" or direct_status == 1:
                    is_signed = True
            if not is_signed:
                sign_url = f"https://{API_HOST}/api/lemon/v1/common/activity/signIn"
                sign_resp = session.post(sign_url, headers=headers, json=body, timeout=15)
                sign_result = sign_resp.json()
                sign_msg = sign_result.get("message", "").lower()
                if "已签到" in sign_msg or "already" in sign_msg or "repeat" in sign_msg:
                    is_signed = True

            valuable_rewards = data.get("valuableRewardList", []) or []
            product_recommend = data.get("productRecommend", {}) or {}
            product_count = len(product_recommend.keys()) if product_recommend else 0
            return {
                "success": True,
                "sum_award": data.get("sumAward", 0),
                "sum_allow_withdraw": data.get("sumAllowWithdraw", 0),
                "is_signed": is_signed,
                "reward_count": len(valuable_rewards),
                "product_count": product_count,
            }
        else:
            return {"success": False, "error": result.get("message", result.get("msg", "API返回错误"))}

    except Exception as e:
        return {"success": False, "error": f"查询异常: {str(e)[:50]}"}

def validate_token(token_str):
    if not token_str or token_str.strip() == '':
        return False, ["Token为空"]

    access_token, cookie = parse_token_cookie(token_str)
    if not access_token or not cookie:
        return False, ["格式错误，需Access-Token#Cookie格式"]

    missing = []
    if not access_token:
        missing.append("Access-Token")
    if not cookie:
        missing.append("Cookie")

    if missing:
        return False, missing

    return True, []

def mask_name(name):
    if not name or name == "未知":
        return name
    if len(name) <= 1:
        return name
    if len(name) == 2:
        return name[0] + "*"
    return name[0] + "*" * (len(name) - 2) + name[-1]


def check_token_alive(token_cookie):
    try:
        info = query_zajk_info(token_cookie)
        return info.get("success", False), info.get("error", "")
    except:
        return False, "请求异常"


def bind():
    def accvip(Newaddition):
        auth_status = '✅ 已授权' if accountVip >= today_time else '⚠️ 未授权'
        next_step = f'发送 {randommanagecommand} 可管理账号' if accountVip >= today_time else f'发送 {randommanagecommand} 可进行授权'

        success_msg = f"""=======绑定成功=======
📱 账号: {display_account}
🔐 状态: {auth_status}
⏰ 操作: {next_step}
===================="""
        if len(accountVip) != 0 and accountVip >= today_time:
            ql_value = token_cookie.replace('#', '&')
            Addenvs(osname=dd_zajk_osname, value=ql_value, account=account, username=display_account)

        if account not in accounts:
            accounts.append(account)
            unique_accounts = list(dict.fromkeys(accounts))
            sg.bucketSet(bucket='dd_zajk_user', key=userid, value=f'{unique_accounts}')

        sender.reply(success_msg)

    sender.reply("""=======众安登录=======
请输入您的众安健康账号，格式为：Access-Token#Cookie
------------------
⚠️ 建议私聊登录,账号安全
⭐ 例如：token值#cookie值

📌 抓包方法：
1. 打开微信小程序「众安健康」
2. 抓包 ihealth.zhongan.com 请求
3. 获取请求头中的 Access-Token
4. 获取请求头中的 Cookie

📌 格式要求：
• Access-Token#Cookie 用 # 连接

⭐ 输入q退出操作
====================""")
    input_account = sender.input(60000, 1, False)
    if not input_account:
        sender.reply('⏰ 操作超时（60秒未响应），请重新发送指令操作')
        exit(0)
    elif input_account.lower() == 'q':
        sender.reply("✅ 已取消登录")
        exit(0)

    token_cookie = input_account.strip()

    is_valid, missing = validate_token(token_cookie)
    if not is_valid:
        missing_str = '、'.join(missing)
        sender.reply(f"""=======验证失败=======
❌ Token格式错误
------------------
缺少参数: {missing_str}

⚠️ 正确格式：
Access-Token#Cookie
====================""")
        exit(0)

    sender.reply("🔄 正在验证账号...")
    info = query_zajk_info(token_cookie)
    if not info["success"]:
        sender.reply(f"""=======验证失败=======
❌ 账号验证失败: {info.get('error', '未知错误')}
请检查Token和Cookie是否正确
====================""")
        exit(0)

    access_token_val, _ = parse_token_cookie(token_cookie)
    display_account = mask_name(access_token_val) if access_token_val else "众安用户"

    account_str = token_cookie
    account = str(int(time.time() * 1000))

    old_auth = None
    accounts = []
    if len(uservalue) != 0:
        accounts = _sg_literal(uservalue)
        cur_token = token_cookie.split('#')[0] if '#' in token_cookie else ''
        for acc in accounts:
            acc_account = sg.bucketGet(bucket='dd_zajk_account', key=acc)
            acc_token = acc_account.split('#')[0] if acc_account and '#' in acc_account else ''
            if acc_token and acc_token == cur_token:
                old_auth = '2099-12-31'
                sender.reply('📝 检测到已绑定账号，将更新信息')
                accounts.remove(acc)
                sg.bucketDel(bucket='dd_zajk_account', key=acc)
                sg.bucketDel(bucket='dd_zajk_username', key=acc)
                True
                qlid = allenvs(osname=dd_zajk_osname, account=str(acc))
                if qlid:
                    delenvs(id=qlid)
                break

    sg.bucketSet(bucket='dd_zajk_username', key=account, value=display_account)
    sg.bucketSet(bucket='dd_zajk_account', key=account, value=account_str)

    if old_auth:
        True
        if old_auth >= today_time:
            ql_value = token_cookie.replace('#', '&')
            Addenvs(osname=dd_zajk_osname, value=ql_value, account=account, username=display_account)

    if len(uservalue) == 0:
        accounts = []

    accountVip = '2099-12-31'
    accvip(True)

def ValueErrors(value, count):
    try:
        value = int(value)
        if value > count or value == 0:
            sender.reply(f"""=======输入无效=======
❌ 请输入 1-{count} 之间的数字
====================""")
            exit(0)
        return value
    except ValueError:
        sender.reply("""=======输入无效=======
❌ 请输入正确的数字
====================""")
        exit(0)

def empower(empowertime, me_as_int):
    day = me_as_int * 30
    try:
        if len(empowertime) == 0:
            delayed_date = today_date + timedelta(days=day)
        else:
            empower_date = datetime.strptime(empowertime, "%Y-%m-%d").date()
            if empower_date <= today_date:
                delayed_date = today_date + timedelta(days=day)
            else:
                delayed_date = empower_date + timedelta(days=day)

        return str(delayed_date)
    except Exception as e:
        print(f"授权时间计算出错: {str(e)}")
        return str(today_date + timedelta(days=day))

def management():
    if len(uservalue) == 0:
        sender.reply(f"""=======未绑定账号=======
❌ 未找到任何账号信息
💡 发送 {randomsigncommand} 绑定
====================""")
        return
    count = 1
    account_list = """
======我的众安健康账号======"""

    accounts = list(dict.fromkeys(_sg_literal(uservalue))) if uservalue else []
    sg.bucketSet(bucket='dd_zajk_user', key=userid, value=f'{accounts}')
    for account in accounts:
        accountVip = '2099-12-31'
        account_str = sg.bucketGet(bucket='dd_zajk_account', key=account)

        token_status = ''
        if account_str:
            token_cookie = account_str
            is_alive, err = check_token_alive(token_cookie)
            if not is_alive:
                token_status = ' 🔴Token失效'

        if len(accountVip) == 0:
            vip_status = '⚠️ 未授权'
        elif accountVip < today_time:
            vip_status = '❌ 已过期'
        else:
            vip_status = f'✅ {accountVip}'

        username = sg.bucketGet(bucket='dd_zajk_username', key=account)
        if username:
            display_username = username
        else:
            display_username = account[:3] + "****" + account[7:]

        account_list += f"""
------------------
[{count}] 账号信息
📱 账号: {display_username}
🔐 授权: {vip_status}{token_status}"""
        count += 1

    account_list += """
==================
回复数字选择账号
回复"q"退出操作
=================="""

    sender.reply(account_list)

    inputmessage = sender.input(60000, 1, False)
    if not inputmessage:
        sender.reply('⏰ 操作超时（60秒未响应），请重新发送指令操作')
        exit(0)
    elif inputmessage.lower() == 'q':
        sender.reply('✅ 已退出管理')
        exit(0)

    try:
        me_as_int = int(inputmessage)
        if me_as_int > count - 1:
            sender.reply('❌ 输入的序号无效')
            exit(0)
    except ValueError:
        sender.reply('❌ 输入必须是数字')
        exit(0)

    account = accounts[me_as_int - 1]
    account_str = sg.bucketGet(bucket='dd_zajk_account', key=account)
    accountVip = '2099-12-31'
    username = sg.bucketGet(bucket='dd_zajk_username', key=account)

    if len(accountVip) == 0:
        vip_status = '⚠️ 未授权'
    elif accountVip < today_time:
        vip_status = '❌ 已过期'
    else:
        vip_status = f'✅ {accountVip}'

    account_info = f"""
=======账号详情======
📱 账号: {username}
🔐 授权: {vip_status}
=================="""
    sender.reply(account_info)
    menu = """
=======账号管理======
[1] 授权账号
[2] 删除账号
------------------
回复数字选择功能
回复"q"退出操作
=================="""
    sender.reply(menu)
    inputmessage = sender.input(60000, 1, False)
    if not inputmessage:
        sender.reply('⏰ 操作超时（60秒未响应），请重新发送指令操作')
        exit(0)
    elif inputmessage == '2':
        confirm_msg = """=======删除警告=======
❌ 确定要删除该账号吗？
------------------
此操作不可恢复！
[y] 确认删除
[n] 取消操作
===================="""
        sender.reply(confirm_msg)

        yesorno = sender.input(60000, 1, False)
        if not yesorno:
            sender.reply('⏰ 操作超时（60秒未响应），请重新发送指令操作')
            exit(0)
        elif yesorno.lower() in ['y', '是']:
            accounts.remove(str(account))
            qlid = allenvs(osname=dd_zajk_osname, account=str(account))
            delenvs(id=qlid)
            if len(accounts) == 0:
                sg.bucketDel(bucket='dd_zajk_user', key=userid)
            else:
                sg.bucketSet(bucket='dd_zajk_user', key=userid, value=f'{accounts}')
            sg.bucketDel(bucket='dd_zajk_account', key=account)
            sg.bucketDel(bucket='dd_zajk_username', key=account)
            True
            sender.reply('✅ 账号删除成功!')
        else:
            sender.reply('✅ 已取消删除')
            exit(0)

    elif inputmessage == '1':
        auth_guide = """=======授权设置=======
请输入授权月数(如:1)
------------------
回复数字设置月数
回复"q"退出操作
===================="""
        sender.reply(auth_guide)

        mes = sender.input(60000, 1, False)
        if not mes:
            sender.reply('⏰ 操作超时（60秒未响应），请重新发送指令操作')
            exit(0)
        elif mes.lower() == 'q':
            sender.reply("✅ 已取消授权")
            exit(0)

        mes = ValueErrors(value=mes, count=999)
        money = Decimal(mes) * Decimal(zajkVipmoney)

        zf(project='众安授权', me_as_int=mes, accountVip=accountVip, account_str=account_str,
           username=username, account=account)

        accountVip = empower(empowertime=accountVip, me_as_int=mes)
        True
        ql_value = account_str.replace('#', '&') if account_str else ''
        Addenvs(osname=dd_zajk_osname, value=ql_value, account=account, username=username)

        result_msg = f"""=======订单完成=======
🎈 名称: 众安授权
🎉 数量: {mes} 个月
💰 金额: {money} 元
===================="""
        sender.reply(result_msg)

    elif inputmessage.lower() == 'q':
        sender.reply('✅ 已退出管理')
        exit(0)
    else:
        sender.reply('❌ 输入无效')
        exit(0)

def yesornos():
    yesorno = sender.input(60000, 1, False)
    if yesorno.lower() in ['y', '是']:
        return True
    elif yesorno.lower() in ['n', '否']:
        return False
    elif not yesorno:
        sender.reply('⏰ 操作超时（60秒未响应），请重新发送指令操作')
        exit(0)
    elif yesorno.lower() in ['q', '退出']:
        sender.reply('✅ 已退出!')
        exit(0)
    else:
        sender.reply('❌ 输入错误！')
        exit(0)

def zf(project, me_as_int, accountVip, account_str, username, account):
    try:
        zsm = sg.bucketGet('dd_zajk_config', 'zsm')
        use_ma_pay = '2099-12-31' == 'true'

        if not zsm and not use_ma_pay:
            sender.reply('❌ 未配置收款方式,请检查配置!')
            exit(0)

        usercoin = sg.bucketGet('dd_sign_points', userid) or '0'
        zfcoin = int(zajkcoin) * me_as_int

        pay_options = []

        if zsm:
            money = Decimal(me_as_int) * Decimal(zajkVipmoney)
            pay_options.append({
                'type': 'wechat',
                'name': '微信支付',
                'money': money,
                'zfcoin': 0
            })

        if use_ma_pay:
            ma_pay_config = {
                'switch': '2099-12-31' or 'false',
                'gateway': '2099-12-31',
                'pid': '2099-12-31',
                'key': '2099-12-31',
                'type': '2099-12-31',
                'notify_url': '2099-12-31',
                'return_url': '2099-12-31'
            }

            if ma_pay_config['switch'].lower() == 'true' and all([ma_pay_config['gateway'], ma_pay_config['pid'], ma_pay_config['key']]):
                money = Decimal(me_as_int) * Decimal(zajkVipmoney)
                pay_options.append({
                    'type': 'mapay',
                    'name': '在线处理',
                    'money': money,
                    'zfcoin': 0,
                    'config': ma_pay_config
                })

        if zajkcoin and int(zajkcoin) > 0:
            pay_options.append({
                'type': 'coin',
                'name': '积分支付',
                'money': 0,
                'zfcoin': zfcoin
            })

        pay_menu = """=====选择支付方式===="""
        for idx, option in enumerate(pay_options, 1):
            if option['type'] == 'wechat':
                pay_menu += f"""
{idx}️⃣ 微信支付
   💰 {option['money']}元/{me_as_int}月"""
            elif option['type'] == 'mapay':
                pay_menu += f"""
{idx}️⃣ 在线处理
   💰 {option['money']}元/{me_as_int}月"""
            elif option['type'] == 'coin':
                pay_menu += f"""
{idx}️⃣ 积分支付
   🎯 {option['zfcoin']}积分/{me_as_int}月
   💫 当前积分: {usercoin}"""

        pay_menu += """
------------------
回复数字选择方式
回复"q"退出操作
=================="""
        sender.reply(pay_menu)
        choice = sender.input(60000, 1, False)

        if choice == 'q' or choice == 'Q':
            sender.reply("✅ 已取消支付")
            exit(0)

        try:
            choice_idx = int(choice) - 1
            if choice_idx < 0 or choice_idx >= len(pay_options):
                sender.reply("❌ 输入无效")
                exit(0)
            selected = pay_options[choice_idx]
        except ValueError:
            sender.reply("❌ 输入无效")
            exit(0)

        if selected['type'] == 'wechat':
            zfzt = False
            if zfzt:
                sender.reply('⚠️ 当前有人正在支付,请稍后再试！')
                exit(0)

            money = selected['money']

            pay_msg = f"""=====微信扫在线处理====
🎫 商品: {project}
📅 时长: {me_as_int}月
💰 金额: {money}元
------------------
请使用微信扫在线处理
回复"q"取消支付
=================="""
            sender.reply(pay_msg)
            sender.replyImage(zsm)

            ddzf = False

            if str(ddzf) == 'q':
                sender.reply('✅ 已取消支付')
                exit(0)

            try:
                if isinstance(ddzf, dict):
                    if ddzf.get('Type') == '微信赞赏':
                        Money = float(ddzf.get('Money', 0))
                    elif ddzf.get('Type') == '微信收款':
                        Money = float(ddzf.get('Money', 0))
                    elif ddzf.get('Money'):
                        Money = float(ddzf.get('Money', 0))
                    elif ddzf.get('money'):
                        Money = float(ddzf.get('money', 0))
                    else:
                        sender.reply('❌ 不支持的支付消息格式')
                        exit(0)
                else:
                    try:
                        ddzf = json.loads(ddzf)
                        Money = float(ddzf.get('Money', ddzf.get('money', 0)))
                    except:
                        sender.reply("❌ 无法解析支付结果")
                        exit(0)

                if float(Money) >= float(money):
                    return True
                else:
                    sender.reply(f"""=====支付金额错误=====
💰 应付: {money}元
💳 实付: {Money}元
❗ 请稍后核对支付记录！
==================""")
                    exit(0)
            except Exception as e:
                sender.reply(f"❌ 处理支付结果时出错: {str(e)}")
                exit(0)

        elif selected['type'] == 'coin':
            if int(usercoin) < selected['zfcoin']:
                sender.reply(f"""=====积分不足=====
👤 当前积分: {usercoin}
📍 需要积分: {selected['zfcoin']}
==================""")
                exit(0)

            confirm_msg = f"""=====积分支付确认=====
💫 消耗积分: {selected['zfcoin']}
⏰ 授权时长: {me_as_int}月
------------------
确认请回复【y】
取消请回复【n】
=================="""
            sender.reply(confirm_msg)

            if yesornos():
                new_balance = int(usercoin) - selected['zfcoin']
                sg.bucketSet('dd_sign_points', userid, str(new_balance))
                return True
            else:
                sender.reply("✅ 已取消支付")
                exit(0)

    except Exception as e:
        sender.reply(f"❌ 支付处理发生错误: {str(e)}")
        exit(0)

def cxs():
    if len(uservalue) == 0:
        sender.reply(f"""=======未绑定账号=======
❌ 未找到任何账号信息
💡 发送 {randomsigncommand} 绑定
====================""")
        return
    accounts = list(dict.fromkeys(_sg_literal(uservalue))) if uservalue else []
    sg.bucketSet(bucket='dd_zajk_user', key=userid, value=f'{accounts}')
    for account in accounts:
        account_str = sg.bucketGet(bucket='dd_zajk_account', key=account)
        accountVip = '2099-12-31'
        username = sg.bucketGet(bucket='dd_zajk_username', key=account)

        if len(accountVip) == 0 or accountVip < today_time:
            sender.reply(f"""=======授权过期=======
📱 账号: {username}
⚠️ 状态: 授权已过期
💡 发送 {randommanagecommand} 续费
====================""")
            continue

        token_cookie = account_str

        info = query_zajk_info(token_cookie)

        if info["success"]:
            sum_award = info.get("sum_award", 0) / 100
            sum_withdraw = info.get("sum_allow_withdraw", 0) / 100
            is_signed = info.get("is_signed", False)
            reward_count = info.get("reward_count", 0)
            sign_icon = '✅ 已签到' if is_signed else '❌ 未签到'

            msg = f"""=======账号详情=======
📱 账号: {username}
🔐 授权至: {accountVip}
━━━━━━━━━━━━━━
💰 累计金额: {sum_award:.2f}元
💵 可提现: {sum_withdraw:.2f}元
📋 签到状态: {sign_icon}"""
            if reward_count > 0:
                msg += f"\n🎁 待领奖励: {reward_count}个"
            msg += "\n===================="
            sender.reply(msg)
        else:
            sender.reply(f"""=======账号详情=======
📱 账号: {username}
🔐 授权至: {accountVip}
❌ 查询失败: {info.get('error', '未知错误')}
💡 请重新登录更新账号
====================""")

def zajk_auth():
    return True

def clean_expired_accounts():
    users = sg.bucketAllKeys('dd_zajk_user')
    if not users:
        sender.reply("""=======清理完成=====
🧹 没有需要清理的账号
====================""")
        exit(0)

    cleaned_count = 0
    ql_cleaned = 0

    for user in users:
        accountlist = sg.bucketGet('dd_zajk_user', user)
        if accountlist == '' or accountlist == '{}':
            continue

        accounts = _sg_literal(accountlist)
        valid_accounts = []

        for account in accounts:
            accountVip = '2099-12-31'
            if accountVip and accountVip > today_time:
                valid_accounts.append(account)
            else:
                cleaned_count += 1
                sg.bucketDel(bucket='dd_zajk_account', key=account)
                sg.bucketDel(bucket='dd_zajk_username', key=account)
                True

                try:
                    qlid = allenvs(dd_zajk_osname, account)
                    if qlid:
                        delenvs(qlid)
                        ql_cleaned += 1
                except:
                    pass

        if len(valid_accounts) == 0:
            sg.bucketDel(bucket='dd_zajk_user', key=user)
        else:
            sg.bucketSet('dd_zajk_user', user, str(valid_accounts))

    sender.reply(
        "=====清理完成=====\n"
        f"🧹 清理插件账号: {cleaned_count}个\n"
        f"🔧 清理青龙变量: {ql_cleaned}个\n"
        "==================="
    )
    exit(0)

if __name__ == '__main__':
    dd_zajk_osname, dd_zajk_qlname, dd_managecommand, dd_querycommand, dd_signcommand, randommanagecommand, randomquerycommand, randomsigncommand, zajkVipmoney, zajkcoin = getusercontent()
    QLurl, qltoken = seekql()
    usermessage = sender.getMessage()

    if usermessage in ['众安登录', '登录众安']:
        bind()
    elif usermessage in ['众安管理', '管理众安']:
        management()
    elif usermessage in ['众安查询', '查询众安']:
        cxs()
    elif usermessage in ['众安授权']:
        zajk_auth()
    elif usermessage in ['众安清理', '清理众安']:
        clean_expired_accounts()
    else:
        users = sg.bucketAllKeys(bucket='dd_zajk_user')
        if not users:
            exit(0)

        for user in users:
            try:
                user_val = sg.bucketGet(bucket='dd_zajk_user', key=user)
                if not user_val:
                    continue

                accounts = _sg_literal(user_val)
                for account in accounts:
                    try:
                        account_str = sg.bucketGet(bucket='dd_zajk_account', key=account)
                        accountVip = '2099-12-31'

                        if not account_str:
                            continue

                        if len(accountVip) == 0 or accountVip < today_time:
                            print(f"账号 {account} 授权已过期")
                            continue

                        token_cookie = account_str

                        access_token, cookie = parse_token_cookie(token_cookie)
                        if not access_token or not cookie:
                            print(f"账号 {account} Token格式错误")
                            continue

                        session = requests.Session()
                        session.verify = False

                        headers = za_get_headers(access_token, use_cookie=False)
                        home_body = {"activityCode": ACTIVITY_CODE, "channelCode": CHANNEL_CODE}
                        home_url = f"https://{API_HOST}/api/lemon/v1/common/activity/homePage"

                        resp = session.post(home_url, headers=headers, json=home_body, timeout=15)
                        home_result = resp.json()

                        if home_result.get("code") != "0":
                            print(f"账号 {account} 获取首页失败: {home_result.get('message', '未知')}")
                            continue

                        print(f"账号 {account} 获取首页成功")
                        time.sleep(random.uniform(2, 4))

                        sign_url = f"https://{API_HOST}/api/lemon/v1/common/activity/signIn"
                        sign_resp = session.post(sign_url, headers=headers, json=home_body, timeout=15)
                        sign_result = sign_resp.json()
                        if sign_result.get("code") == "0":
                            print(f"账号 {account} 签到成功")
                        else:
                            print(f"账号 {account} 签到: {sign_result.get('message', '失败')}")
                        time.sleep(random.uniform(2, 4))

                        product_recommend = home_result.get("result", {}).get("productRecommend", {}) or {}
                        product_keys = list(product_recommend.keys())[:3]
                        product_headers = za_get_headers(access_token, use_cookie=True, cookie=cookie)
                        for goods_code in product_keys:
                            task_url = f"https://{API_HOST}/api/lemon/v1/applet/mgm/activity/add/award"
                            task_body = {
                                "activityCode": ACTIVITY_CODE,
                                "channelCode": "1000000004",
                                "goodsCode": goods_code,
                                "taskId": "110"
                            }
                            task_resp = session.post(task_url, headers=product_headers, json=task_body, timeout=15)
                            task_result = task_resp.json()
                            if task_result.get("code") == "0":
                                print(f"账号 {account} 商品任务 {goods_code} 完成")
                            else:
                                print(f"账号 {account} 商品任务 {goods_code} 失败: {task_result.get('message')}")
                            time.sleep(random.uniform(2, 4))

                        resp2 = session.post(home_url, headers=headers, json=home_body, timeout=15)
                        home_result2 = resp2.json()

                        if home_result2.get("code") == "0":
                            reward_list = home_result2.get("result", {}).get("valuableRewardList", []) or []
                            lottery_url = f"https://{API_HOST}/api/lemon/v1/common/activity/lottery"
                            for reward in reward_list:
                                award_id = reward.get("awardDetailId")
                                if not award_id:
                                    continue
                                lottery_body = {
                                    "channelCode": CHANNEL_CODE,
                                    "activityCode": ACTIVITY_CODE,
                                    "id": award_id
                                }
                                lottery_resp = session.post(lottery_url, headers=headers, json=lottery_body, timeout=15)
                                lottery_result = lottery_resp.json()
                                if lottery_result.get("code") == "0":
                                    print(f"账号 {account} 抽奖 {award_id} 成功")
                                else:
                                    print(f"账号 {account} 抽奖 {award_id} 失败: {lottery_result.get('message')}")
                                time.sleep(random.uniform(2, 4))
                            else:
                                if not reward_list:
                                    print(f"账号 {account} 今日无可领取奖励")
                        else:
                            print(f"账号 {account} 二次获取首页失败")

                        sum_allow_withdraw = home_result2.get("result", {}).get("sumAllowWithdraw", 0) if home_result2.get("code") == "0" else 0
                        sum_award = home_result2.get("result", {}).get("sumAward", 0) if home_result2.get("code") == "0" else 0
                        print(f"账号 {account} 累计金额: {sum_award/100:.2f}元 | 可提现: {sum_allow_withdraw/100:.2f}元")

                        if sum_allow_withdraw >= 500:  # 500分=5元
                            withdraw_url = f"https://{API_HOST}/api/lemon/v1/common/activity/withdraw"
                            withdraw_body = {
                                "channelCode": CHANNEL_CODE,
                                "activityCode": ACTIVITY_CODE,
                                "amount": 500
                            }
                            withdraw_resp = session.post(withdraw_url, headers=headers, json=withdraw_body, timeout=15)
                            withdraw_result = withdraw_resp.json()
                            if withdraw_result.get("code") == "0":
                                print(f"账号 {account} 提现5元成功!")
                            else:
                                print(f"账号 {account} 提现失败: {withdraw_result.get('message')}")
                        else:
                            print(f"账号 {account} 可提现不足5元，跳过")

                        print(f"账号 {account} 运行完毕")

                    except Exception as e:
                        print(f"处理账号 {account} 时出错: {str(e)}")
                        continue

            except Exception as e:
                print(f"处理用户 {user} 时出错: {str(e)}")
                continue
