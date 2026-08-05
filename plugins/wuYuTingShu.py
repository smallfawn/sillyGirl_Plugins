# [title: 唔语听书]
# [name: wuYuTingShu]
# [language: python]
# [class: 任务]
# [author: 97610325]
# [version: V2.3]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^唔语管理$|^管理唔语$|^唔语查询$|^查询唔语$|^唔语登录$|^登录唔语$|^登陆唔语$|^唔语登陆$|^唔语$|^唔语清理$|^清理唔语$]
# [cron: 18 8,12,16 * * *]
# [icon: https://nos.netease.com/ysf/d4f8b7f99ae2b9ffb33ebfdedcf0776c.jpg]
# [description: 唔语听书插件；指令：唔语登录、唔语管理、唔语查询、唔语清理；功能：自动领红花、每日抽奖、自动看广告，完美对接青龙面板,适配呆呆系统系统]
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
    'dd_wuyu_config_Qinglong': form.string().title('设置对接容器').default('').description('你的变量需要添加到的容器？参数用丨分割，这个符号是中文的竖(直接复制)'),
    'dd_wuyu_config_osname': form.string().title('青龙变量名').default('').description('青龙容器内唔语听书的变量名'),
})
_CONFIG_FIELD_MAP = {
    ('dd_wuyu_config', 'Qinglong'): 'dd_wuyu_config_Qinglong',
    ('dd_wuyu_config', 'osname'): 'dd_wuyu_config_osname',
}

import time
import requests
import hashlib
import json
from datetime import datetime, timedelta
from decimal import Decimal
import urllib.parse
import re
def normalize_token(token):
    """标准化Token,自动处理Bearer前缀

    Args:
        token: 原始Token字符串,可能包含Bearer前缀

    Returns:
        str: 标准化后的Token(不包含Bearer前缀)
    """
    if not token:
        return ''

    token = str(token).strip()

    if token.lower().startswith('bearer '):
        token = token[7:]

    return token
senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()
uservalue = sg.bucketGet(bucket='dd_wuyu_user', key=userid)
def getusercontent():
    """获取插件配置信息"""
    dd_wuyu_osname = sg.bucketGet('dd_wuyu_config', 'osname') or 'WuyuToken'
    dd_wuyu_qlname = sg.bucketGet('dd_wuyu_config', 'Qinglong')
    dd_managecommand = sg.bucketGet('dd_wuyu_config', 'dd_managecommand') or '唔语管理'
    dd_querycommand = sg.bucketGet('dd_wuyu_config', 'dd_querycommand') or '唔语查询'
    dd_signcommand = sg.bucketGet('dd_wuyu_config', 'dd_signcommand') or '唔语登录'

    randommanagecommand = dd_managecommand
    randomquerycommand = dd_querycommand
    randomsigncommand = dd_signcommand

    WuyuVipmoney = Decimal(sg.bucketGet('dd_wuyu_config', 'WuyuVipmoney') or '0')
    Wuyucoin = int(sg.bucketGet('dd_wuyu_config', 'Wuyucoin') or '0')

    return (dd_wuyu_osname, dd_wuyu_qlname, dd_managecommand, dd_querycommand,
            dd_signcommand, randommanagecommand, randomquerycommand,
            randomsigncommand, WuyuVipmoney, Wuyucoin)
