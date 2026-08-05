# [title: 牛牛短剧小程序版]
# [name: niuNiuDuanJuXiaoChengXuBan]
# [language: python]
# [class: 任务]
# [author: 8165799]
# [version: v1.4.0]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(小牛牛)(登录|登陆)$|^登(录|陆)(小牛牛)$|^(小牛牛)(查询|管理)$|^(查询|管理)(小牛牛)$|^小牛牛清理$|^小牛牛$|^小牛牛教程$|^小牛牛通知 ?(.*)$|^清理小牛牛$|^小牛牛广播 ?(.*)$]
# [cron: 5 10 5 * *]
# [icon: https://api.iconify.design/lucide:bot.svg]
# [description: 小牛牛提交计费版；2. 支持批量登录，仅需token即可登录；3.]
# [depe: ["requests"]]
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
    'dd_xnn_panel_type': form.string().title('对接面板类型').default('').description('qinglong=青龙面板 daidai=呆呆面板'),
    'dd_xnn_dd_xnn_qlname': form.string().title('对接系统配置').default('').description('青龙:URL丨ID丨Secret 呆呆:URL丨Key丨Secret'),
    'dd_xnn_dd_xnn_osname': form.string().title('系统变量名').default('').description('系统容器内变量名(默认为niuniuTOKENS)'),
    'dd_xnn_enable_proxy': form.boolean().title('是否启用代理').default(False).description('是否启用代理功能'),
    'dd_xnn_proxy_pool_url': form.string().title('代理池地址').default('').description('代理API服务地址'),
    'dd_xnn_enable_remark': form.boolean().title('启用备注功能').default(False).description('是否启用账号备注功能'),
})
_CONFIG_FIELD_MAP = {
    ('dd_xnn', 'panel_type'): 'dd_xnn_panel_type',
    ('dd_xnn', 'dd_xnn_qlname'): 'dd_xnn_dd_xnn_qlname',
    ('dd_xnn', 'dd_xnn_osname'): 'dd_xnn_dd_xnn_osname',
    ('dd_xnn', 'enable_proxy'): 'dd_xnn_enable_proxy',
    ('dd_xnn', 'proxy_pool_url'): 'dd_xnn_proxy_pool_url',
    ('dd_xnn', 'enable_remark'): 'dd_xnn_enable_remark',
}

import re
import ast
from datetime import datetime, timedelta
from urllib.parse import unquote
from decimal import Decimal
import requests
import time
import hashlib
import logging
import base64
import warnings
import random
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed

warnings.filterwarnings('ignore', message='Unverified HTTPS request')
requests.packages.urllib3.disable_warnings()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('xnn_plugin')

REQUEST_TIMEOUT = 30
MAINTENANCE_CK_MAX_WORKERS = 8

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = str(sender.getUserID())
usermessage = sender.getMessage()

_RUNTIME_BUCKET = "plugin_push_runtime"
_RUNTIME_KEY = "牛牛短剧小程序版"
try:
    current_imtype = str(sender.getImtype() or "")
except:
    current_imtype = ""
if current_imtype and current_imtype.lower() not in ["fake", "cron"]:
    try: sg.bucketSet(_RUNTIME_BUCKET, _RUNTIME_KEY + "_sender", str(senderID))
    except: pass
    try: sg.bucketSet(_RUNTIME_BUCKET, _RUNTIME_KEY + "_imtype", current_imtype)
    except: pass
    if userid and userid.lower() not in ["none", "null"]:
        try: sg.bucketSet(bucket="dd_xnn_sender", key=userid, value=str(senderID))
        except: pass
        try: sg.bucketSet(bucket="dd_xnn_imtype", key=userid, value=current_imtype)
        except: pass


