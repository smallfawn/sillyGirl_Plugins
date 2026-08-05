# [title: 白鲸鱼]
# [name: baiJingYu]
# [language: python]
# [class: 任务]
# [author: yueiqiu4523]
# [version: v1.5.1]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^^白鲸鱼登录$|^白鲸鱼登陆$|^登陆白鲸鱼$|^登录白鲸鱼$|^白鲸鱼查询$|^查询白鲸鱼$|^白鲸鱼管理$|^管理白鲸鱼$|^白鲸鱼清理$|^白鲸鱼$|^白鲸鱼教程$]
# [cron: 0 8 * * *]
# [icon: https://www.yili.com/static/images/logo.png]
# [description: 白鲸鱼旧衣服回收插件；1.使用手机号+密码登录；1.2版本.就行了美化处理；1.5.1版本支持青龙/呆呆面板填在同一格子里面]
# [depe: ["requests","urllib3"]]


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
    'JQB_bjy_panel_config': form.string().title('面板配置').default('').description('支持青龙/呆呆面板格式：Host丨AppKey丨AppSecret 使用中文竖线丨分隔'),
    'JQB_bjy_ql_host': form.string().title('【兼容旧版】青龙地址').default('').description('若未配置上方面板配置，则使用此项（仅限青龙）'),
    'JQB_bjy_ql_client_id': form.string().title('【兼容旧版】青龙应用ID').default(''),
    'JQB_bjy_ql_client_secret': form.string().title('【兼容旧版】青龙应用秘钥').default(''),
    'JQB_bjy_var_name': form.string().title('环境变量名').default('').description('面板内的环境变量名，如 bjy'),
    'JQB_bjy_proxy_pool': form.string().title('代理池地址').default(''),
})
_CONFIG_FIELD_MAP = {
    ('JQB', 'bjy.panel_config'): 'JQB_bjy_panel_config',
    ('JQB', 'bjy.ql_host'): 'JQB_bjy_ql_host',
    ('JQB', 'bjy.ql_client_id'): 'JQB_bjy_ql_client_id',
    ('JQB', 'bjy.ql_client_secret'): 'JQB_bjy_ql_client_secret',
    ('JQB', 'bjy.var_name'): 'JQB_bjy_var_name',
    ('JQB', 'bjy.proxy_pool'): 'JQB_bjy_proxy_pool',
}

import re
from datetime import datetime, timedelta
import urllib3
from decimal import Decimal
import requests
import time
import json
import asyncio
import traceback

urllib3.disable_warnings()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

MAX_RETRIES = 3
IS_PROXY = False
PROXY_API = sg.bucketGet('JQB.bjy', 'proxy_pool') or "http://代理池API"
proxy = None

def mask_phone(phone):
    if len(phone) != 11:
        return phone
    return phone[:3] + '****' + phone[7:]

def update_proxy():
    global proxy
    try:
        if not IS_PROXY:
            proxy = None
            return
        response = requests.get(PROXY_API, timeout=10)
        ip = response.text.strip()
        proxy = {'http': ip, 'https': ip}
    except Exception as e:
        print(f"代理获取失败: {str(e)}")
        proxy = None

def _send_request(method, url, **kwargs):
    global proxy
    attempts = 0
    while attempts < MAX_RETRIES:
        try:
            if IS_PROXY and not proxy:
                update_proxy()
            kwargs['timeout'] = kwargs.get('timeout', 15)
            kwargs['verify'] = False
            response = requests.request(
                method=method,
                url=url,
                proxies=proxy if IS_PROXY and proxy else None,
                **kwargs
            )
            response.raise_for_status()
            return response
        except (requests.exceptions.ProxyError, requests.exceptions.Timeout) as e:
            print(f"代理异常: {str(e)}")
            if IS_PROXY:
                update_proxy()
                attempts += 1
                time.sleep(2)
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {str(e)}")
            attempts += 1
            if attempts == MAX_RETRIES:
                raise

def extract_cash_value(cash_str):
    if isinstance(cash_str, (int, float)):
        return float(cash_str)
    match = re.search(r'(\d+\.\d+)|(\d+)', str(cash_str))
    if match:
        return float(match.group(0))
    return 0.0

def login(account_name, password):
    try:
        if not account_name or not password:
            return "账号或密码不能为空", None

        url = "https://www.52bjy.com/api/app/member.php"
        payload = {
            'action': "login",
            'username': account_name,
            'password': password,
            'app': "self",
            'sign': ""
        }
        headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 11; SHARK KLE-A0 Build/KLEN2202130CN00MR4; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/29.09091)",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'EnvConnection': "test",
        }

        response = _send_request('POST', url, data=payload, headers=headers)
        result = response.json()

        if result.get("message") != "登录成功":
            return f"登录失败: {result.get('message', '未知错误')}", None

        return f"{mask_phone(account_name)}", password

    except Exception as e:
        return f"登录异常: {str(e)}", None

def bind(sender):
    senderID = sg.getSenderID()
    sender = sg.Sender(senderID)
    userid = sender.getUserID()
    uservalue = sg.bucketGet(bucket='JQB.bjy.user', key=userid)

    sender.reply(
        """=====白鲸鱼登录=====
📝 请输入登录参数:手机号#密码
说明: 支持批量，一个账号一行
示例：
    13888888888#password123
    13999999999#password456
=====================
⭐ 输入q退出操作"""
    )

    input_text = sender.input(120000, 10, True).strip()
    if not input_text or input_text.lower() == 'q':
        sender.reply('已取消操作')
        return

    accounts = []
    success_count = 0
    fail_count = 0

    lines = input_text.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue

        if '#' not in line:
            sender.reply(f"❌ 格式错误: {line} (缺少#分隔符)")
            fail_count += 1
            continue

        parts = line.split('#', 1)
        if len(parts) < 2:
            sender.reply(f"❌ 格式错误: {line} (缺少密码)")
            fail_count += 1
            continue

        phone = parts[0].strip()
        password = parts[1].strip()

        if not re.match(r'^1[3-9]\d{9}$', phone):
            sender.reply(f"❌ 手机号格式错误: {phone}")
            fail_count += 1
            continue

        username, valid_password = login(phone, password)
        if not valid_password:
            sender.reply(f'{username}')
            fail_count += 1
            continue

        try:
            account_data = {
                'password': valid_password,
                'account_name': phone
            }
            sg.bucketSet('JQB.bjy.account', phone, json.dumps(account_data))

            if phone not in accounts:
                accounts.append(phone)
                success_count += 1
        except Exception as e:
            sender.reply(f"❌ 保存失败: {phone} - {str(e)}")
            fail_count += 1

    if accounts:
        existing_accounts = _sg_literal(uservalue or '[]')
        for account in accounts:
            if account not in existing_accounts:
                existing_accounts.append(account)
        sg.bucketSet('JQB.bjy.user', userid, str(existing_accounts))

    result_msg = f"""=====绑定结果=====
✅ 成功绑定: {success_count}个账号
❌ 失败绑定: {fail_count}个账号
------------------
发送"白鲸鱼查询"查看状态
发送"白鲸鱼管理"管理账号
====================="""
    sender.reply(result_msg)

