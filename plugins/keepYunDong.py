# [title: Keep运动]
# [name: keepYunDong]
# [language: python]
# [class: 任务]
# [author: 8165799]
# [version: v1.2.2]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(Keep|keep)(登录|登陆|管理|查询|清理|授权|教程)$|^(登录|登陆|管理|查询|清理)(Keep|keep)$]
# [cron: 5 10 * * *]
# [icon: https://api.iconify.design/lucide:bot.svg]
# [description: Keep运动币代挂提交；2. 采用Token配置登录，支持带备注提交；3. 支持查询接口实时获取运动币余额、签到状态和抽奖记录；4.]
# [depe: ["requests"]]
import asyncio as _sg_asyncio
import os as _sg_os
import time as _sg_time
import types as _sg_types
from threading import Thread as _sg_Thread
from sillygirl import Adapter as _SGAdapter, Bucket as _SGBucket, Sender as _SGSender, sender as _sg_sender, plugin

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
    'keep_plugin_panel_type': plugin.Form.string().title('对接面板类型').default('').description('qinglong=青龙面板 daidai=呆呆面板'),
    'keep_plugin_keep_qlname': plugin.Form.string().title('对接系统配置').default('').description('青龙:URL丨ID丨Secret 呆呆:URL丨Key丨Secret'),
    'keep_plugin_keep_osname': plugin.Form.string().title('系统变量名').default('').description('系统容器内变量名(默认为keep)'),
    'keep_plugin_enable_proxy': plugin.Form.boolean().title('启用代理').default(False).description('是否启用代理功能'),
    'keep_plugin_proxy_pool_url': plugin.Form.string().title('代理池地址').default('').description('代理API服务地址'),
    'keep_plugin_enable_remark': plugin.Form.boolean().title('启用备注功能').default(False).description('是否启用账号备注功能'),
    'keep_plugin_admin_notify_ids': plugin.Form.string().title('管理员汇总接收QQ').default('').description('每日自动检测汇总的接收人QQ，多个用|或,分隔'),
})
_CONFIG_FIELD_MAP = {
    ('keep_plugin', 'panel_type'): 'keep_plugin_panel_type',
    ('keep_plugin', 'keep_qlname'): 'keep_plugin_keep_qlname',
    ('keep_plugin', 'keep_osname'): 'keep_plugin_keep_osname',
    ('keep_plugin', 'enable_proxy'): 'keep_plugin_enable_proxy',
    ('keep_plugin', 'proxy_pool_url'): 'keep_plugin_proxy_pool_url',
    ('keep_plugin', 'enable_remark'): 'keep_plugin_enable_remark',
    ('keep_plugin', 'admin_notify_ids'): 'keep_plugin_admin_notify_ids',
}

import re
import ast
from datetime import datetime, timedelta, timezone
import urllib.parse
from decimal import Decimal
import requests
import time
import hashlib
import logging
import base64
import warnings
import random
import string
import traceback
import json
from base64 import urlsafe_b64decode
from concurrent.futures import ThreadPoolExecutor, as_completed

warnings.filterwarnings('ignore', message='Unverified HTTPS request')
requests.packages.urllib3.disable_warnings()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('keep_plugin')

REQUEST_TIMEOUT = 30
MAINTENANCE_CK_MAX_WORKERS = 8
TZ = timezone(timedelta(hours=8))  # 北京时间

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = str(sender.getUserID())
usermessage = sender.getMessage()

try:
    sg.bucketSet(bucket='keep_sender', key=userid, value=str(senderID))
    sg.bucketSet(bucket='keep_imtype', key=userid, value=str(sender.getImtype()))
except:
    pass

def getusercontent():
    panel_type = sg.bucketGet('keep_plugin', 'panel_type') or 'qinglong'
    panel_type = panel_type.lower()

    env_qlconfig = sg.bucketGet('keep_plugin', 'keep_qlname') or ''
    env_name = sg.bucketGet('keep_plugin', 'keep_osname') or 'keep'

    if not env_qlconfig:
        sender.reply("❌ 配置错误：请在插件配置中填写【对接系统配置】(面板信息)。")
        exit(0)

    keep_managecommand = sg.bucketGet('keep_plugin', 'keep_managecommand') or 'Keep管理'
    keep_querycommand = sg.bucketGet('keep_plugin', 'keep_querycommand') or 'Keep查询'
    keep_signcommand = sg.bucketGet('keep_plugin', 'keep_signcommand') or 'Keep登录'

    enable_proxy = (sg.bucketGet('keep_plugin', 'enable_proxy') or 'false').lower() == 'true'
    proxy_pool_url = sg.bucketGet('keep_plugin', 'proxy_pool_url') or ''
    points_bucket = sg.bucketGet('keep_plugin', 'points_bucket') or 'dd_sign_points'
    enable_remark = (sg.bucketGet('keep_plugin', 'enable_remark') or 'false').lower() == 'true'
    admin_notify_ids = sg.bucketGet('keep_plugin', 'admin_notify_ids') or ''

    randommanagecommand = keep_managecommand
    randomquerycommand = keep_querycommand
    randomsigncommand = keep_signcommand

    zsVipmoney = Decimal(sg.bucketGet('keep_plugin', 'zsVipmoney') or '0')
    zscoin = int(sg.bucketGet('keep_plugin', 'zscoin') or '0')
    reminder_days = int(sg.bucketGet('keep_plugin', 'reminder_days') or '2')

    enable_zsm = (sg.bucketGet('keep_plugin', 'enable_zsm') or 'false').lower() == 'true'
    zsm = sg.bucketGet('keep_plugin', 'zsm') or ''

    epay_url = '2099-12-31'
    epay_pid = '2099-12-31'
    epay_key = '2099-12-31'
    epay_alipay = ('2099-12-31').lower() == 'true'
    epay_wxpay = ('2099-12-31').lower() == 'true'
    epay_qqpay = ('2099-12-31').lower() == 'true'

    return {
        'panel_type': panel_type,
        'env_name': env_name,
        'env_qlconfig': env_qlconfig,
        'keep_managecommand': keep_managecommand,
        'keep_querycommand': keep_querycommand,
        'keep_signcommand': keep_signcommand,
        'randommanagecommand': randommanagecommand,
        'randomquerycommand': randomquerycommand,
        'randomsigncommand': randomsigncommand,
        'enable_zsm': enable_zsm,
        'zsm': zsm,
        'enable_proxy': enable_proxy,
        'proxy_pool_url': proxy_pool_url,
        'points_bucket': points_bucket,
        'enable_remark': enable_remark,
        'admin_notify_ids': admin_notify_ids,
        'zsVipmoney': zsVipmoney,
        'zscoin': zscoin,
        'reminder_days': reminder_days,
        'epay_url': epay_url,
        'epay_pid': epay_pid,
        'epay_key': epay_key,
        'epay_alipay': epay_alipay,
        'epay_wxpay': epay_wxpay,
        'epay_qqpay': epay_qqpay
    }

config = getusercontent()

def get_admin_notify_targets():
    raw_value = str(config.get('admin_notify_ids') or '').strip()
    if not raw_value:
        return []
    targets = []
    seen = set()
    for part in re.split(r'[|,，\s]+', raw_value):
        part = str(part).strip()
        if not part or part in seen:
            continue
        seen.add(part)
        targets.append(part)
    return targets

