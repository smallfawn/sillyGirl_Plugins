# [title: 品赞]
# [name: pinZan]
# [language: python]
# [class: 任务]
# [author: sky2022]
# [version: v1.4.1]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(品赞|pz)(登录|登陆)$|^登(录|陆)(品赞|pz)$|^(品赞|pz)(查询|管理)$|^(查询|管理)(品赞|pz)$|^品赞清理$|^品赞$|^品赞教程$|^品赞任务运行$|^品赞$|^品赞删除$|^品赞自动$]
# [cron: 0 8 * * 1]
# [icon: https://api.iconify.design/lucide:apple.svg]
# [description: 介绍：品赞代理自动签到插件；支持自动签到、用户ID查询、账号管理；登录格式：手机号#密码#备注；每周一自动执行签到任务，无需手动操作；📝 更新日志；v1.4：整体重构代码结构，提升可维护性]
# [depe: ["pycryptodome","requests","urllib3"]]


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
    'dd_pz_superior_account': form.string().title('上级账号').default('').description('填写上级账号信息，格式：账号#密码，用于判断下级关系'),
    'dd_pz_free_proxy': form.boolean().title('下级免费代挂').default(False).description('是否开启下级免费代挂功能'),
})
_CONFIG_FIELD_MAP = {
    ('dd_pz', 'superior_account'): 'dd_pz_superior_account',
    ('dd_pz', 'free_proxy'): 'dd_pz_free_proxy',
}

import re
import json
import base64
import random
import string
import requests
import urllib3
import time
from datetime import datetime, timedelta
from Crypto.Cipher import AES
from binascii import hexlify

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()
uservalue = sg.bucketGet(bucket='dd_pz_user', key=userid)


def getusercontent():
    pzVipmoney = float(sg.bucketGet('dd_pz', 'pzVipmoney') or '1')
    pzcoin = int(sg.bucketGet('dd_pz', 'pzcoin') or '0')
    superior_account = sg.bucketGet('dd_pz', 'superior_account') or ''
    free_proxy = (sg.bucketGet('dd_pz', 'free_proxy') or 'false').lower() == 'true'
    use_ma_pay = ('2099-12-31' or 'false').lower() == 'true'
    return pzVipmoney, pzcoin, superior_account, free_proxy, use_ma_pay


def mask_phone(phone):
    return phone[:3] + "****" + phone[7:]

def parse_accounts(raw):
    if not raw:
        return []
    try:
        result = _sg_literal(raw)
        return list(result) if isinstance(result, (list, tuple, set)) else []
    except Exception:
        return []

def parse_token_info(token_info):
    if '|' in token_info:
        account_info, token = token_info.split('|', 1)
    else:
        account_info, token = token_info, None
    parts = account_info.split('#')
    if len(parts) != 3:
        return None, None, None, None
    return parts[0], parts[1], parts[2], token

def parse_batch_selection(input_str, max_count):
    selected = []
    for part in input_str.split(','):
        part = part.strip()
        if '-' in part:
            a, b = part.split('-', 1)
            start, end = int(a.strip()), int(b.strip())
            if start <= end and start >= 1:
                selected.extend(range(start, end + 1))
        else:
            selected.append(int(part))
    selected = sorted(set(selected))
    valid = [i for i in selected if 1 <= i <= max_count]
    invalid = [i for i in selected if not (1 <= i <= max_count)]
    return valid, invalid

def ValueErrors(value, count):
    try:
        value = int(value)
        if value > count or value == 0:
            sender.reply(f"=====输入无效=====\n❌ 请输入 1-{count} 之间的数字\n==================")
            exit(0)
        return value
    except ValueError:
        sender.reply("=====输入无效=====\n❌ 请输入正确的数字\n==================")
        exit(0)


PZ_BASE = "https://service.ipzan.com"
PZ_HEADERS_BASE = {
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Host': 'service.ipzan.com',
}

def _pz_ua():
    models = ['Xiaomi', 'Samsung Galaxy', 'Huawei', 'OPPO', 'Vivo']
    versions = ['10', '11', '12', '13']
    m, v = random.choice(models), random.choice(versions)
    build = f"Build/SP1A.{random.randint(210812,230812)}.{random.randint(1,999)}"
    return (f"Mozilla/5.0 (Linux; Android {v}; {m} {build}; wv) AppleWebKit/537.36 "
            f"(KHTML, like Gecko) Version/4.0 Chrome/{random.randint(100,120)}.0."
            f"{random.randint(1000,9999)}.{random.randint(100,999)} Mobile Safari/537.36 "
            f"MicroMessenger/8.0.41.2441(0x28002951)")

def _pz_encode(phone, password):
    encoded = base64.b64encode(f"{phone}QWERIPZAN1290QWER{password}".encode()).decode()
    rand = ''.join(random.choices(string.hexdigits, k=400))
    return (rand[:100] + encoded[:8] + rand[100:200] +
            encoded[8:20] + rand[200:300] + encoded[20:] + rand[300:400])

