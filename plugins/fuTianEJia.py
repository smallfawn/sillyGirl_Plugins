# [title: 福田e家]
# [name: fuTianEJia]
# [language: python]
# [class: 任务]
# [author: sky2022]
# [version: v1.0.1]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^福田(登录|登陆|批量登录|批量登陆|查询|管理|订单查询|清理)$|^(登录|登陆|批量登录|批量登陆|查询|管理)福田$|^清理福田$]
# [icon: https://images.mingming.dev/file/7c1c97c112588fbf7c0db.png]
# [description: 福田e家账号登录、批量导入、积分/订单查询、管理与面板同步]
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
    'dd_fukuda_config_panel_type': plugin.Form.string().title('对接面板类型').default('').description('填写你当前使用的面板类型，支持：青龙、青龙面板、QL、呆呆、呆呆面板、Daidai'),
    'dd_fukuda_config_panel_config': plugin.Form.string().title('对接面板配置').default('').description('统一填写面板对接参数。青龙：Host丨ClientID丨ClientSecret；呆呆：Host丨AppKey丨AppSecret；分隔符使用中文丨'),
    'dd_fukuda_config_panel_group': plugin.Form.string().title('对接面板分组').default('').description('仅呆呆面板生效。填写后新增或更新变量时会同步写入 group 字段；留空则不处理分组'),
    'dd_fukuda_config_osname': plugin.Form.string().title('面板变量名').default('').description('提交到面板中的福田e家变量名'),
    'dd_fukuda_config_proxy_url': plugin.Form.string().title('代理地址').default('').description('登录请求使用的代理拉取接口，返回 http(s)://host:port'),
})
_CONFIG_FIELD_MAP = {
    ('dd_fukuda_config', 'panel_type'): 'dd_fukuda_config_panel_type',
    ('dd_fukuda_config', 'panel_config'): 'dd_fukuda_config_panel_config',
    ('dd_fukuda_config', 'panel_group'): 'dd_fukuda_config_panel_group',
    ('dd_fukuda_config', 'osname'): 'dd_fukuda_config_osname',
    ('dd_fukuda_config', 'proxy_url'): 'dd_fukuda_config_proxy_url',
}

import requests
from datetime import datetime
import json
import time

senderID = sg.getSenderID()  # 创建发送者
sender = sg.Sender(senderID)  # 向用户发送消息
userid = sender.getUserID()  # 消息接收者
uservalue = sg.bucketGet(bucket='dd_fukuda_user', key=userid) or ''  # 获取用户的值

def normalize_panel_type(panel_type_value):
    value = str(panel_type_value or '').strip().lower()
    if value in ('呆呆', '呆呆面板', 'daidai', 'dd'):
        return 'daidai'
    if value in ('青龙', '青龙面板', 'qinglong', 'ql'):
        return 'qinglong'
    return ''

def QLtoken(QLurl, ClientID, ClientSecret):
    try:
        url = f'{QLurl}/open/auth/token?client_id={ClientID}&client_secret={ClientSecret}'
        response = requests.get(url)

        if response.status_code != 200:
            sender.reply("""
==================
    请求失败
==================
❌ 青龙API请求失败
------------------
状态码: {response.status_code}
请检查:
• API地址是否正确
• 面板是否正常运行
==================""")
            exit(0)

        result = response.json()
        if "token" in result.get('data', {}):
            return result['data']['token']
        else:
            sender.reply("""
==================
    认证失败
==================
❌ 获取Token失败
------------------
请检查:
• ClientID是否正确
• ClientSecret是否正确
• 应用是否有权限
==================""")
            exit(0)

    except requests.exceptions.RequestException as e:
        sender.reply(f"""
==================
    网络错误
==================
❌ 连接青龙面板失败
------------------
请检查:
• 青龙地址是否正确
• 网络是否正常
• 错误信息: {str(e)}
==================""")
        exit(0)
    except Exception as e:
        sender.reply(f"""
==================
    系统错误
==================
❌ 处理请求时出错
------------------
请检查:
• 配置格式是否正确
• 错误信息: {str(e)}
==================""")
        exit(0)

