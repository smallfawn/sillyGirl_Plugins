# [title: 腾讯地图]
# [name: tengXunDiTu]
# [language: python]
# [class: 任务]
# [author: huawei]
# [version: v1.0.0]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(地图)(登录|登陆)$|^登(录|陆)(地图)$|^(地图)(查询|管理)$|^(查询|管理)(地图)$|^清理地图$|^地图$|^地图教程$|^地图检测$|^地图一键运行$]
# [cron: 0 0 4,19 * * *]
# [icon: https://free.picui.cn/free/2025/11/14/6916bb4577d7a.png]
# [description: 腾讯地图现金毛，日0.1]
# [depe: ["requests"]]


import asyncio as _sg_asyncio
import os as _sg_os
import time as _sg_time
import types as _sg_types
import json as _sg_json
from threading import Thread as _sg_Thread
from sillygirl import Adapter as _SGAdapter, Bucket as _SGBucket, Sender as _SGSender, sender as _sg_sender, form
check_auth_status = lambda *args, **kwargs: "账号默认可用"
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
    'G_TXDT_CONFIG_notify': form.string().title('通知渠道').default('').description('配置检测通知推送渠道'),
    'G_TXDT_CONFIG_proxy_api': form.string().title('代理API').default(''),
})
_CONFIG_FIELD_MAP = {
    ('G_TXDT_CONFIG', 'notify'): 'G_TXDT_CONFIG_notify',
    ('G_TXDT_CONFIG', 'proxy_api'): 'G_TXDT_CONFIG_proxy_api',
}

import json
import time
import uuid
import hashlib
import requests
from datetime import datetime
import threading

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()

def get_proxy_api() -> str:
    try:
        return sg.bucketGet(bucket=BUCKET_CONFIG, key='proxy_api') or ''
    except Exception:
        return ''

proxy_url = get_proxy_api()
IS_PROXY = bool(proxy_url)

if IS_PROXY:
    print('[INFO] 地图代理模式: 已启用')
    print(f'[INFO] 地图代理API: {proxy_url}')
else:
    print('[INFO] 地图代理模式: 未启用')

proxy_cache = {}
proxy_lock_dict = threading.Lock()

def get_proxy(force_new=False, account_key=None):
    if not IS_PROXY or not proxy_url:
        return None

    if account_key and not force_new:
        with proxy_lock_dict:
            if account_key in proxy_cache:
                return proxy_cache[account_key]

    try:
        response = requests.get(proxy_url, timeout=5)
        if response.status_code == 200:
            ip = response.text.strip()
            if "请先添加白名单" in ip:
                print('[WARNING] 地图代理服务异常：请先添加白名单')
                return None

            proxy_dict = {'http': ip, 'https': ip}

            if account_key:
                with proxy_lock_dict:
                    proxy_cache[account_key] = proxy_dict

            print(f'[INFO] 地图获取代理成功: {ip}')
            return proxy_dict
        else:
            print(f'[WARNING] 地图代理API响应异常: {response.status_code}')
            return None
    except Exception as e:
        print(f'[WARNING] 地图获取代理失败: {str(e)}')
        return None

def request_with_retry(method, url, max_retries=3, account_key=None, **kwargs):
    current_proxy = None

    for attempt in range(max_retries):
        try:
            if IS_PROXY:
                if attempt == 0:
                    current_proxy = get_proxy(force_new=False, account_key=account_key)
                else:
                    current_proxy = get_proxy(force_new=True, account_key=account_key)

                if current_proxy:
                    kwargs['proxies'] = current_proxy
                else:
                    kwargs['proxies'] = None

            if method.upper() == 'GET':
                response = requests.get(url, **kwargs)
            else:
                response = requests.post(url, **kwargs)

            return response

        except (requests.exceptions.ProxyError, requests.exceptions.ConnectionError) as e:
            print(f'[WARNING] 地图代理连接错误: {str(e)[:100]}')
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            else:
                print('[ERROR] 地图代理请求失败，已达最大重试次数')
                raise
        except requests.exceptions.Timeout:
            print('[WARNING] 地图请求超时')
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            else:
                print('[ERROR] 地图请求超时，已达最大重试次数')
                raise
        except Exception as e:
            print(f'[ERROR] 地图请求异常: {str(e)[:100]}')
            raise

    return None