def send_message_to_framework_admins(msg, manual_targets=None):
    notify_func = getattr(sg, 'notifyMasters', None)
    if not callable(notify_func):
        return False

    tried = []
    if manual_targets:
        tried.append(("with_targets", manual_targets))
    tried.extend([
        ("auto_empty_list", []),
        ("auto_none", None),
    ])

    for mode, arg in tried:
        try:
            if arg is None:
                notify_func(msg)
            else:
                notify_func(msg, arg)
            return True
        except TypeError:
            try:
                notify_func(msg)
                return True
            except Exception: pass
        except Exception: pass
    return False

def send_daily_admin_report(report_data, force_send=False, notify_status=False):
    report_date = str(report_data.get('report_date') or datetime.now().date())
    report_key = f"daily_admin_report_{report_date}"
    if not force_send and sg.bucketGet('keep_plugin_runtime', report_key):
        if notify_status:
            sender.reply("ℹ️ 今日管理员汇总已发送过，如需重发请明天自动发送或再次手动清理。")
        return False

    msg = (
        "=====Keep维护完成=====\n"
        f"✅ 检测完成，共 {report_data.get('scanned_accounts', 0)} 个账号\n"
        f"📣 发送通知: {report_data.get('sent_notifications', 0)} 条\n"
        f"🗑️ 清理过期: {report_data.get('cleaned_count', 0)} 个\n"
        "=================="
    )

    admin_targets = get_admin_notify_targets()
    framework_sent = send_message_to_framework_admins(msg, admin_targets)
    if framework_sent:
        try:
            sg.bucketSet('keep_plugin_runtime', report_key, "framework")
        except Exception:
            pass
        if notify_status:
            sender.reply("✅ 管理员汇总已发送（框架自动管理员）")
        return True

    if not admin_targets:
        if notify_status:
            sender.reply("⚠️ 框架管理员自动推送失败，且未填写备用接收QQ。可在插件配置 admin_notify_ids 填 QQ/用户ID 作为兜底。")
        return False

    success_count = 0
    for target in admin_targets:
        ok, err = send_user_notice(str(target), msg, "Keep管理员汇总")
        if ok:
            success_count += 1
        else:
            logger.error(f"发送管理员汇总失败 {target}: {err}")

    if success_count > 0:
        try:
            sg.bucketSet('keep_plugin_runtime', report_key, str(success_count))
        except Exception:
            pass
        if notify_status:
            sender.reply(f"✅ 管理员汇总已发送: {success_count} 人（备用QQ模式）")
        return True
    if notify_status:
        sender.reply("❌ 管理员汇总发送失败，请检查接收QQ/用户ID是否正确。")
    return False

def batch_verify_account_ck(tasks, max_workers=MAINTENANCE_CK_MAX_WORKERS):
    if not tasks:
        return {}

    result_map = {}
    worker_count = min(max_workers, len(tasks))

    def _verify_one(task):
        user, account, token = task
        if not token:
            return (user, account, True)
        try:
            time.sleep(random.uniform(0.1, 0.35))
            client = KeepClient(token)
            return (user, account, client.verify_ck())
        except Exception:
            return (user, account, True)

    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        future_list = [executor.submit(_verify_one, task) for task in tasks]
        for future in as_completed(future_list):
            try:
                user, account, is_valid = future.result()
                result_map[(str(user), str(account))] = is_valid
            except Exception:
                pass

    return result_map

def send_user_notice(user_id, msg, title="Keep通知"):
    try:
        imtype = sg.bucketGet(bucket='keep_imtype', key=str(user_id)) or sender.getImtype()
    except:
        imtype = sender.getImtype()

    push_targets = [
        (imtype, "", str(user_id)),
        (sender.getImtype(), "", str(user_id)),
    ]
    last_error = "未知错误"
    for im_type, group_code, target_user in list(dict.fromkeys(push_targets)):
        for func_name in ['Push', 'push']:
            push_func = getattr(sg, func_name, None)
            if not callable(push_func):
                continue
            try:
                push_func(str(im_type), str(group_code), str(target_user), title, msg)
                return True, ""
            except Exception as e:
                last_error = f"{func_name}({im_type},{target_user}): {str(e) or e.__class__.__name__}"

    targets = []
    try:
        saved_sender = sg.bucketGet(bucket='keep_sender', key=str(user_id))
        if saved_sender:
            targets.append(str(saved_sender))
    except:
        pass
    targets.append(str(user_id))

    method_names = ['Reply', 'reply', 'ReplyMarkdown', 'replyMarkdown', 'send', 'replyText', 'sendText', 'push', 'sendMsg', 'sendMessage']
    for target in list(dict.fromkeys(targets)):
        try:
            target_sender = sg.Sender(target)
        except Exception as e:
            last_error = f"Sender({target})初始化失败: {str(e) or e.__class__.__name__}"
            continue

        tried_methods = []
        for method_name in method_names:
            method = getattr(target_sender, method_name, None)
            if not callable(method):
                continue
            tried_methods.append(method_name)
            try:
                method(msg)
                return True, ""
            except Exception as e:
                last_error = f"{method_name}: {str(e) or e.__class__.__name__}"

        if not tried_methods:
            available = [name for name in dir(target_sender) if not name.startswith('_')]
            last_error = "无可用发送方法，可用方法: " + ",".join(available[:12])
    return False, last_error

def safe_send_message(user_id, msg, log_context=""):
    ok, err = send_user_notice(user_id, msg, "Keep提醒")
    if not ok:
        logger.warning(f"消息发送失败 {log_context}: {err}")
    return ok

def sync_local_auth_from_panel():
    return True

def mask_account(account):
    account = str(account)
    return account[:4] + "****" + account[-4:] if len(account) > 8 else account

def get_account_display(account, remark=""):
    remark = str(remark or "").strip()
    return remark if remark else mask_account(account)

def is_cron_trigger():
    imtype = ""
    try:
        imtype = str(sender.getImtype() or "").lower()
    except:
        pass
    msg = str(usermessage or "").strip().lower()
    return imtype in ["fake", "cron"] or msg in ["", "cron", "定时任务"]

def encrypt_token(token):
    try:
        return base64.b64encode(token.encode()).decode()
    except:
        return token

def decrypt_token(encrypted_token):
    try:
        return base64.b64decode(encrypted_token.encode()).decode()
    except:
        return encrypted_token

def normalize_keep_token(raw_token):
    token = str(raw_token or "").strip().strip('"').strip("'")
    if not token:
        return ""

    token = re.sub(r'^(authorization|auth|token)\s*[:=]\s*', '', token, flags=re.I).strip()
    if re.match(r'^bearer\s+', token, flags=re.I):
        token = re.sub(r'^bearer\s+', '', token, flags=re.I).strip()
        return f"Bearer {token}"

    if re.match(r'^[A-Za-z0-9\-_=.]+\.[A-Za-z0-9\-_=.]+\.[A-Za-z0-9\-_=.]+$', token):
        return f"Bearer {token}"
    return token

def random_device_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=32))

def decode_jwt_payload(token):
    try:
        if token.startswith("Bearer "):
            token = token[7:]
        parts = token.split('.')
        if len(parts) != 3:
            return None
        payload = parts[1]
        payload += '=' * (4 - len(payload) % 4)
        decoded = urlsafe_b64decode(payload)
        data = json.loads(decoded)
        return data.get("_id")
    except:
        return None

