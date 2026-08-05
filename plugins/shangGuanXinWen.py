# [title: 上观新闻]
# [name: shangGuanXinWen]
# [language: python]
# [class: 任务]
# [author: rujingxianghai]
# [version: v1.1.2]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(上观|sgxw)(登录|登陆)$|^登(录|陆)(上观|sgxw)$|^(上观|sgxw)(查询|管理)$|^(查询|管理)(上观|sgxw)$|^清理上观$|^上观$|^上观教程$]
# [icon: https://y.gtimg.cn/music/photo_new/T053M000001NYort1rZecQ.png]
# [description: 。]
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
    'sgxw_config_sgxw_qlname': form.string().title('设置对接容器').default('').description('你的变量需要添加到的容器？参数用丨分割'),
    'sgxw_config_sgxw_osname': form.string().title('提交到青龙的变量名').default('').description('青龙容器内上观新闻的变量名'),
    'sgxw_config_fixed_token': form.string().title('登录签名Token').default('').description('上观登录接口签名Token'),
})
_CONFIG_FIELD_MAP = {
    ('sgxw_config', 'sgxw_qlname'): 'sgxw_config_sgxw_qlname',
    ('sgxw_config', 'sgxw_osname'): 'sgxw_config_sgxw_osname',
    ('sgxw_config', 'fixed_token'): 'sgxw_config_fixed_token',
}

import os
import json
import time
import hashlib
import requests
from datetime import datetime

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()
uservalue = sg.bucketGet(bucket='sgxw_user', key=userid)

BASE_URL = "https://services.shobserver.cn"
FIXED_TOKEN = ""

PLUGIN_CONFIG = {
    'bucket': 'sgxw_config',
    'coin_key': 'sgxwcoin',
    'name': '上观新闻'
}


def get_user_content():
    sgxw_osname = sg.bucketGet('sgxw_config', 'sgxw_osname') or 'S_SGXW'
    sgxw_qlname = sg.bucketGet('sgxw_config', 'sgxw_qlname') or 'S_SGXW'
    sgxw_managecommand = sg.bucketGet('sgxw_config', 'sgxw_managecommand') or '上观管理'
    sgxw_querycommand = sg.bucketGet('sgxw_config', 'sgxw_querycommand') or '上观查询'
    sgxw_signcommand = sg.bucketGet('sgxw_config', 'sgxw_signcommand') or '上观登录'

    randommanagecommand = sgxw_managecommand
    randomquerycommand = sgxw_querycommand
    randomsigncommand = sgxw_signcommand

    sgxwVipmoney = float(sg.bucketGet('sgxw_config', 'sgxwVipmoney') or '1')

    sgxwcoin = sg.bucketGet(PLUGIN_CONFIG['bucket'], PLUGIN_CONFIG['coin_key'])
    if not sgxwcoin:
        sgxwcoin = sg.bucketGet('sgxw_config', 'sgxwcoin') or '0'
    sgxwcoin = int(sgxwcoin)

    return (sgxw_osname, sgxw_qlname, randommanagecommand,
            randomquerycommand, randomsigncommand, sgxwVipmoney, sgxwcoin)

def mask_phone(phone):
    if not phone or len(phone) != 11:
        return phone
    return f"{phone[:3]}****{phone[7:]}"


def generate_signature(raw_str: str) -> str:
    try:
        return hashlib.md5(raw_str.encode(), usedforsecurity=True).hexdigest()
    except TypeError:
        return hashlib.md5(raw_str.encode()).hexdigest()

def verify_account(username, password):
    try:
        timestamp = int(time.time() * 1000)
        fixed_token = sg.bucketGet("sgxw_config", "fixed_token") or FIXED_TOKEN
        if not fixed_token:
            return {"success": False, "message": "未配置登录签名Token"}
        sign_str = f"{username}${timestamp}${fixed_token}"
        sign = generate_signature(sign_str)

        data = {
            "mobile": username,
            "password": password,
            "times": timestamp,
            "sign": sign
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "okhttp/4.10.0",
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive"
        }

        response = requests.post(f"{BASE_URL}/user/login", data=data, headers=headers, timeout=10, verify=False)
        result = response.json()

        if result.get("breturn", False):
            user_id = result.get("object", {}).get("id", "")
            score = result.get("object", {}).get("score", "未知")
            return {
                "success": True,
                "message": "登录成功",
                "user_id": user_id,
                "score": score
            }
        else:
            return {
                "success": False,
                "message": result.get('errorinfo', '登录失败，请检查账号密码')
            }

    except Exception as e:
        print(f"验证账号失败: {str(e)}")
        return {"success": False, "message": str(e)}

