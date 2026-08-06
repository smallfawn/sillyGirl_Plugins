# [title: 顺易充（新）]
# [name: shunYiChongXin]
# [language: python]
# [class: 任务]
# [author: huawei]
# [version: v1.1.8]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(顺易充|syc)(登录|登陆|绑定|管理|查询|运行|一键运行|刷新|一键刷新)$]
# [icon: https://i.mji.rip/2025/07/11/5132e8c191f16ac574c0328105061ec4.jpeg]
# [description: 顺易充账号登录、积分查询、Token 刷新与任务运行]
# [depe: ["pycryptodome","requests","urllib3"]]

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
    'G_SYC_concurrent_count': plugin.Form.string().title('并发数量').default('3').description('任务执行时的并发线程数量'),
    'G_SYC_proxy_api': plugin.Form.string().title('代理API').default('').description('填写代理接口或固定代理地址，不填则不启用代理'),
})
_CONFIG_FIELD_MAP = {
    ('G_SYC', 'concurrent_count'): 'G_SYC_concurrent_count',
    ('G_SYC', 'proxy_api'): 'G_SYC_proxy_api',
}

import requests
import json
import time
import hashlib
import re
import warnings
import random
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad
from urllib.parse import quote
import base64
try:
    from urllib3.exceptions import InsecureRequestWarning
    warnings.filterwarnings("ignore", category=InsecureRequestWarning)
except Exception:
    pass
class _FallbackSender:
    def getMessage(self):
        return ""
    def reply(self, *_args, **_kwargs):
        return None
    def input(self, *_args, **_kwargs):
        return None
    def replyImage(self, *_args, **_kwargs):
        return None
    def listen(self, *_args, **_kwargs):
        return ""
    def isAdmin(self):
        return False
    def getUserID(self):
        return ""
    def setContinue(self):
        return None
try:
    senderID = sg.getSenderID()
    sender = sg.Sender(senderID)
    userid = sender.getUserID()
except Exception:
    senderID = ""
    sender = _FallbackSender()
    userid = ""

BUCKET_CONFIG = "G_SYC"
BUCKET_USER = "G_SYC_user"
BUCKET_TOKEN = "G_SYC_token"
BUCKET_AUTH_STATE = "G_SYC_auth_state"
BUCKET_TOKEN_STATUS = "G_SYC_token_status"


def get_bucket_config_value(key: str, default=""):
    try:
        value = sg.bucketGet(bucket=BUCKET_CONFIG, key=key)
        return default if value in [None, ""] else value
    except Exception:
        return default



def get_user_phones(user_id=None) -> list:
    if not user_id:
        user_id = userid
    try:
        phones_json = sg.bucketGet(BUCKET_USER, user_id) or "[]"
        phones = json.loads(phones_json)
        if not isinstance(phones, list):
            return []
        return [str(phone).strip() for phone in phones if str(phone).strip()]
    except Exception:
        return []




def get_proxy_api() -> str:
    return get_bucket_config_value("proxy_api", "")
proxy_url = get_proxy_api()
IS_PROXY = bool(proxy_url)
if IS_PROXY:
    print("[INFO] 代理模式: 已启用")
    print(f"[INFO] 代理API: {proxy_url}")
else:
    print("[INFO] 代理模式: 未启用")
proxy_cache = {}
proxy_cache_time = {}
proxy_lock_dict = threading.Lock()
PROXY_CACHE_TTL = 300
def get_proxy(force_new=False, account_key=None):
    if not IS_PROXY or not proxy_url:
        return None
    current_time = time.time()
    if account_key and not force_new:
        with proxy_lock_dict:
            if account_key in proxy_cache:
                cache_time = proxy_cache_time.get(account_key, 0)
                if current_time - cache_time < PROXY_CACHE_TTL:
                    return proxy_cache[account_key]
                else:
                    del proxy_cache[account_key]
                    del proxy_cache_time[account_key]
    try:
        response = requests.get(proxy_url, timeout=5)
        if response.status_code == 200:
            ip = response.text.strip()
            if "请先添加白名单" in ip:
                print("[WARNING] 代理服务异常：请先添加白名单")
                return None
            proxy_dict = {"http": ip, "https": ip}
            if account_key:
                with proxy_lock_dict:
                    expired_keys = [
                        k
                        for k, t in proxy_cache_time.items()
                        if current_time - t >= PROXY_CACHE_TTL
                    ]
                    for k in expired_keys:
                        proxy_cache.pop(k, None)
                        proxy_cache_time.pop(k, None)
                    proxy_cache[account_key] = proxy_dict
                    proxy_cache_time[account_key] = current_time
            print(f"[INFO] 获取代理成功: {ip}")
            return proxy_dict
        else:
            print(f"[WARNING] 代理API响应异常: {response.status_code}")
            return None
    except Exception as e:
        print(f"[WARNING] 获取代理失败: {str(e)}")
        return None