class KeepClient:
    def __init__(self, token_str):
        self.raw_token = normalize_keep_token(token_str)
        if not self.raw_token.startswith("Bearer ") and len(self.raw_token) > 50:
            self.auth_token = f"Bearer {self.raw_token}"
        else:
            self.auth_token = self.raw_token

        self.user_id = decode_jwt_payload(self.auth_token)
        self.device_id = random_device_id()
        self.uid_type = "jwt_id" if self.user_id else "token_md5"
        self.uid = self.user_id or hashlib.md5(self.auth_token.encode()).hexdigest()[:10]

        self.headers = {
            "User-Agent": "Keep/8.7.80 (Android 12; Xiaomi Redmi K30 Pro)",
            "x-app-platform": "keepapp",
            "x-version-name": "8.7.80",
            "x-version-code": "49487",
            "x-os": "Android",
            "x-os-version": "12",
            "x-model": "Redmi K30 Pro",
            "x-device-id": self.device_id,
            "x-is-guest": "N",
            "x-channel": "xiaomi_store___",
            "x-locale": "zh--CN",
            "x-keep-timezone": "Asia/Shanghai",
            "x-curpage": "mine",
            "x-screen-width": "392",
            "x-screen-height": "872",
            "x-manufacturer": "Xiaomi",
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Authorization": self.auth_token
        }
        if self.user_id:
            self.headers["x-user-id"] = self.user_id

    def request(self, method, url, params=None, json_data=None, host="https://api.gotokeep.com"):
        full_url = host + url
        headers = self.headers.copy()
        headers["Host"] = host.split("://")[1]
        if params:
            full_url += "?" + urllib.parse.urlencode(params)

        proxy = None
        if config.get('enable_proxy') and config.get('proxy_pool_url'):
            try:
                res = requests.get(config['proxy_pool_url'], timeout=5, verify=False)
                match = re.search(r'(?:https?://)?\d+\.\d+\.\d+\.\d+:\d+', res.text)
                if match:
                    proxy_url = match.group(0)
                    if not proxy_url.startswith(('http://', 'https://')):
                        proxy_url = f"http://{proxy_url}"
                    proxy = {'http': proxy_url, 'https': proxy_url}
            except: pass

        try:
            if method.upper() == "GET":
                resp = requests.get(full_url, headers=headers, proxies=proxy, timeout=15, verify=False)
            else:
                resp = requests.post(full_url, headers=headers, json=json_data, proxies=proxy, timeout=15, verify=False)

            if resp.status_code == 429:
                return {"_status_code": 429, "ok": False}
            if resp.status_code >= 400:
                try:
                    err_data = resp.json()
                    err_data["_status_code"] = resp.status_code
                    err_data["ok"] = False
                    return err_data
                except: return None
            return resp.json()
        except Exception:
            return None

    def get_coin_balance(self):
        url = "/api/v1/marketing/sportCoin/home"
        data = self.request("GET", url, host="https://store.gotokeep.com")
        if data and data.get("ok"):
            inner = data.get("data") or {}
            return inner.get("userSportsCoinNum")
        return None

    def get_sign_info(self):
        url = "/dune-webapp/sportcoin/sign/in/info"
        data = self.request("GET", url)
        if data is None:
            return None
        if isinstance(data, dict) and data.get("_status_code") == 429:
            return {"today_already_signed": True}
        if data.get("ok"):
            return data.get("data") or {}
        return None

    def find_today_item(self, sign_list):
        for item in sign_list or []:
            day_text = str(item.get('day', '') or '')
            if '今' in day_text:
                return item
        return None

    def find_tomorrow_item(self, sign_list):
        for item in sign_list or []:
            day_text = str(item.get('day', '') or '')
            if '明' in day_text:
                return item
        return None

    def get_lotto_records(self, page=1, size=5):
        url = "/dune-webapp/lotto/user/list"
        params = {"page": page, "size": size}
        data = self.request("GET", url, params=params)
        if data and data.get("ok"):
            tasks = (data.get("data") or {}).get("tasks", [])
            records = []
            for t in tasks:
                records.append({
                    "date": t.get("roundNote", ""),
                    "award": t.get("awardName", "未知"),
                    "status": t.get("statusNote", ""),
                })
            return records
        return []

    def get_info(self):
        try:
            balance = self.get_coin_balance()
            if balance is None:
                return True, False, 0, "登录失效或Token已过期"

            sign_info = self.get_sign_info()
            sign_msg = "未知状态"
            if sign_info:
                if sign_info.get("today_already_signed"):
                    sign_msg = "✅ 今日已签到"
                else:
                    sign_list = sign_info.get("signInList", [])
                    today_item = self.find_today_item(sign_list)
                    if today_item and not today_item.get("signIn", False):
                        coin_expected = today_item.get("sportCoinNum", "?")
                        sign_msg = f"⏳ 今日待签到 (预计可得 {coin_expected} 币)"
                    elif today_item and today_item.get("signIn", False):
                        sign_msg = "✅ 今日已签到"
                    else:
                        tomorrow_item = self.find_tomorrow_item(sign_list)
                        if tomorrow_item:
                            sign_msg = "✅ 今日已签到"
                        elif sign_list:
                            signed_count = sum(1 for item in sign_list if item.get("signIn"))
                            sign_msg = "✅ 今日已签到" if signed_count else "❌ 今日未签到"
                        else:
                            sign_msg = "🕒 签到状态待确认"

            lotto_msg = "未查询到记录"
            try:
                records = self.get_lotto_records(page=1, size=5)
                today = datetime.now(TZ).strftime("%Y.%m.%d")
                today_rec = next((r for r in records if r['date'] == today), None)
                if today_rec:
                    if today_rec['status'] != "未中奖" and today_rec['award'] != "谢谢参与":
                        lotto_msg = f"🎉 {today_rec['status']} ({today_rec['award']})"
                    else:
                        lotto_msg = "😔 今日未中奖"
                else:
                    lotto_msg = "🕒 今日暂未抽奖"
            except:
                pass

            msg = f"💰运动币余额: {balance} 币\n📅签到状态: {sign_msg}\n🎁今日抽奖: {lotto_msg}"
            return True, True, balance, msg
        except Exception as e:
            return False, True, 0, str(e)

    def verify_ck(self):
        net_ok, is_valid, _, _ = self.get_info()
        if net_ok and not is_valid:
            return False
        return True

    def check_info(self):
        safe_id = self.uid[:4] + "****" + self.uid[-4:] if len(self.uid) > 8 else self.uid
        nickname = f"Keep_{safe_id}"

        return {
            "nickname": nickname,
            "phone": self.uid,
            "acc_key": self.uid,
            "acc_type": self.uid_type,
            "aliases": [self.uid, hashlib.md5(self.auth_token.encode()).hexdigest()[:10]],
            "legacy_key": hashlib.md5(self.auth_token.encode()).hexdigest()[:8],
            "final_token": self.auth_token
        }

class RemarkManager:
    @staticmethod
    def get_account_remark(user_id, account_id):
        try:
            remark_data = sg.bucketGet(bucket='keep_remarks', key=f'{user_id}_{account_id}')
            return str(remark_data) if remark_data else ""
        except: return ""

    @staticmethod
    def set_account_remark(user_id, account_id, remark):
        try:
            remark_clean = str(remark).strip()[:20]
            if remark_clean:
                sg.bucketSet(bucket='keep_remarks', key=f'{user_id}_{account_id}', value=remark_clean)
                return remark_clean
            return ""
        except: return ""

    @staticmethod
    def get_all_remarks(user_id):
        try:
            accounts = AccountManager.get_accounts(user_id)
            remarks = {}
            for account in accounts:
                remark = RemarkManager.get_account_remark(user_id, account)
                if remark: remarks[str(account)] = remark
            return remarks
        except: return {}

    @staticmethod
    def delete_account_remark(user_id, account_id):
        try:
            sg.bucketDel(bucket='keep_remarks', key=f'{user_id}_{account_id}')
            return True
        except: return False

