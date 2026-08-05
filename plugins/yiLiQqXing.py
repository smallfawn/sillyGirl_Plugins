# [title: 伊利QQ星]
# [name: yiLiQqXing]
# [language: python]
# [class: 任务]
# [author: 8165799]
# [version: v1.1]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(伊利|伊利【Qq]
# [cron: 5 11 * * *]
# [icon: https://api.iconify.design/lucide:bot.svg]
# [description: 伊利QQ星代挂提交；4.]
# [depe: ["requests"]]
# [staticmethod: def find_migration_source(user_id, new_account, aliases=None, acc_type="", legacy_key=""):]


import asyncio as _sg_asyncio, os as _sg_os, time as _sg_time, types as _sg_types, json as _sg_json, re as _sg_re, urllib.parse as _sg_urlparse
from threading import Thread as _sg_Thread
from sillygirl import Adapter as _SGAdapter, Bucket as _SGBucket, Sender as _SGSender, sender as _sg_sender, container as _sg_container
try:
    import ast as _sg_ast
except Exception:
    _sg_ast = None
try:
    import decimal as decimal
except Exception:
    decimal = None

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

def _sg_literal(value, default=None):
    if isinstance(value,(list,dict,tuple,set,int,float,bool)) or value is None:
        return value if value is not None else ([] if default is None else default)
    text=str(value or "").strip()
    if not text: return [] if default is None else default
    for parser in (_sg_json.loads, (_sg_ast.literal_eval if _sg_ast else None)):
        if parser:
            try: return parser(text)
            except Exception: pass
    return [] if default is None else default

def _sg_sender_sync(uuid=""):
    s=_SGSender(uuid or _sg_os.environ.get("SENDER_ID", ""))
    def call(name,*a,**k): return _sg_run(getattr(s,name)(*a,**k))
    def listen(timeout=60000,*a,**k):
        try:
            r=call("listen", {"timeout": int(timeout or 0)})
            return _sg_run(r.getContent()) if r else ""
        except Exception: return ""
    return _sg_types.SimpleNamespace(
        getUserID=lambda:call("getUserId"), getUserId=lambda:call("getUserId"), getMessage=lambda:call("getContent"), getContent=lambda:call("getContent"),
        getUserName=lambda:call("getUserName"), getNickname=lambda:call("getUserName"), getChatID=lambda:call("getChatId"), getChatId=lambda:call("getChatId"),
        getImtype=lambda:call("getPlatform"), getPlatform=lambda:call("getPlatform"), getMessageID=lambda:call("getMessageId"), getPluginName=lambda:_sg_os.environ.get("PLUGIN_NAME",""), getPluginVersion=lambda:_sg_os.environ.get("PLUGIN_VERSION",""),
        isAdmin=lambda:bool(call("isAdmin")), reply=lambda msg="":call("reply", str(msg)), replyImage=lambda url="":call("reply", str(url) if str(url).startswith("[") else f"[CQ:image,file={url}]"),
        listen=listen, input=listen, waitInput=listen, setContinue=lambda *a,**k:call("continue_"), breakIn=lambda *a,**k:call("continue_"))

def _sg_bucket_get(bucket=None,key=None,default="",**kw):
    try:
        v=_SGBucket(str(kw.get("bucket",bucket) or ""))[str(kw.get("key",key) or "")]
        return default if v in (None,"") and default not in (None,"") else (v if v is not None else "")
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
    i=a[0] if a and isinstance(a[0],dict) else {}; platform=i.get("imType") or i.get("platform") or kw.get("platform") or (a[0] if a else ""); group=i.get("groupCode") or i.get("group_id") or kw.get("group_id") or (a[1] if len(a)>1 else ""); user=i.get("userID") or i.get("user_id") or kw.get("userID") or (a[2] if len(a)>2 else ""); title=i.get("title") or kw.get("title") or (a[3] if len(a)>3 else ""); content=i.get("content") or i.get("message") or kw.get("content") or (a[4] if len(a)>4 else title)
    return _sg_run(_SGAdapter(str(platform or "")).push({"group_id":str(group or ""),"user_id":str(user or ""),"title":str(title or ""),"content":str(content or "")}))
def _sg_notify(msg,channels=None,*a,**k): return _sg_run(_sg_sender.pushAdmin(str(msg), {"platforms":list(channels or [])} if channels else {}))
class _SGFacade:
    Sender=staticmethod(_sg_sender_sync); getSenderID=staticmethod(lambda:_sg_os.environ.get("SENDER_ID","")); getPluginName=staticmethod(lambda:_sg_os.environ.get("PLUGIN_NAME","")); bucketGet=staticmethod(_sg_bucket_get); bucketSet=staticmethod(_sg_bucket_set); bucketDel=staticmethod(_sg_bucket_del); bucketDelete=staticmethod(_sg_bucket_del); bucketAllKeys=staticmethod(_sg_bucket_keys); bucketKeys=staticmethod(_sg_bucket_keys); bucketAll=staticmethod(_sg_bucket_all); notifyMasters=staticmethod(_sg_notify); pushAdmin=staticmethod(_sg_notify); push=staticmethod(_sg_push); Push=staticmethod(_sg_push); reply=staticmethod(lambda msg="":_sg_sender_sync().reply(msg)); get=staticmethod(lambda key,default="":_sg_bucket_get(*(str(key).split(".",1) if "." in str(key) else ["otto",key]), default=default)); getParam=get; version=staticmethod(lambda:{"sn":_sg_os.environ.get("SILLYGIRL_VERSION","3.0.0"),"version":_sg_os.environ.get("SILLYGIRL_VERSION","3.0.0")}); port=staticmethod(lambda:_sg_os.environ.get("SILLYGIRL_PORT","8080")); sleep=staticmethod(lambda sec:_sg_time.sleep(float(sec or 0)))
sg=_SGFacade(); Sender=sg.Sender; getSenderID=sg.getSenderID; bucketGet=sg.bucketGet; bucketSet=sg.bucketSet; bucketAllKeys=sg.bucketAllKeys; notifyMasters=sg.notifyMasters

def mask_account(value):
    value=str(value or ""); return value if len(value)<=7 else value[:3]+"***"+value[-4:]
def generate_qrcode_url(text): return "https://api.qrserver.com/v1/create-qr-code/?size=260x260&data="+_sg_urlparse.quote(str(text or ""))
def get_pay_config(): return {}
class MaPayClient:
    def create_order(self,*a,**k): return {"error":"","status":True,"data":None}
    def is_paid(self,*a,**k): return True
