# [title: 望潮]
# [name: wangChao]
# [language: python]
# [class: 任务]
# [author: sky2022]
# [version: v2.3]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(望潮管理|管理望潮|望潮查询|查询望潮|望潮登录|望潮登陆|登录望潮|登陆望潮|望潮望潮|望潮教程|望潮检测|望潮通知|通知望潮|望潮对接测试|望潮清理|清理望潮|望潮同步|同步望潮)$]
# [cron: 56 8,15 * * *]
# [icon: https://pp.myapp.com/ma_icon/0/icon_42259219_1711261436/256]
# [description: 望潮插件；1.1更新了WXPUSH通知，现在可以把每个人登录的账户收益通知全部单独发给用户；1.6更新：统一面板配置为面板类型+对接面板配置，并新增呆呆面板分组配置]
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
    'dd_wcconfig_PanelType': form.string().title('面板类型').default('').description('对接面板：qinglong=青龙，daidai=呆呆（DaiDaiPanel），不填默认为青龙'),
    'dd_wcconfig_Qinglong': form.string().title('设置对接容器').default('').description('青龙用丨分割3项；呆呆为 Open API 的 host、app_key、app_secret'),
    'dd_wcconfig_osname': form.string().title('变量名').default('').description('面板内望潮账号使用的变量名（青龙/呆呆通用）'),
    'dd_wcconfig_zjsl': form.string().title('中奖记录条数').default('').description('查询时显示的中奖记录条数，默认30条'),
    'dd_wcconfig_cxproxy': form.string().title('查询代理API').default('').description('望潮查询使用的代理API地址，每查询一个账号自动切换IP'),
    'dd_wcconfig_docking_enabled': form.boolean().title('启用对接运行').default(False).description('是否对接到作者容器运行，开启后需上传容器配置,同步指令：望潮对接测试'),
    'dd_wcconfig_wxpusher_app_token': form.string().title('WxPusher AppToken').default('').description('不填则不推送WxPusher日志'),
})
_CONFIG_FIELD_MAP = {
    ('dd_wcconfig', 'PanelType'): 'dd_wcconfig_PanelType',
    ('dd_wcconfig', 'Qinglong'): 'dd_wcconfig_Qinglong',
    ('dd_wcconfig', 'osname'): 'dd_wcconfig_osname',
    ('dd_wcconfig', 'zjsl'): 'dd_wcconfig_zjsl',
    ('dd_wcconfig', 'cxproxy'): 'dd_wcconfig_cxproxy',
    ('dd_wcconfig', 'docking_enabled'): 'dd_wcconfig_docking_enabled',
    ('dd_wcconfig', 'wxpusher_app_token'): 'dd_wcconfig_wxpusher_app_token',
}

import json
from datetime import datetime, timedelta
import hashlib
import random
import time
import re
from urllib3.exceptions import InsecureRequestWarning
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
import base64
import uuid
import urllib.parse
import requests
import urllib3
import threading

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
DOCKING_API = 'http://vip.xa.frp.one:39701/api'
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
wxzsm = sg.bucketGet('dd_wcconfig', 'wxzsm')
sqje = '2099-12-31' or '6.6'
sqsj = '2099-12-31' or '30'
wccoin = sg.bucketGet('dd_wcconfig', 'wccoin') or '0'
zjsl = int(sg.bucketGet('dd_wcconfig', 'zjsl') or '30')
today_date = datetime.now().date()
today_time = str(today_date)
docking_enabled = sg.bucketGet('dd_wcconfig', 'docking_enabled') == 'true'
docking_key = sg.bucketGet('dd_wcconfig', 'docking_key') or ''
SIGNIN_Q = sg.bucketGet('dd_wcconfig', 'signin_q') or _DEFAULT_SIGNIN_Q
try:
    SIGNIN_LOTTERY_ACTIVITY_ID = int(sg.bucketGet('dd_wcconfig', 'signin_lottery_activity_id') or _DEFAULT_SIGNIN_LOTTERY_ACTIVITY_ID)
except ValueError:
    SIGNIN_LOTTERY_ACTIVITY_ID = _DEFAULT_SIGNIN_LOTTERY_ACTIVITY_ID
SIGNIN_LOTTERY_Q = sg.bucketGet('dd_wcconfig', 'signin_lottery_q') or _DEFAULT_SIGNIN_LOTTERY_Q

