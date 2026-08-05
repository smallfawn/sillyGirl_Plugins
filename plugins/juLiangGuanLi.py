# [title: 巨量管理]
# [name: juLiangGuanLi]
# [language: python]
# [class: 任务]
# [author: chuan]
# [version: v2.1.0]
# [public: true]
# [disable: false]
# [admin: true]
# [rule: ^ip$|^剩余ip$|^巨量账号管理$|^巨量$|^生成api$|^巨量余额$|^巨量签到$]
# [icon: https://api.iconify.design/lucide:bot.svg]
# [description: 巨量账号管理、签到和余额查询。]
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
    'otto_jl_imtypes': form.string().title('jl_imtypes').default('').description('巨量签到通知平台，多个用,隔开，例如qq,wb'),
    'otto_jl_token': form.string().title('jl_token').default('').description('请前往http://www.gxfc-s4.com使用token'),
})
_CONFIG_FIELD_MAP = {
    ('otto', 'jl_imtypes'): 'otto_jl_imtypes',
    ('otto', 'jl_token'): 'otto_jl_token',
}

import re
import sys
import json
import requests
import random
import hashlib
from urllib.parse import quote_plus

def current_ip():
    html = requests.get('https://ddns.oray.com/checkip')
    currentIp = re.findall( r'[0-9]+(?:\.[0-9]+){3}',html.text)[0]
    return currentIp

def get_ua():
    first_num = random.randint(55, 62)
    third_num = random.randint(0, 3200)
    fourth_num = random.randint(0, 140)
    os_type = [
        '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)',
        '(Macintosh; Intel Mac OS X 10_12_6)'
    ]
    chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

    ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
                   '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
                  )
    return ua

def login(username,password,ua):
    try:
        url = f'https://www.juliangip.com/login/go?type=password&username={username}&password={password}&sms_code='
        headers = {
            'user-agent': ua,
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }
        res = requests.post(url,headers=headers)
        if res.json()['state'] == 'ok':
            print('登陆成功')
            return res.headers['Set-Cookie']
    except:
        return

def get_info(ck,ua):
    url = 'https://www.juliangip.com/users/'
    headers = {
        'Connection': 'keep-alive',
        'cookie': ck,
        'user-agent': ua,
        'content-type': 'application/json;charset=UTF-8'
    }
    res = requests.get(url,headers=headers)
    return res.text