def getusercontent():
    panel_type = sg.bucketGet('dd_xnn', 'panel_type') or 'qinglong'
    panel_type = panel_type.lower()

    dd_hhtt_qlname = sg.bucketGet('dd_xnn', 'dd_xnn_qlname') or ''
    dd_hhtt_osname = sg.bucketGet('dd_xnn', 'dd_xnn_osname') or 'niuniuTOKENS'

    if not dd_hhtt_qlname:
        sender.reply("❌ 配置错误：请在插件配置中填写【对接系统配置】(面板信息)。")
        exit(0)

    dd_managecommand = sg.bucketGet('dd_xnn', 'dd_managecommand') or '小牛牛管理'
    dd_querycommand = sg.bucketGet('dd_xnn', 'dd_querycommand') or '小牛牛查询'
    dd_signcommand = sg.bucketGet('dd_xnn', 'dd_signcommand') or '小牛牛登录'
    zsm = sg.bucketGet('dd_xnn', 'zsm') or ''

    enable_proxy = sg.bucketGet('dd_xnn', 'enable_proxy') or 'false'
    enable_proxy = enable_proxy.lower() == 'true'
    proxy_pool_url = sg.bucketGet('dd_xnn', 'proxy_pool_url') or ''

    points_bucket = sg.bucketGet('dd_xnn', 'points_bucket') or 'dd_sign_points'

    enable_remark = sg.bucketGet('dd_xnn', 'enable_remark') or 'false'
    enable_remark = enable_remark.lower() == 'true'

    randommanagecommand = dd_managecommand
    randomquerycommand = dd_querycommand
    randomsigncommand = dd_signcommand

    xyVipmoney = Decimal(sg.bucketGet('dd_xnn', 'hhttVipmoney') or '0')
    xycoin = int(sg.bucketGet('dd_xnn', 'hhttcoin') or '0')

    show_point_status = sg.bucketGet('dd_xnn', 'show_point_status') or 'false'
    show_point_status = show_point_status.lower() == 'true'

    use_ma_pay = '2099-12-31' or 'false'
    use_ma_pay = use_ma_pay.lower() == 'true'

    epay_url = '2099-12-31' or ''
    epay_pid = '2099-12-31' or ''
    epay_key = '2099-12-31' or ''
    epay_alipay = ('2099-12-31' or 'true').lower() == 'true'
    epay_wxpay = ('2099-12-31' or 'false').lower() == 'true'
    epay_qqpay = ('2099-12-31' or 'false').lower() == 'true'

    reminder_days = int(sg.bucketGet('dd_xnn', 'reminder_days') or '2')

    return {
        'panel_type': panel_type,
        'dd_hhtt_osname': dd_hhtt_osname,
        'dd_hhtt_qlname': dd_hhtt_qlname,
        'dd_managecommand': dd_managecommand,
        'dd_querycommand': dd_querycommand,
        'dd_signcommand': dd_signcommand,
        'randommanagecommand': randommanagecommand,
        'randomquerycommand': randomquerycommand,
        'randomsigncommand': randomsigncommand,
        'zsm': zsm,
        'enable_proxy': enable_proxy,
        'proxy_pool_url': proxy_pool_url,
        'points_bucket': points_bucket,
        'enable_remark': enable_remark,
        'xyVipmoney': xyVipmoney,
        'xycoin': xycoin,
        'show_point_status': show_point_status,
        'use_ma_pay': use_ma_pay,
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
        for owner in sg.bucketAllKeys(bucket='dd_xnn_user'):
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
    return

def send_user_notice(user_id, msg, title="牛牛短剧小程序版通知", preferred_imtypes=None):
    user_id = str(user_id or "").strip()
    if not user_id:
        return False

    imtype_candidates = []
    for item in preferred_imtypes or []:
        item = str(item or "").strip()
        if item:
            imtype_candidates.append(item)
    try:
        imtype_candidates.append(str(sg.bucketGet(bucket="dd_xnn_imtype", key=user_id) or ""))
    except:
        pass
    try:
        imtype_candidates.append(str(sender.getImtype() or ""))
    except:
        pass
    try:
        imtype_candidates.append(str(sg.bucketGet(_RUNTIME_BUCKET, _RUNTIME_KEY + "_imtype") or ""))
    except:
        pass
    if user_id.isdigit():
        imtype_candidates.extend(["qq", "qb"])

    last_error = ""
    valid_imtypes = [x for x in imtype_candidates if x and x.lower() not in ["fake", "cron"]]
    for imtype in list(dict.fromkeys(valid_imtypes)):
        for func_name in ["Push", "push"]:
            push_func = getattr(sg, func_name, None)
            if not callable(push_func):
                continue
            try:
                push_func(imtype, "", user_id, title, msg)
                try: sg.bucketSet(_RUNTIME_BUCKET, _RUNTIME_KEY + "_imtype", imtype)
                except: pass
                return True
            except Exception as e:
                last_error = f"{func_name}({imtype},{user_id}): {str(e) or e.__class__.__name__}"
                logger.warning(f"Push发送失败 {user_id}: {last_error}")

    targets = []
    try:
        saved_sender = sg.bucketGet(bucket="dd_xnn_sender", key=user_id)
        if saved_sender:
            targets.append(str(saved_sender))
    except:
        pass
    try:
        runtime_sender = sg.bucketGet(_RUNTIME_BUCKET, _RUNTIME_KEY + "_sender")
        if runtime_sender:
            targets.append(str(runtime_sender))
    except:
        pass
    targets.append(user_id)

    method_names = ["Reply", "reply", "ReplyMarkdown", "replyMarkdown", "send", "replyText", "sendText", "sendMsg", "sendMessage"]
    for target in list(dict.fromkeys([x for x in targets if x])):
        try:
            target_sender = sg.Sender(target)
        except Exception as e:
            last_error = f"Sender({target})初始化失败: {str(e) or e.__class__.__name__}"
            continue
        for method_name in method_names:
            method = getattr(target_sender, method_name, None)
            if not callable(method):
                continue
            try:
                method(msg)
                return True
            except Exception as e:
                last_error = f"{method_name}: {str(e) or e.__class__.__name__}"

    if last_error:
        logger.warning(f"消息发送失败 {user_id}: {last_error}")
    return False

def safe_send_message(user_id, msg, log_context=""):
    ok = send_user_notice(user_id, msg)
    if not ok:
        logger.warning(f"消息发送失败 {log_context}")
    return ok

def send_message_to_framework_admins(msg):
    notify_func = getattr(sg, 'notifyMasters', None)
    if not callable(notify_func):
        return False
    for arg in [None, []]:
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
            except:
                pass
        except Exception as e:
            logger.warning(f"框架管理员推送失败: {e}")
    return False

def send_daily_admin_report(report_data, force_send=False, notify_status=False):
    report_date = str(report_data.get('report_date') or datetime.now().date())
    report_key = f"daily_admin_report_{report_date}"
    if not force_send and sg.bucketGet('dd_xnn_runtime', report_key):
        if notify_status:
            sender.reply("ℹ️ 今日管理员汇总已发送过。")
        return False

    msg = (
        "=====小牛牛维护完成=====\n"
        f"✅ 检测完成，共 {report_data.get('scanned_accounts', 0)} 个账号\n"
        f"🌐 面板变量: {report_data.get('panel_scanned_accounts', 0)} 个\n"
        f"📣 发送通知: {report_data.get('sent_notifications', 0)} 条\n"
        f"⚠️ CK失效通知: {report_data.get('ck_expired_count', 0)} 个\n"
        f"🗑️ 清理过期: {report_data.get('cleaned_count', 0)} 个\n"
        "=================="
    )

    if send_message_to_framework_admins(msg):
        try: sg.bucketSet('dd_xnn_runtime', report_key, "framework")
        except: pass
        if notify_status:
            sender.reply("✅ 管理员汇总已发送（框架自动管理员）")
        return True
    if notify_status:
        sender.reply("❌ 管理员汇总发送失败，请检查框架默认管理员配置。")
    return False

def empower(empowertime, days):
    try:
        today_date = datetime.now().date()
        if not empowertime or empowertime <= str(today_date):
            delayed_date = today_date + timedelta(days=days)
        elif empowertime > str(today_date):
            empower_date = datetime.strptime(empowertime, "%Y-%m-%d").date()
            delayed_date = empower_date + timedelta(days=days)
        return str(delayed_date)
    except Exception as e:
        logger.error(f"授权时间计算失败: {e}")
        raise Exception(f"授权时间计算失败: {e}")

def get_safe_account(account):
    acc_str = str(account)
    if len(acc_str) == 11 and acc_str.isdigit():
        return acc_str[:3] + "****" + acc_str[-4:]
    return acc_str

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

def batch_verify_account_ck(tasks, max_workers=MAINTENANCE_CK_MAX_WORKERS):
    if not tasks:
        return {}

    result_map = {}
    worker_count = min(max_workers, len(tasks))

    def _verify_one(task):
        if isinstance(task, dict):
            user = task.get('user', '')
            account = task.get('account', '')
            token = task.get('token', '')
            source = task.get('source', 'local')
        else:
            user, account, token = task
            source = 'local'
        token_hash = hashlib.md5(str(token or '').encode()).hexdigest() if token else f"{source}_{user}_{account}"
        if not token:
            return (source, user, account, token_hash, True)
        try:
            time.sleep(random.uniform(0.1, 0.35))
            client = XiaoNiuClient(token)
            return (source, user, account, token_hash, client.verify_ck())
        except Exception as e:
            logger.warning(f"CK校验异常，按有效处理: {user}-{account} - {e}")
            return (source, user, account, token_hash, True)

    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        futures = [executor.submit(_verify_one, task) for task in tasks]
        for future in as_completed(futures):
            try:
                source, user, account, token_hash, is_valid = future.result()
                result_map[(str(source), str(user), str(account), str(token_hash))] = is_valid
                result_map[(str(user), str(account))] = is_valid
            except Exception as e:
                logger.warning(f"CK校验结果读取失败: {e}")
    return result_map


def _create_epay_qr(out_trade_no, channel, project_name, money_str):
    return True

def parse_index_selection(text, total_count, allow_all=True):
    text = str(text or "").strip().lower()
    if allow_all and text == 'a':
        return list(range(1, total_count + 1)), []
    selected = []
    invalid = []
    for part in re.split(r'[,，\\s]+', text):
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            try:
                start, end = [int(x.strip()) for x in part.split('-', 1)]
                if start > end:
                    start, end = end, start
                for idx in range(start, end + 1):
                    if 1 <= idx <= total_count:
                        selected.append(idx)
                    else:
                        invalid.append(str(idx))
            except:
                invalid.append(part)
        else:
            try:
                idx = int(part)
                if 1 <= idx <= total_count:
                    selected.append(idx)
                else:
                    invalid.append(part)
            except:
                invalid.append(part)
    return list(dict.fromkeys(selected)), invalid


def parse_panel_xnn_remark(remarks):
    try:
        remarks = str(remarks or '')
        user_match = re.search(r'用户[:：]\s*([^丨|\s]+)', remarks)
        id_match = re.search(r'ID[:：]\s*([^丨|\s]+)', remarks)
        date_match = re.search(r'到期[:：]\s*(\d{4}-\d{2}-\d{2})', remarks)
        remark_match = re.search(r'备注[:：]\s*([^丨|]+)', remarks)
        return {
            'user': user_match.group(1).strip() if user_match else '',
            'account': id_match.group(1).strip() if id_match else '',
            'auth_date': date_match.group(1).strip() if date_match else '',
            'remark': remark_match.group(1).strip() if remark_match else ''
        }
    except:
        return {'user': '', 'account': '', 'auth_date': '', 'remark': ''}

def split_env_tokens(value):
    value = str(value or '').strip()
    if not value:
        return []
    tokens = [x.strip() for x in re.split(r'[\n&@]', value) if x.strip()]
    return list(dict.fromkeys(tokens))

def find_local_account_by_token(token):
    token = str(token or '').strip()
    if not token:
        return '', ''
    for owner in AccountManager.get_all_users():
        try:
            for account in AccountManager.get_accounts(owner):
                local_token = AccountManager.get_token(account)
                if local_token and str(local_token).strip() == token:
                    return str(owner), str(account)
        except:
            continue
    return '', ''

def collect_panel_ck_tasks():
    tasks = []
    if not getattr(sys_api, 'enabled', False):
        return tasks
    try:
        envs = sys_api.get_all_envs()
    except Exception as e:
        logger.warning(f"读取面板变量失败: {e}")
        return tasks

    seen = set()
    for env in envs:
        try:
            if env.get('name') != config['dd_hhtt_osname']:
                continue
            value = env.get('value') or ''
            remarks = env.get('remarks') or env.get('remark') or ''
            parsed = parse_panel_xnn_remark(remarks)
            tokens = split_env_tokens(value)
            for idx, token in enumerate(tokens, 1):
                owner = parsed.get('user') or ''
                account = parsed.get('account') or ''
                if not owner or not account:
                    local_owner, local_account = find_local_account_by_token(token)
                    owner = owner or local_owner
                    account = account or local_account
                if not account:
                    account = hashlib.md5(token.encode()).hexdigest()[:12]
                task_key = hashlib.md5(token.encode()).hexdigest()
                dedupe = (task_key, owner, account)
                if dedupe in seen:
                    continue
                seen.add(dedupe)
                tasks.append({
                    'source': 'panel',
                    'user': str(owner or ''),
                    'account': str(account),
                    'token': token,
                    'auth_date': parsed.get('auth_date') or '',
                    'remarks': remarks,
                    'env_id': env.get('id') if env.get('id') is not None else env.get('_id'),
                    'index': idx
                })
        except Exception as e:
            logger.warning(f"解析面板变量失败: {e}")
    return tasks

class XiaoNiuClient:
    def __init__(self, token_str):
        self.token = unquote(token_str.strip())
        self.base_url = "https://api.tianjinzhitongdaohe.com"

        self.headers = {
            "Host": "api.tianjinzhitongdaohe.com",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Linux; Android 12; M2012K11AC Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 MicroMessenger/8.0.40.2420(0x28002851) NetType/WIFI Language/zh_CN miniProgram/wxcb95401f250e9a53",
            "xweb_xhr": "1",
            "token": self.token,
            "Accept": "*/*",
            "Referer": "https://servicewechat.com/wxcb95401f250e9a53/19/page-frame.html",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }

    def _get_proxies(self):
        proxies = None
        if config['enable_proxy'] and config['proxy_pool_url']:
            try:
                res = requests.get(config['proxy_pool_url'], timeout=3)
                if res.status_code == 200:
                    proxy_ip = res.text.strip()
                    match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+)', proxy_ip)
                    if match:
                        proxy_ip = match.group(1)
                        proxies = {'http': f"http://{proxy_ip}", 'https': f"http://{proxy_ip}"}
            except Exception as e:
                logger.warning(f"代理获取失败: {e}")
        return proxies

    def check_info(self):
        proxies = self._get_proxies()

        user_url = f"{self.base_url}/sqx_fast/app/user/selectUserById"
        try:
            res_user = requests.get(user_url, headers=self.headers, verify=False, proxies=proxies, timeout=10)
            rj_user = res_user.json()
            if rj_user.get("code") != 0:
                raise Exception(rj_user.get("msg", "Token无效或已过期"))

            data = rj_user.get("data", {})
            phone = data.get("phone", "")
            if not phone:
                uid = str(data.get("id") or data.get("userId") or "")
                if uid:
                    phone = f"UID_{uid}"
                else:
                    phone = hashlib.md5(self.token.encode()).hexdigest()[:11]

            day_num = data.get("lookDayVideoNum")
            ok_num = data.get("okLookVideoNum")
            watched_today = 0
            if day_num is not None: watched_today = int(day_num)
            elif ok_num is not None: watched_today = int(ok_num)

        except Exception as e:
            raise Exception(f"验证失败: {str(e)}")

        gold_url = f"{self.base_url}/sqx_fast/app/integral/selectByUserId"
        gold = 0
        try:
            res_gold = requests.get(gold_url, headers=self.headers, verify=False, proxies=proxies, timeout=10)
            rj_gold = res_gold.json()
            if rj_gold.get("code") == 0:
                gold = rj_gold.get("data", {}).get("integralNum", 0)
        except:
            pass

        safe_phone = get_safe_account(phone)

        return {
            "nickname": f"小牛牛_{safe_phone}",
            "phone": phone,
            "gold": gold,
            "watched_today": watched_today,
            "acc_key": phone,
            "final_token": self.token
        }

    def verify_ck(self):
        try:
            self.check_info()
            return True
        except Exception as e:
            err = str(e)
            if any(key in err for key in ["token失效", "重新登录", "Token无效", "已过期", "无效", "失效", "验证失败"]):
                return False
            logger.warning(f"小牛牛CK校验异常，暂按有效处理: {err}")
            return True