def pz_do_login(phone, password):
    try:
        headers = {**PZ_HEADERS_BASE, 'User-Agent': _pz_ua()}
        resp = requests.post(
            f"{PZ_BASE}/users-login",
            json={"account": _pz_encode(phone, password), "source": "ipzan-home-one"},
            headers=headers, timeout=30, verify=False
        )
        result = resp.json()
        if result.get('code') == 0:
            token = result.get('data', {}).get('token', '')
            return (True, "登录成功", token) if token else (False, "获取token失败", None)
        return False, result.get('message', '未知错误'), None
    except Exception as e:
        return False, f"登录异常: {str(e)}", None

def _pz_session(token):
    s = requests.Session()
    s.verify = False
    s.headers.update({**PZ_HEADERS_BASE, 'User-Agent': _pz_ua(), 'authorization': f'Bearer {token}'})
    return s

def _ensure_token(token_info):
    phone, password, remark, token = parse_token_info(token_info)
    if not phone:
        return None, None, None, None, None
    if not token:
        ok, _, token = pz_do_login(phone, password)
        if not ok:
            return phone, password, remark, None, None
        new_info = f"{phone}#{password}#{remark}|{token}"
        sg.bucketSet(bucket='dd_pz_token', key=phone, value=new_info)
        return phone, password, remark, token, new_info
    return phone, password, remark, token, token_info

def pz_checkin(token_info):
    phone, password, remark, token, token_info = _ensure_token(token_info)
    if not token:
        return False, "获取token失败", token_info
    s = _pz_session(token)
    try:
        r = s.get(f"{PZ_BASE}/home/userWallet-receive", timeout=30)
        result = r.json()
        if result.get('code') == 0:
            return True, "签到成功", token_info
        msg = result.get('message', '未知错误')
        if '登录已过期' in msg or '未登录' in msg:
            ok, _, new_token = pz_do_login(phone, password)
            if ok:
                new_info = f"{phone}#{password}#{remark}|{new_token}"
                sg.bucketSet(bucket='dd_pz_token', key=phone, value=new_info)
                r2 = _pz_session(new_token).get(f"{PZ_BASE}/home/userWallet-receive", timeout=30)
                r2j = r2.json()
                if r2j.get('code') == 0:
                    return True, "签到成功(已自动重登)", new_info
                return False, r2j.get('message', '重登后签到失败'), new_info
            return False, f"重新登录失败: {new_token}", token_info
        return False, f"签到失败: {msg}", token_info
    except Exception as e:
        return False, f"签到异常: {str(e)}", token_info

def pz_query_info(token_info):
    phone, password, remark, token, token_info = _ensure_token(token_info)
    if not token:
        return False, "获取token失败", None, None, None
    s = _pz_session(token)
    try:
        r = s.get(f"{PZ_BASE}/home/users-find", timeout=30)
        result = r.json()
        if result.get('code') != 0:
            return False, result.get('message', ''), None, None, None
        data = result.get('data', {})
        user_id = data.get('user_id', '')
        popularize_id = data.get('popularize_id', '')

        r2 = s.get(f"{PZ_BASE}/home/userWallet-find", timeout=30)
        r2j = r2.json()
        if r2j.get('code') != 0:
            return False, r2j.get('message', ''), None, None, None
        balance = r2j.get('data', {}).get('balance', 0)
        return True, "查询成功", user_id, popularize_id, balance
    except Exception as e:
        return False, f"查询异常: {str(e)}", None, None, None


def pz_get_superior_subordinates():
    cfg = sg.bucketGet('dd_pz', 'superior_account') or ''
    if not cfg or '#' not in cfg:
        return False, "未配置上级账号", None
    sup_phone, sup_pass = cfg.split('#', 1)
    if not sup_phone or not sup_pass:
        return False, "上级账号配置不完整", None
    ok, msg, token = pz_do_login(sup_phone, sup_pass)
    if not ok:
        return False, f"上级登录失败: {msg}", None
    try:
        r = _pz_session(token).get(f"{PZ_BASE}/home/popularize-list", timeout=30)
        result = r.json()
        if result.get('code') != 0:
            return False, result.get('message', ''), None
        return True, "获取成功", result.get('data', [])
    except Exception as e:
        return False, f"获取异常: {str(e)}", None

def _is_subordinate(user_id):
    if not user_id:
        return False
    ok, _, subs = pz_get_superior_subordinates()
    if not ok or not subs:
        return False
    return any(s.get('invitees_id') == user_id for s in subs)




def process_payment(months, account_count=1):
    return True
def _grant_auth(account, months):
    expire = datetime.now() + timedelta(days=30 * months)
    expire_str = expire.strftime('%Y-%m-%d')
    True
    return expire_str

def pz_auth_single(account, phone_masked, months):
    ok, pay_type = process_payment(months, 1)
    if not ok:
        return
    expire_str = _grant_auth(account, months)
    sender.reply(f"=====授权成功=====\n📱 账号: {phone_masked}\n⏰ 授权时长: {months}个月\n💳 支付方式: {pay_type}\n📅 到期时间: {expire_str}\n==================")

