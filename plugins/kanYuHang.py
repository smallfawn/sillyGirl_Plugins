# [title: 看余杭]
# [name: kanYuHang]
# [language: python]
# [class: 任务]
# [author: Lies]
# [version: v1.9]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(看余杭)(登录|登陆)$|^登(录|陆)(看余杭)$|^(看余杭)(查询|管理)$|^(查询|管理)(看余杭)$|^清理看余杭$|^看余杭$]
# [cron: 0 0 * * *]
# [icon: https://www.helloimg.com/i/2025/02/03/67a06719bd58f.jpg]
# [description: 看余杭插件，支持短信跟Token登录；由流云集团附属集团开发，维护能力有限，；账号交青龙禁用启用逻辑；更新:  修复未登录查询异常bug；更新:  修复未登录管理异常；更新:  优化了一些已知问题；更新:  优化了一些已知问题2/26/22:20；相关脚本链接：【看余杭交流学习文件.py]
# [depe: ["aiohttp","requests"]]


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
    'kangyh_ql_host': form.string().title('青龙地址').default('').description('青龙面板的访问地址'),
    'kangyh_ql_client_id': form.string().title('青龙应用ID').default('').description('青龙面板的应用ID'),
    'kangyh_ql_client_secret': form.string().title('青龙应用秘钥').default('').description('青龙面板的应用秘钥'),
    'kangyh_var_name': form.string().title('青龙变量名').default('').description('提交到青龙的变量名'),
})
_CONFIG_FIELD_MAP = {
    ('kangyh', 'ql_host'): 'kangyh_ql_host',
    ('kangyh', 'ql_client_id'): 'kangyh_ql_client_id',
    ('kangyh', 'ql_client_secret'): 'kangyh_ql_client_secret',
    ('kangyh', 'var_name'): 'kangyh_var_name',
}

import re#处理正则表达式
from datetime import datetime, timedelta#操作日期、时间以及时间间隔
import urllib.parse #处理url编码
from decimal import Decimal#处理浮点数
import requests#处理http请求
import time#处理时间
import json#处理json数据
import hashlib#处理哈希值
import uuid#生成唯一ID
import asyncio
import aiohttp
from functools import lru_cache
import decimal

senderID = sg.getSenderID()#获取发送者QQ号
sender = sg.Sender(senderID)#获取发送者对象
userid = sender.getUserID()#存储当前发送者的用户 ID，与 senderID 类似，但通常用于内部标识
uservalue = sg.bucketGet(bucket='kangyh_user', key=userid)


def get_config():
    """获取插件配置"""
    try:
        var_name = sg.bucketGet('kangyh', 'var_name')
        if not var_name:
            print("未配置变量名，使用默认值: Look_at_Yuhang")
            var_name = 'Look_at_Yuhang'
            sg.bucketSet('kangyh', 'var_name', var_name)

        ql_host = sg.bucketGet('kangyh', 'ql_host')
        ql_client_id = sg.bucketGet('kangyh', 'ql_client_id')
        ql_client_secret = sg.bucketGet('kangyh', 'ql_client_secret')

        if not all([ql_host, ql_client_id, ql_client_secret]):
            raise Exception("青龙配置不完整，请检查配置")

        manage_cmd = sg.bucketGet('kangyh', 'manage_cmd') or '看余杭管理'
        query_cmd = sg.bucketGet('kangyh', 'query_cmd') or '看余杭查询'
        login_cmd = sg.bucketGet('kangyh', 'login_cmd') or '看余杭登录'

        try:
            price = Decimal(sg.bucketGet('kangyh', 'price') or '1')
            if price < 0:
                raise ValueError("价格不能为负数")
        except (ValueError, decimal.InvalidOperation):
            print("价格配置无效，使用默认值: 1")
            price = Decimal('1')
            sg.bucketSet('kangyh', 'price', '1')

        try:
            coin_price = int(sg.bucketGet('kangyh', 'coin') or '0')
            if coin_price < 0:
                raise ValueError("积分不能为负数")
        except ValueError:
            print("积分配置无效，使用默认值: 0")
            coin_price = 0
            sg.bucketSet('kangyh', 'coin', '0')

        return (var_name, ql_host, ql_client_id, ql_client_secret, manage_cmd, query_cmd, login_cmd, price, coin_price)

    except Exception as e:
        error_msg = f"获取配置失败: {str(e)}"
        print(error_msg)
        sender.reply(f"❌ {error_msg}")
        raise

def init_qinglong():
    """初始化青龙连接"""
    try:
        ql_host = sg.bucketGet('kangyh', 'ql_host') or ''
        ql_client_id = sg.bucketGet('kangyh', 'ql_client_id') or ''
        ql_client_secret = sg.bucketGet('kangyh', 'ql_client_secret') or ''

        if not ql_host or not ql_client_id or not ql_client_secret:
            sender.reply("❌ 未配置完整的青龙信息")
            exit(0)

        if not ql_host.endswith('/'):
            ql_host += '/'

        token = get_ql_token(ql_host, ql_client_id, ql_client_secret)
        return ql_host, token

    except Exception as e:
        sender.reply(f"❌ 连接青龙失败: {str(e)}")
        exit(0)

