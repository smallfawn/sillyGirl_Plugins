# [title: 胖乖生活]
# [name: pangGuaiShengHuo]
# [language: python]
# [class: 任务]
# [author: sky2022]
# [version: v4.4]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^胖乖管理$|^管理胖乖$|^胖乖查询$|^查询胖乖$|^胖乖登录$|^登录胖乖$|^登陆胖乖$|^胖乖登陆$|^胖乖$|^胖乖清理$|^清理胖乖$]
# [cron: 18 8,15 * * *]
# [icon: https://y.gtimg.cn/music/photo_new/T053M000002Qqrye0oyZSp.jpg]
# [description: 2.0全新UI；指令：胖乖登录、胖乖管理、胖乖查询、胖乖清理；4.3更新：统一面板配置为面板类型+对接面板配置，并新增呆呆面板分组配置]
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
    'dd_pg_config_panel_type': form.string().title('对接面板类型').default('').description('填写你当前使用的面板类型，支持：青龙、青龙面板、QL、呆呆、呆呆面板、Daidai'),
    'dd_pg_config_panel_config': form.string().title('对接面板配置').default('').description('统一填写面板对接参数。青龙：Host丨ClientID丨ClientSecret；呆呆：Host丨AppKey丨AppSecret；分隔符使用中文丨'),
    'dd_pg_config_panel_group': form.string().title('对接面板分组').default('').description('仅呆呆面板生效。填写后新增或更新变量时会同步写入 group 字段；留空则不处理分组'),
    'dd_pg_config_osname': form.string().title('面板变量名').default('').description('提交到面板中的胖乖变量名'),
})
_CONFIG_FIELD_MAP = {
    ('dd_pg_config', 'panel_type'): 'dd_pg_config_panel_type',
    ('dd_pg_config', 'panel_config'): 'dd_pg_config_panel_config',
    ('dd_pg_config', 'panel_group'): 'dd_pg_config_panel_group',
    ('dd_pg_config', 'osname'): 'dd_pg_config_osname',
}

import time
import requests
import hashlib
from urllib.parse import urlparse
import json
from datetime import datetime, timedelta
from decimal import Decimal
import urllib.parse
import re


senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()
uservalue = sg.bucketGet(bucket='dd_pg_user', key=userid) or ''

def normalize_panel_type(panel_type_value):
    """统一解析面板类型。"""
    value = str(panel_type_value or '').strip().lower()
    if value in ('呆呆', '呆呆面板', 'daidai', 'dd'):
        return 'daidai'
    if value in ('青龙', '青龙面板', 'qinglong', 'ql'):
        return 'qinglong'
    return ''

def getusercontent():
    """获取插件配置信息"""
    dd_pg_osname = sg.bucketGet('dd_pg_config', 'osname') or 'pangguai'
    panel_type = normalize_panel_type(sg.bucketGet('dd_pg_config', 'panel_type') or '')
    if not panel_type:
        sender.reply("对接面板类型填写无效，请填写：青龙/青龙面板/QL 或 呆呆/呆呆面板/Daidai")
        exit(0)

    panel_config = (sg.bucketGet('dd_pg_config', 'panel_config') or '').strip()
    dd_pg_qlname = panel_config if panel_type == 'qinglong' else ''
    dd_pg_ddname = panel_config if panel_type == 'daidai' else ''
    dd_managecommand = sg.bucketGet('dd_pg_config', 'dd_managecommand') or '胖乖管理'
    dd_querycommand = sg.bucketGet('dd_pg_config', 'dd_querycommand') or '胖乖查询'
    dd_signcommand = sg.bucketGet('dd_pg_config', 'dd_signcommand') or '胖乖登录'

    randommanagecommand = dd_managecommand
    randomquerycommand = dd_querycommand
    randomsigncommand = dd_signcommand

    pgVipmoney = Decimal(sg.bucketGet('dd_pg_config', 'pgVipmoney') or '1')
    pgcoin = int(sg.bucketGet('dd_pg_config', 'pgcoin') or '0')
    panel_group = (sg.bucketGet('dd_pg_config', 'panel_group') or '').strip()

    return (dd_pg_osname, dd_pg_qlname, dd_managecommand, dd_querycommand,
            dd_signcommand, randommanagecommand, randomquerycommand,
            randomsigncommand, pgVipmoney, pgcoin, panel_type == 'daidai', dd_pg_ddname, panel_group)

def seekql():
    """连接并验证面板配置"""
    try:
        panel_config = dd_pg_ddname if use_daidai else dd_pg_qlname
        if len(panel_config) == 0:
            if use_daidai:
                sender.reply("""=======配置错误=====
❌ 未配置呆呆面板信息
------------------
请在插件配置中填写:
• 对接面板类型: 呆呆
• 对接面板配置: Host丨AppKey丨AppSecret
====================""")
            else:
                sender.reply("""=======配置错误=====
❌ 未配置青龙面板信息
------------------
请在插件配置中填写:
• 对接面板类型: 青龙
• 对接面板配置: Host丨ClientID丨ClientSecret
====================""")
            exit(0)

        qllist = panel_config.split('丨')
        if len(qllist) != 3:
            if use_daidai:
                sender.reply(f"""=======格式错误=====
❌ 呆呆面板配置格式错误
------------------
当前格式: {panel_config}
正确格式:
Host丨AppKey丨AppSecret
====================""")
            else:
                sender.reply(f"""=======格式错误=====
❌ 青龙面板配置格式错误
------------------
当前格式: {panel_config}
正确格式:
Host丨ClientID丨ClientSecret
====================""")
            exit(0)

        QLurl = qllist[0].strip()
        ClientID = qllist[1].strip()
        ClientSecret = qllist[2].strip()

        if not all([QLurl, ClientID, ClientSecret]):
            sender.reply("❌ 面板配置参数不完整")
            exit(0)

        if not QLurl.startswith(('http://', 'https://')):
            sender.reply(f"❌ 面板地址格式错误: {QLurl}")
            exit(0)

        try:
            if use_daidai:
                qltoken = DDtoken(DDurl=QLurl, AppKey=ClientID, AppSecret=ClientSecret)
            else:
                qltoken = QLtoken(QLurl=QLurl, ClientID=ClientID, ClientSecret=ClientSecret)
            return QLurl, qltoken
        except Exception as e:
            raise Exception(f"获取Token失败: {str(e)}")

    except Exception as e:
        sender.reply(f"""=======网络错误=====
❌ 无法连接{'呆呆' if use_daidai else '青龙'}面板
------------------
请检查:
1. 面板是否运行
2. 网络是否正常
3. 配置是否正确
4. 错误信息: {str(e)}
------------------
当前配置:
• 地址: {QLurl if 'QLurl' in locals() else '未设置'}
• Key: {ClientID[:4] + '****' if 'ClientID' in locals() else '未设置'}
====================""")
        exit(0)

