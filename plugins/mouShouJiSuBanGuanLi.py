# [title: 某手极速版管理]
# [name: mouShouJiSuBanGuanLi]
# [language: python]
# [class: 任务]
# [author: 8165799]
# [version: v1.5.1]
# [public: true]
# [disable: false]
# [admin: true]
# [rule: ^某手极速版(登录|登陆|查询|管理|教程)?$|^登(录|陆)某手极速版$|^(查询|管理)某手极速版$|^ks(login|query|manage)$]
# [icon: https://api.iconify.design/lucide:bot.svg]
# [description: 某手极速版账号登录、查询、面板同步与管理]
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
    'ks_nebula_panel_type': plugin.Form.string().title('对接面板类型').default('').description('qinglong=青龙面板 daidai=呆呆面板'),
    'ks_nebula_ks_nebula_qlname': plugin.Form.string().title('对接系统配置').default('').description('青龙:URL丨ID丨Secret 呆呆:URL丨Key丨Secret'),
    'ks_nebula_ks_nebula_osname': plugin.Form.string().title('系统变量名').default('').description('系统容器内变量名(默认为ksck)'),
    'ks_nebula_enable_proxy': plugin.Form.boolean().title('启用代理').default(False).description('是否启用代理功能'),
    'ks_nebula_proxy_pool_url': plugin.Form.string().title('代理池地址').default('').description('代理API服务地址'),
    'ks_nebula_enable_remark': plugin.Form.boolean().title('启用备注功能').default(False).description('是否启用账号备注功能'),
})
_CONFIG_FIELD_MAP = {
    ('ks_nebula', 'panel_type'): 'ks_nebula_panel_type',
    ('ks_nebula', 'ks_nebula_qlname'): 'ks_nebula_ks_nebula_qlname',
    ('ks_nebula', 'ks_nebula_osname'): 'ks_nebula_ks_nebula_osname',
    ('ks_nebula', 'enable_proxy'): 'ks_nebula_enable_proxy',
    ('ks_nebula', 'proxy_pool_url'): 'ks_nebula_proxy_pool_url',
    ('ks_nebula', 'enable_remark'): 'ks_nebula_enable_remark',
}

import re
import ast
from datetime import datetime, timedelta
import gzip
from decimal import Decimal
import requests
import time
import hashlib
import logging
import base64
import warnings
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.error import HTTPError, URLError
from urllib.request import Request, ProxyHandler, build_opener

warnings.filterwarnings('ignore', message='Unverified HTTPS request')
requests.packages.urllib3.disable_warnings()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ks_nebula_plugin')

REQUEST_TIMEOUT = 30
MAINTENANCE_CK_MAX_WORKERS = 8

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = str(sender.getUserID())
usermessage = sender.getMessage()

try:
    sg.bucketSet(bucket='ks_nebula_sender', key=userid, value=str(senderID))
    sg.bucketSet(bucket='ks_nebula_imtype', key=userid, value=str(sender.getImtype()))
except:
    pass

def getusercontent():
    panel_type=(sg.bucketGet('ks_nebula','panel_type') or 'qinglong').lower()
    panel_config=sg.bucketGet('ks_nebula','ks_nebula_qlname') or ''
    if not panel_config:
        sender.reply('❌ 请先配置青龙或呆呆面板信息')
        raise SystemExit
    return {
        'panel_type': panel_type,
        'env_name': sg.bucketGet('ks_nebula','ks_nebula_osname') or 'ksck',
        'env_qlconfig': panel_config,
        'randommanagecommand': '某手极速版管理',
        'randomquerycommand': '某手极速版查询',
        'randomsigncommand': '某手极速版登录',
        'enable_proxy': str(sg.bucketGet('ks_nebula','enable_proxy') or 'false').lower()=='true',
        'proxy_pool_url': sg.bucketGet('ks_nebula','proxy_pool_url') or '',
        'enable_remark': str(sg.bucketGet('ks_nebula','enable_remark') or 'false').lower()=='true',
    }

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
        for owner in sg.bucketAllKeys(bucket='ks_nebula_user'):
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


















