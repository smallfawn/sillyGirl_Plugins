# [title: 【插件】-星韵]
# [name: chaJianXingYun]
# [language: python]
# [class: 任务]
# [author: huawei]
# [version: v1.0.0]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(星韵|xing yun)(登录|登陆)$|^登(录|陆)(星韵|xingyun)$|^(星韵|xingyun)(查询|管理)$|^(查询|管理)(星韵|xingyun)$|^清理星韵$|^星韵$|^星韵清理$|^星韵上传$]
# [icon: https://i.mji.rip/2025/07/11/2350538ac014afbea48b64409bd5931c.png]
# [description: 星韵优选账号管理插件]
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
    'G_xy_config_ql_config': form.string().title('青龙配置').default('').description('青龙面板地址丨应用ID丨应用密钥'),
    'G_xy_config_ql_envname': form.string().title('环境变量名').default('G_XY_TOKEN').description('青龙环境变量名称'),
})
_CONFIG_FIELD_MAP = {
    ('G_xy_config', 'ql_config'): 'G_xy_config_ql_config',
    ('G_xy_config', 'ql_envname'): 'G_xy_config_ql_envname',
}

from datetime import datetime
import time
import json
import re
import requests
import warnings

warnings.filterwarnings("ignore", message="Unverified HTTPS request")

BASE_URL = "https://gzpengru.weimbo.com/api/index.php?ackey=GZYTAPPLET"

HEADERS = {
    "Host": "gzpengru.weimbo.com",
    "Connection": "keep-alive",
    "content-type": "application/json",
    "User-Agent": "Mozilla/5.0 (Linux; Android 12; SM-G9810 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.5845.163 MicroMessenger/8.0.45.2400(0x28002B3D) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
    "Referer": "https://servicewechat.com/wxc86c9aecdb67f876/9/page-frame.html",
}

loginMessage = """
=====星韵优选登录=====
请输入您的Token
格式：备注#token 或 直接输入token
------------------
回复「q」退出绑定
=================="""

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()


def mask_token(token):
    """将token进行脱敏处理"""
    if not token or len(token) < 10:
        return token
    return f"{token[:6]}****{token[-4:]}"


def get_config():
    """动态获取插件配置"""
    try:
        price_str = sg.bucketGet(bucket="G_xy_config", key="price") or "0.88"
        price = float(price_str) if price_str.replace(".", "", 1).isdigit() else 0.88

        zsm = (
            '2099-12-31'
            or sg.bucketGet(bucket="dd_sign_config", key="zsm")
            or ""
        )

        points_per_month_str = (
            sg.bucketGet(bucket="G_xy_config", key="points_per_month") or "100"
        )
        points_per_month = (
            int(points_per_month_str) if points_per_month_str.isdigit() else 100
        )

        ql_config = sg.bucketGet(bucket="G_xy_config", key="ql_config") or ""
        ql_envname = (
            sg.bucketGet(bucket="G_xy_config", key="ql_envname") or "G_XY_TOKEN"
        )

        return {
            "price": price,
            "zsm": zsm,
            "points_per_month": points_per_month,
            "ql_config": ql_config,
            "ql_envname": ql_envname,
        }
    except Exception as e:
        sender.reply(f"❌ 配置获取失败: {str(e)}")
        return {
            "price": 0.88,
            "zsm": "",
            "points_per_month": 100,
            "ql_config": "",
            "ql_envname": "G_XY_TOKEN",
        }


def get_user_accounts(user_id=None):
    """获取用户账号列表"""
    target_userid = user_id if user_id else userid
    uservalue = sg.bucketGet("G_xy_user", target_userid) or "[]"
    user_accounts = []

    if uservalue:
        try:
            accounts_list = json.loads(uservalue)
            if isinstance(accounts_list, list):
                user_accounts = accounts_list
            else:
                user_accounts = [str(accounts_list)]
        except json.JSONDecodeError:
            try:
                accounts_eval = _sg_literal(uservalue)
                if isinstance(accounts_eval, (list, tuple, set)):
                    user_accounts = list(accounts_eval)
                elif accounts_eval:
                    user_accounts = [str(accounts_eval)]
            except:
                user_accounts = []

    return [str(acc) for acc in user_accounts if acc]


