# [title: 雨云签到]
# [name: yuYunQianDao]
# [language: python]
# [class: 任务]
# [author: rujingxianghai]
# [version: v1.1]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(雨云|yy)(登录|登陆)$|^登(录|陆)(雨云|yy)$|^(雨云|yy)(查询|管理|检测|教程)$|^(查询|管理)(雨云|yy)$]
# [cron: 45 6 * * *]
# [icon: https://api.iconify.design/lucide:apple.svg]
# [description: 。]
# [depe: ["requests"]]


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
    's_yy_qlname': form.string().title('设置对接容器').default('').description('面板容器参数，不填则使用默认配置'),
    's_yy_use_dumbpanel': form.boolean().title('使用呆呆面板').default(False).description('勾选使用呆呆面板，不勾选使用青龙面板'),
    's_yy_panel_group': form.string().title('呆呆面板分组').default('').description('填写后新增/更新变量时同步写入group字段，留空则不处理'),
    's_yy_osname': form.string().title('青龙变量名').default('').description('青龙或呆呆面板内雨云签到变量名'),
    's_yy_proxy_api': form.string().title('代理API').default('').description('获取代理IP的API链接，返回格式 host:port'),
    's_yy_notify': form.string().title('通知渠道').default('').description('检测通知推送渠道'),
})
_CONFIG_FIELD_MAP = {
    ('s_yy', 'qlname'): 's_yy_qlname',
    ('s_yy', 'use_dumbpanel'): 's_yy_use_dumbpanel',
    ('s_yy', 'panel_group'): 's_yy_panel_group',
    ('s_yy', 'osname'): 's_yy_osname',
    ('s_yy', 'proxy_api'): 's_yy_proxy_api',
    ('s_yy', 'notify'): 's_yy_notify',
}

import ast
import base64
import json
import time

import requests

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()
uservalue = sg.bucketGet(bucket='s_yy_user', key=userid)

PLUGIN_CONFIG = {
    'bucket': 's_yy',
    'coin_key': 'dd_sign_points',
    'name': '雨云',
}
PLUGIN_NAME = PLUGIN_CONFIG['name']
CONFIG_BUCKET = PLUGIN_CONFIG['bucket']
USER_BUCKET = 's_yy_user'
TOKEN_BUCKET = 's_yy_token'
AUTH_BUCKET = 's_yy_auth'
CURRENT_VERSION = "1.1.0"
PAY_TYPE_NAMES = {'alipay': '支付宝', 'wxpay': '微信支付', 'qqpay': 'QQ钱包'}


def get_user_content():
    """获取用户配置内容。"""
    osname = sg.bucketGet(CONFIG_BUCKET, 'osname') or 'S_YYQD'
    qlname = sg.bucketGet(CONFIG_BUCKET, 'qlname') or ''
    vip_money = float(sg.bucketGet(CONFIG_BUCKET, 'Vipmoney') or '1')
    coin_raw = sg.bucketGet(CONFIG_BUCKET, 'coin') or '0'
    return osname, qlname, '雨云管理', '雨云查询', '雨云登录', vip_money, int(coin_raw)


def parse_batch_accounts(input_text):
    """解析批量登录输入，格式为 账号#密码。"""
    accounts = []
    for line in input_text.strip().splitlines():
        line = line.strip()
        if not line or '#' not in line:
            continue
        username, password = line.split('#', 1)
        username = username.strip()
        password = password.strip()
        if username and password:
            accounts.append({'username': username, 'password': password})
    return accounts


def load_user_accounts(user_id=None):
    """读取用户绑定账号列表。"""
    target_user = str(user_id or userid)
    raw_value = sg.bucketGet(USER_BUCKET, target_user)
    if not raw_value:
        return []

    try:
        data = ast.literal_eval(raw_value)
        if isinstance(data, list):
            return [str(item).strip() for item in data if str(item).strip()]
    except Exception:
        pass
    return []


