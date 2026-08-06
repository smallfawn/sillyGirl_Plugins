# [title: 爱坤助手]
# [name: aiKunZhuShou]
# [language: python]
# [class: 任务]
# [author: rujingxianghai]
# [version: v1.0.3]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(爱坤|ik)(登录|登陆)$|^登(录|陆)(爱坤|ik)$|^(爱坤|ik)(查询|管理|检测|教程)$]
# [cron: 0 8 * * *]
# [icon: https://api.iconify.design/lucide:bot.svg]
# [description: 爱坤/ik登录、爱坤/ik管理、爱坤/ik查询]
# [depe: ["parsel","requests"]]

import asyncio as _sg_asyncio
import os as _sg_os
import time as _sg_time
import types as _sg_types
import json as _sg_json
from threading import Thread as _sg_Thread
from sillygirl import Adapter as _SGAdapter, Bucket as _SGBucket, Sender as _SGSender, sender as _sg_sender, plugin
check_auth_status = lambda *args, **kwargs: "账号默认可用"
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
    "enable": plugin.Form.boolean().title("是否启用").default(True),
    's_ikuu_qlname': plugin.Form.string().title('设置对接容器').default('').description('青龙容器参数用丨分割'),
    's_ikuu_osname': plugin.Form.string().title('青龙变量名').default('').description('青龙容器内的变量名'),
    's_ikuu_notify': plugin.Form.string().title('通知渠道').default('').description('检测通知推送渠道'),
    's_ikuu_proxy_api': plugin.Form.string().title('代理API地址').default('').description('代理API返回txt格式ip:port，未配置则直连'),
})
_CONFIG_FIELD_MAP = {
    ('s_ikuu', 'qlname'): 's_ikuu_qlname',
    ('s_ikuu', 'osname'): 's_ikuu_osname',
    ('s_ikuu', 'notify'): 's_ikuu_notify',
    ('s_ikuu', 'proxy_api'): 's_ikuu_proxy_api',
}

import os
import json
import time
import base64
import requests
import parsel
from datetime import datetime

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()
uservalue = sg.bucketGet(bucket='s_ikuu_user', key=userid)

PLUGIN_CONFIG = {'bucket': 's_ikuu', 'coin_key': 'dd_sign_points', 'name': '爱坤'}
PAY_TYPE_NAMES = {'alipay': '支付宝', 'wxpay': '微信支付', 'qqpay': 'QQ钱包'}
BASE_URL = "https://ikuuu.de"

_proxy_cache = {'proxy': None, 'time': 0}

def get_proxy():
    proxy_api = sg.bucketGet('s_ikuu', 'proxy_api')
    if not proxy_api:
        return None

    current_time = time.time()
    if _proxy_cache['proxy'] and (current_time - _proxy_cache['time']) < 30:
        return _proxy_cache['proxy']

    try:
        resp = requests.get(proxy_api, timeout=10)
        resp.raise_for_status()
        proxy_text = resp.text.strip()

        if not proxy_text or ':' not in proxy_text:
            return None

        proxy_ip = proxy_text.split('\n')[0].strip()
        if not proxy_ip or ':' not in proxy_ip:
            return None

        proxy_dict = {
            'http': f'http://{proxy_ip}',
            'https': f'http://{proxy_ip}'
        }

        _proxy_cache['proxy'] = proxy_dict
        _proxy_cache['time'] = current_time

        return proxy_dict
    except Exception:
        return None

def get_user_content():
    osname = sg.bucketGet('s_ikuu', 'osname') or 'S_IKUU'
    qlname = sg.bucketGet('s_ikuu', 'qlname') or ''
    Vipmoney = float(sg.bucketGet('s_ikuu', 'Vipmoney') or '1')
    coin = int(sg.bucketGet('s_ikuu', 'coin') or '0')
    return osname, qlname, Vipmoney, coin

