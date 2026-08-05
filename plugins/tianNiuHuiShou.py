# [title: 天牛回收]
# [name: tianNiuHuiShou]
# [language: python]
# [class: 任务]
# [author: 8165799]
# [version: v1.1]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(天牛)(登录|登陆)$|^登(录|陆)(天牛)$|^(天牛)(查询|管理)$|^(查询|管理)(天牛)$|^天牛清理$|^天牛$|^天牛教程$|^天牛通知 ?(.*)$|^清理天牛$|^天牛广播 ?(.*)$]
# [cron: 5 10 * * *]
# [icon: https://api.iconify.design/lucide:bot.svg]
# [description: 天牛代挂提交；2. 用户提交 token 自动识别手机号；4.]
# [depe: ["requests"]]
# [staticmethod: def find_migration_source(user_id, new_account, aliases=None, acc_type="", legacy_key=""):]


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
    'tian_niu_panel_type': form.string().title('对接面板类型').default('').description('qinglong=青龙面板 daidai=呆呆面板'),
    'tian_niu_tian_niu_qlname': form.string().title('对接系统配置').default('').description('青龙:URL丨ID丨Secret 呆呆:URL丨Key丨Secret'),
    'tian_niu_tian_niu_osname': form.string().title('系统变量名').default('').description('系统容器内变量名(默认为tnhs)'),
    'tian_niu_enable_proxy': form.boolean().title('启用代理').default(False).description('是否启用代理功能'),
    'tian_niu_proxy_pool_url': form.string().title('代理池地址').default('').description('代理API服务地址'),
    'tian_niu_enable_remark': form.boolean().title('启用备注功能').default(False).description('是否启用账号备注功能'),
})
_CONFIG_FIELD_MAP = {
    ('tian_niu', 'panel_type'): 'tian_niu_panel_type',
    ('tian_niu', 'tian_niu_qlname'): 'tian_niu_tian_niu_qlname',
    ('tian_niu', 'tian_niu_osname'): 'tian_niu_tian_niu_osname',
    ('tian_niu', 'enable_proxy'): 'tian_niu_enable_proxy',
    ('tian_niu', 'proxy_pool_url'): 'tian_niu_proxy_pool_url',
    ('tian_niu', 'enable_remark'): 'tian_niu_enable_remark',
}

import re
import ast
from datetime import datetime, timedelta
import urllib.parse
from decimal import Decimal
import requests
import time
import hashlib
import logging
import base64
import warnings
import random
import traceback
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

warnings.filterwarnings('ignore', message='Unverified HTTPS request')
requests.packages.urllib3.disable_warnings()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('tian_niu_plugin')

REQUEST_TIMEOUT = 30
MAINTENANCE_CK_MAX_WORKERS = 8

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = str(sender.getUserID())
usermessage = sender.getMessage()

try:
    sg.bucketSet(bucket='tian_niu_sender', key=userid, value=str(senderID))
    sg.bucketSet(bucket='tian_niu_imtype', key=userid, value=str(sender.getImtype()))
except:
    pass


