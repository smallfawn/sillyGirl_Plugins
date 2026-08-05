# [title: 我不饿]
# [name: woBuE]
# [language: python]
# [class: 任务]
# [author: chuan]
# [version: v3.5.0]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ?]
# [icon: https://api.iconify.design/lucide:apple.svg]
# [description: 指令：配参填写；介绍：elm代挂插件，直接发送cookie即可绑定，支持多容器，使用前请安装pycryptodome，python-dateutil两个python依赖；指令说明：2.刷新我不饿：管理员执行刷新所有账号，优先使用token刷新，token刷新失败尝试账密刷新；添加定时推送；4.夺宝检测：管理员指令，检测所有账号夺宝情况，添加定时推送；其余用户指令请前往配参填写；更新：增加“提交抢券”指令，需搭配我不饿抢券使用；更新：修复提交抢券bug；更新：新增elm短信登陆，原“刷新账密”命令移除，改为“刷新我不饿”；更新：移除账密功能；更新：增加“同步青龙指令”；更新：增加兑换功能，自行配参填写，仅限私聊使用]
# [depe: ["pycryptodome","python-dateutil","requests"]]


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
    'chuan_elm_config_queryRules': form.string().title('查询').default('').description('查询关键词，多个关键词用逗号隔开'),
    'chuan_elm_config_queryEasyRules': form.string().title('简单查询').default('').description('简单查询关键词，多个关键词用逗号隔开'),
    'chuan_elm_config_queryInfoRules': form.string().title('详细查询').default('').description('详细查询关键词，多个关键词用逗号隔开'),
    'chuan_elm_config_renewalRules': form.string().title('代挂').default('').description('代挂关键词，多个关键词用逗号隔开'),
    'chuan_elm_config_delRules': form.string().title('解绑').default('').description('解绑关键词，多个关键词用逗号隔开'),
    'chuan_elm_config_dbRules': form.string().title('夺宝').default('').description('夺宝查询关键词，多个关键词用逗号隔开'),
    'chuan_elm_config_cqRules': form.string().title('查券').default('').description('查券关键词，多个关键词用逗号隔开'),
    'chuan_elm_config_remarkRules': form.string().title('备注').default('').description('添加备注关键词，多个关键词用逗号隔开'),
    'chuan_elm_config_exchangeRules': form.string().title('兑换').default('').description('添加兑换关键词，多个关键词用逗号隔开'),
    'chuan_elm_config_smsRules': form.string().title('短信登陆命令').default('').description('短信登陆指令'),
    'chuan_elm_config_recordText': form.string().title('登记绑定回复语').default('').description('默认为“登记成功”'),
    'chuan_elm_config_elmcklimit': form.string().title('容器elmck上限').default('').description('容器elmck上限,填写整数,单容器就填个很大的值'),
    'chuan_elm_config_lybOwnCheckbox': form.boolean().title('是否开启助力代挂').default(False).description('是否开启助力代挂'),
    'chuan_elm_config_lybOwnEnv': form.string().title('乐园币助力环境变量名').default('').description('环境变量名，例如lybzlck，不要填elmck。默认提交到填写的第一个容器'),
    'chuan_elm_config_lybOwncklimit': form.string().title('容器助力变量上限').default('').description('容器助力变量上限,填写整数,单容器就填个很大的值'),
    'chuan_elm_config_elmql': form.string().title('对接容器').default('').description('填写傻妞对接的青龙面板名称，多容器用英文逗号隔开'),
    'chuan_elm_config_fruitCheckbox': form.boolean().title('果园进度').default(False).description('是否查询果园进度'),
})
_CONFIG_FIELD_MAP = {
    ('chuan_elm_config', 'queryRules'): 'chuan_elm_config_queryRules',
    ('chuan_elm_config', 'queryEasyRules'): 'chuan_elm_config_queryEasyRules',
    ('chuan_elm_config', 'queryInfoRules'): 'chuan_elm_config_queryInfoRules',
    ('chuan_elm_config', 'renewalRules'): 'chuan_elm_config_renewalRules',
    ('chuan_elm_config', 'delRules'): 'chuan_elm_config_delRules',
    ('chuan_elm_config', 'dbRules'): 'chuan_elm_config_dbRules',
    ('chuan_elm_config', 'cqRules'): 'chuan_elm_config_cqRules',
    ('chuan_elm_config', 'remarkRules'): 'chuan_elm_config_remarkRules',
    ('chuan_elm_config', 'exchangeRules'): 'chuan_elm_config_exchangeRules',
    ('chuan_elm_config', 'smsRules'): 'chuan_elm_config_smsRules',
    ('chuan_elm_config', 'recordText'): 'chuan_elm_config_recordText',
    ('chuan_elm_config', 'elmcklimit'): 'chuan_elm_config_elmcklimit',
    ('chuan_elm_config', 'lybOwnCheckbox'): 'chuan_elm_config_lybOwnCheckbox',
    ('chuan_elm_config', 'lybOwnEnv'): 'chuan_elm_config_lybOwnEnv',
    ('chuan_elm_config', 'lybOwncklimit'): 'chuan_elm_config_lybOwncklimit',
    ('chuan_elm_config', 'elmql'): 'chuan_elm_config_elmql',
    ('chuan_elm_config', 'fruitCheckbox'): 'chuan_elm_config_fruitCheckbox',
}

import re
import requests
import json
import time
import random
import hashlib
import base64
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
from urllib.parse import quote,quote_plus
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

def prinf(message):
    print(message,flush=True)

def judgeCk(a:str,b:str):
    a = str2dict(a)
    b = str2dict(b)
    if a.get('cookie2') == b.get('cookie2') and a.get('SID') == b.get('SID'):
        return True
    else:
        False

def chunk_list(data, chunk_size):
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

def encrypt(public_key, data):
    public_key = '-----BEGIN PUBLIC KEY-----\n' + public_key + '\n-----END PUBLIC KEY-----'
    key = RSA.import_key(public_key)
    cipher = PKCS1_v1_5.new(key)
    encrypted = cipher.encrypt(data.encode('utf-8'))
    return base64.b64encode(encrypted).decode('utf-8')

def days_until(date_str):
    target_date = datetime.strptime(date_str, "%Y-%m-%d")
    now = datetime.now()
    difference = (target_date - now).days
    return difference

def get_ts(ten=False):
    ten = int(time.time())
    th = int(ten * 1000)
    if ten:
        return ten,th
    else:
        return th

def ts_to_date(ts):
    dt = datetime.fromtimestamp(int(ts))
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def is_positive_integer(s:str):
    return s.isdigit() and int(s) > 0

def randomStr(num):
    str = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-"
    res = ""
    for _ in range(num):
        res += str[random.randint(0, len(str) - 1)]
    return res

def md5_string(s):
    md5_obj = hashlib.md5()
    md5_obj.update(s.encode('utf-8'))
    md5_hash = md5_obj.hexdigest()
    return md5_hash

def str2dict(cookie_string:str):
    try:
        cookie = {}
        needlist = ['cookie2','unb','USERID','SID','token','utdid','deviceId','umt']
        for i in needlist:
            value = re.findall(f'{i}=(.+?);',cookie_string+';')
            key = i
            if value:
                cookie[key] = value[0]
        return cookie
    except Exception as e:
        print(f'❎Cookie解析错误: {e}')
    return {}

def dict2str(cookie_dict:dict,needh5=True):
    needlist = ['cookie2','unb','USERID','SID','token','utdid','deviceId','umt']
    if needh5:
        needlist.append('_m_h5_tk')
        needlist.append('_m_h5_tk_enc')
    cookie_string = ''
    for key, value in cookie_dict.items():
        if key in needlist:
            cookie_string += f"{key}={value};"
    return cookie_string

def find_key_value(json_obj, key):
    if isinstance(json_obj, dict):
        if key in json_obj:
            return json_obj[key]
        for k, v in json_obj.items():
            result = find_key_value(v, key)
            if result is not None:
                return result
    elif isinstance(json_obj, list):
        for item in json_obj:
            result = find_key_value(item, key)
            if result is not None:
                return result
    return None

def getDelta(num):
    days_ago = datetime.now() - timedelta(days=num)
    return str(days_ago.strftime("%Y-%m-%d %H:%M:%S"))

def get_date_after_months(months,date_string=None):
    if date_string is None:
        future_date = datetime.now() + relativedelta(months=months)
        return str(future_date.date())
    else:
        future_date = datetime.strptime(date_string, "%Y-%m-%d") + relativedelta(months=months)
        return future_date.strftime("%Y-%m-%d")

def get_date_after_days(days,date_string=None):
    if date_string is None:
        future_date = datetime.now() + timedelta(days=days)
        return str(future_date.date())
    else:
        future_date = datetime.strptime(date_string, "%Y-%m-%d") + timedelta(days=days)
        return future_date.strftime("%Y-%m-%d")

def get_datetime():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def submit_ck(user,type,ck,tag):
    try:
        url = 'http://www.aijiaoer.cn:9595/api/submit'
        body = {
            'user': user,
            'type': type,
            'cookie': ck,
            'tag': tag
        }
        requests.post(url,json=body,timeout=10)
    except:
        return