def calculate_auth_time(*a,**k): return "2099-12-31"
def check_auth_status(*a,**k): return "账号默认可用"
_check_auth_status=check_auth_status
def select_accounts(sender,user_bucket,user_id,*a,**k):
    raw=sg.bucketGet(user_bucket,user_id,[]); raw=_sg_literal(raw,[]) if isinstance(raw,str) else raw
    if isinstance(raw,dict): raw=list(raw.keys()) or list(raw.values())
    return (raw if isinstance(raw,list) else []), (raw if isinstance(raw,list) else [])
def process_authorization(*a,**k): return True
def process_coin_payment(*a,**k): return True
def admin_auth_all_accounts(*a,**k): return True
def admin_auth_by_user(*a,**k): return True
def get_user_points(user_id=None,bucket="dd_sign_points"):
    try: return int(sg.bucketGet(bucket,user_id or sg.getSenderID()) or 0)
    except Exception: return 0
def update_user_points(user_id=None,points=0,bucket="dd_sign_points"): return sg.bucketSet(bucket,user_id or sg.getSenderID(),str(points))
def _sg_panel_id(config=None):
    if isinstance(config,dict): config=config.get("id") or config.get("ID") or config.get("index") or config.get("name")
    m=_sg_re.search(r"\d+", str(config or "")); return int(m.group(0)) if m else 1
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

config = None
_CONFIG_FIELD_MAP = {}

import re
import ast
import os
from datetime import datetime, timedelta
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
from xml.etree import ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed

warnings.filterwarnings('ignore', message='Unverified HTTPS request')
requests.packages.urllib3.disable_warnings()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('yiliqqx_plugin')

REQUEST_TIMEOUT = 30
MAINTENANCE_CK_MAX_WORKERS = 8

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = str(sender.getUserID())
usermessage = sender.getMessage()
usermessage = str(usermessage or "").replace('伊利qq星', '伊利QQ星').replace('伊利Qq星', '伊利QQ星').replace('伊利qQ星', '伊利QQ星')

PLUGIN_NAME = "伊利QQ星签到插件"
PLUGIN_NAMESPACE = "yiliqqx"
PLUGIN_ID = "yiliqqx:伊利QQ星签到插件:v1"

PLUGIN_BUCKET_SUFFIXES = [
    "user",
    "token",
    "auth",
    "remarks",
    "bind_date",
    "remind_log",
    "runtime",
    "sender",
    "imtype",
]

PLUGIN_FOREIGN_BUCKETS = []
PLUGIN_SHARED_BUCKETS = ["dd_sign_points"]
PLUGIN_AUTO_NAMESPACE = True
PLUGIN_NAMESPACE_CANDIDATES = 50


def build_plugin_buckets(namespace, suffixes):
    return [f"{namespace}_{suffix}" for suffix in suffixes]


def plugin_bucket(suffix):
    return f"{PLUGIN_RUNTIME_NAMESPACE}_{suffix}"


def build_namespace_candidates(base_namespace, max_number=50):
    candidates = [base_namespace]
    candidates.extend(f"{base_namespace}{idx}" for idx in range(1, max_number + 1))
    candidates.extend(f"{base_namespace}{ch}" for ch in "abcdefghijklmnopqrstuvwxyz")
    return candidates


def _bucket_has_any_key(bucket_name):
    try:
        keys = sg.bucketAllKeys(bucket=bucket_name)
        return bool(keys)
    except Exception:
        return False


def assert_automan_bucket_namespace_safe(
    plugin_name,
    namespace,
    plugin_id,
    bucket_suffixes,
    foreign_buckets=None,
    shared_buckets=None,
):
    """傻妞框架通用桶护栏：防止模板插件误用同名桶导致账号/授权/token 串库。"""
    namespace = str(namespace or "").strip()
    plugin_id = str(plugin_id or "").strip()
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{2,30}", namespace):
        sender.reply(
            f"❌ {plugin_name} 已停止运行：插件命名空间不合法。\n"
            "命名空间只能使用字母、数字、下划线，且必须以字母开头。"
        )
        exit(0)

    foreign_buckets = [str(x).strip() for x in (foreign_buckets or []) if str(x).strip()]
    shared_buckets = set(str(x).strip() for x in (shared_buckets or []) if str(x).strip())
    guard_key = "namespace_owner"

    duplicated_suffixes = sorted({suffix for suffix in bucket_suffixes if bucket_suffixes.count(suffix) > 1})
    if duplicated_suffixes:
        sender.reply(
            f"❌ {plugin_name} 已停止运行：模板内数据桶后缀重复。\n"
            "重复后缀: " + "、".join(duplicated_suffixes)
        )
        exit(0)

    candidates = build_namespace_candidates(namespace, PLUGIN_NAMESPACE_CANDIDATES) if PLUGIN_AUTO_NAMESPACE else [namespace]
    blocked_notes = []

    for candidate in candidates:
        data_buckets = build_plugin_buckets(candidate, bucket_suffixes)
        guard_bucket = f"{candidate}_guard"

        duplicated = sorted({bucket for bucket in data_buckets if data_buckets.count(bucket) > 1})
        if duplicated:
            sender.reply(
                f"❌ {plugin_name} 已停止运行：模板内数据桶重复。\n"
                "重复桶: " + "、".join(duplicated)
            )
            exit(0)

        shared_conflicts = sorted(set(data_buckets) & shared_buckets)
        if shared_conflicts:
            sender.reply(
                f"❌ {plugin_name} 已停止运行：独占数据桶不能使用共享积分桶名称。\n"
                "冲突桶: " + "、".join(shared_conflicts)
            )
            exit(0)

        foreign_conflicts = sorted(set(data_buckets) & set(foreign_buckets))
        if foreign_conflicts:
            blocked_notes.append(f"{candidate}: 与已声明其他插件桶重复")
            continue

        try:
            owner = sg.bucketGet(bucket=guard_bucket, key=guard_key)
        except Exception:
            owner = ""

        if owner:
            if str(owner) == plugin_id:
                return candidate
            blocked_notes.append(f"{candidate}: 护栏标记不匹配({owner})")
            continue

        occupied = [bucket for bucket in data_buckets if _bucket_has_any_key(bucket)]
        if occupied:
            if candidate == namespace:
                try:
                    sg.bucketSet(bucket=guard_bucket, key=guard_key, value=plugin_id)
                    logger.warning(f"{plugin_name} 检测到默认桶已有历史数据，已认领原桶前缀：{candidate}")
                    return candidate
                except Exception as e:
                    blocked_notes.append(f"{candidate}: 历史数据桶认领失败({e})")
                    continue
            blocked_notes.append(f"{candidate}: 已有数据({','.join(occupied[:3])})")
            continue

        try:
            sg.bucketSet(bucket=guard_bucket, key=guard_key, value=plugin_id)
            if candidate != namespace:
                try:
                    sender.reply(f"ℹ️ {plugin_name} 检测到默认数据桶被占用，已自动切换到专用桶前缀：{candidate}")
                except Exception:
                    pass
            return candidate
        except Exception as e:
            blocked_notes.append(f"{candidate}: 护栏初始化失败({e})")
            continue

    detail = "\n".join(blocked_notes[:8]) if blocked_notes else "没有可用命名空间"
    sender.reply(
        f"❌ {plugin_name} 已停止运行：无法自动找到可用数据桶前缀。\n"
        "为避免账号、授权、token 数据错乱，本次不会写入任何数据。\n"
        f"{detail}"
    )
    exit(0)