BUCKET_USER = 'G_TXDT_USER'  # 用户账号列表
BUCKET_TOKEN = 'G_TXDT_TOKEN'  # 账号token信息
BUCKET_AUTH = 'G_TXDT_AUTH'  # 账号授权信息
BUCKET_CONFIG = 'G_TXDT_CONFIG'  # 插件配置

uservalue = sg.bucketGet(bucket=BUCKET_USER, key=userid)

PAY_TYPE_NAMES = {
    'alipay': '支付宝',
    'wxpay': '微信支付',
    'qqpay': 'QQ钱包',
}

def mask_user_id(user_id):
    if not user_id or len(user_id) < 8:
        return user_id
    return f"{user_id[:4]}****{user_id[-4:]}"









def get_headers(user_id, urlparams):
    reqid = str(uuid.uuid4())
    reqtime = str(int(time.time()*1000))
    secret_key = '03a9875e795c3ecff15f617085e72d4cc'
    tmapdefaultstr = f'mapinst=0&mapnonce=0&reqid={reqid}&reqtime={reqtime}{urlparams}{secret_key}'
    tmapdefaultsign = hashlib.md5(tmapdefaultstr.encode()).hexdigest()
    timestamp = reqtime[:-3]
    signstr = f'request_id={reqid}&from_source=wx7643d5f831302ab0&timestamp={timestamp}&token='
    sign = hashlib.sha256(signstr.encode()).hexdigest().upper()
    return {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'from_source': 'wx7643d5f831302ab0',
        'request_id': reqid,
        'tmap-nonce': '0',
        'tmap-engine': 'web',
        'tmap-reqid': reqid,
        'sign': sign,
        'user_id': user_id,
        'tmap-reqtime': reqtime,
        'timestamp': timestamp,
        'tmap-install-id': '0',
        'tmap-default-sign': tmapdefaultsign
    }

def verify_account(user_id):
    try:
        headers = get_headers(user_id, '/activity/v1/lottery/detail')
        resp = request_with_retry(
            'POST',
            'https://mmapgwh.map.qq.com/activity/v1/lottery/detail',
            headers=headers,
            json={'activity_id':1721983577,'game_id':3,'rule_id':'tencent_map_lottery'},
            timeout=10,
            account_key=user_id
        )
        return resp.status_code == 200 and resp.json().get('message') == 'ok'
    except:
        return False

def do_checkin(user_id):
    try:
        headers = get_headers(user_id, '/activity/v1/checkin')
        resp = request_with_retry(
            'POST',
            'https://mmapgwh.map.qq.com/activity/v1/checkin',
            headers=headers,
            json={'activity_id':1721983577,'game_id':1},
            timeout=10,
            account_key=user_id
        ).json()
        if resp['message'] == 'ok':
            prizes = [prize['name'] for prize in resp['data']['prizes']]
            return True, '、'.join(prizes)
        else:
            return False, resp['message']
    except Exception as e:
        return False, str(e)

def do_lottery(user_id):
    try:
        headers = get_headers(user_id, '/activity/v1/lottery/detail')
        resp = request_with_retry(
            'POST',
            'https://mmapgwh.map.qq.com/activity/v1/lottery/detail',
            headers=headers,
            json={'activity_id':1721983577,'game_id':3,'rule_id':'tencent_map_lottery'},
            timeout=10,
            account_key=user_id
        ).json()

        if resp['message'] != 'ok':
            return False, resp['message'], 0

        tickets = resp['data']['available_ticket_number']
        results = []

        for i in range(tickets):
            lottery_resp = request_with_retry(
                'POST',
                'https://mmapgwh.map.qq.com/activity/v1/lottery',
                headers=get_headers(user_id, '/activity/v1/lottery'),
                json={'activity_id':1721983577,'game_id':3},
                timeout=10,
                account_key=user_id
            ).json()

            if lottery_resp['message'] == 'ok':
                prizes = [prize['name'] for prize in lottery_resp['data']['prizes']]
                results.append('、'.join(prizes))
            else:
                results.append(lottery_resp['message'])
            time.sleep(0.5)

        return True, results, tickets
    except Exception as e:
        return False, str(e), 0

