# [title: 伊利QQ星]
# [name: yiLiQqXing]
# [language: python]
# [class: 任务]
# [author: 8165799]
# [version: v1.2.1]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(伊利|伊利QQ星)(登录|登陆|管理|查询|教程)$|^(登录|登陆|管理|查询)(伊利|伊利QQ星)$]
# [icon: https://api.iconify.design/lucide:bot.svg]
# [description: 伊利QQ星账号登录、会员积分查询、管理与面板同步]
# [depe: ["requests"]]
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
import os
import requests
import time
import hashlib
import logging
import base64
import warnings
import json
from xml.etree import ElementTree as ET

warnings.filterwarnings('ignore', message='Unverified HTTPS request')
requests.packages.urllib3.disable_warnings()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('yiliqqx_plugin')

REQUEST_TIMEOUT = 30
MAINTENANCE_CK_MAX_WORKERS = 8

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = str(sender.getUserID())
usermessage = sender.getMessage()
usermessage = str(usermessage or "").replace('伊利qq星', '伊利QQ星').replace('伊利Qq星', '伊利QQ星').replace('伊利qQ星', '伊利QQ星')

PLUGIN_NAME = "伊利QQ星签到插件"
PLUGIN_NAMESPACE = "yiliqqx"
PLUGIN_ID = "yiliqqx:伊利QQ星签到插件:v1"

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
PLUGIN_AUTO_NAMESPACE = True
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
        keys = sg.bucketAllKeys(bucket=bucket_name)
        return bool(keys)
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

        duplicated = sorted({bucket for bucket in data_buckets if data_buckets.count(bucket) > 1})
        if duplicated:
            sender.reply(
                f"❌ {plugin_name} 已停止运行：模板内数据桶重复。\n"
                "重复桶: " + "、".join(duplicated)
            )
            exit(0)

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
            blocked_notes.append(f"{candidate}: 护栏标记不匹配({owner})")
            continue

        occupied = [bucket for bucket in data_buckets if _bucket_has_any_key(bucket)]
        if occupied:
            if candidate == namespace:
                try:
                    sg.bucketSet(bucket=guard_bucket, key=guard_key, value=plugin_id)
                    logger.warning(f"{plugin_name} 检测到默认桶已有历史数据，已认领原桶前缀：{candidate}")
                    return candidate
                except Exception as e:
                    blocked_notes.append(f"{candidate}: 历史数据桶认领失败({e})")
                    continue
            blocked_notes.append(f"{candidate}: 已有数据({','.join(occupied[:3])})")
            continue

        try:
            sg.bucketSet(bucket=guard_bucket, key=guard_key, value=plugin_id)
            if candidate != namespace:
                try:
                    sender.reply(f"ℹ️ {plugin_name} 检测到默认数据桶被占用，已自动切换到专用桶前缀：{candidate}")
                except Exception:
                    pass
            return candidate
        except Exception as e:
            blocked_notes.append(f"{candidate}: 护栏初始化失败({e})")
            continue

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
    return {'panel_type':str(sg.bucketGet('yiliqqx','panel_type') or 'qinglong').lower(),'env_name':sg.bucketGet('yiliqqx','yiliqqx_osname') or 'YILIQQX_AUTH_KEY','env_qlconfig':sg.bucketGet('yiliqqx','yiliqqx_qlname') or '','randommanagecommand':'伊利管理','randomquerycommand':'伊利查询','randomsigncommand':'伊利登录','enable_proxy':str(sg.bucketGet('yiliqqx','enable_proxy') or 'false').lower()=='true','proxy_pool_url':sg.bucketGet('yiliqqx','proxy_pool_url') or '','enable_remark':True}


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
    account = str(account)
    return account[:3] + "****" + account[-3:] if len(account) > 6 else account

def get_account_display(account, remark=""):
    remark = str(remark or "").strip()
    return remark if remark else mask_account(account)







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