def mask_account(account):
    if not account or len(account) < 4:
        return account
    if '@' in account:
        local, domain = account.split('@', 1)
        if len(local) <= 4:
            return f"{local[:1]}***@{domain}"
        return f"{local[:3]}****{local[-2:]}@{domain}"
    if account.isdigit() and len(account) == 11:
        return f"{account[:3]}****{account[7:]}"
    if len(account) <= 16:
        return f"{account[:4]}****{account[-4:]}"
    return f"{account[:8]}****{account[-8:]}"

def get_ikuuu_session(email, password):
    session = requests.Session()
    login_url = f'{BASE_URL}/auth/login'

    proxies = get_proxy()

    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Origin': BASE_URL,
        'Referer': f'{BASE_URL}/auth/login',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest'
    })

    payload = {
        'host': 'ikuuu.de',
        'email': email,
        'passwd': password,
        'code': '',
        'pageLoadedAt': str(int(datetime.now().timestamp() * 1000))
    }

    try:
        response = session.post(login_url, data=payload, timeout=15, proxies=proxies)
        result = response.json()
        if result.get('ret') == 1:
            session.proxies = proxies or {}
            return session, "登录成功"
        else:
            return None, result.get('msg', '登录失败')
    except Exception as e:
        return None, f"网络请求异常: {str(e)}"

def query_flow(session):
    user_url = f'{BASE_URL}/user'
    try:
        response = session.get(user_url, timeout=15)
        response.encoding = 'utf-8'
        html_text = response.text

        import re
        base64_match = re.search(r'var\s+originBody\s*=\s*"([^"]+)"', html_text)
        if base64_match:
            encoded_body = base64_match.group(1)
            try:
                html_text = base64.b64decode(encoded_body).decode('utf-8')
            except Exception:
                pass  # 解码失败则使用原始响应

        selector = parsel.Selector(html_text)

        target_card = selector.xpath('//div[@class="card-wrap"][.//h4[contains(text(), "剩余流量")]]')

        if target_card:
            full_text = target_card.xpath('.//div[@class="card-body"]').xpath('string(.)').get()
            if full_text:
                return full_text.strip().replace("\n", "")

        return "未能解析流量信息"
    except Exception as e:
        return f"查询异常: {str(e)}"

def get_ql_token(host, client_id, client_secret):
    try:
        url = f'{host}/open/auth/token?client_id={client_id}&client_secret={client_secret}'
        resp = requests.get(url, timeout=10).json()
        if resp.get('code') == 200:
            return resp['data']['token']
        return None
    except:
        return None

def update_ql_env(account, account_info):
    env_value = account_info.get('token', '')
    if not env_value:
        return False

    qlconfig = sg.bucketGet('s_ikuu', 'qlname')
    if not qlconfig:
        return False

    configs = qlconfig.replace('|', '丨').split('丨')
    if len(configs) < 3:
        return False

    host, client_id, client_secret = [x.strip() for x in configs]

    try:
        token = get_ql_token(host, client_id, client_secret)
        if not token:
            return False

        headers = {'Authorization': f'Bearer {token}'}
        osname = sg.bucketGet('s_ikuu', 'osname') or 'S_IKUU'
        auth_time = '2099-12-31'

        envs = requests.get(
            f'{host}/open/envs?searchValue={account[:10]}',
            headers=headers, timeout=10
        ).json().get('data', [])
        env_id = next((e.get('id') for e in envs if e['name'] == osname and account in e.get('value', '')), None)

        env_data = {
            'name': osname,
            'value': env_value,
            'remarks': f"爱坤：{mask_account(account)}|到期:{auth_time}"
        }

        if env_id:
            env_data['id'] = env_id
            requests.put(f'{host}/open/envs', headers=headers, json=env_data, timeout=10)
            requests.put(f'{host}/open/envs/enable', headers=headers, json=[env_id], timeout=10)
        else:
            resp = requests.post(f'{host}/open/envs', headers=headers, json=[env_data], timeout=10).json()
            if resp.get('data'):
                new_id = resp['data'][0].get('_id') or resp['data'][0].get('id')
                if new_id:
                    requests.put(f'{host}/open/envs/enable', headers=headers, json=[new_id], timeout=10)
        return True
    except:
        return False