def bind_account():
    sender.reply("""
=====上观新闻登录=====
请按照提示依次输入账号信息
回复"q"随时退出操作
==================""")

    sender.reply("请输入手机号（上观新闻登录账号）:")
    username = sender.input(120000, 1, False)
    if not username:
        sender.reply("⏰ 操作超时,已退出")
        return
    elif username.lower() == 'q':
        sender.reply("✅ 已取消登录")
        return

    if not username.isdigit() or len(username) != 11:
        sender.reply("""
=====格式错误=====
❌ 手机号格式不正确
------------------
请输入11位数字手机号
==================""")
        return

    sender.reply("请输入密码（上观新闻登录密码）:")
    password = sender.input(120000, 1, False)
    if not password:
        sender.reply("⏰ 操作超时,已退出")
        return
    elif password.lower() == 'q':
        sender.reply("✅ 已取消登录")
        return

    sender.reply("请输入备注名称（用于区分不同账号）:")
    remark = sender.input(120000, 1, False)
    if not remark:
        sender.reply("⏰ 操作超时,已退出")
        return
    elif remark.lower() == 'q':
        sender.reply("✅ 已取消登录")
        return

    try:
        login_result = verify_account(username, password)
        if login_result.get('success'):
            user_id = login_result.get('user_id')
            score = login_result.get('score')

            if not uservalue:
                sg.bucketSet('sgxw_user', userid, str([username]))
            else:
                accounts = _sg_literal(uservalue)
                if username not in accounts:
                    accounts.append(username)
                    sg.bucketSet('sgxw_user', userid, str(accounts))

            account_info = {
                "username": username,
                "password": password,
                "remark": remark,
                "user_id": user_id
            }
            sg.bucketSet('sgxw_token', username, json.dumps(account_info))

            success_msg = f"""
=====绑定成功=====
👤 备注: {remark}
📱 手机号: {mask_phone(username)}
🪙 当前积分: {score}
=================="""
            sender.reply(success_msg)

            authorize_account(username, account_info)

        else:
            sender.reply(f"""
=====验证失败=====
❌ 原因: {login_result.get('message', '未知错误')}
请检查账号密码是否正确
==================""")

    except Exception as e:
        sender.reply(f"""
=====绑定异常=====
❌ 错误: {str(e)}
请重试或检查配置
==================""")

def query_accounts():
    if not uservalue:
        sender.reply(f"""
=====未绑定账号=====
❌ 未找到任何账号信息
💡 发送 {randomsigncommand} 绑定
==================""")
        return

    accounts = _sg_literal(uservalue)
    account_list = """
========选择账号=======
[0] 全部账号"""

    for i, username in enumerate(accounts, 1):
        account_info = json.loads(sg.bucketGet('sgxw_token', username))
        remark = account_info.get('remark', username)
        auth_time = '2099-12-31'

        if not auth_time:
            auth_status = '未授权'
        elif auth_time < str(datetime.now().date()):
            auth_status = '已过期'
        else:
            auth_status = f'到期:{auth_time}'

        account_list += f"""
[{i}]{mask_phone(username)}({remark}, {auth_status})"""

    account_list += """
=====================
支持多选，用英文逗号分隔
例如: 1,2,3
回复"q"退出操作
====================="""

    sender.reply(account_list)

    choice = sender.input(120000, 1, False)
    if not choice or choice.lower() == 'q':
        sender.reply("✅ 已退出查询")
        return

    try:
        selected_accounts = []

        if choice == '0':
            selected_accounts = accounts.copy()
        else:
            indices = choice.split(',')
            for idx in indices:
                idx = idx.strip()
                if not idx.isdigit():
                    continue

                index = int(idx) - 1
                if 0 <= index < len(accounts):
                    selected_accounts.append(accounts[index])

        if not selected_accounts:
            sender.reply("❌ 未选择有效账号")
            return

        sender.reply(f"✅ 已选择 {len(selected_accounts)} 个账号，正在查询...")

        query_count = 0
        for username in selected_accounts:
            try:
                account_info = json.loads(sg.bucketGet('sgxw_token', username))
                password = account_info.get('password', '')

                login_result = verify_account(username, password)

                if login_result.get('success'):
                    account_info['user_id'] = login_result.get('user_id', '')
                    sg.bucketSet('sgxw_token', username, json.dumps(account_info))

                    auth_time = '2099-12-31'
                    auth_status = '已授权' if auth_time and auth_time >= str(datetime.now().date()) else '未授权'

                    account_info_msg = f"""
=====账号信息[{query_count+1}/{len(selected_accounts)}]=====
📱 手机号: {mask_phone(username)}
👤 备注: {account_info.get('remark')}
🔐 授权状态: {auth_status}
🪙 当前积分: {login_result.get('score', '未知')}
=================="""
                    sender.reply(account_info_msg)
                    query_count += 1

                    if query_count < len(selected_accounts) and len(selected_accounts) > 3:
                        time.sleep(0.5)

                else:
                    sender.reply(f"""
=====查询失败[{query_count+1}/{len(selected_accounts)}]=====
📱 手机号: {mask_phone(username)}
❌ 状态: {login_result.get('message', '账号验证失败')}
==================""")
                    query_count += 1

            except Exception as e:
                sender.reply(f"""
=====查询异常[{query_count+1}/{len(selected_accounts)}]=====
📱 手机号: {mask_phone(username)}
❌ 错误: {str(e)}
==================""")
                query_count += 1

        if query_count > 0:
            sender.reply(f"✅ 查询完成，共查询了 {query_count} 个账号")

    except Exception as e:
        sender.reply(f"❌ 查询失败: {str(e)}")

