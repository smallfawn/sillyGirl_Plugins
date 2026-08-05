# [title: m038_爱仙居]
# [name: m038AiXianJu]
# [language: python]
# [class: 任务]
# [author: mrconli]
# [version: v1.5.0]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^爱仙居(.*)|(.*)爱仙居$]
# [cron: 38 8,18 * * *]
# [icon: https://pp.myapp.com/ma_icon/0/icon_52529046_1757929454/256]
# [description: 支持短信登录，ck提交青龙；格式“session_id#account_id#client_id#user_agent”；1.4.0更新：修正中奖记录查询问题；1.3.0更新：新增登录方式配参选择；1.0.0初版：支持批量ck登录，支持代理]
# [depe: ["requests", "urllib3"]]


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
    'mrconli_config_ddddocr': form.string().title('DDDDOCR').default('').description('DDDDOCR服务地址,可用雪乃docker自建'),
    'mrconli_aixianju_bind': form.string().title('登录方式').default('').description('0：所有方式，1：仅短信登录，2：仅CK登录'),
    'mrconli_aixianju_ql_config': form.string().title('对接青龙').default('').description('http://ip:端口丨ClientID丨ClientSecret'),
    'mrconli_aixianju_var_name': form.string().title('环境变量名').default('').description('青龙容器内的变量名，默认为：m_axj'),
    'mrconli_aixianju_is_proxy': form.boolean().title('是否启用代理').default(False).description('true/false'),
    'mrconli_aixianju_proxy_pool': form.string().title('代理池地址').default('').description('代理API服务地址'),
})
_CONFIG_FIELD_MAP = {
    ('mrconli', 'config.ddddocr'): 'mrconli_config_ddddocr',
    ('mrconli', 'aixianju.bind'): 'mrconli_aixianju_bind',
    ('mrconli', 'aixianju.ql_config'): 'mrconli_aixianju_ql_config',
    ('mrconli', 'aixianju.var_name'): 'mrconli_aixianju_var_name',
    ('mrconli', 'aixianju.is_proxy'): 'mrconli_aixianju_is_proxy',
    ('mrconli', 'aixianju.proxy_pool'): 'mrconli_aixianju_proxy_pool',
}

scripts_name =  "爱仙居"
full_scripts_name =  "爱仙居"
bucket_prefix = "mrconli.aixianju"


from decimal import Decimal  # 处理浮点数
import string
try:
    import requests
except ImportError:
    print("❌ 缺少依赖: requests，请运行 pip install requests")
    exit(1)
try:
    import re
except ImportError:
    print("❌ 缺少依赖: re，请确保在sillygirl环境中运行")
    exit(1)
try:
    import os
except ImportError:
    print("❌ 缺少依赖: os，请确保在sillygirl环境中运行")
    exit(1)
try:
    import uuid
except ImportError:
    print("❌ 缺少依赖: uuid，请确保在sillygirl环境中运行")
    exit(1)
try:
    import random
except ImportError:
    print("❌ 缺少依赖: random，请确保在sillygirl环境中运行")
    exit(1)
try:
    import hashlib
except ImportError:
    print("❌ 缺少依赖: hashlib，请确保在sillygirl环境中运行")
    exit(1)
try:
    import json
except ImportError:
    print("❌ 缺少依赖: json，请确保在sillygirl环境中运行")
    exit(1)
try:
    import time
except ImportError:
    print("❌ 缺少依赖: time，请确保在sillygirl环境中运行")
    exit(1)
try:
    import base64
except ImportError:
    print("❌ 缺少依赖: base64，请确保在sillygirl环境中运行")
    exit(1)
from datetime import datetime, timedelta
from urllib.parse import unquote, quote
from typing import Optional


import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

senderID = sg.getSenderID()  # 获取发送者QQ号
sender = sg.Sender(senderID)  # 获取发送者对象
userid = sender.getUserID()  # 存储当前发送者的用户 ID，与 senderID 类似，但通常用于内部标识
uservalue = sg.bucketGet(bucket=f'{bucket_prefix}.user', key=userid)
today_date = datetime.now().date()
today_time = str(today_date)


MAX_RETRIES = 10  # 最大重试次数
IS_PROXY = sg.bucketGet(bucket_prefix, 'is_proxy')  # 是否启用代理True
PROXY_API = sg.bucketGet(bucket_prefix, 'proxy_pool')
proxy = None  # 初始化全局代理变量


def update_proxy():
    """更新代理IP地址"""
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
    """手机号脱敏处理"""
    if not phone or len(phone) != 11:
        return phone
    return f"{phone[:3]}****{phone[7:]}"

def is_valid_phone(phone):
    """验证手机号格式是否正确
    Args:
        phone: 待验证的手机号字符串
    Returns:
        bool: 格式正确返回True，否则返回False
    """
    if not phone or not isinstance(phone, str):
        return False
    pattern = r'^1[3-9]\d{9}$'    # 中国大陆手机号正则表达式：以1开头，第二位3-9，后面9位数字
    return re.match(pattern, phone) is not None


OCR_ENABLED = True  # 是否启用OCR自动识别（默认开启）
OCR_SERVER = sg.bucketGet('mrconli.config', 'ddddocr') or "http://116.208.9.161:7777"
OCR_API_URL = f"{OCR_SERVER}/classification"
OCR_TIMEOUT = 10  # OCR请求超时时间（秒）
OCR_RETRY = 3  # OCR识别失败重试次数

CLIENT_ID = '10016'
TENANT_ID = '62'
SIGNATURE_SALT = 'FR*r!isE5W'


def generate_random_device_info() -> str:
    android_v = random.choice(["10", "11", "12", "13", "14", "15"])
    model = random.choice(["SM-G998B", "V2049A", "M2102K1C", "PGM110", "PD2241"])
    build_id = f"{random.choice(['RP1A', 'SP1A', 'TP1A'])}.{random.randint(100000, 999999)}.0{random.randint(10, 99)}"
    chrome_v = f"{random.randint(110, 144)}.0.{random.randint(5000, 8000)}.132"
    return f"Mozilla/5.0 (Linux; Android {android_v}; {model} Build/{build_id}; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/{chrome_v} Mobile Safari/537.36;xsb_xianju;xsb_xianju;2.1.3;native_app;7.8.0"