def validate_token(token):
    """验证token是否有效，返回用户信息"""
    try:
        headers = {
            "Host": "gzpengru.weimbo.com",
            "Connection": "keep-alive",
            "3rdsession": token,
            "content-type": "application/json",
            "User-Agent": HEADERS["User-Agent"],
            "Referer": HEADERS["Referer"],
        }
        payload = {"action": "userInfoData"}
        response = requests.post(
            BASE_URL, headers=headers, json=payload, timeout=15, verify=False
        )
        data = response.json()
        if data and data.get("Status"):
            user_data = data.get("Data", {})
            return {
                "name": user_data.get("user", {}).get("name", "未知"),
                "jifen": user_data.get("u_money", {}).get("jifen", 0),
            }
    except Exception as e:
        print(f"验证token失败: {e}")
    return None


ql_token_cache = {}


def get_ql_token(host: str, client_id: str, client_secret: str) -> str:
    """获取青龙Token（带缓存）"""
    if host in ql_token_cache:
        return ql_token_cache[host]

    try:
        url = f"{host}/open/auth/token"
        params = {"client_id": client_id, "client_secret": client_secret}
        resp = requests.get(url, params=params, timeout=10, verify=False)
        data = resp.json()

        if data.get("code") == 200:
            token = data["data"]["token"]
            ql_token_cache[host] = token
            return token
    except Exception as e:
        print(f"[ERROR] 获取青龙Token失败: {e}")
    return ""


def add_or_update_ql_env(
    host: str, ql_token: str, env_name: str, value: str, remarks: str = ""
) -> bool:
    """添加或更新青龙环境变量"""
    if not host or not ql_token:
        return False

    headers = {
        "Authorization": f"Bearer {ql_token}",
        "Content-Type": "application/json",
    }

    try:
        search_url = f"{host}/open/envs"
        resp = requests.get(
            search_url,
            headers=headers,
            params={"searchValue": env_name},
            timeout=10,
            verify=False,
        )
        envs = resp.json().get("data", [])

        account_id = value.split("#")[0] if "#" in value else value[:20]
        existing = None
        for e in envs:
            if e.get("name") == env_name:
                env_remarks = e.get("remarks", "")
                if f"星韵:{account_id}" in env_remarks:
                    existing = e
                    break

        if existing:
            update_url = f"{host}/open/envs"
            env_id = existing.get("id") or existing.get("_id")
            data = {"id": env_id, "name": env_name, "value": value, "remarks": remarks}
            requests.put(
                update_url, headers=headers, json=data, timeout=10, verify=False
            )
        else:
            add_url = f"{host}/open/envs"
            data = [{"name": env_name, "value": value, "remarks": remarks}]
            requests.post(add_url, headers=headers, json=data, timeout=10, verify=False)

        return True
    except Exception as e:
        print(f"[ERROR] 青龙操作失败: {e}")
    return False


def delete_ql_env(host: str, ql_token: str, env_name: str, account_id: str) -> bool:
    """删除青龙环境变量"""
    if not host or not ql_token:
        return False

    headers = {
        "Authorization": f"Bearer {ql_token}",
        "Content-Type": "application/json",
    }

    try:
        search_url = f"{host}/open/envs"
        resp = requests.get(
            search_url,
            headers=headers,
            params={"searchValue": env_name},
            timeout=10,
            verify=False,
        )
        envs = resp.json().get("data", [])

        for env in envs:
            if env.get("name") == env_name:
                env_remarks = env.get("remarks", "")
                if f"星韵:{account_id}" in env_remarks:
                    delete_url = f"{host}/open/envs"
                    env_id = env.get("id") or env.get("_id")
                    requests.delete(
                        delete_url,
                        headers=headers,
                        json=[env_id],
                        timeout=10,
                        verify=False,
                    )
                    return True
    except Exception as e:
        print(f"[ERROR] 删除青龙变量失败: {e}")
    return False