def DDtoken(DDurl, AppKey, AppSecret):
    try:
        response = requests.post(f'{DDurl}/api/open-api/token', json={"app_key": AppKey, "app_secret": AppSecret})
        if response.status_code != 200:
            raise Exception(f"请求失败: {response.status_code}")
        result = response.json()
        access_token = result.get('data', {}).get('access_token')
        if access_token:
            return access_token
        raise Exception("获取Token失败")
    except Exception as e:
        sender.reply(f"""
==================
    系统错误
==================
❌ 获取呆呆面板Token失败
------------------
请检查:
• 配置格式是否正确
• 错误信息: {str(e)}
==================""")
        exit(0)

def PluginsData():
    panel_type=normalize_panel_type(sg.bucketGet('dd_fukuda_config','panel_type') or 'qinglong')
    panel=str(sg.bucketGet('dd_fukuda_config','panel_config') or '').strip();parts=panel.split('丨') if panel else []
    host,client_id,secret=(parts+['','',''])[:3]
    return host,client_id,secret,0,sg.bucketGet('dd_fukuda_config','osname') or 'FUKUDA',0,False,sg.bucketGet('dd_fukuda_config','proxy_url') or '',panel_type=='daidai',sg.bucketGet('dd_fukuda_config','panel_group') or ''


def update_proxy(session, proxy_url):
    if not proxy_url:
        return
    try:
        ip = requests.get(proxy_url).text
        if not ip or '请先添加白名单' in ip:
            return
        session.proxies = {'http': ip, 'https': ip}
    except Exception:
        return

def create_proxy_session(headers: dict | None=None):
    session = requests.Session()
    if headers:
        session.headers.update(headers)
    update_proxy(session, proxy_url)
    return session

def allenvs(osname, account):
    if use_daidai:
        url = f"{QLurl}/api/envs"
        headers = {
            "Authorization": f"Bearer {qltoken}",
            "accept": "application/json"
        }
    else:
        url = f"{QLurl}/open/envs"
        headers = {
            "Authorization": f"Bearer {qltoken}",
            "accept": "application/json"
        }

    try:
        if use_daidai:
            response = requests.get(url=url, headers=headers, params={"keyword": str(account), "page_size": 100})
            if response.status_code != 200:
                sender.reply("连接呆呆面板获取变量失败")
                exit(0)
            result = response.json()
            qlid = None
            for env in result.get('data', []):
                if (env.get('name') == osname and env.get('remarks') and str(account) in env['remarks']):
                    qlid = env['id']
                    break
        else:
            response = requests.get(url=url, headers=headers)
            if response.status_code != 200:
                sender.reply("""
==================
    请求失败
==================
❌ 获取变量失败
------------------
请检查:
• 青龙面板是否正常
• Token是否有效
==================""")
                exit(0)

            result = response.json()
            if result['code'] != 200:
                sender.reply("""
==================
    响应错误
==================
❌ 获取变量失败
------------------
请检查:
• 应用权限是否正确
• 变量是否存在
==================""")
                exit(0)

            qlid = None
            for env in result['data']:
                if (env.get('name') == osname and
                    env.get('remarks') and
                    str(account) in env['remarks']):
                    qlid = env['id']
                    break

        return qlid

    except Exception as e:
        sender.reply(f"""
==================
    系统错误
==================
❌ 获取变量时出错
------------------
错误信息: {str(e)}
==================""")
        exit(0)

def login(name, password):
    url = "https://czyl.foton.com.cn/ehomes-new/homeManager/getLoginMember"
    payload = json.dumps({
        "password": password,
        "name": name,
    })
    headers = {
        'User-Agent': "okhttp/3.14.9",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Content-Type': "application/json",
    }

    try:
        session = requests.Session()
        session.headers.update(headers)
        update_proxy(session, proxy_url)
        response = session.post(url, data=payload)
        if response.status_code != 200:
            return "网络请求失败", "登录失败", False

        result = response.json()
        if 'data' not in result:
            return result.get('msg', "登录失败"), "登录失败", False

        memberID = result['data']['memberID']
        account = result['data']['uid']
        return str(account), memberID, f'{name}#{password}'

    except Exception as e:
        return f"登录异常: {str(e)}", "登录异常", False