def build_panel_env_value(token, remark=""):
    token = str(token or "").strip()
    remark = str(remark or "").strip()
    if not remark:
        return token

    parts = [p.strip() for p in token.split('#') if p.strip()]
    if not parts:
        return token

    if 'kuaishou.api_st=' in token or 'kpn=' in token or ('=' in token and token.count(';') >= 2):
        if token.startswith(f"{remark}#"):
            return token
        return f"{remark}#{token}"

    cookie_idx = -1
    for idx, part in enumerate(parts):
        if 'kuaishou.api_st=' in part or 'kpn=' in part or ('=' in part and part.count(';') >= 2):
            cookie_idx = idx
            break

    if cookie_idx >= 0:
        tail = parts[cookie_idx + 1:]
        if tail:
            return '#'.join([remark, parts[cookie_idx]] + tail[:1])
        return f"{remark}#{parts[cookie_idx]}"

    if token.startswith(f"{remark}#"):
        return token
    return f"{remark}#{token}"

def parse_ks_submission_line(line, default_remark=""):
    line = str(line or "").strip()
    default_remark = str(default_remark or "").strip()
    if not line:
        return "", "", "内容为空"

    first_hash = line.find('#')
    if first_hash > 0:
        head = line[:first_hash].strip()
        rest = line[first_hash + 1:].strip()
        if rest and ('kuaishou.api_st=' in rest or 'kpn=' in rest or ('=' in rest and rest.count(';') >= 2)):
            return rest, head or default_remark, ""

    if 'kuaishou.api_st=' in line or 'kpn=' in line or ('=' in line and line.count(';') >= 2):
        return line, default_remark, ""

    parts = [p.strip() for p in line.split('#') if p.strip()]
    cookie_idx = -1
    for idx, part in enumerate(parts):
        if 'kuaishou.api_st=' in part or 'kpn=' in part or ('=' in part and part.count(';') >= 2):
            cookie_idx = idx
            break

    if cookie_idx < 0:
        return "", default_remark, "未识别到快手 CK"

    ck = parts[cookie_idx]
    tail = parts[cookie_idx + 1:]
    salt = tail[0] if tail else ""
    remark = default_remark
    if cookie_idx > 0:
        remark = parts[0]
    elif len(tail) >= 2:
        remark = tail[1]
    token = f"{ck}#{salt}" if salt else ck
    return token, remark, ""

def validate_ks_token(token):
    client = ksckClient(token)
    cookie_map = client.cookie_map or {}
    missing = []
    if not cookie_map.get("kuaishou.api_st"):
        missing.append("kuaishou.api_st")
    if not cookie_map.get("ud"):
        missing.append("ud")
    if not cookie_map.get("kpn"):
        missing.append("kpn")
    if missing:
        return False, "CK缺少必要参数: " + ",".join(missing)
    return True, ""


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

def parse_ks_cookie(cookie_text):
    data = {}
    for seg in str(cookie_text or "").split(';'):
        if '=' not in seg:
            continue
        key, value = seg.split('=', 1)
        key = key.strip()
        value = value.strip()
        if key:
            data[key] = value
    return data