def getusercontent():
    """获取插件完整配置"""
    panel_type = sg.bucketGet('tian_niu', 'panel_type') or 'qinglong'
    panel_type = panel_type.lower()

    env_qlconfig = sg.bucketGet('tian_niu', 'tian_niu_qlname') or ''
    env_name = sg.bucketGet('tian_niu', 'tian_niu_osname') or 'tnhs'

    if not env_qlconfig:
        sender.reply("❌ 配置错误：请在插件配置中填写【对接系统配置】(面板信息)。")
        exit(0)

    tian_niu_managecommand = sg.bucketGet('tian_niu', 'tian_niu_managecommand') or '天牛管理'
    tian_niu_querycommand = sg.bucketGet('tian_niu', 'tian_niu_querycommand') or '天牛查询'
    tian_niu_signcommand = sg.bucketGet('tian_niu', 'tian_niu_signcommand') or '天牛登录'

    enable_proxy = (sg.bucketGet('tian_niu', 'enable_proxy') or 'false').lower() == 'true'
    proxy_pool_url = sg.bucketGet('tian_niu', 'proxy_pool_url') or ''
    points_bucket = sg.bucketGet('tian_niu', 'points_bucket') or 'dd_sign_points'
    enable_remark = (sg.bucketGet('tian_niu', 'enable_remark') or 'false').lower() == 'true'

    randommanagecommand = tian_niu_managecommand
    randomquerycommand = tian_niu_querycommand
    randomsigncommand = tian_niu_signcommand

    zsVipmoney = Decimal(sg.bucketGet('tian_niu', 'zsVipmoney') or '0')
    zscoin = int(sg.bucketGet('tian_niu', 'zscoin') or '0')
    reminder_days = int(sg.bucketGet('tian_niu', 'reminder_days') or '2')

    enable_zsm = (sg.bucketGet('tian_niu', 'enable_zsm') or 'false').lower() == 'true'
    zsm = sg.bucketGet('tian_niu', 'zsm') or ''

    epay_url = '2099-12-31' or ''
    epay_pid = '2099-12-31' or ''
    epay_key = '2099-12-31' or ''
    epay_alipay = ('2099-12-31' or 'true').lower() == 'true'
    epay_wxpay = ('2099-12-31' or 'false').lower() == 'true'
    epay_qqpay = ('2099-12-31' or 'false').lower() == 'true'

    return {
        'panel_type': panel_type,
        'env_name': env_name,
        'env_qlconfig': env_qlconfig,
        'tian_niu_managecommand': tian_niu_managecommand,
        'tian_niu_querycommand': tian_niu_querycommand,
        'tian_niu_signcommand': tian_niu_signcommand,
        'randommanagecommand': randommanagecommand,
        'randomquerycommand': randomquerycommand,
        'randomsigncommand': randomsigncommand,
        'enable_zsm': enable_zsm,
        'zsm': zsm,
        'enable_proxy': enable_proxy,
        'proxy_pool_url': proxy_pool_url,
        'points_bucket': points_bucket,
        'enable_remark': enable_remark,
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

def get_owner_user_id(account, fallback_userid=None):
    account = str(account or "")
    try:
        if fallback_userid and account in [str(x) for x in AccountManager.get_accounts(str(fallback_userid))]:
            return str(fallback_userid)
    except:
        pass
    try:
        for frame_info in __import__('inspect').stack()[1:6]:
            local_vars = frame_info.frame.f_locals
            for key in ['owner_user_id', 'target_userid', 'target_qq', 'target_user', 'user', 'uid']:
                candidate = local_vars.get(key)
                if not candidate:
                    continue
                candidate = str(candidate)
                try:
                    if account in [str(x) for x in AccountManager.get_accounts(candidate)]:
                        return candidate
                except:
                    pass
    except:
        pass
    try:
        for owner in sg.bucketAllKeys(bucket='tian_niu_user'):
            try:
                if account in [str(x) for x in AccountManager.get_accounts(owner)]:
                    return str(owner)
            except:
                pass
    except:
        pass
    try:
        if not sender.isAdmin() and str(userid):
            return str(userid)
    except:
        pass
    return ""

def send_message_to_framework_admins(msg):
    """
    优先走傻妞框架原生管理员推送。
    某些框架支持 notifyMasters(msg) 自动发给管理员。
    """
    notify_func = getattr(sg, 'notifyMasters', None)
    if not callable(notify_func):
        return False

    tried = [
        ("auto_none", None),
        ("auto_empty_list", []),
    ]

    for mode, arg in tried:
        try:
            if arg is None:
                notify_func(msg)
            else:
                notify_func(msg, arg)
            logger.info(f"框架管理员推送成功 mode={mode}")
            return True
        except TypeError:
            try:
                notify_func(msg)
                logger.info(f"框架管理员推送成功 mode={mode}->msg_only")
                return True
            except Exception as e:
                logger.warning(f"框架管理员推送失败 mode={mode}->msg_only: {e}")
        except Exception as e:
            logger.warning(f"框架管理员推送失败 mode={mode}: {e}")
    return False

def send_daily_admin_report(report_data, force_send=False, notify_status=False):
    report_date = str(report_data.get('report_date') or datetime.now().date())
    report_key = f"daily_admin_report_{report_date}"
    if not force_send and sg.bucketGet('tian_niu_runtime', report_key):
        if notify_status:
            sender.reply("ℹ️ 今日管理员汇总已发送过，如需重发请明天自动发送或再次手动清理。")
        return False

    msg = (
        "=====天牛维护完成=====\n"
        f"✅ 检测完成，共 {report_data.get('scanned_accounts', 0)} 个账号\n"
        f"📣 发送通知: {report_data.get('sent_notifications', 0)} 条\n"
        f"⚠️ CK失效通知: {report_data.get('ck_expired_count', 0)} 个\n"
        f"🗑️ 清理过期: {report_data.get('cleaned_count', 0)} 个\n"
        "=================="
    )

    framework_sent = send_message_to_framework_admins(msg)
    if framework_sent:
        try:
            sg.bucketSet('tian_niu_runtime', report_key, "framework")
        except Exception:
            pass
        if notify_status:
            sender.reply("✅ 管理员汇总已发送（框架自动管理员）")
        return True

    logger.info("框架管理员自动推送失败")
    if notify_status:
        sender.reply("❌ 管理员汇总发送失败：框架自动管理员推送未成功，请检查傻妞默认管理员配置。")
    return False

def batch_verify_account_ck(tasks, max_workers=MAINTENANCE_CK_MAX_WORKERS):
    return {}

def send_user_notice(user_id, msg, title="天牛通知"):
    try:
        imtype = sg.bucketGet(bucket='tian_niu_imtype', key=str(user_id)) or sender.getImtype()
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
        saved_sender = sg.bucketGet(bucket='tian_niu_sender', key=str(user_id))
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
    ok, err = send_user_notice(user_id, msg, "天牛提醒")
    if not ok:
        logger.warning(f"消息发送失败 {log_context}: {err}")
    return ok

def parse_panel_tian_niu_remark(remarks):
    try:
        remarks = str(remarks or '')
        user_match = re.search(r'用户[:：]\s*([^丨|\s]+)', remarks)
        id_match = re.search(r'ID[:：]\s*([^丨|\s]+)', remarks)
        date_match = re.search(r'到期[:：]\s*(\d{4}-\d{2}-\d{2})', remarks)
        if not user_match or not id_match or not date_match:
            return None
        return {
            'user': user_match.group(1).strip(),
            'account': id_match.group(1).strip(),
            'auth_date': date_match.group(1).strip()
        }
    except:
        return None

def normalize_panel_token_value(value, account_id=""):
    parts = [p.strip() for p in str(value or '').split('#') if p.strip()]
    account_id = str(account_id or '').strip()
    if len(parts) >= 4:
        return '#'.join(parts[-3:])
    if len(parts) == 3:
        if account_id and parts[1] == account_id:
            return '#'.join(parts[1:])
        return '#'.join(parts)
    if len(parts) == 2:
        return '#'.join(parts)
    return str(value or '').strip()

def sync_local_auth_from_panel():
    return True

def mask_account(account):
    account = str(account)
    return account[:3] + "****" + account[-3:] if len(account) > 6 else account

def mask_mobile(mobile):
    mobile = str(mobile or "").strip()
    return mobile[:3] + "****" + mobile[-4:] if len(mobile) >= 11 else mask_account(mobile)

def get_account_display(account, remark=""):
    remark = str(remark or "").strip()
    account = str(account or "").strip()
    try:
        mobile = AccountManager.get_account_mobile(account)
        if mobile:
            mobile_display = mask_mobile(mobile)
            return f"{mobile_display}({remark})" if remark else mobile_display
    except:
        pass
    if looks_like_mobile(account):
        mobile_display = mask_mobile(account)
        return f"{mobile_display}({remark})" if remark else mobile_display
    return remark if remark else mask_account(account)

def deep_get_any(data, keys):
    if not isinstance(data, dict):
        return ""
    for key in keys:
        value = data.get(key)
        if value not in [None, ""]:
            return value
    for value in data.values():
        if isinstance(value, str) and value.strip().startswith("{"):
            try:
                value = json.loads(value)
            except:
                pass
        if isinstance(value, dict):
            found = deep_get_any(value, keys)
            if found not in [None, ""]:
                return found
    return ""

def get_points_bucket_candidates():
    buckets = []
    configured_bucket = str(config.get('points_bucket') or '').strip()
    if configured_bucket and configured_bucket != 'dd_sign_points':
        buckets.append(configured_bucket)
    for bucket in ['dd_sign_points', configured_bucket]:
        bucket = str(bucket or '').strip()
        if bucket and bucket not in buckets:
            buckets.append(bucket)
    return buckets

def get_user_points():
    return 0

def set_user_points(points, bucket=None):
    target_bucket = bucket or (get_points_bucket_candidates()[0] if get_points_bucket_candidates() else str(config.get('points_bucket') or 'dd_sign_points'))
    sg.bucketSet(target_bucket, userid, str(points))

def is_cron_trigger():
    imtype = ""
    try:
        imtype = str(sender.getImtype() or "").lower()
    except:
        pass
    msg = str(usermessage or "").strip().lower()
    return imtype == "cron" or msg in ["", "cron", "定时任务"] or (imtype == "fake" and not msg)

def empower(empowertime, days):
    try:
        today_date = datetime.now().date()
        if not empowertime or empowertime <= str(today_date):
            delayed_date = today_date + timedelta(days=days)
        elif empowertime > str(today_date):
            empower_date = datetime.strptime(empowertime, "%Y-%m-%d").date()
            delayed_date = empower_date + timedelta(days=days)
        if days < 0 and delayed_date < today_date:
            delayed_date = today_date
        return str(delayed_date)
    except Exception as e:
        logger.error(f"授权时间计算失败: {e}")
        raise Exception(f"授权时间计算失败: {e}")

def _build_epay_sign(params_dict, key, exclude_keys=('sign', 'sign_type')):
    return True

def _create_epay_qr(out_trade_no, channel, project_name, money_str):
    return True

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

class ZsptvClient:
    BASE_URL = "https://tianniunew.fzjingzhou.com"

    def __init__(self, token_str):
        self.token = self.normalize_token(token_str)
        self.mobile = ""
        self.nickname = ""
        self.uid = self.legacy_key()
        self.uid_type = "token_md5"
        self.aliases = []
        self.web_token = ""
        self.score = "0"
        self.exchange = "0.00"
        self.sign_in_num = 0

    @staticmethod
    def normalize_token(raw):
        raw = str(raw or "").strip().strip('"').strip("'")
        if not raw:
            return ""
        if "#" in raw and "token=" not in raw:
            raw = [p.strip() for p in raw.split("#") if p.strip()][-1]
        if "token=" in raw:
            parsed = urllib.parse.urlparse(raw)
            query = parsed.query or raw
            token = urllib.parse.parse_qs(query).get("token", [""])[0]
            if token:
                return token.strip()
        return raw.replace("\r", "").replace("\n", "").strip()

    def build_headers(self):
        return {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Content-Type": "application/x-www-form-urlencoded",
            "Platform": "MP-WEIXIN",
            "Referer": "https://servicewechat.com/wx887c2f947bffa76e/6/page-frame.html",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0x2541a1e) XWEB/19957",
            "Xweb_xhr": "1",
        }

    def _get_proxy(self):
        if not config.get('enable_proxy') or not config.get('proxy_pool_url'):
            return None
        try:
            res = requests.get(config['proxy_pool_url'], timeout=8, verify=False)
            match = re.search(r'(?:https?://)?\d+\.\d+\.\d+\.\d+:\d+', res.text.strip())
            if match:
                proxy = match.group(0)
                return proxy if proxy.startswith(('http://', 'https://')) else f"http://{proxy}"
        except Exception as e:
            logger.warning(f"天牛查询获取代理失败: {e}")
        return None

    def _post_api(self, path, data=None, timeout=20, max_retries=3):
        if not self.token:
            raise RuntimeError("token为空")
        last_exc = None
        for attempt in range(1, max_retries + 1):
            try:
                proxy = self._get_proxy()
                proxies = {'http': proxy, 'https': proxy} if proxy else None
                res = requests.post(
                    f"{self.BASE_URL}{path}",
                    headers=self.build_headers(),
                    data=data or {},
                    proxies=proxies,
                    timeout=timeout,
                )
                return res.json()
            except Exception as e:
                last_exc = e
                if attempt < max_retries:
                    time.sleep(1)
                    continue
                raise RuntimeError(str(e))
        raise RuntimeError(str(last_exc) if last_exc else "请求失败")

    def legacy_key(self):
        token = self.token if hasattr(self, "token") else ""
        return hashlib.md5(str(token).encode()).hexdigest()[:8]

    def refresh_profile(self):
        resp = self._post_api("/api/Person/index", {"token": self.token})
        if resp.get("code") != 1000 or not isinstance(resp.get("data"), dict):
            raise RuntimeError(resp.get("msg") or f"接口返回异常: {resp}")
        data = resp.get("data") or {}
        self.mobile = str(data.get("mobile") or "").strip()
        self.nickname = str(data.get("nickname") or "").strip()
        self.score = str(data.get("score", "0"))
        self.exchange = str(data.get("exchange", data.get("money", "0.00")))
        self.sign_in_num = data.get("sign_in_num", 0)
        if self.mobile:
            self.uid = self.mobile
            self.uid_type = "mobile"
        return data

    def get_info(self):
        """返回: (网络是否成功, token是否有效, 当前积分, 提示信息)"""
        try:
            self.refresh_profile()
            if not self.mobile:
                return True, False, self.score, "未识别到手机号，请先到天牛旧衣小程序授权手机号后再提交"
            msg = (
                f"🪙 当前积分: {self.score}\n"
                f"💰 当前金额: {self.exchange}元\n"
                f"📅 签到次数: {self.sign_in_num}"
            )
            return True, True, self.score, msg
        except Exception as e:
            return False, True, 0, str(e)

    def get_wallet_info(self, web_token=None):
        return None

    def verify_ck(self):
        net_ok, is_valid, _, _ = self.get_info()
        if net_ok and not is_valid:
            return False
        return True

    def check_info(self):
        net_ok, is_valid, _, msg = self.get_info()
        if net_ok and not is_valid:
            raise RuntimeError(msg)
        if not net_ok:
            raise RuntimeError(f"网络查询异常: {msg}")
        if not self.mobile:
            raise RuntimeError("未识别到手机号，请先到天牛旧衣小程序授权手机号后再提交")
        display_id = mask_mobile(self.mobile)
        return {
            "nickname": self.nickname or f"天牛_{display_id}",
            "phone": self.mobile,
            "acc_key": self.mobile,
            "acc_type": "mobile",
            "aliases": [self.legacy_key()],
            "legacy_key": self.legacy_key(),
            "final_token": self.token,
            "mobile": self.mobile,
            "score": self.score,
            "exchange": self.exchange,
        }