def manage_account():
    if not uservalue:
        sender.reply(f"""
=====未绑定账号=====
❌ 未找到任何账号信息
💡 发送 {randomsigncommand} 绑定
==================""")
        return

    accounts = _sg_literal(uservalue)

    menu = """
=====账号管理=====
[1] 授权账号
[2] 删除账号
[3] 提交青龙
------------------
回复数字选择功能
回复"q"退出操作
=================="""
    sender.reply(menu)

    choice = sender.input(120000, 1, False)
    if not choice or choice.lower() == 'q':
        sender.reply("✅ 已退出操作")
        return

    account_list = """
========选择账号=======
[0] 全部账号"""

    for i, username in enumerate(accounts, 1):
        account_info = json.loads(sg.bucketGet('sgxw_token', username))
        remark = account_info.get('remark', username)
        auth_time = '2099-12-31'

        if not auth_time:
            auth_status = '未授权'
        elif auth_time < str(datetime.now().date()):
            auth_status = '已过期'
        else:
            auth_status = f'到期:{auth_time}'

        account_list += f"""
[{i}]{mask_phone(username)}({remark}, {auth_status})"""

    account_list += """
=====================
支持多选，用英文逗号分隔
例如: 1,2,3
回复"q"退出操作
====================="""

    sender.reply(account_list)

    account_choice = sender.input(120000, 1, False)
    if not account_choice or account_choice.lower() == 'q':
        sender.reply("✅ 已退出操作")
        return

    try:
        selected_accounts = []

        if account_choice == '0':
            selected_accounts = accounts.copy()
        else:
            indices = account_choice.split(',')
            for idx in indices:
                idx = idx.strip()
                if not idx.isdigit():
                    continue

                index = int(idx) - 1
                if 0 <= index < len(accounts):
                    selected_accounts.append(accounts[index])

        if not selected_accounts:
            sender.reply("❌ 未选择有效账号")
            return

        sender.reply(f"✅ 已选择 {len(selected_accounts)} 个账号")

        if choice == '1':
            authorize_multiple_accounts(selected_accounts)

        elif choice == '2':
            confirm = """
=====确认删除=====
⚠️ 此操作不可恢复
------------------
回复 y 确认删除
回复 n 取消操作
=================="""
            sender.reply(confirm)

            confirm = sender.input(120000, 1, False)
            if confirm.lower() == 'y':
                success_count = 0
                for username in selected_accounts:
                    try:
                        if username in accounts:
                            accounts.remove(username)

                        sg.bucketDel('sgxw_token', username)
                        True

                        delete_ql_env(username)
                        success_count += 1
                    except Exception as e:
                        print(f"删除账号失败: {username}, 错误: {str(e)}")

                if accounts:
                    sg.bucketSet('sgxw_user', userid, str(accounts))
                else:
                    sg.bucketDel('sgxw_user', userid)

                sender.reply(f"✅ 已成功删除 {success_count}/{len(selected_accounts)} 个账号")
            else:
                sender.reply("✅ 已取消删除")

        elif choice == '3':
            success_count = 0
            for username in selected_accounts:
                try:
                    account_info = json.loads(sg.bucketGet('sgxw_token', username))

                    auth_time = '2099-12-31'
                    if auth_time and auth_time >= str(datetime.now().date()):
                        if update_ql_env(username, account_info):
                            success_count += 1
                    else:
                        print(f"账号未授权或已过期: {username}")
                except Exception as e:
                    print(f"提交青龙失败: {username}, 错误: {str(e)}")

            sender.reply(f"""
=====提交结果=====
📊 选择账号: {len(selected_accounts)}个
✅ 提交成功: {success_count}个
❌ 提交失败: {len(selected_accounts) - success_count}个
------------------
💡 提示: 未授权账号无法提交
==================""")
        else:
            sender.reply("❌ 无效的选择")

    except Exception as e:
        sender.reply(f"❌ 操作失败: {str(e)}")

