# [title: 和合天台]
# [name: heHeTianTai]
# [language: python]
# [class: 任务]
# [author: 8165799]
# [version: v1.8.1]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(和合)(登录|登陆|管理|查询|教程)$|^(登录|登陆|管理|查询)(和合)$]
# [icon: https://api.iconify.design/lucide:bot.svg]
# [description: 和合天台账号登录、积分余额查询、管理与面板同步]
# [depe: ["pycryptodome","requests"]]
import asyncio as _sg_asyncio
import os as _sg_os
import time as _sg_time
import types as _sg_types
from threading import Thread as _sg_Thread
from sillygirl import Adapter as _SGAdapter, Bucket as _SGBucket, Sender as _SGSender, sender as _sg_sender
try:
    import ast as _sg_ast
except Exception:
    _sg_ast = None
try:
    import decimal as decimal
except Exception:
    decimal = None

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

config = None
_CONFIG_FIELD_MAP = {}

import re
import ast
from urllib.parse import unquote
import requests
import time
import json
import hashlib
import logging
import base64
import warnings
import random
import uuid
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

warnings.filterwarnings('ignore', message='Unverified HTTPS request')
requests.packages.urllib3.disable_warnings()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('hhtt_plugin')

REQUEST_TIMEOUT = 30

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = str(sender.getUserID())
usermessage = sender.getMessage()

MAINTENANCE_CK_MAX_WORKERS = 8

PLUGIN_NAME = "和合天台插件"
PLUGIN_NAMESPACE = "dd_hhtt"
PLUGIN_ID = "dd_hhtt:和合天台:v2"

PLUGIN_BUCKET_SUFFIXES = [
    "user",
    "token",
    "auth",
    "remarks",
    "bind_date",
    "remind_log",
    "runtime",
    "sender",
    "imtype",
]

PLUGIN_FOREIGN_BUCKETS = []
PLUGIN_SHARED_BUCKETS = ["dd_sign_points"]
PLUGIN_AUTO_NAMESPACE = False
PLUGIN_NAMESPACE_CANDIDATES = 50

def build_plugin_buckets(namespace, suffixes):
    return [f"{namespace}_{suffix}" for suffix in suffixes]

def plugin_bucket(suffix):
    return f"{PLUGIN_RUNTIME_NAMESPACE}_{suffix}"

def build_namespace_candidates(base_namespace, max_number=50):
    candidates = [base_namespace]
    candidates.extend(f"{base_namespace}{idx}" for idx in range(1, max_number + 1))
    candidates.extend(f"{base_namespace}{ch}" for ch in "abcdefghijklmnopqrstuvwxyz")
    return candidates

def _bucket_has_any_key(bucket_name):
    try:
        return bool(sg.bucketAllKeys(bucket=bucket_name))
    except Exception:
        return False

def assert_automan_bucket_namespace_safe(
    plugin_name,
    namespace,
    plugin_id,
    bucket_suffixes,
    foreign_buckets=None,
    shared_buckets=None,
):
    namespace = str(namespace or "").strip()
    plugin_id = str(plugin_id or "").strip()
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{2,30}", namespace):
        sender.reply(
            f"❌ {plugin_name} 已停止运行：插件命名空间不合法。\n"
            "命名空间只能使用字母、数字、下划线，且必须以字母开头。"
        )
        exit(0)

    foreign_buckets = [str(x).strip() for x in (foreign_buckets or []) if str(x).strip()]
    shared_buckets = set(str(x).strip() for x in (shared_buckets or []) if str(x).strip())
    guard_key = "namespace_owner"

    duplicated_suffixes = sorted({suffix for suffix in bucket_suffixes if bucket_suffixes.count(suffix) > 1})
    if duplicated_suffixes:
        sender.reply(
            f"❌ {plugin_name} 已停止运行：模板内数据桶后缀重复。\n"
            "重复后缀: " + "、".join(duplicated_suffixes)
        )
        exit(0)

    candidates = build_namespace_candidates(namespace, PLUGIN_NAMESPACE_CANDIDATES) if PLUGIN_AUTO_NAMESPACE else [namespace]
    blocked_notes = []
    for candidate in candidates:
        data_buckets = build_plugin_buckets(candidate, bucket_suffixes)
        guard_bucket = f"{candidate}_guard"

        shared_conflicts = sorted(set(data_buckets) & shared_buckets)
        if shared_conflicts:
            sender.reply(
                f"❌ {plugin_name} 已停止运行：独占数据桶不能使用共享积分桶名称。\n"
                "冲突桶: " + "、".join(shared_conflicts)
            )
            exit(0)

        foreign_conflicts = sorted(set(data_buckets) & set(foreign_buckets))
        if foreign_conflicts:
            blocked_notes.append(f"{candidate}: 与已声明其他插件桶重复")
            continue

        try:
            owner = sg.bucketGet(bucket=guard_bucket, key=guard_key)
        except Exception:
            owner = ""
        if owner:
            if str(owner) == plugin_id:
                return candidate
            logger.warning(f"{plugin_name} 检测到旧护栏标记不匹配({owner})，继续使用原数据桶 {candidate}")
            return candidate

        occupied = [bucket for bucket in data_buckets if _bucket_has_any_key(bucket)]
        if occupied:
            if candidate == namespace:
                try:
                    sg.bucketSet(bucket=guard_bucket, key=guard_key, value=plugin_id)
                    logger.info(f"{plugin_name} 继续使用旧版数据桶: {','.join(occupied[:3])}")
                    return candidate
                except Exception as e:
                    logger.warning(f"{plugin_name} 旧版数据桶护栏写入失败({e})，继续使用原数据桶 {candidate}")
                    return candidate
            blocked_notes.append(f"{candidate}: 已有数据({','.join(occupied[:3])})")
            continue

        try:
            sg.bucketSet(bucket=guard_bucket, key=guard_key, value=plugin_id)
            return candidate
        except Exception as e:
            logger.warning(f"{plugin_name} 护栏初始化失败({e})，继续使用原数据桶 {candidate}")
            return candidate

    detail = "\n".join(blocked_notes[:8]) if blocked_notes else "没有可用命名空间"
    sender.reply(
        f"❌ {plugin_name} 已停止运行：无法自动找到可用数据桶前缀。\n"
        "为避免账号、状态、token 数据错乱，本次不会写入任何数据。\n"
        f"{detail}"
    )
    exit(0)