def do_withdraw(user_id):
    try:
        headers = get_headers(user_id, '/activity/v1/withdraw/home')
        resp = request_with_retry(
            'POST',
            'https://mmapgwh.map.qq.com/activity/v1/withdraw/home',
            headers=headers,
            json={'activity_id':1721983577,'game_id':4,'rule_id':'tencent_map_withdraw'},
            timeout=10,
            account_key=user_id
        ).json()

        if resp['message'] != 'ok':
            return False, resp['message'], 0, 0

        data = resp['data']
        coins = data['coins']/100
        withdrawable = data['withdrawable_amount']/100

        if data['withdrawable_amount'] >= data['current_withdraw_threshold']:
            withdraw_resp = request_with_retry(
                'POST',
                'https://mmapgwh.map.qq.com/activity/v1/withdraw',
                headers=get_headers(user_id, '/activity/v1/withdraw'),
                json={'activity_id':1721983577,'game_id':4},
                timeout=10,
                account_key=user_id
            ).json()
            return True, withdraw_resp['message'], coins, withdrawable
        else:
            return True, '未达到提现阈值', coins, withdrawable
    except Exception as e:
        return False, str(e), 0, 0

def query_balance(user_id):
    try:
        headers = get_headers(user_id, '/activity/v1/withdraw/home')
        resp = request_with_retry(
            'POST',
            'https://mmapgwh.map.qq.com/activity/v1/withdraw/home',
            headers=headers,
            json={'activity_id':1721983577,'game_id':4,'rule_id':'tencent_map_withdraw'},
            timeout=10,
            account_key=user_id
        ).json()

        if resp['message'] == 'ok':
            data = resp['data']
            coins = data['coins']/100
            withdrawable = data['withdrawable_amount']/100
            return True, coins, withdrawable
        else:
            return False, 0, 0
    except:
        return False, 0, 0

def query_coins_history(user_id, limit=5):
    return 0