def query_balance(account_name):
    try:
        account_data = sg.bucketGet('JQB.bjy.account', account_name)
        if not account_data:
            return "账号信息不存在", 0, 0

        account_info = json.loads(account_data)
        password = account_info.get('password')

        if not password:
            return "账号信息不完整", 0, 0

        url = "https://www.52bjy.com/api/app/member.php"
        payload = {
            'action': "login",
            'username': account_name,
            'password': password,
            'app': "self",
            'sign': ""
        }
        headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 11; SHARK KLE-A0 Build/KLEN2202130CN00MR4; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/29.09091)",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'EnvConnection': "test",
        }

        response = _send_request('POST', url, data=payload, headers=headers)
        result = response.json()

        if result.get("message") != "登录成功":
            return f"登录失败: {result.get('message', '未知错误')}", 0, 0

        token = result["data"]["token"]

        url = "https://www.52bjy.com/api/app/user.php"
        params = {
            'action': 'userinfo',
            'app': 'self',
            'appkey': 'a9827e37ed2becd8',
            'auth': token,
            'is_pop': '0',
            'username': account_name,
            'version': '2'
        }

        response = _send_request('GET', url, params=params, headers=headers)
        result = response.json()

        if result.get('code') == 0:
            credit_to_cash = result.get('data', {}).get('credit_to_cash', '0元')
            cash_value = extract_cash_value(credit_to_cash)
            return cash_value, cash_value, 1
        elif 'data' in result and 'credit_to_cash' in result['data']:
            credit_to_cash = result['data']['credit_to_cash']
            cash_value = extract_cash_value(credit_to_cash)
            return cash_value, cash_value, 1
        else:
            error_msg = result.get('message', '未知错误')
            return f"查询失败: {error_msg}", 0, 0

    except Exception as e:
        return f"查询异常: {str(e)}", 0, 0

def get_panel_config():
    """
    获取面板配置，返回 (host, app_key, app_secret)
    优先使用新的 panel_config 参数，兼容旧的青龙三个独立参数
    """
    config_str = sg.bucketGet('JQB.bjy', 'panel_config')
    if config_str and '丨' in config_str:
        parts = config_str.split('丨', 2)
        if len(parts) == 3:
            host = parts[0].strip()
            app_key = parts[1].strip()
            app_secret = parts[2].strip()
            if host and app_key and app_secret:
                return host, app_key, app_secret
    host = sg.bucketGet('JQB.bjy', 'ql_host')
    client_id = sg.bucketGet('JQB.bjy', 'ql_client_id')
    client_secret = sg.bucketGet('JQB.bjy', 'ql_client_secret')
    if host and client_id and client_secret:
        print("警告: 使用旧的青龙配置，建议迁移到新的 panel_config 格式(Host丨AppKey丨AppSecret)")
        return host, client_id, client_secret
    return None, None, None

def get_qinglong_token(host, app_key, app_secret):
    """获取青龙面板token"""
    try:
        if not host.endswith('/'):
            host += '/'
        url = f"{host}open/auth/token?client_id={app_key}&client_secret={app_secret}"
        response = requests.get(url, timeout=10, verify=False)
        if response.status_code == 200:
            data = response.json()
            return data.get('data', {}).get('token')
    except Exception as e:
        print(f"获取青龙token失败: {str(e)}")
    return None

def add_to_qinglong(host, token, env_data):
    """添加或更新青龙环境变量，返回环境变量ID"""
    try:
        if not host.endswith('/'):
            host += '/'
        url = f"{host}open/envs"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code != 200:
            return None
        envs = response.json().get('data', [])
        exists_id = None
        match = re.search(r'账号([^丨]+)丨用户:([^丨]+)', env_data['remarks'])
        account_phone_mask = match.group(1) if match else None
        user_id = match.group(2) if match else None

        for env in envs:
            if env.get('name') != env_data['name']:
                continue
            env_remarks = env.get('remarks', '')
            if account_phone_mask and user_id:
                if account_phone_mask in env_remarks and user_id in env_remarks:
                    exists_id = env.get('id')
                    break
            else:
                if env_data.get('remarks') in env_remarks:
                    exists_id = env.get('id')
                    break

        if exists_id:
            update_url = f"{host}open/envs"
            env_data['id'] = exists_id
            response = requests.put(update_url, headers=headers, json=env_data, verify=False)
            if response.status_code == 200:
                return exists_id
        else:
            response = requests.post(url, headers=headers, json=[env_data], verify=False)
            if response.status_code == 200:
                resp_data = response.json()
                if resp_data.get('data') and len(resp_data['data']) > 0:
                    return resp_data['data'][0]['id']
    except Exception as e:
        print(f"青龙添加环境变量失败: {str(e)}")
    return None

def delete_qinglong_env(host, token, env_id):
    """删除青龙环境变量"""
    try:
        if not host.endswith('/'):
            host += '/'
        url = f"{host}open/envs"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        data = [int(env_id)]
        response = requests.delete(url, headers=headers, json=data, verify=False)
        return response.status_code == 200
    except Exception as e:
        print(f"删除青龙环境变量失败: {str(e)}")
        return False

def get_daidai_token(host, app_key, app_secret):
    """获取呆呆面板token"""
    try:
        if not host.endswith('/'):
            host += '/'
        url = f"{host}api/open-api/token"
        headers = {"Content-Type": "application/json"}
        payload = {"app_key": app_key, "app_secret": app_secret}
        response = requests.post(url, json=payload, timeout=10, verify=False)
        if response.status_code == 200:
            data = response.json()
            return data.get("data", {}).get("access_token")
    except Exception as e:
        print(f"获取呆呆token失败: {str(e)}")
    return None

def _daidai_request(method, host, token, url_suffix, **kwargs):
    """呆呆面板请求封装，自动处理401刷新token"""
    if not host.endswith('/'):
        host += '/'
    full_url = host + url_suffix.lstrip('/')
    headers = kwargs.pop('headers', {})
    headers['Authorization'] = f"Bearer {token}"
    headers['Content-Type'] = 'application/json'
    resp = requests.request(method, full_url, headers=headers, timeout=10, verify=False, **kwargs)
    if resp.status_code == 401:
        new_token = get_daidai_token(host, *get_panel_config()[1:])  # 重新获取token
        if new_token:
            headers['Authorization'] = f"Bearer {new_token}"
            resp = requests.request(method, full_url, headers=headers, timeout=10, verify=False, **kwargs)
    return resp

def add_to_daidai(host, token, env_data):
    """添加或更新呆呆环境变量，返回环境变量ID"""
    try:
        search_url = f"api/envs?keyword={env_data['name']}&page_size=100"
        search_resp = _daidai_request('GET', host, token, search_url)
        if search_resp.status_code != 200:
            return None
        search_result = search_resp.json()
        envs = search_result if isinstance(search_result, list) else search_result.get('data', [])

        match = re.search(r'账号([^丨]+)丨用户:([^丨]+)', env_data['remarks'])
        account_phone_mask = match.group(1) if match else None
        user_id = match.group(2) if match else None

        exists_id = None
        for env in envs:
            if env.get('name') != env_data['name']:
                continue
            env_remarks = env.get('remarks', '')
            if account_phone_mask and user_id:
                if account_phone_mask in env_remarks and user_id in env_remarks:
                    exists_id = env.get('id')
                    break
            else:
                if env_data.get('remarks') in env_remarks:
                    exists_id = env.get('id')
                    break

        data = env_data.copy()
        data['enabled'] = True

        if exists_id:
            update_url = f"api/envs/{exists_id}"
            update_resp = _daidai_request('PUT', host, token, update_url, json=data)
            if update_resp.status_code == 200:
                return exists_id
        else:
            add_url = "api/envs"
            add_resp = _daidai_request('POST', host, token, add_url, json=data)
            if add_resp.status_code == 200:
                resp_data = add_resp.json()
                return resp_data.get('data', {}).get('id')
    except Exception as e:
        print(f"呆呆添加环境变量失败: {str(e)}")
    return None