def seekql():
    """连接并验证青龙配置"""
    try:
        if len(dd_wuyu_qlname) == 0:
            sender.reply("""=======配置错误=======
❌ 未配置青龙信息
------------------
请在插件配置中填写:
Host丨ClientID丨ClientSecret
• 使用中文丨分隔
• 示例:
http://ql.example.com丨abcd丨1234
====================""")
            exit(0)

        qllist = dd_wuyu_qlname.split('丨')
        if len(qllist) != 3:
            sender.reply(f"""=======格式错误=======
❌ 青龙配置格式错误
------------------
当前格式: {dd_wuyu_qlname}
正确格式:
Host丨ClientID丨ClientSecret
====================""")
            exit(0)

        QLurl = qllist[0].strip()
        ClientID = qllist[1].strip()
        ClientSecret = qllist[2].strip()

        if not all([QLurl, ClientID, ClientSecret]):
            sender.reply("""=======参数错误=======
❌ 青龙配置参数不完整
------------------
请确保以下参数都已填写:
• 青龙面板地址(Host)
• 应用ID(ClientID)
• 应用密钥(ClientSecret)
====================""")
            exit(0)

        if not QLurl.startswith(('http://', 'https://')):
            sender.reply(f"""=======地址错误=======
❌ 青龙地址格式错误
------------------
当前地址: {QLurl}
正确格式:
• http://qinglong.example.com
• https://ql.example.com:5700
====================""")
            exit(0)

        try:
            qltoken = QLtoken(QLurl=QLurl, ClientID=ClientID, ClientSecret=ClientSecret)
            return QLurl, qltoken
        except Exception as e:
            raise Exception(f"获取Token失败: {str(e)}")

    except Exception as e:
        sender.reply(f"""=======网络错误=======
❌ 无法连接青龙面板
------------------
请检查:
1. 青龙面板是否运行
2. 网络是否正常
3. 配置是否正确
4. 错误信息: {str(e)}
------------------
当前配置:
• 地址: {QLurl if 'QLurl' in locals() else '未设置'}
• 应用ID: {ClientID[:4] + '****' if 'ClientID' in locals() else '未设置'}
====================""")
        exit(0)