PLUGIN_RUNTIME_NAMESPACE = assert_automan_bucket_namespace_safe(
    PLUGIN_NAME,
    PLUGIN_NAMESPACE,
    PLUGIN_ID,
    PLUGIN_BUCKET_SUFFIXES,
    foreign_buckets=PLUGIN_FOREIGN_BUCKETS,
    shared_buckets=PLUGIN_SHARED_BUCKETS,
)

try:
    sg.bucketSet(bucket=plugin_bucket('sender'), key=userid, value=str(senderID))
    sg.bucketSet(bucket=plugin_bucket('imtype'), key=userid, value=str(sender.getImtype()))
except:
    pass


def getusercontent():
    """获取插件完整配置"""
    panel_type = sg.bucketGet('yiliqqx', 'panel_type') or 'qinglong'
    panel_type = panel_type.lower()

    env_qlconfig = sg.bucketGet('yiliqqx', 'yiliqqx_qlname') or ''
    env_name = sg.bucketGet('yiliqqx', 'yiliqqx_osname') or 'YILIQQX_AUTH_KEY'

    if not env_qlconfig:
        sender.reply("❌ 配置错误：请在插件配置中填写【对接系统配置】(面板信息)。")
        exit(0)

    yiliqqx_managecommand = sg.bucketGet('yiliqqx', 'yiliqqx_managecommand') or '伊利管理'
    yiliqqx_querycommand = sg.bucketGet('yiliqqx', 'yiliqqx_querycommand') or '伊利查询'
    yiliqqx_signcommand = sg.bucketGet('yiliqqx', 'yiliqqx_signcommand') or '伊利登录'

    enable_proxy = (sg.bucketGet('yiliqqx', 'enable_proxy') or 'false').lower() == 'true'
    proxy_pool_url = sg.bucketGet('yiliqqx', 'proxy_pool_url') or ''
    enable_ck_notice = (sg.bucketGet('yiliqqx', 'enable_ck_notice') or 'true').lower() == 'true'
    points_bucket = sg.bucketGet('yiliqqx', 'points_bucket') or 'dd_sign_points'
    enable_remark = (sg.bucketGet('yiliqqx', 'enable_remark') or 'false').lower() == 'true'

    randommanagecommand = yiliqqx_managecommand
    randomquerycommand = yiliqqx_querycommand
    randomsigncommand = yiliqqx_signcommand

    yiliqqxVipmoney = Decimal(sg.bucketGet('yiliqqx', 'yiliqqxVipmoney') or '0')
    yiliqqxcoin = int(sg.bucketGet('yiliqqx', 'yiliqqxcoin') or '0')
    reminder_days = int(sg.bucketGet('yiliqqx', 'reminder_days') or '2')

    enable_wechat_qr = (sg.bucketGet('yiliqqx', 'enable_wechat_qr') or 'false').lower() == 'true'
    wechat_qr = sg.bucketGet('yiliqqx', 'wechat_qr') or ''

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
        'yiliqqx_managecommand': yiliqqx_managecommand,
        'yiliqqx_querycommand': yiliqqx_querycommand,
        'yiliqqx_signcommand': yiliqqx_signcommand,
        'randommanagecommand': randommanagecommand,
        'randomquerycommand': randomquerycommand,
        'randomsigncommand': randomsigncommand,
        'enable_wechat_qr': enable_wechat_qr,
        'wechat_qr': wechat_qr,
        'enable_proxy': enable_proxy,
        'proxy_pool_url': proxy_pool_url,
        'enable_ck_notice': enable_ck_notice,
        'points_bucket': points_bucket,
        'enable_remark': enable_remark,
        'yiliqqxVipmoney': yiliqqxVipmoney,
        'yiliqqxcoin': yiliqqxcoin,
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
        for owner in sg.bucketAllKeys(bucket=plugin_bucket('user')):
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
    if not force_send and sg.bucketGet(bucket=plugin_bucket('runtime'), key=report_key):
        if notify_status:
            sender.reply("ℹ️ 今日管理员汇总已发送过，如需重发请明天自动发送或再次手动清理。")
        return False

    msg = (
        "=====伊利QQ星维护完成=====\n"
        f"✅ 检测完成，共 {report_data.get('scanned_accounts', 0)} 个账号\n"
        f"📣 发送通知: {report_data.get('sent_notifications', 0)} 条\n"
        f"⚠️ CK失效通知: {report_data.get('ck_expired_count', 0)} 个\n"
        f"🗑️ 清理过期: {report_data.get('cleaned_count', 0)} 个\n"
        "=================="
    )

    framework_sent = send_message_to_framework_admins(msg)
    if framework_sent:
        try:
            sg.bucketSet(bucket=plugin_bucket('runtime'), key=report_key, value="framework")
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
    """
    批量验证 AuthKey。
    只在接口明确返回 AuthKey 无效时标记失效；网络异常、代理异常、接口超时都视为暂时未知，避免误推。
    """
    results = {}
    if not tasks or not config.get('enable_ck_notice', True):
        return results

    def verify_one(user, account, token):
        try:
            client = CastClient(token)
            net_ok, is_valid, _, msg = client.get_info()
            if net_ok and not is_valid:
                return (str(user), str(account)), {
                    "net_ok": True,
                    "valid": False,
                    "msg": str(msg or "AuthKey无效或已过期"),
                }
            return (str(user), str(account)), {
                "net_ok": bool(net_ok),
                "valid": True,
                "msg": str(msg or ""),
            }
        except Exception as e:
            return (str(user), str(account)), {
                "net_ok": False,
                "valid": True,
                "msg": str(e),
            }

    workers = max(1, min(int(max_workers or 1), len(tasks)))
    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_map = {
            executor.submit(verify_one, user, account, token): (user, account)
            for user, account, token in tasks
        }
        for future in as_completed(future_map):
            try:
                key, value = future.result()
                results[key] = value
            except Exception as e:
                user, account = future_map[future]
                results[(str(user), str(account))] = {
                    "net_ok": False,
                    "valid": True,
                    "msg": str(e),
                }
    return results

