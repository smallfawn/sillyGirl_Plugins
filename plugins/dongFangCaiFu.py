# [title: 东方财富]
# [name: dongFangCaiFu]
# [language: python]
# [class: 任务]
# [author: rujingxianghai]
# [version: v1.4]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^东方登录$|^登录东方$|^东方查询$|^东方管理$|^东方$|^东方$|^东方检测$|^东方教程$]
# [cron: 10 7 * * *]
# [icon: https://api.iconify.design/lucide:apple.svg]
# [description: 刷视频领现金，1.5r/日，需实名；微信扫码登录 + 账号密码登录，需要手动登录app绑定账号，进入活动页面一次；脚本群内获取；1.0.7：更新自动识别验证码，使用ddddocr，推荐自行搭建接口；接口项目：https://github.com/sml2h3/ddddocr-fastapi]
# [depe: ["requests"]]


import asyncio as _sg_asyncio, os as _sg_os, time as _sg_time, types as _sg_types, json as _sg_json, re as _sg_re, urllib.parse as _sg_urlparse
from threading import Thread as _sg_Thread
from sillygirl import Adapter as _SGAdapter, Bucket as _SGBucket, Sender as _SGSender, sender as _sg_sender, container as _sg_container
try:
    import ast as _sg_ast
except Exception:
    _sg_ast = None
try:
    import decimal as decimal
except Exception:
    decimal = None

def _sg_run(coro):
    try:
        _sg_asyncio.get_running_loop()
    except RuntimeError:
        return _sg_asyncio.run(coro)
    box={}
    def runner():
        try: box["v"]=_sg_asyncio.run(coro)
        except BaseException as e: box["e"]=e
    t=_sg_Thread(target=runner, daemon=True); t.start(); t.join()
    if "e" in box: raise box["e"]
    return box.get("v")

def _sg_literal(value, default=None):
    if isinstance(value,(list,dict,tuple,set,int,float,bool)) or value is None:
        return value if value is not None else ([] if default is None else default)
    text=str(value or "").strip()
    if not text: return [] if default is None else default
    for parser in (_sg_json.loads, (_sg_ast.literal_eval if _sg_ast else None)):
        if parser:
            try: return parser(text)
            except Exception: pass
    return [] if default is None else default

def _sg_sender_sync(uuid=""):
    s=_SGSender(uuid or _sg_os.environ.get("SENDER_ID", ""))
    def call(name,*a,**k): return _sg_run(getattr(s,name)(*a,**k))
    def listen(timeout=60000,*a,**k):
        try:
            r=call("listen", {"timeout": int(timeout or 0)})
            return _sg_run(r.getContent()) if r else ""
        except Exception: return ""
    return _sg_types.SimpleNamespace(
        getUserID=lambda:call("getUserId"), getUserId=lambda:call("getUserId"), getMessage=lambda:call("getContent"), getContent=lambda:call("getContent"),
        getUserName=lambda:call("getUserName"), getNickname=lambda:call("getUserName"), getChatID=lambda:call("getChatId"), getChatId=lambda:call("getChatId"),
        getImtype=lambda:call("getPlatform"), getPlatform=lambda:call("getPlatform"), getMessageID=lambda:call("getMessageId"), getPluginName=lambda:_sg_os.environ.get("PLUGIN_NAME",""), getPluginVersion=lambda:_sg_os.environ.get("PLUGIN_VERSION",""),
        isAdmin=lambda:bool(call("isAdmin")), reply=lambda msg="":call("reply", str(msg)), replyImage=lambda url="":call("reply", str(url) if str(url).startswith("[") else f"[CQ:image,file={url}]"),
        listen=listen, input=listen, waitInput=listen, setContinue=lambda *a,**k:call("continue_"), breakIn=lambda *a,**k:call("continue_"))

def _sg_bucket_get(bucket=None,key=None,default="",**kw):
    try:
        v=_SGBucket(str(kw.get("bucket",bucket) or ""))[str(kw.get("key",key) or "")]
        return default if v in (None,"") and default not in (None,"") else (v if v is not None else "")
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
    i=a[0] if a and isinstance(a[0],dict) else {}; platform=i.get("imType") or i.get("platform") or kw.get("platform") or (a[0] if a else ""); group=i.get("groupCode") or i.get("group_id") or kw.get("group_id") or (a[1] if len(a)>1 else ""); user=i.get("userID") or i.get("user_id") or kw.get("userID") or (a[2] if len(a)>2 else ""); title=i.get("title") or kw.get("title") or (a[3] if len(a)>3 else ""); content=i.get("content") or i.get("message") or kw.get("content") or (a[4] if len(a)>4 else title)
    return _sg_run(_SGAdapter(str(platform or "")).push({"group_id":str(group or ""),"user_id":str(user or ""),"title":str(title or ""),"content":str(content or "")}))
def _sg_notify(msg,channels=None,*a,**k): return _sg_run(_sg_sender.pushAdmin(str(msg), {"platforms":list(channels or [])} if channels else {}))
class _SGFacade:
    Sender=staticmethod(_sg_sender_sync); getSenderID=staticmethod(lambda:_sg_os.environ.get("SENDER_ID","")); getPluginName=staticmethod(lambda:_sg_os.environ.get("PLUGIN_NAME","")); bucketGet=staticmethod(_sg_bucket_get); bucketSet=staticmethod(_sg_bucket_set); bucketDel=staticmethod(_sg_bucket_del); bucketDelete=staticmethod(_sg_bucket_del); bucketAllKeys=staticmethod(_sg_bucket_keys); bucketKeys=staticmethod(_sg_bucket_keys); bucketAll=staticmethod(_sg_bucket_all); notifyMasters=staticmethod(_sg_notify); pushAdmin=staticmethod(_sg_notify); push=staticmethod(_sg_push); Push=staticmethod(_sg_push); reply=staticmethod(lambda msg="":_sg_sender_sync().reply(msg)); get=staticmethod(lambda key,default="":_sg_bucket_get(*(str(key).split(".",1) if "." in str(key) else ["otto",key]), default=default)); getParam=get; version=staticmethod(lambda:{"sn":_sg_os.environ.get("SILLYGIRL_VERSION","3.0.0"),"version":_sg_os.environ.get("SILLYGIRL_VERSION","3.0.0")}); port=staticmethod(lambda:_sg_os.environ.get("SILLYGIRL_PORT","8080")); sleep=staticmethod(lambda sec:_sg_time.sleep(float(sec or 0)))
sg=_SGFacade(); Sender=sg.Sender; getSenderID=sg.getSenderID; bucketGet=sg.bucketGet; bucketSet=sg.bucketSet; bucketAllKeys=sg.bucketAllKeys; notifyMasters=sg.notifyMasters

def mask_account(value):
    value=str(value or ""); return value if len(value)<=7 else value[:3]+"***"+value[-4:]
def generate_qrcode_url(text): return "https://api.qrserver.com/v1/create-qr-code/?size=260x260&data="+_sg_urlparse.quote(str(text or ""))
def get_pay_config(): return {}
class MaPayClient:
    def create_order(self,*a,**k): return {"error":"","status":True,"data":None}
    def is_paid(self,*a,**k): return True
