# [title: 四个朋友]
# [name: siGePengYou]
# [language: python]
# [class: 任务]
# [author: huawei]
# [version: v1.0.1]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(四个朋友|四友)(登录|登陆|查询|管理|清理|教程|上传|上传青龙|上传呆呆)$]
# [cron: 30 8 * * *]
# [icon: https://tg.96218.xyz/file/BQACAgUAAxkDAAIHH2ndrLaGBqLSp_CBtVTMX_APbIu_AAJVIAAC-STxVqpdpxV5PVduOwQ.png]
# [description: 指令：；四个朋友登录：绑定或更新 user_id（支持多号换行，格式：备注#user_id）；四个朋友教程：查看 user_id 提交说明；四个朋友上传青龙：强制上传到青龙；四个朋友上传呆呆：强制上传到呆呆面板；四个朋友清理：清理失效或过期账号；更新：1.0.0 首版适配 G_SGPY_UID；脚本地址]
# [depe: ["requests","urllib3"]]


import asyncio as _sg_asyncio
import os as _sg_os
import time as _sg_time
import types as _sg_types
import json as _sg_json
import re as _sg_re
from threading import Thread as _sg_Thread
from sillygirl import Adapter as _SGAdapter, Bucket as _SGBucket, Sender as _SGSender, sender as _sg_sender, container as _sg_container, form
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
def get_pay_config(): return {}
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

config = form({
    'G_SGPY_ql_config': form.string().title('青龙配置').default('').description('青龙面板配置，格式：地址丨ID丨密钥'),
    'G_SGPY_ql_envname': form.string().title('环境变量名').default('G_SGPY_UID').description('推送到青龙或呆呆的环境变量名，默认与脚本 G_SGPY_UID 对齐'),
    'G_SGPY_use_daidai': form.boolean().title('使用呆呆面板').default(False).description('勾选后默认上传呆呆，不勾选默认上传青龙'),
    'G_SGPY_daidai_config': form.string().title('呆呆配置').default('').description('呆呆面板配置，格式：地址丨app_key丨app_secret'),
    'G_SGPY_daidai_group': form.string().title('呆呆分组').default('四个朋友').description('呆呆分组名称，不填默认项目名'),
    'G_SGPY_proxy': form.string().title('查询代理').default('').description('仅插件校验与查询接口使用，可留空直连'),
})
_CONFIG_FIELD_MAP = {
    ('G_SGPY', 'ql_config'): 'G_SGPY_ql_config',
    ('G_SGPY', 'ql_envname'): 'G_SGPY_ql_envname',
    ('G_SGPY', 'use_daidai'): 'G_SGPY_use_daidai',
    ('G_SGPY', 'daidai_config'): 'G_SGPY_daidai_config',
    ('G_SGPY', 'daidai_group'): 'G_SGPY_daidai_group',
    ('G_SGPY', 'proxy'): 'G_SGPY_proxy',
}

import base64
import hashlib
import json
import random
import re
import time
import warnings
from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List, Optional, Tuple

import requests
import urllib3

warnings.filterwarnings("ignore", category=urllib3.exceptions.InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



PROJECT_NAME = "四个朋友"
BASE_URL = "https://iot.hs499.com/"
BUCKET_CONFIG = "G_SGPY"
BUCKET_USER = "G_SGPY_user"
BUCKET_TOKEN = "G_SGPY_token"
BUCKET_AUTH = "G_SGPY_auth"
DEFAULT_QL_ENVNAME = "G_SGPY_UID"
DEFAULT_OEM_ID = "300ab330835844d58a8bccfc1c8b0800"
DEFAULT_SIGN_SECRET = ""
DEFAULT_TIMEOUT = 20
PAY_POLL_TIMES = 60
PAY_POLL_INTERVAL_MS = 5000
DEFAULT_PAY_TYPE_NAMES = {
    "alipay": "支付宝",
    "wxpay": "微信支付",
    "qqpay": "QQ钱包",
}
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf2541411) XWEB/16965",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.52(0x18003426) NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_10 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.50(0x1800322f) NetType/4G Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 14; 23013RK75C Build/UKQ1.231003.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/120.0.6099.144 Mobile Safari/537.36 MicroMessenger/8.0.53.2800(0x2800353D) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android",
]

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = str(sender.getUserID() or "").strip()


class BindError(RuntimeError):
    pass