def send_user_notice(user_id, msg, title="伊利QQ星通知"):
    try:
        imtype = sg.bucketGet(bucket=plugin_bucket('imtype'), key=str(user_id)) or sender.getImtype()
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
        saved_sender = sg.bucketGet(bucket=plugin_bucket('sender'), key=str(user_id))
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
    ok, err = send_user_notice(user_id, msg, "伊利QQ星提醒")
    if not ok:
        logger.warning(f"消息发送失败 {log_context}: {err}")
    return ok

def parse_panel_yiliqqx_remark(remarks):
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
    if len(parts) >= 3:
        if account_id and parts[0] == account_id:
            return '#'.join(parts[:2])
        return '#'.join(parts[-2:])
    if len(parts) == 2:
        return '#'.join(parts)
    return str(value or '').strip()

def sync_local_auth_from_panel():
    return True

def mask_account(account):
    account = str(account)
    return account[:3] + "****" + account[-3:] if len(account) > 6 else account

def get_account_display(account, remark=""):
    remark = str(remark or "").strip()
    return remark if remark else mask_account(account)

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
    return imtype in ["fake", "cron"] or msg in ["", "cron", "定时任务"]

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

class YiLiQQStarClient:
    APPID = "wx650bdff059f63f5b"
    BASE_URL = "https://mall.yili.com/MAMAIF/MCSWSIAPI.asmx/Call"

    def __init__(self, token_str):
        self.token = str(token_str or '').strip()
        self.auth_key = self._extract_auth_key(self.token)
        self.member_info = None
        self.member_id = ""
        self.nickname = ""

    def _extract_auth_key(self, text):
        text = str(text or "").strip()
        if not text:
            return ""
        if "#" in text:
            parts = [p.strip() for p in text.split("#") if p.strip()]
            text = parts[-1] if parts else text
        if text.startswith("{"):
            try:
                data = json.loads(text)
                text = data.get("auth_key") or data.get("AuthKey") or text
            except:
                pass
        match = re.search(r'(?:AuthKey|auth_key)\s*[:=]\s*"?([0-9a-fA-F-]{32,64})"?', text)
        return match.group(1) if match else text.strip()

    def _get_proxy(self):
        if not config.get('enable_proxy') or not config.get('proxy_pool_url'):
            return None
        try:
            res = requests.get(config['proxy_pool_url'], timeout=8, verify=False)
            text = res.text.strip()
            match = re.search(r'(?:https?://)?\d+\.\d+\.\d+\.\d+:\d+', text)
            if match:
                proxy = match.group(0)
                if not proxy.startswith(('http://', 'https://')):
                    proxy = 'http://' + proxy
                return proxy
        except Exception as e:
            logger.warning(f"伊利QQ星查询获取代理失败: {e}")
        return None

    def _headers(self):
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows',
            'Content-Type': 'application/x-www-form-urlencoded',
            'xweb_xhr': '1',
            'Referer': f'https://servicewechat.com/{self.APPID}/162/page-frame.html',
        }

    def _parse_response(self, resp):
        text = resp.text.strip()
        if not text:
            return {}
        if text.startswith('<?xml') or text.startswith('<string'):
            try:
                root = ET.fromstring(text)
                text = root.text or ""
            except:
                match = re.search(r'<string[^>]*>(.*?)</string>', text, re.S)
                text = match.group(1) if match else text
        try:
            data = json.loads(text)
        except:
            return {}
        if isinstance(data.get('Result'), str):
            try:
                data['Result'] = json.loads(data['Result'])
            except:
                pass
        return data

    def call(self, method, params=""):
        if isinstance(params, dict):
            params = json.dumps(params, ensure_ascii=False)
        payload = {
            "DeviceCode": self.APPID,
            "AuthKey": self.auth_key or "0" * 36,
            "Method": method,
            "Params": params or "",
        }
        last_exc = None
        for attempt in range(1, 4):
            kwargs = {
                "headers": self._headers(),
                "data": {"RequestPack": json.dumps(payload, ensure_ascii=False)},
                "timeout": REQUEST_TIMEOUT,
                "verify": False,
            }
            proxy = self._get_proxy()
            if proxy:
                kwargs["proxies"] = {"http": proxy, "https": proxy}
            try:
                resp = requests.post(self.BASE_URL, **kwargs)
                if resp.status_code in [429, 500, 502, 503, 504] and attempt < 3:
                    time.sleep(2)
                    continue
                resp.raise_for_status()
                return self._parse_response(resp)
            except Exception as exc:
                last_exc = exc
                if attempt < 3:
                    time.sleep(2)
                    continue
        raise RuntimeError(str(last_exc) if last_exc else "请求失败")

    def legacy_key(self):
        return hashlib.md5(self.auth_key.encode()).hexdigest()[:10]

    def query_member_info(self):
        if not self.auth_key:
            raise RuntimeError("AuthKey为空")
        data = self.call("MemberService.GetMyMemberInfo", "")
        if data.get("Return") != 0:
            raise RuntimeError(f"AuthKey无效或已过期: {data.get('Return')}")
        info = data.get("Result") or {}
        if not isinstance(info, dict):
            info = {}
        self.member_info = info
        self.member_id = str(info.get("ID") or self.legacy_key())
        self.nickname = str(info.get("RealName") or info.get("NickName") or f"伊利QQ星_{mask_account(self.member_id)}")
        return info

    def get_points_balance(self):
        try:
            data = self.call("PointsService.GetPointsBalance", "")
            if data.get("Return") == 0 and isinstance(data.get("Result"), dict):
                return data.get("Result") or {}
        except:
            pass
        return {}

    def get_info(self):
        """返回: (网络请求是否成功, Token是否有效, 查询数值, 提示信息)"""
        try:
            info = self.query_member_info()
            points_info = self.get_points_balance()
            points = points_info.get("Points", info.get("PointsBalance", 0))
            try:
                points_num = int(float(points or 0))
            except:
                points_num = 0
            msg = (
                f"✅ AuthKey有效\n"
                f"👤 昵称: {self.nickname}\n"
                f"🏅 等级: {info.get('MemberLevelName') or '未知'}\n"
                f"💰 积分: {points}"
            )
            return True, True, points_num, msg
        except Exception as e:
            text = str(e)
            if "AuthKey无效" in text or "-10" in text:
                return True, False, 0, text
            return False, True, 0, text

    def verify_ck(self):
        net_ok, is_valid, _, _ = self.get_info()
        return False if net_ok and not is_valid else True

    def check_info(self):
        info = self.query_member_info()
        acc_key = str(info.get("ID") or self.legacy_key())
        nickname = self.nickname or f"伊利QQ星_{mask_account(acc_key)}"
        return {
            'nickname': nickname,
            'phone': acc_key,
            'acc_key': acc_key,
            'acc_type': 'member_id',
            'aliases': [self.legacy_key()],
            'legacy_key': self.legacy_key(),
            'final_token': self.auth_key,
        }