class RemarkManager:
    @staticmethod
    def get_account_remark(user_id, account_id):
        try:
            remark_data = sg.bucketGet(bucket='dd_xnn_remarks', key=f'{user_id}_{account_id}')
            return str(remark_data) if remark_data else ""
        except: return ""

    @staticmethod
    def set_account_remark(user_id, account_id, remark):
        try:
            remark_clean = str(remark).strip()[:20]
            if remark_clean:
                sg.bucketSet(bucket='dd_xnn_remarks', key=f'{user_id}_{account_id}', value=remark_clean)
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
            sg.bucketDel(bucket='dd_xnn_remarks', key=f'{user_id}_{account_id}')
            return True
        except: return False

class AccountManager:
    @staticmethod
    def get_accounts(user_id):
        try:
            value = sg.bucketGet(bucket='dd_xnn_user', key=str(user_id))
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
                sg.bucketSet(bucket='dd_xnn_user', key=str(user_id), value=str(accounts))
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
                    sg.bucketSet(bucket='dd_xnn_user', key=str(user_id), value=str(accounts))
                else:
                    sg.bucketDel(bucket='dd_xnn_user', key=str(user_id))
                return True
            return False
        except: return False

    @staticmethod
    def update_account_token(account, token):
        try:
            encrypted_token = encrypt_token(str(token))
            sg.bucketSet(bucket='dd_xnn_token', key=str(account), value=encrypted_token)
            return True
        except: return False

    @staticmethod
    def get_token(account):
        try:
            enc = sg.bucketGet(bucket='dd_xnn_token', key=str(account))
            return decrypt_token(enc) if enc else None
        except: return None

    @staticmethod
    def get_all_users():
        try:
            users = sg.bucketAllKeys(bucket='dd_xnn_user')
            user_list = []
            for user in users:
                accounts = AccountManager.get_accounts(user)
                if accounts: user_list.append(str(user))
            return user_list
        except: return []

