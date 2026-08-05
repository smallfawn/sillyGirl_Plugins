# [title: 星芽短剧]
# [name: xingYaDuanJu]
# [language: python]
# [class: 任务]
# [author: mrconli]
# [version: v2.7.0]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^星芽(.*)|(.*)星芽$]
# [cron: 6 6,18 * * *]
# [icon: https://api.iconify.design/lucide:bot.svg]
# [description: 仅环境变量提交青龙；2.7.0更新:新增token自动续期支持，token有效1月，可自定义是否开启，若开启，需要重新登录一次；2.5.0更新:修复短信登录的一个bug报错；2.4.0更新：优化ck失效查询信息；2.3.0更新：优化登录逻辑，增加管理员同步青龙；2.2.0更新：增加提交青龙环境变量是否携带设备id配参，修复查询ck失效即终止查询的bug；2.1.6更新：调整查询逻辑，只有一个账号时直接查询，否则列表选择查询；2.1.5更新：增加查询时显示账号列表，查询指定账号]
# [depe: ["pycryptodome", "requests", "urllib3"]]


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
    'mrconli_xydj_ql_config': form.string().title('对接青龙').default('').description('|'),
    'mrconli_xydj_var_name': form.string().title('环境变量名').default('').description('青龙容器内的变量名，默认为：Xydj'),
    'mrconli_xydj_is_proxy': form.boolean().title('是否启用代理').default(False).description('开启代理就勾选，其实不需要代理'),
    'mrconli_xydj_proxy_pool': form.string().title('代理池地址').default('').description('代理API服务地址'),
    'mrconli_xydj_is_xuqi': form.boolean().title('是否开启token续期').default(False).description('默认关闭'),
    'mrconli_xydj_weekdays': form.string().title('续期运行时间').default('').description('0,1,2,3,4,5,6对应周一到周日,默认在18:00以后的定时运行'),
})
_CONFIG_FIELD_MAP = {
    ('mrconli', 'xydj.ql_config'): 'mrconli_xydj_ql_config',
    ('mrconli', 'xydj.var_name'): 'mrconli_xydj_var_name',
    ('mrconli', 'xydj.is_proxy'): 'mrconli_xydj_is_proxy',
    ('mrconli', 'xydj.proxy_pool'): 'mrconli_xydj_proxy_pool',
    ('mrconli', 'xydj.is_xuqi'): 'mrconli_xydj_is_xuqi',
    ('mrconli', 'xydj.weekdays'): 'mrconli_xydj_weekdays',
}

from datetime import datetime, timedelta  # 操作日期、时间以及时间间隔
import urllib3
from decimal import Decimal  # 处理浮点数
import requests  # 处理http请求
import time  # 处理时间
import json  # 处理json数据
import re
from datetime import datetime, timedelta
import json
import hashlib
import uuid
import string
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64


urllib3.disable_warnings()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

senderID = sg.getSenderID()  # 获取发送者QQ号
sender = sg.Sender(senderID)  # 获取发送者对象
userid = sender.getUserID()  # 存储当前发送者的用户 ID，与 senderID 类似，但通常用于内部标识
uservalue = sg.bucketGet(bucket='mrconli.xydj.user', key=userid)
today_date = datetime.now().date()
today_time = str(today_date)
number = int(sg.bucketGet('mrconli.xydj', 'number') or 5)
weekdays = sg.bucketGet('mrconli.xydj', 'weekdays') or "0,1,2,3,4,5,6"


MAX_RETRIES = 10  # 最大重试次数
IS_PROXY = sg.bucketGet('mrconli.xydj', 'is_proxy') or "false"  # 是否启用代理true
PROXY_API = sg.bucketGet('mrconli.xydj', 'proxy_pool') or "http://10.10.10.251:12306/help/proxy/original"
proxy = None  # 初始化全局代理变量


def update_proxy():
    """更新代理IP地址"""
    global proxy
    try:
        if not IS_PROXY or IS_PROXY == "false":
            proxy = None
            return
        response = requests.get(PROXY_API, timeout=10)
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
    """带代理重试的请求方法"""
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
    """手机号脱敏处理"""
    if not phone or len(phone) != 11:
        return phone
    return f"{phone[:3]}****{phone[7:]}"


def update_proxy():
    """更新代理 IP 地址"""
    global proxy
    try:
        if not IS_PROXY:
            proxy = None
            return
        response = requests.get(PROXY_API, timeout=10)
        ip = response.text.strip()
        if "请先添加白名单" in ip:
            raise ValueError("请配置代理白名单")
        proxy = {
            'http': ip,
            'https': ip,
        }
        print(f"✅ 代理获取成功: {ip}")
    except Exception as e:
        print(f"❌ 代理获取失败: {str(e)}")
        proxy = None