class ksckClient:
    def __init__(self, token_str):
        self.token = token_str.strip()
        self.cookie = ""
        self.salt = ""
        self.remark_from_token = ""
        self.cookie_map = {}
        self.uid = ""
        self.uid_type = "ud"
        self.aliases = []
        self._parse_token()

    def _looks_like_cookie(self, text):
        text = str(text or "")
        return "kuaishou.api_st=" in text or "kpn=" in text or ("=" in text and text.count(";") >= 2)

    def _parse_token(self):
        first_hash = self.token.find('#')
        if first_hash > 0:
            head = self.token[:first_hash].strip()
            rest = self.token[first_hash + 1:].strip()
            if rest and self._looks_like_cookie(rest):
                self.remark_from_token = head
                self.cookie = rest
                self.cookie_map = parse_ks_cookie(self.cookie)
                self.uid = (
                    self.cookie_map.get("ud")
                    or self.cookie_map.get("userId")
                    or self.cookie_map.get("did")
                    or self.legacy_key()
                )
                if self.uid == self.legacy_key():
                    self.uid_type = "token_md5"
                for key in ["ud", "did", "oDid", "egid"]:
                    value = self.cookie_map.get(key)
                    if value and value != self.uid:
                        self.aliases.append(value)
                return

        if self._looks_like_cookie(self.token):
            self.cookie = self.token
            self.cookie_map = parse_ks_cookie(self.cookie)
            self.uid = (
                self.cookie_map.get("ud")
                or self.cookie_map.get("userId")
                or self.cookie_map.get("did")
                or self.legacy_key()
            )
            if self.uid == self.legacy_key():
                self.uid_type = "token_md5"
            for key in ["ud", "did", "oDid", "egid"]:
                value = self.cookie_map.get(key)
                if value and value != self.uid:
                    self.aliases.append(value)
            return

        parts = [p.strip() for p in self.token.split('#') if p.strip()]
        cookie_idx = -1
        for idx, part in enumerate(parts):
            if self._looks_like_cookie(part):
                cookie_idx = idx
                break

        if cookie_idx >= 0:
            self.cookie = parts[cookie_idx]
            if cookie_idx > 0:
                self.remark_from_token = parts[0]
            tail = parts[cookie_idx + 1:]
            self.salt = tail[0] if tail else ""
            if len(tail) >= 2 and not self.remark_from_token:
                self.remark_from_token = tail[1]
        else:
            self.cookie = parts[0] if parts else self.token
            self.salt = parts[1] if len(parts) > 1 else ""
            self.remark_from_token = parts[2] if len(parts) > 2 else ""

        self.cookie_map = parse_ks_cookie(self.cookie)
        self.uid = (
            self.cookie_map.get("ud")
            or self.cookie_map.get("userId")
            or self.cookie_map.get("did")
            or self.legacy_key()
        )
        if self.uid == self.legacy_key():
            self.uid_type = "token_md5"
        for key in ["ud", "did", "oDid", "egid"]:
            value = self.cookie_map.get(key)
            if value and value != self.uid:
                self.aliases.append(value)

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
                    proxy = f"http://{proxy}"
                return proxy
        except Exception as e:
            logger.warning(f"某手极速版查询获取代理失败: {e}")
        return None

    def _http_json(self, method, url, body=None, timeout=25, max_retries=3, headers=None):
        payload = body
        if isinstance(payload, str):
            payload = payload.encode("utf-8")
        elif payload is not None:
            payload = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")

        last_exc = None
        for attempt in range(1, max_retries + 1):
            req = Request(url=url, data=payload, method=method.upper())
            request_headers = headers or {}
            for key, value in request_headers.items():
                req.add_header(key, value)

            proxy = self._get_proxy()
            opener = build_opener(ProxyHandler({'http': proxy, 'https': proxy})) if proxy else build_opener()

            try:
                with opener.open(req, timeout=timeout) as response:
                    raw = response.read()
                    if response.headers.get("Content-Encoding", "").lower() == "gzip":
                        raw = gzip.decompress(raw)
                    text = raw.decode("utf-8", errors="replace")
                    return json.loads(text)
            except HTTPError as e:
                last_exc = e
                if attempt < max_retries and e.code in [500, 502, 503, 504]:
                    time.sleep(2)
                    continue
                try:
                    raw = e.read()
                    if e.headers.get("Content-Encoding", "").lower() == "gzip":
                        raw = gzip.decompress(raw)
                    text = raw.decode("utf-8", errors="replace")
                except:
                    text = str(e)
                raise RuntimeError(f"HTTP {e.code}: {text[:120]}") from e
            except (URLError, TimeoutError, json.JSONDecodeError, Exception) as e:
                last_exc = e
                if attempt < max_retries:
                    time.sleep(2)
                    continue
                raise RuntimeError(str(e)) from e

        raise RuntimeError(str(last_exc) if last_exc else "请求失败")

    def legacy_key(self):
        return hashlib.md5(self.token.encode()).hexdigest()[:8]

    def get_info(self):
        try:
            if not self.cookie or "kuaishou.api_st=" not in self.cookie:
                return True, False, 0, "CK缺少 kuaishou.api_st"

            headers = {
                "Host": "nebula.kuaishou.com",
                "Connection": "keep-alive",
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; MI 8 Build/QKQ1.190828.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.101 Mobile Safari/537.36 Yoda/3.2.16-rc4 ksNebula/13.7.20.10468",
                "Accept": "*/*",
                "X-Requested-With": "com.kuaishou.nebula",
                "Cookie": self.cookie,
            }
            result = self._http_json(
                "GET",
                "https://nebula.kuaishou.com/rest/n/nebula/account/overview",
                headers=headers,
            )

            if result.get("result") != 1:
                msg = result.get("error_msg") or result.get("message") or "账号详情获取失败"
                return True, False, 0, msg

            data = result.get("data") or {}
            coin_balance = self.safe_int(data.get("coinBalance", 0))
            cash_balance = data.get("cashBalance", "0")
            total_cash = self.format_money(data.get("accumulativeAmount", "0"))
            nickname = data.get("nickname") or self.remark_from_token or self.uid
            msg = (
                f"✅ CK有效\n"
                f"👤 昵称: {nickname}\n"
                f"💰 金币: {coin_balance} ({coin_balance / 10000:.2f}元)\n"
                f"💵 余额: {cash_balance}元\n"
                f"💎 累计收益: {total_cash}元"
            )
            extra = {
                "nickname": nickname,
                "coin_balance": coin_balance,
                "cash_balance": str(cash_balance),
                "total_cash": str(total_cash),
            }
            return True, True, coin_balance, msg, extra
        except Exception as e:
            return False, True, 0, str(e)

    def safe_int(self, value):
        try:
            if value is None or value == "":
                return 0
            return int(float(str(value)))
        except Exception:
            return 0

    def format_money(self, value):
        try:
            return f"{Decimal(str(value)):.2f}"
        except Exception:
            return str(value)

    def verify_ck(self):
        info_result = self.get_info()
        net_ok, is_valid = info_result[0], info_result[1]
        if net_ok and not is_valid:
            return False
        return True

    def check_info(self):
        if not self.uid:
            self.uid = self.legacy_key()
            self.uid_type = "token_md5"

        safe_id = self.uid[:3] + "****" + self.uid[-3:] if len(self.uid) > 6 else self.uid
        nickname = self.remark_from_token or f"某手极速版_{safe_id}"
        final_token = f"{self.cookie}#{self.salt}" if self.salt else self.cookie

        return {
            "nickname": nickname,
            "phone": self.uid, # 沿用原版字段名保持兼容
            "acc_key": self.uid,
            "acc_type": self.uid_type,
            "aliases": self.aliases,
            "legacy_key": self.legacy_key(),
            "final_token": final_token
        }