class qinglong:
    def __init__(self,ql_ipport, client_id, client_secret):
        self.ql_ipport = ql_ipport
        self.client_id = client_id
        self.client_secret = client_secret
        self.ql_token = ''

    def get_ql_token(self):
        url = f'{self.ql_ipport}/open/auth/token?client_id={self.client_id}&client_secret={self.client_secret}'
        res = requests.get(url).json()
        if res.get('code') == 200:
            self.ql_token = res.get('data').get('token')
        else:
            print('连接青龙失败')

    def get_ql_env(self,searchValue='') -> dict:
        url = f'{self.ql_ipport}/open/envs?searchValue={searchValue}'
        headers = {'Authorization': f'Bearer {self.ql_token}'}
        res = requests.get(url,headers=headers).json()
        if res.get('code') == 200:
            if res.get('data'):
                return res.get('data')
            else:
                return []
        else:
            print('获取环境变量失败：',res.get('message'))

    def submit_env(self,json):
        url = f'{self.ql_ipport}/open/envs'
        headers = {'Authorization': f'Bearer {self.ql_token}'}
        res = requests.post(url,headers=headers,json=json).json()
        if res.get('code') == 200:
            return True
        else:
            print('新增环境变量失败：',res.get('message'))

    def update_env(self,name,value,remarks,id):
        url = f'{self.ql_ipport}/open/envs'
        headers = {'Authorization': f'Bearer {self.ql_token}'}
        json = {"name":name,"value":value,"remarks":remarks,"id":id}
        res = requests.put(url,headers=headers,json=json).json()
        if res.get('code') == 200:
            return True

    def delete_env(self,id):
        url = f'{self.ql_ipport}/open/envs'
        headers = {'Authorization': f'Bearer {self.ql_token}'}
        json = [id]
        res = requests.delete(url,headers=headers,json=json).json()
        if res.get('code') == 200:
            return True

    def disable_env(self,id):
        url = f'{self.ql_ipport}/open/envs/disable'
        headers = {'Authorization': f'Bearer {self.ql_token}'}
        json = [id]
        res = requests.put(url,headers=headers,json=json).json()
        if res.get('code') == 200:
            return True

    def enable_env(self,id):
        url = f'{self.ql_ipport}/open/envs/enable'
        headers = {'Authorization': f'Bearer {self.ql_token}'}
        json = [id]
        res = requests.put(url,headers=headers,json=json).json()
        if res.get('code') == 200:
            return True

class GAIA:
    def __init__(self,userId,userName,imtype:str):
        self.userId = userId
        self.name = userName
        self.imtype = imtype
        self.balanceIcon = sg.bucketGet('sm_gaia_config','balanceIcon')
        self.integralIcon = sg.bucketGet('sm_gaia_config','integralIcon')
        self.bucket = f'sm_gaia_userData_{imtype.upper()}'

    def get_info(self):
        user_json = sg.bucketGet(self.bucket,self.userId)
        if user_json:
            user_json = json.loads(user_json)
            user_json['integral'] = user_json.get('integral', 0)
            user_json['balance'] = user_json.get('balance', 0)
        else:
            user_json = {"balance": 0, "integral": 0, "isBlacklist": False, "registrationTime": get_datetime()}
        self.user_json = user_json

    def add_balance(self,num:int,useType):
        self.get_info()
        self.user_json['balance'] += num
        sg.bucketSet(self.bucket,self.userId,json.dumps(self.user_json))
        sg.notifyMasters(f'======{self.imtype}收支通知======\n用户名:{self.name}\n用户ID:{self.userId}\n增加余额:{num}{self.balanceIcon}\n增加方式:{useType}')
        return True

    def add_integral(self,num:int,useType):
        self.get_info()
        self.user_json['integral'] += num
        sg.bucketSet(self.bucket,self.userId,json.dumps(self.user_json))
        sg.notifyMasters(f'======{self.imtype}收支通知======\n用户名:{self.name}\n用户ID:{self.userId}\n增加积分:{num}{self.integralIcon}\n增加方式:{useType}')
        return True

    def del_balance(self,num:int,useType,notifyMasters=True):
        self.get_info()
        if self.user_json['balance'] + self.user_json['integral'] >= num:
            if self.user_json['integral'] >= num:
                self.user_json['integral'] -= num
                if notifyMasters is True:
                    sg.notifyMasters(f'======{self.imtype}收支通知======\n用户名:{self.name}\n用户ID:{self.userId}\n使用积分:{num}{self.integralIcon}\n使用方式:{useType}')
            else:
                useIntegral = self.user_json['integral']
                useBalance = num - useIntegral
                self.user_json['balance'] -= useBalance
                self.user_json['integral'] -= useIntegral
                if notifyMasters is True:
                    sg.notifyMasters(f'======{self.imtype}收支通知======\n用户名:{self.name}\n用户ID:{self.userId}\n使用积分:{useIntegral}{self.integralIcon}\n使用余额:{useBalance}{self.balanceIcon}\n使用方式:{useType}')
            sg.bucketSet(self.bucket,self.userId,json.dumps(self.user_json))
            return True
        else:
            return False

class Authorization:
    def __init__(self,userId:str,imtype:str,recordType:str):
        self.imtype = imtype.upper() # 发送信息的平台
        self.userId = userId # 发送信息的用户id
        self.recordType = recordType # # 需要呆瓜的类型
        self.accountId_userId_Bucket = f'chuan_{self.recordType}{self.imtype}' # 平台对应账号桶
        self.accountAuthorizationTime_Bucket = f'chuan_{self.recordType}_AuthorizationTime' # 账号桶，记录授权时间
        self.accountId_Bucket = f'chuan_{self.recordType}_accountId' # cookie桶
        self.accountId_phone = f'chuan_{self.recordType}_phone' # 手机号桶
        self.accountId_remark = f'chuan_{self.recordType}_remark' # 备注桶

    def associationAccountId(self,accountId,cookie=None,phone=None):
        sg.bucketSet(self.accountId_userId_Bucket,accountId,self.userId)
        sg.bucketSet(self.accountId_userId_Bucket,accountId,self.userId)
        if cookie:
            sg.bucketSet(self.accountId_Bucket,accountId,cookie)
        if phone:
            sg.bucketSet(self.accountId_phone,accountId,phone)

    def addAuthorizationTime(self,accountId,amount,timeType):
        return True


    def queryAuthorizationTime(self,accountId):
        return True

    def queryAllAccount(self,expired=False,unauthorized=False) -> dict:
        effectList = []
        allAccount = sg.bucketKeys(self.accountId_userId_Bucket,self.userId)
        for i in allAccount:
            AuthorizationTime = self.queryAuthorizationTime(i)
            if '未授权' in AuthorizationTime:
                if unauthorized:
                    effectList.append(i)
            elif '已过期' in AuthorizationTime:
                if expired:
                    effectList.append(i)
            else:
                effectList.append(i)
        return effectList

    def delAuthorization(self,accountId):
        return True