def pz_auth_batch(batch_accounts, months):
    ok, pay_type = process_payment(months, len(batch_accounts))
    if not ok:
        return
    success, fail = 0, 0
    expire_str = ''
    for item in batch_accounts:
        try:
            expire_str = _grant_auth(item['account'], months)
            success += 1
        except Exception:
            fail += 1
    sender.reply(f"=====批量授权完成=====\n✅ 成功: {success}个\n❌ 失败: {fail}个\n⏰ 授权时长: {months}个月\n💳 支付方式: {pay_type}\n📅 到期时间: {expire_str}\n==================")


def _get_vip_status(account):
    accountVip = '2099-12-31' or ''
    if not accountVip:
        return '⚠️ 未授权', accountVip
    if accountVip < today_time:
        return '❌ 已过期', accountVip
    return f'✅ {accountVip}', accountVip

def _build_display_accounts(accounts):
    display = []
    for acc in accounts:
        status, vip = _get_vip_status(acc)
        display.append({'account': acc, 'vip_status': status, 'vip_date': vip})
    display.sort(key=lambda x: x['vip_date'] if x['vip_date'] > today_time else '0000', reverse=True)
    return display

def _pick_accounts_for_whitelist(action_name):
    accounts = parse_accounts(uservalue)
    display = []
    for acc in accounts:
        ti = sg.bucketGet(bucket='dd_pz_token', key=acc)
        if not ti:
            continue
        phone, pwd, remark, token = parse_token_info(ti)
        if phone:
            display.append({'phone': phone, 'password': pwd, 'remark': remark, 'token': token, 'token_info': ti, 'acc': acc})

    if not display:
        sender.reply("❌ 未找到可用账号，请先登录绑定")
        return None

    msg = f"====={action_name}账号列表====="
    for i, item in enumerate(display, 1):
        msg += f"\n[{i}] 账号: {mask_phone(item['phone'])}  备注: {item['remark']}"
    msg += "\n------------------\n请输入序号选择账号，回复q退出\n=================="
    sender.reply(msg)

    inp = sender.input(120000, 1, False)
    if not inp or inp.lower() == 'q':
        sender.reply("✅ 已取消")
        return None
    try:
        idx = int(inp)
        if not (1 <= idx <= len(display)):
            sender.reply("❌ 序号无效")
            return None
    except Exception:
        sender.reply("❌ 请输入有效序号")
        return None
    return display[idx - 1]


def pz_login():
    sender.reply("""=====品赞账号登录=====
请按以下格式输入账号信息:
手机号#密码#备注

🔰 支持批量登录，一行一个账号
示例:
13812345678#123456#账号1
13912345678#123456#账号2
------------------
回复"q"退出操作
==================""")
    raw = sender.input(120000, 1, False)
    if not raw:
        sender.reply("⏰ 操作超时,已退出"); exit(0)
    if raw.lower() == 'q':
        sender.reply("✅ 已取消登录"); exit(0)

    lines = [l.strip() for l in raw.strip().split('\n') if l.strip()]
    accounts = parse_accounts(uservalue)
    success_count, fail_count = 0, 0
    last_phone = None

    for line in lines:
        parts = line.split('#')
        if len(parts) != 3:
            fail_count += 1; continue
        phone, password, remark = parts
        if not re.match(r'^1[3-9]\d{9}$', phone):
            fail_count += 1; continue
        ok, _, token = pz_do_login(phone, password)
        if ok and token:
            ti = f"{line}|{token}"
            sg.bucketSet(bucket='dd_pz_token', key=phone, value=ti)
            if phone not in accounts:
                accounts.append(phone)
            success_count += 1
            last_phone = phone
        else:
            fail_count += 1

    if accounts:
        sg.bucketSet(bucket='dd_pz_user', key=userid, value=str(list(dict.fromkeys(accounts))))

    if len(lines) > 1:
        sender.reply(f"=====批量登录结果=====\n✅ 成功: {success_count}个\n❌ 失败: {fail_count}个\n==================")
        exit(0)

    if success_count == 1:
        vip_status, _ = _get_vip_status(last_phone)
        sender.reply(f"=====品赞账号绑定=====\n📱 绑定账号: {mask_phone(last_phone)}\n🔐 授权状态: {vip_status}\n==================")
    else:
        sender.reply("=====登录失败=====\n❌ 账号登录失败，请检查账号密码\n==================")