class YiLiQQStarClient:
    APPID = "wx650bdff059f63f5b"
    BASE_URL = "https://mall.yili.com/MAMAIF/MCSWSIAPI.asmx/Call"

    def __init__(self, token_str):
        self.token = str(token_str or '').strip()
        self.auth_key = self._extract_auth_key(self.token)
        self.member_info = None
        self.member_id = ""
        self.nickname = ""

    def _extract_auth_key(self, text):
        text = str(text or "").strip()
        if not text:
            return ""
        if "#" in text:
            parts = [p.strip() for p in text.split("#") if p.strip()]
            text = parts[-1] if parts else text
        if text.startswith("{"):
            try:
                data = json.loads(text)
                text = data.get("auth_key") or data.get("AuthKey") or text
            except:
                pass
        match = re.search(r'(?:AuthKey|auth_key)\s*[:=]\s*"?([0-9a-fA-F-]{32,64})"?', text)
        return match.group(1) if match else text.strip()

    def _get_proxy(self):
        if not config.get('enable_proxy') or not config.get('proxy_pool_url'):
            return None
        try:
            res = requests.get(config['proxy_pool_url'], timeout=8, verify=False)
            text = res.text.strip()
            match = re.search(r'(?:https?://)?\d+\.\d+\.\d+\.\d+:\d+', text)
            if match:
                proxy = match.group(0)
                if not proxy.startswith(('http://', 'https://')):
                    proxy = 'http://' + proxy
                return proxy
        except Exception as e:
            logger.warning(f"伊利QQ星查询获取代理失败: {e}")
        return None

    def _headers(self):
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows',
            'Content-Type': 'application/x-www-form-urlencoded',
            'xweb_xhr': '1',
            'Referer': f'https://servicewechat.com/{self.APPID}/162/page-frame.html',
        }

    def _parse_response(self, resp):
        text = resp.text.strip()
        if not text:
            return {}
        if text.startswith('<?xml') or text.startswith('<string'):
            try:
                root = ET.fromstring(text)
                text = root.text or ""
            except:
                match = re.search(r'<string[^>]*>(.*?)</string>', text, re.S)
                text = match.group(1) if match else text
        try:
            data = json.loads(text)
        except:
            return {}
        if isinstance(data.get('Result'), str):
            try:
                data['Result'] = json.loads(data['Result'])
            except:
                pass
        return data

    def call(self, method, params=""):
        if isinstance(params, dict):
            params = json.dumps(params, ensure_ascii=False)
        payload = {
            "DeviceCode": self.APPID,
            "AuthKey": self.auth_key or "0" * 36,
            "Method": method,
            "Params": params or "",
        }
        last_exc = None
        for attempt in range(1, 4):
            kwargs = {
                "headers": self._headers(),
                "data": {"RequestPack": json.dumps(payload, ensure_ascii=False)},
                "timeout": REQUEST_TIMEOUT,
                "verify": False,
            }
            proxy = self._get_proxy()
            if proxy:
                kwargs["proxies"] = {"http": proxy, "https": proxy}
            try:
                resp = requests.post(self.BASE_URL, **kwargs)
                if resp.status_code in [429, 500, 502, 503, 504] and attempt < 3:
                    time.sleep(2)
                    continue
                resp.raise_for_status()
                return self._parse_response(resp)
            except Exception as exc:
                last_exc = exc
                if attempt < 3:
                    time.sleep(2)
                    continue
        raise RuntimeError(str(last_exc) if last_exc else "请求失败")

    def legacy_key(self):
        return hashlib.md5(self.auth_key.encode()).hexdigest()[:10]

    def query_member_info(self):
        if not self.auth_key:
            raise RuntimeError("AuthKey为空")
        data = self.call("MemberService.GetMyMemberInfo", "")
        if data.get("Return") != 0:
            raise RuntimeError(f"AuthKey无效或已过期: {data.get('Return')}")
        info = data.get("Result") or {}
        if not isinstance(info, dict):
            info = {}
        self.member_info = info
        self.member_id = str(info.get("ID") or self.legacy_key())
        self.nickname = str(info.get("RealName") or info.get("NickName") or f"伊利QQ星_{mask_account(self.member_id)}")
        return info

    def get_points_balance(self):
        try:
            data = self.call("PointsService.GetPointsBalance", "")
            if data.get("Return") == 0 and isinstance(data.get("Result"), dict):
                return data.get("Result") or {}
        except:
            pass
        return {}

    def get_info(self):
        try:
            info = self.query_member_info()
            points_info = self.get_points_balance()
            points = points_info.get("Points", info.get("PointsBalance", 0))
            try:
                points_num = int(float(points or 0))
            except:
                points_num = 0
            msg = (
                f"✅ AuthKey有效\n"
                f"👤 昵称: {self.nickname}\n"
                f"🏅 等级: {info.get('MemberLevelName') or '未知'}\n"
                f"💰 积分: {points}"
            )
            return True, True, points_num, msg
        except Exception as e:
            text = str(e)
            if "AuthKey无效" in text or "-10" in text:
                return True, False, 0, text
            return False, True, 0, text

    def verify_ck(self):
        net_ok, is_valid, _, _ = self.get_info()
        return False if net_ok and not is_valid else True

    def check_info(self):
        info = self.query_member_info()
        acc_key = str(info.get("ID") or self.legacy_key())
        nickname = self.nickname or f"伊利QQ星_{mask_account(acc_key)}"
        return {
            'nickname': nickname,
            'phone': acc_key,
            'acc_key': acc_key,
            'acc_type': 'member_id',
            'aliases': [self.legacy_key()],
            'legacy_key': self.legacy_key(),
            'final_token': self.auth_key,
        }

