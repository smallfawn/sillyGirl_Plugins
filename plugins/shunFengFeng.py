# [title: 顺丰丰]
# [name: shunFengFeng]
# [language: python]
# [class: 任务]
# [author: Lxg-021002]
# [version: v1.0.6]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^顺风登录$|^顺风登陆$|^登陆顺风$|^登录顺风$|^顺风查询$|^查询顺风$|^顺风管理$|^管理顺风$|^顺丰登录$|^顺丰登陆$|^登陆顺丰$|^登录顺丰$|^顺丰查询$|^查询顺丰$|^顺丰管理$|^管理顺丰$]
# [cron: 56 6,9,13,16,19,20 * * *]
# [icon: https://img.icons8.com/fluency/96/plugin.png]
# [description: 顺丰账号登录、查询和任务管理。]
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
    "enable": plugin.Form.boolean().title("是否启用").default(True),
    'Yzyxmm_sf_Yzyxmm_sf_Qinglong': plugin.Form.string().title('设置对接容器').default('').description('你的变量需要添加到的容器？参数用丨分割，这个符号是中文的竖(直接复制)'),
    'Yzyxmm_sf_Yzyxmm_sf_osname': plugin.Form.string().title('提交到青龙的变量名').default('').description('青龙容器内顺丰的变量名'),
})
_CONFIG_FIELD_MAP = {
    ('Yzyxmm_sf', 'Yzyxmm_sf_Qinglong'): 'Yzyxmm_sf_Yzyxmm_sf_Qinglong',
    ('Yzyxmm_sf', 'Yzyxmm_sf_osname'): 'Yzyxmm_sf_Yzyxmm_sf_osname',
}

import re
from datetime import datetime, timedelta
from decimal import Decimal
import requests
import time
import json
import hashlib
import urllib.parse
import uuid

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()
uservalue = sg.bucketGet(bucket='Yzyxmm_sf_bind', key=userid)

def getusercontent():
    Yzyxmm_sf_osname = sg.bucketGet(bucket='Yzyxmm_sf', key='Yzyxmm_sf_osname')  # 变量
    Yzyxmm_sf_qlname = sg.bucketGet(bucket='Yzyxmm_sf', key='Yzyxmm_sf_Qinglong')  # 青龙
    sfVipmoney = sg.bucketGet(bucket='Yzyxmm_sf', key='sfVipmoney')
    sfcoin = sg.bucketGet(bucket='Yzyxmm_sf', key='sfcoin')
    if len(Yzyxmm_sf_osname) == 0:
        sender.reply("顺丰变量名称未填写")
        exit(0)
    '''if len(Yzyxmm__managecommand) == 0:
        Yzyxmm__managecommand = '顺丰管理'
    randommanagecommand = Yzyxmm__managecommand
    if '丨' in Yzyxmm__managecommand:
        parts = Yzyxmm__managecommand.split('丨')
        randommanagecommand = random.choice(parts)

    if len(Yzyxmm_querycommand) == 0:
        Yzyxmm_querycommand = '顺丰查询'
    randomquerycommand = Yzyxmm_querycommand
    if '丨' in Yzyxmm_querycommand:
        parts = Yzyxmm_querycommand.split('丨')
        randomquerycommand = random.choice(parts)
    if len(Yzyxmm_signcommand) == 0:
        Yzyxmm_signcommand = '顺丰登录'
    randomsigncommand = Yzyxmm_signcommand
    if '丨' in Yzyxmm_signcommand:
        parts = Yzyxmm_signcommand.split('丨')
        randomsigncommand = random.choice(parts)'''
    if len(sfVipmoney) == 0 or sfVipmoney == '0':
        sfVipmoney = Decimal('0')
    if len(sfcoin) == 0:
        sfcoin = 9999
    else:
        sfcoin = int(sfcoin)
    Yzyxmm__managecommand = '顺丰管理'
    Yzyxmm_querycommand = '顺丰查询'
    Yzyxmm_signcommand = '顺丰登录'
    randommanagecommand = '顺丰管理'
    randomquerycommand = '顺丰查询'
    randomsigncommand = '顺丰登录'
    return Yzyxmm_sf_osname, Yzyxmm_sf_qlname, Yzyxmm__managecommand, Yzyxmm_querycommand, Yzyxmm_signcommand, randommanagecommand, randomquerycommand, randomsigncommand, sfVipmoney, sfcoin

