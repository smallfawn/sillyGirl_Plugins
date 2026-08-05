# [title: 梨园]
# [name: liYuan]
# [language: python]
# [class: 任务]
# [author: huawei]
# [version: v1.2.2]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(梨园|ly)(扫码|登录|登陆|查询|任务)$]
# [cron: 30 7 * * *]
# [icon: https://api.iconify.design/lucide:apple.svg]
# [description: 梨园行戏曲-金币任务自动化；指令：梨园扫码、梨园查询、梨园任务]
# [depe: ["pycryptodome","requests","urllib3"]]


import asyncio as _sg_asyncio
import os as _sg_os
import time as _sg_time
import types as _sg_types
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
    'G_LYHXQ_proxy_api': form.string().title('代理API').default('').description('代理API地址，留空直连'),
})
_CONFIG_FIELD_MAP = {
    ('G_LYHXQ', 'proxy_api'): 'G_LYHXQ_proxy_api',
}

import json
import re
import time
import uuid
import hashlib
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
import urllib3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BUCKET_USER = "G_LYHXQ_user"
BUCKET_TOKEN = "G_LYHXQ_token"
BUCKET_CONFIG = "G_LYHXQ"

APPID_APP = "wxe2e7e595988751cc"
APP_BUNDLEID = "uni.UNIA317E51"
FLY_BASE = "https://fly.daoran.tv"
AOP_BASE = "http://wechat.daoran.tv"
FLY_MD5 = "SkvyrWqK9QHTdCT12Rhxunjx+WwMTe9y4KwgeASFDhbYabRSPskR0Q=="
AOP_MD5 = "GYWmhK2MfuQtDc9Cj8Fbw9hGoJwQ+f3Wbn0R6KhfUJmoy+8Nz7xP1A=="
SIGN_AES_KEY = b"E5Up6N2RkuWyJc5@"
SIGN_AES_IV = b"z8eFg_b_CSG9~kU9"
APP_SHA1 = "2B8FA3EE98CA3F7270CC599DAB07CF413DE74ABF"
WX_UA = "Mozilla/5.0 (Linux; Android 14; Build/TP1A.220905.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/130.0.6723.103 Mobile Safari/537.36 MicroMessenger/8.0.57.2820 WeChat/arm64"

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()

import threading

proxy_url = sg.bucketGet(BUCKET_CONFIG, 'proxy_api') or ''
IS_PROXY = bool(proxy_url)
_proxy_cache = {}
_proxy_lock = threading.Lock()


def _extract_proxy(raw):
    raw = str(raw or '').strip().strip('"').strip("'")
    if not raw:
        return ''
    if '\n' in raw:
        raw = next((l.strip() for l in raw.split('\n') if l.strip()), '')
    if raw.startswith('{'):
        try:
            data = json.loads(raw)
            if isinstance(data, dict):
                for key in ('proxy', 'data', 'result', 'ip_port', 'socks'):
                    val = data.get(key)
                    if val and isinstance(val, str):
                        return val.strip()
                    if val and isinstance(val, dict) and val.get('ip') and val.get('port'):
                        return f"{val['ip']}:{val['port']}"
                if data.get('ip') and data.get('port'):
                    return f"{data['ip']}:{data['port']}"
        except:
            pass
    return raw


def _build_proxy(raw):
    ip = _extract_proxy(raw)
    if not ip or '白名单' in ip:
        return None
    if '://' not in ip:
        ip = f'http://{ip}'
    return {'http': ip, 'https': ip}


def _is_direct_proxy(source):
    if not source:
        return False
    candidate = source if '://' in source else f'http://{source}'
    from urllib.parse import urlparse
    parsed = urlparse(candidate)
    return bool(parsed.hostname and parsed.port and parsed.path in ('', '/'))


def get_proxy(account_key="default") -> dict:
    if not IS_PROXY:
        return None
    with _proxy_lock:
        cached = _proxy_cache.get(account_key)
        if cached:
            return cached

    if _is_direct_proxy(proxy_url):
        proxy = _build_proxy(proxy_url)
    else:
        for attempt in range(3):
            try:
                r = requests.get(proxy_url, timeout=5, verify=False)
                if r.status_code != 200:
                    time.sleep(1)
                    continue
                proxy = _build_proxy(r.text)
                if proxy:
                    break
            except:
                time.sleep(1)
        else:
            return None

    if proxy:
        with _proxy_lock:
            _proxy_cache[account_key] = proxy
    return proxy


def reset_proxy(account_key="default"):
    with _proxy_lock:
        _proxy_cache.pop(account_key, None)