CastClient = YiLiQQStarClient

class RemarkManager:
    @staticmethod
    def get_account_remark(user_id, account_id):
        try:
            remark_data = sg.bucketGet(bucket=plugin_bucket('remarks'), key=f'{user_id}_{account_id}')
            return str(remark_data) if remark_data else ""
        except: return ""

    @staticmethod
    def set_account_remark(user_id, account_id, remark):
        try:
            remark_clean = str(remark).strip()[:20]
            if remark_clean:
                sg.bucketSet(bucket=plugin_bucket('remarks'), key=f'{user_id}_{account_id}', value=remark_clean)
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
            sg.bucketDel(bucket=plugin_bucket('remarks'), key=f'{user_id}_{account_id}')
            return True
        except: return False

class AccountManager:
    @staticmethod
    def get_accounts(user_id):
        try:
            value = sg.bucketGet(bucket=plugin_bucket('user'), key=str(user_id))
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
                sg.bucketSet(bucket=plugin_bucket('user'), key=str(user_id), value=str(accounts))
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
                    sg.bucketSet(bucket=plugin_bucket('user'), key=str(user_id), value=str(accounts))
                else:
                    sg.bucketDel(bucket=plugin_bucket('user'), key=str(user_id))
                return True
            return False
        except: return False

    @staticmethod
    def update_account_token(account, token):
        try:
            encrypted_token = encrypt_token(str(token))
            sg.bucketSet(bucket=plugin_bucket('token'), key=str(account), value=encrypted_token)
            return True
        except: return False

    @staticmethod
    def get_token(account):
        try:
            enc = sg.bucketGet(bucket=plugin_bucket('token'), key=str(account))
            return decrypt_token(enc) if enc else None
        except: return None

    @staticmethod
    def get_all_users():
        try:
            users = sg.bucketAllKeys(bucket=plugin_bucket('user'))
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
                pass
            old_bind_date = sg.bucketGet(bucket=plugin_bucket('bind_date'), key=old_account)
            if old_bind_date and not sg.bucketGet(bucket=plugin_bucket('bind_date'), key=new_account):
                sg.bucketSet(bucket=plugin_bucket('bind_date'), key=new_account, value=old_bind_date)

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
            sg.bucketSet(bucket=plugin_bucket('user'), key=str(user_id), value=str(new_accounts))

            AccountManager.update_account_token(new_account, new_token)
            try: sg.bucketDel(bucket=plugin_bucket('token'), key=old_account)
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

                old_client = CastClient(old_token)
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

            safe_phone = phone[:3] + "****" + phone[-3:] if len(phone) > 6 else phone
            remarks_parts = [f'伊利QQ星:{safe_phone}']
            if auth_time: remarks_parts.append(f'到期:{auth_time}')
            else: remarks_parts.append('到期:未授权')
            if remark: remarks_parts.append(f'备注:{remark}')

            owner_user = get_owner_user_id(phone, owner_user_id)
            if not owner_user:
                raise Exception("无法确认账号真实归属，已阻止写入面板备注，避免青龙数据错乱")
            remarks_parts.extend([f'用户:{owner_user}', f'ID:{phone}', '伊利QQ星提交'])
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
                if not full_token or len(full_token) < 10:
                    raise Exception("凭证异常或为空")

                client = CastClient(full_token)
                client.check_info()
                nickname = account_display

                net_ok, is_valid, total_profit, msg = client.get_info()
                if net_ok and not is_valid:
                    status_text = f"⚠️ 账号登录失败: {msg}"
                elif not net_ok:
                    status_text = f"⚠️ 网络查询异常: {str(msg)[:50]}"
                else:
                    status_text = msg

                account_info = f"""
=====伊利QQ星详情=====
🚀 平台: 伊利QQ星
👤 账号: {nickname}
{status_text}
⏰ 授权到期: {auth_time}"""
                return account_info.strip()
            except Exception as e:
                return f"""
=====伊利QQ星查询异常=====
📱 账号: {account_display}
❌ 错误: {str(e)[:50]}
=================="""
        else:
            return f"""
=====伊利QQ星状态=====
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

        menu = "=====伊利QQ星查询====="
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
        response = normalize_listen_text(response)
        if response.lower() in ['q', 'quit', 'exit', '退出', 'cancel', '取消']: return 'q'
        return response
    except: return None

def normalize_listen_text(response):
    if response is None:
        return ""
    if isinstance(response, str):
        return response.strip()
    if isinstance(response, dict):
        for key in ("message", "text", "content", "msg"):
            value = response.get(key)
            if value:
                return str(value).strip()
    return str(response).strip()

def is_cancel_input(response):
    return normalize_listen_text(response).lower() in ['q', 'quit', 'exit', '退出', 'cancel', '取消']

def reply_cancelled(text="✅ 已退出"):
    try:
        sender.reply(text)
    except Exception:
        pass

def wait_epay_order(out_trade_no, timeout_seconds=180):
    return True

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

def build_account_selection_preview(accounts, account_remarks=None, limit=20):
    account_remarks = account_remarks or {}
    lines = []
    for i, account in enumerate(accounts[:limit], 1):
        account = str(account)
        lines.append(f"[{i}] {get_account_display(account, account_remarks.get(account, ''))}")
    if len(accounts) > limit:
        lines.append(f"...等 {len(accounts)} 个账号")
    return "\n".join(lines)

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
=====伊利QQ星 登录=====
------------------
👉 请直接发送账号配置，格式如下(一行一个)支持批量登录：
AuthKey
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
                parts = [p.strip() for p in line_val.split('#') if p.strip()]
                line_remark = remark

                if len(parts) >= 2:
                    auth_candidates = [p for p in parts if re.search(r'[0-9a-fA-F-]{32,64}', p)]
                    if auth_candidates:
                        final_token_str = auth_candidates[-1]
                        remark_candidates = [p for p in parts if p != final_token_str]
                        if remark_candidates:
                            line_remark = remark_candidates[0][:20]
                    else:
                        final_token_str = parts[-1]
                        line_remark = parts[0][:20] if parts[0] != final_token_str else line_remark
                elif len(parts) == 1:
                    final_token_str = parts[0]
                else:
                    bind_stats["fail"] += 1
                    fail_msgs.append("格式错误: 需提供AuthKey")
                    if len(token_lines) == 1:
                        sender.reply("❌ 格式错误: 请提供 AuthKey、AuthKey#备注 或 备注#AuthKey。")
                    continue

                client = CastClient(final_token_str)
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
            sender.reply(f"""=====伊利QQ星登录汇总=====
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
            next_step = f'发送 {config["randommanagecommand"]} 进行授权'

        if config['enable_remark'] and not remark:
            remark = RemarkManager.get_account_remark(userid, account)

        remark_info = f"\n📝 备注: {remark}" if remark else ""
        account_display = get_account_display(account, remark)

        is_new = AccountManager.add_account(userid, account)
        action = "new" if is_new else "update"
        if is_new:
            try: sg.bucketSet(bucket=plugin_bucket('bind_date'), key=account, value=str(datetime.now().date()))
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
=====伊利QQ星账号更新=====
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
    account_list = "======我的伊利QQ星账号====="
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
    preview = build_account_selection_preview(all_accounts, account_remarks)
    sender.reply(f"""=====选择授权账号=====
请输入要授权的账号序号
------------------
{preview}
------------------
{selection_tip('授权')}
==================""")
    sel = get_user_input()
    if not sel:
        return
    if sel.lower() == 'q':
        reply_cancelled()
        return

    selected_idxs, invalid_parts = parse_index_selection(sel, len(all_accounts), allow_all=True)
    selected_accs = pick_accounts_by_indexes(all_accounts, selected_idxs)
    if selected_accs:
        if invalid_parts:
            sender.reply(f"⚠️ 已忽略无效内容: {','.join(invalid_parts[:5])}")
        batch_auth_selected(selected_accs, account_remarks)
    else:
        sender.reply("❌ 无效的序号，请回复如 1,2 或 3-6")