class AiXianJu_SMS:
    def __init__(self):
        self.session = requests.Session()
        self.user_agent = None
        self.req_id = None
        self._init_session()

    def _init_session(self):
        """初始化session，访问首页获取必要的cookies和session状态"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            self.session.get(
                "https://passport.tmuyun.com/",
                headers=headers,
                timeout=10,
                verify=False
            )
            acw_tc = ''.join(random.choices('0123456789abcdef', k=40))
            self.session.cookies.set('acw_tc', acw_tc)
            jsessionid = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
            self.session.cookies.set('JSESSIONID', jsessionid)
            self.session.cookies.set('client_id', CLIENT_ID)
        except Exception as e:
            print(f"⚠️ 初始化session失败: {e}")

    def generate_uuid(self):
        return str(uuid.uuid4())

    def generate_user_agent(self):
        if self.user_agent:
            return self.user_agent

        models = [
            {'model': 'OnePlus PLC110', 'brand': 'xiaomi'},
            {'model': 'SM-G998B', 'brand': 'samsung'},
            {'model': 'V2049A', 'brand': 'vivo'},
            {'model': 'M2102K1C', 'brand': 'xiaomi'},
            {'model': 'PGM110', 'brand': 'OPPO'},
            {'model': 'PD2241', 'brand': 'vivo'}
        ]

        device = random.choice(models)
        android_v = random.randint(10, 16)

        uuid_suffix = self.generate_uuid()[9:]
        device_id = f"00000000-{uuid_suffix}"
        self.device_id = device_id  # 保存为实例属性

        self.user_agent = f"2.1.3;{device_id};{device['model']};Android;{android_v};{device['brand']};7.8.0"
        return self.user_agent

    def generate_signature(self, path, session_id, request_id, timestamp):
        clean_path = path[7:] if path.startswith('/api/v1') else path
        sign_string = f"{clean_path}&&{session_id}&&{request_id}&&{timestamp}&&{SIGNATURE_SALT}&&{TENANT_ID}"
        return hashlib.sha256(sign_string.encode()).hexdigest()

    def make_request(self, url, method='GET', data=None, custom_headers=None):
        headers = {
            'User-Agent': self.generate_user_agent(),
            'Accept-Encoding': 'gzip',
            'Connection': 'Keep-Alive',
            'Cache-Control': 'no-cache',
        }

        if custom_headers:
            headers.update(custom_headers)

        try:
            if method == 'GET':
                response = self.session.get(url, headers=headers, verify=False, timeout=30)
            else:
                response = self.session.post(url, data=data, headers=headers, verify=False, timeout=30)
            return {'code': response.status_code, 'body': response.content, 'text': response.text, 'error': None}
        except Exception as e:
            return {'code': 0, 'body': b'', 'text': '', 'error': str(e)}

    def get_captcha(self):
        dummy_data = {
            'captcha': '0000',
            'client_id': CLIENT_ID,
            'phone_number': ''
        }
        self.make_request(
            "https://passport.tmuyun.com/web/security/send_security_code",
            "POST",
            dummy_data,
            {
                "X-REQUEST-ID": self.generate_uuid(),
                "X-SIGNATURE": hashlib.sha256(f"{self.generate_uuid()}{time.time()}".encode()).hexdigest(),
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
            }
        )

        self.req_id = self.generate_uuid()
        res = self.make_request(
            "https://passport.tmuyun.com/web/security/captcha_image",
            "GET",
            None,
            {"X-REQUEST-ID": self.req_id}
        )
        if res['code'] == 200 and res['body']:
            body_bytes = res['body']
            if body_bytes[:3] == b'GIF' or b'PNG' in body_bytes or b'JFIF' in body_bytes:
                captcha_text = ""
                if OCR_ENABLED:
                    for attempt in range(OCR_RETRY):
                        try:
                            b64_image = base64.b64encode(body_bytes).decode()
                            ocr_res = requests.post(
                                OCR_API_URL,
                                json={'image': b64_image},
                                headers={'Content-Type': 'application/json'},
                                timeout=OCR_TIMEOUT
                            )
                            if ocr_res.status_code == 200:
                                raw_text = ocr_res.text.strip()
                                try:
                                    import json
                                    json_data = json.loads(raw_text)
                                    if isinstance(json_data, dict) and 'result' in json_data:
                                        raw_text = str(json_data['result'])
                                    elif isinstance(json_data, dict) and 'data' in json_data:
                                        raw_text = str(json_data['data'])
                                    else:
                                        raw_text = str(json_data)
                                except:
                                    pass
                                captcha_text = raw_text.replace(' ', '').lower()
                                for prefix in ['result', 'code', 'captcha', 'text']:
                                    if captcha_text.startswith(prefix):
                                        captcha_text = captcha_text[len(prefix):]
                                captcha_text = ''.join(c for c in captcha_text if c.isalnum())
                                print(f"✅ OCR识别成功: {captcha_text}")
                                break
                            else:
                                print(f"⚠️ OCR服务返回错误: {ocr_res.status_code}")
                                try:
                                    print(f"   响应内容: {ocr_res.text[:200]}")
                                except:
                                    pass
                                if attempt < OCR_RETRY - 1:
                                    print(f"🔄 第{attempt + 2}次重试...")
                                    time.sleep(1)
                        except requests.exceptions.ConnectionError:
                            print(f"❌ OCR服务连接失败: {OCR_API_URL}")
                            if attempt < OCR_RETRY - 1:
                                print(f"🔄 第{attempt + 2}次重试...")
                                time.sleep(1)
                        except requests.exceptions.Timeout:
                            print(f"⏱️ OCR服务请求超时")
                            if attempt < OCR_RETRY - 1:
                                print(f"🔄 第{attempt + 2}次重试...")
                                time.sleep(1)
                        except Exception as e:
                            print(f"⚠️ OCR识别失败: {e}")
                            if attempt < OCR_RETRY - 1:
                                print(f"🔄 第{attempt + 2}次重试...")
                                time.sleep(1)

                return {'success': True, 'captcha': captcha_text}
            else:
                return {'success': False, 'msg': "返回数据非图片格式"}
        return {'success': False, 'msg': f"获取图形失败 HTTP {res['code']}"}

    def get_captcha_auto(self):
        """自动获取并识别验证码，失败时自动重试"""
        max_attempts = 3
        for attempt in range(max_attempts):
            result = self.get_captcha()
            if result['success'] and result.get('captcha') and len(result['captcha']) >= 4:
                return result
            print(f"🔄 验证码识别失败或结果无效，第{attempt + 2}次尝试...")
            time.sleep(1)
        return {'success': False, 'msg': '验证码识别失败，已达最大重试次数'}

    def send_sms(self, phone, captcha):
        req_id = self.generate_uuid()
        sig = hashlib.sha256(f"{self.generate_uuid()}{time.time()}".encode()).hexdigest()

        data = {
            'captcha': captcha,
            'client_id': CLIENT_ID,
            'phone_number': phone
        }

        res = self.make_request(
            "https://passport.tmuyun.com/web/security/send_security_code",
            "POST",
            data,
            {
                "X-REQUEST-ID": req_id,
                "X-SIGNATURE": sig,
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
            }
        )

        if res['text']:
            try:
                return __import__('json').loads(res['text'])
            except:
                return {'code': -1, 'msg': res['text']}
        return {'code': -1, 'msg': f"请求失败 {res['code']}"}

    def login(self, phone, code):
        req_id = self.generate_uuid()
        sig = hashlib.sha256(f"{self.generate_uuid()}{time.time()}".encode()).hexdigest()

        data1 = {
            'client_id': CLIENT_ID,
            'phone_number': phone,
            'security_code': code
        }

        res1 = self.make_request(
            "https://passport.tmuyun.com/web/oauth/security_code_auth",
            "POST",
            data1,
            {
                "X-REQUEST-ID": req_id,
                "X-SIGNATURE": sig,
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
            }
        )

        try:
            json1 = __import__('json').loads(res1['text'])
        except:
            return {'code': -1, 'msg': '解析响应失败', 'raw': res1.get('text', '')}

        if 'data' not in json1 or 'authorization_code' not in json1.get('data', {}) or 'code' not in json1['data'].get('authorization_code', {}):
            return {'code': -1, 'msg': '短信验证失败或过期', 'raw': json1}

        auth_code = json1['data']['authorization_code']['code']

        mock_session_id = "68ff31bd3cbc283c4ca83496"
        path10 = "/api/zbtxz/login"
        req_id10 = self.generate_uuid()
        timestamp10 = str(int(time.time() * 1000))
        sig10 = self.generate_signature(path10, mock_session_id, req_id10, timestamp10)

        data10 = {
            'check_token': '',
            'code': auth_code,
            'token': '',
            'type': '-1',
            'union_id': ''
        }

        res10 = self.make_request(
            f"https://vapp.tmuyun.com{path10}",
            "POST",
            data10,
            {
                "X-SESSION-ID": mock_session_id,
                "X-REQUEST-ID": req_id10,
                "X-TIMESTAMP": timestamp10,
                "X-SIGNATURE": sig10,
                "X-TENANT-ID": TENANT_ID,
                "X-Requested-With": "com.increator.cc.xianjusmk",
                "Accept": "application/json, text/plain, */*",
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )

        if res10['text']:
            try:
                return __import__('json').loads(res10['text'])
            except:
                return {'code': -1, 'msg': res10['text']}
        return {'code': -1, 'msg': f"终极请求失败 {res10['code']}"}


class AiXianJu:
    """查询用户信息类"""
    Q_VALUE = "1GwxSBurLoUdKeZiyHuqn7u0cv2qTf081Qj/sdyPH2E="
    BASE_URL = "https://vapp.tmuyun.com"
    SIGNATURE_SALT = "FR*r!isE5W"
    TENANT_ID = "62"

    def __init__(self, session_id: str, account_id: str, device_id = None, user_agent=None):
        """初始化权益钱包类"""
        self.account_id = account_id
        self.session_id = session_id
        self.user_agent = user_agent or 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;;xsb;xsb_xianju;2.1.3;Appstore;native_app;7.8.0'
        self.activity_token = None
        self.equity_token = None
        self.q_value = None
        self.u_value = None
        self.nickname = None
        self.phone = None
        self.device_id = device_id
        self.base_headers = {
            "User-Agent": self.user_agent,
            "Accept": "application/json, text/plain, */*",
            "sec-ch-ua": '"Chromium";v="118", "Android WebView";v="118", "Not=A?Brand";v="99"',
            "sec-ch-ua-platform": '"Android"',
            "X-Requested-With": "com.increator.cc.xianjusmk",
            "X-TENANT-ID": self.TENANT_ID,
        }


    def get_phone(self):
        """获取手机号"""
        request_id = str(uuid.uuid4())
        timestamp = str(int(time.time() * 1000))

        path = "/api/user_mumber/numberCenter"
        if path.startswith("/api/v1"):
            path = path.replace("/api/v1", "")
        sign_string = f"{path}&&{self.session_id}&&{request_id}&&{timestamp}&&FR*r!isE5W&&62"
        signature = hashlib.sha256(sign_string.encode('utf-8')).hexdigest()

        headers = self.base_headers.copy()
        headers.update({
            "X-SESSION-ID": self.session_id,
            "X-REQUEST-ID": request_id,
            "X-TIMESTAMP": timestamp,
            "X-SIGNATURE": signature,
            "X-ACCOUNT-ID": self.account_id,
        })
        url = f"{self.BASE_URL}{path}"
        try:
            response = requests.get(url, headers=headers, params={"is_new": 1}, timeout=15, verify=False)
            response.raise_for_status()
            member_info = response.json()
            if member_info and "error" not in member_info:
                data = member_info.get("data", {}).get("rst", {}) or {}
                if data:
                    mobile = data.get('mobile', '')
                    self.phone = mobile
                    return True, self.phone
                else:
                    print("❌ 获取手机号失败: 响应中无手机号")
                    return False, None
            else:
                print(f"❌ 获取手机号失败: {member_info}")
                return False, None
        except Exception as e:
            print(f"❌ 请求失败: {str(e)}")
            return False, None


    def get_activity_token(self):
        """获取活动系统令牌"""
        url = "https://act.tmlyun.com/activity-api/lottery/api/auth/userLogin"
        headers = {
            'Sec-Fetch-Dest': 'empty',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'Sec-Fetch-Site': 'same-origin',
            'Origin': 'https://act.tmlyun.com',
            'User-Agent': self.user_agent,
            'Sec-Fetch-Mode': 'cors',
            'Host': 'act.tmlyun.com',
            'Referer': f'https://act.tmlyun.com/lottery/?q={self.Q_VALUE}',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Accept': 'application/json, text/plain, */*'
        }
        body = {
            "q": self.Q_VALUE,
            "accountId": self.account_id,
            "sessionId": self.session_id,
            "tenantCode": "xsb_xianju"
        }
        try:
            response = requests.post(
                url,
                headers=headers,
                json=body,
                timeout=15,
                verify=False
            )
            result = response.json()
            if result.get("success"):
                token = result.get("data", {}).get("token", "")
                q_value = result.get("data", {}).get("q", "")
                nickName = result.get("data", {}).get("nickName", "")
                self.activity_token = token
                self.q_value = q_value
                self.nickname = nickName
                return token
            else:
                print("❌ 获取活动token失败: 响应中无token")
                return None
        except Exception as e:
            print(f"❌ 获取活动token异常: {e}")
            return None

    def get_u(self, task_token=None):
        """获取u参数"""
        token = task_token or self.activity_token
        if not token:
            print("❌ 缺少活动token")
            return None
        url = "https://act.tmlyun.com/activity-api/lottery/h5/activity/lottery/accountPrizeRecord/jumpEquityWallet"
        headers = {
            'Sec-Fetch-Dest': 'empty',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': self.user_agent,
            'Authorization': token,
            'Sec-Fetch-Mode': 'cors',
            'Referer': f'https://act.tmlyun.com/lottery/prizeRecord?q={self.Q_VALUE}',
            'Host': 'act.tmlyun.com',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Accept': 'application/json, text/plain, */*'
        }
        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=15,
                verify=False
            )
            result = response.json()
            if result.get("code") == 0:
                data = result.get("data", "")
                if data:
                    u_part = data.split("u=")[1].split("&")[0]
                    u_value = unquote(u_part)
                    self.u_value = u_value
                    return u_value
                else:
                    print("❌ 获取u参数失败: 响应数据为空")
                    return None
            else:
                print(f"❌ 获取u参数失败: {result.get('message', '未知错误')}")
                return None
        except Exception as e:
            print(f"❌ 获取u参数异常: {e}")
            return None

    def login(self, u=None):
        """登录权益钱包"""
        login_url = "https://my.tmlyun.com/equity-api/user/auth/userLogin"
        login_headers = {
            'Sec-Fetch-Dest': 'empty',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'Sec-Fetch-Site': 'same-origin',
            'Origin': 'https://my.tmlyun.com',
            'User-Agent': self.user_agent,
            'Authorization': '',
            'Sec-Fetch-Mode': 'cors',
            'Host': 'my.tmlyun.com',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Accept': 'application/json, text/plain, */*'
        }

        login_body = {
            "u": u or self.u_value,
            "accountId": self.account_id,
            "sessionId": self.session_id
        }

        if not login_body["u"]:
            print("❌ 缺少u参数")
            sender.reply("❌ 缺少u参数")
            return None

        try:
            response = requests.post(
                login_url,
                headers=login_headers,
                json=login_body,
                timeout=15,
                verify=False
            )
            try:
                login_result = response.json()
                sender.reply(login_result)
                if login_result.get("success"):
                    token = login_result.get("data", {}).get("token", "")
                    if token:
                        self.equity_token = token

                        return token
                    else:
                        print("❌ 登录成功但无token")

                        return None
                else:
                    print(f"\n❌ 登录失败: {login_result.get('message', '未知错误')}")
                    return None
            except json.JSONDecodeError:
                print("❌ 登录响应解析失败")
                print(response.text)
                return None
        except requests.exceptions.RequestException as e:
            print(f"\n❌ 登录请求失败: {e}")
            return None

    def get_wallet_info(self, token=None):
        """获取钱包信息"""
        equity_token = token or self.equity_token
        if not equity_token:
            sender.reply("❌ 缺少权益钱包token")
            return None, None
        device_id = self.device_id or f"device_{random.randint(100000, 999999)}"
        wallet_url = f"https://my.tmlyun.com/equity-api/redBag/getWalletInfo?device={device_id}"
        mingxi_url = "https://my.tmlyun.com/equity-api/redBag/pageWalletDetail?current=1&pageSize=10&fundsChannelType=0"
        wallet_headers = {
            'Sec-Fetch-Dest': 'empty',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'Sec-Fetch-Site': 'same-origin',
            'Origin': 'https://my.tmlyun.com',
            'User-Agent': self.user_agent,
            'Authorization': equity_token,
            'Sec-Fetch-Mode': 'cors',
            'Host': 'my.tmlyun.com',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Accept': 'application/json, text/plain, */*'
        }
        if self.u_value:
            wallet_headers['Referer'] = f"https://my.tmlyun.com/equitypacket/?u={quote(self.u_value)}"
        try:
            wallet_response = requests.get(
                wallet_url,
                headers=wallet_headers,
                timeout=15,
                verify=False
            )
            mingxi_response = requests.get(
                mingxi_url,
                headers=wallet_headers,
                timeout=15,
                verify=False
            )
            try:
                wallet_result = wallet_response.json()
                if wallet_result.get("success"):
                    data_list = wallet_result.get("data") or []
                    if data_list:
                        data = data_list[0] if data_list[0] else {}
                        total = data.get('totalPrice', 0)
                        trans = data.get('totalTransPrice', 0)
                        bal = data.get('aliPayTotalPrice', 0)
                        wallet_msg = f"💰 余额: {bal}元\n🧧 提现: {trans}元\n📊 累计: {total}元"
                    else:
                        wallet_msg = "钱包数据为空"
                else:
                    err_msg = wallet_result.get('message', '未知错误')
                    wallet_msg = f"钱包余额查询失败: {err_msg}"
                mingxi_result = mingxi_response.json()
                mingxi_msg = f"🎁 最近中奖记录:"
                if mingxi_result.get("success"):
                    prize_list = mingxi_result.get("data",[])
                    if prize_list:

                        for prize in prize_list:
                            price = prize.get("price")
                            createdAt = prize.get("createdAt")
                            status = prize.get("status")
                            if status == "发放成功":
                                mingxi_msg += f"\n  - [{price}]{createdAt}"
                    else:
                        mingxi_msg += "\n暂无中奖记录"
                else:
                    mingxi_msg += "\n获取中奖记录失败"
                return wallet_msg, mingxi_msg
            except json.JSONDecodeError as e:
                print("❌ 钱包响应解析失败")
                print(wallet_response.text)
                return wallet_msg, mingxi_msg
        except Exception as e:
            print(f"\n❌ 查询失败: {e}")
            return wallet_msg, mingxi_msg


    def process_lottery_and_reading(self):
        """处理抽奖和阅读任务"""
        task_token = self._get_task_token(self.Q_VALUE)
        if not task_token:
            print("⚠️ 获取任务Token失败，跳过抽奖任务。")
            return False, "获取任务Token失败"
        success, msg = self.execute_daily_reading(task_token)
        return True, msg

    def _get_task_token(self, q_val: str) -> Optional[str]:
        """获取任务token"""
        headers = self.base_headers.copy()
        headers.update({"Content-Type": "application/json"})
        try:
            response = requests.post(
                "https://act.tmlyun.com/activity-api/task/h5/auth/userLogin",
                headers=headers,
                json={"q": q_val, "accountId": self.account_id, "sessionId": self.session_id, "tenantCode": "xsb_xianju"},
                timeout=15,
                verify=False
            )
            response.raise_for_status()
            res = response.json()
            self.token = res.get("data", {}).get("token") if res else None
            return self.token
        except requests.exceptions.RequestException as e:
            print(f"❌ 请求失败: {str(e)}")
            return None


    def execute_daily_reading(self, task_token: str):
        """执行每日阅读任务"""
        msg = ""
        headers = self.base_headers.copy()
        headers.update({'Authorization': task_token})
        try:
            response = requests.get(
                "https://act.tmlyun.com/activity-api/task/h5/activity/getHomeUserLevelTaskList",
                headers=headers,
                timeout=15,
                verify=False
            )
            response.raise_for_status()
            tasks_response = response.json()

            if not tasks_response or "error" in tasks_response:
                return False, "获取任务列表失败"

            today = datetime.now().strftime('%Y-%m-%d')
            today_task = next((t for t in tasks_response.get("data", []) if t.get("limitTimeStart", "").startswith(today)),
                              None)

            if not today_task:
                print("⚠️ 未找到今日对应的抽奖阅读任务。")
                return False, "无任务"

            task_level_id = today_task.get("taskLevelId", 0)
            msg += f"🎯 今日活动ID: {task_level_id}\n"
            msg += self.get_reading_loop(task_token, task_level_id)
            return True, msg
        except requests.exceptions.RequestException as e:
            print(f"❌ 请求失败: {str(e)}")
            return False, "获取任务列表失败"

    def get_reading_loop(self, task_token: str, level_task_id: int):
        """获取阅读进度"""
        headers = self.base_headers.copy()
        headers.update({'Authorization': task_token})
        try:
            response = requests.get(
                f"https://act.tmlyun.com/activity-api/task/h5/activity/getLevelTaskUserList?levelTaskId={level_task_id}",
                headers=headers,
                timeout=15,
                verify=False
            )
            response.raise_for_status()
            detail = response.json()
            read_task = next((t for t in detail.get("data", {}).get("appBaseList", []) if t.get("name") == "阅读文章"),
                                 None)
            status = read_task.get("taskUserStatusBO", {}) if read_task else {}
            complete_num, total = status.get("completeNum", 0), status.get("total", 0)
            msg = f"📋 阅读进度: {complete_num} / {total}"
            return msg
        except requests.exceptions.RequestException as e:
            print(f"❌ 请求失败: {str(e)}")
            return "获取阅读进度失败"


    def run(self, u=None):
        """运行完整流程"""
        try:
            success, phone = self.get_phone()
            if success:
                self.phone = phone
                if not self.activity_token:
                    self.get_activity_token()

                if not self.u_value:
                    self.get_u()

                self.login(u)

                wallet_msg, mingxi_msg = self.get_wallet_info()
                success, message = self.process_lottery_and_reading()
                return True, phone, wallet_msg, mingxi_msg, message
            else:
                return False, None, None, None, None
        except Exception as e:
            print(f"❌ run方法执行异常: {e}")
            return False, None, None, None, None


def bind():
    """账号登录"""
    login_guide = """