def bind_account():
    sender.reply("""
=====腾讯地图登录=====
请按照格式输入账号信息
------------------
📝 格式: 备注#user_id
📝 示例:
张三#abc123def456
李四#xyz789ghi012
------------------
💡 支持批量登录，每行一个账号
💡 回复"q"随时退出操作
==================""")

    input_text = sender.input(120000, 10000, False)

    if not input_text:
        sender.reply("⏰ 操作超时,已退出")
        return
    elif input_text.lower() == 'q':
        sender.reply("✅ 已取消登录")
        return

    accounts_list = []
    for line in input_text.split('\n'):
        line = line.strip()
        if '#' in line:
            parts = line.split('#', 1)
            if len(parts) == 2:
                remark = parts[0].strip()
                user_id = parts[1].strip()
                if remark and user_id:
                    accounts_list.append({'remark': remark, 'user_id': user_id})

    if not accounts_list:
        sender.reply("""
=====格式错误=====
❌ 未检测到有效账号
------------------
请按照格式输入: 备注#user_id
示例: 张三#abc123def456
==================""")
        return


    success_count = 0
    fail_count = 0
    results = []

    current_accounts = _sg_literal(uservalue) if uservalue else []

    for idx, acc in enumerate(accounts_list, 1):
        remark = acc['remark']
        user_id = acc['user_id']


        try:
            if len(user_id) < 10:
                fail_count += 1
                results.append(f"❌ {remark} - user_id格式不正确")
                continue

            if not verify_account(user_id):
                fail_count += 1
                results.append(f"❌ {remark} - 账号验证失败")
                continue

            if user_id not in current_accounts:
                current_accounts.append(user_id)

            account_info = {
                "user_id": user_id,
                "remark": remark,
                "create_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            sg.bucketSet(BUCKET_TOKEN, user_id, json.dumps(account_info))

            dqsj = datetime.now().strftime("%Y-%m-%d")
            accountVip = '2099-12-31'

            if accountVip and accountVip > dqsj:
                success_count += 1
                results.append(f"✅ {remark} ({mask_user_id(user_id)}) - 已授权至{accountVip}")
            else:
                success_count += 1
                results.append(f"✅ {remark} ({mask_user_id(user_id)}) - 登录成功，需授权")

            time.sleep(0.3)

        except Exception as e:
            fail_count += 1
            results.append(f"❌ {remark} - 异常: {str(e)}")

    sg.bucketSet(BUCKET_USER, userid, str(current_accounts))

    result_msg = f"""
=====批量登录完成=====
📊 总数: {len(accounts_list)}个
✅ 成功: {success_count}个
❌ 失败: {fail_count}个
==================
"""
    for result in results:
        result_msg += result + "\n"

    result_msg += """==================
💡 发送"地图管理"可管理账号
💡 发送"地图查询"可查询信息
=================="""

    sender.reply(result_msg)

def query_accounts():
    if not uservalue:
        sender.reply("""
=====未绑定账号=====
❌ 未找到任何账号信息
💡 发送"地图登录"绑定
==================""")
        return

    accounts = _sg_literal(uservalue)
    account_list = """
========选择账号=======
[0] 全部账号"""

    for i, user_id in enumerate(accounts, 1):
        try:
            account_info = json.loads(sg.bucketGet(BUCKET_TOKEN, user_id))
            remark = account_info.get('remark', user_id)
            auth_time = '2099-12-31'

            if not auth_time:
                auth_status = '未授权'
            elif auth_time < str(datetime.now().date()):
                auth_status = '已过期'
            else:
                auth_status = f'到期:{auth_time}'

            account_list += f"""
[{i}]{mask_user_id(user_id)}({remark}, {auth_status})"""
        except:
            account_list += f"""
[{i}]{mask_user_id(user_id)}(信息异常)"""

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
        for user_id in selected_accounts:
            try:
                account_info = json.loads(sg.bucketGet(BUCKET_TOKEN, user_id))
                auth_time = '2099-12-31'
                auth_status = '已授权' if auth_time and auth_time >= str(datetime.now().date()) else '未授权'

                success, coins, withdrawable = query_balance(user_id)

                history_success, history_list = query_coins_history(user_id, limit=5)

                if success:
                    account_info_msg = f"""
=====账号信息[{query_count+1}/{len(selected_accounts)}]=====
🆔 账号: {mask_user_id(user_id)}
📝 备注: {account_info.get('remark')}
🔐 授权状态: {auth_status}
💰 金币余额: {coins}元
💵 可提现: {withdrawable}元"""

                    if history_success and history_list:
                        account_info_msg += "\n==================\n📋 金币明细(最近5条):"
                        for history_item in history_list:
                            account_info_msg += f"\n{history_item}"

                    account_info_msg += "\n=================="
                else:
                    account_info_msg = f"""
=====账号信息[{query_count+1}/{len(selected_accounts)}]=====
🆔 账号: {mask_user_id(user_id)}
👤 备注: {account_info.get('remark')}
🔐 授权状态: {auth_status}
❌ 余额查询失败
=================="""

                sender.reply(account_info_msg)
                query_count += 1

                if query_count < len(selected_accounts) and len(selected_accounts) > 3:
                    time.sleep(0.5)

            except Exception as e:
                sender.reply(f"""
=====查询失败[{query_count+1}/{len(selected_accounts)}]=====
🆔 账号: {mask_user_id(user_id)}
❌ 错误: {str(e)}
==================""")
                query_count += 1

        if query_count > 0:
            sender.reply(f"✅ 查询完成，共查询了 {query_count} 个账号")

    except Exception as e:
        sender.reply(f"❌ 查询失败: {str(e)}")


def manage_account():
    if not uservalue:
        sender.reply("""
=====未绑定账号=====
❌ 未找到任何账号信息
💡 发送"地图登录"绑定
==================""")
        return

    accounts = _sg_literal(uservalue)

    menu = """
=====账号管理=====
[1] 授权账号
[2] 删除账号
[3] 执行任务
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

    for i, user_id in enumerate(accounts, 1):
        try:
            account_info = json.loads(sg.bucketGet(BUCKET_TOKEN, user_id))
            remark = account_info.get('remark', user_id)
            auth_time = '2099-12-31'

            if not auth_time:
                auth_status = '未授权'
            elif auth_time < str(datetime.now().date()):
                auth_status = '已过期'
            else:
                auth_status = f'到期:{auth_time}'

            account_list += f"""
[{i}]{mask_user_id(user_id)}({remark}, {auth_status})"""
        except:
            account_list += f"""
[{i}]{mask_user_id(user_id)}(信息异常)"""

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

            confirm_input = sender.input(120000, 1, False)
            if confirm_input and confirm_input.lower() == 'y':
                success_count = 0
                for user_id in selected_accounts:
                    try:
                        if user_id in accounts:
                            accounts.remove(user_id)

                        sg.bucketDel(BUCKET_TOKEN, user_id)
                        True
                        success_count += 1
                    except Exception as e:
                        print(f"删除账号失败: {user_id}, 错误: {str(e)}")

                if accounts:
                    sg.bucketSet(BUCKET_USER, userid, str(accounts))
                else:
                    sg.bucketDel(BUCKET_USER, userid)

                sender.reply(f"✅ 已成功删除 {success_count}/{len(selected_accounts)} 个账号")
            else:
                sender.reply("✅ 已取消删除")

        elif choice == '3':
            success_count = 0
            for user_id in selected_accounts:
                try:
                    account_info = json.loads(sg.bucketGet(BUCKET_TOKEN, user_id))
                    remark = account_info.get('remark', user_id)

                    task_msg = f"""
=====任务执行: {remark}====="""

                    checkin_success, checkin_result = do_checkin(user_id)
                    if checkin_success:
                        task_msg += f"\n✅ 签到成功: {checkin_result}"
                    else:
                        task_msg += f"\n❌ 签到失败: {checkin_result}"

                    time.sleep(1)

                    lottery_success, lottery_result, tickets = do_lottery(user_id)
                    if lottery_success:
                        task_msg += f"\n🎰 抽奖券: {tickets}张"
                        if tickets > 0:
                            for idx, prize in enumerate(lottery_result, 1):
                                task_msg += f"\n  第{idx}次: {prize}"
                    else:
                        task_msg += f"\n❌ 抽奖失败: {lottery_result}"

                    time.sleep(1)

                    withdraw_success, withdraw_result, coins, withdrawable = do_withdraw(user_id)
                    if withdraw_success:
                        task_msg += f"\n💰 金币余额: {coins}元"
                        task_msg += f"\n💵 可提现: {withdrawable}元"
                        task_msg += f"\n📤 提现结果: {withdraw_result}"
                    else:
                        task_msg += f"\n❌ 提现失败: {withdraw_result}"

                    task_msg += "\n===================="

                    sender.reply(task_msg)

                    success_count += 1

                    if success_count < len(selected_accounts):
                        time.sleep(2)

                except Exception as e:
                    sender.reply(f"""
=====任务执行失败=====
👤 账号: {remark}
❌ 错误: {str(e)}
=====================""")

            sender.reply(f"✅ 任务执行完成，共处理 {success_count}/{len(selected_accounts)} 个账号")

        else:
            sender.reply("❌ 无效的选择")

    except Exception as e:
        sender.reply(f"❌ 操作失败: {str(e)}")


def authorize_multiple_accounts(user_ids):
    return True



def admin_authorize():
    return True


def clean_expired_accounts():
    if not sender.isAdmin():
        sender.reply("""
=====权限不足=====
❌ 此功能仅限管理员使用
==================""")
        return

    try:
        sender.reply("🧹 开始清理过期账号...")

        expired_accounts = []
        dqsj = datetime.now().strftime("%Y-%m-%d")

        for user_id in []:
            auth_time = '2099-12-31'
            if auth_time and auth_time < dqsj:
                expired_accounts.append(user_id)

        if not expired_accounts:
            sender.reply("✅ 没有找到过期账号")
            return

        sender.reply(f"🔍 找到 {len(expired_accounts)} 个过期账号，开始清理...")

        success_count = 0
        for user_id in expired_accounts:
            try:
                sg.bucketDel(BUCKET_TOKEN, user_id)
                True

                for uid in sg.bucketAllKeys(BUCKET_USER):
                    user_accounts = sg.bucketGet(BUCKET_USER, uid)
                    if user_accounts:
                        try:
                            accounts_list = _sg_literal(user_accounts)
                            if user_id in accounts_list:
                                accounts_list.remove(user_id)
                                if accounts_list:
                                    sg.bucketSet(BUCKET_USER, uid, str(accounts_list))
                                else:
                                    sg.bucketDel(BUCKET_USER, uid)
                                break
                        except:
                            continue

                success_count += 1
            except Exception as e:
                print(f"清理账号异常: {user_id}, 错误: {str(e)}")

        sender.reply(f"""
=====清理完成=====
📊 过期账号: {len(expired_accounts)}个
✅ 清理成功: {success_count}个
==================""")

    except Exception as e:
        sender.reply(f"""
=====清理异常=====
❌ 错误: {str(e)}
==================""")

def run_all_accounts():
    if not sender.isAdmin():
        sender.reply("""
=====权限不足=====
❌ 此功能仅限管理员使用
==================""")
        return

    try:
        sender.reply("🔄 开始一键运行所有已授权账号...")

        all_users = sg.bucketAllKeys(BUCKET_USER)
        if not all_users:
            sender.reply("❌ 未找到任何用户")
            return

        today = datetime.now().strftime("%Y-%m-%d")
        total_accounts = 0
        valid_accounts = 0
        success_count = 0

        for user_id in all_users:
            try:
                user_accounts = sg.bucketGet(BUCKET_USER, user_id)
                if not user_accounts:
                    continue

                accounts = _sg_literal(user_accounts)

                for account_id in accounts:
                    total_accounts += 1

                    auth_time = '2099-12-31'
                    if not auth_time or auth_time <= today:
                        continue  # 跳过未授权或已过期的账号

                    valid_accounts += 1

                    try:
                        account_info = json.loads(sg.bucketGet(BUCKET_TOKEN, account_id))
                        remark = account_info.get('remark', account_id)

                        task_msg = f"\n🔄 执行账号: {remark}"

                        checkin_success, checkin_result = do_checkin(account_id)
                        if checkin_success:
                            task_msg += f"\n  ✅ 签到: {checkin_result}"
                        else:
                            task_msg += f"\n  ❌ 签到: {checkin_result}"

                        time.sleep(1)

                        lottery_success, lottery_result, tickets = do_lottery(account_id)
                        if lottery_success and tickets > 0:
                            task_msg += f"\n  🎰 抽奖: {tickets}张券"
                            for idx, prize in enumerate(lottery_result, 1):
                                task_msg += f"\n    第{idx}次: {prize}"

                        time.sleep(1)

                        withdraw_success, withdraw_result, coins, withdrawable = do_withdraw(account_id)
                        if withdraw_success:
                            task_msg += f"\n  💰 余额: {coins}元 | 提现: {withdraw_result}"

                        sender.reply(task_msg)
                        success_count += 1

                        time.sleep(2)

                    except Exception as e:
                        sender.reply(f"\n❌ 账号执行失败: {account_id}, 错误: {str(e)}")
                        continue

            except Exception as e:
                print(f"处理用户失败: {user_id}, 错误: {str(e)}")
                continue

        result_msg = f"""
=====一键运行完成=====
📊 总账号数: {total_accounts}个
✅ 已授权: {valid_accounts}个
🎯 执行成功: {success_count}个
❌ 执行失败: {valid_accounts - success_count}个
=================="""
        sender.reply(result_msg)

    except Exception as e:
        sender.reply(f"""
=====运行异常=====
❌ 错误: {str(e)}
==================""")


def show_tutorial():
    tutorial = """
=====腾讯地图教程=====
📱 用户指令:
• 地图登录 - 绑定账号
• 地图管理 - 管理账号
• 地图查询 - 查询信息
• 地图教程 - 查看教程
------------------
🔧 管理员指令:
• 地图授权 - 管理员授权
• 地图检测 - 检测账号状态
• 清理地图 - 清理过期账号
------------------
💡 登录格式:
📝 格式: 备注#user_id
📝 示例:
张三#abc123def456
李四#xyz789ghi012
💡 支持批量登录，每行一个账号
------------------
📝 如何获取user_id:
1. 打开腾讯地图小程序
2. 进入活动页面
3. 抓包获取请求头的user_id参数
------------------
💰 收益说明:
• 每日签到: 获得金币
• 抽奖活动: 随机奖励
• 自动提现: 达到阈值自动提现
• 预计收益: 0.1/天
------------------
🎯 使用流程:
1. 发送"地图登录"绑定账号
2. 发送"地图管理"进行授权
3. 在管理中选择"执行任务"
4. 自动完成签到、抽奖、提现
=================="""
    sender.reply(tutorial)

if __name__ == '__main__':
    message = sender.getMessage()

    if '登录' in message or '登陆' in message:
        bind_account()

    elif '管理' in message:
        manage_account()

    elif '查询' in message:
        query_accounts()

    elif '授权' in message:
        admin_authorize()

    elif '检测' in message:
        check_auth_status()

    elif '清理' in message:
        clean_expired_accounts()

    elif '一键运行' in message:
        run_all_accounts()

    elif '教程' in message:
        show_tutorial()