def delete_daidai_env(host, token, env_id):
    """删除呆呆环境变量"""
    try:
        del_url = f"api/envs/{env_id}"
        del_resp = _daidai_request('DELETE', host, token, del_url)
        return del_resp.status_code == 200
    except Exception as e:
        print(f"删除呆呆环境变量失败: {str(e)}")
        return False

def add_to_panel(env_data):
    """
    统一添加/更新环境变量，自动识别青龙或呆呆
    返回带前缀的环境变量ID，格式 "ql:123" 或 "dd:456"
    """
    host, app_key, app_secret = get_panel_config()
    if not host:
        return None
    ql_token = get_qinglong_token(host, app_key, app_secret)
    if ql_token:
        env_id = add_to_qinglong(host, ql_token, env_data)
        if env_id:
            return f"ql:{env_id}"
    dd_token = get_daidai_token(host, app_key, app_secret)
    if dd_token:
        env_id = add_to_daidai(host, dd_token, env_data)
        if env_id:
            return f"dd:{env_id}"
    return None

def delete_from_panel(env_id_with_prefix):
    """
    统一删除环境变量，根据前缀调用对应面板的删除函数
    """
    if not env_id_with_prefix:
        return False
    parts = env_id_with_prefix.split(':', 1)
    if len(parts) != 2:
        return False
    panel_type, env_id = parts
    host, app_key, app_secret = get_panel_config()
    if not host:
        return False
    if panel_type == 'ql':
        token = get_qinglong_token(host, app_key, app_secret)
        if token:
            return delete_qinglong_env(host, token, env_id)
    elif panel_type == 'dd':
        token = get_daidai_token(host, app_key, app_secret)
        if token:
            return delete_daidai_env(host, token, env_id)
    return False

def query(sender):
    senderID = sg.getSenderID()
    sender = sg.Sender(senderID)
    userid = sender.getUserID()
    uservalue = sg.bucketGet(bucket='JQB.bjy.user', key=userid)
    today_date = datetime.now().date()
    today_time = str(today_date)

    accounts = _sg_literal(uservalue or '[]')
    if not accounts:
        sender.reply(
            """\n=====白鲸鱼账号查询=====
❌ 未找到任何账号
------------------
💡 发送"白鲸鱼登录"绑定账号
==================="""
        )
        return

    if len(accounts) > 1:
        menu = """=====请选择查询账号=====
[0] 查询全部账号
"""
        for idx, acc in enumerate(accounts, 1):
            menu += f"[{idx}] {mask_phone(acc)}\n"
        menu += "=======================\n⚠️ 请回复数字序号(输入q退出)"
        sender.reply(menu)

        choice = sender.input(30000, 1, False)
        if not choice or choice.lower() == 'q':
            sender.reply('已取消查询')
            return

        if choice == '0':
            target_accounts = accounts
        else:
            try:
                index = int(choice) - 1
                if 0 <= index < len(accounts):
                    target_accounts = [accounts[index]]
                else:
                    sender.reply('选择超出范围，已取消查询')
                    return
            except:
                sender.reply('格式错误，已取消查询')
                return
    else:
        target_accounts = accounts

    for account in target_accounts:
        try:
            account_auth = '2099-12-31'
            auth_status = f"⏰ 授权到期: {account_auth}" if account_auth and account_auth >= today_time else "❌ 未授权"

            total_balance, withdraw_balance, status = query_balance(account)
            if status == 0:
                sender.reply(f'【{mask_phone(account)}】{total_balance}')
                continue

            sender.reply(
                f"""=====账号详情=====
📱 账号: {mask_phone(account)}
{auth_status}
💮 可回收金额: {total_balance}灵石💮
==================="""
            )
        except Exception as e:
            sender.reply(f'【{mask_phone(account)}】查询出错: {str(e)}')

def sign_in(sender):
    senderID = sg.getSenderID()
    sender = sg.Sender(senderID)
    userid = sender.getUserID()
    uservalue = sg.bucketGet(bucket='JQB.bjy.user', key=userid)
    today_date = datetime.now().date()
    today_time = str(today_date)

    accounts = _sg_literal(uservalue or '[]')
    if not accounts:
        sender.reply('❌ 未绑定任何账号')
        return

    for account in accounts:
        try:
            auth = '2099-12-31'
            if not auth or auth < today_time:
                sender.reply(f'【{mask_phone(account)}】未授权，无法签到')
                continue

            account_data = sg.bucketGet('JQB.bjy.account', account)
            if not account_data:
                sender.reply(f'【{mask_phone(account)}】账号信息不存在')
                continue

            account_info = json.loads(account_data)
            password = account_info.get('password')

            if not password:
                sender.reply(f'【{mask_phone(account)}】账号信息不完整')
                continue

            login_url = "https://www.52bjy.com/api/app/member.php"
            payload = {
                'action': "login",
                'username': account,
                'password': password,
                'app': "self",
                'sign': ""
            }
            headers = {
                'User-Agent': "Mozilla/5.0 (Linux; Android 11; SHARK KLE-A0 Build/KLEN2202130CN00MR4; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/29.09091)",
                'Connection': "Keep-Alive",
                'Accept-Encoding': "gzip",
                'EnvConnection': "test",
            }

            login_response = _send_request('POST', login_url, data=payload, headers=headers)
            login_result = login_response.json()

            if login_result.get("message") != "登录成功":
                sender.reply(f"【{mask_phone(account)}】登录失败: {login_result.get('message', '未知错误')}")
                continue

            token = login_result["data"]["token"]

            sign_url = f"https://www.52bjy.com/api/app/user.php?action=qiandao&app=self&auth={token}&username={account}"

            sign_response = _send_request('GET', sign_url, headers=headers)
            sign_result = sign_response.json()

            if sign_result.get('message') == "签到成功":
                query_url = "https://www.52bjy.com/api/app/user.php"
                params = {
                    'action': 'userinfo',
                    'app': 'self',
                    'appkey': 'a9827e37ed2becd8',
                    'auth': token,
                    'is_pop': '0',
                    'username': account,
                    'version': '2'
                }

                query_response = _send_request('GET', query_url, params=params, headers=headers)
                query_result = query_response.json()

                if query_result.get('code') == 0:
                    credit_to_cash = query_result.get('data', {}).get('credit_to_cash', '0元')
                    cash_value = extract_cash_value(credit_to_cash)
                    sender.reply(f"【{mask_phone(account)}】签到成功，当前可回收金额: {cash_value}元")
                elif 'data' in query_result and 'credit_to_cash' in query_result['data']:
                    credit_to_cash = query_result['data']['credit_to_cash']
                    cash_value = extract_cash_value(credit_to_cash)
                    sender.reply(f"【{mask_phone(account)}】签到成功，当前可回收金额: {cash_value}元")
                else:
                    error_msg = query_result.get('message', '未知错误')
                    sender.reply(f"【{mask_phone(account)}】签到成功，但查询金额失败: {error_msg}")
            else:
                error_msg = sign_result.get('message', '未知错误')
                sender.reply(f"【{mask_phone(account)}】签到失败: {error_msg}")

        except Exception as e:
            sender.reply(f'【{mask_phone(account)}】签到失败: {str(e)}')