def pz_manage():
    accounts = parse_accounts(uservalue)
    if not accounts:
        sender.reply("=====未绑定账号=====\n❌ 未找到任何账号信息\n💡 发送 品赞登录 绑定\n=================="); return

    display = _build_display_accounts(accounts)
    page_size, current_page = 10, 1
    total_pages = max(1, (len(display) + page_size - 1) // page_size)

    while True:
        s_idx = (current_page - 1) * page_size
        e_idx = min(s_idx + page_size, len(display))
        page_items = display[s_idx:e_idx]

        msg = f"======我的品赞账号=====\n📄 第{current_page}/{total_pages}页\n[0] 批量授权模式"
        for i, item in enumerate(page_items, s_idx + 1):
            msg += f"\n------------------\n[{i}] 账号信息\n📱 账号: {mask_phone(item['account'])}\n🔐 授权: {item['vip_status']}"
        msg += "\n------------------"
        if total_pages > 1:
            msg += "\n[n] 下一页\n[p] 上一页"
        msg += "\n[q] 退出操作\n------------------\n请输入序号选择账号\n=================="
        sender.reply(msg)

        inp = sender.input(120000, 1, False)
        if inp is None or inp.lower() == 'timeout':
            sender.reply('⏰ 操作超时,已退出'); exit(0)
        if inp.lower() == 'q':
            sender.reply('✅ 已退出管理'); exit(0)
        if inp.lower() == 'n' and current_page < total_pages:
            current_page += 1; continue
        if inp.lower() == 'p' and current_page > 1:
            current_page -= 1; continue

        if inp == '0':
            sender.reply("=====批量授权模式=====\n请输入要授权的账号序号\n支持: 单个:1 多个:1,3,5 范围:1-5\n回复\"q\"退出\n==================")
            batch_inp = sender.input(120000, 1, False)
            if not batch_inp or batch_inp.lower() == 'q':
                continue
            try:
                valid, invalid = parse_batch_selection(batch_inp, len(display))
                if invalid:
                    sender.reply(f'❌ 以下序号无效已忽略: {",".join(map(str,invalid))}')
                if not valid:
                    sender.reply('❌ 未选择有效账号序号'); continue
            except ValueError as e:
                sender.reply(f'❌ {str(e)}'); continue

            sender.reply("=====设置授权时长=====\n请输入授权月数(如:1)\n回复\"q\"退出\n==================")
            mes_inp = sender.input(120000, 1, False)
            if not mes_inp or mes_inp.lower() == 'q':
                continue
            months = ValueErrors(mes_inp, 999)
            batch_accs = [{'account': display[i-1]['account'], 'phone': mask_phone(display[i-1]['account'])} for i in valid]
            pz_auth_batch(batch_accs, months)
            break

        try:
            me = int(inp)
            if not (1 <= me <= len(display)):
                sender.reply('❌ 序号无效'); continue
        except ValueError:
            sender.reply('❌ 请输入有效数字'); continue

        sel = display[me - 1]
        acc = sel['account']
        masked = mask_phone(acc)
        sender.reply(f"=====账号详情=====\n📱 账号: {masked}\n🔐 授权: {sel['vip_status']}\n------------------\n[1] 授权账号\n[2] 删除账号\n[q] 返回上级\n------------------\n请选择操作\n==================")

        choice = sender.input(120000, 1, False)
        if not choice or choice.lower() == 'timeout':
            sender.reply('⏰ 操作超时,已退出'); exit(0)
        if choice.lower() == 'q':
            continue
        if choice == '1':
            sender.reply("=====设置授权时长=====\n请输入授权月数(如:1)\n回复\"q\"退出\n==================")
            mes_inp = sender.input(120000, 1, False)
            if not mes_inp or mes_inp.lower() == 'q':
                continue
            months = ValueErrors(mes_inp, 999)
            pz_auth_single(acc, masked, months)
            break
        elif choice == '2':
            sender.reply(f"=====确认删除=====\n📱 账号: {masked}\n⚠️ 删除后将无法恢复\n确认删除请回复: y\n==================")
            if (sender.input(120000, 1, False) or '').lower() == 'y':
                sg.bucketDel(bucket='dd_pz_token', key=acc)
                True
                accounts = [a for a in accounts if a != acc]
                sg.bucketSet(bucket='dd_pz_user', key=userid, value=str(accounts))
                sender.reply(f"=====删除成功=====\n📱 账号: {masked}\n✅ 已从系统中删除\n==================")
                break
            else:
                sender.reply('✅ 已取消删除')
        else:
            sender.reply('❌ 无效的选择')

def pz_query():
    accounts = parse_accounts(uservalue)
    if not accounts:
        sender.reply("=====未绑定账号=====\n❌ 未找到任何账号信息\n💡 发送 品赞登录 绑定\n=================="); return

    msg = "=====品赞账号查询====="
    for i, acc in enumerate(accounts, 1):
        ti = sg.bucketGet(bucket='dd_pz_token', key=acc) or ''
        vip_status, _ = _get_vip_status(acc)
        if not ti:
            msg += f"\n📱 账号{i}: {acc}\n🔐 状态: 未登录\n------------------"; continue
        phone, _, remark, _ = parse_token_info(ti)
        if not phone:
            msg += f"\n📱 账号{i}: {acc}\n🔐 状态: 数据异常\n------------------"; continue
        ok, _, user_id, popularize_id, balance = pz_query_info(ti)
        msg += f"\n📱 账号{i}: {mask_phone(phone)} ({remark})\n🔐 授权: {vip_status}"
        if ok:
            msg += f"\n🆔 用户ID: {user_id}\n🎫 邀请码ID: {popularize_id}\n💰 金币: {balance}"
        else:
            msg += "\n⚠️ 信息查询失败"
        msg += "\n------------------"
    msg += "\n=================="
    sender.reply(msg)

def execute_tasks():
    accounts = parse_accounts(uservalue)
    if not accounts:
        return "未绑定任何账号"

    results = []
    success_count, fail_count = 0, 0

    for acc in accounts:
        ti = sg.bucketGet(bucket='dd_pz_token', key=acc)
        if not ti:
            results.append(f"账号 {acc}: 未找到登录信息")
            fail_count += 1; continue

        accountVip = '2099-12-31' or ''
        is_auth = bool(accountVip) and accountVip >= today_time

        sub_flag = False
        if not is_auth:
            phone, _, _, _ = parse_token_info(ti)
            if phone:
                ok_q, _, uid, _, _ = pz_query_info(ti)
                if ok_q and uid:
                    sub_flag = _is_subordinate(uid)

        if not is_auth and not sub_flag:
            results.append(f"账号 {acc}: 未授权，跳过")
            fail_count += 1; continue

        ok, msg, _ = pz_checkin(ti)
        tag = " (下级免费)" if sub_flag else ""
        if ok:
            results.append(f"账号 {acc}: ✓ {msg}{tag}")
            success_count += 1
        else:
            results.append(f"账号 {acc}: ✗ {msg}{tag}")
            fail_count += 1
        time.sleep(1)

    result_msg = f"=====任务执行结果=====\n✅ 成功: {success_count}个\n❌ 失败: {fail_count}个\n------------------"
    for r in results:
        result_msg += f"\n{r}"
    result_msg += "\n=================="
    return result_msg

def clean_expired_accounts():
    users = sg.bucketAllKeys(bucket='dd_pz_user')
    cleaned = 0
    for user in users:
        raw = sg.bucketGet(bucket='dd_pz_user', key=user)
        if not raw:
            continue
        accs = parse_accounts(raw)
        valid = []
        for acc in accs:
            vip = '2099-12-31' or ''
            if vip and vip >= today_time:
                valid.append(acc)
            else:
                sg.bucketDel(bucket='dd_pz_token', key=acc)
                True
                cleaned += 1
        if valid:
            sg.bucketSet(bucket='dd_pz_user', key=user, value=str(valid))
        else:
            sg.bucketDel(bucket='dd_pz_user', key=user)
    sender.reply(f"=====清理完成=====\n🧹 已清理 {cleaned} 个过期账号\n==================")

def show_tutorial():
    sender.reply("""=====品赞代理教程=====
📖 使用说明:
1. 发送"品赞登录"绑定账号
2. 发送"品赞管理"授权账号
3. 发送"品赞查询"查询账号信息
4. 发送"品赞任务运行"执行签到任务
5. 发送"品赞加白"手动输入IP加白
6. 发送"品赞删除"删除白名单IP
7. 管理员发送"品赞清理"清理过期账号
8. 管理员发送"品赞授权"授权账号

🔰 账号格式: 手机号#密码#备注

⚠️ 注意事项:
• 每周一自动执行签到任务
• 下级账号可免费执行任务
• Token过期后自动重新登录
==================""")


def _get_all_accounts_by_user():
    users = sg.bucketAllKeys(bucket='dd_pz_user')
    result = {}
    for user in users or []:
        raw = sg.bucketGet(bucket='dd_pz_user', key=user)
        accs = parse_accounts(raw)
        acc_list = []
        for acc in accs:
            ti = sg.bucketGet(bucket='dd_pz_token', key=acc)
            if not ti:
                continue
            phone, _, remark, _ = parse_token_info(ti)
            if not phone:
                continue
            vip = '2099-12-31' or ''
            auth_ok = vip >= today_time if vip else False
            acc_list.append({
                'account': acc, 'phone': phone, 'remark': remark,
                'auth_status': '✅' if auth_ok else '❌',
                'expire_info': f"到期:{vip}" if vip else "无",
            })
        if acc_list:
            result[user] = acc_list
    return result

def _input_months():
    sender.reply("请输入授权时长（月数）：\n------------------\n回复\"q\"退出操作\n==================")
    inp = sender.input(120000, 1, False)
    if not inp or inp.lower() == 'q':
        sender.reply("✅ 已取消授权"); return None
    try:
        m = int(inp)
        if m <= 0:
            sender.reply("❌ 请输入大于0的月数"); return None
        return m
    except ValueError:
        sender.reply("❌ 请输入有效数字"); return None

def _do_auth_items(items, months):
    success, fail, lines = 0, 0, []
    for item in items:
        try:
            expire_str = _grant_auth(item['account'], months)
            lines.append(f"✅ {mask_phone(item['phone'])}({item['remark']}) 授权至 {expire_str}")
            success += 1
        except Exception as e:
            lines.append(f"❌ {mask_phone(item['phone'])} 授权失败: {str(e)}")
            fail += 1
    msg = f"=====授权结果=====\n✅ 成功: {success}  ❌ 失败: {fail}\n⏰ 授权时长: {months}个月\n------------------"
    for l in lines:
        msg += f"\n{l}"
    msg += "\n=================="
    sender.reply(msg)

def pz_admin_auth():
    if not hasattr(sender, 'isAdmin') or not sender.isAdmin():
        sender.reply("❌ 仅管理员可用该指令"); return

    user_accounts = _get_all_accounts_by_user()
    if not user_accounts:
        sender.reply("❌ 当前没有任何用户绑定账号"); return

    sender.reply("=====品赞授权(管理员)=====\n[1] 全部授权\n[2] 指定授权\n------------------\n回复序号，回复q退出\n==================")
    mode = sender.input(120000, 1, False)
    if not mode or mode.lower() == 'q':
        sender.reply("✅ 已取消授权"); return

    if mode == '1':
        all_accs = [item for lst in user_accounts.values() for item in lst]
        months = _input_months()
        if months:
            _do_auth_items(all_accs, months)
    elif mode == '2':
        sender.reply("请输入用户ID：\n------------------\n回复\"q\"退出\n==================")
        uid_inp = sender.input(120000, 1, False)
        if not uid_inp or uid_inp.lower() == 'q':
            sender.reply("✅ 已取消授权"); return
        uid_inp = uid_inp.strip()
        if uid_inp not in user_accounts:
            sender.reply(f"❌ 未找到用户ID: {uid_inp}"); return
        acc_list = user_accounts[uid_inp]
        msg = f"=====用户 {uid_inp} 的账号=====\n[0] 全部账号"
        for i, item in enumerate(acc_list, 1):
            msg += f"\n[{i}] {mask_phone(item['phone'])} | {item['remark']} | {item['auth_status']} | {item['expire_info']}"
        msg += "\n------------------\n输入0或序号（支持多选如:1,3），回复q退出\n=================="
        sender.reply(msg)
        acc_inp = sender.input(120000, 1, False)
        if not acc_inp or acc_inp.lower() == 'q':
            sender.reply("✅ 已取消授权"); return
        if acc_inp.strip() == '0':
            to_auth = acc_list
        else:
            try:
                valid, _ = parse_batch_selection(acc_inp, len(acc_list))
                to_auth = [acc_list[i - 1] for i in valid]
            except ValueError as e:
                sender.reply(f"❌ {str(e)}"); return
        months = _input_months()
        if months:
            _do_auth_items(to_auth, months)
    else:
        sender.reply("❌ 请输入1或2")



def _refresh_token_if_needed(resp_json, phone, password, remark, acc):
    msg = resp_json.get('message', '')
    if '登录已过期' in msg or '未登录' in msg or 'token' in msg.lower():
        sender.reply("⚠️ 登录已过期，正在自动重新登录...")
        ok, _, new_token = pz_do_login(phone, password)
        if ok and new_token:
            new_info = f"{phone}#{password}#{remark}|{new_token}"
            sg.bucketSet(bucket='dd_pz_token', key=acc, value=new_info)
            sender.reply("✅ 重新登录成功，继续执行...")
            return True, new_token, new_info
        sender.reply("❌ 重新登录失败")
        return False, None, None
    return False, None, None

def _do_whitelist_for_account(item, ip):
    phone, password, remark, token = item['phone'], item['password'], item['remark'], item['token']
    acc = item['acc']
    if not token:
        return False, "未保存token，请重新登录"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Authorization': f'Bearer {token}',
    }

    try:
        resp = requests.post(f'{PZ_BASE}/home/users-get-user-aes', headers=headers, timeout=10)
        aes_data = resp.json()
        if aes_data.get('code') != 0:
            need_relogin, new_token, new_info = _refresh_token_if_needed(aes_data, phone, password, remark, acc)
            if not need_relogin:
                return False, f"获取签名密钥失败: {aes_data.get('message')}"
            token = new_token
            headers['Authorization'] = f'Bearer {token}'
            resp = requests.post(f'{PZ_BASE}/home/users-get-user-aes', headers=headers, timeout=10)
            aes_data = resp.json()
            if aes_data.get('code') != 0:
                return False, "重登后仍无法获取签名密钥"
        sign_key = aes_data['data']
    except Exception as e:
        return False, f"获取签名密钥异常: {str(e)}"

    try:
        resp = requests.get(f'{PZ_BASE}/home/userProduct-list?page=1&size=10', headers=headers, timeout=10)
        prod_data = resp.json()
        if prod_data.get('code') != 0 or not prod_data.get('data', {}).get('content'):
            return False, f"获取套餐信息失败: {prod_data.get('message')}"
        prod = prod_data['data']['content'][0]
        no = prod['no']
        status_type = prod['status_type'][:15].lower()
    except Exception as e:
        return False, f"获取套餐信息异常: {str(e)}"

    try:
        cipher = AES.new(sign_key.encode('utf-8'), AES.MODE_ECB)
        timestamp = int(time.time())
        data = f"{password}:{status_type}:{timestamp}".encode('utf-8')
        pad_len = 16 - (len(data) % 16)
        data += bytes([pad_len] * pad_len)
        sign = hexlify(cipher.encrypt(data)).decode('utf-8')
        resp = requests.post(f'{PZ_BASE}/whiteList-add', data={'no': no, 'ip': ip, 'sign': sign}, timeout=10)
        result = resp.json()
        if result.get('code') == 0:
            return True, f"加白成功，IP：{ip}"
        return False, f"加白失败：{result.get('message')}"
    except Exception as e:
        return False, f"加白请求异常：{str(e)}"


