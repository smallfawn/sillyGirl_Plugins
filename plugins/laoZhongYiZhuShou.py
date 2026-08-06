# [title: 老中医助手]
# [name: laoZhongYiZhuShou]
# [language: python]
# [class: 任务]
# [author: 8165799]
# [version: v1.1.2]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(老中医)(登录|登陆)$|^登(录|陆)(老中医)$|^(老中医)(查询|管理)$|^(查询|管理)(老中医)$|^老中医清理$|^老中医$|^老中医教程$|^老中医通知 ?(.*)$|^清理老中医$|^老中医广播 ?(.*)$]
# [cron: 5 10 * * *]
# [icon: https://api.iconify.design/lucide:bot.svg]
# [description: 老中医提交计费版；2. 支持登录验证，防止数据错误也提交；3.]
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
    'dd_lzy_panel_type': plugin.Form.string().title('对接面板类型').default('').description('qinglong=青龙面板 daidai=呆呆面板'),
    'dd_lzy_dd_lzy_qlname': plugin.Form.string().title('对接系统配置').default('').description('青龙:URL丨ID丨Secret 呆呆:URL丨Key丨Secret'),
    'dd_lzy_dd_lzy_osname': plugin.Form.string().title('系统变量名').default('').description('系统容器内变量名(默认为sx_qytm)'),
    'dd_lzy_enable_proxy': plugin.Form.boolean().title('是否启用代理').default(False).description('是否启用代理功能'),
    'dd_lzy_proxy_pool_url': plugin.Form.string().title('代理池地址').default('').description('代理API服务地址'),
    'dd_lzy_enable_remark': plugin.Form.boolean().title('启用备注功能').default(False).description('是否启用账号备注功能'),
})
_CONFIG_FIELD_MAP = {
    ('dd_lzy', 'panel_type'): 'dd_lzy_panel_type',
    ('dd_lzy', 'dd_lzy_qlname'): 'dd_lzy_dd_lzy_qlname',
    ('dd_lzy', 'dd_lzy_osname'): 'dd_lzy_dd_lzy_osname',
    ('dd_lzy', 'enable_proxy'): 'dd_lzy_enable_proxy',
    ('dd_lzy', 'proxy_pool_url'): 'dd_lzy_proxy_pool_url',
    ('dd_lzy', 'enable_remark'): 'dd_lzy_enable_remark',
}

import re
import ast
from datetime import datetime, timedelta
from decimal import Decimal
import requests
import time
import hashlib
import logging
import base64
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed

warnings.filterwarnings('ignore', message='Unverified HTTPS request')
requests.packages.urllib3.disable_warnings()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('lzy_plugin')

REQUEST_TIMEOUT = 30

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = str(sender.getUserID())
usermessage = sender.getMessage()

_RUNTIME_BUCKET = "plugin_push_runtime"
_RUNTIME_KEY = "老中医"
try:
    current_imtype = str(sender.getImtype() or "")
except:
    current_imtype = ""
if current_imtype and current_imtype.lower() not in ["fake", "cron"]:
    try: sg.bucketSet(_RUNTIME_BUCKET, _RUNTIME_KEY + "_sender", str(senderID))
    except: pass
    try: sg.bucketSet(_RUNTIME_BUCKET, _RUNTIME_KEY + "_imtype", current_imtype)
    except: pass

