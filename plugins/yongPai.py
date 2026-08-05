# [title: 甬派]
# [name: yongPai]
# [language: python]
# [class: 任务]
# [author: sky2022]
# [version: v4.5]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(甬派|yy)(登录|登陆)$|^登(录|陆)(甬派|yy)$|^甬派查询$|^甬派管理$|^甬派清理$|^甬派后台管理$|^甬派教程$]
# [cron: 56 6,16 * * *]
# [icon: https://api.iconify.design/lucide:apple.svg]
# [description: 介绍：甬派插件；指令：甬派登录、甬派管理、甬派查询、甬派清理、甬派后台]
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
    'dd_yy_panel_type': form.string().title('对接面板类型').default('').description('填写你当前使用的面板类型，支持：青龙、青龙面板、QL、呆呆、呆呆面板、Daidai'),
    'dd_yy_panel_config': form.string().title('对接面板配置').default('').description('统一填写面板对接参数。青龙：Host丨ClientID丨ClientSecret；呆呆：Host丨AppKey丨AppSecret；分隔符使用中文丨'),
    'dd_yy_panel_group': form.string().title('对接面板分组').default('').description('仅呆呆面板生效。填写后新增或更新变量时会同步写入 group 字段；留空则不处理分组'),
    'dd_yy_dd_yy_osname': form.string().title('面板变量名').default('').description('提交到面板中的甬派变量名'),
    'dd_yy_prize_show_count': form.string().title('中奖记录显示条数').default('').description('查询时显示最近多少条中奖记录，不填默认显示5条'),
    'dd_yy_proxy_url': form.string().title('代理地址').default('').description('代理服务器地址，用于登录请求'),
})
_CONFIG_FIELD_MAP = {
    ('dd_yy', 'panel_type'): 'dd_yy_panel_type',
    ('dd_yy', 'panel_config'): 'dd_yy_panel_config',
    ('dd_yy', 'panel_group'): 'dd_yy_panel_group',
    ('dd_yy', 'dd_yy_osname'): 'dd_yy_dd_yy_osname',
    ('dd_yy', 'prize_show_count'): 'dd_yy_prize_show_count',
    ('dd_yy', 'proxy_url'): 'dd_yy_proxy_url',
}

import re
from datetime import datetime, timedelta
import urllib.parse
from decimal import Decimal
import requests
import time
import json
import hashlib
import urllib.parse
import uuid
import random
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()
uservalue = sg.bucketGet(bucket='dd_yy_user', key=userid)

android_versions = ['7.0', '8.0', '9.0', '10', '11', '12', '13']
phone_models = ['Xiaomi', 'Samsung Galaxy', 'Huawei', 'OPPO', 'Vivo', 'Realme', 'Oppo']

LOTTERY_ACTIVITY_ID = 1997
LOTTERY_Q = "1DvvL80TsnkfuVjfbdhTeOa1Xz0ttq5tQkt33EX3Kvc="
LOTTERY_TENANT_CODE = "yongpai"


def normalize_panel_type(panel_type_value):
    value = str(panel_type_value or '').strip().lower()
    if value in ('呆呆', '呆呆面板', 'daidai', 'dd'):
        return 'daidai'
    if value in ('青龙', '青龙面板', 'qinglong', 'ql'):
        return 'qinglong'
    if value:
        return ''
    return 'qinglong'


def getusercontent():
    dd_yy_osname = sg.bucketGet('dd_yy', 'dd_yy_osname') or 'dd_yy_token'
    panel_type_value = sg.bucketGet('dd_yy', 'panel_type') or ''
    panel_config_value = (sg.bucketGet('dd_yy', 'panel_config') or '').strip()
    panel_group = (sg.bucketGet('dd_yy', 'panel_group') or '').strip()
    legacy_ql_config = sg.bucketGet('dd_yy', 'dd_yy_qlname') or ''
    dd_managecommand = sg.bucketGet('dd_yy', 'dd_managecommand') or '甬派管理'
    dd_querycommand = sg.bucketGet('dd_yy', 'dd_querycommand') or '甬派查询'
    dd_signcommand = sg.bucketGet('dd_yy', 'dd_signcommand') or '甬派登录'
    proxy_url = sg.bucketGet('dd_yy', 'proxy_url')

    randommanagecommand = dd_managecommand
    randomquerycommand = dd_querycommand
    randomsigncommand = dd_signcommand

    yyVipmoney = Decimal(sg.bucketGet('dd_yy', 'yyVipmoney') or '1')
    yycoin = int(sg.bucketGet('dd_yy', 'yycoin') or '0')

    use_ma_pay = '2099-12-31' or 'false'
    use_ma_pay = use_ma_pay.lower() == 'true'

    prize_show_count = int(sg.bucketGet('dd_yy', 'prize_show_count') or '5')

    panel_type = normalize_panel_type(panel_type_value)
    if not panel_type:
        sender.reply("""
=====配置错误=====
❌ 对接面板类型填写无效
------------------
请填写以下任一值:
• 青龙 / 青龙面板 / QL
• 呆呆 / 呆呆面板 / Daidai
==================""")
        exit(0)

    use_daidai = panel_type == 'daidai'
    if use_daidai:
        dd_yy_ddname = panel_config_value or ''
        dd_yy_qlname = legacy_ql_config
    else:
        dd_yy_qlname = panel_config_value or legacy_ql_config
        dd_yy_ddname = ''

    return (dd_yy_osname, dd_yy_qlname, dd_managecommand, dd_querycommand,
            dd_signcommand, randommanagecommand, randomquerycommand,
            randomsigncommand, yyVipmoney, yycoin, proxy_url,
            use_ma_pay, use_daidai, dd_yy_ddname, panel_group, prize_show_count)


def update_proxy(session, proxy_url):
    """更新代理配置，返回代理字典"""
    if not proxy_url:
        return None

    try:
        ip_raw = requests.get(proxy_url, timeout=5).text.strip()
        if "请先添加白名单" in ip_raw:
            print("代理服务异常：请先添加白名单")
            return None

        ip_raw = ip_raw.splitlines()[0].strip()

        if not ip_raw:
            print("获取到的代理为空")
            return None

        if not ip_raw.startswith("http://") and not ip_raw.startswith("https://"):
            proxy_url_full = "http://" + ip_raw
        else:
            proxy_url_full = ip_raw

        proxies = {'http': proxy_url_full, 'https': proxy_url_full}
        return proxies
    except Exception as e:
        print(f"获取代理失败: {str(e)}")
        return None


def seekql():
    try:
        if len(dd_yy_qlname) == 0:
            sender.reply("""
=====配置错误=====
❌ 未配置青龙信息
------------------
请在插件配置中填写:
Host丨ClientID丨ClientSecret
• 使用中文丨分隔
• 示例:
http://ql.example.com丨abcd丨1234
==================""")
            exit(0)

        qllist = dd_yy_qlname.split('丨')
        if len(qllist) != 3:
            sender.reply("""
=====格式错误=====
❌ 青龙配置格式错误
------------------
当前格式: {dd_yy_qlname}
正确格式:
Host丨ClientID丨ClientSecret
==================""")
            exit(0)

        QLurl = qllist[0].strip()
        ClientID = qllist[1].strip()
        ClientSecret = qllist[2].strip()

        if not all([QLurl, ClientID, ClientSecret]):
            sender.reply("""
=====参数错误=====
❌ 青龙配置参数不完整
------------------
请确保以下参数都已填写:
• 青龙面板地址(Host)
• 应用ID(ClientID)
• 应用密钥(ClientSecret)
==================""")
            exit(0)

        if not QLurl.startswith(('http://', 'https://')):
            sender.reply(f"""
=====地址错误=====
❌ 青龙地址格式错误
------------------
当前地址: {QLurl}
正确格式:
• http://qinglong.example.com
• https://ql.example.com:5700
==================""")
            exit(0)

        try:
            qltoken = QLtoken(QLurl=QLurl, ClientID=ClientID, ClientSecret=ClientSecret)
            return QLurl, qltoken
        except Exception as e:
            raise Exception(f"获取Token失败: {str(e)}")

    except Exception as e:
        sender.reply(f"""
=====连接失败=====
❌ 无法连接青龙面板
------------------
请检查:
1. 青龙面板是否运行
2. 网络是否正常
3. 配置是否正确
4. 错误信息: {str(e)}
------------------
当前配置:
• 地址: {QLurl if 'QLurl' in locals() else '未设置'}
• 应用ID: {ClientID[:4] + '****' if 'ClientID' in locals() else '未设置'}
==================""")
        exit(0)


