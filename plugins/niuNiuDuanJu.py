# [title: 牛牛短剧]
# [name: niuNiuDuanJu]
# [language: python]
# [class: 任务]
# [author: huawei]
# [version: v1.1]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^牛牛(登录|登陆|查询|管理|清理|教程|上传|上传青龙|上传呆呆)$]
# [cron: 30 8 * * *]
# [icon: https://tg.96218.xyz/file/BQACAgUAAxkDAAIHFmnWkfnJZmy8WvxGVwUfxeodeYpbAAKrHwACEl6xVmklajBDFl5AOwQ.png]
# [description: 指令：；牛牛登录：绑定或更新 token（支持多号换行，格式：备注#token）；牛牛教程：查看 token 提交说明；牛牛上传青龙：强制上传到青龙；牛牛上传呆呆：强制上传到呆呆面板；牛牛清理：清理失效或过期账号；更新：1.1 查询结果新增余额显示；脚本地址]
# [depe: ["requests"]]


import asyncio as _sg_asyncio, os as _sg_os, time as _sg_time, types as _sg_types, json as _sg_json, re as _sg_re, urllib.parse as _sg_urlparse
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
    'G_NNDJ_ql_config': form.string().title('青龙配置').default('').description('青龙面板配置，格式：地址丨ID丨密钥'),
    'G_NNDJ_ql_envname': form.string().title('环境变量名').default('G_NNDJ_TOKEN').description('推送到青龙或呆呆的环境变量名'),
    'G_NNDJ_use_daidai': form.boolean().title('使用呆呆面板').default(False).description('勾选后默认上传呆呆，不勾选默认上传青龙'),
    'G_NNDJ_daidai_config': form.string().title('呆呆配置').default('').description('呆呆面板配置，格式：地址丨app_key丨app_secret'),
    'G_NNDJ_daidai_group': form.string().title('呆呆分组').default('牛牛短剧').description('呆呆分组名称，不填默认项目名'),
})
_CONFIG_FIELD_MAP = {
    ('G_NNDJ', 'ql_config'): 'G_NNDJ_ql_config',
    ('G_NNDJ', 'ql_envname'): 'G_NNDJ_ql_envname',
    ('G_NNDJ', 'use_daidai'): 'G_NNDJ_use_daidai',
    ('G_NNDJ', 'daidai_config'): 'G_NNDJ_daidai_config',
    ('G_NNDJ', 'daidai_group'): 'G_NNDJ_daidai_group',
}

import base64
import json
import re
import time
from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List, Optional, Tuple

import requests



PROJECT_NAME = "牛牛短剧"
PROJECT_ALIAS = "nndj"
API_ROOT = "https://api.tianjinzhitongdaohe.com/sqx_fast"
BUCKET_CONFIG = "G_NNDJ"
BUCKET_USER = "G_NNDJ_user"
BUCKET_TOKEN = "G_NNDJ_token"
BUCKET_AUTH = "G_NNDJ_auth"
DEFAULT_QL_ENVNAME = "G_NNDJ_TOKEN"
DEFAULT_TIMEOUT = 20
PAY_POLL_TIMES = 60
PAY_POLL_INTERVAL_MS = 5000
DEFAULT_PAY_TYPE_NAMES = {
    "alipay": "支付宝",
    "wxpay": "微信支付",
    "qqpay": "QQ钱包",
}

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = str(sender.getUserID() or "").strip()


class BindError(RuntimeError):
    pass


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


def decode_jwt_payload(token: str) -> Dict[str, Any]:
    parts = str(token or "").split(".")
    if len(parts) != 3:
        return {}
    payload = parts[1]
    padding = "=" * (-len(payload) % 4)
    try:
        raw = base64.urlsafe_b64decode((payload + padding).encode("ascii")).decode("utf-8", errors="ignore")
        data = json.loads(raw)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


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


def remove_user_account(account_key: str, uid: Optional[str] = None):
    current_uid = str(uid or userid or "").strip()
    accounts = get_user_accounts(current_uid)
    if account_key not in accounts:
        return False
    accounts.remove(account_key)
    save_user_accounts(accounts, current_uid)
    return True


