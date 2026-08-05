# [title: 美团团]
# [name: meiTuanTuan]
# [language: python]
# [class: 任务]
# [author: Lxg-021002]
# [version: v2.2.7]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^.*$]
# [cron: 18 5,8,12,15,18,21 * * *]
# [icon: https://api.iconify.design/lucide:apple.svg]
# [description: 彻底解决千寻框架emjio问题 请使用最新版本SillyGirl和千寻框架 以及傻妞勾选 新版千寻框架 支持 查询丨删除 账号丨自定义命令(详见配参)，后续的任何使用问题都可以联系幼稚园小妹妹！使用前请安装Python的user-agent和sseclient依赖]
# [depe: ["requests","user-agent"]]


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
    'MMjson_Meituan_Qinglong': form.string().title('设置对接容器').default('').description('你的变量需要添加到的容器？参数用丨分割，这个符号是中文的竖(直接复制)'),
    'MMjson_mtloginmessage': form.string().title('登录消息').default('').description('发送 登录命令 需要回复的消息'),
    'MMjson_Meituan_os_mtname': form.string().title('领券变量名').default('').description('青龙容器内领券的变量名,不可与团币变量名相同'),
    'MMjson_Meituan_os_tbname': form.string().title('团币变量名').default('').description('青龙容器内团币的变量名,不可与领券变量名相同'),
    'MMjson_Meituan_signcommand': form.string().title('登陆口令').default('').description('多个口令用‘丨’分割，这个符号是中文的竖(直接复制)'),
    'MMjson_Meituan_querycommand': form.string().title('查询口令').default('').description('多个口令用‘丨’分割，这个符号是中文的竖(直接复制)'),
    'MMjson_Meituan_managecommand': form.string().title('账号管理口令').default('').description('多个口令用‘丨’分割，这个符号是中文的竖(直接复制)'),
})
_CONFIG_FIELD_MAP = {
    ('MMjson', 'Meituan_Qinglong'): 'MMjson_Meituan_Qinglong',
    ('MMjson', 'mtloginmessage'): 'MMjson_mtloginmessage',
    ('MMjson', 'Meituan_os_mtname'): 'MMjson_Meituan_os_mtname',
    ('MMjson', 'Meituan_os_tbname'): 'MMjson_Meituan_os_tbname',
    ('MMjson', 'Meituan_signcommand'): 'MMjson_Meituan_signcommand',
    ('MMjson', 'Meituan_querycommand'): 'MMjson_Meituan_querycommand',
    ('MMjson', 'Meituan_managecommand'): 'MMjson_Meituan_managecommand',
}

import json
import random
import string
import requests
from datetime import datetime, timedelta
from user_agent import generate_user_agent
from urllib.parse import urlparse, parse_qs
import re
import time
from decimal import Decimal

ua = generate_user_agent(os='android')
senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()
useroldvalue = sg.bucketGet(bucket='MMjson', key=userid)
uservalue = sg.bucketGet(bucket='Yzyxmm_mt_bind', key=userid)


def seekql():
    try:
        ql = sg.bucketGet(bucket="MMjson", key="Meituan_Qinglong")
        if len(ql) == 0:
            sender.reply('美团团未填写插件对接的容器，请检查配参')
            exit(0)
        else:
            qllist = ql.split('丨')
            QLurl = qllist[0]
            ClientID = qllist[1]
            ClientSecret = qllist[2]
            qltoken = QLtoken(QLurl=QLurl, ClientID=ClientID, ClientSecret=ClientSecret)
            return QLurl, qltoken
    except Exception:
        sender.reply("美团团获取青龙Token失败,请检查对接容器的参数！并仔细阅读提示内容！")
        exit(0)


def QLtoken(QLurl, ClientID, ClientSecret):  # 获取青龙token
    try:
        url = f'{QLurl}/open/auth/token?client_id={ClientID}&client_secret={ClientSecret}'
        A = requests.get(url)
        if "token" in A.text:
            ql = A.content
            qlrequests = json.loads(ql)
            qltoken = qlrequests['data']['token']

            return qltoken
        else:
            sender.reply('美团团链接青龙失败,请检查青龙配参！并仔细阅读提示内容！')
            exit(0)
    except Exception:
        sender.reply("美团团链接青龙失败,请检查青龙配参！并仔细阅读提示内容！")
        exit(0)


def getusercontent():
    Meituan_Lingquanmoney = sg.bucketGet(bucket='MMjson', key='Meituan_Lingquanmoney')  # 领券的价格
    Meituan_tbmoney = sg.bucketGet(bucket='MMjson', key='Meituan_tbmoney')  # 团币价格
    Meituan_Lingquancoin = sg.bucketGet(bucket='MMjson', key='Meituan_Lingquancoin')  # 领券的价格
    Meituan_tbcoin = sg.bucketGet(bucket='MMjson', key='Meituan_tbcoin')
    Meituan_zsm = sg.bucketGet(bucket='MMjson', key='Meituan_zsm')  # 二维码链接
    Meituan_os_mtname = sg.bucketGet(bucket='MMjson', key='Meituan_os_mtname')  # 领券变量名
    Meituan_os_tbname = sg.bucketGet(bucket='MMjson', key='Meituan_os_tbname')  # 团币变量名
    mt_managecommand = sg.bucketGet(bucket='MMjson', key='Meituan_managecommand')  # 触发管理的命令
    mt_querycommand = sg.bucketGet(bucket='MMjson', key='Meituan_querycommand')  # 触发查询的命令
    Mt_signcommand = sg.bucketGet(bucket='MMjson', key='Meituan_signcommand')  # 触发登陆的命令
    mtloginmessage = sg.bucketGet(bucket='MMjson', key='mtloginmessage')  # 美团登录发送的消息
    if len(Meituan_Lingquanmoney) == 0:
        Meituan_Lingquanmoney = Decimal('0')
    if len(Meituan_tbmoney) == 0:
        Meituan_tbmoney = Decimal('0')
    if len(Meituan_zsm) == 0:
        sender.reply("赞赏码链接未填写")
        exit(0)
    if len(Meituan_os_mtname) == 0:
        sender.reply("美团变量名称未填写")
        exit(0)
    if len(Meituan_os_tbname) == 0:
        sender.reply("团币变量名称未填写")
        exit(0)
    if len(Meituan_Lingquancoin) == 0:
        Meituan_Lingquancoin = 999999
    if len(Meituan_tbcoin) == 0:
        Meituan_tbcoin = 999999
    if len(mt_managecommand) == 0:
        mt_managecommand = '美团管理'
    randommanagecommand = mt_managecommand
    if '丨' in mt_managecommand:
        parts = mt_managecommand.split('丨')
        randommanagecommand = random.choice(parts)

    if len(mt_querycommand) == 0:
        mt_querycommand = '美团查询'
    randomquerycommand = mt_querycommand
    if '丨' in mt_querycommand:
        parts = mt_querycommand.split('丨')
        randomquerycommand = random.choice(parts)
    if len(Mt_signcommand) == 0:
        Mt_signcommand = '美团登录'
    randomsigncommand = Mt_signcommand
    if '丨' in Mt_signcommand:
        parts = Mt_signcommand.split('丨')
        randomsigncommand = random.choice(parts)
    if len(mtloginmessage) == 0:
        mtloginmessage = '美团Token获取丨http://u9v.cn/6hEfM8\n请输入您的Token:'
    return Meituan_tbmoney, Meituan_Lingquanmoney, Meituan_zsm, Meituan_os_mtname, Meituan_os_tbname, mt_managecommand, mt_querycommand, Mt_signcommand, randommanagecommand, randomsigncommand, randomquerycommand, Meituan_Lingquancoin, Meituan_tbcoin, mtloginmessage