def _send_request(method, url, **kwargs):
    """带代理重试的请求方法"""
    global proxy
    attempts = 0
    while attempts < MAX_RETRIES:
        try:
            if IS_PROXY and proxy is None:
                update_proxy()
            kwargs['timeout'] = kwargs.get('timeout', 15)  # 默认超时时间 15 秒
            response = requests.request(
                method=method,
                url=url,
                proxies=proxy if IS_PROXY and proxy else None,
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

def getoaid():
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    return random_string.lower()

def generate_android_id():
    """随机生成一个Android ID (16位十六进制字符串)"""
    return ''.join(random.choice(string.hexdigits.lower()) for _ in range(16))

def android_id_to_device_id(android_id):
    """将Android ID转换为设备ID"""
    if not android_id or android_id == "9774d56d68369ce":
        return "9" + str(uuid.uuid4()).replace("-", "")
    else:
        return "2" + str(uuid.uuid5(uuid.NAMESPACE_DNS, android_id)).replace("-", "")

def getdid():
    '''
    随机生成安卓id并生成did
    :return: android_id, device_id
    '''
    android_id = generate_android_id()
    device_id = android_id_to_device_id(android_id)
    return android_id, device_id


def header():
    def getdevtoken():
        return hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()[:8]

    oaid, device_id = getdid()
    auth_token = getdefaultToken(oaid, device_id)

    headers = {
            'X-App-Id': '7',
            'Authorization': '',
            'platform': '1',
            'manufacturer': 'Xiaomi',
            'version_name': '3.8.6',
            'user_agent': 'Mozilla/5.0 (Linux; Android 15; 24018RPACC Build/AQ3A.240627.003; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/130.0.6723.86 Safari/537.36',
            'app_version': '3.8.6',
            'device_platform': 'android',
            'personalized_recommend_status': '1',
            'device_type': '24018RPACC',
            'device_brand': 'Xiaomi',
            'os_version': '15',
            'channel': 'default',
            'raw_channel': 'default',
            "dev_token": f'{getdevtoken()}',  # 使用本地定义的函数
            'oaid': oaid,
            'msa_oaid': oaid,
            'uuid': f"randomUUID_{uuid.uuid4()}",
            'device_id': device_id,
            'ab_id': '',
            'support_h265': '1',
            'font_scale': '1.0',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/4.10.0',
            'authorization': auth_token,
            'content-type': "application/json; charset=UTF-8"
        }


    return headers

def aes_encrypt(plaintext: str) -> str:
    """AES加密"""
    key = 'B@ecf920Od8A4df7'.encode('utf-8')
    cipher = AES.new(key, AES.MODE_ECB)
    padded_plaintext = pad(plaintext.encode('utf-8'), AES.block_size)
    return base64.b64encode(cipher.encrypt(padded_plaintext)).decode('utf-8')

def getdefaultToken(android_id, device_id):
    """获取初始设备token"""
    timestamp = int(time.time() * 1000)
    data = {
        "device": device_id,
        "android_id": android_id,
        "first_install_time": timestamp - 3600000,
        "last_update_time": timestamp - 3600000,
        "timestamp": timestamp
    }


    encrypted = aes_encrypt(json.dumps(data))

    headers = {
        'X-App-Id': '7',
        'platform': '1',
        'user_agent': 'Mozilla/5.0 (Linux; Android 15; 23127PN0CC Build/AQ3A.240627.003; wv)',
        'Content-Type': 'application/json; charset=utf-8',
        'device_id': device_id,
        'User-Agent': 'okhttp/4.10.0'
    }
    try:
        response = _send_request('POST',
            "https://u.shytkjgs.com/user/v3/account/login",
            headers=headers,
            data=encrypted
        )
        token = response.json().get('data', {}).get('token')
        return token
    except Exception as e:
        print(f"获取初始token失败: {e}")
    return False

def batch_login():
    sender.reply("CK批量登录暂不可用，请使用短信验证码登录")
    return None

def bind():
    """选择登录方式"""
    sender.reply(
        "=====星芽登录=====\n"
        "1. 短信验证码登录\n"
        "2. ck登录（可批量）\n"
        "=====================\n"
        "📝 请输入数字选择登录方式\n"
        "⭐ 输入q退出操作\n"
    )
    choice = sender.input(60000, 1, False)
    if choice == 'q' or choice == 'Q':
        sender.reply('❌ 已退出登录操作')
        return
    if not choice:
        sender.reply('❌ 输入超时！')
        return
    if choice == '1':
        sms_login()
    elif choice == '2':
        batch_login()

def sms_send():
    """短信登录实现"""
    update_proxy()
    try:
        headers = header()
        sender.reply('📝 请输入星芽手机号:')
        phone = sender.input(120000, 1, False)
        if phone == 'q' or phone == 'Q':
            sender.reply("❌ 退出！")
            return
        if phone is None:
            sender.reply("❌ 超时退出！")
            return
        if not re.match(r'^1[3-9]\d{9}$', phone):
            sender.reply("❌ 请输入有效的手机号")
            sms_send()

        url = "https://u.shytkjgs.com/user/v1/sms/code"
        response = _send_request('POST',
            url,
            data=json.dumps({"mobile": phone}),
            headers=headers,
            timeout=10
        )
        res_data = response.json()

        if res_data.get('code') != 'ok':
            sender.reply(f"❌ 验证码发送失败: {res_data.get('msg', '未知错误')}")
            return

        sender.reply('📝 请输入4位验证码（2分钟内有效）:')
        message = sender.input(120000, 1, False)
        if len(message) != 4 or not message.isdigit():
            sender.reply("❌ 登录失败，请输入有效的4位数字验证码")
            return

        login_url = "https://u.shytkjgs.com/user/v1/account/sms/login"
        login_response = _send_request('POST',
            login_url,
            json={"mobile": phone, "code": message},
            headers=headers,
            timeout=10
        )

        login_data = login_response.json()

        if login_data.get('code') != 'ok':
            sender.reply(f"❌ 登录失败: {login_data.get('msg', '未知错误')}")
            return None, None, None, None, None

        token = login_data['data']['token']
        oaid = headers['oaid']
        device_id = headers['device_id']
        uuid = headers['uuid']
        phone = str(phone)
        return phone, token, uuid, oaid, device_id
    except Exception as e:
        sender.reply(f"⚠️ 发生未知错误: {str(e)}")
        return None, None, None, None, None


def get_info(token_info):
    try:
        authorization, device_id = token_info.split('#')
        headers = {
            "Authorization": authorization.strip(),
            "device_id": device_id.strip()
        }
        url = "https://u.shytkjgs.com/user/v1/account/detail"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"网络请求失败: 状态码 {response.status_code}")

        data = response.json()
        if data.get('code') != 'ok':
            raise Exception(f"API返回错误: {data.get('msg', '未知错误')}")
        user_id = data['data'].get('user_id')   # 用户id
        cash_remain = data['data'].get('cash_remain', '0')   # 余额
        species = data['data'].get('species', '0')  # 金币
        return user_id, cash_remain, species
    except Exception as e:
        print(f"⚠️ 发生未知错误: {str(e)}")
        return None, None, None