CastClient = YiLiQQStarClient

class RemarkManager:
    @staticmethod
    def get_account_remark(user_id, account_id):
        try:
            remark_data = sg.bucketGet(bucket=plugin_bucket('remarks'), key=f'{user_id}_{account_id}')
            return str(remark_data) if remark_data else ""
        except: return ""

    @staticmethod
    def set_account_remark(user_id, account_id, remark):
        try:
            remark_clean = str(remark).strip()[:20]
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
                if remark: remarks[str(account)] = remark
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
            account = str(account)
            accounts = AccountManager.get_accounts(user_id)
            if account not in accounts:
                accounts.append(account)
                sg.bucketSet(bucket=plugin_bucket('user'), key=str(user_id), value=str(accounts))
                return True
            return False
        except: return False

    @staticmethod
    def remove_account(user_id, account):
        try:
            account = str(account)
            accounts = AccountManager.get_accounts(user_id)
            if account in accounts:
                accounts.remove(account)
                if accounts:
                    sg.bucketSet(bucket=plugin_bucket('user'), key=str(user_id), value=str(accounts))
                else:
                    sg.bucketDel(bucket=plugin_bucket('user'), key=str(user_id))
                return True
            return False
        except: return False

    @staticmethod
    def update_account_token(account, token):
        try:
            encrypted_token = encrypt_token(str(token))
            sg.bucketSet(bucket=plugin_bucket('token'), key=str(account), value=encrypted_token)
            return True
        except: return False

    @staticmethod
    def get_token(account):
        try:
            enc = sg.bucketGet(bucket=plugin_bucket('token'), key=str(account))
            return decrypt_token(enc) if enc else None
        except: return None

    @staticmethod
    def get_all_users():
        try:
            users = sg.bucketAllKeys(bucket=plugin_bucket('user'))
            user_list = []
            for user in users:
                accounts = AccountManager.get_accounts(user)
                if accounts: user_list.append(str(user))
            return user_list
        except: return []

    @staticmethod
    def migrate_account(user_id, old_account, new_account, new_token, remark=""):
        try:
            old_account = str(old_account)
            new_account = str(new_account)
            if not old_account or not new_account or old_account == new_account:
                return False

            accounts = AccountManager.get_accounts(user_id)
            if old_account not in accounts:
                return False

            old_vip = '2099-12-31'
            new_vip = '2099-12-31'
            if old_vip and (not new_vip or str(old_vip) > str(new_vip)):
                pass
            old_bind_date = sg.bucketGet(bucket=plugin_bucket('bind_date'), key=old_account)
            if old_bind_date and not sg.bucketGet(bucket=plugin_bucket('bind_date'), key=new_account):
                sg.bucketSet(bucket=plugin_bucket('bind_date'), key=new_account, value=old_bind_date)

            if config['enable_remark']:
                old_remark = RemarkManager.get_account_remark(user_id, old_account)
                final_remark = remark or old_remark
                if final_remark:
                    RemarkManager.set_account_remark(user_id, new_account, final_remark)
                RemarkManager.delete_account_remark(user_id, old_account)

            new_accounts = []
            for acc in accounts:
                if acc == old_account:
                    acc = new_account
                if acc not in new_accounts:
                    new_accounts.append(acc)
            sg.bucketSet(bucket=plugin_bucket('user'), key=str(user_id), value=str(new_accounts))

            AccountManager.update_account_token(new_account, new_token)
            try: sg.bucketDel(bucket=plugin_bucket('token'), key=old_account)
            except: pass
            try:
                pass
            except: pass
            return True
        except Exception as e:
            logger.error(f"Account migrate failed: {e}")
            return False

    @staticmethod
    def find_migration_source(user_id, new_account, aliases=None, acc_type="", legacy_key=""):
        try:
            new_account = str(new_account)
            legacy_key = str(legacy_key or "")
            aliases = [str(x) for x in (aliases or []) if str(x)]

            new_ids = set(aliases)
            if acc_type != "token_md5":
                new_ids.add(new_account)
            if legacy_key:
                new_ids.discard(legacy_key)

            for old_account in AccountManager.get_accounts(user_id):
                old_account = str(old_account)
                if old_account == new_account:
                    continue
                if old_account in new_ids:
                    return old_account

                old_token = AccountManager.get_token(old_account)
                if not old_token:
                    continue

                old_client = CastClient(old_token)
                old_info = old_client.check_info()
                old_ids = set(old_info.get('aliases', []))
                if old_info.get('acc_type') != "token_md5":
                    old_ids.add(str(old_info.get('acc_key', "")))
                old_legacy = str(old_info.get('legacy_key', ""))
                if old_legacy:
                    old_ids.discard(old_legacy)

                if new_ids and old_ids and (new_ids & old_ids):
                    return old_account
            return ""
        except Exception as e:
            logger.error(f"Find migration source failed: {e}")
            return ""