class AccountManager:
    @staticmethod
    def get_accounts(user_id):
        try:
            value = sg.bucketGet(bucket='keep_user', key=str(user_id))
            if not value: return []
            if value.startswith('[') and value.endswith(']'):
                try:
                    accounts = ast.literal_eval(value)
                    if isinstance(accounts, (list, tuple, set)):
                        return [str(x) for x in list(dict.fromkeys(accounts))]
                except: pass
            return [str(value)]
        except: return []

    @staticmethod
    def add_account(user_id, account):
        try:
            account = str(account)
            accounts = AccountManager.get_accounts(user_id)
            if account not in accounts:
                accounts.append(account)
                sg.bucketSet(bucket='keep_user', key=str(user_id), value=str(accounts))
                return True
            return False
        except: return False

    @staticmethod
    def remove_account(user_id, account):
        try:
            account = str(account)
            accounts = AccountManager.get_accounts(user_id)
            if account in accounts:
                accounts.remove(account)
                if accounts:
                    sg.bucketSet(bucket='keep_user', key=str(user_id), value=str(accounts))
                else:
                    sg.bucketDel(bucket='keep_user', key=str(user_id))
                return True
            return False
        except: return False

    @staticmethod
    def update_account_token(account, token):
        try:
            encrypted_token = encrypt_token(str(token))
            sg.bucketSet(bucket='keep_token', key=str(account), value=encrypted_token)
            return True
        except: return False

    @staticmethod
    def get_token(account):
        try:
            enc = sg.bucketGet(bucket='keep_token', key=str(account))
            return decrypt_token(enc) if enc else None
        except: return None

    @staticmethod
    def get_all_users():
        try:
            users = sg.bucketAllKeys(bucket='keep_user')
            user_list = []
            for user in users:
                accounts = AccountManager.get_accounts(user)
                if accounts: user_list.append(str(user))
            return user_list
        except: return []

    @staticmethod
    def migrate_account(user_id, old_account, new_account, new_token, remark=""):
        try:
            old_account = str(old_account)
            new_account = str(new_account)
            if not old_account or not new_account or old_account == new_account:
                return False

            accounts = AccountManager.get_accounts(user_id)
            if old_account not in accounts:
                return False

            old_vip = '2099-12-31'
            new_vip = '2099-12-31'
            if old_vip and (not new_vip or str(old_vip) > str(new_vip)):
                True

            old_bind_date = sg.bucketGet(bucket='keep_bind_date', key=old_account)
            if old_bind_date and not sg.bucketGet(bucket='keep_bind_date', key=new_account):
                sg.bucketSet(bucket='keep_bind_date', key=new_account, value=old_bind_date)

            if config['enable_remark']:
                old_remark = RemarkManager.get_account_remark(user_id, old_account)
                final_remark = remark or old_remark
                if final_remark:
                    RemarkManager.set_account_remark(user_id, new_account, final_remark)
                RemarkManager.delete_account_remark(user_id, old_account)

            new_accounts = []
            for acc in accounts:
                if acc == old_account:
                    acc = new_account
                if acc not in new_accounts:
                    new_accounts.append(acc)
            sg.bucketSet(bucket='keep_user', key=str(user_id), value=str(new_accounts))

            AccountManager.update_account_token(new_account, new_token)
            try: sg.bucketDel(bucket='keep_token', key=old_account)
            except: pass
            try:
                pass
            except: pass
            return True
        except Exception as e:
            logger.error(f"Account migrate failed: {e}")
            return False

    @staticmethod
    def find_migration_source(user_id, new_account, aliases=None, acc_type="", legacy_key=""):
        try:
            new_account = str(new_account)
            legacy_key = str(legacy_key or "")
            aliases = [str(x) for x in (aliases or []) if str(x)]

            new_ids = set(aliases)
            if acc_type != "token_md5" and acc_type != "jwt_id":
                new_ids.add(new_account)
            if legacy_key:
                new_ids.discard(legacy_key)

            for old_account in AccountManager.get_accounts(user_id):
                old_account = str(old_account)
                if old_account == new_account:
                    continue
                if old_account in new_ids:
                    return old_account

                old_token = AccountManager.get_token(old_account)
                if not old_token:
                    continue

                old_client = KeepClient(old_token)
                old_info = old_client.check_info()
                old_ids = set(old_info.get('aliases', []))
                if old_info.get('acc_type') not in ("token_md5", "jwt_id"):
                    old_ids.add(str(old_info.get('acc_key', "")))
                old_legacy = str(old_info.get('legacy_key', ""))
                if old_legacy:
                    old_ids.discard(old_legacy)

                if new_ids and old_ids and (new_ids & old_ids):
                    return old_account
            return ""
        except Exception as e:
            logger.error(f"Find migration source failed: {e}")
            return ""