def calculate_auth_time(*a,**k): return "2099-12-31"
def check_auth_status(*a,**k): return "账号默认可用"
_check_auth_status=check_auth_status
def select_accounts(sender,user_bucket,user_id,*a,**k):
    raw=sg.bucketGet(user_bucket,user_id,[]); raw=_sg_literal(raw,[]) if isinstance(raw,str) else raw
    if isinstance(raw,dict): raw=list(raw.keys()) or list(raw.values())
    return (raw if isinstance(raw,list) else []), (raw if isinstance(raw,list) else [])
def process_authorization(*a,**k): return True
def process_coin_payment(*a,**k): return True
def admin_auth_all_accounts(*a,**k): return True
def admin_auth_by_user(*a,**k): return True
def get_user_points(user_id=None,bucket="dd_sign_points"):
    try: return int(sg.bucketGet(bucket,user_id or sg.getSenderID()) or 0)
    except Exception: return 0
def update_user_points(user_id=None,points=0,bucket="dd_sign_points"): return sg.bucketSet(bucket,user_id or sg.getSenderID(),str(points))
def _sg_panel_id(config=None):
    if isinstance(config,dict): config=config.get("id") or config.get("ID") or config.get("index") or config.get("name")
    m=_sg_re.search(r"\d+", str(config or "")); return int(m.group(0)) if m else 1
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

config = None
_CONFIG_FIELD_MAP = {}

import json
import requests
import re
import uuid
import time
import random
import string
import base64
import hashlib
from datetime import datetime
from decimal import Decimal
import urllib.parse
import os

BUCKET_USER = 's_eastmoney_user'  # 用户账号列表
BUCKET_TOKEN = 's_eastmoney_token'  # 用户Token信息
BUCKET_AUTH = 's_eastmoney_auth'   # 授权信息
BUCKET_CONFIG = 's_eastmoney'      # 插件配置

PAY_TYPE_NAMES = {'alipay': '支付宝', 'wxpay': '微信支付', 'qqpay': 'QQ钱包'}
PLUGIN_NAME = '东方财富'

APPID = "wxb062331269cec15f"  # 东方财富App的微信AppID
BUNDLEID = "com.eastmoney.android.berlin"  # 东方财富App的BundleID
DEFAULT_UA = "Mozilla/5.0 (Linux; Android 15; 2210132C Build/AQ3A.240812.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/130.0.6723.103 Mobile Safari/537.36 XWEB/1300473 MMWEBSDK/20250201 MMWEBID/9172 MicroMessenger/8.0.57.2820(0x28003939) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64"

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()

def get_config():
    """获取插件配置"""
    price = Decimal(sg.bucketGet(BUCKET_CONFIG, 'price') or '0')
    coin_price = sg.bucketGet(BUCKET_CONFIG, 'coin') or ''
    zsm = sg.bucketGet(BUCKET_CONFIG, 'zsm') or ''
    ql_config = sg.bucketGet(BUCKET_CONFIG, 'ql_config') or ''
    ql_envname = sg.bucketGet(BUCKET_CONFIG, 'ql_envname') or 'S_DFCF'
    captcha_api = sg.bucketGet(BUCKET_CONFIG, 'captcha_api') or "http://42.194.132.65:30052/ocr"

    return price, coin_price, zsm, ql_config, ql_envname, captcha_api


def set_auth_success(uid, months, total_price):
    """设置授权成功并显示成功信息"""
    try:
        token_info_str = sg.bucketGet(BUCKET_TOKEN, uid)
        if not token_info_str:
            sender.reply(f"❌ 未找到账号 {uid} 的Token信息")
            return False

        token_info = json.loads(token_info_str)
        alias = token_info.get("Alias", "未知用户")

        auth_time = calculate_auth_time(uid, months)
        True

        _, _, _, ql_config, ql_envname, _ = get_config()
        ql_result = False

        if ql_config:
            ql_result, ql_message = add_to_qinglong(uid, token_info, ql_envname)

        success_msg = f"""
=====授权成功=====
👤 用户: {alias}
📱 UID: {uid}
💰 支付: {total_price}元
📅 有效期至: {auth_time}
------------------
🔄 青龙同步: {'成功' if ql_result else '失败'}
=================="""

        sender.reply(success_msg)
        return True

    except Exception as e:
        sender.reply(f"❌ 设置授权失败: {str(e)}")
        return False

def process_payment_zsm(uid):
    return True

def process_coin_auth(uid):
    return True

def generate_iframe_url(url):
    """将URL通过base64编码生成iframe页面链接

    Args:
        url: 原始支付链接

    Returns:
        str: iframe页面链接
    """
    try:
        encoded = base64.b64encode(url.encode('utf-8')).decode('utf-8')
        iframe_url = f"https://metwhale.github.io?u={encoded}"
        return iframe_url
    except Exception as e:
        return url

def generate_qrcode(url):
    """生成二维码图片

    Args:
        url: 要生成二维码的URL

    Returns:
        str: 二维码图片的URL
    """
    try:
        encoded_url = requests.utils.quote(url)
        api_url = f"https://api.qrtool.cn/?text={encoded_url}&size=300&level=M"
        return api_url
    except Exception as e:
        return None

def handle_mapay_order(project, months, money, pay_type=None):
    return True

def process_auth(uid):
    return True

def process_payment_zsm_with_months(uid, months):
    return True

def process_coin_auth_with_months(uid, months):
    """处理积分兑换授权（已知月数）"""
    try:
        _, coin_price, _, _, _, _ = get_config()

        if not coin_price:
            sender.reply("❌ 积分授权未开启")
            return False

        token_info_str = sg.bucketGet(BUCKET_TOKEN, uid)
        if not token_info_str:
            sender.reply(f"❌ 未找到账号 {uid} 的Token信息")
            return False

        token_info = json.loads(token_info_str)
        alias = token_info.get("Alias", "未知用户")
        user_coin = Decimal(sg.bucketGet('dd_sign_points', userid) or '0')
        required_coin = Decimal(coin_price) * months

        if user_coin < required_coin:
            sender.reply(f"❌ 积分不足，当前积分: {user_coin}，需要积分: {required_coin}")
            return False

        confirm_msg = f"""
=====兑换确认=====
👤 用户: {alias}
📱 UID: {uid}
💰 当前积分: {user_coin}
🎟 兑换: {months}个月
💵 需要积分: {required_coin}
💰 剩余积分: {user_coin - required_coin}
------------------
回复"y"确认兑换
回复其他取消"""

        sender.reply(confirm_msg)
        confirm = sender.listen(60000)

        if confirm.lower() != 'y':
            sender.reply("✅ 已取消兑换")
            return False

        remaining_coin = user_coin - required_coin
        sg.bucketSet('dd_sign_points', userid, str(remaining_coin))

        auth_time = calculate_auth_time(uid, months)
        True

        _, _, _, ql_config, ql_envname, _ = get_config()
        ql_result = False

        if ql_config:
            ql_result, _ = add_to_qinglong(uid, token_info, ql_envname)

        success_msg = f"""
=====兑换成功=====
👤 用户: {alias}
📱 UID: {uid}
🎟️ 兑换: {months}个月授权
📅 有效期至: {auth_time}
💰 剩余积分: {remaining_coin}
------------------
🔄 青龙同步: {'成功' if ql_result else '失败'}
=================="""

        sender.reply(success_msg)
        return True

    except Exception as e:
        sender.reply(f"❌ 积分兑换失败: {str(e)}")
        return False