def manage_accounts(sender):
    senderID = sg.getSenderID()
    sender = sg.Sender(senderID)
    userid = sender.getUserID()
    uservalue = sg.bucketGet(bucket='JQB.bjy.user', key=userid)

    accounts = _sg_literal(uservalue or '[]')
    if not accounts:
        sender.reply("""=====账号管理=====
❌ 未找到任何账号
------------------
💡 发送"白鲸鱼登录"绑定账号
====================""")
        return

    menu = """=====账号管理=====
[1] 授权所有账号
[2] 删除账号
[3] 选择账号授权
------------------
请回复数字选择操作"""
    sender.reply(menu)

    choice = sender.input(30000, 1, False)
    if not choice:
        return sender.reply('操作超时')

    if choice == '1':
        authorize_accounts(sender, accounts)
    elif choice == '2':
        delete_account(sender)
    elif choice == '3':
        select_accounts_authorize(sender, accounts)
    else:
        sender.reply('无效的选择')

def delete_account(sender):
    senderID = sg.getSenderID()
    sender = sg.Sender(senderID)
    userid = sender.getUserID()
    uservalue = sg.bucketGet(bucket='JQB.bjy.user', key=userid)

    accounts = _sg_literal(uservalue or '[]')
    if not accounts:
        return sender.reply('❌ 无账号可删除')

    if len(accounts) > 1:
        menu = "=====选择要删除的账号=====\n"
        for idx, acc in enumerate(accounts, 1):
            menu += f"[{idx}] {mask_phone(acc)}\n"
        menu += "=======================\n⚠️ 回复数字序号(输入q退出)"
        sender.reply(menu)

        choice = sender.input(30000, 1, False)
        if not choice or choice.lower() == 'q':
            return sender.reply('已取消')

        try:
            index = int(choice) - 1
            if 0 <= index < len(accounts):
                account = accounts[index]

                confirm_msg = f"""=====⚠️警告⚠️=====
即将删除账号:
📱 账号: {mask_phone(account)}
------------------
此操作不可恢复！
确认请回复【y】
取消请回复【n】
=================="""
                sender.reply(confirm_msg)

                confirm = sender.input(30000, 1, False)
                if confirm.lower() != 'y':
                    return sender.reply('✅ 已取消删除操作')

                env_id_with_prefix = sg.bucketGet('JQB.bjy.env_id', account)
                if env_id_with_prefix:
                    delete_from_panel(env_id_with_prefix)

                sg.bucketDel('JQB.bjy.account', account)
                True
                sg.bucketDel('JQB.bjy.env_id', account)

                accounts.pop(index)
                sg.bucketSet('JQB.bjy.user', userid, str(accounts))
                sender.reply(f'✅ 已删除账号: {mask_phone(account)}')
            else:
                sender.reply('选择超出范围')
        except:
            sender.reply('输入错误')
    else:
        account = accounts[0]

        confirm_msg = f"""=====⚠️警告⚠️=====
即将删除账号:
📱 账号: {mask_phone(account)}
------------------
此操作不可恢复！
确认请回复【y】
取消请回复【n】
=================="""
        sender.reply(confirm_msg)

        confirm = sender.input(30000, 1, False)
        if confirm.lower() != 'y':
            return sender.reply('✅ 已取消删除操作')

        env_id_with_prefix = sg.bucketGet('JQB.bjy.env_id', account)
        if env_id_with_prefix:
            delete_from_panel(env_id_with_prefix)

        sg.bucketDel('JQB.bjy.account', account)
        True
        sg.bucketDel('JQB.bjy.env_id', account)
        sg.bucketSet('JQB.bjy.user', userid, '[]')
        sender.reply(f'✅ 已删除账号: {mask_phone(account)}')

def authorize_accounts(sender, accounts):
    if not accounts:
        return sender.reply('❌ 无账号可授权')

    account_list = "\n".join([f"  - {mask_phone(acc)}" for acc in accounts])
    sender.reply(f"""=====即将授权以下账号=====
{account_list}
------------------""")

    coin_bucket = sg.bucketGet('JQB.bjy', 'coin_bucket') or 'dd_sign_points'
    coin_price = int(sg.bucketGet('JQB.bjy', 'coin') or '0')
    price = Decimal(sg.bucketGet('JQB.bjy', 'price') or '1')

    menu = f"""=====授权方式选择=====
[1] 微信支付 ({price}元/账号/月)
[2] 积分支付 ({coin_price}积分/账号/月)
------------------
请回复数字选择方式"""
    sender.reply(menu)

    choice = sender.input(30000, 1, False)
    if not choice or choice not in ['1', '2']:
        return sender.reply('已取消')

    sender.reply("请输入授权月数:")
    months = sender.input(30000, 1, False)
    if not months:
        return sender.reply('输入超时')

    try:
        months = int(months)
        if months <= 0:
            return sender.reply('月数必须大于0')

        var_name = sg.bucketGet('JQB.bjy', 'var_name') or 'bjy'

        if choice == '1':
            amount = price * months * len(accounts)
            if process_payment(amount, months * 30, sender):
                today_date = datetime.now().date()
                today_time = str(today_date)
                for account in accounts:
                    auth = '2099-12-31'
                    if not auth or auth < today_time:
                        auth_time = (datetime.now() + timedelta(days=months*30)).strftime('%Y-%m-%d')
                    else:
                        auth_time = (datetime.strptime(auth, "%Y-%m-%d") + timedelta(days=months*30)).strftime('%Y-%m-%d')

                    True

                    account_data = sg.bucketGet('JQB.bjy.account', account)
                    if account_data:
                        account_info = json.loads(account_data)
                        password = account_info.get('password')

                        if password:
                            remarks = f"白鲸鱼账号{mask_phone(account)}丨用户:{sender.getUserID()}丨授权时间:{auth_time}"
                            env_data = {
                                "name": var_name,
                                "value": f"{account}#{password}",
                                "remarks": remarks
                            }
                            env_id_with_prefix = add_to_panel(env_data)
                            if env_id_with_prefix:
                                sg.bucketSet('JQB.bjy.env_id', account, env_id_with_prefix)

                sender.reply(f'✅ 已授权 {len(accounts)} 个账号 {months} 个月')
        elif choice == '2':
            user_coin = Decimal(sg.bucketGet(coin_bucket, sender.getUserID()) or '0')
            need_coin = coin_price * months * len(accounts)
            if user_coin < need_coin:
                return sender.reply(f'❌ 积分不足，需要{need_coin}，当前有{user_coin}')

            new_coin = user_coin - need_coin
            sg.bucketSet(coin_bucket, sender.getUserID(), str(new_coin))
            today_date = datetime.now().date()
            today_time = str(today_date)
            for account in accounts:
                auth = '2099-12-31'
                if not auth or auth < today_time:
                    auth_time = (datetime.now() + timedelta(days=months*30)).strftime('%Y-%m-%d')
                else:
                    auth_time = (datetime.strptime(auth, "%Y-%m-%d") + timedelta(days=months*30)).strftime('%Y-%m-%d')

                True

                account_data = sg.bucketGet('JQB.bjy.account', account)
                if account_data:
                    account_info = json.loads(account_data)
                    password = account_info.get('password')

                    if password:
                        remarks = f"白鲸鱼账号{mask_phone(account)}丨用户:{sender.getUserID()}丨授权时间:{auth_time}"
                        env_data = {
                            "name": var_name,
                            "value": f"{account}#{password}",
                            "remarks": remarks
                        }
                        env_id_with_prefix = add_to_panel(env_data)
                        if env_id_with_prefix:
                            sg.bucketSet('JQB.bjy.env_id', account, env_id_with_prefix)

            sender.reply(
                f"""✅ 已用 {need_coin} 积分授权 {len(accounts)} 个账号 {months} 个月
剩余积分: {new_coin}"""
            )

    except Exception as e:
        sender.reply(f'❌ 授权失败: {str(e)}')