class SystemAPI:
    def __init__(self):
        self.enabled = False
        self.panel_type = config.get('panel_type', 'qinglong')
        ql_config = config['dd_hhtt_qlname']
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
                url = f"{self.QLurl}/api/envs?keyword={config['dd_hhtt_osname']}&page_size=9999"
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
                if env.get('name') != config['dd_hhtt_osname']: continue

                env_id = env.get('id') if env.get('id') is not None else env.get('_id')

                if env.get('remarks') and f'ID:{phone}' in env.get('remarks'):
                    return env_id

                if env.get('remarks') and phone in env.get('remarks'):
                    return env_id

                if token and env.get('value'):
                    env_val = env.get('value').strip()
                    input_val = str(token).strip()
                    if env_val == input_val:
                        return env_id

            return None
        except: return None

    def delete_env(self, phone):
        if not self.enabled: return False
        phone = str(phone)
        try:
            env_id = self.find_env(phone)
            if env_id is None: return False
            if self.panel_type == 'daidai':
                url = f"{self.QLurl}/api/envs/{env_id}"
                headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
                requests.delete(url, headers=headers, timeout=10, verify=False)
            else:
                url = f"{self.QLurl}/open/envs"
                headers = {"Authorization": f"Bearer {self.qltoken}", "Content-Type": "application/json"}
                requests.delete(url, headers=headers, json=[env_id], timeout=10, verify=False)
            return True
        except: return False

    def sync_env(self, token, phone, remark="", auth_time="", owner_user_id=None):
        if not self.enabled: return False
        phone = str(phone)
        try:
            env_id = self.find_env(phone, token)

            safe_phone = get_safe_account(phone)
            remarks_parts = [f'小牛牛:{safe_phone}']
            if auth_time: remarks_parts.append(f'到期:{auth_time}')
            else: remarks_parts.append('到期:未授权')
            if remark: remarks_parts.append(f'备注:{remark}')

            owner_user = get_owner_user_id(locals().get('account') or locals().get('phone') or locals().get('user_id') or '', owner_user_id if 'owner_user_id' in locals() else None)
            if not owner_user:
                raise Exception("无法确认账号真实归属，已阻止写入面板备注，避免青龙数据错乱")
            remarks_parts.extend([f'用户:{owner_user}', f'ID:{phone}', '小牛牛提交'])
            final_remark = '丨'.join(remarks_parts)

            if self.panel_type == 'daidai':
                headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
                if env_id is not None:
                    url = f"{self.QLurl}/api/envs/{env_id}"
                    data = {"name": config['dd_hhtt_osname'], "value": token, "remarks": final_remark}
                    res = requests.put(url, headers=headers, json=data, timeout=10, verify=False)
                    if res.status_code == 200:
                        try: requests.put(f"{self.QLurl}/api/envs/{env_id}/enable", headers=headers, timeout=5, verify=False)
                        except: pass
                    else: return False
                else:
                    url = f"{self.QLurl}/api/envs"
                    data = {"name": config['dd_hhtt_osname'], "value": token, "remarks": final_remark}
                    res = requests.post(url, headers=headers, json=data, timeout=10, verify=False)
                    if res.status_code != 200: return False
            else:
                headers = {"Authorization": f"Bearer {self.qltoken}", "Content-Type": "application/json"}
                url = f"{self.QLurl}/open/envs"
                if env_id is not None:
                    data = {"value": token, "name": config['dd_hhtt_osname'], "remarks": final_remark}
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
                    data = [{"value": token, "name": config['dd_hhtt_osname'], "remarks": final_remark}]
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

        safe_display = get_safe_account(account)
        remark_display = f" [{remark}]" if remark else ""

        if accountVip and accountVip > today_time:
            try:
                if not full_token or len(full_token) < 10:
                    raise Exception("凭证异常或为空")

                client = XiaoNiuClient(full_token)
                info = client.check_info()

                nickname = info.get("nickname", safe_display)
                gold = info.get("gold", "0")
                watched_today = info.get("watched_today", "未知")

                account_info = f"""
=====小牛牛详情=====
🚀 小程序: 小牛牛优选 (天津志同道合)
👤 账号: {nickname}{remark_display}
💰 当前金币: {gold}
🎬 视频进度: {watched_today}/20
⏰ 授权到期: {auth_time}"""
                return account_info.strip()
            except Exception as e:
                return f"""
=====小牛牛查询异常=====
📱 账号: {safe_display}
❌ 错误: {str(e)[:50]}
=================="""
        else:
            return f"""
=====小牛牛状态=====
📝 备注: {remark if remark else "账号"+str(index)}
📱 账号: {safe_display}
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

        menu = "=====小牛牛查询====="
        for i, acc in enumerate(accounts, 1):
            acc = str(acc)
            remark = account_remarks.get(acc, "") if config['enable_remark'] else ""
            safe_acc = get_safe_account(acc)
            vip = '2099-12-31'
            if not vip:
                vip_tag = '⚠️未授权'
            elif vip < today_time:
                vip_tag = '❌已过期'
            else:
                vip_tag = f'✅{vip}'
            remark_disp = f" [{remark}]" if remark else ""
            menu += f"\n[{i}] {safe_acc}{remark_disp} {vip_tag}"
        menu += "\n------------------\n[a] 查询全部\n支持单选/多选/区间，如 1,2 或 3-6\n回复q退出\n=================="
        sender.reply(menu)

        sel = get_user_input(timeout=60)
        if not sel or sel.lower() == 'q':
            sender.reply("✅ 已退出")
            return

        if sel.lower() == 'a':
            target_accounts = list(enumerate(accounts, 1))
        else:
            selected_idxs, invalid_parts = parse_index_selection(sel, total_count, allow_all=True)
            if not selected_idxs:
                sender.reply("❌ 序号无效，请回复如 1,2 或 3-6")
                return
            if invalid_parts:
                sender.reply(f"⚠️ 已忽略无效内容: {','.join(invalid_parts[:5])}")
            target_accounts = [(idx, accounts[idx - 1]) for idx in selected_idxs]

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
=====小牛牛 登录=====
当前模式: 🌐 提交至面板
------------------
👉 请按格式发送抓包数据 (Token)：
------------------
支持批量提交，一行一个
系统将尽力自动匹配旧号实现无损继承授权!
(可直接复制带星号旧账号升级：旧号#新Token)
(示例：10f****ab84#eyJhbG...)
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

        existing_accounts = AccountManager.get_accounts(userid)
        hash_accounts = [acc for acc in existing_accounts if not (acc.isdigit() and len(acc) == 11)]

        for line in token_lines:
            try:
                token_val = line.strip()
                explicit_old_id = None
                if '#' in line:
                    parts = line.split('#', 1)
                    explicit_old_id = parts[0].strip()
                    token_val = parts[1].strip() # 兼容带有老格式的输入

                if len(token_val) < 10:
                    sender.reply(f"❌ 格式错误: {line[:15]}... (请输入有效的Token)")
                    continue

                if explicit_old_id and '*' in explicit_old_id:
                    matched_accs = [acc for acc in existing_accounts if get_safe_account(acc) == explicit_old_id]
                    if matched_accs:
                        explicit_old_id = matched_accs[0]

                client = XiaoNiuClient(token_val)
                info_res = client.check_info()

                nick = info_res['nickname']
                final_token_str = info_res['final_token']
                new_acc_id = str(info_res['acc_key'])

                old_acc_id = explicit_old_id
                if not old_acc_id and len(hash_accounts) == 1 and new_acc_id not in existing_accounts:
                    old_acc_id = hash_accounts[0]

                if old_acc_id and old_acc_id in existing_accounts and old_acc_id != new_acc_id:
                    accountVip = '2099-12-31'
                    old_remark = RemarkManager.get_account_remark(userid, old_acc_id) if config['enable_remark'] else ""

                    if accountVip:
                        if config['enable_remark'] and old_remark:
                            RemarkManager.set_account_remark(userid, new_acc_id, old_remark)

                        AccountManager.remove_account(userid, old_acc_id)
                        try: sg.bucketDel(bucket='dd_xnn_token', key=str(old_acc_id))
                        except: pass
                        try:
                            pass
                        except: pass
                        if config['enable_remark']:
                            RemarkManager.delete_account_remark(userid, old_acc_id)
                        sys_api.delete_env(old_acc_id)

                        o_safe = get_safe_account(old_acc_id)
                        n_safe = get_safe_account(new_acc_id)
                        sender.reply(f"🔄 [身份升级] 发现更稳定的账号主体！已安全将旧身份 [{o_safe}] 的授权平滑转移至 [{n_safe}]")

                process_account_binding(final_token_str, new_acc_id, nick, remark)
            except Exception as ex:
                sender.reply(f"❌ 登录失败 ({line[:15]}...): {str(ex)}")

    except Exception as e:
        logger.error(f"绑定失败: {e}")
        sender.reply(f"❌ 绑定失败: {e}")

def process_account_binding(full_token, unique_id, nickname, remark=""):
    try:
        account = str(unique_id)

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

        remark_info = f"\n📝 备注: {remark}" if remark else ""
        safe_display = get_safe_account(account)

        is_new = AccountManager.add_account(userid, account)
        if is_new:
            try: sg.bucketSet(bucket='dd_xnn_bind_date', key=account, value=str(datetime.now().date()))
            except: pass
        AccountManager.update_account_token(account, full_token)

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

        sender.reply(f"""
