# [title: 爱路桥]
# [name: aiLuQiao]
# [language: python]
# [class: 任务]
# [author: rujingxianghai]
# [version: v1.3.0]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(爱路桥|alq)(登录|登陆)$|^登(录|陆)(爱路桥|alq)$|^(爱路桥|alq)(查询|管理|检测|教程)$|^(查询|管理|检测|教程)(爱路桥|alq)$]
# [cron: 18 9 * * *]
# [icon: https://api.iconify.design/lucide:apple.svg]
# [description: 。]
# [depe: ["cryptography","requests"]]
import asyncio as _sg_asyncio
import os as _sg_os
import time as _sg_time
import types as _sg_types
import json as _sg_json
import re as _sg_re
from threading import Thread as _sg_Thread
from sillygirl import Adapter as _SGAdapter, Bucket as _SGBucket, Sender as _SGSender, sender as _sg_sender, container as _sg_container, form
check_auth_status = lambda *args, **kwargs: "账号默认可用"
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
def select_accounts(sender,user_bucket,user_id,*a,**k):
    raw=sg.bucketGet(user_bucket,user_id,[]); raw=_sg_literal(raw,[]) if isinstance(raw,str) else raw; raw=(list(raw.keys()) or list(raw.values())) if isinstance(raw,dict) else raw; return (raw if isinstance(raw,list) else []),(raw if isinstance(raw,list) else [])
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
    's_alq_qlname': form.string().title('设置对接容器').default('').description('面板容器参数；use_daipanel=true 时此处应填写呆呆面板 Host丨AppKey丨AppSecret，不填则回退使用 默认配置 全局配置'),
    's_alq_use_daipanel': form.boolean().title('使用呆呆面板').default(False).description('勾选后使用呆呆面板，不勾选使用青龙面板'),
    's_alq_panel_group': form.string().title('呆呆面板分组').default('').description('仅 use_daipanel=true 时生效，填写后同步写入 group 字段'),
    's_alq_osname': form.string().title('青龙变量名').default('S_ALQ').description('上传到面板的变量名'),
    's_alq_notify': form.string().title('通知渠道').default('').description('检测通知推送渠道'),
})
_CONFIG_FIELD_MAP = {
    ('s_alq', 'qlname'): 's_alq_qlname',
    ('s_alq', 'use_daipanel'): 's_alq_use_daipanel',
    ('s_alq', 'panel_group'): 's_alq_panel_group',
    ('s_alq', 'osname'): 's_alq_osname',
    ('s_alq', 'notify'): 's_alq_notify',
}

import base64
import json
import random
import string
import time
from datetime import datetime

import requests


senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = str(sender.getUserID())

PLUGIN_NAME = "爱路桥"
CONFIG_BUCKET = "s_alq"
LEGACY_CONFIG_BUCKET = "s_alq_config"
USER_BUCKET = "s_alq_user"
TOKEN_BUCKET = "s_alq_token"
AUTH_BUCKET = "s_alq_auth"
BASE_URL = "https://www.ailuqiao.cn/mobile"
DDDDOCR_URL = "https://ocr-xn.vzvv.de"
USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 15; 2210132C Build/AQ3A.240812.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/135.0.7049.37 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel 6 Build/UQ1A.240605.004; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/133.0.6638.41 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1",
]
LEGACY_KEY_MAP = {
    "qlname": ("qlname", "alq_qlname"),
    "osname": ("osname", "alq_osname"),
    "Vipmoney": ("Vipmoney", "alqVipmoney"),
    "coin": ("coin", "alqcoin"),
    "notify": ("notify",),
    "notify_days": ("notify_days",),
    "use_daipanel": ("use_daipanel", "use_dumbpanel"),
    "panel_group": ("panel_group",),
}


def _loads(raw, default=None):
    if default is None:
        default = {}
    try:
        data = json.loads(raw)
        return data if data is not None else default
    except Exception:
        return default


def _today():
    return str(datetime.now().date())