def userdata(usertoken):  # 美团ck状态，用户信息
    try:
        url = "https://open.meituan.com/user/v1/info?fields=mobile,username,avatarurl,regTime"
        h = {
            'Connection': 'keep-alive',
            'Origin': 'https://mtaccount.meituan.com',
            'User-Agent': ua,
            'token': usertoken,
            'Referer': 'https://mtaccount.meituan.com/user/',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.9',
            'X-Requested-With': 'com.sankuai.meituan',
        }
        MT = requests.get(url, headers=h)

        if '登录失败' in MT.text:
            MTname = 'Token失效'
            mobile = '查询失败'
            accountid = 'Token失效'
            return MTname, accountid, mobile
        elif '已将账号锁定' in MT.text:
            MTname = 'Token失效'
            mobile = '查询失败'
            accountid = 'Token失效'
            return MTname, accountid, mobile
        else:
            MTjson = MT.json()
            MTname = MTjson['user']['username']
            mobile = MTjson['user']['mobile']
            accountid = MTjson['user']['id']
            return MTname, accountid, mobile
    except Exception:
        sender.reply(f'查询用户信息错误')
        exit(0)


def allenvs(osname, token, account):
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
        sender.reply(qlid)
        return qlid
    else:
        sender.reply('连接青龙获取变量失败')
        exit(0)