def sync_to_qinglong(account_id):
    """单个账号同步到青龙（授权后自动调用）"""
    config = get_config()
    ql_config_str = config.get("ql_config", "")
    ql_envname = config.get("ql_envname", "G_XY_TOKEN")

    if not ql_config_str:
        print(f"[INFO] 未配置青龙面板，跳过自动上传")
        return {"success": False, "reason": "未配置青龙"}

    sep = "丨" if "丨" in ql_config_str else "|" if "|" in ql_config_str else None
    if not sep:
        return {"success": False, "reason": "青龙配置格式错误"}

    parts = ql_config_str.split(sep)
    if len(parts) != 3:
        return {"success": False, "reason": "青龙配置不完整"}

    host, client_id, client_secret = (
        parts[0].rstrip("/"),
        parts[1].strip(),
        parts[2].strip(),
    )

    ql_token = get_ql_token(host, client_id, client_secret)
    if not ql_token:
        return {"success": False, "reason": "获取青龙Token失败"}

    token = sg.bucketGet("G_xy_token", account_id)
    if not token:
        return {"success": False, "reason": "账号Token不存在"}

    auth_data_str = '2099-12-31'
    expire_date = ""
    acc_userid = userid
    if auth_data_str:
        try:
            auth_data = json.loads(auth_data_str)
            expire_date = auth_data.get("expire_time", "")
            acc_userid = auth_data.get("userid", userid)
        except:
            pass

    env_value = f"{account_id}#{token}"

    remarks = f"星韵:{account_id}|用户:{acc_userid}|到期:{expire_date}"

    if add_or_update_ql_env(host, ql_token, ql_envname, env_value, remarks):
        return {"success": True, "reason": "上传成功"}
    else:
        return {"success": False, "reason": "上传失败"}


def login():
    """用户登录"""
    sender.reply(loginMessage)
    user_input = sender.input(120000, 1, False)

    if user_input is None:
        sender.reply("⏰ 输入超时，已退出")
        return

    user_input = user_input.strip()

    if user_input.lower() == "q":
        sender.reply("✅ 已退出登录")
        return

    parts = user_input.split("#")
    if len(parts) >= 2:
        remark = parts[0]
        token = parts[1]
    else:
        remark = ""
        token = parts[0]

    user_info = validate_token(token)
    if user_info:
        user_name = user_info.get("name", "")
        account_id = (
            remark if remark else user_name if user_name else f"用户_{int(time.time())}"
        )
        save_account_info(account_id, token)
    else:
        sender.reply(f"⚠️ token有误或者token过期了，请重新检查")
        return


def save_account_info(account_id, token):
    """保存账号信息"""
    accounts = get_user_accounts()

    if account_id not in accounts:
        accounts.append(account_id)
        sg.bucketSet("G_xy_user", userid, json.dumps(accounts))

    sg.bucketSet("G_xy_token", account_id, token)
    success_msg = f"""
=====登录成功=====
📱 账号: {account_id}
✅ 状态: 添加成功
------------------
发送"星韵管理"管理账号
发送"星韵查询"查询账号
💡 授权后自动同步青龙"""
    sender.reply(success_msg)


def query_accounts():
    """查询所有账号"""
    today = str(datetime.now().date())
    accounts = get_user_accounts()

    if not accounts:
        sender.reply("❌ 您尚未绑定任何账号，请先使用「星韵登录」绑定")
        return

    account_info_list = []

    for account in accounts:
        account_info = query_accounts_for_item(account, today)
        if account_info:
            account_info_list.append(account_info)

    final_msg = "=====星韵账号信息汇总=====" + "".join(account_info_list) + "\n"
    sender.reply(final_msg)