def _mask_account(account):
    return mask_account(str(account or ""))




def _cfg(key, default=""):
    aliases = LEGACY_KEY_MAP.get(key, (key,))
    for bucket in (CONFIG_BUCKET, LEGACY_CONFIG_BUCKET):
        for alias in aliases:
            value = sg.bucketGet(bucket, alias)
            if value not in (None, ""):
                return value
    return default






def _pkcs7_pad(raw_bytes, block_size=16):
    pad_len = block_size - (len(raw_bytes) % block_size)
    return raw_bytes + bytes([pad_len]) * pad_len


def _aes_encrypt_text(text, key="ailuqiaoAb112112", iv="ailuqiaobagebaao"):
    try:
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    except Exception as exc:
        raise RuntimeError("缺少 cryptography 依赖，无法执行短信登录加密") from exc

    plain_bytes = _pkcs7_pad(str(text or "").encode("utf-8"))
    cipher = Cipher(
        algorithms.AES(str(key).encode("utf-8")),
        modes.CBC(str(iv).encode("utf-8")),
    )
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(plain_bytes) + encryptor.finalize()
    return base64.b64encode(encrypted).decode("utf-8")


def _get_user_accounts(user_id=None):
    user_id = str(user_id or userid)
    raw = sg.bucketGet(USER_BUCKET, user_id) or "[]"
    try:
        data = json.loads(raw)
        if isinstance(data, list):
            return [str(item).strip() for item in data if str(item).strip()]
    except Exception:
        pass
    try:
        data = _sg_literal(raw)
        if isinstance(data, (list, tuple, set)):
            return [str(item).strip() for item in data if str(item).strip()]
    except Exception:
        pass
    return []


def _save_user_accounts(accounts, user_id=None):
    user_id = str(user_id or userid)
    cleaned = list(dict.fromkeys(str(item).strip() for item in accounts if str(item).strip()))
    if cleaned:
        sg.bucketSet(USER_BUCKET, user_id, json.dumps(cleaned, ensure_ascii=False))
    else:
        sg.bucketDel(USER_BUCKET, user_id)


def _get_token_info(account):
    return _loads(sg.bucketGet(TOKEN_BUCKET, str(account).strip()), {})


def _save_token_info(account, account_info):
    sg.bucketSet(TOKEN_BUCKET, str(account).strip(), json.dumps(account_info, ensure_ascii=False))


def _get_auth_text(account):
    auth_time = '2099-12-31'
    if not auth_time:
        return "未授权"
    if auth_time < _today():
        return f"已过期:{auth_time}"
    return f"到期:{auth_time}"


def _select_accounts():
    accounts, selected = select_accounts(sender, USER_BUCKET, userid, AUTH_BUCKET, PLUGIN_NAME)
    if accounts is None and selected is None:
        return None, None
    return accounts or [], list(dict.fromkeys(selected or []))


def _get_ql_client():
    osname = str(sg.bucketGet(CONFIG_BUCKET, "osname") or "S_ALQ").strip()
    qlname = str(sg.bucketGet(CONFIG_BUCKET, "qlname") or "").strip()
    use_daipanel = str(sg.bucketGet(CONFIG_BUCKET, "use_daipanel") or "").lower() == "true"
    if use_daipanel:
        return DumbPanelClient(osname, qlname) if qlname else DumbPanelClient(osname)
    return QingLongClient(osname, qlname) if qlname else QingLongClient(osname)


def _get_panel_name():
    return "呆呆面板" if str(sg.bucketGet(CONFIG_BUCKET, "use_daipanel") or "").lower() == "true" else "青龙面板"


def _build_panel_env(account, account_info):
    phone = str(account or "").strip()
    uid = str((account_info or {}).get("uid") or "").strip()
    cookie = str((account_info or {}).get("cookie") or "").strip()
    if not phone or not uid or not cookie:
        return None
    auth_time = '2099-12-31' or "未授权"
    panel_group = str(_cfg("panel_group", "") or "").strip()
    remarks = f"{PLUGIN_NAME}:{phone}|uid:{uid}|到期:{auth_time}"
    return phone, f"{uid}#{cookie}", remarks, panel_group