class SystemAPI:
    def __init__(self):
        self.enabled = False
        self.panel_type = config.get('panel_type', 'qinglong')
        ql_config = config['env_qlconfig']
        try:
            if not ql_config: raise ValueError("对接配置为空")
            qllist = ql_config.split('丨')
            if len(qllist) != 3: raise ValueError("对接配置格式错误")
            self.QLurl = qllist[0].strip().rstrip('/')
            self.ClientID = qllist[1].strip()
            self.ClientSecret = qllist[2].strip()

            if self.panel_type == 'daidai':
                self.access_token = self._get_daidai_token()
            else:
                self.qltoken = self._get_ql_token()
            self.enabled = True
        except Exception as e:
            logger.error(f"系统初始化失败: {e}")

    def _get_ql_token(self):
        try:
            url = f"{self.QLurl}/open/auth/token?client_id={self.ClientID}&client_secret={self.ClientSecret}"
            response = requests.get(url, timeout=10, verify=False)
            if response.status_code == 200:
                return response.json()['data']['token']
            raise Exception("获取青龙Token失败")
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
                url = f"{self.QLurl}/api/envs?keyword={config['env_name']}&page_size=9999"
                headers = {"Authorization": f"Bearer {self.access_token}", "accept": "application/json"}
                response = requests.get(url, headers=headers, timeout=10, verify=False)
                if response.status_code == 200:
                    return response.json().get('data', [])
                return []
            else:
                url = f"{self.QLurl}/open/envs"
                headers = {"Authorization": f"Bearer {self.qltoken}", "accept": "application/json"}
                response = requests.get(url, headers=headers, timeout=10, verify=False)
                if response.status_code == 200:
                    return response.json()['data']
                return []
        except: return []

    def find_env(self, phone, token=None):
        if not self.enabled: return None
        phone = str(phone)
        try:
            envs = self.get_all_envs()
            for env in envs:
                if env.get('name') != config['env_name']: continue

                env_id = env.get('id') if env.get('id') is not None else env.get('_id')

                if env.get('remarks') and f'ID:{phone}' in env.get('remarks'):
                    return env_id

                if env.get('remarks') and phone in env.get('remarks'):
                    return env_id

                if token and env.get('value'):
                    env_val = env.get('value').strip()
                    input_val = str(token).strip()
                    if input_val in env_val:
                        return env_id

            return None
        except: return None

    def find_env_ids(self, phone, token=None):
        if not self.enabled: return []
        phone = str(phone)
        token = str(token or "").strip()
        try:
            envs = self.get_all_envs()
            matched_ids = []
            matched_set = set()
            for env in envs:
                if env.get('name') != config['env_name']:
                    continue

                env_id = env.get('id') if env.get('id') is not None else env.get('_id')
                if env_id is None:
                    continue

                env_remarks = str(env.get('remarks') or '')
                env_value = str(env.get('value') or '').strip()
                is_match = False

                if env_remarks and f'ID:{phone}' in env_remarks:
                    is_match = True
                elif env_remarks and phone in env_remarks:
                    is_match = True
                elif token and env_value and token in env_value:
                    is_match = True

                if is_match:
                    env_id_key = str(env_id)
                    if env_id_key not in matched_set:
                        matched_set.add(env_id_key)
                        matched_ids.append(env_id)

            return matched_ids
        except:
            return []

    def delete_env(self, phone, token=None):
        if not self.enabled: return False
        phone = str(phone)
        try:
            env_ids = self.find_env_ids(phone, token)
            if not env_ids:
                env_id = self.find_env(phone, token)
                if env_id is not None:
                    env_ids = [env_id]
            if not env_ids:
                return False

            if self.panel_type == 'daidai':
                headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
                success = False
                for env_id in env_ids:
                    url = f"{self.QLurl}/api/envs/{env_id}"
                    res = requests.delete(url, headers=headers, timeout=10, verify=False)
                    if res.status_code == 200:
                        success = True
                return success
            else:
                url = f"{self.QLurl}/open/envs"
                headers = {"Authorization": f"Bearer {self.qltoken}", "Content-Type": "application/json"}
                res = requests.delete(url, headers=headers, json=env_ids, timeout=10, verify=False)
                return res.status_code == 200
        except: return False

    def sync_env(self, token, phone, remark="", auth_time="", owner_user_id=None):
        if not self.enabled: return False
        phone = str(phone)
        try:
            env_id = self.find_env(phone, token)

            ql_value = f"{token}"

            safe_phone = phone[:3] + "****" + phone[-3:] if len(phone) > 6 else phone
            remarks_parts = [f'伊利QQ星:{safe_phone}']
            if remark: remarks_parts.append(f'备注:{remark}')

            owner_user = get_owner_user_id(phone, owner_user_id)
            if not owner_user:
                raise Exception("无法确认账号真实归属，已阻止写入面板备注，避免青龙数据错乱")
            remarks_parts.extend([f'用户:{owner_user}', f'ID:{phone}', '伊利QQ星提交'])
            final_remark = '丨'.join(remarks_parts)

            if self.panel_type == 'daidai':
                headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
                if env_id is not None:
                    url = f"{self.QLurl}/api/envs/{env_id}"
                    data = {"name": config['env_name'], "value": ql_value, "remarks": final_remark}
                    res = requests.put(url, headers=headers, json=data, timeout=10, verify=False)
                    if res.status_code == 200:
                        try: requests.put(f"{self.QLurl}/api/envs/{env_id}/enable", headers=headers, timeout=5, verify=False)
                        except: pass
                    else: return False
                else:
                    url = f"{self.QLurl}/api/envs"
                    data = {"name": config['env_name'], "value": ql_value, "remarks": final_remark}
                    res = requests.post(url, headers=headers, json=data, timeout=10, verify=False)
                    if res.status_code != 200: return False
            else:
                headers = {"Authorization": f"Bearer {self.qltoken}", "Content-Type": "application/json"}
                url = f"{self.QLurl}/open/envs"
                if env_id is not None:
                    data = {"value": ql_value, "name": config['env_name'], "remarks": final_remark}
                    if isinstance(env_id, int) or str(env_id).isdigit():
                        data["id"] = env_id
                    else:
                        data["_id"] = env_id

                    res = requests.put(url, headers=headers, json=data, timeout=10, verify=False)
                    if res.status_code == 200:
                        try: requests.put(f"{self.QLurl}/open/envs/enable", headers=headers, json=[env_id], timeout=5, verify=False)
                        except: pass
                    else: return False
                else:
                    data = [{"value": ql_value, "name": config['env_name'], "remarks": final_remark}]
                    res = requests.post(url, headers=headers, json=data, timeout=10, verify=False)
                    if res.status_code != 200: return False
            return True
        except Exception as e:
            logger.error(f"Sync Env Error: {e}")
            return False