def generate_sign():
    sha1_md5 = hashlib.md5(APP_SHA1.encode()).hexdigest()
    plaintext = f"daoransign_{sha1_md5}_{int(time.time())}"
    cipher = AES.new(SIGN_AES_KEY, AES.MODE_CBC, SIGN_AES_IV)
    return base64.b64encode(cipher.encrypt(pad(plaintext.encode(), 16))).decode()


def get_user_members() -> list:
    data = sg.bucketGet(BUCKET_USER, userid) or ""
    return [p.strip() for p in data.split(",") if p.strip()]


def save_user_members(members: list):
    sg.bucketSet(BUCKET_USER, userid, ",".join(members))


def get_member_info(member_id: str) -> dict:
    data = sg.bucketGet(BUCKET_TOKEN, member_id) or ""
    if not data:
        return {}
    parts = data.split("#")
    return {"memberId": parts[0], "nick": parts[1] if len(parts) > 1 else ""}


def save_member_info(member_id: str, nick: str):
    sg.bucketSet(BUCKET_TOKEN, member_id, f"{member_id}#{nick}")


def wx_qr_get_uuid():
    try:
        resp = requests.get("https://open.weixin.qq.com/connect/app/qrconnect",
            params={"appid": APPID_APP, "bundleid": APP_BUNDLEID,
                    "scope": "snsapi_userinfo", "state": "lyhxcx", "pass_ticket": str(uuid.uuid4())},
            headers={"User-Agent": WX_UA, "Referer": "https://open.weixin.qq.com/"},
            timeout=15, verify=False)
        m = re.search(r'uuid\s*:\s*"(\w+)"', resp.text)
        return m.group(1) if m else None
    except:
        return None


def wx_qr_check_scan(uuid_str, last=""):
    try:
        params = {"uuid": uuid_str, "f": "url", "_": int(time.time() * 1000)}
        if last:
            params["last"] = last
        resp = requests.get("https://long.open.weixin.qq.com/connect/l/qrconnect",
            params=params, headers={"User-Agent": WX_UA, "Referer": "https://open.weixin.qq.com/"},
            timeout=5, verify=False)
        text = resp.text
        if "window.wx_errcode=405" in text:
            m = re.search(r"oauth\?code=([^&\"']+)", text) or re.search(r"wx_code='([^']+)'", text)
            if m:
                return {"status": "ok", "code": m.group(1)}
        elif "window.wx_errcode=402" in text:
            return {"status": "scanned"}
        elif "window.wx_errcode=408" in text:
            return {"status": "waiting"}
        elif "window.wx_errcode=404" in text:
            return {"status": "waiting"}
    except requests.exceptions.Timeout:
        pass
    except:
        pass
    return {"status": "waiting"}


def wx_qr_login():
    uuid_str = wx_qr_get_uuid()
    if not uuid_str:
        sender.reply("获取二维码失败，请重试")
        return None

    qr_url = f"https://open.weixin.qq.com/connect/qrcode/{uuid_str}"
    sender.reply(f"=====梨园行扫码登录=====\n请用微信扫描二维码:\n[CQ:image,file={qr_url}]\n3分钟内有效，发送 Q 取消等待")

    last = "408"
    scanned_notified = False
    deadline = time.time() + 180
    while time.time() < deadline:
        result = wx_qr_check_scan(uuid_str, last)
        if result["status"] == "ok":
            return result["code"]
        elif result["status"] == "scanned":
            if not scanned_notified:
                sender.reply("已扫码，请在微信上点确认...")
                scanned_notified = True
            last = "402"
        else:
            last = "408"
        try:
            user_msg = sender.waitInput(timeout=2)
            if user_msg and str(user_msg).strip().upper() == 'Q':
                sender.reply("已取消扫码")
                return None
        except:
            pass

    sender.reply("等待超时，请重新发送「梨园扫码」")
    return None


def login_app_with_code(code):
    sign_val = generate_sign()
    try:
        resp = requests.post(f"{FLY_BASE}/API_UBP/wx/app/userinfo",
            headers={"Content-Type": "application/json; charset=UTF-8", "User-Agent": "okhttp/3.12.10",
                     "md5": FLY_MD5, "sign": sign_val, "project": "lyhxcx", "item": "x5"},
            json={"client": "Mobile", "code": code, "devUid": f"sillygirl_{int(time.time())}",
                  "ip": "127.0.0.1", "item": "x5", "needMemberId": True,
                  "project": "lyhxcx", "province": "100", "sign": sign_val},
            proxies=get_proxy(), verify=False, timeout=20)
        result = resp.json()
        if result.get("code") != 10000000:
            return None
        return {
            "memberId": result.get("memberId"),
            "nick": result.get("nickName") or "",
            "bindWX": result.get("bindWX", False),
        }
    except:
        return None