def batch_delete_flow(all_accounts):
    account_remarks = RemarkManager.get_all_remarks(userid) if config['enable_remark'] else {}
    preview = build_account_selection_preview(all_accounts, account_remarks)
    sender.reply(f"""=====选择删除账号=====
请输入要删除的账号序号
------------------
{preview}
------------------
{selection_tip('删除')}
==================""")
    sel = get_user_input()
    if not sel:
        return
    if sel.lower() == 'q':
        reply_cancelled()
        return

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
        if not choice:
            return
        if choice == 'q':
            reply_cancelled()
            return

        if choice == '1':
            sender.reply("请输入授权月数(如:1)，Q退出")
            months_str = get_user_input()
            if not months_str:
                return
            if months_str == 'q':
                reply_cancelled()
                return
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
                        try: sg.bucketDel(bucket=plugin_bucket('remind_log'), key=remind_key)
                        except: pass

                    if token:
                        sys_api.sync_env(token, account, remark, new_auth_time)
                        sender.reply("🔄 授权成功并同步到系统！")
                    else:
                        sender.reply("✅ 授权成功")

                    money = Decimal(months) * config['yiliqqxVipmoney']
                    sender.reply(f"=====订单完成=====\n💰 金额: {money}元\n📅 到期: {new_auth_time}")
                except Exception as ex:
                    sender.reply(f"❌ 授权后续写入异常: {ex}")

        elif choice == '2':
            sender.reply("确认删除回复【y】，回复 q 取消")
            delete_confirm = get_user_input()
            if delete_confirm == 'q':
                reply_cancelled("✅ 已取消删除")
                return
            if delete_confirm == 'y':
                try:
                    AccountManager.remove_account(userid, account)
                    try: sg.bucketDel(bucket=plugin_bucket('token'), key=account)
                    except: pass
                    try:
                        pass
                    except: pass
                    if config['enable_remark']: RemarkManager.delete_account_remark(userid, account)
                    sys_api.delete_env(account, token)
                    today_date = datetime.now().date()
                    for d in range(config['reminder_days'] + 1):
                        remind_key = f"{userid}_{account}_{today_date - timedelta(days=d)}"
                        try: sg.bucketDel(bucket=plugin_bucket('remind_log'), key=remind_key)
                        except: pass
                    sender.reply("✅ 删除成功")
                except Exception as ex:
                    sender.reply(f"❌ 删除异常: {ex}")

        elif choice == '3':
             sender.reply("请输入新备注:")
             new_remark = get_user_input()
             if new_remark == 'q':
                 reply_cancelled()
                 return
             if new_remark:
                 RemarkManager.set_account_remark(userid, account, new_remark)
                 if token and accountVip and accountVip >= today_time:
                     sys_api.sync_env(token, account, new_remark, accountVip)
                     sender.reply("✅ 备注更新成功并同步到系统")
                 else:
                     sender.reply("✅ 备注更新成功（未授权/已过期账号不同步系统）")

    except Exception as e:
        sender.reply(f"操作失败: {e}")

def process_payment(months, accountVip, token, account, remark=""):
    return True
def batch_auth_selected(accounts, account_remarks):
    sender.reply(f"已选择 {len(accounts)} 个账号\n请输入授权月数，Q退出")
    m = get_user_input()
    if not m:
        return
    if m == 'q':
        reply_cancelled()
        return
    if not m.isdigit(): return
    months = int(m)
    if months <= 0: return

    count = len(accounts)
    total_money = Decimal(months) * config['yiliqqxVipmoney'] * count
    total_points = config['yiliqqxcoin'] * months * count
    user_points, points_bucket = get_user_points()

    options = []
    idx = 1

    if config['yiliqqxcoin'] > 0:
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

    if config['enable_wechat_qr'] and config['wechat_qr']:
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
    if not sel:
        return
    if sel == 'q':
        reply_cancelled()
        return

    try:
        choice = int(sel)
        opt = next((o for o in options if o['id'] == choice), None)
        if not opt: raise ValueError

        if opt['type'] == 'epay':
            out_trade_no = f"yiliqqx_BATCH_{int(time.time())}_{userid}_{random.randint(1000,9999)}"
            formatted_money = f"{float(opt['amount']):.2f}"
            channel_name = "支付宝" if opt['channel'] == 'alipay' else ("微信支付" if opt['channel'] == 'wxpay' else "QQ钱包")

            qr_image_url, _ = _create_epay_qr(out_trade_no, opt['channel'], f"Batch_{count}_{months}M", formatted_money)

            sender.reply(f"=====等待支付=====\n💰 金额: {formatted_money}元\n💳 方式: {channel_name}\n📋 订单: {out_trade_no}\n------------------\n请在 180 秒内完成扫在线处理 (完成后自动批量授权)\n回复\"q\"取消支付")
            sender.replyImage(qr_image_url)

            pay_status = wait_epay_order(out_trade_no, timeout_seconds=180)
            if pay_status == "cancelled":
                sender.reply("✅ 已取消支付")
                return
            if pay_status != "paid":
                sender.reply("❌ 支付超时，请重新发起。")
                return

        elif opt['type'] == 'wx':
            if False:
                sender.reply("⚠️ 当前有人支付中")
                return

            out_trade_no = f"WX_{int(time.time())}_{random.randint(100,999)}"
            sender.reply(f"=====等待支付=====\n💰 金额: {opt['amount']}元\n💳 方式: 个人微信收款\n📋 订单: {out_trade_no}\n------------------\n请在 60 秒内完成扫在线处理 (完成后自动授权)\n回复\"q\"取消支付")
            sender.replyImage(config['wechat_qr'])
            res = False
            if is_cancel_input(res):
                reply_cancelled("✅ 已取消支付")
                return

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
            points_confirm = get_user_input()
            if points_confirm == 'q':
                reply_cancelled("✅ 已取消支付")
                return
            if points_confirm != 'y': return
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
                try: sg.bucketDel(bucket=plugin_bucket('remind_log'), key=remind_key)
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
    delete_confirm = get_user_input()
    if delete_confirm == 'q':
        reply_cancelled("✅ 已取消删除")
        return
    if delete_confirm == "确认删除":
        today_date = datetime.now().date()
        for account in accounts:
            try:
                 account = str(account)
                 AccountManager.remove_account(userid, account)
                 token = AccountManager.get_token(account)
                 try: sg.bucketDel(bucket=plugin_bucket('token'), key=account)
                 except: pass
                 try:
                     pass
                 except: pass
                 if config['enable_remark']: RemarkManager.delete_account_remark(userid, account)
                 sys_api.delete_env(account, token)
                 for d in range(config['reminder_days'] + 1):
                     remind_key = f"{userid}_{account}_{today_date - timedelta(days=d)}"
                     try: sg.bucketDel(bucket=plugin_bucket('remind_log'), key=remind_key)
                     except: pass
            except: pass
        sender.reply("✅ 批量删除完成")