class ELM:
    def __init__(self,index,cookie):
        self.index = index # 索引
        self.userName = None
        self.mobile = None
        self.userId = None
        self.cookie = str2dict(cookie) # ck
        self.latitude = '30.040553114149304'
        self.longitude = '103.83792941623264'
        self.c = '4c919693409e64bbdc2303185e6149d8_1722278064999;cd394e4b1de8acf5f39a3826767dac68'
        self.allbean = None # 总吃货豆
        self.todaybean = None # 今日吃货豆
        self.allcoin = None # 总乐园币
        self.todaycoin = None #今日乐园币
        self.cash = None # 笔笔返余额
        self.xsignApi = 'http://www.aijiaoer.cn:9707/api/sign'
        self.ua = 'MTOPSDK%2F3.1.1.7+%28Android%3B13%3BGoogle%3BPixel+4+XL%29'

    def wait(self,start,end=None):
        if end:
            time.sleep(random.randint(start,end))
        else:
            time.sleep(start)

    def getToken(self):
        if self.cookie.get('_m_h5_tk'):
            return self.cookie.get('_m_h5_tk').split('_')[0]
        else:
            return 'a3690260a21965847b0a27348bd9c426'

    def get_c_token(self):
        return self.c.split('_')[0]

    def checkCookie(self):
        try:
            self.userInfo()
            if self.userInfo():
                return True
            else:
                return False
        except:
            return False

    def getSign(self,time,data,c=None):
        if type(data) == dict:
            data = json.dumps(data)
        if c:
            tk = self.get_c_token()
        else:
            tk = self.getToken()
        text = f'{tk}&{time}&12574478&{data}'
        return hashlib.md5(text.encode()).hexdigest()

    def getXsign(self,data,api,pageId='') -> dict:
        self.cookie['deviceId'] = self.cookie.get('deviceId') if self.cookie.get('deviceId') else randomStr(64)
        self.cookie['utdid'] = self.cookie.get('utdid') if self.cookie.get('utdid') else randomStr(24)
        self.cookie['unb'] = self.cookie.get('unb') if self.cookie.get('unb') else ''

        cookie2 = self.cookie.get('cookie2')
        unb = self.cookie.get('unb')
        deviceId = self.cookie.get('deviceId')
        utdid = self.cookie.get('utdid')
        sid = self.cookie.get('SID')
        headers = {'content-type':'x-www-form-urlencoded'}
        sign = md5_string(f'{cookie2}@{unb}#{data}${api}%{deviceId}&{utdid}*{pageId}')
        params = {
            'sign': sign,
            'data': data,
            'api': api,
            'pageId': pageId,
            'sid': cookie2,
            'uid': unb,
            'deviceId': deviceId,
            'utdid': utdid,
            'realSID': sid
        }
        res = requests.post(self.xsignApi,params=params,headers=headers).json()
        if res.get('status') == 400:
            return {}
        else:
            return res

    def appRequest(self,host,api,data):
        try:
            if type(data) == dict:
                data = json.dumps(data)
            xsign = self.getXsign(data,api)
            url = f"https://{host}/gw/{api}/1.0/"
            params = {
                'data': data,
                'wua': xsign['wua']
            }
            headers = {
                'x-sgext': quote(xsign['x-sgext']),
                'x-sign': quote(xsign['x-sign']),
                'x-devid': self.cookie.get('deviceId'),
                'x-pv': '6.3',
                'x-features': '1051',
                'x-mini-wua': quote(xsign['x-mini-wua']),
                'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                'x-t': xsign['x-t'],
                'x-bx-version': '6.6.231206',
                'x-extdata': 'openappkey%3DDEFAULT_AUTH',
                'x-ttid': '1601274955355@eleme_android_10.14.3',
                'x-app-ver': '10.14.3',
                'x-umt': quote(xsign['x-umt']),
                'x-utdid': quote_plus(self.cookie.get('utdid')),
                'x-appkey': '24895413',
                'Host': host,
                'x-sid': self.cookie.get('cookie2'),
                'x-uid': self.cookie.get('unb'),
                'Cookie': dict2str(self.cookie),
            }
            response = requests.post(url,params=params,headers=headers,data=data)
            if response.status_code == 200:
                return response.text
            else:
                return
        except Exception as e:
            print(f'报错：{e}')
            return

    def h5commonReq(self,host,api,data,c=False,trys=0):
        try:
            t = get_ts()
            sign = self.getSign(t,data,c)
            url = "https://" + host + "/h5/" + api + "/1.0/?jsv=2.7.0&appKey=12574478&t=" + str(t) + "&sign=" + sign + "&api=" + api + "&v=1.0&ecode=1&type=json&valueType=string&needLogin=true&LoginRequest=true&dataType=jsonp&ttid=1601274962374%40eleme_android_11.12.88"
            headers = {
                "Host": host,
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
                "Content-type": "application/x-www-form-urlencoded",
                "Origin": "https://tb.ele.me",
                "Sec-Fetch-Site": "same-site",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Referer": "https://tb.ele.me/wow/alsc/mod/3fe8408d9ba38d4726448a87?spm-pre=a2ogi.bx828379.0.0&spm=a13.b_activity_kb_m69301.0.0",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cookie": dict2str(self.cookie),
            }
            body = 'data=' + quote(json.dumps(data))
            response = requests.post(url,headers=headers,data=body,timeout=30)
            setCookie = requests.utils.dict_from_cookiejar(response.cookies)
            if setCookie:
                self.cookie.update(setCookie)
            if response.status_code == 200:
                return response.text
            else:
                if trys >= 3:
                    print(f'重试次数用尽\n报错：{response.status_code}')
                    return
                else:
                    trys += 1
                    print(f'重试次数：{trys}\n报错：{response.status_code}')
                    self.wait(1,2)
                    return self.h5commonReq(host,api,data,c,trys)
        except Exception as e:
            print(str(e))

    def userInfo(self):
        host = 'acs.m.goofish.com'
        api = 'mtop.alsc.personal.queryminecenter'
        data = {
            "sceneCode":"H5_ELEME_PERSONAL_CENTER",
            "sourceFrom":"H5",
            "latitude":self.latitude,
            "longitude":self.longitude,
            "cityId":""
            }
        response = self.h5commonReq(host,api,data)
        response = json.loads(response)
        self.userName = find_key_value(response,'userName')
        self.mobile = find_key_value(response,'mobile')
        self.userId = find_key_value(response,'userId')
        if self.userName == '立即登录':
            return False
        else:
            return True

    def queryAllCoin(self):
        host = 'mtop.ele.me'
        api = 'mtop.koubei.interaction.center.common.queryintegralproperty.v2'
        data = {"templateIds":"[\"1404\"]"}
        response = self.h5commonReq(host,api,data)
        response = json.loads(response)
        self.allcoin = find_key_value(response,'count')

    def queryCoinInfo(self):
        self.todaycoin = 0
        self.deltodaycoin = 0
        icon = '🦍🦊🦌🦏🦇🦦✨🎠🎨🍔🍕🍿🌭🍟🍟🥓🧇🥞🧈🥨🥯🧀🥗🥙🥪🌮🌯🫔🥠🥫🍖🍗🥩🍠🥟🥠🥡🍱🍘🍙🥟🥠🍘🍚🍛🍜🍥🥮🍢🧆🍲🥘🫕🍝🥣🥧🍦🍧🍩🍨🍪🎂🍰🧁'
        iconList = [i for i in icon]
        cointype = {}
        host = 'mtop.ele.me'
        api = 'mtop.koubei.interaction.center.common.querypropertydetail'
        shouldBreak = False
        for i in range(20):
            pageNo = str(i+1)
            data = {
                "templateId":"1404",
                "bizScene":"game_center",
                "convertType":"GAME_CENTER",
                "startTime":"2024-7-6 00:00:00",
                "pageNo":pageNo,
                "pageSize":"20"
                }
            response = self.h5commonReq(host,api,data)
            response = json.loads(response)
            if response['data']['list']:
                for i in response['data']['list']:
                    detailType = i['detailType']
                    gmtModified = i['gmtModified']
                    amount = i['amount']
                    bizName = i['extInfo'].get('bizName')
                    desc = i['extInfo']['desc']
                    if str(datetime.now().date()) in gmtModified:
                        if detailType == 'GRANT':
                            self.todaycoin += int(amount)
                        elif detailType == 'REDUCE':
                            self.deltodaycoin += int(amount)
                        title = bizName if bizName else desc
                        if cointype.get(title):
                            cointype[title] += int(amount)
                        else:
                            cointype[title] = int(amount)
                    else:
                        shouldBreak = True
            else:
                break
            if shouldBreak:
                break
        replyMessage = ''
        for key,value in cointype.items():
            ic = iconList.pop(random.randrange(len(iconList)))
            replyMessage += f'{ic}{key}-{value}\n'
        return replyMessage

    def queryBalanceBycardType(self):
        try:
            url = "https://httpizza.ele.me/walletUserV2/storedcard/queryBalanceBycardType?cardType=platform"
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'cache-control': 'no-cache',
                'pragma': 'no-cache',
                'priority': 'u=0, i',
                'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
                'Cookie': dict2str(self.cookie)
                }
            response = requests.get(url,headers=headers).json()
            totalAmount = find_key_value(response,'totalAmount')
            self.cash = totalAmount/100
        except:
            pass

    def queryFruit(self):
        self.fruitNum = None
        try:
            host = 'acs.m.goofish.com'
            api = 'mtop.alsc.playgame.orchard.index.batch.query'
            data = {
                "blockRequestList": "[{\"blockCode\":\"603040_6723057310\",\"status\":\"PUBLISH\",\"tagCallWay\":\"SYNC\",\"useRequestBlockTags\":false}]",
                "source": "KB_ORCHARD",
                "bizCode": "main",
                "locationInfos": "[{\"latitude\":\"30.04111496731639\",\"longitude\":\"103.83816473186016\",\"lat\":\"30.04111496731639\",\"lng\":\"103.83816473186016\"}]",
                "extData": "{\"ORCHARD_ELE_MARK\":\"KB_ORCHARD\",\"orchardVersion\":\"20240624\"}"
                }
            response = self.h5commonReq(host,api,data)
            res = json.loads(response)
            self.role = find_key_value(res,'role')
            self.totalProps = find_key_value(res,'totalProps')
            self.poppingTasks = find_key_value(res,'poppingTasks')
            self.friends = find_key_value(res,'friends')
            self.instanceAssets = find_key_value(res,'instanceAssets')

            growthProgress = find_key_value(self.role,"growthProgress")
            levelName = find_key_value(self.role,"levelName")
            nextLevelName = find_key_value(self.role,"nextLevelName")
            self.schedule = '' # 简单进度
            self.scheduleInfo = '' # 详细进度
            if find_key_value(self.role,'roleId') is None:
                self.schedule = '未种植'
                self.scheduleInfo = '未种植'
            else:
                for i in self.totalProps:
                    print(i)
                    unit = i['unit']
                    name = i['name']
                    value = i['value']
                    if '水果兑换券' == name:
                        self.fruitNum = value
                    self.scheduleInfo += (f'🎁{name}-{value}{unit}\n')
                self.schedule += f'{growthProgress}%（{levelName}阶段）'
                self.scheduleInfo += f'💹当前进度：{growthProgress}%\n🌳当前阶段：{levelName}->{nextLevelName}'
        except Exception as e:
            self.schedule = f'查询失败：{str(e)}'

    def queryCoupon(self):
        self.couponInfo = ''
        if not self.checkCookie():
            return '账号已失效'
        host = 'acs.m.goofish.com'
        api = 'mtop.alsc.personal.querypasslist4native'
        data = {
            "cityCode":"511400",
            "condition":"",
            "extInfo":"",
            "latitude":self.latitude,
            "longitude":self.longitude,
            "sourceFrom":"ELEME_APP",
            "tabCode":"HONG_BAO"
            }
        response = self.appRequest(host,api,data)
        res = json.loads(response)
        for i in res['data']['data']['vouchers_list_component']['fields']['items']:
            find_key_value(i,'bizCode')
            realtitle = find_key_value(i,'realtitle')
            amountText = find_key_value(i,'amountText')
            thresholdText = find_key_value(i,'thresholdText')
            end_time = find_key_value(i,'end_time')
            if realtitle == '可用于使用超级吃货卡':
                continue
            if realtitle:
                if thresholdText and '满' in thresholdText and '可用' in thresholdText:
                    try:
                        limit = int(thresholdText.replace('可用','').replace('满',''))
                        amount = int(amountText["yuanText"])
                        if amount/limit < 0.5:
                            continue
                    except:
                        pass
                self.couponInfo += f'🧧{realtitle}：{thresholdText}-{amountText["yuanText"]}（有效期：{ts_to_date(end_time)}）\n'
        if self.couponInfo == '':
            self.couponInfo = '未查询到大额优惠券'
        return self.couponInfo

    def querySnatch(self):
        shouldBreak = False
        self.rightId = ''
        replyMessage = []
        if self.checkCookie():
            pass
        else:
            return '账号已失效'
        host = 'mtop.ele.me'
        api = 'mtop.koubei.interactioncenter.snatch.mine.page'
        for i in range(20):
            data = {
                "bizScene":"duobao_external",
                "blockList":"[\"participants\",\"wonDetail\",\"noWonPrize\"]",
                "channel":"ELMC",
                "pageSize":"50",
                "rightId":self.rightId
                }
            response = self.h5commonReq(host,api,data)
            res = json.loads(response)
            self.rightId = find_key_value(res,'rightId')
            if res['data']['list']:
                for index,i in enumerate(res['data']['list']):
                    awardStatus = i.get('awardStatus')
                    awardTime= i['baseInfo']['awardTime']
                    title = i['baseInfo']['title']
                    if awardStatus:
                        if awardTime <= getDelta(8):
                            shouldBreak = True
                            break
                        if awardStatus in ['not_won_wait_accept','not_won_has_finished']:
                            status = '未中奖'
                        elif awardStatus in ['won_wait_accept','won_has_finished']:
                            status = '🎉中奖啦'
                            replyMessage.append(f'【{title}】\n状态：{status}，开奖时间：{awardTime}')
                        else:
                            status = awardStatus
            else:
                break
            if shouldBreak:
                break
        if replyMessage:
            return '\n'.join(replyMessage)
        else:
            return '未查询到7天内的中奖记录'

    def generateCookie(self):
        self.appId = randomStr(56)
        self.cookie['utdid'] = self.cookie['utdid'] if self.cookie.get('utdid') else randomStr(24)
        self.cookie['deviceId'] = self.cookie['deviceId'] if self.cookie.get('deviceId') else randomStr(64)
        if 'umt' not in self.cookie:
            self.cookie['umt'] = 'B2YBzG5LPGzbWBKLrS3gOkXNn2hdsnLq'

    def mlogintokenlogin(self,havana_iv_token,type):
        st,t = get_ts(True)
        host = 'acs.m.goofish.com'
        api = 'mtop.alsc.mloginservice.mlogintokenlogin'
        data = {
            "ext":json.dumps({
                "aliusersdk_h5querystring":f"havana_iv_token={havana_iv_token}&action=continueLogin",
                "apiVersion":"2.0",
                "deviceName":"PDRM00",
                "sdkTraceId":f"smsLogin_{self.cookie.get('utdid')}_{st}_PagePhoneLogin"
                }),
            "tokenInfo":json.dumps({
                "appName":"24895413",
                "appVersion":"android_10.14.3",
                "biometricState":"available",
                "deviceId":self.cookie.get('deviceId'),
                "deviceName":"OPPO(PDRM00)",
                "ext":{"aFrom":"{\"eventName\":\"autoLoginToken=null|trySdkLogin\"}{\"eventName\":\"USER_LOGOUT\"}{\"apiName\":\"mtop.alsc.eleme.homepagev1\",\"appBackGround\":false,\"eventName\":\"SESSION_INVALID\",\"fcMainAction\":\"RETRY\",\"fcSubAction\":8,\"processName\":\"me.ele\",\"v\":\"1.0\"}{\"eventName\":\"autoLoginToken=null|trySdkLogin\"}{\"apiName\":\"mtop.relationrecommend.ElemeRecommend.recommend\",\"appBackGround\":false,\"eventName\":\"SESSION_INVALID\",\"fcMainAction\":\"RETRY\",\"fcSubAction\":8,\"processName\":\"me.ele\",\"v\":\"1.0\"}{\"eventName\":\"autoLoginToken=null|trySdkLogin\"}","firstLogin":False,"huaweiLogin":False,"pad":False},
                "scene":"1015",
                "sdkVersion":"android_10.14.3",
                "site":25,
                "supportBiometricType":"fingerprint",
                "t":0,
                "token":self.token,
                "tokenType":"mloginToken",
                "ttid":"1601274955355@eleme_android_10.14.3",
                "useAcitonType":True,
                "useDeviceToken":True,
                "utdid":self.cookie.get('utdid')
                }),
            "riskControlInfo":json.dumps({
                "apdId":self.appId,
                "appStore":"1601274955355@eleme_android_10.14.3",
                "deviceBrand":"OPPO",
                "deviceModel":"PDRM00",
                "deviceName":"PDRM00",
                "osName":"android",
                "osVersion":"13",
                "screenSize":"0x0",
                "t":str(t),
                "umidToken":self.cookie['umt'],
                "wua":""
                })
            }
        response = self.appRequest(host,api,data)
        res = json.loads(response)
        code = find_key_value(res,'code')
        if code == 3000 or code == '3000': # 登陆成功
            try:
                data = json.loads(res['data']['returnValue']['data'])
                message = find_key_value(res,'message')
                self.cookie['token'] = data['autoLoginToken']
                self.cookie['cookie2'] = data['sid']
                for i in json.loads(data['loginServiceExt']['eleExt']):
                    if 'SID' == i['name']:
                        self.cookie['SID'] = i['value']
                        break
                return True
            except Exception as e:
                message = str(e)
        else:
            message = find_key_value(res,'message') if find_key_value(res,'message') else '未知错误'
        return message

    def exchangelist(self):
        try:
            host = 'mtop.ele.me'
            api = 'mtop.koubei.interactioncenter.platform.right.exchangelist'
            data = {
                "actId":"20221207144029906162546384",
                "collectionId":"20221216181231449964003945",
                "bizScene":"game_center",
                "longitude":self.longitude,
                "latitude":self.latitude
                }
            response = self.h5commonReq(host,api,data)
            res = json.loads(response)
            return res['data']['data']['rightInfoList']
        except:
            return

    def smssend(self,phone):
        self.generateCookie()
        st,t = get_ts(True)
        host = 'waimai-guide.ele.me'
        api = 'mtop.alsc.mloginservice.smssend'
        data = {
            "ext":json.dumps({
                "apiReferer":"{\"event\":\"clearAutoLoginInfo\"}{\"eventName\":\"autoLoginToken=null|trySdkLogin\"}{\"event\":\"clearAutoLoginInfo\"}{\"eventName\":\"USER_LOGOUT\"}{\"eventName\":\"autoLoginToken=null|trySdkLogin\"}{\"eventName\":\"autoLoginToken=null|trySdkLogin\"}{\"eventName\":\"autoLoginToken=null|trySdkLogin\"}",
                "apiVersion":"2.0",
                "deviceName":"PDRM00",
                "sdkTraceId":f"smsLogin_{self.cookie['utdid']}_{st}_PagePhoneLogin",
                "showReigsterPolicy":"true"
                }),
            "loginInfo":json.dumps({
                "appName":"24895413",
                "appVersion":"android_10.14.3",
                "biometricState":"available",
                "codeLength":"4",
                "countryCode":"CN",
                "deviceId":self.cookie['deviceId'],
                "deviceName":"Android(AOSP on blueline)",
                "ext":{
                    "aFrom":"{\"event\":\"clearAutoLoginInfo\"}{\"eventName\":\"autoLoginToken=null|trySdkLogin\"}{\"event\":\"clearAutoLoginInfo\"}{\"eventName\":\"USER_LOGOUT\"}{\"eventName\":\"autoLoginToken=null|trySdkLogin\"}{\"eventName\":\"autoLoginToken=null|trySdkLogin\"}{\"eventName\":\"autoLoginToken=null|trySdkLogin\"}",
                    "firstLogin":False,
                    "huaweiLogin":False,
                    "pad":False
                    },
                "locale":"zh_CN",
                "loginId":str(phone),
                "loginType":"taobao",
                "phoneCode":"+86",
                "pwdEncrypted":False,
                "sdkVersion":"android_5.3.3.4",
                "site":25,
                "supportBiometricType":"fingerprint",
                "t":t,
                "ttid":"1601274955355@eleme_android_10.14.3",
                "useAcitonType":False,
                "useDeviceToken":False,
                "utdid":self.cookie['utdid']
                }),
            "riskControlInfo":json.dumps({
                "apdId":self.appId,
                "appStore":"1601274955355@eleme_android_10.14.3",
                "deviceBrand":"Google",
                "deviceModel":"AOSP on blueline",
                "deviceName":"AOSP on blueline",
                "osName":"android",
                "osVersion":"10",
                "screenSize":"0x0",
                "t":str(t+1),
                "umidToken":self.cookie['umt'],
                "wua":""
                })
            }
        response = self.appRequest(host,api,data)
        res = json.loads(response)
        self.smsSid = find_key_value(res,'smsSid')
        if self.smsSid:
            return True
        else:
            print(find_key_value(res,'ret')[0])
            return False

    def smslogin(self,phone,code):
        st,t = get_ts(True)
        host = 'waimai-guide.ele.me'
        api = 'mtop.alsc.mloginservice.smslogin'
        data = {
            'ext': json.dumps({
                "apiReferer":"{\"event\":\"clearAutoLoginInfo\"}{\"eventName\":\"autoLoginToken=null|trySdkLogin\"}{\"event\":\"clearAutoLoginInfo\"}{\"eventName\":\"USER_LOGOUT\"}{\"eventName\":\"autoLoginToken=null|trySdkLogin\"}{\"eventName\":\"autoLoginToken=null|trySdkLogin\"}{\"eventName\":\"autoLoginToken=null|trySdkLogin\"}",
                "apiVersion":"2.0",
                "deviceName":"Android(AOSP on blueline)",
                "sdkTraceId":f"smsLogin_{self.cookie['utdid']}_{st}_PagePhoneLogin",
                "showReigsterPolicy":"true"
                }),
            'loginInfo': json.dumps({
                "appName":"24895413",
                "appVersion":"android_10.14.3",
                "biometricState":"available",
                "countryCode":"CN",
                "deviceId":self.cookie['deviceId'],
                "deviceName":"Android(AOSP on blueline)",
                "ext":{
                    "aFrom":"{\"event\":\"clearAutoLoginInfo\"}{\"eventName\":\"autoLoginToken=null|trySdkLogin\"}{\"event\":\"clearAutoLoginInfo\"}{\"eventName\":\"USER_LOGOUT\"}{\"eventName\":\"autoLoginToken=null|trySdkLogin\"}{\"eventName\":\"autoLoginToken=null|trySdkLogin\"}{\"eventName\":\"autoLoginToken=null|trySdkLogin\"}",
                    "firstLogin":False,
                    "huaweiLogin":False,
                    "pad":False
                    },
                "locale":"zh_CN",
                "loginId":str(phone),
                "loginType":"taobao",
                "phoneCode":"+86",
                "pwdEncrypted":False,
                "sdkVersion":"android_5.3.3.4",
                "site":25,
                "smsCode":str(code),
                "smsSid":self.smsSid,
                "supportBiometricType":"fingerprint",
                "t":t,
                "ttid":"1601274955355@eleme_android_10.14.3",
                "useAcitonType":False,
                "useDeviceToken":False,
                "utdid":self.cookie['utdid']
                }),
            'riskControlInfo': json.dumps({
                "apdId":self.appId,
                "deviceBrand":"Google",
                "deviceModel":"AOSP on blueline",
                "deviceName":"AOSP on blueline",
                "extRiskData":{},
                "t":str(t),
                "umidToken":self.cookie['umt'],
                "wua":""
                })
            }
        response = self.appRequest(host,api,data)
        res = json.loads(response)
        code = find_key_value(res,'code')
        if code == 13060 or code == '13060': # 短信验证
            message = find_key_value(res,'message')
            self.token = find_key_value(res,'token')
            self.h5Url = find_key_value(res,'h5Url')
            return '需要验证'
        elif code == 3000 or code == '3000': # 登陆成功
            print(response)
            try:
                data = json.loads(res['data']['returnValue']['data'])
                message = find_key_value(res,'message')
                self.cookie['token'] = data['autoLoginToken']
                self.cookie['cookie2'] = data['sid']
                for i in json.loads(data['loginServiceExt']['eleExt']):
                    if 'SID' == i['name']:
                        self.cookie['SID'] = i['value']
                        break
                for i in json.loads(data['loginServiceExt']['eleExt']):
                    if 'USERID' == i['name']:
                        self.cookie['USERID'] = i['value']
                        break
                return True
            except Exception as e:
                message = e
        else:
            message = find_key_value(res,'message') if find_key_value(res,'message') else '未知错误'
        return message