=====小牛牛账号更新=====
✅ 处理成功!
👤 用户: {nickname}
📱 账号: {safe_display}{remark_info}
🔐 授权: {auth_status}{ql_msg}
⏰ 下一步操作:
   {next_step}
==================""")

    except Exception as e:
        logger.error(f"入库异常: {e}")
        sender.reply(f"❌ 入库异常: {e}")

def xy_manage():
    accounts = AccountManager.get_accounts(userid)
    if not accounts:
        sender.reply(f"❌ 未找到账号，请发送 {config['randomsigncommand']} 绑定")
        return

    account_remarks = RemarkManager.get_all_remarks(userid) if config['enable_remark'] else {}
    count = 1
    account_list = "======我的小牛牛账号====="
    today_time = str(datetime.now().date())

    for account in accounts:
        account = str(account)
        accountVip = '2099-12-31'
        if not accountVip: vip_status = '⚠️ 未授权'
        elif accountVip < today_time: vip_status = '❌ 已过期'
        else: vip_status = f'✅ {accountVip}'

        remark = account_remarks.get(account, "") if config['enable_remark'] else ""
        remark_display = f" - {remark}" if remark else ""

        safe_display = get_safe_account(account)

        account_list += f"\n------------------\n[{count}] 账号: {safe_display}{remark_display}\n🔐 授权: {vip_status}"
        count += 1

    account_list += "\n------------------\n[b] 批量授权\n[d] 批量删除\n[q] 退出管理\n=================="
    sender.reply(account_list)

    response = get_user_input()
    if not response or response == 'q':
        sender.reply('✅ 已退出')
        return

    if response.lower() == 'b':
        batch_auth_all_accounts(accounts, account_remarks)
        return
    elif response.lower() == 'd':
        batch_delete_all_accounts(accounts)
        return

    try:
        choice_num = int(response)
        if 1 <= choice_num < count:
            manage_single_account(str(accounts[choice_num - 1]), account_remarks)
        else:
            sender.reply('❌ 序号无效')
    except:
        sender.reply('❌ 输入必须是数字')

def manage_single_account(account, account_remarks):
    try:
        account = str(account)
        token = AccountManager.get_token(account)
        if not token: token = ""
        accountVip = '2099-12-31'
        remark = account_remarks.get(account, "") if config['enable_remark'] else ""

        today_time = str(datetime.now().date())
        vip_status = '⚠️ 未授权' if not accountVip else ('❌ 已过期' if accountVip < today_time else f'✅ {accountVip}')

        safe_display = get_safe_account(account)

        menu_items = """
