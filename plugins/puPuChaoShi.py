# [title: 朴朴超市]
# [name: puPuChaoShi]
# [language: python]
# [class: 任务]
# [author: sky2022]
# [version: v1.0.0]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^朴朴登陆$|^朴朴登录$|^登录朴朴$|^登陆朴朴$|^朴朴查询$|^查询朴朴$|^朴朴管理$|^管理朴朴$|^朴朴刷新$|^刷新朴朴$]
# [icon: https://static.foodtalks.cn/company/images/214/35logo.jpg]
# [description: 2.0全新UI 支持扫码登录和手动抓包登录；指令：朴朴登录、朴朴管理、朴朴查询、朴朴刷新；脚本请进]
# [depe: ["requests"]]


import asyncio as _sg_asyncio
import os as _sg_os
import time as _sg_time
import types as _sg_types
import json as _sg_json
from threading import Thread as _sg_Thread
from sillygirl import Adapter as _SGAdapter, Bucket as _SGBucket, Sender as _SGSender, sender as _sg_sender, form
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

config = form({
    'dd_pp_panel_type': form.string().title('对接面板类型').default('').description('填写你当前使用的面板类型，支持：青龙、青龙面板、QL、呆呆、呆呆面板、Daidai'),
    'dd_pp_panel_config': form.string().title('对接面板配置').default('').description('青龙：Host丨ClientID丨ClientSecret；呆呆：Host丨AppKey丨AppSecret；分隔符使用中文丨。老的 Qinglong 配置仍兼容'),
    'dd_pp_files': form.string().title('写入脚本路径').default('').description('写入面板中的目标脚本路径，例如 leafTheFish_DeathNote/pupuCookie.txt 或 pupuCookie.txt'),
})
_CONFIG_FIELD_MAP = {
    ('dd_pp', 'panel_type'): 'dd_pp_panel_type',
    ('dd_pp', 'panel_config'): 'dd_pp_panel_config',
    ('dd_pp', 'files'): 'dd_pp_files',
}

import requests
import json
from datetime import datetime
import time

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()
uservalue = sg.bucketGet(bucket='dd_pp_user', key=userid)
filespath = sg.bucketGet(bucket='dd_pp', key='files')

def normalize_panel_type(panel_type_value):
    value = str(panel_type_value or '').strip().lower()
    if value in ('呆呆', '呆呆面板', 'daidai', 'dd'):
        return 'daidai'
    if value in ('青龙', '青龙面板', 'qinglong', 'ql', ''):
        return 'qinglong'
    return ''

def split_script_path(script_path):
    normalized = str(script_path or '').replace('\\', '/').strip('/')
    if '/' in normalized:
        path, filename = normalized.rsplit('/', 1)
        return path, filename, normalized
    return '', normalized, normalized