def generate_unique_id():
    """生成随机的UniqueId，格式类似: Mcb2djFlYjEwMDZmNDc5MmRmNWVkNTAyNDU4YTAwZTA0MGN8fGllbWlfdGx1YWZlZF9tZQ=eb1b="""
    hex_part = ''.join(random.choice('0123456789abcdef') for _ in range(random.randint(32, 40)))

    random_str = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(20, 30)))

    random_str = f"{random_str}|{random.choice('|+*')}|{random.choice(string.ascii_letters)}{random.choice(string.ascii_letters)}{random.choice(string.ascii_letters)}_" \
                + f"{random.choice(string.ascii_letters)}{random.choice(string.ascii_letters)}{random.choice(string.ascii_letters)}{random.choice(string.ascii_letters)}{random.choice(string.ascii_letters)}_" \
                + f"{random.choice(string.ascii_letters)}{random.choice(string.ascii_letters)}"

    base64_part = base64.b64encode(random_str.encode()).decode()

    suffix = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(4))

    return f"M{hex_part}|{base64_part}{suffix}="

def get_qr_code():
    """获取微信二维码UUID"""
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
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            match = re.search(r'uuid\: *"(\w+)"', response.text)
            if match:
                return match.group(1)
    except Exception as e:
        print(f'获取二维码失败：{e}')
    return None

def check_scan_status(uuid_str):
    """检查二维码扫描状态"""
    url = f"https://long.open.weixin.qq.com/connect/l/qrconnect"
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
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
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

def get_token_by_code(code, device_id=None):
    """通过授权码获取Token（东方财富版本）"""
    if not device_id:
        device_id = generate_device_id()

    em_gt = 'ceab-' + ''.join(random.choice('0123456789abcdef') for _ in range(31))

    wechat_token_url = "https://awebapi2-account.eastmoney.com/core/api/ThirdParty/WeChatAccessToken"
    wechat_token_headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 15; 2210132C Build/AQ3A.240912.001)',
        'Host': 'awebapi2-account.eastmoney.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'
    }

    unique_id = generate_unique_id()

    wechat_token_data = {
        "AppId": APPID,
        "UniqueId": unique_id,
        "ProductType": "DFCFT",
        "Version": "10.28.1",
        "DeviceType": "Android15",
        "DomainName": "EastMoneyApp",
        "DeviceModel": "2210132C",
        "DeviceAlias": "",
        "AuthCode": code
    }

    try:
        wechat_token_response = requests.post(
            wechat_token_url,
            headers=wechat_token_headers,
            json=wechat_token_data
        )

        if wechat_token_response.status_code == 200:
            wechat_token_result = wechat_token_response.json()

            if wechat_token_result.get("ReturnCode") == "0":
                wechat_data = wechat_token_result.get("Data", {})
                access_token = wechat_data.get("Access_Token")
                union_id = wechat_data.get("UnionId")
                nick_name = wechat_data.get("NickName", "未知用户")

                dfcf_token_url = "https://awebapi2-account.eastmoney.com/core/api/ThirdParty/AppThirdpartyAccountLoginV2"
                dfcf_token_headers = {
                    'Accept': 'application/json',
                    'EM-OS': 'Android',
                    'EM-PKG': 'com.eastmoney.android.berlin',
                    'EM-VER': '10.28.1',
                    'qgqp-b-id': em_gt,
                    'EM-GT': em_gt,
                    'Content-Type': 'application/json',
                    'Host': 'awebapi2-account.eastmoney.com',
                    'Connection': 'Keep-Alive',
                    'Accept-Encoding': 'gzip',
                    'User-Agent': 'okhttp/3.12.13'
                }

                dfcf_token_data = {
                    "AppId": APPID,
                    "UniqueId": unique_id,
                    "ProductType": "DFCFT",
                    "Version": "10.28.1",
                    "DeviceType": "Android15",
                    "DomainName": "EastMoneyApp",
                    "DeviceModel": "2210132C",
                    "DeviceAlias": "",
                    "ScenarioId": "202004073458",
                    "ThirdAccountType": "500",
                    "OpenId": union_id,
                    "At": access_token,
                    "AppType": "cft",
                    "Alias": nick_name,
                    "WangZhengExtension": {
                        "PackageName": "com.eastmoney.android.berlin"
                    }
                }

                dfcf_token_response = requests.post(
                    dfcf_token_url,
                    headers=dfcf_token_headers,
                    json=dfcf_token_data
                )

                if dfcf_token_response.status_code == 200:
                    dfcf_token_result = dfcf_token_response.json()

                    info_service_result = send_info_service_request(em_gt)

                    save_user_info(
                        token_result={
                            "wechat_token": wechat_token_result,
                            "dfcf_token": dfcf_token_result,
                            "em_gt": em_gt,
                            "info_service": info_service_result
                        },
                        em_gt=em_gt,
                        device_id=device_id
                    )

                    return {
                        "wechat_token": wechat_token_result,
                        "dfcf_token": dfcf_token_result,
                        "em_gt": em_gt,
                        "info_service": info_service_result
                    }
                else:
                    sender.reply(f"获取东方财富Token失败: {dfcf_token_response.text}")
            else:
                sender.reply(f"获取微信AccessToken失败: {wechat_token_result.get('Msg')}")
        else:
            sender.reply(f"请求失败: {wechat_token_response.text}")
    except Exception as e:
        sender.reply(f"获取Token过程中出错: {str(e)}")

    return None

def scan_login():
    """微信扫码登录流程"""
    uuid_str = get_qr_code()
    if not uuid_str:
        sender.reply("❌ 获取登录二维码失败，请稍后再试")
        return False

    qr_url = f"https://open.weixin.qq.com/connect/qrcode/{uuid_str}"

    sender.reply("请使用微信扫描下方二维码登录")
    sender.replyImage(qr_url)
    sender.reply("扫码后请在微信中点击「确认登录」\n等待扫码中...\n回复'q'取消操作")

    retry_count = 0
    max_retries = 60  # 最多等待60秒

    while retry_count < max_retries:
        try:
            message = sender.listen(1000)  # 等待1秒
            if message and message.lower() == 'q':
                sender.reply("✅ 已取消扫码登录")
                return False
        except:
            pass

        result = check_scan_status(uuid_str)

        if isinstance(result, dict):
            if 'code' in result:
                code = result['code']
                nickname = result.get('nickname', '未知用户')
                sender.reply(f"✅ {nickname} 扫码成功，正在处理登录...")

                token_result = get_token_by_code(code)

                return token_result
            elif result.get('status') == 'waiting':
                pass
            elif result.get('status') == 'unknown':
                sender.reply("❌ 扫码出现未知状态，请重新尝试")
                return False
            elif result.get('status') == 'error':
                sender.reply("❌ 扫码出现错误，请重新尝试")
                return False

        retry_count += 1
        time.sleep(1)

    sender.reply("⚠️ 扫码超时，请重新尝试")
    return False

def generate_device_id():
    """生成随机的设备ID, 格式: 随机32位字符串||iemi_tluafed_me"""
    random_str = ''.join(random.choice('0123456789abcdef') for _ in range(32))
    return f"{random_str}||iemi_tluafed_me"