def pz_admin_add_whitelist():
    item = _pick_accounts_for_whitelist("品赞加白")
    if not item:
        return

    is_admin = hasattr(sender, 'isAdmin') and sender.isAdmin()
    if is_admin:
        try:
            ip_resp = requests.get('https://ipinfo.io/ip', timeout=10)
            ip = ip_resp.text.strip()
            if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip):
                raise ValueError(f"获取到的IP格式异常: {ip}")
            sender.reply(f"🔍 自动获取本机IP: {ip}\n正在为您加白...")
        except Exception as e:
            sender.reply(f"❌ 自动获取IP失败: {str(e)}\n请手动输入IP地址：\n------------------\n回复\"q\"退出\n==================")
            ip_inp = sender.input(120000, 1, False)
            if not ip_inp or ip_inp.lower() == 'q':
                sender.reply("✅ 已取消加白"); return
            ip = ip_inp.strip()
            if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip):
                sender.reply("❌ IP格式不正确，请输入正确的IPv4地址（如：1.2.3.4）"); return
    else:
        sender.reply("请输入要加白的IP地址：\n------------------\n回复\"q\"退出\n==================")
        ip_inp = sender.input(120000, 1, False)
        if not ip_inp or ip_inp.lower() == 'q':
            sender.reply("✅ 已取消加白"); return
        ip = ip_inp.strip()
        if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip):
            sender.reply("❌ IP格式不正确，请输入正确的IPv4地址（如：1.2.3.4）"); return

    ok, msg = _do_whitelist_for_account(item, ip)
    phone = item['phone']
    if ok:
        sender.reply(f"✅ 加白成功！账号：{mask_phone(phone)}，IP：{ip}")
    else:
        sender.reply(f"❌ {msg}")