class SystemAPI:
    def __init__(self):
        self.enabled = False
        self.panel_type = config.get('panel_type', 'qinglong')
        ql_config = config['env_qlconfig']
        try:
            if not ql_config: raise ValueError("对接配置为空")
            qllist = ql_config.split('丨')
            if len(qllist) != 3: raise ValueError("对接配置格式错误")
            self.QLurl = qllist[0].strip().rstrip('/')
            self.ClientID = qllist[1].strip()
            self.ClientSecret = qllist[2].strip()

            if self.panel_type == 'daidai':
                self.access_token = self._get_daidai_token()
            else:
                self.qltoken = self._get_ql_token()
            self.enabled = True
        except Exception as e:
            logger.error(f"系统初始化失败: {e}")

    def _get_ql_token(self):
        try:
            url = f"{self.QLurl}/open/auth/token?client_id={self.ClientID}&client_secret={self.ClientSecret}"
            response = requests.get(url, timeout=10, verify=False)
            if response.status_code == 200:
                return response.json()['data']['token']
            raise Exception("获取青龙Token失败")
        except Exception: raise

    def _get_daidai_token(self):
        try:
            url = f"{self.QLurl}/api/open-api/token"
            data = {"app_key": self.ClientID, "app_secret": self.ClientSecret}
            response = requests.post(url, json=data, timeout=10, verify=False)
            if response.status_code == 200:
                return response.json()['data']['access_token']
            raise Exception("获取呆呆Token失败")
        except Exception: raise

    def get_all_envs(self):
        if not self.enabled: return []
        try:
            if self.panel_type == 'daidai':
                url = f"{self.QLurl}/api/envs?keyword={config['env_name']}&page_size=9999"
                headers = {"Authorization": f"Bearer {self.access_token}", "accept": "application/json"}
                response = requests.get(url, headers=headers, timeout=10, verify=False)
                if response.status_code == 200:
                    return response.json().get('data', [])
                return []
            else:
                url = f"{self.QLurl}/open/envs"
                headers = {"Authorization": f"Bearer {self.qltoken}", "accept": "application/json"}
                response = requests.get(url, headers=headers, timeout=10, verify=False)
                if response.status_code == 200:
                    return response.json()['data']
                return []
        except: return []

    def find_env(self, phone, token=None):
        if not self.enabled: return None
        phone = str(phone)
        try:
            envs = self.get_all_envs()
            for env in envs:
                if env.get('name') != config['env_name']: continue

                env_id = env.get('id') if env.get('id') is not None else env.get('_id')

                if env.get('remarks') and f'ID:{phone}' in env.get('remarks'):
                    return env_id

                if env.get('remarks') and phone in env.get('remarks'):
                    return env_id

                if token and env.get('value'):
                    env_val = env.get('value').strip()
                    input_val = str(token).strip()
                    if input_val in env_val:
                        return env_id

            return None
        except: return None

    def find_env_ids(self, phone, token=None):
        if not self.enabled: return []
        phone = str(phone)
        token = str(token or "").strip()
        try:
            envs = self.get_all_envs()
            matched_ids = []
            matched_set = set()
            for env in envs:
                if env.get('name') != config['env_name']:
                    continue

                env_id = env.get('id') if env.get('id') is not None else env.get('_id')
                if env_id is None:
                    continue

                env_remarks = str(env.get('remarks') or '')
                env_value = str(env.get('value') or '').strip()
                is_match = False

                if env_remarks and f'ID:{phone}' in env_remarks:
                    is_match = True
                elif env_remarks and phone in env_remarks:
                    is_match = True
                elif token and env_value and token in env_value:
                    is_match = True

                if is_match:
                    env_id_key = str(env_id)
                    if env_id_key not in matched_set:
                        matched_set.add(env_id_key)
                        matched_ids.append(env_id)

            return matched_ids
        except:
            return []

    def delete_env(self, phone, token=None):
        if not self.enabled: return False
        phone = str(phone)
        try:
            env_ids = self.find_env_ids(phone, token)
            if not env_ids:
                env_id = self.find_env(phone, token)
                if env_id is not None:
                    env_ids = [env_id]
            if not env_ids:
                return False

            if self.panel_type == 'daidai':
                headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
                success = False
                for env_id in env_ids:
                    url = f"{self.QLurl}/api/envs/{env_id}"
                    res = requests.delete(url, headers=headers, timeout=10, verify=False)
                    if res.status_code == 200:
                        success = True
                return success
            else:
                url = f"{self.QLurl}/open/envs"
                headers = {"Authorization": f"Bearer {self.qltoken}", "Content-Type": "application/json"}
                res = requests.delete(url, headers=headers, json=env_ids, timeout=10, verify=False)
                return res.status_code == 200
        except: return False

    def sync_env(self, token, phone, remark="", auth_time=""):
        if not self.enabled: return False
        phone = str(phone)
        try:
            env_id = self.find_env(phone, token)

            ql_value = f"{token}"

            safe_phone = mask_account(phone)
            remarks_parts = [f'Keep:{safe_phone}']
            if auth_time: remarks_parts.append(f'到期:{auth_time}')
            else: remarks_parts.append('到期:未授权')
            if remark: remarks_parts.append(f'备注:{remark}')

            remarks_parts.extend([f'用户:{userid}', f'ID:{phone}', 'Keep提交'])
            final_remark = '丨'.join(remarks_parts)

            if self.panel_type == 'daidai':
                headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
                if env_id is not None:
                    url = f"{self.QLurl}/api/envs/{env_id}"
                    data = {"name": config['env_name'], "value": ql_value, "remarks": final_remark}
                    res = requests.put(url, headers=headers, json=data, timeout=10, verify=False)
                    if res.status_code == 200:
                        try: requests.put(f"{self.QLurl}/api/envs/{env_id}/enable", headers=headers, timeout=5, verify=False)
                        except: pass
                    else: return False
                else:
                    url = f"{self.QLurl}/api/envs"
                    data = {"name": config['env_name'], "value": ql_value, "remarks": final_remark}
                    res = requests.post(url, headers=headers, json=data, timeout=10, verify=False)
                    if res.status_code != 200: return False
            else:
                headers = {"Authorization": f"Bearer {self.qltoken}", "Content-Type": "application/json"}
                url = f"{self.QLurl}/open/envs"
                if env_id is not None:
                    data = {"value": ql_value, "name": config['env_name'], "remarks": final_remark}
                    if isinstance(env_id, int) or str(env_id).isdigit():
                        data["id"] = env_id
                    else:
                        data["_id"] = env_id

                    res = requests.put(url, headers=headers, json=data, timeout=10, verify=False)
                    if res.status_code == 200:
                        try: requests.put(f"{self.QLurl}/open/envs/enable", headers=headers, json=[env_id], timeout=5, verify=False)
                        except: pass
                    else: return False
                else:
                    data = [{"value": ql_value, "name": config['env_name'], "remarks": final_remark}]
                    res = requests.post(url, headers=headers, json=data, timeout=10, verify=False)
                    if res.status_code != 200: return False
            return True
        except Exception as e:
            logger.error(f"Sync Env Error: {e}")
            return False

try:
    sys_api = SystemAPI()
    if not sys_api.enabled and sender.getImtype() != 'fake':
        sender.reply("⚠️ 系统API初始化失败，青龙/呆呆同步功能不可用，请检查配置。")
except:
    sys_api = type('obj', (object,), {'enabled': False, 'sync_env': lambda *a, **k: None, 'delete_env': lambda *a, **k: None})()
    if sender.getImtype() != 'fake':
        sender.reply("⚠️ 系统API初始化异常，青龙/呆呆同步功能不可用，请检查配置。")

def process_single_account_query(account, index, total_count, account_remarks):
    try:
        account = str(account)
        full_token = AccountManager.get_token(account)
        if not full_token: full_token = ""

        accountVip = '2099-12-31'
        remark = account_remarks.get(account, "") if config['enable_remark'] else ""

        today_time = str(datetime.now().date())
        if not accountVip:
            auth_time = "无"
        elif accountVip <= today_time:
            auth_time = f"{accountVip} (已过期)"
        else:
            auth_time = accountVip

        account_display = get_account_display(account, remark)

        if accountVip and accountVip > today_time:
            try:
                if not full_token or len(full_token) < 20:
                    raise Exception("凭证异常或为空")

                client = KeepClient(full_token)
                client.check_info()
                nickname = account_display

                net_ok, is_valid, balance, msg = client.get_info()
                if net_ok and not is_valid:
                    status_text = f"⚠️ 账号登录失败: {msg}"
                elif not net_ok:
                    status_text = f"⚠️ 网络查询异常: {str(msg)[:50]}"
                else:
                    status_text = f"✅ 当前状态: 正常\n{msg}"

                account_info = f"""
=====Keep详情=====
🚀 平台: Keep运动币
👤 账号: {nickname}
{status_text}
⏰ 授权到期: {auth_time}"""
                return account_info.strip()
            except Exception as e:
                return f"""
=====Keep查询异常=====
📱 账号: {account_display}
❌ 错误: {str(e)[:50]}
=================="""
        else:
            return f"""
=====Keep状态=====
📱 账号: {account_display}
📝 备注: {remark if remark else "无"}
🔐 授权: {'⚠️ 未授权' if not accountVip else ('❌ 已过期' if accountVip < today_time else f'✅ {accountVip}')}
⏰ 到期: {auth_time}
=================="""
    except Exception:
        return None