def seekdd():
    try:
        if not dd_yy_ddname:
            sender.reply("""
=====配置错误=====
❌ 未配置呆呆面板信息
------------------
请在插件配置中填写:
• 对接面板类型: 呆呆
• 对接面板配置: Host丨AppKey丨AppSecret
• 使用中文丨分隔
==================""")
            exit(0)

        ddlist = dd_yy_ddname.split('丨')
        if len(ddlist) != 3:
            sender.reply(f"""
=====格式错误=====
❌ 呆呆面板配置格式错误
------------------
当前格式: {dd_yy_ddname}
正确格式:
Host丨AppKey丨AppSecret
==================""")
            exit(0)

        DDurl = ddlist[0].strip()
        AppKey = ddlist[1].strip()
        AppSecret = ddlist[2].strip()

        if not all([DDurl, AppKey, AppSecret]):
            sender.reply("""
=====参数错误=====
❌ 呆呆面板配置参数不完整
------------------
请确保以下参数都已填写:
• 面板地址(Host)
• AppKey
• AppSecret
==================""")
            exit(0)

        if not DDurl.startswith(('http://', 'https://')):
            sender.reply(f"""
=====地址错误=====
❌ 呆呆面板地址格式错误
------------------
当前地址: {DDurl}
正确格式:
• http://panel.example.com
• https://panel.example.com
==================""")
            exit(0)

        try:
            ddtoken = DDtoken(DDurl=DDurl, AppKey=AppKey, AppSecret=AppSecret)
            return DDurl, ddtoken
        except Exception as e:
            raise Exception(f"获取Token失败: {str(e)}")

    except SystemExit:
        raise
    except Exception as e:
        sender.reply(f"""
=====连接失败=====
❌ 无法连接呆呆面板
------------------
请检查:
1. 面板是否运行
2. 网络是否正常
3. 配置是否正确
4. 错误信息: {str(e)}
------------------
当前配置:
• 地址: {DDurl if 'DDurl' in locals() else '未设置'}
• AppKey: {AppKey[:4] + '****' if 'AppKey' in locals() else '未设置'}
==================""")
        exit(0)


def DDtoken(DDurl, AppKey, AppSecret):
    try:
        url = f'{DDurl}/api/open-api/token'
        data = {"app_key": AppKey, "app_secret": AppSecret}
        response = requests.post(url, json=data)

        if response.status_code != 200:
            sender.reply(f"""
=====请求失败=====
❌ 呆呆面板API请求失败
状态码: {response.status_code}
==================""")
            exit(0)

        result = response.json()
        access_token = result.get('data', {}).get('access_token')
        if access_token:
            return access_token
        else:
            sender.reply("""
=====认证失败=====
❌ 获取Token失败
------------------
请检查:
• AppKey是否正确
• AppSecret是否正确
• 应用是否有权限
==================""")
            exit(0)

    except requests.exceptions.RequestException as e:
        sender.reply(f"""
=====网络错误=====
❌ 连接呆呆面板失败
错误信息: {str(e)}
==================""")
        exit(0)
    except SystemExit:
        raise
    except Exception as e:
        sender.reply(f"""
=====系统错误=====
❌ 处理请求时出错
错误信息: {str(e)}
==================""")
        exit(0)


def get_dd_headers(content_type="application/json"):
    return {
        "Authorization": f"Bearer {panel_token}",
        "accept": "application/json",
        "Content-Type": content_type
    }


def dd_allenvs(osname, account):
    url = f"{panel_url}/api/envs"
    headers = get_dd_headers()
    params = {"keyword": str(account), "page_size": 100}
    response = requests.get(url=url, headers=headers, params=params).json()

    data_list = response.get('data', [])
    if isinstance(data_list, list):
        for envs in data_list:
            envname = envs.get('name', '')
            remarks = envs.get('remarks', '')
            if remarks is None:
                continue
            if osname == envname and str(account) in remarks:
                return envs['id']
        return None
    else:
        sender.reply('连接呆呆面板获取变量失败')
        exit(0)


def dd_delenvs(id):
    if id is None:
        return
    url = f"{panel_url}/api/envs/{id}"
    headers = get_dd_headers()
    requests.delete(url, headers=headers)


def DDcreate(osname, value, account, phone, target_userid=None):
    try:
        actual_userid = target_userid if target_userid else userid
        accountVip = '2099-12-31' or str(datetime.now().date())
        url = f"{panel_url}/api/envs"

        data = {
            "value": value,
            "name": osname,
            "remarks": f'甬派:{account}丨用户:{actual_userid}丨手机:{phone}丨到期:{accountVip}丨甬派管理'
        }
        if panel_group:
            data["group"] = panel_group

        headers = get_dd_headers()
        response = requests.post(url, headers=headers, json=data)

        if response.status_code not in (200, 201):
            sender.reply(f"""
=====添加变量失败=====
❌ 请求失败
状态码: {response.status_code}
==================""")
            exit(0)

        result = response.json()
        resp_data = result.get('data')
        if resp_data:
            return resp_data.get('id')

    except SystemExit:
        raise
    except Exception as e:
        sender.reply(f"""
=====系统错误=====
❌ 添加变量失败
错误信息: {str(e)}
==================""")
        exit(0)


def DDupdate(osname, value, account, env_id, phone, target_userid=None):
    actual_userid = target_userid if target_userid else userid
    accountVip = '2099-12-31' or str(datetime.now().date())
    url = f"{panel_url}/api/envs/{env_id}"

    data = {
        "value": value,
        "name": osname,
        "remarks": f'甬派:{account}丨用户:{actual_userid}丨手机:{phone}丨到期:{accountVip}丨甬派管理'
    }
    if panel_group:
        data["group"] = panel_group

    headers = get_dd_headers()
    response = requests.put(url, headers=headers, json=data)

    if response.status_code == 200:
        return env_id, None
    else:
        sender.reply('更新变量失败,请稍后重试')
        exit(0)


