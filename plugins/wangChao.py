# [title: 望潮]
# [name: wangChao]
# [language: python]
# [class: 任务]
# [author: sky2022]
# [version: v1.4.2]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(望潮管理|管理望潮|望潮查询|查询望潮|望潮登录|望潮登陆|登录望潮|登陆望潮|望潮教程|望潮删除|删除望潮|望潮更新青龙|望潮同步|同步望潮)$]
# [cron: 56 8,15 * * *]
# [icon: https://pp.myapp.com/ma_icon/0/icon_42259219_1711261436/256]
# [description: 望潮插件；1.1更新了WXPUSH通知，现在可以把每个人登录的账户收益通知全部单独发给用户；1.6更新：统一面板配置为面板类型+对接面板配置，并新增呆呆面板分组配置]
# [depe: ["cryptography","requests","urllib3"]]

import asyncio as _sg_asyncio
import os as _sg_os
import time as _sg_time
import types as _sg_types
import json as _sg_json
from threading import Thread as _sg_Thread
from sillygirl import Adapter as _SGAdapter, Bucket as _SGBucket, Sender as _SGSender, sender as _sg_sender, plugin
try: import ast as _sg_ast
except Exception: _sg_ast=None

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
    "enable": plugin.Form.boolean().title("是否启用").default(True),
    'dd_wcconfig_PanelType': plugin.Form.string().title('面板类型').default('').description('对接面板：qinglong=青龙，daidai=呆呆（DaiDaiPanel），不填默认为青龙'),
    'dd_wcconfig_Qinglong': plugin.Form.string().title('设置对接容器').default('').description('青龙用丨分割3项；呆呆为 Open API 的 host、app_key、app_secret'),
    'dd_wcconfig_osname': plugin.Form.string().title('变量名').default('').description('面板内望潮账号使用的变量名（青龙/呆呆通用）'),
    'dd_wcconfig_zjsl': plugin.Form.string().title('中奖记录条数').default('').description('查询时显示的中奖记录条数，默认30条'),
    'dd_wcconfig_cxproxy': plugin.Form.string().title('查询代理API').default('').description('望潮查询使用的代理API地址，每查询一个账号自动切换IP'),
})
_CONFIG_FIELD_MAP = {
    ('dd_wcconfig', 'PanelType'): 'dd_wcconfig_PanelType',
    ('dd_wcconfig', 'Qinglong'): 'dd_wcconfig_Qinglong',
    ('dd_wcconfig', 'osname'): 'dd_wcconfig_osname',
    ('dd_wcconfig', 'zjsl'): 'dd_wcconfig_zjsl',
    ('dd_wcconfig', 'cxproxy'): 'dd_wcconfig_cxproxy',
}

import json
from datetime import datetime
import hashlib
import random
import time
import re
from urllib3.exceptions import InsecureRequestWarning
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
import base64
import urllib.parse
import requests
import urllib3
import threading

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
_DEFAULT_SIGNIN_Q = "Kmqh2bf7dyAQl2I770dCKHUVSnXhOYSzhc6XfCKHGY0="
_DEFAULT_SIGNIN_LOTTERY_ACTIVITY_ID = 1889
_DEFAULT_SIGNIN_LOTTERY_Q = "23dK9z2aWFgpe9ZqxA4ARLby61Zf4Yqt4mcdKX9NlBo="
_PUBLIC_KEY_PEM = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQD6XO7e9YeAOs+cFqwa7ETJ+WXizPqQeXv68i5vqw9pFREsrqiBTRcg7wB0RIp3rJkDpaeVJLsZqYm5TW7FWx/iOiXFc+zCPvaKZric2dXCw27EvlH5rq+zwIPDAJHGAfnn1nmQH7wR3PCatEIb8pz5GFlTHMlluw4ZYmnOwg+thwIDAQAB"
_USER_AGENT = "6.0.2;00000000-699e-0680-0000-0000090ca05c;Xiaomi Redmi Note 8 Pro;Android;11;xiaomi;6.10.0"
SIGNIN_PREFIXES = ['签到红包:', '红包:', '望潮签到打卡红包:', '签到打卡红包:']

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()
dd_wc_osname = sg.bucketGet('dd_wcconfig', 'osname') or 'wangchao'
dd_wc_qlname = sg.bucketGet('dd_wcconfig', 'Qinglong')
dd_wc_panel_type = (sg.bucketGet('dd_wcconfig', 'PanelType') or 'qinglong').strip().lower()
zjsl = int(sg.bucketGet('dd_wcconfig', 'zjsl') or '30')
today_date = datetime.now().date()
today_time = str(today_date)
SIGNIN_Q = sg.bucketGet('dd_wcconfig', 'signin_q') or _DEFAULT_SIGNIN_Q
try:
    SIGNIN_LOTTERY_ACTIVITY_ID = int(sg.bucketGet('dd_wcconfig', 'signin_lottery_activity_id') or _DEFAULT_SIGNIN_LOTTERY_ACTIVITY_ID)
except ValueError:
    SIGNIN_LOTTERY_ACTIVITY_ID = _DEFAULT_SIGNIN_LOTTERY_ACTIVITY_ID
SIGNIN_LOTTERY_Q = sg.bucketGet('dd_wcconfig', 'signin_lottery_q') or _DEFAULT_SIGNIN_LOTTERY_Q

def QLtoken(QLurl, ClientID, ClientSecret):
    url = f'{QLurl}/open/auth/token?client_id={ClientID}&client_secret={ClientSecret}'

    try:
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            raise Exception(f"API请求失败，状态码: {response.status_code}")

        result = response.json()

        if result.get('code') == 200 and result.get('data', {}).get('token'):
            return result['data']['token']
        else:
            error_msg = result.get('message', '未知错误')
            raise Exception(f"认证失败: {error_msg}")

    except requests.exceptions.Timeout:
        raise Exception("连接超时，请检查网络和青龙面板状态")
    except requests.exceptions.ConnectionError:
        raise Exception("连接失败，请检查青龙地址和面板状态")
    except Exception as e:
        raise Exception(f"系统错误: {str(e)}")