def delete_ql_env(account):
    qlconfig = sg.bucketGet('s_ikuu', 'qlname')
    if not qlconfig:
        return False

    configs = qlconfig.replace('|', '丨').split('丨')
    if len(configs) < 3:
        return False

    host, client_id, client_secret = [x.strip() for x in configs]

    try:
        token = get_ql_token(host, client_id, client_secret)
        if not token:
            return False

        headers = {'Authorization': f'Bearer {token}'}
        osname = sg.bucketGet('s_ikuu', 'osname') or 'S_IKUU'
        envs = requests.get(f'{host}/open/envs', headers=headers, timeout=10).json().get('data', [])

        for env in envs:
            if env['name'] == osname and account in env.get('value', ''):
                env_id = env.get('_id') or env.get('id')
                requests.delete(f'{host}/open/envs', headers=headers, json=[env_id], timeout=10)
                return True
        return False
    except:
        return False

def bind_account():
    sender.reply(
        "=====爱坤登录=====\n"
        "请输入账号信息\n"
        "格式: 邮箱#密码\n"
        "------------------\n"
        "支持批量登录(换行分隔)\n"
        "回复\"q\"退出\n"
        "=================="
    )
    input_text = sender.input(120000, 1, False)
    if not input_text:
        sender.reply("⏰ 操作超时")
        return
    if input_text.lower() == 'q':
        sender.reply("✅ 已取消")
        return

    lines = [line.strip() for line in input_text.split('\n') if line.strip()]
    success_count = 0
    fail_count = 0
    results = []

    for line in lines:
        if '#' not in line:
            results.append(f"❌ 格式错误: {line[:20]}...")
            fail_count += 1
            continue

        parts = line.split('#', 1)
        if len(parts) != 2:
            results.append(f"❌ 格式错误: {line[:20]}...")
            fail_count += 1
            continue

        email, password = parts[0].strip(), parts[1].strip()

        session, msg = get_ikuuu_session(email, password)
        if not session:
            results.append(f"❌ {mask_account(email)}: {msg}")
            fail_count += 1
            continue

        accounts = _sg_literal(uservalue) if uservalue else []
        if email not in accounts:
            accounts.append(email)
            sg.bucketSet('s_ikuu_user', userid, str(accounts))

        token_info = {
            'email': email,
            'password': password,
            'token': f"{email}#{password}"  # 青龙变量格式
        }
        sg.bucketSet('s_ikuu_token', email, json.dumps(token_info))

        results.append(f"✅ {mask_account(email)}: 登录成功")
        success_count += 1

    result_text = "\n".join(results[:10])
    if len(results) > 10:
        result_text += f"\n... 共 {len(results)} 条"

    sender.reply(
        f"=====登录完成=====\n"
        f"✅ 成功: {success_count}个\n"
        f"❌ 失败: {fail_count}个\n"
        f"------------------\n"
        f"{result_text}\n"
        f"=================="
    )