def get_ql_token(url, client_id, client_secret):
    """获取青龙token"""
    try:
        if not url.endswith('/'):
            url += '/'

        r = requests.get(f'{url}open/auth/token?client_id={client_id}&client_secret={client_secret}')
        if r.status_code != 200:
            raise Exception(f"请求失败: {r.status_code}")

        data = r.json()
        if "token" not in data.get('data', {}):
            raise Exception("获取token失败")

        return data['data']['token']

    except Exception as e:
        raise Exception(f"获取token失败: {str(e)}")

def add_to_qinglong(token, account, mobile):
    """添加变量到青龙"""
    try:
        url = f"{ql_url}/open/envs"
        headers = {
            "Authorization": f"Bearer {ql_token}",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception("获取变量失败")

        try:
            response_data = response.json()
            if not isinstance(response_data, dict) or 'data' not in response_data:
                raise Exception("青龙返回数据格式错误")
            envs_data = response_data['data']
            if not isinstance(envs_data, list):
                raise Exception("青龙环境变量数据格式错误")
        except json.JSONDecodeError:
            raise Exception("解析青龙返回数据失败")

        exists_id = None
        for env in envs_data:
            if isinstance(env, dict) and env.get('name') == var_name and account in env.get('remarks', ''):
                exists_id = env.get('id')
                break

        if len(token) == 32:  # 标准token长度为32位
            remarks = f"账号:{account}丨用户:{userid}丨Token:{token[:6]}...{token[-6:]}"
        else:
            remarks = f"账号:{account}丨用户:{userid}丨手机:{mobile}"

        data = {
            "name": var_name,
            "value": token,
            "remarks": remarks
        }

        new_env_ids = []
        if exists_id:
            data['id'] = exists_id
            response = requests.put(url, headers=headers, json=data)
            if response.status_code == 200:
                new_env_ids.append(exists_id)
                print(f"更新变量成功: {var_name}")
        else:
            response = requests.post(url, headers=headers, json=[data])
            if response.status_code == 200:
                try:
                    resp_data = response.json()
                    if isinstance(resp_data, dict) and isinstance(resp_data.get('data'), list):
                        for env_item in resp_data['data']:
                            if isinstance(env_item, dict) and 'id' in env_item:
                                new_env_ids.append(env_item['id'])
                                print(f"添加变量成功: {var_name}")
                except Exception as e:
                    print(f"解析新增变量响应失败: {str(e)}")

        if response.status_code != 200:
            raise Exception(f"提交变量失败: HTTP {response.status_code}")

        if new_env_ids:
            sg.bucketSet('kangyh_env_id', account, json.dumps(new_env_ids))
            print(f"保存环境变量ID成功: {new_env_ids}")

        return True

    except Exception as e:
        error_msg = f"青龙操作失败: {str(e)}"
        print(error_msg)
        sender.reply(f"❌ {error_msg}")
        return False

def enable_in_qinglong(env_ids):
    """启用环境变量"""
    try:
        url = f"{ql_url}/open/envs/enable"
        headers = {
            "Authorization": f"Bearer {ql_token}",
            "Content-Type": "application/json"
        }
        response = requests.put(url, headers=headers, data=json.dumps(env_ids))
        if response.status_code == 200:
            rjson = response.json()
            if rjson.get('code') == 200:
                return True
            else:
                sender.reply(f"❌ 启用环境变量失败: {rjson.get('message')}")
                return False
        else:
            raise Exception(f"{response.status_code}")
    except Exception as e:
        sender.reply(f"❌ 启用环境变量失败: {str(e)}")
        return False

def disable_in_qinglong(env_ids):
    """禁用环境变量"""
    try:
        url = f"{ql_url}/open/envs/disable"
        headers = {
            "Authorization": f"Bearer {ql_token}",
            "Content-Type": "application/json"
        }
        response = requests.put(url, headers=headers, data=json.dumps(env_ids))
        if response.status_code == 200:
            rjson = response.json()
            if rjson.get('code') == 200:
                return True
            else:
                sender.reply(f"❌ 禁用环境变量失败: {rjson.get('message')}")
                return False
        else:
            raise Exception(f"{response.status_code}")
    except Exception as e:
        sender.reply(f"❌ 禁用环境变量失败: {str(e)}")
        return False

def delete_from_qinglong(account):
    """从青龙删除变量"""
    try:
        url = f"{ql_url}/open/envs"
        headers = {
            "Authorization": f"Bearer {ql_token}"
        }

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception("获取变量失败")

        env_id = None
        for env in response.json()['data']:
            if env['name'] == var_name and account in env.get('remarks', ''):
                env_id = env['id']
                break

        if env_id:
            response = requests.delete(url, headers=headers, json=[env_id])
            if response.status_code != 200:
                raise Exception("删除变量失败")

        return True

    except Exception as e:
        sender.reply(f"❌ 青龙操作失败: {str(e)}")
        return False

def login():
    """登录实现"""
    login_guide = """
=====登录方式=====
[1] 验证码登录
[2] Token登录
------------------
回复数字选择方式
回复"q"退出"""

    sender.reply(login_guide)
    choice = sender.listen(60000)

    if not choice:
        sender.reply("❌ 操作超时")
        return
    elif choice == 'q':
        sender.reply("✅ 已取消登录")
        return

    try:
        if choice == '1':
            return code_login()
        elif choice == '2':
            return token_login()
        else:
            sender.reply("❌ 无效的选择")
            return

    except Exception as e:
        sender.reply(f"❌ 登录失败: {str(e)}")
        return

def code_login():
    """验证码登录实现"""
    try:
        sender.reply("请输入手机号:")
        mobile = sender.listen(60000)

        if not mobile:
            sender.reply("❌ 操作超时")
            return
        elif mobile == 'q':
            sender.reply("✅ 已取消登录")
            return

        if not re.match(r'^1[3-9]\d{9}$', mobile):
            raise Exception("无效的手机号")

        send_data = {
            "traceId": f"G9OBF59J{int(time.time()*1000)}",
            "data": {
                "mobilePhone": mobile
            },
            "service": "core",
            "userDevice": {
                "os": "14",
                "deviceBrand": "Redmi",
                "deviceId": "13666addccf39a5c",
                "equipmentId": "13666addccf39a5c",
                "deviceType": "Xiaomi Redmi K30 Pro Zoom Edition",
                "device": "android",
                "clientVersion": "5.2.3",
                "gtCid": ""
            },
            "api": "v2/login/sendLoginCode",
            "token": ""
        }

        response = requests.post(
            "https://app.eyh.cn/gateway/api",
            json=send_data,
            headers={"Content-Type": "application/json; charset=utf-8"}
        )

        if response.status_code != 200:
            raise Exception("发送验证码失败")

        result = response.json()
        if result['code'] != "0":
            raise Exception(f"发送验证码失败: {result['message']}")

        serial_num = result['data']

        sender.reply("请输入收到的验证码:")
        code = sender.listen(60000)

        if not code:
            sender.reply("❌ 操作超时")
            return
        elif code == 'q':
            sender.reply("✅ 已取消登录")
            return

        if not code.isdigit():
            raise Exception("无效的验证码")

        login_data = {
            "traceId": f"EAROJV8N{int(time.time()*1000)}",
            "data": {
                "serialNum": serial_num,
                "code": code
            },
            "service": "core",
            "userDevice": {
                "os": "14",
                "deviceBrand": "Redmi",
                "deviceId": "13666addccf39a5c",
                "equipmentId": "13666addccf39a5c",
                "deviceType": "Xiaomi Redmi K30 Pro Zoom Edition",
                "device": "android",
                "clientVersion": "5.2.3",
                "gtCid": ""
            },
            "api": "v2/login/codeLogin",
            "token": ""
        }

        response = requests.post(
            "https://app.eyh.cn/gateway/api",
            json=login_data,
            headers={"Content-Type": "application/json; charset=utf-8"}
        )

        if response.status_code != 200:
            raise Exception("登录失败")

        result = response.json()
        if result['code'] != "0":
            raise Exception(f"登录失败: {result['message']}")

        token = result['data']
        return process_login(token, mobile, mobile)

    except Exception as e:
        raise Exception(f"验证码登录失败: {str(e)}")

def token_login():
    """Token登录实现"""
    token_guide = """
=====看余杭Token登录=====
请在一分钟内输入Token字符串
示例: 08adb1b15e5492381cb6d900
a416407b
=======================
回复"q"退出"""

    sender.reply(token_guide)
    token = sender.listen(60000)

    if not token:
        sender.reply("❌ 操作超时")
        return
    elif token == 'q':
        sender.reply("✅ 已取消登录")
        return

    try:
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        data = {
            "service": "media",
            "api": "lottery/queryActivityAwardRecordList",
            "data": {
                "uid": "30a7f9016d224fc2a8367200cbbab62a",
                "content": "null"
            },
            "userDevice": {
                "os": "14",
                "deviceBrand": "Redmi",
                "deviceId": "13666addccf39a5c",
                "equipmentId": "13666addccf39a5c",
                "deviceType": "Xiaomi Redmi K30 Pro Zoom Edition",
                "device": "android",
                "clientVersion": "5.2.3",
                "gtCid": ""
            },
            "traceId": f"KICUBKZ9{int(time.time()*1000)}",
            "token": token
        }

        response = requests.post(
            "https://app.eyh.cn/gateway/api",
            json=data,
            headers=headers
        )

        if response.status_code != 200:
            raise Exception("Token验证失败")

        result = response.json()
        if result['code'] != "0":
            error_msg = result.get('message', '未知错误')
            if "登录状态已失效" in error_msg:
                raise Exception("Token已失效,请重新登录")
            raise Exception(f"Token无效: {error_msg}")

        mobile = userid  # 使用发送者ID替代手机号

        log_operation('token_login', userid, mobile, 'success')

        return process_login(token, mobile, mobile)

    except Exception as e:
        log_operation('token_login', userid, 'unknown', 'failed', str(e))
        raise Exception(f"Token登录失败: {str(e)}")

def process_login(token, account, mobile):
    """处理登录成功后的操作"""
    try:
        accounts = _sg_literal(uservalue or '[]')
        if len(token) == 32:
            account = token
            display = f"Token...{token[-6:]}"
        else:
            account = mobile
            display = f"{mobile[:3]}****{mobile[-4:]}"

        if account not in accounts:
            accounts.append(account)
            sg.bucketSet('kangyh_user', userid, str(accounts))

        sg.bucketSet('kangyh_token', account, token)

        if not add_to_qinglong(token, account, mobile):
            raise Exception("添加青龙变量失败")

        env_id_str = sg.bucketGet('kangyh_env_id', account)
        if env_id_str:
            env_ids = json.loads(env_id_str)
            disable_in_qinglong(env_ids)

        success_msg = f"""
=====登录成功=====
📱 账号: {display}
✅ 已保存到青龙(当前禁用)
------------------
发送"{manage_cmd}"管理账号
发送"{query_cmd}"查询账号
"""
        sender.reply(success_msg)
        return True
    except Exception as e:
        raise Exception(f"处理登录失败: {str(e)}")

def manage_accounts():
    """管理账号"""
    if not uservalue:
        sender.reply(f"""
=====账号管理=====
❌ 未找到任何账号
------------------
💡 发送"{login_cmd}"登录账号
==================""")
        return

    accounts = _sg_literal(uservalue)
    if not accounts:  # 如果账号列表为空
        sender.reply(f"""
=====账号管理=====
❌ 未找到任何账号
------------------
💡 发送"{login_cmd}"登录账号
==================""")
        return

    account_list = """
=====账号列表=====
批量操作:
[01] 删除全部账号
[00] 授权全部账号
------------------
账号列表:"""

    for i, account in enumerate(accounts, 1):
        token = sg.bucketGet('kangyh_token', account)
        auth = '2099-12-31'
        auth_status = "✅ 已授权" if auth and auth > today else "❌ 未授权"

        if len(token) == 32:  # Token登录
            display = f"Token...{token[-6:]}"  # 只显示token后6位
        else:  # 手机号登录
            display = f"{account[:3]}****{account[-4:]}"  # 隐藏中间4位手机号

        account_list += f"\n[{i}] {display}\n    {auth_status}"
        if auth and auth > today:
            account_list += f"\n    到期: {auth}"

    account_list += """
------------------
回复数字选择账号
回复"q"退出"""

    sender.reply(account_list)
    choice = sender.listen(60000)

    if not choice:
        sender.reply("❌ 操作超时")
        return
    elif choice == 'q':
        sender.reply("✅ 已取消操作")
        return

    try:
        if choice == '01':
            for account in accounts:
                delete_account(account)
            sender.reply("✅ 已删除全部账号")
        elif choice == '00':
            sender.reply("请输入授权天数:")
            days = sender.listen(60000)

            if not days:
                sender.reply("❌ 操作超时")
                return
            elif days == 'q':
                sender.reply("✅ 已取消授权")
                return

            try:
                days = int(days)
                if days <= 0:
                    raise ValueError()

                amount = price * (Decimal(days) / Decimal(30)) * Decimal(len(accounts))
                amount = Decimal(str(amount)).quantize(Decimal('0.01'), rounding='ROUND_UP')

                if process_payment(amount, days):
                    success_count = 0
                    for account in accounts:
                        calculate_auth_time(account, days/30)
                        True
                        success_count += 1

                    sender.reply(f"""
=====批量授权成功=====
💰 支付: {amount}元
⏰ 时长: {days}天
✅ 成功: {success_count}个账号
==================""")

            except ValueError:
                sender.reply("❌ 无效的天数")
            except Exception as e:
                sender.reply(f"❌ 批量授权失败: {str(e)}")
        else:
            index = int(choice) - 1
            if not 0 <= index < len(accounts):
                raise ValueError()

            account = accounts[index]
            show_account_menu(account)

    except ValueError:
        sender.reply("❌ 无效的选择")
    except Exception as e:
        sender.reply(f"❌ 操作失败: {str(e)}")

def show_account_menu(account):
    """显示账号操作菜单"""
    token = sg.bucketGet('kangyh_token', account)
    auth = '2099-12-31'

    if len(token) == 32:
        display = f"Token...{token[-6:]}"
    else:
        display = f"{account[:3]}****{account[-4:]}"

    auth_status = "✅ 已授权" if auth and auth > today else "❌ 未授权"
    auth_info = f"\n    到期: {auth}" if auth and auth > today else ""

    menu = f"""
=====账号操作=====
📱 账号: {display}
🔐 状态: {auth_status}{auth_info}
------------------
[1] 授权账号
[2] 删除账号
------------------
回复数字选择操作
回复"q"退出"""

    sender.reply(menu)
    choice = sender.listen(60000)

    if not choice:
        sender.reply("❌ 操作超时")
        return
    elif choice == 'q':
        sender.reply("✅ 已取消操作")
        return

    try:
        if choice == '1':
            auth_account(account)
        elif choice == '2':
            delete_account(account)
        else:
            sender.reply("❌ 无效的选择")
    except Exception as e:
        sender.reply(f"❌ 操作失败: {str(e)}")

def auth_account(account):
    """账号授权"""
    try:
        user_coin = sg.bucketGet('dd_sign_coin', userid) or '0'
        user_coin = Decimal(user_coin)  # 使用 Decimal 处理大数值

        month_coin = Decimal(coin_price)  # 从配置获取每月所需积分

        if month_coin <= 0:
            auth_guide = """
=====授权方式=====
[1] 微信支付
------------------
回复数字选择方式
回复"q"退出"""
        else:
            auth_guide = f"""
=====授权方式=====
[1] 微信支付
[2] 积分支付 (当前积分: {user_coin})
------------------
💰 积分比例: {month_coin}积分/月
回复数字选择方式
回复"q"退出"""

        sender.reply(auth_guide)
        choice = sender.listen(60000)

        if not choice:
            sender.reply("❌ 操作超时")
            return False
        elif choice == 'q':
            sender.reply("✅ 已取消授权")
            return False

        if choice == '1':
            sender.reply("请输入授权天数:")
            days = sender.listen(60000)

            if not days:
                sender.reply("❌ 操作超时")
                return False
            elif days == 'q':
                sender.reply("✅ 已取消授权")
                return False

            days = int(days)
            if days <= 0:
                raise ValueError()

            amount = price * (Decimal(days) / Decimal(30))
            amount = Decimal(str(amount)).quantize(Decimal('0.01'), rounding='ROUND_UP')
            if amount < Decimal('0.01'):
                amount = Decimal('0.01')

            payment_success = process_payment(amount, days)  # 处理支付
            if payment_success:  # 只有在支付成功的情况下才进行授权
                auth_time = calculate_auth_time(account, days/30)
                True

                env_id_str = sg.bucketGet('kangyh_env_id', account)
                if env_id_str:
                    env_ids = json.loads(env_id_str)
                    enable_in_qinglong(env_ids)

                sender.reply(f"""
=====授权成功=====
📱 账号: {account[:3]}****{account[-4:]}
💰 支付: {amount}元
⏰ 时长: {days}天
📅 到期: {auth_time}
==================""")
                return True
            else:
                sender.reply("❌ 支付未成功，授权未完成")
                return False

        elif choice == '2' and month_coin > 0:  # 只有积分支付开启时才处理
            sender.reply("请输入授权月数:")
            months = sender.listen(60000)

            if not months:
                sender.reply("❌ 操作超时")
                return False
            elif months == 'q':
                sender.reply("✅ 已取消授权")
                return False

            months = int(months)
            if months <= 0:
                raise ValueError()

            need_coin = month_coin * months

            if user_coin < need_coin:
                sender.reply(f"""
=====积分不足=====
❌ 积分余额不足
------------------
💰 所需积分: {need_coin}
💵 当前积分: {user_coin}
==================""")
                return False

            new_coin = user_coin - need_coin
            sg.bucketSet('dd_sign_coin', userid, str(new_coin))

            auth_time = calculate_auth_time(account, months)
            True

            env_id_str = sg.bucketGet('kangyh_env_id', account)
            if env_id_str:
                env_ids = json.loads(env_id_str)
                enable_in_qinglong(env_ids)

            sender.reply(f"""
=====授权成功=====
📱 账号: {account[:3]}****{account[-4:]}
💰 消耗: {need_coin}积分
⏰ 时长: {months}月
📅 到期: {auth_time}
------------------
💵 剩余: {new_coin}积分
==================""")
            return True

        else:
            sender.reply("❌ 无效的选择")

    except ValueError:
        sender.reply("❌ 无效的数值")
    except Exception as e:
        sender.reply(f"❌ 授权失败: {str(e)}")
    return False

def process_payment(amount, days):
    return True

def query_account():
    """查询账号信息"""
    if not uservalue:
        sender.reply(f"""
=====账号查询=====
❌ 未找到任何账号
------------------
💡 发送"{login_cmd}"登录账号
==================""")
        return

    accounts = _sg_literal(uservalue)
    if not accounts:  # 如果账号列表为空
        sender.reply(f"""
=====账号查询=====
❌ 未找到任何账号
------------------
💡 发送"{login_cmd}"登录账号
==================""")
        return

    for account in accounts:
        try:
            auth = '2099-12-31'
            token = sg.bucketGet('kangyh_token', account)

            if len(token) == 32:
                display = f"Token...{token[-6:]}"
            else:
                display = f"{account[:3]}****{account[-4:]}"

            if not auth or auth <= today:
                sender.reply(f"""
=====账号未授权=====
📱 账号: {display}
❌ 状态: 未授权
💡 请先完成授权后再查询
==================""")
                continue

            if not token:
                continue

            headers = {
                "Content-Type": "application/json; charset=utf-8",
                "User-Agent": "okhttp/5.0.0-alpha.2",
                "Host": "app.eyh.cn",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip"
            }

            data = {
                "service": "media",
                "api": "lottery/queryActivityAwardRecordList",
                "data": {
                    "uid": "30a7f9016d224fc2a8367200cbbab62a",
                    "content": "null"
                },
                "userDevice": {
                    "os": "14",
                    "deviceBrand": "Redmi",
                    "deviceId": "13666addccf39a5c",
                    "equipmentId": "13666addccf39a5c",
                    "deviceType": "Xiaomi Redmi K30 Pro Zoom Edition",
                    "device": "android",
                    "clientVersion": "5.2.3",
                    "gtCid": ""
                },
                "traceId": f"QUERY{int(time.time()*1000)}",
                "token": token
            }

            response = requests.post(
                "https://app.eyh.cn/gateway/api",
                json=data,
                headers=headers
            )

            if response.status_code != 200:
                raise Exception("查询失败")

            result = response.json()
            if result['code'] != "0":
                raise Exception(f"查询失败: {result['message']}")

            awards = result['data']

            auth_status = "✅ 已授权" if auth and auth > today else "❌ 未授权"
            auth_time = f"\n📅 到期: {auth}" if auth else ""

            recent_awards = sorted(awards, key=lambda x: x['createTime'], reverse=True)[:3]
            total_amount = sum(
                float(award['description'].replace('元微信红包', ''))
                for award in recent_awards
                if '元微信红包' in award['description']
            )

            awards_display = ""
            if recent_awards:
                awards_display = "最近奖励记录:"
                for award in recent_awards:
                    award_time = datetime.fromtimestamp(award['createTime']/1000).strftime('%Y-%m-%d %H:%M:%S')
                    status = '已发放' if award['status'] == 2 else '未发放'
                    awards_display += f"\n🎁 {award['name']} ({award['description']})"
                    awards_display += f"\n⏰ 时间: {award_time}"
                    awards_display += f"\n📌 状态: {status}"
                    if award.get('grantTip'):
                        awards_display += f"\n💡 说明: {award['grantTip']}"

                if total_amount > 0:
                    awards_display += f"\n💰 近期总额: {total_amount:.2f}元"

            account_info = f"""
=====账号信息=====
📱 账号: {display}
🔐 授权: {auth_status}{auth_time}{awards_display}
=================="""
            account_info = account_info.replace("\n\n", "\n")  # 去掉多余的换行
            sender.reply(account_info)

        except Exception as e:
            error_msg = str(e)
            sender.reply(f"❌ 查询失败: {error_msg}")
            log_operation('query_account', userid, account, 'failed', error_msg)
            continue

def clean_expired():
    try:
        sender.reply('该管理项已取消，账号直接运行')
    except Exception:
        pass
    return None
def main():
    """主函数"""
    message = sender.getMessage()

    if '登录' in message:
        login()
    elif '管理' in message:
        manage_accounts()
    elif '查询' in message:
        query_account()
    elif message == '清理看余杭':
        clean_expired()
    elif message == '看余杭授权' and sender.isAdmin():
        admin_auth()
    else:
        sender.setContinue()

def cron_task():
    """定时任务处理"""
    if imtype != 'fake':
        return

    try:
        users = sg.bucketAllKeys('kangyh_user')
        for user in users:
            accounts = _sg_literal(sg.bucketGet('kangyh_user', user) or '[]')
            for account in accounts:
                try:
                    token = sg.bucketGet('kangyh_token', account)
                    if not token:
                        continue

                    auth = '2099-12-31'
                    if auth and auth <= today:
                        env_id_str = sg.bucketGet('kangyh_env_id', account)
                        if env_id_str:
                            env_ids = json.loads(env_id_str)
                            disable_in_qinglong(env_ids)
                        notify_user(user, account, "授权已过期,环境变量已禁用,请及时续费")
                        continue

                    headers = {
                        "Content-Type": "application/json; charset=utf-8",
                        "User-Agent": "okhttp/5.0.0-alpha.2",
                        "Host": "app.eyh.cn",
                        "Connection": "Keep-Alive",
                        "Accept-Encoding": "gzip"
                    }

                    data = {
                        "service": "media",
                        "api": "lottery/queryActivityAwardRecordList",
                        "data": {
                            "uid": "30a7f9016d224fc2a8367200cbbab62a",
                            "content": "null"
                        },
                        "userDevice": {
                            "os": "14",
                            "deviceBrand": "Redmi",
                            "deviceId": "13666addccf39a5c",
                            "equipmentId": "13666addccf39a5c",
                            "deviceType": "Xiaomi Redmi K30 Pro Zoom Edition",
                            "device": "android",
                            "clientVersion": "5.2.3",
                            "gtCid": ""
                        },
                        "traceId": f"CRON{int(time.time()*1000)}",
                        "token": token
                    }

                    response = requests.post(
                        "https://app.eyh.cn/gateway/api",
                        json=data,
                        headers=headers
                    )

                    if response.status_code != 200:
                        notify_user(user, account, "账号状态异常,请更新token")
                        continue

                    result = response.json()
                    if result['code'] != "0":
                        error_msg = result.get('message', '未知错误')
                        if "登录状态已失效" in error_msg:
                            notify_user(user, account, "Token已失效,请重新登录")
                            sg.bucketDel('kangyh_token', account)
                        else:
                            notify_user(user, account, f"账号异常: {error_msg}")
                        continue

                    auth = '2099-12-31'
                    if auth and auth <= today:
                        notify_user(user, account, "授权已过期,请及时续费")

                except Exception as e:
                    print(f"处理账号 {account} 出错: {str(e)}")
                    continue

    except Exception as e:
        print(f"定时任务出错: {str(e)}")

def notify_user(user, account, message):
    """发送用户通知"""
    try:
        notify_msg = f"""
=====账号通知=====
📱 账号: {account[:3]}****{account[-4:]}
📢 消息: {message}
=================="""

        sg.push('qq', '', user, '', notify_msg)
        sg.push('wx', '', user, '', notify_msg)
        sg.push('tg', '', user, '', notify_msg)

    except Exception as e:
        print(f"发送通知失败: {str(e)}")

def retry_on_error(func, retries=3, delay=1):
    """错误重试装饰器"""
    def wrapper(*args, **kwargs):
        for i in range(retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if i == retries - 1:
                    raise e
                time.sleep(delay)
        return None
    return wrapper

def log_operation(operation, user, account, status, message=''):
    """记录操作日志"""
    try:
        log = {
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'operation': operation,
            'user': user,
            'account': account,
            'status': status,
            'message': message
        }

        logs = _sg_literal(sg.bucketGet('kangyh_logs', 'operations') or '[]')
        logs.append(log)
        if len(logs) > 1000:  # 只保留最近1000条
            logs = logs[-1000:]
        sg.bucketSet('kangyh_logs', 'operations', str(logs))

    except Exception as e:
        print(f"记录日志失败: {str(e)}")

def admin_auth():
    try:
        sender.reply('该管理项已取消，账号直接运行')
    except Exception:
        pass
    return None
def auth_all_users():
    """一键授权所有用户"""
    sender.reply("""
=====批量授权=====
请输入授权天数
------------------
回复数字设置天数
回复"q"退出""")

    try:
        days = sender.listen(60000)
        if not days or days == 'q':
            sender.reply("✅ 已取消授权")
            return

        days = int(days)
        if days <= 0:
            raise ValueError()

        users = sg.bucketAllKeys('kangyh_user')
        success = 0
        failed = 0

        for user in users:
            accounts = _sg_literal(sg.bucketGet('kangyh_user', user) or '[]')
            for account in accounts:
                try:
                    calculate_auth_time(account, days/30)
                    True

                    token = sg.bucketGet('kangyh_token', account)
                    if token:
                        phone = account[:3] + '*'*4 + account[7:]
                        add_to_qinglong(token, account, phone)

                    env_ids_str = sg.bucketGet('kangyh_env_id', account)
                    if env_ids_str:
                        env_ids = json.loads(env_ids_str)
                        enable_in_qinglong(env_ids)

                    success += 1
                    log_operation('batch_auth', user, account, 'success')
                except Exception as e:
                    failed += 1
                    log_operation('batch_auth', user, account, 'failed', str(e))

        sender.reply(f"""
=====授权完成=====
✅ 成功: {success}个账号
❌ 失败: {failed}个账号
⏰ 授权: {days}天
==================""")

    except ValueError:
        sender.reply("❌ 无效的天数")
    except Exception as e:
        sender.reply(f"❌ 授权失败: {str(e)}")

def auth_specific_user():
    """指定用户授权"""
    sender.reply("""
=====指定授权=====
请输入用户ID
(发送myuid可获取ID)
------------------
回复"q"退出""")

    user_id = sender.listen(60000)
    if not user_id or user_id == 'q':
        return

    accounts = _sg_literal(sg.bucketGet('kangyh_user', user_id) or '[]')
    if not accounts:
        sender.reply("❌ 未找到该用户的账号")
        return

    account_list = """
=====账号列表=====
[0] 授权全部账号"""

    for i, account in enumerate(accounts, 1):
        auth = '2099-12-31'
        status = "✅ 已授权" if auth and auth > today else "❌ 未授权"
        account_list += f"\n[{i}] {account[:3]}****{account[-4:]}\n    {status}"

    account_list += """
------------------
回复数字选择账号
回复"q"退出"""

    sender.reply(account_list)
    choice = sender.listen(60000)

    if not choice or choice == 'q':
        return

    try:
        sender.reply("""
=====设置授权时间=====
请输入授权天数
------------------
回复数字设置天数
回复"q"退出""")

        days = sender.listen(60000)
        if not days or days == 'q':
            return

        days = int(days)
        if days <= 0:
            raise ValueError()

        if choice == '0':
            for account in accounts:
                try:
                    auth_time = calculate_auth_time(account, days/30)
                    True

                    token = sg.bucketGet('kangyh_token', account)
                    if token:
                        phone = account[:3] + '*'*4 + account[7:]
                        add_to_qinglong(token, account, phone)

                    env_ids_str = sg.bucketGet('kangyh_env_id', account)
                    if env_ids_str:
                        env_ids = json.loads(env_ids_str)
                        enable_in_qinglong(env_ids)

                    log_operation('auth', user_id, account, 'success')
                except Exception as e:
                    log_operation('auth', user_id, account, 'failed', str(e))

            sender.reply(f"✅ 已授权所有账号 {days}天")

        else:
            index = int(choice) - 1
            if not 0 <= index < len(accounts):
                raise ValueError()

            account = accounts[index]
            auth_time = calculate_auth_time(account, days/30)
            True

            token = sg.bucketGet('kangyh_token', account)
            if token:
                phone = account[:3] + '*'*4 + account[7:]
                add_to_qinglong(token, account, phone)

            env_ids_str = sg.bucketGet('kangyh_env_id', account)
            if env_ids_str:
                env_ids = json.loads(env_ids_str)
                enable_in_qinglong(env_ids)

            sender.reply(f"""
=====授权成功=====
📱 账号: {account[:3]}****{account[-4:]}
⏰ 时长: {days}天
📅 到期: {auth_time}
==================""")

            log_operation('auth', user_id, account, 'success')

    except ValueError:
        sender.reply("❌ 无效的输入")
    except Exception as e:
        sender.reply(f"❌ 授权失败: {str(e)}")
        log_operation('auth', user_id, account, 'failed', str(e))

def check_account_status(self, token):
    """检查账号状态"""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    data = {
        "service": "media",
        "api": "lottery/queryActivityAwardRecordList",
        "data": {
        "uid": "30a7f9016d224fc2a8367200cbbab62a",
        "content": "null"}
    }

    response = requests.post(
        "https://app.eyh.cn/gateway/api",
        json=data,
        headers=headers
    )
    return response

def delete_account(account):
    """删除账号"""
    try:
        if not delete_from_qinglong(account):
            raise Exception("从青龙删除变量失败")

        sg.bucketDel('kangyh_token', account)
        True

        accounts = _sg_literal(uservalue)
        if account in accounts:
            accounts.remove(account)
            sg.bucketSet('kangyh_user', userid, str(accounts))

        sender.reply(f"""
=====删除成功=====
📱 账号: {account[:3]}****{account[-4:]}
✅ 状态: 已删除
==================""")

        log_operation('delete_account', userid, account, 'success')
        return True

    except Exception as e:
        error_msg = f"删除账号失败: {str(e)}"
        sender.reply(f"❌ {error_msg}")
        log_operation('delete_account', userid, account, 'failed', str(e))
        return False

async def async_request(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            return await response.json()

@lru_cache(maxsize=100)
def cached_bucket_get(bucket, key):
    return sg.bucketGet(bucket, key)

login_data = globals().get("login_data", {})


async def async_add_to_qinglong(token):
    return add_to_qinglong(token, globals().get("userid", ""), globals().get("userid", ""))

async def async_login():
    token = await async_request("https://app.eyh.cn/gateway/api", login_data)
    if token:
        await async_add_to_qinglong(token)

if __name__ == "__main__":
    try:
        var_name, ql_host, ql_client_id, ql_client_secret, manage_cmd, query_cmd, login_cmd, price, coin_price = get_config()

        ql_url, ql_token = init_qinglong()

        imtype = sender.getImtype()
        today = str(datetime.now().date())

        if imtype == 'fake':
            cron_task()
        else:
            main()

    except Exception as e:
        sender.reply(f"❌ 运行出错: {str(e)}")