def delenvs(id):
    if id is None:
        return
    if use_daidai:
        dd_delenvs(id)
        return
    url = f"{QLurl}/open/envs"
    headers = {
        "Authorization": "Bearer" + ' ' + qltoken,
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    data = [id]
    response = requests.delete(url, headers=headers, json=data).json()


def allenvs(osname, account):
    if use_daidai:
        return dd_allenvs(osname, account)
    url = f"{QLurl}/open/envs"
    headers = {
        "Authorization": "Bearer" + ' ' + qltoken,
        "accept": "application/json"
    }
    response = requests.get(url=url, headers=headers).json()
    qlid = None
    if response['code'] == 200:
        envslist = response['data']
        for envs in envslist:
            envname = envs['name']
            remarks = envs['remarks']
            if remarks is None:
                continue
            if osname == envname and str(account) in remarks:
                qlid = envs['id']
                break
        return qlid
    else:
        sender.reply('连接青龙获取变量失败')
        exit(0)


def Addenvs(osname, value, account, phone, target_userid=None):
    phone = phone[:3] + '*' * 4 + phone[7:]

    if use_daidai:
        env_id = dd_allenvs(osname, account)
        if env_id is None:
            DDcreate(osname, value, account, phone, target_userid)
        else:
            DDupdate(osname, value, account, env_id, phone, target_userid)
        return

    url = f"{QLurl}/open/envs"
    headers = {
        "Authorization": "Bearer" + ' ' + qltoken,
        "accept": "application/json"
    }
    response = requests.get(url=url, headers=headers).json()
    qlid = None
    if response['code'] == 200:
        envslist = response['data']
        for envs in envslist:
            remarks = envs['remarks']
            envname = envs['name']
            if remarks is None:
                continue
            if account in remarks and osname == envname:
                qlid = envs['id']
                break
    else:
        sender.reply('连接青龙获取变量失败')
        exit(0)

    if qlid is None:
        QLzt(osname, value, account, phone, target_userid)
    else:
        QLupdate(osname, value, account, qlid, phone, target_userid)


def QLupdate(osname, value, account, qlid, phone, target_userid=None):
    qlurl = f"{QLurl}/open/envs"
    accountVip = '2099-12-31' or str(datetime.now().date())
    user_id_for_remarks = target_userid if target_userid is not None else userid
    data = {
        "value": value,
        "name": osname,
        "remarks": f'甬派:{account}丨用户:{user_id_for_remarks}丨到期:{accountVip}丨甬派管理',
        "id": qlid
    }
    headers = {
        "Authorization": "Bearer" + ' ' + qltoken,
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    response = requests.put(qlurl, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        response_json = response.json()
        data = response_json['data']
        if data is None:
            exit(0)
        id = data['id']
        createdAt = data['createdAt']
        return id, createdAt
    else:
        sender.reply('更新变量失败,请稍后重试')
        exit(0)


def QLzt(osname, value, account, phone, target_userid=None):  # 添加青龙变量
    try:
        qlurl = f"{QLurl}/open/envs"
        accountVip = '2099-12-31' or str(datetime.now().date())
        user_id_for_remarks = target_userid if target_userid is not None else userid

        data = [{
            "value": value,
            "name": osname,
            "remarks": f'甬派:{account}丨用户:{user_id_for_remarks}丨到期:{accountVip}丨甬派管理'
        }]

        headers = {
            "Authorization": f"Bearer {qltoken}",
            "accept": "application/json",
            "Content-Type": "application/json",
        }

        response = requests.post(qlurl, headers=headers, json=data)

        if response.status_code != 200:
            sender.reply(f"""
=====添加变量失败=====
❌ 请求失败
状态码: {response.status_code}
==================""")
            exit(0)

        result = response.json()
        if result.get('code') != 200:
            sender.reply(f"""
=====添加变量失败=====
❌ 青龙返回错误
错误信息: {result.get('message')}
==================""")
            exit(0)

        if "value must be unique" in response.text:
            return

        data = result.get('data')
        if not data or not isinstance(data, list) or len(data) == 0:
            sender.reply("""
=====添加变量失败=====
❌ 青龙返回数据异常
==================""")
            exit(0)

        return data[0].get('id')

    except Exception as e:
        sender.reply(f"""
=====系统错误=====
❌ 添加青龙变量失败
------------------
错误信息: {str(e)}
==================""")
        exit(0)


def QLtoken(QLurl, ClientID, ClientSecret):  # 获取青龙token
    try:
        url = f'{QLurl}/open/auth/token?client_id={ClientID}&client_secret={ClientSecret}'
        response = requests.get(url)

        if response.status_code != 200:
            sender.reply(f"""
=====请求失败=====
❌ 青龙API请求失败
------------------
状态码: {response.status_code}
请检查:
• API地址是否正确
• 面板是否正常运行
==================""")
            exit(0)

        result = response.json()
        if "token" in result.get('data', {}):
            return result['data']['token']
        else:
            sender.reply("""
=====认证失败=====
❌ 获取Token失败
------------------
请检查:
• ClientID是否正确
• ClientSecret是否正确
• 应用是否有权限
==================""")
            exit(0)

    except requests.exceptions.RequestException as e:
        sender.reply(f"""
=====网络错误=====
❌ 连接青龙面板失败
------------------
请检查:
• 青龙地址是否正确
• 网络是否正常
• 错误信息: {str(e)}
==================""")
        exit(0)
    except Exception as e:
        sender.reply(f"""
=====系统错误=====
❌ 处理请求时出错
------------------
请检查:
• 配置格式是否正确
• 错误信息: {str(e)}
==================""")
        exit(0)


def getRandom(start, end):
    return random.randint(start, end)


def generate_random_ua():
    android_version = random.choice(android_versions)
    phone_model = random.choice(phone_models) + random.choice(['Note', 'Pro', 'X', 'S']) + str(random.randint(1, 30))
    ua = f'Mozilla/5.0 (Linux; Android {android_version}; {phone_model} Build/RP1A.00121.012) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/104.0.5112.92 Mobile Safari/537.36'
    return ua


def ValueErrors(value, count):
    """验证输入值是否为有效的整数且在合理范围内"""
    try:
        value = int(value)
        if value > count or value == 0:
            sender.reply(f"""
=====输入无效=====
❌ 请输入 1-{count} 之间的数字
==================""")
            exit(0)
        return value
    except ValueError:
        sender.reply("""
=====输入无效=====
❌ 请输入正确的数字
==================""")
        exit(0)


def parse_batch_selection(input_str, max_count):
    """解析批量选择输入，支持逗号分隔和范围选择
    示例：
    - 1,3,5 -> [1,3,5]
    - 1-5 -> [1,2,3,4,5]
    - 1,3-5,7 -> [1,3,4,5,7]
    """
    try:
        selected_indices = []
        parts = input_str.split(',')

        for part in parts:
            part = part.strip()
            if '-' in part:
                range_parts = part.split('-')
                if len(range_parts) == 2:
                    start = int(range_parts[0].strip())
                    end = int(range_parts[1].strip())
                    if start <= end and start >= 1:
                        selected_indices.extend(range(start, end + 1))
                    else:
                        raise ValueError(f"范围格式错误: {part}")
                else:
                    raise ValueError(f"范围格式错误: {part}")
            else:
                selected_indices.append(int(part))

        selected_indices = sorted(list(set(selected_indices)))

        valid_indices = []
        invalid_indices = []

        for idx in selected_indices:
            if 1 <= idx <= max_count:
                valid_indices.append(idx)
            else:
                invalid_indices.append(idx)

        return valid_indices, invalid_indices

    except ValueError as e:
        raise ValueError(f"输入格式错误: {str(e)}")


def generate_md5(input_string):
    md5_hash = hashlib.md5()
    md5_hash.update(input_string.encode('utf-8'))
    md5_digest = md5_hash.hexdigest()
    return md5_digest


def yesornos():
    yesorno = sender.input(120000, 1, False)
    if yesorno == 'Y' or yesorno == 'y' or yesorno == '是':
        return True
    elif yesorno == 'n' or yesorno == 'N' or yesorno == '否':
        return False
    elif yesorno == '':
        sender.reply('输入超时！')
        exit(0)
    elif yesorno == 'q' or yesorno == 'Q' or yesorno == '退出':
        sender.reply('退出!')
        exit(0)
    else:
        sender.reply('输入错误！')
        exit(0)


def sf_login(sender):
    """甬派账号登录"""
    login_guide = """
=====甬派账号登录=====
请按以下格式输入账号信息:
手机号#密码#zfb账号(可用邮箱)#zfb姓名

🔰 支持批量登录，一行一个账号
示例:
13812345678#123456#13888888888#张三
13912345678#123456#13999999999#李四

注意:
• zfb信息用于自动提现
• 批量登录时请确保格式正确
------------------
回复"q"退出操作
=================="""
    sender.reply(login_guide)

    account_info = sender.input(120000, 1, False)
    if not account_info:
        sender.reply("⏰ 操作超时,已退出")
        exit(0)
    elif account_info.lower() == 'q':
        sender.reply("✅ 已取消登录")
        exit(0)

    account_lines = account_info.strip().split('\n')
    success_count = 0
    fail_count = 0

    accounts = []
    if uservalue:
        try:
            existing_accounts = _sg_literal(uservalue)
            if isinstance(existing_accounts, (list, tuple, set)):
                accounts = list(existing_accounts)
            else:
                accounts = [str(existing_accounts)]
        except:
            accounts = []

    is_batch = len(account_lines) > 1
    last_success_info = None
    last_success_phone = None

    for line in account_lines:
        line = line.strip()
        if not line:  # 跳过空行
            continue

        try:
            parts = line.split('#')
            if len(parts) != 4:
                fail_count += 1
                continue

            phone, password, alipay, realname = parts

            if not re.match(r'^1[3-9]\d{9}$', phone):
                fail_count += 1
                continue

            session = requests.session()
            proxies = None
            if proxy_url:
                proxies = update_proxy(session, proxy_url)

            ua = generate_random_ua() + ' agentweb/4.0.2 UCBrowser/11.6.4.950 yongpai'

            session.headers.update({
                'Host': 'ypapp.cnnb.com.cn',
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': ua,
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive'
            })

            deviceId = str(uuid.uuid4())
            ts = str(int(time.time() * 1000))
            sign = hashlib.md5(f'globalDatetime{ts}username{phone}test_123456679890123456'.encode()).hexdigest()
            url = f'https://ypapp.cnnb.com.cn/yongpai-user/api/login2/local3?username={phone}&password={password}&deviceId={deviceId}&globalDatetime={ts}&sign={sign}'

            result = None
            login_success = False
            for retry in range(3):
                try:
                    response = session.get(url, proxies=proxies, timeout=5)
                    result = response.json()
                    login_success = True
                    break
                except Exception as e:
                    if retry < 2:
                        time.sleep(1)
                        if proxy_url:
                            proxies = update_proxy(session, proxy_url)
                        continue
                    else:
                        fail_count += 1
                        break

            if not login_success or not result:
                continue

            if result.get("code") == 0:
                sg.bucketSet(bucket='dd_yy_token', key=phone, value=line)

                if phone not in accounts:
                    accounts.append(phone)
                success_count += 1

                last_success_info = line
                last_success_phone = phone
            else:
                fail_count += 1

        except Exception as e:
            fail_count += 1
            continue

    if accounts:
        accounts = list(dict.fromkeys(accounts))
        sg.bucketSet(bucket='dd_yy_user', key=userid, value=str(accounts))

    if is_batch:
        updated_count = 0
        for line in account_lines:
            line = line.strip()
            if not line:
                continue

            try:
                parts = line.split('#')
                if len(parts) != 4:
                    continue

                phone, password, alipay, realname = parts

                if not re.match(r'^1[3-9]\d{9}$', phone):
                    continue

                stored_info = sg.bucketGet(bucket='dd_yy_token', key=phone)
                if stored_info and stored_info == line:  # 确认是刚才成功登录的账号
                    accountVip = '2099-12-31'
                    if accountVip and accountVip >= today_time:
                        try:
                            login_mobile = phone[:3] + '*' * 4 + phone[7:]
                            qlid = allenvs(osname=dd_yy_osname, account=phone)
                            if qlid:
                                QLupdate(osname=dd_yy_osname, value=line, account=phone, qlid=qlid, phone=login_mobile)
                            else:
                                Addenvs(osname=dd_yy_osname, value=line, account=phone, phone=login_mobile)
                            updated_count += 1
                        except Exception as e:
                            print(f"更新账号 {phone} 的青龙变量时出错: {str(e)}")
                            continue

            except Exception as e:
                continue

        result_msg = f"""
=====批量登录结果=====
✅ 成功: {success_count}个账号
❌ 失败: {fail_count}个账号"""

        if updated_count > 0:
            result_msg += f"""
🔄 已更新: {updated_count}个已授权账号的青龙变量"""

        result_msg += f"""
------------------
💡 发送 {randommanagecommand} 可管理账号
=================="""
        sender.reply(result_msg)
        exit(0)  # 批量登录后直接退出
    elif success_count == 1:
        return last_success_info, last_success_phone, last_success_phone
    else:
        sender.reply("""
=====登录失败=====
❌ 所有账号登录均失败
==================""")
        exit(0)


def bindaccount():
    account_info, account, mobile = sf_login(sender)

    def accvip(account, account_info, mobile):
        accountVip = '2099-12-31'
        auth_status = '✅ 已授权' if accountVip and accountVip >= today_time else '⚠️ 未授权'
        next_step = f'发送 {randommanagecommand} 可管理账号' if accountVip and accountVip >= today_time else f'发送 {randommanagecommand} 可进行授权'

        success_msg = f"""
=====甬派账号绑定=====
📱 绑定账号: {mobile}
🔐 授权状态: {auth_status}
⏰ 下一步操作:
   {next_step}
=================="""

        accounts = []
        if uservalue:
            try:
                existing_accounts = _sg_literal(uservalue)
                if isinstance(existing_accounts, (list, tuple, set)):
                    accounts = list(existing_accounts)
                else:
                    accounts = [str(existing_accounts)]
            except:
                accounts = []

        if account not in accounts:
            accounts.append(account)

        accounts = list(dict.fromkeys(accounts))

        if accounts:
            sg.bucketSet(bucket='dd_yy_user', key=userid, value=str(accounts))

        sg.bucketSet(bucket='dd_yy_token', key=account, value=account_info)

        if accountVip and accountVip >= today_time:
            try:
                qlid = allenvs(osname=dd_yy_osname, account=account)
                if qlid:
                    QLupdate(osname=dd_yy_osname, value=account_info, account=account, qlid=qlid, phone=mobile)
                else:
                    Addenvs(osname=dd_yy_osname, value=account_info, account=account, phone=mobile)
            except Exception as e:
                sender.reply(f"""
=====青龙更新失败=====
❌ 更新青龙变量失败
⚠️ 错误: {str(e)}
==================""")

        sender.reply(success_msg)

    accvip(account, account_info, mobile)


def empower(empowertime, me_as_int):
    """授权时间计算"""
    day = me_as_int * 30
    if len(empowertime) == 0 or empowertime <= str(today_time):
        delayed_date = today_date + timedelta(days=day)
    elif empowertime > today_time:
        empower_date = datetime.strptime(empowertime, "%Y-%m-%d")
        delayed_date = empower_date + timedelta(days=day)
        delayed_date = delayed_date.date()
    else:
        sender.reply('出错！')
        exit(0)
    return str(delayed_date)


def sf_auth():
    return True


def meituanmanage():
    if len(uservalue) != 0:
        try:
            accounts = []
            try:
                cleaned_value = uservalue.strip('[]').strip()
                if cleaned_value:
                    accounts = [acc.strip().strip("'\"") for acc in cleaned_value.split(',')]
                    accounts = [acc for acc in accounts if acc]  # 移除空值
            except Exception as e:
                print(f"解析账号列表出错: {str(e)}")
                accounts = []

            display_accounts = []

            for account in accounts:
                accountVip = '2099-12-31'
                if len(accountVip) == 0:
                    vip_status = '⚠️ 未授权'
                elif accountVip < today_time:
                    vip_status = '❌ 已过期'
                else:
                    vip_status = f'✅ {accountVip}'

                display_accounts.append({
                    'account': account,
                    'vip_status': vip_status
                })

            display_accounts.sort(key=lambda x: (
                '9999-99-99' if len(x.get('vip_status', '')) <= 5  # 未授权或已过期
                else x.get('vip_status', '').split(' ')[-1]  # 获取日期部分
            ), reverse=True)

            page_size = 10  # 每页显示的账号数
            total_pages = (len(display_accounts) + page_size - 1) // page_size
            current_page = 1

            while True:
                start_idx = (current_page - 1) * page_size
                end_idx = min(start_idx + page_size, len(display_accounts))
                current_accounts = display_accounts[start_idx:end_idx]

                account_list = f"""
======我的甬派账号=====
📄 第{current_page}/{total_pages}页
[0] 批量授权模式"""

                for i, acc_info in enumerate(current_accounts, start_idx + 1):
                    account = acc_info['account']
                    vip_status = acc_info['vip_status']
                    login_mobile = account[:3] + "****" + account[7:]
                    account_list += f"""
------------------
[{i}] 账号信息
📱 账号: {login_mobile}
🔐 授权: {vip_status}"""

                account_list += """
------------------"""
                if total_pages > 1:
                    account_list += """
[n] 下一页
[p] 上一页"""

                account_list += """
[q] 退出操作
------------------
请输入序号选择账号
=================="""

                sender.reply(account_list)

                inputmessage = sender.input(120000, 1, False)
                if inputmessage is None or inputmessage == 'timeout':
                    sender.reply('⏰ 操作超时,已退出')
                    exit(0)
                elif inputmessage.lower() == 'q':
                    sender.reply('✅ 已退出管理')
                    exit(0)
                elif inputmessage.lower() == 'n' and current_page < total_pages:
                    current_page += 1
                    continue
                elif inputmessage.lower() == 'p' and current_page > 1:
                    current_page -= 1
                    continue
                elif inputmessage == '0':
                    sender.reply("""
=====批量授权模式=====
请输入要授权的账号序号
支持以下格式:
• 单个: 1
• 多个: 1,3,5
• 范围: 1-5
• 混合: 1,3-5,7
------------------
示例: 1-3,5,7-9
回复"q"退出操作
==================""")

                    batch_input = sender.input(120000, 1, False)
                    if batch_input is None or batch_input == 'timeout':
                        sender.reply('⏰ 操作超时,已退出')
                        continue
                    elif batch_input.lower() == 'q':
                        sender.reply('✅ 已退出批量授权')
                        continue

                    try:
                        valid_indices, invalid_indices = parse_batch_selection(batch_input, len(display_accounts))

                        if invalid_indices:
                            sender.reply(f'❌ 以下序号无效已忽略: {",".join(map(str, invalid_indices))}')

                        if not valid_indices:
                            sender.reply('❌ 未选择有效的账号序号')
                            continue

                        selected_info = f"""
=====选中账号列表=====
📱 共选择: {len(valid_indices)}个账号
------------------"""
                        for idx in valid_indices:
                            account = display_accounts[idx - 1]['account']
                            login_mobile = account[:3] + "****" + account[7:]
                            selected_info += f"""
[{idx}] {login_mobile}"""

                        selected_info += """
------------------
确认选择请继续
=================="""
                        sender.reply(selected_info)

                        auth_guide = """
=====设置授权时长=====
请输入授权月数(如:1)
------------------
回复数字设置月数
回复"q"退出操作
=================="""
                        sender.reply(auth_guide)

                        mes = sender.input(120000, 1, False)
                        if mes is None or mes == 'timeout':
                            sender.reply('⏰ 操作超时,已退出')
                            continue
                        elif mes == 'q' or mes == 'Q':
                            sender.reply('✅ 已退出授权')
                            continue

                        mes = ValueErrors(value=mes, count=999)

                        batch_accounts = []
                        for idx in valid_indices:
                            account = display_accounts[idx - 1]['account']
                            userurl = sg.bucketGet(bucket='dd_yy_token', key=f'{account}')
                            accountVip = '2099-12-31'
                            batch_accounts.append({
                                'account': account,
                                'token': userurl,
                                'accountVip': accountVip,
                                'phone': account[:3] + "****" + account[7:]
                            })

                        zf(project='甬派授权', me_as_int=mes, accountVip='', token='', phone='', account='',
                           batch_accounts=batch_accounts)
                        break

                    except ValueError as ve:
                        sender.reply(f'❌ {str(ve)}')
                        continue
                    except Exception as e:
                        sender.reply(f'❌ 处理输入时出错: {str(e)}')
                        continue

                try:
                    me_as_int = int(inputmessage)
                    if me_as_int <= 0 or me_as_int > len(display_accounts):
                        sender.reply('❌ 输入的序号无效')
                        continue

                    selected_account = display_accounts[me_as_int - 1]['account']
                    userurl = sg.bucketGet('dd_yy_token', selected_account)
                    accountVip = '2099-12-31'

                    if len(accountVip) == 0:
                        vip_status = '⚠️ 未授权'
                    elif accountVip < today_time:
                        vip_status = '❌ 已过期'
                    else:
                        vip_status = f'✅ {accountVip}'

                    login_mobile = selected_account[:3] + "****" + selected_account[7:]

                    combined_menu = f"""
=====账号详情=====
📱 账号: {login_mobile}
🔐 授权: {vip_status}
------------------
[1] 授权账号
[2] 删除账号
------------------
回复数字选择功能
回复"q"退出操作
=================="""
                    sender.reply(combined_menu)

                    inputmessage = sender.input(120000, 1, False)
                    if inputmessage is None or inputmessage == 'timeout':
                        sender.reply('⏰ 操作超时,已退出')
                        exit(0)
                    elif inputmessage == 'q' or inputmessage == 'Q':
                        sender.reply('✅ 已退出管理')
                        exit(0)
                    elif inputmessage == '2':
                        confirm_msg = """
=====警告=====
确定要删除该账号吗？
此操作不可恢复！
------------------
[y] 确认删除
[n] 取消操作
=================="""
                        sender.reply(confirm_msg)

                        yesorno = sender.input(120000, 1, False)
                        if yesorno is None or yesorno == 'timeout':
                            sender.reply('⏰ 操作超时,已退出')
                            exit(0)
                        elif yesorno == 'Y' or yesorno == 'y' or yesorno == '是':
                            accounts.remove(str(selected_account))
                            qlid = allenvs(osname=dd_yy_osname, account=str(selected_account))
                            delenvs(id=qlid)
                            if len(accounts) == 0:
                                sg.bucketDel(bucket='dd_yy_user', key=userid)
                            else:
                                sg.bucketSet(bucket='dd_yy_user', key=userid, value=f'{accounts}')
                            sender.reply('✅ 账号删除成功!')
                            break
                        elif yesorno == 'n' or yesorno == 'N' or yesorno == '否':
                            sender.reply('✅ 已取消删除')
                            break
                    elif inputmessage == '1':
                        auth_guide = """
=====设置授权时长=====
请输入授权月数(如:1)
------------------
回复数字设置月数
回复"q"退出操作
=================="""
                        sender.reply(auth_guide)

                        mes = sender.input(120000, 1, False)
                        if mes is None or mes == 'timeout':
                            sender.reply('⏰ 操作超时,已退出')
                            exit(0)
                        elif mes == 'q' or mes == 'Q':
                            sender.reply('✅ 已退出管理')
                            exit(0)
                        mes = ValueErrors(value=mes, count=999)
                        zf(project='甬派授权', me_as_int=mes, accountVip=accountVip, token=userurl,
                           phone=selected_account, account=selected_account)
                        break

                except ValueError:
                    sender.reply('❌ 输入必须是数字')
                    continue

            return

        except Exception as e:
            sender.reply(f"""
=====账号处理错误=====
❌ 账号列表处理失败
⚠️ 错误: {str(e)}
==================""")
            return
    else:
        sender.reply(f"""
=====未绑定账号=====
❌ 未找到任何账号信息
💡 发送 {randomsigncommand} 绑定
==================""")


def generate_qrcode(url):
    try:
        encoded_url = urllib.parse.quote(url, safe='')
        return f"https://api.qrtool.cn/?text={encoded_url}"
    except Exception as e:
        print(f"生成二维码失败: {str(e)}")
        return None


def get_payment_config():
    return {}


def zf(project, me_as_int, accountVip, token, phone, account, batch_accounts=None):
    """支付功能,支持单个和批量账号支付"""
    try:
        zsm, use_ma_pay_local, ma_pay_config = get_payment_config()
        if not zsm and not use_ma_pay_local:
            sender.reply('❌ 未配置收款方式，请检查配置')
            exit(0)

        accounts_count = len(batch_accounts) if batch_accounts else 1
        total_money = Decimal(me_as_int) * Decimal(yyVipmoney) * accounts_count
        total_coins = int(yycoin) * me_as_int * accounts_count

        if total_money == 0:
            success_count = 0
            accounts_to_process = batch_accounts if batch_accounts else [
                {'account': account, 'token': token, 'accountVip': accountVip, 'phone': phone}]
            for acc in accounts_to_process:
                try:
                    new_auth_time = empower(empowertime=acc['accountVip'], me_as_int=me_as_int)
                    True
                    stored_info = sg.bucketGet('dd_yy_token', acc['account'])
                    if stored_info:
                        Addenvs(osname=dd_yy_osname, value=stored_info, account=acc['account'],
                                phone=acc['phone'])
                        success_count += 1
                except Exception as e:
                    print(f"处理账号 {acc['account']} 时出错: {str(e)}")
                    continue
            sender.reply(f"""
=====免费授权成功=====
🎫 商品: {project}
💰 金额: 免费
✅ 成功: {success_count}/{len(accounts_to_process)}个账号
⏰ 授权时长: {me_as_int}月/每个
==================""")
            return True

        usercoin = sg.bucketGet('dd_sign_points', userid) or '0'

        pay_menu = f"""
=====选择支付方式====
📱 账号数量: {accounts_count}个
⏰ 授权时长: {me_as_int}月"""

        option_num = 1
        options_map = {}

        if zsm and not use_ma_pay_local:
            pay_menu += f"""
{option_num}️⃣ 微信支付
   💰 {total_money}元"""
            options_map[str(option_num)] = 'wechat'
            option_num += 1

        if use_ma_pay_local:
            pay_menu += f"""
{option_num}️⃣ 在线处理
   💰 {total_money}元"""
            options_map[str(option_num)] = 'ma'
            option_num += 1

        if yycoin and int(yycoin) > 0:
            pay_menu += f"""
{option_num}️⃣ 积分支付
   🎯 {total_coins}积分
   💫 当前积分: {usercoin}"""
            options_map[str(option_num)] = 'points'

        pay_menu += """
------------------
回复数字选择方式
回复"q"退出操作
=================="""

        sender.reply(pay_menu)
        choice = sender.input(60000, 1, False)

        if choice == 'q' or choice == 'Q':
            sender.reply("✅ 已取消支付")
            exit(0)

        selected_pay = options_map.get(choice)

        if selected_pay == 'wechat' and zsm:
            zfzt = False
            if zfzt:
                sender.reply('⚠️ 当前有人正在支付,请稍后再试！')
                exit(0)

            pay_msg = f"""
=====微信扫在线处理====
🎫 商品: {project}
📱 数量: {accounts_count}个账号
📅 时长: {me_as_int}月/每个
💰 金额: {total_money}元
------------------
请使用微信扫在线处理
回复"q"取消支付
=================="""
            sender.reply(pay_msg)
            sender.replyImage(zsm)

            ddzf = False

            if str(ddzf) == 'q':
                sender.reply('✅ 已取消支付')
                exit(0)

            try:
                if isinstance(ddzf, dict):
                    if ddzf.get('type') == '微信赞赏':
                        Money = float(ddzf.get('money', 0))
                        Time = ddzf.get('time', '')
                        ddzf.get('from_name', '')
                    elif ddzf.get('type') == '微信收款':
                        Money = float(ddzf.get('money', 0))
                        Time = ddzf.get('time', '')
                        ddzf.get('from_name', '')
                    else:
                        Money = float(ddzf.get('Money', 0))
                        Time = ddzf.get('Time', '')
                else:
                    try:
                        ddzf = json.loads(ddzf)
                        if ddzf.get('type') == '微信赞赏':
                            Money = float(ddzf.get('money', 0))
                            Time = ddzf.get('time', '')
                            ddzf.get('from_name', '')
                        elif ddzf.get('type') == '微信收款':
                            Money = float(ddzf.get('money', 0))
                            Time = ddzf.get('time', '')
                            ddzf.get('from_name', '')
                        else:
                            Money = float(ddzf.get('Money', 0))
                            Time = ddzf.get('Time', '')
                    except:
                        if "二维码赞赏到账" in str(ddzf):
                            try:
                                amount = str(ddzf).split("收款金额￥")[1].split("\n")[0]
                                time = str(ddzf).split("到账时间")[1].split("\n")[0]
                                Money = float(amount)
                                Time = time.strip()
                            except Exception as e:
                                sender.reply(f"❌ 解析收款信息失败: {str(e)}")
                                exit(0)
                        else:
                            sender.reply("❌ 无法解析支付结果")
                            exit(0)

                if float(Money) >= float(total_money):
                    success_count = 0
                    accounts_to_process = batch_accounts if batch_accounts else [
                        {'account': account, 'token': token, 'accountVip': accountVip, 'phone': phone}]

                    for acc in accounts_to_process:
                        try:
                            new_auth_time = empower(empowertime=acc['accountVip'], me_as_int=me_as_int)
                            True

                            stored_info = sg.bucketGet('dd_yy_token', acc['account'])
                            if stored_info:
                                Addenvs(osname=dd_yy_osname, value=stored_info, account=acc['account'],
                                        phone=acc['phone'])
                                success_count += 1

                        except Exception as e:
                            print(f"处理账号 {acc['account']} 时出错: {str(e)}")
                            continue

                    result_msg = f"""
=====支付成功=====
🎫 商品: {project}
💰 金额: {Money}元
⏰ 时间: {Time}
✅ 成功: {success_count}/{len(accounts_to_process)}个账号
=================="""
                    sender.reply(result_msg)
                    return True

                else:
                    sender.reply(f"""
=====支付金额错误=====
💰 应付: {total_money}元
💳 实付: {Money}元
❗ 请稍后核对支付记录！
==================""")
                    exit(0)

            except Exception as e:
                sender.reply(f"❌ 处理支付结果时出错: {str(e)}")
                exit(0)

        elif selected_pay == 'ma' and use_ma_pay_local:
            out_trade_no = f"YY{int(time.time())}{userid}"
            params = {
                'pid': ma_pay_config['pid'],
                'type': ma_pay_config['type'].split(',')[0],
                'out_trade_no': out_trade_no,
                'name': f"{senderID}-甬派授权-{str(total_money)}",
                'money': str(total_money),
                'notify_url': ma_pay_config['notify_url'],
                'return_url': ma_pay_config['return_url'],
                'param': userid
            }
            params = {k: v for k, v in params.items() if v}
            sorted_params = dict(sorted(params.items(), key=lambda x: x[0]))
            sign_str = "&".join([f"{k}={v}" for k, v in sorted_params.items()])
            sign = hashlib.md5((sign_str + ma_pay_config['key']).encode('utf-8')).hexdigest().lower()
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
                    sender.reply(f"""
=====支付失败=====
❌ 创建支付订单失败
HTTP状态码: {response.status_code}
==================""")
                    exit(0)

                try:
                    result = response.json()
                except:
                    sender.reply("""
=====支付失败=====
❌ 创建支付订单失败
返回数据格式错误
==================""")
                    exit(0)

                code = result.get('code', 0)
                msg = result.get('msg', '未知状态')

                if code == 1:
                    payurl = result.get('payurl', '')
                    if not payurl:
                        sender.reply("""
=====支付失败=====
❌ 未获取到支付链接
==================""")
                        exit(0)

                    qrcode_url = generate_qrcode(payurl)
                    if qrcode_url:
                        sender.replyImage(qrcode_url)
                    else:
                        sender.reply(f"""=====在线处理=====
🎫 商品: {project}
💰 金额: {total_money}元
⏰ 有效期: 5分钟
------------------
二维码生成失败，请点击链接完成支付:
{payurl}
==================""")
                else:
                    sender.reply(f"""
=====支付失败=====
❌ 创建订单失败: {msg}
==================""")
                    exit(0)

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
                            accounts_to_process = batch_accounts if batch_accounts else [
                                {'account': account, 'token': token, 'accountVip': accountVip, 'phone': phone}]

                            for acc in accounts_to_process:
                                try:
                                    new_auth_time = empower(empowertime=acc['accountVip'], me_as_int=me_as_int)
                                    True

                                    stored_info = sg.bucketGet('dd_yy_token', acc['account'])
                                    if stored_info:
                                        Addenvs(osname=dd_yy_osname, value=stored_info, account=acc['account'],
                                                phone=acc['phone'])
                                        success_count += 1
                                except Exception as e:
                                    print(f"处理账号 {acc['account']} 时出错: {str(e)}")
                                    continue

                            sender.reply(f"""
=====支付成功=====
🎫 商品: {project}
💰 金额: {total_money}元
✅ 成功: {success_count}/{len(accounts_to_process)}个账号
⏰ 授权时长: {me_as_int}月/每个
==================""")
                            return True
                    except Exception as e:
                        print(f"查询订单状态出错: {str(e)}")

                    result = sender.listen(5000)
                    if result == 'q' or result == 'Q':
                        sender.reply("✅ 已取消支付")
                        exit(0)

                sender.reply("❌ 支付超时,请重新发起支付!")
                exit(0)
            except SystemExit:
                raise
            except Exception as e:
                sender.reply(f"❌ 支付请求失败: {str(e)}")
                exit(0)

        elif selected_pay == 'points' and yycoin and int(yycoin) > 0:
            if int(usercoin) < total_coins:
                sender.reply(f"""
=====积分不足=====
👤 当前积分: {usercoin}
📍 需要积分: {total_coins}
==================""")
                exit(0)

            confirm_msg = f"""
=====积分支付确认=====
📱 账号数量: {accounts_count}个
💫 消耗积分: {total_coins}
⏰ 授权时长: {me_as_int}月/每个
------------------
确认请回复【y】
取消请回复【n】
=================="""
            sender.reply(confirm_msg)

            if yesornos():
                try:
                    new_balance = int(usercoin) - total_coins
                    sg.bucketSet('dd_sign_points', userid, str(new_balance))

                    success_count = 0
                    accounts_to_process = batch_accounts if batch_accounts else [
                        {'account': account, 'token': token, 'accountVip': accountVip, 'phone': phone}]

                    for acc in accounts_to_process:
                        try:
                            new_auth_time = empower(empowertime=acc['accountVip'], me_as_int=me_as_int)
                            True

                            stored_info = sg.bucketGet('dd_yy_token', acc['account'])
                            if stored_info:
                                Addenvs(osname=dd_yy_osname, value=stored_info, account=acc['account'],
                                        phone=acc['phone'])
                                success_count += 1

                        except Exception as e:
                            print(f"处理账号 {acc['account']} 时出错: {str(e)}")
                            continue

                    result_msg = f"""
=====支付成功=====
💫 扣除积分: {total_coins}
💰 剩余积分: {new_balance}
✅ 成功: {success_count}/{len(accounts_to_process)}个账号
⏰ 授权时长: {me_as_int}月/每个
=================="""
                    sender.reply(result_msg)
                    return True

                except Exception as e:
                    sender.reply(f"❌ 积分支付处理失败: {str(e)}")
                    exit(0)
            else:
                sender.reply("✅ 已取消支付")
                exit(0)
        else:
            sender.reply("❌ 输入无效")
            exit(0)

    except Exception as e:
        sender.reply(f"❌ 支付处理发生错误: {str(e)}")
        exit(0)


def cx(token, use_proxy=False):
    """查询用户信息和中奖记录"""
    try:
        account_info = token.split('#')
        if len(account_info) < 2:
            return "未知", "未知", []

        phone = account_info[0]
        password = account_info[1]

        session = requests.session()
        proxies = None
        if use_proxy and proxy_url:
            proxies = update_proxy(session, proxy_url)

        ua = generate_random_ua() + ' agentweb/4.0.2 UCBrowser/11.6.4.950 yongpai'
        session.headers.update({
            'Host': 'ypapp.cnnb.com.cn',
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': ua,
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        })

        ts = str(int(time.time() * 1000))
        deviceId = str(uuid.uuid4())
        sign = hashlib.md5(f'globalDatetime{ts}username{phone}test_123456679890123456'.encode()).hexdigest()
        url = f'https://ypapp.cnnb.com.cn/yongpai-user/api/login2/local3?username={phone}&password={password}&deviceId={deviceId}&globalDatetime={ts}&sign={sign}'

        response = session.get(url, proxies=proxies, timeout=5)
        result = response.json()

        if result.get("code") != 0:
            return "未知", "未知", []

        nickname = result.get("data", {}).get("nickname", "未知")
        mobile = result.get("data", {}).get("mobile", "未知")
        userId = result.get("data", {}).get("userId")
        new_token = result.get("data", {}).get("token")

        prizes = []
        try:
            lottery_login_body = {
                "accountId": str(userId),
                "sessionId": new_token,
                "q": LOTTERY_Q,
                "tenantCode": LOTTERY_TENANT_CODE,
            }
            lottery_headers = {
                "accept": "application/json, text/plain, */*",
                "content-type": "application/json",
                "user-agent": ua,
                "X-REQUEST-ID": f"{random.randint(1000,9999)}.{uuid.uuid4().hex[:12]}|{int(time.time() * 1000)}"
            }
            lottery_resp = requests.post(
                "https://act.tmlyun.com/activity-api/lottery/api/auth/userLogin",
                headers=lottery_headers,
                json=lottery_login_body,
                proxies=proxies,
                timeout=10
            )
            lottery_data = lottery_resp.json().get("data") or {}
            lottery_token = lottery_data.get("token")
            x_token = lottery_data.get("xToken") or lottery_data.get("x_token")

            if lottery_token:
                record_headers = {
                    "accept": "application/json, text/plain, */*",
                    "authorization": lottery_token,
                    "user-agent": ua,
                    "X-REQUEST-ID": f"{random.randint(1000,9999)}.{uuid.uuid4().hex[:12]}|{int(time.time() * 1000)}"
                }
                if x_token:
                    record_headers["X-TOKEN"] = x_token

                record_resp = requests.get(
                    f"https://act.tmlyun.com/activity-api/lottery/h5/activity/lottery/accountPrizeRecord/userPrizeRecord?activityId={LOTTERY_ACTIVITY_ID}",
                    headers=record_headers,
                    proxies=proxies,
                    timeout=10
                )
                record_result = record_resp.json()

                if record_result.get("code") == 0 or record_result.get("success") is True:
                    prize_list = record_result.get("data", {}).get("activityAccountPrizeVoList", [])
                    for prize in prize_list:
                        prizes.append({
                            'type': prize.get('grade', '未知类型'),
                            'title': prize.get('prizeName', '未知奖品'),
                            'time': prize.get('createTime', '')
                        })
        except Exception as prize_error:
            print(f"[警告] 查询中奖记录失败: {str(prize_error)}")

        return nickname, mobile, prizes

    except Exception as e:
        print(f"查询异常: {str(e)}")
        return "未知", "未知", []


def calculate_today_income(prizes):
    """计算今日收益"""
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        today_income = 0.0

        for prize in prizes:
            prize_time = prize.get('time', '')
            if prize_time.startswith(today):
                amount = re.search(r'(\d+\.?\d*)元', prize['title'])
                if amount:
                    today_income += float(amount.group(1))

        return today_income
    except Exception as e:
        print(f"计算今日收益出错: {str(e)}")
        return 0.0


def cxs():
    if len(uservalue) != 0:
        accounts = []
        try:
            cleaned_value = uservalue.strip('[]').strip()
            if cleaned_value:
                accounts = [acc.strip().strip("'\"") for acc in cleaned_value.split(',')]
                accounts = [acc for acc in accounts if acc]  # 移除空值
        except Exception as e:
            print(f"解析账号列表出错: {str(e)}")
            accounts = []

        if not accounts:
            sender.reply(f"""
=====未绑定账号=====
❌ 账号信息异常
💡 发送 {randomsigncommand} 重新绑定
==================""")
            return

        account_menu = """
=====甬派查询=====
[0] 查询全部账号
[9999] 查询全部账号今日收益
------------------"""

        for i, account in enumerate(accounts, 1):
            accountVip = '2099-12-31'
            login_mobile = account[:3] + "****" + account[7:]

            if len(accountVip) == 0:
                auth_status = "⚠️ 未授权"
            elif accountVip <= today_time:
                auth_status = "❌ 已过期"
            else:
                auth_status = "✅ 已授权"

            account_menu += f"""
[{i}] 账号: {login_mobile}
    授权: {auth_status}
------------------"""

        account_menu += """
回复数字选择查询方式
回复"q"退出操作
=================="""

        sender.reply(account_menu)

        choice = sender.input(120000, 1, False)
        if choice is None or choice == 'timeout':
            sender.reply('⏰ 操作超时,已退出')
            return
        elif choice.lower() == 'q':
            sender.reply('✅ 已退出查询')
            return

        try:
            if choice == '0':
                sender.reply('⏳ 正在查询全部账号,请稍候...')

                for i, account in enumerate(accounts, 1):
                    userToken = sg.bucketGet(bucket='dd_yy_token', key=f'{account}')
                    accountVip = '2099-12-31'
                    login_mobile = account[:3] + "****" + account[7:]

                    if len(accountVip) == 0:
                        auth_status = "⚠️ 未授权"
                        auth_time = "无"
                    elif accountVip <= today_time:
                        auth_status = "❌ 已过期"
                        auth_time = accountVip
                    else:
                        auth_status = "✅ 已授权"
                        auth_time = accountVip

                    if len(accountVip) != 0 and accountVip > today_time:
                        try:
                            nickname, mobile, prizes = cx(userToken)

                            success_count = 0
                            total_income = 0.0

                            for prize in prizes:
                                amount = re.search(r'(\d+\.?\d*)元', prize['title'])
                                if amount:
                                    success_count += 1
                                    total_income += float(amount.group(1))

                            account_info = f"""
=====账号详情[{i}]=====
📱 账号: {login_mobile}
👤 昵称: {nickname}
🔐 授权状态: {auth_status}
📅 到期时间: {auth_time}
💰 成功领取: {success_count}笔, 总计: {total_income:.2f}元"""

                            if prizes:
                                account_info += "\n===== 🎁转盘抽奖🎁 ====="
                                sorted_prizes = sorted(prizes, key=lambda x: x['time'], reverse=True)[:prize_show_count]
                                for prize in sorted_prizes:
                                    amount = re.search(r'(\d+\.?\d*)元', prize['title'])
                                    if amount:
                                        amount = f"现金{amount.group(1)}元"
                                    else:
                                        amount = prize['title']
                                    account_info += f"\n{amount}-{prize['time']}"
                            else:
                                account_info += "\n暂无中奖记录"

                            account_info += "\n=================="""
                            sender.reply(account_info)

                        except Exception as e:
                            sender.reply(f"""
=====甬派查询异常[{i}]=====
📱 账号: {login_mobile}
🔐 授权状态: {auth_status}
📅 到期时间: {auth_time}
❌ 状态: 查询失败
==================""")
                            continue
                    else:
                        sender.reply(f"""
=====甬派授权过期[{i}]=====
📱 账号: {login_mobile}
🔐 授权状态: {auth_status}
📅 到期时间: {auth_time}
==================""")

            elif choice == '9999':
                sender.reply('⏳ 正在查询今日收益,请稍候...')

                results = cx_batch_today_income(accounts)

                income_summary = f"""
=====今日收益汇总=====
📅 查询日期: {datetime.now().strftime("%Y-%m-%d")}
------------------"""

                total_today_income = 0.0
                valid_count = 0
                error_count = 0
                unauthorized_count = 0

                for i, account in enumerate(accounts, 1):
                    result = results.get(account, {})
                    status = result.get('status', 'unknown')
                    income = result.get('income', 0.0)
                    mobile = result.get('mobile', account[:3] + "****" + account[7:])

                    if status == 'success':
                        income_summary += f"""
[{i}]-{mobile}-今日收益:{income:.2f}元"""
                        total_today_income += income
                        valid_count += 1
                    elif status == 'unauthorized':
                        income_summary += f"""
[{i}]-{mobile}-今日收益:账号未授权"""
                        unauthorized_count += 1
                    else:
                        income_summary += f"""
[{i}]-{mobile}-今日收益:查询失败"""
                        error_count += 1

                income_summary += f"""
------------------
💰 总计收益: {total_today_income:.2f}元
📊 有效账号: {valid_count}/{len(accounts)}个
=================="""

                sender.reply(income_summary)

            else:
                choice_num = int(choice)
                if choice_num < 1 or choice_num > len(accounts):
                    sender.reply('❌ 输入的序号无效')
                    return

                account = accounts[choice_num - 1]
                userToken = sg.bucketGet(bucket='dd_yy_token', key=f'{account}')
                accountVip = '2099-12-31'
                login_mobile = account[:3] + "****" + account[7:]

                if len(accountVip) == 0:
                    auth_status = "⚠️ 未授权"
                    auth_time = "无"
                elif accountVip <= today_time:
                    auth_status = "❌ 已过期"
                    auth_time = accountVip
                else:
                    auth_status = "✅ 已授权"
                    auth_time = accountVip

                if len(accountVip) != 0 and accountVip > today_time:
                    try:
                        nickname, mobile, prizes = cx(userToken)

                        success_count = 0
                        total_income = 0.0
                        today_income = calculate_today_income(prizes)

                        for prize in prizes:
                            amount = re.search(r'(\d+\.?\d*)元', prize['title'])
                            if amount:
                                success_count += 1
                                total_income += float(amount.group(1))

                        account_info = f"""
=====账号详情[{choice_num}]=====
📱 账号: {login_mobile}
👤 昵称: {nickname}
🔐 授权状态: {auth_status}
📅 到期时间: {auth_time}
💰 总计收益: {total_income:.2f}元({success_count}笔)
💵 今日收益: {today_income:.2f}元"""

                        if prizes:
                            account_info += "\n===== 🎁转盘抽奖🎁 ====="
                            sorted_prizes = sorted(prizes, key=lambda x: x['time'], reverse=True)[:prize_show_count]
                            for prize in sorted_prizes:
                                amount = re.search(r'(\d+\.?\d*)元', prize['title'])
                                if amount:
                                    amount = f"现金{amount.group(1)}元"
                                else:
                                    amount = prize['title']
                                account_info += f"\n{amount}-{prize['time']}"
                        else:
                            account_info += "\n暂无中奖记录"

                        account_info += "\n=================="""
                        sender.reply(account_info)

                    except Exception as e:
                        sender.reply(f"""
=====甬派查询异常=====
📱 账号: {login_mobile}
🔐 授权状态: {auth_status}
📅 到期时间: {auth_time}
❌ 状态: 查询失败
⚠️ 错误: {str(e)}
==================""")
                else:
                    sender.reply(f"""
=====甬派授权过期=====
📱 账号: {login_mobile}
🔐 授权状态: {auth_status}
📅 到期时间: {auth_time}
💡 请及时续费授权
==================""")

        except ValueError:
            sender.reply('❌ 输入必须是数字')
            return
        except Exception as e:
            sender.reply(f'❌ 查询过程中出错: {str(e)}')
            return

    else:
        sender.reply(f"""
=====未绑定账号=====
❌ 未找到任何账号信息
💡 发送 {randomsigncommand} 绑定
==================""")


def push(user, account, c):
    login_mobile = account[:3] + "****" + account[7:]

    push_msg = f"""
=====甬派账号通知=====
📱 账号: {login_mobile}
📢 消息: {c}
=================="""

    sg.push('wb', '', user, '', push_msg)
    sg.push('tg', '', user, '', push_msg)
    sg.push('qq', '', user, '', push_msg)
    sg.push('qb', '', user, '', push_msg)
    sg.push('wx', '', user, '', push_msg)


def clean_expired_accounts():
    """清理过期的甬派账号"""
    if not sender.isAdmin():
        sender.reply("❌ 您没有权限执行此操作")
        exit(0)

    users = sg.bucketAllKeys(bucket='dd_yy_user')
    if not users:
        sender.reply("❌ 未找到任何绑定账号")
        exit(0)

    sender.reply(f"""
=====开始清理=====
📊 共找到: {len(users)}个用户
⏳ 清理中请稍候...
==================""")

    cleaned_accounts = 0
    cleaned_vars = 0
    cleaned_users = 0

    for user in users:
        try:
            accountlist = sg.bucketGet(bucket='dd_yy_user', key=user)
            if not accountlist:
                continue

            accounts = _sg_literal(accountlist)
            if isinstance(accounts, (list, tuple, set)):
                accounts = list(dict.fromkeys(accounts))
            else:
                accounts = [str(accounts)]

            valid_accounts = []

            for account in accounts:
                accountVip = '2099-12-31'

                if len(accountVip) == 0 or accountVip <= today_time:
                    try:
                        qlid = allenvs(osname=dd_yy_osname, account=account)
                        if qlid:
                            delenvs(id=qlid)
                            cleaned_vars += 1
                        sg.bucketDel(bucket='dd_yy_token', key=account)
                        True
                        cleaned_accounts += 1
                    except Exception as e:
                        print(f"处理账号 {account} 时出错: {str(e)}")
                        continue
                else:
                    valid_accounts.append(account)

            if valid_accounts:
                sg.bucketSet(bucket='dd_yy_user', key=user, value=str(valid_accounts))
            else:
                sg.bucketDel(bucket='dd_yy_user', key=user)
                cleaned_users += 1

        except Exception as e:
            print(f"处理用户 {user} 时出错: {str(e)}")
            continue

    sender.reply(f"""
=====清理完成=====
✅ 已清理:
• {cleaned_accounts}个过期账号
• {cleaned_vars}个面板变量
• {cleaned_users}个空用户记录
==================""")


def show_tutorial():
    """显示甬派插件使用教程"""
    tutorial = """
=====甬派插件教程=====
🔰 基础功能指令:
------------------
1️⃣ 甬派登录
• 输入格式: 手机号#密码#zfb账号(可用邮箱)#zfb姓名
• 示例: 13812345678#123456#13888888888#张三
• zfb信息用于自动提现

2️⃣ 甬派查询
• 查看账号信息
• 查看中奖信息

3️⃣ 甬派管理
• 管理已绑定账号
• 授权账号/删除账号
• 支持积分/微信支付

🔧 管理员功能:
------------------
• 甬派后台: 后台管理
• 甬派清理: 清理过期账号

⚠️ 注意事项:
------------------
1. 首次使用请先登录绑定
2. 定期查看账号状态
3. 及时处理授权到期
4. 请确保zfb信息准确
=================="""
    sender.reply(tutorial)


def cx_today_income_fast(token, use_proxy=False):
    """快速查询今日收益（只查询最近记录）"""
    try:
        account_info = token.split('#')
        if len(account_info) < 2:
            return 0.0, "未知"

        phone = account_info[0]
        password = account_info[1]

        session = requests.session()
        proxies = None
        if use_proxy and proxy_url:
            proxies = update_proxy(session, proxy_url)

        ua = generate_random_ua() + ' agentweb/4.0.2 UCBrowser/11.6.4.950 yongpai'
        session.headers.update({
            'Host': 'ypapp.cnnb.com.cn',
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': ua,
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        })

        ts = str(int(time.time() * 1000))
        deviceId = str(uuid.uuid4())
        sign = hashlib.md5(f'globalDatetime{ts}username{phone}test_123456679890123456'.encode()).hexdigest()
        url = f'https://ypapp.cnnb.com.cn/yongpai-user/api/login2/local3?username={phone}&password={password}&deviceId={deviceId}&globalDatetime={ts}&sign={sign}'

        response = session.get(url, proxies=proxies, timeout=5)
        result = response.json()

        if result.get("code") != 0:
            return 0.0, "登录失败"

        nickname = result.get("data", {}).get("nickname", "未知")
        userId = result.get("data", {}).get("userId")

        today_income = 0.0
        try:
            lottery_login_body = {
                "accountId": str(userId),
                "sessionId": result.get("data", {}).get("token", ""),
                "q": LOTTERY_Q,
                "tenantCode": LOTTERY_TENANT_CODE,
            }
            lottery_headers = {
                "accept": "application/json, text/plain, */*",
                "content-type": "application/json",
                "user-agent": ua,
                "X-REQUEST-ID": f"{random.randint(1000,9999)}.{uuid.uuid4().hex[:12]}|{int(time.time() * 1000)}"
            }
            lottery_resp = requests.post(
                "https://act.tmlyun.com/activity-api/lottery/api/auth/userLogin",
                headers=lottery_headers,
                json=lottery_login_body,
                proxies=proxies,
                timeout=10
            )
            lottery_data = lottery_resp.json().get("data") or {}
            lottery_token = lottery_data.get("token")
            x_token = lottery_data.get("xToken") or lottery_data.get("x_token")

            if lottery_token:
                record_headers = {
                    "accept": "application/json, text/plain, */*",
                    "authorization": lottery_token,
                    "user-agent": ua,
                    "X-REQUEST-ID": f"{random.randint(1000,9999)}.{uuid.uuid4().hex[:12]}|{int(time.time() * 1000)}"
                }
                if x_token:
                    record_headers["X-TOKEN"] = x_token

                record_resp = requests.get(
                    f"https://act.tmlyun.com/activity-api/lottery/h5/activity/lottery/accountPrizeRecord/userPrizeRecord?activityId={LOTTERY_ACTIVITY_ID}",
                    headers=record_headers,
                    proxies=proxies,
                    timeout=10
                )
                record_result = record_resp.json()

                if record_result.get("code") == 0 or record_result.get("success") is True:
                    today = datetime.now().strftime("%Y-%m-%d")
                    prize_list = record_result.get("data", {}).get("activityAccountPrizeVoList", [])
                    for prize in prize_list:
                        prize_time = prize.get('createTime', '')
                        if prize_time.startswith(today):
                            prize_name = prize.get('prizeName', '')
                            amount = re.search(r'(\d+\.?\d*)元', prize_name)
                            if amount:
                                today_income += float(amount.group(1))
        except Exception as prize_error:
            print(f"[警告] 查询今日收益失败: {str(prize_error)}，昵称: {nickname}")

        return today_income, nickname

    except Exception as e:
        print(f"快速查询今日收益异常: {str(e)}")
        return 0.0, "查询失败"


def cx_batch_today_income(accounts):
    """批量查询今日收益（支持并发）"""
    results = {}

    def query_single_account(account):
        try:
            userToken = sg.bucketGet(bucket='dd_yy_token', key=f'{account}')
            accountVip = '2099-12-31'
            login_mobile = account[:3] + "****" + account[7:]

            if len(accountVip) != 0 and accountVip > today_time:
                today_income, nickname = cx_today_income_fast(userToken)
                return account, {
                    'status': 'success',
                    'income': today_income,
                    'nickname': nickname,
                    'mobile': login_mobile
                }
            else:
                return account, {
                    'status': 'unauthorized',
                    'income': 0.0,
                    'nickname': '未授权',
                    'mobile': login_mobile
                }
        except Exception as e:
            return account, {
                'status': 'error',
                'income': 0.0,
                'nickname': '查询失败',
                'mobile': login_mobile,
                'error': str(e)
            }

    with ThreadPoolExecutor(max_workers=min(5, len(accounts))) as executor:
        future_to_account = {executor.submit(query_single_account, account): account for account in accounts}

        for future in as_completed(future_to_account):
            account, result = future.result()
            results[account] = result

    return results


dd_yy_osname, dd_yy_qlname, dd_managecommand, dd_querycommand, dd_signcommand, \
    randommanagecommand, randomquerycommand, randomsigncommand, yyVipmoney, yycoin, proxy_url, \
    use_ma_pay, use_daidai, dd_yy_ddname, panel_group, prize_show_count = getusercontent()
if use_daidai:
    panel_url, panel_token = seekdd()
    QLurl, qltoken = panel_url, panel_token
else:
    QLurl, qltoken = seekql()
    panel_url, panel_token = QLurl, qltoken
imtype = sender.getImtype()
today_date = datetime.now().date()
today_time = str(today_date)
usermessage = sender.getMessage()

if '登录' in usermessage or '登陆' in usermessage:
    bindaccount()
elif usermessage == '甬派后台管理':
    sf_auth()
elif usermessage == '甬派清理':
    clean_expired_accounts()
elif usermessage == '甬派教程':
    show_tutorial()
elif '管理' in usermessage:
    if len(uservalue) != 0:
        meituanmanage()
    else:
        sender.reply(f"""
=====未绑定账号=====
❌ 未找到任何账号信息
💡 发送 {randomsigncommand} 绑定
==================""")
elif '查询' in usermessage:
    if len(uservalue) != 0:
        cxs()
    else:
        sender.reply(f"""
=====未绑定账号=====
❌ 未找到任何账号信息
💡 发送 {randomsigncommand} 绑定
==================""")
elif imtype == 'fake':
    users = sg.bucketAllKeys(bucket='dd_yy_user')
    for user in users:
        accountlist = sg.bucketGet(bucket='dd_yy_user', key=f'{user}')
        accounts = _sg_literal(accountlist)
        for account in accounts:
            token = sg.bucketGet(bucket='dd_yy_token', key=f'{account}')
            accountVip = '2099-12-31'

            if len(accountVip) != 0 and accountVip > today_time:
                continue
            else:
                qlid = allenvs(osname=dd_yy_osname, account=account)
                delenvs(id=qlid)
                push(user=user, account=account, c="""
⚠️ 授权已过期
------------------
❌ 授权状态失效
💡 请及时续费授权""")
else:
    sender.setContinue()