[1] 授权账号
[2] 删除账号
[3] 修改备注"""

        sender.reply(f"""
=====账号详情=====
📱 账号: {safe_display}
📝 备注: {remark}
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

            if process_payment('小牛牛授权', months, accountVip, token, account, remark):
                try:
                    days = months * 30
                    new_auth_time = empower(accountVip, days)
                    try:
                        pass
                    except: pass

                    today_date = datetime.now().date()
                    for d in range(config['reminder_days'] + 1):
                        remind_key = f"{userid}_{account}_{today_date - timedelta(days=d)}"
                        try: sg.bucketDel('dd_xnn_remind_log', remind_key)
                        except: pass

                    if token:
                        sys_api.sync_env(token, account, remark, new_auth_time, owner_user_id=userid)
                        sender.reply("🔄 授权成功并同步到系统！")
                    else:
                        sender.reply("✅ 授权成功")

                    money = Decimal(months) * config['xyVipmoney']
                    sender.reply(f"=====订单完成=====\n💰 金额: {money}元\n📅 到期: {new_auth_time}")
                except Exception as ex:
                    sender.reply(f"❌ 授权后续写入异常: {ex}")

        elif choice == '2':
            sender.reply("确认删除回复【y】")
            if get_user_input() == 'y':
                try:
                    AccountManager.remove_account(userid, account)
                    try: sg.bucketDel(bucket='dd_xnn_token', key=account)
                    except: pass
                    try:
                        pass
                    except: pass
                    if config['enable_remark']: RemarkManager.delete_account_remark(userid, account)
                    sys_api.delete_env(account)
                    today_date = datetime.now().date()
                    for d in range(config['reminder_days'] + 1):
                        remind_key = f"{userid}_{account}_{today_date - timedelta(days=d)}"
                        try: sg.bucketDel('dd_xnn_remind_log', remind_key)
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

def process_payment(project, months, accountVip, token, account, remark=""):
    return True
def batch_auth_all_accounts(accounts, account_remarks):
    sender.reply("请输入授权月数，Q退出")
    m = get_user_input()
    if not m or not m.isdigit(): return
    months = int(m)
    if months <= 0: return

    count = len(accounts)
    total_money = Decimal(months) * config['xyVipmoney'] * count
    total_points = config['xycoin'] * months * count
    user_points = int(sg.bucketGet(config['points_bucket'], userid) or '0')

    options = []
    idx = 1
    if config['zsm']:
        options.append({'id': idx, 'type': 'wx', 'name': '微信支付', 'amount': total_money})
        idx += 1
    if config['use_ma_pay']:
        ma_conf = {
            'switch': '2099-12-31',
            'gateway': '2099-12-31',
            'pid': '2099-12-31',
            'key': '2099-12-31'
        }
        if ma_conf['switch'] == 'true':
            options.append({'id': idx, 'type': 'ma', 'name': '在线处理', 'amount': total_money, 'conf': ma_conf})
            idx += 1
    if config['epay_url'] and config['epay_pid'] and config['epay_key']:
        if config['epay_alipay']:
            options.append({'id': idx, 'type': 'epay', 'channel': 'alipay', 'name': '易支付支付宝', 'amount': total_money})
            idx += 1
        if config['epay_wxpay']:
            options.append({'id': idx, 'type': 'epay', 'channel': 'wxpay', 'name': '易支付微信', 'amount': total_money})
            idx += 1
        if config['epay_qqpay']:
            options.append({'id': idx, 'type': 'epay', 'channel': 'qqpay', 'name': '易支付QQ钱包', 'amount': total_money})
            idx += 1

    if config['xycoin'] > 0:
        options.append({'id': idx, 'type': 'pt', 'name': '积分支付', 'amount': total_points, 'curr': user_points})

    if not options:
        sender.reply("❌ 未配置支付方式")
        return

    msg = f"=====批量授权确认=====\n👥 账号数量: {count}个\n📅 授权时长: {months}个月\n💰 总需金额: {total_money}元\n💎 总需积分: {total_points}"
    msg += "\n------------------"
    for opt in options:
        amount_str = f"{opt['amount']}积分" if opt['type'] == 'pt' else f"{opt['amount']}元"
        suffix = f" (当前: {opt['curr']})" if opt['type'] == 'pt' else ""
        msg += f"\n[{opt['id']}] {opt['name']} ({amount_str}){suffix}"
    msg += "\n------------------\n回复数字选择，Q退出\n=================="
    sender.reply(msg)

    sel = get_user_input()
    if not sel or sel == 'q': return

    try:
        choice = int(sel)
        opt = next((o for o in options if o['id'] == choice), None)
        if not opt: raise ValueError

        if opt['type'] == 'wx':
            if False:
                sender.reply("⚠️ 当前有人支付中")
                return
            sender.reply(f"=====微信扫码=====\n金额: {opt['amount']}元")
            sender.replyImage(config['zsm'])
            res = False
            if str(res) == 'q': return

        elif opt['type'] == 'epay':
            formatted_money = f"{Decimal(opt['amount']):.2f}"
            out_trade_no = f"XNN_BATCH_{userid}_{int(time.time())}"
            qr_image_url, pay_url = _create_epay_qr(out_trade_no, opt['channel'], f"小牛牛批量-{count}号-{months}月", formatted_money)
            sender.reply(f"""=====易支付订单=====
🎫 商品: 小牛牛批量授权
👥 账号数量: {count}个
💰 金额: {formatted_money}元
💳 通道: {opt['name']}
------------------
请扫在线处理，系统将自动查询支付状态
==================""")
            try: sender.replyImage(qr_image_url)
            except: sender.reply(f"支付链接: {pay_url}")

            query_url = f"{config['epay_url'].rstrip('/')}/api.php?act=order&pid={config['epay_pid']}&key={config['epay_key']}&out_trade_no={out_trade_no}"
            paid = False
            for _ in range(20):
                time.sleep(3)
                try:
                    order_res = requests.get(query_url, timeout=10, verify=False).json()
                    status = str(order_res.get('status') or order_res.get('trade_status') or '')
                    if status in ['1', 'TRADE_SUCCESS', 'success', 'paid']:
                        paid = True
                        break
                except Exception as e:
                    logger.warning(f"易支付查单异常: {e}")
            if not paid:
                sender.reply("⚠️ 未检测到支付完成，请稍后重试或检查配置核对订单")
                return
            sender.reply("✅ 易支付订单已支付")

        elif opt['type'] == 'pt':
            if int(opt['curr']) < int(opt['amount']):
                sender.reply(f"❌ 积分不足，需要 {opt['amount']}，当前 {opt['curr']}")
                return
            sender.reply(f"确认消耗 {opt['amount']} 积分？回复【y】")
            if get_user_input() != 'y': return
            new_pt = int(opt['curr']) - int(opt['amount'])
            try: sg.bucketSet(config['points_bucket'], userid, str(new_pt))
            except Exception as e:
                sender.reply(f"❌ 积分扣除异常: {e}")
                return

        elif opt['type'] == 'ma':
            conf = opt['conf']
            out_trade_no = f"XNN_BATCH_{int(time.time())}{userid}"
            params = {
                'pid': conf['pid'],
                'type': 'alipay',
                'out_trade_no': out_trade_no,
                'name': f"小牛牛批量-{count}号-{months}月",
                'money': str(opt['amount']),
                'notify_url': '', 'return_url': '', 'param': userid
            }
            sorted_params = sorted(params.items(), key=lambda x: x[0])
            sign_str = "&".join([f"{k}={v}" for k, v in sorted_params])
            sign = hashlib.md5((sign_str + conf['key']).encode()).hexdigest().lower()
            params['sign'] = sign
            params['sign_type'] = 'MD5'

            url = conf['gateway'].rstrip('/') + '/submit.php'
            res = requests.post(url, data=params, timeout=10)
            if 'http' in res.text:
                sender.reply("请完成支付后检查配置")
            else:
                sender.reply("❌ 创建订单失败")
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
                try: sg.bucketDel('dd_xnn_remind_log', remind_key)
                except: pass
        except: pass

    sender.reply("✅ 批量授权完成")