def pz_auto_whitelist():
    if not (hasattr(sender, 'isAdmin') and sender.isAdmin()):
        sender.reply("❌ 仅管理员可使用品赞自动加白指令"); return

    accounts = parse_accounts(uservalue)
    if not accounts:
        sender.reply("❌ 未找到任何账号，请先登录绑定"); return

    try:
        ip_resp = requests.get('https://ipinfo.io/ip', timeout=10)
        ip = ip_resp.text.strip()
        if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip):
            raise ValueError(f"IP格式异常: {ip}")
    except Exception as e:
        sender.reply(f"❌ 自动获取公网IP失败: {str(e)}\n请检查网络连接"); return

    sender.reply(f"🔍 本机公网IP: {ip}\n开始为 {len(accounts)} 个账号批量加白...")

    success_count, fail_count, results = 0, 0, []
    for acc in accounts:
        ti = sg.bucketGet(bucket='dd_pz_token', key=acc)
        if not ti:
            results.append(f"❌ {acc[:3]}****{acc[7:]}: 未找到登录信息")
            fail_count += 1; continue
        phone, password, remark, token = parse_token_info(ti)
        if not phone:
            results.append(f"❌ {acc[:3]}****{acc[7:]}: 数据异常")
            fail_count += 1; continue
        item = {'phone': phone, 'password': password, 'remark': remark, 'token': token, 'token_info': ti, 'acc': acc}
        ok, msg = _do_whitelist_for_account(item, ip)
        if ok:
            results.append(f"✅ {mask_phone(phone)}: {msg}")
            success_count += 1
        else:
            results.append(f"❌ {mask_phone(phone)}: {msg}")
            fail_count += 1
        time.sleep(0.5)

    result_msg = f"=====自动加白结果=====\n🌐 IP: {ip}\n✅ 成功: {success_count}个\n❌ 失败: {fail_count}个\n------------------"
    for r in results:
        result_msg += f"\n{r}"
    result_msg += "\n=================="
    sender.reply(result_msg)