def QLupdate(osname, value, account, oldToken):
    qlid = allenvs(osname=osname, token=oldToken, account=account)
    if qlid is None:
        QLzt(osname=osname, value=value, userid=userid, account=account)
    else:
        qlurl = f"{QLurl}/open/envs"
        data = {
            "value": value,
            "name": osname,
            "remarks": f'美团团管理丨用户:{userid}丨美团:{account}',
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


def QLzt(osname, value, userid, account):  # 添加青龙变量
    try:
        qlurl = f"{QLurl}/open/envs"
        data = [{
            "value": value,
            "name": osname,
            "remarks": f'美团团管理丨用户:{userid}丨美团:{account}'
        }]
        headers = {
            "Authorization": "Bearer" + ' ' + qltoken,
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        r = requests.post(qlurl, headers=headers, data=json.dumps(data))
        r_json = r.json()
        if "value must be unique" in r.text:
            return
        else:
            r_json['data'][0]['id']
            return

    except Exception:
        sender.reply("添加青龙变量错误,请稍后重试")
        exit(0)


def binds(accounts, Lingquantime, token, account, MTname, Tbtime, UUID, oldtoken):
    sg.bucketSet(bucket='Yzyxmm_mt_bind', key=f'{userid}', value=f'{accounts}')
    if len(Lingquantime) != 0 and Lingquantime != '未开通' and Lingquantime != '授权过期' and Lingquantime >= str(
            today_time):
        QLzt(osname=Meituan_os_mtname, value=f'{token}', userid=userid, account=f'{account}')
    if len(Tbtime) != 0 and Tbtime != '未开通' and Tbtime != '授权过期' and Tbtime >= str(today_time):
        if len(UUID) == 0:
            sg.bucketSet(bucket='Yzyxmm_mt_account', key=f'{account}', value=f'{oldtoken}')
            sender.reply('账号未添加UUID，请添加后重试！')
            exit(0)
        QLzt(osname=Meituan_os_tbname, value=f'{token}#{UUID}', userid=userid, account=f'{account}')
    sender.reply(f'登陆成功! 🤪用户名:{MTname}，可对我说‘{randommanagecommand}’对账号进行管理!')


def bindaccount():
    if len(useroldvalue) == 0:
        sender.reply(mtloginmessage)
        userurl = sender.input(120000, 1, False)
        if userurl == 'q' or userurl == 'Q':
            sender.reply('退出！')
            exit(0)
        if 'meituan.com' in userurl and 'token' in userurl:
            token = re.search(r"token=([^&]+)", userurl).group(1)
            MTname, account, mobile = userdata(token)
            if MTname == 'Token失效':
                sender.reply('Token无效，请重新获取！')
                exit(0)
            else:
                oldtoken = sg.bucketGet(bucket='Yzyxmm_mt_account', key=f'{account}')
                sg.bucketSet(bucket='Yzyxmm_mt_MTname', key=f'{account}', value=f'{MTname}')
                sg.bucketSet(bucket='Yzyxmm_mt_account', key=f'{account}', value=f'{token}')
                sg.bucketSet(bucket='Yzyxmm_mt_mobile', key=f'{account}', value=f'{mobile}')
                Lingquantime = sg.bucketGet(bucket='Yzyxmm_mt_Lingquantime', key=f'{account}')
                UUID = sg.bucketGet(bucket='Yzyxmm_mt_UUID', key=f'{account}')
                Tbtime = sg.bucketGet(bucket='Yzyxmm_mt_Tbtime', key=f'{account}')
        elif 'Ag' in userurl and '#' not in userurl:
            token = userurl
            MTname, account, mobile = userdata(token)
            if MTname == 'Token失效':
                sender.reply('Token无效，请重新获取！')
                exit(0)
            else:
                oldtoken = sg.bucketGet(bucket='Yzyxmm_mt_account', key=f'{account}')
                sg.bucketSet(bucket='Yzyxmm_mt_MTname', key=f'{account}', value=f'{MTname}')
                sg.bucketSet(bucket='Yzyxmm_mt_account', key=f'{account}', value=f'{token}')
                sg.bucketSet(bucket='Yzyxmm_mt_mobile', key=f'{account}', value=f'{mobile}')
                Lingquantime = sg.bucketGet(bucket='Yzyxmm_mt_Lingquantime', key=f'{account}')
                UUID = sg.bucketGet(bucket='Yzyxmm_mt_UUID', key=f'{account}')
                Tbtime = sg.bucketGet(bucket='Yzyxmm_mt_Tbtime', key=f'{account}')
        elif 'Ag' in userurl and '#' in userurl:
            tokens = userurl.split('#')
            token = tokens[0]
            UUID = tokens[1]
            MTname, account, mobile = userdata(token)
            if MTname == 'Token失效':
                sender.reply('Token无效，请重新获取！')
                exit(0)
            else:
                oldtoken = sg.bucketGet(bucket='Yzyxmm_mt_account', key=f'{account}')
                sg.bucketSet(bucket='Yzyxmm_mt_MTname', key=f'{account}', value=f'{MTname}')
                sg.bucketSet(bucket='Yzyxmm_mt_account', key=f'{account}', value=f'{token}')
                sg.bucketSet(bucket='Yzyxmm_mt_mobile', key=f'{account}', value=f'{mobile}')
                sg.bucketSet(bucket='Yzyxmm_mt_UUID', key=f'{account}', value=f'{UUID}')
                Lingquantime = sg.bucketGet(bucket='Yzyxmm_mt_Lingquantime', key=f'{account}')
                Tbtime = sg.bucketGet(bucket='Yzyxmm_mt_Tbtime', key=f'{account}')
        else:
            sender.reply('未找到有效Token，请检查！')
            exit(0)
        if len(uservalue) < 3:
            accounts = []
            accounts.append(str(account))
            binds(accounts, Lingquantime, token, account, MTname, Tbtime, UUID, oldtoken)
        else:
            accounts = _sg_literal(uservalue)
            if str(account) not in uservalue:
                accounts.append(str(account))
                binds(accounts, Lingquantime, token, account, MTname, Tbtime, UUID, oldtoken)
            else:
                if len(Lingquantime) != 0 and Lingquantime != '未开通' and Lingquantime != '授权过期' and Lingquantime >= str(
                        today_time):
                    QLupdate(osname=Meituan_os_mtname, value=token, account=account, oldToken=oldtoken)

                if len(Tbtime) != 0 and Tbtime != '未开通' and Tbtime != '授权过期' and Tbtime >= str(today_time):
                    if len(UUID) == 0:
                        sender.reply('账号未添加UUID，请添加UUID！')
                        UUID = getUUID()
                        if UUID is None:
                            sg.bucketSet(bucket='Yzyxmm_mt_account', key=f'{account}', value=f'{oldtoken}')
                            sender.reply('提取UUID错误')
                            exit(0)
                        sg.bucketSet(bucket='Yzyxmm_mt_UUID', key=f'{account}', value=f'{UUID}')

                        QLupdate(osname=Meituan_os_tbname, value=f'{token}#{UUID}', account=account,
                                 oldToken=f'{oldtoken}')
                        sender.reply(f'更新成功! 🤪用户名:{MTname}，可对我说‘{randommanagecommand}’对账号进行管理!')
                        exit(0)
                    else:
                        QLupdate(osname=Meituan_os_tbname, value=f'{token}#{UUID}', account=account,
                                 oldToken=f'{oldtoken}#{UUID}')
                sender.reply(f'更新成功! 🤪用户名:{MTname}，可对我说‘{randommanagecommand}’对账号进行管理!')


    else:
        oldmtt()


def delenvs(id):
    if id is None:
        return
    url = f"{QLurl}/open/envs"
    headers = {
        "Authorization": "Bearer" + ' ' + qltoken,
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    data = [id]
    response = requests.delete(url, headers=headers, json=data).json()


def lq(token):
    url = 'http://8.130.140.144:22222/mtcoupon'

    data = {
        "token": token
    }
    response = requests.post(url, json=data)
    return response


def meituanmanage():
    if len(uservalue) > 3:
        count = 1
        message = ''
        accounts = _sg_literal(uservalue)
        for account in accounts:
            token = sg.bucketGet(bucket='Yzyxmm_mt_account', key=f'{account}')
            mobile = sg.bucketGet(bucket='Yzyxmm_mt_mobile', key=f'{account}')
            MTname = sg.bucketGet(bucket='Yzyxmm_mt_MTname', key=f'{account}')
            Lingquantime = sg.bucketGet(bucket='Yzyxmm_mt_Lingquantime', key=f'{account}')
            Tbtime = sg.bucketGet(bucket='Yzyxmm_mt_Tbtime', key=f'{account}')
            UUID = sg.bucketGet(bucket='Yzyxmm_mt_UUID', key=f'{account}')
            if len(UUID) == 0:
                UUID = '🥹'
            else:
                UUID = '😀'
            if len(Lingquantime) != 0 or Lingquantime < str(today_time):
                balance = '授权过期'
            if len(Lingquantime) == 0:
                balance = '未开通'
            if Lingquantime > str(today_time):
                balance = Lingquantime
            if len(Tbtime) != 0 or Tbtime < str(today_time):
                balance2 = '授权过期'
            if len(Tbtime) == 0:
                balance2 = '未开通'
            if Tbtime > str(today_time):
                balance2 = Tbtime
            message += f'[{count}]-----\n🤪用户名:{MTname}\n🔥用户ID:{mobile}\n☁领券授权:{balance}\n🌤团币授权:{balance2}\n🔗UUID:  {UUID}\n'
            count += 1
        message_to_send = f"=====我的团团=====\n团币:{str(Meituan_tbmoney)}元丨领券:{str(Meituan_Lingquanmoney)}元\n{message}"
        sender.reply(message_to_send)
        sender.reply('请选择[]内的数字对团团进行管理，回复‘q’退出')
        inputmessage = sender.input(120000, 1, False)
        if inputmessage == 'timeout':
            sender.reply('超时退出！')
            exit(0)
        elif inputmessage == 'q' or inputmessage == 'Q' or inputmessage == '0':
            sender.reply('退出！')
            exit(0)
        try:
            me_as_int = int(inputmessage)
            if me_as_int > count:
                sender.reply('输入错误')
                exit(0)
        except ValueError:
            sender.reply('输入错误')
            exit(0)
        accountA = accounts[me_as_int - 1]
        token = sg.bucketGet(bucket='Yzyxmm_mt_account', key=f'{accountA}')
        MTname, account, mobile = userdata(token)
        accountst = None
        if MTname == 'Token失效':
            accountst = 'Token失效'
            mobile = sg.bucketGet(bucket='Yzyxmm_mt_mobile', key=f'{accountA}')
            MTname = sg.bucketGet(bucket='Yzyxmm_mt_MTname', key=f'{accountA}')
        Lingquantime = sg.bucketGet(bucket='Yzyxmm_mt_Lingquantime', key=f'{accountA}')
        Tbtime = sg.bucketGet(bucket='Yzyxmm_mt_Tbtime', key=f'{accountA}')
        UUID = sg.bucketGet(bucket='Yzyxmm_mt_UUID', key=f'{accountA}')
        if len(UUID) == 0:
            UUIDs = '➖➖'
        else:
            UUIDs = '✔️'
        if Lingquantime > str(today_time):
            balance = Lingquantime
        if len(Tbtime) != 0 or Tbtime < str(today_time):
            balance2 = '授权过期'
        if len(Tbtime) == 0:
            balance2 = '未开通'
        if Tbtime > str(today_time):
            balance2 = Tbtime
        if accountst == 'Token失效':
            sender.reply(
                f'🤪用户名:{MTname}\n🔥用户ID:{mobile}\n🪫账号状态:Token失效')
            sender.reply('[3]丨关停服务 [4]丨添加UUID\n [q]丨退出')
        else:
            sender.reply(
                f'🤪用户名:{MTname}\n🔥用户ID:{mobile}\n☁领券授权:{balance}\n🌤团币授权:{balance2}\n🏷UUID:  {UUIDs}')
            sender.reply('[1]丨开通领券 [2]丨开通团币\n[3]丨关停服务 [4]丨添加UUID\n [q]丨退出')
        inputmessage = sender.input(120000, 1, False)
        if inputmessage == 'Q' or inputmessage == 'q' or inputmessage == '0':
            sender.reply('退出！')
            exit(0)
        try:
            me_as_int = int(inputmessage)
        except ValueError:
            sender.reply('输入错误')
            exit(0)
        if me_as_int == 1:
            if accountst == 'Token失效':
                sender.reply(f'【{mobile}】账号Token无效')
                exit(0)
            renew(Monthly=Meituan_Lingquanmoney, token=token, account=account, osname=Meituan_os_mtname, UUID=None,
                  Lingquantime=Lingquantime, Tbtime=Tbtime)
        elif me_as_int == 2:
            if accountst == 'Token失效':
                sender.reply(f'【{mobile}】账号Token无效')
                exit(0)
            if UUIDs != '✔️':
                sender.reply('请先添加UUID后再试！')
                exit(0)
            renew(Monthly=Meituan_tbmoney, token=token, account=account, osname=Meituan_os_tbname, UUID=UUID,
                  Lingquantime=Lingquantime, Tbtime=Tbtime)
        elif me_as_int == 3:
            if (balance == '未开通' or balance == '授权过期') and (balance2 == '未开通' or balance2 == '授权过期'):
                sender.reply('当前账号未开通任何授权，请问您是否要删除这个账号?')
                sender.reply('[y] 是丨[n] 否')
                yesorno = sender.input(120000, 1, False)
                if yesorno == 'Y' or yesorno == 'y' or yesorno == '是':
                    accounts.remove(str(accountA))
                    sg.bucketSet(bucket='Yzyxmm_mt_bind', key=f'{userid}', value=f'{accounts}')
                    sender.reply('删除成功，感谢您的使用！')
                elif yesorno == 'n' or yesorno == 'N' or yesorno == '否':
                    sender.reply('退出！')
                    exit(0)
            else:
                delaccount(balance, balance2, token, UUID, accounts, accountA)
        elif me_as_int == 4:
            uuid = getUUID()
            if uuid is None:
                sender.reply('uuid提取失败，！')
                exit(0)
            if balance2 == '未开通' or balance2 == '授权过期':
                sg.bucketSet(bucket='Yzyxmm_mt_UUID', key=f'{account}', value=f'{uuid}')
                sender.reply(f'添加成功！UUID_{uuid}')
            else:
                oldToken = f'{token}#{UUID}'
                QLupdate(osname=Meituan_os_tbname, value=f'{token}#{uuid}', account=account, oldToken=oldToken)
                sg.bucketSet(bucket='Yzyxmm_mt_UUID', key=f'{account}', value=f'{uuid}')
                sender.reply(f'更新成功！UUID_{uuid}')

        '''elif me_as_int == 5:
            sender.reply(
                '该领券可能出现如下情况:\n情况一:25-8丨30-9丨40-10丨20-7\n情况二:20-6丨25-7丨30-8丨40-9\n情况三:20-5丨25-6丨30-7丨40-8\n情况四:活动过于火爆\n情况五:今日已经领过券\n账号正常只会有第一，第二种情况，其中:活动火爆丨今日已领，可询问群主退款\n注:该领券皆为代替手动领券实现自动化，不存在如:刷券丨卖券等')
            sender.reply('该次代领券费用(0.88)元，同意以上协议\n[y] 是丨[n] 否')
            yesorno = sender.input(120000, 1, False)
            if yesorno == 'Y' or yesorno == 'y' or yesorno == '是':
                zf(money='0.88', project='单次领券', me_as_int='1次')
                try:
                    r = lq(token)
                    message = r.json()['message']
                    coupons = r.json()['coupons']
                    if message == 'fail':
                        sender.reply(f'领券失败>>>{coupons}')
                    else:
                        sender.reply(f'{coupons}')
                except Exception as e:
                    sender.reply(f'领券异常出错>>>{e}')
                    exit(0)
            elif inputmessage == 'Q' or inputmessage == 'q' or inputmessage == '0':
                sender.reply('退出！')
            else:
                sender.reply('输入错误')'''


def delaccount(balance, balance2, token, UUID, accounts, account):
    sender.reply('[1]丨关停领券\n[2]丨关停团币\n[3]丨关停服务删除全部\n[q]丨退出')
    inputmessage = sender.input(120000, 1, False)
    if inputmessage == '1':
        if balance == '未开通' or balance == '授权过期':
            sender.reply('账号还未开通领券！')
            exit(0)
        else:
            qlid = allenvs(osname=Meituan_os_mtname, token=token, account=account)
            sender.reply(f'当前账号已经开通了领券，确定要关停领券服务吗？(授权时间会一并清空)')
            sender.reply('[y] 是丨[n] 否')
            yesorno = sender.input(120000, 1, False)
            if yesorno == 'Y' or yesorno == 'y' or yesorno == '是':
                delenvs(id=qlid)
                sg.bucketDel(bucket='Yzyxmm_mt_Lingquantime', key=f'{account}')
                sender.reply('删除成功，感谢您的使用！')
            elif yesorno == 'n' or yesorno == 'N' or yesorno == '否':
                sender.reply('退出！')
                exit(0)
    elif inputmessage == '2':
        if balance2 == '未开通' or balance2 == '授权过期':
            sender.reply('账号还未开通团币！')
            exit(0)
        else:
            qlid = allenvs(osname=Meituan_os_tbname, token=f'{token}#{UUID}', account=account)
        sender.reply(f'当前账号已经开通了团币，确定要关停团币服务吗？(授权时间会一并清空)')
        sender.reply('[y] 是丨[n] 否')
        yesorno = sender.input(120000, 1, False)
        if yesorno == 'Y' or yesorno == 'y' or yesorno == '是':
            sg.bucketDel(bucket='Yzyxmm_mt_Tbtime', key=f'{account}')
            delenvs(id=qlid)
            sender.reply('删除成功，感谢您的使用！')
        elif yesorno == 'n' or yesorno == 'N' or yesorno == '否':
            sender.reply('退出！')
            exit(0)
    elif inputmessage == '3':
        sender.reply(f'确定要关停当前账号的全部数据吗？请您慎重选择！')
        sender.reply('[y] 是丨[n] 否')
        yesorno = sender.input(120000, 1, False)
        if yesorno == 'Y' or yesorno == 'y' or yesorno == '是':
            mtid = allenvs(osname=Meituan_os_mtname, token=token, account=account)
            tbid = allenvs(osname=Meituan_os_tbname, token=f'{token}#{UUID}', account=account)
            delenvs(id=mtid)
            delenvs(id=tbid)
            accounts.remove(str(account))
            sg.bucketSet(bucket='Yzyxmm_mt_bind', key=f'{userid}', value=f'{accounts}')
        elif yesorno == 'n' or yesorno == 'N' or yesorno == '否':
            sender.reply('退出！')
            exit(0)
        sender.reply('删除成功！，感谢您的使用！')
    elif inputmessage == 'q':
        sender.reply('退出！')


def empower(empowertime, me_as_int):
    day = me_as_int * 30
    if len(empowertime) == 0 or empowertime == '未开通' or empowertime == '授权过期' or empowertime <= str(today_time):
        delayed_date = today_time + timedelta(days=day)
    elif empowertime > str(today_time):
        empower_date = datetime.strptime(empowertime, "%Y-%m-%d")
        delayed_date = empower_date + timedelta(days=day)
        delayed_date = delayed_date.date()

    else:
        sender.reply('出错！')
        exit(0)
    return str(delayed_date)


def renew(Monthly, token, account, osname, UUID, Lingquantime, Tbtime):
    usercoin = sg.bucketGet(bucket='Yzyxmm_sign_coin', key=f'{userid}')
    if len(usercoin) == 0 or usercoin == '0':
        usercoin = 0
    sender.reply('请问您需要几个月？例:1')
    inputmessage = sender.input(120000, 1, False)
    if inputmessage == '0':
        sender.reply('退出！')
        exit(0)
    if inputmessage == 'q' or inputmessage == 'timeout' or inputmessage == '0':
        sender.reply('退出！')
        exit(0)
    numbers = re.findall(r'\d+', inputmessage)
    if numbers:
        numbers = [int(num) for num in numbers]
        num = numbers[0]
    else:
        sender.reply('输入错误！')
        exit(0)
    money = Decimal(num) * Decimal(Monthly)
    project = '出错！'
    if Decimal(money) == Decimal('0'):
        if osname == Meituan_os_mtname:
            project = '领券'
            delayed_date = empower(empowertime=Lingquantime, me_as_int=num)
            QLzt(osname=osname, value=f'{token}', userid=userid, account=f'{account}')
            sg.bucketSet(bucket='Yzyxmm_mt_Lingquantime', key=f'{account}', value=f'{delayed_date}')
        if osname == Meituan_os_tbname:
            project = '团币'
            delayed_date = empower(empowertime=Tbtime, me_as_int=num)
            QLzt(osname=osname, value=f'{token}#{UUID}', userid=userid, account=f'{account}')
            sg.bucketSet(bucket='Yzyxmm_mt_Tbtime', key=f'{account}', value=f'{delayed_date}')
        sender.reply(
            f'=====订单完成=====\n🎈名称:{project}\n✨数量:{num}个月\n💰支付金额:{money}元')
        exit(0)
    else:
        if osname == Meituan_os_mtname:
            project = '领券'
            ordercoin = int(num) * int(Meituan_Lingquancoin)
            Deduction, usercoin = Pointpayment(ordercoin=ordercoin, usercoin=usercoin)
            if Deduction is True:
                cc = '积分'
                delayed_date = empower(empowertime=Lingquantime, me_as_int=num)
                sg.bucketSet(bucket='Yzyxmm_sign_coin', key=f'{userid}', value=f'{usercoin}')
            else:
                cc = '元'
                zf(money=money, project=project, me_as_int=num)
                delayed_date = empower(empowertime=Lingquantime, me_as_int=num)
            QLzt(osname=osname, value=f'{token}', userid=userid, account=f'{account}')
            sg.bucketSet(bucket='Yzyxmm_mt_Lingquantime', key=f'{account}', value=delayed_date)
        if osname == Meituan_os_tbname:
            project = '团币'
            ordercoin = int(num) * int(Meituan_tbcoin)
            Deduction, usercoin = Pointpayment(ordercoin=ordercoin, usercoin=usercoin)
            if Deduction is True:
                delayed_date = empower(empowertime=Tbtime, me_as_int=num)
                sg.bucketSet(bucket='Yzyxmm_sign_coin', key=f'{userid}', value=f'{usercoin}')
                cc = '积分'
            else:
                cc = '元'
                zf(money=money, project=project, me_as_int=num)
                delayed_date = empower(empowertime=Tbtime, me_as_int=num)
            QLzt(osname=osname, value=f'{token}#{UUID}', userid=userid, account=f'{account}')
            sg.bucketSet(bucket='Yzyxmm_mt_Tbtime', key=f'{account}', value=delayed_date)

        sender.reply(
            f'=====订单完成=====\n🎈名称:{project}\n✨数量:{num}个月\n💰支付金额:{money}{cc}')
        exit(0)


def Pointpayment(ordercoin, usercoin):
    return True


def zf(money, project, me_as_int):  # 等待支付并且发送ck到青龙
    zsm = sg.bucketGet(bucket='MMjson', key='zsm')  # 获取发链接还是图片
    zfzt = False
    if zfzt != True:
        if project == '单次领券':
            sender.reply(f'=====订单结算=====\n🎈名称:{project}\n✨数量:{me_as_int}\n💰应付:{money}元')
        else:
            sender.reply(f'=====订单结算=====\n🎈名称:{project}\n✨数量:{me_as_int}个月\n💰应付:{money}元')
        if zsm == 'true':
            sender.replyImage(Meituan_zsm)
        else:
            sender.reply(f'支付链接:{Meituan_zsm}')
        ddzf = False
        if str(ddzf) == 'q':
            sender.reply('退出支付')
            exit(0)
        if 'Time' in str(ddzf):
            try:
                zfjson = json.loads(ddzf)
                zfmoney = zfjson['Money']
            except Exception:
                zfmoney = ddzf['Money']

            if float(zfmoney) >= float(money):
                return
            else:
                sender.reply(f'支付金额错误\n应付:{money}元\n实付:{zfmoney}元\n请稍后核对支付记录！')
                exit(0)
        elif ddzf == 'timeout':
            sender.reply('支付超时！')
            exit(0)
    else:
        sender.reply('当前有人正在支付,请稍后再试！')
        exit(0)


def getUUID():
    def segmentation(UUIDurl):
        parsed_url1 = urlparse(UUIDurl)
        query_params1 = parse_qs(parsed_url1.query)
        utm_term_value1 = query_params1.get('utm_term', [''])[0]
        if '2024' in utm_term_value1:
            index_2024 = utm_term_value1.index('2024')
            if index_2024 < len(utm_term_value1) / 2:
                start_index = index_2024 + 14
                end_index = start_index + 64
                uuid = utm_term_value1[start_index:end_index]
            else:
                end_index = index_2024
                start_index = max(0, end_index - 64)
                uuid = utm_term_value1[start_index:end_index]
        else:
            uuid = None
        return uuid

    def UUID(url):
        response = requests.get(url, allow_redirects=False)
        response.raise_for_status()
        redirect_url = response.headers.get('Location')
        uuid = segmentation(UUIDurl=redirect_url)
        return uuid

    sender.reply('请前往 美团APP-我的-团团赚-游戏中心右上角分享:')
    sender.replyImage('http://120.46.35.143:1212/UUID.png')
    inputmessage = sender.input(120000, 1, False)
    if '来团团赚玩更多游戏 您的好友邀请您来玩游戏！ http://dpurl.cn' in inputmessage:
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, inputmessage)
        url = urls[0]
        uuid = UUID(url)
    elif 'jumpUrl' in inputmessage:  # QQ的格式
        jump_url = re.search(r'"jumpUrl":"(.*?)"', inputmessage).group(1)
        uuid = UUID(jump_url)
    elif '<url>' in inputmessage:
        start_tag = "<url>"
        end_tag = "</url>"
        start_index = inputmessage.find(start_tag) + len(start_tag)
        end_index = inputmessage.find(end_tag)
        UUIDurl = inputmessage[start_index:end_index]
        uuid = segmentation(UUIDurl)
    else:
        uuid = None
        sender.reply('提取uuid失败，请检查配置！')
        exit(0)
    return uuid


def Tbcx(usertoken):
    try:
        sing = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        url = "https://open.meituan.com/user/v1/info/auditting?fields=auditAvatarUrl%2CauditUsername"
        h = {
            'Connection': 'keep-alive',
            'Origin': 'https://mtaccount.meituan.com',
            'User-Agent': ua,
            'token': usertoken,
            'Referer': 'https://mtaccount.meituan.com/user/',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.9',
            'X-Requested-With': 'com.sankuai.meituan',
        }
        r = requests.get(url, headers=h)

        MTdata = r.content
        MTjson = json.loads(MTdata)
        login = MTjson.keys()

        if "user" in login:
            rj = r.json()
            usid = rj["user"]["id"]
            url1 = 'https://game.meituan.com/mgc/gamecenter/front/api/v1/login'
            h1 = {
                'Accept': 'application/json, text/plain, */*',
                'Content-Length': '307',
                'x-requested-with': 'XMLHttpRequest',
                'User-Agent': ua,
                'Content-Type': 'application/json;charset=UTF-8',
                'cookie': f'token={usertoken}'
            }
            data1 = {
                "mtToken": usertoken,
                "deviceUUID": '0000000000000A3467823460D436CAB51202F336236F6A167191373531985811',
                "mtUserId": usid,
                "idempotentString": sing
            }
            r1 = requests.post(url1, headers=h1, json=data1)
            actoken = r1.json()['data']['loginInfo']['accessToken']


            url2 = 'https://game.meituan.com/mgc/gamecenter/skuExchange/resource/counts?sceneId=3&gameId=10102'
            t_h = {
                'User-Agent': ua,
                'actoken': actoken,
                'mtoken': usertoken,
            }
            r2 = requests.get(url2, headers=t_h)
            rj = r2.json()
            ttb = float(rj['data'][0]['count'])
            money = round(ttb / 1000, 2)
        else:
            ttb = "Token过期"
            money = "0"
        print(ttb, money)
        return int(ttb), money
    except Exception:
        return 'Token过期', '0'


def count_jrtb(usertoken):
    try:
        def get_coin_rec(usertoken, offset):
            headers = {
                'Host': 'game.meituan.com',
                'Accept': 'application/json, text/plain, */*',
                'X-Requested-With': 'XMLHttpRequest',
                'Sec-Fetch-Site': 'same-site',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
                'Sec-Fetch-Mode': 'cors',
                'Content-Type': 'application/json',
                'Origin': 'https://awp.meituan.com',
                'User-Agent': ua,
                'Referer': 'https://awp.meituan.com/',
                'Connection': 'keep-alive',
                'Sec-Fetch-Dest': 'empty'
            }
            params = {
                'yodaReady': 'h5',
                'csecplatform': '4',
                'csecversion': '2.3.1',
                'mtgsig': '{"a1":"1.1","a2":1703869899600,"a3":"1703667675570AAAUGGU868c0ee73ab28e1d0b03bc83148500067970","a5":"sES6rta18s7aMmHqRHX6","a6":"hs1.4a4gsvX1s4RLQYqBR3sFhAa3DMq/oCARZURaKrpiINxNiC0rXQnF5ffvc6Zi383ak+37Vcyy6mroJ3oQJHmnf1Ra37KQdKjE/bRI1E4RP7ho=","x0":4,"d1":"4eaa678b4abaf15b62bec14d041096d2"}',
            }
            json_data = {
                'mtToken': usertoken,
                'lastUpdateTime': int(time.time()) * 1000,
                'limit': 20,
                'offset': offset,
            }
            response = requests.post(
                'https://game.meituan.com/coin/billPage/getCoinAccountFlow',
                params=params,
                headers=headers,
                json=json_data,
            )
            record = response.json()
            if '身份验证失败' in response.text:
                record = 999
            return record

        TodayTb = 0
        current_time = datetime.now()
        todaytime = current_time.strftime("%Y-%m-%d")
        offset = 0
        while True:
            record = get_coin_rec(usertoken, offset)
            if record == 999:
                break
            else:
                recordlist = record['data']['coinChangeLogBOList']
                if len(recordlist) == 0:
                    break
                for recordjson in recordlist:
                    utimeGmt = recordjson['utimeGmt']
                    datetime_obj = datetime.strptime(utimeGmt, "%Y-%m-%d %H:%M:%S")
                    recordtime = datetime_obj.strftime("%Y-%m-%d")
                    if recordtime < todaytime:
                        break
                    else:
                        changeType = recordjson['changeType']
                        operationNote = recordjson['operationNote']
                        if changeType == 1:
                            if '退款' in operationNote:
                                continue
                            else:
                                changeAmount = recordjson['changeAmount']
                                TodayTb = changeAmount + TodayTb
                recordjson = recordlist[-1]
                utimeGmt = recordjson['utimeGmt']
                datetime_obj = datetime.strptime(utimeGmt, "%Y-%m-%d %H:%M:%S")
                recordtime = datetime_obj.strftime("%Y-%m-%d")
                if recordtime < todaytime:
                    break
                else:
                    offset = offset + 20
        while True:
            record = get_coin_rec(usertoken, offset)
            if record == 999:
                break
            else:
                recordlist = record['data']['coinChangeLogBOList']
                if len(recordlist) == 0:
                    break
                for recordjson in recordlist:
                    utimeGmt = recordjson['utimeGmt']
                    datetime_obj = datetime.strptime(utimeGmt, "%Y-%m-%d %H:%M:%S")
                    recordtime = datetime_obj.strftime("%Y-%m-%d")
                    if recordtime < todaytime:
                        break
                    else:
                        changeType = recordjson['changeType']
                        operationNote = recordjson['operationNote']
                        if changeType == 1:
                            if '退款' in operationNote:
                                continue
                            else:
                                changeAmount = recordjson['changeAmount']
                                TodayTb = changeAmount + TodayTb
                recordjson = recordlist[-1]
                utimeGmt = recordjson['utimeGmt']
                datetime_obj = datetime.strptime(utimeGmt, "%Y-%m-%d %H:%M:%S")
                recordtime = datetime_obj.strftime("%Y-%m-%d")
                if recordtime < todaytime:
                    break
                else:
                    offset = offset + 20
        Todaymoney = round(TodayTb / 1000, 2) if TodayTb != 0 else 0
        print(Todaymoney)
        return TodayTb, Todaymoney
    except Exception:
        return '查询失败', '0'


def cx(usertoken):
    TodayTb, Todaymoney = count_jrtb(usertoken)
    ttb, money = Tbcx(usertoken)
    return TodayTb, Todaymoney, ttb, money


def cxs():
    accounts = _sg_literal(uservalue)
    message = ''
    count = 1
    account2 = []
    for account in accounts:
        token = sg.bucketGet(bucket='Yzyxmm_mt_account', key=f'{account}')
        MTname, accountid, mobile = userdata(usertoken=token)
        if mobile == '查询失败':
            mobile = sg.bucketGet(bucket='Yzyxmm_mt_mobile', key=f'{account}')
        Tbtime = sg.bucketGet(bucket='Yzyxmm_mt_Tbtime', key=f'{account}')
        if len(Tbtime) != 0 and Tbtime != '未开通' and Tbtime != '授权过期' and Tbtime > str(today_time):
            message += f'\n【{count}】丨{mobile}'
            count += 1
            account2.append(account)
        else:
            sender.reply(f'【{mobile}】团币云授权过期')
    if len(account2) == 1:
        account = account2[0]
        token = sg.bucketGet(bucket='Yzyxmm_mt_account', key=f'{account}')
        mobile = sg.bucketGet(bucket='Yzyxmm_mt_mobile', key=f'{account}')
        MTname = sg.bucketGet(bucket='Yzyxmm_mt_MTname', key=f'{account}')
        TodayTb, Todaymoney, ttb, money = cx(token)
        if ttb == 'Token过期':
            sender.reply(f'【{mobile}】账号Token过期')
            exit(0)
        else:
            sender.reply(
                f'🤪用户名:{MTname}\n🔥用户ID:{mobile}\n💰团币余额:{ttb}({money})\n✨今日团币:{TodayTb}({Todaymoney})')
            exit(0)
    else:
        if message == '':
            exit(0)
        message_to_send = "=====团币查询=====\n" + '【0】丨全部账号' + message
        sender.reply(message_to_send)
        sender.reply('请输入[]内要查询的账号')
        inputmessage = sender.input(120000, 1, False)
        if inputmessage == 'q' or inputmessage == 'Q':
            sender.reply('退出查询！')
            exit(0)
        if inputmessage == '0':
            for account in account2:
                token = sg.bucketGet(bucket='Yzyxmm_mt_account', key=f'{account}')
                TodayTb, Todaymoney, ttb, money = cx(token)
                mobile = sg.bucketGet(bucket='Yzyxmm_mt_mobile', key=f'{account}')

                MTname = sg.bucketGet(bucket='Yzyxmm_mt_MTname', key=f'{account}')
                if ttb == 'Token过期':
                    sender.reply(f'【{mobile}】账号Token过期')
                else:
                    sender.reply(
                        f'🤪用户名:{MTname}\n🔥用户ID:{mobile}\n💰团币余额:{ttb}({money})\n✨今日团币:{TodayTb}({Todaymoney})')
        else:
            try:
                me_as_int = int(inputmessage)
                if me_as_int > len(account2):
                    sender.reply('输入错误!')
                    exit(0)
            except ValueError:
                sender.reply('输入错误!')
                exit(0)
            account = account2[me_as_int - 1]
            token = sg.bucketGet(bucket='Yzyxmm_mt_account', key=f'{account}')
            TodayTb, Todaymoney, ttb, money = cx(token)
            mobile = sg.bucketGet(bucket='Yzyxmm_mt_mobile', key=f'{account}')
            MTname = sg.bucketGet(bucket='Yzyxmm_mt_MTname', key=f'{account}')
            if ttb == 'Token过期':
                sender.reply(f'【{mobile}】账号Token过期')
                exit(0)
            else:
                sender.reply(
                    f'🤪用户名:{MTname}\n🔥用户ID:{mobile}\n💰团币余额:{ttb}({money})\n✨今日团币:{TodayTb}({Todaymoney})')


def oldmtt():
    sender.reply('检测到旧版本数据，正在更新数据！')
    accounts = _sg_literal(useroldvalue)
    newaccounts = []
    for account, item in accounts.items():
        token = item['token']
        MTname, accountid, mobile = userdata(token)
        MTname = item['MTname']
        Lingquantime = item['Lingquantime']
        Tbtime = item['Tbtime']
        sg.bucketSet(bucket='Yzyxmm_mt_account', key=f'{account}', value=f'{token}')
        sg.bucketSet(bucket='Yzyxmm_mt_MTname', key=f'{account}', value=f'{MTname}')
        sg.bucketSet(bucket='Yzyxmm_mt_Lingquantime', key=f'{account}', value=f'{Lingquantime}')
        sg.bucketSet(bucket='Yzyxmm_mt_Tbtime', key=f'{account}', value=f'{Tbtime}')
        sg.bucketSet(bucket='Yzyxmm_mt_mobile', key=f'{account}', value=f'{mobile}')
        newaccounts.append(str(account))
    sg.bucketSet(bucket='Yzyxmm_mt_bind', key=f'{userid}', value=f'{newaccounts}')
    sg.bucketDel(bucket='MMjson', key=f'{userid}')
    sender.reply('数据更新完成, 请重新唤起机器人！')


def push(user, mobile, message):
    sg.push('wb', '', user, '',
                    f'🤪用户‘{mobile}’,{message}')
    sg.push('tg', '', user, '',
                    f'🤪用户‘{mobile}’,{message}')
    sg.push('qq', '', user, '',
                    f'🤪用户‘{mobile}’,{message}')
    sg.push('qb', '', user, '',
                    f'🤪用户‘{mobile}’,{message}')
    sg.push('wx', '', user, '',
                    f'🤪用户‘{mobile}’,{message}')


usermessage = sender.getMessage()
today_time = datetime.now().date()

if usermessage == '':
    usermessage = '1'
Meituan_tbmoney, Meituan_Lingquanmoney, Meituan_zsm, Meituan_os_mtname, Meituan_os_tbname, mt_managecommand, mt_querycommand, Mt_signcommand, randommanagecommand, randomsigncommand, randomquerycommand, Meituan_Lingquancoin, Meituan_tbcoin, mtloginmessage = getusercontent()
imtype = sender.getImtype()
if any(usermessage == s for s in Mt_signcommand.split('丨')):
    QLurl, qltoken = seekql()
    bindaccount()
elif any(usermessage == s for s in mt_managecommand.split('丨')):
    QLurl, qltoken = seekql()
    if len(useroldvalue) == 0:
        if len(uservalue) > 3:
            meituanmanage()
        else:
            sender.reply(f'未绑定美团账号，请发送’{randomsigncommand}‘进行账号绑定！')

    else:
        oldmtt()
elif any(usermessage == s for s in mt_querycommand.split('丨')):
    QLurl, qltoken = seekql()
    if len(useroldvalue) == 0:
        if len(uservalue) > 3:
            today_time = datetime.now().date()
            QLurl, qltoken = seekql()
            cxs()
        else:
            sender.reply(f'未绑定美团账号，请发送’{randomsigncommand}‘进行账号绑定！')
    else:
        oldmtt()
elif imtype == 'fake':

    QLurl, qltoken = seekql()
    today_time = datetime.now().date()
    userlist = sg.bucketAllKeys(bucket='Yzyxmm_mt_bind')
    for user in userlist:

        uservalue = sg.bucketGet(bucket='Yzyxmm_mt_bind', key=f'{user}')

        accounts = _sg_literal(uservalue)
        for account in accounts:
            token = sg.bucketGet(bucket='Yzyxmm_mt_account', key=f'{account}')
            MTname = sg.bucketGet(bucket='Yzyxmm_mt_MTname', key=f'{account}')
            mobile = sg.bucketGet(bucket='Yzyxmm_mt_mobile', key=f'{account}')
            Lingquantime = sg.bucketGet(bucket='Yzyxmm_mt_Lingquantime', key=f'{account}')
            Tbtime = sg.bucketGet(bucket='Yzyxmm_mt_Tbtime', key=f'{account}')
            UUID = sg.bucketGet(bucket='Yzyxmm_mt_UUID', key=f'{account}')

            if Lingquantime != '未开通' and Lingquantime != '授权过期' and len(Lingquantime) != 0:
                if Lingquantime < str(today_time):
                    qlid = allenvs(osname=Meituan_os_tbname, token=f'{token}', account=account)
                    if qlid is not None:
                        delenvs(qlid)
                    push(user, mobile, '美团领券云授权已过期,请及时续费！')

            if Tbtime != '未开通' and Tbtime != '授权过期' and len(Tbtime) != 0:
                if Tbtime < str(today_time):
                    qlid = allenvs(osname=Meituan_os_tbname, token=f'{token}#{UUID}', account=account)
                    if qlid is not None:
                        delenvs(qlid)
                    push(user, mobile, '美团团币云授权已过期,请及时续费！')
            MTname1, account1, mobile1 = userdata(token)
            if mobile1 == '查询失败':
                push(user, mobile, '美团账号Token过期,请及时更新！')

else:
    sender.setContinue()