def QLtoken(QLurl, ClientID, ClientSecret):
    """获取青龙token"""
    try:
        url = f'{QLurl}/open/auth/token?client_id={ClientID}&client_secret={ClientSecret}'
        response = requests.get(url)

        if response.status_code != 200:
            sender.reply(f"""=======请求失败=====
❌ 青龙API请求失败
------------------
状态码: {response.status_code}
请检查:
• API地址是否正确
• 面板是否正常运行
====================""")
            exit(0)

        result = response.json()
        if "token" in result.get('data', {}):
            return result['data']['token']
        else:
            sender.reply("""=======认证失败=====
❌ 获取Token失败
------------------
请检查:
• ClientID是否正确
• ClientSecret是否正确
• 应用是否有权限
====================""")
            exit(0)

    except requests.exceptions.RequestException as e:
        sender.reply(f"""=======网络错误=====
❌ 连接青龙面板失败
------------------
请检查:
• 青龙地址是否正确
• 网络是否正常
• 错误信息: {str(e)}
====================""")
        exit(0)
    except Exception as e:
        sender.reply(f"""=======系统错误=====
❌ 处理请求时出错
------------------
请检查:
• 配置格式是否正确
• 错误信息: {str(e)}
====================""")
        exit(0)

def DDtoken(DDurl, AppKey, AppSecret):
    """获取呆呆面板token"""
    try:
        url = f'{DDurl}/api/open-api/token'
        response = requests.post(url, json={"app_key": AppKey, "app_secret": AppSecret})
        if response.status_code != 200:
            sender.reply("❌ 呆呆面板API请求失败")
            exit(0)
        result = response.json()
        access_token = result.get('data', {}).get('access_token')
        if access_token:
            return access_token
        sender.reply("❌ 获取呆呆面板Token失败")
        exit(0)
    except Exception as e:
        sender.reply(f"❌ 连接呆呆面板失败: {str(e)}")
        exit(0)