def cxs():
    try:
        accounts = AccountManager.get_accounts(userid)
        if not accounts:
            sender.reply(f"""
=====未绑定账号=====
❌ 未找到任何账号信息
💡 发送 {config['randomsigncommand']} 绑定
==================""")
            return

        account_remarks = {}
        if config['enable_remark']:
            account_remarks = RemarkManager.get_all_remarks(userid)

        total_count = len(accounts)
        today_time = str(datetime.now().date())

        menu = "=====Keep查询====="
        for i, acc in enumerate(accounts, 1):
            acc = str(acc)
            remark = account_remarks.get(acc, "") if config['enable_remark'] else ""
            account_display = get_account_display(acc, remark)
            vip = '2099-12-31'
            if not vip:
                vip_tag = '⚠️未授权'
            elif vip < today_time:
                vip_tag = '❌已过期'
            else:
                vip_tag = f'✅{vip}'
            menu += f"\n[{i}] {account_display} {vip_tag}"
        menu += "\n------------------\n[a] 查询全部\n支持单选/多选/区间，如 1,2 或 3-6\n回复q退出\n=================="
        sender.reply(menu)

        sel = get_user_input(timeout=60)
        if not sel or sel.lower() == 'q':
            sender.reply("✅ 已退出")
            return

        if sel.lower() == 'a':
            target_accounts = list(enumerate(accounts, 1))
        else:
            selected_idxs, invalid_parts = parse_index_selection(sel, total_count, allow_all=False)
            target_accounts = [(idx, accounts[idx - 1]) for idx in selected_idxs]

            if not target_accounts:
                sender.reply("❌ 请输入有效序号，例如 1,2 或 3-6")
                return
            if invalid_parts:
                sender.reply(f"⚠️ 已忽略无效内容: {','.join(invalid_parts[:5])}")

        sender.reply(f"🚀 正在查询 {len(target_accounts)} 个账号，请稍候...")
        max_workers = min(10, len(target_accounts))
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_account = {}
            for index, account in target_accounts:
                future = executor.submit(process_single_account_query, account, index, total_count, account_remarks)
                future_to_account[future] = account

            for future in as_completed(future_to_account):
                result_msg = future.result()
                if result_msg: sender.reply(result_msg)

    except Exception as e:
        logger.error(f"批量查询失败: {e}")
        sender.reply(f"❌ 查询失败: {e}")

def notify_authorized_users():
    return True

def get_user_input(timeout=60):
    try:
        response = sender.listen(timeout * 1000)
        if not response: return None
        response = response.strip()
        if response.lower() in ['q', 'quit', 'exit', '退出', 'cancel']: return 'q'
        return response
    except: return None

def parse_index_selection(text, total_count, allow_all=True):
    try:
        if text is None:
            return [], []
        raw = str(text).strip()
        if not raw:
            return [], []
        if allow_all and raw.lower() in ['a', 'all', '全部', '全选']:
            return list(range(1, total_count + 1)), []

        selected = []
        invalid = []
        parts = re.split(r'[,\s，、;；]+', raw)
        for part in parts:
            part = part.strip()
            if not part:
                continue

            range_match = re.match(r'^(\d+)\s*(?:-|~|到|至)\s*(\d+)$', part)
            if range_match:
                start = int(range_match.group(1))
                end = int(range_match.group(2))
                if start > end:
                    start, end = end, start
                start = max(1, start)
                end = min(total_count, end)
                if start <= end:
                    selected.extend(range(start, end + 1))
                else:
                    invalid.append(part)
                continue

            if part.isdigit():
                idx = int(part)
                if 1 <= idx <= total_count:
                    selected.append(idx)
                else:
                    invalid.append(part)
                continue

            invalid.append(part)

        return list(dict.fromkeys(selected)), invalid
    except:
        return [], [str(text)]

def bindaccount():
    try:
        remark = ""
        if config['enable_remark']:
            sender.reply("""
=====账号备注设置=====
🎯 请输入账号备注名
(批量提交时此备注将应用到所有账号)
------------------
回复备注名继续
回复"n"跳过备注
回复"q"退出操作
==================""")
            remark_input = get_user_input(timeout=120)
            if remark_input == 'q':
                sender.reply("✅ 已取消")
                return
            elif remark_input != 'n' and remark_input:
                remark = remark_input.strip()[:20]

        sender.reply("""
=====Keep 登录=====
当前模式: 🌐 提交至面板
------------------
👉 请直接发送账号抓包到的 Token，例如(Bearer开头或原生JWT)：
Bearer eyJ...
或
eyJ...

支持带备注提交格式:
备注#Token
------------------
⚠️ 绑定后无损覆盖旧数据，不会重复!
------------------
回复"q"退出操作
==================""")

        input_str = get_user_input(timeout=120)
        if not input_str or input_str.lower() == 'q':
            sender.reply("✅ 已取消")
            return

        token_lines = []
        raw_lines = [line.strip() for line in input_str.split('\n') if line.strip()]
        for line in raw_lines:
            token_lines.append(line.strip())

        if not token_lines:
            sender.reply("❌ 内容为空")
            return

        sender.reply(f"⏳ 正在处理 {len(token_lines)} 个账号，请稍候...")
        bind_stats = {"success": 0, "fail": 0, "new": 0, "update": 0, "migrate": 0}
        fail_msgs = []

        for line in token_lines:
            try:
                line_val = line.strip()
                line_remark = remark

                if '#' in line_val and not re.match(r'^\s*bearer\s+', line_val, flags=re.I):
                    parts = line_val.split('#', 1)
                    if len(parts[0]) <= 20: # 认为是备注
                        line_remark = parts[0].strip()
                        final_token_str = parts[1].strip()
                    else:
                        final_token_str = line_val
                else:
                    final_token_str = line_val

                final_token_str = normalize_keep_token(final_token_str)
                if len(final_token_str) < 30:
                    bind_stats["fail"] += 1
                    fail_msgs.append("Token格式错误/过短")
                    continue

                client = KeepClient(final_token_str)
                info_res = client.check_info()

                nick = info_res['nickname']
                final_token_str = info_res['final_token']
                acc_id = info_res['acc_key']
                aliases = info_res.get('aliases', [])
                acc_type = info_res.get('acc_type', '')
                legacy_key = info_res.get('legacy_key', '')

                bind_result = process_account_binding(final_token_str, acc_id, nick, line_remark, aliases, acc_type, legacy_key, silent=(len(token_lines) > 1))
                if bind_result.get("ok"):
                    bind_stats["success"] += 1
                    bind_stats[bind_result.get("action", "update")] += 1
                    if bind_result.get("migrated"):
                        bind_stats["migrate"] += 1
                else:
                    bind_stats["fail"] += 1
                    fail_msgs.append(bind_result.get("msg", "处理失败"))
            except Exception as ex:
                bind_stats["fail"] += 1
                fail_msgs.append(str(ex)[:30])
                if len(token_lines) == 1:
                    sender.reply(f"❌ 登录处理失败: {str(ex)}")

        if len(token_lines) > 1:
            fail_text = ""
            if fail_msgs:
                fail_text = "\n❌ 失败原因: " + "；".join(list(dict.fromkeys(fail_msgs))[:3])
            sender.reply(f"""=====Keep登录汇总=====
✅ 成功: {bind_stats['success']} 个
🆕 新增: {bind_stats['new']} 个
🔄 更新: {bind_stats['update']} 个
🔁 承接旧账号: {bind_stats['migrate']} 个
❌ 失败: {bind_stats['fail']} 个{fail_text}
==================""")

    except Exception as e:
        logger.error(f"绑定失败: {e}")
        sender.reply(f"❌ 绑定失败: {e}")

