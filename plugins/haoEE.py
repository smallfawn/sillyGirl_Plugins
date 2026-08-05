# [title: 好饿饿]
# [name: haoEE]
# [language: python]
# [class: 任务]
# [author: Lxg-021002]
# [version: v2.2.6]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^.*cookie2=.*$|^吃饱了$|^我快饿死了$|^夺宝信息$|^(饿了.*|.*饿了)$]
# [cron: 28 8,18,21 * * *]
# [icon: https://pp.myapp.com/ma_icon/0/icon_1029694_1725435529/256]
# [description: 如果需要账密续期 请在我的市场下载我的续期食用 增加提交 账号密码  (饿了管理>选择账号>提交账密)  也可以在ck中添加loginId=xxx；password=xxx]
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
    'Yzyxmm_elm_elm_Qinglong': form.string().title('设置对接容器').default('').description('你的变量需要添加到的容器？参数用丨分割，这个符号是中文的竖(直接复制)，多容器用&分割'),
    'Yzyxmm_elm_elm_leyuanosname': form.string().title('乐园币变量名').default('').description('青龙容器内乐园币的变量名,默认elmck\n乐园和助力变量名不可一致！！！'),
    'Yzyxmm_elm_zlosname': form.string().title('助力账号变量名').default('').description('青龙容器内助力的变量名,默认nczlck\n乐园和助力变量名不可一致！！！'),
})
_CONFIG_FIELD_MAP = {
    ('Yzyxmm_elm', 'elm_Qinglong'): 'Yzyxmm_elm_elm_Qinglong',
    ('Yzyxmm_elm', 'elm_leyuanosname'): 'Yzyxmm_elm_elm_leyuanosname',
    ('Yzyxmm_elm', 'zlosname'): 'Yzyxmm_elm_zlosname',
}

from decimal import Decimal
import re
import urllib.parse
from datetime import datetime, timedelta
import hashlib
import json
import requests
import time
from urllib.parse import urlencode


global QLurl
global qltoken


def getusercontent():
    elm_leyuanmoney = sg.bucketGet(bucket='Yzyxmm_elm', key='elm_leyuanmoney')
    elm_zlmoney = sg.bucketGet(bucket='Yzyxmm_elm', key='elm_zlmoney')
    elm_leyuanosname = sg.bucketGet(bucket='Yzyxmm_elm', key='elm_leyuanosname')
    elm_zlosname = sg.bucketGet(bucket='Yzyxmm_elm', key='zlosname')
    elm_container_max = sg.bucketGet(bucket='Yzyxmm_elm', key='elm_container_max')
    elm_zlcontainer_max = sg.bucketGet(bucket='Yzyxmm_elm', key='elm_zlcontainer_max')
    moneycoin = sg.bucketGet(bucket='Yzyxmm_elm', key='moneycoin')
    zlmoneycoin = sg.bucketGet(bucket='Yzyxmm_elm', key='zlmoneycoin')
    wx_zsm = sg.bucketGet(bucket='Yzyxmm_elm', key='wx_zsm')
    zsm = sg.bucketGet(bucket='Yzyxmm_elm', key='zsm')
    if len(elm_leyuanmoney) == 0 or elm_leyuanmoney == '0':
        elm_leyuanmoney = Decimal('0')
    if len(elm_zlmoney) == 0 or elm_zlmoney == '0':
        elm_zlmoney = Decimal('0')
    if len(elm_leyuanosname) == 0:
        elm_leyuanosname = 'elmck'
    if len(elm_zlosname) == 0:
        elm_zlosname = 'nczlck'
    if len(moneycoin) == 0:
        moneycoin = 9999999
    if len(zlmoneycoin) == 0:
        zlmoneycoin = 9999999
    if len(elm_container_max) == 0 or elm_container_max == '0':
        elm_container_max = 180
    else:
        elm_container_max = int(elm_container_max)
    if len(elm_zlcontainer_max) == 0 or elm_zlcontainer_max == '0':
        elm_zlcontainer_max = 5
    else:
        elm_zlcontainer_max = int(elm_zlcontainer_max)
    randommanagecommand = '我快饿死了'
    randomquerycommand = '吃饱了'
    return zsm, wx_zsm, elm_leyuanmoney, elm_leyuanosname, moneycoin, randommanagecommand, randomquerycommand, elm_container_max, elm_zlmoney, elm_zlosname, zlmoneycoin, elm_zlcontainer_max


def seekql():
    try:
        qljson = {}
        Qinglong = sg.bucketGet(bucket="Yzyxmm_elm", key="elm_Qinglong")
        if len(Qinglong) == 0:
            sender.reply('饿了么插件未填写插件对接的容器，请检查配参')
            exit(0)
        else:
            qllist = Qinglong.split('&')
            for index, ql in enumerate(qllist, start=1):
                try:

                    delimiters = ['丨', '|', '#', '＃']
                    Delimiter = next((d for d in delimiters if d in ql), None)
                    qls = ql.split(Delimiter)
                    QLurl = qls[0]
                    ClientID = qls[1]
                    ClientSecret = qls[2]
                    qltoken = QLtoken(QLurl=QLurl, ClientID=ClientID, ClientSecret=ClientSecret)
                    qljson[QLurl] = qltoken
                except Exception as e:
                    sg.notifyMasters(
                        content=f'好饿饿检查发现第{index}个容器无法链接: {ql}请检查！',
                        imtypes=['wb', 'tg', 'qb', 'qq'])
            return qljson
    except Exception:
        sender.reply("获取青龙token失败")
        exit(0)