class RemarkManager:
    @staticmethod
    def get_account_remark(user_id, account_id):
        try:
            remark_data = sg.bucketGet(bucket='ks_nebula_remarks', key=f'{user_id}_{account_id}')
            return str(remark_data) if remark_data else ""
        except: return ""

    @staticmethod
    def set_account_remark(user_id, account_id, remark):
        try:
            remark_clean = str(remark).strip()[:20]
            if remark_clean:
                sg.bucketSet(bucket='ks_nebula_remarks', key=f'{user_id}_{account_id}', value=remark_clean)
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
            sg.bucketDel(bucket='ks_nebula_remarks', key=f'{user_id}_{account_id}')
            return True
        except: return False

class AccountManager:
    @staticmethod
    def get_accounts(user_id):
        try:
            value = sg.bucketGet(bucket='ks_nebula_user', key=str(user_id))
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
                sg.bucketSet(bucket='ks_nebula_user', key=str(user_id), value=str(accounts))
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
                    sg.bucketSet(bucket='ks_nebula_user', key=str(user_id), value=str(accounts))
                else:
                    sg.bucketDel(bucket='ks_nebula_user', key=str(user_id))
                return True
            return False
        except: return False

    @staticmethod
    def update_account_token(account, token):
        try:
            encrypted_token = encrypt_token(str(token))
            sg.bucketSet(bucket='ks_nebula_token', key=str(account), value=encrypted_token)
            return True
        except: return False

    @staticmethod
    def get_token(account):
        try:
            enc = sg.bucketGet(bucket='ks_nebula_token', key=str(account))
            return decrypt_token(enc) if enc else None
        except: return None

    @staticmethod
    def get_all_users():
        try:
            users = sg.bucketAllKeys(bucket='ks_nebula_user')
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
                True

            old_bind_date = sg.bucketGet(bucket='ks_nebula_bind_date', key=old_account)
            if old_bind_date and not sg.bucketGet(bucket='ks_nebula_bind_date', key=new_account):
                sg.bucketSet(bucket='ks_nebula_bind_date', key=new_account, value=old_bind_date)

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
            sg.bucketSet(bucket='ks_nebula_user', key=str(user_id), value=str(new_accounts))

            AccountManager.update_account_token(new_account, new_token)
            try: sg.bucketDel(bucket='ks_nebula_token', key=old_account)
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

                old_client = ksckClient(old_token)
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
            raise Exception(f"获取青龙Token失败 HTTP {response.status_code}: {response.text[:120]}")
        except Exception: raise

    def _get_daidai_token(self):
        try:
            url = f"{self.QLurl}/api/open-api/token"
            data = {"app_key": self.ClientID, "app_secret": self.ClientSecret}
            response = requests.post(url, json=data, timeout=10, verify=False)
            if response.status_code == 200:
                return response.json()['data']['access_token']
            raise Exception(f"获取呆呆Token失败 HTTP {response.status_code}: {response.text[:120]}")
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

    def sync_env(self, token, phone, remark="", owner_user_id=None):
        if not self.enabled: return False
        phone = str(phone)
        try:
            token_ok, token_error = validate_ks_token(token)
            if not token_ok:
                logger.warning(f"跳过同步不完整CK: account={phone} error={token_error}")
                return False

            env_id = self.find_env(phone, token)

            ql_value = build_panel_env_value(token, remark)

            safe_phone = phone[:3] + "****" + phone[-3:] if len(phone) > 6 else phone
            remarks_parts = [f'某手极速版:{safe_phone}']
            if remark: remarks_parts.append(f'备注:{remark}')

            owner_user = get_owner_user_id(phone, owner_user_id)
            if not owner_user:
                raise Exception("无法确认账号真实归属，已阻止写入面板备注，避免青龙数据错乱")
            remarks_parts.extend([f'用户:{owner_user}', f'ID:{phone}', '某手极速版提交'])
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