def QLzt(osname, value, account, phone):
    """添加青龙变量"""
    try:
        accountVip = '2099-12-31' or ''
        headers = {
            "Authorization": "Bearer" + ' ' + qltoken,
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        if use_daidai:
            data = {
                "value": value,
                "name": osname,
                "remarks": f'胖乖:{phone}丨用户:{userid}丨授权时间:{accountVip}丨胖乖管理'
            }
            if panel_group:
                data["group"] = panel_group
            r = requests.post(f"{QLurl}/api/envs", headers=headers, json=data)
            if r.status_code not in (200, 201):
                sender.reply("❌ 添加呆呆面板变量失败")
                exit(0)
            return
        else:
            qlurl = f"{QLurl}/open/envs"
            data = [{
                "value": value,
                "name": osname,
                "remarks": f'胖乖:{phone}丨用户:{userid}丨授权时间:{accountVip}丨胖乖管理'
            }]
            r = requests.post(qlurl, headers=headers, data=json.dumps(data))
            r_json = r.json()
            if "value must be unique" in r.text:
                return
            else:
                r_json['data'][0]['id']
                return
    except Exception as e:
        sender.reply(f"""=======添加失败=====
❌ 添加青龙变量失败
------------------
请检查:
• 青龙面板状态
• 变量格式是否正确
• 错误信息: {str(e)}
====================""")
        exit(0)

def QLupdate(osname, value, account, qlid, phone):
    """更新青龙变量"""
    try:
        accountVip = '2099-12-31' or ''
        headers = {
            "Authorization": "Bearer" + ' ' + qltoken,
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        if use_daidai:
            data = {
                "value": value,
                "name": osname,
                "remarks": f'胖乖:{phone}丨用户:{userid}丨授权时间:{accountVip}丨胖乖管理'
            }
            if panel_group:
                data["group"] = panel_group
            response = requests.put(f"{QLurl}/api/envs/{qlid}", headers=headers, json=data)
            if response.status_code == 200:
                return qlid, None
            sender.reply("❌ 更新呆呆面板变量失败")
            exit(0)
        else:
            qlurl = f"{QLurl}/open/envs"
            data = {
                "value": value,
                "name": osname,
                "remarks": f'胖乖:{phone}丨用户:{userid}丨授权时间:{accountVip}丨胖乖管理',
                "id": qlid
            }
            response = requests.put(qlurl, headers=headers, data=json.dumps(data))
            if response.status_code == 200:
                response_json = response.json()
                data = response_json['data']
                if data is None:
                    exit(0)
                return data['id'], data['createdAt']
            else:
                sender.reply("""=======更新失败=====
❌ 更新青龙变量失败
------------------
请稍后重试
====================""")
                exit(0)
    except Exception as e:
        sender.reply(f"""=======更新错误=====
❌ 更新变量时出错
------------------
错误信息: {str(e)}
====================""")
        exit(0)

def Addenvs(osname, value, account, phone):
    """添加或更新青龙变量"""
    try:
        qlid = None
        phone_qlid = None
        if use_daidai:
            headers = {
                "Authorization": "Bearer" + ' ' + qltoken,
                "accept": "application/json"
            }
            response = requests.get(url=f"{QLurl}/api/envs", headers=headers, params={"keyword": str(account), "page_size": 100}).json()
            envslist = response.get('data', [])
        else:
            url = f"{QLurl}/open/envs"
            headers = {
                "Authorization": "Bearer" + ' ' + qltoken,
                "accept": "application/json"
            }
            response = requests.get(url=url, headers=headers).json()
            if response['code'] != 200:
                sender.reply("""=======连接失败=====
❌ 连接青龙获取变量失败
====================""")
                exit(0)
            envslist = response['data']

        for envs in envslist:
            remarks = envs.get('remarks')
            envname = envs.get('name')
            if not remarks or envname != osname:
                continue

            if account in remarks:
                qlid = envs['id']
                break

            if '胖乖:' in remarks:
                try:
                    remark_phone = remarks.split('胖乖:')[1].split('丨')[0]
                    if remark_phone == phone:
                        phone_qlid = envs['id']
                except:
                    continue

        if not qlid and phone_qlid:
            qlid = phone_qlid

        value = urllib.parse.quote(value)
        if qlid:
            QLupdate(osname, value, account, qlid, phone)
        else:
            QLzt(osname, value, account, phone)
    except Exception as e:
        sender.reply(f"""=======操作失败=====
❌ 处理变量时出错
------------------
错误信息: {str(e)}
====================""")
        exit(0)

def times13():
    """生成13位时间戳"""
    timestamp = time.time()
    return int(timestamp * 1000)

def calculate_sha2562(timestamp_ms, token, url):
    """计算SHA256签名"""
    parsed_url = urlparse(url)
    path = parsed_url.path
    data = f'appSecret=&channel=alipay&timestamp={timestamp_ms}&token={token}&version=1.57.0&{path}'
    sha256_hash = hashlib.sha256()
    sha256_hash.update(data.encode('utf-8'))
    return sha256_hash.hexdigest()

def login(token):
    """登录验证token"""
    try:
        url = "https://userapi.qiekj.com/user/info"
        timestamp_ms = times13()
        sign = calculate_sha2562(timestamp_ms, token, url)
        payload = f"token={token}"

        headers = {
            'User-Agent': "okhttp/3.14.9",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'Content-Type': "application/x-www-form-urlencoded",
            'Authorization': f"{token}",
            'Version': "1.57.0",
            'channel': "android_app",
            'phoneBrand': "meizu",
            'timestamp': f"{timestamp_ms}",
            'sign': f"{sign}",
        }

        response = requests.post(url, data=payload, headers=headers)
        if '成功' in response.text:
            r = response.json()
            phone = r['data']['phone']
            display_phone = phone[:3] + '*' * 4 + phone[7:]
            account = r['data']['id']
            return phone, str(account), display_phone
        else:
            return 'Token失效', 'Token失效', 'Token失效'
    except Exception as e:
        sender.reply(f"""=======登录失败=====
❌ 验证Token失败
------------------
错误信息: {str(e)}
====================""")
        exit(0)

def sms(phone):
    """发送验证码"""
    try:
        url = "https://userapi.qiekj.com/common/sms/sendCode"
        timestamp_ms = times13()
        sign = calculate_sha2562(timestamp_ms, '', url)
        payload = f"phone={phone}&template=reg"

        headers = {
            'User-Agent': "okhttp/3.14.9",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'Content-Type': "application/x-www-form-urlencoded",
            'Authorization': "",
            'Version': "1.57.0",
            'channel': "android_app",
            'phoneBrand': "meizu",
            'timestamp': f"{timestamp_ms}",
            'sign': f"{sign}",
        }

        response = requests.post(url, data=payload, headers=headers)
        result = response.json()

        if result.get('code') == 0 and result.get('msg') == '成功':
            return True
        else:
            error_msg = result.get('msg', '未知错误')
            sender.reply(f"""=======发送失败=====
❌ 获取验证码失败
------------------
错误信息: {error_msg}
====================""")
            exit(0)

    except Exception as e:
        sender.reply(f"""=======请求失败=====
❌ 发送验证码失败
------------------
错误信息: {str(e)}
====================""")
        exit(0)

def smslogin(phone, code):
    """短信验证码登录"""
    if len(code) != 4:
        sender.reply("""=======验证码错误=====
❌ 请输入正确的4位验证码
====================""")
        exit(0)

    try:
        url = "https://userapi.qiekj.com/user/reg"
        timestamp_ms = times13()
        sign = calculate_sha2562(timestamp_ms, '', url)
        payload = f"channel=h5&phone={phone}&verify={code}"
        headers = {
            'User-Agent': "okhttp/3.14.9",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'Content-Type': "application/x-www-form-urlencoded",
            'Authorization': "",
            'Version': "1.57.0",
            'channel': "android_app",
            'phoneBrand': "meizu",
            'timestamp': f"{timestamp_ms}",
            'sign': f"{sign}"
        }
        response = requests.post(url, data=payload, headers=headers)
        if '成功' in response.text:
            r = response.json()
            token = r['data']['token']
            phone, account, display_phone = login(token)
            if phone == 'Token失效':
                sender.reply("""=======登录失败=====
❌ 登录验证失败
====================""")
                exit(0)
            else:
                return phone, account, token, display_phone
        else:
            sender.reply("""=======登录失败=====
❌ 登录请求失败
====================""")
            exit(0)
    except Exception as e:
        sender.reply(f"""=======系统错误=====
❌ 登录处理失败
------------------
错误信息: {str(e)}
====================""")
        exit(0)

def bind():
    """绑定账号"""
    def accvip(Newaddition):
        '添加' if Newaddition else '更新'
        auth_status = '✅ 已授权' if accountVip >= today_time else '⚠️ 未授权'
        next_step = f'发送 {randommanagecommand} 可管理账号' if accountVip >= today_time else f'发送 {randommanagecommand} 可进行授权'

        success_msg = f"""=======绑定成功=====
📱 账号: {display_phone}
🔐 状态: {auth_status}
⏰ 操作: {next_step}
===================="""

        if len(accountVip) != 0 and accountVip >= today_time:
            Addenvs(osname=dd_pg_osname, value=token, account=account, phone=phone)

        if account not in accounts:
            accounts.append(account)
            unique_accounts = list(dict.fromkeys(accounts))
            sg.bucketSet(bucket='dd_pg_user', key=userid, value=f'{unique_accounts}')

        sender.reply(success_msg)

    sender.reply("""=======胖乖登录=====
请输入手机号:
------------------
回复"q"退出操作
====================""")
    input_phone = sender.input(120000, 1, False)

    if input_phone.lower() == 'q':
        sender.reply("✅ 已取消登录")
        exit(0)

    if not input_phone.isdigit() or len(input_phone) != 11:
        sender.reply("""=======格式错误=====
❌ 请输入正确的11位手机号
====================""")
        exit(0)

    old_auth = None
    accounts = []
    if len(uservalue) != 0:
        accounts = _sg_literal(uservalue)
        for acc in accounts:
            acc_phone = sg.bucketGet(bucket='dd_pg_mobile', key=acc)
            if acc_phone == input_phone:
                old_auth = '2099-12-31' or ''
                accounts.remove(acc)
                sg.bucketDel(bucket='dd_pg_mobile', key=acc)
                sg.bucketDel(bucket='dd_pg_token', key=acc)
                qlid = allenvs(osname=dd_pg_osname, account=acc)
                if qlid:
                    delenvs(id=qlid)
                break

    sms(input_phone)
    sender.reply("""=======验证码登录=====
请输入收到的4位验证码:
------------------
回复"q"退出操作
====================""")
    code = sender.input(120000, 1, False)

    if code.lower() == 'q':
        sender.reply("✅ 已取消登录")
        exit(0)

    phone, account, token, display_phone = smslogin(input_phone, code)

    sg.bucketSet(bucket='dd_pg_mobile', key=account, value=phone)
    sg.bucketSet(bucket='dd_pg_token', key=account, value=token)

    if old_auth:
        True
        if old_auth >= today_time:
            Addenvs(osname=dd_pg_osname, value=token, account=account, phone=phone)

    if len(uservalue) == 0:
        accounts = []

    accountVip = '2099-12-31' or ''
    accvip(True)  # 添加新账号

def ValueErrors(value, count):
    """验证输入值是否为有效的整数且在合理范围内"""
    try:
        value = int(value)
        if value > count or value == 0:
            sender.reply(f"""=======输入无效=====
❌ 请输入 1-{count} 之间的数字
====================""")
            exit(0)
        return value
    except ValueError:
        sender.reply("""=======输入无效=====
❌ 请输入正确的数字
====================""")
        exit(0)

def empower(empowertime, me_as_int):
    """授权时间计算"""
    day = me_as_int * 30
    try:
        if len(empowertime) == 0:
            delayed_date = today_date + timedelta(days=day)
        else:
            empower_date = datetime.strptime(empowertime, "%Y-%m-%d").date()
            if empower_date <= today_date:
                delayed_date = today_date + timedelta(days=day)
            else:
                delayed_date = empower_date + timedelta(days=day)

        return str(delayed_date)
    except Exception as e:
        print(f"授权时间计算出错: {str(e)}")
        return str(today_date + timedelta(days=day))

def management():
    """账号管理功能"""
    if len(uservalue) == 0:
        sender.reply(f"""=======未绑定账号=====
❌ 未找到任何账号信息
💡 发送 {randomsigncommand} 绑定
====================""")
        return

    count = 1
    account_list = """
======我的胖乖账号====="""

    accounts = list(dict.fromkeys(_sg_literal(uservalue))) if uservalue else []
    sg.bucketSet(bucket='dd_pg_user', key=userid, value=f'{accounts}')

    for account in accounts:
        accountVip = '2099-12-31' or ''
        if len(accountVip) == 0:
            vip_status = '⚠️ 未授权'
        elif accountVip < today_time:
            vip_status = '❌ 已过期'
        else:
            vip_status = f'✅ {accountVip}'

        phone = sg.bucketGet(bucket='dd_pg_mobile', key=account)
        if phone:
            display_phone = phone[:3] + '*' * 4 + phone[7:]
        else:
            display_phone = account[:3] + "****" + account[7:]

        account_list += f"""
------------------
[{count}] 账号信息
📱 账号: {display_phone}
🔐 授权: {vip_status}"""
        count += 1

    account_list += """
==================
回复数字选择账号
回复"q"退出操作
=================="""

    sender.reply(account_list)

    inputmessage = sender.input(120000, 1, False)
    if inputmessage == 'timeout':
        sender.reply('⏰ 操作超时,已退出')
        exit(0)
    elif inputmessage == 'q':
        sender.reply('✅ 已退出管理')
        exit(0)

    try:
        me_as_int = int(inputmessage)
        if me_as_int > count:
            sender.reply('❌ 输入的序号无效')
            exit(0)
    except ValueError:
        sender.reply('❌ 输入必须是数字')
        exit(0)

    account = accounts[me_as_int - 1]
    token = sg.bucketGet(bucket='dd_pg_token', key=f'{account}')
    accountVip = '2099-12-31' or ''
    phone, account_status, display_phone = login(token)

    if len(accountVip) == 0:
        vip_status = '⚠️ 未授权'
    elif accountVip < today_time:
        vip_status = '❌ 已过期'
    else:
        vip_status = f'✅ {accountVip}'

    account_info = f"""
=======账号详情======
📱 账号: {display_phone}
🔐 授权: {vip_status}
=================="""
    sender.reply(account_info)

    menu = """
=======账号管理======
[1] 授权账号
[2] 删除账号
------------------
回复数字选择功能
回复"q"退出操作
=================="""
    sender.reply(menu)

    inputmessage = sender.input(120000, 1, False)
    if inputmessage == '2':
        confirm_msg = """=======删除警告=====
❌ 确定要删除该账号吗？
------------------
此操作不可恢复！
[y] 确认删除
[n] 取消操作
===================="""
        sender.reply(confirm_msg)

        yesorno = sender.input(120000, 1, False)
        if yesorno.lower() in ['y', '是']:
            accounts.remove(str(account))
            qlid = allenvs(osname=dd_pg_osname, account=str(account))
            delenvs(id=qlid)
            if len(accounts) == 0:
                sg.bucketDel(bucket='dd_pg_user', key=userid)
            else:
                sg.bucketSet(bucket='dd_pg_user', key=userid, value=f'{accounts}')
            sender.reply('✅ 账号删除成功!')
        else:
            sender.reply('✅ 已取消删除')
            exit(0)

    elif inputmessage == '1':
        auth_guide = """=======授权设置=====
请输入授权月数(如:1)
------------------
回复数字设置月数
回复"q"退出操作
===================="""
        sender.reply(auth_guide)

        mes = sender.input(120000, 1, False)
        if mes.lower() == 'q':
            sender.reply("✅ 已取消授权")
            exit(0)

        mes = ValueErrors(value=mes, count=999)
        money = Decimal(mes) * Decimal(pgVipmoney)

        zf(project='胖乖授权', me_as_int=mes, accountVip=accountVip, token=token,
           phone=phone, account=account)

        accountVip = empower(empowertime=accountVip, me_as_int=mes)
        True
        Addenvs(osname=dd_pg_osname, value=token, account=account, phone=phone)

        result_msg = f"""=======订单完成=====
🎈 名称: 胖乖授权
🎉 数量: {mes} 个月
💰 金额: {money} 元
===================="""
        sender.reply(result_msg)

    elif inputmessage.lower() == 'q':
        sender.reply('✅ 已退出管理')
        exit(0)
    else:
        sender.reply('❌ 输入无效')
        exit(0)

def yesornos():
    """确认操作"""
    yesorno = sender.input(120000, 1, False)
    if yesorno.lower() in ['y', '是']:
        return True
    elif yesorno.lower() in ['n', '否']:
        return False
    elif yesorno == '':
        sender.reply('⏰ 输入超时！')
        exit(0)
    elif yesorno.lower() in ['q', '退出']:
        sender.reply('✅ 已退出!')
        exit(0)
    else:
        sender.reply('❌ 输入错误！')
        exit(0)

def zf(project, me_as_int, accountVip, token, phone, account):
    """支付处理"""
    try:
        zsm = sg.bucketGet('dd_pg_config', 'zsm')
        use_ma_pay = '2099-12-31' == 'true'

        if not zsm and not use_ma_pay:
            sender.reply('❌ 未配置收款方式,请检查配置!')
            exit(0)

        usercoin = sg.bucketGet('dd_sign_points', userid) or '0'
        zfcoin = int(pgcoin) * me_as_int

        pay_menu = """=====选择支付方式===="""

        if zsm:
            money = Decimal(me_as_int) * Decimal(pgVipmoney)
            pay_menu += f"""
1️⃣ 微信支付
   💰 {money}元/{me_as_int}月"""

        if use_ma_pay:
            ma_pay_config = {
                'switch': '2099-12-31' or 'false',
                'gateway': '2099-12-31',
                'pid': '2099-12-31',
                'key': '2099-12-31',
                'type': '2099-12-31',
                'notify_url': '2099-12-31',
                'return_url': '2099-12-31'
            }

            if ma_pay_config['switch'].lower() == 'true' and all([ma_pay_config['gateway'], ma_pay_config['pid'], ma_pay_config['key']]):
                money = Decimal(me_as_int) * Decimal(pgVipmoney)
                pay_menu += f"""
2️⃣ 在线处理
   💰 {money}元/{me_as_int}月"""

        if pgcoin and int(pgcoin) > 0:
            pay_menu += f"""
3️⃣ 积分支付
   🎯 {zfcoin}积分/{me_as_int}月
   💫 当前积分: {usercoin}"""

        pay_menu += """
------------------
回复数字选择方式
回复"q"退出操作
=================="""

        sender.reply(pay_menu)
        choice = sender.input(60000, 1, False)

        if choice == 'q' or choice == 'Q':
            sender.reply("✅ 已取消支付")
            exit(0)

        elif choice == '1' and zsm:
            zfzt = False
            if zfzt:
                sender.reply('⚠️ 当前有人正在支付,请稍后再试！')
                exit(0)

            money = Decimal(me_as_int) * Decimal(pgVipmoney)

            pay_msg = f"""=====微信扫在线处理====
🎫 商品: {project}
📅 时长: {me_as_int}月
💰 金额: {money}元
------------------
请使用微信扫在线处理
回复"q"取消支付
=================="""
            sender.reply(pay_msg)
            sender.replyImage(zsm)

            ddzf = False

            if str(ddzf) == 'q':
                sender.reply('✅ 已取消支付')
                exit(0)

            try:
                if isinstance(ddzf, dict):
                    if ddzf.get('Type') == '微信赞赏':
                        Money = float(ddzf.get('Money', 0))
                        ddzf.get('Time', '').split('.')[0].replace('T', ' ')
                        From = ddzf.get('FromName', '')
                    elif ddzf.get('Type') == '微信收款':
                        Money = float(ddzf.get('Money', 0))
                        ddzf.get('Time', '').split('.')[0].replace('T', ' ')
                        From = ddzf.get('FromName', '')
                    elif ddzf.get('Money'):
                        Money = float(ddzf.get('Money', 0))
                        ddzf.get('Time', '').replace('T', ' ').split('.')[0]
                        From = ddzf.get('FromName', '')
                    elif ddzf.get('money'):
                        Money = float(ddzf.get('money', 0))
                        ddzf.get('time', '').replace('T', ' ').split('.')[0]
                        From = ddzf.get('fromName', '')
                    else:
                        sender.reply('不支持的支付消息格式')
                        exit(0)
                else:
                    try:
                        ddzf = json.loads(ddzf)
                        if ddzf.get('Type') == '微信赞赏':
                            Money = float(ddzf.get('Money', 0))
                            ddzf.get('Time', '').split('.')[0].replace('T', ' ')
                            From = ddzf.get('FromName', '')
                        elif ddzf.get('Type') == '微信收款':
                            Money = float(ddzf.get('Money', 0))
                            ddzf.get('Time', '').split('.')[0].replace('T', ' ')
                            From = ddzf.get('FromName', '')
                        else:
                            Money = float(ddzf.get('Money', 0))
                            ddzf.get('Time', '').replace('T', ' ').split('.')[0]
                            From = ddzf.get('FromName', '')
                    except:
                        if "二维码赞赏到账" in str(ddzf):
                            try:
                                amount = str(ddzf).split("收款金额￥")[1].split("\n")[0]
                                time = str(ddzf).split("到账时间")[1].split("\n")[0]
                                Money = float(amount)
                                time.strip()
                                From = ''
                            except Exception as e:
                                sender.reply(f"❌ 解析收款信息失败: {str(e)}")
                                exit(0)
                        else:
                            sender.reply("❌ 无法解析支付结果")
                            exit(0)

                if float(Money) >= float(money):
                    return True
                else:
                    sender.reply(f"""=====支付金额错误=====
💰 应付: {money}元
💳 实付: {Money}元
{f'👤 付款人: {From}' if From else ''}

❗ 请稍后核对支付记录！
==================""")
                    exit(0)
            except Exception as e:
                sender.reply(f"❌ 处理支付结果时出错: {str(e)}")
                exit(0)

        elif choice == '2' and use_ma_pay:
            money = Decimal(me_as_int) * Decimal(pgVipmoney)

            out_trade_no = f"PG{int(time.time())}{userid}"

            params = {
                'pid': ma_pay_config['pid'],
                'type': ma_pay_config['type'].split(',')[0],  # 默认使用第一个支付方式
                'out_trade_no': out_trade_no,
                'name': f"{senderID}-胖乖授权-{str(money)}",
                'money': str(money),
                'notify_url': ma_pay_config['notify_url'],
                'return_url': ma_pay_config['return_url'],
                'param': userid  # 传递用户ID作为附加参数
            }

            sorted_params = sorted(params.items(), key=lambda x: x[0])

            sign_str = "&".join([f"{k}={v}" for k, v in sorted_params])

            sign = hashlib.md5((sign_str + ma_pay_config['key']).encode()).hexdigest().lower()

            params['sign'] = sign
            params['sign_type'] = 'MD5'

            gateway = ma_pay_config['gateway']
            if not gateway.endswith('/'):
                gateway += '/'
            submit_url = gateway + 'submit.php'

            try:
                response = requests.post(submit_url, data=params)
                if 'location.href' in response.text:
                    match = re.search(r'location\.href\s*=\s*[\'"](.*?)[\'"]', response.text)
                    if match:
                        pay_url = match.group(1)
                        if not pay_url.startswith('http'):
                            pay_url = gateway + pay_url

                        sender.reply(f"""=====在线处理=====
🎫 商品: {project}
💰 金额: {money}元
⏰ 有效期: 5分钟
------------------
请点击链接完成支付:
{pay_url}
==================""")

                        for _ in range(60):  # 最多等待5分钟
                            time.sleep(5)
                            check_url = gateway + 'api.php'
                            check_params = {
                                'act': 'order',
                                'pid': ma_pay_config['pid'],
                                'key': ma_pay_config['key'],
                                'out_trade_no': out_trade_no
                            }

                            try:
                                check_resp = requests.get(check_url, params=check_params)
                                result = check_resp.json()

                                if result.get('code') == 1:  # 支付成功
                                    return True
                            except:
                                continue

                        sender.reply("❌ 支付超时,请重新发起支付!")
                        exit(0)
                else:
                    sender.reply("❌ 创建支付订单失败!")
                    exit(0)
            except Exception as e:
                sender.reply(f"❌ 支付请求失败: {str(e)}")
                exit(0)

        elif choice == '3' and pgcoin != 0:
            if int(usercoin) < zfcoin:
                sender.reply(f"""=====积分不足=====
👤 当前积分: {usercoin}
📍 需要积分: {zfcoin}
==================""")
                exit(0)

            confirm_msg = f"""=====积分支付确认=====
💫 消耗积分: {zfcoin}
⏰ 授权时长: {me_as_int}月
------------------
确认请回复【y】
取消请回复【n】
=================="""
            sender.reply(confirm_msg)

            if yesornos():
                try:
                    new_balance = int(usercoin) - zfcoin
                    sg.bucketSet('dd_sign_points', userid, str(new_balance))
                    return True
                except Exception as e:
                    sender.reply(f"❌ 积分支付处理失败: {str(e)}")
                    exit(0)
            else:
                sender.reply("✅ 已取消支付")
                exit(0)
        else:
            sender.reply("❌ 输入无效")
            exit(0)

    except Exception as e:
        sender.reply(f"❌ 支付处理发生错误: {str(e)}")
        exit(0)

def cx(token):
    """查询账号信息"""
    try:
        url = "https://userapi.qiekj.com/user/balance"
        timestamp_ms = times13()
        sign = calculate_sha2562(timestamp_ms, token, url)
        payload = f"token={token}"

        headers = {
            'User-Agent': "okhttp/3.14.9",
            'Authorization': token,
            'Version': "1.57.0",
            'channel': "android_app",
            'timestamp': str(timestamp_ms),
            'sign': sign,
            'Content-Type': "application/x-www-form-urlencoded"
        }

        response = requests.post(url, data=payload, headers=headers)
        if '成功' in response.text:
            balance_data = response.json()['data']

            h = {
                'User-Agent': 'okhttp/3.14.9',
                'Accept': 'application/json, text/plain, */*',
                'channel': 'android_app',
                'Authorization': token,
                'Version': '1.57.0'
            }
            data = {
                'page': (None, '1'),
                'pageSize': (None, '100'),
                'type': (None, '100'),
                'receivedStatus': (None, '1'),
                'token': (None, token),
            }
            integral_response = requests.post(
                'https://userapi.qiekj.com/integralRecord/pageList',
                headers=h,
                files=data
            ).json()

            current_date = datetime.now().strftime('%Y-%m-%d')
            today_integral = 0
            for item in integral_response['data']['items']:
                received_date = item['receivedTime'][:10]
                if received_date == current_date:
                    today_integral += item['amount']

            return {
                'balance': balance_data['balance'],
                'integral': balance_data['integral'],
                'today_integral': today_integral
            }
        return None
    except:
        return None

def cxs():
    """查询所有账号"""
    if len(uservalue) == 0:
        sender.reply(f"""=======未绑定账号=====
❌ 未找到任何账号信息
💡 发送 {randomsigncommand} 绑定
====================""")
        return

    accounts = list(dict.fromkeys(_sg_literal(uservalue))) if uservalue else []
    sg.bucketSet(bucket='dd_pg_user', key=userid, value=f'{accounts}')

    for account in accounts:
        token = sg.bucketGet(bucket='dd_pg_token', key=account)
        accountVip = '2099-12-31' or ''
        phone = sg.bucketGet(bucket='dd_pg_mobile', key=account)

        if len(accountVip) == 0 or accountVip < today_time:
            sender.reply(f"""=======授权过期=====
📱 账号: {phone[:3]}****{phone[7:]}
⚠️ 状态: 授权已过期
====================""")
            continue

        info = cx(token)
        if not info:
            sender.reply(f"""=======查询异常=====
📱 账号: {phone[:3]}****{phone[7:]}
❌ 状态: 查询失败
====================""")
            continue

        account_info = f"""=======账号详情=====
📱 账号: {phone[:3]}****{phone[7:]}
🎯 总积分: {info['integral']}
📈 今日积分: {info['today_integral']}
🔐 授权至: {accountVip}
===================="""
        sender.reply(account_info)

def push(user, account, message):
    """推送通知"""
    phone = sg.bucketGet(bucket='dd_pg_mobile', key=account)
    if not phone:
        return

    phone = phone[:3] + "****" + phone[7:]
    push_msg = f"""=======账号通知=====
📱 账号: {phone}
📢 消息: {message}
===================="""

    accountlist = sg.bucketGet('dd_pg_user', user)
    if accountlist:
        accounts = list(dict.fromkeys(_sg_literal(accountlist)))
        sg.bucketSet(bucket='dd_pg_user', key=user, value=f'{accounts}')

    sg.push('wb', '', user, '', push_msg)
    sg.push('tg', '', user, '', push_msg)
    sg.push('qq', '', user, '', push_msg)
    sg.push('qb', '', user, '', push_msg)
    sg.push('wx', '', user, '', push_msg)

def pangguai_auth():
    return True

def allenvs(osname, account):
    """查询青龙变量"""
    try:
        headers = {
            "Authorization": "Bearer" + ' ' + qltoken,
            "accept": "application/json"
        }
        if use_daidai:
            response = requests.get(url=f"{QLurl}/api/envs", headers=headers, params={"keyword": str(account), "page_size": 100}).json()
            for env in response.get('data', []):
                if env.get('remarks') and account in env['remarks'] and osname == env.get('name'):
                    return env['id']
        else:
            url = f"{QLurl}/open/envs"
            response = requests.get(url=url, headers=headers).json()

            if response['code'] == 200:
                for env in response['data']:
                    if env['remarks'] and account in env['remarks'] and osname == env['name']:
                        return env['id']
        return None

    except Exception as e:
        sender.reply(f"""=======查询失败=====
❌ 查询变量时出错
------------------
错误信息: {str(e)}
====================""")
        exit(0)

def delenvs(id):
    """删除青龙变量"""
    if not id:
        return

    try:
        headers = {
            "Authorization": "Bearer" + ' ' + qltoken,
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        if use_daidai:
            response = requests.delete(f"{QLurl}/api/envs/{id}", headers=headers)
            if response.status_code != 200:
                sender.reply("❌ 删除呆呆面板变量失败")
        else:
            url = f"{QLurl}/open/envs"
            data = [id]
            response = requests.delete(url, headers=headers, json=data)

            if response.status_code != 200:
                sender.reply("""=======删除失败=====
❌ 删除变量失败
------------------
请检查青龙面板状态
====================""")

    except Exception as e:
        sender.reply(f"""=======删除错误=====
❌ 删除变量时出错
------------------
错误信息: {str(e)}
====================""")
        exit(0)

def clean_expired_accounts():
    """清理过期账号"""
    if not sender.isAdmin():
        sender.reply("""=======权限错误=====
⛔ 您没有权限执行此操作
====================""")
        return

    dd_pg_osname, dd_pg_qlname, _, _, _, _, _, _, _, _, _, _, _ = getusercontent()
    QLurl, qltoken = seekql()

    sender.reply("""=======清理确认=====
⚠️ 即将清理所有过期账号
⚠️ 此操作不可恢复
------------------
[y] 确认清理
[n] 取消操作
====================""")

    if not yesornos():
        sender.reply("✅ 已取消清理")
        return

    users = sg.bucketAllKeys(bucket='dd_pg_user')
    if not users:
        sender.reply("""=======查询结果=====
ℹ️ 没有找到任何用户
====================""")
        return

    total_accounts = 0
    expired_accounts = 0
    cleaned_accounts = 0
    cleaned_vars = 0

    try:
        url = f"{QLurl}/open/envs"
        headers = {
            "Authorization": "Bearer" + ' ' + qltoken,
            "accept": "application/json"
        }
        response = requests.get(url=url, headers=headers).json()
        if response['code'] != 200:
            sender.reply("""=======查询失败=====
❌ 无法获取青龙变量
------------------
请检查青龙面板状态
====================""")
            return
        all_envs = response['data']
    except Exception as e:
        sender.reply(f"""=======查询错误=====
❌ 获取青龙变量失败
------------------
错误信息: {str(e)}
====================""")
        return

    env_ids_to_delete = []

    for user in users:
        accountlist = sg.bucketGet('dd_pg_user', user)
        if not accountlist:
            continue

        accounts = list(dict.fromkeys(_sg_literal(accountlist))) if accountlist else []
        valid_accounts = []

        for account in accounts:
            total_accounts += 1
            accountVip = '2099-12-31' or ''

            if len(accountVip) == 0 or accountVip < today_time:
                expired_accounts += 1
                phone = sg.bucketGet('dd_pg_mobile', key=account)

                for env in all_envs:
                    if env['name'] == dd_pg_osname:
                        remarks = env.get('remarks', '')
                        if (account in remarks) or (phone and phone in remarks):
                            env_ids_to_delete.append(env['id'])
                            cleaned_vars += 1

                cleaned_accounts += 1
                sg.bucketDel(bucket='dd_pg_mobile', key=account)
                sg.bucketDel(bucket='dd_pg_token', key=account)
                True
            else:
                valid_accounts.append(account)

        if valid_accounts:
            sg.bucketSet(bucket='dd_pg_user', key=user, value=f'{valid_accounts}')
        else:
            sg.bucketDel(bucket='dd_pg_user', key=user)

    if env_ids_to_delete:
        try:
            url = f"{QLurl}/open/envs"
            headers = {
                "Authorization": "Bearer" + ' ' + qltoken,
                "accept": "application/json",
                "Content-Type": "application/json"
            }
            response = requests.delete(url, headers=headers, json=env_ids_to_delete)
            if response.status_code != 200:
                sender.reply("""=======删除失败=====
❌ 删除青龙变量失败
------------------
请检查青龙面板状态
====================""")
        except Exception as e:
            sender.reply(f"""=======删除错误=====
❌ 删除青龙变量时出错
------------------
错误信息: {str(e)}
====================""")
            return

    result_msg = f"""=======清理完成=====
📊 统计信息:
• 总账号数: {total_accounts}
• 过期账号: {expired_accounts}
• 清理账号: {cleaned_accounts}
• 清理变量: {cleaned_vars}
===================="""
    sender.reply(result_msg)

dd_pg_osname, dd_pg_qlname, dd_managecommand, dd_querycommand, \
dd_signcommand, randommanagecommand, randomquerycommand, \
randomsigncommand, pgVipmoney, pgcoin, use_daidai, dd_pg_ddname, panel_group = getusercontent()

QLurl, qltoken = seekql()

today_date = datetime.now().date()
today_time = str(today_date)

imtype = sender.getImtype()
usermessage = sender.getMessage()

if '登录' in usermessage or '登陆' in usermessage:
    bind()
elif '管理' in usermessage:
    management()
elif '查询' in usermessage:
    cxs()
elif usermessage.strip() == '胖乖授权':
    try:
        pangguai_auth()
    except Exception as e:
        sender.reply(f"""=======系统错误=====
❌ 执行授权功能时出错
------------------
错误信息: {str(e)}
====================""")
elif usermessage.strip() in ['胖乖清理', '清理胖乖']:
    try:
        clean_expired_accounts()
    except Exception as e:
        sender.reply(f"""=======系统错误=====
❌ 执行清理功能时出错
------------------
错误信息: {str(e)}
====================""")
elif imtype == 'fake':
    users = sg.bucketAllKeys(bucket='dd_pg_user')
    for user in users:
        accountlist = sg.bucketGet(bucket='dd_pg_user', key=user)
        if not accountlist:
            continue

        accounts = list(dict.fromkeys(_sg_literal(accountlist))) if accountlist else []
        sg.bucketSet(bucket='dd_pg_user', key=user, value=f'{accounts}')

        for account in accounts:
            token = sg.bucketGet(bucket='dd_pg_token', key=account)
            accountVip = '2099-12-31' or ''

            info = cx(token)
            if not info:
                qlid = allenvs(osname=dd_pg_osname, account=account)
                delenvs(id=qlid)

                push(user, account, """=======胖乖定时检测=====
⏰ 定时检测提醒
------------------
❌ Token已失效
💡 请尽快更新账号
====================""")
                continue

            if len(accountVip) == 0 or accountVip <= today_time:
                qlid = allenvs(osname=dd_pg_osname, account=account)
                delenvs(id=qlid)
                push(user, account, """=======胖乖定时检测=====
⏰ 定时检测提醒
------------------
❌ 授权已过期
💡 请及时续费授权
====================""")
            else:
                try:
                    expire_date = datetime.strptime(accountVip, '%Y-%m-%d').date()
                    days_left = (expire_date - datetime.now().date()).days
                    if days_left <= 3:
                        push(user, account, f"""=======胖乖定时检测=====
⏰ 定时检测提醒
------------------
⚠️ 授权即将到期
📅 到期时间: {accountVip}
⏳ 剩余天数: {days_left}天
💡 请及时续费授权
====================""")
                except:
                    pass
else:
    sender.setContinue()
