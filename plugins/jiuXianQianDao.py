# [title: 酒仙签到]
# [name: jiuXianQianDao]
# [language: python]
# [class: 任务]
# [author: rujingxianghai]
# [version: v1.6]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(酒仙|jx)(登录|登陆)$|^登(录|陆)(酒仙|jx)$|^(酒仙|jx)(查询|管理)$|^(查询|管理)(酒仙|jx)$|^酒仙$|^酒仙检测$|^(酒仙|jx)教程$|^教程(酒仙|jx)$]
# [cron: 0 9 * * *]
# [icon: https://api.iconify.design/lucide:apple.svg]
# [description: 酒仙签到，每日签到浏览任务领金币；1.5：支持AI验证码识别，可配置开关、API地址、密钥、模型]
# [depe: ["requests","urllib3"]]


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
    's_jx_qlname': form.string().title('设置对接容器').default('').description('青龙容器参数用丨分割'),
    's_jx_osname': form.string().title('青龙变量名').default('').description('青龙容器内酒仙的变量名'),
    's_jx_notify': form.string().title('通知渠道').default('').description('检测通知推送渠道'),
    's_jx_ai_ocr_switch': form.boolean().title('AI验证码识别').default(False).description('开启后使用AI自动识别验证码，关闭则手动输入'),
    's_jx_ai_api_url': form.string().title('AI API地址').default('').description('默认使用硅基流动'),
    's_jx_ai_api_key': form.string().title('AI API密钥').default('').description('硅基流动或其他兼容OpenAI API的密钥'),
    's_jx_ai_model': form.string().title('AI模型').default('').description('视觉语言模型名称'),
})
_CONFIG_FIELD_MAP = {
    ('s_jx', 'qlname'): 's_jx_qlname',
    ('s_jx', 'osname'): 's_jx_osname',
    ('s_jx', 'notify'): 's_jx_notify',
    ('s_jx', 'ai_ocr_switch'): 's_jx_ai_ocr_switch',
    ('s_jx', 'ai_api_url'): 's_jx_ai_api_url',
    ('s_jx', 'ai_api_key'): 's_jx_ai_api_key',
    ('s_jx', 'ai_model'): 's_jx_ai_model',
}

import os
import json
import time
import random
import string
import re
import requests
import base64
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()
uservalue = sg.bucketGet(bucket='s_jx_user', key=userid)

PLUGIN_CONFIG = {'bucket': 's_jx', 'coin_key': 'dd_sign_points', 'name': '酒仙'}
PAY_TYPE_NAMES = {'alipay': '支付宝', 'wxpay': '微信支付', 'qqpay': 'QQ钱包'}