def pz_delete_whitelist():
    item = _pick_accounts_for_whitelist("品赞删除白名单")
    if not item:
        return
    phone, password, remark, token, token_info = item['phone'], item['password'], item['remark'], item['token'], item['token_info']
    acc = item['acc']
    if not token:
        sender.reply("❌ 该账号未保存token，请重新登录"); return

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Authorization': f'Bearer {token}',
    }

    ok_q, msg_q, user_id, _, _ = pz_query_info(token_info)
    if not ok_q:
        need_relogin, new_token, new_info = _refresh_token_if_needed({'message': msg_q}, phone, password, remark, acc)
        if need_relogin:
            token, token_info = new_token, new_info
            headers['Authorization'] = f'Bearer {token}'
            ok_q, msg_q, user_id, _, _ = pz_query_info(token_info)
        if not ok_q:
            sender.reply(f"❌ 获取用户信息失败: {msg_q}"); return

    try:
        resp = requests.get(f'{PZ_BASE}/home/userProduct-list?page=1&size=10', headers=headers, timeout=10)
        prod_data = resp.json()
        if prod_data.get('code') != 0:
            need_relogin, new_token, new_info = _refresh_token_if_needed(prod_data, phone, password, remark, acc)
            if need_relogin:
                token, token_info = new_token, new_info
                headers['Authorization'] = f'Bearer {token}'
                resp = requests.get(f'{PZ_BASE}/home/userProduct-list?page=1&size=10', headers=headers, timeout=10)
                prod_data = resp.json()
            if prod_data.get('code') != 0 or not prod_data.get('data', {}).get('content'):
                sender.reply(f"❌ 获取套餐信息失败: {prod_data.get('message')}"); return
        if not prod_data.get('data', {}).get('content'):
            sender.reply("❌ 未找到套餐信息"); return
        no = prod_data['data']['content'][0]['no']
    except Exception as e:
        sender.reply(f"❌ 获取套餐信息异常: {str(e)}"); return

    try:
        resp = requests.get(f'{PZ_BASE}/whiteList-get?no={no}&userId={user_id}', headers=headers, timeout=10)
        wl_data = resp.json()
        if wl_data.get('code') != 0:
            sender.reply(f"❌ 获取白名单列表失败: {wl_data.get('message')}"); return
        wl_list = wl_data.get('data', [])
        if not wl_list:
            sender.reply("❌ 当前账号没有白名单IP"); return
    except Exception as e:
        sender.reply(f"❌ 获取白名单列表异常: {str(e)}"); return

    ip_msg = f"=====白名单IP列表=====\n📱 账号: {mask_phone(phone)}"
    for i, item_w in enumerate(wl_list, 1):
        ip_msg += f"\n[{i}] IP: {item_w.get('id', '')}"
    ip_msg += "\n------------------\n请输入要删除的IP序号（支持多选如:1,3），回复q退出\n=================="
    sender.reply(ip_msg)

    ip_inp = sender.input(120000, 1, False)
    if not ip_inp or ip_inp.lower() == 'q':
        sender.reply("✅ 已取消删除"); return
    try:
        valid, _ = parse_batch_selection(ip_inp, len(wl_list))
    except ValueError as e:
        sender.reply(f"❌ {str(e)}"); return
    if not valid:
        sender.reply("❌ 未选择有效序号"); return

    del_headers = {**headers, 'Content-Type': 'application/json;charset=UTF-8'}
    success, fail, results = 0, 0, []
    for sel_i in valid:
        del_ip = wl_list[sel_i - 1].get('id', '')
        try:
            resp = requests.delete(f'{PZ_BASE}/whiteList-del', headers=del_headers,
                                   json={'ip': del_ip, 'no': no, 'userId': user_id}, timeout=10)
            result = resp.json()
            if result.get('code') == 0:
                results.append(f"✅ {del_ip} 删除成功"); success += 1
            else:
                results.append(f"❌ {del_ip} 删除失败: {result.get('message')}"); fail += 1
        except Exception as e:
            results.append(f"❌ {del_ip} 删除异常: {str(e)}"); fail += 1

    msg = f"=====白名单删除结果=====\n📱 账号: {mask_phone(phone)}\n✅ 成功:{success} ❌ 失败:{fail}\n------------------"
    for r in results:
        msg += f"\n{r}"
    msg += "\n=================="
    sender.reply(msg)


