# [title: 甬派]
# [name: yongPai]
# [language: python]
# [class: 任务]
# [author: sky2022]
# [version: v1.5.1]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(甬派|yy)(登录|登陆)$|^登(录|陆)(甬派|yy)$|^甬派(查询|管理|教程)$]
# [icon: https://api.iconify.design/lucide:apple.svg]
# [description: 甬派账号登录、中奖查询、账号管理与面板同步]
# [depe: ["requests"]]

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
    'dd_yy_panel_type': plugin.Form.string().title('对接面板类型').default('').description('填写你当前使用的面板类型，支持：青龙、青龙面板、QL、呆呆、呆呆面板、Daidai'),
    'dd_yy_panel_config': plugin.Form.string().title('对接面板配置').default('').description('统一填写面板对接参数。青龙：Host丨ClientID丨ClientSecret；呆呆：Host丨AppKey丨AppSecret；分隔符使用中文丨'),
    'dd_yy_panel_group': plugin.Form.string().title('对接面板分组').default('').description('仅呆呆面板生效。填写后新增或更新变量时会同步写入 group 字段；留空则不处理分组'),
    'dd_yy_dd_yy_osname': plugin.Form.string().title('面板变量名').default('').description('提交到面板中的甬派变量名'),
    'dd_yy_prize_show_count': plugin.Form.string().title('中奖记录显示条数').default('').description('查询时显示最近多少条中奖记录，不填默认显示5条'),
    'dd_yy_proxy_url': plugin.Form.string().title('代理地址').default('').description('代理服务器地址，用于登录请求'),
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
from datetime import datetime
import requests
import time
import json
import hashlib
import uuid
import random
import os

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
    panel_type=normalize_panel_type(sg.bucketGet('dd_yy','panel_type') or 'qinglong')
    return {
        'osname':sg.bucketGet('dd_yy','dd_yy_osname') or 'dd_yy_token',
        'panel_type':panel_type,
        'panel_config':str(sg.bucketGet('dd_yy','panel_config') or sg.bucketGet('dd_yy','dd_yy_qlname') or '').strip(),
        'panel_group':str(sg.bucketGet('dd_yy','panel_group') or '').strip(),
        'proxy_url':sg.bucketGet('dd_yy','proxy_url') or '',
        'prize_show_count':max(1,int(sg.bucketGet('dd_yy','prize_show_count') or 5)),
    }


def update_proxy(session, proxy_url):
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
        accountVip = '2099-12-31'
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
    accountVip = '2099-12-31'
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
    requests.delete(url, headers=headers, json=data).json()

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
    accountVip = '2099-12-31'
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
        accountVip = '2099-12-31'
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

def generate_random_ua():
    android_version = random.choice(android_versions)
    phone_model = random.choice(phone_models) + random.choice(['Note', 'Pro', 'X', 'S']) + str(random.randint(1, 30))
    ua = f'Mozilla/5.0 (Linux; Android {android_version}; {phone_model} Build/RP1A.00121.012) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/104.0.5112.92 Mobile Safari/537.36'
    return ua




def sf_login(sender):
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
                except Exception:
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

        except Exception:
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

            except Exception:
                continue

        result_msg = f"""
=====批量登录结果=====
✅ 成功: {success_count}个账号
❌ 失败: {fail_count}个账号"""

        if updated_count > 0:
            result_msg += f"""
🔄 已更新: {updated_count}个账号的面板变量"""

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
    account_info,account,mobile=sf_login(sender)
    accounts=list(dict.fromkeys(_sg_literal(sg.bucketGet('dd_yy_user',userid),[])+[account]))
    sg.bucketSet('dd_yy_user',userid,str(accounts));sg.bucketSet('dd_yy_token',account,account_info)
    sync='未配置面板，仅本地保存'
    if QLurl and qltoken:
        try:
            env=allenvs(dd_yy_osname,account)
            if env:QLupdate(dd_yy_osname,account_info,account,env,mobile)
            else:Addenvs(dd_yy_osname,account_info,account,mobile)
            sync='面板同步成功'
        except Exception as error:sync=f'面板同步失败：{error}'
    sender.reply(f'甬派账号 {mobile} 绑定成功；{sync}')