def process_single_account_query(account, index=0, total_count=0, account_remarks=None):
    account=str(account)
    token=AccountManager.get_token(account) or ''
    remark=(account_remarks or {}).get(account,'') if config['enable_remark'] else ''
    display=get_account_display(account,remark)
    if len(token)<10:
        return f'❌ {display}: 未保存有效 CK'
    try:
        client=ksckClient(token)
        client.check_info()
        result=client.get_info()
        net_ok,valid,money,msg=result[:4]
        if not net_ok:return f'⚠️ {display}: 网络查询异常：{str(msg)[:60]}'
        if not valid:return f'⚠️ {display}: 登录失效：{str(msg)[:60]}'
        return f'=====某手极速版=====\n👤 {display}\n💰 {money}\n{msg}\n=================='
    except Exception as e:
        return f'❌ {display}: {str(e)[:80]}'

def cxs():
    accounts=[str(x) for x in AccountManager.get_accounts(userid)]
    if not accounts:
        sender.reply(f"❌ 未绑定账号，请发送 {config['randomsigncommand']}")
        return
    remarks=RemarkManager.get_all_remarks(userid) if config['enable_remark'] else {}
    sender.reply('=====某手极速版查询=====\n'+'\n'.join(f'[{i}] {get_account_display(a,remarks.get(a,""))}' for i,a in enumerate(accounts,1))+'\n[a] 全部；支持 1,2 或 3-6；q 退出')
    choice=get_user_input(timeout=60)
    if not choice or choice.lower()=='q':return
    indexes=list(range(1,len(accounts)+1)) if choice.lower()=='a' else parse_index_selection(choice,len(accounts),False)[0]
    if not indexes:
        sender.reply('❌ 序号无效')
        return
    sender.reply(f'⏳ 正在查询 {len(indexes)} 个账号')
    with ThreadPoolExecutor(max_workers=min(8,len(indexes))) as pool:
        futures=[pool.submit(process_single_account_query,accounts[i-1],i,len(accounts),remarks) for i in indexes]
        for future in as_completed(futures):
            result=future.result()
            if result:sender.reply(result)





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
=====某手极速版 登录=====
当前模式: 🌐 提交至面板
------------------
👉 请直接发送账号配置，格式如下(一行一个)：
备注#一键获取的ck
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
                final_token_str, line_remark, parse_error = parse_ks_submission_line(line_val, remark)
                if parse_error:
                    bind_stats["fail"] += 1
                    fail_msgs.append(f"格式错误: {parse_error}")
                    if len(token_lines) == 1:
                        sender.reply("❌ 格式错误: 未识别到快手 CK，请使用 备注#ck。")
                    continue

                token_ok, token_error = validate_ks_token(final_token_str)
                if not token_ok:
                    bind_stats["fail"] += 1
                    fail_msgs.append(token_error)
                    if len(token_lines) == 1:
                        sender.reply(f"❌ CK不完整：{token_error}\n请重新抓取完整 CK 后按 备注#ck 提交。")
                    continue

                client = ksckClient(final_token_str)
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
            sender.reply(f"""=====某手极速版登录汇总=====
✅ 成功: {bind_stats['success']} 个
🆕 新增: {bind_stats['new']} 个
🔄 更新: {bind_stats['update']} 个
🔁 承接旧账号: {bind_stats['migrate']} 个
❌ 失败: {bind_stats['fail']} 个{fail_text}
==================""")

    except Exception as e:
        logger.error(f"绑定失败: {e}")
        sender.reply(f"❌ 绑定失败: {e}")