def save_user_accounts(accounts, user_id=None):
    """保存用户绑定账号列表。"""
    target_user = str(user_id or userid)
    cleaned = []
    for account in accounts:
        account = str(account).strip()
        if account and account not in cleaned:
            cleaned.append(account)

    if cleaned:
        sg.bucketSet(USER_BUCKET, target_user, str(cleaned))
    else:
        sg.bucketDel(USER_BUCKET, target_user)


def load_account_info(username):
    """读取单个账号信息。"""
    raw_value = sg.bucketGet(TOKEN_BUCKET, username)
    if not raw_value:
        return None

    try:
        data = json.loads(raw_value)
        return data if isinstance(data, dict) else None
    except Exception:
        return None


def build_env_value(account_info):
    """构造面板环境变量值。"""
    username = str(account_info.get('username', '')).strip()
    password = str(account_info.get('password', '')).strip()
    if not username or not password:
        return ''
    return f"{username}#{password}"


def is_valid_auth(auth_time):
    return True


def render_batch_result(title, success_list=None, fail_list=None, warn_list=None, extra_lines=None):
    """生成批量操作统一回执。"""
    success_list = success_list or []
    fail_list = fail_list or []
    warn_list = warn_list or []
    extra_lines = extra_lines or []

    result = f"====={title}=====\n"
    result += f"✅ 成功: {len(success_list)}个\n"
    if success_list:
        result += "\n".join(success_list) + "\n"
    if warn_list:
        result += f"⚠️ 注意: {len(warn_list)}项\n"
        result += "\n".join(warn_list) + "\n"
    if fail_list:
        result += f"❌ 失败: {len(fail_list)}个\n"
        result += "\n".join(fail_list) + "\n"
    if extra_lines:
        result += "\n".join(extra_lines) + "\n"
    result += "=================="
    return result


def _get_ql_client():
    """获取面板客户端，根据开关决定使用青龙或呆呆面板。"""
    osname = sg.bucketGet(CONFIG_BUCKET, 'osname') or 'S_YYQD'
    qlname = sg.bucketGet(CONFIG_BUCKET, 'qlname') or ''
    use_dp = str(sg.bucketGet(CONFIG_BUCKET, 'use_dumbpanel') or '').lower() == 'true'

    if use_dp:
        return DumbPanelClient(osname, qlname) if qlname else DumbPanelClient(osname)
    return QingLongClient(osname, qlname) if qlname else QingLongClient(osname)


def update_ql_env(username, account_info):
    """更新面板环境变量（青龙 / 呆呆面板通用）。"""
    env_value = build_env_value(account_info)
    if not env_value:
        return False

    auth_time = '2099-12-31' or '未授权'
    panel_group = (sg.bucketGet(CONFIG_BUCKET, 'panel_group') or '').strip()
    ql = _get_ql_client()
    return ql.update_env(
        username,
        env_value,
        f"雨云:{username}|到期:{auth_time}",
        group=panel_group,
    )


def delete_ql_env(username):
    """删除面板环境变量（青龙 / 呆呆面板通用）。"""
    return _get_ql_client().delete_env(username)