try:
    sys_api = SystemAPI()
    if not sys_api.enabled and sender.getImtype() != 'fake':
        sender.reply("⚠️ 系统API初始化失败，青龙/呆呆同步功能不可用，请检查配置。")
except:
    sys_api = type('obj', (object,), {'enabled': False, 'sync_env': lambda *a, **k: None, 'delete_env': lambda *a, **k: None})()
    if sender.getImtype() != 'fake':
        sender.reply("⚠️ 系统API初始化异常，青龙/呆呆同步功能不可用，请检查配置。")


def process_single_account_query(account,index,total,remarks):
    account=str(account);token=AccountManager.get_token(account) or '';display=get_account_display(account,remarks.get(account,''))
    if not token:return f'{index}/{total} {display}：凭证不存在'
    try:
        net_ok,valid,points,message=YiLiQQStarClient(token).get_info()
        if not net_ok:return f'{index}/{total} {display}：网络异常 {message}'
        if not valid:return f'{index}/{total} {display}：登录失效 {message}'
        return f'{index}/{total} {display}：积分 {points}，{message}'
    except Exception as error:return f'{index}/{total} {display}：查询失败 {error}'

def cxs():
    accounts=AccountManager.get_accounts(userid)
    if not accounts:return sender.reply('未绑定账号，请发送【伊利登录】')
    remarks=RemarkManager.get_all_remarks(userid);sender.reply('请输入查询序号，a 查询全部，q 退出\n'+'\n'.join(f'{i}. {get_account_display(str(a),remarks.get(str(a),""))}' for i,a in enumerate(accounts,1)))
    choice=get_user_input()
    if not choice or choice=='q':return
    targets=list(enumerate(accounts,1)) if choice=='a' else []
    if not targets:
        indexes,_=parse_index_selection(choice,len(accounts),False);targets=[(i,accounts[i-1]) for i in indexes]
    if not targets:return sender.reply('序号无效')
    for index,account in targets:
        message=process_single_account_query(account,index,len(accounts),remarks)
        if message:sender.reply(message)