def get_token_info(account_key: str) -> Dict[str, str]:
    raw = sg.bucketGet(BUCKET_TOKEN, account_key) or ""
    parts = str(raw).split("#", 2)
    if len(parts) < 2:
        return {}
    return {
        "note": decode_note(parts[0]),
        "token": parts[1].strip(),
        "saved_at": parts[2].strip() if len(parts) >= 3 else "",
    }


def save_token_info(account_key: str, note: str, token: str):
    value = "#".join([encode_note(note), str(token or "").strip(), time.strftime("%Y-%m-%d %H:%M:%S")])
    sg.bucketSet(BUCKET_TOKEN, account_key, value)


def get_auth(account_key: str) -> str:
    return '2099-12-31'


def save_auth(account_key: str, expire_date: str):
    return True


def is_authorized(account_key: str) -> bool:
    return True


def get_auth_status(account_key: str) -> str:
    return '2099-12-31'


def find_account_owners(account_key: str, exclude_uid: Optional[str] = None) -> List[str]:
    result = []
    current_exclude = str(exclude_uid or "").strip()
    for current_uid in get_all_user_ids():
        if current_exclude and current_uid == current_exclude:
            continue
        if account_key in get_user_accounts(current_uid):
            result.append(current_uid)
    return unique_keep_order(result)