def process_account_binding(full_token, unique_id, nickname, remark='', aliases=None, acc_type='', legacy_key='', silent=False):
    account=str(unique_id)
    try:
        is_new=AccountManager.add_account(userid,account)
        AccountManager.update_account_token(account,full_token)
        if config['enable_remark'] and remark:
            RemarkManager.set_account_remark(userid,account,remark)
        synced=sys_api.sync_env(full_token,account,remark,owner_user_id=userid)
        if not silent:
            sender.reply(f'✅ {nickname or account} 已保存；面板'+('同步成功' if synced else '未同步'))
        return {'ok':True,'account':account,'action':'new' if is_new else 'update','migrated':False}
    except Exception as e:
        if not silent:sender.reply(f'❌ 入库失败：{e}')
        return {'ok':False,'msg':str(e)}

def xy_manage():
    accounts = [str(x) for x in AccountManager.get_accounts(userid)]
    if not accounts:
        sender.reply(f"❌ 未找到账号，请发送 {config['randomsigncommand']} 绑定")
        return
    sender.reply("=====账号管理=====\n" + "\n".join(
        f"[{i}] {account}" for i, account in enumerate(accounts, 1)
    ) + "\n[d] 删除多个账号\n[q] 退出\n==================")
    choice = get_user_input()
    if not choice or choice.lower() == "q":
        return
    if choice.lower() == "d":
        sender.reply("请输入账号序号，多个用逗号分隔：")
        selected, _ = parse_index_selection(get_user_input(), len(accounts), allow_all=False)
        if selected:
            batch_delete_selected([accounts[i - 1] for i in selected])
        return
    selected, _ = parse_index_selection(choice, len(accounts), allow_all=False)
    if len(selected) == 1:
        manage_single_account(accounts[selected[0] - 1], {})
    elif selected:
        manage_multiple_accounts([accounts[i - 1] for i in selected], {})
    else:
        sender.reply("❌ 序号无效")