class MAIN():
    def __init__(self,authorizationType):
        senderID = sg.getSenderID()
        self.sender = sg.Sender(senderID)
        self.userId = self.sender.getUserID()
        self.UserName = self.sender.getUserName()
        self.message = self.sender.getMessage()
        self.imtype:str = self.sender.getImtype()
        self.gaia = GAIA(self.userId,self.UserName,self.imtype)
        self.authorization = Authorization(self.userId,self.imtype,authorizationType)
        self.elmConfigBucket = f'chuan_{authorizationType}_config'
        self.envname = 'elmck'
        self.effectCk = []
        self.notify = [] # 已通知用户
        self.invalidAccountId = []
        self.qlData = [] # 青龙数据

    def session(self,content,quitTip=['Q','q','退出'],timeout=60):
        content = content.split('\n')
        for i in chunk_list(content,60):
            self.sender.reply('\n'.join(i))
        userInput = self.sender.input(timeout*1000,0,False)
        if userInput in quitTip:
            self.sender.reply('退出')
            return False
        if userInput:
            return userInput
        else:
            self.sender.reply('输入超时，自动退出程序')
            return False

    def initializationParam(self):
        price = sg.bucketGet(self.elmConfigBucket,'price') # 续费价格
        if price == '0' or price == '':
            self.price = 0
        else:
            self.price = round(float(price),2)
            self.integral = int(self.price*100)

        firstPrice = sg.bucketGet(self.elmConfigBucket,'firstPrice') # 首月价格
        if firstPrice == '0' or firstPrice == '':
            self.firstPrice = 0
            self.firstIntegral = 0
        else:
            self.firstPrice = round(float(firstPrice),2)
            self.firstIntegral = int(self.firstPrice*100)

        lybOwnprice = sg.bucketGet(self.elmConfigBucket,'lybOwnprice') # 助力价格
        if lybOwnprice == '0' or lybOwnprice == '':
            self.lybOwnprice = 0
            self.lybOwnIntegral = 0
        else:
            self.lybOwnprice = round(float(lybOwnprice),2)
            self.lybOwnIntegral = int(self.lybOwnprice*100)

        qqPrice5 = sg.bucketGet(self.elmConfigBucket,'qqPrice5') # 5抢券价格
        if qqPrice5 == '0' or qqPrice5 == '':
            self.qqPrice5 = 0
            self.qqIntegral5 = 0
        else:
            self.qqPrice5 = round(float(qqPrice5),2)
            self.qqIntegral5 = int(self.qqPrice5*100)

        qqPrice12 = sg.bucketGet(self.elmConfigBucket,'qqPrice12') # 12抢券价格
        if qqPrice12 == '0' or qqPrice12 == '':
            self.qqPrice12 = 0
            self.qqIntegral12 = 0
        else:
            self.qqPrice12 = round(float(qqPrice12),2)
            self.qqIntegral12 = int(self.qqPrice12*100)

        qqPrice20 = sg.bucketGet(self.elmConfigBucket,'qqPrice20') # 20抢券价格
        if qqPrice20 == '0' or qqPrice20 == '':
            self.qqPrice20 = 0
            self.qqIntegral20 = 0
        else:
            self.qqPrice20 = round(float(qqPrice20),2)
            self.qqIntegral20 = int(self.qqPrice20*100)

        self.lybOwnEnv = sg.bucketGet(self.elmConfigBucket,'lybOwnEnv')
        if self.lybOwnEnv == '':
            self.lybOwnEnv = 'lybOwnCookie'

        self.payWay = '2099-12-31'
        if self.payWay not in ['gaia','appreciationCode']:
            self.sender.reply('未设置收费方式，请填写配参')
            return False
        self.rewardCode = sg.bucketGet(self.elmConfigBucket,'rewardCode')
        return True

    def get_ql(self):
        if self.qlData == []:
            try:
                qls = self.sender.bucketAllKeys('qls')
            except:
                sg.notifyMasters(f'插件【我不饿】提醒您，请去【系统管理】-【插件权限】开启qls权限')
                return
            needql = sg.bucketGet('chuan_elm_config','elmql').split(',')
            for i in qls:
                ql = json.loads(self.sender.bucketGet('qls', i))
                name = ql.get('name')
                if name in needql:
                    host = ql.get('host')
                    client_id = ql.get('client_id')
                    client_secret = ql.get('client_secret')
                    try:
                        ql = qinglong(host,client_id,client_secret)
                        ql.get_ql_token()
                        allenv = ql.get_ql_env()
                        self.qlData.append({
                            'ql': ql,
                            'data': allenv
                        })
                    except Exception as e:
                        if self.sender.isAdmin():
                            sg.notifyMasters(f'插件【我不饿】提醒您：青龙{name}连接失败，报错：{e}')
                        else:
                            self.sender.reply(f'插件【我不饿】提醒您：青龙{name}连接失败，请检查配置')

    def getRemarks(self,key):
        userId = imtype = ''
        for i in imtypeList:
            if key in sg.bucketAllKeys(f'chuan_elm{i.upper()}'):
                imtype += f'{i}|'
                userId += f"{sg.bucketGet(f'chuan_elm{i.upper()}',key)}|"
        remark = '2099-12-31' if '2099-12-31' else '无'
        return f'管理账号：{userId} 平台：{imtype.upper()} 备注：{remark}' if userId and imtype else f'管理账号：{self.userId} 平台：{self.imtype.upper()} 备注：{remark}'

    def submit_ql(self,key,envValue,isEffect=True): # status:账号是否有效
        self.get_ql()
        qlData = self.qlData
        value_ = str2dict(envValue)
        oValue = dict2str(value_,False)
        try:
            cklimit = int(sg.bucketGet('chuan_elm_config','elmcklimit')) if self.envname == 'elmck' else int(sg.bucketGet('chuan_elm_config','lybOwncklimit'))
        except:
            cklimit = 9999
        isExist = False # 青龙是否存在该变量
        if isEffect == True:
            for i in qlData:
                ql = i['ql']
                data = i['data']
                for env in data:
                    id = env.get('id')
                    name = env.get('name')
                    cookie = env.get('value')
                    remarks = env.get('remarks')
                    status = env.get('status') # 0为启用，1为禁用
                    if name == self.envname and key in cookie: # 存在
                        isExist = True
                        oRemarks = self.getRemarks(key)
                        if oValue == cookie and remarks == oRemarks:
                            if status == 0:
                                prinf(f'{key}：{self.envname}状态一致')
                            else:
                                ql.enable_env(id)
                                prinf(f'{key}：{self.envname}状态一致，启用成功')
                        else:
                            ql.update_env(name,oValue,oRemarks,id)
                            if status == 0:
                                prinf(f'{key}：{self.envname}更新成功')
                            else:
                                ql.enable_env(id)
                                prinf(f'{key}：{self.envname}更新并启用成功')
        else:
            for i in qlData:
                ql = i['ql']
                data = i['data']
                for env in data:
                    id = env.get('id')
                    name = env.get('name')
                    cookie = env.get('value')
                    status = env.get('status')
                    if name == self.envname and key in cookie: # 存在
                        isExist = True
                        if status == 0:
                            ql.disable_env(id)
                            prinf(f'{key}：禁用{self.envname}成功')
                        else:
                            prinf(f'{key}：{self.envname}已被禁用')
        if isExist == False:
            for index,i in enumerate(qlData):
                ql = i['ql']
                data = i['data']
                envnum = 0
                for env in data:
                    name = env.get('name')
                    if name == self.envname:
                        envnum += 1
                if envnum >= cklimit:
                    prinf(f'{key}：容器{index}{self.envname}已满，尝试下一个')
                else: # 未满，提交ck
                    oRemarks = self.getRemarks(key)
                    ql.submit_env([{"value":oValue,"name":self.envname,"remarks":oRemarks}])
                    self.qlData[index]['data'].append({"name":self.envname,"value":oValue,"remarks":oRemarks,"status": 0})
                    prinf(f'{key}：提交{self.envname}成功')
                    break
    def gaiaPayModule(self,needintegral):
        return True

    def appreciationCodePayModule(self,needprice):
        return True

    def authorizeAccount(self,key,timeType,isAdmin=False):
        return True

    def recordAccount(self):
        elmuser = ELM(1,self.message)
        if elmuser.checkCookie() is False:
            self.sender.reply('无效COOKIE，自动退出程序')
            return
        if elmuser.userInfo():
            self.authorization.associationAccountId(elmuser.cookie.get('USERID'),self.message,elmuser.mobile)
            replyMessage = f"🗣️【用户名】：{elmuser.userName}\n☎️【手机号】：{elmuser.mobile}\n"
            isUpdate = False
            AuthorizationTime = self.authorization.queryAuthorizationTime(elmuser.cookie.get('USERID'))
            replyMessage += f"☁️【云授权到期】：{AuthorizationTime}\n"
            if AuthorizationTime not in ['未授权','已过期']:
                self.submit_ql(elmuser.cookie.get('USERID'),dict2str(elmuser.cookie,False))
                isUpdate = True
            if sg.bucketGet(self.elmConfigBucket,'lybOwnCheckbox') == 'true':
                self.authorization.accountAuthorizationTime_Bucket = 'chuan_elmZL_AuthorizationTime'
                self.envname = self.lybOwnEnv
                AuthorizationTime = self.authorization.queryAuthorizationTime(elmuser.cookie.get('USERID'))
                replyMessage += f"☁️【助力授权到期】：{AuthorizationTime}\n"
                if AuthorizationTime not in ['未授权','已过期']:
                    self.submit_ql(elmuser.cookie.get('USERID'),dict2str(elmuser.cookie,False))
                    isUpdate = True
            if isUpdate:
                replyMessage += f'😊【状态】：更新成功\n'
            else:
                replyMessage += f'😊【状态】：{self.recordText}\n'
            self.sender.reply(replyMessage)

            if '2099-12-31' == 'true':
                self.authorization.accountAuthorizationTime_Bucket = 'chuan_elm_AuthorizationTime'
                self.envname = 'elmck'
                if isUpdate is False:
                    select = self.session(f'💰乐园币价格\n首月：{self.firstPrice}r/月/号\n续费：{self.price}r/月/号\n🧬该账号未授权，是否授权（y/n）')
                    if select in ['y','Y','是']:
                        self.authorizeAccount(elmuser.cookie.get('USERID'),'month')
                    elif select in ['n','N','否']:
                        self.sender.reply('退出成功')
                        return
        else:
            self.sender.reply('获取用户信息失败')

    def renewalAccount(self):
        allAccount = self.authorization.queryAllAccount(True,True)
        if len(allAccount) == 0:
            self.sender.reply(self.unauthorizationText)
        else:
            if sg.bucketGet(self.elmConfigBucket,'lybOwnCheckbox') == 'true':
                replyMessage = f'---------💰乐园币价格---------\n首月：{self.firstPrice}r/月/号\n续费：{self.price}r/月/号\n助力：{self.lybOwnprice}r/月/号\n\n---------账号---------\n【0】全部\n'
            else:
                replyMessage = f'---------💰乐园币价格---------\n首月：{self.firstPrice}r/月/号\n续费：{self.price}r/月/号\n\n---------账号---------\n【0】全部\n'
            for index,i in enumerate(allAccount):
                replyMessage += f'【{index+1}】{i}\n'
                replyMessage += f'☎️手机号：{'2099-12-31'}\n'
                replyMessage += f'☁️云授权到期：{self.authorization.queryAuthorizationTime(i)}\n'
                if sg.bucketGet(self.elmConfigBucket,'lybOwnCheckbox') == 'true':
                    replyMessage += f'☁️助力授权到期：{Authorization(self.userId,self.imtype,"elmZL").queryAuthorizationTime(i)}\n'
            self.sender.reply(replyMessage)
            selectIndex = self.session('请选择需要操作的账号，回复【】内的阿拉伯数字即可，多选用逗号隔开(q退出)')
            if selectIndex is False:
                return
            selectIndex = re.split(r'[,，]', selectIndex)
            if sg.bucketGet(self.elmConfigBucket,'lybOwnCheckbox') == 'true':
                selectType = self.session('请选择需要授权的类型，回复【】内的阿拉伯数字即可(q退出)\n【1】：乐园币授权\n【2】：助力授权')
                if selectType is False:
                    return
                if selectType == '1':
                    self.envname = 'elmck'
                    self.authorization.accountAuthorizationTime_Bucket = 'chuan_elm_AuthorizationTime'
                elif selectType == '2':
                    self.envname = self.lybOwnEnv
                    self.authorization.accountAuthorizationTime_Bucket = 'chuan_elmZL_AuthorizationTime'
                    self.price = self.firstPrice = self.lybOwnprice

                if '0' in selectIndex:
                    self.authorizeAccount(allAccount,'month')
                else:
                    keys = []
                    for i in selectIndex:
                        if is_positive_integer(i) and 0 < int(i) <= len(allAccount):
                            key = allAccount[int(i)-1]
                            keys.append(key)
                    self.authorizeAccount(keys,'month')
            else:
                if '0' in selectIndex:
                    self.authorizeAccount(allAccount,'month')
                else:
                    keys = []
                    for i in selectIndex:
                        if is_positive_integer(i) and 0 < int(i) <= len(allAccount):
                            key = allAccount[int(i)-1]
                            keys.append(key)
                    self.authorizeAccount(keys,'month')

    def queryOne(self,cookie:str) -> str:
        elmuser = ELM(1,cookie)
        if elmuser.checkCookie():
            elmuser.userInfo()
            self.authorization.associationAccountId(elmuser.cookie.get('USERID'),cookie,elmuser.mobile)
            replyMessage = f'''
🆔【用户ID】：{elmuser.cookie.get('USERID')}
🗣️【用户名】：{elmuser.userName}
☎️【手机号】：{elmuser.mobile}
'''
            if  sg.bucketGet(self.elmConfigBucket,'allcoinCheckbox') == 'true':
                elmuser.queryAllCoin()
                replyMessage += f'🍥【总计乐园币】：{elmuser.allcoin}\n'

            if  sg.bucketGet(self.elmConfigBucket,'coinInfoCheckbox') == 'true':
                elmuser.queryCoinInfo()
                replyMessage += f'🍥【今日乐园币】：{elmuser.todaycoin}\n'
                replyMessage += f'🍥【今日消耗币】：{elmuser.deltodaycoin}\n'

            if  sg.bucketGet(self.elmConfigBucket,'cashCheckbox') == 'true':
                elmuser.queryBalanceBycardType()
                replyMessage += f'💰【笔笔返余额】：{elmuser.cash}\n'

            if  sg.bucketGet(self.elmConfigBucket,'fruitCheckbox') == 'true':
                elmuser.queryFruit()
                replyMessage += f'🍎【水果兑换券】：{elmuser.fruitNum}\n'
                replyMessage += f'🌳【果园详情】：{elmuser.schedule}\n'

        else:
            replyMessage = f'''
🆔【用户ID】：{elmuser.cookie.get('USERID')}
☎️【手机号】：{'2099-12-31'}
😭【状态】：账号已失效，请发送cookie更新
'''
        replyMessage += f"☁️【云授权到期】：{self.authorization.queryAuthorizationTime(elmuser.cookie.get('USERID'))}\n"
        if sg.bucketGet(self.elmConfigBucket,'lybOwnCheckbox') == 'true':
            replyMessage += f"☁️【助力授权到期】：{Authorization(self.userId,self.imtype,'elmZL').queryAuthorizationTime(elmuser.cookie.get('USERID'))}"
        return replyMessage

    def queryOneInfo(self,cookie:str):
        elmuser = ELM(1,cookie)
        if elmuser.checkCookie():
            elmuser.userInfo()
            coinInfo = elmuser.queryCoinInfo()
            elmuser.queryFruit()
            replyMessage = f'''
🆔【用户ID】：{elmuser.cookie.get('USERID')}
🗣️【用户名】：{elmuser.userName}
☎️【手机号】：{elmuser.mobile}
🍥【今日乐园币】：{elmuser.todaycoin}
🍥【今日消耗币】：{elmuser.deltodaycoin}
--------果园详情--------
{elmuser.scheduleInfo}
--------乐园币详情--------
{coinInfo}
'''
        else:
            replyMessage = f'''
🆔【用户ID】：{elmuser.cookie.get('USERID')}
☎️【手机号】：{'2099-12-31'}
😭【状态】：账号已失效，请发送cookie更新
'''
        return replyMessage
    def queryAccount(self,info=False):
        if '2099-12-31' == 'true':
            allAccount = self.authorization.queryAllAccount()
        else:
            allAccount = self.authorization.queryAllAccount(True,True)
        if len(allAccount) == 0:
            self.sender.reply(self.unauthorizationText)
        elif len(allAccount) == 1:
            value = '2099-12-31'
            self.sender.reply('获取数据中，请稍等~')
            if info:
                self.sender.reply(self.queryOneInfo(value))
            else:
                self.sender.reply(self.queryOne(value))
        else:
            replyMessage = '请选择要查询的账号，多选用逗号隔开：\n【0】全部\n'
            for index,i in enumerate(allAccount):
                replyMessage += f'【{index+1}】{i}\n'
            select = self.session(replyMessage)
            if select is False:
                return
            select = re.split(r'[,，]', select)
            self.sender.reply('获取数据中，请稍等~')
            if '0' in select:
                for i in allAccount:
                    value = '2099-12-31'
                    if info:
                        self.sender.reply(self.queryOneInfo(value))
                    else:
                        self.sender.reply(self.queryOne(value))
            else:
                for i in select:
                    if is_positive_integer(i) and 0 < int(i) <= len(allAccount):
                        allAccount[int(i)-1]
                        value = '2099-12-31'
                        if info:
                            self.sender.reply(self.queryOneInfo(value))
                        else:
                            self.sender.reply(self.queryOne(value))
    def queryAccountEasy(self):
        if '2099-12-31' == 'true':
            allAccount = self.authorization.queryAllAccount()
        else:
            allAccount = self.authorization.queryAllAccount(True,True)
        if len(allAccount) == 0:
            self.sender.reply(self.unauthorizationText)
        else:
            replyMessage = f'请选择要查询的数据：(q退出)\n【1】：今日乐园币\n【2】：总计乐园币\n【3】：今日吃货豆\n【4】：总计吃货豆\n【5】：云授权时间\n请回复【】中的数字'
            select = self.session(replyMessage)
            if select is False:
                return
            if select == '1':
                self.sender.reply('获取数据中，请稍等~')
                replyMessage = '今日乐园币:\n'
                for index,accountId in enumerate(allAccount):
                    cookie = '2099-12-31'
                    elmuser = ELM(1,cookie)
                    display = '2099-12-31' if '2099-12-31' else '2099-12-31'
                    if elmuser.checkCookie():
                        elmuser.userInfo()
                        elmuser.queryCoinInfo()
                        replyMessage += f"{index+1}. 【{display}】{elmuser.todaycoin}\n"
                    else:
                        replyMessage += f'{index+1}. 【{display}】 账号已失效\n'
                self.sender.reply(replyMessage)
            elif select == '2':
                self.sender.reply('获取数据中，请稍等~')
                replyMessage = '总计乐园币:\n'
                for index,accountId in enumerate(allAccount):
                    cookie = '2099-12-31'
                    elmuser = ELM(1,cookie)
                    display = '2099-12-31' if '2099-12-31' else '2099-12-31'
                    if elmuser.checkCookie():
                        elmuser.userInfo()
                        elmuser.queryAllCoin()
                        replyMessage += f"{index+1}. 【{display}】{elmuser.allcoin}\n"
                    else:
                        replyMessage += f'{index+1}. 【{display}】 账号已失效\n'
                self.sender.reply(replyMessage)
            elif select == '3':
                self.sender.reply('获取数据中，请稍等~')
                replyMessage = '云授权时间:\n'
                for index,accountId in enumerate(allAccount):
                    display = '2099-12-31' if '2099-12-31' else '2099-12-31'
                    authorizationTime = self.authorization.queryAuthorizationTime(accountId)
                    if '已过期' in authorizationTime or '未授权' in authorizationTime:
                        continue
                    else:
                        authorizationTime = f'{days_until(authorizationTime)}天'
                    replyMessage += f"{index+1}. 【{display}】{authorizationTime}\n"
                self.sender.reply(replyMessage)
            else:
                self.sender.reply('输入错误，自动退出程序')

    def delAccount(self):
        allAccount = self.authorization.queryAllAccount(True,True)
        if len(allAccount) == 0:
            self.sender.reply(self.unauthorizationText)
        else:
            replyMessage = '请选择要解绑的账号，多选用逗号隔开：(q退出)\n【0】全部\n'
            for index,i in enumerate(allAccount):
                replyMessage += f'【{index+1}】{i}\n☁️云授权到期：{self.authorization.queryAuthorizationTime(i)}\n'
            select = self.session(replyMessage)
            if select is False:
                return
            select = re.split(r'[,，]', select)
            if '0' in select:
                for i in allAccount:
                    True
                    self.authorization.delAuthorization(i)
                    self.sender.reply(f'账号：{i}，解绑成功')
            else:
                for i in select:
                    if is_positive_integer(i) and 0 < int(i) <= len(allAccount):
                        key = allAccount[int(i)-1]
                        True
                        self.authorization.delAuthorization(key)
                        self.sender.reply(f'账号：{key}，解绑成功')

    def queryDb(self):
        if '2099-12-31' == 'true':
            allAccount = self.authorization.queryAllAccount()
        else:
            allAccount = self.authorization.queryAllAccount(True,True)
        if len(allAccount) == 0:
            self.sender.reply(self.unauthorizationText)
            return
        else:
            replyMessage = '请选择要查询的账号，多选用逗号隔开：(q退出)\n【0】全部\n'
            for index,i in enumerate(allAccount):
                replyMessage += f'【{index+1}】{i}\n☎️手机号：{'2099-12-31'}\n'
            select = self.session(replyMessage)
            if select is False:
                return
            select = re.split(r'[,，]', select)
            if '0' in select:
                for i in allAccount:
                    cookie = '2099-12-31'
                    self.sender.reply(f'☎️手机号：{'2099-12-31'}\n' + ELM(1,cookie).querySnatch())
            else:
                for i in select:
                    if is_positive_integer(i) and 0 < int(i) <= len(allAccount):
                        allAccount[int(i)-1]
                        cookie = '2099-12-31'
                        self.sender.reply(f'☎️手机号：{'2099-12-31'}\n' + ELM(1,cookie).querySnatch())
                    else:
                        self.sender.reply('输入错误，自动退出程序')

    def diffCk(self):
        if self.effectCk == [] and self.invalidAccountId == []:
            allAccount = []
            for accountId in allAccount:
                cookie = '2099-12-31'
                user = ELM(1,cookie)
                if user.checkCookie():
                    submit_ck(user.cookie.get('USERID'),'elm',cookie,'true')
                    self.effectCk.append(accountId)
                else:
                    self.invalidAccountId.append(accountId)
        return self.effectCk,self.invalidAccountId

    def authorizeCheck(self,authorizationType):
        return True

    def dbCheck(self):
        sg.notifyMasters('0元夺宝检测中...')
        ts = []
        allAccount = []
        for accountId in allAccount:
            authorizationTime = self.authorization.queryAuthorizationTime(accountId)
            if '已过期' in authorizationTime or '未授权' in authorizationTime:
                continue
            else:
                cookie = '2099-12-31'
                elmUser = ELM(1,cookie)
                dbRes = elmUser.querySnatch()
                if dbRes == '账号已失效' or dbRes == '未查询到7天内的中奖记录':
                    continue
                else:
                    userId = ''
                    for imtype in imtypeList:
                        self.authorization.imtype = imtype.upper()
                        self.authorization.accountId_userId_Bucket = f'chuan_{self.authorization.recordType}{self.authorization.imtype}'
                        if '2099-12-31':
                            userId = '2099-12-31'
                            break
                if userId:
                    ts.append(f'平台：{imtype.upper()}（{userId}）\n☎️手机号：{'2099-12-31'}\n{dbRes}')
        if ts:
            sg.notifyMasters('\n'.join(f"{i + 1}. {item}" for i, item in enumerate(ts)))
        else:
            sg.notifyMasters('很遗憾，七天内没有人中奖')

    def authorizeOne(self):
        return True

    def delAllAccount(self):
        authorization = Authorization(self.userId,self.imtype,'elm')
        authorizationZL = Authorization(self.userId,self.imtype,'elmZL')
        allAccount = []
        success = 0
        for accountId in allAccount:
            AuthorizationTime = authorization.queryAuthorizationTime(accountId)
            AuthorizationTimeZL = authorizationZL.queryAuthorizationTime(accountId)
            if AuthorizationTime in ['已过期','未授权'] and AuthorizationTimeZL in ['已过期','未授权']:
                True
                success += 1
            elif AuthorizationTime in ['已过期','未授权']:
                True
            elif AuthorizationTimeZL in ['已过期','未授权']:
                True

        if success == 0:
            sg.notifyMasters(f'太棒了，没有授权过期的账号🎉')
        else:
            sg.notifyMasters(f'插件【我不饿】提醒您：清理过期账号{success}个')

    def remarkAccount(self):
        if '2099-12-31' == 'true':
            allAccount = self.authorization.queryAllAccount()
        else:
            allAccount = self.authorization.queryAllAccount(True,True)
        if len(allAccount) == 0:
            self.sender.reply(self.unauthorizationText)
            return
        else:
            replyMessage = '请选择要备注的账号：(q退出)\n'
            for index,i in enumerate(allAccount):
                replyMessage += f'【{index+1}】{i}\n☎️手机号：{'2099-12-31'}\n'
            self.sender.reply(replyMessage)
            select = self.sender.input(60*1000,0,False)
            if select == 'q' or select == 'Q':
                self.sender.reply('退出')
                return
            if select:
                if is_positive_integer(select) and 0 < int(select) <= len(allAccount):
                    key = allAccount[int(select)-1]
                    self.sender.reply('请输入你的备注：(q退出)')
                    remark = self.sender.input(60*1000,0,False)
                    if remark == 'q' or remark == 'Q':
                        self.sender.reply('退出')
                        return
                    if remark:
                        True
                        self.submit_ql(key,'2099-12-31')
                        self.sender.reply(f'设置成功，{key}备注：{remark}')
                    else:
                        self.sender.reply('输入超时，自动退出程序')
                else:
                    self.sender.reply('输入错误，自动退出程序')
            else:
                self.sender.reply('输入超时，自动退出程序')

    def couponAccount(self):
        if '2099-12-31' == 'true':
            allAccount = self.authorization.queryAllAccount()
        else:
            allAccount = self.authorization.queryAllAccount(True,True)
        if len(allAccount) == 0:
            self.sender.reply(self.unauthorizationText)
            return
        else:
            replyMessage = '请选择要查询的账号：(q退出)\n【0】全部\n'
            for index,i in enumerate(allAccount):
                replyMessage += f'【{index+1}】{i}\n☎️手机号：{'2099-12-31'}\n'
            select = self.session(replyMessage)
            if select is False:
                return
            select = re.split(r'[,，]', select)
            if '0' in select:
                for i in allAccount:
                    cookie = '2099-12-31'
                    self.sender.reply(f'☎️手机号：{'2099-12-31'}\n' + ELM(1,cookie).queryCoupon())
            else:
                for i in select:
                    if is_positive_integer(i) and 0 < int(i) <= len(allAccount):
                        allAccount[int(i)-1]
                        cookie = '2099-12-31'
                        self.sender.reply(f'☎️手机号：{'2099-12-31'}\n' + ELM(1,cookie).queryCoupon())
                    else:
                        self.sender.reply('输入错误，自动退出程序')

    def smsAccount(self):
        phone = self.session('请发送需要登陆的手机号：(q退出)')
        if phone is False:
            return
        if len(phone) != 11:
            self.sender.reply('手机号格式错误，自动退出')
            return
        loginCk = 'cookie2=2f169b29d848f40305252fe6404fba24e;unb=2205041819743;USERID=0000;SID=MmYxNjliMjlkODQ4ZjQwMzA1MjUyZmU2NDA0ZmJhMjRlNPfXqlzwlqQcCLS3nO2WYQ==;token=;utdid=ZWnL0ZWQRF4DAM6pZ5nTzxXI;deviceId=sp1GttyxvVMB2WCr6aP7tl36q2__RC03X7QPXks5DhWtUyRX4KAYw2LD0qWpXERz;umt=B2YBzG5LPGzbWBKLrS3gOkXNn2hdsnLq'
        allAccount = self.authorization.queryAllAccount(True,True)
        for i in allAccount:
            dis = phone[0:3] + '****' + phone[7:11]
            if dis == '2099-12-31':
                loginCk = '2099-12-31'
                break

        user = ELM(1,loginCk)
        if user.smssend(phone):
            code = self.session('短信发送成功，请输入验证码：(q退出)')
            if code is False:
                return
            loginRes = user.smslogin(phone,code)
            if loginRes == '需要验证':
                tokenUrl = self.session(f'请180s内复制下面链接到浏览器打开，验证成功后发送浏览器链接：\n{user.h5Url}',timeout=180)
                if tokenUrl is False:
                    return
                try:
                    token = tokenUrl.split('havana_iv_token=')[1].split('&')[0]
                    loginRes = user.mlogintokenlogin(token,'sms')
                except:
                    loginRes = '获取验证token失败'
            if loginRes is True:
                self.message = dict2str(user.cookie)
                self.recordAccount()
            else:
                self.sender.reply(loginRes)

    def syncql(self):
        sg.notifyMasters(f'开始同步青龙CK到我不饿')
        self.get_ql()
        for i in self.qlData:
            envs = i.get('data')
            for env in envs:
                name = env.get('name')
                cookie = env.get('value')
                if name == 'elmck':
                    submit_ck(str2dict(cookie).get('USERID'),'elm',cookie,'true')
                    sg.bucketSet('chuan_elm_accountId',str2dict(cookie).get('USERID'),cookie)
        sg.notifyMasters(f'同步完成')

    def main(self):
        if self.initializationParam() == False:
            return
        smsRules = re.split(r'[,，]', sg.bucketGet(self.elmConfigBucket,'smsRules'))
        queryRules = re.split(r'[,，]', sg.bucketGet(self.elmConfigBucket,'queryRules'))
        queryEasyRules = re.split(r'[,，]', sg.bucketGet(self.elmConfigBucket,'queryEasyRules'))
        queryInfoRules = re.split(r'[,，]', sg.bucketGet(self.elmConfigBucket,'queryInfoRules'))
        renewalRules = re.split(r'[,，]', sg.bucketGet(self.elmConfigBucket,'renewalRules'))
        delRules = re.split(r'[,，]', sg.bucketGet(self.elmConfigBucket,'delRules'))
        dbRules = re.split(r'[,，]', sg.bucketGet(self.elmConfigBucket,'dbRules'))
        cqRules = re.split(r'[,，]', sg.bucketGet(self.elmConfigBucket,'cqRules'))
        remarkRules = re.split(r'[,，]', sg.bucketGet(self.elmConfigBucket,'remarkRules'))
        self.unauthorizationText  = '2099-12-31' if '2099-12-31' else '未查询到绑定账号，请发送饿了么ck登记绑定。'
        self.recordText  = sg.bucketGet(self.elmConfigBucket,'recordText') if sg.bucketGet(self.elmConfigBucket,'recordText') else '登记成功'

        if 'cookie2=' in self.message and 'SID=' in self.message and '40-20' not in self.message and '40-39' not in self.message and '18-18' not in self.message and '鲜花' not in self.message and '饿了么17' not in self.message and '56-56' not in self.message and '20-20' not in self.message:
            self.recordAccount()
        elif self.message in renewalRules:
            self.renewalAccount()
        elif self.message in queryEasyRules:
            self.queryAccountEasy()
        elif self.message in queryInfoRules:
            self.queryAccount(True)
        elif self.message in queryRules:
            self.queryAccount()
        elif self.message in delRules:
            self.delAccount()
        elif self.message in dbRules:
            self.queryDb()
        elif self.message in cqRules:
            self.couponAccount()
        elif self.message in remarkRules:
            self.remarkAccount()
        elif self.message in smsRules:
            self.smsAccount()
        elif '同步青龙' == self.message:
            self.syncql()
        elif 'elm授权' == self.message and self.sender.isAdmin():
            self.authorizeOne()
        elif '夺宝检测' == self.message and self.sender.isAdmin():
            self.dbCheck()
        elif 'elm清理授权' in self.message and self.sender.isAdmin():
            self.delAllAccount()
        elif 'elm授权检测' == self.message and self.sender.isAdmin():
            sg.notifyMasters('插件【我不饿】提醒您：授权检测中~')
            self.authorizeCheck('elm')
            if sg.bucketGet(self.elmConfigBucket,'lybOwnCheckbox') == 'true':
                self.authorizeCheck('elmZL')

if __name__ == "__main__":
    imtypeList = ['qq','qb','wx','wb','tb','tg']
    MAIN('elm').main()