def Addenvs(osname, value, account, phone):
    phone = phone[:3] + '*' * 4 + phone[7:]
    qlid = allenvs(osname, account)

    if qlid is None:
        QLzt(osname, value, account, phone)
    else:
        QLupdate(osname, value, account, qlid, phone)

def QLzt(osname, value, account, phone):
    try:
        if use_daidai:
            url = f"{QLurl}/api/envs"
            data = {
                "value": value,
                "name": osname,
                "remarks": f'福田:{account}丨用户:{userid}丨手机:{phone}丨福田管理'
            }
            if panel_group:
                data["group"] = panel_group
            headers = {
                "Authorization": f"Bearer {qltoken}",
                "accept": "application/json",
                "Content-Type": "application/json",
            }
            response = requests.post(url, headers=headers, json=data)
            if response.status_code not in (200, 201):
                sender.reply("添加呆呆面板变量失败")
                exit(0)
            result = response.json()
            return result.get('data', {}).get('id')
        else:
            url = f"{QLurl}/open/envs"
            data = [{
                "value": value,
                "name": osname,
                "remarks": f'福田:{account}丨用户:{userid}丨手机:{phone}丨福田管理'
            }]
            headers = {
                "Authorization": f"Bearer {qltoken}",
                "accept": "application/json",
                "Content-Type": "application/json",
            }

            response = requests.post(url, headers=headers, data=json.dumps(data))
            if response.status_code != 200:
                sender.reply("""
==================
    请求失败
==================
❌ 添加变量失败
------------------
请检查:
• 青龙面板是否正常
• Token是否有效
==================""")
                exit(0)

            result = response.json()
            if "value must be unique" in response.text:
                return

            if result.get('code') != 200:
                sender.reply("""
==================
    添加失败
==================
❌ 变量添加失败
------------------
请检查:
• 变量格式是否正确
• 应用权限是否正确
==================""")
                exit(0)

            return result['data'][0]['id']

    except Exception as e:
        sender.reply(f"""
==================
    系统错误
==================
❌ 添加变量时出错
------------------
错误信息: {str(e)}
==================""")
        exit(0)

def QLupdate(osname, value, account, qlid, phone):
    try:
        if use_daidai:
            url = f"{QLurl}/api/envs/{qlid}"
            data = {
                "value": value,
                "name": osname,
                "remarks": f'福田:{account}丨用户:{userid}丨手机:{phone}丨福田管理'
            }
            if panel_group:
                data["group"] = panel_group
            headers = {
                "Authorization": f"Bearer {qltoken}",
                "accept": "application/json",
                "Content-Type": "application/json",
            }
            response = requests.put(url, headers=headers, json=data)
            if response.status_code != 200:
                sender.reply("更新呆呆面板变量失败")
                exit(0)
            return qlid, None
        else:
            url = f"{QLurl}/open/envs"
            data = {
                "value": value,
                "name": osname,
                "remarks": f'福田:{account}丨用户:{userid}丨手机:{phone}丨福田管理',
                "id": qlid
            }
            headers = {
                "Authorization": f"Bearer {qltoken}",
                "accept": "application/json",
                "Content-Type": "application/json",
            }

            response = requests.put(url, headers=headers, data=json.dumps(data))
            if response.status_code != 200:
                sender.reply("""
==================
    请求失败
==================
❌ 更新变量失败
------------------
请检查:
• 青龙面板是否正常
• Token是否有效
==================""")
                exit(0)

            result = response.json()
            if result.get('code') != 200:
                sender.reply("""
==================
    更新失败
==================
❌ 变量更新失败
------------------
请检查:
• 变量格式是否正确
• 应用权限是否正确
==================""")
                exit(0)

            data = result.get('data')
            if not data:
                sender.reply("""
==================
    数据错误
==================
❌ 未返回更新数据
------------------
请检查:
• 变量ID是否存在
• 数据格式是否正确
==================""")
                exit(0)

            return data['id'], data['createdAt']

    except Exception as e:
        sender.reply(f"""
==================
    系统错误
==================
❌ 更新变量时出错
------------------
错误信息: {str(e)}
==================""")
        exit(0)