def add_viewing_duration(user_id, token, duration):
    """增加观看时长"""
    try:
        authorization, device_id = token.split('#')
        random_uuid = uuid.uuid4()
        if not authorization or not device_id:
            return False, "账号信息不完整，请重新登录！"
        headers = {
            "x-app-id": "7",
            "authorization": authorization,
            "platform": "1",
            "manufacturer": "Xiaomi",
            "version_name": "3.8.3.1",
            "user_agent": "Mozilla/5.0 (Linux; Android 15; 2210132C Build/AQ3A.240812.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/131.0.6778.260 Mobile Safari/537.36",
            "app_version": "3.8.3.1",
            "device_platform": "android",
            "personalized_recommend_status": "1",
            "device_type": "2210132C",
            "device_brand": "Xiaomi",
            "os_version": "15",
            "channel": "default",
            "raw_channel": "default",
            "uuid": f"randomUUID_{random_uuid}",
            "device_id": device_id,
            "ab_id": "",
            "support_h265": "1",
            "font_scale": "1.0",
            "content-type": "application/json; charset=utf-8"
        }
        current_timestamp = int(time.time() * 1000)

        request_body = [
            {
                "event_id": "action_episode_view",
                "page_id": "page_drama_detail",
                "eventType": "action",
                "event_type": "action",
                "timestamp": current_timestamp,
                "user_id": str(user_id),
                "login_status": True,
                "retry": 0,
                "device_id": device_id,
                "device_type": "Xiaomi",
                "phone_version": "2210132C",
                "os_type": 1,
                "os_name": "15",
                "version": "3.8.3.1",
                "package_name": "com.jz.xydj",
                "app_id": "7",
                "channel": "default",
                "raw_channel": "default",
                "font_scale": 1.0,
                "define_args": json.dumps({
                    "page": "page_drama_detail",
                    "theater_id": "4328",
                    "theater_number": "1",
                    "theater_duration": str(duration),
                    "lock": "0",
                    "complete": "0",
                    "show_id": "7de1f4a3cfb04c93bb31c11f7e896ad8",
                    "classification_id": "0",
                    "position": "4",
                    "entrance_scene": "0",
                    "entrance": "5",
                    "top_classification_id": "1",
                    "top_classification_name": "剧场",
                    "ab_id": "",
                    "last_page": "page_drama_detail"
                })
            }
        ]
        response = requests.post(
            "https://xingya-track.shytkjgs.com/receive",
            headers=headers,
            json=request_body,
            timeout=10
        )
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == "ok":
                return True, f"成功增加 {duration} 秒观看时长！"
            else:
                return False, f"{result.get('msg', '未知错误')}"
        else:
            return False, f"请求失败，状态码: {response.status_code}"
    except Exception as e:
        return False, f"增加观看时长异常: {str(e)}"