class RainyunAPI:
    """雨云 API 客户端。"""

    BASE_URL = "https://api.v2.rainyun.com"
    TEST_URL = "http://www.baidu.com"

    def __init__(self):
        self.session = requests.Session()
        self.csrf_token = None
        self.proxy_api_url = sg.bucketGet(CONFIG_BUCKET, 'proxy_api') or ''
        self._set_proxy()

    def test_proxy(self, proxy_url):
        """测试代理是否可用。"""
        try:
            proxies = {
                'http': f'http://{proxy_url}',
                'https': f'http://{proxy_url}',
            }
            response = requests.get(self.TEST_URL, proxies=proxies, timeout=10)
            return response.status_code == 200
        except Exception:
            return False

    def _set_proxy(self):
        """从代理 API 获取代理并设置到会话。"""
        if not self.proxy_api_url:
            return

        try:
            response = requests.get(self.proxy_api_url, timeout=10)
            response.raise_for_status()
            proxy_address = response.text.strip()
            if not proxy_address:
                return

            if self.test_proxy(proxy_address):
                self.session.proxies = {
                    'http': f'http://{proxy_address}',
                    'https': f'http://{proxy_address}',
                }
        except Exception:
            pass

    def login(self, username, password):
        """登录雨云账号。"""
        try:
            response = self.session.post(
                f"{self.BASE_URL}/user/login",
                headers={"Content-Type": "application/json"},
                data=json.dumps({"field": username, "password": password}),
                timeout=10,
            )
            result = response.json()
            if result.get('code') == 200:
                self.csrf_token = response.cookies.get_dict().get('X-CSRF-Token')
                return True, result.get('message') or result.get('msg') or '登录成功'
            return False, result.get('message') or result.get('msg') or '登录失败'
        except Exception as exc:
            return False, f"登录异常: {str(exc)}"

    def get_user_info(self):
        """获取用户信息。"""
        if not self.csrf_token:
            return False, "未获取到 csrf_token"

        try:
            response = self.session.get(
                f"{self.BASE_URL}/user/?no_cache=false",
                headers={
                    "Content-Type": "application/json",
                    "x-csrf-token": self.csrf_token,
                },
                timeout=10,
            )
            result = response.json()
            if result.get('code') == 200:
                return True, result.get('data', {})
            return False, result.get('message') or result.get('msg') or '获取失败'
        except Exception as exc:
            return False, str(exc)


def yy_login(username, password):
    """雨云登录兼容函数。"""
    api = RainyunAPI()
    success, message = api.login(username, password)
    if success:
        return True, api, message
    return False, None, message


def yy_userinfo(username, api, csrf_token=None):
    """雨云用户信息兼容函数。"""
    if isinstance(api, RainyunAPI):
        return api.get_user_info()
    return False, "API对象无效"


def bind_account():
    """绑定账号。"""
    sender.reply(
        "=====雨云登录=====\n"
        "请输入账号信息\n"
        "格式: 账号#密码\n"
        "------------------\n"
        "支持批量登录(换行分隔)\n"
        "回复\"q\"退出\n"
        "=================="
    )
    input_text = sender.input(120000, 1, False)
    if not input_text:
        sender.reply("⏰ 操作超时")
        return
    if input_text.lower() == 'q':
        sender.reply("✅ 已取消")
        return

    account_list = parse_batch_accounts(input_text)
    if not account_list:
        sender.reply("❌ 未检测到有效账号\n格式: 账号#密码")
        return

    sender.reply(f"🔄 正在登录 {len(account_list)} 个账号...")

    bound_accounts = load_user_accounts()
    success_list = []
    fail_list = []
    warn_list = []
    success_accounts = []

    for account in account_list:
        username = account['username']
        password = account['password']
        success, _, message = yy_login(username, password)
        if not success:
            fail_list.append(f"{mask_account(username)} {message}")
            continue

        if username not in bound_accounts:
            bound_accounts.append(username)

        account_info = {
            'username': username,
            'password': password,
            'version': CURRENT_VERSION,
        }
        sg.bucketSet(TOKEN_BUCKET, username, json.dumps(account_info, ensure_ascii=False))
        success_accounts.append({'username': username, 'info': account_info})
        success_list.append(f"{mask_account(username)} 登录成功")

    save_user_accounts(bound_accounts)

    panel_client = _get_ql_client()
    panel_configured = panel_client.is_configured()
    already_authed_count = 0
    need_auth = []

    for account in success_accounts:
        username = account['username']
        auth_time = '2099-12-31'
        if is_valid_auth(auth_time):
            already_authed_count += 1
            if panel_configured and not update_ql_env(username, account['info']):
                warn_list.append(f"{mask_account(username)} 已授权，但面板同步失败")
        else:
            need_auth.append(username)

    extra_lines = []
    if already_authed_count:
        if panel_configured:
            extra_lines.append(f"🔄 已授权并尝试同步: {already_authed_count}个")
        else:
            extra_lines.append(f"🔄 已授权账号: {already_authed_count}个（当前未配置面板，同步已跳过）")
    if need_auth:
        extra_lines.append(f"📋 待授权: {len(need_auth)}个")

    sender.reply(render_batch_result("登录完成", success_list, fail_list, warn_list, extra_lines))

    if need_auth:
        sender.reply(f"📋 检测到 {len(need_auth)} 个账号尚未授权，进入授权流程")
        authorize_multiple_accounts(need_auth)