class JiuxianConfig:
    APP_NAME = "酒仙"
    VERSION = "9.2.16"
    LOGIN_URL = "https://newappuser.jiuxian.com/user/loginUserNamePassWd.htm"
    CAPTCHA_URL = "https://newappuser.jiuxian.com/messages/graphCode.htm"
    MEMBER_INFO_URL = "https://newappuser.jiuxian.com/memberChannel/memberInfo.htm"

    APP_DEVICE_INFO = {
        "appKey": "daab51fd-a40a-3943-bc95-2f46919da694",
        "appVersion": "9.2.16",
        "areaId": "500",
        "channelCode": "0",
        "cpsId": "tencent",
        "deviceIdentify": "daab51fd-a40a-3943-bc95-2f46919da694",
        "deviceType": "ANDROID",
        "deviceTypeExtra": "0",
        "equipmentType": "SM-A5260",
        "netEnv": "wifi",
        "screenReslolution": "720x1280",
        "supportWebp": "1",
        "sysVersion": "12"
    }

    APP_HEADERS = {
        "User-Agent": "okhttp/3.14.9",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "newappuser.jiuxian.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }

    MINI_PROGRAM_INFO = {
        'appKey': '1ba8b341-5a56-49dc-8ee3-92b32db7fc21',
        'appVersion': '9.2.12',
        'apiVersion': '1.0',
        'areaId': '2048',
        'channelCode': '0, 1',
        'appChannel': 'xiaochengxu',
        'deviceType': 'XIAOCHENGXU',
        'supportWebp': '2',
        'longi': '115.80287868923611',
        'lati': '28.155340440538193',
        'screenReslolution': '412x915',
        'sysVersion': 'Android 14'
    }

    MINI_PROGRAM_HEADERS = {
        "Host": "newappuser.jiuxian.com",
        "Connection": "keep-alive",
        "content-type": "application/json",
        "User-Agent": "Mozilla/5.0 (Linux; Android 14; M2011K2C) AppleWebKit/537.36 Chrome/138.0.7258.158 Mobile Safari/537.36 MicroMessenger/8.0.64.2940",
        "Accept-Encoding": "gzip, deflate, br"
    }


def get_ai_config():
    """获取AI验证码识别配置"""
    ai_switch = sg.bucketGet('s_jx', 'ai_ocr_switch') or 'false'
    ai_url = sg.bucketGet('s_jx', 'ai_api_url') or 'https://api.siliconflow.cn/v1'
    ai_key = sg.bucketGet('s_jx', 'ai_api_key') or ''
    ai_model = sg.bucketGet('s_jx', 'ai_model') or 'Qwen/Qwen3-VL-235B-A22B-Thinking'
    return ai_switch.lower() == 'true', ai_url.strip(), ai_key.strip(), ai_model.strip()


def generate_push_token(length=44):
    """生成随机pushToken，由大小写字母和数字组成"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def get_captcha():
    """获取验证码图片
    :return: (成功标志, 验证码base64编码)
    """
    try:
        params = JiuxianConfig.APP_DEVICE_INFO.copy()
        params["pushToken"] = generate_push_token()
        params["type"] = "13"

        headers = {
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive",
            "Host": "newappuser.jiuxian.com",
            "User-Agent": "okhttp/3.14.9"
        }

        response = requests.get(
            JiuxianConfig.CAPTCHA_URL,
            params=params,
            headers=headers,
            timeout=15,
            verify=False
        )

        if response.status_code == 200:
            data = response.json()
            if data.get("success") == "1" and data.get("result", {}).get("imgCode"):
                return True, data["result"]["imgCode"]
            return False, data.get('errMsg', '获取验证码失败')
        return False, f"HTTP {response.status_code}"
    except Exception as e:
        return False, str(e)


def recognize_captcha_with_ai(img_base64):
    """使用AI识别验证码
    :param img_base64: 验证码图片的base64编码
    :return: 识别结果，失败返回None
    """
    ai_switch, ai_url, ai_key, ai_model = get_ai_config()

    if not ai_key:
        return None

    try:
        url = f"{ai_url.rstrip('/')}/chat/completions"

        headers = {
            "Authorization": f"Bearer {ai_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": ai_model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_base64}",
                                "detail": "high"
                            }
                        },
                        {
                            "type": "text",
                            "text": "这是一个验证码图片，请识别图片中的验证码字符。只需要返回验证码内容，不要包含任何其他文字、解释或标点符号。验证码通常是4-6位的字母和数字组合。"
                        }
                    ]
                }
            ],
            "max_tokens": 50,
            "temperature": 0.1
        }

        response = requests.post(url, json=payload, headers=headers, timeout=30, verify=False)
        response.raise_for_status()

        result = response.json()

        if "choices" in result and len(result["choices"]) > 0:
            content = result["choices"][0].get("message", {}).get("content", "")
            code = re.sub(r'[^a-zA-Z0-9]', '', content.strip())
            if code:
                return code
        return None
    except Exception as e:
        return None


def jx_login(username, password, verify_code=None):
    """酒仙登录（带验证码）"""
    try:
        login_data = JiuxianConfig.APP_DEVICE_INFO.copy()
        login_data["pushToken"] = generate_push_token()
        login_data.update({
            "userName": username,
            "passWord": password,
            "verifyCode": verify_code or ""
        })

        response = requests.post(
            JiuxianConfig.LOGIN_URL,
            data=login_data,
            headers=JiuxianConfig.APP_HEADERS,
            timeout=15,
            verify=False
        )

        if response.status_code == 200:
            result = response.json()
            if result.get("success") == "1":
                user_info = result["result"]["userInfo"]
                return True, user_info["token"], user_info.get("uname", "")
            return False, None, result.get('errMsg', '登录失败')
        return False, None, f"HTTP {response.status_code}"
    except Exception as e:
        return False, None, str(e)


def jx_userinfo(token):
    """获取酒仙用户信息"""
    try:
        params = JiuxianConfig.MINI_PROGRAM_INFO.copy()
        params["token"] = token
        params["equipmentType"] = json.dumps({
            "deviceAbi": "arm64-v8a",
            "system": "Android 14",
            "model": "M2011K2C",
            "brand": "Xiaomi",
            "platform": "android"
        })

        response = requests.get(
            JiuxianConfig.MEMBER_INFO_URL,
            params=params,
            headers=JiuxianConfig.MINI_PROGRAM_HEADERS,
            timeout=15,
            verify=False
        )

        if response.status_code == 200:
            result = response.json()
            if result.get("success") == "1":
                return True, result["result"]
        return False, "获取失败"
    except Exception as e:
        return False, str(e)


def get_user_content():
    osname = sg.bucketGet('s_jx', 'osname') or 'S_JIUXIAN'
    qlname = sg.bucketGet('s_jx', 'qlname') or ''
    Vipmoney = float(sg.bucketGet('s_jx', 'Vipmoney') or '1')
    coin = sg.bucketGet(PLUGIN_CONFIG['bucket'], PLUGIN_CONFIG['coin_key'])
    if not coin:
        coin = sg.bucketGet('s_jx', 'coin') or '0'
    return osname, qlname, '酒仙管理', '酒仙查询', '酒仙登录', Vipmoney, int(coin)


def mask_account(account):
    if not account or len(account) < 4:
        return account
    if account.isdigit() and len(account) == 11:
        return f"{account[:3]}****{account[7:]}"
    return f"{account[:2]}***{account[-2:]}"


def login_with_captcha(username, password):
    """登录流程：支持AI自动识别或手动输入验证码
    :return: (success, token, result_msg)
    """
    ai_switch, ai_url, ai_key, ai_model = get_ai_config()

    captcha_success, captcha_result = get_captcha()
    if not captcha_success:
        return False, None, f"获取验证码失败: {captcha_result}"

    img_base64 = captcha_result
    verify_code = None

    if ai_switch and ai_key:
        verify_code = recognize_captcha_with_ai(img_base64)
        if not verify_code:
            sender.reply(f"❌ AI识别失败，请手动输入")

    if not verify_code:
        sender.reply("请输入验证码（60秒内有效）：")
        try:
            api_url = "https://qrcode.example.invalid/api/image/base64"
            api_key = ""

            response = requests.post(
                api_url,
                json={"base64": img_base64},
                headers={"X-API-Key": api_key},
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()
                if result.get('success') and result.get('data', {}).get('url'):
                    sender.replyImage(result['data']['url'])
                else:
                    sender.reply(f"[验证码图片转换失败: {result.get('error', '未知错误')}，请重试]")
                    return False, None, "验证码图片转换失败"
            else:
                sender.reply(f"[验证码图片上传失败: HTTP {response.status_code}，请重试]")
                return False, None, "验证码图片上传失败"
        except Exception as e:
            sender.reply(f"[验证码图片发送失败: {str(e)}，请重试]")
            return False, None, "验证码图片发送失败"

        user_input = sender.input(60000, 1, False)
        if not user_input:
            return False, None, "验证码输入超时"
        if user_input.lower() == 'q':
            return False, None, "用户取消"
        verify_code = user_input.strip()

    success, token, result = jx_login(username, password, verify_code)

    if not success and result and "验证码" in result and ai_switch and ai_key:
        sender.reply(f"⚠️ 验证码错误，正在重试...")
        captcha_success, captcha_result = get_captcha()
        if captcha_success:
            verify_code = recognize_captcha_with_ai(captcha_result)
            if verify_code:
                success, token, result = jx_login(username, password, verify_code)

    return success, token, result


def bind_account():
    """绑定账号"""
    sender.reply(
        "=====酒仙登录=====\n"
        "支持批量登录，格式如下:\n"
        "账号#密码\n"
        "（多账号换行分隔）\n"
        "------------------\n"
        "回复\"q\"退出操作\n"
        "=================="
    )
    input_text = sender.input(120000, 1, False)
    if not input_text:
        sender.reply("⏰ 操作超时")
        return
    if input_text.lower() == 'q':
        sender.reply("✅ 已取消")
        return

    lines = [line.strip() for line in input_text.strip().split('\n') if line.strip()]
    account_list = []
    for line in lines:
        if '#' in line:
            parts = line.split('#', 1)
            if len(parts) == 2 and parts[0].strip() and parts[1].strip():
                account_list.append({
                    'username': parts[0].strip(),
                    'password': parts[1].strip()
                })

    if not account_list:
        sender.reply("❌ 未检测到有效账号\n格式: 账号#密码")
        return

    sender.reply(f"🔄 正在登录 {len(account_list)} 个账号...")

    success_count = 0
    fail_count = 0
    success_accounts = []

    for acc in account_list:
        username = acc['username']
        password = acc['password']

        try:
            success, token, result = login_with_captcha(username, password)
            if not success:
                sender.reply(f"❌ {mask_account(username)} 登录失败: {result}")
                fail_count += 1
                continue

            current_value = sg.bucketGet('s_jx_user', userid)
            if not current_value:
                sg.bucketSet('s_jx_user', userid, str([username]))
            else:
                accounts = _sg_literal(current_value)
                if username not in accounts:
                    accounts.append(username)
                    sg.bucketSet('s_jx_user', userid, str(accounts))

            account_info = {"username": username, "password": password, "token": token}
            sg.bucketSet('s_jx_token', username, json.dumps(account_info))

            success_count += 1
            success_accounts.append({'username': username, 'info': account_info})
            sender.reply(f"✅ {mask_account(username)} 登录成功")

        except Exception as e:
            sender.reply(f"❌ {mask_account(username)} 异常: {str(e)}")
            fail_count += 1

    sender.reply(
        f"=====登录完成=====\n"
        f"✅ 成功: {success_count}个\n"
        f"❌ 失败: {fail_count}个\n"
        f"=================="
    )

    if success_accounts:
        dqsj = datetime.now().strftime("%Y-%m-%d")
        need_auth = []
        for acc in success_accounts:
            username = acc['username']
            accountVip = '2099-12-31'
            if accountVip and accountVip > dqsj:
                sender.reply(f"📱 {mask_account(username)} 已授权，到期: {accountVip}")
                update_ql_env(username, acc['info'])
            else:
                need_auth.append(acc)

        if need_auth:
            sender.reply(f"\n📋 {len(need_auth)} 个账号需要授权")
            authorize_multiple_accounts([acc['username'] for acc in need_auth])


def query_accounts():
    """查询账号"""
    if not uservalue:
        sender.reply(f"=====未绑定账号=====\n❌ 未找到账号\n💡 发送 酒仙登录 绑定\n==================")
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
                account_info = json.loads(sg.bucketGet('s_jx_token', username))
                auth_time = '2099-12-31'
                auth_status = '已授权' if auth_time and auth_time >= str(datetime.now().date()) else '未授权'

                login_success, token, _ = jx_login(username, account_info.get('password', ''))
                user_info_text = ""
                if login_success:
                    info_success, user_data = jx_userinfo(token)
                    if info_success:
                        gold = user_data.get('goldMoney', 0)
                        sign_days = user_data.get('signDays', 0)
                        is_signed = user_data.get('isSignTody', False)
                        user_info_text = (
                            f"\n💰 金币: {gold}"
                            f"\n📅 连续签到: {sign_days}天"
                            f"\n✅ 今日签到: {'已签' if is_signed else '未签'}"
                        )

                sender.reply(
                    f"=====账号信息[{i}/{len(selected)}]=====\n"
                    f"📱 账号: {mask_account(username)}\n"
                    f"🏷 状态: {auth_status}\n"
                    f"📅 到期: {auth_time or '未授权'}{user_info_text}\n"
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
                sg.bucketDel('s_jx_token', username)
                True
                delete_ql_env(username)

            if accounts:
                sg.bucketSet('s_jx_user', userid, str(accounts))
            else:
                sg.bucketDel('s_jx_user', userid)
            sender.reply(f"✅ 已删除 {len(selected)} 个账号")
        else:
            sender.reply("✅ 已取消")
    elif choice == '3':
        success = 0
        for username in selected:
            try:
                account_info = json.loads(sg.bucketGet('s_jx_token', username))
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



def admin_authorization(username, account_info, days):
    return True



def generate_iframe_url(url):
    """将URL通过base64编码生成iframe页面链接"""
    try:
        encoded = base64.b64encode(url.encode('utf-8')).decode('utf-8')
        iframe_url = f"https://metwhale.github.io?u={encoded}"
        return iframe_url
    except Exception as e:
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
    except Exception as e:
        pass

    try:
        encoded_url = requests.utils.quote(url)
        api_url = f"https://api.qrtool.cn/?text={encoded_url}&size=300&level=M"
        return api_url
    except Exception as e:
        return None


def handle_mapay_order(project, months, money, pay_type=None):
    return True


def pay_order(project, months, money):
    return True


def get_ql_token(host, client_id, client_secret):
    """获取青龙Token"""
    try:
        url = f'{host}/open/auth/token?client_id={client_id}&client_secret={client_secret}'
        resp = requests.get(url, timeout=10).json()
        if resp.get('code') == 200:
            return resp['data']['token']
        return None
    except:
        return None


def update_ql_env(username, account_info):
    """更新青龙环境变量"""
    account = account_info.get('username', '')
    password = account_info.get('password', '')
    if not account or not password:
        return False

    env_value = f"{account}#{password}"
    qlconfig = sg.bucketGet('s_jx', 'qlname')
    if not qlconfig:
        return False

    configs = qlconfig.replace('|', '丨').split('丨')
    if len(configs) < 3:
        return False

    host, client_id, client_secret = [x.strip() for x in configs]

    try:
        token = get_ql_token(host, client_id, client_secret)
        if not token:
            return False

        headers = {'Authorization': f'Bearer {token}'}
        osname = sg.bucketGet('s_jx', 'osname') or 'S_JIUXIAN'
        auth_time = '2099-12-31' or '未授权'

        envs = requests.get(
            f'{host}/open/envs?searchValue={username}',
            headers=headers,
            timeout=10
        ).json().get('data', [])
        env_id = next((e.get('id') for e in envs if e['name'] == osname), None)

        env_data = {
            'name': osname,
            'value': env_value,
            'remarks': f"酒仙：{username}|到期:{auth_time}"
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


def delete_ql_env(username):
    """删除青龙环境变量"""
    qlconfig = sg.bucketGet('s_jx', 'qlname')
    if not qlconfig:
        return False

    configs = qlconfig.replace('|', '丨').split('丨')
    if len(configs) < 3:
        return False

    host, client_id, client_secret = [x.strip() for x in configs]

    try:
        token = get_ql_token(host, client_id, client_secret)
        if not token:
            return False

        headers = {'Authorization': f'Bearer {token}'}
        osname = sg.bucketGet('s_jx', 'osname') or 'S_JIUXIAN'
        envs = requests.get(f'{host}/open/envs', headers=headers, timeout=10).json().get('data', [])

        for env in envs:
            if env['name'] == osname and username in env.get('remarks', ''):
                env_id = env.get('_id') or env.get('id')
                requests.delete(f'{host}/open/envs', headers=headers, json=[env_id], timeout=10)
                return True
        return False
    except:
        return False



def ks_auth():
    return True


def show_tutorial():
    """显示酒仙使用教程"""
    tutorial = (
        "=====酒仙教程=====\n"
        "📱 用户指令:\n"
        "• 酒仙登录 - 批量绑定酒仙账号\n"
        "• 酒仙查询 - 查询账号状态和金币信息\n"
        "• 酒仙管理 - 授权/删除/提交青龙\n"
        "• 酒仙教程 - 查看本教程\n"
        "------------------\n"
        "🔧 管理员指令:\n"
        "• 酒仙授权 - 管理员按天数授权\n"
        "• 酒仙检测 - 检测过期账号并清理\n"
        "------------------\n"
        "💡 登录格式:\n"
        "📝 格式: 账号#密码\n"
        "📝 示例: \n"
        "13812345678#password123\n"
        "user@example.com#mypass456\n"
        "💡 支持批量登录，每行一个账号\n"
        "------------------\n"
        "📝 账号获取方式:\n"
        "1. 下载酒仙APP注册账号\n"
        "2. 使用手机号或邮箱注册\n"
        "3. 设置登录密码\n"
        "4. 完成实名认证(签到需要)\n"
        "------------------\n"
        "💰 功能说明:\n"
        "• 账号绑定: 保存账号密码到系统\n"
        "• 状态查询: 查看金币、签到天数等\n"
        "• 授权管理: 付费使用插件功能\n"
        "• 青龙提交: 自动提交到青龙容器\n"
        "• 过期检测: 自动清理过期账号\n"
        "------------------\n"
        "🎯 使用流程:\n"
        "1. 发送\"酒仙登录\"绑定账号\n"
        "2. 发送\"酒仙查询\"查看账号状态\n"
        "3. 发送\"酒仙管理\"选择授权账号\n"
        "4. 选择授权时长并完成支付\n"
        "5. 系统自动提交到青龙容器\n"
        "6. 等待定时任务自动执行签到\n"
        "------------------\n"
        "⚠️ 注意事项:\n"
        "• 授权后才能使用签到功能\n"
        "• 过期账号会被自动清理\n"
        "• 支持微信支付和积分兑换\n"
        "• 管理员可批量授权用户\n"
        "=================="
    )
    sender.reply(tutorial)


def main():
    msg = sender.getMessage()

    if '登录' in msg or '登陆' in msg:
        bind_account()
    elif '查询' in msg and ('酒仙' in msg or 'jx' in msg.lower()):
        query_accounts()
    elif '管理' in msg and ('酒仙' in msg or 'jx' in msg.lower()):
        manage_account()
    elif '酒仙授权' in msg:
        ks_auth()
    elif '酒仙检测' in msg:
        if not sender.isAdmin():
            sender.reply("❌ 仅限管理员")
            return
        sender.reply("🔍 正在检测...")
        sender.reply(check_auth_status())
    elif '教程' in msg and ('酒仙' in msg or 'jx' in msg.lower()):
        show_tutorial()
    elif sender.getImtype() == 'fake':
        try:
            sg.notifyMasters(check_auth_status())
        except:
            pass
    else:
        sender.setContinue()


if __name__ == "__main__":
    main()