def seekql():
    panel_type = normalize_panel_type(sg.bucketGet(bucket='dd_pp', key='panel_type') or '')
    if not panel_type:
        sender.reply("❌ 对接面板类型填写无效，请填写：青龙/青龙面板/QL 或 呆呆/呆呆面板/Daidai")
        exit(0)

    panel_config = (sg.bucketGet(bucket='dd_pp', key='panel_config') or '').strip()
    legacy_qinglong = sg.bucketGet(bucket='dd_pp', key='Qinglong') or ''
    current_config = panel_config or (legacy_qinglong if panel_type == 'qinglong' else '')
    try:
        if len(current_config) == 0:
            if panel_type == 'daidai':
                sender.reply("""
=====面板配置错误=====
❌ 未配置呆呆面板信息
------------------
请在插件配置中填写:
对接面板类型: 呆呆
对接面板配置: Host丨AppKey丨AppSecret
==================""")
            else:
                sender.reply("""
=====面板配置错误=====
❌ 未配置青龙面板信息
------------------
请在插件配置中填写:
对接面板类型: 青龙
对接面板配置: Host丨ClientID丨ClientSecret
==================""")
            exit(0)

        qllist = current_config.split('丨')
        if len(qllist) != 3:
            if panel_type == 'daidai':
                sender.reply(f"""
======格式错误======
❌ 呆呆面板配置格式错误
------------------
当前格式: {current_config}
正确格式:
Host丨AppKey丨AppSecret
==================""")
            else:
                sender.reply(f"""
======格式错误======
❌ 青龙面板配置格式错误
------------------
当前格式: {current_config}
正确格式:
Host丨ClientID丨ClientSecret
==================""")
            exit(0)

        QLurl = qllist[0].strip()
        ClientID = qllist[1].strip()
        ClientSecret = qllist[2].strip()

        if not all([QLurl, ClientID, ClientSecret]):
            sender.reply("""
======参数错误=======
❌ 面板配置参数不完整
------------------
请确保以下参数都已填写:
• 面板地址(Host)
• Key / ID
• Secret
==================""")
            exit(0)

        if not QLurl.startswith(('http://', 'https://')):
            sender.reply(f"""
=====地址错误======
❌ 面板地址格式错误
------------------
当前地址: {QLurl}
正确格式:
• http://panel.example.com
• https://panel.example.com
==================""")
            exit(0)

        try:
            if panel_type == 'daidai':
                qltoken = DDtoken(DDurl=QLurl, AppKey=ClientID, AppSecret=ClientSecret)
            else:
                qltoken = QLtoken(QLurl=QLurl, ClientID=ClientID, ClientSecret=ClientSecret)
            return QLurl, qltoken
        except Exception as e:
            raise Exception(f"获取Token失败: {str(e)}")

    except Exception as e:
        sender.reply(f"""
======连接失败======
❌ 无法连接{'呆呆' if panel_type == 'daidai' else '青龙'}面板
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
==================""")
        exit(0)