def upload_docking_config():
    if not docking_enabled:
        return False, "未启用对接运行功能"

    if not docking_key:
        return False, "未配置对接卡密，请检查配置获取"

    if not DOCKING_API:
        return False, "对接API地址未配置"

    if not dd_wc_qlname:
        return False, "未配置对接容器信息"

    try:
        panel_type, p1, p2, p3 = _get_panel_config()

        if panel_type == "daidai":
            host, app_key, app_secret = p1, p2, p3
            try:
                token = _daidai_get_token(host, app_key, app_secret)
                if not token:
                    return False, "呆呆面板连接失败，请检查配置"
            except Exception as e:
                return False, f"呆呆面板连接失败: {str(e)}"
        else:
            QLurl, ClientID, ClientSecret = p1, p2, p3
            try:
                token = QLtoken(QLurl, ClientID, ClientSecret)
                if not token:
                    return False, "青龙容器连接失败，请检查配置"
            except Exception as e:
                return False, f"青龙容器连接失败: {str(e)}"

        upload_data = {
            "docking_key": docking_key,
            "user_id": userid,
            "qinglong_url": p1,  # 青龙为URL，呆呆为host
            "client_id": p2,     # 青龙为ClientID，呆呆为app_key
            "client_secret": p3, # 青龙为ClientSecret，呆呆为app_secret
            "env_name": dd_wc_osname,
            "panel_type": panel_type,  # 添加面板类型
            "timestamp": datetime.now().isoformat()
        }
        response = requests.post(
            f"{DOCKING_API}/upload_config",
            json=upload_data,
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 200:
                return True, result.get('message', '对接配置上传成功')
            else:
                return False, result.get('message', '上传失败')
        else:
            return False, f"请求失败，状态码: {response.status_code}"

    except Exception as e:
        return False, f"上传异常: {str(e)}"

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
    """返回 (panel_type, p1, p2, p3)：panel_type 为 'qinglong' 或 'daidai'，呆呆时为 host, app_key, app_secret，青龙时为 QLurl, ClientID, ClientSecret。"""
    if not dd_wc_qlname:
        raise Exception("未配置对接容器信息，请先在插件配置中设置")
    parts = [p.strip() for p in dd_wc_qlname.split('丨') if p.strip()]
    if len(parts) != 3:
        raise Exception("对接容器格式错误：青龙为 URL丨ClientID丨ClientSecret，呆呆为 URL丨app_key丨app_secret")
    if dd_wc_panel_type == "daidai":
        return "daidai", parts[0].rstrip("/"), parts[1], parts[2]
    return "qinglong", parts[0], parts[1], parts[2]


def _get_ql_config():
    """青龙面板：返回 (QLurl, ClientID, ClientSecret)，仅用于青龙。"""
    panel_type, p1, p2, p3 = _get_panel_config()
    if panel_type != "qinglong":
        raise Exception("当前为呆呆面板，此操作仅支持青龙")
    return p1, p2, p3


def _daidai_get_token(host: str, app_key: str, app_secret: str) -> str:
    """呆呆面板：通过 Open API 获取 access_token。"""
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
    """呆呆面板统一请求：自动带 Authorization，401 时重新取 Token 再试一次。"""
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
    """呆呆：按变量名和 remarks 关键字查找环境变量，返回 id 或 None。"""
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
    """按 keyword 查询环境变量，返回与青龙一致的格式：[{"id", "name", "value", "remarks"}, ...]"""
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
    remarks = f'望潮:{name}丨账户:{account}丨用户:{owner_uid}丨授权时间:{auth_time}丨望潮管理'
    result = _ql_request('post', '/open/envs', [{"value": value, "name": osname, "remarks": remarks}])
    if result and "value must be unique" not in str(result):
        return result.get('data', [{}])[0].get('id')

def QLupdate(osname, value, account, qlid, name, auth_time=None, user_id=None):
    auth_time = auth_time or today_time
    owner_uid = user_id or userid
    remarks = f'望潮:{name}丨账户:{account}丨用户:{owner_uid}丨授权时间:{auth_time}丨望潮管理'
    _ql_request('put', '/open/envs', {"value": value, "name": osname, "remarks": remarks, "id": qlid})

def Addenvs(osname, value, account, name, auth_time=None, user_id=None):
    """
    向当前配置的面板（青龙或呆呆）添加/更新环境变量。
    - 成功时返回 True
    - 失败时抛出异常（由上层根据需要捕获并提示）
    """
    auth_time = auth_time or today_time
    owner_uid = user_id or userid
    remarks = f'望潮:{name}丨账户:{account}丨用户:{owner_uid}丨授权时间:{auth_time}丨望潮管理'

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

def parse_prize_time(create_time, fallback_date=None):
    if not create_time:
        return fallback_date or datetime.now(), (fallback_date or datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
    try:
        if 'T' in create_time:
            date_str = create_time.split('T')[0]
            time_str = create_time.split('T')[1].split('.')[0] if '.' in create_time.split('T')[1] else create_time.split('T')[1]
            date = datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %H:%M:%S')
        elif ' ' in create_time:
            date = datetime.strptime(create_time.split('.')[0], '%Y-%m-%d %H:%M:%S')
        else:
            date = datetime.strptime(create_time, '%Y-%m-%d')
            create_time = date.strftime('%Y-%m-%d %H:%M:%S')
        return date, create_time
    except:
        return fallback_date or datetime.now(), (fallback_date or datetime.now()).strftime('%Y-%m-%d %H:%M:%S')

def is_same_month(date, current_date):
    return date.month == current_date.month and date.year == current_date.year

def is_same_day(date, current_date):
    return date.day == current_date.day and date.month == current_date.month and date.year == current_date.year
def build_query_msg(account_data, sqsj, jrsy=None, bysy=None, xxsy=None, error_msg=None):
    msg = f'========望潮查询========\n账号: {account_data["name"]}\n授权时间: ⏰{account_data["sqsj"]}({sqsj})\n'
    if jrsy is not None and bysy is not None:
        msg += f'今日收益: 💰{jrsy}\n本月收益: 💰{bysy}\n'
    msg += '====================='
    if error_msg:
        msg += f'\n{error_msg}\n====================='
    elif xxsy and xxsy != '暂无中奖记录\n':
        msg += f'\n中奖记录:\n{xxsy.rstrip()}\n====================='
    else:
        msg += '\n暂无中奖记录\n====================='
    return msg

def generate_qrcode(url):
    try:
        return f"https://api.qrtool.cn/?text={urllib.parse.quote(url, safe='')}"
    except Exception as e:
        print(f"生成二维码失败: {str(e)}")
        return None

def send_qrcode_image(sender, qrcode_url, pay_type):
    pay_type_names = {'alipay': '支付宝', 'wxpay': '微信', 'qqpay': 'QQ钱包'}
    pay_type_name = pay_type_names.get(pay_type, pay_type)

    try:
        sender.replyImage(qrcode_url)
        if pay_type == 'qqpay':
            sender.reply(f"请使用【{pay_type_name}】扫描上方二维码完成支付\nQQ支付打开图片若是黑屏，长按屏幕进行\"识别二维码\"即可！\n支付过程中输入'q'可取消支付")
        else:
            sender.reply(f"请使用【{pay_type_name}】扫描上方二维码完成支付\n支付过程中输入'q'可取消支付")
    except:
        if pay_type == 'qqpay':
            pay_msg = f'请使用【{pay_type_name}】扫描下方二维码完成支付，支付过程中输入"q"可取消支付:\nQQ支付打开图片若是黑屏，长按屏幕进行"识别二维码"即可！\n[CQ:image,file={qrcode_url}]'
        else:
            pay_msg = f'请使用【{pay_type_name}】扫描下方二维码完成支付，支付过程中输入"q"可取消支付:\n[CQ:image,file={qrcode_url}]'
        sender.reply(pay_msg)

def get_payment_config():
    return {}


def _api_request(method, url, authorization="", body=None, x_token=None, proxies=None):
    h = {"accept": "application/json, text/plain, */*", "authorization": authorization,
         "accept-language": "zh-CN,zh-Hans;q=0.9", "user-agent": _USER_AGENT}
    if body:
        h["content-type"] = "application/json"
    if x_token:
        h["X-TOKEN"] = x_token
    if "lottery" in url:
        h["X-REQUEST-ID"] = f"{uuid.uuid4().hex}.{int(time.time() * 1000)}"
    kwargs = {'headers': h, 'verify': False, 'timeout': 20}
    if body:
        kwargs['data'] = json.dumps(body)
    if proxies:
        kwargs['proxies'] = proxies
    resp = (requests.post if method == 'POST' else requests.get)(url, **kwargs)
    resp.raise_for_status()
    return resp.json() or {}

def signin_get(path: str, authorization: str, proxies=None):
    return _api_request('GET', f"https://act.tmlyun.com/activity-api/signin/h5{path}", authorization, None, None, proxies)

def signin_post(path: str, body: dict, authorization: str = "", proxies=None):
    return _api_request('POST', f"https://act.tmlyun.com/activity-api/signin/h5{path}", authorization, body, None, proxies)

def lottery_get(path: str, authorization: str, x_token: str = None, proxies=None):
    return _api_request('GET', f"https://act.tmlyun.com/activity-api/lottery/h5{path}", authorization, None, x_token, proxies)

def lottery_post(path: str, authorization: str, body_dict: dict, proxies=None):
    return _api_request('POST', f"https://act.tmlyun.com/activity-api/lottery{path}", authorization, body_dict, None, proxies)

def ts_qb(data, wxpusher_alluid, name, arg1, arg2):
    api_url = 'https://wxpusher.zjiecode.com/api/send/message'
    app_token = sg.bucketGet('dd_wcconfig', 'wxpusher_app_token') or ''
    if not app_token:
        return False

    sorted_data = sorted(data, key=lambda x: x['序号'])

    table_content = ''
    for row in sorted_data:
        table_content += f"<tr><td style='border: 1px solid #ccc; padding: 6px;'>{row['序号']}</td><td style='border: 1px solid #ccc; padding: 6px;'>{row['用户']}</td><td style='border: 1px solid #ccc; padding: 6px;'>{row['arg1']}</td><td style='border: 1px solid #ccc; padding: 6px;'>{row['arg2']}</td></tr>"

    table_html = f"<table style='border-collapse: collapse;'><tr style='background-color: #f2f2f2;'><th style='border: 1px solid #ccc; padding: 8px;'>🆔</th><th style='border: 1px solid #ccc; padding: 8px;'>{name}</th><th style='border: 1px solid #ccc; padding: 8px;'>{arg1}</th><th style='border: 1px solid #ccc; padding: 8px;'>{arg2}</th></tr>{table_content}</table>"

    params = {
        "appToken": app_token,
        'content': table_html,
        'contentType': 3,  # 表格类型
        'topicIds': [],  # 接收消息的用户ID列表，为空表示发送给所有用户
        "summary": f'望潮日志推送',
        "uids": [wxpusher_alluid],
    }

    response = requests.post(api_url, json=params)

    notify = sg.bucketGet('dd_wcconfig', 'notify')

    def _notify(msg):
        if notify:
            sg.notifyMasters(msg, notify.split(','))
        sender.reply(msg)

    if response.status_code == 200:
        result = response.json()
        _notify(f"🎉wxpusher望潮日志推送成功" if result.get('code') == 1000 else f'💔wxpusher望潮日志推送失败，错误信息：{result.get("msg", "未知错误")}')
    else:
        _notify('⛔️wxpusher望潮日志推送请求失败')


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
        ts = sg.bucketGet('dd_wccks', self.user)
        today_str = datetime.now().strftime("%Y-%m-%d")
        if not ts:
            data = {f'{self.account}': {'name': self.name, 'ck': self.session, 'ql_value': ql_value, 'sqsj': today_str}}
            sg.bucketSet('dd_wccks', self.user, f'{data}')
            return True, today_str
        ts = _sg_literal(ts)
        if self.account in ts:
            old_sqsj = ts[f'{self.account}']['sqsj']
            ts[f'{self.account}'] = {'name': self.name, 'ck': self.session, 'ql_value': ql_value, 'sqsj': old_sqsj}
            sg.bucketSet('dd_wccks', self.user, f'{ts}')
            return False, old_sqsj
        ts[f'{self.account}'] = {'name': self.name, 'ck': self.session, 'ql_value': ql_value, 'sqsj': today_str}
        sg.bucketSet('dd_wccks', self.user, f'{ts}')
        return True, today_str

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
        input_text = self.sender.input(120000, 10000, False)
        if input_text in ('q', 'Q'):
            self.sender.reply("✅ 已为你取消本次批量登录操作")
            return
        elif input_text is None:
            self.sender.reply("⏰ 操作已超时，本次批量登录已退出")
            return
        accounts_list = self._parse_accounts(input_text)
        if not accounts_list:
            self.sender.reply("❌ 未检测到有效账号，请确认：\n1）每行仅包含一个账号\n2）使用「手机号#密码」格式，例如：13800138000#abc123")
            return

        success_count = 0
        fail_count = 0
        results = []

        for idx, acc in enumerate(accounts_list, 1):
            self.sender.reply(f"🔄 正在登录第 {idx}/{len(accounts_list)} 个账号，请稍候…")

            self.phone = acc['phone']
            plaintext1 = acc['password']
            self.original_password = plaintext1
            plaintext1.encode()

            try:
                self.passwd = encrypt_password(plaintext1)
                if self.get_session() and self.get_info():
                    ql_value = f"{self.phone}#{self.original_password}"
                    is_new, sqsj_val = self._save_account_data(ql_value)
                    if not is_new:
                        try:
                            Addenvs(osname=dd_wc_osname, value=ql_value, account=self.account, name=self.name, auth_time=sqsj_val)
                            results.append(f"✅ {self.name} ({self.mask_phone(self.phone)}) 已更新并提交青龙")
                        except Exception as e:
                            results.append(f"✅ {self.name} ({self.mask_phone(self.phone)}) 已更新但青龙提交失败")
                            print(f"青龙提交错误: {str(e)}")
                        success_count += 1
                        continue
                    success_count += 1
                    results.append(f"✅ {self.name} ({self.mask_phone(self.phone)}) 登录成功，请先授权")
                else:
                    fail_count += 1
                    results.append(f"❌ {acc['phone'][:3]}**** {'登录失败' if self.get_session() else '获取session失败'}")
            except Exception as e:
                fail_count += 1
                results.append(f"❌ {acc['phone'][:3]}**** 异常: {str(e)}")
            time.sleep(0.3)
        result_msg = f"===== 批量登录结果 =====\n✅ 登录成功：{success_count} 个\n❌ 登录失败：{fail_count} 个\n======================\n"
        result_msg += "\n".join(results) + "\n======================\n💡 发送「望潮管理」可对账号进行管理"
        self.sender.reply(result_msg)

    def zh_login(self):
        self.sender.reply(self._get_login_tips(is_batch=False))
        ck = self.sender.input(120000, 1000, False)
        if ck in ('q', 'Q'):
            self.sender.reply("✅ 已为你取消本次登录操作")
            return
        elif ck is None:
            self.sender.reply('⏰ 操作已超时，本次登录已退出')
            return

        elif '#' in ck:
            self.phone, plaintext1 = ck.split('#', 1)
            self.original_password = plaintext1
            try:
                self.passwd = encrypt_password(plaintext1)
            except ValueError:
                print("公钥加载失败")
            try:
                if self.get_session() and self.get_info():
                    ql_value = f"{self.phone}#{self.original_password}" if hasattr(self, 'original_password') else self.session
                    is_new, sqsj_val = self._save_account_data(ql_value)
                    try:
                        if sqsj_val > today_time:
                            Addenvs(osname=dd_wc_osname, value=ql_value, account=self.account, name=self.name, auth_time=sqsj_val)
                        msg = f'{self.name}>>>🔔{"更新成功" if not is_new else "登录成功"}!发送【望潮管理】对账号进行管理!'
                        self.sender.reply(msg)
                    except:
                        self.sender.reply(f'{self.name}>>>🔔{"更新成功" if not is_new else "登录成功"}!青龙提交失败，请稍后重试')
                else:
                    self.sender.reply(f'获取ck错误：{self.get_session()}')
            except Exception as e:
                self.sender.reply(f'{self.name}登录错误>>>{e}')
        else:
            self.sender.reply('❌ 输入格式有误，请使用「手机号#密码」格式重新发送')

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
        ts = sg.bucketGet('dd_wccks', self.user)
        if ts == '' or ts == '{}':
            self.sender.reply("🔔望潮系统未查询到您的信息! 请先登录! ")
        else:
            ts = _sg_literal(ts)
            account_count = len(ts)
            n = 0
            id_dict = {}
            zhszt = {}
            msg = '========望潮管理========\n'
            msg += f'[0] 🎯 一键批量授权所有账号\n'
            msg += f'[00] 🆕 一键批量授权过期账号\n'
            batch_size = 20
            batch_count = 0
            current_batch_msg = ''

            for k, y in ts.items():
                n += 1
                id_dict[n] = {'usid': k, 'name': y['name'], 'ck': y['ck'], 'sqsj': y['sqsj']}

                if y['sqsj'] <= datetime.now().strftime("%Y-%m-%d"):
                    sqsj = '已过期'
                    zhzt = '已过期'
                else:
                    sqsj = '有效'
                    zhzt = '✅有效'

                display_name = self.get_display_name(y)
                current_batch_msg += f'{n}、{display_name}\n账号状态: {zhzt}\n授权时间: ⏰{y["sqsj"]}({sqsj})\n====================\n'
                zhszt[n] = {'zhzt': zhzt}
                if n % batch_size == 0 or n == account_count:
                    batch_count += 1
                    batch_msg = (msg if batch_count == 1 else '') + current_batch_msg
                    if n < account_count:
                        batch_msg += f'\n[第 {batch_count} 批，共 {n}/{account_count} 个账号]\n'
                        self.sender.reply(batch_msg)
                        current_batch_msg = ''
                    else:
                        self.sender.reply(batch_msg + '回复序号选择账号,退出【q】！')
            xz = self.sender.listen(60000)
            xz_list = []
            for k, y in id_dict.items():
                xz_list.append(k)
            xz_list.append(0)
            if xz == 'q' or xz == 'Q':
                self.sender.reply("退出！")
            elif xz is None:
                self.sender.reply(f'超时退出！')
            elif xz == '00':
                self.batch_auth_expired_accounts(ts)
            else:
                try:
                    xz_int = int(xz)
                    if xz_int == 0:
                        self.batch_user_auth(ts)
                    elif xz_int in xz_list:
                        zh = id_dict[int(xz)]
                        self.account = zh['usid']
                        self.session = zh['ck']
                        self.name = zh['name']
                        self.sqsj = zh['sqsj']
                        self.gl_zh()
                    else:
                        self.sender.reply(f'输入有误，退出！')
                except:
                    self.sender.reply(f'输入有误，退出！')

    def gl_zh(self):
        msg = f'========账号管理========\n账号: {self.name}\n1、账号授权\n2、删除账号\n=====================\n回复序号,退出【q】！'
        self.sender.reply(msg)
        zh = self.sender.listen(60000)
        if zh == 'q' or zh == 'Q':
            self.sender.reply("退出！")
        elif zh is None:
            self.sender.reply(f'超时退出！')
        elif zh == '1':
            self.dssq()
        elif zh == '2':
            self.del_zh()
        else:
            self.sender.reply(f'输入有误!!')

    def batch_user_auth(self, ts):
        return True

    def batch_auth_expired_accounts(self, ts):
        try:
            today_time = datetime.now().strftime("%Y-%m-%d")
            expired_accounts = []

            for k, y in ts.items():
                if y['sqsj'] <= today_time:
                    expired_accounts.append({
                        'account': k,
                        'name': y['name'],
                        'ck': y['ck'],
                        'ql_value': y.get('ql_value', y['ck']),
                        'sqsj': y['sqsj']
                    })

            if not expired_accounts:
                self.sender.reply("✅ 当前没有需要授权的过期账号！")
                return

            sqje = '2099-12-31' or '6.6'
            sqsj = '2099-12-31' or '30'
            wxzsm, use_ma_pay, ma_pay_config = get_payment_config()
            wccoin = sg.bucketGet('dd_wcconfig', 'wccoin') or '0'

            if not wxzsm and not use_ma_pay and (not wccoin or int(wccoin) <= 0):
                self.sender.reply('❌ 管理员还未配置二维码、在线处理或积分支付!')
                return

            account_list = f"""=====批量授权过期账号=====
📊 过期账号数量: {len(expired_accounts)}个
💰 单价: {sqje}元/月

📋 过期账号列表:
"""
            for idx, acc in enumerate(expired_accounts, 1):
                display_name = self.get_display_name(acc)
                account_list += f"{idx}、{display_name} (授权过期: {acc['sqsj']})\n"

            account_list += """=====================
请输入授权月数(如: 1 表示授权1个月)
回复"q"退出操作
====================="""

            self.sender.reply(account_list)
            months_input = self.sender.listen(60000)

            if months_input == 'q' or months_input == 'Q':
                self.sender.reply("✅ 已取消授权")
                return
            elif months_input is None:
                self.sender.reply("⏰ 操作超时,已退出")
                return

            try:
                months = int(months_input)
                if months <= 0:
                    self.sender.reply("❌ 授权月数必须大于0")
                    return
            except:
                self.sender.reply("❌ 请输入正确的数字")
                return

            total_money = float(sqje) * months * len(expired_accounts)
            total_money_str = f"{total_money:.2f}"
            total_days = int(sqsj) * months

            if float(sqje) == 0:
                success_count = 0
                for acc in expired_accounts:
                    try:
                        datetime.now().strftime("%Y-%m-%d")
                        new_sqsj_date = datetime.now() + timedelta(days=int(sqsj) * months)
                        new_sqsj = new_sqsj_date.strftime("%Y-%m-%d")

                        ts[acc['account']] = {
                            'name': acc['name'],
                            'ck': acc['ck'],
                            'ql_value': acc['ql_value'],
                            'sqsj': new_sqsj
                        }

                        try:
                            Addenvs(
                                osname=dd_wc_osname,
                                value=acc['ql_value'],
                                account=acc['account'],
                                name=acc['name'],
                                auth_time=new_sqsj,
                                user_id=self.user
                            )
                        except Exception as e:
                            pass

                        success_count += 1
                    except:
                        continue

                sg.bucketSet('dd_wccks', self.user, f'{ts}')

                msg = f"""=====授权成功=====
🎫 商品: 望潮批量授权过期账号
💰 支付方式: 免费授权
📊 过期账号数量: {len(expired_accounts)}个
⏰ 授权时长: {months}月/每个账号 ({total_days}天/每个账号)
📊 成功: {success_count}/{len(expired_accounts)}个账号
✅ 已提交青龙
=================="""
                self.sender.reply(msg)
                return

            pay_menu = f"""=====批量授权过期账号=====
📊 过期账号数量: {len(expired_accounts)}个
⏰ 授权时长: {months}月/每个账号 ({total_days}天/每个账号)
💰 单价: {sqje}元/月
💰 总金额: {total_money}元
=====================
=====选择支付方式===="""

            option_num = 1
            options_map = {}

            if wxzsm:
                pay_menu += f"""
{option_num}️⃣ 微信支付
   💰 {total_money}元"""
                options_map[str(option_num)] = 'wechat'
                option_num += 1

            if use_ma_pay:
                pay_menu += f"""
{option_num}️⃣ 在线处理
   💰 {total_money}元"""
                options_map[str(option_num)] = 'ma'
                option_num += 1

            if wccoin and int(wccoin) > 0:
                need_coin = int(wccoin) * months * len(expired_accounts)
                usercoin = sg.bucketGet('dd_sign_points', self.user) or '0'
                pay_menu += f"""
{option_num}️⃣ 积分支付
   🎯 {need_coin}积分
   💫 当前积分: {usercoin}"""
                options_map[str(option_num)] = 'points'
                option_num += 1

            pay_menu += """
------------------
回复数字选择方式
回复"q"退出操作
=================="""

            self.sender.reply(pay_menu)
            choice = self.sender.listen(60000)

            if choice == 'q' or choice == 'Q':
                self.sender.reply("✅ 已取消授权")
                return
            elif choice is None:
                self.sender.reply("⏰ 操作超时,已退出")
                return

            selected_pay = options_map.get(choice)

            if selected_pay == 'wechat' and wxzsm:
                status = False
                if status == "True" or status or status == "true":
                    self.sender.reply("🔔目前有其他用户正在付款，请稍后再试！！")
                    return

                self.sender.replyImage(wxzsm)
                self.sender.reply(f"""=====微信扫在线处理====
🎫 商品: 望潮批量授权过期账号
📊 账号数量: {len(expired_accounts)}个
⏰ 时长: {months}月/每个账号
💰 总金额: {total_money}元
------------------
请使用微信扫在线处理
回复"q"取消支付
==================""")

                waitPay = False

                if waitPay == 'q':
                    self.sender.reply("✅ 已取消支付")
                    return

                if isinstance(waitPay, str):
                    waitPay = json.loads(waitPay)

                Time = waitPay['Time']
                userName = waitPay['FromName']
                Money = waitPay['Money']
                waitPay['Type']

                if float(Money) >= float(total_money):
                    success_count = 0
                    for acc in expired_accounts:
                        try:
                            datetime.now().strftime("%Y-%m-%d")
                            new_sqsj_date = datetime.now() + timedelta(days=int(sqsj) * months)
                            new_sqsj = new_sqsj_date.strftime("%Y-%m-%d")

                            ts[acc['account']] = {
                                'name': acc['name'],
                                'ck': acc['ck'],
                                'ql_value': acc['ql_value'],
                                'sqsj': new_sqsj
                            }

                            try:
                                Addenvs(osname=dd_wc_osname, value=acc['ql_value'], account=acc['account'],
                                       name=acc['name'], auth_time=new_sqsj)
                            except Exception as e:
                                pass

                            success_count += 1
                        except:
                            continue

                    sg.bucketSet('dd_wccks', self.user, f'{ts}')

                    msg = f"""=====支付成功=====
🎫 商品: 望潮批量授权过期账号
💰 金额: {Money}元
📊 成功: {success_count}/{len(expired_accounts)}个账号
⏰ 时间: {Time}
👤 付款人: {userName}
✅ 已提交青龙
=================="""
                    self.sender.reply(msg)
                else:
                    self.sender.reply(f"""=====支付金额错误=====
💰 应付: {total_money}元
💳 实付: {Money}元
👤 付款人: {userName}

❗ 请稍后核对支付记录！
==================""")

            elif selected_pay == 'ma' and use_ma_pay:
                out_trade_no = f"WCEXP{int(time.time())}{self.user}"

                params = {
                    'pid': ma_pay_config['pid'],
                    'type': ma_pay_config['type'].split(',')[0],
                    'out_trade_no': out_trade_no,
                    'name': f"{senderID}-望潮批量授权过期账号-{str(total_money)}",
                    'money': str(total_money),
                    'notify_url': ma_pay_config['notify_url'],
                    'return_url': ma_pay_config['return_url'],
                    'param': self.user
                }
                params = {k: v for k, v in params.items() if v}
                sorted_params = dict(sorted(params.items(), key=lambda x: x[0]))
                sign_str = "&".join([f"{k}={v}" for k, v in sorted_params.items()])
                sign = hashlib.md5((sign_str + ma_pay_config['key']).encode()).hexdigest().lower()

                params['sign'] = sign
                params['sign_type'] = 'MD5'

                gateway = ma_pay_config['gateway']
                if gateway.endswith('/'):
                    gateway = gateway[:-1]
                mapi_url = f"{gateway}/mapi.php"

                try:
                    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                    response = requests.post(mapi_url, data=params, headers=headers, timeout=10)

                    if response.status_code != 200:
                        self.sender.reply(f"❌ 创建支付订单失败，HTTP状态码: {response.status_code}")
                        return

                    try:
                        result = response.json()
                    except:
                        self.sender.reply("❌ 创建支付订单失败，返回数据格式错误")
                        return

                    code = result.get('code', 0)
                    msg = result.get('msg', '未知状态')

                    if code == 1:
                        payurl = result.get('payurl', '')
                        if not payurl:
                            self.sender.reply("❌ 未获取到支付链接")
                            return

                        qrcode_url = generate_qrcode(payurl)
                        pay_type = ma_pay_config['type'].split(',')[0] if ma_pay_config.get('type') else 'alipay'

                        if qrcode_url:
                            send_qrcode_image(self.sender, qrcode_url, pay_type)
                        else:
                            self.sender.reply(f"""=====在线处理=====
🎫 商品: 望潮批量授权过期账号
💰 金额: {total_money}元
📊 账号数量: {len(expired_accounts)}个
⏰ 有效期: 5分钟
------------------
二维码生成失败，请点击链接完成支付:
{payurl}
==================""")
                    else:
                        if "没有找到可用支付账号" in msg or "没有找到可用的" in msg:
                            self.sender.reply(f"❌ 在线处理暂不可用({msg})")
                        else:
                            self.sender.reply(f"❌ 创建订单失败: {msg}")
                        return

                    for i in range(60):
                        check_url = gateway
                        if check_url.endswith('/'):
                            check_url = check_url[:-1]
                        if '/xpay/epay/api.php' not in check_url:
                            check_url = f"{check_url}/xpay/epay/api.php"

                        check_params = {
                            'act': 'order',
                            'pid': ma_pay_config['pid'],
                            'key': ma_pay_config['key'],
                            'out_trade_no': out_trade_no
                        }

                        try:
                            check_resp = requests.get(check_url, params=check_params, timeout=10)
                            check_result = check_resp.json()

                            if check_result.get('code') == 1 and check_result.get('status') == 1:
                                success_count = 0
                                for acc in expired_accounts:
                                    try:
                                        datetime.now().strftime("%Y-%m-%d")
                                        new_sqsj_date = datetime.now() + timedelta(days=int(sqsj) * months)
                                        new_sqsj = new_sqsj_date.strftime("%Y-%m-%d")

                                        ts[acc['account']] = {
                                            'name': acc['name'],
                                            'ck': acc['ck'],
                                            'ql_value': acc['ql_value'],
                                            'sqsj': new_sqsj
                                        }

                                        try:
                                            Addenvs(osname=dd_wc_osname, value=acc['ql_value'], account=acc['account'],
                                                   name=acc['name'], auth_time=new_sqsj, user_id=self.user)
                                        except:
                                            pass

                                        success_count += 1
                                    except:
                                        continue

                                sg.bucketSet('dd_wccks', self.user, f'{ts}')

                                self.sender.reply(f"""=====支付成功=====
🎫 商品: 望潮批量授权过期账号
💰 金额: {total_money}元
📊 成功: {success_count}/{len(expired_accounts)}个账号
⏰ 授权时长: {months}月/每个账号
✅ 已提交青龙
==================""")
                                return
                        except Exception as e:
                            print(f"查询订单状态出错: {str(e)}")

                        result = self.sender.listen(5000)
                        if result == 'q' or result == 'Q':
                            self.sender.reply("✅ 已取消支付")
                            return

                    self.sender.reply("❌ 支付超时,请重新发起支付!")
                    return
                except Exception as e:
                    self.sender.reply(f"❌ 支付请求失败: {str(e)}")
                    return

            elif selected_pay == 'points' and wccoin and int(wccoin) > 0:
                need_coin = int(wccoin) * months * len(expired_accounts)
                usercoin = sg.bucketGet('dd_sign_points', self.user) or '0'

                if int(usercoin) < need_coin:
                    self.sender.reply(f"❌ 积分不足\n当前积分: {usercoin}\n需要积分: {need_coin}")
                    return

                new_balance = int(usercoin) - need_coin
                sg.bucketSet('dd_sign_points', self.user, str(new_balance))

                success_count = 0
                for acc in expired_accounts:
                    try:
                        datetime.now().strftime("%Y-%m-%d")
                        new_sqsj_date = datetime.now() + timedelta(days=int(sqsj) * months)
                        new_sqsj = new_sqsj_date.strftime("%Y-%m-%d")

                        ts[acc['account']] = {
                            'name': acc['name'],
                            'ck': acc['ck'],
                            'ql_value': acc['ql_value'],
                            'sqsj': new_sqsj
                        }

                        try:
                            Addenvs(
                                osname=dd_wc_osname,
                                value=acc['ql_value'],
                                account=acc['account'],
                                name=acc['name'],
                                auth_time=new_sqsj,
                                user_id=self.user
                            )
                        except Exception as e:
                            pass

                        success_count += 1
                    except:
                        continue

                sg.bucketSet('dd_wccks', self.user, f'{ts}')

                msg = f"""=====支付成功=====
🎫 商品: 望潮批量授权过期账号
💰 支付方式: 积分支付
💫 消耗积分: {need_coin}
💰 剩余积分: {new_balance}
📊 成功: {success_count}/{len(expired_accounts)}个账号
✅ 已提交青龙
=================="""
                self.sender.reply(msg)
            else:
                self.sender.reply("❌ 输入无效")

        except Exception as e:
            self.sender.reply(f"❌ 批量授权过期账号处理失败: {str(e)}")


    def dssq(self):
        try:
            wxzsm = sg.bucketGet('dd_wcconfig', 'wxzsm')
            sqsj = '2099-12-31' or '30'
            sqje = '2099-12-31' or '1'
            wccoin = sg.bucketGet('dd_wcconfig', 'wccoin') or '0'

            self.sender.reply("请输入授权月数(如: 1 表示授权1个月):")
            months_input = self.sender.listen(60000)

            if months_input == 'q' or months_input == 'Q':
                self.sender.reply("✅ 已取消授权")
                return
            elif months_input is None:
                self.sender.reply("⏰ 操作超时,已退出")
                return

            try:
                months = int(months_input)
                if months <= 0:
                    self.sender.reply("❌ 授权月数必须大于0")
                    return
            except:
                self.sender.reply("❌ 请输入正确的数字")
                return

            total_days = int(sqsj) * months
            total_money = float(sqje) * months
            total_money_str = f"{total_money:.2f}"
            need_coin_single = int(wccoin) * months if wccoin and int(wccoin) > 0 else 0

            if float(sqje) == 0:
                dqsj = datetime.now().strftime("%Y-%m-%d")
                if self.sqsj > dqsj:
                    self.sqsj = datetime.strptime(self.sqsj, "%Y-%m-%d")
                    new_sqsj = self.sqsj + timedelta(days=total_days)
                    new_sqsj = new_sqsj.strftime("%Y-%m-%d")
                else:
                    sj = datetime.now()
                    new_sqsj = sj + timedelta(days=total_days)
                    new_sqsj = new_sqsj.strftime("%Y-%m-%d")

                ts = sg.bucketGet('dd_wccks', self.user)
                ts = _sg_literal(ts)
                for k, y in ts.items():
                    if self.account == k:
                        ql_value = y.get('ql_value', self.session)
                        ts[f'{k}'] = {'name': self.name, 'ck': self.session, 'ql_value': ql_value, 'sqsj': new_sqsj}
                        sg.bucketSet('dd_wccks', self.user, f'{ts}')
                        ql_success = False
                        try:
                            Addenvs(osname=dd_wc_osname, value=ql_value, account=self.account, name=self.name, auth_time=new_sqsj)
                            ql_success = True
                        except Exception as e:
                            print(f'单账号免费授权提交青龙失败 - 账号: {self.account}, 错误: {str(e)}')

                        status_text = "✅ 已提交青龙" if ql_success else "⚠️ 青龙提交失败，请检查青龙配置或网络"
                        msg = f"""=====授权成功=====
🎫 商品: 望潮授权
💰 支付方式: 免费授权
⏰ 授权时长: {months}月 ({total_days}天)
👤 账号: {self.name}
📅 到期时间: {new_sqsj}
{status_text}
=================="""
                        self.sender.reply(msg)
                        return
                    else:
                        continue
                return

            wxzsm, use_ma_pay, ma_pay_config = get_payment_config()

            if not wxzsm and not use_ma_pay and (not wccoin or int(wccoin) <= 0):
                self.sender.reply('❌ 管理员还未配置二维码、在线处理或积分支付!')
                return

            confirm_msg = f"""=====授权确认=====
👤 账号: {self.name}
⏰ 授权时长: {months}月 ({total_days}天)
💰 总金额: {total_money}元
------------------"""

            pay_menu = confirm_msg + f"""
=====选择支付方式===="""

            option_num = 1
            options_map = {}

            if wxzsm:
                pay_menu += f"""
{option_num}️⃣ 微信支付
   💰 {total_money}元"""
                options_map[str(option_num)] = 'wechat'
                option_num += 1

            if use_ma_pay:
                pay_menu += f"""
{option_num}️⃣ 在线处理
   💰 {total_money}元"""
                options_map[str(option_num)] = 'ma'
                option_num += 1

            if wccoin and int(wccoin) > 0:
                usercoin = sg.bucketGet('dd_sign_points', self.user) or '0'
                pay_menu += f"""
{option_num}️⃣ 积分支付
   🎯 {need_coin_single}积分
   💫 当前积分: {usercoin}"""
                options_map[str(option_num)] = 'points'
                option_num += 1

            pay_menu += """
------------------
回复数字选择方式
回复"q"退出操作
=================="""

            self.sender.reply(pay_menu)

            choice = self.sender.listen(60000)
            if choice == 'q' or choice == 'Q':
                self.sender.reply("✅ 已取消支付")
                return
            elif choice is None:
                self.sender.reply("⏰ 操作超时,已退出")
                return

            selected_pay = options_map.get(choice)

            if selected_pay == 'wechat':
                status = False
                if status == "True" or status or status == "true":
                    self.sender.reply("🔔目前有其他用户正在付款，请稍后再试！！")
                else:
                    self.sender.replyImage(wxzsm)
                    self.sender.reply(
                        f"""=====微信扫在线处理====
🎫 商品: 望潮授权
👤 账号: {self.name}
⏰ 授权时长: {months}月 ({total_days}天)
💰 应付金额: {total_money_str}元
------------------
请在120s内使用wx扫码付款
如支付金额不足，授权天数会按实际金额等比例折算
发起支付期间不要发其他无关内容！退出回复'q'退出！
==================""")
                    waitPay = False
                    if waitPay == 'q':
                        self.sender.reply("✅ 已取消支付")
                    elif isinstance(waitPay, dict) or isinstance(waitPay, str):
                        if isinstance(waitPay, str):
                            waitPay = json.loads(waitPay)
                        Time = waitPay['Time']
                        userName = waitPay['FromName']
                        Money = waitPay['Money']
                        Type = waitPay['Type']
                        dqsj = datetime.now().strftime("%Y-%m-%d")
                        if self.sqsj > dqsj:
                            self.sqsj = datetime.strptime(self.sqsj, "%Y-%m-%d")
                            new_sqsj = self.sqsj + timedelta(days=int(float(Money) / float(sqje) * int(sqsj)))
                            new_sqsj = new_sqsj.strftime("%Y-%m-%d")
                        else:
                            sj = datetime.now()
                            new_sqsj = sj + timedelta(days=int(float(Money) / float(sqje) * int(sqsj)))
                            new_sqsj = new_sqsj.strftime("%Y-%m-%d")
                        ts = sg.bucketGet('dd_wccks', self.user)
                        ts = _sg_literal(ts)
                        for k, y in ts.items():
                            if self.account == k:
                                ql_value = y.get('ql_value', self.session)
                                ts[f'{k}'] = {'name': self.name, 'ck': self.session, 'ql_value': ql_value, 'sqsj': new_sqsj}
                                sg.bucketSet('dd_wccks', self.user, f'{ts}')
                                ql_success = False
                                try:
                                    Addenvs(osname=dd_wc_osname, value=ql_value, account=self.account, name=self.name, auth_time=new_sqsj)
                                    ql_success = True
                                except Exception as e:
                                    print(f'单账号付费授权提交青龙失败 - 账号: {self.account}, 错误: {str(e)}')

                                status_text = "✅ 已提交青龙" if ql_success else "⚠️ 青龙提交失败，请检查青龙配置或网络"
                                msg = f'当前用户: {self.user}\n付款时间: {Time}\n付款来源: {Type}\n付款用户: {userName}\n付款金额: {Money}\n授权用户: {self.name}\n授权id: {self.account}\n授权天数: {int(float(Money) / float(sqje) * int(sqsj))}天\n到期时间: {new_sqsj}\n{status_text}'
                                self.sender.reply(msg)
                                notify = sg.bucketGet('dd_wcconfig', 'notify')
                                if notify == '':
                                    pass
                                else:
                                    tsqd = notify.split(',')
                                    sg.notifyMasters(msg, tsqd)
                                return
                            else:
                                continue
                    else:
                        self.sender.reply("❌ 支付失败或取消")
                        return
                return

            elif selected_pay == 'ma' and use_ma_pay:
                pay_money = float(f"{total_money:.2f}")
                selected_type = ma_pay_config['type'].split(',')[0] if ma_pay_config.get('type') else 'alipay'

                out_trade_no = f"WC{int(time.time())}{self.user}"

                params = {
                    'pid': ma_pay_config['pid'],
                    'type': selected_type,
                    'out_trade_no': out_trade_no,
                    'name': f"{senderID}-望潮授权-{str(pay_money)}",
                    'money': str(pay_money),
                    'notify_url': ma_pay_config['notify_url'],
                    'return_url': ma_pay_config['return_url'],
                    'param': self.user
                }
                params = {k: v for k, v in params.items() if v}
                sorted_params = dict(sorted(params.items(), key=lambda x: x[0]))
                sign_str = "&".join([f"{k}={v}" for k, v in sorted_params.items()])
                sign = hashlib.md5((sign_str + ma_pay_config['key']).encode()).hexdigest().lower()

                params['sign'] = sign
                params['sign_type'] = 'MD5'

                gateway = ma_pay_config['gateway']
                if gateway.endswith('/'):
                    gateway = gateway[:-1]
                mapi_url = f"{gateway}/mapi.php"

                try:
                    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                    response = requests.post(mapi_url, data=params, headers=headers, timeout=10)

                    if response.status_code != 200:
                        self.sender.reply(f"❌ 创建支付订单失败，HTTP状态码: {response.status_code}")
                        return

                    try:
                        result = response.json()
                    except:
                        self.sender.reply("❌ 创建支付订单失败，返回数据格式错误")
                        return

                    code = result.get('code', 0)
                    msg = result.get('msg', '未知状态')

                    if code == 1:
                        payurl = result.get('payurl', '')
                        if not payurl:
                            self.sender.reply("❌ 未获取到支付链接")
                            return

                        qrcode_url = generate_qrcode(payurl)
                        if qrcode_url:
                            send_qrcode_image(self.sender, qrcode_url, selected_type)
                        else:
                            self.sender.reply(f"""=====在线处理=====
🎫 商品: 望潮授权
💰 金额: {total_money}元
⏰ 授权时长: {months}月 ({total_days}天)
⏰ 有效期: 5分钟
------------------
二维码生成失败，请点击链接完成支付:
{payurl}
==================""")
                    else:
                        if "没有找到可用支付账号" in msg or "没有找到可用的" in msg:
                            self.sender.reply(f"❌ 在线处理暂不可用({msg})")
                        else:
                            self.sender.reply(f"❌ 创建订单失败: {msg}")
                        return

                    for i in range(60):
                        check_url = gateway
                        if check_url.endswith('/'):
                            check_url = check_url[:-1]
                        if '/xpay/epay/api.php' not in check_url:
                            check_url = f"{check_url}/xpay/epay/api.php"

                        check_params = {
                            'act': 'order',
                            'pid': ma_pay_config['pid'],
                            'key': ma_pay_config['key'],
                            'out_trade_no': out_trade_no
                        }

                        try:
                            check_resp = requests.get(check_url, params=check_params, timeout=10)
                            check_result = check_resp.json()

                            if check_result.get('code') == 1 and check_result.get('status') == 1:
                                dqsj = datetime.now().strftime("%Y-%m-%d")
                                auth_days = total_days
                                if self.sqsj > dqsj:
                                    self.sqsj = datetime.strptime(self.sqsj, "%Y-%m-%d")
                                    new_sqsj = self.sqsj + timedelta(days=auth_days)
                                    new_sqsj = new_sqsj.strftime("%Y-%m-%d")
                                else:
                                    sj = datetime.now()
                                    new_sqsj = sj + timedelta(days=auth_days)
                                    new_sqsj = new_sqsj.strftime("%Y-%m-%d")

                                ts = sg.bucketGet('dd_wccks', self.user)
                                ts = _sg_literal(ts)
                                for k, y in ts.items():
                                    if self.account == k:
                                        ql_value = y.get('ql_value', self.session)
                                        ts[f'{k}'] = {'name': self.name, 'ck': self.session, 'ql_value': ql_value, 'sqsj': new_sqsj}
                                        sg.bucketSet('dd_wccks', self.user, f'{ts}')

                                        success_count = 0
                                        try:
                                            if Addenvs(osname=dd_wc_osname, value=ql_value, account=self.account, name=self.name, auth_time=new_sqsj):
                                                success_count = 1
                                        except:
                                            pass

                                        status_text = "✅ 已提交青龙" if success_count > 0 else "⚠️ 青龙提交失败，请检查青龙配置或网络"
                                        self.sender.reply(f"""=====支付成功=====
🎫 商品: 望潮授权
💰 金额: {pay_money}元
⏰ 授权时长: {months}月 ({total_days}天)
{status_text}
==================""")
                                        return
                                return
                        except Exception as e:
                            print(f"查询订单状态出错: {str(e)}")

                        result = self.sender.listen(5000)
                        if result == 'q' or result == 'Q':
                            self.sender.reply("✅ 已取消支付")
                            return

                    self.sender.reply("❌ 支付超时,请重新发起支付!")
                    return
                except Exception as e:
                    self.sender.reply(f"❌ 支付请求失败: {str(e)}")
                    return

            elif selected_pay == 'points' and wccoin and int(wccoin) > 0:
                need_coin = need_coin_single
                usercoin = sg.bucketGet('dd_sign_points', self.user) or '0'

                if int(usercoin) < need_coin:
                    self.sender.reply(f"❌ 积分不足\n当前积分: {usercoin}\n需要积分: {need_coin}")
                    return

                points_confirm_msg = f"""=====积分支付确认=====
👤 账号: {self.name}
⏰ 授权时长: {months}月 ({total_days}天)
💫 消耗积分: {need_coin}
💫 当前积分: {usercoin}
------------------
回复 "y" 确认授权
回复 "q" 取消
=================="""
                self.sender.reply(points_confirm_msg)
                confirm = self.sender.listen(60000)
                if confirm in ['q', 'Q']:
                    self.sender.reply("✅ 已取消授权")
                    return
                if confirm is None or str(confirm).strip().lower() != 'y':
                    self.sender.reply("⏰ 操作超时或无效，已取消授权")
                    return

                try:
                    new_balance = int(usercoin) - need_coin
                    sg.bucketSet('dd_sign_points', self.user, str(new_balance))

                    dqsj = datetime.now().strftime("%Y-%m-%d")
                    if self.sqsj > dqsj:
                        self.sqsj = datetime.strptime(self.sqsj, "%Y-%m-%d")
                        new_sqsj = self.sqsj + timedelta(days=total_days)
                        new_sqsj = new_sqsj.strftime("%Y-%m-%d")
                    else:
                        sj = datetime.now()
                        new_sqsj = sj + timedelta(days=total_days)
                        new_sqsj = new_sqsj.strftime("%Y-%m-%d")

                    ts = sg.bucketGet('dd_wccks', self.user)
                    ts = _sg_literal(ts)
                    for k, y in ts.items():
                        if self.account == k:
                            ql_value = y.get('ql_value', self.session)
                            ts[f'{k}'] = {'name': self.name, 'ck': self.session, 'ql_value': ql_value, 'sqsj': new_sqsj}
                            sg.bucketSet('dd_wccks', self.user, f'{ts}')
                            try:
                                Addenvs(osname=dd_wc_osname, value=ql_value, account=self.account, name=self.name, auth_time=new_sqsj)
                            except:
                                pass

                            msg = f"""=====支付成功=====
🎫 商品: 望潮授权
💰 支付方式: 积分支付
💫 消耗积分: {need_coin}
💰 剩余积分: {new_balance}
⏰ 授权时长: {months}月 ({total_days}天)
👤 账号: {self.name}
📅 到期时间: {new_sqsj}
=================="""
                            self.sender.reply(msg)
                            return
                        else:
                            continue
                except Exception as e:
                    self.sender.reply(f"❌ 积分支付处理失败: {str(e)}")
                    return

            else:
                self.sender.reply("❌ 输入无效")
                return
        except Exception as e:
            self.sender.reply(f"❌ 授权处理失败: {str(e)}")
            return

    def del_zh(self):
        self.sender.reply(f'是否删除账号【{self.name}】？(y/n)')
        zh = self.sender.listen(60000)
        if zh == 'n' or zh == 'N':
            self.sender.reply("退出！")

        elif zh is None:
            self.sender.reply(f'超时退出！')

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
            self.sender.reply(f'输入有误，退出！')

    def batch_delete_accounts(self):
        ts = sg.bucketGet('dd_wccks', self.user)
        if ts == '' or ts == '{}':
            self.sender.reply("🔔望潮系统未查询到您的信息! 请先登录! ")
            return

        ts = _sg_literal(ts)
        if not ts:
            self.sender.reply("❌ 未找到有效账号")
            return

        accounts = []
        for k, y in ts.items():
            accounts.append({
                'account': k,
                'name': y['name'],
                'ck': y['ck'],
                'ql_value': y.get('ql_value', y['ck']),
                'sqsj': y['sqsj']
            })

        if not accounts:
            self.sender.reply("❌ 未找到有效账号")
            return

        account_list = f"""=====批量删除账号=====
📊 账号数量: {len(accounts)}个

[0] 🎯 一键删除所有账号

=====账号列表====="""

        batch_size = 20
        batch_count = 0
        current_batch_msg = ''

        for idx, acc in enumerate(accounts, 1):
            display_name = self.get_display_name(acc)

            if acc['sqsj'] <= datetime.now().strftime("%Y-%m-%d"):
                sqsj_status = '已过期'
            else:
                sqsj_status = '有效'

            current_batch_msg += f"{idx}、{display_name}\n授权状态: {sqsj_status}\n授权时间: {acc['sqsj']}\n====================\n"

            if idx % batch_size == 0 or idx == len(accounts):
                batch_count += 1
                batch_msg = ''
                if batch_count == 1:
                    batch_msg = account_list + current_batch_msg
                else:
                    batch_msg = current_batch_msg

                if idx < len(accounts):
                    batch_msg += f'\n[第 {batch_count} 批，共 {idx}/{len(accounts)} 个账号]\n'
                    self.sender.reply(batch_msg)
                    current_batch_msg = ''
                else:
                    batch_msg += f'回复序号选择账号删除\n回复"0"一键删除所有账号\n回复"q"退出操作\n===================='
                    self.sender.reply(batch_msg)

        choice = self.sender.listen(60000)

        if choice == 'q' or choice == 'Q':
            self.sender.reply("✅ 已取消删除操作")
            return
        elif choice is None:
            self.sender.reply("⏰ 操作超时,已退出")
            return
        elif choice == '0':
            confirm_msg = f"""⚠️ 警告：即将删除所有账号！

📊 账号数量: {len(accounts)}个

此操作不可恢复！
确认删除请输入: yes
取消删除请输入: no
===================="""
            self.sender.reply(confirm_msg)
            confirm = self.sender.listen(60000)

            if confirm == 'yes' or confirm == 'YES' or confirm == 'Yes':
                success_count = 0
                failed_count = 0
                deleted_accounts = []

                for acc in accounts:
                    try:
                        account_id = acc['account']
                        account_name = acc['name']

                        if account_id in ts:
                            del ts[account_id]
                            deleted_accounts.append(account_name)

                        try:
                            qlid = allenvs(osname=dd_wc_osname, account=account_id)
                            if qlid:
                                delenvs(id=qlid)
                        except Exception as e:
                            print(f"删除青龙变量失败 - 账户: {account_name}, 错误: {str(e)}")

                        success_count += 1
                    except Exception as e:
                        print(f"删除账号失败 - 账户: {acc.get('name', '未知')}, 错误: {str(e)}")
                        failed_count += 1
                        continue

                sg.bucketSet('dd_wccks', self.user, f'{ts}')

                result_msg = f"""=====批量删除完成=====
📊 总账号数: {len(accounts)}个
✅ 成功删除: {success_count}个
❌ 删除失败: {failed_count}个
✅ 已同步删除青龙变量

已删除账号:"""

                for idx, name in enumerate(deleted_accounts[:10], 1):
                    result_msg += f"\n{idx}、{name}"

                if len(deleted_accounts) > 10:
                    result_msg += f"\n... 还有 {len(deleted_accounts) - 10} 个账号"

                result_msg += "\n===================="
                self.sender.reply(result_msg)
            elif confirm == 'no' or confirm == 'NO' or confirm == 'No':
                self.sender.reply("✅ 已取消删除操作")
                return
            else:
                self.sender.reply("❌ 输入有误，操作已取消")
                return
        else:
            try:
                choice_int = int(choice)
                if choice_int < 1 or choice_int > len(accounts):
                    self.sender.reply("❌ 序号超出范围，操作已取消")
                    return

                selected_acc = accounts[choice_int - 1]
                account_id = selected_acc['account']
                account_name = selected_acc['name']
                display_name = self.get_display_name(selected_acc)

                confirm_msg = f"""⚠️ 确认删除账号？

账号: {display_name}
授权时间: {selected_acc['sqsj']}

确认删除请输入: yes
取消删除请输入: no
===================="""
                self.sender.reply(confirm_msg)
                confirm = self.sender.listen(60000)

                if confirm == 'yes' or confirm == 'YES' or confirm == 'Yes':
                    try:
                        if account_id in ts:
                            del ts[account_id]
                            sg.bucketSet('dd_wccks', self.user, f'{ts}')

                        ql_success = False
                        try:
                            qlid = allenvs(osname=dd_wc_osname, account=account_id)
                            if qlid:
                                delenvs(id=qlid)
                                ql_success = True
                        except Exception as e:
                            print(f"删除青龙变量失败: {str(e)}")

                        result_msg = f"""=====删除成功=====
账号: {display_name}
✅ 本地数据已删除"""

                        if ql_success:
                            result_msg += "\n✅ 青龙变量已同步删除"
                        else:
                            result_msg += "\n⚠️ 青龙变量删除失败，请手动检查"

                        result_msg += "\n===================="
                        self.sender.reply(result_msg)
                    except Exception as e:
                        self.sender.reply(f"❌ 删除失败: {str(e)}")
                elif confirm == 'no' or confirm == 'NO' or confirm == 'No':
                    self.sender.reply("✅ 已取消删除操作")
                    return
                else:
                    self.sender.reply("❌ 输入有误，操作已取消")
                    return
            except ValueError:
                self.sender.reply("❌ 请输入正确的序号")
                return

    def query_single_account(self, account_id, account_data, query_proxy_api=None, max_retries=3):
        self.session = account_data['ck']
        self.account = account_id
        self.name = account_data['name']
        self.sqsj = account_data['sqsj']

        if account_data['sqsj'] <= datetime.now().strftime("%Y-%m-%d"):
            sqsj = '已过期'
        else:
            sqsj = '有效'

        for retry in range(max_retries):
            try:
                proxies = None
                if query_proxy_api:
                    proxies = get_query_proxy(query_proxy_api, silent=True)

                cjjl = self.get_cjjl(proxies=proxies)

                if isinstance(cjjl, tuple):
                    jrsy, bysy, xxsy = cjjl
                    return build_query_msg(account_data, sqsj, jrsy, bysy, xxsy)
                else:
                    error_str = str(cjjl)
                    if any(keyword in error_str for keyword in ['频繁', '稍后再试', '操作频繁', '接口频繁']):
                        if retry < max_retries - 1:
                            time.sleep(10)
                            continue
                        else:
                            return build_query_msg(account_data, sqsj, error_msg='⚠️ 接口繁忙，请稍后再试')

                    if any(keyword in error_str.lower() for keyword in ['timeout', 'timed out']) or 'Read timed out' in error_str:
                        if retry < max_retries - 1:
                            continue
                        else:
                            try:
                                if self.get_info() is not True:
                                    return build_query_msg(account_data, sqsj, error_msg='❌ 账户已失效，请重新登录！')
                            except:
                                pass
                            return build_query_msg(account_data, sqsj, error_msg='⚠️ 网络超时，请稍后再试')

                    if retry == max_retries - 1:
                        try:
                            if self.get_info() is not True:
                                return build_query_msg(account_data, sqsj, error_msg='❌ 账户已失效，请重新登录！')
                        except:
                            pass
                        return build_query_msg(account_data, sqsj, error_msg='⚠️ 查询失败，请稍后再试')

                    time.sleep(1)
                    continue

            except Exception as e:
                if retry == max_retries - 1:
                    try:
                        if self.get_info() is not True:
                            return build_query_msg(account_data, sqsj, error_msg='❌ 账户验证失败，请重新登录！')
                    except:
                        pass
                    return build_query_msg(account_data, sqsj, error_msg='⚠️ 查询异常，请稍后再试')
                time.sleep(1)
                continue
        return build_query_msg(account_data, sqsj, error_msg='⚠️ 查询失败，请稍后再试')

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
            msg += f'[0] 一键查询所有账号\n'

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

            msg += f'=====================\n'
            msg += f'回复序号选择账号,退出【q】！'
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
                self.sender.reply(f'超时退出！')
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
                self.sender.reply(f'输入有误，退出！')

    def get_signin_records(self, proxies=None):
        try:
            if not SIGNIN_Q:
                return []

            body_login = {
                "accountId": self.account,
                "sessionId": self.session,
                "q": SIGNIN_Q,
                "tenantCode": "xsb_wangchao",
            }
            try:
                resp_login = signin_post("/auth/userLogin", body_login, authorization="", proxies=proxies)
                if not isinstance(resp_login, dict):
                    return []
                token = resp_login.get("data", {}).get("token")
                if not token:
                    return []
            except Exception as e:
                return []

            lottery_login_body = {
                "accountId": self.account,
                "sessionId": self.session,
                "q": SIGNIN_LOTTERY_Q,
                "tenantCode": "xsb_wangchao",
            }
            try:
                lottery_login_resp = lottery_post("/api/auth/userLogin", "", lottery_login_body, proxies=proxies)
                if not isinstance(lottery_login_resp, dict):
                    return []
                lottery_data = lottery_login_resp.get("data") or {}
                lottery_token = lottery_data.get("token")
                x_token = lottery_data.get("xToken") or lottery_data.get("x_token") or None
                if not lottery_token:
                    return []
            except Exception as e:
                return []

            try:
                record_resp = lottery_get(
                    f"/activity/lottery/accountPrizeRecord/userPrizeRecord?activityId={SIGNIN_LOTTERY_ACTIVITY_ID}",
                    lottery_token,
                    x_token=x_token,
                    proxies=proxies
                )
                if not isinstance(record_resp, dict):
                    return []

                if record_resp.get("code") != 0 and record_resp.get("success") is not True:
                    message = record_resp.get("message", "")
                    if '频繁' in message or '稍后再试' in message:
                        return []
                    return []

                record_data = record_resp.get("data") or {}
                prize_list_raw = record_data.get("activityAccountPrizeVoList")

                if not isinstance(prize_list_raw, list):
                    return []

                signin_records = []
                current_time = datetime.now()

                sorted_prizes = sorted(prize_list_raw, key=lambda x: x.get("prizeRecordId", 0), reverse=True)

                for idx, prize in enumerate(sorted_prizes):
                    if not isinstance(prize, dict) or not (prize_name := prize.get("prizeName", "")):
                        continue
                    create_time = (prize.get("createTime") or prize.get("prizeTime") or prize.get("createDate") or
                                 prize.get("prizeDate") or prize.get("time") or "")
                    fallback_date = current_time - timedelta(days=idx)
                    date, formatted_time = parse_prize_time(create_time, fallback_date)
                    if date:
                        signin_records.append({'time': formatted_time, 'award': prize_name, 'date': date})

                return signin_records
            except Exception:
                return []
        except Exception:
            return []

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


    def wcpz(self):
        wxzsm = sg.bucketGet('dd_wcconfig', 'wxzsm')
        if wxzsm == '':
            pz1 = '未配置'
        else:
            pz1 = '已配置'

        sqje = '2099-12-31'
        if sqje == '':
            sqje = 1

        sqsj = '2099-12-31'
        if sqsj == '':
            sqsj = 30

        sdyx = sg.bucketGet('dd_wcconfig', 'sdyx')
        if sdyx == '':
            sdyx = 'false'

        notify = sg.bucketGet('dd_wcconfig', 'notify')
        if notify == '':
            notify = '未配置'
        else:
            notify = '已配置'

        wxpusher = sg.bucketGet('dd_wcconfig', 'wxpusher')
        if wxpusher == '':
            pz2 = '未配置'
        else:
            pz2 = '已配置'

        dlapi = sg.bucketGet('dd_wcconfig', 'dlapi')
        if dlapi == '':
            dlapi = '未配置'
        else:
            dlapi = '已配置'

        cxproxy = sg.bucketGet('dd_wcconfig', 'cxproxy')
        if cxproxy == '':
            cxproxy = '未配置'
        else:
            cxproxy = '已配置'

        msg = f'========望潮配置========\n1、赞赏码({pz1})\n2、授权金额({sqje}元)\n3、授权时间({sqsj}天)\n4、手动运行({sdyx})\n5、管理员通知({notify})\n6、WxPusher推送({pz2})\n7、抽奖代理api({dlapi})\n8、查询代理api({cxproxy})\n=====================\n回复序号,退出【q】！'
        self.sender.reply(msg)
        zh = self.sender.listen(60000)
        if zh == 'q' or zh == 'Q':
            self.sender.reply("退出！")
        elif zh is None:
            self.sender.reply(f'超时退出！')
        elif zh == '1':
            self.sender.reply('请发送您的wx机器人赞赏码:')
            pz = self.sender.listen(60000)
            if pz == 'q' or pz == 'Q':
                self.sender.reply("退出！")
            elif pz is None:
                self.sender.reply(f'超时退出！')
            else:
                self.sender.replyImage(pz)
                sg.bucketSet('dd_wcconfig', 'wxzsm', f'{pz}')
                self.sender.reply('赞赏码配置成功!')
        elif zh == '2':
            self.sender.reply('设置授权金额:')
            pz = self.sender.listen(60000)
            if pz == 'q' or pz == 'Q':
                self.sender.reply("退出！")
            elif pz is None:
                self.sender.reply(f'超时退出！')
            else:
                True
                self.sender.reply(f'授权金额配置成功: {pz}元')
        elif zh == '3':
            self.sender.reply('设置授权时间:')
            pz = self.sender.listen(60000)
            if pz == 'q' or pz == 'Q':
                self.sender.reply("退出！")
            elif pz is None:
                self.sender.reply(f'超时退出！')
            else:
                True
                self.sender.reply(f'授权时间配置成功: {pz}天')
        elif zh == '4':
            self.sender.reply('设置是否运行用户手动运行, 输入(true/false)')
            pz = self.sender.listen(60000)
            if pz == 'q' or pz == 'Q':
                self.sender.reply("退出！")
            elif pz is None:
                self.sender.reply(f'超时退出！')
            else:
                sg.bucketSet('dd_wcconfig', 'sdyx', f'{pz}')
                self.sender.reply(f'是否用户手动续期配置成功: {pz}')
        elif zh == '5':
            self.sender.reply('设置接受管理员通知的渠道，如 qq,wx,tg  用英文"，"符号分割,不设置不推送')
            pz = self.sender.listen(60000)
            if pz == 'q' or pz == 'Q':
                self.sender.reply("退出！")
            elif pz is None:
                self.sender.reply(f'超时退出！')
            else:
                sg.bucketSet('dd_wcconfig', 'notify', f'{pz}')
                self.sender.reply(f'设置接受管理员通知的渠道: {pz}')
        elif zh == '6':
            self.sender.reply('设置你的WxPusher的UID:')
            pz = self.sender.listen(60000)
            if pz == 'q' or pz == 'Q':
                self.sender.reply("退出！")
            elif pz is None:
                self.sender.reply(f'超时退出！')
            else:
                sg.bucketSet('dd_wcconfig', 'wxpusher', f'{pz}')
                self.sender.reply(f'设置WxPusher的UID为: {pz}')
        elif zh == '7':
            self.sender.reply('设置望潮抽奖代理api地址:')
            pz = self.sender.listen(60000)
            if pz == 'q' or pz == 'Q':
                self.sender.reply("退出！")
            elif pz is None:
                self.sender.reply(f'超时退出！')
            else:
                sg.bucketSet('dd_wcconfig', 'dlapi', f'{pz}')
                self.sender.reply(f'设置望潮抽奖代理api地址: {pz}')
        elif zh == '8':
            self.sender.reply('设置望潮查询代理api地址（每查询一个账号自动切换IP）:')
            pz = self.sender.listen(60000)
            if pz == 'q' or pz == 'Q':
                self.sender.reply("退出！")
            elif pz is None:
                self.sender.reply(f'超时退出！')
            else:
                sg.bucketSet('dd_wcconfig', 'cxproxy', f'{pz}')
                self.sender.reply(f'设置望潮查询代理api地址: {pz}')
        else:
            self.sender.reply(f'输入有误!!')

    def check_all_accounts_auth(self):
        return True

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

    def wc_notify(self):
        try:
            ts_raw = sg.bucketGet('dd_wccks', self.user)
            if not ts_raw or ts_raw == '{}' or not ts_raw.strip():
                self.sender.reply("❌ 未找到您的账号信息，请先登录账号后再设置通知")
                return

            try:
                ts_preview = _sg_literal(ts_raw)
            except Exception:
                ts_preview = {}

            if not isinstance(ts_preview, dict) or len(ts_preview) == 0:
                self.sender.reply("❌ 未找到您的账号信息，请先登录账号后再设置通知")
                return

            existing_uids = None
            for _, account_data in ts_preview.items():
                if isinstance(account_data, dict) and account_data.get('wxpusher_uid'):
                    existing_uids = str(account_data.get('wxpusher_uid'))
                    break

            tip_lines = [
                "请关注应用：https://wxpusher.zjiecode.com/wxuser/?type=1&id=115421#/follow",
                "",
                "关注后请获取自己的UIDS并输入（可输入一个或多个UIDS，用英文逗号 , 分隔）",
            ]
            if existing_uids:
                tip_lines.append(f"当前已绑定UIDS：{existing_uids}")
                tip_lines.append("再次发送新的UIDS将覆盖原有设置，实现通知UID的同步更新")
            tip_lines.append("退出回复【q】！")

            self.sender.reply("\n".join(tip_lines))

            uids_input = self.sender.listen(60000)

            if uids_input == 'q' or uids_input == 'Q':
                self.sender.reply("✅ 已取消设置")
                return
            elif uids_input is None:
                self.sender.reply("⏰ 操作超时,已退出")
                return

            raw_uids = uids_input.strip()
            if not raw_uids:
                self.sender.reply("❌ UIDS不能为空")
                return

            uid_list = [u.strip() for u in raw_uids.split(",") if u.strip()]
            if not uid_list:
                self.sender.reply("❌ UIDS格式不正确，请重新输入")
                return

            for u in uid_list:
                if not u.startswith("UID"):
                    self.sender.reply("❌ 输入格式错误，请发送以「UID」开头的完整 UIDS（可用英文逗号分隔多个）")
                    return

            seen = set()
            normalized_list = []
            for u in uid_list:
                if u not in seen:
                    seen.add(u)
                    normalized_list.append(u)
            uids = ",".join(normalized_list)

            ts = ts_preview

            len(ts)
            success_count = 0
            fail_count = 0

            for account_id, account_data in ts.items():
                try:
                    if not isinstance(account_data, dict):
                        account_data = {}
                    account_data['wxpusher_uid'] = uids
                    ts[account_id] = account_data
                    success_count += 1
                except Exception as e:
                    fail_count += 1
                    print(f"更新账号 {account_id} 失败: {str(e)}")

            sg.bucketSet('dd_wccks', self.user, f'{ts}')

            ql_success = 0
            ql_fail = 0
            if dd_wc_qlname:
                for account_id, account_data in ts.items():
                    try:
                        ql_value = account_data.get('ql_value', account_data.get('ck', ''))
                        if not ql_value:
                            continue
                        auth_time = account_data.get('sqsj', datetime.now().strftime("%Y-%m-%d"))
                        Addenvs(
                            osname=dd_wc_osname,
                            value=ql_value,
                            account=account_id,
                            name=account_data.get('name', ''),
                            auth_time=auth_time,
                            user_id=self.user
                        )
                        ql_success += 1
                    except Exception as e:
                        ql_fail += 1
                        print(f"更新青龙失败 - 账户: {account_data.get('name', account_id)}, 错误: {str(e)}")

            result_msg = f"""=====望潮通知设置完成=====
📊 总账号数: {len(ts)}个
✅ 本地成功更新UIDS: {success_count}个
❌ 本地更新失败: {fail_count}个
✅ 青龙同步成功: {ql_success}个
❌ 青龙同步失败: {ql_fail}个
🔔 新UIDS: {uids}
=====================
💡 说明:
• 所有账号的通知UIDS已同步为最新设置
• 如果之前已配置UIDS，本次操作会覆盖为新UIDS
• 同时已尝试将所有账号重新提交到青龙，保证变量与账号信息同步
• 查询或定时任务时会自动按新UIDS推送收益通知
====================="""
            self.sender.reply(result_msg)

        except Exception as e:
            self.sender.reply(f"❌ 设置失败: {str(e)}")

    def wcsq(self):
        msg = (
            '========望潮授权========\n'
            '1、全部授权\n'
            '2、指定授权\n'
            '=====================\n'
            '回复序号,退出【q】！'
        )
        self.sender.reply(msg)
        zh = self.sender.listen(60000)
        if zh == 'q' or zh == 'Q':
            self.sender.reply("退出！")
        elif zh is None:
            self.sender.reply(f'超时退出！')
        elif zh == '1':
            self.qbsq()
        elif zh == '2':
            self.zdsq()
        else:
            self.sender.reply(f'输入有误!!')

    def qbsq(self):
        self.sender.reply(f"请输入给所有账号授权的天数！！\n回复序号,退出【q】！")
        sjts = self.sender.listen(60000)
        if sjts == 'q' or sjts == 'Q':
            self.sender.reply("退出！")

        elif sjts is None:
            self.sender.reply(f'超时退出！')

        elif isinstance(int(sjts), int):
            ts = sg.bucketAllKeys('dd_wccks')
            for myuid in ts:
                ts_data = sg.bucketGet('dd_wccks', f'{myuid}')
                ts_data = _sg_literal(ts_data)
                if ts_data == {}:
                    sg.bucketDel('dd_wccks', f'{myuid}')
                    continue
                else:
                    for k, y in ts_data.items():
                        sqsj = y.get('sqsj', datetime.now().strftime("%Y-%m-%d"))
                        dqsj = datetime.now().strftime("%Y-%m-%d")
                        if sqsj > dqsj:
                            sqsj = datetime.strptime(sqsj, "%Y-%m-%d")
                            new_sqsj = sqsj + timedelta(days=int(sjts))
                            new_sqsj = new_sqsj.strftime("%Y-%m-%d")
                        else:
                            sj = datetime.now()
                            new_sqsj = sj + timedelta(days=int(sjts))
                            new_sqsj = new_sqsj.strftime("%Y-%m-%d")
                        ql_value = y.get('ql_value', y['ck'])
                        ts_data[f'{k}'] = {
                            'name': y['name'],
                            'ck': y['ck'],
                            'ql_value': ql_value,
                            'sqsj': f'{new_sqsj}'
                        }
                        sg.bucketSet('dd_wccks', f'{myuid}', f'{ts_data}')
                        try:
                            Addenvs(osname=dd_wc_osname, value=ql_value, account=k, name=y['name'], auth_time=new_sqsj)
                        except:
                            pass
            self.sender.reply(f"🔔望潮系统授权所有账号{int(sjts)}天全部完成！")

        else:
            self.sender.reply(f'{sjts} 输入有误，退出！')

    def zdsq(self):
        msg = (
            "请输入需要授权的账号 ID\n"
            "（可通过给机器人发送 myuid 获取）\n"
            "退出请回复【q】！"
        )
        self.sender.reply(msg)
        myuid = self.sender.listen(60000)
        if myuid == 'q' or myuid == 'Q':
            self.sender.reply("退出！")
        elif myuid is None:
            self.sender.reply(f'超时退出！')
        else:
            ts = sg.bucketGet('dd_wccks', myuid)
            if ts == '' or ts == '{}':
                self.sender.reply(f"🔔望潮系统未查询到{myuid}的信息! 请先登录! ")
            else:
                ts = _sg_literal(ts)
                n = 0
                id_dict = {}
                msg = (
                    "========望潮授权========\n"
                    "[0] 🎯 一键授权当前 UID 下全部账号\n"
                    "[00] ⏰ 一键授权当前 UID 下所有【过期】账号\n"
                    "=====================\n"
                )
                for k, y in ts.items():
                    n += 1
                    self.session = y['ck']
                    self.sqsj = y.get('sqsj', datetime.now().strftime("%Y-%m-%d"))
                    id_dict[n] = {
                        'usid': k,
                        'name': y['name'],
                        'ck': y['ck'],
                        'sqsj': y['sqsj']
                    }
                    msg += f'{n}、{y["name"]}\n授权时间: ⏰{self.sqsj}\n=====================\n'
                msg += (
                    "回复序号选择单个账号授权；\n"
                    "回复【0】一键授权全部账号；\n"
                    "回复【00】一键授权所有【过期】账号；\n"
                    "退出请回复【q】！"
                )
                self.sender.reply(msg)
                xz = self.sender.listen(60000)
                xz_list = []
                for k, y in id_dict.items():
                    xz_list.append(k)
                xz_list.append(0)
                if xz == 'q' or xz == 'Q':
                    self.sender.reply("退出！")

                elif xz is None:
                    self.sender.reply(f'超时退出！')

                elif xz == '0':
                    self.uid_batch_auth(myuid, ts)

                elif xz == '00':
                    self.uid_batch_auth_expired(myuid, ts)

                elif int(xz) in xz_list:
                    zh = id_dict[int(xz)]
                    self.account = zh['usid']
                    self.session = zh['ck']
                    self.name = zh['name']
                    self.sqsj = zh['sqsj']

                    msg = f'请输入给【{self.name}】授权的天数！！\n回复序号,退出【q】！'
                    self.sender.reply(msg)
                    sjts = self.sender.listen(60000)
                    if sjts == 'q' or sjts == 'Q':
                        self.sender.reply("退出！")

                    elif sjts is None:
                        self.sender.reply(f'超时退出！')

                    elif isinstance(int(sjts), int):
                        dqsj = datetime.now().strftime("%Y-%m-%d")
                        if self.sqsj > dqsj:
                            self.sqsj = datetime.strptime(self.sqsj, "%Y-%m-%d")
                            new_sqsj = self.sqsj + timedelta(days=int(sjts))
                            new_sqsj = new_sqsj.strftime("%Y-%m-%d")
                        else:
                            sj = datetime.now()
                            new_sqsj = sj + timedelta(days=int(sjts))
                            new_sqsj = new_sqsj.strftime("%Y-%m-%d")
                        ts = sg.bucketGet('dd_wccks', f'{myuid}')
                        ts = _sg_literal(ts)
                        for k, y in ts.items():
                            if self.account == k:
                                ql_value = y.get('ql_value', self.session)
                                ts[f'{k}'] = {
                                    'name': self.name,
                                    'ck': self.session,
                                    'ql_value': ql_value,
                                    'sqsj': f'{new_sqsj}'
                                }
                                sg.bucketSet('dd_wccks', myuid, f'{ts}')
                                try:
                                    Addenvs(osname=dd_wc_osname, value=ql_value, account=self.account, name=self.name, auth_time=new_sqsj)
                                except:
                                    pass

                                msg = f'========望潮授权========\n当前用户: {myuid}\n授权用户: {self.name}\n授权id: {self.account}\n授权天数: {int(sjts)}天\n到期时间: {new_sqsj}\n✅ 已提交青龙'
                                self.sender.reply(msg)
                                break
                            else:
                                continue
                    else:
                        self.sender.reply(f'{sjts} 输入有误，退出！')
                else:
                    self.sender.reply(f'{xz} 输入有误，退出！')

    def uid_batch_auth(self, myuid, ts):
        return True

    def uid_batch_auth_expired(self, myuid, ts):
        if not isinstance(ts, dict) or len(ts) == 0:
            self.sender.reply(f"🔔望潮系统未查询到 {myuid} 的有效账号信息! ")
            return

        today_str = datetime.now().strftime("%Y-%m-%d")
        expired_accounts = {}
        for account_id, info in ts.items():
            sqsj = str(info.get('sqsj', today_str))
            if sqsj <= today_str:
                expired_accounts[account_id] = info

        if not expired_accounts:
            self.sender.reply(f"✅ 当前 UID: {myuid} 下暂时没有授权过期的账号")
            return

        self.sender.reply(
            f"当前 UID: {myuid}\n"
            f"检测到【过期】账号数量: {len(expired_accounts)} 个\n"
            f"仅会为授权已过期的账号续费。\n"
            f"请输入需要一键授权的天数！！\n回复序号,退出【q】！"
        )
        sjts = self.sender.listen(60000)

        if sjts == 'q' or sjts == 'Q':
            self.sender.reply("退出！")
            return
        elif sjts is None:
            self.sender.reply('超时退出！')
            return

        try:
            days = int(sjts)
        except Exception:
            self.sender.reply(f'{sjts} 输入有误，退出！')
            return

        if days <= 0:
            self.sender.reply("❌ 授权天数必须大于 0")
            return

        updated_count = 0

        for account_id, info in expired_accounts.items():
            new_sqsj = datetime.now() + timedelta(days=days)
            new_sqsj_str = new_sqsj.strftime("%Y-%m-%d")

            ql_value = info.get('ql_value', info.get('ck', ''))
            if not ql_value:
                continue

            ts[account_id] = {
                'name': info.get('name', ''),
                'ck': info.get('ck', ''),
                'ql_value': ql_value,
                'sqsj': new_sqsj_str
            }

            try:
                Addenvs(
                    osname=dd_wc_osname,
                    value=ql_value,
                    account=account_id,
                    name=info.get('name', ''),
                    auth_time=new_sqsj_str
                )
            except:
                pass

            updated_count += 1

        sg.bucketSet('dd_wccks', myuid, f'{ts}')

        self.sender.reply(
            f"🔔望潮系统一键授权过期账号完成！\n"
            f"UID: {myuid}\n"
            f"授权过期账号数量: {updated_count} 个\n"
            f"授权天数: {days} 天\n"
            f"到期时间已更新。"
        )


def clean_expired_accounts():
    all_users = sg.bucketAllKeys('dd_wccks')
    if not all_users:
        sender.reply("=====清理结果=====\n❌ 未找到任何绑定账号\n==================")
        return

    sender.reply(f"=====开始清理=====\n共找到: {len(all_users)}个用户\n⏳ 清理中请稍候...\n==================")

    cleaned_count = 0
    today_time = datetime.now().strftime("%Y-%m-%d")

    for user_id in all_users:
        try:
            user_data = sg.bucketGet('dd_wccks', user_id)
            if not user_data or user_data == '' or user_data == '{}':
                continue

            user_data = _sg_literal(user_data)
            if not user_data:
                continue

            valid_accounts = {}
            for account_id, account_info in user_data.items():
                sqsj = account_info.get('sqsj', today_time)

                if sqsj < today_time:
                    try:
                        qlid = allenvs(osname=dd_wc_osname, account=account_id)
                        if qlid:
                            delenvs(id=qlid)
                    except:
                        pass
                    cleaned_count += 1
                else:
                    valid_accounts[account_id] = account_info

            if valid_accounts:
                sg.bucketSet('dd_wccks', user_id, str(valid_accounts))
            else:
                sg.bucketDel('dd_wccks', user_id)

        except Exception as e:
            print(f"处理用户 {user_id} 时出错: {str(e)}")
            continue

    sender.reply(f"=====清理完成=====\n✅ 已清理: {cleaned_count}个过期账号\n==================")

def sync_to_panel():
    all_users = sg.bucketAllKeys('dd_wccks')
    if not all_users:
        sender.reply("=====同步结果=====\n❌ 未找到任何绑定账号\n==================")
        return

    sender.reply(f"=====开始同步=====\n共找到: {len(all_users)}个用户\n⏳ 同步中请稍候...\n==================")

    success_count = 0
    skip_count = 0
    fail_count = 0
    today_time = datetime.now().strftime("%Y-%m-%d")

    for user_id in all_users:
        try:
            user_data = sg.bucketGet('dd_wccks', user_id)
            if not user_data or user_data == '' or user_data == '{}':
                continue

            user_data = _sg_literal(user_data)
            if not user_data:
                continue

            for account_id, account_info in user_data.items():
                try:
                    sqsj = account_info.get('sqsj', today_time)
                    if sqsj <= today_time:
                        skip_count += 1
                        continue

                    ql_value = account_info.get('ql_value', account_info.get('ck', ''))
                    if not ql_value:
                        fail_count += 1
                        continue

                    account_name = account_info.get('name', '未知')
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
                    print(f"同步账号 {account_id} 失败: {str(e)}")
                    fail_count += 1
                    continue

        except Exception as e:
            print(f"处理用户 {user_id} 时出错: {str(e)}")
            continue

    result_msg = f"""=====同步完成=====
✅ 成功同步: {success_count}个账号
⏭️ 跳过未授权: {skip_count}个账号
❌ 同步失败: {fail_count}个账号
=================="""
    sender.reply(result_msg)


if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    senderID = sg.getSenderID()
    sender = sg.Sender(senderID)
    user = sender.getUserID()
    message = sender.getMessage()
    atm_tpt = ATM_WC(user, sender)

    msg_lower = message.lower()
    if '登录' in message or '登陆' in message:
        atm_tpt.wcsc()
    elif '管理' in message:
        atm_tpt.wcgl()
    elif '查询' in message:
        atm_tpt.wccx()
    elif '通知' in message:
        atm_tpt.wc_notify()
    elif '删除' in message:
        atm_tpt.batch_delete_accounts()
    elif '配置' in message:
        if sender.isAdmin():
            atm_tpt.wcpz()
        else:
            sender.reply('❌ 您没有权限执行此操作!')
    elif message.strip() == '望潮教程':
        sender.reply("🔔望潮青龙管理插件教程\n🔔支持批量账号密码登录\n🔔登录成功后自动提交到青龙面板\n🔔批量登录格式：每行一个账号，格式：手机号#密码\n"
                    "=====================\n📱 用户指令:\n• 望潮登录 - 登录绑定账号（支持批量）\n• 望潮管理 - 管理账号（支持批量授权）\n"
                    "• 望潮查询 - 查询账号信息和收益（含中奖记录）\n• 望潮通知 - 设置通知UIDS\n• 望潮删除 - 批量删除账号（支持选择删除和一键删除）\n"
                    "• 望潮教程 - 查看教程\n=====================\n💡 使用提示:\n• 批量登录：发送'望潮登录'后，每行输入一个账号\n"
                    "• 批量授权：发送'望潮管理'后，选择[0]一键批量授权\n• 批量删除：发送'望潮删除'后，选择账号删除或[0]一键删除所有\n"
                    "• 支持微信支付和积分支付\n=====================")
    elif '授权检测' in message:
        if sender.isAdmin():
            atm_tpt.check_all_accounts_auth()
        else:
            sender.reply('❌ 您没有权限执行此操作!')
    elif '更新青龙' in message:
        if sender.isAdmin():
            atm_tpt.update_qinglong()
        else:
            sender.reply('❌ 您没有权限执行此操作!')
    elif message.strip() == '望潮对接测试':
        if not sender.isAdmin():
            sender.reply('❌ 您没有权限执行此操作!')
        elif not docking_enabled:
            sender.reply('❌ 未启用对接运行功能，请在配置中开启')
        else:
            success, msg = upload_docking_config()
            sender.reply(f'✅ 对接测试成功！\n\n{msg}\n\n📝 说明：\n• 此配置只需上传一次，无需重复操作' if success
                        else f'❌ 对接测试失败\n\n{msg}\n\n💡 请检查：\n• 对接卡密是否正确\n• 青龙容器配置是否正确\n• 网络连接是否正常')
    elif '同步' in message:
        if sender.isAdmin():
            sync_to_panel()
        else:
            sender.reply('❌ 您没有权限执行此操作!')
    elif '清理' in message:
        if sender.isAdmin():
            clean_expired_accounts()
        else:
            sender.reply('❌ 您没有权限执行此操作!')
    elif '授权' in message:
        if sender.isAdmin():
            atm_tpt.wcsq()
        else:
            sender.reply('❌ 您没有权限执行此操作!')
    elif sender.getImtype() == 'fake':
        all_users = sg.bucketAllKeys('dd_wccks')
        today_time = datetime.now().strftime("%Y-%m-%d")
        for user_id in (all_users or []):
            try:
                user_data = sg.bucketGet('dd_wccks', user_id)
                if not user_data or user_data == '' or user_data == '{}':
                    continue
                user_data = _sg_literal(user_data)
                if not user_data or user_data == {}:
                    continue
                for account_id, account_info in user_data.items():
                    account_name = account_info.get('name', '未知')
                    sqsj = account_info.get('sqsj', today_time)
                    ql_value = account_info.get('ql_value', account_info.get('ck', ''))
                    if not ql_value:
                        continue
                    if sqsj > today_time:
                        try:
                            expire_date = datetime.strptime(sqsj, "%Y-%m-%d")
                            days_left = (expire_date - datetime.now()).days
                            if days_left <= 3:
                                login_mobile = account_id[:3] + '****' + account_id[7:] if len(account_id) >= 11 else account_id
                                push_msg = f"""
=====望潮账号通知=====
📱 账号: {login_mobile}
📢 消息:
⏰ 定时检测提醒
------------------
⚠️ 授权即将到期
📅 到期时间: {sqsj}
⏳ 剩余天数: {days_left}天
💡 请及时续费授权
=================="""
                                for platform in ['wb', 'tg', 'qq', 'qb', 'wx']:
                                    sg.push(platform, '', user_id, '', push_msg)
                        except:
                            pass
                        try:
                            Addenvs(osname=dd_wc_osname, value=ql_value, account=account_id, name=account_name, auth_time=sqsj, user_id=user_id)
                        except:
                            pass
                    else:
                        try:
                            qlid = allenvs(osname=dd_wc_osname, account=account_id)
                            if qlid:
                                delenvs(id=qlid)
                        except:
                            pass
                        login_mobile = account_id[:3] + '****' + account_id[7:] if len(account_id) >= 11 else account_id
                        push_msg = f"""
=====望潮账号通知=====
📱 账号: {login_mobile}
📢 消息:
⏰ 定时检测提醒
------------------
❌ 授权已过期
💡 请及时续费授权
=================="""
                        for platform in ['wb', 'tg', 'qq', 'qb', 'wx']:
                            sg.push(platform, '', user_id, '', push_msg)
            except:
                continue
    else:
        sender.setContinue()