def request_with_retry(method, url, max_retries=3, account_key=None, **kwargs):
    if (
        "headers" in kwargs
        and kwargs["headers"]
        and "_account_key" in kwargs["headers"]
    ):
        if account_key is None:
            account_key = kwargs["headers"].get("_account_key")
        clean_headers = {
            k: v for k, v in kwargs["headers"].items() if k != "_account_key"
        }
        kwargs["headers"] = clean_headers
    current_proxy = None
    for attempt in range(max_retries):
        try:
            if IS_PROXY:
                if attempt == 0:
                    current_proxy = get_proxy(force_new=False, account_key=account_key)
                else:
                    current_proxy = get_proxy(force_new=True, account_key=account_key)
                if current_proxy:
                    kwargs["proxies"] = current_proxy
                else:
                    kwargs["proxies"] = None
            if method.upper() == "GET":
                response = requests.get(url, **kwargs)
            else:
                response = requests.post(url, **kwargs)
            return response
        except (
            requests.exceptions.ProxyError,
            requests.exceptions.ConnectionError,
        ) as e:
            print(f"[WARNING] 代理连接错误: {str(e)[:100]}")
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            else:
                print("[ERROR] 代理请求失败，已达最大重试次数")
                raise
        except requests.exceptions.Timeout:
            print("[WARNING] 请求超时")
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            else:
                print("[ERROR] 请求超时，已达最大重试次数")
                raise
        except Exception as e:
            print(f"[ERROR] 请求异常: {str(e)[:100]}")
            raise
    return None
def get_random_region_pair() -> tuple:
    pairs = [
        ("0551", "340100"),
        ("025", "320100"),
        ("021", "310100"),
        ("010", "110100"),
        ("020", "440100"),
        ("0755", "440300"),
        ("0756", "440400"),
        ("0757", "440600"),
        ("0769", "441900"),
        ("0571", "330100"),
        ("0574", "330200"),
        ("0512", "320500"),
        ("0510", "320200"),
        ("028", "510100"),
        ("023", "500100"),
        ("029", "610100"),
        ("027", "420100"),
        ("0371", "410100"),
        ("0731", "430100"),
        ("0791", "360100"),
        ("0591", "350100"),
        ("0592", "350200"),
        ("0531", "370100"),
        ("0532", "370200"),
        ("024", "210100"),
        ("0411", "210200"),
        ("0431", "220100"),
        ("0451", "230100"),
        ("0871", "530100"),
        ("0851", "520100"),
        ("0771", "450100"),
        ("0898", "460100"),
        ("0899", "460200"),
        ("0351", "140100"),
        ("0311", "130100"),
        ("0553", "340200"),
        ("0519", "320400"),
        ("0518", "320700"),
        ("0710", "420600"),
    ]
    return random.choice(pairs)
def get_random_user_agent() -> str:
    ua_types = [
        lambda: f"okhttp/{random.choice(['4.9.0', '4.9.1', '4.9.3', '4.10.0', '4.11.0', '4.12.0'])}",
        lambda: f"CSPGCharge/{random.choice(['5.6.0', '5.7.0', '5.8.0'])} (iPhone; iOS {random.choice(['16.6', '17.0', '17.1', '17.6'])}; Scale/{random.choice(['2.00', '3.00'])})",
        lambda: f"Mozilla/5.0 (Linux; Android {random.randint(9, 14)}; {random.choice(['OPPO R9s', 'HUAWEI P30', 'Xiaomi MI 10', 'Samsung SM-G973F', 'vivo V2047A'])} Build/QP1A.{random.randint(190000, 210000)}.{random.randint(100, 999)}; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/{random.randint(90, 120)}.0.{random.randint(4000, 5000)}.{random.randint(100, 200)} Mobile Safari/537.36",
    ]
    return random.choice(ua_types)()
def get_task_headers():
    return {
        "User-Agent": get_random_user_agent(),
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "content-type": "application/json;charset=utf-8",
        "loginchannel": "15",
        "client-version": "5.6.0",
        "accept-language": "zh-Hans-CN;q=1",
        "lang": "1",
        "x-client-code": "01",
    }
def get_config():
    try: count=max(1,min(int(get_bucket_config_value('concurrent_count','3')),10))
    except (TypeError,ValueError): count=3
    return {'concurrent_count':count}