def manage_multiple_accounts(selected_accs, account_remarks=None):
    sender.reply(f"确认删除选中的 {len(selected_accs)} 个账号请回复 y")
    if get_user_input().lower() == "y":
        batch_delete_selected(selected_accs)

def manage_single_account(account, account_remarks=None):
    token=AccountManager.get_token(account) or ''
    sender.reply(f'=====账号操作=====\n📱 {account}\n[1] 修改备注\n[2] 查看配置\n[3] 同步面板\n[4] 删除账号')
    choice=get_user_input()
    if choice=='1' and config['enable_remark']:
        sender.reply('请输入新备注：')
        remark=get_user_input()
        if remark and remark.lower()!='q':
            RemarkManager.set_account_remark(userid,account,remark)
            sender.reply('✅ 备注已更新')
    elif choice=='2':sender.reply(token or '❌ 未保存配置')
    elif choice=='3':sender.reply('✅ 同步成功' if token and sys_api.sync_env(token,account,RemarkManager.get_account_remark(userid,account),owner_user_id=userid) else '❌ 同步失败')
    elif choice=='4':
        sender.reply('确认删除请回复 y')
        if get_user_input().lower()=='y':
            AccountManager.remove_account(userid,account)
            RemarkManager.delete_account_remark(userid,account)
            sys_api.delete_env(account,token)
            sender.reply('✅ 删除成功')

def batch_delete_selected(accounts):
    preview = []
    account_remarks = RemarkManager.get_all_remarks(userid) if config['enable_remark'] else {}
    for account in accounts[:5]:
        account = str(account)
        preview.append(get_account_display(account, account_remarks.get(account, "")))
    more = f"\n...等 {len(accounts)} 个账号" if len(accounts) > 5 else ""
    sender.reply(f"=====确认批量删除=====\n已选择 {len(accounts)} 个账号\n{chr(10).join(preview)}{more}\n------------------\n确认删除请回复【确认删除】\n回复 q 取消\n==================")
    if get_user_input() == "确认删除":
        today_date = datetime.now().date()
        for account in accounts:
            try:
                 account = str(account)
                 AccountManager.remove_account(userid, account)
                 token = AccountManager.get_token(account)
                 try: sg.bucketDel(bucket='ks_nebula_token', key=account)
                 except: pass
                 try:
                     pass
                 except: pass
                 if config['enable_remark']: RemarkManager.delete_account_remark(userid, account)
                 sys_api.delete_env(account, token)
                 for d in range(config['reminder_days'] + 1):
                     remind_key = f"{userid}_{account}_{today_date - timedelta(days=d)}"
                     try: sg.bucketDel('ks_nebula_remind_log', remind_key)
                     except: pass
            except: pass
        sender.reply("✅ 批量删除完成")


def show_tutorial():
    sender.reply('=====某手极速版教程=====\n某手极速版登录：提交 备注#CK\n某手极速版查询：查询金币与状态\n某手极速版管理：备注、同步或删除账号\n==================')

try:
    command=usermessage.strip()
    if command in ['某手极速版登录','某手极速版登陆','登录某手极速版','登陆某手极速版','kslogin']:
        bindaccount()
    elif command in ['某手极速版管理','管理某手极速版','ksmanage']:
        xy_manage()
    elif command in ['某手极速版查询','查询某手极速版','ksquery']:
        cxs()
    elif command in ['某手极速版教程','某手极速版']:
        show_tutorial()
except Exception as e:
    logger.error(f'Error: {e}')
    sender.reply(f'❌ 系统错误: {e}')