def get_user_input(timeout=60):
    try:
        response = sender.listen(timeout * 1000)
        if not response: return None
        response = normalize_listen_text(response)
        if response.lower() in ['q', 'quit', 'exit', '退出', 'cancel', '取消']: return 'q'
        return response
    except: return None

def normalize_listen_text(response):
    if response is None:
        return ""
    if isinstance(response, str):
        return response.strip()
    if isinstance(response, dict):
        for key in ("message", "text", "content", "msg"):
            value = response.get(key)
            if value:
                return str(value).strip()
    return str(response).strip()




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




def bindaccount():
    try:
        remark = ""
        if config['enable_remark']:
            sender.reply("""
=====账号备注设置=====
🎯 请输入账号备注名
(批量提交时此备注将应用到所有账号)
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

        sender.reply("""
=====伊利QQ星 登录=====
------------------
👉 请直接发送账号配置，格式如下(一行一个)支持批量登录：
AuthKey
------------------
回复"q"退出操作
==================""")

        input_str = get_user_input(timeout=120)
        if not input_str or input_str.lower() == 'q':
            sender.reply("✅ 已取消")
            return

        token_lines = []
        raw_lines = [line.strip() for line in input_str.split('\n') if line.strip()]
        for line in raw_lines:
            token_lines.append(line.strip())

        if not token_lines:
            sender.reply("❌ 内容为空")
            return

        sender.reply(f"⏳ 正在处理 {len(token_lines)} 个账号，请稍候...")
        bind_stats = {"success": 0, "fail": 0, "new": 0, "update": 0, "migrate": 0}
        fail_msgs = []

        for line in token_lines:
            try:
                line_val = line.strip()
                parts = [p.strip() for p in line_val.split('#') if p.strip()]
                line_remark = remark

                if len(parts) >= 2:
                    auth_candidates = [p for p in parts if re.search(r'[0-9a-fA-F-]{32,64}', p)]
                    if auth_candidates:
                        final_token_str = auth_candidates[-1]
                        remark_candidates = [p for p in parts if p != final_token_str]
                        if remark_candidates:
                            line_remark = remark_candidates[0][:20]
                    else:
                        final_token_str = parts[-1]
                        line_remark = parts[0][:20] if parts[0] != final_token_str else line_remark
                elif len(parts) == 1:
                    final_token_str = parts[0]
                else:
                    bind_stats["fail"] += 1
                    fail_msgs.append("格式错误: 需提供AuthKey")
                    if len(token_lines) == 1:
                        sender.reply("❌ 格式错误: 请提供 AuthKey、AuthKey#备注 或 备注#AuthKey。")
                    continue

                client = CastClient(final_token_str)
                info_res = client.check_info()

                nick = info_res['nickname']
                final_token_str = info_res['final_token']
                acc_id = info_res['acc_key']
                aliases = info_res.get('aliases', [])
                acc_type = info_res.get('acc_type', '')
                legacy_key = info_res.get('legacy_key', '')

                bind_result = process_account_binding(final_token_str, acc_id, nick, line_remark, aliases, acc_type, legacy_key, silent=(len(token_lines) > 1))
                if bind_result.get("ok"):
                    bind_stats["success"] += 1
                    bind_stats[bind_result.get("action", "update")] += 1
                    if bind_result.get("migrated"):
                        bind_stats["migrate"] += 1
                else:
                    bind_stats["fail"] += 1
                    fail_msgs.append(bind_result.get("msg", "处理失败"))
            except Exception as ex:
                bind_stats["fail"] += 1
                fail_msgs.append(str(ex)[:30])
                if len(token_lines) == 1:
                    sender.reply(f"❌ 登录处理失败: {str(ex)}")

        if len(token_lines) > 1:
            fail_text = ""
            if fail_msgs:
                fail_text = "\n❌ 失败原因: " + "；".join(list(dict.fromkeys(fail_msgs))[:3])
            sender.reply(f"""=====伊利QQ星登录汇总=====
✅ 成功: {bind_stats['success']} 个
🆕 新增: {bind_stats['new']} 个
🔄 更新: {bind_stats['update']} 个
🔁 承接旧账号: {bind_stats['migrate']} 个
❌ 失败: {bind_stats['fail']} 个{fail_text}
==================""")

    except Exception as e:
        logger.error(f"绑定失败: {e}")
        sender.reply(f"❌ 绑定失败: {e}")

def process_account_binding(full_token,unique_id,nickname,remark='',aliases=None,acc_type='',legacy_key='',silent=False):
    try:
        account=str(unique_id);aliases=[str(x) for x in aliases or [] if str(x)!=account];existing=AccountManager.get_accounts(userid)
        if account not in existing:
            old=AccountManager.find_migration_source(userid,account,aliases,acc_type,legacy_key)
            if old:AccountManager.migrate_account(userid,old,account,full_token,remark)
        is_new=AccountManager.add_account(userid,account);AccountManager.update_account_token(account,full_token)
        if remark:RemarkManager.set_account_remark(userid,account,remark)
        synced=bool(sys_api.sync_env(full_token,account,remark,'')) if sys_api.enabled else False
        if not silent:sender.reply(f'{get_account_display(account,remark)} 绑定成功；'+('面板同步成功' if synced else '仅本地保存'))
        return {'ok':True,'account':account,'action':'new' if is_new else 'update'}
    except Exception as error:
        if not silent:sender.reply(f'绑定失败：{error}')
        return {'ok':False,'msg':str(error)}


def xy_manage():
    accounts=AccountManager.get_accounts(userid)
    if not accounts:return sender.reply('未绑定账号，请发送【伊利登录】')
    remarks=RemarkManager.get_all_remarks(userid);sender.reply('伊利QQ星账号：\n'+'\n'.join(f'{i}. {get_account_display(str(a),remarks.get(str(a),""))}' for i,a in enumerate(accounts,1))+'\n回复序号管理，q 退出')
    choice=get_user_input()
    if not choice or choice=='q':return
    try:account=str(accounts[int(choice)-1])
    except (ValueError,IndexError):return sender.reply('序号无效')
    manage_single_account(account,remarks)





def manage_single_account(account,remarks):
    token=AccountManager.get_token(account) or '';remark=remarks.get(account,'')
    sender.reply('1. 删除账号\n2. 修改备注\n3. 重新同步面板\nq. 退出');choice=get_user_input()
    if choice=='1':
        sender.reply('回复 y 确认删除')
        if get_user_input()=='y':AccountManager.remove_account(userid,account);sys_api.delete_env(account);RemarkManager.delete_account_remark(userid,account);sender.reply('账号已删除')
    elif choice=='2':
        sender.reply('请输入新备注，n 清空');new=get_user_input()
        if new=='n':RemarkManager.delete_account_remark(userid,account);new=''
        elif new:RemarkManager.set_account_remark(userid,account,new[:20])
        else:return
        if token and sys_api.enabled:sys_api.sync_env(token,account,new,'')
        sender.reply('备注已更新')
    elif choice=='3':
        if not token:return sender.reply('凭证不存在，请重新登录')
        sender.reply('面板同步成功' if sys_api.sync_env(token,account,remark,'') else '面板同步失败或未配置')






def show_tutorial():
    sender.reply('【伊利登录】绑定或更新账号；【伊利查询】查询会员和积分；【伊利管理】删除、备注或重新同步面板。')


command=usermessage.strip().replace('伊利qq星','伊利QQ星').replace('伊利Qq星','伊利QQ星').replace('伊利qQ星','伊利QQ星')
if command in ('伊利登录','伊利登陆','登录伊利','登陆伊利','伊利QQ星登录','伊利QQ星登陆','登录伊利QQ星','登陆伊利QQ星'):bindaccount()
elif command in ('伊利管理','管理伊利','伊利QQ星管理','管理伊利QQ星'):xy_manage()
elif command in ('伊利查询','查询伊利','伊利QQ星查询','查询伊利QQ星'):cxs()
elif command in ('伊利教程','伊利QQ星教程'):show_tutorial()
else:sender.setContinue()