def bind():
    sender.reply('请输入福田e家手机号，q 退出');mobile=sender.input(120000,1,False)
    if not mobile or str(mobile).lower()=='q':return sender.reply('已取消')
    mobile=str(mobile).strip()
    if not mobile.isdigit() or len(mobile)!=11:return sender.reply('手机号格式错误')
    sender.reply('请输入密码');password=sender.input(120000,1,False)
    if not password or str(password).lower()=='q':return sender.reply('已取消')
    account,member_id,credential=login(mobile,str(password))
    if not credential:return sender.reply(f'登录失败：{account}')
    accounts=list(dict.fromkeys(_sg_literal(sg.bucketGet('dd_fukuda_user',userid),[])+[account]));stored=f'{mobile}#{password}'
    sg.bucketSet('dd_fukuda_user',userid,str(accounts));sg.bucketSet('dd_fukuda_token',account,stored)
    sync='未配置面板，仅本地保存'
    if qltoken:
        try:Addenvs(osname,stored,account,mobile);sync='面板同步成功'
        except Exception as error:sync=f'面板同步失败：{error}'
    sender.reply(f'福田账号 {mobile[:3]}****{mobile[-4:]} 登录成功；{sync}')


def batch_bind():
    sender.reply('请按“手机号#密码”每行一个发送，q 退出');text=sender.input(300000,1,False)
    if not text or str(text).lower()=='q':return sender.reply('已取消')
    accounts=list(_sg_literal(sg.bucketGet('dd_fukuda_user',userid),[]));success=failed=0
    for line in str(text).splitlines():
        try:
            mobile,password=map(str.strip,line.split('#',1))
            if len(mobile)!=11 or not mobile.isdigit():raise ValueError('手机号格式错误')
            account,_,credential=login(mobile,password)
            if not credential:raise ValueError(str(account))
            stored=f'{mobile}#{password}';accounts.append(account);sg.bucketSet('dd_fukuda_token',account,stored)
            if qltoken:Addenvs(osname,stored,account,mobile)
            success+=1
        except Exception as error:print(f'批量登录失败 {line}: {error}');failed+=1
    accounts=list(dict.fromkeys(accounts));sg.bucketSet('dd_fukuda_user',userid,str(accounts));sender.reply(f'批量登录完成：成功 {success}，失败 {failed}')


def ValueErrors(value, count):
    if value is None or value == '':
        sender.reply('输入超时！')
        exit(0)
    elif value.lower() == 'q':
        sender.reply('退出！')
        exit(0)

    try:
        value = int(value)
        if value < 0 or (value > count and value != 0):
            sender.reply('输入错误！')
            exit(0)
        return value
    except ValueError:
        sender.reply('输入错误！')
        exit(0)

def Administration():
    accounts=list(_sg_literal(sg.bucketGet('dd_fukuda_user',userid),[]))
    if not accounts:return sender.reply('未绑定账号，请发送【福田登录】')
    rows=[]
    for i,account in enumerate(accounts,1):
        token=sg.bucketGet('dd_fukuda_token',account) or '';mobile=token.split('#',1)[0] if '#' in token else str(account);rows.append(f'{i}. {mobile[:3]}****{mobile[-4:]}')
    sender.reply('福田账号：\n'+'\n'.join(rows)+'\n回复序号管理，q 退出');choice=sender.input(120000,1,False)
    if choice is None or str(choice).lower()=='q':return
    try:account=accounts[int(choice)-1]
    except (ValueError,IndexError):return sender.reply('序号无效')
    sender.reply('1. 删除账号\n2. 重新同步面板\nq. 退出');action=sender.input(60000,1,False);token=sg.bucketGet('dd_fukuda_token',account) or ''
    if action=='1':
        sender.reply('回复 y 确认删除')
        if str(sender.input(60000,1,False)).lower()=='y':
            env=allenvs(osname,account) if qltoken else None
            if env:delenvs(env)
            accounts.remove(account);sg.bucketSet('dd_fukuda_user',userid,str(accounts)) if accounts else sg.bucketDel('dd_fukuda_user',userid);sg.bucketDel('dd_fukuda_token',account);sender.reply('账号已删除')
    elif action=='2':
        if not token:return sender.reply('凭证不存在，请重新登录')
        if not qltoken:return sender.reply('未配置面板')
        mobile=token.split('#',1)[0];Addenvs(osname,token,account,mobile);sender.reply('面板同步完成')