def query_accounts():
    if not uservalue:
        sender.reply("=====未绑定账号=====\n❌ 未找到账号\n💡 发送 爱坤登录 绑定\n==================")
        return

    accounts = _sg_literal(uservalue)
    account_list = "\n========选择账号======\n[0] 全部账号"
    for i, account in enumerate(accounts, 1):
        auth_time = '2099-12-31'
        if not auth_time:
            auth_status = '未授权'
        elif auth_time < str(datetime.now().date()):
            auth_status = '已过期'
        else:
            auth_status = f'到期:{auth_time}'
        account_list += f"\n[{i}]{mask_account(account)}({auth_status})"
    account_list += "\n=====================\n支持多选，用逗号分隔\n回复\"q\"退出\n====================="
    sender.reply(account_list)

    choice = sender.input(120000, 1, False)
    if not choice or choice.lower() == 'q':
        sender.reply("✅ 已退出")
        return

    selected = []
    if choice == '0':
        selected = accounts
    else:
        try:
            indices = [int(x.strip()) for x in choice.split(',')]
            for idx in indices:
                if 1 <= idx <= len(accounts):
                    selected.append(accounts[idx - 1])
        except:
            sender.reply("❌ 输入无效")
            return

    if not selected:
        sender.reply("❌ 未选择有效账号")
        return

    sender.reply("🔍 正在查询...")
    results = []
    for account in selected:
        try:
            token_data = json.loads(sg.bucketGet('s_ikuu_token', account) or '{}')
            email = token_data.get('email', account)
            password = token_data.get('password', '')

            if not password:
                results.append(f"❌ {mask_account(account)}: 缺少密码信息")
                continue

            session, msg = get_ikuuu_session(email, password)
            if session:
                flow = query_flow(session)
                auth_time = '2099-12-31'
                results.append(f"📱 {mask_account(account)}\n   💾 流量: {flow}\n   📅 授权: {auth_time}")
            else:
                results.append(f"❌ {mask_account(account)}: 登录失败-{msg}")
        except Exception as e:
            results.append(f"❌ {mask_account(account)}: 异常-{str(e)}")

    sender.reply(
        "=====查询结果=====\n" +
        "\n------------------\n".join(results) +
        "\n=================="
    )

def authorize_multiple_accounts(accounts):
    return True

def submit_to_ql(accounts):
    osname, qlname, _, _ = get_user_content()
    if not qlname:
        sender.reply("❌ 未配置青龙容器")
        return

    success_count = 0
    fail_count = 0

    for account in accounts:
        try:
            token_data = json.loads(sg.bucketGet('s_ikuu_token', account) or '{}')
            if token_data:
                if update_ql_env(account, token_data):
                    success_count += 1
                else:
                    fail_count += 1
            else:
                fail_count += 1
        except:
            fail_count += 1

    sender.reply(
        f"=====提交青龙=====\n"
        f"✅ 成功: {success_count}个\n"
        f"❌ 失败: {fail_count}个\n"
        f"=================="
    )