def query_accounts_for_item(account, today):
    """获取单个账号信息"""
    token = sg.bucketGet("G_xy_token", account)
    if not token:
        return None

    user_info = validate_token(token)
    if user_info:
        jifen = user_info.get("jifen", 0)
        user_name = user_info.get("name", "未知")

        auth_data_str = '2099-12-31'
        if not auth_data_str:
            auth_status = "授权: ❌ 未授权"
        else:
            try:
                auth_data = json.loads(auth_data_str)
                expire_date = auth_data.get("expire_time")
                auth_status = (
                    f"到期时间: {expire_date}"
                    if expire_date and expire_date > today
                    else "授权: ❌ 已过期"
                )
            except:
                auth_status = "授权: ❌ 数据异常"

        return f"""
📱 账号: {account}
👤 昵称: {user_name}
💰 积分: {jifen}
🔐 {auth_status}
=================="""
    else:
        return f"""
📱 账号: {account}
❌ 登录态异常，请重新抓取
=================="""


def safe_int(value, default=0):
    """安全的整数转换"""
    if not value:
        return default
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.isdigit():
        return int(value)
    return default


def get_user_points(target_userid=None):
    return 0


def set_user_points(target_userid, points):
    """设置用户积分"""
    sg.bucketSet("dd_sign_coin", target_userid, str(points["dd_sign_coin"]))
    sg.bucketSet("dd_sign_points", target_userid, str(points["dd_sign_points"]))

    sign_key = f"sign_{target_userid}"
    sg.bucketSet("dd_sign_coin", sign_key, str(points["dd_sign_coin"]))
    return True


def manage():
    """账号管理"""
    accounts = get_user_accounts()
    if not accounts:
        sender.reply("❌ 您尚未绑定任何账号，请先绑定")
        return

    authorized_count = 0
    unauthorized_accounts = []
    for account_id in accounts:
        auth_data = '2099-12-31'
        if auth_data:
            try:
                auth_info = json.loads(auth_data)
                expire_date = auth_info.get("expire_time", "")
                if expire_date >= str(datetime.now().date()):
                    authorized_count += 1
                else:
                    unauthorized_accounts.append(account_id)
            except:
                unauthorized_accounts.append(account_id)
        else:
            unauthorized_accounts.append(account_id)

    account_list = []
    for i, account_id in enumerate(accounts, 1):
        auth_data = '2099-12-31'
        status = "✅"
        status_text = "已授权"
        if auth_data:
            try:
                auth_info = json.loads(auth_data)
                expire_date = auth_info.get("expire_time", "")
                if expire_date < str(datetime.now().date()):
                    status = "❌"
                    status_text = "已过期"
            except:
                status = "❌"
                status_text = "未授权"
        else:
            status = "❌"
            status_text = "未授权"

        account_list.append(f"[{i}] 📱 {account_id} {status}{status_text}")

    if accounts:
        account_list.append("\n[0] 所有账号授权（支付）")
    if unauthorized_accounts:
        account_list.append("[9999] 未授权账号批量授权（支付）")

    account_list_str = "\n".join(account_list)

    user_points = get_user_points()

    sender.reply(f"""
=====星韵账号管理=====
🔢 绑定账号: {len(accounts)}个
✅ 已授权: {authorized_count}个
❌ 未授权: {len(accounts) - authorized_count}个
📊 当前积分: {user_points["total"]}
-------------------------
{account_list_str}
------------------
回复序号选择操作（q退出）
===================""")

    choice = sender.input(60000, 1, False)
    if choice is None:
        sender.reply("⏰ 输入超时，已退出")
        return

    if choice.lower() == "q":
        sender.reply("已退出管理")
        return

    if choice == "0":
        sender.reply("您选择了所有账号授权")
        for account_id in accounts:
            authorize_account(account_id)
        return
    elif choice == "9999":
        sender.reply("您选择了未授权账号批量授权")
        for account_id in unauthorized_accounts:
            authorize_account(account_id)
        return
    elif not choice.isdigit():
        sender.reply("❌ 输入无效，请重新选择")
        manage()
        return

    selected_idx = int(choice) - 1
    if selected_idx < 0 or selected_idx >= len(accounts):
        sender.reply("❌ 序号无效，请重新选择")
        manage()
        return

    selected_account = accounts[selected_idx]
    sender.reply(f"你选择了账号: {selected_account}\n[1] 授权账号\n[2] 删除账号")
    op = sender.input(60000, 1, False)

    if op == "1":
        authorize_account(selected_account)
    elif op == "2":
        delete_account(selected_account)