def query_accounts():
    """查询账号信息。"""
    _, selected = select_accounts(sender, USER_BUCKET, str(userid), AUTH_BUCKET, PLUGIN_NAME)
    if not selected:
        return

    sender.reply(f"✅ 已选择 {len(selected)} 个账号，正在查询...")
    for index, username in enumerate(selected, 1):
        account_info = load_account_info(username)
        auth_time = '2099-12-31'
        auth_status = '已授权' if is_valid_auth(auth_time) else '未授权'
        user_info_text = ""

        if not account_info:
            user_info_text = "\n⚠️ 本地账号信息缺失"
        else:
            login_success, api, message = yy_login(username, account_info.get('password', ''))
            if login_success:
                info_success, user_data = yy_userinfo(username, api)
                if info_success:
                    points = int(user_data.get('Points', 0) or 0)
                    cash_amount = round(points / 2000, 2)
                    user_info_text = (
                        f"\n💰 积分: {points} (≈{cash_amount}元现金)"
                        f"\n📊 换算: 2000积分 = 1元"
                    )
                else:
                    user_info_text = f"\n⚠️ 获取用户信息失败: {user_data}"
            else:
                user_info_text = f"\n⚠️ 登录失败: {message}"

        sender.reply(
            f"=====账号信息[{index}/{len(selected)}]=====\n"
            f"📱 账号: {mask_account(username)}\n"
            f"🏷 状态: {auth_status}\n"
            f"📅 到期: {auth_time or '未授权'}{user_info_text}\n"
            f"=================="
        )

    sender.reply("✅ 查询完成")


def manage_account():
    """管理账号。"""
    if not load_user_accounts():
        sender.reply("=====未绑定账号=====\n❌ 未找到账号\n==================")
        return

    sender.reply(
        "=====账号管理=====\n"
        "[1] 授权账号\n"
        "[2] 删除账号\n"
        "[3] 提交青龙\n"
        "------------------\n"
        "回复数字选择\n"
        "回复\"q\"退出\n"
        "=================="
    )
    choice = sender.input(120000, 1, False)
    if not choice or choice.lower() == 'q':
        sender.reply("✅ 已退出")
        return

    _, selected = select_accounts(sender, USER_BUCKET, str(userid), AUTH_BUCKET, PLUGIN_NAME)
    if not selected:
        return

    sender.reply(f"✅ 已选择 {len(selected)} 个账号")

    if choice == '1':
        authorize_multiple_accounts(selected)
        return

    if choice == '2':
        sender.reply(
            "=====确认删除=====\n"
            "⚠️ 此操作不可恢复\n"
            "回复 y 确认删除\n"
            "=================="
        )
        confirm = sender.input(120000, 1, False)
        if not confirm or confirm.lower() != 'y':
            sender.reply("✅ 已取消")
            return

        current_accounts = load_user_accounts()
        success_list = []
        fail_list = []
        for username in selected:
            try:
                if username in current_accounts:
                    current_accounts.remove(username)
                sg.bucketDel(TOKEN_BUCKET, username)
                True
                delete_ql_env(username)
                success_list.append(mask_account(username))
            except Exception as exc:
                fail_list.append(f"{mask_account(username)} {str(exc)}")

        save_user_accounts(current_accounts)
        sender.reply(render_batch_result("删除完成", success_list, fail_list))
        return

    if choice == '3':
        panel_client = _get_ql_client()
        success_list = []
        fail_list = []
        extra_lines = []

        if not panel_client.is_configured():
            extra_lines.append("⚠️ 未配置面板容器，请先在插件配置或 默认配置 中补全配置")

        for username in selected:
            account_info = load_account_info(username)
            auth_time = '2099-12-31'

            if not account_info:
                fail_list.append(f"{mask_account(username)} 本地账号信息缺失")
                continue
            if not is_valid_auth(auth_time):
                fail_list.append(f"{mask_account(username)} 未授权或已过期")
                continue
            if update_ql_env(username, account_info):
                success_list.append(f"{mask_account(username)} → {auth_time}")
            else:
                fail_list.append(f"{mask_account(username)} 面板同步失败")

        sender.reply(render_batch_result("提交结果", success_list, fail_list, extra_lines=extra_lines))
        return

    sender.reply("❌ 无效选择")