def delenvs(id):
    if id is None:
        return

    try:
        if use_daidai:
            url = f"{QLurl}/api/envs/{id}"
            headers = {
                "Authorization": f"Bearer {qltoken}",
                "accept": "application/json",
                "Content-Type": "application/json",
            }
            response = requests.delete(url, headers=headers)
            if response.status_code != 200:
                sender.reply("删除呆呆面板变量失败")
                return
        else:
            url = f"{QLurl}/open/envs"
            headers = {
                "Authorization": f"Bearer {qltoken}",
                "accept": "application/json",
                "Content-Type": "application/json",
            }
            data = [id]
            response = requests.delete(url, headers=headers, json=data)
            if response.status_code != 200:
                sender.reply("""
==================
    删除失败
==================
❌ 删除变量失败
------------------
请检查:
• 青龙面板是否正常
• Token是否有效
==================""")
                return

            result = response.json()
            if result.get('code') != 200:
                sender.reply("""
==================
    删除错误
==================
❌ 变量删除失败
------------------
请检查:
• 变量ID是否存在
• 应用权限是否正确
==================""")
            return

    except Exception as e:
        sender.reply(f"""
==================
    系统错误
==================
❌ 删除变量时出错
------------------
错误信息: {str(e)}
==================""")
        return

def cx(memberID):
    try:
        url = "https://czyl.foton.com.cn/ehomes-new/homeManager/api/Member/findMemberPointsInfo"

        payload = json.dumps({
            "memberId": f"{memberID}",
        })

        headers = {
            'User-Agent': "web",
            'Accept-Encoding': "gzip",
            'Content-Type': "application/json",
        }

        session = create_proxy_session(headers)
        response = session.post(url, data=payload, timeout=15)
        if response.status_code != 200:
            return f"错误: HTTP {response.status_code}", 0

        try:
            r = response.json()
        except Exception as e:
            return f"错误: 响应非JSON({str(e)})", 0

        pointValue = 0
        if isinstance(r, dict):
            code = r.get('code') or r.get('stateCode')
            if code == 200 or code == 0 or ('查询成功' in str(r)):
                data = r.get('data') or {}
                if isinstance(data, dict):
                    pv = data.get('pointValue') or data.get('points') or data.get('point')
                else:
                    pv = data
                try:
                    pointValue = int(pv)
                except Exception:
                    return "错误: 未返回有效积分", 0
            else:
                return f"错误: {r.get('msg') or r.get('message') or '查询失败'}", 0
        else:
            return "错误: 返回格式异常", 0

        todaycoin = 0
        url = "https://czyl.foton.com.cn/ehomes-new/homeManager/api/Member/getIntegralList"

        data = {"memberId": memberID, 'transactionDate': today_time}

        response = session.post(url, data=json.dumps(data), timeout=15)
        if response.status_code != 200:
            return pointValue, 0

        try:
            r2 = response.json()
        except Exception:
            return pointValue, 0

        items = r2.get('data') or []
        if not isinstance(items, list):
            items = []

        for coinj in items:
            integral = coinj.get('integral', 0)
            date = coinj.get('date', '') or coinj.get('createTime', '')
            try:
                if str(date)[:10] == today_time:
                    todaycoin += int(integral)
            except Exception:
                continue

        return pointValue, todaycoin

    except Exception as e:
        return f"错误: 查询异常({str(e)})", 0