def http_get(path: str, token: Optional[str] = None, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    headers = {"content-type": "application/x-www-form-urlencoded"}
    if token:
        headers["token"] = token
    response = requests.get(f"{API_ROOT}{path}", headers=headers, params=params or {}, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    data = response.json()
    return data if isinstance(data, dict) else {}


def fetch_profile(token: str) -> Dict[str, Any]:
    return http_get("/app/user/selectUserById", token=token)


def fetch_balance(token: str) -> Dict[str, Any]:
    return http_get("/app/integral/selectByUserId", token=token)


def fetch_money_balance(token: str) -> Dict[str, Any]:
    return http_get("/app/invite/selectInviteMoney", token=token)


def extract_user_id(token: str, data: Optional[Dict[str, Any]] = None) -> str:
    payload = decode_jwt_payload(token)
    sub = str(payload.get("sub") or "").strip()
    if sub:
        return sub
    info = data or {}
    for key in ["id", "userId", "uid"]:
        value = str(info.get(key) or "").strip()
        if value:
            return value
    return ""


def extract_name(data: Optional[Dict[str, Any]] = None) -> str:
    info = data or {}
    for key in ["nickName", "nickname", "name", "userName", "username", "mobile"]:
        value = str(info.get(key) or "").strip()
        if value:
            return value
    return ""


def parse_pay_types(raw_value: Any) -> Dict[str, str]:
    return {}


def format_money(amount: Decimal) -> str:
    return str(amount.quantize(Decimal("0.00")))


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
        '2099-12-31'
        or payment_config.get("zsm")
        or sg.bucketGet("dd_sign_config", "zsm")
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
    }


def get_ql_client():
    config = get_config()
    if QingLongClient is None or not config.get("ql_config"):
        return None
    client = QingLongClient(
        config.get("ql_envname"),
        config.get("ql_config"),
        config_bucket=BUCKET_CONFIG,
        config_key="ql_config",
        env_name_key="ql_envname",
    )
    return client if client.is_configured() else None


def get_daidai_client():
    config = get_config()
    if DadaiPanelClient is None or not config.get("daidai_config"):
        return None
    client = DadaiPanelClient(
        config.get("ql_envname"),
        config.get("daidai_config"),
        config_bucket=BUCKET_CONFIG,
        config_key="daidai_config",
        env_name_key="ql_envname",
        group_key="daidai_group",
        project_name=PROJECT_NAME,
    )
    return client if client.is_configured() else None


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


def build_panel_status_lines() -> List[str]:
    config = get_config()
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
        "=====牛牛上传目标=====",
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


def ensure_upload_target_ready(target: str) -> bool:
    ql_ready = bool(get_ql_client())
    daidai_ready = bool(get_daidai_client())
    if target == "qinglong" and not ql_ready:
        sender.reply("❌ 未配置青龙面板，无法上传")
        return False
    if target == "daidai" and not daidai_ready:
        sender.reply("❌ 未配置呆呆面板，无法上传")
        return False
    if target == "both" and not ql_ready and not daidai_ready:
        sender.reply("❌ 青龙和呆呆都未配置，无法上传")
        return False
    return True


def upload_authorized_accounts(
    accounts: List[str],
    owner_map: Optional[Dict[str, str]] = None,
    force_target: Optional[str] = None,
    manual_select: bool = False,
):
    return True


def sync_account(account_key: str, owner_id: Optional[str] = None, force_target: Optional[str] = None) -> bool:
    token_info = get_token_info(account_key)
    token = str(token_info.get("token") or "").strip()
    if not token:
        return False
    remark = f"{PROJECT_NAME}:{account_key}|备注:{token_info.get('note') or account_key}|用户:{owner_id or userid}|到期:{get_auth(account_key) or '未授权'}"
    target = get_target(force_target)
    if target == "both":
        ql_ok = False
        daidai_ok = False
        ql_client = get_ql_client()
        if ql_client:
            ql_ok = bool(ql_client.update_env(username=account_key, env_value=token, remark=remark))
        daidai_client = get_daidai_client()
        if daidai_client:
            daidai_ok = bool(daidai_client.update_env(username=account_key, env_value=token, remark=remark, project_name=PROJECT_NAME))
        return ql_ok or daidai_ok
    if target == "daidai":
        client = get_daidai_client()
        return bool(client and client.update_env(username=account_key, env_value=token, remark=remark, project_name=PROJECT_NAME))
    client = get_ql_client()
    return bool(client and client.update_env(username=account_key, env_value=token, remark=remark))


def delete_panel_env(account_key: str):
    ql_client = get_ql_client()
    if ql_client:
        try:
            ql_client.delete_env(account_key)
        except Exception:
            pass
    daidai_client = get_daidai_client()
    if daidai_client:
        try:
            daidai_client.delete_env(account_key)
        except Exception:
            pass


def parse_submit_text(raw_text: str) -> List[Dict[str, str]]:
    lines = str(raw_text or "").replace("\r\n", "\n").replace("\r", "\n").split("\n")
    result = []
    for index, line in enumerate(lines, 1):
        current = line.strip()
        if not current:
            continue
        if "#" not in current:
            raise BindError(f"第 {index} 行格式错误，请使用：备注#token")
        note, token = current.split("#", 1)
        note = note.strip()
        token = token.strip()
        if not note or not token:
            raise BindError(f"第 {index} 行格式错误，请使用：备注#token")
        result.append({"note": note, "token": token})
    if not result:
        raise BindError("提交内容为空")
    return result


def validate_token(token: str) -> Dict[str, Any]:
    result = fetch_profile(token)
    if result.get("code") != 0:
        raise BindError(f"token 校验失败：{result.get('msg') or result.get('code')}")
    data = result.get("data")
    if not isinstance(data, dict):
        raise BindError("资料接口返回格式异常")
    user_id = extract_user_id(token, data)
    if not user_id:
        raise BindError("无法提取 userId")
    return {"user_id": user_id, "name": extract_name(data)}


def bind_accounts():
    sender.reply("=====牛牛登录=====\n请输入：备注#token\n支持换行批量\n回复 q 退出")
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
    ok = 0
    fail = []
    for item in items:
        try:
            info = validate_token(item.get("token"))
            account_key = str(info.get("user_id") or "").strip()
            if find_account_owners(account_key, exclude_uid=userid):
                raise BindError("该账号已被其他用户绑定")
            add_user_account(account_key)
            save_token_info(account_key, item.get("note"), item.get("token"))
            if is_authorized(account_key):
                sync_account(account_key, owner_id=userid)
            ok += 1
        except Exception as exc:
            fail.append(f"{item.get('note')}: {exc}")
    lines = [f"提交完成\n成功: {ok}\n失败: {len(fail)}"]
    if fail:
        lines.extend(fail[:10])
    sender.reply("\n".join(lines))


def build_rows(accounts: List[str]) -> List[Dict[str, str]]:
    rows = []
    for account_key in accounts:
        info = get_token_info(account_key)
        rows.append({
            "key": account_key,
            "note": str(info.get("note") or account_key).strip(),
            "status": get_auth_status(account_key),
        })
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


def format_balance_money(value: Any) -> str:
    if value in (None, ""):
        return "未知"
    try:
        return format_money(safe_decimal(value, "0"))
    except Exception:
        text = str(value).strip()
        return text or "未知"


def extract_balance_money(money_result: Optional[Dict[str, Any]]) -> str:
    data = money_result.get("data") if isinstance(money_result, dict) else {}
    if not isinstance(data, dict):
        return "未知"
    invite_money = data.get("inviteMoney")
    if isinstance(invite_money, dict):
        for key in ("money", "moneySum", "cashOut"):
            if invite_money.get(key) not in (None, ""):
                return format_balance_money(invite_money.get(key))
    for key in ("money", "balance", "userMoney", "amount", "cash", "withdrawableMoney"):
        if data.get(key) not in (None, ""):
            return format_balance_money(data.get(key))
    return "未知"


def build_query_result_message(
    account_key: str,
    token_info: Dict[str, str],
    profile_result: Optional[Dict[str, Any]] = None,
    balance_result: Optional[Dict[str, Any]] = None,
    money_result: Optional[Dict[str, Any]] = None,
    error: Optional[str] = None,
    index: Optional[int] = None,
    total: Optional[int] = None,
) -> str:
    note = str(token_info.get("note") or account_key).strip()
    lines = ["=====牛牛查询====="]
    if index is not None and total:
        lines.append(f"📍 账号序号: {index}/{total}")
    lines.append(f"🏷 备注: {note}")
    if error:
        lines.append(f"❌ 查询失败: {error}")
        lines.append("====================")
        return "\n".join(lines)

    balance_data = balance_result.get("data") if isinstance(balance_result, dict) else {}
    gold = "未知"
    if isinstance(balance_data, dict):
        gold = str(balance_data.get("integralNum") or "0")
    lines.extend([
        f"💰 金币: {gold}",
        f"💵 余额: {extract_balance_money(money_result)}",
        f"🛡 {format_status_for_query(get_auth_status(account_key))}",
        "====================",
    ])
    return "\n".join(lines)


def select_accounts_for_action(accounts: List[str], title: str) -> List[str]:
    rows = build_rows(accounts)
    lines = [
        f"====={title}=====",
        f"📦 绑定账号: {len(rows)}个",
        "--------------------",
    ]
    for index, row in enumerate(rows, 1):
        lines.append(f"[{index}] {row.get('note')} | {row.get('key')}")
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
    selected = select_accounts_for_action(accounts, "牛牛查询")
    if not selected:
        return
    total = len(selected)
    for idx, account_key in enumerate(selected, 1):
        info = get_token_info(account_key)
        try:
            result = fetch_profile(info.get("token"))
            balance = fetch_balance(info.get("token"))
            try:
                money_balance = fetch_money_balance(info.get("token"))
            except Exception:
                money_balance = None
            sender.reply(build_query_result_message(account_key, info, result, balance, money_balance, index=idx, total=total))
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
        "=====牛牛管理=====",
        f"📦 绑定账号: {len(rows)}个",
        f"✅ 已授权: {authorized_count}个",
        f"⏳ 未授权: {pending_count}个",
        f"📊 当前积分: {get_manage_points(userid)}",
        "--------------------",
    ]
    for index, row in enumerate(rows, 1):
        lines.append(f"[{index}] {row.get('note')} | {row.get('key')}")
        lines.append(f"     状态: {format_status_for_menu(row.get('status'))}")
    lines.extend([
        "--------------------",
        "[0] 所有账号授权（支付）",
        "[9998] 删除所有账号",
        "[9999] 未授权账号授权",
        "支持格式：1 或 1,3 或 2-4",
        "提示：发送「牛牛上传」可进入独立上传菜单",
        "回复序号选择（q退出）",
        "====================",
    ])
    return "\n".join(lines)


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
            info = get_token_info(account_key)
            label = str(info.get("note") or account_key).strip()
            if days_left < 0:
                lines.append(f"❌ {label} 已过期 {abs(days_left)} 天，到期: {expire_text}")
            elif days_left <= 3:
                lines.append(f"⚠️ {label} 剩余 {days_left} 天，到期: {expire_text}")
        if not lines:
            continue
        content = "=====牛牛账号提醒=====\n" + "\n".join(lines)
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
        "=====牛牛批量操作=====\n"
        f"📦 数量: {len(selected)}\n"
        "[1] 查询账号\n"
        "[2] 授权账号\n"
        "[3] 删除账号\n"
        "[4] 上传默认面板\n"
        "[5] 上传并选择目标\n"
        "说明：上传时仅同步已授权账号\n"
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
        total = len(selected)
        for idx, account_key in enumerate(selected, 1):
            info = get_token_info(account_key)
            try:
                result = fetch_profile(info.get("token"))
                balance = fetch_balance(info.get("token"))
                try:
                    money_balance = fetch_money_balance(info.get("token"))
                except Exception:
                    money_balance = None
                sender.reply(build_query_result_message(account_key, info, result, balance, money_balance, index=idx, total=total))
            except Exception as exc:
                sender.reply(build_query_result_message(account_key, info, error=str(exc), index=idx, total=total))
        return
    if action == "2":
        handle_authorize_accounts(selected, force_payment=True)
        return
    if action == "3":
        delete_accounts(selected, owner_map={account: userid for account in selected})
        return
    if action == "4":
        upload_authorized_accounts(selected, owner_map={account: userid for account in selected})
        return
    if action == "5":
        upload_authorized_accounts(selected, owner_map={account: userid for account in selected}, manual_select=True)
        return
    sender.reply("❌ 无效选择")