def clean_expired_accounts(force_report=False):
    panel_sync = sync_local_auth_from_panel()
    users = sg.bucketAllKeys(bucket=plugin_bucket('user'))
    if not users:
        if sender.isAdmin() and (force_report or usermessage in ['伊利清理', '清理伊利', '伊利QQ星清理', '清理伊利QQ星']):
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

    if sender.isAdmin() and (force_report or usermessage in ['伊利清理', '清理伊利', '伊利QQ星清理', '清理伊利QQ星']):
        sender.reply(f"=====开始执行维护=====\n📊 扫描用户数: {len(users)}\n🔄 面板回写: {panel_sync['synced']}个账号\n⚙️ 提醒天数: {config['reminder_days']}天\n⏳ 处理中...")

    scanned_accounts = 0
    cleaned_count = 0
    reminded_count = 0
    ck_expired_count = 0
    today_date = datetime.now().date()
    reminder_days_cfg = config['reminder_days']
    grace_days_cfg = max(int(reminder_days_cfg or 0), 0)
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
                    bind_date_raw = sg.bucketGet(bucket=plugin_bucket('bind_date'), key=account)
                    try:
                        bind_date = datetime.strptime(str(bind_date_raw), "%Y-%m-%d").date()
                    except:
                        bind_date = today_date
                        try: sg.bucketSet(bucket=plugin_bucket('bind_date'), key=account, value=str(bind_date))
                        except: pass
                    days_diff = (bind_date - today_date).days
                    account_contexts.append({
                        "account": account,
                        "accountVip": accountVip,
                        "days_diff": days_diff,
                        "expiration_str": str(bind_date),
                        "full_token": AccountManager.get_token(account) or "",
                        "status": "unauthorized",
                        "bind_date": str(bind_date),
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
                    "status": "authorized",
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
                    full_token = account_item.get("full_token") or AccountManager.get_token(account) or ""
                    bind_date = account_item.get("bind_date") or expiration_str or str(today_date)
                    grace_elapsed_days = abs(days_diff or 0)
                    if grace_elapsed_days < grace_days_cfg:
                        valid_accounts.append(account)
                        remind_key = f"{user}_{account}_{today_date}_unauth"
                        has_reminded = sg.bucketGet(bucket=plugin_bucket('remind_log'), key=remind_key)
                        if not has_reminded:
                            account_display = get_account_display(account, account_remarks.get(account, ""))
                            remind_day = min(grace_elapsed_days + 1, grace_days_cfg)
                            msg = f"""=====⏰ 未授权提醒=====
您的伊利QQ星账号尚未授权。
📱 账号: {account_display}
📅 提交: {bind_date}
⏳ 提醒进度: 第 {remind_day}/{grace_days_cfg} 天
------------------
请及时发送 {config['randommanagecommand']} 完成授权，逾期将自动清理。
=================="""
                            if safe_send_message(user, msg, f"未授权提醒 {user}-{account}"):
                                try: sg.bucketSet(bucket=plugin_bucket('remind_log'), key=remind_key, value="1")
                                except: pass
                                reminded_count += 1
                        continue

                    try:
                        sys_api.delete_env(account, full_token)
                        try: sg.bucketDel(bucket=plugin_bucket('token'), key=account)
                        except: pass
                        try:
                            pass
                        except: pass
                        try: sg.bucketDel(bucket=plugin_bucket('bind_date'), key=account)
                        except: pass
                        if config['enable_remark']:
                            RemarkManager.delete_account_remark(user, account)
                    except: pass

                    account_display = get_account_display(account, account_remarks.get(account, ""))
                    clean_msg = f"""=====🗑️ 未授权清理通知=====
您的伊利QQ星账号已连续 {grace_days_cfg} 天未授权，已自动清理。
📱 账号: {account_display}
📅 提交: {bind_date}
------------------
如需继续使用，请重新登录并授权。
=================="""
                    safe_send_message(user, clean_msg, f"未授权清理通知 {user}-{account}")
                    cleaned_count += 1
                    user_has_change = True
                    continue

                if days_diff >= 0:
                    valid_accounts.append(account)

                    full_token = account_item["full_token"]
                    ck_state = ck_verify_result.get((str(user), str(account)), {"valid": True})
                    is_ck_valid = bool(ck_state.get("valid", True))

                    if not is_ck_valid:
                        remind_key = f"{user}_{account}_{today_date}_ck_invalid"
                        has_reminded = sg.bucketGet(bucket=plugin_bucket('remind_log'), key=remind_key)
                        if not has_reminded:
                            account_display = get_account_display(account, account_remarks.get(account, ""))
                            reason = str(ck_state.get("msg") or "AuthKey无效或已过期")
                            msg = f"""=====⚠️ CK失效提醒=====
您的伊利QQ星账号 AuthKey 已失效。
📱 账号: {account_display}
📅 授权到期: {expiration_str}
🧾 原因: {reason[:80]}
------------------
请发送 {config['randomsigncommand']} 重新提交新的 AuthKey。
=================="""
                            if safe_send_message(user, msg, f"CK失效提醒 {user}-{account}"):
                                try: sg.bucketSet(bucket=plugin_bucket('remind_log'), key=remind_key, value="1")
                                except: pass
                                ck_expired_count += 1
                        continue

                    if is_ck_valid and 0 <= days_diff <= reminder_days_cfg:
                        remind_key = f"{user}_{account}_{today_date}"
                        has_reminded = sg.bucketGet(bucket=plugin_bucket('remind_log'), key=remind_key)

                        if not has_reminded:
                            account_display = get_account_display(account, account_remarks.get(account, ""))
                            msg = f"""=====⏰ 到期提醒=====
您的伊利QQ星账号授权即将到期！
📱 账号: {account_display}
📅 到期: {expiration_str} (剩余 {days_diff} 天)
------------------
为避免影响挂机，请及时续费。
发送 {config['randommanagecommand']} 进行续费
=================="""
                            if safe_send_message(user, msg, f"到期提醒 {user}-{account}"):
                                try: sg.bucketSet(bucket=plugin_bucket('remind_log'), key=remind_key, value="1")
                                except: pass
                                reminded_count += 1
                    continue

                if days_diff < 0:
                    overdue_days = abs(days_diff)
                    grace_elapsed_days = max(overdue_days - 1, 0)
                    if grace_elapsed_days < grace_days_cfg:
                        valid_accounts.append(account)
                        remind_key = f"{user}_{account}_{today_date}_expired"
                        has_reminded = sg.bucketGet(bucket=plugin_bucket('remind_log'), key=remind_key)
                        if not has_reminded:
                            account_display = get_account_display(account, account_remarks.get(account, ""))
                            remind_day = min(grace_elapsed_days + 1, grace_days_cfg)
                            msg = f"""=====⏰ 过期提醒=====
您的伊利QQ星账号授权已过期。
📱 账号: {account_display}
📅 到期: {expiration_str}
⏳ 提醒进度: 第 {remind_day}/{grace_days_cfg} 天
------------------
请及时发送 {config['randommanagecommand']} 续费，逾期将自动清理。
=================="""
                            if safe_send_message(user, msg, f"过期提醒 {user}-{account}"):
                                try: sg.bucketSet(bucket=plugin_bucket('remind_log'), key=remind_key, value="1")
                                except: pass
                                reminded_count += 1
                        continue

                    try:
                        sys_api.delete_env(account, account_item.get("full_token"))
                        try: sg.bucketDel(bucket=plugin_bucket('token'), key=account)
                        except: pass
                        try:
                            pass
                        except: pass
                        try: sg.bucketDel(bucket=plugin_bucket('bind_date'), key=account)
                        except: pass
                        if config['enable_remark']:
                            RemarkManager.delete_account_remark(user, account)
                    except: pass

                    account_display = get_account_display(account, account_remarks.get(account, ""))
                    clean_msg = f"""=====🗑️ 过期清理通知=====
您的伊利QQ星账号授权过期后已连续提醒 {grace_days_cfg} 天，现已清理。
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
                    try: sg.bucketSet(bucket=plugin_bucket('user'), key=str(user), value=str(valid_accounts))
                    except: pass
                else:
                    try: sg.bucketDel(bucket=plugin_bucket('user'), key=str(user))
                    except: pass

        except Exception:
            continue

    if sender.isAdmin() and (force_report or usermessage in ['伊利清理', '清理伊利', '伊利QQ星清理', '清理伊利QQ星']):
        sender.reply(
            f"=====伊利QQ星维护完成=====\n"
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
    sender.reply(f"""=====伊利QQ星数据总览=====
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
    if not keyword:
        return
    if keyword.lower() == 'q':
        reply_cancelled()
        return
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
    if not choice:
        return
    if choice.lower() == 'q':
        reply_cancelled()
        return

    users = []
    if choice == '1':
        users = AccountManager.get_all_users()
        total_accounts = sum(len(AccountManager.get_accounts(u)) for u in users)
        if len(users) <= 1 and total_accounts > 5:
            sender.reply(
                "⚠️ 已拦截同步所有授权账号。\n"
                f"当前本地归属表异常：用户数 {len(users)}，账号数 {total_accounts}。\n"
                "这通常表示账号被集中到了管理员名下，继续同步会覆盖面板归属备注。\n"
                f"请先恢复 {plugin_bucket('user')} 归属表，或使用 [2] 同步指定用户账号。"
            )
            return
        sender.reply(f"⚠️ 即将同步所有授权账号。\n确认请回复【确认同步】")
        if get_user_input() != "确认同步":
            sender.reply("✅ 已取消同步")
            return
    elif choice == '2':
        sender.reply("请输入用户ID(QQ号或wxid)，回复q退出")
        target_user = get_user_input()
        if not target_user:
            return
        if target_user.lower() == 'q':
            reply_cancelled()
            return
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
=====伊利QQ星管理插件教程=====
当前模式: 🌐 提交至{panel_name}面板

1️⃣ {config['randomsigncommand']}
   发送伊利QQ星配置自动覆盖更新。

2️⃣ {config['randomquerycommand']}
   查询AuthKey存活状态、会员等级和当前积分(支持1,2多选)。

3️⃣ {config['randommanagecommand']}
   全新支付接口，极简扫码无需挂机，付完全自动回调开通。

4️⃣ 伊利QQ星授权
   管理员总管理：授权、总览、配置预览、反查、同步、清理。

5️⃣ 伊利清理 / 伊利广播
   自动维护与消息分发。
==================""")

try:
    command = usermessage.strip()
    command = command.replace('伊利qq星', '伊利QQ星').replace('伊利Qq星', '伊利QQ星').replace('伊利qQ星', '伊利QQ星')

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

    elif re.match(r'^(伊利|伊利QQ星)(通知|广播)\s*', command):
        notify_authorized_users()
    elif command in ['伊利登录', '伊利登陆', '登录伊利', '登陆伊利', '伊利QQ星登录', '伊利QQ星登陆', '登录伊利QQ星', '登陆伊利QQ星']:
        bindaccount()
    elif command in ['伊利管理', '管理伊利', '伊利QQ星管理', '管理伊利QQ星']:
       xy_manage()
    elif command in ['伊利查询', '查询伊利', '伊利QQ星查询', '查询伊利QQ星']:
        cxs()
    elif command in ['伊利清理', '清理伊利', '伊利QQ星清理', '清理伊利QQ星']:
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
    elif command in ['伊利授权', '伊利QQ星授权']:
        admin_auth_options()
    elif command in ['伊利教程', '伊利QQ星教程']:
        show_tutorial()

except Exception as e:
    logger.error(f"Error: {e}")
    sender.reply(f"❌ 系统错误: {e}")