def authorize_multiple_accounts(usernames):
    return True

def authorize_account(username, account_info):
    return True


def get_ql_token(host, client_id, client_secret):
    try:
        url = f'{host}/open/auth/token?client_id={client_id}&client_secret={client_secret}'
        response = requests.get(url)
        data = response.json()
        if data.get('code') == 200:
            return data['data']['token']
        return None
    except:
        return None

def Addenvs(username, env_value, env_name="S_SGXW", account_info=None):
    try:
        qlconfig = sg.bucketGet('sgxw_config', 'sgxw_qlname')
        if not qlconfig:
            print("未配置青龙信息")
            return False, "未配置青龙信息"

        qlconfig = qlconfig.replace('|', '丨')
        configs = qlconfig.split('丨')
        if len(configs) < 3:
            print("青龙配置格式错误")
            return False, "青龙配置格式错误"

        host = configs[0].strip()
        client_id = configs[1].strip()
        client_secret = configs[2].strip()

        url = f'{host}/open/auth/token?client_id={client_id}&client_secret={client_secret}'
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                error_msg = f"获取青龙token失败: {response.text}"
                print(error_msg)
                return False, error_msg

            result = response.json()
            if result['code'] != 200:
                error_msg = f"获取青龙token失败: {result.get('message')}"
                print(error_msg)
                return False, error_msg

            token = result['data']['token']
            headers = {'Authorization': f'Bearer {token}'}
        except Exception as e:
            error_msg = f"获取青龙token异常: {str(e)}"
            print(error_msg)
            return False, error_msg

        try:
            envs_response = requests.get(f'{host}/open/envs', headers=headers, timeout=10)
            if envs_response.status_code != 200:
                error_msg = f"获取环境变量失败: {envs_response.text}"
                print(error_msg)
                return False, error_msg

            envs_data = envs_response.json()
            if envs_data.get('code') != 200:
                error_msg = f"获取环境变量失败: {envs_data.get('message')}"
                print(error_msg)
                return False, error_msg

            envs = envs_data['data']

            for env in envs:
                if env['name'] == env_name and username in env['value']:
                    env_id = env.get('_id') or env.get('id')
                    if env_id:
                        delete_response = requests.delete(f'{host}/open/envs', headers=headers, json=[env_id], timeout=10)
                        if delete_response.status_code != 200:
                            print(f"删除旧变量失败: {delete_response.text}")
                    break
        except Exception as e:
            error_msg = f"查询环境变量异常: {str(e)}"
            print(error_msg)

        if account_info is None:
            try:
                account_info = json.loads(sg.bucketGet('sgxw_token', username))
            except:
                account_info = {}

        user_id = account_info.get('user_id', '')
        auth_time = '2099-12-31' or '未授权'

        data = [{
            'name': env_name,
            'value': f"{env_value}",
            'remarks': f"上观UID：{user_id}|到期:{auth_time}"
        }]

        try:
            add_response = requests.post(f'{host}/open/envs', headers=headers, json=data, timeout=10)
            if add_response.status_code != 200:
                error_msg = f"添加变量失败: {add_response.text}"
                print(error_msg)
                return False, error_msg

            add_result = add_response.json()
            if add_result.get('code') != 200:
                error_msg = f"添加变量失败: {add_result.get('message')}"
                print(error_msg)
                return False, error_msg

            new_id = None
            if 'data' in add_result and add_result['data'] and len(add_result['data']) > 0:
                new_id = add_result['data'][0].get('_id') or add_result['data'][0].get('id')

            if new_id:
                enable_response = requests.put(f'{host}/open/envs/enable', headers=headers, json=[new_id], timeout=10)
                if enable_response.status_code != 200:
                    print(f"启用变量失败: {enable_response.text}")
            else:
                print("未找到变量ID，跳过启用步骤")

            return True, "更新成功"
        except Exception as e:
            error_msg = f"添加变量异常: {str(e)}"
            print(error_msg)
            return False, error_msg

    except Exception as e:
        error_msg = f"更新青龙变量异常: {str(e)}"
        print(error_msg)
        return False, error_msg

def update_ql_env(username, account_info):
    password = account_info.get('password', '')
    user_id = account_info.get('user_id', '')
    remark = account_info.get('remark', '')

    if not password or not user_id:
        print("更新青龙变量失败: 账号信息不完整")
        return False

    env_value = f"{remark}#{username}#{password}"

    success, message = Addenvs(username, env_value, "S_SGXW", account_info)
    if not success:
        print(f"更新青龙变量失败: {message}")
    return success