def QLtoken(QLurl, ClientID, ClientSecret):
    """获取青龙token"""
    try:
        url = f'{QLurl}/open/auth/token?client_id={ClientID}&client_secret={ClientSecret}'
        response = requests.get(url)

        if response.status_code != 200:
            sender.reply(f"""=======请求失败=======
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
            sender.reply("""=======认证失败=======
❌ 获取Token失败
------------------
请检查:
• ClientID是否正确
• ClientSecret是否正确
• 应用是否有权限
====================""")
            exit(0)

    except requests.exceptions.RequestException as e:
        sender.reply(f"""=======网络错误=======
❌ 连接青龙面板失败
------------------
请检查:
• 青龙地址是否正确
• 网络是否正常
• 错误信息: {str(e)}
====================""")
        exit(0)
    except Exception as e:
        sender.reply(f"""=======系统错误=======
❌ 处理请求时出错
------------------
请检查:
• 配置格式是否正确
• 错误信息: {str(e)}
====================""")
        exit(0)
def QLzt(osname, value, account, username):
    """添加青龙变量"""
    try:
        qlurl = f"{QLurl}/open/envs"
        accountVip = '2099-12-31'
        data = [{
            "value": value,
            "name": osname,
            "remarks": f'唔语:{username}丨用户:{userid}丨账号:{account}丨授权时间:{accountVip}丨唔语管理'
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
    except Exception as e:
        sender.reply(f"""=======添加失败=======
❌ 添加青龙变量失败
------------------
请检查:
• 青龙面板状态
• 变量格式是否正确
• 错误信息: {str(e)}
====================""")
        exit(0)
def QLupdate(osname, value, account, qlid, username):
    """更新青龙变量"""
    try:
        qlurl = f"{QLurl}/open/envs"
        accountVip = '2099-12-31'
        data = {
            "value": value,
            "name": osname,
            "remarks": f'唔语:{username}丨用户:{userid}丨账号:{account}丨授权时间:{accountVip}丨唔语管理',
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
            return data['id'], data['createdAt']
        else:
            sender.reply("""=======更新失败=======
❌ 更新青龙变量失败
------------------
请稍后重试
====================""")
            exit(0)
    except Exception as e:
        sender.reply(f"""=======更新错误=======
❌ 更新变量时出错
------------------
错误信息: {str(e)}
====================""")
        exit(0)
def Addenvs(osname, value, account, username):
    """添加或更新青龙变量"""
    url = f"{QLurl}/open/envs"
    headers = {
        "Authorization": "Bearer" + ' ' + qltoken,
        "accept": "application/json"
    }
    try:
        response = requests.get(url=url, headers=headers).json()
        qlid = None
        username_qlid = None

        if response['code'] == 200:
            envslist = response['data']
            for envs in envslist:
                remarks = envs.get('remarks')
                envname = envs.get('name')
                if not remarks or envname != osname:
                    continue

                if account in remarks:
                    qlid = envs['id']
                    break

                if '唔语:' in remarks:
                    try:
                        remark_username = remarks.split('唔语:')[1].split('丨')[0]
                        if remark_username == username:
                            username_qlid = envs['id']
                    except:
                        continue

            if not qlid and username_qlid:
                qlid = username_qlid
        else:
            sender.reply("""=======连接失败=======
❌ 连接青龙获取变量失败
====================""")
            exit(0)

        value = urllib.parse.quote(value)
        if qlid:
            QLupdate(osname, value, account, qlid, username)
        else:
            QLzt(osname, value, account, username)
    except Exception as e:
        sender.reply(f"""=======操作失败=======
❌ 处理变量时出错
------------------
错误信息: {str(e)}
====================""")
        exit(0)
def get_user_detail(token):
    """获取用户详细信息"""
    try:
        token = normalize_token(token)

        url = "https://xcx.myinyun.com:4438/napi/wx/getUserDetail"
        headers = {
            'Host': 'xcx.myinyun.com:4438',
            'Connection': 'keep-alive',
            'content-type': 'application/json',
            'Accept-Encoding': 'gzip,compress,br,deflate',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 26_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.70(0x18004624) NetType/WIFI Language/zh_CN',
            'Referer': 'https://servicewechat.com/wxa25139b08fe6e2b6/23/page-frame.html',
            'authorization': f'Bearer {token}'
        }

        response = requests.get(url, headers=headers, timeout=30)
        return response.json()

    except Exception as e:
        return None
def check_token_valid(token):
    """检查token是否有效"""
    try:
        user_info = get_user_detail(token)
        if user_info and 'username' in user_info:
            return True, user_info.get('username', '未知')
        return False, 'Token失效'
    except:
        return False, 'Token失效'
def bind():
    """绑定账号"""
    def accvip(Newaddition):
        '添加' if Newaddition else '更新'
        auth_status = '✅ 已授权' if accountVip >= today_time else '⚠️ 未授权'
        next_step = f'发送 {randommanagecommand} 可管理账号' if accountVip >= today_time else f'发送 {randommanagecommand} 可进行授权'

        success_msg = f"""=======绑定成功=======
📱 用户名: {username}
🔐 状态: {auth_status}
⏰ 操作: {next_step}
===================="""
        if len(accountVip) != 0 and accountVip >= today_time:
            normalized_token = normalize_token(token)
            Addenvs(osname=dd_wuyu_osname, value=normalized_token, account=account, username=username)

        if account not in accounts:
            accounts.append(account)
            unique_accounts = list(dict.fromkeys(accounts))
            sg.bucketSet(bucket='dd_wuyu_user', key=userid, value=f'{unique_accounts}')

        sender.reply(success_msg)
    sender.reply("""=======唔语登录=======
请输入您的Token:
------------------
⚠️ 建议私聊登录,账号安全
⭐ 支持带Bearer或不带Bearer的Token
⭐ 输入q退出操作
====================""")
    input_token = sender.input(120000, 1, False)

    if input_token.lower() == 'q':
        sender.reply("✅ 已取消登录")
        exit(0)

    is_valid, username_or_error = check_token_valid(input_token)
    if not is_valid:
        sender.reply(f"""=======登录失败=======
❌ {username_or_error}
====================""")
        exit(0)

    token = normalize_token(input_token)
    username = username_or_error
    account = str(int(time.time() * 1000))  # 生成唯一账号ID

    old_auth = None
    accounts = []
    if len(uservalue) != 0:
        accounts = _sg_literal(uservalue)
        for acc in accounts:
            acc_token = sg.bucketGet(bucket='dd_wuyu_token', key=acc)
            if normalize_token(acc_token) == token:
                old_auth = '2099-12-31'
                accounts.remove(acc)
                sg.bucketDel(bucket='dd_wuyu_username', key=acc)
                sg.bucketDel(bucket='dd_wuyu_token', key=acc)
                qlid = allenvs(osname=dd_wuyu_osname, account=acc)
                if qlid:
                    delenvs(id=qlid)
                break

    sg.bucketSet(bucket='dd_wuyu_username', key=account, value=username)
    sg.bucketSet(bucket='dd_wuyu_token', key=account, value=token)

    if old_auth:
        True
        if old_auth >= today_time:
            Addenvs(osname=dd_wuyu_osname, value=token, account=account, username=username)

    if len(uservalue) == 0:
        accounts = []

    accountVip = '2099-12-31'
    accvip(True)  # 添加新账号
def ValueErrors(value, count):
    """验证输入值是否为有效的整数且在合理范围内"""
    try:
        value = int(value)
        if value > count or value == 0:
            sender.reply(f"""=======输入无效=======
❌ 请输入 1-{count} 之间的数字
====================""")
            exit(0)
        return value
    except ValueError:
        sender.reply("""=======输入无效=======
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
def allenvs(osname, account):
    """获取青龙环境变量"""
    url = f"{QLurl}/open/envs"
    headers = {
        "Authorization": f"Bearer {qltoken}",
        "accept": "application/json"
    }

    try:
        response = requests.get(url=url, headers=headers).json()
        qlid = None
        for envs in response['data']:
            if (envs.get('name') == osname and
                envs.get('remarks') and
                str(account) in envs['remarks']):
                qlid = envs['id']
                break
        return qlid
    except:
        return None
def delenvs(id):
    """删除青龙环境变量"""
    if id is None:
        return

    url = f"{QLurl}/open/envs"
    headers = {
        "Authorization": f"Bearer {qltoken}",
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    data = [id]

    try:
        response = requests.delete(url, headers=headers, json=data)
        if response.status_code != 200:
            return
        result = response.json()
        if result.get('code') != 200:
            return
    except:
        return
def management():
    """账号管理功能"""
    if len(uservalue) == 0:
        sender.reply(f"""=======未绑定账号=======
❌ 未找到任何账号信息
💡 发送 {randomsigncommand} 绑定
====================""")
        return
    count = 1
    account_list = """
======我的唔语听书账号======"""

    accounts = list(dict.fromkeys(_sg_literal(uservalue))) if uservalue else []
    sg.bucketSet(bucket='dd_wuyu_user', key=userid, value=f'{accounts}')
    for account in accounts:
        accountVip = '2099-12-31'
        if len(accountVip) == 0:
            vip_status = '⚠️ 未授权'
        elif accountVip < today_time:
            vip_status = '❌ 已过期'
        else:
            vip_status = f'✅ {accountVip}'

        username = sg.bucketGet(bucket='dd_wuyu_username', key=account)
        if username:
            display_username = username[:3] + '*' * 4 + username[7:] if len(username) > 7 else username[:2] + '***'
        else:
            display_username = account[:3] + "****" + account[7:]

        account_list += f"""
------------------
[{count}] 账号信息
📱 用户名: {display_username}
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
        if me_as_int > count - 1:
            sender.reply('❌ 输入的序号无效')
            exit(0)
    except ValueError:
        sender.reply('❌ 输入必须是数字')
        exit(0)

    account = accounts[me_as_int - 1]
    token = sg.bucketGet(bucket='dd_wuyu_token', key=f'{account}')
    accountVip = '2099-12-31'
    username = sg.bucketGet(bucket='dd_wuyu_username', key=f'{account}')

    if len(accountVip) == 0:
        vip_status = '⚠️ 未授权'
    elif accountVip < today_time:
        vip_status = '❌ 已过期'
    else:
        vip_status = f'✅ {accountVip}'

    account_info = f"""
=======账号详情======
📱 用户名: {username}
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
        confirm_msg = """=======删除警告=======
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
            qlid = allenvs(osname=dd_wuyu_osname, account=str(account))
            delenvs(id=qlid)
            if len(accounts) == 0:
                sg.bucketDel(bucket='dd_wuyu_user', key=userid)
            else:
                sg.bucketSet(bucket='dd_wuyu_user', key=userid, value=f'{accounts}')
            sender.reply('✅ 账号删除成功!')
        else:
            sender.reply('✅ 已取消删除')
            exit(0)

    elif inputmessage == '1':
        auth_guide = """=======授权设置=======
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
        money = Decimal(mes) * Decimal(WuyuVipmoney)

        zf(project='唔语授权', me_as_int=mes, accountVip=accountVip, token=token,
           username=username, account=account)

        accountVip = empower(empowertime=accountVip, me_as_int=mes)
        True
        Addenvs(osname=dd_wuyu_osname, value=token, account=account, username=username)

        result_msg = f"""=======订单完成=======
🎈 名称: 唔语授权
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
def zf(project, me_as_int, accountVip, token, username, account):
    """支付处理"""
    try:
        zsm = sg.bucketGet('dd_wuyu_config', 'zsm')
        use_ma_pay = '2099-12-31' == 'true'

        if not zsm and not use_ma_pay:
            sender.reply('❌ 未配置收款方式,请检查配置!')
            exit(0)

        usercoin = sg.bucketGet('dd_sign_points', userid) or '0'
        zfcoin = int(Wuyucoin) * me_as_int

        pay_options = []

        if zsm:
            money = Decimal(me_as_int) * Decimal(WuyuVipmoney)
            pay_options.append({
                'type': 'wechat',
                'name': '微信支付',
                'money': money,
                'zfcoin': 0
            })

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
                money = Decimal(me_as_int) * Decimal(WuyuVipmoney)
                pay_options.append({
                    'type': 'mapay',
                    'name': '在线处理',
                    'money': money,
                    'zfcoin': 0,
                    'config': ma_pay_config
                })

        if Wuyucoin and int(Wuyucoin) > 0:
            pay_options.append({
                'type': 'coin',
                'name': '积分支付',
                'money': 0,
                'zfcoin': zfcoin
            })

        pay_menu = """=====选择支付方式===="""
        for idx, option in enumerate(pay_options, 1):
            if option['type'] == 'wechat':
                pay_menu += f"""
{idx}️⃣ 微信支付
   💰 {option['money']}元/{me_as_int}月"""
            elif option['type'] == 'mapay':
                pay_menu += f"""
{idx}️⃣ 在线处理
   💰 {option['money']}元/{me_as_int}月"""
            elif option['type'] == 'coin':
                pay_menu += f"""
{idx}️⃣ 积分支付
   🎯 {option['zfcoin']}积分/{me_as_int}月
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

        try:
            choice_idx = int(choice) - 1
            if choice_idx < 0 or choice_idx >= len(pay_options):
                sender.reply("❌ 输入无效")
                exit(0)
            selected = pay_options[choice_idx]
        except ValueError:
            sender.reply("❌ 输入无效")
            exit(0)

        if selected['type'] == 'wechat':
            zfzt = False
            if zfzt:
                sender.reply('⚠️ 当前有人正在支付,请稍后再试！')
                exit(0)

            money = selected['money']

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

        elif selected['type'] == 'mapay':
            ma_pay_config = selected['config']
            money = selected['money']

            out_trade_no = f"WY{int(time.time())}{userid}"

            params = {
                'pid': ma_pay_config['pid'],
                'type': ma_pay_config['type'].split(',')[0],  # 默认使用第一个支付方式
                'out_trade_no': out_trade_no,
                'name': f"{senderID}-唔语授权-{str(money)}",
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

        elif selected['type'] == 'coin':
            if int(usercoin) < selected['zfcoin']:
                sender.reply(f"""=====积分不足=====
👤 当前积分: {usercoin}
📍 需要积分: {selected['zfcoin']}
==================""")
                exit(0)

            confirm_msg = f"""=====积分支付确认=====
💫 消耗积分: {selected['zfcoin']}
⏰ 授权时长: {me_as_int}月
------------------
确认请回复【y】
取消请回复【n】
=================="""
            sender.reply(confirm_msg)

            if yesornos():
                try:
                    new_balance = int(usercoin) - selected['zfcoin']
                    sg.bucketSet('dd_sign_points', userid, str(new_balance))
                    return True
                except Exception as e:
                    sender.reply(f"❌ 积分支付处理失败: {str(e)}")
                    exit(0)
            else:
                sender.reply("✅ 已取消支付")
                exit(0)

    except Exception as e:
        sender.reply(f"❌ 支付处理发生错误: {str(e)}")
        exit(0)
def cxs():
    """查询所有账号"""
    if len(uservalue) == 0:
        sender.reply(f"""=======未绑定账号=======
❌ 未找到任何账号信息
💡 发送 {randomsigncommand} 绑定
====================""")
        return
    accounts = list(dict.fromkeys(_sg_literal(uservalue))) if uservalue else []
    sg.bucketSet(bucket='dd_wuyu_user', key=userid, value=f'{accounts}')
    for account in accounts:
        token = sg.bucketGet(bucket='dd_wuyu_token', key=account)
        accountVip = '2099-12-31'
        username = sg.bucketGet(bucket='dd_wuyu_username', key=account)

        if len(accountVip) == 0 or accountVip < today_time:
            sender.reply(f"""=======授权过期=======
📱 账号: {username}
⚠️ 状态: 授权已过期
====================""")
            continue

        info = get_user_detail(normalize_token(token))
        if not info:
            sender.reply(f"""=======查询异常=======
📱 账号: {username}
❌ 状态: 查询失败
====================""")
            continue

        account_info = f"""=======账号详情=======
📱 用户名: {info.get('username', '未知')}
🌹 红花数量: {info.get('flowerCount', 0)}
📺 广告次数: {info.get('adCount', 0)}
⏱️ 总收听时长: {info.get('totalListenTime', 0)}秒
🔐 授权至: {accountVip}
===================="""
        sender.reply(account_info)
def wuyu_auth():
    return True
def clean_expired_accounts():
    """清理过期的唔语听书账号"""
    if not sender.isAdmin():
        sender.reply("⛔ 您没有权限执行此操作！")
        exit(0)

    users = sg.bucketAllKeys(bucket='dd_wuyu_user')
    sender.reply(
        "=====清理统计=====\n"
        f"📊 找到用户数: {len(users) if users else 0}\n"
        "==================="
    )

    if not users:
        sender.reply("❌ 没有找到任何绑定的唔语听书账号")
        exit(0)

    cleaned_count = 0
    ql_cleaned = 0
    ql_failed = 0

    for user in users:
        accountlist = sg.bucketGet(bucket='dd_wuyu_user', key=user)
        if not accountlist:
            continue

        accounts = _sg_literal(accountlist)
        valid_accounts = []

        for account in accounts:
            accountVip = '2099-12-31'

            if len(accountVip) == 0 or accountVip <= today_time:
                try:
                    qlid = allenvs(osname=dd_wuyu_osname, account=account)
                    if qlid:
                        delenvs(id=qlid)
                        ql_cleaned += 1
                    else:
                        ql_failed += 1
                except:
                    ql_failed += 1

                sg.bucketDel(bucket='dd_wuyu_token', key=account)
                True
                sg.bucketDel(bucket='dd_wuyu_username', key=account)
                cleaned_count += 1
            else:
                valid_accounts.append(account)

        if valid_accounts:
            sg.bucketSet(bucket='dd_wuyu_user', key=user, value=str(valid_accounts))
        else:
            sg.bucketDel(bucket='dd_wuyu_user', key=user)

    sender.reply(
        "=====清理完成=====\n"
        f"🧹 清理插件账号: {cleaned_count}个\n"
        f"🔧 清理青龙变量: {ql_cleaned}个\n"
        f"❌ 青龙变量失败: {ql_failed}个\n"
        "==================="
    )
today_date = datetime.now().date()
today_time = str(today_date)
dd_wuyu_osname, dd_wuyu_qlname, dd_managecommand, dd_querycommand, dd_signcommand, randommanagecommand, randomquerycommand, randomsigncommand, WuyuVipmoney, Wuyucoin = getusercontent()
QLurl, qltoken = seekql()
usermessage = sender.getMessage()
imtype = sender.getImtype()
if '登录' in usermessage or '登陆' in usermessage:
    bind()
elif '管理' in usermessage:
    management()
elif '查询' in usermessage:
    cxs()
elif '唔语授权' in usermessage:
    wuyu_auth()
elif '清理唔语' in usermessage or '唔语清理' in usermessage:
    clean_expired_accounts()
elif imtype == 'fake':
    """定时任务处理"""
    users = sg.bucketAllKeys(bucket='dd_wuyu_user')
    if not users:
        exit(0)

    for user in users:
        try:
            uservalue = sg.bucketGet(bucket='dd_wuyu_user', key=user)
            if not uservalue:
                continue

            accounts = _sg_literal(uservalue)
            for account in accounts:
                try:
                    token = sg.bucketGet(bucket='dd_wuyu_token', key=account)
                    accountVip = '2099-12-31'
                    username = sg.bucketGet(bucket='dd_wuyu_username', key=account)

                    if not token:
                        continue

                    if len(accountVip) == 0 or accountVip < today_time:
                        print(f"账号 {account} 授权已过期")
                        continue

                    is_valid, _ = check_token_valid(token)
                    if not is_valid:
                        print(f"账号 {account} token已失效")
                        continue

                    info = get_user_detail(token)
                    if info:
                        if info.get('username') != username:
                            sg.bucketSet(bucket='dd_wuyu_username', key=account, value=info.get('username'))

                    print(f"账号 {account} ({username}) 运行正常")

                except Exception as e:
                    print(f"处理账号 {account} 时出错: {str(e)}")
                    continue

        except Exception as e:
            print(f"处理用户 {user} 时出错: {str(e)}")
            continue