def getusercontent():
    panel_type = sg.bucketGet('dd_lzy', 'panel_type') or 'qinglong'
    panel_type = panel_type.lower()

    env_qlconfig = sg.bucketGet('dd_lzy', 'dd_lzy_qlname') or ''
    env_name = sg.bucketGet('dd_lzy', 'dd_lzy_osname') or 'sx_qytm'

    if not env_qlconfig:
        sender.reply("❌ 配置错误：请在插件配置中填写【对接系统配置】(面板信息)。")
        exit(0)

    dd_managecommand = sg.bucketGet('dd_lzy', 'dd_managecommand') or '老中医管理'
    dd_querycommand = sg.bucketGet('dd_lzy', 'dd_querycommand') or '老中医查询'
    dd_signcommand = sg.bucketGet('dd_lzy', 'dd_signcommand') or '老中医登录'
    zsm = sg.bucketGet('dd_lzy', 'zsm') or ''

    enable_proxy = sg.bucketGet('dd_lzy', 'enable_proxy') or 'false'
    enable_proxy = enable_proxy.lower() == 'true'
    proxy_pool_url = sg.bucketGet('dd_lzy', 'proxy_pool_url') or ''

    points_bucket = sg.bucketGet('dd_lzy', 'points_bucket') or 'dd_sign_points'

    enable_remark = sg.bucketGet('dd_lzy', 'enable_remark') or 'false'
    enable_remark = enable_remark.lower() == 'true'

    randommanagecommand = dd_managecommand
    randomquerycommand = dd_querycommand
    randomsigncommand = dd_signcommand

    lzyVipmoney = Decimal(sg.bucketGet('dd_lzy', 'lzyVipmoney') or '0')
    lzycoin = int(sg.bucketGet('dd_lzy', 'lzycoin') or '0')

    show_point_status = sg.bucketGet('dd_lzy', 'show_point_status') or 'false'
    show_point_status = show_point_status.lower() == 'true'

    use_ma_pay = '2099-12-31'
    use_ma_pay = use_ma_pay.lower() == 'true'

    reminder_days = int(sg.bucketGet('dd_lzy', 'reminder_days') or '2')

    return {
        'panel_type': panel_type,
        'env_name': env_name,
        'env_qlconfig': env_qlconfig,
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
        'lzyVipmoney': lzyVipmoney,
        'lzycoin': lzycoin,
        'show_point_status': show_point_status,
        'use_ma_pay': use_ma_pay,
        'reminder_days': reminder_days
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
        for owner in sg.bucketAllKeys(bucket='dd_lzy_user'):
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

def send_user_notice(user_id, msg, title="老中医助手通知"):
    user_id = str(user_id or "").strip()
    if not user_id:
        return False
    imtype = ""
    try:
        imtype = str(sender.getImtype() or "")
    except:
        pass
    if not imtype or imtype.lower() in ["fake", "cron"]:
        imtype = sg.bucketGet(_RUNTIME_BUCKET, _RUNTIME_KEY + "_imtype") or ""
    try:
        if imtype:
            sg.Push(imtype, "", user_id, title, msg)
            return True
    except Exception as e:
        logger.warning(f"Push发送失败 {user_id}: {e}")
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

class LzyClient:
    def __init__(self, auth, app_sign):
        self.auth = auth.replace('Bearer ', '').strip()
        self.app_sign = app_sign.strip()
        self.token = f"{self.auth}#{self.app_sign}"
        self.host = "dt.yuanhukj.com"

        self.ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf254181c) XWEB/19339"

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

        url = f"https://{self.host}/api/mobile/account/user/overview_my"
        params = {
            "source_type": "2314",
            "source_from": "2321",
            "source_lang": "zh_CN",
            "currency_id": "86",
            "site_id": ""
        }
        headers = {
            "Host": self.host,
            "Connection": "keep-alive",
            "Authorization": f"Bearer {self.auth}",
            "app-sign": self.app_sign,
            "User-Agent": self.ua,
            "xweb_xhr": "1",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "*/*",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": f"https://servicewechat.com/{self.app_sign}/2/page-frame.html",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }

        try:
            res = requests.get(url, params=params, headers=headers, verify=False, proxies=proxies, timeout=10)
            rj = res.json()
            if rj.get("code") != 0:
                raise Exception(rj.get("msg", "Token无效或已过期"))

            user_info = rj.get("data", {})
            phone = str(user_info.get('user_id', ''))
            if not phone:
                raise Exception("未获取到用户ID")

            user_money = user_info.get('user_money', 0)
            user_money_frozen = user_info.get('user_money_frozen', 0)

        except Exception as e:
            raise Exception(f"验证失败: {str(e)}")

        consume_url = f"https://{self.host}/api/mobile/pay/index/consumeRecord"
        consume_params = params.copy()
        consume_params.update({
            "change_type": "0",
            "page": "1",
            "rows": "2"
        })
        records_msg = ""
        try:
            c_res = requests.get(consume_url, params=consume_params, headers=headers, verify=False, proxies=proxies, timeout=10)
            c_rj = c_res.json()
            if c_rj.get("code") == 0:
                items = c_rj.get("data", {}).get("items", [])
                if items:
                    records_msg = "\n".join([f"   - {item.get('record_total')}元 ({item.get('record_time')})" for item in items])
                else:
                    records_msg = "暂无提现记录"
        except:
            pass

        safe_phone = phone[:3] + "****" + phone[-4:] if len(phone) >= 11 else phone[:2] + "***"

        return {
            "nickname": f"老中医_{safe_phone}",
            "phone": phone,
            "user_money": user_money,
            "user_money_frozen": user_money_frozen,
            "records_msg": records_msg,
            "acc_key": phone,
            "final_token": self.token
        }

class RemarkManager:
    @staticmethod
    def get_account_remark(user_id, account_id):
        try:
            remark_data = sg.bucketGet(bucket='dd_lzy_remarks', key=f'{user_id}_{account_id}')
            return str(remark_data) if remark_data else ""
        except: return ""

    @staticmethod
    def set_account_remark(user_id, account_id, remark):
        try:
            remark_clean = str(remark).strip()[:20]
            if remark_clean:
                sg.bucketSet(bucket='dd_lzy_remarks', key=f'{user_id}_{account_id}', value=remark_clean)
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
            sg.bucketDel(bucket='dd_lzy_remarks', key=f'{user_id}_{account_id}')
            return True
        except: return False

class AccountManager:
    @staticmethod
    def get_accounts(user_id):
        try:
            value = sg.bucketGet(bucket='dd_lzy_user', key=str(user_id))
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
                sg.bucketSet(bucket='dd_lzy_user', key=str(user_id), value=str(accounts))
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
                    sg.bucketSet(bucket='dd_lzy_user', key=str(user_id), value=str(accounts))
                else:
                    sg.bucketDel(bucket='dd_lzy_user', key=str(user_id))
                return True
            return False
        except: return False

    @staticmethod
    def update_account_token(account, token):
        try:
            encrypted_token = encrypt_token(str(token))
            sg.bucketSet(bucket='dd_lzy_token', key=str(account), value=encrypted_token)
            return True
        except: return False

    @staticmethod
    def get_token(account):
        try:
            enc = sg.bucketGet(bucket='dd_lzy_token', key=str(account))
            return decrypt_token(enc) if enc else None
        except: return None

    @staticmethod
    def get_all_users():
        try:
            users = sg.bucketAllKeys(bucket='dd_lzy_user')
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

            script_remark = remark if remark else phone
            ql_value = f"{script_remark}#{token}"

            safe_phone = phone[:3] + "****" + phone[-4:] if len(phone) >= 11 else phone[:2] + "***"
            remarks_parts = [f'老中医:{safe_phone}']
            if auth_time: remarks_parts.append(f'到期:{auth_time}')
            else: remarks_parts.append('到期:未授权')
            if remark: remarks_parts.append(f'备注:{remark}')

            owner_user = get_owner_user_id(locals().get('account') or locals().get('phone') or locals().get('user_id') or '', owner_user_id if 'owner_user_id' in locals() else None)
            if not owner_user:
                raise Exception("无法确认账号真实归属，已阻止写入面板备注，避免青龙数据错乱")
            remarks_parts.extend([f'用户:{owner_user}', f'ID:{phone}', '老中医提交'])
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

        safe_display = account[:3] + "****" + account[-4:] if len(account) >= 11 else account[:2] + "***"
        remark_display = f" [{remark}]" if remark else ""

        if accountVip and accountVip > today_time:
            try:
                if not full_token or len(full_token) < 10:
                    raise Exception("凭证异常或为空")

                parts = full_token.split('#')
                auth = parts[0]
                app_sign = parts[1] if len(parts) > 1 else "wxa383330eb33f1ebd"

                client = LzyClient(auth, app_sign)
                info = client.check_info()

                nickname = info.get("nickname", safe_display)
                user_money = info.get("user_money", "0")
                user_money_frozen = info.get("user_money_frozen", "0")
                records_msg = info.get("records_msg", "")

                account_info = f"""
=====老中医详情=====
🚀 小程序: 森选之老中医
👤 账号: {nickname}{remark_display}
💰 账户余额: {user_money}
💸 已提现: {user_money_frozen}
📜 最近提现:
{records_msg if records_msg else "暂无提现记录"}
⏰ 授权到期: {auth_time}"""
                return account_info.strip()
            except Exception as e:
                return f"""
=====老中医查询异常=====
📱 账号: {safe_display}
❌ 错误: {str(e)[:50]}
=================="""
        else:
            return f"""
=====老中医状态=====
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

        menu = "=====老中医查询====="
        for i, acc in enumerate(accounts, 1):
            acc = str(acc)
            remark = account_remarks.get(acc, "") if config['enable_remark'] else ""
            safe_acc = acc[:3] + "****" + acc[-4:] if len(acc) >= 11 else acc[:2] + "***"
            vip = '2099-12-31'
            if not vip:
                vip_tag = '⚠️未授权'
            elif vip < today_time:
                vip_tag = '❌已过期'
            else:
                vip_tag = f'✅{vip}'
            remark_disp = f" [{remark}]" if remark else ""
            menu += f"\n[{i}] {safe_acc}{remark_disp} {vip_tag}"
        menu += "\n------------------\n[a] 查询全部\n回复数字单独查询\n回复q退出\n=================="
        sender.reply(menu)

        sel = get_user_input(timeout=60)
        if not sel or sel.lower() == 'q':
            sender.reply("✅ 已退出")
            return

        if sel.lower() == 'a':
            target_accounts = list(enumerate(accounts, 1))
        else:
            try:
                idx = int(sel)
                if idx < 1 or idx > total_count:
                    sender.reply("❌ 序号无效")
                    return
                target_accounts = [(idx, accounts[idx - 1])]
            except:
                sender.reply("❌ 请输入有效数字或 a")
                return

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
=====老中医 登录=====
当前模式: 🌐 提交至面板
------------------
👉 必须带上 app-sign 录入，支持以下格式：
------------------
格式：备注#Authorization#app-sign
(系统会自动提取并组装)
------------------
支持批量提交，一行一个
⚠️ 自动抓取用户ID作为主键，完美无损续期!
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

        for line in token_lines:
            try:
                val = line.strip()
                parts = val.split('#')

                if len(parts) == 1:
                    sender.reply("❌ 格式错误: 缺少 app-sign。请使用 Authorization#app-sign 或 备注#Authorization#app-sign 格式。")
                    continue
                elif len(parts) == 2:
                    if parts[1].startswith('wx') and len(parts[1]) < 30:
                        auth = parts[0]
                        app_sign = parts[1]
                    else:
                        sender.reply("❌ 格式错误: 缺少 app-sign 或 app-sign 格式不正确(应以wx开头)。")
                        continue
                else:
                    auth = parts[1]
                    app_sign = parts[2]
                    if not app_sign.startswith('wx'):
                        sender.reply("❌ 格式错误: app-sign 格式不正确(应以wx开头)。")
                        continue

                auth = auth.replace('Bearer ', '').strip()

                if len(auth) < 20:
                    sender.reply(f"❌ 格式错误: {val[:15]}... (Authorization长度异常)")
                    continue

                client = LzyClient(auth, app_sign)
                info_res = client.check_info()

                nick = info_res['nickname']
                final_token_str = info_res['final_token']
                acc_id = info_res['acc_key']

                process_account_binding(final_token_str, acc_id, nick, remark)
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
        safe_display = account[:3] + "****" + account[-4:] if len(account) >= 11 else account[:2] + "***"

        is_new = AccountManager.add_account(userid, account)
        if is_new:
            try: sg.bucketSet(bucket='dd_lzy_bind_date', key=account, value=str(datetime.now().date()))
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

        sender.reply(f"""
=====老中医账号更新=====
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
    account_list = "======我的老中医账号====="
    today_time = str(datetime.now().date())

    for account in accounts:
        account = str(account)
        accountVip = '2099-12-31'
        if not accountVip: vip_status = '⚠️ 未授权'
        elif accountVip < today_time: vip_status = '❌ 已过期'
        else: vip_status = f'✅ {accountVip}'

        remark = account_remarks.get(account, "") if config['enable_remark'] else ""
        remark_display = f" - {remark}" if remark else ""

        safe_display = account[:3] + "****" + account[-4:] if len(account) >= 11 else account[:2] + "***"

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

        safe_display = account[:3] + "****" + account[-4:] if len(account) >= 11 else account[:2] + "***"

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

            if process_payment('老中医授权', months, accountVip, token, account, remark):
                try:
                    days = months * 30
                    new_auth_time = empower(accountVip, days)
                    try:
                        pass
                    except: pass

                    today_date = datetime.now().date()
                    for d in range(config['reminder_days'] + 1):
                        remind_key = f"{userid}_{account}_{today_date - timedelta(days=d)}"
                        try: sg.bucketDel('dd_lzy_remind_log', remind_key)
                        except: pass

                    if token:
                        sys_api.sync_env(token, account, remark, new_auth_time)
                        sender.reply("🔄 授权成功并同步到系统！")
                    else:
                        sender.reply("✅ 授权成功")

                    money = Decimal(months) * config['lzyVipmoney']
                    sender.reply(f"=====订单完成=====\n💰 金额: {money}元\n📅 到期: {new_auth_time}")
                except Exception as ex:
                    sender.reply(f"❌ 授权后续写入异常: {ex}")

        elif choice == '2':
            sender.reply("确认删除回复【y】")
            if get_user_input() == 'y':
                try:
                    AccountManager.remove_account(userid, account)
                    try: sg.bucketDel(bucket='dd_lzy_token', key=account)
                    except: pass
                    try:
                        pass
                    except: pass
                    if config['enable_remark']: RemarkManager.delete_account_remark(userid, account)
                    sys_api.delete_env(account)
                    today_date = datetime.now().date()
                    for d in range(config['reminder_days'] + 1):
                        remind_key = f"{userid}_{account}_{today_date - timedelta(days=d)}"
                        try: sg.bucketDel('dd_lzy_remind_log', remind_key)
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
                     sys_api.sync_env(token, account, new_remark, accountVip)
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
    total_money = Decimal(months) * config['lzyVipmoney'] * count
    total_points = config['lzycoin'] * months * count
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

    if config['lzycoin'] > 0:
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
            out_trade_no = f"LZY_BATCH_{int(time.time())}{userid}"
            params = {
                'pid': conf['pid'],
                'type': 'alipay',
                'out_trade_no': out_trade_no,
                'name': f"老中医批量-{count}号-{months}月",
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
                sys_api.sync_env(token, account, curr_remark, new_date)

            today_date = datetime.now().date()
            for d in range(config['reminder_days'] + 1):
                remind_key = f"{userid}_{account}_{today_date - timedelta(days=d)}"
                try: sg.bucketDel('dd_lzy_remind_log', remind_key)
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
                 try: sg.bucketDel(bucket='dd_lzy_token', key=account)
                 except: pass
                 try:
                     pass
                 except: pass
                 if config['enable_remark']: RemarkManager.delete_account_remark(userid, account)
                 sys_api.delete_env(account)
                 for d in range(config['reminder_days'] + 1):
                     remind_key = f"{userid}_{account}_{today_date - timedelta(days=d)}"
                     try: sg.bucketDel('dd_lzy_remind_log', remind_key)
                     except: pass
            except: pass
        sender.reply("✅ 批量删除完成")

def clean_expired_accounts():
    users = sg.bucketAllKeys(bucket='dd_lzy_user')
    if not users:
        if sender.isAdmin() and usermessage in ['老中医清理', '清理老中医']:
            sender.reply("=====执行结果=====\n📭 暂无用户数据")
        return

    if sender.isAdmin() and usermessage in ['老中医清理', '清理老中医']:
        sender.reply(f"=====开始执行维护=====\n📊 扫描用户数: {len(users)}\n⚙️ 提醒天数: {config['reminder_days']}天\n⏳ 处理中...")

    cleaned_count = 0
    reminded_count = 0
    today_date = datetime.now().date()
    reminder_days_cfg = config['reminder_days']

    for user in users:
        try:
            accounts = AccountManager.get_accounts(user)
            if not accounts: continue

            valid_accounts = []
            user_has_change = False

            try:
                sg.Sender(str(user))
            except: continue

            for account in accounts:
                account = str(account)
                accountVip = '2099-12-31'

                if not accountVip:
                    valid_accounts.append(account)
                    continue
                else:
                    try:
                        expiration_date = datetime.strptime(accountVip, "%Y-%m-%d").date()
                        expiration_str = accountVip
                    except:
                        expiration_date = today_date - timedelta(days=1)
                        expiration_str = "日期错误"

                days_diff = (expiration_date - today_date).days

                if days_diff > reminder_days_cfg:
                    valid_accounts.append(account)
                    continue

                if 0 <= days_diff <= reminder_days_cfg:
                    valid_accounts.append(account)
                    remind_key = f"{user}_{account}_{today_date}"
                    has_reminded = sg.bucketGet('dd_lzy_remind_log', remind_key)

                    if not has_reminded:
                        safe_display = account[:3] + "****" + account[-4:] if len(account) >= 11 else account[:2] + "***"
                        msg = f"""=====⏰ 到期提醒=====
您的老中医账号授权即将到期！
📱 账号: {safe_display}
📅 到期: {expiration_str} (剩余 {days_diff} 天)
------------------
为避免影响挂机，请及时续费。
发送 {config['randommanagecommand']} 进行续费
=================="""
                        send_user_notice(user, msg)
                        try: sg.bucketSet('dd_lzy_remind_log', remind_key, "1")
                        except: pass
                        reminded_count += 1
                    continue

                if days_diff < 0:
                    try:
                        sys_api.delete_env(account)
                        try: sg.bucketDel(bucket='dd_lzy_token', key=account)
                        except: pass
                        try:
                            pass
                        except: pass
                        if config['enable_remark']:
                            RemarkManager.delete_account_remark(user, account)
                    except: pass

                    safe_display = account[:3] + "****" + account[-4:] if len(account) >= 11 else account[:2] + "***"
                    clean_msg = f"""=====🗑️ 过期清理通知=====
您的账号授权已过期并清理。
📱 账号: {safe_display}
📅 到期: {expiration_str}
------------------
相关配置已失效移除。
如需继续使用，请重新登录并授权。
=================="""
                    send_user_notice(user, clean_msg)
                    cleaned_count += 1
                    user_has_change = True

            if user_has_change:
                if valid_accounts:
                    try: sg.bucketSet(bucket='dd_lzy_user', key=str(user), value=str(valid_accounts))
                    except: pass
                else:
                    try: sg.bucketDel(bucket='dd_lzy_user', key=str(user))
                    except: pass

        except Exception:
            continue

    if sender.isAdmin() and usermessage in ['老中医清理', '清理老中医']:
        sender.reply(f"=====维护完成=====\n✅ 已清理过期: {cleaned_count}个\n📢 发送提醒: {reminded_count}个\n==================")

def admin_auth_options():
    return True
def show_tutorial():
    panel_name = '青龙' if config['panel_type'] == 'qinglong' else '呆呆'
    sender.reply(f"""
=====老中医插件教程=====
当前模式: 🌐 提交至{panel_name}面板

1️⃣ {config['randomsigncommand']}
   将抓包到的 Authorization 值发送给机器人即可！
   系统会自动提取手机号并无损匹配旧数据。

2️⃣ {config['randomquerycommand']}
   实时查询老中医账号存活状态与当前账户余额。

3️⃣ {config['randommanagecommand']}
   续费、删除、修改备注。

4️⃣ 老中医清理 / 老中医授权 / 老中医广播
   清理过期并同步删除系统变量；
   管理员进行全局或个人独立授权(支持加减天数)；
   系统管理员向所有已授权用户发送广播通知。
==================""")

try:
    if sender.getImtype() == 'fake':
        clean_expired_accounts()

    elif re.search(r'(通知|广播)', usermessage or ''):
        notify_authorized_users()
    elif re.search(r'(通知|广播)', usermessage or ''):
        notify_authorized_users()
    elif '登录' in usermessage or '登陆' in usermessage:
        bindaccount()
    elif '管理' in usermessage:
       xy_manage()
    elif '查询' in usermessage:
        cxs()
    elif usermessage in ['老中医清理', '清理老中医']:
        clean_expired_accounts()
    elif '广播' in usermessage or '通知' in usermessage:
        notify_authorized_users()
    elif '授权' in usermessage:
        admin_auth_options()
    elif '教程' in usermessage:
        show_tutorial()

except Exception as e:
    logger.error(f"Error: {e}")
    sender.reply(f"❌ 系统错误: {e}")