def aop_request(path, member_id, extra=None):
    sign = generate_sign()
    data = {"userId": member_id, "sign": sign, "project": "lyhxcx", "item": "x5"}
    if extra:
        data.update(extra)
    for attempt in range(2):
        try:
            r = requests.post(f"{AOP_BASE}/API_AOP{path}",
                headers={"Content-Type": "application/json; charset=UTF-8", "User-Agent": "okhttp/3.12.10",
                         "md5": AOP_MD5, "sign": sign, "project": "lyhxcx", "item": "x5"},
                json=data, proxies=get_proxy(member_id), verify=False, timeout=15)
            return r.json()
        except:
            reset_proxy(member_id)
            if attempt == 0:
                continue
    return None


def run_tasks(member_id, nick):
    lines = []
    task_resp = aop_request("/act/coin/task/getDetail", member_id, {"actCode": "ott_coin"})
    if not task_resp or task_resp.get("code") != 10000000:
        return f"[{nick}] 获取任务失败"

    task_map = task_resp.get("taskMap", {})
    total_earned = 0
    type_names = {"type2": "签到", "type3": "听戏", "type4": "看视频", "type5": "看短视频", "type6": "广告任务", "type7": "邀请好友", "type1": "额外任务"}

    for type_key, task_info in task_map.items():
        task_type = task_info.get("taskType", 0)
        task_id = task_info.get("taskId", "")
        per_coins = task_info.get("perCoins", 0)
        today_coins = task_info.get("todayCoins", 0)
        max_coins = task_info.get("todayMaxCoins", 0)
        finish_flag = task_info.get("finishFlag", 0)
        task_name = type_names.get(type_key, f"任务{task_type}")

        if finish_flag == 1 or (max_coins > 0 and today_coins >= max_coins):
            lines.append(f"  {task_name}: 已完成({today_coins})")
            continue
        if task_type == 7:
            continue

        if task_type == 2:
            resp = aop_request("/act/coin/task/finish", member_id, {"actCode": "ott_coin", "taskType": task_type, "taskId": task_id})
            if resp and resp.get("result") == 0:
                total_earned += per_coins
                lines.append(f"  {task_name}: +{per_coins}")
            else:
                lines.append(f"  {task_name}: 失败")
            continue

        count = 0
        fail = 0
        max_count = min(50, (max_coins - today_coins) // per_coins + 1) if per_coins > 0 else 10
        sender.reply(f"🔄 {nick} | {task_name} 执行中...")
        while count < max_count and today_coins + (count * per_coins) < max_coins:
            resp = aop_request("/act/coin/task/finish", member_id, {"actCode": "ott_coin", "taskType": task_type, "taskId": task_id})
            if resp and resp.get("result") == 0:
                count += 1
                total_earned += per_coins
                fail = 0
            else:
                fail += 1
                if fail >= 3:
                    break
                time.sleep(0.3)
                continue
            time.sleep(0.1)
        lines.append(f"  {task_name}: +{count * per_coins}")

    task_resp2 = aop_request("/act/coin/task/getDetail", member_id, {"actCode": "ott_coin"})
    if task_resp2 and task_resp2.get("code") == 10000000:
        task_map2 = task_resp2.get("taskMap", {})
        for type_key, task_info in task_map2.items():
            task_type = task_info.get("taskType", 0)
            task_id = task_info.get("taskId", "")
            per_coins = task_info.get("perCoins", 0)
            today_coins = task_info.get("todayCoins", 0)
            max_coins = task_info.get("todayMaxCoins", 0)
            finish_flag = task_info.get("finishFlag", 0)
            task_name = type_names.get(type_key, f"任务{task_type}")

            if finish_flag == 1 or (max_coins > 0 and today_coins >= max_coins) or task_type in (2, 7):
                continue

            remaining = max_coins - today_coins
            if remaining <= 0:
                continue

            count = 0
            fail = 0
            max_count = remaining // per_coins + 1 if per_coins > 0 else 0
            while count < max_count and today_coins + (count * per_coins) < max_coins:
                resp = aop_request("/act/coin/task/finish", member_id, {"actCode": "ott_coin", "taskType": task_type, "taskId": task_id})
                if resp and resp.get("result") == 0:
                    count += 1
                    total_earned += per_coins
                    fail = 0
                else:
                    fail += 1
                    if fail >= 3:
                        break
                    time.sleep(0.3)
                    continue
                time.sleep(0.1)
            if count > 0:
                lines.append(f"  {task_name}(补): +{count * per_coins}")

    cash_msg = do_cash_out(member_id)
    lines.append(f"  {cash_msg}")

    detail = aop_request("/act/coin/task/getDetail", member_id, {"actCode": "ott_coin"})
    current_coins = detail.get("coins", 0) if detail and detail.get("code") == 10000000 else 0

    return f"[{nick}]\n" + "\n".join(lines) + f"\n  本次+{total_earned} | 余额{current_coins}"


def do_cash_out(member_id):
    aop_request("/act/coin/task/cashCoins", member_id, {"actCode": "ott_coin"})

    detail = aop_request("/act/coin/task/getDetail", member_id, {"actCode": "ott_coin"})
    current_coins = detail.get("coins", 0) if detail else 0

    if current_coins < 1000:
        return f"提现: 金币不足(需1000, 当前{current_coins})"
    chosen = (current_coins // 1000) * 1000
    try:
        ad_sign = generate_sign()
        requests.get(f"{FLY_BASE}/API_UBP/xiaomi/ad/clickBack?oaid=37bba68be59bdb7a&pkg=uni.UNIA317E51&dataType=2",
            headers={"User-Agent": "okhttp/3.12.10", "md5": FLY_MD5, "sign": ad_sign, "project": "lyhxcx", "item": "x5"},
            verify=False, timeout=10)
    except:
        pass
    time.sleep(1)

    ex_resp = aop_request("/act/coin/task/exchange", member_id, {"actCode": "ott_coin", "useCoins": chosen})
    if ex_resp and ex_resp.get("result") == 0:
        return f"提现: {chosen}金币成功"
    ret = ex_resp.get("retMsg", "失败") if ex_resp else "失败"
    return f"提现: {ret}"


def process_scan():
    sender.reply("正在获取微信登录二维码...")
    code = wx_qr_login()
    if not code:
        return

    sender.reply("✅ 扫码成功，正在登录...")
    info = login_app_with_code(code)
    if not info:
        sender.reply("❌ 登录失败")
        return

    member_id = info.get("memberId")
    nick = info.get("nick") or "用户"

    if not member_id:
        sender.reply("❌ 该微信号未注册梨园行戏曲APP\n请先在APP内微信登录一次注册")
        return

    save_member_info(member_id, nick)
    members = get_user_members()
    if member_id not in members:
        members.append(member_id)
        save_user_members(members)

    sender.reply(f"✅ 登录成功: {nick}\n正在执行任务...")
    result = run_tasks(member_id, nick)
    sender.reply(result)


def process_query():
    members = get_user_members()
    if not members:
        sender.reply("暂无绑定账号\n💡 发送「梨园扫码」登录")
        return

    lines = ["=====梨园行戏曲====="]
    for mid in members:
        info = get_member_info(mid)
        nick = info.get("nick", mid)
        resp = aop_request("/act/coin/task/getDetail", mid, {"actCode": "ott_coin"})
        coins = resp.get("coins", 0) if resp and resp.get("code") == 10000000 else "查询失败"
        lines.append(f"  {nick}: {coins}金币")
    lines.append("====================")
    sender.reply("\n".join(lines))


def process_task():
    members = get_user_members()
    if not members:
        sender.reply("暂无绑定账号\n💡 发送「梨园扫码」登录")
        return

    sender.reply(f"开始并发执行 {len(members)} 个账号的任务...")

    def _run(mid):
        info = get_member_info(mid)
        nick = info.get("nick", mid)
        return run_tasks(mid, nick)

    results = []
    with ThreadPoolExecutor(max_workers=len(members)) as executor:
        futures = {executor.submit(_run, mid): mid for mid in members}
        for future in as_completed(futures):
            try:
                results.append(future.result())
            except Exception as e:
                results.append(f"[{futures[future]}] 异常: {e}")

    sender.reply("=====梨园行任务报告=====\n" + "\n---\n".join(results) + "\n====================")


def main():
    try:
        msg = sender.getMessage().strip()
    except:
        msg = ""

    if re.match(r"^(梨园|ly)(扫码)$", msg):
        process_scan()
    elif re.match(r"^(梨园|ly)(查询)$", msg):
        process_query()
    elif re.match(r"^(梨园|ly)(任务|登录|登陆)$", msg):
        process_task()
    else:
        sender.setContinue()


main()