class RemarkManager:
    @staticmethod
    def get_account_remark(user_id, account_id):
        try:
            remark_data = sg.bucketGet(bucket='tian_niu_remarks', key=f'{user_id}_{account_id}')
            return str(remark_data) if remark_data else ""
        except: return ""

    @staticmethod
    def set_account_remark(user_id, account_id, remark):
        try:
            remark_clean = str(remark).strip()[:20]
            if remark_clean:
                sg.bucketSet(bucket='tian_niu_remarks', key=f'{user_id}_{account_id}', value=remark_clean)
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
            sg.bucketDel(bucket='tian_niu_remarks', key=f'{user_id}_{account_id}')
            return True
        except: return False

class AccountManager:
    @staticmethod
    def get_accounts(user_id):
        try:
            value = sg.bucketGet(bucket='tian_niu_user', key=str(user_id))
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
                sg.bucketSet(bucket='tian_niu_user', key=str(user_id), value=str(accounts))
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
                    sg.bucketSet(bucket='tian_niu_user', key=str(user_id), value=str(accounts))
                else:
                    sg.bucketDel(bucket='tian_niu_user', key=str(user_id))
                return True
            return False
        except: return False

    @staticmethod
    def update_account_token(account, token):
        try:
            encrypted_token = encrypt_token(str(token))
            sg.bucketSet(bucket='tian_niu_token', key=str(account), value=encrypted_token)
            return True
        except: return False

    @staticmethod
    def update_account_mobile(account, mobile):
        try:
            mobile = str(mobile or "").strip()
            if mobile:
                sg.bucketSet(bucket='tian_niu_mobile', key=str(account), value=mobile)
                return True
            return False
        except: return False

    @staticmethod
    def get_account_mobile(account):
        try:
            return sg.bucketGet(bucket='tian_niu_mobile', key=str(account)) or ""
        except: return ""

    @staticmethod
    def update_account_web_token(account, web_token):
        try:
            web_token = str(web_token or "").strip()
            if web_token:
                sg.bucketSet(bucket='tian_niu_web_token', key=str(account), value=encrypt_token(web_token))
                return True
            return False
        except: return False

    @staticmethod
    def get_account_web_token(account):
        try:
            enc = sg.bucketGet(bucket='tian_niu_web_token', key=str(account))
            return decrypt_token(enc) if enc else ""
        except: return ""

    @staticmethod
    def get_token(account):
        try:
            enc = sg.bucketGet(bucket='tian_niu_token', key=str(account))
            return decrypt_token(enc) if enc else None
        except: return None

    @staticmethod
    def get_all_users():
        try:
            users = sg.bucketAllKeys(bucket='tian_niu_user')
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

            old_bind_date = sg.bucketGet(bucket='tian_niu_bind_date', key=old_account)
            if old_bind_date and not sg.bucketGet(bucket='tian_niu_bind_date', key=new_account):
                sg.bucketSet(bucket='tian_niu_bind_date', key=new_account, value=old_bind_date)

            old_mobile = AccountManager.get_account_mobile(old_account)
            if old_mobile and not AccountManager.get_account_mobile(new_account):
                AccountManager.update_account_mobile(new_account, old_mobile)

            old_web_token = AccountManager.get_account_web_token(old_account)
            if old_web_token and not AccountManager.get_account_web_token(new_account):
                AccountManager.update_account_web_token(new_account, old_web_token)

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
            sg.bucketSet(bucket='tian_niu_user', key=str(user_id), value=str(new_accounts))

            AccountManager.update_account_token(new_account, new_token)
            try: sg.bucketDel(bucket='tian_niu_token', key=old_account)
            except: pass
            try: sg.bucketDel(bucket='tian_niu_mobile', key=old_account)
            except: pass
            try: sg.bucketDel(bucket='tian_niu_web_token', key=old_account)
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
            if acc_type != "token_md5":
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

                old_client = ZsptvClient(old_token)
                old_info = old_client.check_info()
                old_ids = set(old_info.get('aliases', []))
                if old_info.get('acc_type') != "token_md5":
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
        except Exception as e: raise

    def _get_daidai_token(self):
        try:
            url = f"{self.QLurl}/api/open-api/token"
            data = {"app_key": self.ClientID, "app_secret": self.ClientSecret}
            response = requests.post(url, json=data, timeout=10, verify=False)
            if response.status_code == 200:
                return response.json()['data']['access_token']
            raise Exception("获取呆呆Token失败")
        except Exception as e: raise

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

    def sync_env(self, token, phone, remark="", auth_time="", owner_user_id=None):
        if not self.enabled: return False
        phone = str(phone)
        try:
            env_id = self.find_env(phone, token)

            ql_value = f"{token}"

            safe_phone = mask_mobile(phone)
            remarks_parts = [f'天牛:{safe_phone}']
            if auth_time: remarks_parts.append(f'到期:{auth_time}')
            else: remarks_parts.append('到期:未授权')
            if remark: remarks_parts.append(f'备注:{remark}')

            owner_user = get_owner_user_id(phone, owner_user_id)
            if not owner_user:
                raise Exception("无法确认账号真实归属，已阻止写入面板备注，避免青龙数据错乱")
            remarks_parts.extend([f'用户:{owner_user}', f'ID:{phone}', '天牛提交'])
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

        if full_token and len(full_token) >= 10:
            try:
                client = ZsptvClient(full_token)
                client.check_info()
                mobile = client.mobile or AccountManager.get_account_mobile(account)
                if mobile:
                    AccountManager.update_account_mobile(account, mobile)

                net_ok, is_valid, money, msg = client.get_info()
                if net_ok and not is_valid:
                    status_text = f"⚠️ 账号登录失败: {msg}"
                elif not net_ok:
                    status_text = f"⚠️ 网络查询异常: {str(msg)[:50]}"
                else:
                    status_text = msg

                account_info = f"""
=====天牛详情=====
🚀 平台: 天牛旧衣
📝 备注: {remark if remark else "无"}
📱 手机号: {mask_mobile(mobile) if mobile else "无"}
{status_text}
⏰ 授权到期: {auth_time}"""
                return account_info.strip()
            except Exception as e:
                return f"""
=====天牛查询异常=====
📱 账号: {account_display}
❌ 错误: {str(e)[:50]}
=================="""
        else:
            return f"""
=====天牛状态=====
📱 账号: {account_display}
📝 备注: {remark if remark else "无"}
🔐 授权: {'⚠️ 未授权' if not accountVip else ('❌ 已过期' if accountVip < today_time else f'✅ {accountVip}')}
⏰ 到期: {auth_time}
=================="""
    except Exception as e:
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

        menu = "=====天牛查询====="
        for i, acc in enumerate(accounts, 1):
            acc = str(acc)
            remark = account_remarks.get(acc, "") if config['enable_remark'] else ""
            mask_account(acc)
            account_display = get_account_display(acc, remark)
            vip = '2099-12-31'
            if not vip:
                vip_tag = '⚠️未授权'
            elif vip < today_time:
                vip_tag = '❌已过期'
            else:
                vip_tag = f'✅{vip}'
            menu += f"\n[{i}] {account_display} {vip_tag}"
        menu += f"\n------------------\n[a] 查询全部\n支持单选/多选/区间，如 1,2 或 3-6\n回复q退出\n=================="
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