def upload_accounts(force_target: Optional[str] = None):
    target = get_target(force_target) if force_target else choose_upload_target(include_both=True)
    if not target:
        return
    if sender.isAdmin():
        sender.reply(
            f"=====牛牛上传=====\n"
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
            token_info = get_token_info(account_key)
            if not token_info:
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
                    warning_map.setdefault(current_uid, []).append(
                        f"⚠️ {token_info.get('note') or account_key} 剩余 {days_left} 天，到期: {expire_text}"
                    )
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
        if push_notice(current_uid, "账号状态提醒", "=====牛牛账号提醒=====\n" + "\n".join(lines)):
            notified_users += 1

    sender.reply(
        "=====牛牛清理完成=====\n"
        f"👤 影响用户: {affected_users}\n"
        f"⚠️ 临期提醒: {warning_count}\n"
        f"📤 已推送用户: {notified_users}\n"
        f"📱 移除绑定: {removed_bind_count}\n"
        f"🗑 全局删除: {removed_global_count}\n"
        "===================="
    )


def show_tutorial():
    sender.reply(
        "=====牛牛教程=====\n"
        "1. 提交格式：备注#token\n"
        "2. #小程序://牛牛短剧/YeooKG8yVePqsco\n"
        "\n可用命令：\n"
        "牛牛登录 - 提交备注#token，支持换行批量\n"
        "牛牛查询 - 查询已绑定账号资料\n"
        "牛牛管理 - 授权 / 上传 / 删除 / 批量操作\n"
        "牛牛授权 - 管理员授权入口\n"
        "牛牛上传 - 手动选择上传目标\n"
        "牛牛上传青龙 - 直接上传到青龙面板\n"
        "牛牛上传呆呆 - 直接上传到呆呆面板\n"
        "牛牛清理 - 清理过期或无效账号\n"
        "牛牛教程 - 查看本帮助"
    )


def main():
    message = str(sender.getMessage() or "").strip()
    imtype = str(sender.getImtype() or "").strip().lower()
    if re.match(r"^牛牛(登录|登陆)$", message, re.I):
        bind_accounts()
    elif re.match(r"^牛牛查询$", message, re.I):
        query_accounts()
    elif re.match(r"^牛牛管理$", message, re.I):
        manage_accounts()
    elif re.match(r"^牛牛授权$", message, re.I):
        authorize_user_accounts()
    elif re.match(r"^牛牛上传青龙$", message, re.I):
        upload_accounts("qinglong")
    elif re.match(r"^牛牛上传呆呆$", message, re.I):
        upload_accounts("daidai")
    elif re.match(r"^牛牛上传$", message, re.I):
        upload_accounts()
    elif re.match(r"^牛牛清理$", message, re.I):
        clean_accounts()
    elif re.match(r"^牛牛教程$", message, re.I):
        show_tutorial()
    elif imtype == "fake":
        push_auth_status_notifications()
    else:
        sender.setContinue()


main()