def update_token(uuid, oaid, device_id, auth):
    headers = {
        'X-App-Id': '7',
        'platform': '1',
        'manufacturer': 'Xiaomi',
        'version_name': '3.8.6',
        'user_agent': 'Mozilla/5.0 (Linux; Android 15; 23127PN0CC Build/AQ3A.240627.003; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/130.0.6723.86 Mobile Safari/537.36',
        'app_version': '3.8.6', 'device_platform': 'android',
        'personalized_recommend_status': '1',
        'device_type': '23127PN0CC',
        'device_brand': 'Xiaomi', 'os_version': '15', 'channel': 'default',
        'raw_channel': 'default',
        'uuid': uuid,
        'device_id': device_id,
        'ab_id': '',
        'support_h265': '1',
        'font_scale': '1.0',
        'Content-Type': 'application/json; charset=utf-8',
        'Content-Length': '738',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/4.10.0'}

    timestemp = int(time.time()*1000)


    data = {
        "device":device_id,
        "android_id":oaid,
        "install_first_open":False,
        "first_install_time":1748882426598,
        "last_update_time":1748882426598,
        "report_link_url":"",
        "authorization":auth,
        "timestamp":timestemp
    }
    encrypted = aes_encrypt(json.dumps(data))
    response0 = _send_request('POST', "https://u.shytkjgs.com/user/v3/account/login", headers=headers, data=encrypted)
    c = response0.json()


    if c['code']=='ok':
        new_authorization = c['data']['token']
        new_token = f"{new_authorization}#{device_id}"
        return new_token
    else:
        return None


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
            sg.bucketSet('mrconli.xydj.user', userid, json.dumps(accounts))
        else:
            dlzt = "更新"
            if not auth or auth < today_time:
                sender.reply(f"⚠️ 账号未授权或授权已过期，环境变量未提交青龙...")
            else:
                add_to_qinglong(token, account, userid)
        sg.bucketSet('mrconli.xydj.token', account, token)
        sg.bucketSet('mrconli.xydj.oaid', account, oaid)
        sg.bucketSet('mrconli.xydj.uuid', account, uuid)
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


def query():
    accounts = _sg_literal(uservalue or '[]')
    if not accounts:
        sender.reply(
            '\n=====星芽账号查询=====\n❌ 未找到任何账号\n------------------\n💡 发送"星芽登录"绑定账号\n===================')
        return
    if len(accounts) > 1:
        menu = "=====请选择查询账号=====\n[0] 查询全部账号\n------------------\n"
        for idx, acc in enumerate(accounts, 1):
            menu += f"[{idx}] {acc[:3]}****{acc[-4:]}\n"
        menu += "=======================\n⚠️ 请回复数字序号(输入q退出)"
        sender.reply(menu)

        choice = sender.input(30000, 1, False)
        if choice.lower() == 'q':
            sender.reply('已取消查询')
            return
        if not choice.isdigit():
            sender.reply('输入格式错误，请回复数字')
            return

        choice = int(choice)
        if choice < 0 or choice > len(accounts):
            sender.reply('选择超出范围，已取消查询')
            return
    else:
        choice = 1  # 单个账号直接查询

    if choice == 0:
        target_accounts = accounts
        sender.reply('正在查询全部账号...')
    else:
        target_accounts = [accounts[choice - 1]]
        sender.reply('正在查询星芽，请耐心等待...')

    for account in target_accounts:
        try:
            auth = '2099-12-31'
            token = sg.bucketGet('mrconli.xydj.token', account)
            if not token:
                sender.reply(f'【{mask_phone(account)}】token获取失败')
                continue
            if not auth:
                sender.reply(f'【{mask_phone(account)}】账号未授权')
            elif auth < today_time:
                sender.reply(f'【{mask_phone(account)}】云授权过期')
            else:
                user_id, cash_remain, species = get_info(token)
                if species is None:
                    sender.reply(f'【{mask_phone(account)}】ck失效，请重新登录更新...')
                    continue
                sender.reply(f"""
=====星芽账号详情=====
📱 账号：{mask_phone(account)}
👤 ID: {user_id}
🎯 今日金币：{species}
💰 账户余额：{cash_remain} 元
⏰ 授权到期：{auth}
==================""")
        except Exception as e:
            sender.reply(f'❌ 【{mask_phone(account)}】查询出错: {str(e)}')


def add_view_time():
    sender.reply("""
=====设置刷新时长=====
📝 请输入需要增加的观看时长(秒)：
例如: 3600 (代表1小时)
------------------
回复"q"退出操作
==================""")
    duration_input = sender.input(120000, 1, False)
    if not duration_input:
        sender.reply("❌ 输入超时！")
        return
    if duration_input.lower() == 'q':
        sender.reply("❌ 已退出操作")
        return
    duration = int(duration_input)
    if duration <= 0:
        sender.reply("❌ 时长必须大于0")
        return
    accounts = _sg_literal(uservalue or '[]')
    if not accounts:
        sender.reply(
            '\n=====星芽时长刷新=====\n❌ 未找到任何账号\n------------------\n💡 发送"星芽登录"绑定账号\n===================')
        return
    if len(accounts) > 1:
        menu = "====请选择时长刷新账号====\n[0] 刷新全部账号\n------------------\n"
        for idx, acc in enumerate(accounts, 1):
            menu += f"[{idx}] {acc[:3]}****{acc[-4:]}\n"
        menu += "=======================\n⚠️ 请回复数字序号(输入q退出)"
        sender.reply(menu)

        choice = sender.input(30000, 1, False)
        if choice.lower() == 'q':
            sender.reply('已取消查询')
            return
        if not choice.isdigit():
            sender.reply('输入格式错误，请回复数字')
            return

        choice = int(choice)
        if choice < 0 or choice > len(accounts):
            sender.reply('选择超出范围，已取消查询')
            return
    else:
        choice = 1  # 单个账号直接查询

    if choice == 0:
        target_accounts = accounts
        sender.reply('正在刷新全部账号时长...')
    else:
        target_accounts = [accounts[choice - 1]]
        sender.reply('正在刷新时长，请耐心等待...')

    for account in target_accounts:
        try:
            auth = '2099-12-31'
            token = sg.bucketGet('mrconli.xydj.token', account)
            if not token:
                sender.reply(f'【{mask_phone(account)}】token获取失败')
                continue
            if not auth:
                sender.reply(f'【{mask_phone(account)}】账号未授权')
            elif auth < today_time:
                sender.reply(f'【{mask_phone(account)}】云授权过期')
            else:
                user_id, cash_remain, species = get_info(token)
                if not user_id or user_id == None:
                    sender.reply(f'【{mask_phone(account)}】ck失效，请重新登录更新！')
                    continue
                success, message = add_viewing_duration(user_id, token, duration)
                if success:
                    sender.reply(f'✅ 【{mask_phone(account)}】时长刷新成功: {message}')
                else:
                    sender.reply(f'❌ 【{mask_phone(account)}】时长刷新失败: {message}')
        except Exception as e:
            sender.reply(f'❌ 【{mask_phone(account)}】时长刷新出错: {str(e)}')


def get_config():
    """获取插件配置"""
    try:
        sg.bucketGet('mrconli.xydj', 'coin_bucket') or 'dd_sign_points'
        var_name = sg.bucketGet('mrconli.xydj', 'var_name') or "Xydj"
        if not var_name:
            print("未配置变量名，使用默认值: Xydj")
            var_name = 'Xydj'
            sg.bucketSet('mrconli.xydj', 'var_name', var_name)
        ql_config = sg.bucketGet('mrconli.xydj', 'ql_config')
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
        manage_cmd = sg.bucketGet('mrconli.xydj', 'manage_cmd') or '星芽管理'
        query_cmd = sg.bucketGet('mrconli.xydj', 'query_cmd') or '星芽查询'
        login_cmd = sg.bucketGet('mrconli.xydj', 'login_cmd') or '星芽登录'
        try:
            price = Decimal(sg.bucketGet('mrconli.xydj', 'price') or '1')
            if price < 0:
                raise ValueError("价格不能为负数")
        except (ValueError, decimal.InvalidOperation):
            print("价格配置无效，使用默认值: 1")
            price = Decimal('1')
            sg.bucketSet('mrconli.xydj', 'price', '1')
        try:
            coin_price = int(sg.bucketGet('mrconli.xydj', 'coin') or '0')
            if coin_price < 0:
                raise ValueError("积分不能为负数")
        except ValueError:
            print("积分配置无效，使用默认值: 0")
            coin_price = 0
            sg.bucketSet('mrconli.xydj', 'coin', '0')
        try:
            show_records = int(sg.bucketGet('mrconli.xydj', 'show_records') or '3')
            if show_records < 1:
                raise ValueError("显示记录数不能小于1")
        except ValueError:
            print("显示记录数配置无效，使用默认值: 3")
            show_records = 3
            sg.bucketSet('mrconli.xydj', 'show_records', '3')
        return (var_name, ql_host, ql_client_id, ql_client_secret, manage_cmd, query_cmd, login_cmd, price, coin_price,
                show_records, show_records)
    except Exception as e:
        error_msg = f"获取配置失败: {str(e)}"
        print(error_msg)
        sender.reply(f"❌ {error_msg}")
        raise


def init_qinglong():
    """初始化青龙连接"""
    try:
        ql_config = sg.bucketGet('mrconli.xydj', 'ql_config')
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
    """获取青龙token"""
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
    """添加变量到青龙"""
    include_device = sg.bucketGet('mrconli.xydj', 'include_device') or 'false'
    authorization, device_id = token.split('#')
    if include_device == "true":
        new_token = f'{authorization}#{device_id}'
    else:
        new_token = f'{authorization}'
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

        auth_time = '2099-12-31' or '未授权'
        data = {
            "name": var_name,
            "value": new_token,
            "remarks": f"星芽账号:{account}丨用户:{username}丨授权时间:{auth_time}",
        }

        max_retries = 3
        for attempt in range(max_retries):
            response = requests.post(url, headers=headers, json=[data])
            if response.status_code == 200:
                new_ids = [item['id'] for item in response.json().get('data', [])]
                sg.bucketSet('mrconli.xydj.env_id', account, json.dumps(new_ids))
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


def enable_in_qinglong(env_ids):
    """启用环境变量"""
    try:
        url = f"{ql_url}/open/envs/enable"
        headers = {
            "Authorization": f"Bearer {ql_token}",
            "Content-Type": "application/json"
        }
        response = requests.put(url, headers=headers, data=json.dumps(env_ids))
        if response.status_code == 200:
            rjson = response.json()
            if rjson.get('code') == 200:
                return True
            else:
                sender.reply(f"❌ 启用环境变量失败: {rjson.get('message')}")
                return False
        else:
            raise Exception(f"{response.status_code}")
    except Exception as e:
        sender.reply(f"❌ 启用环境变量失败: {str(e)}")
        return False


def disable_in_qinglong(env_ids):
    """禁用环境变量"""
    try:
        url = f"{ql_url}/open/envs/disable"
        headers = {
            "Authorization": f"Bearer {ql_token}",
            "Content-Type": "application/json"
        }
        response = requests.put(url, headers=headers, data=json.dumps(env_ids))
        if response.status_code == 200:
            rjson = response.json()
            if rjson.get('code') == 200:
                return True
            else:
                sender.reply(f"❌ 禁用环境变量失败: {rjson.get('message')}")
                return False
        else:
            raise Exception(f"{response.status_code}")
    except Exception as e:
        sender.reply(f"❌ 禁用环境变量失败: {str(e)}")
        return False


def delete_from_qinglong(account):
    """从青龙删除变量"""
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
    """管理账号"""
    accounts = _sg_literal(uservalue or "[]")
    if not accounts:
        sender.reply(f"""
=====账号管理=====
❌ 未找到任何账号
------------------
💡 发送"{login_cmd}"绑定账号
==================""")
        return

    account_list = """
=====账号列表=====
批量操作:
[00] 授权全部账号
[01] 删除全部账号
------------------
账号列表:"""
    for i, account in enumerate(accounts, 1):
        token = sg.bucketGet('mrconli.xydj.token', account)
        auth = '2099-12-31'
        auth_status = "✅ 已授权" if auth and auth > today else "❌ 未授权"
        username = f"{account}"
        account_list += f"\n[{i}] {username[:3]}****{username[-4:]}\n    {auth_status}"
        if auth and auth > today:
            account_list += f"\n    授权到期: {auth}"
    account_list += "\n------------------\n回复数字选择账号\n回复'q'退出"

    sender.reply(account_list)
    choice = sender.listen(60000)

    if not choice:
        sender.reply("❌ 操作超时")
        return
    elif choice == 'q':
        sender.reply("✅ 已取消操作")
        return

    try:
        if choice == '01':
            accounts.copy()
            for account in accounts:
                delete_account(account)
            sg.bucketSet('mrconli.xydj.user', userid, '[]')
            sender.reply("✅ 已删除全部账号")

        elif choice == '00':
            sender.reply("📝 请输入授权天数(如使用积分兑换，必须为30的倍数):")
            days = sender.listen(60000)
            if not days:
                sender.reply("❌ 操作超时")
                return
            elif days == 'q':
                sender.reply("✅ 已取消授权")
                return
            coin_bucket = sg.bucketGet('mrconli.xydj', 'coin_bucket') or 'dd_sign_points'
            coin_price = int(sg.bucketGet('mrconli.xydj', 'coin') or '0')  # 确保获取最新积分价格

            try:
                days = int(days)
                if days <= 0:
                    raise ValueError("天数必须大于0")

                pay_choice = '1'
                if coin_price > 0:
                    user_coin = Decimal(sg.bucketGet('coin_bucket', userid) or '0')
                    auth_guide = f"""
=====批量授权方式=====
[1] 微信支付
[2] 积分支付 (当前积分: {user_coin})
--------------------
💰 积分比例: {coin_price}积分/月
回复数字选择方式"""
                    sender.reply(auth_guide)
                    pay_choice = sender.listen(60000)
                    if pay_choice not in ['1', '2']:
                        sender.reply("❌ 无效的支付方式")
                        return

                if pay_choice == '1':
                    amount = price * (Decimal(days) / 30) * len(accounts)
                    amount = amount.quantize(Decimal('0.01'), rounding='ROUND_UP')
                    if process_payment(amount, days):
                        success_count = 0
                        for account in accounts:
                            calculate_auth_time(account, days / 30)
                            True
                            token = sg.bucketGet('mrconli.xydj.token', account)
                            if token and username:
                                add_to_qinglong(token, account, userid)
                            success_count += 1
                        sender.reply(f"""
=====批量授权成功=====
💰 支付: {amount}元
⏰ 时长: {days}天
✅ 成功: {success_count}个账号
====================""")

                elif pay_choice == '2':
                    coin_bucket = sg.bucketGet('mrconli.xydj', 'coin_bucket') or 'dd_sign_points'
                    user_coin = Decimal(sg.bucketGet(coin_bucket, userid) or '0')
                    months = days / 30
                    if months != int(months):
                        sender.reply("❌ 积分支付需整月授权")
                        return
                    months = int(months)
                    need_coin = coin_price * months * len(accounts)
                    if user_coin < need_coin:
                        sender.reply(f"""
=====积分不足=====
❌ 积分余额不足
------------------
💰 所需积分: {need_coin}
💵 当前积分: {user_coin}
====================""")
                        return

                    new_coin = int(user_coin - need_coin)
                    sg.bucketSet(coin_bucket, userid, str(new_coin))
                    success_count = 0
                    for account in accounts:
                        calculate_auth_time(account, months)
                        True
                        token = sg.bucketGet('mrconli.xydj.token', account)
                        username = account
                        if token and username:
                            add_to_qinglong(token, account, username)

                        success_count += 1
                    sender.reply(f"""
=====批量授权成功=====
💰 消耗: {need_coin}积分
⏰ 时长: {days}天
✅ 成功: {success_count}个账号
💵 剩余: {new_coin}积分
====================""")

                for account in accounts:
                    env_id_str = sg.bucketGet('mrconli.xydj.env_id', account)
                    if env_id_str:
                        env_ids = json.loads(env_id_str)
                        enable_in_qinglong(env_ids)

            except ValueError as ve:
                sender.reply(f"❌ 无效的输入: {str(ve)}")
            except Exception as e:
                sender.reply(f"❌ 批量授权失败: {str(e)}")

        else:
            index = int(choice) - 1
            if 0 <= index < len(accounts):
                show_account_menu(accounts[index])
            else:
                sender.reply("❌ 无效的序号")

    except Exception as e:
        sender.reply(f"❌ 操作失败: {str(e)}")


def show_account_menu(account):
    """显示账号操作菜单"""
    token = sg.bucketGet('mrconli.xydj.token', account)
    auth = '2099-12-31'
    if len(token) == 32:
        username = f"Token...{token[-6:]}"
    else:
        username = f"{account}"
    auth_status = "✅ 已授权" if auth and auth > today else "❌ 未授权"
    auth_info = f"\n    到期: {auth}" if auth and auth > today else ""
    menu = f"""
=====账号操作=====
📱 账号: {username[:3]}****{username[-4:]}
🔐 状态: {auth_status}{auth_info}
------------------
[1] 授权账号
[2] 删除账号
[3] 续期ck
------------------
回复数字选择操作
回复"q"退出"""
    sender.reply(menu)
    choice = sender.listen(60000)
    if not choice:
        sender.reply("❌ 操作超时")
        return
    elif choice == 'q':
        sender.reply("✅ 已取消操作")
        return
    try:
        if choice == '1':
            auth_account(account)
        elif choice == '2':
            delete_account(account)
        elif choice == '3':
            xuqi(account, userid)
        else:
            sender.reply("❌ 无效的选择")
    except Exception as e:
        sender.reply(f"❌ 操作失败: {str(e)}")


def auth_account(account):
    """账号授权"""
    try:
        coin_bucket = sg.bucketGet('mrconli.xydj', 'coin_bucket') or 'dd_sign_points'
        user_coin = sg.bucketGet(coin_bucket, userid) or '0'
        user_coin = Decimal(user_coin)  # 使用 Decimal 处理大数值
        month_coin = Decimal(coin_price)  # 从配置获取每月所需积分
        if month_coin <= 0:
            auth_guide = """
=====授权方式=====
[1] 微信支付
------------------
回复数字选择方式
回复"q"退出"""
        else:
            auth_guide = f"""
=====授权方式=====
[1] 微信支付
[2] 积分支付 (当前积分: {user_coin})
------------------
💰 积分比例: {month_coin}积分/月
回复数字选择方式
回复"q"退出"""
        sender.reply(auth_guide)
        choice = sender.listen(60000)
        if not choice:
            sender.reply("❌ 操作超时")
            return False
        elif choice == 'q':
            sender.reply("✅ 已取消授权")
            return False
        if choice == '1':
            sender.reply("📝 请输入授权天数:")
            days = sender.listen(60000)
            if not days:
                sender.reply("❌ 操作超时")
                return False
            elif days == 'q':
                sender.reply("✅ 已取消授权")
                return False
            days = int(days)
            if days <= 0:
                raise ValueError()
            amount = price * (Decimal(days) / Decimal(30))
            amount = Decimal(str(amount)).quantize(Decimal('0.01'), rounding='ROUND_UP')
            if amount < Decimal('0.01'):
                amount = Decimal('0.01')
            payment_success = process_payment(amount, days)  # 处理支付
            if payment_success:  # 只有在支付成功的情况下才进行授权
                auth_time = calculate_auth_time(account, days / 30)
                True
                token = sg.bucketGet('mrconli.xydj.token', account)
                username = account  # 假设account存储的是手机号
                if token and username:
                    add_to_qinglong(token, account, username)  # 强制更新变量
                else:
                    sender.reply("⚠️ 令牌获取失败，请检查配置")
                env_id_str = sg.bucketGet('mrconli.xydj.env_id', account)
                if env_id_str:
                    env_ids = json.loads(env_id_str)
                    enable_in_qinglong(env_ids)
                sender.reply(f"""
=====授权成功=====
📱 账号: {account[:3]}****{account[-4:]}
💰 支付: {amount}元
⏰ 时长: {days}天
📅 到期: {auth_time}
==================""")
                return True
            else:
                sender.reply("❌ 支付未成功，授权未完成")
                return False
        elif choice == '2' and month_coin > 0:  # 只有积分支付开启时才处理
            sender.reply("📝 授权月数:")
            months = sender.listen(60000)
            if not months:
                sender.reply("❌ 操作超时")
                return False
            elif months == 'q':
                sender.reply("✅ 已取消授权")
                return False
            months = int(months)
            if months <= 0:
                raise ValueError()
            need_coin = month_coin * months
            if user_coin < need_coin:
                sender.reply(f"""
=====积分不足=====
❌ 积分余额不足
------------------
💰 所需积分: {need_coin}
💵 当前积分: {user_coin}
==================""")
                return False
            new_coin = int(user_coin - need_coin)
            sg.bucketSet(coin_bucket, userid, str(new_coin))
            auth_time = calculate_auth_time(account, months)
            True
            token = sg.bucketGet('mrconli.xydj.token', account)
            if token and userid:
                add_to_qinglong(token, account, userid)  # 强制更新变量
            else:
                sender.reply("⚠️ 令牌获取失败，请检查配置")

            env_id_str = sg.bucketGet('mrconli.xydj.env_id', account)
            if env_id_str:
                env_ids = json.loads(env_id_str)
                enable_in_qinglong(env_ids)
            sender.reply(f"""
=====授权成功=====
📱 账号: {account[:3]}****{account[-4:]}
💰 消耗: {need_coin}积分
⏰ 时长: {months}月
📅 到期: {auth_time}
------------------
💵 剩余: {new_coin}积分
==================""")
            return True
        else:
            sender.reply("❌ 无效的选择")
    except ValueError:
        sender.reply("❌ 无效的数值")
    except Exception as e:
        sender.reply(f"❌ 授权失败: {str(e)}")
    return False


def process_payment(amount, days):
    return True

def clean_expired():
    try:
        sender.reply('该管理项已取消，账号直接运行')
    except Exception:
        pass
    return None
def cron_task():
    """定时任务处理"""
    if imtype != 'fake':
        return
    try:
        users = sg.bucketAllKeys('mrconli.xydj.user')
        for user in users:
            accounts = _sg_literal(sg.bucketGet('mrconli.xydj.user', user) or '[]')
            for account in accounts:
                try:
                    auth = '2099-12-31'
                    if auth and auth <= today:
                        delete_from_qinglong(account)
                        notify_user(user, account, "授权已过期,环境变量已删除,请及时续费")
                        continue
                    current_day = datetime.today().weekday()
                    is_xuqi = sg.bucketGet('mrconli.xydj.is_xuqi', account) or "false"
                    if is_xuqi == "true" and current_day in weekdays and datetime.now().time().hour >= 18:
                        oaid = sg.bucketGet('mrconli.xydj.oaid', account)
                        uuid = sg.bucketGet('mrconli.xydj.uuid', account)
                        token = sg.bucketGet('mrconli.xydj.token', account)
                        auth, device_id = token.split('#')
                        try:
                            new_token = update_token(uuid, oaid, device_id, auth)
                            if new_token:
                                sg.bucketSet('mrconli.xydj.token', account, new_token)
                                add_to_qinglong(new_token, account, user)
                                notify_user(user, account, "token续期成功")
                            else:
                                notify_user(user, account, "token续期失败，请检查token有效性")
                        except Exception as e:
                            print(f"token续期出错: {str(e)}")
                except Exception as e:
                    print(f"处理账号出错: {str(e)}")
    except Exception as e:
        print(f"定时任务出错: {str(e)}")

def notify_user(user, account, message):
    """发送用户通知"""
    try:
        notify_msg = f"""
=====星芽账号通知=====
📱 账号: {account}
📢 消息: {message}
=================="""
        sg.push('qq', '', user, '', notify_msg)
        sg.push('wx', '', user, '', notify_msg)
        sg.push('tg', '', user, '', notify_msg)
        sg.push('ipad', '', user, '', notify_msg)
        sg.push('qx', '', user, '', notify_msg)
    except Exception as e:
        print(f"发送通知失败: {str(e)}")


def retry_on_error(func, retries=3, delay=1):
    """错误重试装饰器"""
    def wrapper(*args, **kwargs):
        for i in range(retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if i == retries - 1:
                    raise e
                time.sleep(delay)
        return None
    return wrapper


def log_operation(operation, user, account, status, message=''):
    """记录操作日志"""
    try:
        log = {
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'operation': operation,
            'user': user,
            'account': account,
            'status': status,
            'message': message
        }
        logs = _sg_literal(sg.bucketGet('mrconli.xydj.logs', 'operations') or '[]')
        logs.append(log)
        if len(logs) > 1000:  # 只保留最近1000条
            logs = logs[-1000:]
        sg.bucketSet('mrconli.xydj.logs', 'operations', str(logs))
    except Exception as e:
        print(f"记录日志失败: {str(e)}")


def admin_auth():
    try:
        sender.reply('该管理项已取消，账号直接运行')
    except Exception:
        pass
    return None
def update_qinglong_env():
    """更新全部青龙环境变量"""
    sender.reply("正在更新全部账号的青龙环境变量...")
    users = sg.bucketAllKeys('mrconli.xydj.user')
    total_users = len(users)
    total_accounts = 0
    success = 0
    failed = 0
    for user in users:
        accounts = _sg_literal(sg.bucketGet('mrconli.xydj.user', user) or '[]')
        for account in accounts:
            total_accounts += 1
            try:
                token = sg.bucketGet('mrconli.xydj.token', account)
                if token:
                    add_to_qinglong(token, account, user)
                env_ids_str = sg.bucketGet('mrconli.xydj.env_id', account)
                if env_ids_str:
                    env_ids = json.loads(env_ids_str)
                    enable_in_qinglong(env_ids)
                success += 1
            except Exception as e:
                failed += 1
    sender.reply(f"""
=====更新青龙完成=====
共计: {total_users}个用户{total_accounts}个账号
------------------
✅ 成功: {success}个账号
❌ 失败: {failed}个账号
==================""")


def auth_all_users():
    """一键授权所有用户"""
    sender.reply("""
=====批量授权=====
📝 请输入授权天数
------------------
回复数字设置天数
回复"q"退出""")
    try:
        days = sender.listen(60000)
        if not days or days == 'q':
            sender.reply("✅ 已取消授权")
            return
        days = int(days)
        if days <= 0:
            raise ValueError()
        users = sg.bucketAllKeys('mrconli.xydj.user')
        success = 0
        failed = 0
        for user in users:
            accounts = _sg_literal(sg.bucketGet('mrconli.xydj.user', user) or '[]')
            for account in accounts:
                try:
                    calculate_auth_time(account, days / 30)
                    True
                    token = sg.bucketGet('mrconli.xydj.token', account)
                    if token:
                        add_to_qinglong(token, account, user)
                    env_ids_str = sg.bucketGet('mrconli.xydj.env_id', account)
                    if env_ids_str:
                        env_ids = json.loads(env_ids_str)
                        enable_in_qinglong(env_ids)
                    success += 1
                    log_operation('batch_auth', user, account, 'success')
                except Exception as e:
                    failed += 1
                    log_operation('batch_auth', user, account, 'failed', str(e))
        sender.reply(f"""
=====授权完成=====
✅ 成功: {success}个账号
❌ 失败: {failed}个账号
⏰ 授权: {days}天
==================""")
    except ValueError:
        sender.reply("❌ 无效的天数")
    except Exception as e:
        sender.reply(f"❌ 授权失败: {str(e)}")


def auth_specific_user():
    """指定用户授权"""
    sender.reply("""
=====指定授权=====
📝 请输入用户ID
(发送myuid可获取ID)
------------------
回复"q"退出""")
    user_id = sender.listen(60000)
    if not user_id or user_id == 'q':
        return
    accounts = _sg_literal(sg.bucketGet('mrconli.xydj.user', user_id) or '[]')
    if not accounts:
        sender.reply("❌ 未找到该用户的账号")
        return
    account_list = """
=====账号列表=====
[0] 授权全部账号"""
    for i, account in enumerate(accounts, 1):
        auth = '2099-12-31'
        status = "✅ 已授权" if auth and auth > today else "❌ 未授权"
        account_list += f"\n[{i}] {account[:3]}****{account[-4:]}\n    {status}"
    account_list += """
------------------
回复数字选择账号
回复"q"退出"""
    sender.reply(account_list)
    choice = sender.listen(60000)
    if not choice or choice == 'q':
        return
    try:
        sender.reply("""
=====设置授权时间=====
📝 请输入授权天数
------------------
回复数字设置天数
回复"q"退出""")
        days = sender.listen(60000)
        if not days or days == 'q':
            return
        days = int(days)
        if days <= 0:
            raise ValueError()
        if choice == '0':
            for account in accounts:
                try:
                    auth_time = calculate_auth_time(account, days / 30)
                    True
                    token = sg.bucketGet('mrconli.xydj.token', account)
                    if token:
                        add_to_qinglong(token, account, user_id)
                    env_ids_str = sg.bucketGet('mrconli.xydj.env_id', account)
                    if env_ids_str:
                        env_ids = json.loads(env_ids_str)
                        enable_in_qinglong(env_ids)
                    log_operation('auth', user_id, account, 'success')
                except Exception as e:
                    log_operation('auth', user_id, account, 'failed', str(e))
            sender.reply(f"✅ 已授权所有账号 {days}天")
        else:
            index = int(choice) - 1
            if not 0 <= index < len(accounts):
                raise ValueError()
            account = accounts[index]
            auth_time = calculate_auth_time(account, days / 30)
            True
            token = sg.bucketGet('mrconli.xydj.token', account)
            if token:
                add_to_qinglong(token, account, user_id)
            env_ids_str = sg.bucketGet('mrconli.xydj.env_id', account)
            if env_ids_str:
                env_ids = json.loads(env_ids_str)
                enable_in_qinglong(env_ids)
            sender.reply(f"""
=====授权成功=====
📱 账号: {account[:3]}****{account[-4:]}
⏰ 时长: {days}天
📅 到期: {auth_time}
==================""")
            log_operation('auth', user_id, account, 'success')
    except ValueError:
        sender.reply("❌ 无效的输入")
    except Exception as e:
        sender.reply(f"❌ 授权失败: {str(e)}")
        log_operation('auth', user_id, account, 'failed', str(e))


def delete_account(account):
    """删除账号"""
    try:
        if not delete_from_qinglong(account):
            raise Exception("从青龙删除变量失败")
        sg.bucketDel('mrconli.xydj.token', account)
        True
        sg.bucketDel('mrconli.xydj.env_id', account)
        try:
            accounts = _sg_literal(uservalue or "[]")
        except (json.JSONDecodeError, TypeError) as e:
            print(f"用户列表解析失败: {str(e)}")

        if account in accounts:
            accounts.remove(account)
            try:
                sg.bucketSet('mrconli.xydj.user', userid, json.dumps(accounts, ensure_ascii=False))
            except Exception as e:
                raise Exception(f"用户列表更新失败: {str(e)}")
        sender.reply(f"""
=====删除成功=====
📱 账号: {account[:3]}****{account[-4:]}
✅ 状态: 已删除
==================""")
        log_operation('delete_account', userid, account, 'success')
        return True
    except Exception as e:
        error_msg = f"删除账号失败: {str(e)}"
        sender.reply(f"❌ {error_msg}")
        log_operation('delete_account', userid, account, 'failed', str(e))
        return False

def xuqi(account, userid):
    """刷新token"""
    token = sg.bucketGet('mrconli.xydj.token', account)
    oaid = sg.bucketGet('mrconli.xydj.oaid', account)
    uuid = sg.bucketGet('mrconli.xydj.uuid', account)

    auth, device_id = token.split('#')
    try:
        new_token = update_token(uuid, oaid, device_id, auth)
        if new_token:
            sg.bucketSet('mrconli.xydj.token', account, new_token)
            sender.reply(f"✅ token续期成功")
            add_to_qinglong(new_token, account, userid)
        else:
            sender.reply("❌ 刷新失败")
    except Exception as e:
        sender.reply(f"❌ 刷新失败: {str(e)}")


def tutorial():
    """显示星芽使用教程"""
    tutorial_text = (
        "=====星芽教程=====\n"
        "📝 入口:\n"
        "    应用商店下载“星芽免费短剧”app\n"
        "    注册后绑定提现支付宝\n"
        "🌟 基础指令:\n"
        "1. 星芽登录 - 绑定账号\n"
        "2. 星芽查询 - 查看状态\n"
        "3. 星芽时长 - 刷新时长\n"
        "4. 星芽管理 - 管理账号\n"
        "5. 星芽授权 - 管理员授权账号\n"
        "6. 星芽清理 - 管理员清理过期\n"
        "-------------------\n"
        "🚩 收益说明:\n"
        "▸ 呆瓜为每日自动获取金币\n"
        "▸ 金币兑换现金比例每日浮动\n"
        "▸ 每月收益20+\n"
        "-------------------\n"
        "⚠️ 注意事项:\n"
        "提现晚上10点到白天9点可能不会秒到\n"
        "=================="
    )
    sender.reply(tutorial_text)


def main():
    """主函数"""
    message = sender.getMessage()
    if '登录' in message or '登陆' in message or '上车' in message:
        sms_login()
    elif '管理' in message:
        manage_accounts()
    elif '查询' in message:
        query()
    elif '刷新' in message or '时长' in message:
        add_view_time()
    elif '教程' in message:
        tutorial()
    elif message == '星芽清理':
        clean_expired()
    elif message == '星芽授权' and sender.isAdmin():
        admin_auth()


if __name__ == "__main__":
    try:
        var_name, ql_host, ql_client_id, ql_client_secret, manage_cmd, query_cmd, login_cmd, price, coin_price, show_records, show_records = get_config()
        ql_url, ql_token = init_qinglong()
        imtype = sender.getImtype()
        today = str(datetime.now().date())
        if imtype == 'fake':
            cron_task()
        else:
            main()
    except Exception as e:
        sender.reply(f"❌ 运行出错: {str(e)}")