def authorize_account(account_id):
    return True


def wechat_payment_flow(account_id, months, amount, config):
    return True


def point_payment_flow(account_id, months, required_points, config):
    return True


def parse_payment_result(raw_data):
    return True


def complete_authorization(account_id, months):
    return True


def delete_account(account_id):
    """删除账号"""
    accounts = get_user_accounts()

    sender.reply(f"""
=====删除账号确认=====
确认删除账号 {account_id} 吗？
请回复 [Y] 确认
回复 [N] 取消
==================""")
    user_confirm = sender.input(120000, 1, False)

    if user_confirm is None:
        sender.reply("⏰ 输入超时，已退出")
        return

    if user_confirm.strip().lower() != "y":
        sender.reply("✅ 已取消删除操作")
        return

    try:
        config = get_config()
        ql_config_str = config.get("ql_config", "")
        if ql_config_str:
            sep = (
                "丨" if "丨" in ql_config_str else "|" if "|" in ql_config_str else None
            )
            if sep:
                parts = ql_config_str.split(sep)
                if len(parts) == 3:
                    host = parts[0].rstrip("/")
                    client_id = parts[1].strip()
                    client_secret = parts[2].strip()
                    ql_token = get_ql_token(host, client_id, client_secret)
                    if ql_token:
                        ql_envname = config.get("ql_envname", "G_XY_TOKEN")
                        delete_ql_env(host, ql_token, ql_envname, account_id)

        sg.bucketDel(bucket="G_xy_token", key=account_id)
        True

        if account_id in accounts:
            accounts.remove(account_id)
            if accounts:
                sg.bucketSet(
                    bucket="G_xy_user", key=userid, value=json.dumps(accounts)
                )
            else:
                sg.bucketDel(bucket="G_xy_user", key=userid)

        sender.reply("✅ 账号删除成功（已同步删除青龙变量）")

    except Exception as e:
        sender.reply(f"❌ 删除失败: {str(e)}")