def QLtoken(QLurl, ClientID, ClientSecret):  # 获取青龙token
    try:
        url = f'{QLurl}/open/auth/token?client_id={ClientID}&client_secret={ClientSecret}'
        response = requests.get(url)

        if response.status_code != 200:
            sender.reply(f"""
======请求失败======
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
======认证失败======
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
======网络错误======
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
======系统错误======
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
            sender.reply(f"""
======请求失败======
❌ 呆呆面板API请求失败
------------------
状态码: {response.status_code}
请检查:
• API地址是否正确
• 面板是否正常运行
==================""")
            exit(0)

        result = response.json()
        access_token = result.get('data', {}).get('access_token')
        if access_token:
            return access_token
        sender.reply("""
======认证失败======
❌ 获取Token失败
------------------
请检查:
• AppKey是否正确
• AppSecret是否正确
• 应用是否有权限
==================""")
        exit(0)
    except requests.exceptions.RequestException as e:
        sender.reply(f"""
======网络错误======
❌ 连接呆呆面板失败
------------------
请检查:
• 呆呆地址是否正确
• 网络是否正常
• 错误信息: {str(e)}
==================""")
        exit(0)
    except Exception as e:
        sender.reply(f"""
======系统错误======
❌ 处理请求时出错
------------------
请检查:
• 配置格式是否正确
• 错误信息: {str(e)}
==================""")
        exit(0)


QLurl, qltoken = seekql()
use_daidai = normalize_panel_type(sg.bucketGet(bucket='dd_pp', key='panel_type') or '') == 'daidai'


def login(refresh_token):
    try:
        url = 'https://cauth.pupuapi.com/clientauth/user/refresh_token'
        h = {
            "User-Agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.46(0x18002e2c) NetType/WIFI Language/zh_CN miniProgram/wx122ef876a7132eb4'
        }
        data = {
            'refresh_token': refresh_token
        }

        response = requests.put(url=url, json=data, headers=h).json()
        access_token = response['data']['access_token']
        refresh_token = response['data']['refresh_token']
        user_id = response['data']['user_id']
        url = "https://cauth.pupuapi.com/clientauth/user/info"
        h['Authorization'] = f"Bearer {access_token}"
        response = requests.get(url, headers=h)
        r = response.json()

        mobile = r['data']['phone']
        nick_name = r['data']['nick_name']
        mobile = mobile[:3] + "****" + mobile[7:]
        return mobile, nick_name, refresh_token, access_token, user_id
    except Exception:
        return 'Token过期', 'Token过期', 'Token过期', 'Token过期', 'Token过期'


def Addfiles(filespath, content):
    try:
        path, filename, full_path = split_script_path(filespath)
        headers = {
            'accept': 'application/json',
            'Authorization': f"Bearer {qltoken}",
        }

        if use_daidai:
            response = requests.put(
                f'{QLurl}/api/scripts/content',
                headers={**headers, 'Content-Type': 'application/json'},
                json={'path': full_path, 'content': content}
            )
            if response.status_code != 200:
                sender.reply(f"""
======保存失败======
❌ 无法保存到呆呆面板
------------------
状态码: {response.status_code}
==================""")
                exit(0)
        else:
            url = f'{QLurl}/open/scripts'
            json_data = {
                'filename': filename,
                'path': path,
                'content': content,
            }

            response = requests.post(url, headers=headers, json=json_data)
            result = response.json()

            if result['code'] != 200:
                sender.reply(f"""
======保存失败======
❌ 无法保存到青龙
------------------
错误代码: {result['code']}
错误信息: {result.get('message', '未知错误')}
==================""")
                exit(0)

    except Exception as e:
        sender.reply(f"""

=====系统错误======
❌ 保存文件时出错
------------------
错误信息: {str(e)}
==================""")
        exit(0)


def lookfiles(filespath):
    try:
        path, file, full_path = split_script_path(filespath)
        headers = {
            'accept': 'application/json',
            'Authorization': f"Bearer {qltoken}",
        }

        if use_daidai:
            list_response = requests.get(f"{QLurl}/api/scripts", headers=headers)
            if list_response.status_code != 200:
                sender.reply("❌ 无法读取呆呆面板脚本列表")
                exit(0)

            scripts = list_response.json().get('data', []) or []
            normalized_paths = {str(item.get('path', '')).replace('\\', '/').strip('/') for item in scripts}
            if full_path not in normalized_paths:
                return ''

            response = requests.get(f"{QLurl}/api/scripts/content", headers=headers, params={"path": full_path})
            if response.status_code != 200:
                sender.reply("❌ 无法读取呆呆面板脚本内容")
                exit(0)
            result = response.json()
            return result.get('data', {}).get('content', '') or ''
        else:
            url = f"{QLurl}/open/scripts/{file}"
            response = requests.get(url, headers=headers, params={"path": path})
            result = response.json()

            if result['code'] == 200:
                return result['data']
            else:
                sender.reply(f"""
==================
    读取失败
==================
❌ 无法读取青龙文件
------------------
错误代码: {result['code']}
错误信息: {result.get('message', '未知错误')}
==================""")
                exit(0)

    except Exception as e:
        sender.reply(f"""
==================
    系统错误
==================
❌ 读取文件时出错
------------------
错误信息: {str(e)}
==================""")
        exit(0)


def ScanCodeLogin():
    try:
        scan_msg = """
=====微信扫码登录=====
⌛ 正在加载二维码...
⏳ 请稍候...
=================="""
        sender.reply(scan_msg)

        url_getQr = 'https://wxsm.linzixuan.top/api/getQr'
        url_checkQr = 'https://wxsm.linzixuan.top/api/checkQr'
        response = requests.post(url_getQr, json={'project': 'ppcs'})
        response_data = response.json()
        if not response_data.get('data') or 'uuid' not in response_data['data']:
            sender.reply('❌ 获取二维码失败!')
            exit(0)

        QRcode = response_data['data']['uuid']
        QRcodeImg = response_data['data']['img_url']

        sender.replyImage(QRcodeImg)

        scan_guide = """
=====登录说明=====
📱 请使用微信扫描二维码登录
------------------
⚠️ 注意事项:
1. 请确保已用微信登录过朴朴APP和微信小程序
2. 如果登录失败,请先下载朴朴APP和登录小程序
=================="""
        sender.reply(scan_guide)

        retry = 60
        while True:
            time.sleep(1)
            try:
                data = {'project': 'ppcs', 'uuid': QRcode}
                response = requests.post(url_checkQr, json=data, timeout=5)
                response_data = response.json()

                if response_data.get('code') == 0 and response_data.get('data', {}).get('code'):
                    code = response_data['data']['code']
                    break
            except Exception:
                pass

            retry -= 1
            if retry == 0:
                sender.reply('❌ 扫码超时,请重新尝试!')
                exit(0)

        url = "https://cauth.pupuapi.com/clientauth/user/society/wechat/login"
        params = {
            'user_society_type': "11"
        }

        payload = json.dumps({
            "code": code,
            "user_device": {
                "app_version": 400804,
                "device_model": "MEIZU 20",
                "device_os": 10,
                "device_token": "",
                "mac_address": ""
            }
        })

        headers = {
            'User-Agent': "Pupumall/4.8.4;Android/13;",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'pp-version': "2023022500",
            'pp-os': "10",
            'pp_store_city_zip': "440100",
            'pp-elder-mode': "false",
            'Content-Type': "application/json; charset=UTF-8"
        }

        response = requests.post(url, params=params, data=payload, headers=headers)
        refresh_token = response.json()['data']['refresh_token']
        return refresh_token

    except Exception:
        sender.reply('❌ 获取扫码登录接口失败，请联系呆呆！')
        exit(0)


def bind():
    Adminvalue = lookfiles(filespath)
    sender.reply("""
=====朴朴超市登录=====
[1] 扫码登录
[2] CK登录
------------------
回复数字选择方式
回复"q"退出操作
==================""")

    input_choice = sender.input(120000, 1, False)
    if input_choice == 'q' or input_choice == 'Q':
        sender.reply("✅ 已退出登录")
        exit(0)
    elif input_choice == 'timeout':
        sender.reply("⏰ 操作超时,已退出")
        exit(0)

    if input_choice == '1':
        refresh_token = ScanCodeLogin()
    elif input_choice == '2':
        sender.reply("""
=====朴朴CK登录=====
请输入refresh_token:
------------------
💡 可通过以下方式获取:
1. 抓包获取
2. 扫码后复制
==================""")
        ck_input = sender.input(120000, 1, False)
        if ck_input == 'q' or ck_input == 'Q':
            sender.reply("✅ 已退出登录")
            exit(0)
        elif ck_input == 'timeout':
            sender.reply("⏰ 操作超时,已退出")
            exit(0)
        refresh_token = ck_input
    else:
        sender.reply("❌ 输入无效")
        exit(0)

    mobile, nick_name, refresh_token, access_token, user_id = login(refresh_token)
    if mobile == 'Token过期':
        sender.reply(f"""
=====账号状态=====
📱 账号: {mobile}
❌ Token已过期
==================""")
        exit(0)
    sg.bucketSet(bucket='dd_pp_mobile', key=user_id, value=mobile)
    if len(uservalue) == 0:
        accounts = []
        accounts.append(user_id)
        new_line = f'{refresh_token}#By 朴朴管理丨朴朴:{mobile}丨用户:{userid}丨身份id:{user_id}'
        if user_id in Adminvalue:
            Adminvalue = "\n".join(new_line if user_id in line else line for line in Adminvalue.split("\n"))
        else:
            Adminvalue = f'{Adminvalue}\n{new_line}'
        sg.bucketSet(bucket='dd_pp_user', key=userid, value=f'{accounts}')
        Addfiles(filespath=filespath, content=Adminvalue)
        sender.reply(f"""
=====账号添加成功=====
📱 账号: {mobile}
✅ 状态: 添加成功
==================""")
    else:
        accounts = _sg_literal(uservalue)
        new_line = f'{refresh_token}#By 朴朴管理丨朴朴:{mobile}丨用户:{userid}丨身份id:{user_id}'
        if user_id in Adminvalue:
            Adminvalue = "\n".join(new_line if user_id in line else line for line in Adminvalue.split("\n"))
            Addfiles(filespath=filespath, content=Adminvalue)
            sender.reply(f"""
=====账号更新成功=====
📱 账号: {mobile}
✅ 状态: 更新成功
==================""")
        else:
            Adminvalue = f'{Adminvalue}\n{new_line}'
            Addfiles(filespath=filespath, content=Adminvalue)
            sender.reply(f"""
=====账号添加成功=====
📱 账号: {mobile}
✅ 状态: 添加成功
==================""")
        if user_id not in accounts:
            accounts.append(user_id)
            sg.bucketSet(bucket='dd_pp_user', key=userid, value=f'{accounts}')


def coin(access_token):
    try:
        url = "https://j1.pupuapi.com/client/coin"

        headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 13; MEIZU 20 Build/TKQ1.221114.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/108.0.5359.128 Mobile Safari/537.36 D/d53f198d94ef00ec424d9aac9b0db734",
            'Accept': "application/json, text/plain, */*",
            'Accept-Encoding': "gzip, deflate",
            'Authorization': f"Bearer {access_token}"
        }
        response = requests.get(url, headers=headers)
        balance = response.json()['data']['balance']
        url = "https://j1.pupuapi.com/client/coin/record"
        params = {
            'page': "1",
            'size': "20"
        }

        response = requests.get(url, params=params, headers=headers)
        data = response.json()['data']
        todaycoin = 0
        if len(data) != 0:
            for coinjson in data:
                time_create = coinjson['time_create']
                timestamp = time_create / 1000
                cointime = str(datetime.fromtimestamp(timestamp))
                if today_time in cointime:
                    types = coinjson['type']
                    if types == 0:
                        coins = coinjson['value']
                        todaycoin += coins
                else:
                    continue
        return balance, todaycoin
    except Exception:
        sender.reply("""
=====积分查询失败=====
❌ 无法获取积分信息
------------------
💡 请稍后重试
==================""")
        return '查询失败', '0'


def push(user, account, c):
    mobile = sg.bucketGet(bucket='dd_pp_mobile', key=account)
    if not mobile:
        mobile = account
    mobile = mobile[:3] + "****" + mobile[7:]

    push_msg = f"""
=====朴朴超市通知=====
📱 账号: {mobile}
📢 消息: {c}
===================="""

    sg.push('wb', '', user, '', push_msg)
    sg.push('tg', '', user, '', push_msg)
    sg.push('qq', '', user, '', push_msg)
    sg.push('qb', '', user, '', push_msg)
    sg.push('wx', '', user, '', push_msg)


def cx():
    if len(uservalue) != 0:
        data = lookfiles(filespath)
        accounts = _sg_literal(uservalue)
        for account in accounts:
            mobiles = sg.bucketGet(bucket='dd_pp_mobile', key=account)
            if account not in data:
                if sender.getImtype() == 'fake':
                    push(userid, account, """
⚠️ 账号状态异常
------------------
❌ Token已失效
💡 请尽快登录更新
------------------
发送"朴朴登录"进行更新""")
                else:
                    sender.reply(f"""
=====账号状态=====
📱 账号: {mobiles}
❌ Token已失效
==================""")
            else:
                result = [line.strip().split("#")[0] for line in data.split("\n") if account in line][0]
                mobile, nick_name, refresh_token, access_token, user_id = login(result)
                if mobile == 'Token过期':
                    if sender.getImtype() == 'fake':
                        push(userid, account, """
⚠️ 账号状态异常
------------------
❌ Token已过期
💡 请尽快登录更新
------------------
发送"朴朴登录"进行更新""")
                    else:
                        sender.reply(f"""
=====账号状态=====
📱 账号: {mobiles}
❌ Token已过期
==================""")
                    continue

                if refresh_token != result:
                    new_line = f'{refresh_token}#By 朴朴管理丨朴朴:{mobile}丨用户:{userid}丨身份id:{account}'
                    updated_content = "\n".join(new_line if account in line else line for line in data.split("\n"))
                    Addfiles(filespath=filespath, content=updated_content)

                balance, todaycoin = coin(access_token)
                if sender.getImtype() == 'fake':
                    last_balance = sg.bucketGet('dd_pp_balance', account) or '0'
                    if last_balance != str(balance):
                        sg.bucketSet('dd_pp_balance', account, str(balance))
                        if int(balance) > int(last_balance):
                            change = int(balance) - int(last_balance)
                            push(userid, account, f"""
💫 积分变动提醒
------------------
📈 积分增加: +{change}
💰 当前积分: {balance}
------------------
发送"朴朴查询"查看详情""")
                else:
                    sender.reply(f"""
=====账号详情=====
📱 账号: {mobile}
🎈 当前积分: {balance}
✨ 今日积分: {todaycoin}
==================""")
    else:
        if sender.getImtype() != 'fake':
            sender.reply("""
=====未绑定账号=====
❌ 未找到任何账号信息
------------------
💡 发送 朴朴登录 绑定
==================""")


def manage():
    if len(uservalue) == 0:
        sender.reply("""
=====未绑定账号=====
❌ 未找到任何账号信息
------------------
💡 发送 朴朴登录 绑定
==================""")
        return

    accounts = _sg_literal(uservalue)
    data = lookfiles(filespath)

    account_list = """
=====朴朴账号管理====="""
    for i, account in enumerate(accounts, 1):
        mobile = sg.bucketGet(bucket='dd_pp_mobile', key=account)
        if not mobile:
            mobile = account
        mobile = mobile[:3] + "****" + mobile[7:]

        if account not in data:
            status = "❌ Token已失效"
        else:
            result = [line.strip().split("#")[0] for line in data.split("\n") if account in line][0]
            mobile, nick_name, refresh_token, access_token, user_id = login(result)
            if mobile == 'Token过期':
                status = "❌ Token已过期"
            else:
                balance, todaycoin = coin(access_token)
                status = f"💰 积分: {balance}"

        account_list += f"""
------------------
[{i}] 账号信息
📱 账号: {mobile}
{status}"""

    account_list += """
------------------
回复序号选择账号
回复"q"退出操作
=================="""

    sender.reply(account_list)

    user_input = sender.input(120000, 1, False)
    if user_input == 'timeout':
        sender.reply("⏰ 操作超时,已退出")
        return
    elif user_input == '0' or user_input.lower() == 'q':
        sender.reply("✅ 已退出管理")
        return

    try:
        index = int(user_input) - 1
        if 0 <= index < len(accounts):
            account = accounts[index]
            mobile = sg.bucketGet(bucket='dd_pp_mobile', key=account)
            if not mobile:
                mobile = account
            mobile = mobile[:3] + "****" + mobile[7:]

            if account not in data:
                sender.reply(f"""
=====账号状态=====
📱 账号: {mobile}
❌ Token已失效
==================""")
            else:
                result = [line.strip().split("#")[0] for line in data.split("\n") if account in line][0]
                mobile, nick_name, refresh_token, access_token, user_id = login(result)
                if mobile == 'Token过期':
                    sender.reply(f"""
=====账号状态=====
📱 账号: {mobile}
❌ Token已过期
==================""")
                else:
                    balance, todaycoin = coin(access_token)
                    sender.reply(f"""
=====账号详情=====
📱 账号: {mobile}
👤 昵称: {nick_name}
🎈 当前积分: {balance}
✨ 今日积分: {todaycoin}
==================""")

                    menu = """
=====账号管理=====
[1] 更新账号
[2] 删除账号
------------------
回复数字选择功能
回复"q"退出操作
=================="""
                    sender.reply(menu)

                    choice = sender.input(120000, 1, False)
                    if choice == '1':
                        new_line = f'{refresh_token}#By 朴朴管理丨朴朴:{mobile}丨用户:{userid}丨身份id:{account}'
                        updated_content = "\n".join(new_line if account in line else line for line in data.split("\n"))
                        Addfiles(filespath=filespath, content=updated_content)
                        sender.reply(f"""
=====更新成功=====
📱 账号: {mobile}
✅ 状态: 已更新
==================""")
                    elif choice == '2':
                        confirm_msg = """
=====警告=====
确定要删除该账号吗？
此操作不可恢复！
------------------
[y] 确认删除
[n] 取消操作
=================="""
                        sender.reply(confirm_msg)

                        confirm = sender.input(120000, 1, False)
                        if confirm.lower() == 'y':
                            accounts.remove(account)
                            if len(accounts) == 0:
                                sg.bucketDel(bucket='dd_pp_user', key=userid)
                            else:
                                sg.bucketSet(bucket='dd_pp_user', key=userid, value=f'{accounts}')

                            new_content = '\n'.join(line for line in data.split('\n') if account not in line)
                            Addfiles(filespath=filespath, content=new_content)

                            sender.reply(f"""
=====删除成功=====
📱 账号: {mobile}
✅ 状态: 已删除
==================""")
                        else:
                            sender.reply("✅ 已取消删除")
                    elif choice == 'q':
                        sender.reply("✅ 已退出管理")
                    else:
                        sender.reply("❌ 无效的操作指令")
        else:
            sender.reply("❌ 无效的账号序号")
    except ValueError:
        sender.reply("❌ 无效的输入格式")


def refresh_all_tokens():
    if len(uservalue) == 0:
        sender.reply("""
=====未绑定账号=====
❌ 未找到任何账号信息
------------------
💡 发送 朴朴登录 绑定
==================""")
        return

    sender.reply("""
=====开始刷新Token=====
⏳ 正在刷新所有账号...
==================""")

    accounts = _sg_literal(uservalue)
    data = lookfiles(filespath)

    success_count = 0
    fail_count = 0
    fail_list = []

    for account in accounts:
        mobile = sg.bucketGet(bucket='dd_pp_mobile', key=account)
        if not mobile:
            mobile = account
        mobile_display = mobile[:3] + "****" + mobile[7:]

        if account not in data:
            fail_count += 1
            fail_list.append(f"{mobile_display} (Token已失效)")
            continue

        try:
            result = [line.strip().split("#")[0] for line in data.split("\n") if account in line][0]

            mobile, nick_name, new_refresh_token, access_token, user_id = login(result)

            if mobile == 'Token过期':
                fail_count += 1
                fail_list.append(f"{mobile_display} (Token已过期)")
                continue

            if new_refresh_token != result:
                new_line = f'{new_refresh_token}#By 朴朴管理丨朴朴:{mobile}丨用户:{userid}丨身份id:{account}'
                data = "\n".join(new_line if account in line else line for line in data.split("\n"))

            success_count += 1

        except Exception:
            fail_count += 1
            fail_list.append(f"{mobile_display} (刷新失败)")

    if success_count > 0:
        Addfiles(filespath=filespath, content=data)

    report = f"""
=====刷新完成=====
✅ 成功: {success_count}个账号
❌ 失败: {fail_count}个账号
------------------"""

    if fail_list:
        report += "\n失败账号列表:"
        for fail_info in fail_list:
            report += f"\n• {fail_info}"
        report += "\n------------------"

    report += """
💡 失败的账号请重新登录
=================="""

    sender.reply(report)


usermessage = sender.getMessage()
today_date = datetime.now().date()
today_time = str(today_date)
imtype = sender.getImtype()

if '登录' in usermessage:
    bind()
elif '查询' in usermessage:
    cx()
elif '管理' in usermessage:
    manage()
elif '刷新' in usermessage:
    refresh_all_tokens()
elif imtype == 'fake':
    cx()  # 执行定时任务检查