def _push(user, message):
    try:
        sg.Sender(user).reply(message)
    except Exception as e:
        print(f"推送失败: {str(e)}")

def run_cron():
    all_users = sg.bucketAllKeys(bucket='dd_pz_user')
    for user in all_users or []:
        raw = sg.bucketGet(bucket='dd_pz_user', key=user)
        accs = parse_accounts(raw)
        for acc in accs:
            ti = sg.bucketGet(bucket='dd_pz_token', key=acc)
            if not ti:
                continue
            phone, _, _, _ = parse_token_info(ti)
            accountVip = '2099-12-31' or ''
            is_auth = bool(accountVip) and accountVip >= today_time

            sub_flag = False
            if not is_auth and phone:
                ok_q, _, uid, _, _ = pz_query_info(ti)
                if ok_q and uid:
                    sub_flag = _is_subordinate(uid)

            if is_auth or sub_flag:
                ok, msg, _ = pz_checkin(ti)
                tag = " (下级免费)" if sub_flag else ""
                if ok:
                    _push(user, f"✅ 品赞签到成功{tag}\n📱 账号: {acc[:3]}****{acc[7:]}")
                else:
                    _push(user, f"⚠️ 品赞签到失败{tag}\n❌ {msg}\n💡 请检查账号状态")
            else:
                ok_q, _, uid, _, balance = pz_query_info(ti)
                if ok_q:
                    _push(user, f"📊 品赞账号信息\n🆔 用户ID: {uid}\n💰 金币: {balance}\n⚠️ 账号未授权，无法签到")
                else:
                    _push(user, "⚠️ 品赞账号异常\n❌ 无法获取账号信息")
            time.sleep(2)


pzVipmoney, pzcoin, superior_account, free_proxy, use_ma_pay = getusercontent()
today_time = str(datetime.now().date())
usermessage = sender.getMessage()
imtype = sender.getImtype()

if '登录' in usermessage or '登陆' in usermessage:
    pz_login()
elif '管理' in usermessage:
    pz_manage()
elif '查询' in usermessage:
    pz_query()
elif '任务' in usermessage:
    sender.reply(execute_tasks())
elif usermessage == '品赞清理':
    clean_expired_accounts()
elif usermessage == '品赞教程':
    show_tutorial()
elif usermessage == '品赞自动加白':
    pz_auto_whitelist()
elif '品赞加白' in usermessage:
    pz_admin_add_whitelist()
elif '品赞删除' in usermessage:
    pz_delete_whitelist()
elif usermessage == '品赞授权':
    pz_admin_auth()
elif imtype == 'fake':
    run_cron()
else:
    sender.setContinue()