def upload_to_qinglong():
    """上传Token到青龙面板"""
    if not sender.isAdmin():
        sender.reply("❌ 仅管理员可使用上传功能")
        return

    config = get_config()
    ql_config_str = config.get("ql_config", "")
    ql_envname = config.get("ql_envname", "G_XY_TOKEN")

    if not ql_config_str:
        sender.reply("❌ 未配置青龙面板，请在插件参数中配置")
        return

    sep = "丨" if "丨" in ql_config_str else "|" if "|" in ql_config_str else None
    if not sep:
        sender.reply(
            "❌ 青龙配置格式错误，应为：http://ip:5700丨client_id丨client_secret"
        )
        return

    parts = ql_config_str.split(sep)
    if len(parts) != 3:
        sender.reply("❌ 青龙配置格式错误，需要3部分：地址丨ID丨密钥")
        return

    host, client_id, client_secret = (
        parts[0].rstrip("/"),
        parts[1].strip(),
        parts[2].strip(),
    )

    ql_token = get_ql_token(host, client_id, client_secret)
    if not ql_token:
        sender.reply("❌ 获取青龙Token失败，请检查配置")
        return

    sender.reply("正在获取已授权账号...")

    authorized_accounts = []
    auth_keys = [] or []

    for account_id in auth_keys:
        auth_data_str = '2099-12-31'
        if not auth_data_str:
            continue

        try:
            auth_data = json.loads(auth_data_str)
            expire_date = auth_data.get("expire_time")

            if expire_date:
                try:
                    expire_date_obj = datetime.strptime(expire_date, "%Y-%m-%d").date()
                    if datetime.now().date() <= expire_date_obj:
                        authorized_accounts.append(
                            {
                                "account_id": account_id,
                                "expire_date": expire_date,
                                "userid": auth_data.get("userid", ""),
                            }
                        )
                except:
                    pass
        except:
            pass

    if not authorized_accounts:
        sender.reply("❌ 没有已授权的账号可上传")
        return

    sender.reply(f"找到 {len(authorized_accounts)} 个已授权账号，开始上传...")

    success_count = 0
    fail_count = 0

    for acc in authorized_accounts:
        account_id = acc["account_id"]
        expire_date = acc["expire_date"]
        acc_userid = acc["userid"]

        token = sg.bucketGet("G_xy_token", account_id)
        if not token:
            fail_count += 1
            continue

        env_value = f"{account_id}#{token}"

        remarks = f"星韵:{account_id}|用户:{acc_userid}|到期:{expire_date}"

        if add_or_update_ql_env(host, ql_token, ql_envname, env_value, remarks):
            success_count += 1
        else:
            fail_count += 1

    sender.reply(f"""
=====星韵上传完成=====
📊 已授权账号: {len(authorized_accounts)}个
✅ 上传成功: {success_count}个
❌ 上传失败: {fail_count}个
📋 变量名: {ql_envname}
------------------
💡 青龙脚本将自动读取变量执行任务
==================""")


def admin_authorize_account():
    return True
def clear_accounts():
    """清理账号数据"""
    accounts = get_user_accounts()
    if not accounts:
        sender.reply("❌ 您没有绑定任何账号")
        return

    sender.reply(f"""
=====清理星韵数据=====
⚠️ 警告：此操作将清除您的所有星韵账号数据
当前绑定账号数：{len(accounts)}个
------------------
回复 [Y] 确认清理
回复 [N] 取消
==================""")

    confirm = sender.input(60000, 1, False).lower()
    if confirm != "y":
        sender.reply("✅ 已取消清理操作")
        return

    try:
        for account_id in accounts:
            sg.bucketDel(bucket="G_xy_token", key=account_id)
            True

        sg.bucketDel(bucket="G_xy_user", key=userid)

        sender.reply(f"✅ 已清理 {len(accounts)} 个账号数据")
    except Exception as e:
        sender.reply(f"❌ 清理失败: {str(e)}")


try:
    usermessage = sender.getMessage()
except AttributeError:
    usermessage = ""

if re.search(r"星韵登录|星韵登陆", usermessage):
    login()
elif re.search(r"星韵管理", usermessage):
    manage()
elif re.search(r"星韵查询", usermessage):
    query_accounts()
elif re.search(r"星韵上传", usermessage):
    upload_to_qinglong()
elif re.search(r"星韵教程", usermessage):
    sender.reply(
        "=====星韵优选使用教程=====\n"
        "1. 「星韵登录」绑定账号\n"
        "   格式：备注#token 或 直接输入token\n"
        "2. 「星韵管理」进行账号授权\n"
        "   授权成功后自动同步到青龙面板\n"
        "3. 「星韵查询」查看账号状态\n"
        "4. 「星韵上传」手动上传到青龙(管理员)\n"
        "===================="
    )
elif re.search(r"星韵授权$", usermessage) and sender.isAdmin():
    admin_authorize_account()
elif re.search(r"清理星韵|星韵清理", usermessage):
    clear_accounts()
else:
    sender.setContinue()