PLUGIN_RUNTIME_NAMESPACE = assert_automan_bucket_namespace_safe(
    PLUGIN_NAME,
    PLUGIN_NAMESPACE,
    PLUGIN_ID,
    PLUGIN_BUCKET_SUFFIXES,
    foreign_buckets=PLUGIN_FOREIGN_BUCKETS,
    shared_buckets=PLUGIN_SHARED_BUCKETS,
)

try:
    sg.bucketSet(bucket=plugin_bucket('sender'), key=userid, value=str(senderID))
    sg.bucketSet(bucket=plugin_bucket('imtype'), key=userid, value=str(sender.getImtype()))
except:
    pass

def getusercontent():
    return {'dd_hhtt_osname':sg.bucketGet('dd_hhtt','dd_hhtt_osname') or 'ty_hhtt','dd_hhtt_qlname':sg.bucketGet('dd_hhtt','dd_hhtt_qlname') or '','panel_type':str(sg.bucketGet('dd_hhtt','panel_type') or 'qinglong').lower(),'randommanagecommand':'和合管理','randomquerycommand':'和合查询','randomsigncommand':'和合登录','global_q':sg.bucketGet('dd_hhtt','global_q') or '','require_q_link':str(sg.bucketGet('dd_hhtt','require_q_link') or 'false').lower()=='true','enable_proxy':str(sg.bucketGet('dd_hhtt','enable_proxy') or 'false').lower()=='true','proxy_pool_url':sg.bucketGet('dd_hhtt','proxy_pool_url') or '','enable_remark':True}


config = getusercontent()

def get_owner_user_id(account, fallback_userid=None):
    account = str(account or "")
    try:
        if fallback_userid and account in [str(x) for x in AccountManager.get_accounts(str(fallback_userid))]:
            return str(fallback_userid)
    except:
        pass
    try:
        for frame_info in __import__('inspect').stack()[1:6]:
            local_vars = frame_info.frame.f_locals
            for key in ['owner_user_id', 'target_userid', 'target_qq', 'target_user', 'user', 'uid']:
                candidate = local_vars.get(key)
                if not candidate:
                    continue
                candidate = str(candidate)
                try:
                    if account in [str(x) for x in AccountManager.get_accounts(candidate)]:
                        return candidate
                except:
                    pass
    except:
        pass
    try:
        for owner in sg.bucketAllKeys(bucket=plugin_bucket('user')):
            try:
                if account in [str(x) for x in AccountManager.get_accounts(owner)]:
                    return str(owner)
            except:
                pass
    except:
        pass
    try:
        if not sender.isAdmin() and str(userid):
            return str(userid)
    except:
        pass
    return ""









def mask_account(account):
    account = str(account or "")
    if len(account) >= 11 and account.isdigit():
        return account[:3] + "****" + account[-4:]
    if len(account) > 6:
        return account[:3] + "****" + account[-3:]
    return account