def select_accounts_authorize(sender, accounts):
    if not accounts:
        return sender.reply('❌ 无账号可授权')

    menu = "=====选择要授权的账号=====\n"
    for idx, acc in enumerate(accounts, 1):
        menu += f"[{idx}] {mask_phone(acc)}\n"
    menu += "=======================\n⚠️ 回复数字序号(多个用逗号分隔, 输入q退出)"
    sender.reply(menu)

    choice_str = sender.input(30000, 1, False)
    if not choice_str or choice_str.lower() == 'q':
        return sender.reply('已取消授权操作')

    try:
        selected_indexes = [int(idx.strip()) for idx in choice_str.split(',')]
        selected_accounts = []

        for idx in selected_indexes:
            if 1 <= idx <= len(accounts):
                selected_accounts.append(accounts[idx-1])
            else:
                sender.reply(f"❌ 无效的序号: {idx}，已跳过")

        if not selected_accounts:
            return sender.reply('❌ 未选择有效账号')

        account_list = "\n".join([f"  - {mask_phone(acc)}" for acc in selected_accounts])
        sender.reply(f"""=====已选择以下账号=====
{account_list}
------------------""")

        authorize_selected_accounts(sender, selected_accounts)

    except Exception as e:
        sender.reply(f'❌ 选择失败: {str(e)}')

def authorize_selected_accounts(sender, selected_accounts):
    coin_bucket = sg.bucketGet('JQB.bjy', 'coin_bucket') or 'dd_sign_points'
    coin_price = int(sg.bucketGet('JQB.bjy', 'coin') or '0')
    price = Decimal(sg.bucketGet('JQB.bjy', 'price') or '1')

    menu = f"""=====授权方式选择=====
[1] 微信支付 ({price}元/账号/月)
[2] 积分支付 ({coin_price}积分/账号/月)
------------------
请回复数字选择方式"""
    sender.reply(menu)

    choice = sender.input(30000, 1, False)
    if not choice or choice not in ['1', '2']:
        return sender.reply('已取消')

    sender.reply("请输入授权月数:")
    months = sender.input(30000, 1, False)
    if not months:
        return sender.reply('输入超时')

    try:
        months = int(months)
        if months <= 0:
            return sender.reply('月数必须大于0')

        var_name = sg.bucketGet('JQB.bjy', 'var_name') or 'bjy'

        if choice == '1':
            amount = price * months * len(selected_accounts)
            if process_payment(amount, months * 30, sender):
                today_date = datetime.now().date()
                today_time = str(today_date)
                for account in selected_accounts:
                    auth = '2099-12-31'
                    if not auth or auth < today_time:
                        auth_time = (datetime.now() + timedelta(days=months*30)).strftime('%Y-%m-%d')
                    else:
                        auth_time = (datetime.strptime(auth, "%Y-%m-%d") + timedelta(days=months*30)).strftime('%Y-%m-%d')

                    True

                    account_data = sg.bucketGet('JQB.bjy.account', account)
                    if account_data:
                        account_info = json.loads(account_data)
                        password = account_info.get('password')

                        if password:
                            remarks = f"白鲸鱼账号{mask_phone(account)}丨用户:{sender.getUserID()}丨授权时间:{auth_time}"
                            env_data = {
                                "name": var_name,
                                "value": f"{account}#{password}",
                                "remarks": remarks
                            }
                            env_id_with_prefix = add_to_panel(env_data)
                            if env_id_with_prefix:
                                sg.bucketSet('JQB.bjy.env_id', account, env_id_with_prefix)

                sender.reply(f'✅ 已授权 {len(selected_accounts)} 个账号 {months} 个月')
        elif choice == '2':
            user_coin = Decimal(sg.bucketGet(coin_bucket, sender.getUserID()) or '0')
            need_coin = coin_price * months * len(selected_accounts)
            if user_coin < need_coin:
                return sender.reply(f'❌ 积分不足，需要{need_coin}，当前有{user_coin}')

            new_coin = user_coin - need_coin
            sg.bucketSet(coin_bucket, sender.getUserID(), str(new_coin))
            today_date = datetime.now().date()
            today_time = str(today_date)
            for account in selected_accounts:
                auth = '2099-12-31'
                if not auth or auth < today_time:
                    auth_time = (datetime.now() + timedelta(days=months*30)).strftime('%Y-%m-%d')
                else:
                    auth_time = (datetime.strptime(auth, "%Y-%m-%d") + timedelta(days=months*30)).strftime('%Y-%m-%d')

                True

                account_data = sg.bucketGet('JQB.bjy.account', account)
                if account_data:
                    account_info = json.loads(account_data)
                    password = account_info.get('password')

                    if password:
                        remarks = f"白鲸鱼账号{mask_phone(account)}丨用户:{sender.getUserID()}丨授权时间:{auth_time}"
                        env_data = {
                            "name": var_name,
                            "value": f"{account}#{password}",
                            "remarks": remarks
                        }
                        env_id_with_prefix = add_to_panel(env_data)
                        if env_id_with_prefix:
                            sg.bucketSet('JQB.bjy.env_id', account, env_id_with_prefix)

            sender.reply(
                f"""✅ 已用 {need_coin} 积分授权 {len(selected_accounts)} 个账号 {months} 个月
剩余积分: {new_coin}"""
            )

    except Exception as e:
        sender.reply(f'❌ 授权失败: {str(e)}')

def process_payment(amount, days, sender):
    return True
def tutorial(sender):
    sender.reply("""=====白鲸鱼教程=====
🌟 核心功能指令:
1. 白鲸鱼登录 - 绑定账号(手机号#密码)
2. 白鲸鱼查询 - 查看可回收金额
3. 白鲸鱼签到 - 每日签到
4. 白鲸鱼管理 - 账号管理功能

⚙️ 授权说明:
1. 支持微信支付和积分支付
2. 授权后解锁全部功能
3. 自动同步到青龙/呆呆面板

⚠️ 注意事项:
1. 使用手机号+密码登录
2. 每日签到可获得积分
3. 积分可兑换现金
======================""")