class FourFriendsClient:
    def __init__(self, user_id: str, oem_id: str, sign_secret: str, proxy: str = ""):
        self.user_id = str(user_id or "").strip()
        self.oem_id = str(oem_id or DEFAULT_OEM_ID).strip() or DEFAULT_OEM_ID
        self.sign_secret = str(sign_secret or DEFAULT_SIGN_SECRET).strip() or DEFAULT_SIGN_SECRET
        self.proxy = str(proxy or "").strip()
        self.session = requests.Session()
        self.session.verify = False
        self.session.headers.update(
            {
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "*/*",
                "User-Agent": random.choice(USER_AGENTS),
            }
        )
        if self.proxy:
            self.session.proxies.update({"http": self.proxy, "https": self.proxy})

    def _base_payload(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "userId": self.user_id,
            "oemId": self.oem_id,
            "api_version_interceptor": 1,
            "timestamp": int(time.time() * 1000),
            "oemType": 1,
        }

    def _post(self, path: str, extra_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if not self.user_id:
            raise BindError("缺少 user_id")
        payload = self._base_payload()
        if extra_data:
            payload.update(extra_data)
        payload["sign"] = generate_sign(payload, self.sign_secret)
        response = self.session.post(
            BASE_URL.rstrip("/") + "/" + path.lstrip("/"),
            data=payload,
            timeout=DEFAULT_TIMEOUT,
        )
        try:
            data = response.json()
        except Exception as exc:
            raise BindError(f"接口返回非 JSON: {response.text[:120]}") from exc
        if response.status_code != 200:
            raise BindError(f"接口返回 HTTP {response.status_code}")
        if not isinstance(data, dict):
            raise BindError("接口返回格式异常")
        return data

    def welfare_index(self) -> Dict[str, Any]:
        return self._post("applet/activity/welfare/index")


def parse_bool(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if value in (None, ""):
        return default
    return str(value).strip().lower() in {"true", "1", "yes", "y", "on", "是"}


def safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(str(value).strip())
    except Exception:
        return default


def safe_decimal(value: Any, default: str = "0") -> Decimal:
    try:
        return Decimal(str(value).strip() or default)
    except (InvalidOperation, TypeError, ValueError):
        return Decimal(default)


def unique_keep_order(items: List[str]) -> List[str]:
    result = []
    seen = set()
    for item in items:
        text = str(item or "").strip()
        if not text or text in seen:
            continue
        seen.add(text)
        result.append(text)
    return result


def sanitize_text(value: Any, max_len: int = 32) -> str:
    text = str(value or "").replace("\r", " ").replace("\n", " ").replace("|", " ").strip()
    return text[:max_len]


def parse_selection(choice: str, max_idx: int) -> Optional[List[int]]:
    if not choice or not choice.strip():
        return None
    indices = set()
    try:
        for part in choice.strip().split(","):
            current = part.strip()
            if not current:
                continue
            if "-" in current:
                start_text, end_text = current.split("-", 1)
                start = int(start_text.strip())
                end = int(end_text.strip())
                if start < 1 or end < 1 or start > max_idx or end > max_idx or start > end:
                    return None
                indices.update(range(start - 1, end))
            else:
                value = int(current)
                if value < 1 or value > max_idx:
                    return None
                indices.add(value - 1)
        return sorted(indices) if indices else None
    except Exception:
        return None


def parse_date(date_text: str):
    if not date_text:
        return None
    try:
        return datetime.strptime(str(date_text).strip(), "%Y-%m-%d").date()
    except Exception:
        return None


def format_money(amount: Decimal) -> str:
    return str(amount.quantize(Decimal("0.00")))


def encode_note(note: str) -> str:
    return base64.urlsafe_b64encode(str(note or "").encode("utf-8")).decode("ascii")


def decode_note(text: str) -> str:
    value = str(text or "").strip()
    if not value:
        return ""
    try:
        padding = "=" * (-len(value) % 4)
        return base64.urlsafe_b64decode((value + padding).encode("ascii")).decode("utf-8", errors="ignore")
    except Exception:
        return value


def mask_account(account_key: str) -> str:
    text = str(account_key or "").strip()
    if not text:
        return "***"
    if len(text) <= 8:
        return text
    if len(text) <= 12:
        return f"{text[:3]}...{text[-3:]}"
    return f"{text[:6]}...{text[-6:]}"


def generate_sign(params: Dict[str, Any], secret: str) -> str:
    ordered_keys = sorted(params.keys())
    joined = "".join(f"{key}={params[key]}" for key in ordered_keys)
    return hashlib.md5((joined + secret).encode("utf-8")).hexdigest()


def get_all_user_ids() -> List[str]:
    raw = sg.bucketGet(BUCKET_CONFIG, "all_user_ids") or ""
    values = [item.strip() for item in str(raw).split(",") if item and str(item).strip()]
    if userid and userid not in values:
        values.append(userid)
    return unique_keep_order(values)


def register_user_id(uid: Optional[str] = None):
    current_uid = str(uid or userid or "").strip()
    if not current_uid:
        return
    values = get_all_user_ids()
    if current_uid not in values:
        values.append(current_uid)
    sg.bucketSet(BUCKET_CONFIG, "all_user_ids", ",".join(unique_keep_order(values)))


def get_user_accounts(uid: Optional[str] = None) -> List[str]:
    current_uid = str(uid or userid or "").strip()
    raw = sg.bucketGet(BUCKET_USER, current_uid) or ""
    return unique_keep_order(str(raw).split(","))


def save_user_accounts(accounts: List[str], uid: Optional[str] = None):
    current_uid = str(uid or userid or "").strip()
    values = unique_keep_order(accounts)
    if values:
        sg.bucketSet(BUCKET_USER, current_uid, ",".join(values))
    else:
        try:
            sg.bucketDel(BUCKET_USER, current_uid)
        except Exception:
            sg.bucketSet(BUCKET_USER, current_uid, "")


def add_user_account(account_key: str, uid: Optional[str] = None):
    current_uid = str(uid or userid or "").strip()
    register_user_id(current_uid)
    accounts = get_user_accounts(current_uid)
    if account_key not in accounts:
        accounts.append(account_key)
        save_user_accounts(accounts, current_uid)


def remove_user_account(account_key: str, uid: Optional[str] = None) -> bool:
    current_uid = str(uid or userid or "").strip()
    accounts = get_user_accounts(current_uid)
    if account_key not in accounts:
        return False
    accounts.remove(account_key)
    save_user_accounts(accounts, current_uid)
    return True


def find_account_owners(account_key: str, exclude_uid: Optional[str] = None) -> List[str]:
    result = []
    current_exclude = str(exclude_uid or "").strip()
    for current_uid in get_all_user_ids():
        if current_exclude and current_uid == current_exclude:
            continue
        if account_key in get_user_accounts(current_uid):
            result.append(current_uid)
    return unique_keep_order(result)


def get_account_info(account_key: str) -> Dict[str, str]:
    raw = str(sg.bucketGet(BUCKET_TOKEN, account_key) or "").strip()
    if not raw:
        return {}
    parts = raw.split("#", 1)
    note = decode_note(parts[0]) if parts else ""
    return {
        "note": note,
        "saved_at": parts[1].strip() if len(parts) > 1 else "",
    }


def save_account_info(account_key: str, note: str):
    value = "#".join([encode_note(note), time.strftime("%Y-%m-%d %H:%M:%S")])
    sg.bucketSet(BUCKET_TOKEN, account_key, value)


def get_auth(account_key: str) -> str:
    return '2099-12-31'


def save_auth(account_key: str, expire_date: str):
    return True


def is_authorized(account_key: str) -> bool:
    return True


def get_auth_status(account_key: str) -> str:
    return '2099-12-31'


def parse_pay_types(raw_value: Any) -> Dict[str, str]:
    return {}


def get_config() -> Dict[str, Any]:
    payment_config = get_pay_config() if callable(get_pay_config) else {}
    pay_types = payment_config.get("pay_types") or {}
    if not pay_types:
        pay_types = parse_pay_types(
            '2099-12-31'
            or '2099-12-31'
            or ""
        )
    zsm = (
        sg.bucketGet("dd_sign_config", "zsm")
        or '2099-12-31'
        or payment_config.get("zsm")
        or ""
    )
    return {
        "price": safe_decimal(sg.bucketGet(BUCKET_CONFIG, "price") or "0.88", "0.88"),
        "coin": safe_int(sg.bucketGet(BUCKET_CONFIG, "coin") or "0", 0),
        "zsm": str(zsm).strip(),
        "ma_pay_switch": parse_bool(
            payment_config.get("ma_pay_switch")
            or '2099-12-31'
            or "false"
        ),
        "pay_types": pay_types,
        "ql_config": str(sg.bucketGet(BUCKET_CONFIG, "ql_config") or "").strip(),
        "ql_envname": str(sg.bucketGet(BUCKET_CONFIG, "ql_envname") or DEFAULT_QL_ENVNAME).strip() or DEFAULT_QL_ENVNAME,
        "use_daidai": parse_bool(sg.bucketGet(BUCKET_CONFIG, "use_daidai") or "false"),
        "daidai_config": str(sg.bucketGet(BUCKET_CONFIG, "daidai_config") or "").strip(),
        "daidai_group": str(sg.bucketGet(BUCKET_CONFIG, "daidai_group") or PROJECT_NAME).strip() or PROJECT_NAME,
        "oem_id": str(sg.bucketGet(BUCKET_CONFIG, "oem_id") or DEFAULT_OEM_ID).strip() or DEFAULT_OEM_ID,
        "sign_secret": str(sg.bucketGet(BUCKET_CONFIG, "sign_secret") or DEFAULT_SIGN_SECRET).strip() or DEFAULT_SIGN_SECRET,
        "proxy": str(sg.bucketGet(BUCKET_CONFIG, "proxy") or "").strip(),
    }


def build_ql_client(config: Optional[Dict[str, Any]] = None):
    config = config or get_config()
    if QingLongClient is None:
        return None, "未配置青龙面板，无法同步"
    client = QingLongClient(
        config.get("ql_envname"),
        config.get("ql_config"),
        config_bucket=BUCKET_CONFIG,
        config_key="ql_config",
        env_name_key="ql_envname",
    )
    if not client.is_configured():
        return None, f"未配置青龙面板，请填写 {BUCKET_CONFIG}.ql_config"
    if not client.get_token():
        return None, "青龙认证失败，请检查地址和 Client 信息"
    return client, ""


def build_daidai_client(config: Optional[Dict[str, Any]] = None):
    config = config or get_config()
    if DadaiPanelClient is None:
        return None, "未配置呆呆面板，无法同步"
    client = DadaiPanelClient(
        config.get("ql_envname"),
        config.get("daidai_config"),
        config_bucket=BUCKET_CONFIG,
        config_key="daidai_config",
        env_name_key="ql_envname",
        group_key="daidai_group",
        project_name=PROJECT_NAME,
    )
    if not client.is_configured():
        return None, f"未配置呆呆面板，请填写 {BUCKET_CONFIG}.daidai_config"
    if not client.get_token():
        detail = getattr(client, "last_error", "") or "请检查 AppKey / AppSecret"
        return None, f"呆呆面板认证失败：{detail}"
    return client, ""


def get_target(force_target: Optional[str] = None) -> str:
    text = str(force_target or "").strip().lower()
    if text in ["qinglong", "ql", "青龙"]:
        return "qinglong"
    if text in ["daidai", "dd", "呆呆"]:
        return "daidai"
    if text in ["both", "all", "全部", "双传", "一起"]:
        return "both"
    config = get_config()
    return "daidai" if config.get("use_daidai") else "qinglong"


def get_target_name(force_target: Optional[str] = None) -> str:
    target = get_target(force_target)
    if target == "qinglong":
        return "青龙面板"
    if target == "daidai":
        return "呆呆面板"
    return "青龙+呆呆"


def build_panel_status_lines(config: Optional[Dict[str, Any]] = None) -> List[str]:
    config = config or get_config()
    default_target = "呆呆面板" if config.get("use_daidai") else "青龙面板"
    ql_status = "已配置" if config.get("ql_config") else "未配置"
    daidai_status = "已配置" if config.get("daidai_config") else "未配置"
    env_name = str(config.get("ql_envname") or DEFAULT_QL_ENVNAME).strip() or DEFAULT_QL_ENVNAME
    return [
        f"⚙️ 默认上传: {default_target}",
        f"🧪 环境变量: {env_name}",
        f"🔄 青龙配置: {ql_status}",
        f"🔄 呆呆配置: {daidai_status}",
    ]


def choose_upload_target(include_both: bool = True) -> Optional[str]:
    default_target_name = get_target_name()
    lines = [
        "=====四个朋友上传目标=====",
        *build_panel_status_lines(),
        f"[1] 默认面板（{default_target_name}）",
        "[2] 青龙面板",
        "[3] 呆呆面板",
    ]
    if include_both:
        lines.append("[4] 青龙+呆呆（双传）")
    lines.extend([
        '回复数字选择，回复 "q" 取消',
        "====================",
    ])
    sender.reply("\n".join(lines))
    choice = sender.input(120000, 1, False)
    if not choice:
        sender.reply("⏰ 操作超时")
        return None
    choice = choice.strip().lower()
    if choice == "q":
        sender.reply("✅ 已取消")
        return None
    if choice == "1":
        return get_target()
    if choice == "2":
        return "qinglong"
    if choice == "3":
        return "daidai"
    if include_both and choice == "4":
        return "both"
    sender.reply("❌ 无效选择")
    return None


def ensure_upload_target_ready(target: str, config: Optional[Dict[str, Any]] = None) -> bool:
    config = config or get_config()
    if target == "qinglong":
        _, msg = build_ql_client(config)
        if msg:
            sender.reply(f"❌ {msg}")
            return False
        return True
    if target == "daidai":
        _, msg = build_daidai_client(config)
        if msg:
            sender.reply(f"❌ {msg}")
            return False
        return True
    ql_client, ql_msg = build_ql_client(config)
    daidai_client, daidai_msg = build_daidai_client(config)
    if ql_client or daidai_client:
        return True
    sender.reply(f"❌ 青龙和呆呆都不可用\n青龙: {ql_msg or '未配置'}\n呆呆: {daidai_msg or '未配置'}")
    return False


def build_env_remark(account_key: str, owner_id: str, expire_date: str) -> str:
    info = get_account_info(account_key)
    note = sanitize_text(info.get("note") or account_key, 24) or account_key
    return f"{PROJECT_NAME}:{account_key}|备注:{note}|用户:{owner_id}|到期:{expire_date}"


def sync_account(account_key: str, owner_id: Optional[str] = None, force_target: Optional[str] = None) -> bool:
    if not account_key:
        return False
    expire_date = get_auth(account_key)
    if not expire_date:
        return False
    config = get_config()
    remark = build_env_remark(account_key, str(owner_id or userid or "").strip(), expire_date)
    env_value = account_key
    target = get_target(force_target)
    if target == "both":
        ql_ok = False
        daidai_ok = False
        ql_client, _ = build_ql_client(config)
        if ql_client:
            try:
                ql_ok = bool(ql_client.update_env(username=account_key, env_value=env_value, remark=remark))
            except Exception:
                ql_ok = False
        daidai_client, _ = build_daidai_client(config)
        if daidai_client:
            try:
                daidai_ok = bool(daidai_client.update_env(username=account_key, env_value=env_value, remark=remark, project_name=PROJECT_NAME))
            except Exception:
                daidai_ok = False
        return ql_ok or daidai_ok
    if target == "daidai":
        client, _ = build_daidai_client(config)
        if not client:
            return False
        try:
            return bool(client.update_env(username=account_key, env_value=env_value, remark=remark, project_name=PROJECT_NAME))
        except Exception:
            return False
    client, _ = build_ql_client(config)
    if not client:
        return False
    try:
        return bool(client.update_env(username=account_key, env_value=env_value, remark=remark))
    except Exception:
        return False


def delete_panel_env(account_key: str):
    config = get_config()
    ql_client, _ = build_ql_client(config)
    if ql_client:
        try:
            ql_client.delete_env(account_key)
        except Exception:
            pass
    daidai_client, _ = build_daidai_client(config)
    if daidai_client:
        try:
            daidai_client.delete_env(account_key)
        except Exception:
            pass


def build_api_client(account_key: str, config: Optional[Dict[str, Any]] = None) -> FourFriendsClient:
    config = config or get_config()
    return FourFriendsClient(
        user_id=account_key,
        oem_id=config.get("oem_id"),
        sign_secret=config.get("sign_secret"),
        proxy=config.get("proxy"),
    )


def get_result_payload(response: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if isinstance(response, dict):
        result = response.get("result")
        if isinstance(result, dict):
            return result
    return {}


def fetch_welfare_snapshot(account_key: str, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    client = build_api_client(account_key, config)
    response = client.welfare_index()
    if response.get("code") != 1:
        raise BindError(str(response.get("msg") or "接口返回失败"))
    return response


def find_task_by_type(result: Dict[str, Any], task_type: int) -> Optional[Dict[str, Any]]:
    for item in result.get("taskInfoList") or []:
        if item.get("type") == task_type:
            return item
    return None


def build_sign_text(result: Dict[str, Any]) -> str:
    sign_info = result.get("signInfo") or {}
    continuous = safe_int(sign_info.get("continuousQuantity"), 0)
    if sign_info.get("todayIsSign") == 1:
        return f"已签到｜连续{continuous}天"
    if sign_info.get("isAllowSign") == 1:
        return f"未签到｜连续{continuous}天"
    return f"不可签到｜连续{continuous}天"


def build_ad_text(result: Dict[str, Any]) -> str:
    ad_task = find_task_by_type(result, 13)
    if not ad_task:
        return "未找到"
    name = sanitize_text(ad_task.get("name") or "广告任务", 18) or "广告任务"
    if ad_task.get("isComplete") == 1:
        return f"{name}｜已完成"
    return f"{name}｜未完成"


def build_pending_text(result: Dict[str, Any]) -> str:
    unclaimed = result.get("unclaimedPrizeList") or []
    if not unclaimed:
        return "0"
    first = sanitize_text((unclaimed[0] or {}).get("prizeAbstracts") or "", 18)
    if first:
        return f"{len(unclaimed)}个｜{first}"
    return f"{len(unclaimed)}个"


def validate_account_binding(account_key: str, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if not str(account_key or "").strip():
        raise BindError("user_id 不能为空")
    snapshot = fetch_welfare_snapshot(account_key, config)
    result = get_result_payload(snapshot)
    user_info = result.get("userInfo") or {}
    return {
        "user_id": account_key,
        "gold_balance": str(user_info.get("goldBalance") or "0"),
    }


def parse_submit_text(raw_text: str) -> List[Dict[str, str]]:
    lines = str(raw_text or "").replace("\r\n", "\n").replace("\r", "\n").split("\n")
    result = []
    for index, line in enumerate(lines, 1):
        current = line.strip()
        if not current:
            continue
        if "#" not in current:
            raise BindError(f"第 {index} 行格式错误，请使用：备注#user_id")
        note, account_key = current.split("#", 1)
        note = note.strip()
        account_key = account_key.strip()
        if not note or not account_key:
            raise BindError(f"第 {index} 行格式错误，请使用：备注#user_id")
        result.append({"note": note, "account_key": account_key})
    if not result:
        raise BindError("提交内容为空")
    return result




def build_rows(accounts: List[str]) -> List[Dict[str, str]]:
    rows = []
    for account_key in accounts:
        info = get_account_info(account_key)
        rows.append(
            {
                "key": account_key,
                "key_masked": mask_account(account_key),
                "note": str(info.get("note") or account_key).strip(),
                "status": get_auth_status(account_key),
            }
        )
    return rows


def format_status_for_menu(status: str) -> str:
    text = str(status or "").strip()
    if text.startswith("已授权:"):
        return f"已授权｜到期: {text.split(':', 1)[1].strip()}"
    if text.startswith("已过期:"):
        return f"已过期｜到期: {text.split(':', 1)[1].strip()}"
    return text


def format_status_for_query(status: str) -> str:
    text = str(status or "").strip()
    if text.startswith("已授权:"):
        return f"已授权｜{text.split(':', 1)[1].strip()}"
    if text.startswith("已过期:"):
        return f"已过期｜{text.split(':', 1)[1].strip()}"
    return text


def bind_accounts():
    sender.reply("=====四个朋友登录=====\n请输入：备注#user_id\n支持换行批量\n回复 \"q\" 退出")
    raw_text = sender.input(120000, 1, False)
    if not raw_text:
        sender.reply("⏰ 操作超时")
        return
    raw_text = str(raw_text).strip()
    if raw_text.lower() == "q":
        sender.reply("✅ 已取消")
        return
    try:
        items = parse_submit_text(raw_text)
    except Exception as exc:
        sender.reply(f"❌ 提交失败\n{exc}")
        return
    config = get_config()
    ok = 0
    fail = []
    auto_sync_ok = []
    auto_sync_fail = []
    for item in items:
        account_key = str(item.get("account_key") or "").strip()
        note = str(item.get("note") or "").strip()
        display_name = note or account_key
        try:
            validate_account_binding(account_key, config)
            if find_account_owners(account_key, exclude_uid=userid):
                raise BindError("该账号已被其他用户绑定")
            add_user_account(account_key)
            save_account_info(account_key, note)
            ok += 1
            if is_authorized(account_key):
                if sync_account(account_key, owner_id=userid):
                    auto_sync_ok.append(display_name)
                else:
                    auto_sync_fail.append(display_name)
        except Exception as exc:
            fail.append(f"{display_name}: {exc}")
    lines = [
        "=====四个朋友登录=====",
        f"📠 提交数量: {len(items)}",
        f"✅ 成功: {ok}",
        f"❌ 失败: {len(fail)}",
        f"📝 当前绑定: {len(get_user_accounts())}个",
    ]
    if auto_sync_ok:
        lines.append(f"🔄 自动同步面板: {len(auto_sync_ok)}")
    if auto_sync_fail:
        lines.append(f"⚠️ 自动同步失败: {len(auto_sync_fail)}")
        lines.extend([f"同步失败: {name}" for name in auto_sync_fail[:10]])
    if fail:
        lines.extend(fail[:10])
    lines.append("您可以发送「四个朋友管理」查看详情")
    sender.reply("\n".join(lines))




def select_accounts_for_action(accounts: List[str], title: str) -> List[str]:
    rows = build_rows(accounts)
    lines = [
        f"====={title}=====",
        f"📦 绑定账号: {len(rows)}个",
        "--------------------",
    ]
    for index, row in enumerate(rows, 1):
        lines.append(f"[{index}] {row.get('note')} | {row.get('key_masked')}")
        lines.append(f"     状态: {format_status_for_menu(row.get('status'))}")
    lines.extend([
        "--------------------",
        "[0] 查询所有账号",
        "支持格式：1 或 1,3 或 2-4",
        "回复序号选择（q退出）",
        "====================",
    ])
    sender.reply("\n".join(lines))
    choice = sender.input(120000, 1, False)
    if not choice:
        sender.reply("⏰ 操作超时")
        return []
    choice = str(choice).strip().lower()
    if choice == "q":
        sender.reply("✅ 已取消")
        return []
    if choice == "0":
        return accounts[:]
    indices = parse_selection(choice, len(accounts))
    if indices is None:
        sender.reply("❌ 选择格式错误")
        return []
    return [accounts[index] for index in indices]


def query_accounts():
    accounts = get_user_accounts()
    if not accounts:
        sender.reply("❌ 当前未绑定账号")
        return
    selected = select_accounts_for_action(accounts, "四个朋友查询")
    if not selected:
        return
    config = get_config()
    total = len(selected)
    for idx, account_key in enumerate(selected, 1):
        info = get_account_info(account_key)
        try:
            snapshot = fetch_welfare_snapshot(account_key, config)
            sender.reply(build_query_result_message(account_key, info, snapshot=snapshot, index=idx, total=total))
        except Exception as exc:
            sender.reply(build_query_result_message(account_key, info, error=str(exc), index=idx, total=total))


def get_manage_points(uid: Optional[str] = None) -> int:
    current_uid = str(uid or userid or "").strip()
    return safe_int(sg.bucketGet("dd_sign_points", current_uid) or "0", 0)


def parse_waitpay_amount(result: Any) -> Decimal:
    if result is None:
        return Decimal("0")
    data = result
    if isinstance(result, str):
        text = result.strip()
        try:
            data = json.loads(text)
        except Exception:
            if "收款金额￥" in text:
                try:
                    amount_text = text.split("收款金额￥", 1)[1].splitlines()[0].strip()
                    return safe_decimal(amount_text, "0")
                except Exception:
                    return Decimal("0")
            return Decimal("0")
    if isinstance(data, dict):
        amount = data.get("Money")
        if amount in (None, ""):
            amount = data.get("money")
        return safe_decimal(amount, "0")
    return Decimal("0")


def process_qrcode_payment(total_price: Decimal) -> bool:
    return True


def choose_ma_pay_type(config: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
    items = list((config.get("pay_types") or {}).items())
    if not items:
        return None, None
    if len(items) == 1:
        return items[0]
    lines = ["=====选择在线处理方式====="]
    for index, item in enumerate(items, 1):
        lines.append(f"[{index}] {item[1]}")
    lines.append('回复序号选择，回复 "q" 取消')
    lines.append("====================")
    sender.reply("\n".join(lines))
    choice = sender.input(120000, 1, False)
    if not choice:
        sender.reply("⏰ 操作超时")
        return None, None
    choice = choice.strip().lower()
    if choice == "q" or not choice.isdigit():
        return None, None
    idx = int(choice) - 1
    if idx < 0 or idx >= len(items):
        return None, None
    return items[idx]


def ma_payment_flow(
    target_label: str,
    months: int,
    amount: Decimal,
    config: Dict[str, Any],
    pay_type_key: Optional[str] = None,
    pay_type_name: Optional[str] = None,
) -> bool:
    return True



def calc_new_expire(account_key: str, months: int) -> str:
    expire = parse_date(get_auth(account_key))
    base_date = expire if expire and expire >= datetime.now().date() else datetime.now().date()
    return (base_date + timedelta(days=30 * months)).strftime("%Y-%m-%d")


def apply_authorization(accounts: List[str], months: int, owner_map: Optional[Dict[str, str]] = None):
    return True


def handle_authorize_accounts(accounts: List[str], owner_map: Optional[Dict[str, str]] = None, force_payment: bool = False):
    return True


def build_manage_accounts_message() -> str:
    accounts = get_user_accounts()
    rows = build_rows(accounts)
    authorized_count = sum(1 for account in accounts if is_authorized(account))
    pending_count = max(0, len(accounts) - authorized_count)
    lines = [
        "=====四个朋友管理=====",
        f"📦 绑定账号: {len(rows)}个",
        f"✅ 已授权: {authorized_count}个",
        f"⏳ 未授权: {pending_count}个",
        f"📊 当前积分: {get_manage_points(userid)}",
        "--------------------",
    ]
    for index, row in enumerate(rows, 1):
        lines.append(f"[{index}] {row.get('note')} | {row.get('key_masked')}")
        lines.append(f"     状态: {format_status_for_menu(row.get('status'))}")
    lines.extend([
        "--------------------",
        "[0] 所有账号授权（支付）",
        "[9997] 同步已授权账号",
        "[9998] 删除所有账号",
        "[9999] 未授权账号授权",
        "支持格式：1 或 1,3 或 2-4",
        "提示：发送「四个朋友上传」可进入独立上传菜单",
        "回复序号选择（q退出）",
        "====================",
    ])
    return "\n".join(lines)


def upload_authorized_accounts(
    accounts: List[str],
    owner_map: Optional[Dict[str, str]] = None,
    force_target: Optional[str] = None,
    manual_select: bool = False,
):
    return True


def delete_accounts(accounts: List[str], owner_map: Optional[Dict[str, str]] = None):
    accounts = unique_keep_order(accounts)
    if not accounts:
        sender.reply("❌ 未选择有效账号")
        return
    sender.reply(f"⚠️ 确认删除 {len(accounts)} 个账号？\n回复 y 确认，回复 q 取消")
    confirm = sender.input(120000, 1, False)
    if not confirm:
        sender.reply("⏰ 操作超时")
        return
    confirm = confirm.strip().lower()
    if confirm == "q":
        sender.reply("✅ 已取消")
        return
    if confirm != "y":
        sender.reply("❌ 已取消")
        return
    for account_key in accounts:
        owner_id = (owner_map or {}).get(account_key, userid)
        remove_user_account(account_key, owner_id)
        if not find_account_owners(account_key):
            delete_panel_env(account_key)
            try:
                sg.bucketDel(BUCKET_TOKEN, account_key)
                True
            except Exception:
                pass
    sender.reply(f"删除完成\n数量: {len(accounts)}")


def push_notice(uid: str, title: str, content: str) -> bool:
    pushed = False
    for platform in ("wx", "qq"):
        try:
            sg.push(platform, "", uid, title, content)
            pushed = True
        except Exception:
            pass
    return pushed


def push_auth_status_notifications():
    pushed_users = 0
    for current_uid in get_all_user_ids():
        lines = []
        for account_key in get_user_accounts(current_uid):
            expire_text = get_auth(account_key)
            expire_date = parse_date(expire_text)
            if not expire_date:
                continue
            days_left = (expire_date - datetime.now().date()).days
            info = get_account_info(account_key)
            label = str(info.get("note") or account_key).strip()
            if days_left < 0:
                lines.append(f"❌ {label} 已过期 {abs(days_left)} 天，到期: {expire_text}")
            elif days_left <= 3:
                lines.append(f"⚠️ {label} 剩余 {days_left} 天，到期: {expire_text}")
        if not lines:
            continue
        content = "=====四个朋友账号提醒=====\n" + "\n".join(lines)
        if push_notice(current_uid, "账号状态提醒", content):
            pushed_users += 1
    return pushed_users


def collect_all_accounts() -> Tuple[List[str], Dict[str, str]]:
    accounts: List[str] = []
    owner_map: Dict[str, str] = {}
    for current_uid in get_all_user_ids():
        for account_key in get_user_accounts(current_uid):
            if account_key not in owner_map:
                owner_map[account_key] = current_uid
            accounts.append(account_key)
    return unique_keep_order(accounts), owner_map


def authorize_user_accounts():
    return True




def upload_accounts(force_target: Optional[str] = None):
    target = get_target(force_target) if force_target else choose_upload_target(include_both=True)
    if not target:
        return
    if sender.isAdmin():
        sender.reply(
            "=====四个朋友上传=====\n"
            + "\n".join(build_panel_status_lines())
            + "\n"
            f"🎯 本次目标: {get_target_name(target)}\n"
            "[1] 上传我的已授权账号\n"
            "[2] 上传所有用户已授权账号\n"
            '回复数字选择，回复 "q" 退出\n'
            "===================="
        )
        choice = sender.input(120000, 1, False)
        if not choice:
            sender.reply("⏰ 操作超时")
            return
        choice = str(choice).strip().lower()
        if choice == "q":
            sender.reply("✅ 已取消")
            return
        if choice == "2":
            accounts, owner_map = collect_all_accounts()
            upload_authorized_accounts(accounts, owner_map=owner_map, force_target=target)
            return
        if choice != "1":
            sender.reply("❌ 无效选择")
            return
    accounts = get_user_accounts()
    if not accounts:
        sender.reply("❌ 当前未绑定账号")
        return
    upload_authorized_accounts(accounts, owner_map={account: userid for account in accounts}, force_target=target)


def clean_accounts():
    user_ids = get_all_user_ids() if sender.isAdmin() else [userid]
    affected_users = 0
    warning_count = 0
    removed_bind_count = 0
    removed_global_count = 0
    notified_users = 0
    warning_map: Dict[str, List[str]] = {}
    removed_global: List[str] = []
    for current_uid in user_ids:
        accounts = get_user_accounts(current_uid)
        if not accounts:
            continue
        remaining = []
        removed_this_user = 0
        for account_key in accounts:
            info = get_account_info(account_key)
            if not info:
                removed_this_user += 1
                removed_bind_count += 1
                removed_global.append(account_key)
                continue
            expire_text = get_auth(account_key)
            expire_date = parse_date(expire_text)
            if expire_date:
                days_left = (expire_date - datetime.now().date()).days
                if days_left < 0:
                    removed_this_user += 1
                    removed_bind_count += 1
                    removed_global.append(account_key)
                    continue
                if days_left <= 3:
                    warning_count += 1
                    warning_map.setdefault(current_uid, []).append(f"⚠️ {info.get('note') or account_key} 剩余 {days_left} 天，到期: {expire_text}")
            remaining.append(account_key)
        if removed_this_user:
            save_user_accounts(remaining, current_uid)
            affected_users += 1
    for account_key in unique_keep_order(removed_global):
        if not find_account_owners(account_key):
            delete_panel_env(account_key)
            try:
                sg.bucketDel(BUCKET_TOKEN, account_key)
                True
            except Exception:
                pass
            removed_global_count += 1
    for current_uid, lines in warning_map.items():
        if push_notice(current_uid, "账号状态提醒", "=====四个朋友账号提醒=====\n" + "\n".join(lines)):
            notified_users += 1
    sender.reply(
        "=====四个朋友清理完成=====\n"
        f"👤 影响用户: {affected_users}\n"
        f"⚠️ 临期提醒: {warning_count}\n"
        f"📤 已推送用户: {notified_users}\n"
        f"📱 移除绑定: {removed_bind_count}\n"
        f"🗑 全局删除: {removed_global_count}\n"
        "===================="
    )


def show_tutorial():
    sender.reply(
        "=====四个朋友教程=====\n"
        "1. 提交格式：备注#user_id\n"
        "2. user_id 对应脚本环境变量 G_SGPY_UID\n"
        "3. 如果脚本端改了 OEM ID 或签名密钥，请同步修改插件参数 G_SGPY.oem_id / G_SGPY.sign_secret\n"
        "4. 默认上传环境变量名：G_SGPY_UID\n"
        "\n可用命令：\n"
        "四个朋友登录 - 提交备注#user_id，支持换行批量\n"
        "四个朋友查询 - 查询金币、可兑余额、签到与授权状态\n"
        "四个朋友管理 - 授权 / 上传 / 删除 / 批量操作\n"
        "四个朋友授权 - 管理员授权入口\n"
        "四个朋友上传 - 手动选择上传目标\n"
        "四个朋友上传青龙 - 直接上传到青龙面板\n"
        "四个朋友上传呆呆 - 直接上传到呆呆面板\n"
        "四个朋友清理 - 清理过期或无效账号\n"
        "四个朋友教程 - 查看本帮助"
    )


def build_query_result_message(
    account_key: str,
    info: Dict[str, str],
    snapshot: Optional[Dict[str, Any]] = None,
    error: Optional[str] = None,
    index: Optional[int] = None,
    total: Optional[int] = None,
) -> str:
    note = str(info.get("note") or account_key).strip()
    lines = ["=====四个朋友查询====="]
    if index is not None and total:
        lines.append(f"📍 账号序号: {index}/{total}")
    lines.append(f"🏷 备注: {note}")
    lines.append(f"🛡 {format_status_for_query(get_auth_status(account_key))}")
    if error:
        lines.append(f"❌ 查询失败: {error}")
        lines.append("====================")
        return "\n".join(lines)
    result = get_result_payload(snapshot)
    user_info = result.get("userInfo") or {}
    lines.extend(
        [
            f"💵 余额: {user_info.get('goldBalance') or 0}",
            f"📅 签到: {build_sign_text(result)}",
            f"🎞 广告任务: {build_ad_text(result)}",
            "====================",
        ]
    )
    return "\n".join(lines)


def manage_accounts():
    accounts = get_user_accounts()
    if not accounts:
        sender.reply("❌ 当前未绑定账号")
        return
    sender.reply(build_manage_accounts_message())
    choice = sender.input(120000, 1, False)
    if not choice:
        sender.reply("⏰ 操作超时")
        return
    choice = choice.strip().lower()
    if choice == "q":
        sender.reply("✅ 已取消")
        return
    if choice == "0":
        handle_authorize_accounts(accounts, force_payment=True)
        return
    if choice == "9997":
        upload_authorized_accounts(accounts, owner_map={account: userid for account in accounts})
        return
    if choice == "9998":
        delete_accounts(accounts, owner_map={account: userid for account in accounts})
        return
    if choice == "9999":
        pending = [account for account in accounts if not is_authorized(account)]
        if not pending:
            sender.reply("✅ 当前没有未授权账号")
            return
        handle_authorize_accounts(pending, force_payment=True)
        return
    indices = parse_selection(choice, len(accounts))
    if indices is None:
        sender.reply("❌ 选择格式错误")
        return
    selected = [accounts[index] for index in indices]
    if not selected:
        sender.reply("❌ 未选择账号")
        return
    sender.reply(
        "=====四个朋友批量操作=====\n"
        f"📦 数量: {len(selected)}\n"
        "[1] 查询账号\n"
        "[2] 授权账号\n"
        "[3] 删除账号\n"
        '回复序号选择，回复 "q" 返回\n'
        "===================="
    )
    action = sender.input(120000, 1, False)
    if not action:
        sender.reply("⏰ 操作超时")
        return
    action = action.strip().lower()
    if action == "q":
        sender.reply("✅ 已取消")
        return
    if action == "1":
        config = get_config()
        total = len(selected)
        for idx, account_key in enumerate(selected, 1):
            info = get_account_info(account_key)
            try:
                snapshot = fetch_welfare_snapshot(account_key, config)
                sender.reply(build_query_result_message(account_key, info, snapshot=snapshot, index=idx, total=total))
            except Exception as exc:
                sender.reply(build_query_result_message(account_key, info, error=str(exc), index=idx, total=total))
        return
    if action == "2":
        handle_authorize_accounts(selected, force_payment=True)
        return
    if action == "3":
        delete_accounts(selected, owner_map={account: userid for account in selected})
        return
    sender.reply("❌ 无效选择")


def main():
    message = str(sender.getMessage() or "").strip()
    imtype = str(sender.getImtype() or "").strip().lower()
    if re.match(r"^(四个朋友|四友)(登录|登陆)$", message, re.I):
        bind_accounts()
    elif re.match(r"^(四个朋友|四友)查询$", message, re.I):
        query_accounts()
    elif re.match(r"^(四个朋友|四友)管理$", message, re.I):
        manage_accounts()
    elif re.match(r"^(四个朋友|四友)授权$", message, re.I):
        authorize_user_accounts()
    elif re.match(r"^(四个朋友|四友)上传青龙$", message, re.I):
        upload_accounts("qinglong")
    elif re.match(r"^(四个朋友|四友)上传呆呆$", message, re.I):
        upload_accounts("daidai")
    elif re.match(r"^(四个朋友|四友)上传$", message, re.I):
        upload_accounts()
    elif re.match(r"^(四个朋友|四友)清理$", message, re.I):
        clean_accounts()
    elif re.match(r"^(四个朋友|四友)教程$", message, re.I):
        show_tutorial()
    elif imtype == "fake":
        push_auth_status_notifications()
    else:
        sender.setContinue()


main()