def _get_panel_config():
    if not dd_wc_qlname:
        raise Exception("未配置对接容器信息，请先在插件配置中设置")
    parts = [p.strip() for p in dd_wc_qlname.split('丨') if p.strip()]
    if len(parts) != 3:
        raise Exception("对接容器格式错误：青龙为 URL丨ClientID丨ClientSecret，呆呆为 URL丨app_key丨app_secret")
    if dd_wc_panel_type == "daidai":
        return "daidai", parts[0].rstrip("/"), parts[1], parts[2]
    return "qinglong", parts[0], parts[1], parts[2]

def _get_ql_config():
    panel_type, p1, p2, p3 = _get_panel_config()
    if panel_type != "qinglong":
        raise Exception("当前为呆呆面板，此操作仅支持青龙")
    return p1, p2, p3

def _daidai_get_token(host: str, app_key: str, app_secret: str) -> str:
    url = f"{host}/api/open-api/token"
    payload = {"app_key": app_key, "app_secret": app_secret}
    resp = requests.post(url, json=payload, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    token = (data.get("data") or {}).get("access_token")
    if not token:
        raise Exception(data.get("message", "未获取到 access_token"))
    return token

def _daidai_request(host: str, app_key: str, app_secret: str, method: str, path: str, json_data=None, token=None):
    if token is None:
        token = _daidai_get_token(host, app_key, app_secret)
    url = f"{host}{path}" if path.startswith("/") else f"{host}/{path}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    fn = getattr(requests, method.lower())
    kwargs = {"headers": headers, "timeout": 10}
    if json_data is not None:
        kwargs["json"] = json_data
    resp = fn(url, **kwargs)
    if resp.status_code == 401:
        token = _daidai_get_token(host, app_key, app_secret)
        headers["Authorization"] = f"Bearer {token}"
        resp = fn(url, **kwargs)
    return resp

def _daidai_find_env(host: str, app_key: str, app_secret: str, name: str, keyword: str = ""):
    path = f"/api/envs?keyword={name}&page_size=100"
    resp = _daidai_request(host, app_key, app_secret, "get", path)
    if resp.status_code != 200:
        raise Exception(f"呆呆面板请求失败，状态码: {resp.status_code}")
    for env in (resp.json().get("data") or []):
        if env.get("name") == name and (not keyword or (keyword in (env.get("remarks") or ""))):
            return env.get("id")
    return None

def _daidai_add_env(host: str, app_key: str, app_secret: str, name: str, value: str, remarks: str = "") -> bool:
    path = "/api/envs"
    data = {"name": name, "value": value, "remarks": remarks}
    resp = _daidai_request(host, app_key, app_secret, "post", path, json_data=data)
    return 200 <= resp.status_code < 300

def _daidai_update_env(host: str, app_key: str, app_secret: str, env_id, name: str, value: str, remarks: str = "") -> bool:
    path = f"/api/envs/{env_id}"
    data = {"name": name, "value": value, "remarks": remarks}
    resp = _daidai_request(host, app_key, app_secret, "put", path, json_data=data)
    return 200 <= resp.status_code < 300

def _daidai_delete_env(host: str, app_key: str, app_secret: str, env_id) -> bool:
    path = f"/api/envs/{env_id}"
    resp = _daidai_request(host, app_key, app_secret, "delete", path)
    return 200 <= resp.status_code < 300

def _daidai_list_envs(host: str, app_key: str, app_secret: str, keyword: str):
    path = f"/api/envs?keyword={keyword}&page_size=100"
    resp = _daidai_request(host, app_key, app_secret, "get", path)
    if resp.status_code != 200:
        raise Exception(f"呆呆面板请求失败，状态码: {resp.status_code}")
    raw = resp.json().get("data") or []
    return [{"id": e.get("id"), "name": e.get("name", ""), "value": e.get("value", ""), "remarks": e.get("remarks") or ""} for e in raw]

def _ql_request(method, url_suffix, data, max_retries=3):
    for attempt in range(max_retries):
        try:
            QLurl, ClientID, ClientSecret = _get_ql_config()
            qltoken = QLtoken(QLurl, ClientID, ClientSecret)
            headers = {"Authorization": f"Bearer {qltoken}", "accept": "application/json", "Content-Type": "application/json"}
            func = getattr(requests, method.lower())
            response = func(f"{QLurl}{url_suffix}", headers=headers, json=data, timeout=10, verify=False)
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 200:
                    return result
                elif attempt == 2:
                    raise Exception(f"操作失败: {result.get('message', '未知错误')}")
            elif attempt == 2:
                raise Exception(f"请求失败，状态码: {response.status_code}")
            time.sleep(1)
        except requests.exceptions.Timeout:
            if attempt == 2:
                raise Exception("连接超时，请检查网络和青龙面板状态")
            time.sleep(1)
        except Exception as e:
            if attempt == 2:
                raise Exception(f"青龙操作失败: {str(e)}")
            time.sleep(1)

def QLzt(osname, value, account, name, auth_time=None, user_id=None):
    auth_time = auth_time or today_time
    owner_uid = user_id or userid
    remarks = f'望潮:{name}丨账户:{account}丨用户:{owner_uid}丨望潮管理'
    result = _ql_request('post', '/open/envs', [{"value": value, "name": osname, "remarks": remarks}])
    if result and "value must be unique" not in str(result):
        return result.get('data', [{}])[0].get('id')

def QLupdate(osname, value, account, qlid, name, auth_time=None, user_id=None):
    auth_time = auth_time or today_time
    owner_uid = user_id or userid
    remarks = f'望潮:{name}丨账户:{account}丨用户:{owner_uid}丨望潮管理'
    _ql_request('put', '/open/envs', {"value": value, "name": osname, "remarks": remarks, "id": qlid})

def Addenvs(osname, value, account, name, auth_time=None, user_id=None):
    auth_time = auth_time or today_time
    owner_uid = user_id or userid
    remarks = f'望潮:{name}丨账户:{account}丨用户:{owner_uid}丨望潮管理'

    panel_type, p1, p2, p3 = _get_panel_config()
    if panel_type == "daidai":
        host, app_key, app_secret = p1, p2, p3
        env_id = _daidai_find_env(host, app_key, app_secret, osname, keyword=account)
        if env_id:
            ok = _daidai_update_env(host, app_key, app_secret, env_id, osname, value, remarks)
        else:
            ok = _daidai_add_env(host, app_key, app_secret, osname, value, remarks)
        if not ok:
            raise Exception("呆呆面板添加/更新环境变量失败")
        return True

    QLurl, ClientID, ClientSecret = p1, p2, p3
    qltoken = QLtoken(QLurl, ClientID, ClientSecret)
    resp = requests.get(
        f"{QLurl}/open/envs",
        headers={"Authorization": f"Bearer {qltoken}", "accept": "application/json"},
        timeout=10,
        verify=False
    )
    if resp.status_code != 200:
        raise Exception(f"获取青龙环境变量失败，HTTP 状态码: {resp.status_code}")
    result = resp.json()
    if result.get('code') != 200:
        raise Exception(f"获取青龙环境变量失败，错误信息: {result.get('message', '未知错误')}")

    account_key, name_key = f'账户:{account}', f'望潮:{name}'
    qlid = next(
        (
            env['id']
            for env in result.get('data', [])
            if env.get('name') == osname
            and env.get('remarks')
            and (
                account_key in env['remarks']
                or (name_key in env['remarks'] and env.get('value') == value)
            )
        ),
        None
    )
    if qlid:
        QLupdate(osname=osname, value=value, account=account, qlid=qlid, name=name, auth_time=auth_time, user_id=user_id)
    else:
        QLzt(osname=osname, value=value, account=account, name=name, auth_time=auth_time, user_id=user_id)
    return True

def allenvs(osname, account):
    try:
        panel_type, p1, p2, p3 = _get_panel_config()
        if panel_type == "daidai":
            host, app_key, app_secret = p1, p2, p3
            env_list = _daidai_list_envs(host, app_key, app_secret, osname)
            account_key = f'账户:{account}'
            for env in env_list:
                if env.get("name") == osname and env.get("remarks") and (account_key in env["remarks"] or str(account) in (env.get("remarks") or "")):
                    return env.get("id")
            return None
        QLurl, ClientID, ClientSecret = p1, p2, p3
        qltoken = QLtoken(QLurl, ClientID, ClientSecret)
        resp = requests.get(f"{QLurl}/open/envs", headers={"Authorization": f"Bearer {qltoken}", "accept": "application/json"}, timeout=10, verify=False)
        if resp.status_code == 200:
            result = resp.json()
            if result.get('code') == 200:
                account_key = f'账户:{account}'
                return next((env['id'] for env in result['data'] if env.get('name') == osname and env.get('remarks') and (account_key in env['remarks'] or str(account) in env['remarks'])), None)
    except Exception as e:
        print(f"查询变量时出错: {str(e)}")
    return None

def delenvs(id):
    if not id:
        return
    try:
        panel_type, p1, p2, p3 = _get_panel_config()
        if panel_type == "daidai":
            host, app_key, app_secret = p1, p2, p3
            _daidai_delete_env(host, app_key, app_secret, id)
        else:
            _ql_request('delete', '/open/envs', [id])
    except Exception as e:
        print(f"删除变量时出错: {str(e)}")

def get_query_proxy(proxy_api_url, silent=False):
    if not proxy_api_url:
        return None
    try:
        resp = requests.get(proxy_api_url, timeout=5)
        if resp.status_code == 200:
            proxy_data = resp.text.strip()
            if proxy_data:
                if not silent:
                    print(f'🔔查询使用代理: {proxy_data}')
                return {'http': f'http://{proxy_data}', 'https': f'http://{proxy_data}'}
    except Exception as e:
        if not silent:
            print(f'🔔获取查询代理失败: {str(e)}')
    return None

def random_string(s, length):
    return ''.join(random.choices(s, k=length))

def generate_uuid():
    return f'{random_string("1234567890abcdef", 8)}-{random_string("1234567890abcdef", 4)}-{random_string("1234567890abcdef", 4)}-{random_string("1234567890abcdef", 4)}-{random_string("1234567890abcdef", 12)}'

def build_signature(path, session, req_id, timestamp):
    sha = f'{path}&&{session}&&{req_id}&&{timestamp}&&FR*r!isE5W&&64'
    return hashlib.sha256(sha.encode('utf-8')).hexdigest()

def encrypt_password(password):
    key_bytes = base64.b64decode(_PUBLIC_KEY_PEM)
    public_key = serialization.load_der_public_key(key_bytes)
    cipher_text = public_key.encrypt(password.encode(), padding.PKCS1v15())
    return urllib.parse.quote(base64.b64encode(cipher_text).decode('utf-8'), safe='')

def extract_signin_amount(award_name):
    try:
        amount_str = normalize_award_name(award_name)
        for prefix in SIGNIN_PREFIXES:
            if prefix in amount_str:
                amount_str = amount_str.split(prefix)[-1]
        amount_str = amount_str.replace('元', '').strip()
        match = re.search(r'(\d+\.?\d*)', amount_str)
        return float(match.group(1)) if match else None
    except:
        return None

def normalize_award_name(award_name):
    award_display = str(award_name or '').strip()
    return award_display.replace('Ԫ', '元').replace('¥', '元')

def format_signin_award(award_name):
    award_display = normalize_award_name(award_name)
    for prefix in SIGNIN_PREFIXES:
        if prefix in award_display:
            award_display = award_display.split(prefix)[-1]
    award_display = award_display.strip()
    if re.search(r'\d+\.?\d*', award_display) and '元' not in award_display:
        award_display += '元'
    return award_display

def is_same_month(date, current_date):
    return date.month == current_date.month and date.year == current_date.year

def is_same_day(date, current_date):
    return date.day == current_date.day and date.month == current_date.month and date.year == current_date.year
def build_query_msg(account_data, _legacy_status="", jrsy=None, bysy=None, xxsy=None, error_msg=None):
    msg = f'========望潮查询========\n账号: {account_data["name"]}\n'
    if jrsy is not None and bysy is not None:
        msg += f'今日收益: 💰{jrsy}\n本月收益: 💰{bysy}\n'
    if error_msg:
        msg += f'=====================\n{error_msg}'
    elif xxsy and xxsy != '暂无中奖记录\n':
        msg += f'中奖记录:\n{xxsy.rstrip()}'
    else:
        msg += '暂无中奖记录'
    return msg + '\n====================='

class ATM_WC:
    def __init__(self, u, s):
        self.sqsj = None
        self.name = None
        self.user = u
        self.sender = s
        self.account = None
        self.session = None
        self.id_dict = {}
        self.JSESSIONID = None
        self.s_JSESSIONID = None
        self.phone = None
        self.passwd = None
        self.code = None
        self.idd = None
        self.new_id = None
        self.query_lock = threading.Lock()  # 线程锁，用于保护查询时的属性访问
        self.headers = {
            "X-SESSION-ID": "6498052ebf15a44961f350e1",
            "X-REQUEST-ID": "7c549049-a97b-4acb-96c6-3e2db706667d",
            "X-TIMESTAMP": "1687685127765",
            "X-SIGNATURE": "50e1530a02086535f5f0c2c58e7bbdea521468d3e5a2874541456da7755bbd6e",
            "X-TENANT-ID": "64",
            "User-Agent": "5.3.1;00000000-699e-76bc-ffff-ffff9e3d172a;Meizu 16T;Android;9;huawei",
            "Cache-Control": "no-cache",
            "Host": "vapp.taizhou.com.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip"
        }
        self.cx_headers = {
            'Host': 'xmt.taizhou.com.cn',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36;xsb_wangchao;xsb_wangchao;5.3.1;native_app',
            'Accept': '*/*',
            'X-Requested-With': 'com.shangc.tiennews.taizhou',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://xmt.taizhou.com.cn/readingAward/',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        }

    def mask_phone(self, phone):
        return phone[:3] + '*' * 4 + phone[7:] if len(phone) >= 11 else phone

    def _get_login_tips(self, is_batch=False):
        batch_tip = "支持批量登录，请按下面格式发送账号信息：\n   格式：手机号#密码（每行一个账号）\n   示例：\n   13800138000#password1\n   13800138001#password2\n" if is_batch else "请输入你的账号和密码，格式如下：\n   手机号#密码（中间不加空格）\n"
        return (f"👋 你好，欢迎使用【望潮】{'批量' if is_batch else ''}登录功能～\n"
                f"📱 软件：望潮 App\n"
                f"📍 入口：首页 → 阅读有礼 → 右下角抽奖\n"
                f"⚠️ 请先在 App 内绑定支付宝账号，避免提现失败\n"
                f"✅ {batch_tip}"
                f"🔐 如未设置密码，请前往：我的 → 头像 → 账号信息 中设置或修改密码\n"
                f"🔧 望潮可修改密码版本：https://d.igdu.xyz/5Kia\n"
                f"{'如需退出本次操作，请回复「q」或「Q」。' if is_batch else '如需退出本次操作，请回复「q」或「Q」。'}")

    def _parse_accounts(self, input_text):
        accounts = []
        for line in input_text.split('\n'):
            line = line.strip()
            if '#' in line:
                phone, password = line.split('#', 1)
                accounts.append({'phone': phone.strip(), 'password': password.strip()})
        return accounts

    def _save_account_data(self, ql_value, is_new=True):
        data = _sg_literal(sg.bucketGet('dd_wccks', self.user) or '{}', {})
        created = self.account not in data
        previous = data.get(self.account, {})
        data[self.account] = {
            'name': self.name, 'ck': self.session, 'ql_value': ql_value,
            'sqsj': previous.get('sqsj', '2099-12-31'),
        }
        sg.bucketSet('dd_wccks', self.user, str(data))
        return created, data[self.account]['sqsj']

    def get_display_name(self, account_data):
        ql_value = account_data.get('ql_value', '')
        if ql_value:
            ql_value_str = str(ql_value).strip()
            if '#' in ql_value_str:
                phone = ql_value_str.split('#')[0].strip()
                if phone.isdigit() and len(phone) == 11:
                    return self.mask_phone(phone)
            elif ql_value_str.isdigit() and len(ql_value_str) == 11:
                return self.mask_phone(ql_value_str)
        name = str(account_data.get('name', '')).strip()
        if name and name.isdigit() and len(name) == 11:
            return self.mask_phone(name)
        return name if name else '未知'

    def wcsc(self):
        self.zh_login_batch()

    def zh_login_batch(self):
        self.sender.reply(self._get_login_tips(is_batch=True))
        raw = self.sender.input(120000, 10000, False)
        if not raw or str(raw).lower() == 'q': return
        accounts = self._parse_accounts(raw)
        success = 0; results = []
        for item in accounts:
            self.phone = item['phone']; self.original_password = item['password']
            try:
                self.passwd = encrypt_password(self.original_password)
                if not (self.get_session() and self.get_info()): raise ValueError('登录失败')
                value = f'{self.phone}#{self.original_password}'
                self._save_account_data(value)
                Addenvs(dd_wc_osname, value, self.account, self.name, '2099-12-31', self.user)
                success += 1; results.append(f'✅ {self.name} ({self.mask_phone(self.phone)})')
            except Exception as exc: results.append(f'❌ {self.mask_phone(self.phone)}：{exc}')
        self.sender.reply(f'=====批量登录结果=====\n✅ 成功：{success}\n❌ 失败：{len(accounts)-success}\n' + '\n'.join(results) + '\n=====================')

    def get_session(self):
        get_code = self.get_code()
        if get_code is True:
            try:
                request = generate_uuid()
                current_timestamp = int(time.time() * 1000)
                self.session = '66545332bf15a47d5156525d'
                signature = build_signature('/api/zbtxz/login', self.session, request, current_timestamp)
                self.headers['X-SESSION-ID'] = self.session
                self.headers['X-REQUEST-ID'] = f'{request}'
                self.headers['X-TIMESTAMP'] = f'{current_timestamp}'
                self.headers['X-SIGNATURE'] = f'{signature}'
                data = f"check_token=&code={self.code}&token=&type=-1&union_id="
                r = requests.post(
                    "https://vapp.taizhou.com.cn/api/zbtxz/login",
                    headers={
                        'User-Agent': "6.0.2;00000000-699e-0680-0000-0000090ca05c;Xiaomi Redmi Note 8 Pro;Android;11;xiaomi;6.10.0",
                        'Connection': "Keep-Alive",
                        'Accept-Encoding': "gzip",
                        'Content-Type': "application/x-www-form-urlencoded",
                        'X-SESSION-ID': "66545332bf15a47d5156525d",
                        'X-REQUEST-ID': "13af7ac0-2430-48ae-af04-7d58e5c7a12b",
                        'X-TIMESTAMP': "1716962517478",
                        'X-SIGNATURE': "3f6fe2e705c5923f48452ff68d83d78e7ee00efa03882757c3e5b64610cdb4a3",
                        'X-TENANT-ID': "64",
                        'Cache-Control': "no-cache"
                    },
                    data=data,
                    verify=False
                )
                code = r.json().get('code', None)
                messages = r.json().get('message', None)
                if code == 0:
                    self.session = r.json()['data']['session']['id']
                    return True
                else:
                    return messages
            except Exception as e:
                return e
        else:
            self.sender.reply(f'获取code失败：{get_code}')

    def get_code(self):
        try:
            data = f"client_id=10019&password={self.passwd}&phone_number={self.phone}"
            r = requests.post(
                "https://passport.tmuyun.com/web/oauth/credential_auth",
                headers={
                    'Content-Type': "application/x-www-form-urlencoded"
                },
                data=data,
                verify=False
            )
            code = r.json().get('code', None)
            messages = r.json().get('message', None)
            if code == 0:
                self.code = r.json()['data']['authorization_code']['code']
                return True
            else:
                return messages
        except Exception as e:
            return e

    def get_info(self):
        try:
            request = generate_uuid()
            current_timestamp = int(time.time() * 1000)
            signature = build_signature('/api/user_mumber/account_detail', self.session, request, current_timestamp)
            self.headers['X-SESSION-ID'] = self.session
            self.headers['X-REQUEST-ID'] = f'{request}'
            self.headers['X-TIMESTAMP'] = f'{current_timestamp}'
            self.headers['X-SIGNATURE'] = f'{signature}'

            r = requests.get('https://vapp.taizhou.com.cn/api/user_mumber/account_detail', headers=self.headers,
                             verify=False,timeout=5)
            if 'success' in r.json()['message']:
                self.name = r.json()["data"]["rst"]["nick_name"]
                self.account = r.json()['data']['rst']['id']
                return True
            else:
                return f"❌登录失败!\n{r.json()['message']}"
        except Exception as e:
            return f"⛔登录异常!\n{e}"

    def wcgl(self):
        data = _sg_literal(sg.bucketGet('dd_wccks', self.user) or '{}', {})
        if not data:
            self.sender.reply('❌ 未绑定账号，请先发送「望潮登录」')
            return
        accounts = list(data.items())
        self.sender.reply('========望潮管理========\n' + '\n'.join(
            f'[{i}] {self.get_display_name(info)}' for i, (_, info) in enumerate(accounts, 1)
        ) + '\n=====================\n回复序号，输入 q 退出')
        choice = self.sender.listen(60000)
        if not choice or str(choice).lower() == 'q': return
        if not str(choice).isdigit() or not 1 <= int(choice) <= len(accounts):
            self.sender.reply('❌ 序号无效'); return
        self.account, info = accounts[int(choice)-1]
        self.session = info.get('ck', ''); self.name = info.get('name', self.account)
        self.gl_zh()

    def gl_zh(self):
        self.sender.reply(f'========账号管理========\n账号: {self.name}\n[1] 查询账号\n[2] 删除账号\n=====================')
        choice = self.sender.listen(60000)
        if choice == '1':
            data = _sg_literal(sg.bucketGet('dd_wccks', self.user) or '{}', {})
            if self.account in data: self.sender.reply(self.query_single_account(self.account, data[self.account]))
        elif choice == '2': self.del_zh()

    def del_zh(self):
        self.sender.reply(f'是否删除账号【{self.name}】？(y/n)')
        zh = self.sender.listen(60000)
        if zh == 'n' or zh == 'N':
            self.sender.reply("退出！")

        elif zh is None:
            self.sender.reply('超时退出！')

        elif zh == 'y' or zh == 'Y':
            ts = sg.bucketGet('dd_wccks', self.user)
            ts = _sg_literal(ts)
            del ts[f'{self.account}']
            sg.bucketSet('dd_wccks', self.user, f'{ts}')
            try:
                qlid = allenvs(osname=dd_wc_osname, account=self.account)
                if qlid:
                    delenvs(id=qlid)
            except:
                pass
            self.sender.reply(f'{self.name}>>>删除成功！')
        else:
            self.sender.reply('输入有误，退出！')

    def batch_delete_accounts(self):
        data = _sg_literal(sg.bucketGet('dd_wccks', self.user) or '{}', {})
        if not data:
            self.sender.reply('❌ 暂无账号'); return
        accounts = list(data.items())
        self.sender.reply('=====删除账号=====\n[0] 删除全部\n' + '\n'.join(
            f'[{i}] {self.get_display_name(info)}' for i, (_, info) in enumerate(accounts, 1)
        ) + '\n==================')
        raw = self.sender.listen(60000)
        if not raw or str(raw).lower() == 'q': return
        if str(raw) == '0': selected = list(range(len(accounts)))
        else:
            try: selected = sorted({int(x.strip())-1 for x in str(raw).split(',')})
            except ValueError: selected = []
        selected = [i for i in selected if 0 <= i < len(accounts)]
        if not selected:
            self.sender.reply('❌ 序号无效'); return
        self.sender.reply(f'确认删除 {len(selected)} 个账号请回复 y')
        if str(self.sender.listen(60000)).lower() != 'y': return
        removed = 0
        for i in selected:
            account, _ = accounts[i]
            data.pop(account, None)
            try:
                env_id = allenvs(dd_wc_osname, account)
                if env_id: delenvs(env_id)
            except Exception: pass
            removed += 1
        sg.bucketSet('dd_wccks', self.user, str(data))
        self.sender.reply(f'✅ 已删除 {removed} 个账号')

    def query_single_account(self, account_id, account_data, query_proxy_api=None, max_retries=3):
        self.session = account_data.get('ck', ''); self.account = account_id
        self.name = account_data.get('name', account_id)
        for retry in range(max_retries):
            try:
                proxies = get_query_proxy(query_proxy_api, silent=True) if query_proxy_api else None
                result = self.get_cjjl(proxies=proxies)
                if isinstance(result, tuple):
                    return build_query_msg(account_data, '', *result)
                if retry + 1 < max_retries: time.sleep(1); continue
                if self.get_info() is not True: return build_query_msg(account_data, '', error_msg='❌ 账户已失效，请重新登录')
                return build_query_msg(account_data, '', error_msg=f'⚠️ 查询失败：{result}')
            except Exception as exc:
                if retry + 1 == max_retries: return build_query_msg(account_data, '', error_msg=f'⚠️ 查询异常：{exc}')
        return build_query_msg(account_data, '', error_msg='⚠️ 查询失败')

    def wccx(self):
        ts = sg.bucketGet('dd_wccks', self.user)
        if ts == '' or ts == '{}':
            self.sender.reply("望潮系统未查询到您的信息! 请先登录! ")
        else:
            query_proxy_api = sg.bucketGet('dd_wcconfig', 'cxproxy') or ''
            if query_proxy_api:
                query_proxy_api = query_proxy_api.strip()

            ts = _sg_literal(ts)
            n = 0
            id_dict = {}
            msg = '========望潮查询========\n'
            msg += '[0] 一键查询所有账号\n'

            for k, y in ts.items():
                n += 1
                id_dict[n] = {
                    'usid': k,
                    'name': y['name'],
                    'ck': y['ck'],
                    'sqsj': y['sqsj']
                }
                display_name = self.get_display_name(y)
                msg += f'[{n}] {display_name}\n'

            msg += '=====================\n'
            msg += '回复序号选择账号,退出【q】！'
            self.sender.reply(msg)

            xz = self.sender.listen(60000)
            xz_list = []
            for k, y in id_dict.items():
                xz_list.append(k)
            xz_list.append(0)  # 添加一键查询选项

            try:
                xz_int = int(xz)
            except:
                xz_int = -1

            if xz == 'q' or xz == 'Q':
                self.sender.reply("退出！")
            elif xz is None:
                self.sender.reply('超时退出！')
            elif xz_int == 0:
                total_accounts = len(ts)
                for idx, (k, y) in enumerate(ts.items(), 1):
                    account_msg = self.query_single_account(k, y, query_proxy_api=query_proxy_api if query_proxy_api else None)
                    self.sender.reply(account_msg)
                    if idx < total_accounts:
                        time.sleep(0.1)  # 减少延迟时间
            elif xz_int in xz_list:
                zh = id_dict[int(xz)]
                account_msg = self.query_single_account(zh['usid'], {
                    'name': zh['name'],
                    'ck': zh['ck'],
                    'sqsj': zh['sqsj']
                }, query_proxy_api=query_proxy_api if query_proxy_api else None)
                self.sender.reply(account_msg)
            else:
                self.sender.reply('输入有误，退出！')

    def get_cjjl(self, proxies=None, max_retries=2):
        for retry in range(max_retries):
            try:
                JSESSIONID = self.get_s_JSESSIONID(proxies=proxies)
                if JSESSIONID is True:
                    self.cx_headers['Cookie'] = self.s_JSESSIONID
                    h = {
                    'Host': 'srv-app.taizhou.com.cn',
                    'Connection': 'keep-alive',
                    'Pragma': 'no-cache',
                    'Cache-Control': 'no-cache',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36;xsb_wangchao;xsb_wangchao;5.3.1;native_app',
                    'Accept': '*/*',
                    'X-Requested-With': 'com.shangc.tiennews.taizhou',
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Dest': 'empty',
                    'Referer': 'https://srv-app.taizhou.com.cn/luckdraw/',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                    'Cookie': self.s_JSESSIONID,
                }
                    jl_params = {
                        'pageSize': str(max(100, zjsl * 3)),  # 至少获取100条或配置条数的3倍
                        'pageNum': '1',
                        'activityId': '67',
                    }
                    request_kwargs = {
                        'params': jl_params,
                        'headers': h,
                        'verify': False,
                        'timeout': 15  # 增加超时时间到15秒
                    }
                    if proxies:
                        request_kwargs['proxies'] = proxies

                    try:
                        jl_r = requests.get(
                            'https://srv-app.taizhou.com.cn/tzrb/userAwardRecordUpgrade/pageList',
                            **request_kwargs
                        )
                        jl_data = jl_r.json()

                        message = jl_data.get('message', '')
                        if '频繁' in message or '稍后再试' in message or '操作频繁' in message:
                            if retry < max_retries - 1:
                                time.sleep(10)
                                continue
                            return "接口频繁，请稍后再试"

                        if '成功' in message:
                            jl_list = jl_data.get('data', {}).get('records', [])
                            current_date = datetime.now()
                            bysy = 0.0
                            jrsy = 0.0
                            reading_records = []  # 存储阅读中奖记录

                            is_early_month = current_date.day <= 5
                            if is_early_month:
                                if current_date.month == 1:
                                    last_month_start = datetime(current_date.year - 1, 12, 26)
                                else:
                                    last_month_start = datetime(current_date.year, current_date.month - 1, 26)
                            else:
                                last_month_start = None

                            for i in jl_list:
                                try:
                                    createTime = i.get("createTime", "")
                                    awardName = normalize_award_name(i.get("awardName", ""))
                                    if not createTime or not awardName:
                                        continue

                                    date = datetime.strptime(createTime, '%Y-%m-%d %H:%M:%S')

                                    is_valid_date = (date.month == current_date.month and date.year == current_date.year) or (is_early_month and last_month_start and date >= last_month_start)

                                    if is_valid_date:
                                        reading_records.append({
                                            'time': createTime,
                                            'award': awardName,
                                            'date': date
                                        })

                                        if amount := extract_signin_amount(awardName):
                                            if is_same_month(date, current_date):
                                                bysy += amount
                                            if is_same_day(date, current_date):
                                                jrsy += amount
                                except Exception:
                                    continue

                            duration_records = []
                            duration_params = {
                                'pageSize': str(max(100, zjsl * 3)),
                                'pageNum': '1',
                                'activityId': '169',
                            }
                            duration_request_kwargs = {
                                'params': duration_params,
                                'headers': h,
                                'verify': False,
                                'timeout': 15
                            }
                            if proxies:
                                duration_request_kwargs['proxies'] = proxies

                            try:
                                duration_r = requests.get(
                                    'https://srv-app.taizhou.com.cn/tzrb/userAwardRecordUpgrade/pageList',
                                    **duration_request_kwargs
                                )
                                duration_data = duration_r.json()
                                duration_list = duration_data.get('data', {}).get('records', [])
                                for i in duration_list:
                                    try:
                                        create_time = i.get('createTime', '')
                                        award_name = normalize_award_name(i.get('awardName', ''))
                                        if not create_time or not award_name:
                                            continue
                                        date = datetime.strptime(create_time, '%Y-%m-%d %H:%M:%S')
                                        is_valid_date = (date.month == current_date.month and date.year == current_date.year) or (is_early_month and last_month_start and date >= last_month_start)
                                        if is_valid_date:
                                            duration_records.append({
                                                'time': create_time,
                                                'award': award_name,
                                                'date': date
                                            })
                                    except Exception:
                                        continue
                            except Exception:
                                duration_records = []

                            duration_today_amount = 0.0
                            duration_month_amount = 0.0
                            for record in duration_records:
                                if amount := extract_signin_amount(record['award']):
                                    if is_same_month(record['date'], current_date):
                                        duration_month_amount += amount
                                    if is_same_day(record['date'], current_date):
                                        duration_today_amount += amount

                            jrsy = round(jrsy + duration_today_amount, 2)
                            bysy = round(bysy + duration_month_amount, 2)

                            reading_records.sort(key=lambda x: x['date'], reverse=True)
                            duration_records.sort(key=lambda x: x['date'], reverse=True)
                            reading_display = reading_records[:zjsl]
                            duration_display = duration_records[:zjsl]
                            xxsy = ''
                            if reading_display or duration_display:
                                if reading_display:
                                    xxsy += "阅读:\n"
                                    for record in reading_display:
                                        xxsy += f"⏰{record['time']}: {normalize_award_name(record['award'])}\n"
                                if duration_display:
                                    xxsy += "=====================\n时长:\n"
                                    for record in duration_display:
                                        xxsy += f"⏰{record['time']}: {format_signin_award(record['award'])}\n"
                            else:
                                xxsy = '暂无中奖记录\n'

                            return round(jrsy, 2), round(bysy, 2), xxsy
                        else:
                            if retry < max_retries - 1:
                                time.sleep(1)
                                continue
                            return f"查询失败: {message}"
                    except requests.exceptions.Timeout:
                        if retry < max_retries - 1:
                            continue
                        return "请求超时"
                    except requests.exceptions.RequestException as e:
                        if retry < max_retries - 1:
                            time.sleep(1)
                            continue
                        return f"网络错误: {str(e)}"
                    except Exception as e:
                        if retry < max_retries - 1:
                            time.sleep(1)
                            continue
                        return f"查询异常: {str(e)}"
                else:
                    if retry < max_retries - 1:
                        time.sleep(1)
                        continue
                    return JSESSIONID
            except Exception as e:
                if retry < max_retries - 1:
                    time.sleep(1)
                    continue
                return f"查询异常: {str(e)}"

        return "查询失败，请稍后再试"

    def get_s_JSESSIONID(self, proxies=None, max_retries=2):
        for retry in range(max_retries):
            try:
                params = {
                    'accountId': self.account,
                    'sessionId': self.session,
                }
                h = {
                    'Connection': 'Keep-Alive',
                    'Accept': '*/*',
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Dest': 'empty',
                    'cookie': '',
                    'Referer': 'https://xmt.taizhou.com.cn/readingLuck-v1/',
                    'X-Requested-With': 'com.shangc.tiennews.taizhou',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                    'user-agent': 'Mozilla/5.0 (Linux; Android 11; 21091116AC Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.85 Mobile Safari/537.36;xsb_wangchao;xsb_wangchao;6.0.2;native_app;6.10.0',
                }
                request_kwargs = {
                    'params': params,
                    'headers': h,
                    'verify': False,
                    'timeout': 15  # 增加超时时间
                }
                if proxies:
                    request_kwargs['proxies'] = proxies

                try:
                    c_r = requests.get(
                        'https://srv-app.taizhou.com.cn/tzrb/user/loginWC',
                        **request_kwargs
                    )
                    message = c_r.json().get('message', None)
                    if message == '操作成功':
                        jsessionid = c_r.cookies
                        cookies_dict = jsessionid.get_dict()
                        for k, y in cookies_dict.items():
                            JSESSIONID = f'{k}={y}'
                            self.s_JSESSIONID = JSESSIONID
                        return True
                    else:
                        if '频繁' in str(message) or '稍后再试' in str(message):
                            if retry < max_retries - 1:
                                time.sleep(10)
                                continue
                        if retry < max_retries - 1:
                            time.sleep(1)
                            continue
                        return message
                except requests.exceptions.Timeout:
                    if retry < max_retries - 1:
                        continue
                    return "请求超时"
                except requests.exceptions.RequestException as e:
                    if retry < max_retries - 1:
                        time.sleep(1)
                        continue
                    return f"网络错误: {str(e)}"
            except Exception as e:
                if retry < max_retries - 1:
                    time.sleep(1)
                    continue
                return f"获取JSESSIONID异常: {str(e)}"

        return "获取JSESSIONID失败"

    def update_qinglong(self):
        try:
            self.sender.reply("🔔 开始更新所有账户数据到青龙...")

            if not dd_wc_qlname:
                self.sender.reply("❌ 未配置青龙容器信息，请在配置中设置")
                return

            all_users = sg.bucketAllKeys('dd_wccks')
            if not all_users:
                self.sender.reply("❌ 未找到任何用户数据")
                return

            today_time = datetime.now().strftime("%Y-%m-%d")

            success_count = 0  # 成功更新的数量
            error_count = 0     # 处理失败的数量
            skip_count = 0      # 跳过数量（没有ql_value的）

            total_accounts = 0  # 总账户数

            for user_id in all_users:
                try:
                    user_data = sg.bucketGet('dd_wccks', user_id)
                    if not user_data or user_data == '' or user_data == '{}':
                        continue

                    user_data = _sg_literal(user_data)
                    if not user_data or user_data == {}:
                        continue

                    for account_id, account_info in user_data.items():
                        total_accounts += 1
                        account_name = account_info.get('name', '未知')
                        sqsj = account_info.get('sqsj', today_time)
                        ql_value = account_info.get('ql_value', account_info.get('ck', ''))

                        if not ql_value:
                            skip_count += 1
                            continue

                        try:
                            Addenvs(
                                osname=dd_wc_osname,
                                value=ql_value,
                                account=account_id,
                                name=account_name,
                                auth_time=sqsj,
                                user_id=user_id
                            )
                            success_count += 1
                        except Exception as e:
                            error_count += 1
                            print(f"更新青龙失败 - 账户: {account_name}, 错误: {str(e)}")

                except Exception as e:
                    error_count += 1
                    print(f"处理用户 {user_id} 时出错: {str(e)}")
                    continue

            result_msg = f"""=====更新青龙完成=====
📊 总账户数: {total_accounts}个
✅ 成功更新: {success_count}个
⏭️ 跳过数量: {skip_count}个
❌ 处理失败: {error_count}个
=====================
💡 说明:
• 所有账户数据已更新到青龙
• 包括已过期和未过期的账户
====================="""

            self.sender.reply(result_msg)

        except Exception as e:
            self.sender.reply(f"❌ 更新青龙失败: {str(e)}")

if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    sender = sg.Sender(sg.getSenderID()); user = sender.getUserID(); message = sender.getMessage()
    plugin = ATM_WC(user, sender)
    if '登录' in message or '登陆' in message: plugin.wcsc()
    elif '管理' in message: plugin.wcgl()
    elif '查询' in message: plugin.wccx()
    elif '删除' in message: plugin.batch_delete_accounts()
    elif message.strip() == '望潮教程':
        sender.reply('=====望潮教程=====\n望潮登录：批量绑定 手机号#密码\n望潮管理：查询或删除单个账号\n望潮查询：查询收益和中奖记录\n望潮删除：批量删除账号\n望潮更新青龙：同步全部账号到面板\n=====================')
    elif '更新青龙' in message or '同步' in message:
        if sender.isAdmin(): plugin.update_qinglong()
    elif sender.getImtype() == 'fake': plugin.update_qinglong()
    else: sender.setContinue()