def authorize_multiple_accounts(usernames):
    return True


def authorize_account(username, account_info):
    return True



def generate_iframe_url(url):
    """将 URL 转为 iframe 页面链接。"""
    try:
        encoded = base64.b64encode(url.encode('utf-8')).decode('utf-8')
        return f"https://metwhale.github.io?u={encoded}"
    except Exception:
        return url


def process_qrcode_payment(project, months, money):
    return True


def process_mapay_payment(project, months, money, pay_type='alipay'):
    return True


def pay_order(project, months, money):
    return True



def ks_auth():
    return True


def show_tutorial():
    """显示使用教程。"""
    tutorial = """
=====雨云签到教程=====
📱 用户指令:
• 雨云登录 - 绑定雨云账号
• 雨云查询 - 查询账号状态和积分信息
• 雨云管理 - 授权 / 删除 / 提交青龙
• 雨云教程 - 查看本教程
------------------
🔧 管理员指令:
• 雨云授权 - 管理员按天数授权
• 雨云检测 - 检测过期账号并清理
------------------
💡 登录说明:
• 格式: 账号#密码
• 支持批量登录，多账号换行分隔
• 插件负责管理账号并同步环境变量，实际签到脚本请在面板中运行
------------------
🧩 面板支持:
• 默认支持 QingLong
• 勾选 s_yy.use_dumbpanel 后可切换为 DumbPanel
• 可选配置 s_yy.panel_group 作为 DumbPanel 分组
------------------
💳 支付说明:
• 扫在线处理 / 在线处理 / 支付方式统一读取 默认配置 配置
• 插件内不再单独配置二维码和在线处理参数
------------------
🌐 代理说明:
• 可配置 s_yy.proxy_api 获取代理 IP
• API 返回格式需为 host:port
==================
"""
    sender.reply(tutorial.strip())


def main():
    """主入口。"""
    msg = sender.getMessage()
    lower_msg = msg.lower()

    if '登录' in msg or '登陆' in msg:
        bind_account()
    elif '查询' in msg and ('雨云' in msg or 'yy' in lower_msg):
        query_accounts()
    elif '管理' in msg and ('雨云' in msg or 'yy' in lower_msg):
        manage_account()
    elif '教程' in msg and ('雨云' in msg or 'yy' in lower_msg):
        show_tutorial()
    elif '雨云授权' in msg:
        ks_auth()
    elif '雨云检测' in msg:
        if not sender.isAdmin():
            sender.reply("❌ 仅限管理员")
            return
        sender.reply("🔍 正在检测雨云账号...")
        sender.reply(check_auth_status())
    elif sender.getImtype() == 'fake':
        try:
            sg.notifyMasters(check_auth_status())
        except Exception:
            pass
    else:
        sender.setContinue()


if __name__ == "__main__":
    main()