=====登录方式=====
[1] 短信登录
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
            sms_login()
        elif choice == '2':
            batch_login()
        else:
            sender.reply("❌ 无效的选择")
            return
    except Exception as e:
        sender.reply(f"❌ 登录失败: {str(e)}")
        return

def sms_login():
    """短信验证码登录"""
    sender.reply(
        f"""=={scripts_name}短信登录===
📱 请输入手机号
⭐ 输入q退出操作
====================="""
    )
    axj_sms = AiXianJu_SMS()
    phone = sender.input(120000, 1, True).strip()  # 私聊模式
    if not phone:
        sender.reply('❌ 输入超时！')
        return
    elif phone.lower() == 'q':
        sender.reply('❌ 已取消操作')
        return
    if not re.match(r'^1[3-9]\d{9}$', phone):
        sender.reply('❌ 手机号格式不正确，请重新输入')
        return

    result = axj_sms.get_captcha_auto()
    if not result['success']:
        sender.reply(f"❌ {result.get('msg', '获取图形验证码错误')}")
        return
    captcha = result.get('captcha', '')
    if not captcha:
        sender.reply(f"❌ 验证码识别失败，结果无效，已重试3次")
        return
    sms_result = axj_sms.send_sms(phone, captcha)
    if sms_result.get('code') != 0:
        sender.reply(f"❌ 获取短信验证码失败: {sms_result.get('message', sms_result.get('msg', '未知错误'))}")
        return

    sender.reply(
        """=====请输入验证码=====
📝 请输入收到的6位验证码
⭐ 输入q退出操作
====================="""
    )
    sms_code = sender.input(120000, 1, True).strip()  # 2分钟超时
    if not sms_code:
        sender.reply('❌ 输入超时！')
        return
    elif sms_code.lower() == 'q':
        sender.reply('❌ 已取消操作')
        return
    if not re.match(r'^\d{6}$', sms_code):
        sender.reply('❌ 验证码格式不正确，请重新输入')
        return
    login_result = axj_sms.login(phone, sms_code)
    if login_result.get('code') == 0 and login_result.get('data', {}).get('session'):
        session_id = login_result['data']['session']['id']
        account_id = login_result['data']['session']['account_id']
        device_id = axj_sms.device_id
        user_agent = axj_sms.user_agent
        token = f"{session_id}#{account_id}#{device_id}#{user_agent}"

        sg.bucketSet(f'{bucket_prefix}.token', phone, token)
        current_accounts = _sg_literal(sg.bucketGet(f'{bucket_prefix}.user', userid) or '[]')
        if phone not in current_accounts:
            status = f"{scripts_name}登录成功"
            accountVip = '2099-12-31'
            if not accountVip or accountVip < today_time:
                accountVip = f"❌ 未授权"
            current_accounts.append(phone)
            sg.bucketSet(f'{bucket_prefix}.user', userid, json.dumps(current_accounts, ensure_ascii=False))
        else:
            status = f"{scripts_name}更新成功"
            accountVip = '2099-12-31'
            if not accountVip or accountVip < today_time:
                accountVip = f"❌ 未授权"
                sender.reply(f"⚠️ 账号未授权或授权已过期，环境变量未提交青龙...")
            else:
                add_to_qinglong(token, phone, userid)
        sender.reply(f"""
====={status}=====
📱 账号: {mask_phone(phone)}
⏰ 授权到期：{accountVip}
=====================""")
    else:
        token = None
        sender.reply('❌ 登录失败，请稍后重试')
        return