def delenvs(qlid, QLurl, qltoken):
    if qlid is None:
        return
    url = f"{QLurl}/open/envs"
    headers = {
        "Authorization": "Bearer" + ' ' + qltoken,
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    data = [qlid]
    response = requests.delete(url, headers=headers, json=data).json()
    code = response['code']
    if code == 200:
        print('删除成功')


senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()


def req(cookie, api, data_str, v="1.0"):
    def hbh5tk(tk_cookie, enc_cookie, cookie_str):
        """
        合并带_m_h5_tk
        """
        txt = cookie_str.replace(" ", "")
        txt = txt.replace("chushi;", "")
        txt = txt.replace("zhuli;", "")
        txt = txt.replace("zhuli", "")
        if txt[-1] != ';':
            txt += ';'
        cookie_parts = txt.split(';')[:-1]
        updated = False
        for i, part in enumerate(cookie_parts):
            key_value = part.split('=')
            if key_value[0].strip() in ["_m_h5_tk", " _m_h5_tk"]:
                cookie_parts[i] = tk_cookie
                updated = True
            elif key_value[0].strip() in ["_m_h5_tk_enc", " _m_h5_tk_enc"]:
                cookie_parts[i] = enc_cookie
                updated = True

        if updated:
            return ';'.join(cookie_parts) + ';'
        else:
            return txt + tk_cookie + ';' + enc_cookie + ';'

    def check_cookie(cookie):
        url = "https://waimai-guide.ele.me/h5/mtop.alsc.personal.queryminecenter/1.0/?jsv=2.6.2&appKey=12574478"
        headers = {
            "Cookie": cookie,
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36"
        }

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                cookie_jar = response.cookies
                token = cookie_jar.get('_m_h5_tk', '')
                token_cookie = "_m_h5_tk=" + token
                enc_token = cookie_jar.get('_m_h5_tk_enc', '')
                enc_token_cookie = "_m_h5_tk_enc=" + enc_token
                cookie = hbh5tk(token_cookie, enc_token_cookie, cookie)
                return cookie
            else:
                return None
        except Exception as e:
            print(f"解析ck错误{e}")
            return None

    def tq1(cookie_string):
        """
        获取_m_h5_tk
        """

        if not cookie_string:
            return '-1'
        cookie_pairs = cookie_string.split(';')
        for pair in cookie_pairs:
            key_value = pair.split('=')
            if key_value[0].strip() in ["_m_h5_tk", " _m_h5_tk"]:
                return key_value[1]
        return '-1'

    def md5(text):
        """
        md5加密
        """
        hash_md5 = hashlib.md5()
        hash_md5.update(text.encode())
        return hash_md5.hexdigest()

    try:
        cookie = check_cookie(cookie)
        headers = {
            "authority": "shopping.ele.me",
            "accept": "application/json",
            "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded",
            "cookie": cookie,
            "user-agent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36"
        }
        timestamp = int(time.time() * 1000)
        token = tq1(cookie)
        token_part = token.split("_")[0]

        sign_str = f"{token_part}&{timestamp}&12574478&{data_str}"
        sign = md5(sign_str)
        url = f"https://guide-acs.m.taobao.com/h5/{api}/{v}/?jsv=2.6.1&appKey=12574478&t={timestamp}&sign={sign}&api={api}&v={v}&type=originaljson&dataType=json"
        data1 = urlencode({'data': data_str})
        r = requests.post(url, headers=headers, data=data1)
        if r:
            return r
        else:
            return None
    except Exception as e:
        return None


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
            sender.reply('链接青龙失败,请检查青龙配参！')
            exit(0)
    except Exception:
        sender.reply("链接青龙失败,请检查青龙配参！")
        exit(0)


def QLupdate(QLurl, qltoken, osname, value, account, qlid):
    qlurl = f"{QLurl}/open/envs"
    data = {
        "value": value,
        "name": osname,
        "remarks": f'饿了么管理丨用户:{userid}丨账号:{account}',
        "id": qlid
    }
    headers = {
        "Authorization": "Bearer" + ' ' + qltoken,
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    response = requests.put(qlurl, headers=headers, data=json.dumps(data))
    qlurl2 = f"{QLurl}/open/envs/enable"
    data2 = [qlid]
    response2 = requests.put(qlurl2, headers=headers, json=data2)
    if response.status_code == 200:
        response_json = response.json()
        data = response_json['data']
        if data is None:
            exit(0)
        qlid = data['id']
        qlurl2 = f"{QLurl}/open/envs/enable"
        return qlid


def QLzt(QLurl, qltoken, osname, value, account):  # 添加青龙变量
    try:
        qlurl = f"{QLurl}/open/envs"
        data = [{
            "value": value,
            "name": osname,
            "remarks": f'饿了么管理丨用户:{userid}丨账号:{account}'
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


def Addenvs(osname, value, account, OrderPoints=0):
    qlid = None
    QLurl = None
    qltoken = None
    for QLurl, qltoken in qljson.items():
        url = f"{QLurl}/open/envs"
        headers = {
            "Authorization": "Bearer" + ' ' + qltoken,
            "accept": "application/json"
        }
        response = requests.get(url=url, headers=headers).json()

        if response['code'] == 200:
            envslist = response['data']
            for envs in envslist:
                remarks = envs['remarks']
                envname = envs['name']
                if remarks is None:
                    continue

                if str(account) in remarks and osname == envname:
                    qlid = envs['id']
                    break
            if qlid is not None:
                break
        else:
            sender.reply('连接青龙获取变量失败')
            exit(0)

    if qlid is None:
        for idx, (QLurl, qltoken) in enumerate(qljson.items()):

            url = f"{QLurl}/open/envs"
            headers = {
                "Authorization": "Bearer" + ' ' + qltoken,
                "accept": "application/json"
            }
            response = requests.get(url=url, headers=headers).json()
            if response['code'] == 200:
                envslist = response['data']
                if osname == elm_zlosname:
                    count = sum(1 for item in envslist if item['name'] == elm_zlosname)
                    if count < elm_zlcontainer_max:
                        QLzt(QLurl, qltoken, osname, value, account)
                        break

                    else:
                        if idx == len(qljson) - 1:
                            usercoin = sg.bucketGet(bucket='Yzyxmm_sign_coin', key=f'{userid}')
                            if len(usercoin) == 0:
                                usercoin = 0
                            if zlmoneycoin == 9999999 or zlmoneycoin == 0:
                                sender.reply('当前服务容器内乐园账号已达上限，请稍后重试！')
                            else:
                                usercoin = int(usercoin) + int(OrderPoints)
                                sg.bucketSet(bucket='Yzyxmm_sign_coin', key=f'{userid}', value=str(usercoin))
                                sender.reply('当前服务容器内账号已达上限，该次支付已经退为积分！')
                                sender.reply(f'当前积分{usercoin}！')
                            exit(0)
                        else:
                            continue
                elif osname == elm_leyuanosname:
                    count = sum(1 for item in envslist if item['name'] == elm_leyuanosname)
                    if count < elm_container_max:
                        QLzt(QLurl, qltoken, osname, value, account)
                        break
                    else:
                        if idx == len(qljson) - 1:
                            usercoin = sg.bucketGet(bucket='Yzyxmm_sign_coin', key=f'{userid}')
                            if len(usercoin) == 0:
                                usercoin = 0
                            if moneycoin == 9999999 or moneycoin == 0:
                                sender.reply('当前服务容器内乐园账号已达上限，请稍后重试！')

                            else:
                                usercoin = int(usercoin) + int(OrderPoints)
                                sg.bucketSet(bucket='Yzyxmm_sign_coin', key=f'{userid}', value=str(usercoin))
                                sender.reply('当前服务容器内账号已达上限，该次支付已经退为积分！')
                                sender.reply(f'当前积分{usercoin}！')
                            exit(0)
                        else:
                            continue

            else:
                sender.reply('连接青龙获取变量失败')
                exit(0)

    else:
        QLupdate(QLurl, qltoken, osname, value, account, qlid)


def allenvs(osname, token, account):
    qlid = None
    QLurl = None
    qltoken = None
    for QLurl, qltoken in qljson.items():
        url = f"{QLurl}/open/envs"
        headers = {
            "Authorization": "Bearer" + ' ' + qltoken,
            "accept": "application/json"
        }
        response = requests.get(url=url, headers=headers).json()
        if response['code'] == 200:
            envslist = response['data']
            for envs in envslist:
                remarks = envs['remarks']
                envname = envs['name']
                if remarks is None:
                    continue
                if str(account) in remarks and osname == envname:
                    qlid = envs['id']
                    break
            if qlid is not None:
                break

        else:
            sender.reply('连接青龙获取变量失败')
            exit(0)
    return qlid, QLurl, qltoken


def userdata(cookie):
    try:
        r = req(cookie, 'mtop.alsc.user.detail.query', json.dumps({}), v="1.0")
        if '过期' in r.text:
            return '查询失败', '查询失败', '查询失败'
        encryptMobile = r.json()['data']['encryptMobile']
        localId = r.json()['data']['localId']
        userName = r.json()['data']['userName']

        return str(localId), encryptMobile, userName
    except Exception:
        return '查询失败', '查询失败', '查询失败'


def tq2(txt):
    """
    拆分cookie，将字符串形式的Cookie解析为字典。
    """
    try:
        txt = txt.replace(" ", "").replace("zhuli;", "").replace("zhuli", "").replace("chishi;", "")

        if not txt.endswith(';'):
            txt += ';'

        pairs = txt.split(";")[:-1]
        ck_json = {}

        for pair in pairs:
            if "=" in pair:  # 确保是合法的键值对
                key, value = pair.split("=", 1)
                ck_json[key.strip()] = value.strip()
            else:
                raise ValueError(f"无效的键值对: {pair}")

        return ck_json
    except Exception as e:
        print(f'Cookie解析错误: {e}')
        return {}


def sign(cookie):


    def accvip(Newaddition):
        if len(zlaccountVip) != 0 and zlaccountVip >= str(now_time):
            Addenvs(osname=elm_zlosname, value=cookie, account=account)
        if len(accountVip) != 0 and accountVip >= str(now_time):
            Addenvs(osname=elm_leyuanosname, value=cookie, account=account)

            if Newaddition:
                accounts.append(account)
                sender.reply(f'🤪{bind}添加成功！\n————————————————\n» 可发送‘饿了管理’进行管理！')
            else:
                sender.reply(f'🤪{bind}更新成功！\n————————————————\n» 可发送‘饿了管理’进行管理！')

        else:
            if Newaddition:
                accounts.append(account)
                sender.reply(f'🤪{bind}添加成功！\n————————————————\n» 暂未授权‘饿了管理’进行授权！')
            else:
                sender.reply(f'🤪{bind}更新成功！\n————————————————\n» 授权过期‘饿了管理’进行续期！')

        sg.bucketSet(bucket='Yzyxmm_elm_bind', key=userid, value=f'{accounts}')


    account, bind, username = userdata(cookie)
    if account == '查询失败':
        if 'loginId' in cookie and 'password' in cookie and 'umt' in cookie:
            ck_json = tq2(cookie)
            account = ck_json['USERID']
            bind = ck_json['loginId']
            bind = bind[:3] + "*" * 4 + bind[7:]
            password = f'{ck_json["loginId"]}#{ck_json["password"]}'
            sg.bucketSet(bucket='Yzyxmm_elm_password', key=f'{account}',
                                 value=password)
        else:
            sender.reply('用户信息查询失败,请检查Cookie后重试！')
            exit(0)
    uservalue = sg.bucketGet(bucket='Yzyxmm_elm_bind', key=userid)
    accountVip = sg.bucketGet(bucket='Yzyxmm_elm_svip', key=f'{account}')
    zlaccountVip = sg.bucketGet(bucket='Yzyxmm_elm_vip', key=f'{account}')
    passwords = sg.bucketGet(bucket='Yzyxmm_elm_password', key=f'{account}')
    sg.bucketSet(bucket='Yzyxmm_elm_phone', key=f'{account}', value=f'{bind}')
    sg.bucketSet(bucket='Yzyxmm_elm_account', key=f'{account}', value=f'{cookie}')

    if len(passwords) != 0:
        passwordlist = passwords.split('#')
        phone = passwordlist[0]
        password = passwordlist[1]
        cookie += f'loginId={phone};password={password};'
        sg.bucketSet(bucket='Yzyxmm_elm_account', key=f'{account}', value=f'{cookie}')
    if len(uservalue) == 0:
        accounts = []
        accvip(True)
    else:
        accounts = _sg_literal(uservalue)
        if account in accounts:
            accvip(False)
        else:
            accvip(True)
    '''else:
        exit(0)'''


def getaccountmes(account):
    cookie = sg.bucketGet(bucket='Yzyxmm_elm_account', key=f'{account}')
    accsvip = sg.bucketGet(bucket='Yzyxmm_elm_svip', key=f'{account}')
    zlaccsvip = sg.bucketGet(bucket='Yzyxmm_elm_vip', key=f'{account}')
    bind = sg.bucketGet(bucket='Yzyxmm_elm_phone', key=f'{account}')
    if len(accsvip) == 0:
        accsvip = '未授权'
    elif accsvip < str(now_time):
        accsvip = '授权过期'

    if len(zlaccsvip) == 0:
        zlaccsvip = '未授权'
    elif accsvip < str(now_time):
        zlaccsvip = '授权过期'

    return cookie, bind, accsvip, zlaccsvip


def empower2(empowertime, me_as_int):
    day = me_as_int * 30
    if empowertime == '未授权' or empowertime == '授权过期' or empowertime <= str(today_time):
        delayed_date = today_date + timedelta(days=day)
    elif empowertime > today_time:
        empower_date = datetime.strptime(empowertime, "%Y-%m-%d")
        delayed_date = empower_date + timedelta(days=day)
        delayed_date = delayed_date.date()
    else:
        sender.reply('出错！')
        exit(0)
    return str(delayed_date)


def inputm(mes, long=99999999999, count=99999999999):
    sender.reply(mes)
    mes = sender.input(120000, 1, False)
    if mes == 'y' or mes == 'Y':
        return True
    if mes == 'n' or mes == 'N':
        return False
    if mes is None:
        sender.reply('输入超时！')
        exit(0)
    elif mes.lower() == 'q':
        sender.reply('退出！')
        exit(0)
    elif len(mes) < long:
        sender.reply('输入错误！')
        exit(0)
    try:
        mes = int(mes)
        if mes > count:
            sender.reply('输入错误！')
            exit(0)
    except ValueError:
        pass
    return mes


def Pointpayment2(OrderPoints):
    return True


def zf2(project, me_as_int, money):
    zfzt = False
    if money == 0:
        return
    if not zfzt:
        sender.reply(f'————《订单信息》————\n🎈名称:{project}\n🎉数量:{me_as_int}\n💰应付:{money}元')
        if zsm == 'true':
            sender.replyImage(wx_zsm)
        else:
            sender.reply(f'支付链接:{wx_zsm}')
        ddzf = False  # 等待支付
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
        elif ddzf == '':
            sender.reply('支付超时！')
            exit(0)
        else:
            exit(0)
    else:
        sender.reply('当前有人正在支付,请稍后再试！')
        exit(0)


def manage():
    accounts = sg.bucketGet(bucket='Yzyxmm_elm_bind', key=userid)
    message = ''
    count = 1
    if len(accounts) != 0:
        accounts = acclist = _sg_literal(accounts)
        for accid in acclist:
            cookie = sg.bucketGet(bucket='Yzyxmm_elm_account', key=accid)
            accsvip = sg.bucketGet(bucket='Yzyxmm_elm_svip', key=accid)
            zlaccsvip = sg.bucketGet(bucket='Yzyxmm_elm_vip', key=f'{accid}')
            bind = sg.bucketGet(bucket='Yzyxmm_elm_phone', key=f'{accid}')
            password = sg.bucketGet(bucket='Yzyxmm_elm_password', key=f'{accid}')
            if len(accsvip) == 0:
                accsvip = '未授权'
            elif accsvip < str(now_time):
                accsvip = '授权过期'

            if len(zlaccsvip) == 0:
                zlaccsvip = '未授权'
            elif accsvip < str(now_time):
                zlaccsvip = '授权过期'
            account, binds, username = userdata(cookie)
            if account == '查询失败':
                accountst = 'Cookie过期'
            else:
                accountst = '状态正常'
            if len(password) == 0:
                password = '还没提交'
            else:
                password = '已经提交'
            bind = bind[:3] + "*" * 4 + bind[7:]
            message += f'【{count}】      ———\n🤪用户ID:{bind}\n🪫账号状态:{accountst}\n🔥账密状态:{password}\n☁助力授权:{zlaccsvip}\n☁乐园授权:{accsvip}\n'
            count = count + 1
        message_to_send = f"———《饿了管理》———\n乐园:{elm_leyuanmoney}元/月丨助力:{elm_zlmoney}元/月\n{message}"
        sender.reply(message_to_send)
        sender.reply('请输入【】中需要管理的账号:\n【a】一键授权丨【q】退出执行')
        mations = sender.input(120000, 1, False)
        if mations == 'q':
            sender.reply('退出！')
            exit(0)
        elif mations is None:
            sender.reply('超时,退出！')
            exit(0)
        elif mations == 'a' or mations == 'A':
            sender.reply('【1】丨授权乐园\n【2】丨授权助力')
            option = sender.input(120000, 1, False)
            if option not in ['1', '2']:
                sender.reply('输入错误！')
                exit(0)
            sender.reply('请输入每个账号需要的月数,例: 1')
            mation = sender.input(120000, 1, False)
            if option == '1':
                try:
                    mation_int = int(mation)
                    money = Decimal(mation) * Decimal(elm_leyuanmoney) * Decimal(len(accounts))
                    order = OrderPoints = int(moneycoin) * int(mation_int) * len(accounts)
                except ValueError:
                    sender.reply('输入错误！')
                    exit(0)
                if money == Decimal('0'):
                    for account in accounts:
                        cookie, bind, accsvip, zlaccsvip = getaccountmes(account)
                        accsvip = empower2(accsvip, mation_int)
                        Addenvs(osname=elm_leyuanosname, value=cookie, account=account)
                        sg.bucketSet(bucket='Yzyxmm_elm_svip', key=account, value=accsvip)
                else:
                    Deduction = Pointpayment2(OrderPoints)
                    if not Deduction:
                        zf2(project='批量乐园', me_as_int=len(accounts) * int(mation_int), money=money)
                    for account in accounts:
                        cookie, bind, accsvip, zlaccsvip = getaccountmes(account)
                        accsvip = empower2(accsvip, mation_int)
                        Addenvs(osname=elm_leyuanosname, value=cookie, account=account, OrderPoints=OrderPoints)
                        sg.bucketSet(bucket='Yzyxmm_elm_svip', key=account, value=accsvip)
                        OrderPoints -= int(moneycoin)
                    if not Deduction:
                        sender.reply(
                            f'———《订单完成》———\n🎈名称:批量乐园\n🎉数量:{len(accounts) * int(mation_int)}月\n💰支付金额:{money}元')
                    else:
                        sender.reply(
                            f'———《订单完成》———\n🎈名称:批量乐园\n🎉数量:{len(accounts) * int(mation_int)}月\n💰支付金额:{order}积分')
            elif option == '2':
                try:
                    mation_int = int(mation)
                    money = Decimal(mation) * Decimal(elm_zlmoney) * Decimal(len(accounts))

                    order = OrderPoints = int(zlmoneycoin) * int(mation_int) * len(accounts)

                except ValueError:
                    sender.reply('输入错误！')
                    exit(0)
                if money == Decimal('0'):
                    for account in accounts:
                        cookie, bind, accsvip, zlaccsvip = getaccountmes(account)
                        accsvip = empower2(zlaccsvip, mation_int)
                        Addenvs(osname=elm_zlosname, value=cookie, account=account)
                        sg.bucketSet(bucket='Yzyxmm_elm_vip', key=account, value=accsvip)
                else:
                    Deduction = Pointpayment2(OrderPoints)
                    if not Deduction:
                        zf2(project='批量助力', me_as_int=len(accounts) * int(mation_int), money=money)

                    for account in accounts:
                        cookie, bind, accsvip, zlaccsvip = getaccountmes(account)
                        accsvip = empower2(zlaccsvip, mation_int)
                        Addenvs(osname=elm_zlosname, value=cookie, account=account, OrderPoints=OrderPoints)
                        sg.bucketSet(bucket='Yzyxmm_elm_vip', key=account, value=accsvip)
                        OrderPoints -= int(zlmoneycoin)
                    if not Deduction:
                        sender.reply(
                            f'———《订单完成》———\n🎈名称:批量助力\n🎉数量:{len(accounts) * int(mation_int)}月\n💰支付金额:{money}元')
                    else:
                        sender.reply(
                            f'———《订单完成》———\n🎈名称:批量助力\n🎉数量:{len(accounts) * int(mation_int)}月\n💰支付金额:{order}积分')
            else:
                sender.reply('输入错误！')


        else:
            try:
                mation_int = int(mations)
                mation_int = mation_int - 1
                account = acclist[mation_int]
                cookie = sg.bucketGet(bucket='Yzyxmm_elm_account', key=f'{account}')

                accsvip = sg.bucketGet(bucket='Yzyxmm_elm_svip', key=f'{account}')
                zlaccsvip = sg.bucketGet(bucket='Yzyxmm_elm_vip', key=f'{account}')
                bind = sg.bucketGet(bucket='Yzyxmm_elm_phone', key=f'{account}')
                password = sg.bucketGet(bucket='Yzyxmm_elm_password', key=f'{account}')
                if len(accsvip) == 0:
                    accsvip = '未授权'
                elif accsvip < str(now_time):
                    accsvip = '授权过期'
                if len(zlaccsvip) == 0:
                    zlaccsvip = '未授权'
                elif accsvip < str(now_time):
                    zlaccsvip = '授权过期'
                accountzt, binds, username = userdata(cookie)
                if accountzt == '查询失败':
                    accountst = 'Cookie过期'
                else:
                    accountst = '状态正常'
                if len(password) == 0:
                    password = '还没提交'
                else:
                    password = '已经提交'
                '''ck_json = tq2(cookie)
                 passwords = password.split('#')
                ck_json['loginId'] = passwords[0]
                ck_json['password'] = passwords[1]
                cookie = ''
                for field, value in ck_json.items():
                    cookie += f"{field}={value};"
                bind = bind[:3] + "*" * 4 + bind[7:]'''
                sender.reply(
                    f'🤪用户ID:{bind}\n🪫账号状态:{accountst}\n🔥账密状态:{password}\n☁助力授权:{zlaccsvip}\n☁乐园授权:{accsvip}')

                sender.reply('【1】授权乐园\n【2】授权助力\n【3】提交账密\n【4】我要Cookie\n【5】删除账号\n【q】退出')

                mation = sender.input(120000, 1, False)
                if mation == '1':
                    sender.reply('请输入需要的月数,例: 1')
                    mation = sender.input(120000, 1, False)
                    try:
                        mation_int = int(mation)
                        money = Decimal(mation) * Decimal(elm_leyuanmoney)
                        if money == Decimal('0'):
                            empower(empowertime=accsvip, account=account, cookie=cookie, mation_int=mation_int,
                                    phone=bind, osname=elm_leyuanosname, project='Yzyxmm_elm_svip')
                        else:
                            OrderPoints = int(moneycoin) * int(mation_int)
                            Pointpayment(mation_int, accsvip, cookie, account, bind, moneycoin, elm_leyuanosname,
                                         OrderPoints=OrderPoints)
                            zf(money=money, osname=elm_leyuanosname, mation_int=mation_int)
                            empower(empowertime=accsvip, account=account, cookie=cookie, mation_int=mation_int,
                                    phone=bind, osname=elm_leyuanosname, project='Yzyxmm_elm_svip',
                                    OrderPoints=OrderPoints)
                        sender.reply(
                            f'———《订单完成》———\n🎈名称:乐园币\n🎉数量:{mation_int}月\n💰支付金额:{money}元')
                    except ValueError:
                        sender.reply('输入错误')
                elif mation == '2':
                    try:
                        sender.reply('请输入需要的月数,例: 1')
                        mation = sender.input(120000, 1, False)
                        mation_int = int(mation)
                        money = Decimal(mation) * Decimal(elm_zlmoney)
                        if money == Decimal('0'):
                            empower(empowertime=zlaccsvip, account=account, cookie=cookie, mation_int=mation_int,
                                    phone=bind, osname=elm_zlosname, project='Yzyxmm_elm_vip')
                        else:
                            OrderPoints = int(zlmoneycoin) * int(mation_int)
                            Pointpayment(mation_int, zlaccsvip, cookie, account, bind, zlmoneycoin, elm_zlosname,
                                         OrderPoints=OrderPoints)
                            zf(money=money, osname=elm_zlosname, mation_int=mation_int)
                            empower(empowertime=zlaccsvip, account=account, cookie=cookie, mation_int=mation_int,
                                    phone=bind, osname=elm_zlosname, project='Yzyxmm_elm_vip', OrderPoints=OrderPoints)
                        sender.reply(
                            f'———《订单完成》———\n🎈名称:乐园助力\n🎉数量:{mation_int}月\n💰支付金额:{money}元')
                    except ValueError:
                        sender.reply('输入错误')
                elif mation == '3':
                    loginId = str(inputm('请输入11位手机号:', long=11))
                    password = str(inputm('请输入密码:'))
                    ck_json = tq2(cookie)
                    ck_json['loginId'] = loginId
                    ck_json['password'] = password
                    cookie = ''
                    for field, value in ck_json.items():
                        cookie += f"{field}={value};"

                    sg.bucketSet(bucket='Yzyxmm_elm_password', key=f'{account}', value=f'{loginId}#{password}')
                    sg.bucketSet(bucket='Yzyxmm_elm_account', key=f'{account}', value=f'{cookie}')
                    if accsvip != '未授权' and accsvip != '授权过期':
                        Addenvs(osname=elm_leyuanosname, value=cookie, account=account)
                    if zlaccsvip != '未授权' and zlaccsvip != '授权过期':
                        Addenvs(osname=elm_zlosname, value=cookie, account=account)
                    sender.reply('账密提交成功！此功能不会检查账号密码的正确性,请自行检查！')
                elif mation == '4':
                    sender.reply(cookie)
                elif mation == '5':
                    sender.reply(
                        '请确认是否删除该账号？账号删除后授权时间会一同删除，这条信息将会通知管理员处理\n[y]确认丨[n]退出')
                    mation = sender.input(120000, 1, False)
                    if mation == 'y':
                        acclist.remove(f'{account}')
                        qlid, QLurl, qltoken = allenvs(osname=elm_leyuanosname, token=cookie, account=account)
                        delenvs(qlid=qlid, QLurl=QLurl, qltoken=qltoken)
                        qlid, QLurl, qltoken = allenvs(osname=elm_zlosname, token=cookie, account=account)
                        delenvs(qlid=qlid, QLurl=QLurl, qltoken=qltoken)
                        if len(acclist) == 0:
                            sg.bucketDel(bucket='Yzyxmm_elm_bind', key=userid)
                        else:
                            sg.bucketSet(bucket='Yzyxmm_elm_bind', key=userid, value=f'{acclist}')
                        sg.bucketDel(bucket='Yzyxmm_elm_account', key=f'{account}')
                        sg.bucketDel(bucket='Yzyxmm_elm_vip', key=f'{account}')
                        sg.bucketDel(bucket='Yzyxmm_elm_svip', key=f'{account}')
                        sg.bucketDel(bucket='Yzyxmm_elm_vip', key=f'{account}')
                        sg.notifyMasters(
                            content=f'用户:{userid}来自:{imtype}删除了一个账号，请您进行联系下一步的处理',
                            imtypes=['wb', 'tg', 'qb', 'qq'])
                        sender.reply('账号删除成功，并且已经告知管理员！')
                    elif mation == 'n':
                        sender.reply('退出！')
                    else:
                        sender.reply('输入错误')
                elif mation == 'q':
                    sender.reply('退出！')
                else:
                    sender.reply('输入错误！')
            except ValueError as e:
                sender.reply('输入错误')
    else:
        sender.reply('暂未绑定饿了么账号，请获取Cookie后直接发给我！')


def Pointpayment(mation_int, accsvip, cookie, account, bind, coin, osname, OrderPoints, batch=False):
    return True


def empower(empowertime, account, cookie, mation_int, phone, osname, project, OrderPoints=0, batch=False):
    day = mation_int * 30
    Addenvs(osname=osname, value=cookie, account=account, OrderPoints=OrderPoints)
    if empowertime == '授权过期' or empowertime == '未授权' or empowertime <= str(now_time):
        new_time = now_time + timedelta(days=day)
        sg.bucketSet(bucket=project, key=f'{account}',
                             value=str(new_time))
    elif empowertime > str(now_time):
        empower_date = datetime.strptime(empowertime, "%Y-%m-%d")
        delayed_date = empower_date + timedelta(days=day)
        new_time = delayed_date.date()
        sg.bucketSet(bucket=project, key=f'{account}',
                             value=str(new_time))
    else:
        sender.reply('出错')
        exit(0)


def zf(money, osname, mation_int):  # 等待支付并且发送ck到青龙、
    zfzt = False
    if osname == elm_leyuanosname:
        project = '乐园币'
    else:
        project = '乐园助力'
    if zfzt != True:
        sender.reply(f'———《订单结算》———\n🎈名称:{project}\n🎉数量:{mation_int}月\n💰应付:{money}元')
        if zsm == 'true':
            sender.replyImage(wx_zsm)
        else:
            sender.reply(f'支付链接:{wx_zsm}')
        ddzf = False

        if 'Time' in str(ddzf):
            try:
                zfjson = json.loads(ddzf)
                zfmoney = zfjson['Money']
            except Exception:
                zfmoney = ddzf['Money']
            if int(zfmoney) == int(money):
                return
            else:
                sender.reply(f'支付金额错误\n应付:{money}元\n实付:{zfmoney}元\n请稍后核对支付记录！')
                exit(0)

        elif ddzf is None:
            sender.reply('支付超时！')
            exit(0)
        else:
            sender.reply('退出支付')
            exit(0)
    else:
        sender.reply('当前有人正在支付,请稍后再试！')
        exit(0)


def signs(mh5tk, ts, data):
    data_str = json.dumps(data, separators=(',', ':'))

    e = mh5tk + "&" + ts + "&" + '12574478' + "&" + data_str
    sign = hashlib.md5(e.encode()).hexdigest()
    return sign


def res(header, cookie):
    str_header = str(header)
    mh5tk = re.search(r'_m_h5_tk=([^_]+)', str_header).group(1)
    regex1 = r'_m_h5_tk=[0-9a-f]+_[0-9]+;'
    regex2 = r'_m_h5_tk_enc=[0-9a-f]+;'
    str1 = re.search(regex1, str_header).group(0)
    str2 = re.search(regex2, str_header).group(0)
    cookie = re.sub(r'_m_h5_tk=[^;]+;?', '', cookie)
    cookie = re.sub(r'_m_h5_tk_enc=[^;]+;?', '', cookie)
    cookie = str1 + str2 + cookie
    return cookie, mh5tk


def eatapi(cookie):
    try:
        todayeat = 0
        respnse = req(cookie, 'mtop.alibaba.svip.langrisser.query', json.dumps({
            "lgrsRequestItems": "[{\"backup\":false,\"count\":1,\"data\":{\"needHead\":true,\"month\":\"\"},\"resId\":\"867018\"}]",
            "latitude": "33.76706790179014",
            "longitude": "114.37013771384954"}),
                      v="1.0")

        if '未登录' in respnse.text:
            eatcount = '查询失败'
        else:

            eat = respnse.json()
            eatcount = eat['data']['data']['867018']['data'][0]['peaCount']

            records = eat['data']['data']['867018']['data'][0]['accountMonthRecords'][0]['records']

            if records is None:
                return eatcount, '0'
            for eats in records:
                createdTime = eats['createdTime']
                datetime_obj = datetime.strptime(createdTime, "%Y-%m-%d %H:%M:%S")
                recordtime = datetime_obj.strftime("%Y-%m-%d")
                if recordtime < str(now_time):
                    break
                else:
                    count = eats['count']
                    optType = eats['optType']
                    if optType == 2:
                        continue
                    else:
                        todayeat = todayeat + int(count)

        return eatcount, todayeat
    except Exception as e:
        print(e)
        return '查询错误', '查询错误'


def bbf(cookie):
    try:
        url = 'https://wallet.ele.me/api/storedcard/queryBalanceBycardType?cardType=platform'
        headers = {
            "cookie": cookie,
        }
        respnse = requests.get(url=url, headers=headers)
        if '未登录' in respnse.text or '成功' not in respnse.text:
            money = '- -'
        else:
            wallet = respnse.json()
            money = wallet['data']['totalAvailableAmount'] / 100
        return money
    except Exception:
        return '查询错误'


def leyuanB(cookie):
    try:
        mh5tk = 'a8b654ea8b2d8897556edb7eed592e4e'

        for _ in range(2):
            ts = str(time.time() * 1000)
            data = {"templateIds": "[\"1404\"]"}
            sign = signs(mh5tk, ts, data)
            url = f'https://mtop.ele.me/h5/mtop.koubei.interaction.center.common.queryintegralproperty.v2/1.0/?jsv=2.7.0&appKey=12574478&t={ts}&sign={sign}&api=mtop.koubei.interaction.center.common.queryintegralproperty.v2&v=1.0&ecode=1&type=json&valueType=string&needLogin=true&LoginRequest=true&dataType=jsonp'
            headers = {
                "Host": "mtop.ele.me",
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
                "Cookie": cookie,
            }
            data = "data=%7B%22templateIds%22%3A%22%5B%5C%221404%5C%22%5D%22%7D"
            response = requests.post(url, headers=headers, data=data)
            if '调用成功' in response.text:
                leyuan = response.json()
                count = leyuan['data']['data']['1404']['count']

                return count

            else:
                header = response.headers
                cookie, mh5tk = res(header, cookie)
    except Exception:
        return '查询错误'


def Orchard_inquiry(cookie):
    try:
        r = req(cookie, 'mtop.alsc.playgame.orchard.index.batch.query', json.dumps({
            "blockRequestList": "[{\"blockCode\":\"603040_6723057310\",\"status\":\"PUBLISH\",\"tagCallWay\":\"SYNC\",\"useRequestBlockTags\":false}]",
            "source": "KB_ORCHARD", "bizCode": "main",
            "locationInfos": "[{\"latitude\":\"99.597472842782736\",\"longitude\":\"99.75325090438128\",\"lat\":\"99.597472842782736\",\"lng\":\"99.75325090438128\"}]",
            "extData": "{\"ORCHARD_ELE_MARK\":\"KB_ORCHARD\",\"orchardVersion\":\"20240624\"}"}), v="1.0")
        for tag_data in r.json()["data"]["data"]["603040_6723057310"]["blockData"]["role"]["tagData"]:
            for result in tag_data["result"]:
                for role_info in result["roleInfoDtoList"]:
                    for cc in role_info["rolePropertyInfoDtoList"]:
                        remainingProgress = role_info['roleLevelExpInfoDto']["remainingProgress"]
                        levelName = role_info['roleLevelExpInfoDto']["levelName"]
                        return f"\n🍒果树进度:{100 - remainingProgress:.2f}/{levelName}"
        return f"\n🍒果树进度:- -"
    except Exception as e:
        return f"\n🍒果树进度:- -"


def WinningTheTreasureHunt(cookie):
    try:
        WinningInformations = ''

        def get_dates():
            today = datetime.today()
            date_format = "%Y-%m-%d"

            dates = [(today - timedelta(days=i)).strftime(date_format) for i in range(7)]

            return dates

        date = get_dates()
        data = json.dumps(
            {"bizScene": "duobao_external", "blockList": "[\"participants\",\"wonDetail\",\"noWonPrize\"]",
             "channel": "ELMC",
             "pageSize": "50", "rightId": ""})
        api = 'mtop.koubei.interactioncenter.snatch.mine.page'
        res = req(cookie, api, data, v="1.0")
        for prizes in res.json()['data']['list']:
            if prizes['status'] in ['ONLINE', 'DRAWN']:
                continue
            for sj in date:
                if sj in prizes['baseInfo']['awardTime']:
                    title = prizes['baseInfo']['title']
                    if prizes['awardStatus'] in ['not_won_wait_accept', 'not_won_has_finished']:  # 没中奖
                        continue
                    elif prizes['awardStatus'] == 'won_has_finished':  # 中奖

                        WinningInformations += f'\n🍡夺宝中奖:{title}'
                    else:  # 可能中奖了
                        WinningInformations += f'\n🍡夺宝中奖:{title}'
        if WinningInformations == '':
            return '\n🍡夺宝中奖:- -'
        return WinningInformations
    except Exception as e:
        sender.reply(f'{e}')
        return '\n🍡夺宝中奖:- -'


def OrchardExchangeVoucher(cookie):
    try:
        respnse = req(cookie, 'mtop.koubei.interaction.center.common.queryintegralproperty.v2',
                      json.dumps({"templateIds": "[\"497\"]"}), v="1.0")
        count = respnse.json()['data']['data']['497']['count']
        return f"\n🌸果园兑换卡:{count}"

    except Exception:
        return f"\n🌸果园兑换卡:- -"


def todayreques(cookie):
    try:
        Bdetailed = {}
        pageNo = 1
        retrynum = 0
        todayleyuanB = 0
        mh5tk = 'a8b654ea8b2d8897556edb7eed592e4e'
        while True:
            ts = str(time.time() * 1000)
            data = {"templateId": "1404", "bizScene": "game_center", "convertType": "GAME_CENTER",
                    "startTime": "2023-1-5 00:00:00", "pageNo": str(pageNo), "pageSize": "100"}
            sign = signs(mh5tk, ts, data)
            url = f'https://mtop.ele.me/h5/mtop.koubei.interaction.center.common.querypropertydetail/1.0/5.0/?jsv=2.7.0&appKey=12574478&t={ts}&sign={sign}&api=mtop.koubei.interaction.center.common.querypropertydetail&v=1.0&ecode=1&type=json&valueType=string&needLogin=true&LoginRequest=true&dataType=jsonp'
            headers = {
                "Host": "mtop.ele.me",
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
                "Content-type": "application/x-www-form-urlencoded;charset=UTF-8",
                "Origin": "https://tb.ele.me",
                "Referer": "https://tb.ele.me/",
                "Accept-Language": "zh-CN,zh-Hans;q=0.9",
                "x-ele-check-client": "ele",
                "Content-Length": "214",
                "Connection": "keep-alive",
                "Cookie": cookie
            }
            data = f'{{"templateId":"1404","bizScene":"game_center","convertType":"GAME_CENTER","startTime":"2023-1-5 00:00:00","pageNo":"{pageNo}","pageSize":"100"}}'
            encoded_string = urllib.parse.quote(data, safe='')
            response = requests.post(url, headers=headers, data=f'data={encoded_string}')
            if '调用成功' in response.text:
                tleyuan = response.json()
                list = tleyuan['data']['list']
                if len(list) == 0:
                    return todayleyuanB, Bdetailed
                for details in list:
                    gmtModifiedStr = details['gmtModifiedStr']
                    datetime_obj = datetime.strptime(gmtModifiedStr, "%Y-%m-%d %H:%M:%S")
                    recordtime = datetime_obj.strftime("%Y-%m-%d")
                    if recordtime < str(now_time):
                        return todayleyuanB, Bdetailed
                    else:
                        amount = details['amount']
                    detailType = details['detailType']
                    if detailType == 'REDUCE':
                        continue
                    else:
                        bizName = details['extInfo']['desc']
                        bizName = bizName.replace("玩一玩", "")
                        bizName = bizName.replace("玩", "")
                        if bizName in Bdetailed:
                            Bdetailed[bizName] = Bdetailed[bizName] + int(amount)
                        else:
                            Bdetailed[bizName] = int(amount)

                        todayleyuanB = todayleyuanB + int(amount)
                detailss = list[-1]
                gmtModifiedStr = detailss['gmtModifiedStr']
                datetime_obj = datetime.strptime(gmtModifiedStr, "%Y-%m-%d %H:%M:%S")
                recordtime = datetime_obj.strftime("%Y-%m-%d")
                if recordtime < str(now_time):
                    return todayleyuanB, Bdetailed
                else:
                    pageNo = pageNo + 1
                    continue

            else:
                if retrynum == 2:
                    exit(0)
                retrynum = retrynum + 1
                header = response.headers
                cookie, mh5tk = res(header, cookie)
    except Exception as e:
        print(e)
        return '查询错误', '查询错误'


def Checkcoupons():
    message = f'🌸大额券:'
    try:
        res = req(cookie, 'mtop.alsc.personal.querypasslist4native', json.dumps(
            {"condition": "", "cityCode": "411600", "latitude": "33.76706790179014", "tabCode": "HONG_BAO",
             "userId": "6011282906", "extInfo": "", "longitude": "114.37013771384954", "sourceFrom": "ELEME_APP",
             "userGeoHash": "ww124e1g3mey"}))
        for Coupons in res.json()['data']['data']['vouchers_list_component']['fields']['items']:
            Couponamount = Coupons['amountText']['yuanText']
            message += f'[{Couponamount}]'
        return message
    except Exception:
        message += f'--'


def cx(cookie):
    money = bbf(cookie)
    eatcount, todayeat = eatapi(cookie)
    count = leyuanB(cookie)
    todayleyuanB, Bdetailed = todayreques(cookie)
    return count, money, eatcount, todayeat, todayleyuanB


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


def cxs():
    accounts = sg.bucketGet(bucket='Yzyxmm_elm_bind', key=userid)
    message = ''
    count = 4
    if len(accounts) != 0:
        acclist = _sg_literal(accounts)
        for accid in acclist:
            cookie = sg.bucketGet(bucket='Yzyxmm_elm_account', key=accid)
            bind = sg.bucketGet(bucket='Yzyxmm_elm_phone', key=f'{accid}')
            bind = bind[:3] + "*" * 4 + bind[7:]
            message += f'\n【{count}】丨{bind}'
            count = count + 1
        message_to_send = f"———《饿了查询》———\n【0】常规全部【1】今日总币\n【2】当前总币【3】今日明细{message}"
        sender.reply(message_to_send)
        sender.reply('请输入【】中需要查询的账号:')
        mations = sender.input(120000, 1, False)

        if mations == '0':
            sender.reply('正在获取数据....')
            acclist = _sg_literal(accounts)
            for account in acclist:
                cookie = sg.bucketGet(bucket='Yzyxmm_elm_account', key=f'{account}')
                accsvip = sg.bucketGet(bucket='Yzyxmm_elm_svip', key=f'{account}')
                zlaccsvip = sg.bucketGet(bucket='Yzyxmm_elm_vip', key=account)
                count = '查询失败'
                eatcount = '查询失败'
                money = '查询失败'
                todayeat = '查询失败'
                todayleyuanB = '查询失败'
                if len(accsvip) == 0:
                    count = accsvip = '未授权'
                elif accsvip < str(now_time):
                    count = accsvip = '云授权过期'
                if len(accsvip) == 0:
                    count = accsvip = '未授权'
                elif accsvip < str(now_time):
                    count = accsvip = '云授权过期'
                if len(zlaccsvip) == 0:
                    zlaccsvip = '未授权'
                elif zlaccsvip < str(now_time):
                    zlaccsvip = '云授权过期'
                account2, bind, username = userdata(cookie)
                if account2 == '查询失败':
                    bind = sg.bucketGet(bucket='Yzyxmm_elm_phone', key=f'{account}')
                    bind = bind[:3] + "*" * 4 + bind[7:]
                    sender.reply(
                        f'【{bind}】账号Cookie过期')
                else:
                    if accsvip not in ['未授权', '云授权过期'] or zlaccsvip not in ['未授权', '云授权过期']:
                        count, money, eatcount, todayeat, todayleyuanB = cx(cookie)

                        sender.reply(
                            f'🤪用户ID:{bind}\n📒今日乐园币:{todayleyuanB}\n🎈乐园币:{count}\n🔥今日吃货豆:{todayeat}\n🎉饿了吃货豆:{eatcount}{Orchard_inquiry(cookie)}{OrchardExchangeVoucher(cookie)}\n💰钱包余额:{money}{WinningTheTreasureHunt(cookie)}')

                        bind = bind[:3] + "*" * 4 + bind[7:]

                    else:
                        bind = bind[:3] + "*" * 4 + bind[7:]
                        sender.reply(
                            f'【{bind}】账号{accsvip}')
        elif mations == '1' or mations == '2' or mations == '3':
            sender.reply('正在努力获取数据....')
            acclist = _sg_literal(accounts)
            message = ''
            AlltodayleyuanB = 0
            AllleyuanB = 0
            todayleyuanB = 0
            success = 0
            for account in acclist:

                cookie = sg.bucketGet(bucket='Yzyxmm_elm_account', key=f'{account}')
                accsvip = sg.bucketGet(bucket='Yzyxmm_elm_svip', key=f'{account}')
                zlaccsvip = sg.bucketGet(bucket='Yzyxmm_elm_vip', key=f'{account}')
                count = '查询失败'
                eatcount = '查询失败'
                money = '查询失败'
                todayeat = '查询失败'
                todayleyuanB = '查询失败'
                if len(accsvip) == 0:
                    count = accsvip = '未授权'
                elif accsvip < str(now_time):
                    count = accsvip = '云授权过期'
                if len(zlaccsvip) == 0:
                    zlaccsvip = '未授权'
                elif zlaccsvip < str(now_time):
                    zlaccsvip = '云授权过期'
                account2, bind, username = userdata(cookie)
                if account2 == '查询失败':
                    bind = sg.bucketGet(bucket='Yzyxmm_elm_phone', key=f'{account}')
                    bind = bind[:3] + "*" * 4 + bind[7:]
                    sender.reply(
                        f'【{bind}】账号Cookie过期')
                else:

                    if accsvip not in ['未授权', '云授权过期'] or zlaccsvip not in ['未授权', '云授权过期']:
                        if mations == '1':
                            todayleyuanB, Bdetailed = todayreques(cookie)
                            if todayleyuanB == '查询错误':
                                sender.reply(f'【{bind}】查询出错')
                                continue
                            bind = bind[:3] + "*" * 4 + bind[7:]
                            success += 1
                            message += f'\n【{bind}】丨{todayleyuanB}'
                            AlltodayleyuanB += todayleyuanB
                        if mations == '2':
                            leyuanBs = leyuanB(cookie)
                            if leyuanBs == '查询错误':
                                sender.reply(f'【{bind}】查询出错')
                                continue
                            success += 1
                            bind = bind[:3] + "*" * 4 + bind[7:]
                            message += f'\n【{bind}】丨{leyuanBs}'
                            AllleyuanB += leyuanBs
                        if mations == '3':
                            message = ''
                            todayleyuanB, Bdetailed = todayreques(cookie)
                            if todayleyuanB == '查询错误':
                                sender.reply(f'【{bind}】查询出错')
                                continue
                            if todayleyuanB == 0:
                                sender.reply(f'【{bind}】今日0币')
                                continue

                            bind = bind[:3] + "*" * 4 + bind[7:]
                            for key, value in Bdetailed.items():
                                message += f'\n【{key}】丨{value}'
                            sender.reply(f'———《{bind}》———\n【今日总币】丨{todayleyuanB}{message}')
                    else:
                        bind = bind[:3] + "*" * 4 + bind[7:]
                        sender.reply(
                            f'【{bind}】账号{accsvip}')
            if mations == '1':
                if success != 0:
                    sender.reply(f'【今日总币】丨{AlltodayleyuanB}{message}')

            if mations == '2':
                if success != 0:
                    sender.reply(f'【当前总币】丨{AllleyuanB}{message}')

        else:

            try:
                mation_int = int(mations)
                mation_int = mation_int - 4
                account = acclist[mation_int]
                sender.reply('正在努力获取数据...')
                cookie = sg.bucketGet(bucket='Yzyxmm_elm_account', key=account)
                bind = sg.bucketGet(bucket='Yzyxmm_elm_phone', key=f'{account}')
                accsvip = sg.bucketGet(bucket='Yzyxmm_elm_svip', key=account)
                zlaccsvip = sg.bucketGet(bucket='Yzyxmm_elm_vip', key=f'{account}')

                if len(accsvip) == 0:
                    count = accsvip = '未授权'
                elif accsvip < str(now_time):
                    count = accsvip = '云授权过期'
                if len(zlaccsvip) == 0:
                    zlaccsvip = '未授权'
                elif zlaccsvip < str(now_time):
                    zlaccsvip = '云授权过期'

                account2, bind, username = userdata(cookie)
                if account2 == '查询失败':
                    bind = sg.bucketGet(bucket='Yzyxmm_elm_phone', key=f'{account}')
                    bind = bind[:3] + "*" * 4 + bind[7:]
                    sender.reply(
                        f'【{bind}】Cookie过期')
                else:
                    if accsvip not in ['未授权', '云授权过期'] or zlaccsvip not in ['未授权', '云授权过期']:
                        count, money, eatcount, todayeat, todayleyuanB = cx(cookie)
                        bind = bind[:3] + "*" * 4 + bind[7:]
                        sender.reply(
                            f'🤪用户ID:{bind}\n📒今日乐园币:{todayleyuanB}\n🎈乐园币:{count}\n🔥今日吃货豆:{todayeat}\n🎉饿了吃货豆:{eatcount}{Orchard_inquiry(cookie)}{OrchardExchangeVoucher(cookie)}\n💰钱包余额:{money}{WinningTheTreasureHunt(cookie)}')

                    else:
                        bind = bind[:3] + "*" * 4 + bind[7:]
                        sender.reply(
                            f'【{bind}】账号{accsvip}')
            except ValueError:
                sender.reply('输入错误！')


    else:
        sender.reply('未绑定饿了么账号，请获取Cookie后直接发给我！')


def AlluserTreasureHunt():
    sender.reply('正在检索所有用户的中奖信息，该过程时间较长 请耐心等待...')
    message = ''
    bindlist = sg.bucketAllKeys(bucket='Yzyxmm_elm_bind')
    for user in bindlist:
        accouts = sg.bucketGet(bucket='Yzyxmm_elm_bind', key=f'{user}')
        accouts = _sg_literal(accouts)
        UserHeader = f'\n{user}:'
        for account in accouts:
            '''if len(accsvip) == 0:
                accsvip = '未授权'
            elif accsvip < str(now_time):
                accsvip = '云授权过期'
            if len(accsvip) == 0:
                accsvip = '未授权'
            elif accsvip < str(now_time):
                accsvip = '云授权过期'
            if len(zlaccsvip) == 0:
                zlaccsvip = '未授权'
            elif zlaccsvip < str(now_time):
                zlaccsvip = '云授权过期'''
            cookie, bind, accsvip, zlaccsvip = getaccountmes(account)
            if accsvip in ['未授权', '授权过期'] and zlaccsvip in ['未授权', '授权过期']:
                continue
            account, bind, username = userdata(cookie)

            if account == '查询失败':
                continue
            WinningInformations = WinningTheTreasureHunt(cookie)
            if WinningInformations == '\n🍡夺宝中奖:- -':
                continue
            UserHeader += f"\n———《{bind}》———{WinningInformations}"
        if UserHeader == f'\n{user}:':
            continue
        message += UserHeader
    if message == '':
        sender.reply('检索所有用户均无中奖信息')
        exit(0)
    sender.reply(f'{message}')


today_date = datetime.now().date()
today_time = str(today_date)
now_time = datetime.now().date()
qljson = seekql()
zsm, wx_zsm, elm_leyuanmoney, elm_leyuanosname, moneycoin, randommanagecommand, randomquerycommand, elm_container_max, elm_zlmoney, elm_zlosname, zlmoneycoin, elm_zlcontainer_max = getusercontent()
imtype = sender.getImtype()
usermessage = sender.getMessage()
messageID = sender.getMessageID()
if 'cookie2=' in usermessage and 'SID=' in usermessage and 'USERID=' in usermessage:
    A = sender.recallMessage(messageID)
    sign(usermessage)
elif '我快饿死了' in usermessage or '管理' in usermessage:
    manage()
elif '吃饱了' in usermessage or '查询' in usermessage:
    cxs()
elif '夺宝' in usermessage:
    if sender.isAdmin():
        AlluserTreasureHunt()
    else:
        sender.reply('无权使用！')


elif imtype == 'fake':
    bindlist = sg.bucketAllKeys(bucket='Yzyxmm_elm_bind')
    for user in bindlist:
        accouts = sg.bucketGet(bucket='Yzyxmm_elm_bind', key=f'{user}')
        accoutlist = _sg_literal(accouts)
        for useraccount in accoutlist:
            cookie = sg.bucketGet(bucket='Yzyxmm_elm_account', key=f'{useraccount}')
            phone = sg.bucketGet(bucket='Yzyxmm_elm_phone', key=f'{useraccount}')
            empower = sg.bucketGet(bucket='Yzyxmm_elm_svip', key=f'{useraccount}')
            zlempower = sg.bucketGet(bucket='Yzyxmm_elm_vip', key=f'{useraccount}')
            account, bind, username = userdata(cookie)
            if '查询失败' in bind:
                push(user=user, mobile=phone, message='饿了么Cookie已过期,请及时更新！')
            if len(empower) == 0:
                pass
            elif str(now_time) > empower:
                qlid, QLurl, qltoken = allenvs(osname=elm_leyuanosname, token=cookie, account=useraccount)
                delenvs(qlid=qlid, QLurl=QLurl, qltoken=qltoken)
                push(user=user, mobile=phone, message=f'饿了么授权已过期,可发送‘{randommanagecommand}’进行授权！')
            if len(zlempower) == 0:
                pass
            elif str(now_time) > zlempower:
                qlid, QLurl, qltoken = allenvs(osname=elm_zlosname, token=cookie, account=useraccount)
                delenvs(qlid=qlid, QLurl=QLurl, qltoken=qltoken)
                push(user=user, mobile=phone, message=f'饿了么助力授权已过期,可发送‘{randommanagecommand}’进行授权！')

else:
    sender.setContinue()