def cxs():
    accounts=list(_sg_literal(sg.bucketGet('dd_fukuda_user',userid),[]))
    if not accounts:return sender.reply('未绑定账号，请发送【福田登录】')
    rows=[]
    for account in accounts:
        stored=sg.bucketGet('dd_fukuda_token',account) or ''
        try:mobile,password=stored.split('#',1)
        except ValueError:rows.append(f'{account}：凭证损坏');continue
        current,member_id,token=login(mobile,password);masked=mobile[:3]+'****'+mobile[-4:]
        if not token:rows.append(f'{masked}：登录失效');continue
        points,today=cx(member_id);orders,_=cx_orders(member_id,current,mobile,stored)
        rows.append(f'{masked}：积分 {points}，今日 {today}，订单 {orders if isinstance(orders,int) else "查询失败"}')
    sender.reply('福田查询：\n'+'\n'.join(rows))


def clean_expired_accounts():
    if not sender.isAdmin():return sender.reply('仅管理员可清理')
    cleaned=0
    for user in sg.bucketAllKeys('dd_fukuda_user'):
        accounts=list(_sg_literal(sg.bucketGet('dd_fukuda_user',user),[]));valid=[]
        for account in accounts:
            stored=sg.bucketGet('dd_fukuda_token',account) or ''
            try:mobile,password=stored.split('#',1);_,_,token=login(mobile,password)
            except Exception:token=None
            if token:valid.append(account)
            else:sg.bucketDel('dd_fukuda_token',account);cleaned+=1
        if valid:sg.bucketSet('dd_fukuda_user',user,str(valid))
        else:sg.bucketDel('dd_fukuda_user',user)
    sender.reply(f'清理完成：删除 {cleaned} 个失效账号')


def cx_orders(memberID, userId, mobile, stored_token):
    try:
        payload = {
            "memberId": memberID,
            "userId": userId,
            "userType": "61",
            "uid": userId,
            "mobile": mobile,
            "tel": mobile,
            "phone": mobile,
            "brandName": "萨普",
            "seriesName": "萨普T",
            "token": "ebf76685e48d4e14a9de6fccc76483e3",  # 使用硬编码的token
            "safeEnc": int(time.time() * 1000),
            "businessId": 1,
            "pageNum": 1,
            "pageSize": 10
        }

        headers = {
            'User-Agent': "web",
            'Accept-Encoding': "gzip",
            'Content-Type': "application/json",
            'app-key': "7918d2d1a92a02cbc577adb8d570601e72d3b640",
            'content-type': "application/json; charset=utf-8",
            'token': "",  # 订单API的token在headers中为空
            'app-token': "58891364f56afa1b6b7dae3e4bbbdfbfde9ef489"
        }

        url = "https://czyl.foton.com.cn/ehomes-new/homeManager/api/other/foton365MyOrders"

        session = create_proxy_session(headers)
        response = session.post(url, data=json.dumps(payload), timeout=15)
        if response.status_code != 200:
            return f"HTTP错误: {response.status_code}", []

        result = response.json()
        if result.get('code') != 200:
            return f"查询失败: {result.get('msg', '未知错误')}", []

        data = result.get('data', {})
        items = data.get('items', [])
        total = data.get('total', 0)

        return total, items

    except Exception as e:
        return f"查询异常: {str(e)}", []