def batch_login():
    """批量登录函数"""
    global uservalue
    sender.reply(
        f"======={login_cmd}=======\n"
        "📝 请输入ck参数: session_id#account_id#client_id#user_agent\n"
        "说明:\n"
        "  1. 支持批量，一个账号一行\n"
        "  2.至少包含session_id#account_id\n"
        "  3.client_id和user_agent可以随机生成\n"
        "  4. user_agent格式示例：\n"
        "     2.1.3;A60BCXXX9-XXXX-4413-9D32-0A709D68XXXXXXXX;iPhone18,1;IOS;26.2;Appstore;7.8.0\n"
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
            if '#' not in account:
                fail_count += 1
                error_reasons.append(f"❌ {account} 格式错误")
                continue
            patrs = account.split('#')
            if len(patrs) == 2:
                session_id, account_id = patrs
                device_id = str(uuid.uuid4())
                user_agent = generate_random_device_info()
            elif len(patrs) == 4:
                session_id, account_id, device_id, user_agent = patrs
            else:
                fail_count += 1
                error_reasons.append(f"❌ {account} 格式错误")
                continue
            if not session_id or not account_id or not device_id or not user_agent:
                fail_count += 1
                error_reasons.append(f"❌ {account} 格式错误")
                continue
            wallet = AiXianJu(session_id, account_id, device_id, user_agent)
            success, mobile, wallet_msg, mingxi_msg, message = wallet.run()
            if not success:
                fail_count += 1
                error_reasons.append(f"❌ {account} 登录认证失败")
                continue
            if success:
                phone = str(mobile)
                success_count += 1
                token = f"{session_id}#{account_id}#{device_id}#{user_agent}"
                sg.bucketSet(f'{bucket_prefix}.token', phone, token)
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
                        sender.reply(f"⚠️ 账号未授权或授权已过期，环境变量未提交青龙...")
                    else:
                        add_to_qinglong(token, phone, userid)
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
        menu = "=====请选择查询账号=====\n[0] 查询全部账号\n------------------\n"
        for idx, acc in enumerate(accounts, 1):
            menu += f"[{idx}] {mask_phone(acc)} \n"
        menu += "====================\n⚠️ 请回复数字序号(输入q退出)"
        sender.reply(menu)

        choice = sender.input(30000, 1, False)
        if not choice:
            sender.reply('❌ 输入超时！')
            return
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
        sender.reply(f'正在查询全部{scripts_name}账号...')
    else:
        target_accounts = [accounts[choice - 1]]

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
                session_id, account_id, device_id, user_agent = token.split('#')
                axj = AiXianJu(session_id, account_id, device_id, user_agent)
                success, phone, wallet_msg, mingxi_msg, message = axj.run()
                if not success:
                    sender.reply(f'❌ 【{mask_phone(account)}】查询失败')
                    continue
                sender.reply(f"""
====={full_scripts_name}详情=====
📱 账号：{mask_phone(account)}
{wallet_msg}
⏰ 授权到期：{accountVip}
----------------
{message}
----------------
{mingxi_msg}
==================""")
        except Exception as e:
            sender.reply(f'❌ 【{mask_phone(account)}】查询出错: {str(e)}')


def get_user_info(token):
    try:
        parts = str(token or "").split("#")
        if len(parts) >= 4:
            success, phone, _wallet, _detail, _message = AiXianJu(parts[0], parts[1], parts[2], parts[3]).run()
            return success, phone, "", "0"
    except Exception:
        pass
    return False, "", "", "0"

def cron_task():
    """定时任务处理"""
    if imtype != 'fake':
        return
    try:
        users = sg.bucketAllKeys(f'{bucket_prefix}.user')
        for user in users:
            accounts = _sg_literal(sg.bucketGet(f'{bucket_prefix}.user', user) or '[]')
            for account in accounts:
                try:
                    auth = '2099-12-31'
                    if auth and auth <= today:
                        delete_from_qinglong(account)
                        notify_user(user, account, "授权已过期,环境变量已删除,请及时续费")
                        continue
                    token =  sg.bucketGet(f'{bucket_prefix}.token', account)
                    if not token:
                        continue
                    success, phone, nickname, exchange = get_user_info(token)
                    if not success:
                        notify_user(user, account, "ck失效,请及时更新")
                        delete_from_qinglong(account)
                        continue
                    exchange_num = round(float(exchange), 1)
                    if exchange_num > 0.3:
                        notify_user(user, account, f"余额已到{exchange}元，可以提现了")
                except Exception as e:
                    print(f"处理账号 {account} 出错: {str(e)}")
                    continue
    except Exception as e:
        print(f"定时任务出错: {str(e)}")


def notify_user(user, account, message):
    """发送用户通知"""
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
    """获取插件配置"""
    try:
        var_name = sg.bucketGet(bucket_prefix, 'var_name') or "m_axj"
        if not var_name:
            print("未配置变量名，使用默认值: m_axj")
            var_name = 'm_axj'
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
    """初始化青龙连接"""
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
                elif env['name'] == var_name and env['value'] == token:  # 新增重复值检测
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
    accounts = _sg_literal(sg.bucketGet(bucket=f'{bucket_prefix}.user', key=userid))
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
[02] 查看全部账号ck
------------------
账号列表:"""
    for i, account in enumerate(accounts, 1):
        token = sg.bucketGet(f'{bucket_prefix}.token', account)
        auth = '2099-12-31'
        auth_status = "✅ 已授权" if auth and auth > today else "❌ 未授权"
        account_list += f"\n[{i}] {mask_phone(account)}\n    {auth_status}"
        if auth and auth > today:
            account_list += f"\n    授权到期: {auth}"
    account_list += "\n------------------\n回复数字选择账号\n回复'q'退出"

    sender.reply(account_list)
    choice = sender.listen(60000)

    if not choice:
        sender.reply("❌ 操作超时")
        return
    elif choice == 'q' or choice == 'Q':
        sender.reply("✅ 已取消操作")
        return
    try:
        if choice == '01':
            for account in accounts:
                delete_account(account)
            sg.bucketSet(f'{bucket_prefix}.user', userid, '[]')
            sender.reply("✅ 已删除全部账号")
        elif choice == '02':
            for account in accounts:
                show_ck(account)
        elif choice == '00':
            sender.reply("📝 请输入授权天数(如使用积分兑换，必须为30的倍数):")
            days = sender.listen(60000)
            if not days:
                sender.reply("❌ 操作超时")
                return
            elif days == 'q' or days == 'Q':
                sender.reply("✅ 已取消授权")
                return
            coin_bucket = sg.bucketGet(bucket_prefix, 'coin_bucket') or 'dd_sign_points'
            coin_price = int(sg.bucketGet(bucket_prefix, 'coin') or '0')  # 确保获取最新积分价格
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
                            token = sg.bucketGet(f'{bucket_prefix}.token', account)

                            if token:
                                add_to_qinglong(token, account, userid)
                            success_count += 1
                        sender.reply(f"""
=====批量授权成功=====
💰 支付: {amount}元
⏰ 时长: {days}天
✅ 成功: {success_count}个账号
====================""")

                elif pay_choice == '2':
                    coin_bucket = sg.bucketGet(bucket_prefix, 'coin_bucket') or 'dd_sign_points'
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
                        token = sg.bucketGet(f'{bucket_prefix}.token', account)

                        if token:
                            add_to_qinglong(token, account, userid)
                        success_count += 1
                    sender.reply(f"""
=====批量授权成功=====
💰 消耗: {need_coin}积分
⏰ 时长: {days}天
✅ 成功: {success_count}个账号
💵 剩余: {new_coin}积分
====================""")

                for account in accounts:
                    env_id_str = sg.bucketGet(f'{bucket_prefix}.env_id', account)
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
    auth = '2099-12-31'
    auth_status = "✅ 已授权" if auth and auth > today else "❌ 未授权"
    auth_info = f"\n    到期: {auth}" if auth and auth > today else ""
    menu = f"""
=====账号操作=====
📱 账号: {mask_phone(account)}
🔐 状态: {auth_status}{auth_info}
------------------
[1] 授权账号
[2] 删除账号
[3] 查看账号ck
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
            show_ck(account)
        else:
            sender.reply("❌ 无效的选择")
    except Exception as e:
        sender.reply(f"❌ 操作失败: {str(e)}")


def auth_account(account):
    """账号授权"""
    try:
        price = Decimal(sg.bucketGet(bucket_prefix, 'price') or '1')   #  每月价格
        coin_bucket = sg.bucketGet(bucket_prefix, 'coin_bucket') or 'dd_sign_points'
        user_coin = sg.bucketGet(coin_bucket, userid) or '0'
        user_coin = Decimal(user_coin)  # 使用 Decimal 处理大数值
        month_coin = Decimal(coin_price)  # 从配置获取每月所需积分

        if price == 0:
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
            auth_time = calculate_auth_time(account, days / 30)
            True
            token = sg.bucketGet(f'{bucket_prefix}.token', account)
            if token:
                add_to_qinglong(token, account, userid)  # 强制更新变量
            else:
                sender.reply("⚠️ token获取失败，请检查配置")
            env_id_str = sg.bucketGet(f'{bucket_prefix}.env_id', account)
            if env_id_str:
                env_ids = json.loads(env_id_str)
                enable_in_qinglong(env_ids)
            sender.reply(f"""
=====授权成功=====
📱 账号: {mask_phone(account)}
⏰ 时长: {days}天
📅 到期: {auth_time}
==================""")
            return True
        if month_coin <= 0:
            auth_guide = """
=====授权方式=====
[1] 微信支付
------------------
💰 现金比例: {price}元/30天
回复数字选择方式
回复"q"退出"""
        else:
            auth_guide = f"""
=====授权方式=====
[1] 微信支付
[2] 积分支付 (当前积分: {user_coin})
------------------
💰 现金比例: {price}元/30天
🌸 积分比例: {month_coin}积分/月
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

            if amount == 0:
                auth_time = calculate_auth_time(account, days / 30)
                True
                token = sg.bucketGet(f'{bucket_prefix}.token', account)
                if token:
                    add_to_qinglong(token, account, userid)  # 强制更新变量
                else:
                    sender.reply("⚠️ 令牌获取失败，请检查配置")
                env_id_str = sg.bucketGet(f'{bucket_prefix}.env_id', account)
                if env_id_str:
                    env_ids = json.loads(env_id_str)
                    enable_in_qinglong(env_ids)
                sender.reply(f"""
=====授权成功=====
📱 账号: {mask_phone(account)}
⏰ 时长: {days}天
📅 到期: {auth_time}
==================""")
                return True

            if amount != 0:
                payment_success = process_payment(amount, days)  # 处理支付
                if payment_success:  # 只有在支付成功的情况下才进行授权
                    auth_time = calculate_auth_time(account, days / 30)
                    True
                    token = sg.bucketGet(f'{bucket_prefix}.token', account)
                    if token:
                        add_to_qinglong(token, account, userid)  # 强制更新变量
                    else:
                        sender.reply("⚠️ 令牌获取失败，请检查配置")
                    env_id_str = sg.bucketGet(f'{bucket_prefix}.env_id', account)
                    if env_id_str:
                        env_ids = json.loads(env_id_str)
                        enable_in_qinglong(env_ids)
                    sender.reply(f"""
    =====授权成功=====
    📱 账号: {mask_phone(account)}
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
            token = sg.bucketGet(f'{bucket_prefix}.token', account)

            if token:
                add_to_qinglong(token, account, userid)  # 强制更新变量
            else:
                sender.reply("⚠️ 令牌获取失败，请检查配置")

            env_id_str = sg.bucketGet(f'{bucket_prefix}.env_id', account)
            if env_id_str:
                env_ids = json.loads(env_id_str)
                enable_in_qinglong(env_ids)
            sender.reply(f"""
=====授权成功=====
📱 账号: {mask_phone(account)}
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
        logs = _sg_literal(sg.bucketGet(f'{bucket_prefix}.logs', 'operations') or '[]')
        logs.append(log)
        if len(logs) > 1000:  # 只保留最近1000条
            logs = logs[-1000:]
        sg.bucketSet(f'{bucket_prefix}.logs', 'operations', str(logs))
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
    users = sg.bucketAllKeys(f'{bucket_prefix}.user')
    total_users = len(users)
    total_accounts = 0
    success = 0
    failed = 0
    for user in users:
        accounts = _sg_literal(sg.bucketGet(f'{bucket_prefix}.user', user) or '[]')
        for account in accounts:
            total_accounts += 1
            try:
                token = sg.bucketGet(f'{bucket_prefix}.token', account)
                if token:
                    add_to_qinglong(token, account, user)
                env_ids_str = sg.bucketGet(f'{bucket_prefix}.env_id', account)
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
        users = sg.bucketAllKeys(f'{bucket_prefix}.user')
        success = 0
        failed = 0
        for user in users:
            accounts = _sg_literal(sg.bucketGet(f'{bucket_prefix}.user', user) or '[]')
            for account in accounts:
                try:
                    calculate_auth_time(account, days / 30)
                    True
                    token = sg.bucketGet(f'{bucket_prefix}.token', account)
                    if token:
                        add_to_qinglong(token, account, user)
                    env_ids_str = sg.bucketGet(f'{bucket_prefix}.env_id', account)
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
    accounts = _sg_literal(sg.bucketGet(f'{bucket_prefix}.user', user_id) or '[]')
    if not accounts:
        sender.reply("❌ 未找到该用户的账号")
        return
    account_list = """
=====账号列表=====
[00] 授权全部账号
[01] 修改全部账号授权
----------------"""
    for i, account in enumerate(accounts, 1):
        auth = '2099-12-31'
        status = "✅ 已授权" if auth and auth > today else "❌ 未授权"
        account_list += f"\n[{i}] {mask_phone(account)}\n    {status}"
    account_list += """
------------------
回复数字选择账号
回复"q"退出"""
    sender.reply(account_list)
    choice = sender.listen(60000)
    if not choice:
        sender.reply("❌ 操作超时！")
        return
    if choice == 'q' or choice == 'Q':
        sender.reply("❌ 退出操作！")
        return

    if choice == '00':
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
        for account in accounts:
            try:
                auth_time = calculate_auth_time(account, days / 30)
                True
                token = sg.bucketGet(f'{bucket_prefix}.token', account)
                if token:
                    add_to_qinglong(token, account, user_id)
                env_ids_str = sg.bucketGet(f'{bucket_prefix}.env_id', account)
                if env_ids_str:
                    env_ids = json.loads(env_ids_str)
                    enable_in_qinglong(env_ids)
                log_operation('auth', user_id, account, 'success')
            except Exception as e:
                log_operation('auth', user_id, account, 'failed', str(e))
        sender.reply(f"✅ 已授权所有账号 {days}天")
    elif choice == '01':
        sender.reply("""=====批量修改授权=====
📝 请输入授权日期
格式：2025-01-01
------------------
回复"q"退出""")
        new_auth = sender.listen(60000)
        if not new_auth:
            sender.reply("❌ 操作超时！")
            return
        if new_auth == 'q' or new_auth == 'Q':
            sender.reply("❌ 退出操作！")
            return
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(date_pattern, new_auth):
                sender.reply("❌ 日期格式错误！请使用格式：2025-01-01")
                return
        try:
            datetime.strptime(new_auth, '%Y-%m-%d')
        except ValueError:
            sender.reply("❌ 无效的日期！请检查输入的日期是否正确")
            return
        for account in accounts:
            True
            token = sg.bucketGet(f'{bucket_prefix}.token', account)
            if token:
                add_to_qinglong(token, account, user_id)
            env_ids_str = sg.bucketGet(f'{bucket_prefix}.env_id', account)
            if env_ids_str:
                env_ids = json.loads(env_ids_str)
                enable_in_qinglong(env_ids)
        sender.reply(f"✅ 所有账号授权日期修改为： {new_auth}")

    else:
        try:
            index = int(choice) - 1
            if not 0 <= index < len(accounts):
                raise ValueError()
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
            account = accounts[index]
            auth_time = calculate_auth_time(account, days / 30)
            True
            token = sg.bucketGet(f'{bucket_prefix}.token', account)
            if token:
                add_to_qinglong(token, account, user_id)
            env_ids_str = sg.bucketGet(f'{bucket_prefix}.env_id', account)
            if env_ids_str:
                env_ids = json.loads(env_ids_str)
                enable_in_qinglong(env_ids)
            sender.reply(f"""
=====授权成功=====
📱 账号: {mask_phone(account)}
⏰ 时长: {days}天
📅 到期: {auth_time}
==================""")
            log_operation('auth', user_id, account, 'success')
        except Exception as e:
            sender.reply(f"❌ 授权失败: {str(e)}")
            log_operation('auth', user_id, account, 'failed', str(e))


def delete_account(account):
    """删除账号"""
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
    """查看账号ck"""
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
    """显示使用教程"""
    tutorial_text = (
        f"====={full_scripts_name}教程=====\n"
        "📝 入口:\n"
        "   APP 爱仙居\n"
        "🌟 基础指令:\n"
        f"1. {scripts_name}登录 - 绑定账号\n"
        f"2. {scripts_name}查询 - 查看状态\n"
        f"3. {scripts_name}管理 - 管理账号\n"
        f"4. {scripts_name}授权 - 管理员授权账号\n"
        f"5. {scripts_name}清理 - 管理员清理过期\n"
        "-------------------\n"
        "🚩 收益说明:\n"
        "▸ 阅读抽奖\n"
        "=================="
    )
    sender.reply(tutorial_text)


def main():
    """主函数"""
    message = sender.getMessage()
    if '登录' in message or '登陆' in message or '上车' in message:
        bind_choice = sg.bucketGet(bucket_prefix, 'bind') or "0"
        if bind_choice == "0" or bind_choice == "所有方式":
            bind()
        elif bind_choice == "1" or bind_choice == "仅短信登录":
            sms_login()
        elif bind_choice == "2" or bind_choice == "仅CK登录":
            batch_login()
    elif '管理' in message:
        manage_accounts()
    elif '查询' in message:
        query()
    elif '教程' in message:
        tutorial()
    elif message == f'{scripts_name}清理':
        clean_expired()
    elif message == f'{scripts_name}授权':
        if sender.isAdmin():
            admin_auth()
        else:
            sender.reply("❌ 您不是管理员，无法执行此操作")


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