def sync_ql_env(account, account_info):
    ql = _get_ql_client()
    panel_name = _get_panel_name()
    if not ql.is_configured():
        return False, f"{panel_name}未配置"

    env_data = _build_panel_env(account, account_info)
    if not env_data:
        return False, "账号凭证不完整"

    phone, env_value, remarks, panel_group = env_data
    use_daipanel = str(sg.bucketGet(CONFIG_BUCKET, "use_daipanel") or "").lower() == "true"
    if use_daipanel and panel_group:
        ok = ql.update_env(phone, env_value, remarks, group=panel_group)
    else:
        ok = ql.update_env(phone, env_value, remarks)
    if ok:
        return True, f"{panel_name}同步成功"
    return False, f"{panel_name}变量更新失败"


def delete_ql_env(account):
    return _get_ql_client().delete_env(str(account or "").strip())


class AiLuQiaoClient:
    def __init__(self, phone="", cookie=""):
        self.phone = str(phone or "").strip()
        self.cookie = str(cookie or self._generate_cookie()).strip()
        self.session = requests.Session()

    @staticmethod
    def _generate_cookie():
        session_id = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(32))
        return f"beegosessionID={session_id}"

    @staticmethod
    def _generate_cid():
        chars = string.ascii_lowercase + string.digits
        return "".join(random.choice(chars) for _ in range(32))

    @staticmethod
    def _current_time_text():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _build_sms_headers(self, uid):
        uid = str(uid or self.phone).strip()
        now_text = self._current_time_text()
        return {
            "Content-Types": _aes_encrypt_text(uid),
            "Content-Type2": _aes_encrypt_text(f"{now_text}{uid}"),
        }

    def _request_json(self, method, endpoint, params=None, data=None, extra_headers=None):
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Cookie": self.cookie,
        }
        if data is not None:
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        if extra_headers:
            headers.update(extra_headers)
        response = self.session.request(
            method=method.upper(),
            url=f"{BASE_URL}{endpoint}",
            params=params,
            data=data,
            headers=headers,
            timeout=15,
        )
        response.raise_for_status()
        return response.json()

    def _get_captcha(self):
        try:
            data = self._request_json("GET", "/GenerateCaptcha")
        except Exception as exc:
            return None, None, f"获取验证码图片失败: {exc}"
        captcha_data = data.get("data") or data
        captcha_id = str(captcha_data.get("captcha_id") or "").strip()
        captcha_img = str(captcha_data.get("captcha_img") or "").strip()
        if not captcha_id or not captcha_img:
            return None, None, "验证码数据为空"
        return captcha_id, captcha_img, ""

    @staticmethod
    def _recognize_captcha(captcha_img_base64):
        img_data = captcha_img_base64
        if "," in img_data:
            img_data = img_data.split(",", 1)[1]
        try:
            resp = requests.post(
                f"{DDDDOCR_URL}/classification",
                json={"image": img_data},
                timeout=10,
            )
            resp.raise_for_status()
            result = resp.json()
            code = str(result.get("result") or "").strip()
            if not code:
                return None, "验证码识别结果为空"
            return code, ""
        except Exception as exc:
            return None, f"验证码识别失败: {exc}"

    def send_sms_code(self):
        captcha_id, captcha_img, err = self._get_captcha()
        if err:
            return False, err
        captcha_code, err = self._recognize_captcha(captcha_img)
        if err:
            return False, err
        try:
            uid = self.phone
            data = self._request_json(
                "POST",
                "/service_send_0407new",
                data={
                    "cid": self._generate_cid(),
                    "mobile": self.phone,
                    "uid": uid,
                    "captcha_id": captcha_id,
                    "captcha_code": captcha_code,
                },
                extra_headers=self._build_sms_headers(uid),
            )
        except Exception as exc:
            return False, f"发送验证码失败: {exc}"
        if data.get("status") == 1:
            return True, data
        return False, str(data.get("message") or data.get("msg") or "发送验证码失败")

    def fetch_profile(self, uid):
        try:
            data = self._request_json("GET", "/myinfo", params={"uid": uid})
        except Exception as exc:
            return False, f"获取用户信息失败: {exc}"
        user_data = data.get("data") or {}
        if not user_data:
            return False, str(data.get("message") or data.get("msg") or "用户信息为空")
        return True, {
            "nickname": str(user_data.get("nickname") or self.phone),
            "integral": str(user_data.get("integral") or "0"),
        }

    def fetch_records(self, uid, limit=5):
        try:
            data = self._request_json("GET", "/my_luck", params={"uid": uid, "cid": 1028})
        except Exception as exc:
            return False, f"获取红包记录失败: {exc}"
        records = []
        for item in (data.get("data") or [])[:limit]:
            records.append({
                "prize": str(item.get("draw") or ""),
                "time": str(item.get("create_time") or ""),
            })
        return True, records

    def login_with_code(self, code):
        try:
            data = self._request_json("POST", "/service_yz", data={"mobile": self.phone, "code": str(code).strip()})
        except Exception as exc:
            return False, f"登录失败: {exc}"
        if data.get("status") != 1:
            return False, str(data.get("message") or data.get("msg") or "验证码错误或已过期")
        uid = str(data.get("uid") or "").strip()
        if not uid:
            return False, "登录失败: 未获取到 UID"
        nickname = self.phone
        integral = "0"
        ok, profile = self.fetch_profile(uid)
        if ok:
            nickname = profile.get("nickname") or nickname
            integral = profile.get("integral") or integral
        return True, {
            "phone": self.phone,
            "uid": uid,
            "cookie": self.cookie,
            "nickname": nickname,
            "integral": integral,
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }


def _query_live_state(account, account_info):
    phone = str(account or "").strip()
    uid = str((account_info or {}).get("uid") or "").strip()
    cookie = str((account_info or {}).get("cookie") or "").strip()
    if not uid or not cookie:
        return False, "缺少 UID 或 Cookie"
    client = AiLuQiaoClient(phone=phone, cookie=cookie)
    ok, profile = client.fetch_profile(uid)
    if not ok:
        return False, profile
    ok_records, records = client.fetch_records(uid)
    return True, {
        "uid": uid,
        "nickname": profile.get("nickname") or phone,
        "integral": profile.get("integral") or "0",
        "records": records if ok_records else [],
        "record_error": "" if ok_records else records,
        "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def bind_account():
    sender.reply(
        "=====爱路桥登录=====\n"
        "请输入手机号码\n"
        "------------------\n"
        '回复"q"退出\n'
        "=================="
    )
    phone = sender.input(120000, 1, False)
    if not phone:
        sender.reply("⏰ 操作超时")
        return
    phone = str(phone).strip()
    if phone.lower() == "q":
        sender.reply("✅ 已取消")
        return
    if not phone.isdigit() or len(phone) != 11:
        sender.reply("❌ 手机号格式错误，请输入 11 位数字")
        return

    client = AiLuQiaoClient(phone=phone)
    ok, result = client.send_sms_code()
    if not ok:
        sender.reply(f"❌ {result}")
        return

    sender.reply(
        "=====验证码已发送=====\n"
        f"📱 手机号: {_mask_account(phone)}\n"
        "------------------\n"
        "请输入短信验证码\n"
        '回复"q"退出\n'
        "=================="
    )
    code = sender.input(300000, 1, False)
    if not code:
        sender.reply("⏰ 验证码输入超时")
        return
    if str(code).strip().lower() == "q":
        sender.reply("✅ 已取消")
        return

    ok, account_info = client.login_with_code(code)
    if not ok:
        sender.reply(f"❌ {account_info}")
        return

    accounts = _get_user_accounts()
    if phone not in accounts:
        accounts.append(phone)
        _save_user_accounts(accounts)
    _save_token_info(phone, account_info)

    auth_time = str('2099-12-31' or "").strip()
    sync_text = '未授权，可发送"爱路桥管理"开通'
    if auth_time and auth_time >= _today():
        sync_ok, sync_msg = sync_ql_env(phone, account_info)
        sync_text = f"已授权，{sync_msg}" if sync_ok else f"已授权，但{sync_msg}"

    sender.reply(
        "=====绑定成功=====\n"
        f"📱 账号: {_mask_account(phone)}\n"
        f"👤 昵称: {account_info.get('nickname') or '未设置'}\n"
        f"🆔 UID: {account_info.get('uid') or '未知'}\n"
        f"💰 积分: {account_info.get('integral') or '0'}\n"
        f"📅 授权: {_get_auth_text(phone)}\n"
        f"🔄 状态: {sync_text}\n"
        "=================="
    )


def query_accounts():
    accounts, selected = _select_accounts()
    if accounts is None:
        return
    if not selected:
        sender.reply("❌ 未选择有效账号")
        return

    sender.reply(f"✅ 已选择 {len(selected)} 个账号，正在查询...")
    blocks = []
    for phone in selected:
        token_info = _get_token_info(phone)
        cached_nickname = token_info.get("nickname") or "未设置"
        cached_integral = token_info.get("integral") or "未知"
        ok, result = _query_live_state(phone, token_info)
        if ok:
            token_info.update({
                "phone": phone,
                "uid": result.get("uid") or token_info.get("uid", ""),
                "cookie": token_info.get("cookie", ""),
                "nickname": result.get("nickname") or cached_nickname,
                "integral": result.get("integral") or cached_integral,
                "update_time": result.get("update_time", ""),
            })
            _save_token_info(phone, token_info)
            lines = [
                f"账号: {_mask_account(phone)}",
                f"昵称: {result.get('nickname') or cached_nickname}",
                f"UID: {result.get('uid') or token_info.get('uid') or '未知'}",
                f"积分: {result.get('integral') or cached_integral}",
                f"授权: {_get_auth_text(phone)}",
            ]
            if result.get("records"):
                lines.append("最近红包记录:")
                lines.extend(
                    f"- {item.get('prize') or '未知'} ({item.get('time') or '未知'})"
                    for item in result["records"]
                )
            elif result.get("record_error"):
                lines.append(f"红包记录: {result.get('record_error')}")
        else:
            lines = [
                f"账号: {_mask_account(phone)}",
                f"昵称: {cached_nickname}",
                f"UID: {token_info.get('uid') or '未知'}",
                f"积分: {cached_integral}",
                f"授权: {_get_auth_text(phone)}",
                f"查询说明: {result}",
            ]
        blocks.append("\n".join(lines))

    sender.reply("=====查询结果=====\n" + "\n------------------\n".join(blocks) + "\n==================")






def authorize_accounts(accounts):
    return True


def manage_account():
    accounts = _get_user_accounts()
    if not accounts:
        sender.reply(
            "=====未绑定账号=====\n"
            "❌ 未找到账号\n"
            '💡 发送"爱路桥登录"绑定\n'
            "=================="
        )
        return

    sender.reply(
        "=====爱路桥管理=====\n"
        "[1] 授权账号\n"
        "[2] 删除账号\n"
        "[3] 提交面板\n"
        "------------------\n"
        "回复数字选择\n"
        '回复"q"退出\n'
        "=================="
    )
    choice = sender.input(120000, 1, False)
    if not choice or str(choice).strip().lower() == "q":
        sender.reply("✅ 已退出")
        return

    accounts, selected = _select_accounts()
    if accounts is None:
        return
    if not selected:
        sender.reply("❌ 未选择有效账号")
        return

    if str(choice).strip() == "1":
        authorize_accounts(selected)
        return

    if str(choice).strip() == "2":
        sender.reply(f'⚠️ 确认删除 {len(selected)} 个账号？回复 y 确认，其它任意内容取消')
        confirm = sender.input(120000, 1, False)
        if not confirm or str(confirm).strip().lower() != "y":
            sender.reply("✅ 已取消")
            return
        remain_accounts = accounts[:]
        success_list = []
        fail_list = []
        for account in selected:
            try:
                if account in remain_accounts:
                    remain_accounts.remove(account)
                sg.bucketDel(TOKEN_BUCKET, account)
                True
                try:
                    delete_ql_env(account)
                except Exception:
                    pass
                success_list.append(_mask_account(account))
            except Exception as exc:
                fail_list.append(f"{_mask_account(account)} -> {exc}")
        _save_user_accounts(remain_accounts)
        lines = ["=====删除完成=====", f"✅ 成功: {len(success_list)}个"]
        lines.extend(success_list[:20])
        if fail_list:
            lines.append(f"❌ 失败: {len(fail_list)}个")
            lines.extend(fail_list[:20])
        lines.append("==================")
        sender.reply("\n".join(lines))
        return

    if str(choice).strip() == "3":
        success_list = []
        fail_list = []
        today = _today()
        for account in selected:
            auth_time = str('2099-12-31' or "").strip()
            if not auth_time or auth_time < today:
                fail_list.append(f"{_mask_account(account)} -> 未授权或已过期")
                continue
            info = _get_token_info(account)
            if not info.get("uid") or not info.get("cookie"):
                fail_list.append(f"{_mask_account(account)} -> 缺少账号凭证，请重新登录")
                continue
            sync_ok, sync_msg = sync_ql_env(account, info)
            if sync_ok:
                success_list.append(_mask_account(account))
            else:
                fail_list.append(f"{_mask_account(account)} -> {sync_msg}")
        lines = ["=====提交结果=====", f"✅ 成功: {len(success_list)}个"]
        lines.extend(success_list[:20])
        if fail_list:
            lines.append(f"❌ 失败: {len(fail_list)}个")
            lines.extend(fail_list[:20])
        lines.append("变量格式: uid#cookie")
        lines.append("==================")
        sender.reply("\n".join(lines))
        return

    sender.reply("❌ 无效的选择")




def ks_auth():
    return True


def show_tutorial():
    sender.reply(
        "=====爱路桥教程=====\n"
        "用户指令:\n"
        "1. 爱路桥登录 - 绑定账号\n"
        "2. 爱路桥查询 - 查询积分与近期红包记录\n"
        "3. 爱路桥管理 - 授权、删除、提交面板\n"
        "4. 爱路桥教程 - 查看说明\n"
        "------------------\n"
        "管理员指令:\n"
        "1. 爱路桥授权 - 批量授权\n"
        "2. 爱路桥检测 - 检测过期并清理\n"
        "------------------\n"
        "登录方式:\n"
        "按提示输入手机号并完成短信验证码校验\n"
        "一个手机号绑定一个账号\n"
        "=================="
    )



def _is_target_message(message):
    text = str(message or "")
    return PLUGIN_NAME in text or "alq" in text.lower()


def main():
    msg = str(sender.getMessage() or "")
    if sender.getImtype() == "fake":
        try:
            sg.notifyMasters(check_auth_status())
        except Exception:
            pass
        return

    if ("登录" in msg or "登陆" in msg) and _is_target_message(msg):
        bind_account()
    elif "查询" in msg and _is_target_message(msg):
        query_accounts()
    elif "管理" in msg and _is_target_message(msg):
        manage_account()
    elif "教程" in msg and _is_target_message(msg):
        show_tutorial()
    elif "授权" in msg and _is_target_message(msg):
        ks_auth()
    elif "检测" in msg and _is_target_message(msg):
        if not sender.isAdmin():
            sender.reply("❌ 仅限管理员")
            return
        sender.reply("🔍 正在检测...")
        sender.reply(check_auth_status())
    else:
        sender.setContinue()


if __name__ == "__main__":
    main()