def md5_encrypt(text):
    """计算文本的MD5值"""
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def get_gtoken_from_api(uid):
    """从API获取gtoken
    Args:
        uid: 用户ID
    Returns:
        gtoken或None
    """
    try:
        admin_username = userid
        if not admin_username:
            print("未配置管理员用户名")
            return None

        url = "http://42.194.132.65:62173/get_dfcf_gtoken"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "user": admin_username,
            "uid": uid
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 0:
                gtoken = result.get("data", {}).get("gtoken")
                if gtoken == "limit":
                    sender.reply("❌ 该账号已达到gtoken使用上限")
                    return None

                used_count = result.get("data", {}).get("used_count", 0)
                limit = result.get("data", {}).get("limit", 0)
                sender.reply(f"✅ 成功从API获取gtoken: {gtoken[:8]}...\n已使用: {used_count}/{limit}")
                return gtoken
            else:
                print(f"获取gtoken失败: {result.get('message')}")
                return None
        else:
            print(f"请求失败: 状态码 {response.status_code}")
            return None
    except Exception as e:
        print(f"获取gtoken异常: {str(e)}")
        return None

def generate_random_code():
    """生成随机的randomCode，格式类似UUID"""
    return str(uuid.uuid4())

def get_timestamp():
    """获取当前时间戳（毫秒）"""
    return int(time.time() * 1000)

def send_info_service_request(em_gt=None):
    """发送信息服务请求
    Args:
        em_gt: EM-GT头部值，如果为None则随机生成
    Returns:
        响应内容
    """
    if not em_gt:
        em_gt = 'ceab-' + ''.join(random.choice('0123456789abcdef') for _ in range(32))

    device_id = generate_device_id()

    url = "https://emdcadvertise.eastmoney.com/infoService/v2"
    headers = {
        'Host': 'emdcadvertise.eastmoney.com',
        'em-os': 'Android',
        'em-pkg': 'com.eastmoney.android.berlin',
        'em-ver': '10.28.1',
        'em-gt': em_gt,
        'em-chl': 'xiaomi22_64',
        'em-gv': '3f4605b67',
        'em-sl': '0',
        'em-pa': '1',
        'em-dns': '1',
        'em-ab': 'R_1Lk;test_1LG;',
        'content-type': 'text/json; charset=utf-8',
        'accept-encoding': 'gzip',
        'user-agent': 'okhttp/3.12.13'
    }

    request_body = {
        "appKey": "cfw",
        "args": {
            "customerId": "",
            "fundLogin": False,
            "hkFundLogin": False,
            "line": 5,
            "pageId": "app_grzx",
            "positions": "",
            "switchMap": {"shilaohua": "0"},
            "uid": ""
        },
        "client": "android",
        "clientType": "cfw",
        "clientVersion": "10.28.1",
        "deviceId": device_id,
        "method": "marketad",
        "randomCode": generate_random_code(),
        "reserve": "",
        "timestamp": get_timestamp()
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=request_body
        )

        if response.status_code == 200:
            try:
                response_json = response.json()
                return response_json
            except:
                return response.text
        else:
            return None
    except Exception as e:
        print(f"发送请求出错: {str(e)}")
        return None

def save_user_info(token_result, em_gt, device_id):
    """保存用户信息到数据桶
    Args:
        token_result: 获取token的响应结果
        em_gt: EM-GT值
        device_id: 设备ID
    Returns:
        是否保存成功
    """
    try:
        if not token_result or "dfcf_token" not in token_result:
            sender.reply("❌ 无法保存用户信息，数据不完整")
            return False

        dfcf_data = token_result.get("dfcf_token", {}).get("Data", {})
        if not dfcf_data:
            sender.reply("❌ 无法获取用户Token数据")
            return False

        uid = dfcf_data.get("UID")
        c_token = dfcf_data.get("CToken")
        u_token = dfcf_data.get("UToken")
        f"ceab-{dfcf_data.get('CId')}"
        alias = dfcf_data.get("Alias", "未知用户")  # 用户昵称

        em_md = base64.b64encode(device_id.encode()).decode()

        if not uid:
            sender.reply("❌ 无法获取用户UID")
            return False

        api_gtoken = get_gtoken_from_api(uid)
        if not api_gtoken:
            sender.reply(f"⚠️ 从API获取gtoken失败，使用原始gtoken: {em_gt[:15]}...")

        token_data = {
            "UID": uid,
            "CToken": c_token,
            "UToken": u_token,
            "EM-MD": em_md,
            "GToken": api_gtoken or em_gt,  # 优先使用API获取的gtoken，失败则使用原始的
            "DeviceID": device_id,
            "Alias": alias,
            "UpdateTime": int(time.time())  # 保存更新时间
        }

        user_accounts = _sg_literal(sg.bucketGet(BUCKET_USER, userid) or '[]')

        if uid not in user_accounts:
            user_accounts.append(uid)
            sg.bucketSet(BUCKET_USER, userid, str(user_accounts))

        sg.bucketSet(BUCKET_TOKEN, uid, json.dumps(token_data, ensure_ascii=False))

        success_msg = f"""
=====登录成功=====
👤 用户: {alias}
📱 UID: {uid}
✅ 数据已保存
=================="""

        sender.reply(success_msg)

        auth_time = '2099-12-31' or ''
        current_date = datetime.now().strftime("%Y-%m-%d")
        if not auth_time or auth_time < current_date:
            process_auth(uid)
        else:
            _, _, _, ql_config, ql_envname, _ = get_config()
            if ql_config:
                ql_result, ql_message = add_to_qinglong(uid, token_data, ql_envname)
                if ql_result:
                    print(f"更新青龙变量成功: {uid}")
                else:
                    print(f"更新青龙变量失败: {ql_message}")

        return True

    except Exception as e:
        sender.reply(f"❌ 保存用户信息失败: {str(e)}")
        return False