def seekql():
    try:
        if len(Yzyxmm_sf_qlname) == 0:
            sender.reply('顺丰丰未填写插件对接的容器，请检查配参')
            exit(0)
        else:
            qllist = Yzyxmm_sf_qlname.split('丨')
            QLurl = qllist[0]
            ClientID = qllist[1]
            ClientSecret = qllist[2]
            qltoken = QLtoken(QLurl=QLurl, ClientID=ClientID, ClientSecret=ClientSecret)
            return QLurl, qltoken
    except Exception:
        sender.reply("获取青龙token失败")
        exit(0)

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
    requests.delete(url, headers=headers, json=data).json()

def allenvs(osname, account):
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

def QLupdate(osname, value, account, qlid, phone):
    qlurl = f"{QLurl}/open/envs"
    data = {
        "value": value,
        "name": osname,
        "remarks": f'顺丰:{account}丨用户:{userid}丨手机:{phone}丨顺丰丰管理',
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

def Addenvs(osname, value, account, phone):
    phone = phone[:3] + '*' * 4 + phone[7:]
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
    value = urllib.parse.quote(value)
    if qlid is None:

        QLzt(osname, value, account, phone)
    else:
        QLupdate(osname, value, account, qlid, phone)

def QLzt(osname, value, account, phone):  # 添加青龙变量
    try:
        qlurl = f"{QLurl}/open/envs"
        data = [{
            "value": value,
            "name": osname,
            "remarks": f'顺丰:{account}丨用户:{userid}丨手机:{phone}丨顺丰丰管理'
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

def session_ids(url):
    response = requests.get(url, allow_redirects=False)
    session_id_pattern = r'sessionId=([^;]+);'
    login_mobile_pattern = r'_login_mobile_=([^;]+);'
    session_id = re.search(session_id_pattern, str(response.headers)).group(1)
    login_mobile = re.search(login_mobile_pattern, str(response.headers)).group(1)
    if session_id and login_mobile and '用户手机号校验未通过' not in response.text:
        return session_id, login_mobile
    else:
        sender.reply('用户信息无效，请检查')
        exit(0)

def Honey(session_id):
    url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~receiveExchangeIndexService~indexData"

    headers = {
        "Cookie": f"sessionId={session_id}"
    }
    data = {}
    response = requests.post(url, headers=headers, json=data)
    honeydata = response.json()
    if '用户手机号校验未通过' not in response.text:
        capacity = honeydata['obj']['capacity']
        usableHoney = honeydata['obj']['usableHoney']
    else:
        capacity = '校验未通过'
        usableHoney = '0'
    return capacity, usableHoney

def todaycoin(session_id):
    pageNo = 1
    coin = 0
    while True:
        url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberIntegral~memberPoint~queryMemberPointDetail"

        headers = {
            "Cookie": f"sessionId={session_id}"
        }

        data = {
            "type": "ALL",
            "pageNo": pageNo,
            "pageSize": 10
        }

        response = requests.post(url, headers=headers, json=data).json()
        success = response['success']
        data = response['obj']['data']
        if len(data) < 1:
            return 0, '0'
        if success:
            allcoin = response['obj']['usablePoint']
            for coinjson in data:
                createTm = coinjson['createTm']
                datetime_obj = datetime.strptime(createTm, "%Y-%m-%d %H:%M:%S")
                date_str = datetime_obj.strftime("%Y-%m-%d")
                if date_str < str(today_time):
                    break
                else:
                    opCode = coinjson['opCode']
                    pointVal = coinjson['pointVal']
                    if opCode == 'ADD':
                        coin = coin + int(pointVal)
                    else:
                        continue
            createTm = data[-1]['createTm']
            datetime_obj = datetime.strptime(createTm, "%Y-%m-%d %H:%M:%S")
            date_str = datetime_obj.strftime("%Y-%m-%d")
            if date_str >= str(today_time):
                pageNo = pageNo + 1
            else:
                break
    return coin, allcoin

def todayhoney(session_id):
    pageNo = 1
    honey = 0
    while True:
        url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~receiveExchangeIndexService~detail"

        headers = {
            "Cookie": f"sessionId={session_id}"
        }

        data = {
            "pageNo": pageNo,
            "pageSize": 10
        }

        response = requests.post(url, headers=headers, json=data).json()
        success = response['success']
        if success:
            allhoney = response['obj']['usableHoney']
            data = response['obj']['data']
            if len(data) == 0:
                break
            for coinjson in data:
                createTm = coinjson['time']
                datetime_obj = datetime.strptime(createTm, "%Y-%m-%d %H:%M:%S")
                date_str = datetime_obj.strftime("%Y-%m-%d")
                if date_str < str(today_time):
                    break
                else:
                    pointVal = coinjson['value']
                    if '-' not in pointVal:
                        honey = honey + int(pointVal)
                    else:
                        continue
            createTm = data[-1]['time']
            datetime_obj = datetime.strptime(createTm, "%Y-%m-%d %H:%M:%S")
            date_str = datetime_obj.strftime("%Y-%m-%d")
            if date_str >= str(today_time):
                if len(data) < 10:
                    break
                else:
                    pageNo = pageNo + 1
            else:
                break
    return honey, allhoney

def ValueErrors(value, count):
    try:
        value = int(value)
        if value > count or value == 0:
            sender.reply('输入错误！')
            exit(0)
        return value
    except ValueError:
        sender.reply('输入错误！')
        exit(0)

def sytTokens(payload, deviceId):
    t = int(time.time() * 1000)
    datamd5 = generate_md5(payload + '&080R3MAC57J2{A19!$3:WO{I<1N$31BI')
    deviceidmd5 = generate_md5(
        deviceId + f'{t}' + '9.65.302NBF+BE4{@P:@X${Q9BAE>{PAK!D:N*^CNsc' + datamd5 + '705088894ad6ef475bdf4875c9d533b8&2NBF+BE4{@P:@X${Q9BAE>{PAK!D:N*^')

    sytToken = generate_md5(deviceidmd5 + '&0HQ%H91K&AA{DH$*XV>XR)VKL:QFE{&%')
    return sytToken, t

def generate_md5(input_string):
    md5_hash = hashlib.md5()
    md5_hash.update(input_string.encode('utf-8'))
    md5_digest = md5_hash.hexdigest()

    return md5_digest

def ScanCodeLogin():
    try:
        sender.reply('正在加载二维码...')
        url = 'http://yi100.top:1222/wxcode'
        data = {'project': 'sf', 'type': 'qrcode'}
        response = requests.get(url, json=data)
        QRcode = response.json()['data']['QRcode']
        QRcodeImg = response.json()['data']['QRcodeImg']

        sender.replyImage(QRcodeImg)
        sender.reply(
            '请使用微信扫描该二维码，使用机器人前请确保使用微信登录过一次App')
        retry = 60
        while True:
            time.sleep(1)
            data = {'project': 'sf', 'type': 'code', 'QRcode': QRcode}
            response = requests.get(url, json=data)
            if '成功' in response.text:
                code = response.json()['data']['code']
                break
            else:
                retry += -1
                if retry == 0:
                    sender.reply('扫码超时！')
                    exit(0)
        deviceId = str(uuid.uuid4())
        url = "https://ccsp-egmas.sf-express.com/cx-app-member/member/app/weixin/getAccessTokenByCode"

        payload = json.dumps({
            "code": code
        })
        sytToken, t = sytTokens(payload, deviceId)
        headers = {
            'User-Agent': "okhttp/4.9.1",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'Content-Type': "application/json",
            'jsbundle': "705088894ad6ef475bdf4875c9d533b8",
            'clientVersion': "9.65.30",
            'languageCode': "sc",
            'systemVersion': "13",
            'deviceId': deviceId,
            'regionCode': "CN",
            'carrier': "unknown",
            'screenSize': "1080x2400",
            'sytToken': sytToken,
            'timeInterval': f"{t}",
            'model': "MEIZU 20",
            'mediaCode': "AndroidML"
        }
        response = requests.post(url, data=payload, headers=headers)
        url = "https://ccsp-egmas.sf-express.com/cx-app-member/member/app/user/universalSign"
        account = response.json()['obj']['memInfos'][0]['userId']
        memNo = response.json()['obj']['memInfos'][0]['memNo']
        mobile = response.json()['obj']['memInfos'][0]['mobile']
        payload = json.dumps({
            "mobile": mobile,
            "userId": account,
            "memNo": memNo,
            "name": "mcs-mimp-web.sf-express.com",
            "extra": "",
            "needReqTime": "1"
        })
        sytToken, t = sytTokens(payload, deviceId)
        headers['sytToken'] = sytToken
        headers['timeInterval'] = str(t)
        response = requests.post(url, data=payload, headers=headers)
        sign = response.json()['obj']['sign']
        encoded_string = urllib.parse.quote(sign)
        Token = f'https://mcs-mimp-web.sf-express.com/mcs-mimp/share/app/shareRedirect?sign={encoded_string}&source=SFAPP&bizCode=619'
        account = mobile
        mobile = mobile[:3] + '*' * 4 + mobile[7:]

        return Token, str(account), mobile
    except Exception:
        sender.reply('登录出错！')
        exit(0)

def bindaccount():
    def accvip(Newaddition):
        if len(accountVip) != 0 and accountVip >= today_time:
            Addenvs(osname=Yzyxmm_sf_osname, value=f'{Token}', account=account, phone=mobile)
            if Newaddition:
                accounts.append(account)
                sender.reply(f'🤪{mobile}添加成功，可对我说‘{randommanagecommand}’对账号进行管理！')
            else:
                sender.reply(f'🤪{mobile}更新成功，可对我说‘{randommanagecommand}对账号进行管理！')

        else:
            if Newaddition:
                accounts.append(account)
                sender.reply(f'🤪{mobile}添加成功，可对我说‘{randommanagecommand}对账号进行管理！')
            else:
                sender.reply(f'🤪{mobile}更新成功,授权已过期！可对我说‘{randommanagecommand}对账号进行授权！')
        sg.bucketSet(bucket='Yzyxmm_sf_bind', key=userid, value=f'{accounts}')

    Token, account, mobile = ScanCodeLogin()
    session_id, login_mobile = session_ids(Token)
    accountVip = sg.bucketGet(bucket='Yzyxmm_sf_Vip', key=account)
    sg.bucketSet(bucket='Yzyxmm_sf_account', key=account, value=Token)
    if len(uservalue) == 0:
        accounts = []
        accvip(True)
    else:
        accounts = _sg_literal(uservalue)
        if account in accounts:
            accvip(False)
        else:
            accvip(True)

def empower(empowertime, me_as_int):
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

def meituanmanage():
    if len(uservalue) != 0:
        count = 1
        message = ''
        accounts = _sg_literal(uservalue)

        for account in accounts:
            accountVip = sg.bucketGet(bucket='Yzyxmm_sf_Vip', key=f'{account}')
            if len(accountVip) == 0:
                accountVip = '未授权'
            elif accountVip < today_time:
                accountVip = '授权过期'
            login_mobile = account[:3] + "****" + account[7:]
            message += f'[{count}]-----\n🤪用户ID:{login_mobile}\n☁云授权:{accountVip}\n'
            count += 1
        sender.reply(f'=====我的顺丰=====\n{message}')
        sender.reply('请选择[]内的数字对顺丰账号进行管理，回复‘q’退出')
        inputmessage = sender.input(120000, 1, False)
        if inputmessage == 'timeout':
            sender.reply('超时退出！')
            exit(0)
        elif inputmessage == 'q':
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
        account = accounts[me_as_int - 1]
        userurl = sg.bucketGet(bucket='Yzyxmm_sf_account', key=f'{account}')
        accountVip = sg.bucketGet(bucket='Yzyxmm_sf_Vip', key=f'{account}')
        session_id, login_mobile = session_ids(userurl)
        if len(accountVip) == 0:
            accountVipst = '未授权'
        elif accountVip < today_time:
            accountVipst = '授权过期'
        else:
            accountVipst = accountVip
        login_mobile = login_mobile[:3] + "****" + login_mobile[7:]
        sender.reply(f'‍🤪用户ID:{login_mobile}\n☁云授权:{accountVipst}')
        sender.reply('[1]丨授权账号 [2]丨关停服务\n[q]丨退出')
        inputmessage = sender.input(120000, 1, False)
        if inputmessage == '2':
            sender.reply('确定要删除这个账号吗？请您三思！')
            sender.reply('[y] 是丨[n] 否')
            yesorno = sender.input(120000, 1, False)
            if yesorno == 'Y' or yesorno == 'y' or yesorno == '是':
                accounts.remove(str(account))
                qlid = allenvs(osname=Yzyxmm_sf_osname, account=str(account))
                delenvs(id=qlid)
                if len(accounts) == 0:
                    sg.bucketDel(bucket='Yzyxmm_sf_bind', key=userid)
                else:
                    sg.bucketSet(bucket='Yzyxmm_sf_bind', key=userid, value=f'{accounts}')
                sender.reply('删除成功，感谢您的使用！')
            elif yesorno == 'n' or yesorno == 'N' or yesorno == '否':
                sender.reply('退出！')
                exit(0)
        elif inputmessage == '1':
            sender.reply('请输入需要的月数:例1')
            mes = sender.input(120000, 1, False)
            mes = ValueErrors(value=mes, count=999)
            money = Decimal(mes) * Decimal(sfVipmoney)
            zf(project='顺丰授权', me_as_int=mes, accountVip=accountVip, token=urllib.parse.quote(userurl),
               phone=account, account=account)
            accountVip = empower(empowertime=accountVip, me_as_int=mes)
            Addenvs(osname=Yzyxmm_sf_osname, value=f'{userurl}', account=account, phone=login_mobile)
            sg.bucketSet(bucket='Yzyxmm_sf_Vip', key=f'{account}', value=f'{accountVip}')
            sender.reply(f'=====订单完成=====\n🎈名称:顺丰授权\n🎉数量:{mes}\n💰付款金额:{money}元')
        elif inputmessage == 'q' or inputmessage == 'Q':
            sender.reply('退出！')

    else:
        sender.reply('未绑定顺丰账号，请先发送顺丰登录.')

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
        sender.reply('退出！')
        exit(0)
    else:
        sender.reply('输入错误！')
        exit(0)

def zf(project, me_as_int, accountVip, token, phone, account):  # 等待支付并且发送ck到青龙
    def Pointpayment(mation_int, accountVip, token, phone, account):
        usercoin = sg.bucketGet(bucket='Yzyxmm_sign_coin', key=f'{userid}')
        login_mobile = account[:3] + "****" + account[7:]
        if len(usercoin) != 0 and usercoin != '0':
            zfcoin = int(sfcoin) * mation_int
            if int(usercoin) >= int(zfcoin):
                sender.reply(f'当前积分{usercoin}积分，订单所需{zfcoin}积分是否使用积分进行抵扣？')
                sender.reply('[y]是丨[n]否')
                if yesornos():
                    usercoin = int(usercoin) - int(zfcoin)
                    sg.bucketSet(bucket='Yzyxmm_sign_coin', key=f'{userid}',
                                         value=f'{usercoin}')
                    accountVip = empower(empowertime=accountVip, me_as_int=me_as_int)
                    sg.bucketSet(bucket='Yzyxmm_sf_Vip', key=account, value=accountVip)
                    Addenvs(osname=Yzyxmm_sf_osname, value=f'{token}', account=account, phone=login_mobile)
                    sender.reply(f'=====订单完成=====\n🎈名称: 顺丰授权\n🎉数量:{mation_int}月\n💰支付金额:{zfcoin}积分')
                    exit(0)

    Pointpayment(me_as_int, accountVip, token, phone, account)
    zsm = sg.bucketGet(bucket='Yzyxmm_sf', key='zsm')
    zfzt = False
    if sfVipmoney == Decimal(0):
        return
    money = Decimal(me_as_int) * Decimal(sfVipmoney)
    if not zfzt:
        sender.reply(f'======订单信息=====\n🎈名称:{project}\n🎉数量:{me_as_int}\n💰应付:{money}元')
        sender.replyImage(zsm)
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
        sender.reply('当前有人正在支付,请稍后再试！')
        exit(0)

def cx(url):
    session_id, login_mobile = session_ids(url)
    coin, allcoin = todaycoin(session_id)
    honey, allhoney = todayhoney(session_id)
    capacity, usableHoney = Honey(session_id)
    if capacity == '查询失败':
        exit(0)
    return coin, allcoin, honey, allhoney, capacity, usableHoney

def cxs():
    sender.reply('获取数据...')
    if len(uservalue) != 0:
        accounts = _sg_literal(uservalue)
        for account in accounts:

            userurl = sg.bucketGet(bucket='Yzyxmm_sf_account', key=f'{account}')
            accountVip = sg.bucketGet(bucket='Yzyxmm_sf_Vip', key=f'{account}')
            login_mobile = account[:3] + "****" + account[7:]
            if len(accountVip) != 0 and accountVip > today_time:
                try:
                    coin, allcoin, honey, allhoney, capacity, usableHoney = cx(userurl)
                    sender.reply(
                        f'🤪用户ID:{login_mobile}\n🔥当前蜂蜜:{allhoney}\n🎈今日蜂蜜:{honey}\n🎉蜜罐容量:{capacity}\n💰当前积分:{allcoin}\n📒今日积分:{coin}')
                except SystemExit:
                    sender.reply(f'‍🤪用户ID:{login_mobile}查询异常！')
                    continue
            else:
                sender.reply(f'【{login_mobile}】顺丰云授权过期')

def push(user, account, c):
    login_mobile = account[:3] + "****" + account[7:]
    sg.push('wb', '', user, '',
                    f'🤪用户‘{login_mobile}’，{c}')
    sg.push('tg', '', user, '',
                    f'🤪用户‘{login_mobile}’，{c}')
    sg.push('qq', '', user, '',
                    f'🤪用户‘{login_mobile}’，{c}')
    sg.push('qb', '', user, '',
                    f'🤪用户‘{login_mobile}’，{c}')
    sg.push('wx', '', user, '',
                    f'🤪用户‘{login_mobile}’，{c}')

Yzyxmm_sf_osname, Yzyxmm_sf_qlname, Yzyxmm__managecommand, Yzyxmm_querycommand, Yzyxmm_signcommand, randommanagecommand, randomquerycommand, randomsigncommand, sfVipmoney, sfcoin = getusercontent()
QLurl, qltoken = seekql()
imtype = sender.getImtype()
getusercontent()
today_date = datetime.now().date()
today_time = str(today_date)
usermessage = sender.getMessage()
if '登录' in usermessage or '登陆' in usermessage:
    bindaccount()
elif '管理' in usermessage:
    if len(uservalue) != 0:
        meituanmanage()
    else:
        sender.reply(f'未绑定顺丰账号，请发送‘{randomsigncommand}’进行账号绑定操作！')
elif '查询' in usermessage:
    if len(uservalue) != 0:
        cxs()
    else:
        sender.reply(f'未绑定顺丰账号，请发送‘{randomsigncommand}’进行账号绑定操作！')

elif imtype == 'fake':
    users = sg.bucketAllKeys(bucket='Yzyxmm_sf_bind')
    for user in users:
        accountlist = sg.bucketGet(bucket='Yzyxmm_sf_bind', key=f'{user}')

        accounts = _sg_literal(accountlist)
        for account in accounts:
            accurl = sg.bucketGet(bucket='Yzyxmm_sf_account', key=f'{account}')
            accountVip = sg.bucketGet(bucket='Yzyxmm_sf_Vip', key=account)
            try:
                session_id, login_mobile = session_ids(accurl)
            except SystemExit:
                push(user=user, account=account, c='顺丰账号Cookie失效请及时更新！')
                continue
            capacity, usableHoney = Honey(session_id)
            if capacity == '校验未通过':
                continue
            if int(capacity) <= int(usableHoney):
                push(user=user, account=account, c='顺丰账号蜂罐已满，快去使用蜂蜜！')
            if len(accountVip) != 0 and accountVip > today_time:
                continue
            else:
                qlid = allenvs(osname=Yzyxmm_sf_osname, account=account)
                delenvs(id=qlid)
                push(user=user, account=account, c='顺丰账号云授权已到期，请及时续费！！')
else:
    sender.setContinue()