def generate_ua_from_phone(phone_number: str) -> str:
    version = "4.5.6"
    seed_value = int(hashlib.md5(phone_number.encode()).hexdigest()[:8], 16)
    random.seed(seed_value)

    def generate_deterministic_uuid(phone: str):
        md5_hash = hashlib.md5(phone.encode()).hexdigest()
        sha_hash = hashlib.sha256(phone.encode()).hexdigest()
        part1 = "00000000"
        part2 = sha_hash[8:12]
        part3 = sha_hash[20:24]
        part4 = "ffff"
        part5 = md5_hash[16:28]
        return f"{part1}-{part2}-{part3}-{part4}-{part5}"

    uuid_str = generate_deterministic_uuid(phone_number)

    device_pools = {
        0: ("xiaomi", ["22081212C", "2210132C", "23013RK75C", "2201122C", "2211133G"]),
        1: ("samsung", ["SM-G998B", "SM-S901E", "SM-F721B", "SM-A736B", "SM-M336B"]),
        2: ("huawei", ["NOH-AN00", "LIO-AL00", "TET-AN00", "ANA-AN00", "JAD-AL50"]),
        3: ("oppo", ["CPH2207", "CPH2419", "CPH2487", "PFFM10", "PHQ110"]),
        4: ("vivo", ["V2244A", "V2218A", "V2217A", "V2220A", "V2232A"]),
        5: ("oneplus", ["NE2210", "CPH2417", "KB2000", "LE2120", "GM1910"]),
    }

    last_digit = int(phone_number[-1]) if phone_number[-1].isdigit() else 0
    brand_idx = last_digit % len(device_pools)
    brand, models = device_pools[brand_idx]

    if len(phone_number) >= 6:
        mid_digit = int(phone_number[len(phone_number) // 2]) % len(models)
    else:
        mid_digit = seed_value % len(models)

    device_model = models[mid_digit]
    phone_sum = sum(int(c) for c in phone_number if c.isdigit())
    if phone_sum % 10 < 2:
        os_type = "iOS"
        os_versions = ["17.0", "16.6", "15.7", "14.8", "13.5"]
        ios_models = ["iPhone15,2", "iPhone14,2", "iPhone13,2", "iPhone12,8", "iPhone11,8"]
        device_model = ios_models[mid_digit % len(ios_models)]
        brand = "apple"
    else:
        os_type = "Android"
        os_versions = ["13", "12", "11", "10", "9", "14"]

    version_idx = (seed_value + int(phone_number[-2:]) if len(phone_number) >= 2 else seed_value) % len(os_versions)
    os_version = os_versions[version_idx]
    app_version = "6.8.0"
    brand_lower = brand.lower()
    ua_string = f"{version};{uuid_str};{device_model};{os_type};{os_version};{brand_lower};{app_version}"
    random.seed()
    return ua_string



def encrypt_token(token):
    try:
        return base64.b64encode(token.encode()).decode()
    except:
        return token

def decrypt_token(encrypted_token):
    try:
        return base64.b64decode(encrypted_token.encode()).decode()
    except:
        return encrypted_token

class HeHeTianTai:
    def __init__(self, phone, password, q):
        self.url = "vapp.tmuyun.com"
        self.session = requests.Session()
        self.session_id = ""
        self.account_id = ""
        self.request_id = ""
        self.t = ""
        self.signature = ""
        self.phone = phone
        self.password = password

        latest_q = config.get('global_q', '')
        if latest_q:
            self.q = unquote(latest_q.replace("https://act.tmlyun.com/lottery/?q=", ""))
        elif q:
            self.q = unquote(q.replace("https://act.tmlyun.com/lottery/?q=", ""))
        else:
            self.q = ""

        self.token = ""
        self.u = ""
        self.ua = generate_ua_from_phone(self.phone)
        self.price = 0
        self.totalPrice = 0
        self.last_error = "" # 记录具体错误信息

        if config['enable_proxy'] and config['proxy_pool_url']:
            try:
                res = requests.get(config['proxy_pool_url'], timeout=5)
                if res.status_code == 200:
                    proxy_ip = res.text.strip()
                    if "{" in proxy_ip:
                        try:
                            json_data = res.json()
                            proxy_ip = json_data.get('proxy') or json_data.get('http') or list(json_data.values())[0]
                        except: pass
                    if proxy_ip and ":" in proxy_ip:
                        self.session.proxies.update({'http': proxy_ip, 'https': proxy_ip})
            except: pass

    def _safe_json(self, response):
        try:
            return response.json()
        except ValueError:
            return {"code": -1, "message": f"返回异常(HTTP状态: {response.status_code})"}

    def get_sign(self, path, e=None, d=None, t=None):
        if e is None: e = self.session_id
        if d is None: d = self.request_id
        if t is None: t = self.t
        if '?' in path: l = path.split('?')[0]
        else: l = path
        sign_str = f"{l}&&{e}&&{d}&&{t}&&FR*r!isE5W&&5"
        self.signature = hashlib.sha256(sign_str.encode()).hexdigest()

    def g(self, path):
        self.request_id = str(uuid.uuid4())
        self.t = str(int(time.time() * 1000))
        self.get_sign(path)

        headers = {
            "User-Agent": self.ua,
            "Host": self.url,
            'Cache-Control': "no-cache",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            "X-TENANT-ID": "5",
            "X-SESSION-ID": self.session_id,
            "X-REQUEST-ID": self.request_id,
            "X-TIMESTAMP": self.t,
            "X-SIGNATURE": self.signature,
            "X-ACCOUNT-ID": self.account_id,
        }
        response = self.session.get(
            f"https://{self.url}{path}",
            headers=headers,
            verify=False,
            timeout=15
        )
        return self._safe_json(response)

    def p(self, path, data=""):
        self.request_id = str(uuid.uuid4())
        self.t = str(int(time.time() * 1000))
        self.get_sign(path)

        headers = {
            "User-Agent": self.ua,
            "Host": self.url,
            "X-SESSION-ID": self.session_id,
            "X-REQUEST-ID": self.request_id,
            "X-TIMESTAMP": self.t,
            "X-SIGNATURE": self.signature,
            "X-ACCOUNT-ID": self.account_id,
            "X-TENANT-ID": "5",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Cache-Control": "no-cache"
        }
        response = self.session.post(
            f"https://{self.url}{path}",
            headers=headers,
            data=data,
            verify=False,
            timeout=15
        )
        return self._safe_json(response)

    def rsa_encrypt(self, password, public_key_pem):
        rsa_key = RSA.import_key(public_key_pem)
        cipher = PKCS1_v1_5.new(rsa_key)
        encrypted = cipher.encrypt(password.encode())
        return base64.b64encode(encrypted).decode()

    def login(self):
        try:
            init_data = self.p("/api/account/init", "")
            self.session_id = init_data.get("data", {}).get("session", {}).get("id", "")

            public_key = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQD6XO7e9YeAOs+cFqwa7ETJ+WXi
zPqQeXv68i5vqw9pFREsrqiBTRcg7wB0RIp3rJkDpaeVJLsZqYm5TW7FWx/iOiXF
c+zCPvaKZric2dXCw27EvlH5rq+zwIPDAJHGAfnn1nmQH7wR3PCatEIb8pz5GFlT
HMlluw4ZYmnOwg+thwIDAQAB
-----END PUBLIC KEY-----"""

            encrypted_pwd = self.rsa_encrypt(self.password, public_key)

            d = str(uuid.uuid4())
            t = str(int(time.time() * 1000))
            l = "/web/oauth/credential_auth"
            sign_str = f"{l}&&{self.session_id}&&{d}&&{t}&&FR*r!isE5W&&5"
            s = hashlib.sha256(sign_str.encode()).hexdigest()

            auth_data = {
                "client_id": "10",
                "password": encrypted_pwd,
                "phone_number": self.phone
            }

            headers = {
                "User-Agent": self.ua,
                "X-REQUEST-ID": d,
                "X-SIGNATURE": s,
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                "Host": "passport.tmuyun.com"
            }

            response = self.session.post(
                "https://passport.tmuyun.com/web/oauth/credential_auth",
                headers=headers,
                data=auth_data,
                verify=False,
                timeout=15
            )

            code_data = self._safe_json(response)
            if code_data.get("code") != 0:
                self.last_error = f"账号认证失败: {code_data.get('message')}"
                return code_data

            code = code_data.get("data", {}).get("authorization_code", {}).get("code", "")

            login_data = self.p(
                "/api/zbtxz/login",
                f"check_token=&code={code}&token=&type=-1&union_id="
            )

            self.session_id = login_data.get("data", {}).get("session", {}).get("id", "")
            self.account_id = login_data.get("data", {}).get("session", {}).get("account_id", "")
            return login_data
        except Exception as e:
            logger.error(f"登录异常: {e}")
            self.last_error = f"登录异常: {str(e)}"
            return {"code": -1, "message": str(e)}

    def get_u(self):
        try:
            url = "https://act.tmlyun.com/activity-api/lottery/h5/activity/lottery/accountPrizeRecord/jumpEquityWallet"
            headers = {
                'User-Agent': self.ua,
                'Authorization': self.token,
                'X-REQUEST-ID': self.request_id,
            }
            response = self.session.get(url, headers=headers, verify=False, timeout=10)
            if self._safe_json(response).get("code") == 0:
                self.u = unquote(self._safe_json(response).get("data", {}).split("u=")[1].split("&")[0])
                return True
            self.last_error = f"获取U值失败: {self._safe_json(response).get('message')}"
            return False
        except Exception as e:
            self.last_error = f"获取U值异常: {str(e)}"
            return False

    def lottery_login(self):
        try:
            url = "https://act.tmlyun.com/activity-api/lottery/api/auth/userLogin"
            self.request_id = str(uuid.uuid4())
            payload = {
                "q": self.q,
                "accountId": self.account_id,
                "sessionId": self.session_id,
                "tenantCode": "xsb_tiantai"
            }
            headers = {
                'Content-Type': "application/json",
                'X-REQUEST-ID': self.request_id,
                'X-Requested-With': "com.zjonline.tiantai",
            }
            response = self.session.post(url, data=json.dumps(payload), headers=headers, verify=False, timeout=10)
            if self._safe_json(response).get("code") == 0:
                self.token = self._safe_json(response).get("data", {}).get("token", "")
                return True
            self.last_error = f"抽奖登录失败: {self._safe_json(response).get('message')}"
            return False
        except Exception as e:
            self.last_error = f"抽奖登录异常: {str(e)}"
            return False

    def query_login(self):
        try:
            url = "https://my.tmlyun.com/equity-api/user/auth/userLogin"
            self.t = str(int(time.time() * 1000))
            random_float = random.uniform(1000, 9999)
            self.request_id = f"{random_float:.12f}|{self.t}"
            payload = {
                "u": self.u,
                "accountId": self.account_id,
                "sessionId": self.session_id,
            }
            headers = {
                'Content-Type': "application/json",
                'X-REQUEST-ID': self.request_id,
                'X-Requested-With': "com.zjonline.tiantai",
            }
            response = self.session.post(url, data=json.dumps(payload), headers=headers, verify=False, timeout=10)
            if self._safe_json(response).get("code") == 0:
                self.token = self._safe_json(response).get("data", {}).get("token", "")
                return True
            self.last_error = f"钱包登录失败: {self._safe_json(response).get('message')}"
            return False
        except: return False

    def get_wallet_info(self):
        try:
            self.t = str(int(time.time() * 1000))
            random_float = random.uniform(1000, 9999)
            self.request_id = f"{random_float:.12f}|{self.t}"
            url = "https://my.tmlyun.com/equity-api/redBag/getWalletInfo"
            params = {'device': self.ua.split(";")[1]}
            headers = {
                'User-Agent': self.ua,
                'X-REQUEST-ID': self.request_id,
                'Accept': "application/json, text/plain, */*",
                'Authorization': self.token,
            }
            response = self.session.get(url, params=params, headers=headers, verify=False, timeout=10)
            if self._safe_json(response).get("code") == 0:
                self.price = self._safe_json(response).get("data", {})[0].get("aliPayTotalPrice", 0)
                self.totalPrice = self._safe_json(response).get("data", {})[0].get("totalTransPrice", 0)
                return True
            self.last_error = f"获取钱包失败: {self._safe_json(response).get('message')}"
            return False
        except: return False

    def query_wallet_records(self):
        try:
            url = "https://my.tmlyun.com/equity-api/redBag/pageWalletDetail"
            params = {
                'current': "1",
                'pageSize': "5",
                'fundsChannelType': "0"
            }
            self.t = str(int(time.time() * 1000))
            self.request_id = f"{random.uniform(1000, 9999):.12f}|{self.t}"
            headers = {
                'X-REQUEST-ID': self.request_id,
                'Authorization': self.token,
            }
            response = self.session.get(url, params=params, headers=headers, verify=False, timeout=10)

            if self._safe_json(response).get("code") == 0:
                data = self._safe_json(response).get("data", [])
                records = []
                for item in data:
                    status_desc = "阅读红包" if item.get('type', 0) == 0 else (item.get('statusDesc', '未知') or "未知")
                    record_str = f"{item.get('createdAt', '')}[{item.get('price', 0)}][{status_desc}]"
                    records.append(record_str)
                return records
            return []
        except: return []

    def check_info(self):
        try:
            login_result = self.login()
            if login_result.get("code") != 0:
                return None

            nick_name = login_result['data']['account']['nick_name']

            integral_data = self.g("/api/user_mumber/numberCenter?is_new=1")
            total_integral = integral_data.get("data", {}).get("rst", {}).get("total_integral", 0)

            wallet_info = {"price": 0, "totalPrice": 0, "valid": False, "records": []}
            if self.q:
                if not self.lottery_login(): return None
                if not self.get_u(): return None
                if not self.query_login(): return None
                if not self.get_wallet_info(): return None

                wallet_info["price"] = self.price
                wallet_info["totalPrice"] = self.totalPrice
                wallet_info["valid"] = True
                wallet_info["records"] = self.query_wallet_records()

            return {
                "nickname": nick_name,
                "integral": total_integral,
                "wallet": wallet_info
            }
        except Exception as e:
            logger.error(f"查询出错: {e}")
            if not self.last_error:
                self.last_error = f"未知异常: {str(e)}"
            return None

class RemarkManager:
    @staticmethod
    def get_account_remark(user_id, account_id):
        try:
            remark_data = sg.bucketGet(bucket=plugin_bucket('remarks'), key=f'{user_id}_{account_id}')
            if remark_data: return remark_data
            return ""
        except: return ""

    @staticmethod
    def set_account_remark(user_id, account_id, remark):
        try:
            remark_clean = remark.strip()[:20]
            if remark_clean:
                sg.bucketSet(bucket=plugin_bucket('remarks'), key=f'{user_id}_{account_id}', value=remark_clean)
                return remark_clean
            return ""
        except: return ""

    @staticmethod
    def get_all_remarks(user_id):
        try:
            accounts = AccountManager.get_accounts(user_id)
            remarks = {}
            for account in accounts:
                remark = RemarkManager.get_account_remark(user_id, account)
                if remark: remarks[account] = remark
            return remarks
        except: return {}

    @staticmethod
    def delete_account_remark(user_id, account_id):
        try:
            sg.bucketDel(bucket=plugin_bucket('remarks'), key=f'{user_id}_{account_id}')
            return True
        except: return False

class AccountManager:
    @staticmethod
    def get_accounts(user_id):
        try:
            value = sg.bucketGet(bucket=plugin_bucket('user'), key=str(user_id))
            if not value: return []
            if value.startswith('[') and value.endswith(']'):
                try:
                    accounts = ast.literal_eval(value)
                    if isinstance(accounts, (list, tuple, set)):
                        return [str(x) for x in list(dict.fromkeys(accounts))]
                except: pass
            return [str(value)]
        except: return []

    @staticmethod
    def add_account(user_id, account):
        try:
            user_id = str(user_id)
            account = str(account)
            accounts = AccountManager.get_accounts(user_id)
            if account not in accounts:
                accounts.append(account)
                sg.bucketSet(bucket=plugin_bucket('user'), key=user_id, value=str(accounts))
                return True
            return False
        except: return False

    @staticmethod
    def remove_account(user_id, account):
        try:
            user_id = str(user_id)
            account = str(account)
            accounts = AccountManager.get_accounts(user_id)
            if account in accounts:
                accounts.remove(account)
                if accounts:
                    sg.bucketSet(bucket=plugin_bucket('user'), key=user_id, value=str(accounts))
                else:
                    sg.bucketDel(bucket=plugin_bucket('user'), key=user_id)
                return True
            return False
        except: return False

    @staticmethod
    def update_account_token(user_id, account, token):
        try:
            encrypted_token = encrypt_token(str(token))
            sg.bucketSet(bucket=plugin_bucket('token'), key=str(account), value=encrypted_token)
            return True
        except: return False

    @staticmethod
    def get_token(account):
        try:
            encrypted_token = sg.bucketGet(bucket=plugin_bucket('token'), key=str(account))
            return decrypt_token(encrypted_token) if encrypted_token else ""
        except:
            return ""

    @staticmethod
    def get_all_users():
        try:
            users = sg.bucketAllKeys(bucket=plugin_bucket('user'))
            user_list = []
            for user in users:
                accounts = AccountManager.get_accounts(user)
                if accounts: user_list.append(user)
            return user_list
        except: return []

class QingLongAPI:
    def __init__(self):
        self.enabled = False
        self.panel_type = config.get('panel_type', 'qinglong')
        ql_config = config['dd_hhtt_qlname']
        try:
            if not ql_config: raise ValueError("对接配置为空")
            qllist = ql_config.split('丨')
            if len(qllist) != 3: raise ValueError("对接配置格式错误")
            self.QLurl = qllist[0].strip().rstrip('/')
            self.ClientID = qllist[1].strip()
            self.ClientSecret = qllist[2].strip()
            if not all([self.QLurl, self.ClientID, self.ClientSecret]): raise ValueError("配置不完整")
            if self.panel_type == 'daidai':
                self.access_token = self._get_daidai_token()
            else:
                self.qltoken = self._get_token()
            self.enabled = True
        except Exception as e:
            logger.error("系统初始化失败: " + str(e))
            self.init_error = str(e)

    def _get_token(self):
        try:
            url = f"{self.QLurl}/open/auth/token?client_id={self.ClientID}&client_secret={self.ClientSecret}"
            response = requests.get(url, timeout=10, verify=False)
            if response.status_code == 200:
                return response.json()['data']['token']
            raise Exception("获取Token失败")
        except Exception: raise

    def _get_daidai_token(self):
        try:
            url = f"{self.QLurl}/api/open-api/token"
            data = {"app_key": self.ClientID, "app_secret": self.ClientSecret}
            response = requests.post(url, json=data, timeout=10, verify=False)
            if response.status_code == 200:
                return response.json()['data']['access_token']
            raise Exception("获取呆呆Token失败")
        except Exception: raise

    def get_all_envs(self):
        if not self.enabled: return []
        try:
            if self.panel_type == 'daidai':
                url = f"{self.QLurl}/api/envs?keyword={config['dd_hhtt_osname']}&page_size=9999"
                headers = {"Authorization": f"Bearer {self.access_token}", "accept": "application/json"}
                response = requests.get(url, headers=headers, timeout=10, verify=False)
                if response.status_code == 200: return response.json().get('data', [])
            else:
                url = f"{self.QLurl}/open/envs"
                headers = {"Authorization": f"Bearer {self.qltoken}", "accept": "application/json"}
                response = requests.get(url, headers=headers, timeout=10, verify=False)
                if response.status_code == 200: return response.json()['data']
            return []
        except: return []

    def find_env_by_account(self, account, token=None):
        try:
            for env in self.get_all_envs():
                if env.get('name') != config['dd_hhtt_osname']: continue
                env_id = env.get('id') if env.get('id') is not None else env.get('_id')
                env_value = str(env.get('value') or '').strip()
                env_remarks = str(env.get('remarks') or env.get('remark') or '')
                if token and str(token).strip() in env_value: return env_id
                if env_remarks and str(account) in env_remarks: return env_id
            return None
        except: return None

    def delete_env(self, env_id):
        if not self.enabled or not env_id: return False
        try:
            if self.panel_type == 'daidai':
                url = f"{self.QLurl}/api/envs/{env_id}"
                headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
                res = requests.delete(url, headers=headers, timeout=10, verify=False)
            else:
                url = f"{self.QLurl}/open/envs"
                headers = {"Authorization": f"Bearer {self.qltoken}", "Content-Type": "application/json"}
                res = requests.delete(url, headers=headers, json=[env_id], timeout=10, verify=False)
            return res.status_code == 200
        except: return False

    def delete_env_by_account(self, account, token=None):
        try:
            env_id = self.find_env_by_account(account, token)
            if env_id:
                return self.delete_env(env_id)
            return False
        except:
            return False

    def sync_env(self, token, account, remark="", auth_time="", owner_user_id=None):
        if not self.enabled: return False
        try:
            env_id = self.find_env_by_account(account, token)
            if env_id:
                return self.update_env(env_id, token, account, account, remark, auth_time, owner_user_id)
            return self.add_env(token, account, account, remark, auth_time, owner_user_id)
        except:
            return False

    def add_env(self, token, account, phone, remark="", auth_time="", owner_user_id=None):
        if not self.enabled: return False
        try:
            phone_display = phone[:3] + '*' * 4 + phone[7:] if len(phone) >= 11 else phone
            remarks_parts = [f'和合:{account}']
            if remark: remarks_parts.append(f'备注:{remark}')
            owner_user = get_owner_user_id(account, owner_user_id)
            if not owner_user:
                raise Exception("无法确认账号真实归属，已阻止写入面板备注，避免青龙数据错乱")
            remarks_parts.extend([f'用户:{owner_user}', f'手机:{phone_display}', '和合管理'])

            if self.panel_type == 'daidai':
                url = f"{self.QLurl}/api/envs"
                headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
                data = {"value": token, "name": config['dd_hhtt_osname'], "remarks": '丨'.join(remarks_parts)}
                res = requests.post(url, headers=headers, json=data, timeout=10, verify=False)
            else:
                url = f"{self.QLurl}/open/envs"
                headers = {"Authorization": f"Bearer {self.qltoken}", "Content-Type": "application/json"}
                data = [{"value": token, "name": config['dd_hhtt_osname'], "remarks": '丨'.join(remarks_parts)}]
                res = requests.post(url, headers=headers, json=data, timeout=10, verify=False)
            return res.status_code == 200
        except: return False

    def update_env(self, env_id, token, account, phone, remark="", auth_time="", owner_user_id=None):
        if not self.enabled: return False
        try:
            phone_display = phone[:3] + '*' * 4 + phone[7:] if len(phone) >= 11 else phone
            remarks_parts = [f'和合:{account}']
            if remark: remarks_parts.append(f'备注:{remark}')
            owner_user = get_owner_user_id(account, owner_user_id)
            if not owner_user:
                raise Exception("无法确认账号真实归属，已阻止写入面板备注，避免青龙数据错乱")
            remarks_parts.extend([f'用户:{owner_user}', f'手机:{phone_display}', '和合管理'])

            if self.panel_type == 'daidai':
                url = f"{self.QLurl}/api/envs/{env_id}"
                headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
                data = {"value": token, "name": config['dd_hhtt_osname'], "remarks": '丨'.join(remarks_parts)}
                res = requests.put(url, headers=headers, json=data, timeout=10, verify=False)
                if res.status_code == 200:
                    try: requests.put(f"{self.QLurl}/api/envs/{env_id}/enable", headers=headers, timeout=5, verify=False)
                    except: pass
            else:
                url = f"{self.QLurl}/open/envs"
                headers = {"Authorization": f"Bearer {self.qltoken}", "Content-Type": "application/json"}
                data = {"value": token, "name": config['dd_hhtt_osname'], "remarks": '丨'.join(remarks_parts)}
                if isinstance(env_id, int) or str(env_id).isdigit():
                    data["id"] = env_id
                else:
                    data["_id"] = env_id
                res = requests.put(url, headers=headers, json=data, timeout=10, verify=False)
                if res.status_code == 200:
                    try: requests.put(f"{self.QLurl}/open/envs/enable", headers=headers, json=[env_id], timeout=5, verify=False)
                    except: pass
            return res.status_code == 200
        except: return False

try:
    ql_api = QingLongAPI() if config['dd_hhtt_qlname'] else None
    if not ql_api.enabled and sender.getImtype() != 'fake':
        sender.reply("⚠️ 系统API初始化失败，青龙/呆呆同步功能不可用，请检查配置。")
except Exception:
    ql_api = type('obj', (object,), {
        'enabled': False,
        'sync_env': lambda *a, **k: False,
        'delete_env': lambda *a, **k: False,
        'delete_env_by_account': lambda *a, **k: False,
        'find_env_by_account': lambda *a, **k: None,
        'update_env': lambda *a, **k: False,
        'add_env': lambda *a, **k: False,
    })()
    if sender.getImtype() != 'fake':
        sender.reply("⚠️ 系统API初始化异常，青龙/呆呆同步功能不可用，请检查配置。")

def process_single_account(account,index,total,remarks):
    encrypted=sg.bucketGet(plugin_bucket('token'),account);credential=decrypt_token(encrypted) if encrypted else '';display=mask_account(account);remark=remarks.get(account,'')
    if not credential:return f'{index}/{total} {remark or display}：凭证不存在'
    try:
        parts=credential.split('#');phone,password=parts[:2];q=parts[2] if len(parts)>2 else ''
        info=HeHeTianTai(phone,password,q).check_info()
        if not info:return f'{index}/{total} {remark or display}：查询失败'
        wallet=info.get('wallet',{});return f"{index}/{total} {remark or display}：积分 {info.get('integral',0)}，余额 {wallet.get('price',0)}，累计提现 {wallet.get('totalPrice',0)}"
    except Exception as error:return f'{index}/{total} {remark or display}：查询失败 {error}'


def cxs():
    accounts=AccountManager.get_accounts(userid)
    if not accounts:return sender.reply('未绑定账号，请发送【和合登录】')
    remarks=RemarkManager.get_all_remarks(userid);sender.reply('请输入查询序号，a 查询全部，q 退出\n'+'\n'.join(f'{i}. {remarks.get(str(a)) or mask_account(str(a))}' for i,a in enumerate(accounts,1)))
    choice=get_user_input()
    if not choice or choice=='q':return
    targets=list(enumerate(accounts,1)) if choice=='a' else []
    if not targets:
        indexes,_=parse_index_selection(choice,len(accounts),False);targets=[(i,accounts[i-1]) for i in indexes]
    if not targets:return sender.reply('序号无效')
    for index,account in targets:sender.reply(process_single_account(str(account),index,len(accounts),remarks))


def get_user_input(timeout=60):
    try:
        response = sender.listen(timeout * 1000)
        if not response: return None
        response = response.strip()
        if response.lower() in ['q', 'quit', 'exit', '退出', 'cancel']: return 'q'
        return response
    except: return None






def parse_index_selection(text, total_count, allow_all=True):
    try:
        if text is None:
            return [], []
        raw = str(text).strip()
        if not raw:
            return [], []
        if allow_all and raw.lower() in ['a', 'all', '全部', '全选']:
            return list(range(1, total_count + 1)), []

        selected = []
        invalid = []
        parts = re.split(r'[,\s，、;；]+', raw)
        for part in parts:
            part = part.strip()
            if not part:
                continue

            range_match = re.match(r'^(\d+)\s*(?:-|~|到|至)\s*(\d+)$', part)
            if range_match:
                start = int(range_match.group(1))
                end = int(range_match.group(2))
                if start > end:
                    start, end = end, start
                start = max(1, start)
                end = min(total_count, end)
                if start <= end:
                    selected.extend(range(start, end + 1))
                else:
                    invalid.append(part)
                continue

            if part.isdigit():
                idx = int(part)
                if 1 <= idx <= total_count:
                    selected.append(idx)
                else:
                    invalid.append(part)
                continue

            invalid.append(part)

        return list(dict.fromkeys(selected)), invalid
    except:
        return [], [str(text)]



def split_login_entries(input_text):
    text = str(input_text or "").strip()
    if not text:
        return []
    parts = re.split(r'[\r\n&]+', text)
    entries = []
    for part in parts:
        item = str(part or "").strip().strip('，,；;')
        if item:
            entries.append(item)
    return entries

def validate_login_entry(entry, require_q_link=False):
    parts = [str(x).strip() for x in str(entry or "").split('#')]
    if require_q_link:
        if len(parts) < 3:
            return False, "", "", "", "❌ 格式错误，请按照 手机号#密码#Q值的分享链接 格式输入"
        phone, pwd = parts[0], parts[1]
        q = '#'.join(parts[2:]).strip()
        if "q=" not in q:
            return False, phone, pwd, q, (
                "❌ Q值链接错误！\n"
                "请提交包含 [q=] 的抽奖链接\n"
                "通常格式为: https://act.tmlyun.com/lottery/?q=xxxx"
            )
        return True, phone, pwd, q, ""
    if len(parts) < 2:
        return False, "", "", "", "❌ 格式错误，请按照 手机号#密码 格式输入"
    phone, pwd = parts[0], parts[1]
    return True, phone, pwd, "", ""

def execute_single_bind(entry, remark=""):
    require_q_link = config.get('require_q_link', False)
    ok, phone, pwd, q, error_msg = validate_login_entry(entry, require_q_link=require_q_link)
    if not ok:
        return {"success": False, "phone": phone, "message": error_msg}

    client = HeHeTianTai(phone, pwd, q)
    login_res = client.login()
    if login_res.get("code") != 0:
        return {
            "success": False,
            "phone": phone,
            "message": f"❌ 登录失败: {login_res.get('message', '未知错误')}"
        }

    nick = login_res['data']['account']['nick_name']
    bind_msg = process_account_binding(entry, phone, nick, remark, reply=False)
    return {
        "success": True,
        "phone": phone,
        "nickname": nick,
        "message": bind_msg
    }

def bindaccount():
    try:
        remark = ""
        if config['enable_remark']:
            sender.reply("""
=====账号备注设置=====
🎯 请输入账号备注名
------------------
回复备注名继续
回复"n"跳过备注
回复"q"退出操作
==================""")
            remark_input = get_user_input(timeout=120)
            if remark_input == 'q':
                sender.reply("✅ 已取消")
                return
            elif remark_input != 'n' and remark_input:
                remark = remark_input.strip()[:20]

        if config.get('require_q_link', False):
            sender.reply("""
=====和合账号登录=====
请输入格式：
手机号#密码#带q值的分享链接
支持批量：一行一个，或用 & 分隔
------------------
例如: 13800000000#123456#https://act.tmlyun.com...
例如: 13800000000#123456#https://act.tmlyun.com...&13900000000#654321#https://act.tmlyun.com...
------------------
回复"q"退出操作
==================""")
        else:
            sender.reply("""
=====和合账号登录=====
请输入格式：
手机号#密码
支持批量：一行一个，或用 & 分隔
------------------
例如: 13800000000#123456
例如: 13800000000#123456&13900000000#654321
------------------
回复"q"退出操作
==================""")

        input_str = get_user_input(timeout=120)
        if not input_str or input_str == 'q':
            sender.reply("✅ 已取消")
            return

        entries = split_login_entries(input_str)
        if not entries:
            sender.reply("❌ 未识别到有效账号数据")
            return

        if len(entries) == 1:
            sender.reply("⏳ 正在登录验证中，请稍候...")
            result = execute_single_bind(entries[0], remark=remark)
            if result["success"]:
                sender.reply(result["message"])
            else:
                sender.reply(result["message"])
            return

        sender.reply(f"⏳ 检测到 {len(entries)} 个账号，正在批量登录验证，请稍候...")
        success_count = 0
        fail_msgs = []
        success_preview = []

        for idx, entry in enumerate(entries, 1):
            result = execute_single_bind(entry, remark=remark)
            account_tip = mask_account(result.get("phone") or f"第{idx}个账号")
            if result["success"]:
                success_count += 1
                success_preview.append(f"{idx}. {account_tip}")
            else:
                fail_msgs.append(f"{idx}. {account_tip} {result['message'].replace(chr(10), ' ')}")

        msg_lines = [
            "=====批量登录结果=====",
            f"总数量: {len(entries)}",
            f"成功: {success_count}",
            f"失败: {len(fail_msgs)}",
        ]
        if success_preview:
            msg_lines.append("------------------")
            msg_lines.append("✅ 成功账号:")
            msg_lines.extend(success_preview[:15])
            if len(success_preview) > 15:
                msg_lines.append(f"... 另有 {len(success_preview) - 15} 个成功账号")
        if fail_msgs:
            msg_lines.append("------------------")
            msg_lines.append("❌ 失败账号:")
            msg_lines.extend(fail_msgs[:15])
            if len(fail_msgs) > 15:
                msg_lines.append(f"... 另有 {len(fail_msgs) - 15} 个失败账号")
        if success_count:
            msg_lines.append("------------------")
            msg_lines.append(f"下一步可发送 {config['randommanagecommand']} 进行管理")
        msg_lines.append("==================")
        sender.reply("\n".join(msg_lines))

    except Exception as e:
        logger.error("绑定失败: " + str(e))
        sender.reply("❌ 绑定失败: " + str(e))

def process_account_binding(full_token,phone,nickname,remark='',reply=True):
    account=str(phone);existing=AccountManager.get_accounts(userid)
    if account in existing:AccountManager.update_account_token(userid,account,full_token)
    else:AccountManager.add_account(userid,account);sg.bucketSet(plugin_bucket('token'),account,encrypt_token(full_token))
    if remark:RemarkManager.set_account_remark(userid,account,remark)
    sync='仅本地保存'
    if ql_api:
        try:
            env=ql_api.find_env_by_account(account,full_token)
            if env:ql_api.update_env(env,full_token,account,phone,remark,'')
            else:ql_api.add_env(full_token,account,phone,remark,'')
            sync='面板同步成功'
        except Exception as error:sync=f'面板同步失败：{error}'
    message=f'{nickname}（{mask_account(phone)}）绑定成功；{sync}'
    if reply:sender.reply(message)
    return message


def xy_manage():
    accounts=AccountManager.get_accounts(userid)
    if not accounts:return sender.reply('未绑定账号，请发送【和合登录】')
    remarks=RemarkManager.get_all_remarks(userid);sender.reply('和合账号：\n'+'\n'.join(f'{i}. {remarks.get(str(a)) or mask_account(str(a))}' for i,a in enumerate(accounts,1))+'\n回复序号管理，q 退出')
    choice=get_user_input()
    if not choice or choice=='q':return
    try:account=str(accounts[int(choice)-1])
    except (ValueError,IndexError):return sender.reply('序号无效')
    manage_single_account(account,remarks)





def manage_single_account(account,remarks):
    encrypted=sg.bucketGet(plugin_bucket('token'),account);token=decrypt_token(encrypted) if encrypted else '';remark=remarks.get(account,'')
    sender.reply('1. 删除账号\n2. 修改备注\n3. 重新同步面板\nq. 退出');choice=get_user_input()
    if choice=='1':
        sender.reply('回复 y 确认删除')
        if get_user_input()=='y':
            AccountManager.remove_account(userid,account)
            if ql_api:
                env=ql_api.find_env_by_account(account,token)
                if env:ql_api.delete_env(env)
            sg.bucketDel(plugin_bucket('token'),account);RemarkManager.delete_account_remark(userid,account);sender.reply('账号已删除')
    elif choice=='2':
        sender.reply('请输入新备注，n 清空');new=get_user_input()
        if new=='n':RemarkManager.delete_account_remark(userid,account);new=''
        elif new:RemarkManager.set_account_remark(userid,account,new[:20])
        else:return
        if token and ql_api:
            env=ql_api.find_env_by_account(account,token)
            if env:ql_api.update_env(env,token,account,account,new,'')
        sender.reply('备注已更新')
    elif choice=='3':
        if not token:return sender.reply('凭证不存在，请重新登录')
        if not ql_api:return sender.reply('未配置面板')
        env=ql_api.find_env_by_account(account,token)
        if env:ql_api.update_env(env,token,account,account,remark,'')
        else:ql_api.add_env(token,account,account,remark,'')
        sender.reply('面板同步完成')







def show_tutorial():
    sender.reply('【和合登录】绑定账号；【和合查询】查询积分和余额；【和合管理】删除、备注或重新同步面板。')


command_text=str(usermessage or '')
if '登录' in command_text or '登陆' in command_text:bindaccount()
elif '管理' in command_text:xy_manage()
elif '查询' in command_text:cxs()
elif command_text=='和合教程':show_tutorial()
else:sender.setContinue()