def cxdd():
    current_uservalue = sg.bucketGet(bucket='dd_fukuda_user', key=userid) or ''
    if len(current_uservalue) == 0:
        sender.reply("""
======未绑定账号=====
❌ 未找到任何账号信息
💡 发送"福田登录"绑定
==================""")
        return

    accounts = _sg_literal(current_uservalue)
    valid_accounts = []

    if len(accounts) > 1:
        message = '=====选择查询账号=====\n'
        count = 1

        for account in accounts:
            Token = sg.bucketGet(bucket='dd_fukuda_token', key=account)
            if not Token:
                continue

            mobile = Token.split('#')[0]
            phone = mobile[:3] + '*' * 4 + mobile[7:]
            message += f'{count}. 账号: {phone}\n'
            valid_accounts.append(account)
            count += 1

        if not valid_accounts:
            sender.reply("""
======无有效账号======
❌ 未找到有效账号信息
💡 请重新绑定账号
==================""")
            return

        message += '------------------\n请选择要查询的账号序号\n⚠️ 输入"q"退出操作\n=================='
        sender.reply(message)

        mes = sender.input(120000, 1, False)
        mes = ValueErrors(value=mes, count=len(valid_accounts))
        account = valid_accounts[mes - 1]
    else:
        account = accounts[0]
        valid_accounts = [account]

    Token = sg.bucketGet(bucket='dd_fukuda_token', key=account)
    if not Token:
        sender.reply("❌ 未找到账号Token信息")
        return

    mobile = Token.split('#')[0]
    password = Token.split('#')[1]
    phone = mobile[:3] + '*' * 4 + mobile[7:]

    account, memberID, token = login(mobile, password)
    if not token:
        sender.reply(f"""
==================
    登录失败
==================
📱 账号: {phone}
❌ 状态: 登录失败
==================""")
        return

    sender.reply("正在查询订单信息...")
    order_total, order_items = cx_orders(memberID, account, mobile, Token)

    if isinstance(order_total, str):
        sender.reply(f"""
=====订单查询失败=====
📱 账号: {phone}
❌ 错误: {order_total}
==================""")
        return

    if order_total == 0:
        sender.reply(f"""
=====订单查询结果=====
📱 账号: {phone}
📦 订单总数: 0个
💡 暂无订单记录
==================""")
        return

    message = f"""
=====订单查询结果=====
📱 账号: {phone}
📦 订单总数: {order_total}个
=================="""

    for i, order in enumerate(order_items):
        order.get('orderNumber', '未知订单号')
        order_status = order.get('orderStatusName', '未知状态')
        order_time = order.get('orderCreateTime', '未知时间')
        order.get('merchantName', '未知商家')
        order.get('payableAmount', '0.00')

        products = order.get('productList', [])
        product_info = "未知商品"
        if products:
            product = products[0]
            product_name = product.get('name', '未知商品')
            if len(products) > 1:
                product_info = f"{product_name} 等{len(products)}件商品"
            else:
                product_info = product_name

        status_info = ""
        if order.get('sign'):
            status_info += "📋 待签收"

        if order.get('commentable'):
            status_info += " ✅ 已签收"

        status_emoji = ""
        if "待收货" in order_status:
            status_emoji = "🚚"
        elif "已签收" in order_status:
            status_emoji = "🚚"
        elif "待发货" in order_status:
            status_emoji = "📦"
        elif "已取消" in order_status:
            status_emoji = "❌"
        else:
            status_emoji = "📋"

        message += f"""
╭─ {status_emoji} 订单 {i+1}
├🛒 商品: {product_info}
├📅 时间: {order_time[:16]}
{f"╰🔔 {status_info}" if status_info else "╰──────────────────"}"""

    sender.reply(message)

today_time=str(datetime.now().date());QLurl,ClientID,ClientSecret,_,osname,_,_,proxy_url,use_daidai,panel_group=PluginsData();qltoken=''
if QLurl and ClientID and ClientSecret:qltoken=DDtoken(QLurl,ClientID,ClientSecret) if use_daidai else QLtoken(QLurl,ClientID,ClientSecret)
usermessage=sender.getMessage()
if '批量' in usermessage and ('登录' in usermessage or '登陆' in usermessage):batch_bind()
elif '登录' in usermessage or '登陆' in usermessage:bind()
elif '管理' in usermessage:Administration()
elif usermessage in ('福田查询','查询福田'):cxs()
elif usermessage=='福田订单查询':cxdd()
elif usermessage in ('清理福田','福田清理'):clean_expired_accounts()
else:sender.setContinue()