def delete_ql_env(username, env_name="S_SGXW"):
    try:
        ql_config = sg.bucketGet('sgxw_config', 'sgxw_qlname')
        if not ql_config:
            print("未配置青龙信息")
            return False

        ql_config = ql_config.replace('|', '丨')
        host, client_id, client_secret = [x.strip() for x in ql_config.split('丨')]

        token = get_ql_token(host, client_id, client_secret)
        if not token:
            return False

        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(f'{host}/open/envs', headers=headers)
        envs = response.json()['data']

        deleted = False
        for env in envs:
            if env['name'] == env_name and username in env['value']:
                response = requests.delete(
                    f'{host}/open/envs',
                    headers=headers,
                    json=[env.get('_id') or env.get('id')]
                )
                if response.status_code == 200:
                    deleted = True
                    print(f"删除青龙变量成功: {env.get('_id') or env.get('id')}")
                else:
                    print(f"删除青龙变量失败: {response.text}")

        return deleted

    except Exception as e:
        print(f"删除青龙变量异常: {str(e)}")
        return False

def show_tutorial():
    tutorial = """
=====上观新闻使用教程=====
1. 基本功能:
  • 上观登录: 绑定上观新闻账号
  • 上观查询: 查询账号信息和积分
  • 上观管理: 管理账号(授权/删除/提交青龙)
  • 上观授权: 管理员专用授权功能

2. 使用须知:
  • 账号需要先授权才能提交青龙
  • 支持微信支付和积分兑换两种授权方式
  • 授权后可自动同步至青龙环境变量

3. 账号绑定格式:
  • 备注#手机号#密码
  • 示例: 张三#13812345678#123456

4. 青龙提交格式:
  • 变量名: S_SGXW
  • 变量值: UID#账号#密码
  • 备注: 上观UID：xxxx|到期:yyyy-mm-dd

5. 如有问题请检查配置
=================="""
    sender.reply(tutorial)

def check_order(order_id=None):
    if not order_id:
        sender.reply("""
=====订单查询=====
请输入订单号
回复"q"退出操作
==================""")

        order_id = sender.input(120000, 1, False)
        if not order_id or order_id.lower() == 'q':
            sender.reply("✅ 已取消查询")
            return

    try:
        order_info = sg.bucketGet('sgxw_order', order_id)
        if not order_info:
            sender.reply("""
=====查询结果=====
❌ 未找到订单信息
------------------
请确认订单号是否正确
==================""")
            return

        order_data = json.loads(order_info)
        sender.reply(f"""
=====订单详情=====
🔖 订单号: {order_id}
💰 金额: {order_data.get('amount', '未知')}元
⏱️ 时长: {order_data.get('months', '未知')}个月
📊 状态: {'已支付' if order_data.get('status') == 'success' else '未支付'}
==================""")

    except Exception as e:
        sender.reply(f"""
=====查询异常=====
❌ 错误: {str(e)}
==================""")

def ks_auth():
    return True

def main():
    global randommanagecommand, randomquerycommand
    global randomsigncommand, sgxwVipmoney, sgxwcoin

    sgxw_osname, sgxw_qlname, randommanagecommand, randomquerycommand, randomsigncommand, sgxwVipmoney, sgxwcoin = get_user_content()

    usermessage = sender.getMessage()

    if '登录' in usermessage or '登陆' in usermessage:
        bind_account()
    elif '查询' in usermessage and ('上观' in usermessage or 'sgxw' in usermessage):
        query_accounts()
    elif '管理' in usermessage and ('上观' in usermessage or 'sgxw' in usermessage):
        manage_account()
    elif '上观授权' in usermessage:
        ks_auth()
    elif '上观教程' in usermessage:
        show_tutorial()
    elif '清理上观' in usermessage:
        if not sender.isAdmin():
            sender.reply("❌ 此功能仅限管理员使用")
            return

        expired_count = 0
        dqsj = datetime.now().strftime("%Y-%m-%d")

        for username in sg.bucketKeys('sgxw_auth'):
            auth_time = '2099-12-31'
            if auth_time < dqsj:
                True
                expired_count += 1

        sender.reply(f"✅ 已清理 {expired_count} 个过期账号")
    elif usermessage.startswith('SGXW_'):  # 查询订单
        order_result = check_order(usermessage)
        if order_result:
            sender.reply(order_result)
    else:
        sender.setContinue()

if __name__ == "__main__":
    main()