def meituanmanage():
    accounts=list(_sg_literal(sg.bucketGet('dd_yy_user',userid),[]))
    if not accounts:return sender.reply('未绑定账号，请发送【甬派登录】')
    sender.reply('甬派账号：\n'+'\n'.join(f'{i}. {a[:3]}****{a[-4:]}' for i,a in enumerate(accounts,1))+'\n回复序号管理，q 退出')
    choice=sender.input(120000,1,False)
    if choice is None or str(choice).lower()=='q':return
    try:account=accounts[int(choice)-1]
    except (ValueError,IndexError):return sender.reply('序号无效')
    sender.reply('1. 删除账号\n2. 重新同步面板\nq. 退出');action=sender.input(60000,1,False)
    if action=='1':
        sender.reply('回复 y 确认删除')
        if str(sender.input(60000,1,False)).lower()=='y':
            env=allenvs(dd_yy_osname,account) if QLurl and qltoken else None
            if env:delenvs(env)
            accounts.remove(account);sg.bucketSet('dd_yy_user',userid,str(accounts)) if accounts else sg.bucketDel('dd_yy_user',userid);sg.bucketDel('dd_yy_token',account);sender.reply('账号已删除')
    elif action=='2':
        token=sg.bucketGet('dd_yy_token',account)
        if not token:return sender.reply('凭证不存在，请重新登录')
        if not QLurl or not qltoken:return sender.reply('未配置面板')
        env=allenvs(dd_yy_osname,account)
        if env:QLupdate(dd_yy_osname,token,account,env,account)
        else:Addenvs(dd_yy_osname,token,account,account)
        sender.reply('面板同步完成')





def cx(token, use_proxy=False):
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


def cxs():
    accounts=list(_sg_literal(sg.bucketGet('dd_yy_user',userid),[]))
    if not accounts:return sender.reply('未绑定账号，请发送【甬派登录】')
    rows=[]
    for account in accounts:
        token=sg.bucketGet('dd_yy_token',account);masked=account[:3]+'****'+account[-4:]
        if not token:rows.append(f'{masked}：凭证不存在');continue
        try:
            nickname,mobile,prizes=cx(token);latest=prizes[:prize_show_count]
            rows.append(f'{nickname or masked}：'+('；'.join(str(x.get('title','')) for x in latest) if latest else '暂无中奖记录'))
        except Exception as error:rows.append(f'{masked}：查询失败 {error}')
    sender.reply('甬派查询：\n'+'\n'.join(rows))


def show_tutorial():
    sender.reply('【甬派登录】绑定账号；【甬派查询】查询中奖记录；【甬派管理】删除账号或重新同步面板。')




settings=getusercontent();today_time=str(datetime.now().date());randommanagecommand='甬派管理';dd_yy_osname=settings['osname'];panel_group=settings['panel_group'];proxy_url=settings['proxy_url'];prize_show_count=settings['prize_show_count'];use_daidai=settings['panel_type']=='daidai';dd_yy_qlname=settings['panel_config'];dd_yy_ddname=settings['panel_config']
QLurl=qltoken=panel_url=panel_token=''
if settings['panel_config']:
    if use_daidai:panel_url,panel_token=seekdd();QLurl,qltoken=panel_url,panel_token
    else:QLurl,qltoken=seekql();panel_url,panel_token=QLurl,qltoken
usermessage=sender.getMessage()
if '登录' in usermessage or '登陆' in usermessage:bindaccount()
elif usermessage=='甬派管理':meituanmanage()
elif usermessage=='甬派查询':cxs()
elif usermessage=='甬派教程':show_tutorial()
else:sender.setContinue()