def pick_accounts_by_indexes(accounts, indexes):
    return [str(accounts[i - 1]) for i in indexes if 1 <= i <= len(accounts)]

def selection_tip(action="选择"):
    return f"回复 a 全选\n支持单选/多选/区间，如 1,2 或 3-6 或 1,3-8,10\n回复 q 退出"

def looks_like_mobile(value):
    return bool(re.fullmatch(r'1\d{10}', str(value or '').strip()))

def parse_bind_input_line(line, default_remark="", submit_mode="password"):
    raw = str(line or '').strip()
    if not raw:
        raise ValueError("内容为空")

    if "#" in raw and "token=" not in raw:
        parts = [p.strip() for p in raw.split('#') if p.strip()]
        if len(parts) >= 2:
            return ZsptvClient(parts[-1]), parts[0] or default_remark

    return ZsptvClient(raw), default_remark

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

        sender.reply(f"""
=====天牛 数据提交=====
👉 请直接发送数据，格式如下(一行一个)：
token
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
                client, line_remark = parse_bind_input_line(line_val, remark)
                info_res = client.check_info()

                nick = info_res['nickname']
                final_token_str = info_res['final_token']
                acc_id = info_res['acc_key']
                aliases = info_res.get('aliases', [])
                acc_type = info_res.get('acc_type', '')
                legacy_key = info_res.get('legacy_key', '')
                mobile = client.mobile or info_res.get('mobile', '')

                bind_result = process_account_binding(final_token_str, acc_id, nick, line_remark, aliases, acc_type, legacy_key, mobile=mobile, web_token=getattr(client, "web_token", ""), silent=(len(token_lines) > 1))
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
                fail_msgs.append(str(ex)[:50])
                if len(token_lines) == 1:
                    sender.reply(f"❌ 登录处理失败: {str(ex)}")

        if len(token_lines) > 1:
            fail_text = ""
            if fail_msgs:
                fail_text = "\n❌ 失败原因: " + "；".join(list(dict.fromkeys(fail_msgs))[:3])
            sender.reply(f"""=====天牛登录汇总=====
✅ 成功: {bind_stats['success']} 个
🆕 新增: {bind_stats['new']} 个
🔄 更新: {bind_stats['update']} 个
🔁 承接旧账号: {bind_stats['migrate']} 个
❌ 失败: {bind_stats['fail']} 个{fail_text}
==================""")

    except Exception as e:
        logger.error(f"绑定失败: {e}")
        sender.reply(f"❌ 绑定失败: {e}")

def process_account_binding(full_token, unique_id, nickname, remark="", aliases=None, acc_type="", legacy_key="", mobile="", web_token="", silent=False):
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
            next_step = f'发送 {config["randommanagecommand"]} 进行授权'

        if config['enable_remark'] and not remark:
            remark = RemarkManager.get_account_remark(userid, account)

        remark_info = f"\n📝 备注: {remark}" if remark else ""
        account_display = get_account_display(account, remark)

        is_new = AccountManager.add_account(userid, account)
        action = "new" if is_new else "update"
        if is_new:
            try: sg.bucketSet(bucket='tian_niu_bind_date', key=account, value=str(datetime.now().date()))
            except: pass
        AccountManager.update_account_token(account, full_token)
        if mobile:
            AccountManager.update_account_mobile(account, mobile)
        if web_token:
            AccountManager.update_account_web_token(account, web_token)

        if config['enable_remark'] and remark:
            RemarkManager.set_account_remark(userid, account, remark)

        ql_msg = ""
        if is_authorized:
            if sys_api.sync_env(full_token, account, remark, accountVip, owner_user_id=userid):
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
=====天牛账号更新=====
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
    accounts = AccountManager.get_accounts(userid)
    if not accounts:
        sender.reply(f"❌ 未找到账号，请发送 {config['randomsigncommand']} 绑定")
        return

    account_remarks = RemarkManager.get_all_remarks(userid) if config['enable_remark'] else {}
    count = len(accounts)
    account_list = "======我的天牛账号====="
    today_time = str(datetime.now().date())

    for i, account in enumerate(accounts, 1):
        account = str(account)
        accountVip = '2099-12-31'
        if not accountVip: vip_status = '⚠️ 未授权'
        elif accountVip < today_time: vip_status = '❌ 已过期'
        else: vip_status = f'✅ {accountVip}'

        remark = account_remarks.get(account, "") if config['enable_remark'] else ""
        account_display = get_account_display(account, remark)

        account_list += f"\n------------------\n[{i}] 账号: {account_display}\n🔐 授权: {vip_status}"

    account_list += "\n------------------\n[b] 批量授权\n[d] 批量删除\n[q] 退出管理\n提示: 可回复 1,2 或 3-6 多选管理\n=================="
    sender.reply(account_list)

    response = get_user_input()
    if not response or response.lower() == 'q':
        sender.reply('✅ 已退出')
        return

    if response.lower() == 'b':
        batch_auth_flow(accounts, account_remarks)
        return
    elif response.lower() == 'd':
        batch_delete_flow(accounts)
        return

    selected_idxs, invalid_parts = parse_index_selection(response, count, allow_all=False)
    if invalid_parts:
        sender.reply(f"⚠️ 已忽略无效内容: {','.join(invalid_parts[:5])}")

    if len(selected_idxs) == 1:
        manage_single_account(str(accounts[selected_idxs[0] - 1]), account_remarks)
    elif len(selected_idxs) > 1:
        selected_accs = [str(accounts[i - 1]) for i in selected_idxs]
        manage_multiple_accounts(selected_accs, account_remarks)
    else:
        sender.reply('❌ 序号无效或格式错误')

def manage_multiple_accounts(selected_accs, account_remarks):
    sender.reply(f"""=====批量管理=====
已选择 {len(selected_accs)} 个账号
------------------
[1] 批量授权
[2] 批量删除
------------------
回复数字选择，Q退出
==================""")
    sel = get_user_input()
    if sel == '1':
        batch_auth_selected(selected_accs, account_remarks)
    elif sel == '2':
        batch_delete_selected(selected_accs)
    elif sel and sel.lower() == 'q':
        sender.reply("✅ 已退出")

def batch_auth_flow(all_accounts, account_remarks):
    sender.reply(f"""=====选择授权账号=====
请输入要授权的账号序号
------------------
{selection_tip('授权')}
==================""")
    sel = get_user_input()
    if not sel or sel.lower() == 'q': return

    selected_idxs, invalid_parts = parse_index_selection(sel, len(all_accounts), allow_all=True)
    selected_accs = pick_accounts_by_indexes(all_accounts, selected_idxs)
    if selected_accs:
        if invalid_parts:
            sender.reply(f"⚠️ 已忽略无效内容: {','.join(invalid_parts[:5])}")
        batch_auth_selected(selected_accs, account_remarks)
    else:
        sender.reply("❌ 无效的序号，请回复如 1,2 或 3-6")

def batch_delete_flow(all_accounts):
    sender.reply(f"""=====选择删除账号=====
请输入要删除的账号序号
------------------
{selection_tip('删除')}
==================""")
    sel = get_user_input()
    if not sel or sel.lower() == 'q': return

    selected_idxs, invalid_parts = parse_index_selection(sel, len(all_accounts), allow_all=True)
    selected_accs = pick_accounts_by_indexes(all_accounts, selected_idxs)
    if selected_accs:
        if invalid_parts:
            sender.reply(f"⚠️ 已忽略无效内容: {','.join(invalid_parts[:5])}")
        batch_delete_selected(selected_accs)
    else:
        sender.reply("❌ 无效的序号，请回复如 1,2 或 3-6")

def manage_single_account(account, account_remarks):
    try:
        account = str(account)
        token = AccountManager.get_token(account)
        if not token: token = ""
        accountVip = '2099-12-31'
        remark = account_remarks.get(account, "") if config['enable_remark'] else ""

        today_time = str(datetime.now().date())
        vip_status = '⚠️ 未授权' if not accountVip else ('❌ 已过期' if accountVip < today_time else f'✅ {accountVip}')

        account_display = get_account_display(account, remark)

        menu_items = """
[1] 授权账号
[2] 删除账号
[3] 修改备注"""

        sender.reply(f"""
=====账号详情=====
📱 账号: {account_display}
📝 备注: {remark if remark else "无"}
🔐 授权: {vip_status}
=================={menu_items}
------------------
回复数字选择，Q退出
==================""")

        choice = get_user_input()
        if not choice or choice == 'q': return

        if choice == '1':
            sender.reply("请输入授权月数(如:1)，Q退出")
            months_str = get_user_input()
            if not months_str or months_str == 'q': return
            try:
                months = int(months_str)
                if months <= 0: raise ValueError
            except:
                sender.reply("❌ 数字无效")
                return

            if process_payment(months, accountVip, token, account, remark):
                try:
                    days = months * 30
                    new_auth_time = empower(accountVip, days)
                    try:
                        pass
                    except: pass

                    today_date = datetime.now().date()
                    for d in range(config['reminder_days'] + 1):
                        remind_key = f"{userid}_{account}_{today_date - timedelta(days=d)}"
                        try: sg.bucketDel('tian_niu_remind_log', remind_key)
                        except: pass

                    if token:
                        sys_api.sync_env(token, account, remark, new_auth_time, owner_user_id=userid)
                        sender.reply("🔄 授权成功并同步到系统！")
                    else:
                        sender.reply("✅ 授权成功")

                    money = Decimal(months) * config['zsVipmoney']
                    sender.reply(f"=====订单完成=====\n💰 金额: {money}元\n📅 到期: {new_auth_time}")
                except Exception as ex:
                    sender.reply(f"❌ 授权后续写入异常: {ex}")

        elif choice == '2':
            sender.reply("确认删除回复【y】")
            if get_user_input() == 'y':
                try:
                    AccountManager.remove_account(userid, account)
                    try: sg.bucketDel(bucket='tian_niu_token', key=account)
                    except: pass
                    try: sg.bucketDel(bucket='tian_niu_mobile', key=account)
                    except: pass
                    try: sg.bucketDel(bucket='tian_niu_web_token', key=account)
                    except: pass
                    try:
                        pass
                    except: pass
                    if config['enable_remark']: RemarkManager.delete_account_remark(userid, account)
                    sys_api.delete_env(account, token)
                    today_date = datetime.now().date()
                    for d in range(config['reminder_days'] + 1):
                        remind_key = f"{userid}_{account}_{today_date - timedelta(days=d)}"
                        try: sg.bucketDel('tian_niu_remind_log', remind_key)
                        except: pass
                    sender.reply("✅ 删除成功")
                except Exception as ex:
                    sender.reply(f"❌ 删除异常: {ex}")

        elif choice == '3':
             sender.reply("请输入新备注:")
             new_remark = get_user_input()
             if new_remark and new_remark != 'q':
                 RemarkManager.set_account_remark(userid, account, new_remark)
                 if token:
                     sys_api.sync_env(token, account, new_remark, accountVip, owner_user_id=userid)
                 sender.reply("✅ 备注更新成功")

    except Exception as e:
        sender.reply(f"操作失败: {e}")

def process_payment(months, accountVip, token, account, remark=""):
    return True
def batch_auth_selected(accounts, account_remarks):
    sender.reply(f"已选择 {len(accounts)} 个账号\n请输入授权月数，Q退出")
    m = get_user_input()
    if not m or not m.isdigit(): return
    months = int(m)
    if months <= 0: return

    count = len(accounts)
    total_money = Decimal(months) * config['zsVipmoney'] * count
    total_points = config['zscoin'] * months * count
    user_points, points_bucket = get_user_points()

    options = []
    idx = 1

    if config['zscoin'] > 0:
        options.append({'id': idx, 'type': 'pt', 'name': '积分支付', 'amount': total_points, 'curr': user_points})
        idx += 1

    if config['epay_url'] and config['epay_pid'] and config['epay_key']:
        if config['epay_alipay']:
            options.append({'id': idx, 'type': 'epay', 'channel': 'alipay', 'name': '支付宝', 'amount': total_money})
            idx += 1
        if config['epay_wxpay']:
            options.append({'id': idx, 'type': 'epay', 'channel': 'wxpay', 'name': '微信支付', 'amount': total_money})
            idx += 1
        if config['epay_qqpay']:
            options.append({'id': idx, 'type': 'epay', 'channel': 'qqpay', 'name': 'QQ钱包', 'amount': total_money})
            idx += 1

    if config['enable_zsm'] and config['zsm']:
        options.append({'id': idx, 'type': 'wx', 'name': '个人微信收款', 'amount': total_money})
        idx += 1

    if not options:
        sender.reply("❌ 未配置任何支付方式")
        return

    msg = f"=====批量授权确认=====\n👥 账号数量: {count}个\n📅 授权时长: {months}个月\n💰 总需金额: {total_money}元\n💎 总需积分: {total_points}\n------------------"
    for opt in options:
        amount_str = f"{opt['amount']}积分" if opt['type'] == 'pt' else f"{opt['amount']}元"
        suffix = f" (当前: {opt['curr']})" if opt['type'] == 'pt' else ""
        msg += f"\n[{opt['id']}] {opt['name']} ({amount_str}){suffix}"
    msg += "\n------------------\n回复数字选择，Q退出"
    sender.reply(msg)

    sel = get_user_input()
    if not sel or sel == 'q': return

    try:
        choice = int(sel)
        opt = next((o for o in options if o['id'] == choice), None)
        if not opt: raise ValueError

        if opt['type'] == 'epay':
            out_trade_no = f"TNHS_BATCH_{int(time.time())}_{userid}_{random.randint(1000,9999)}"
            formatted_money = f"{float(opt['amount']):.2f}"
            channel_name = "支付宝" if opt['channel'] == 'alipay' else ("微信支付" if opt['channel'] == 'wxpay' else "QQ钱包")

            qr_image_url, _ = _create_epay_qr(out_trade_no, opt['channel'], f"Batch_{count}_{months}M", formatted_money)

            sender.reply(f"=====等待支付=====\n💰 金额: {formatted_money}元\n💳 方式: {channel_name}\n📋 订单: {out_trade_no}\n------------------\n请在 180 秒内完成扫在线处理 (完成后自动批量授权)\n回复\"q\"取消支付")
            sender.replyImage(qr_image_url)

            start_time = time.time()
            paid = False
            query_url = f"{config['epay_url'].rstrip('/')}/api.php?act=order&pid={config['epay_pid']}&key={config['epay_key']}&out_trade_no={out_trade_no}"

            while time.time() - start_time < 180:
                try:
                    res = requests.get(query_url, timeout=5).json()
                    if str(res.get('code')) == '1' and str(res.get('status')) == '1':
                        paid = True
                        break
                except:
                    pass

                cancel_check = sender.listen(3000)
                if cancel_check and cancel_check.lower() == 'q':
                    sender.reply("✅ 已取消支付")
                    return

            if not paid:
                sender.reply("❌ 支付超时，请重新发起。")
                return

        elif opt['type'] == 'wx':
            if False:
                sender.reply("⚠️ 当前有人支付中")
                return

            out_trade_no = f"WX_{int(time.time())}_{random.randint(100,999)}"
            sender.reply(f"=====等待支付=====\n💰 金额: {opt['amount']}元\n💳 方式: 个人微信收款\n📋 订单: {out_trade_no}\n------------------\n请在 60 秒内完成扫在线处理 (完成后自动授权)\n回复\"q\"取消支付")
            sender.replyImage(config['zsm'])
            res = False
            if str(res) == 'q': return

            try:
                if isinstance(res, dict):
                    Money = float(res.get('Money', res.get('money', 0)))
                    From = res.get('FromName', res.get('fromName', ''))
                else:
                    res_json = json.loads(res)
                    Money = float(res_json.get('Money', res_json.get('money', 0)))
                    From = res_json.get('FromName', res_json.get('fromName', ''))

                if float(Money) < float(opt['amount']):
                    sender.reply(f"=====支付金额错误=====\n💰 应付: {opt['amount']}元\n💳 实付: {Money}元\n👤 付款人: {From}\n❗ 请稍后核对支付记录！")
                    return
            except:
                sender.reply("❌ 处理支付结果时出错")
                return

        elif opt['type'] == 'pt':
            if int(opt['curr']) < int(opt['amount']):
                sender.reply(f"❌ 积分不足，需要 {opt['amount']}，当前 {opt['curr']}")
                return
            sender.reply(f"确认消耗 {opt['amount']} 积分？回复【y】")
            if get_user_input() != 'y': return
            new_pt = int(opt['curr']) - int(opt['amount'])
            try: set_user_points(new_pt, points_bucket)
            except Exception as e:
                sender.reply(f"❌ 积分扣除异常: {e}")
                return

    except Exception:
        sender.reply("❌ 输入错误或支付取消")
        return

    sender.reply(f"🚀 支付成功，正在处理 {count} 个账号...")
    for account in accounts:
        try:
            account = str(account)
            accountVip = '2099-12-31'
            new_date = empower(accountVip, months*30)
            try:
                pass
            except: pass

            token = AccountManager.get_token(account)
            curr_remark = account_remarks.get(account, "") if account_remarks else ""

            if token:
                sys_api.sync_env(token, account, curr_remark, new_date, owner_user_id=userid)

            today_date = datetime.now().date()
            for d in range(config['reminder_days'] + 1):
                remind_key = f"{userid}_{account}_{today_date - timedelta(days=d)}"
                try: sg.bucketDel('tian_niu_remind_log', remind_key)
                except: pass
        except: pass

    sender.reply("✅ 批量授权完成")

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
                 try: sg.bucketDel(bucket='tian_niu_token', key=account)
                 except: pass
                 try: sg.bucketDel(bucket='tian_niu_mobile', key=account)
                 except: pass
                 try: sg.bucketDel(bucket='tian_niu_web_token', key=account)
                 except: pass
                 try:
                     pass
                 except: pass
                 if config['enable_remark']: RemarkManager.delete_account_remark(userid, account)
                 sys_api.delete_env(account, token)
                 for d in range(config['reminder_days'] + 1):
                     remind_key = f"{userid}_{account}_{today_date - timedelta(days=d)}"
                     try: sg.bucketDel('tian_niu_remind_log', remind_key)
                     except: pass
            except: pass
        sender.reply("✅ 批量删除完成")

def clean_expired_accounts(force_report=False):
    panel_sync = sync_local_auth_from_panel()
    users = sg.bucketAllKeys(bucket='tian_niu_user')
    if not users:
        if sender.isAdmin() and (force_report or usermessage in ['天牛清理', '清理天牛']):
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

    if sender.isAdmin() and (force_report or usermessage in ['天牛清理', '清理天牛']):
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

    batch_verify_account_ck(ck_verify_tasks)

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
                    is_ck_valid = True

                    if is_ck_valid and 0 <= days_diff <= reminder_days_cfg:
                        remind_key = f"{user}_{account}_{today_date}"
                        has_reminded = sg.bucketGet('tian_niu_remind_log', remind_key)

                        if not has_reminded:
                            account_display = get_account_display(account, account_remarks.get(account, ""))
                            msg = f"""=====⏰ 到期提醒=====
您的天牛账号授权即将到期！
📱 账号: {account_display}
📅 到期: {expiration_str} (剩余 {days_diff} 天)
------------------
为避免影响挂机，请及时续费。
发送 {config['randommanagecommand']} 进行续费
=================="""
                            if safe_send_message(user, msg, f"到期提醒 {user}-{account}"):
                                try: sg.bucketSet('tian_niu_remind_log', remind_key, "1")
                                except: pass
                                reminded_count += 1
                    continue

                if days_diff < 0:
                    try:
                        sys_api.delete_env(account, account_item.get("full_token"))
                        try: sg.bucketDel(bucket='tian_niu_token', key=account)
                        except: pass
                        try: sg.bucketDel(bucket='tian_niu_mobile', key=account)
                        except: pass
                        try: sg.bucketDel(bucket='tian_niu_web_token', key=account)
                        except: pass
                        try:
                            pass
                        except: pass
                        if config['enable_remark']:
                            RemarkManager.delete_account_remark(user, account)
                    except: pass

                    account_display = get_account_display(account, account_remarks.get(account, ""))
                    clean_msg = f"""=====🗑️ 过期清理通知=====
您的天牛账号授权已过期并清理。
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
                    try: sg.bucketSet(bucket='tian_niu_user', key=str(user), value=str(valid_accounts))
                    except: pass
                else:
                    try: sg.bucketDel(bucket='tian_niu_user', key=str(user))
                    except: pass

        except Exception:
            continue

    if sender.isAdmin() and (force_report or usermessage in ['天牛清理', '清理天牛']):
        sender.reply(
            f"=====天牛维护完成=====\n"
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

def admin_auth_options():
    return True
def collect_admin_stats():
    stats = {
        "users": 0, "accounts": 0, "authorized": 0, "unauthorized": 0,
        "expired": 0, "expiring": 0, "no_token": 0
    }
    today = datetime.now().date()
    users = AccountManager.get_all_users()
    stats["users"] = len(users)
    for user in users:
        for account in AccountManager.get_accounts(user):
            try:
                stats["accounts"] += 1
                account = str(account)
                token = AccountManager.get_token(account)
                if not token:
                    stats["no_token"] += 1
                vip = '2099-12-31'
                if not vip:
                    stats["unauthorized"] += 1
                    continue
                try:
                    vip_date = datetime.strptime(str(vip), "%Y-%m-%d").date()
                except:
                    stats["expired"] += 1
                    continue
                if vip_date < today:
                    stats["expired"] += 1
                else:
                    stats["authorized"] += 1
                    if (vip_date - today).days <= config['reminder_days']:
                        stats["expiring"] += 1
            except:
                pass
    return stats

def admin_overview():
    if not sender.isAdmin():
        sender.reply("❌ 权限不足")
        return
    sender.reply("⏳ 正在统计数据，请稍候...")
    stats = collect_admin_stats()
    sender.reply(f"""=====天牛数据总览=====
👥 用户数: {stats['users']}
📦 账号数: {stats['accounts']}
✅ 授权中: {stats['authorized']}
⚠️ 未授权: {stats['unauthorized']}
❌ 已过期: {stats['expired']}
⏰ 即将到期: {stats['expiring']}
🔑 缺少配置: {stats['no_token']}
==================""")

def send_long_admin_message(title, lines, footer="==================", max_len=1500):
    if not lines:
        sender.reply(f"{title}\n📭 暂无数据\n{footer}")
        return
    part = 1
    total_parts = 1
    chunks = []
    current = title
    for line in lines:
        add_text = "\n" + line
        if len(current) + len(add_text) + len(footer) + 20 > max_len and current != title:
            chunks.append(current)
            current = title
        current += add_text
    chunks.append(current)
    total_parts = len(chunks)
    for chunk in chunks:
        page_tip = f"\n-----第 {part}/{total_parts} 段-----" if total_parts > 1 else ""
        sender.reply(f"{chunk}{page_tip}\n{footer}")
        part += 1
        time.sleep(0.2)

def admin_user_ck_preview():
    if not sender.isAdmin():
        sender.reply("❌ 权限不足")
        return
    sender.reply("⏳ 正在生成用户配置预览，请稍候...")

    today = datetime.now().date()
    rows = []
    total_accounts = 0
    for user in AccountManager.get_all_users():
        try:
            accounts = AccountManager.get_accounts(user)
            if not accounts:
                continue
            auth_count = 0
            unauth_count = 0
            expired_count = 0
            expiring_count = 0
            no_token_count = 0

            for account in accounts:
                account = str(account)
                total_accounts += 1
                if not AccountManager.get_token(account):
                    no_token_count += 1
                vip = '2099-12-31'
                if not vip:
                    unauth_count += 1
                    continue
                try:
                    vip_date = datetime.strptime(str(vip), "%Y-%m-%d").date()
                except:
                    expired_count += 1
                    continue
                if vip_date < today:
                    expired_count += 1
                else:
                    auth_count += 1
                    if (vip_date - today).days <= config['reminder_days']:
                        expiring_count += 1

            rows.append({
                "user": str(user),
                "count": len(accounts),
                "auth": auth_count,
                "unauth": unauth_count,
                "expired": expired_count,
                "expiring": expiring_count,
                "no_token": no_token_count
            })
        except:
            pass

    rows.sort(key=lambda x: x["count"], reverse=True)
    lines = [f"👥 用户数: {len(rows)}  📦 账号总数: {total_accounts}", "------------------"]
    for i, row in enumerate(rows, 1):
        extra = []
        if row["unauth"]:
            extra.append(f"未授权{row['unauth']}")
        if row["expired"]:
            extra.append(f"过期{row['expired']}")
        if row["expiring"]:
            extra.append(f"临期{row['expiring']}")
        if row["no_token"]:
            extra.append(f"缺配置{row['no_token']}")
        extra_text = f" ({' / '.join(extra)})" if extra else ""
        lines.append(f"[{i}] 用户: {row['user']}\n配置: {row['count']} 个  授权: {row['auth']} 个{extra_text}")

    send_long_admin_message("=====用户配置预览=====", lines)

def admin_find_account():
    if not sender.isAdmin():
        sender.reply("❌ 权限不足")
        return
    sender.reply("""=====反查账号归属=====
请输入账号尾号/备注/用户ID
例如: 893 或 小号 或 wxid
回复 q 退出
==================""")
    keyword = get_user_input()
    if not keyword or keyword.lower() == 'q': return
    keyword = keyword.strip()

    matches = []
    users = AccountManager.get_all_users()
    for user in users:
        if keyword in str(user):
            user_match = True
        else:
            user_match = False
        remarks = RemarkManager.get_all_remarks(user) if config['enable_remark'] else {}
        for account in AccountManager.get_accounts(user):
            try:
                account = str(account)
                remark = remarks.get(account, "")
                safe_acc = mask_account(account)
                account_display = get_account_display(account, remark)
                vip = '2099-12-31'
                vip_st = '未授权' if not vip else str(vip)
                if user_match or keyword in account or keyword in safe_acc or (remark and keyword in remark):
                    matches.append(f"👤 用户: {user}\n📱 账号: {account_display}\n🔐 授权: {vip_st}")
            except:
                pass

    if not matches:
        sender.reply("❌ 未找到匹配账号")
        return
    msg = f"=====反查结果=====\n共找到 {len(matches)} 条"
    for item in matches[:10]:
        msg += f"\n------------------\n{item}"
    if len(matches) > 10:
        msg += f"\n------------------\n仅显示前10条，共 {len(matches)} 条"
    msg += "\n=================="
    sender.reply(msg)

def admin_sync_panel():
    if not sender.isAdmin():
        sender.reply("❌ 权限不足")
        return
    sender.reply("⚠️ 同步面板变量功能已撤销，避免面板备注反向覆盖本地账号归属。")
    return
    sender.reply("""=====同步面板变量=====
[1] 同步所有授权账号
[2] 同步指定用户账号
------------------
回复数字选择，Q退出
==================""")
    choice = get_user_input()
    if not choice or choice.lower() == 'q': return

    users = []
    if choice == '1':
        users = AccountManager.get_all_users()
        total_accounts = sum(len(AccountManager.get_accounts(u)) for u in users)
        if len(users) <= 1 and total_accounts > 5:
            sender.reply(
                "⚠️ 已拦截同步所有授权账号。\n"
                f"当前本地归属表异常：用户数 {len(users)}，账号数 {total_accounts}。\n"
                "这通常表示账号被集中到了管理员名下，继续同步会覆盖面板归属备注。\n"
                "请先恢复 tian_niu_user 归属表，或使用 [2] 同步指定用户账号。"
            )
            return
        sender.reply(f"⚠️ 即将同步所有授权账号。\n确认请回复【确认同步】")
        if get_user_input() != "确认同步":
            sender.reply("✅ 已取消同步")
            return
    elif choice == '2':
        sender.reply("请输入用户ID(QQ号或wxid)，回复q退出")
        target_user = get_user_input()
        if not target_user or target_user.lower() == 'q': return
        users = [target_user.strip()]
    else:
        sender.reply("❌ 请输入有效选项")
        return

    today = str(datetime.now().date())
    success = 0
    skipped = 0
    failed = 0
    sender.reply("⏳ 正在同步，请稍候...")
    for user in users:
        remarks = RemarkManager.get_all_remarks(user) if config['enable_remark'] else {}
        for account in AccountManager.get_accounts(user):
            try:
                account = str(account)
                vip = '2099-12-31'
                token = AccountManager.get_token(account)
                if not vip or vip < today or not token:
                    skipped += 1
                    continue
                remark = remarks.get(account, "")
                if sys_api.sync_env(token, account, remark, vip, owner_user_id=user):
                    success += 1
                else:
                    failed += 1
            except:
                failed += 1

    sender.reply(f"""=====同步完成=====
✅ 成功: {success}
⏸️ 跳过: {skipped}
❌ 失败: {failed}
==================""")

def admin_auth_all_users():
    return True
def admin_auth_specific_user():
    return True
def show_tutorial():
    panel_name = '青龙' if config['panel_type'] == 'qinglong' else '呆呆'
    sender.reply(f"""
=====天牛管理插件教程=====
当前模式: 🌐 提交至{panel_name}面板

1️⃣ {config['randomsigncommand']}
   发送天牛配置自动覆盖更新。

2️⃣ {config['randomquerycommand']}
   查询存活状态、手机号、当前积分和金额(支持1,2多选)。

3️⃣ {config['randommanagecommand']}
   全新支付接口，极简扫码无需挂机，付完全自动回调开通。

4️⃣ 天牛授权
   管理员总管理：授权、总览、配置预览、反查、同步、清理。

5️⃣ 天牛清理 / 天牛广播
   自动维护与消息分发。
==================""")

try:
    command = usermessage.strip()

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

    elif re.match(r'^天牛(通知|广播)\s*', command):
        notify_authorized_users()
    elif command in ['天牛登录', '天牛登陆', '登录天牛', '登陆天牛']:
        bindaccount()
    elif command in ['天牛管理', '管理天牛']:
       xy_manage()
    elif command in ['天牛查询', '查询天牛']:
        cxs()
    elif command in ['天牛清理', '清理天牛']:
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
    elif command == '天牛授权':
        admin_auth_options()
    elif command == '天牛教程':
        show_tutorial()

except Exception as e:
    logger.error(f"Error: {e}")
    sender.reply(f"❌ 系统错误: {e}")