def bjy_auth(sender):
    if not sender.isAdmin():
        sender.reply("⛔ 您没有权限执行此操作！")
        return

    today_date = datetime.now().date()
    today_time = str(today_date)

    sender.reply(
        "=====白鲸鱼授权管理=====\n"
        "  [1] 📱 一键授权所有用户\n"
        "  [2] 👤 单独授权用户\n"
        "  [3] ⏰ 修改授权时间\n"
        "  [4] 🗑️ 删除用户账号\n"
        "-------------------\n"
        "⚠️ 输入q退出操作\n"
        "=================="
    )
    choice = sender.input(60000, 1, False)

    if choice == 'q' or choice == 'Q':
        sender.reply("✅ 已取消操作")
        return
    elif choice == '':
        sender.reply('⏰ 输入超时!')
        return
    elif choice == '1':
        users = sg.bucketAllKeys('JQB.bjy.user')
        if not users:
            sender.reply("❌ 未找到任何绑定的白鲸鱼账号")
            return

        sender.reply('📝 请输入要给所有用户授权的月数！\n⚠️ 输入"q"退出操作')
        months = sender.input(60000, 1, False)
        if months == 'q' or months == 'Q':
            sender.reply("✅ 已取消操作")
            return
        elif months == '':
            sender.reply('⏰ 输入超时!')
            return

        try:
            months = int(months)
            success_count = 0
            var_name = sg.bucketGet('JQB.bjy', 'var_name') or 'bjy'

            for user in users:
                accountlist = sg.bucketGet('JQB.bjy.user', user)
                if not accountlist or accountlist == '[]':
                    continue

                accounts = _sg_literal(accountlist)
                for account in accounts:
                    try:
                        account_data = sg.bucketGet('JQB.bjy.account', account)
                        if not account_data:
                            continue

                        auth = '2099-12-31'
                        if not auth or auth < today_time:
                            auth_time = (datetime.now() + timedelta(days=months*30)).strftime('%Y-%m-%d')
                        else:
                            auth_time = (datetime.strptime(auth, "%Y-%m-%d") + timedelta(days=months*30)).strftime('%Y-%m-%d')

                        True

                        account_info = json.loads(account_data)
                        password = account_info.get('password')

                        if password:
                            remarks = f"白鲸鱼账号{mask_phone(account)}丨用户:{user}丨授权时间:{auth_time}"
                            env_data = {
                                "name": var_name,
                                "value": f"{account}#{password}",
                                "remarks": remarks
                            }
                            env_id_with_prefix = add_to_panel(env_data)
                            if env_id_with_prefix:
                                sg.bucketSet('JQB.bjy.env_id', account, env_id_with_prefix)
                        success_count += 1
                    except:
                        continue

            msg = f"""
=====一键授权完成=====
✅ 成功授权: {success_count}个账号
⏰ 授权月数: {months}月
=================="""
            sender.reply(msg)

        except ValueError:
            sender.reply('❌ 输入的月数无效!')
            return

    elif choice == '2':
        sender.reply('📝 请输入需要授权的用户ID\n💡 通过给机器人发送"myuid"获得\n⚠️ 输入"q"退出操作')
        user_id = sender.input(60000, 1, False)
        if user_id == 'q' or user_id == 'Q':
            sender.reply("✅ 已取消操作")
            return
        elif user_id == '':
            sender.reply('⏰ 输入超时!')
            return

        accountlist = sg.bucketGet('JQB.bjy.user', user_id)
        if not accountlist or accountlist == '[]':
            sender.reply(f"❌ 未找到用户 {user_id} 的白鲸鱼账号信息!")
            return

        accounts = _sg_literal(accountlist)
        n = 0
        msg = '=====用户账号列表=====\n'
        msg += '0、授权所有账号\n==================\n'

        for account in accounts:
            n += 1
            auth = '2099-12-31'
            if not auth:
                auth_status = '未授权'
            elif auth < today_time:
                auth_status = '授权过期'
            else:
                auth_status = f'到期: {auth}'
            msg += f'{n}、账号:{mask_phone(account)}\n授权状态: {auth_status}\n==================\n'

        msg += f'📝 回复序号选择账号\n⚠️ 输入"q"退出操作'
        sender.reply(msg)
        choice = sender.input(60000, 1, False)

        if choice == 'q' or choice == 'Q':
            sender.reply("✅ 已取消操作")
            return
        elif choice == '':
            sender.reply('⏰ 输入超时!')
            return

        if choice == '0':
            sender.reply('📝 请输入授权月数\n⚠️ 输入"q"退出操作')
            months = sender.input(60000, 1, False)

            if months == 'q' or months == 'Q':
                sender.reply("✅ 已取消操作")
                return
            elif months == '':
                sender.reply('⏰ 输入超时!')
                return

            try:
                months = int(months)
                success_count = 0
                var_name = sg.bucketGet('JQB.bjy', 'var_name') or 'bjy'

                for account in accounts:
                    try:
                        account_data = sg.bucketGet('JQB.bjy.account', account)
                        if not account_data:
                            continue

                        auth = '2099-12-31'
                        if not auth or auth < today_time:
                            auth_time = (datetime.now() + timedelta(days=months*30)).strftime('%Y-%m-%d')
                        else:
                            auth_time = (datetime.strptime(auth, "%Y-%m-%d") + timedelta(days=months*30)).strftime('%Y-%m-%d')

                        True

                        account_info = json.loads(account_data)
                        password = account_info.get('password')

                        if password:
                            remarks = f"白鲸鱼账号{mask_phone(account)}丨用户:{user_id}丨授权时间:{auth_time}"
                            env_data = {
                                "name": var_name,
                                "value": f"{account}#{password}",
                                "remarks": remarks
                            }
                            env_id_with_prefix = add_to_panel(env_data)
                            if env_id_with_prefix:
                                sg.bucketSet('JQB.bjy.env_id', account, env_id_with_prefix)
                        success_count += 1
                    except:
                        continue

                msg = f"""
=====批量授权完成=====
✅ 成功授权: {success_count}个账号
⏰ 授权月数: {months}月
=================="""
                sender.reply(msg)

            except ValueError:
                sender.reply('❌ 输入的月数无效!')
                return

        elif 1 <= int(choice) <= len(accounts):
            account = accounts[int(choice)-1]
            sender.reply('📝 请输入授权月数\n⚠️ 输入"q"退出操作')
            months = sender.input(60000, 1, False)

            if months == 'q' or months == 'Q':
                sender.reply("✅ 已取消操作")
                return
            elif months == '':
                sender.reply('⏰ 输入超时!')
                return

            try:
                months = int(months)
                account_data = sg.bucketGet('JQB.bjy.account', account)

                if not account_data:
                    sender.reply("❌ 未找到账号信息!")
                    return

                auth = '2099-12-31'
                if not auth or auth < today_time:
                    auth_time = (datetime.now() + timedelta(days=months*30)).strftime('%Y-%m-%d')
                else:
                    auth_time = (datetime.strptime(auth, "%Y-%m-%d") + timedelta(days=months*30)).strftime('%Y-%m-%d')

                True

                var_name = sg.bucketGet('JQB.bjy', 'var_name') or 'bjy'
                account_info = json.loads(account_data)
                password = account_info.get('password')

                if password:
                    remarks = f"白鲸鱼账号{mask_phone(account)}丨用户:{user_id}丨授权时间:{auth_time}"
                    env_data = {
                        "name": var_name,
                        "value": f"{account}#{password}",
                        "remarks": remarks
                    }
                    env_id_with_prefix = add_to_panel(env_data)
                    if env_id_with_prefix:
                        sg.bucketSet('JQB.bjy.env_id', account, env_id_with_prefix)

                msg = f"""
=====授权成功=====
✅ 账号: {mask_phone(account)}
⏰ 授权月数: {months}月
📅 到期时间: {auth_time}
=================="""
                sender.reply(msg)

            except ValueError:
                sender.reply('❌ 输入的月数无效!')
                return
        else:
            sender.reply('❌ 输入的序号无效!')
            return
    elif choice == '3':
        sender.reply(
            "=====修改授权时间=====\n"
            "  [1] 📱 修改所有用户\n"
            "  [2] 👤 修改单独用户\n"
            "-------------------\n"
            "⚠️ 输入q退出操作\n"
            "==================="
        )
        sub_choice = sender.input(60000, 1, False)

        if sub_choice == 'q' or sub_choice == 'Q':
            sender.reply("✅ 已取消操作")
            return
        elif sub_choice == '':
            sender.reply('⏰ 输入超时!')
            return
        elif sub_choice == '1':
            users = sg.bucketAllKeys('JQB.bjy.user')
            if not users:
                sender.reply("❌ 未找到任何绑定的白鲸鱼账号")
                return

            sender.reply('📝 请输入要调整的天数:\n➕ 正数增加天数\n➖ 负数减少天数\n💡 例如: 100 或 -100\n⚠️ 输入"q"退出操作')
            days = sender.input(60000, 1, False)
            if days == 'q' or days == 'Q':
                sender.reply("✅ 已取消操作")
                return
            elif days == '':
                sender.reply('⏰ 输入超时!')
                return

            try:
                days = int(days)
                total_success = 0

                var_name = sg.bucketGet('JQB.bjy', 'var_name') or 'bjy'

                for user in users:
                    accountlist = sg.bucketGet('JQB.bjy.user', user)
                    if not accountlist or accountlist == '[]':
                        continue

                    accounts = _sg_literal(accountlist)
                    for account in accounts:
                        try:
                            auth = '2099-12-31'
                            account_data = sg.bucketGet('JQB.bjy.account', account)

                            if not account_data or not auth:
                                continue

                            if auth == '未授权' or auth < today_time:
                                current_date = today_date
                            else:
                                current_date = datetime.strptime(auth, "%Y-%m-%d").date()

                            new_date = current_date + timedelta(days=days)
                            account_info = json.loads(account_data)
                            password = account_info.get('password')

                            if password:
                                remarks = f"白鲸鱼账号{mask_phone(account)}丨用户:{user}丨授权时间:{new_date}"
                                env_data = {
                                    "name": var_name,
                                    "value": f"{account}#{password}",
                                    "remarks": remarks
                                }
                                env_id_with_prefix = add_to_panel(env_data)
                                if env_id_with_prefix:
                                    sg.bucketSet('JQB.bjy.env_id', account, env_id_with_prefix)
                            total_success += 1
                        except:
                            continue

                msg = f"""
=====批量修改完成=====
✅ 成功修改: {total_success}个账号
⏰ 调整天数: {days}天
=================="""
                sender.reply(msg)

            except ValueError:
                sender.reply('❌ 输入的天数无效!')
                return

        elif sub_choice == '2':
            sender.reply('📝 请输入需要修改的用户ID\n💡 通过给机器人发送"myuid"获得\n⚠️ 输入"q"退出操作')
            user_id = sender.input(60000, 1, False)
            if user_id == 'q' or user_id == 'Q':
                sender.reply("✅ 已取消操作")
                return
            elif user_id == '':
                sender.reply('⏰ 输入超时!')
                return

            accountlist = sg.bucketGet('JQB.bjy.user', user_id)
            if not accountlist or accountlist == '[]':
                sender.reply(f"❌ 未找到用户 {user_id} 的白鲸鱼账号信息!")
                return

            accounts = _sg_literal(accountlist)
            n = 0
            msg = '=====用户账号列表=====\n'
            msg += '0、修改所有账号\n==================\n'

            for account in accounts:
                n += 1
                auth = '2099-12-31'
                if not auth:
                    auth_status = '未授权'
                elif auth < today_time:
                    auth_status = '授权过期'
                else:
                    auth_status = f'到期: {auth}'
                msg += f'{n}、账号:{mask_phone(account)}\n授权状态: {auth_status}\n==================\n'

            msg += f'📝 回复序号选择账号\n⚠️ 输入"q"退出操作'
            sender.reply(msg)
            choice = sender.input(60000, 1, False)

            if choice == 'q' or choice == 'Q':
                sender.reply("✅ 已取消操作")
                return
            elif choice == '':
                sender.reply('⏰ 输入超时!')
                return

            if choice == '0':
                sender.reply('📝 请输入要调整的天数:\n➕ 正数增加天数\n➖ 负数减少天数\n💡 例如: 100 或 -100\n⚠️ 输入"q"退出操作')
                days = sender.input(60000, 1, False)

                if days == 'q' or days == 'Q':
                    sender.reply("✅ 已取消操作")
                    return
                elif days == '':
                    sender.reply('⏰ 输入超时!')
                    return

                try:
                    days = int(days)
                    success_count = 0

                    var_name = sg.bucketGet('JQB.bjy', 'var_name') or 'bjy'

                    for account in accounts:
                        try:
                            auth = '2099-12-31'
                            account_data = sg.bucketGet('JQB.bjy.account', account)

                            if not account_data or not auth:
                                continue

                            if auth == '未授权' or auth < today_time:
                                current_date = today_date
                            else:
                                current_date = datetime.strptime(auth, "%Y-%m-%d").date()

                            new_date = current_date + timedelta(days=days)
                            account_info = json.loads(account_data)
                            password = account_info.get('password')

                            if password:
                                remarks = f"白鲸鱼账号{mask_phone(account)}丨用户:{user_id}丨授权时间:{new_date}"
                                env_data = {
                                    "name": var_name,
                                    "value": f"{account}#{password}",
                                    "remarks": remarks
                                }
                                env_id_with_prefix = add_to_panel(env_data)
                                if env_id_with_prefix:
                                    sg.bucketSet('JQB.bjy.env_id', account, env_id_with_prefix)
                            success_count += 1
                        except:
                            continue

                    msg = f"""
=====批量修改完成=====
✅ 成功修改: {success_count}个账号
⏰ 调整天数: {days}天
=================="""
                    sender.reply(msg)

                except ValueError:
                    sender.reply('❌ 输入的天数无效!')
                    return

            elif 1 <= int(choice) <= len(accounts):
                account = accounts[int(choice)-1]
                sender.reply('📝 请输入要调整的天数:\n➕ 正数增加天数\n➖ 负数减少天数\n💡 例如: 100 或 -100\n⚠️ 输入"q"退出操作')
                days = sender.input(60000, 1, False)

                if days == 'q' or days == 'Q':
                    sender.reply("✅ 已取消操作")
                    return
                elif days == '':
                    sender.reply('⏰ 输入超时!')
                    return

                try:
                    days = int(days)
                    auth = '2099-12-31'
                    account_data = sg.bucketGet('JQB.bjy.account', account)

                    if not account_data or not auth:
                        sender.reply("❌ 未找到账号信息!")
                        return

                    if auth == '未授权' or auth < today_time:
                        current_date = today_date
                    else:
                        current_date = datetime.strptime(auth, "%Y-%m-%d").date()

                    new_date = current_date + timedelta(days=days)
                    var_name = sg.bucketGet('JQB.bjy', 'var_name') or 'bjy'
                    account_info = json.loads(account_data)
                    password = account_info.get('password')

                    if password:
                        remarks = f"白鲸鱼账号{mask_phone(account)}丨用户:{user_id}丨授权时间:{new_date}"
                        env_data = {
                            "name": var_name,
                            "value": f"{account}#{password}",
                            "remarks": remarks
                        }
                        env_id_with_prefix = add_to_panel(env_data)
                        if env_id_with_prefix:
                            sg.bucketSet('JQB.bjy.env_id', account, env_id_with_prefix)

                    msg = f"""
=====修改成功=====
✅ 账号: {mask_phone(account)}
⏰ 调整天数: {days}天
📅 新到期时间: {new_date}
=================="""
                    sender.reply(msg)

                except ValueError:
                    sender.reply('❌ 输入的天数无效!')
                    return
            else:
                sender.reply('❌ 输入的序号无效!')
                return
        else:
            sender.reply('❌ 输入的选项无效!')
            return
    elif choice == '4':
        users = sg.bucketAllKeys('JQB.bjy.user')
        if not users:
            return sender.reply("❌ 没有可删除的用户账号")

        menu = "=====选择要删除的用户=====\n"
        for idx, user in enumerate(users, 1):
            accounts = _sg_literal(sg.bucketGet('JQB.bjy.user', user) or [])
            menu += f"[{idx}] 用户ID: {user} (账号数: {len(accounts)})\n"
        menu += "=======================\n⚠️ 回复数字序号(输入q退出)"
        sender.reply(menu)

        choice = sender.input(60000, 1, False)
        if not choice or choice.lower() == 'q':
            return sender.reply('已取消操作')

        try:
            index = int(choice) - 1
            if 0 <= index < len(users):
                user_id = users[index]

                accounts = _sg_literal(sg.bucketGet('JQB.bjy.user', user_id) or [])

                menu = "=====用户账号列表=====\n"
                menu += "0、删除所有账号\n==================\n"
                for idx, account in enumerate(accounts, 1):
                    auth = '2099-12-31'
                    if not auth:
                        auth_status = '未授权'
                    elif auth < today_time:
                        auth_status = '授权过期'
                    else:
                        auth_status = f'到期: {auth}'
                    menu += f"{idx}、账号: {mask_phone(account)}\n授权状态: {auth_status}\n==================\n"
                menu += "📝 回复序号选择账号\n⚠️ 输入'q'退出操作"
                sender.reply(menu)

                acc_choice = sender.input(60000, 1, False)
                if not acc_choice or acc_choice.lower() == 'q':
                    return sender.reply('已取消操作')

                if acc_choice == '0':
                    confirm_msg = f"""=====⚠️警告⚠️=====
即将删除用户ID: {user_id} 的所有账号
账号列表:
{", ".join([mask_phone(acc) for acc in accounts])}
------------------
此操作不可恢复！
确认请回复【y】
取消请回复【n】
=================="""
                    sender.reply(confirm_msg)

                    confirm = sender.input(60000, 1, False)
                    if confirm.lower() != 'y':
                        return sender.reply('✅ 已取消删除操作')

                    deleted_count = 0
                    for account in accounts:
                        try:
                            env_id_with_prefix = sg.bucketGet('JQB.bjy.env_id', account)
                            if env_id_with_prefix:
                                delete_from_panel(env_id_with_prefix)

                            sg.bucketDel('JQB.bjy.account', account)
                            True
                            sg.bucketDel('JQB.bjy.env_id', account)
                            deleted_count += 1
                        except:
                            continue

                    sg.bucketDel('JQB.bjy.user', user_id)

                    sender.reply(f"✅ 已删除用户 {user_id} 的 {deleted_count} 个账号")

                elif acc_choice.isdigit() and 1 <= int(acc_choice) <= len(accounts):
                    acc_index = int(acc_choice) - 1
                    account = accounts[acc_index]

                    confirm_msg = f"""=====⚠️警告⚠️=====
即将删除账号:
📱 账号: {mask_phone(account)}
------------------
此操作不可恢复！
确认请回复【y】
取消请回复【n】
=================="""
                    sender.reply(confirm_msg)

                    confirm = sender.input(60000, 1, False)
                    if confirm.lower() != 'y':
                        return sender.reply('✅ 已取消删除操作')

                    env_id_with_prefix = sg.bucketGet('JQB.bjy.env_id', account)
                    if env_id_with_prefix:
                        delete_from_panel(env_id_with_prefix)

                    sg.bucketDel('JQB.bjy.account', account)
                    True
                    sg.bucketDel('JQB.bjy.env_id', account)

                    accounts.pop(acc_index)
                    if accounts:
                        sg.bucketSet('JQB.bjy.user', user_id, str(accounts))
                    else:
                        sg.bucketDel('JQB.bjy.user', user_id)

                    sender.reply(f"✅ 已删除账号: {mask_phone(account)}")
                else:
                    sender.reply('❌ 输入的序号无效!')
            else:
                sender.reply('❌ 选择超出范围')
        except:
            sender.reply('❌ 输入错误')
    else:
        sender.reply('❌ 输入的选项无效!')