def query_user_info(uid):
    """查询用户信息
    Args:
        uid: 用户UID
    Returns:
        查询结果
    """
    try:
        token_info_str = sg.bucketGet(BUCKET_TOKEN, uid)
        if not token_info_str:
            return f"❌ 未找到账号 {uid} 的Token信息"

        token_info = json.loads(token_info_str)
        c_token = token_info.get("CToken")
        u_token = token_info.get("UToken")
        g_token = token_info.get("GToken")
        em_md = token_info.get("EM-MD")
        alias = token_info.get("Alias", "未知用户")

        auth_time = '2099-12-31' or '未授权'

        if not all([c_token, u_token, g_token, em_md]):
            return f"❌ 账号 {uid} 的Token信息不完整"

        headers = {
            "Host": "empointcpf.eastmoney.com",
            "Connection": "keep-alive",
            "sec-ch-ua-platform": "\"Android\"",
            "CToken": c_token,
            "UToken": u_token,
            "sec-ch-ua": "\"Chromium\";v=\"142\", \"Android WebView\";v=\"142\", \"Not_A Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?1",
            "EM-OS": "Android",
            "EM-VER": "10.37.1",
            "User-Agent": "Mozilla/5.0 (Linux; Android 16; 2210132C Build/BP2A.250605.031.A3; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/142.0.7444.102 Mobile Safari/537.36;eastmoney_android;color=w;pkg=com.eastmoney.android.berlin;appver=10.37.1;tag=260491657;statusBarHeight=35.142857;titleBarHeight=45.142857;density=3.5;androidsdkversion=36;fontsize=2;listFontSize=1;adaptAgedSwitch=0",
            "Appkey": "EIBnBlYuvK",
            "EM-MD": em_md,
            "Accept": "*/*",
            "Origin": "https://vipmoney.eastmoney.com",
            "X-Requested-With": "com.eastmoney.android.berlin",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://vipmoney.eastmoney.com/",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }

        balance_url = "https://empointcpf.eastmoney.com/cashredpackets/Cash/balance?v=0723667712619922"
        response = requests.get(balance_url, headers=headers)

        if response.status_code != 200:
            return f"❌ 请求失败: 状态码 {response.status_code}"

        try:
            result = response.json()
            if result.get("result") != 1:
                return f"❌ 请求失败: {result.get('message', '未知错误')}"

            balance = result.get("data", 0)

            flows_url = "https://empointcpf.eastmoney.com/cashredpackets/cash/flows?pageIndex=1&pageSize=20"
            flows_response = requests.get(flows_url, headers=headers)

            flow_details = ""
            if flows_response.status_code == 200:
                flows_result = flows_response.json()
                if flows_result.get("result") == 1:
                    flows_data = flows_result.get("data", [])
                    for flow in flows_data[:5]:
                        amount = flow.get("Amount", 0)
                        flow_type = flow.get("FlowType", 1)
                        flow_time = flow.get("FlowTime", "")
                        if flow_type == 1:
                            flow_details += f"💵 +{amount:.2f} {flow_time}\n"
                        else:
                            flow_details += f"💸 -{amount:.2f} {flow_time}\n"

            query_msg = f"""=====账号信息=====
👤 用户: {alias}
📱 UID: {uid}
💰 余额: {balance}
📅 授权到期: {auth_time}
==================
{flow_details}=================="""
            return query_msg

        except json.JSONDecodeError:
            return f"❌ 解析响应失败: 响应不是有效的JSON格式"

    except Exception as e:
        return f"❌ 查询失败: {str(e)}"

def query_all_accounts():
    """查询用户所有绑定账号的信息"""
    try:
        user_accounts = _sg_literal(sg.bucketGet(BUCKET_USER, userid) or '[]')
        if not user_accounts:
            sender.reply("❌ 您还没有绑定东方财富账号")
            return

        for uid in user_accounts:
            result = query_user_info(uid)
            sender.reply(result)

    except Exception as e:
        sender.reply(f"❌ 查询失败: {str(e)}")

def manage_eastmoney():
    """东方财富账号管理"""
    try:
        accounts = _sg_literal(sg.bucketGet(BUCKET_USER, userid) or '[]')
        if not accounts:
            sender.reply("❌ 您还没有绑定东方财富账号")
            return

        manage_options = """
=====管理选项=====
[1] 账号授权
[2] 账号删除
------------------
回复数字选择操作
回复"q"退出"""

        sender.reply(manage_options)
        option = sender.listen(60000)

        if not option or option == 'q':
            sender.reply("✅ 已退出管理流程")
            return

        if option not in ['1', '2']:
            sender.reply("❌ 无效的选择")
            return

        account_list = "=====账号列表=====\n[0] 选择全部账号\n"
        for i, uid in enumerate(accounts, 1):
            token_info_str = sg.bucketGet(BUCKET_TOKEN, uid)
            if token_info_str:
                try:
                    token_info = json.loads(token_info_str)
                    alias = token_info.get("Alias", "未知用户")
                    auth_time = '2099-12-31' or '未授权'
                    account_list += f"[{i}] {alias} ({uid}) - {auth_time}\n"
                except:
                    account_list += f"[{i}] {uid} - 数据错误\n"
            else:
                account_list += f"[{i}] {uid} - 数据错误\n"

        manage_msg = f"""{account_list}
------------------
请选择要{option=='1'and'授权'or'删除'}的账号
可以输入多个账号序号，使用英文逗号分隔
例如: 1,3,5
回复"q"退出"""

        sender.reply(manage_msg)
        choice = sender.listen(60000)

        if not choice or choice == 'q':
            sender.reply("✅ 已退出管理流程")
            return

        selected_uids = []
        try:
            if choice == '0':
                selected_uids = accounts.copy()
            else:
                indices = [int(idx.strip()) - 1 for idx in choice.split(',')]
                for index in indices:
                    if 0 <= index < len(accounts):
                        selected_uids.append(accounts[index])
                    else:
                        sender.reply(f"❌ 无效的选择: {index + 1}")
                        return

            if not selected_uids:
                sender.reply("❌ 未选择任何账号")
                return
        except ValueError:
            sender.reply("❌ 无效的选择格式")
            return

        if option == '1':
            success_count = 0
            for selected_uid in selected_uids:
                auth_success = process_auth(selected_uid)

                if auth_success:
                    success_count += 1
                    token_info_str = sg.bucketGet(BUCKET_TOKEN, selected_uid)
                    if token_info_str:
                        token_info = json.loads(token_info_str)
                        _, _, _, ql_config, ql_envname, _ = get_config()
                        if ql_config:
                            add_to_qinglong(selected_uid, token_info, ql_envname)

            if len(selected_uids) > 1:
                sender.reply(f"✅ 授权完成，成功授权 {success_count}/{len(selected_uids)} 个账号")
        else:
            if len(selected_uids) == 1:
                selected_uid = selected_uids[0]
                token_info_str = sg.bucketGet(BUCKET_TOKEN, selected_uid)
                alias = "未知用户"
                if token_info_str:
                    try:
                        token_info = json.loads(token_info_str)
                        alias = token_info.get("Alias", "未知用户")
                    except:
                        pass

                confirm_msg = f"""=====删除确认=====
即将删除以下账号:
👤 用户: {alias}
📱 UID: {selected_uid}
------------------
⚠️ 数据无法恢复
回复"y"确认删除
"""

                sender.reply(confirm_msg)
                confirm = sender.listen(60000)

                if confirm.lower() != 'y':
                    sender.reply("✅ 已取消删除")
                    return

                try:
                    accounts.remove(selected_uid)
                    sg.bucketSet(BUCKET_TOKEN, selected_uid, '')
                    True

                    if accounts:
                        sg.bucketSet(BUCKET_USER, userid, str(accounts))
                    else:
                        sg.bucketDel(BUCKET_USER, userid)

                    _, _, _, ql_config, ql_envname, _ = get_config()
                    if ql_config:
                        delete_from_qinglong(selected_uid, ql_envname)

                    sender.reply(f"✅ 已成功删除账号: {alias} ({selected_uid})")
                except Exception as e:
                    sender.reply(f"❌ 删除失败: {str(e)}")
            else:
                account_info = ""
                for i, uid in enumerate(selected_uids, 1):
                    token_info_str = sg.bucketGet(BUCKET_TOKEN, uid)
                    alias = "未知用户"
                    if token_info_str:
                        try:
                            token_info = json.loads(token_info_str)
                            alias = token_info.get("Alias", "未知用户")
                        except:
                            pass
                    account_info += f"{i}. {alias} ({uid})\n"

                confirm_msg = f"""=====删除确认=====
即将删除以下 {len(selected_uids)} 个账号:
{account_info}
------------------
⚠️ 数据无法恢复
回复"y"确认删除
"""

                sender.reply(confirm_msg)
                confirm = sender.listen(60000)

                if confirm.lower() != 'y':
                    sender.reply("✅ 已取消删除")
                    return

                success_count = 0
                for selected_uid in selected_uids:
                    try:
                        accounts.remove(selected_uid)
                        sg.bucketSet(BUCKET_TOKEN, selected_uid, '')
                        True

                        _, _, _, ql_config, ql_envname, _ = get_config()
                        if ql_config:
                            delete_from_qinglong(selected_uid, ql_envname)

                        success_count += 1
                    except Exception as e:
                        print(f"删除账号 {selected_uid} 失败: {str(e)}")

                if accounts:
                    sg.bucketSet(BUCKET_USER, userid, str(accounts))
                else:
                    sg.bucketDel(BUCKET_USER, userid)

                sender.reply(f"✅ 删除完成，成功删除 {success_count}/{len(selected_uids)} 个账号")

    except Exception as e:
        sender.reply(f"❌ 管理失败: {str(e)}")

def calculate_auth_time_by_days(uid, days):
    return '2099-12-31'


def admin_auth_management():
    return True

def mask_uid(uid):
    """隐藏UID中间部分"""
    if not uid or len(uid) < 6:
        return uid
    return f"{uid[:3]}***{uid[-3:]}"


def get_ql_token(host, client_id, client_secret):
    """获取青龙面板的访问令牌"""
    try:
        url = f'{host}/open/auth/token?client_id={client_id}&client_secret={client_secret}'
        response = requests.get(url)
        data = response.json()
        if data.get('code') == 200:
            return data['data']['token']
        print(f"获取青龙token失败: {data}")
        return None
    except Exception as e:
        print(f"获取青龙token异常: {str(e)}")
        return None

def add_to_qinglong(uid, token_info, env_name="S_DFCF"):
    """添加东方财富账号到青龙"""
    try:
        _, _, _, ql_config, ql_envname, _ = get_config()

        if not ql_config:
            print("未配置青龙信息")
            return False, "未配置青龙信息"

        configs = ql_config.split('丨')
        if len(configs) < 3:
            configs = ql_config.split('|')
            if len(configs) < 3:
                print("青龙配置格式错误")
                return False, "青龙配置格式错误"

        host = configs[0].strip()
        client_id = configs[1].strip()
        client_secret = configs[2].strip()

        token = get_ql_token(host, client_id, client_secret)
        if not token:
            return False, "获取青龙token失败"

        headers = {'Authorization': f'Bearer {token}'}

        envs_response = requests.get(f'{host}/open/envs', headers=headers)
        if envs_response.status_code != 200:
            print(f"获取环境变量失败: {envs_response.text}")
            return False, "获取环境变量失败"

        envs = envs_response.json()['data']
        for env in envs:
            if env['name'] == env_name and uid in env['value']:
                env_id = env.get('_id') or env.get('id')
                if env_id:
                    delete_response = requests.delete(f'{host}/open/envs', headers=headers, json=[env_id])
                    if delete_response.status_code != 200:
                        print(f"删除旧变量失败: {delete_response.text}")
                break

        if isinstance(token_info, str):
            token_info = json.loads(token_info)

        uid = token_info.get("UID", "")
        c_token = token_info.get("CToken", "")
        u_token = token_info.get("UToken", "")
        g_token = token_info.get("GToken", "")
        em_md = token_info.get("EM-MD", "")
        device_id = token_info.get("DeviceID", "")
        alias = token_info.get("Alias", "未知用户")

        env_value = f"{uid}#{c_token}#{u_token}#{g_token}#{em_md}#{device_id}#{alias}"

        auth_time = '2099-12-31' or '未授权'

        data = [{
            'name': env_name,
            'value': env_value,
            'remarks': f"东方UID：{uid}|到期：{auth_time}"
        }]

        add_response = requests.post(f'{host}/open/envs', headers=headers, json=data)
        if add_response.status_code != 200:
            print(f"添加变量失败: {add_response.text}")
            return False, "添加变量失败"

        result = add_response.json()
        if result['code'] != 200:
            print(f"添加变量失败: {result}")
            return False, f"添加变量失败: {result.get('message')}"

        new_id = result['data'][0].get('_id') or result['data'][0].get('id')
        if new_id:
            enable_response = requests.put(f'{host}/open/envs/enable', headers=headers, json=[new_id])
            if enable_response.status_code != 200:
                print(f"启用变量失败: {enable_response.text}")

        return True, "添加青龙变量成功"

    except Exception as e:
        error_msg = f"添加青龙变量异常: {str(e)}"
        print(error_msg)
        return False, error_msg

def delete_from_qinglong(uid, env_name=None):
    """从青龙面板删除指定账号的变量"""
    try:
        _, _, _, ql_config, ql_envname, _ = get_config()

        if not env_name:
            env_name = ql_envname

        if not ql_config:
            print("未配置青龙信息")
            return False, "未配置青龙信息"

        configs = ql_config.split('丨')
        if len(configs) < 3:
            configs = ql_config.split('|')
            if len(configs) < 3:
                print("青龙配置格式错误")
                return False, "青龙配置格式错误"

        host = configs[0].strip()
        client_id = configs[1].strip()
        client_secret = configs[2].strip()

        token = get_ql_token(host, client_id, client_secret)
        if not token:
            return False, "获取青龙token失败"

        headers = {'Authorization': f'Bearer {token}'}

        envs_response = requests.get(f'{host}/open/envs', headers=headers)
        if envs_response.status_code != 200:
            print(f"获取环境变量失败: {envs_response.text}")
            return False, "获取环境变量失败"

        envs = envs_response.json()['data']
        deleted = False

        for env in envs:
            if env['name'] == env_name and uid in env['value']:
                env_id = env.get('_id') or env.get('id')
                if env_id:
                    delete_response = requests.delete(f'{host}/open/envs', headers=headers, json=[env_id])
                    if delete_response.status_code == 200:
                        deleted = True
                        print(f"删除青龙变量成功: {env_id}")
                    else:
                        print(f"删除青龙变量失败: {delete_response.text}")

        return deleted, "删除" + ("成功" if deleted else "失败")

    except Exception as e:
        error_msg = f"删除青龙变量异常: {str(e)}"
        print(error_msg)
        return False, error_msg

def account_login(account, password):
    """账号密码登录东方财富
    Args:
        account: 账号（手机号）
        password: 密码
    Returns:
        登录结果，成功返回True，失败返回False
    """
    try:
        device_id = generate_device_id()

        unique_id = generate_unique_id()

        em_gt = 'ceab-' + ''.join(random.choice('0123456789abcdef') for _ in range(31))

        base64.b64encode(device_id.encode()).decode()

        password_md5 = md5_encrypt(password)

        return account_login_with_verification(account, password_md5, unique_id, device_id, em_gt)
    except Exception as e:
        sender.reply(f"❌ 登录过程出错: {str(e)}")
        return False

def account_login_with_verification(account, password_md5, unique_id, device_id, em_gt, vcode="", vcode_context=""):
    """带验证码处理的账号密码登录流程
    Args:
        account: 账号
        password_md5: MD5加密后的密码
        unique_id: 唯一ID
        device_id: 设备ID
        em_gt: EM-GT值
        vcode: 图片验证码
        vcode_context: 验证码上下文
    Returns:
        登录结果
    """
    try:
        em_md = base64.b64encode(device_id.encode()).decode()

        url = "https://awebapi2-account.eastmoney.com/core/api/MPassport/LoginMobileV4"
        headers = {
            'Accept': 'application/json',
            'em-clt-uiid': unique_id,
            'em-clt-auth': '202107280688;qXU2bhqAdsux+eTFLOqWgXwz8GJyfhX/ejnm0eJ9aMc=',
            'qgqp-b-id': em_gt,
            'em_clt_uiid': unique_id,
            'qgqp_b_id': em_gt,
            'EM-OS': 'Android',
            'EM-PKG': 'com.eastmoney.android.berlin',
            'EM-VER': '10.28.1',
            'EM-GT': em_gt,
            'EM-MD': urllib.parse.quote(em_md),
            'EM-CHL': 'xiaomi22_64',
            'EM-GV': '3f4605b67',
            'EM-CT': '',
            'EM-UT': '',
            'EM-SL': '0',
            'EM-PA': '1',
            'em-dns': '1',
            'EM-AB': 'R_1Lk|1Ls;test_1LG;',
            'Content-Type': 'application/json',
            'Host': 'awebapi2-account.eastmoney.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.12.13'
        }

        request_body = {
            "AppId": "202107280688",
            "UniqueId": unique_id,
            "ProductType": "DFCFT",
            "Version": "10.28.1",
            "DeviceType": "Android15",
            "DomainName": "EastMoneyApp",
            "DeviceModel": "2210132C",
            "DeviceAlias": "",
            "ScenarioId": "202003257918",
            "Account": account,
            "Password": password_md5
        }

        if vcode:
            request_body["VCode"] = vcode
            request_body["VCodeContext"] = vcode_context if vcode_context else "EmPaVCodeCo"

        response = requests.post(url, headers=headers, json=request_body)

        if response.status_code == 200:
            login_result = response.json()

            return_code = login_result.get("ReturnCode")
            error_msg = login_result.get("Msg", "")

            if return_code == "0":
                user_data = login_result.get("Data", {})

                info_service_result = send_info_service_request(em_gt)

                token_result = {
                    "dfcf_token": {
                        "Data": {
                            "UID": user_data.get("UID"),
                            "CToken": user_data.get("CToken"),
                            "UToken": user_data.get("UToken"),
                            "Alias": user_data.get("Alias", "未知用户")
                        }
                    },
                    "em_gt": em_gt,
                    "info_service": info_service_result
                }

                save_success = save_user_info(token_result, em_gt, device_id)
                return save_success
            elif return_code == "42" or "验证码" in error_msg or "图片验证" in error_msg:

                vcode_result, em_pa_vcode_co = get_verify_code_image(account, device_id, em_gt)
                if not vcode_result:
                    sender.reply("❌ 获取图片验证码失败")
                    return False

                if isinstance(vcode_result, str) and vcode_result.startswith('http'):
                    sender.reply("验证码自动识别失败，请手动输入：")
                    sender.replyImage(vcode_result)
                    vcode_input = sender.listen(60000)
                    if not vcode_input or vcode_input == 'q':
                        sender.reply("✅ 已取消登录")
                        return False
                    vcode = vcode_input
                else:
                    vcode = vcode_result
                    sender.reply("验证码自动识别成功")

                return account_login_with_verification(
                    account, password_md5, unique_id, device_id, em_gt,
                    vcode=vcode, vcode_context=em_pa_vcode_co
                )
            elif return_code == "39":


                mobile_active_code_context = login_result.get("Data", {}).get("MobileActiveCodeContext")
                if not mobile_active_code_context:
                    mobile_active_code_context = login_result.get("Data", {}).get("ApiContext")

                if not mobile_active_code_context:
                    sender.reply("❌ 获取短信验证码上下文失败")
                    return False

                return login_with_sms_code(account, password_md5, mobile_active_code_context, unique_id, device_id, em_gt)
            else:
                sender.reply(f"❌ 登录失败: {error_msg}")
                return False
        else:
            sender.reply(f"❌ 请求失败: 状态码 {response.status_code}")
            return False
    except Exception as e:
        sender.reply(f"❌ 登录过程出错: {str(e)}")
        return False

def process_login():
    """处理登录流程"""
    login_options = """
=====登录方式=====
[1] 扫码登录
[2] 账号密码登录
------------------
请选择登录方式
回复"q"退出"""

    sender.reply(login_options)
    option = sender.listen(60000)

    if not option or option == 'q':
        sender.reply("✅ 已取消登录")
        return False

    if option == "1":
        return scan_login()
    elif option == "2":
        sender.reply("请输入账号（手机号）：")
        account = sender.listen(60000)

        if not account or account == 'q':
            sender.reply("✅ 已取消登录")
            return False

        sender.reply("请输入密码：")
        password = sender.listen(60000)

        if not password or password == 'q':
            sender.reply("✅ 已取消登录")
            return False

        return account_login(account, password)
    else:
        sender.reply("❌ 无效的选择")
        return False

def get_verify_code_image(account, device_id, em_gt):
    """获取图片验证码
    Args:
        account: 账号
        device_id: 设备ID
        em_gt: EM-GT值
    Returns:
        验证码图片临时文件路径和验证码cookie值
    """
    try:
        em_md = base64.b64encode(device_id.encode()).decode()
        em_md_encoded = urllib.parse.quote(em_md)

        generate_unique_id()

        rnd = str(int(time.time() * 1000))

        url = f"https://vcode2.eastmoney.com/V2/verifycode2.ashx"
        params = {
            "rnd": rnd,
            "vcodeTarget": account
        }

        headers = {
            'EM-OS': 'Android',
            'EM-PKG': 'com.eastmoney.android.berlin',
            'EM-VER': '10.28.1',
            'EM-GT': em_gt,
            'EM-MD': em_md_encoded,
            'EM-CHL': 'xiaomi22_64',
            'EM-GV': '3f4605b67',
            'EM-CT': '',
            'EM-UT': '',
            'EM-SL': '0',
            'EM-PA': '1',
            'em-dns': '1',
            'EM-AB': 'R_1Lk|1Ls;test_1LG;',
            'Host': 'vcode2.eastmoney.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.12.13'
        }

        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            em_pa_vcode_co = None
            for cookie in response.cookies:
                if cookie.name == "EmPaVCodeCo":
                    em_pa_vcode_co = cookie.value
                    break

            if not em_pa_vcode_co and 'Set-Cookie' in response.headers:
                cookie_header = response.headers.get('Set-Cookie', '')
                match = re.search(r'EmPaVCodeCo=([^;]+)', cookie_header)
                if match:
                    em_pa_vcode_co = match.group(1)

            if not em_pa_vcode_co:
                em_pa_vcode_co = "EmPaVCodeCo"

            image_base64 = base64.b64encode(response.content).decode('utf-8')

            _, _, _, _, _, captcha_api = get_config()

            if captcha_api:
                try:
                    data = {
                        "image": image_base64,
                        "probability": False,
                        "png_fix": False
                    }

                    api_response = requests.post(captcha_api, data=data)

                    result = api_response.json()
                    if result.get("code") == 200:
                        vcode = result.get("data")
                        if vcode:
                            return vcode, em_pa_vcode_co
                except Exception as e:
                    print(f"API识别验证码异常: {str(e)}")

            try:
                upload_url = "https://uapis.cn/api/baseimg.php"
                upload_data = {
                    "imageData": image_base64
                }

                upload_response = requests.post(upload_url, data=upload_data)
                result = upload_response.json()

                if result.get("code") == 200 and result.get("img"):
                    return None, em_pa_vcode_co
            except Exception as e:
                print(f"上传图片获取链接异常: {str(e)}")
            return None, em_pa_vcode_co

        return None, None
    except Exception as e:
        print(f"获取验证码异常: {str(e)}")
        return None, None

def login_with_sms_code(account, password, api_context, unique_id, device_id, em_gt):
    """使用短信验证码完成登录流程
    Args:
        account: 账号
        password: MD5加密后的密码
        api_context: 短信验证码API上下文
        unique_id: 唯一ID
        device_id: 设备ID
        em_gt: EM-GT值
    Returns:
        登录结果
    """
    try:
        sender.reply("请输入收到的短信验证码：")
        sms_code = sender.listen(180000)  # 等待3分钟

        if not sms_code or sms_code.lower() == 'q':
            sender.reply("✅ 已取消登录")
            return False

        em_md = base64.b64encode(device_id.encode()).decode()

        url = "https://awebapi2-account.eastmoney.com/core/api/MPassport/LoginByActiveCodeV4"
        headers = {
            'Accept': 'application/json',
            'em-clt-uiid': unique_id,
            'em-clt-auth': '202107280688;qXU2bhqAdsux+eTFLOqWgXwz8GJyfhX/ejnm0eJ9aMc=',
            'qgqp-b-id': em_gt,
            'em_clt_uiid': unique_id,
            'qgqp_b_id': em_gt,
            'EM-OS': 'Android',
            'EM-PKG': 'com.eastmoney.android.berlin',
            'EM-VER': '10.28.1',
            'EM-GT': em_gt,
            'EM-MD': urllib.parse.quote(em_md),
            'EM-CHL': 'xiaomi22_64',
            'EM-GV': '3f4605b67',
            'EM-CT': '',
            'EM-UT': '',
            'EM-SL': '0',
            'EM-PA': '1',
            'em-dns': '1',
            'EM-AB': 'R_1Lk|1Ls;test_1LG;',
            'Content-Type': 'application/json',
            'Host': 'awebapi2-account.eastmoney.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.12.13'
        }

        request_body = {
            "AppId": "202107280688",
            "UniqueId": unique_id,
            "ProductType": "DFCFT",
            "Version": "10.28.1",
            "DeviceType": "Android15",
            "DomainName": "EastMoneyApp",
            "DeviceModel": "2210132C",
            "DeviceAlias": "",
            "ScenarioId": "202003257918",
            "ActiveCode": sms_code,
            "MobileActiveCodeContext": api_context
        }

        response = requests.post(url, headers=headers, json=request_body)

        if response.status_code == 200:
            login_result = response.json()

            if login_result.get("ReturnCode") == "0":
                user_data = login_result.get("Data", {})

                info_service_result = send_info_service_request(em_gt)

                token_result = {
                    "dfcf_token": {
                        "Data": {
                            "UID": user_data.get("UID"),
                            "CToken": user_data.get("CToken"),
                            "UToken": user_data.get("UToken"),
                            "Alias": user_data.get("Alias", "未知用户")
                        }
                    },
                    "em_gt": em_gt,
                    "info_service": info_service_result
                }

                save_success = save_user_info(token_result, em_gt, device_id)
                return save_success
            else:
                error_msg = login_result.get("Msg", "未知错误")
                sender.reply(f"❌ 短信验证码登录失败: {error_msg}")
                return False
        else:
            sender.reply(f"❌ 请求失败: 状态码 {response.status_code}")
            return False
    except Exception as e:
        sender.reply(f"❌ 短信验证码登录过程出错: {str(e)}")
        return False


def recognize_captcha(base64_image, api_url=None):
    """识别验证码
    Args:
        base64_image: base64编码的图片数据
        api_url: 验证码识别API地址
    Returns:
        识别结果或图片链接
    """
    try:
        if api_url:
            data = {
                "image": base64_image,
                "probability": False,
                "png_fix": False
            }

            response = requests.post(api_url, data=data)

            result = response.json()
            if result.get("code") == 200:
                return result.get("data")

        upload_url = "https://uapis.cn/api/baseimg.php"
        upload_data = {
            "imageData": base64_image
        }

        response = requests.post(upload_url, data=upload_data)
        result = response.json()

        if result.get("code") == 200 and result.get("img"):
            return result.get("img")

        return None
    except Exception as e:
        print(f"识别验证码异常: {str(e)}")
        return None

def show_tutorial():
    """显示东方财富插件使用教程"""
    tutorial = """=====东方教程=====
📱 用户指令:
• 东方登录 - 绑定东方财富账号
• 东方查询 - 查询账号余额和状态
• 东方管理 - 授权/删除账号
• 东方教程 - 查看本教程
------------------
🔧 管理员指令:
• 东方授权 - 管理员按天数授权
• 东方检测 - 检测过期账号并清理
------------------
💡 登录方式:
📝 方式一: 微信扫码登录
📝 方式二: 账号密码登录
💡 登录后自动进入授权流程
------------------
📝 账号获取方式:
1. 下载东方财富APP注册账号
2. 使用手机号注册并设置密码
3. 完成实名认证
4. 进入活动页面一次激活账号
------------------
💰 功能说明:
• 账号绑定: 保存账号信息到系统
• 余额查询: 查看现金余额和明细
• 授权管理: 付费使用插件功能
• 青龙提交: 自动提交到青龙容器
• 过期检测: 自动清理过期账号
------------------
🎯 使用流程:
1. 发送"东方登录"绑定账号
2. 选择扫码或账号密码登录
3. 登录成功后选择授权方式
4. 完成支付获得使用权限
5. 系统自动提交到青龙容器
6. 等待定时任务自动执行
------------------
⚠️ 注意事项:
• 授权后才能使用签到功能
• 过期账号会被自动清理
• 支持微信支付和积分兑换
• 管理员可批量授权用户
• 每日收益约1.5元(需实名)
=================="""
    sender.reply(tutorial)

def main():
    message = sender.getMessage()

    if "东方登录" in message or "登录东方" in message:
        process_login()
    elif "东方查询" in message:
        query_all_accounts()
    elif "东方管理" in message:
        manage_eastmoney()
    elif "东方授权" in message:
        if sender.isAdmin():
            admin_auth_management()
    elif "东方提现" in message:
        sender.reply("东方财富提现功能待实现")
    elif "东方检测" in message:
        if not sender.isAdmin():
            sender.reply("❌ 仅限管理员")
            return
        sender.reply("🔍 正在检测...")
        sender.reply(check_auth_status())
    elif "东方教程" in message:
        show_tutorial()
    elif sender.getImtype() == 'fake':
        try:
            sg.notifyMasters(check_auth_status())
        except:
            pass

if __name__ == "__main__":
    main()