def batch_delete_all_accounts(accounts):
    sender.reply("确认删除回复【确认删除】")
    if get_user_input() == "确认删除":
        today_date = datetime.now().date()
        for account in accounts:
            try:
                 account = str(account)
                 AccountManager.remove_account(userid, account)
                 try: sg.bucketDel(bucket='dd_xnn_token', key=account)
                 except: pass
                 try:
                     pass
                 except: pass
                 if config['enable_remark']: RemarkManager.delete_account_remark(userid, account)
                 sys_api.delete_env(account)
                 for d in range(config['reminder_days'] + 1):
                     remind_key = f"{userid}_{account}_{today_date - timedelta(days=d)}"
                     try: sg.bucketDel('dd_xnn_remind_log', remind_key)
                     except: pass
            except: pass
        sender.reply("✅ 批量删除完成")

def clean_expired_accounts(force_report=False):
    users = sg.bucketAllKeys(bucket='dd_xnn_user')
    if not users:
        if sender.isAdmin() and (force_report or usermessage in ['小牛牛清理', '清理小牛牛']):
            sender.reply("=====执行结果=====\n📭 暂无用户数据")
        return {
            "report_date": str(datetime.now().date()),
            "scanned_users": 0, "scanned_accounts": 0,
            "sent_notifications": 0, "cleaned_count": 0,
            "reminded_count": 0, "ck_expired_count": 0,
        }

    if sender.isAdmin() and (force_report or usermessage in ['小牛牛清理', '清理小牛牛']):
        sender.reply(f"=====开始执行维护=====\n📊 扫描用户数: {len(users)}\n⚙️ 提醒天数: {config['reminder_days']}天\n⏳ 处理中...")

    cleaned_count = 0
    reminded_count = 0
    ck_expired_count = 0
    scanned_accounts = 0
    today_date = datetime.now().date()
    reminder_days_cfg = config['reminder_days']
    user_account_meta = {}
    ck_verify_tasks = []
    panel_ck_tasks = collect_panel_ck_tasks()

    for user in users:
        try:
            accounts = AccountManager.get_accounts(user)
            for account in accounts:
                account = str(account)
                scanned_accounts += 1
                accountVip = '2099-12-31'
                if not accountVip:
                    expiration_date = None
                    expiration_str = "未授权"
                    days_diff = None
                else:
                    try:
                        expiration_date = datetime.strptime(str(accountVip), "%Y-%m-%d").date()
                        expiration_str = str(accountVip)
                    except:
                        expiration_date = today_date - timedelta(days=1)
                        expiration_str = "日期错误"
                    days_diff = (expiration_date - today_date).days

                token = AccountManager.get_token(account)
                user_account_meta[(str(user), account)] = {
                    "accountVip": accountVip,
                    "expiration_str": expiration_str,
                    "days_diff": days_diff,
                    "token": token,
                    "token_hash": hashlib.md5(str(token or '').encode()).hexdigest() if token else '',
                }
                if token and days_diff is not None and days_diff >= 0:
                    ck_verify_tasks.append((str(user), account, token))
        except Exception as e:
            logger.warning(f"维护预扫描用户失败 {user}: {e}")

    ck_verify_tasks.extend(panel_ck_tasks)
    ck_verify_result = batch_verify_account_ck(ck_verify_tasks)
    panel_unmapped_invalid = []

    for task in panel_ck_tasks:
        try:
            token_hash = hashlib.md5(str(task.get('token') or '').encode()).hexdigest()
            result_key = ('panel', str(task.get('user') or ''), str(task.get('account') or ''), token_hash)
            if ck_verify_result.get(result_key) is not False:
                continue

            owner = str(task.get('user') or '').strip()
            account = str(task.get('account') or '').strip()
            auth_date = str(task.get('auth_date') or '未知')
            safe_disp = get_safe_account(account)
            check_fail_key = f"panel_{owner}_{account}_{token_hash}_ck_fail_{today_date}"
            has_notified_fail = sg.bucketGet('dd_xnn_remind_log', check_fail_key)
            if has_notified_fail:
                continue

            msg = f"""=====⚠️ CK失效提醒=====
您的小牛牛账号登录凭证已失效！
📱 账号: {safe_disp}
📅 授权到期: {auth_date}
------------------
面板变量已检测到需要重新登录。
请发送 {config['randomsigncommand']} 更新Token，避免脚本继续空跑。
=================="""

            sent = False
            if owner:
                sent = safe_send_message(owner, msg, f"面板CK失效通知 {owner}-{account}")
            if sent:
                try: sg.bucketSet('dd_xnn_remind_log', check_fail_key, "1")
                except: pass
            else:
                panel_unmapped_invalid.append(f"用户:{owner or '未识别'} 账号:{safe_disp} env:{task.get('env_id')}")
                logger.warning(f"面板CK失效但推送失败/无归属: owner={owner}, account={account}, env={task.get('env_id')}")
            ck_expired_count += 1
        except Exception as e:
            logger.warning(f"处理面板CK失效通知失败: {e}")

    if panel_unmapped_invalid:
        admin_msg = "=====小牛牛面板CK失效未送达=====\n" + "\n".join(panel_unmapped_invalid[:20])
        if len(panel_unmapped_invalid) > 20:
            admin_msg += f"\n...其余 {len(panel_unmapped_invalid) - 20} 条省略"
        admin_msg += "\n请检查面板备注是否包含 用户: 和 ID:\n=================="
        send_message_to_framework_admins(admin_msg)

    for user in users:
        try:
            accounts = AccountManager.get_accounts(user)
            if not accounts:
                continue
            valid_accounts = []
            user_has_change = False

            for account in accounts:
                account = str(account)
                meta = user_account_meta.get((str(user), account), {})
                days_diff = meta.get("days_diff")
                expiration_str = meta.get("expiration_str", "未知")
                token_hash = meta.get("token_hash") or ''

                if days_diff is None:
                    valid_accounts.append(account)
                    continue

                local_result_key = ('local', str(user), account, token_hash)
                local_ck_invalid = ck_verify_result.get(local_result_key) is False if token_hash else ck_verify_result.get((str(user), account)) is False
                if days_diff >= 0 and local_ck_invalid:
                    check_fail_key = f"{user}_{account}_ck_fail_{today_date}"
                    has_notified_fail = sg.bucketGet('dd_xnn_remind_log', check_fail_key)
                    if not has_notified_fail:
                        safe_disp = get_safe_account(account)
                        msg = f"""=====⚠️ CK失效提醒=====
您的小牛牛账号登录凭证已失效！
📱 账号: {safe_disp}
📅 授权到期: {expiration_str}
------------------
脚本已检测到账号需要重新登录。
请发送 {config['randomsigncommand']} 更新Token，避免继续空跑任务。
=================="""
                        if safe_send_message(user, msg, f"CK失效通知 {user}-{account}"):
                            try: sg.bucketSet('dd_xnn_remind_log', check_fail_key, "1")
                            except: pass
                            ck_expired_count += 1

                if days_diff > reminder_days_cfg:
                    valid_accounts.append(account)
                    continue

                if 0 <= days_diff <= reminder_days_cfg:
                    valid_accounts.append(account)
                    remind_key = f"{user}_{account}_{today_date}"
                    has_reminded = sg.bucketGet('dd_xnn_remind_log', remind_key)
                    if not has_reminded:
                        safe_display = get_safe_account(account)
                        msg = f"""=====⏰ 到期提醒=====
您的小牛牛账号授权即将到期！
📱 账号: {safe_display}
📅 到期: {expiration_str} (剩余 {days_diff} 天)
------------------
为避免影响挂机，请及时续费。
发送 {config['randommanagecommand']} 进行续费
=================="""
                        if safe_send_message(user, msg, f"到期提醒 {user}-{account}"):
                            try: sg.bucketSet('dd_xnn_remind_log', remind_key, "1")
                            except: pass
                            reminded_count += 1
                    continue

                if days_diff < 0:
                    try:
                        sys_api.delete_env(account)
                        try: sg.bucketDel(bucket='dd_xnn_token', key=account)
                        except: pass
                        try:
                            pass
                        except: pass
                        if config['enable_remark']:
                            RemarkManager.delete_account_remark(user, account)
                    except Exception as e:
                        logger.warning(f"过期账号清理异常 {user}-{account}: {e}")

                    safe_display = get_safe_account(account)
                    clean_msg = f"""=====🗑️ 过期清理通知=====
您的账号授权已过期并清理。
📱 账号: {safe_display}
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
                    try: sg.bucketSet(bucket='dd_xnn_user', key=str(user), value=str(valid_accounts))
                    except: pass
                else:
                    try: sg.bucketDel(bucket='dd_xnn_user', key=str(user))
                    except: pass

        except Exception as e:
            logger.warning(f"维护任务处理用户失败 {user}: {e}")
            continue

    if sender.isAdmin() and (force_report or usermessage in ['小牛牛清理', '清理小牛牛']):
        sender.reply(
            f"=====维护完成=====\n"
            f"✅ 本地检测: {scanned_accounts}个\n"
            f"🌐 面板检测: {len(panel_ck_tasks)}个\n"
            f"📢 授权提醒: {reminded_count}个\n"
            f"⚠️ CK失效通知: {ck_expired_count}个\n"
            f"🗑️ 已清理过期: {cleaned_count}个\n"
            f"=================="
        )

    return {
        "report_date": str(today_date),
        "scanned_users": len(users),
        "scanned_accounts": scanned_accounts + len(panel_ck_tasks),
        "panel_scanned_accounts": len(panel_ck_tasks),
        "sent_notifications": reminded_count + ck_expired_count + cleaned_count,
        "cleaned_count": cleaned_count,
        "reminded_count": reminded_count,
        "ck_expired_count": ck_expired_count,
    }







def admin_auth_options():
    return True
def show_tutorial():
    panel_name = '青龙' if config['panel_type'] == 'qinglong' else '呆呆'
    sender.reply(f"""