def goods(ck,ua):
    url = 'https://www.juliangip.com/order/list'
    headers = {
        'Connection': 'keep-alive',
        'cookie': ck,
        'user-agent': ua,
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    res = requests.post(url,headers=headers).json()
    return res

def getkey(ck,order,ua):
    url = f'https://www.juliangip.com/order/info?trade_no={order}'
    headers = {
        'Connection': 'keep-alive',
        'cookie': ck,
        'user-agent': ua,
        'content-type': 'application/json;charset=UTF-8'
    }
    res = requests.get(url,headers=headers).json()
    if res['code'] == 100000:
        return res['data']['key']

def change(ip,order,ck,ua):
    url = f'https://www.juliangip.com/users/product/time/setWhiteIp?trade_no={order}&ips={ip}'
    headers = {
        'Connection': 'keep-alive',
        'cookie': ck,
        'user-agent': ua,
        'content-type': 'application/json;charset=UTF-8'
    }
    res = requests.get(url,headers=headers).json()
    return res

def account(order,key,ck,ua):
    api = f'trade_no={order}&key={key}'
    md5 = hashlib.md5()
    md5.update(api.encode('utf-8'))
    sign = md5.hexdigest()
    url = f'http://v2.api.juliangip.com/dynamic/balance?trade_no={order}&sign={sign}'
    headers = {
        'Connection': 'keep-alive',
        'cookie': ck,
        'user-agent': ua,
        'content-type': 'application/json;charset=UTF-8'
    }
    res = requests.get(url,headers=headers).json()
    return res

def get_api(trade_no,key):
    api = f'auto_white=1&num=1&pt=1&result_type=text&split=2&trade_no={trade_no}&key={key}'
    md5 = hashlib.md5()
    md5.update(api.encode('utf-8'))
    sign = md5.hexdigest()
    url = f'http://v2.api.juliangip.com/dynamic/getips?auto_white=1&num=1&pt=1&result_type=text&split=2&trade_no={trade_no}&sign={sign}'
    return url

def assign(randStr,ticket,ck,ua):
    url = 'https://www.juliangip.com/users/getFree'
    headers = {
        'Connection': 'keep-alive',
        'cookie': ck,
        'user-agent': ua,
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    data = f'randStr={quote_plus(randStr)}&ticket={ticket}'
    print(data)
    res = requests.post(url,headers=headers,data=data).json()
    return res.get('message')

def start_sign(user_info,token,ck,ua,username,trys=0):
    try:
        print('去签到')
        aid = re.findall(r"TencentCaptcha\('(.*?)',function\(res\)", user_info)[0]
        print(f'获取到aid：{aid}')
        randstr,ticket = get_ticket(aid,token)
        if randstr and ticket:
            res = assign(randstr,ticket,ck,ua)
            sg.notifyMasters(f'【账号{username}】{res}',imtypes)
        else:
            res = '滑块失败'
            if trys > 3:
                sg.notifyMasters(f'【账号{username}】重试次数用尽，签到失败',imtypes)
            else:
                trys += 1
                sg.notifyMasters(f'【账号{username}】开始{trys}次重试',imtypes)
                return start_sign(user_info,token,ck,ua,username,trys)
    except:
        if trys > 3:
            sg.notifyMasters(f'【账号{username}】重试次数用尽，签到失败',imtypes)
        else:
            trys += 1
            sg.notifyMasters(f'【账号{username}】开始{trys}次重试',imtypes)
            return start_sign(user_info,token,ck,ua,username,trys)

def query_token(token):
    try:
        url = 'http://119.96.239.11:8888/api/getuserinformation'
        headers = {'Content-Type': 'application/json'}
        body = {'token': token}
        res = requests.post(url,headers=headers,json=body).json()
        token_num = res.get('data').get('余额')
        return f'当前余额：{token_num}积分'
    except:
        return '查询失败'

def get_ticket(appid,token):
    try:
        url = 'http://119.96.239.11:8888/api/getcode'
        headers = {'Content-Type': 'application/json'}
        body = {
            "timeout": "60",
            "type": "tencent-turing",
            "appid": appid,
            "token": token,
            "developeraccount": ""
        }
        res = requests.post(url,headers=headers,json=body,timeout=61).json()
        data = json.loads(res.get('data').get('code','{}'))
        print(data)
        randstr = data.get('randstr')
        ticket = data.get('ticket')
        return randstr,ticket
    except:
        return

def main():
    username_list = sg.bucketAllKeys(bucket)
    if msg == '剩余ip':
        if  username_list:
            pass
        else:
            sender.reply('暂无账号，先发送巨量账号管理添加账号吧')
            return

        sender.reply('开始查询，请稍后...')
        for username in username_list:
            ua = get_ua()
            password = sg.bucketGet(bucket,username)
            ck = login(username,password,ua)
            if ck:
                order = goods(ck,ua)
                if order['state'] == 'ok':
                    order = order['data'][0]['children']
                    if order:
                        order = order[0]['value']
                        key = getkey(ck,order,ua)
                        res = account(order,key,ck,ua)
                        if res['code'] == 200:
                            balance = res['data']['balance']
                            sender.reply(f'【账号{username}】剩余{balance}ip可用')
                        else:
                            sender.reply(f'【账号{username}】{res["msg"]}')
                    else:
                        sender.reply('没有可用免费套餐!')
                else:
                    sender.reply('获取套餐失败')
            else:
                sender.reply(f'账号{username}  登陆失败')
    elif msg == '巨量账号管理':
        send_msg = '请在60s内回复(q:退出，-:删除，0:添加):\n'

        if  username_list:
            index = 0
            for username in username_list:
                index += 1
                password = sg.bucketGet(bucket,username)
                send_msg += f'{index}. {username}\n'

        sender.reply(send_msg)
        user_msg = sender.listen(60*1000)
        if 'q' == user_msg:
            sender.reply('退出')
            return
        elif '0' == user_msg:
            sender.reply(f'请60s内输入账号(q退出):')
            username = sender.listen(60*1000)
            if username == 'error' or username == 'q':
                sender.reply('退出')
                return

            sender.reply(f'请60s内输入密码(q退出):')
            password = sender.listen(60*1000)
            if password == 'error' or password == 'q':
                sender.reply('退出')
                return
            ck = login(username,password,get_ua())
            if ck:
                sg.bucketSet(bucket,username,password)
                sender.reply('账号有效，添加成功')
            else:
                sender.reply('账号无效或输入错误，退出')
                return
        elif user_msg in [f'-{i+1}' for i in range(len(username_list))]:
            num = user_msg.split('-')[1]
            del_data = username_list[int(num)-1]
            sg.bucketDel(bucket,del_data)
            sender.reply(f'{del_data}删除成功')
        else:
            sender.reply('输入错误，退出')

    elif msg == '巨量加白':
        if  username_list:
            pass
        else:
            sender.reply('暂无账号，先发送巨量账号管理添加账号吧')
            return

        sender.reply('开始执行，请稍后...')
        now_ip = current_ip()
        sender.reply(f'当前ip：{now_ip}')
        for username in username_list:
            ua = get_ua()
            password = sg.bucketGet(bucket,username)
            ck = login(username,password,ua)
            if ck:
                order = goods(ck,ua)
                if order['state'] == 'ok':
                    order = order['data'][0]['children']
                    if order:
                        order = order[0]['value']
                        res = change(now_ip,order,ck,ua)
                        if res['state'] == 'ok':
                            sender.reply(f'【账号{username}】加白成功')
                        else:
                            sender.reply(f'【账号{username}】{res["message"]}')
                    else:
                        sender.reply(f'【账号{username}】没有可用免费套餐!')
                else:
                    sender.reply(f'【账号{username}】获取套餐失败')
            else:
                sender.reply(f'【账号{username}】登陆失败')
    elif msg == 'ip':
        now_ip = current_ip()
        sender.reply(f'当前ip：{now_ip}')

    elif msg == '生成api':
        if  username_list:
            pass
        else:
            sender.reply('暂无账号，先发送巨量账号管理添加账号吧')
            return

        sender.reply('开始生成，请稍后...')
        for username in username_list:
            ua = get_ua()
            password = sg.bucketGet(bucket,username)
            ck = login(username,password,ua)
            if ck:
                order = goods(ck,ua)
                if order['state'] == 'ok':
                    order = order['data'][0]['children']
                    if order:
                        order = order[0]['value']
                        key = getkey(ck,order,ua)
                        api = get_api(order,key)
                        sender.reply(f'【账号{username}】\n提取api：{api}')
                    else:
                        sender.reply(f'【账号{username}】没有可用免费套餐!')
                else:
                    sender.reply(f'【账号{username}】获取套餐失败')
            else:
                sender.reply(f'【账号{username}】登陆失败')
    elif msg == '巨量余额':
        token = sg.get('jl_token')
        if not token:
            sender.reply(f'未设置token，请前往http://www.gxfc-s4.com/r使用\n发送set otto jl_token xxxxxx')
            sys.exit()
        res = query_token(token)
        sender.reply(res)
    elif msg == '巨量签到':
        token = sg.get('jl_token')
        if not token:
            sg.notifyMasters(f'请前往http://www.gxfc-s4.com使用token\n发送set otto jl_token xxxxxx',imtypes)
            sys.exit()

        if  username_list:
            pass
        else:
            sg.notifyMasters('暂无账号，先发送巨量账号管理添加账号吧',imtypes)
            return

        sg.notifyMasters('开始签到，请稍后...',imtypes)
        for username in username_list:
            ua = get_ua()
            password = sg.bucketGet(bucket,username)
            ck = login(username,password,ua)
            if ck:
                user_info = get_info(ck,ua)
                if '点击领取今日免费IP' in user_info:
                    start_sign(user_info,token,ck,ua,username)
                elif '您已成功领取' in user_info:
                    sg.notifyMasters(f'【账号{username}】今日已签到',imtypes)
            else:
                sg.notifyMasters(f'【账号{username}】登陆失败，建议换ip重试',imtypes)

if __name__ == "__main__":
    senderID = sg.getSenderID()
    sender = sg.Sender(senderID)
    msg = sender.getMessage()
    bucket = 'jl_data'
    imtypes = sg.get('jl_imtypes')
    if not imtypes:
        sender.reply(f'未设置管理员通知，请前往配参填写')
        sys.exit()
    imtypes = imtypes.split(',')
    main()