def process_account_binding(full_token, unique_id, nickname, remark="", aliases=None, acc_type="", legacy_key="", silent=False):
    try:
        account = str(unique_id)
        aliases = [str(x) for x in (aliases or []) if str(x) and str(x) != account]
        migrated_from = ""
        existing_accounts = AccountManager.get_accounts(userid)
        if account not in existing_accounts:
            old_account = AccountManager.find_migration_source(userid, account, aliases, acc_type, legacy_key)
            if old_account and AccountManager.migrate_account(userid, old_account, account, full_token, remark):
                migrated_from = old_account

        accountVip = '2099-12-31'
        today_time = str(datetime.now().date())

        is_authorized = False
        if accountVip and accountVip >= today_time:
            is_authorized = True
            auth_status = f'✅ 已授权 ({accountVip})'
            next_step = f'发送 {config["randommanagecommand"]} 可管理账号'
        else:
            auth_status = '⚠️ 未授权'

        if config['enable_remark'] and not remark:
            remark = RemarkManager.get_account_remark(userid, account)

        remark_info = f"\n📝 备注: {remark}" if remark else ""
        account_display = get_account_display(account, remark)

        is_new = AccountManager.add_account(userid, account)
        action = "new" if is_new else "update"
        if is_new:
            try: sg.bucketSet(bucket='keep_bind_date', key=account, value=str(datetime.now().date()))
            except: pass
        AccountManager.update_account_token(account, full_token)

        if config['enable_remark'] and remark:
            RemarkManager.set_account_remark(userid, account, remark)

        ql_msg = ""
        if is_authorized:
            if sys_api.sync_env(full_token, account, remark, accountVip):
                ql_msg = "\n🌐 状态: ✅ 系统已同步更新"
            else:
                ql_msg = "\n🌐 状态: ❌ 系统同步失败"
        else:
            ql_msg = "\n🌐 状态: ⏸️ 未授权暂不同步"

        migrate_msg = ""
        if migrated_from:
            old_safe = mask_account(migrated_from)
            migrate_msg = f"\n🔁 已承接旧账号: {old_safe}"

        if not silent:
            sender.reply(f"""
=====Keep账号更新=====
✅ 处理成功!
👤 用户: {nickname}
📱 账号: {account_display}{migrate_msg}{remark_info}
🔐 授权: {auth_status}{ql_msg}
⏰ 下一步操作:
   {next_step}
==================""")
        return {"ok": True, "account": account, "action": action, "migrated": bool(migrated_from)}

    except Exception as e:
        logger.error(f"入库异常: {e}")
        if not silent:
            sender.reply(f"❌ 入库异常: {e}")
        return {"ok": False, "msg": str(e)}

def xy_manage():
    accounts = [str(x) for x in AccountManager.get_accounts(userid)]
    if not accounts:
        sender.reply(f"❌ 未找到账号，请发送 {config['randomsigncommand']} 绑定")
        return
    sender.reply("=====账号管理=====\n" + "\n".join(
        f"[{i}] {account}" for i, account in enumerate(accounts, 1)
    ) + "\n[d] 删除多个账号\n[q] 退出\n==================")
    choice = get_user_input()
    if not choice or choice.lower() == "q":
        return
    if choice.lower() == "d":
        sender.reply("请输入账号序号，多个用逗号分隔：")
        selected, _ = parse_index_selection(get_user_input(), len(accounts), allow_all=False)
        if selected:
            batch_delete_selected([accounts[i - 1] for i in selected])
        return
    selected, _ = parse_index_selection(choice, len(accounts), allow_all=False)
    if len(selected) == 1:
        manage_single_account(accounts[selected[0] - 1], {})
    elif selected:
        manage_multiple_accounts([accounts[i - 1] for i in selected], {})
    else:
        sender.reply("❌ 序号无效")

def manage_multiple_accounts(selected_accs, account_remarks=None):
    sender.reply(f"确认删除选中的 {len(selected_accs)} 个账号请回复 y")
    if get_user_input().lower() == "y":
        batch_delete_selected(selected_accs)

def manage_single_account(account, account_remarks=None):
    token = AccountManager.get_token(account) or ""
    sender.reply(f"=====账号操作=====\n📱 {account}\n[1] 修改备注\n[2] 查看配置\n[3] 删除账号\n==================")
    choice = get_user_input()
    if choice == "1" and config.get("enable_remark"):
        sender.reply("请输入新备注：")
        remark = get_user_input()
        if remark and remark.lower() != "q":
            RemarkManager.set_account_remark(userid, account, remark)
            if token:
                sys_api.sync_env(token, account, remark, "2099-12-31")
            sender.reply("✅ 备注已更新")
    elif choice == "2":
        sender.reply(token or "❌ 未保存配置")
    elif choice == "3":
        sender.reply("确认删除请回复 y")
        if get_user_input().lower() == "y":
            AccountManager.remove_account(userid, account)
            if config.get("enable_remark"):
                RemarkManager.delete_account_remark(userid, account)
            sys_api.delete_env(account)
            sender.reply("✅ 删除成功")

def batch_delete_selected(accounts):
    preview = []
    account_remarks = RemarkManager.get_all_remarks(userid) if config['enable_remark'] else {}
    for account in accounts[:5]:
        account = str(account)
        preview.append(get_account_display(account, account_remarks.get(account, "")))
    more = f"\n...等 {len(accounts)} 个账号" if len(accounts) > 5 else ""
    sender.reply(f"=====确认批量删除=====\n已选择 {len(accounts)} 个账号\n{chr(10).join(preview)}{more}\n------------------\n确认删除请回复【确认删除】\n回复 q 取消\n==================")
    if get_user_input() == "确认删除":
        today_date = datetime.now().date()
        for account in accounts:
            try:
                 account = str(account)
                 AccountManager.remove_account(userid, account)
                 token = AccountManager.get_token(account)
                 try: sg.bucketDel(bucket='keep_token', key=account)
                 except: pass
                 try:
                     pass
                 except: pass
                 if config['enable_remark']: RemarkManager.delete_account_remark(userid, account)
                 sys_api.delete_env(account, token)
                 for d in range(config['reminder_days'] + 1):
                     remind_key = f"{userid}_{account}_{today_date - timedelta(days=d)}"
                     try: sg.bucketDel('keep_remind_log', remind_key)
                     except: pass
            except: pass
        sender.reply("✅ 批量删除完成")