=====小牛牛插件教程=====
当前模式: 🌐 提交至{panel_name}面板

1️⃣ {config['randomsigncommand']}
   直接发 Token 给我就行！系统会自动拉取手机号，以后怎么换CK都能完美无缝续期。

2️⃣ {config['randomquerycommand']}
   实时查询账号存活状态与当前金币和视频进度。

3️⃣ {config['randommanagecommand']}
   续费、删除、修改备注。

4️⃣ 小牛牛清理 / 小牛牛授权 / 小牛牛广播
   清理过期并同步删除系统变量；
   管理员进行全局或个人独立授权(支持加减天数)；
   系统管理员向所有已授权用户发送广播通知。
==================""")

try:
    if sender.getImtype() == 'fake':
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

    elif re.search(r'(通知|广播)', usermessage or ''):
        notify_authorized_users()
    elif '登录' in usermessage or '登陆' in usermessage:
        bindaccount()
    elif '管理' in usermessage:
       xy_manage()
    elif '查询' in usermessage:
        cxs()
    elif usermessage in ['小牛牛清理', '清理小牛牛']:
        try:
            report_data = clean_expired_accounts(force_report=True)
        except Exception:
            logger.error(f"手动维护清理异常: {traceback.format_exc()}")
            report_data = {
                "report_date": str(datetime.now().date()),
                "scanned_users": 0, "scanned_accounts": 0,
                "sent_notifications": 0, "cleaned_count": 0,
                "reminded_count": 0, "ck_expired_count": 0,
            }
        send_daily_admin_report(report_data, force_send=True, notify_status=True)
    elif '广播' in usermessage or '通知' in usermessage:
        notify_authorized_users()
    elif '授权' in usermessage:
        admin_auth_options()
    elif '教程' in usermessage:
        show_tutorial()

except Exception as e:
    logger.error(f"Error: {e}")
    sender.reply(f"❌ 系统错误: {e}")