def manage_account():
    if not uservalue:
        sender.reply("=====未绑定账号=====\n❌ 未找到账号\n==================")
        return

    accounts = _sg_literal(uservalue)
    sender.reply(
        "=====账号管理=====\n"
        "[1] 授权账号\n"
        "[2] 删除账号\n"
        "[3] 提交青龙\n"
        "------------------\n"
        "回复数字选择\n"
        "回复\"q\"退出\n"
        "=================="
    )
    choice = sender.input(120000, 1, False)
    if not choice or choice.lower() == 'q':
        sender.reply("✅ 已退出")
        return

    if choice == '1':
        account_list = "\n========选择账号======\n[0] 全部账号"
        for i, account in enumerate(accounts, 1):
            auth_time = '2099-12-31'
            if not auth_time:
                auth_status = '未授权'
            elif auth_time < str(datetime.now().date()):
                auth_status = '已过期'
            else:
                auth_status = f'到期:{auth_time}'
            account_list += f"\n[{i}]{mask_account(account)}({auth_status})"
        account_list += "\n=====================\n支持多选，用逗号分隔\n回复\"q\"退出\n====================="
        sender.reply(account_list)

        sel = sender.input(120000, 1, False)
        if not sel or sel.lower() == 'q':
            sender.reply("✅ 已退出")
            return

        selected = []
        if sel == '0':
            selected = accounts
        else:
            try:
                indices = [int(x.strip()) for x in sel.split(',')]
                for idx in indices:
                    if 1 <= idx <= len(accounts):
                        selected.append(accounts[idx - 1])
            except:
                sender.reply("❌ 输入无效")
                return

        if selected:
            authorize_multiple_accounts(selected)

    elif choice == '2':
        account_list = "\n========选择删除======\n[0] 全部删除"
        for i, account in enumerate(accounts, 1):
            account_list += f"\n[{i}]{mask_account(account)}"
        account_list += "\n=====================\n支持多选，用逗号分隔\n回复\"q\"退出\n====================="
        sender.reply(account_list)

        sel = sender.input(120000, 1, False)
        if not sel or sel.lower() == 'q':
            sender.reply("✅ 已退出")
            return

        to_delete = []
        if sel == '0':
            to_delete = accounts[:]
        else:
            try:
                indices = [int(x.strip()) for x in sel.split(',')]
                for idx in indices:
                    if 1 <= idx <= len(accounts):
                        to_delete.append(accounts[idx - 1])
            except:
                sender.reply("❌ 输入无效")
                return

        for account in to_delete:
            delete_ql_env(account)
            sg.bucketDel('s_ikuu_token', account)
            True
            if account in accounts:
                accounts.remove(account)

        if accounts:
            sg.bucketSet('s_ikuu_user', userid, str(accounts))
        else:
            sg.bucketDel('s_ikuu_user', userid)

        sender.reply(f"✅ 已删除 {len(to_delete)} 个账号")

    elif choice == '3':
        account_list = "\n========选择账号======\n[0] 全部账号"
        for i, account in enumerate(accounts, 1):
            auth_time = '2099-12-31'
            if not auth_time:
                auth_status = '未授权'
            elif auth_time < str(datetime.now().date()):
                auth_status = '已过期'
            else:
                auth_status = f'到期:{auth_time}'
            account_list += f"\n[{i}]{mask_account(account)}({auth_status})"
        account_list += "\n=====================\n支持多选，用逗号分隔\n回复\"q\"退出\n====================="
        sender.reply(account_list)

        sel = sender.input(120000, 1, False)
        if not sel or sel.lower() == 'q':
            sender.reply("✅ 已退出")
            return

        selected = []
        if sel == '0':
            selected = accounts
        else:
            try:
                indices = [int(x.strip()) for x in sel.split(',')]
                for idx in indices:
                    if 1 <= idx <= len(accounts):
                        selected.append(accounts[idx - 1])
            except:
                sender.reply("❌ 输入无效")
                return

        if selected:
            unauthorized = []
            authorized = []
            for acc in selected:
                auth_time = '2099-12-31'
                if auth_time and auth_time >= str(datetime.now().date()):
                    authorized.append(acc)
                else:
                    unauthorized.append(acc)

            if unauthorized:
                sender.reply("⚠️ 以下账号未授权或已过期，无法提交:\n" +
                           "\n".join([f"  - {mask_account(a)}" for a in unauthorized]))

            if authorized:
                submit_to_ql(authorized)

def ks_auth():
    return True

def show_tutorial():
    sender.reply(
        "=====爱坤使用教程=====\n"
        "📝 指令说明：\n"
        "• 爱坤登录 - 添加账号\n"
        "• 爱坤查询 - 查询流量\n"
        "• 爱坤管理 - 管理账号\n"
        "------------------\n"
        "📋 登录格式：\n"
        "邮箱#密码\n"
        "支持多账号换行\n"
        "------------------\n"
        "💡 使用流程：\n"
        "1. 发送\"爱坤登录\"添加账号\n"
        "2. 发送\"爱坤管理\"授权账号\n"
        "3. 授权后提交到青龙执行签到\n"
        "=================="
    )

def main():
    msg = sender.getMessage()

    if '登录' in msg or '登陆' in msg:
        bind_account()
    elif '查询' in msg and ('爱坤' in msg or 'ik' in msg.lower()):
        query_accounts()
    elif '管理' in msg and ('爱坤' in msg or 'ik' in msg.lower()):
        manage_account()
    elif '教程' in msg and ('爱坤' in msg or 'ik' in msg.lower()):
        show_tutorial()
    elif '爱坤授权' in msg or 'ik授权' in msg.lower():
        ks_auth()
    elif '爱坤检测' in msg or 'ik检测' in msg.lower():
        if not sender.isAdmin():
            sender.reply("❌ 仅限管理员")
            return
        sender.reply("🔍 正在检测...")
        sender.reply(check_auth_status())
    elif sender.getImtype() == 'fake':
        try:
            sg.notifyMasters(check_auth_status())
        except:
            pass
    else:
        sender.setContinue()

if __name__ == "__main__":
    main()