def md5_encrypt(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()
def triple_des_encrypt(data: str, key_base64: str) -> str:
    try:
        key_bytes = base64.b64decode(key_base64)
        cipher = DES3.new(key_bytes, DES3.MODE_ECB)
        data_bytes = data.encode("utf-8")
        padded_data = pad(data_bytes, DES3.block_size)
        encrypted = cipher.encrypt(padded_data)
        return base64.b64encode(encrypted).decode("utf-8")
    except Exception as e:
        print(f"❌ 3DES加密错误: {e}")
        return None
def build_signed_params(keyword: str, value: str) -> tuple:
    random_num = str(random.randint(100, 999))
    d0, d1, d2 = random_num[0], random_num[1], random_num[2]
    timestamp_ms = int(time.time() * 1000)
    raw = f"{d0}{keyword}{d1}{value}{d2}{timestamp_ms}{random_num}"
    md5_hash = md5_encrypt(raw)
    key_base64 = "+7+hkq4l97VMgGHTufKDEHzfH8FzQ0aw"
    sign = triple_des_encrypt(md5_hash, key_base64)
    timestamp = str(timestamp_ms) + random_num
    return timestamp, sign, raw, md5_hash
def send_sms_code(mobile: str) -> dict:
    try:
        account_key = f"acc_{mobile}"
        timestamp, encrypted, _, _ = build_signed_params("mobile", mobile)
        if not encrypted:
            return None
        sign_url_encoded = quote(encrypted)
        url = f"https://app.wodeev.com/cst-front/v2.0/sms?verifyType=05&mobile={mobile}&timestamp={timestamp}&sign={sign_url_encoded}&countryAreaTelCode=86"
        headers = {
            "User-Agent": get_random_user_agent(),
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Authorization": "Bearer",
            "client-version": "5.10.0",
            "lang": "1",
            "loginChannel": "07",
            "Origin": "https://www.wodeev.com",
            "Referer": "https://www.wodeev.com/",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "X-Requested-With": "com.longshine.nanwang.electric.charge",
        }
        print(f"[INFO] 发送短信验证码到: {mobile}")
        response = request_with_retry(
            "GET",
            url,
            headers=headers,
            timeout=30,
            verify=False,
            account_key=account_key,
        )
        if response.status_code == 200:
            result = response.json()
            print(f"[INFO] 短信API响应: {result}")
            if result and result.get("ret") == 200:
                print(f"[SUCCESS] 短信发送成功: {result.get('msg', '')}")
                return result
            else:
                print(
                    f"[ERROR] 短信发送失败: ret={result.get('ret')}, msg={result.get('msg')}"
                )
                return None
        else:
            print(f"[ERROR] 短信API请求失败: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"[ERROR] 发送短信异常: {str(e)}")
        return None
def login_with_sms_code(mobile: str, code: str) -> dict:
    try:
        time.sleep(random.uniform(1, 3))
        account_key = f"acc_{mobile}"
        url = "https://app.wodeev.com/cst-front/open/v3.0/login"
        city_code, province_code = get_random_region_pair()
        data = {
            "cityCode": city_code,
            "countryCode": "中国",
            "loginType": "02",
            "mobile": mobile,
            "verifyCode": code,
            "countryAreaTelCode": "86",
            "provinceCode": province_code,
            "rsaFlag": "1",
            "deviceId": "",
            "deviceModel": "Android",
            "systemVersion": "Android 13",
        }
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json, text/plain, */*",
            "Authorization": "",
            "loginChannel": "07",
            "client-version": "5.10.0",
            "lang": "1",
            "User-Agent": "okhttp/4.9.0",
        }
        response = request_with_retry(
            "POST",
            url,
            json=data,
            headers=headers,
            verify=False,
            timeout=15,
            account_key=account_key,
        )
        if response.status_code != 200:
            return {
                "success": False,
                "message": f"登录HTTP异常: {response.status_code}",
                "token": "",
                "refreshToken": "",
                "custInfo": None,
            }
        if not response.text or response.text.strip() == "":
            return {
                "success": False,
                "message": "登录接口返回为空",
                "token": "",
                "refreshToken": "",
                "custInfo": None,
            }
        try:
            res_data = response.json()
        except json.JSONDecodeError:
            return {
                "success": False,
                "message": "登录接口返回非JSON",
                "token": "",
                "refreshToken": "",
                "custInfo": None,
            }
        if res_data.get("ret") == 200:
            return {
                "success": True,
                "message": "登录成功",
                "token": res_data.get("token", ""),
                "refreshToken": res_data.get("refreshToken", ""),
                "custInfo": res_data.get("custInfo"),
            }
        else:
            return {
                "success": False,
                "message": f"登录失败: {res_data.get('msg', '未知错误')}",
                "token": "",
                "refreshToken": "",
                "custInfo": None,
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"登录异常: {str(e)}",
            "token": "",
            "refreshToken": "",
            "custInfo": None,
        }
def query_user_points():
    accounts=get_user_accounts()
    if not accounts:return sender.reply('您还没有绑定顺易充账号，请发送【顺易充登录】')
    rows=[]
    for account in accounts.values():
        phone,token=account.get('phone',''),account.get('token','');masked=phone[:3]+'****'+phone[-4:] if len(phone)==11 else phone
        if not token:rows.append(f'{masked}：缺少 Token');continue
        headers=get_task_headers();headers['authorization']=token if token.lower().startswith('bearer ') else f'Bearer {token}';headers['_account_key']=f'acc_{phone}'
        score=get_score_rank_task(headers)
        if not score:rows.append(f'{masked}：查询失败');continue
        year=datetime.now().year;yearly=get_year_score_task(headers,year)
        rows.append(f"{masked}：总积分 {score['积分']}，可用 {score['可用积分']}"+(f'，{year}年 {yearly}' if yearly is not None else ''))
    sender.reply('顺易充积分：\n'+'\n'.join(rows))

def bind_account():
    bind_account_with_sms()
def bind_account_with_sms():
    sender.reply('请输入手机号，回复 q 退出');phone=sender.input(60000,1,False)
    if not phone or str(phone).lower()=='q':return sender.reply('已取消')
    phone=str(phone).strip()
    if not re.fullmatch(r'1[3-9]\d{9}',phone):return sender.reply('手机号格式错误')
    if not send_sms_code(phone):return sender.reply('短信发送失败，请稍后重试')
    sender.reply('短信已发送，请输入验证码');code=sender.input(180000,1,False)
    if not code or str(code).lower()=='q':return sender.reply('已取消')
    handle_phone_input_sms(phone,str(code).strip())


def build_bind_success_message(phone,*_args):
    masked=phone[:3]+'****'+phone[-4:] if len(phone)==11 else phone
    return f'账号 {masked} 绑定成功'


def handle_phone_input_sms(phone,sms_code):
    result=login_with_sms_code(phone,sms_code)
    if not result.get('success') or not result.get('token'):return sender.reply(f"登录失败：{result.get('message','验证码无效')}")
    accounts=get_user_accounts();account_id=next((k for k,v in accounts.items() if v.get('phone')==phone),phone)
    accounts[account_id]={'phone':phone,'token':result['token'],'refresh_token':result.get('refreshToken',''),'cust_info':result.get('custInfo'),'updated_at':int(time.time())}
    save_user_accounts(accounts);sender.reply(build_bind_success_message(phone))

def get_user_accounts(user_id=None):
    accounts={}
    for phone in get_user_phones(user_id or userid):
        try:state=json.loads(sg.bucketGet(BUCKET_AUTH_STATE,phone) or '{}')
        except (TypeError,ValueError):state={}
        accounts[phone]={'phone':phone,'token':state.get('token') or sg.bucketGet(BUCKET_TOKEN,phone) or '','refresh_token':state.get('refreshToken',''),'cust_info':state.get('custInfo'),'updated_at':state.get('updatedAt',0)}
    return accounts

def save_user_accounts(accounts,user_id=None):
    user_id=user_id or userid;old=set(get_user_phones(user_id));phones=[]
    for account in accounts.values():
        phone=str(account.get('phone','')).strip()
        if not phone:continue
        phones.append(phone);token=account.get('token','')
        if token:sg.bucketSet(BUCKET_TOKEN,phone,token)
        state={'token':token,'refreshToken':account.get('refresh_token',''),'custInfo':account.get('cust_info'),'updatedAt':account.get('updated_at') or int(time.time())}
        sg.bucketSet(BUCKET_AUTH_STATE,phone,json.dumps(state,ensure_ascii=False))
    for phone in old-set(phones):sg.bucketDel(BUCKET_TOKEN,phone);sg.bucketDel(BUCKET_AUTH_STATE,phone);sg.bucketDel(BUCKET_TOKEN_STATUS,phone)
    if phones:sg.bucketSet(BUCKET_USER,user_id,json.dumps(phones,ensure_ascii=False))
    else:sg.bucketDel(BUCKET_USER,user_id)

def manage_accounts():
    accounts=get_user_accounts()
    if not accounts:return sender.reply('您还没有绑定顺易充账号，请发送【顺易充登录】')
    rows=[f'{i}. {a["phone"][:3]}****{a["phone"][-4:]}' for i,a in enumerate(accounts.values(),1)]
    sender.reply('顺易充账号：\n'+'\n'.join(rows)+'\n回复序号管理，9998 删除全部，q 退出');handle_account_selection(sender.input(60000,1,False))

def delete_all_accounts():
    accounts=get_user_accounts()
    if not accounts:return sender.reply('没有可删除的账号')
    sender.reply(f'确认删除全部 {len(accounts)} 个账号？回复 y 确认')
    if str(sender.input(60000,1,False)).lower()!='y':return sender.reply('已取消')
    save_user_accounts({});sender.reply('全部账号已删除')

def handle_account_selection(selection):
    if selection is None or str(selection).lower()=='q':return
    accounts=get_user_accounts();items=list(accounts.items())
    try:choice=int(selection)
    except (TypeError,ValueError):return sender.reply('请输入有效序号')
    if choice==9998:return delete_all_accounts()
    try:account_id,_=items[choice-1]
    except IndexError:return sender.reply('序号无效')
    sender.reply('1. 运行任务\n2. 删除账号\n回复 q 退出');action=sender.input(60000,1,False)
    if action=='1':return run_single_account_task(account_id,accounts)
    if action=='2':
        sender.reply('回复 y 确认删除')
        if str(sender.input(60000,1,False)).lower()=='y':accounts.pop(account_id,None);save_user_accounts(accounts);sender.reply('账号已删除')



def refresh_access_token(refresh_token: str, account_key=None) -> dict:
    try:
        if not refresh_token:
            return {"success": False, "message": "refreshToken为空", "token": "", "refreshToken": ""}
        timestamp, sign, _, _ = build_signed_params("token", refresh_token)
        if not sign:
            return {"success": False, "message": "刷新签名生成失败", "token": "", "refreshToken": ""}
        payload = {"sign": sign, "refreshToken": refresh_token, "timestamp": timestamp}
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json, text/plain, */*",
            "Authorization": "",
            "client-version": "5.10.0",
            "loginChannel": "07",
            "lang": "1",
            "User-Agent": "okhttp/4.9.0",
        }
        url = "https://app.wodeev.com/cst-front/open/v2.0/refreshToken"
        response = request_with_retry("POST", url, json=payload, headers=headers, verify=False, timeout=15, account_key=account_key)
        if not response or response.status_code != 200:
            return {"success": False, "message": f"刷新HTTP异常: {response.status_code if response else '无响应'}", "token": "", "refreshToken": ""}
        try:
            res_data = response.json()
        except json.JSONDecodeError:
            return {"success": False, "message": "刷新接口返回非JSON", "token": "", "refreshToken": ""}
        if res_data.get("ret") == 200:
            return {"success": True, "message": "刷新成功", "token": res_data.get("token", ""), "refreshToken": res_data.get("refreshToken", ""), "response": res_data}
        return {"success": False, "message": f"刷新失败: {res_data.get('msg', '未知错误')}", "token": "", "refreshToken": "", "response": res_data}
    except Exception as e:
        return {"success": False, "message": f"刷新异常: {str(e)}", "token": "", "refreshToken": ""}

def user_refresh_tokens():
    user_accounts = get_user_accounts()
    if not user_accounts:
        sender.reply("❌ 您还没有绑定任何顺易充账号\n请发送「顺易充登录」进行绑定")
        return
    account_list = []
    for idx, (account_id, account) in enumerate(user_accounts.items(), 1):
        phone = account.get("phone", "未知")
        masked_phone = phone[:3] + "****" + phone[-4:] if len(phone) == 11 else phone
        refresh_token = account.get("refresh_token", "")
        cache_json = sg.bucketGet(BUCKET_TOKEN_STATUS, phone) or "{}"
        try:
            cache_data = json.loads(cache_json)
            if cache_data.get("valid") is True:
                token_status = "正常: ✓"
            elif cache_data.get("valid") is False:
                token_status = "需刷新: ❌"
            else:
                token_status = "未检测: ?"
        except Exception:
            token_status = "未检测: ?"
        has_refresh = "有" if refresh_token else "无"
        account_list.append((idx, account_id, phone, masked_phone, token_status, has_refresh))
    list_msg = "====账号Token刷新====\n"
    for idx, _, _, masked_phone, token_status, has_refresh in account_list:
        list_msg += f"[{idx}] 📱 {masked_phone} | {token_status}\n"
    list_msg += "--------------------\n回复序号选择账号刷新 (q退出)\n================="
    sender.reply(list_msg)
    success_count = 0
    fail_count = 0
    while True:
        choice = sender.input(120000, 1, False)
        if choice is None:
            sender.reply("⏰ 操作超时，已退出")
            break
        if str(choice).lower() == "q":
            sender.reply(f"✅ 已退出\n✅ 成功: {success_count}个\n❌ 失败: {fail_count}个")
            break
        try:
            idx = int(choice)
            if idx < 1 or idx > len(account_list):
                sender.reply("❌ 序号无效，请重新输入")
                continue
            _, account_id, phone, masked_phone, _, has_refresh = account_list[idx - 1]
            if has_refresh == "无":
                sender.reply(f"❌ {masked_phone} 缺少refreshToken，无法刷新\n请重新短信登录该账号")
                fail_count += 1
                continue
            sender.reply(f"📱 正在刷新: {masked_phone}")
            refresh_token = user_accounts[account_id].get("refresh_token", "")
            account_key = f"acc_{phone}"
            refresh_result = refresh_access_token(refresh_token, account_key=account_key)
            if refresh_result.get("success") and refresh_result.get("token"):
                new_token = refresh_result.get("token", "")
                new_refresh_token = refresh_result.get("refreshToken") or refresh_token
                user_accounts[account_id]["token"] = new_token
                user_accounts[account_id]["refresh_token"] = new_refresh_token
                user_accounts[account_id]["updated_at"] = int(time.time())
                save_user_accounts(user_accounts)
                cache_data = {"valid": True, "check_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                sg.bucketSet(BUCKET_TOKEN_STATUS, phone, json.dumps(cache_data))
                success_count += 1
                account_list[idx - 1] = (idx, account_id, phone, masked_phone, "正常: ✓", "有")
                new_list_msg = f"✅ {masked_phone} 刷新成功！\n\n====账号Token刷新====\n"
                for i, _, _, m_phone, t_status, h_refresh in account_list:
                    new_list_msg += f"[{i}] 📱 {m_phone} | {t_status}\n"
                new_list_msg += "--------------------\n回复序号选择账号刷新 (q退出)\n================="
                sender.reply(new_list_msg)
            else:
                sender.reply(f"❌ {masked_phone} 刷新失败：{refresh_result.get('message', '未知错误')}\n\n继续选择下一个账号或回复q退出")
                fail_count += 1
        except ValueError:
            sender.reply("❌ 请输入数字")

def admin_refresh_all_tokens():
    if not sender.isAdmin(): return sender.reply('仅管理员可一键刷新')
    users = {user_id: get_user_accounts(user_id) for user_id in sg.bucketAllKeys(BUCKET_USER)}
    targets = [(user_id, account) for user_id, accounts in users.items() for account in accounts.values() if account.get('refresh_token')]
    if not targets: return sender.reply('没有可刷新的账号')
    success = 0
    for user_id, account in targets:
        result = refresh_access_token(account['refresh_token'], account_key=f"acc_{account['phone']}")
        if result.get('success') and result.get('token'):
            account['token'] = result['token']; account['refresh_token'] = result.get('refreshToken') or account['refresh_token']; account['updated_at'] = int(time.time()); success += 1
    for user_id, accounts in users.items(): save_user_accounts(accounts, user_id)
    sender.reply(f'刷新完成：成功 {success}，失败 {len(targets)-success}')



def run_task_for_account(phone, token, account_id=None, user_id=None):
    try:
        if not token:
            return {
                "phone": phone,
                "masked_phone": phone[:3] + "****" + phone[-4:]
                if len(phone) == 11
                else phone,
                "success": False,
                "error": "Token为空",
                "details": [],
                "account_id": account_id,
                "user_id": user_id,
            }
        account_key = f"acc_{phone}"
        if not token.lower().startswith("bearer "):
            token = f"Bearer {token}"
        headers = get_task_headers()
        headers["authorization"] = token
        headers["_account_key"] = account_key  # 在headers中传递账号标识
        masked_phone = phone[:3] + "****" + phone[-4:] if len(phone) == 11 else phone
        result = {
            "phone": phone,
            "masked_phone": masked_phone,
            "success": False,
            "error": None,
            "details": [],
            "account_id": account_id,
            "user_id": user_id,
        }
        try:
            sign_result, sign_success = perform_daily_sign_in_task(headers)
            result["details"].append(sign_result)
        except Exception as e:
            error_msg = f"签到异常: {str(e)}"
            result["details"].append(f"❌ {error_msg}")
            result["error"] = error_msg
        try:
            available_tasks, _ = check_task_status_task(headers)
            if available_tasks:
                task_count = 0
                for task in available_tasks:
                    if task.get("type") != "1216":
                        try:
                            claim_result, success = claim_task_reward_task(
                                headers, task
                            )
                            if success:
                                task_count += 1
                            time.sleep(1)
                        except Exception as e:
                            result["details"].append(f"❌ 任务领取异常: {str(e)}")
                if task_count > 0:
                    result["details"].append(f"✅ 成功领取 {task_count} 个任务奖励")
        except Exception as e:
            error_msg = f"任务检查异常: {str(e)}"
            result["details"].append(f"❌ {error_msg}")
            if not result["error"]:
                result["error"] = error_msg
        try:
            score_info = get_score_rank_task(headers)
            if score_info:
                result["details"].append(
                    f"🏆 积分: {score_info['积分']}"
                )
            else:
                result["details"].append("⚠️ 获取积分信息失败")
        except Exception as e:
            error_msg = f"获取积分异常: {str(e)}"
            result["details"].append(f"❌ {error_msg}")
            if not result["error"]:
                result["error"] = error_msg
        if (
            not result["error"]
            or len([d for d in result["details"] if d.startswith("✅")]) > 0
        ):
            result["success"] = True
        return result
    except Exception as e:
        return {
            "phone": phone,
            "masked_phone": phone[:3] + "****" + phone[-4:]
            if len(phone) == 11
            else phone,
            "success": False,
            "error": f"账号执行异常: {str(e)}",
            "details": [f"❌ 执行任务时发生异常: {str(e)}"],
            "account_id": account_id,
            "user_id": user_id,
        }
def run_user_tasks():
    accounts={k:v for k,v in get_user_accounts().items() if v.get('token')}
    if not accounts:return sender.reply('没有包含 Token 的账号')
    config=get_config();execute_tasks_for_accounts(accounts,config['concurrent_count'],config)

def execute_single_account(account_data, *_args):
    account_id, account = account_data
    phone, token = account.get('phone', ''), account.get('token', '')
    masked = phone[:3] + '****' + phone[-4:] if len(phone) == 11 else phone or '未知'
    if not phone or not token:
        return {'success': False, 'error': '账号信息不完整', 'masked_phone': masked, 'details': []}
    result = run_task_for_account(phone, token, account_id, account.get('user_id', userid))
    result['masked_phone'] = masked
    return result

def execute_tasks_for_accounts(accounts,concurrent_count,_config=None):
    sender.reply(f'开始执行 {len(accounts)} 个账号，{concurrent_count} 线程')
    with ThreadPoolExecutor(max_workers=concurrent_count) as executor:
        results=[future.result() for future in as_completed([executor.submit(execute_single_account,(key,account),{},None) for key,account in accounts.items()])]
    success=sum(bool(r.get('success')) for r in results);rows=[f"{r['masked_phone']}：{'成功' if r.get('success') else r.get('error','失败')}" for r in results]
    sender.reply(f'任务完成：成功 {success}，失败 {len(results)-success}\n'+'\n'.join(rows))

def run_single_account_task(account_id,accounts):
    account=accounts.get(account_id)
    if not account or not account.get('token'):return sender.reply('账号不存在或缺少 Token')
    result=run_task_for_account(account['phone'],account['token'],account_id,userid)
    sender.reply(('任务完成' if result.get('success') else f"任务失败：{result.get('error')}")+'\n'+'\n'.join(result.get('details',[])))

def run_all_tasks():
    if not sender.isAdmin():return sender.reply('仅管理员可一键运行')
    accounts={}
    for user_id in sg.bucketAllKeys(BUCKET_USER):
        for phone,account in get_user_accounts(user_id).items():
            if account.get('token'):account['user_id']=user_id;accounts[f'{user_id}:{phone}']=account
    if not accounts:return sender.reply('没有可运行的账号')
    config=get_config();execute_tasks_for_accounts(accounts,config['concurrent_count'],config)

def perform_daily_sign_in_task(headers):
    try:
        url = "https://app.wodeev.com/bil-front/v2.0/activity/getWelfare"
        payload = {"type": "1201", "taskNo": "20221231"}
        account_key = headers.get("_account_key")  # 从 headers 提取账号标识
        response = request_with_retry(
            "POST",
            url,
            headers=headers,
            json=payload,
            timeout=10,
            verify=False,
            account_key=account_key,
        )
        res_data = response.json()
        ret_code = res_data.get("ret", "未知")
        msg = res_data.get("msg", "无返回信息")
        if ret_code == 200 or ret_code == "200":
            if msg == "调用成功":
                return "✅ 签到成功", True
            else:
                return "✅ 签到成功", True
        elif ret_code == 400 or ret_code == "400":
            if "超过最大可领取次数" in msg:
                return "✅ 今日已签到", True
            else:
                return "❌ 签到失败: " + msg, False
        else:
            print(f"签到返回码: {ret_code}, 消息: {msg}")
            return "❌ 签到失败", False
    except Exception as e:
        return "❌ 签到异常: " + str(e), False
def check_task_status_task(headers):
    try:
        url = "https://app.wodeev.com/bil-front/v2.0/activity/queryWelfareList"
        account_key = headers.get("_account_key")  # 从 headers 提取账号标识
        response = request_with_retry(
            "GET",
            url,
            headers=headers,
            timeout=10,
            verify=False,
            account_key=account_key,
        )
        res_data = response.json()
        if res_data.get("ret") != 200 and res_data.get("ret") != "200":
            return [], False
        available_tasks = []
        task_list = res_data.get("data", {}).get("list", [])
        for task in task_list:
            status = task.get("status")
            if status == "0" or status == 0:
                available_tasks.append(task)
        return available_tasks, True
    except Exception:
        return [], False
def claim_task_reward_task(headers, task):
    try:
        task_type = task.get("type")
        task_no = task.get("taskNo")
        task.get("name", "未知任务")
        account_key = headers.get("_account_key")  # 从 headers 提取账号标识
        payload = {"type": task_type, "taskNo": task_no}
        url = "https://app.wodeev.com/bil-front/v2.0/activity/getWelfare"
        response = request_with_retry(
            "POST",
            url,
            headers=headers,
            json=payload,
            timeout=10,
            verify=False,
            account_key=account_key,
        )
        res_data = response.json()
        ret_code = res_data.get("ret", "未知")
        if ret_code == 200 or ret_code == "200":
            return True, True
        else:
            return False, False
    except Exception:
        return False, False
def get_score_rank_task(headers):
    try:
        account_key = headers.get("_account_key")
        url = "https://app.wodeev.com/bil-front/v2.0/accounts/myScoreRank?scoreType=02"
        response = request_with_retry(
            "GET",
            url,
            headers=headers,
            timeout=10,
            verify=False,
            account_key=account_key,
        )
        res_data = response.json()
        if res_data.get("ret") != 200 and res_data.get("ret") != "200":
            print(f"获取积分接口返回错误: {res_data.get('ret')} - {res_data.get('msg', '无错误信息')}")
            return None
        data = res_data.get("data", {})
        return {
            "积分": data.get("myScores", "0"),
            "可用积分": data.get("myAvailableScores", "0"),
            "排名": data.get("myRank", "未知"),
        }
    except Exception as e:
        print(f"获取积分信息异常: {str(e)}")
        return None
def get_year_score_task(headers, year=None):
    try:
        if year is None:
            year = datetime.now().year
        year_prefix = str(year)
        total_earned = 0
        page_num = 1
        max_pages = 20
        page_size = 100
        account_key = headers.get("_account_key")
        while page_num <= max_pages:
            url = f"https://app.wodeev.com/def-front/v2.0/accounts/pointsInfo?pageNum={page_num}&totalNum={page_size}"
            response = request_with_retry(
                "GET", url, headers=headers, timeout=10, verify=False, account_key=account_key,
            )
            data = response.json()
            if data.get("ret") != 200 and data.get("ret") != "200":
                break
            change_list = data.get("changeList", [])
            if not change_list:
                break
            found_older = False
            for record in change_list:
                record_time = record.get("time", "")
                if record_time < year_prefix:
                    found_older = True
                    break
                if record_time.startswith(year_prefix) and record.get("changeType") == "01":
                    try:
                        total_earned += int(float(record.get("points", "0")))
                    except:
                        pass
            if found_older or len(change_list) < page_size:
                break
            page_num += 1
        return str(total_earned)
    except Exception as e:
        print(f"获取{year}年积分异常: {str(e)}")
        return None
if __name__ == "__main__":
    match=re.fullmatch(r"(顺易充|syc)(登录|登陆|绑定|管理|查询|运行|一键运行|刷新|一键刷新)",sender.getMessage(),re.I)
    if not match:sender.setContinue()
    elif match.group(2) in ('登录','登陆','绑定'):bind_account()
    elif match.group(2)=='管理':manage_accounts()
    elif match.group(2)=='查询':query_user_points()
    elif match.group(2)=='运行':run_user_tasks()
    elif match.group(2)=='一键运行':run_all_tasks()
    elif match.group(2)=='刷新':user_refresh_tokens()
    elif match.group(2)=='一键刷新':admin_refresh_all_tokens()