def clean_expired_accounts(force_report=False):
    panel_sync = sync_local_auth_from_panel()
    users = sg.bucketAllKeys(bucket='keep_user')
    if not users:
        if sender.isAdmin() and (force_report or usermessage in ['Keep清理', '清理Keep']):
            sender.reply("=====执行结果=====\n📭 暂无用户数据")
        return {
            "report_date": str(datetime.now().date()),
            "scanned_users": 0,
            "scanned_accounts": 0,
            "sent_notifications": 0,
            "cleaned_count": 0,
            "reminded_count": 0,
            "ck_expired_count": 0,
        }

    if sender.isAdmin() and (force_report or usermessage in ['Keep清理', '清理Keep']):
        sender.reply(f"=====开始执行维护=====\n📊 扫描用户数: {len(users)}\n🔄 面板回写: {panel_sync['synced']}个账号\n⚙️ 提醒天数: {config['reminder_days']}天\n⏳ 处理中...")

    scanned_accounts = 0
    cleaned_count = 0
    reminded_count = 0
    ck_expired_count = 0
    today_date = datetime.now().date()
    reminder_days_cfg = config['reminder_days']
    user_contexts = []
    ck_verify_tasks = []

    for user in users:
        try:
            accounts = AccountManager.get_accounts(user)
            if not accounts: continue

            account_contexts = []

            for account in accounts:
                account = str(account)
                scanned_accounts += 1
                accountVip = '2099-12-31'

                if not accountVip:
                    account_contexts.append({
                        "account": account,
                        "accountVip": accountVip,
                        "days_diff": None,
                        "expiration_str": "",
                        "full_token": "",
                    })
                    continue
                else:
                    try:
                        expiration_date = datetime.strptime(accountVip, "%Y-%m-%d").date()
                        expiration_str = accountVip
                    except:
                        logger.warning(f"VIP日期解析失败，保留账号: user={user} account={account} vip={accountVip}")
                        expiration_date = today_date + timedelta(days=3650)
                        expiration_str = f"{accountVip}(格式异常)"

                days_diff = (expiration_date - today_date).days
                full_token = AccountManager.get_token(account) or ""

                account_contexts.append({
                    "account": account,
                    "accountVip": accountVip,
                    "days_diff": days_diff,
                    "expiration_str": expiration_str,
                    "full_token": full_token,
                })

                if days_diff >= 0 and full_token:
                    ck_verify_tasks.append((str(user), account, full_token))

            user_contexts.append({
                "user": str(user),
                "accounts": account_contexts,
            })

        except Exception:
            continue

    ck_verify_result = batch_verify_account_ck(ck_verify_tasks)

    for context in user_contexts:
        try:
            user = context["user"]
            valid_accounts = []
            user_has_change = False
            account_remarks = RemarkManager.get_all_remarks(user) if config['enable_remark'] else {}

            for account_item in context["accounts"]:
                account = account_item["account"]
                accountVip = account_item["accountVip"]
                days_diff = account_item["days_diff"]
                expiration_str = account_item["expiration_str"]

                if not accountVip:
                    valid_accounts.append(account)
                    continue

                if days_diff >= 0:
                    valid_accounts.append(account)

                    full_token = account_item["full_token"]
                    is_ck_valid = ck_verify_result.get((str(user), str(account)), True) if full_token else True

                    if not is_ck_valid:
                        ck_remind_key = f"ck_die_{user}_{account}_{today_date}"
                        has_ck_reminded = sg.bucketGet('keep_remind_log', ck_remind_key)

                        if not has_ck_reminded:
                            account_display = get_account_display(account, account_remarks.get(account, ""))
                            msg = f"""=====⚠️ 配置失效提醒=====
您的Keep配置可能已失效！
📱 账号: {account_display}
📅 授权到期: {expiration_str}
------------------
系统检测到该账号无法正常登录或获取数据。
为保证挂机收益，请重新抓取最新 Token 并发送【{config['randomsigncommand']}】更新！
=================="""
                            if safe_send_message(user, msg, f"配置失效提醒 {user}-{account}"):
                                try: sg.bucketSet('keep_remind_log', ck_remind_key, "1")
                                except: pass
                                ck_expired_count += 1

                    if is_ck_valid and 0 <= days_diff <= reminder_days_cfg:
                        remind_key = f"{user}_{account}_{today_date}"
                        has_reminded = sg.bucketGet('keep_remind_log', remind_key)

                        if not has_reminded:
                            account_display = get_account_display(account, account_remarks.get(account, ""))
                            msg = f"""=====⏰ 到期提醒=====
您的Keep账号授权即将到期！
📱 账号: {account_display}
📅 到期: {expiration_str} (剩余 {days_diff} 天)
------------------
为避免影响挂机，请及时续费。
发送 {config['randommanagecommand']} 进行续费
=================="""
                            if safe_send_message(user, msg, f"到期提醒 {user}-{account}"):
                                try: sg.bucketSet('keep_remind_log', remind_key, "1")
                                except: pass
                                reminded_count += 1
                    continue

                if days_diff < 0:
                    try:
                        sys_api.delete_env(account, account_item.get("full_token"))
                        try: sg.bucketDel(bucket='keep_token', key=account)
                        except: pass
                        try:
                            pass
                        except: pass
                        if config['enable_remark']:
                            RemarkManager.delete_account_remark(user, account)
                    except: pass

                    account_display = get_account_display(account, account_remarks.get(account, ""))
                    clean_msg = f"""=====🗑️ 过期清理通知=====
您的Keep账号授权已过期并清理。
📱 账号: {account_display}
📅 到期: {expiration_str}
------------------
相关配置已失效移除。
如需继续使用，请重新登录并授权。
=================="""
                    safe_send_message(user, clean_msg, f"过期清理通知 {user}-{account}")
                    cleaned_count += 1
                    user_has_change = True

            if user_has_change:
                if valid_accounts:
                    try: sg.bucketSet(bucket='keep_user', key=str(user), value=str(valid_accounts))
                    except: pass
                else:
                    try: sg.bucketDel(bucket='keep_user', key=str(user))
                    except: pass

        except Exception:
            continue

    if sender.isAdmin() and (force_report or usermessage in ['Keep清理', '清理Keep']):
        sender.reply(
            f"=====Keep维护完成=====\n"
            f"✅ 检测完成，共 {scanned_accounts} 个账号\n"
            f"📢 授权提醒: {reminded_count} 个\n"
            f"⚠️ CK失效通知: {ck_expired_count} 个\n"
            f"🗑️ 清理过期: {cleaned_count} 个\n"
            f"=================="
        )

    return {
        "report_date": str(today_date),
        "scanned_users": len(users),
        "scanned_accounts": scanned_accounts,
        "sent_notifications": reminded_count + ck_expired_count + cleaned_count,
        "cleaned_count": cleaned_count,
        "reminded_count": reminded_count,
        "ck_expired_count": ck_expired_count,
    }

def show_tutorial():
    panel_name = '青龙' if config['panel_type'] == 'qinglong' else '呆呆'
    sender.reply(f"""
=====Keep管理插件教程=====
当前模式: 🌐 提交至{panel_name}面板

1️⃣ {config['randomsigncommand']}
   发送Keep配置(Token)自动覆盖更新。
   支持格式：`eyJxxxx` 或 带备注 `我的号#eyJxxxx`。

2️⃣ {config['randomquerycommand']}
   查询账号存活状态与当前资产进度(余额、签到、抽奖)。

3️⃣ {config['randommanagecommand']}
   全新极简扫码无需挂机，付完全自动回调开通。

4️⃣ Keep授权

5️⃣ Keep清理 / Keep广播
   自动清理失效和未授权数据，或向授权用户广播。
==================""")

try:
    command = usermessage.strip()
    command_lower = command.lower()

    if is_cron_trigger():
        try:
            report_data = clean_expired_accounts()
        except Exception:
            logger.error(f"定时维护清理异常: {traceback.format_exc()}")
            report_data = {
                "report_date": str(datetime.now().date()),
                "scanned_users": 0, "scanned_accounts": 0,
                "sent_notifications": 0, "cleaned_count": 0,
                "reminded_count": 0, "ck_expired_count": 0,
            }
        send_daily_admin_report(report_data)

    elif re.match(r'^[Kk]eep(通知|广播)\s*', command):
        notify_authorized_users()
    elif command_lower in ['keep登录', 'keep登陆', '登录keep', '登陆keep']:
        bindaccount()
    elif command_lower in ['keep管理', '管理keep']:
       xy_manage()
    elif command_lower in ['keep查询', '查询keep']:
        cxs()
    elif command_lower in ['keep清理', '清理keep']:
        try:
            report_data = clean_expired_accounts()
        except Exception:
            logger.error(f"手动维护清理异常: {traceback.format_exc()}")
            report_data = {
                "report_date": str(datetime.now().date()),
                "scanned_users": 0, "scanned_accounts": 0,
                "sent_notifications": 0, "cleaned_count": 0,
                "reminded_count": 0, "ck_expired_count": 0,
            }
        send_daily_admin_report(report_data, force_send=True, notify_status=True)
    elif command_lower == 'keep教程':
        show_tutorial()

except Exception as e:
    logger.error(f"Error: {e}")
    sender.reply(f"❌ 系统错误: {e}")