def main():
    try:
        senderID = sg.getSenderID()
        sender = sg.Sender(senderID)
        message = sender.getMessage().strip().lower()

        if '登录' in message:
            bind(sender)
        elif '查询' in message:
            query(sender)
        elif '签到' in message:
            sign_in(sender)
        elif '管理' in message:
            manage_accounts(sender)
        elif '教程' in message or '帮助' in message:
            tutorial(sender)
        elif message == '白鲸鱼清理' and sender.isAdmin():
            clean_expired(sender)
        elif message == '白鲸鱼授权' and sender.isAdmin():
            bjy_auth(sender)
        else:
            sender.reply("""指令未识别，可用指令:
白鲸鱼登录 - 绑定账号
白鲸鱼查询 - 查看状态
白鲸鱼签到 - 每日签到
白鲸鱼管理 - 账号管理
白鲸鱼教程 - 使用说明""")
    except Exception as e:
        traceback.print_exc()
        try:
            senderID = sg.getSenderID()
            if senderID:
                sender = sg.Sender(senderID)
                sender.reply(f"❌ 插件运行出错: {str(e)}")
        except:
            pass

def clean_expired(sender):
    try:
        sender.reply('该管理项已取消，账号直接运行')
    except Exception:
        pass
    return None
if __name__ == "__main__":
    try:
        if sg.getSenderID() == "":
            pass  # 定时任务模式（已移除）
        else:
            main()
    except Exception as e:
        traceback.print_exc()
        try:
            senderID = sg.getSenderID()
            if senderID:
                sender = sg.Sender(senderID)
                sender.reply(f"❌ 插件运行出错: {str(e)}")
        except:
            pass
