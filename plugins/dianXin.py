# [title: 电信]
# [name: dianXin]
# [language: python]
# [class: 任务]
# [author: sky2022]
# [version: v2.4]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(电信|dx)(登录|登陆)$|^登(录|陆)(电信|dx)$|^(电信|dx)(查询|管理)$|^(查询|管理)(电信|dx)$|^电信清理$|^电信$|^电信教程$|^电信同步$]
# [cron: 56 8,15 * * *]
# [icon: https://i.pinimg.com/564x/39/f2/20/39f2204f052bb3eeb89a7b6a93276cc0.jpg]
# [description: 介绍：电信金豆查询管理插件，支持账号管理，查询签到，金豆余额查询，本月话费抢购记录查询；登录格式：手机号#密码；V2.0:此版本更新适配了呆呆面板；V2.1:统一面板配置为面板类型+对接面板配置，并新增呆呆面板分组配置；V2.4:新增电信517活动查询]
# [depe: ["pycryptodome","requests","urllib3"]]


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
    'dd_dx_panel_type': form.string().title('对接面板类型').default('').description('填写你当前使用的面板类型，支持：青龙、青龙面板、QL、呆呆、呆呆面板、Daidai'),
    'dd_dx_panel_config': form.string().title('对接面板配置').default('').description('统一填写面板对接参数。青龙：Host丨ClientID丨ClientSecret；呆呆：Host丨AppKey丨AppSecret；分隔符使用中文丨'),
    'dd_dx_panel_group': form.string().title('对接面板分组').default('').description('仅呆呆面板生效。填写后新增或更新变量时会同步写入 group 字段；留空则不处理分组'),
    'dd_dx_dx_osname': form.string().title('面板变量名').default('').description('提交到面板中的电信变量名'),
})
_CONFIG_FIELD_MAP = {
    ('dd_dx', 'panel_type'): 'dd_dx_panel_type',
    ('dd_dx', 'panel_config'): 'dd_dx_panel_config',
    ('dd_dx', 'panel_group'): 'dd_dx_panel_group',
    ('dd_dx', 'dx_osname'): 'dd_dx_dx_osname',
}

import re
import os
import json
import time
import datetime
import requests
import base64
import random
import binascii
import ssl
import urllib3
import hashlib
from Crypto.Cipher import DES3, AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Util.Padding import pad, unpad
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl_ import create_urllib3_context
from datetime import datetime, timedelta
import urllib.parse
from decimal import Decimal

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()
uservalue = sg.bucketGet(bucket='dd_dx_user', key=userid)

DES_KEY = b'1234567`90koiuyhgtfrdews'
DES_IV = 8 * b'\0'
PUBLIC_KEY = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC+ugG5A8cZ3FqUKDwM57GM4io6JGcStivT8UdGt67PEOihLZTw3P7371+N47PrmsCpnTRzbTgcupKtUv8ImZalYk65dU8rjC/ridwhw9ffW2LBwvkEnDkkKKRi2liWIItDftJVBiWOh17o6gfbPoNrWORcAdcbpk2L+udld5kZNwIDAQAB
-----END PUBLIC KEY-----'''
PUBLIC_KEY_B64 = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDBkLT15ThVgz6/NOl6s8GNPofdWzWbCkWnkaAm7O2LjkM1H7dMvzkiqdxU02jamGRHLX/ZNMCXHnPcW/sDhiFCBN18qFvy8g6VYb9QtroI09e176s+ZCtiv7hbin2cCTj99iUpnEloZm19lwHyo69u5UMiPMpq0/XKBO8lYhN/gwIDAQAB
-----END PUBLIC KEY-----'''

MSG_TEMPLATES = {
    'config_error': "=====配置错误=====\n❌ {error}\n==================",
    'login_success': "=====电信账号绑定=====\n📱 绑定账号: {phone}\n🔐 授权状态: {status}\n⏰ 下一步: {next_step}\n==================",
    'auth_expired': "=====授权过期=====\n📱 账号: {phone}\n❌ 授权已过期\n💡 请及时续费\n==================",
    'query_result': "=====查询结果=====\n📱 账号: {phone}\n🔐 授权: {auth}\n🪙 金豆: {coin}\n📅 签到: {days}天\n🎯 今日: {today}\n==================",
    'operation_timeout': "⏰ 操作超时,已退出",
    'invalid_input': "❌ 输入无效",
    'no_accounts': "=====未绑定账号=====\n❌ 未找到任何账号信息\n💡 发送 {cmd} 绑定\n=================="
}

def normalize_panel_type(panel_type_value, legacy_use_daidai_value='false'):
    """统一解析面板类型，兼容新旧配置。"""
    value = str(panel_type_value or '').strip().lower()
    if value in ('呆呆', '呆呆面板', 'daidai', 'dd'):
        return 'daidai'
    if value in ('青龙', '青龙面板', 'qinglong', 'ql'):
        return 'qinglong'
    if value:
        return ''

    legacy_value = str(legacy_use_daidai_value or '').strip().lower()
    if legacy_value == 'true':
        return 'daidai'
    return 'qinglong'

def get_config():
    """获取配置信息"""
    panel_type = normalize_panel_type(
        sg.bucketGet('dd_dx', 'panel_type') or '',
        sg.bucketGet('dd_dx', 'use_daidai') or 'false'
    )
    if not panel_type:
        sender.reply(format_msg('config_error', error='对接面板类型填写无效\n请填写：青龙/青龙面板/QL 或 呆呆/呆呆面板/Daidai'))
        exit(0)

    panel_config = (sg.bucketGet('dd_dx', 'panel_config') or '').strip()
    legacy_ql_config = sg.bucketGet('dd_dx', 'dx_qlname') or ''
    legacy_dd_config = sg.bucketGet('dd_dx', 'dd_dx_ddname') or ''

    return {
        'osname': sg.bucketGet('dd_dx', 'dx_osname') or 'dd_dx_token',
        'qlname': panel_config or legacy_ql_config if panel_type == 'qinglong' else legacy_ql_config,
        'price': Decimal(sg.bucketGet('dd_dx', 'dxVipmoney') or '1'),
        'coin': int(sg.bucketGet('dd_dx', 'dxcoin') or '0'),
        'zsm': sg.bucketGet('dd_dx', 'zsm') or '',
        'use_ma_pay': ('2099-12-31' or 'false').lower() == 'true',
        'use_daidai': panel_type == 'daidai',
        'dd_dx_ddname': panel_config or legacy_dd_config if panel_type == 'daidai' else legacy_dd_config,
        'panel_group': (sg.bucketGet('dd_dx', 'panel_group') or '').strip()
    }

def format_msg(template, **kwargs):
    """格式化消息"""
    return MSG_TEMPLATES.get(template, template).format(**kwargs)

def mask_phone(phone):
    """手机号脱敏"""
    return phone[:3] + "****" + phone[7:]

def generate_qrcode(url):
    """将支付链接转为二维码图片URL"""
    try:
        encoded_url = urllib.parse.quote(url, safe='')
        return f"https://api.qrtool.cn/?text={encoded_url}"
    except Exception as e:
        print(f"生成二维码失败: {str(e)}")
        return None

def send_qrcode_image(pay_sender, qrcode_url, pay_type):
    """发送二维码图片给用户扫在线处理"""
    pay_type_names = {'alipay': '支付宝', 'wxpay': '微信', 'qqpay': 'QQ钱包'}
    pay_type_name = pay_type_names.get(pay_type, pay_type)
    try:
        pay_sender.replyImage(qrcode_url)
        if pay_type == 'qqpay':
            pay_sender.reply(f"请使用【{pay_type_name}】扫描上方二维码完成支付\nQQ支付打开图片若是黑屏，长按屏幕进行\"识别二维码\"即可！\n支付过程中输入'q'可取消支付")
        else:
            pay_sender.reply(f"请使用【{pay_type_name}】扫描上方二维码完成支付\n支付过程中输入'q'可取消支付")
    except:
        if pay_type == 'qqpay':
            pay_msg = f'请使用【{pay_type_name}】扫描下方二维码完成支付，支付过程中输入"q"可取消支付:\nQQ支付打开图片若是黑屏，长按屏幕进行"识别二维码"即可！\n[CQ:image,file={qrcode_url}]'
        else:
            pay_msg = f'请使用【{pay_type_name}】扫描下方二维码完成支付，支付过程中输入"q"可取消支付:\n[CQ:image,file={qrcode_url}]'
        pay_sender.reply(pay_msg)


def parse_accounts(uservalue):
    """解析账号列表"""
    if not uservalue:
        return []
    try:
        cleaned = uservalue.strip('[]').strip()
        if cleaned:
            accounts = [acc.strip().strip("'\"") for acc in cleaned.split(',')]
            return [acc for acc in accounts if acc]
    except:
        pass
    return []

def validate_input(value, max_val, input_type="数字"):
    """验证输入"""
    try:
        value = int(value)
        if value > max_val or value <= 0:
            sender.reply(f"❌ 请输入 1-{max_val} 之间的{input_type}")
            exit(0)
        return value
    except ValueError:
        sender.reply(f"❌ 请输入有效的{input_type}")
        exit(0)

def confirm_operation():
    """确认操作"""
    response = sender.input(120000, 1, False)
    if response in ['Y', 'y', '是']:
        return True
    elif response in ['n', 'N', '否']:
        return False
    elif not response:
        sender.reply(MSG_TEMPLATES['operation_timeout'])
        exit(0)
    else:
        sender.reply(MSG_TEMPLATES['invalid_input'])
        exit(0)

def encrypt_para(plaintext):
    """RSA加密参数"""
    if not isinstance(plaintext, str):
        plaintext = json.dumps(plaintext)
    public_key = RSA.import_key(PUBLIC_KEY)
    cipher = PKCS1_v1_5.new(public_key)
    key_size = public_key.size_in_bytes()
    max_chunk_size = key_size - 11
    plaintext_bytes = plaintext.encode()
    ciphertext = b''
    for i in range(0, len(plaintext_bytes), max_chunk_size):
        chunk = plaintext_bytes[i:i + max_chunk_size]
        encrypted_chunk = cipher.encrypt(chunk)
        ciphertext += encrypted_chunk
    return binascii.hexlify(ciphertext).decode()

def b64_encrypt(plaintext):
    """Base64加密"""
    public_key = RSA.import_key(PUBLIC_KEY_B64)
    cipher = PKCS1_v1_5.new(public_key)
    ciphertext = cipher.encrypt(plaintext.encode())
    return base64.b64encode(ciphertext).decode()

def des_encrypt(text):
    """DES3加密"""
    cipher = DES3.new(DES_KEY, DES3.MODE_CBC, DES_IV)
    ciphertext = cipher.encrypt(pad(text.encode(), DES3.block_size))
    return ciphertext.hex()

def des_decrypt(text):
    """DES3解密"""
    ciphertext = bytes.fromhex(text)
    cipher = DES3.new(DES_KEY, DES3.MODE_CBC, DES_IV)
    plaintext = unpad(cipher.decrypt(ciphertext), DES3.block_size)
    return plaintext.decode()

def aes_encrypt(data, key="34d7cb0bcdf07523"):
    """AES加密"""
    if isinstance(data, dict):
        data = json.dumps(data)
    key_bytes = key.encode('utf-8')
    data_bytes = data.encode('utf-8')
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    ct_bytes = cipher.encrypt(pad(data_bytes, AES.block_size))
    return ct_bytes.hex()

def encode_phone(text):
    """编码手机号"""
    return ''.join(chr(ord(char) + 2) for char in text)

def rsa_encrypt_long(plaintext):
    """处理超长文本的RSA加密函数 - 用于星播客"""
    key_content = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDIPOHtjs6p4sTlpFvrx+ESsYkEvyT4JB/dcEbU6C8+yclpcmWEvwZFymqlKQq89laSH4IxUsPJHKIOiYAMzNibhED1swzecH5XLKEAJclopJqoO95o8W63Euq6K+AKMzyZt1SEqtZ0mXsN8UPnuN/5aoB3kbPLYpfEwBbhto6yrwIDAQAB"
    res_key = "-----BEGIN PUBLIC KEY-----\n" + key_content + "\n-----END PUBLIC KEY-----"

    public_key = RSA.import_key(res_key)
    cipher = PKCS1_v1_5.new(public_key)

    key_size = public_key.size_in_bytes()
    max_chunk_size = key_size - 11

    if not isinstance(plaintext, bytes):
        plaintext = plaintext.encode('utf-8')

    encrypted_chunks = []
    for i in range(0, len(plaintext), max_chunk_size):
        chunk = plaintext[i:i + max_chunk_size]
        encrypted_chunk = cipher.encrypt(chunk)
        encrypted_chunks.append(encrypted_chunk)

    ciphertext = b"".join(encrypted_chunks)
    return base64.b64encode(ciphertext).decode('utf-8')

class DESAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        CIPHERS = 'DEFAULT@SECLEVEL=1'.split(':')
        random.shuffle(CIPHERS)
        self.CIPHERS = ':'.join(CIPHERS) + ':!aNULL:!eNULL:!MD5'
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=self.CIPHERS)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)

class QingLongManager:
    def __init__(self):
        self.config = get_config()
        self.use_daidai = self.config.get('use_daidai', False)
        self.url, self.token = self._get_connection()

    def _get_connection(self):
        """获取面板连接（支持青龙/呆呆面板）"""
        if self.use_daidai:
            dd_ddname = self.config.get('dd_dx_ddname', '')
            if not dd_ddname:
                sender.reply(format_msg('config_error', error='未配置呆呆面板信息\n请填写:\n• 对接面板类型: 呆呆\n• 对接面板配置: Host丨AppKey丨AppSecret'))
                exit(0)

            parts = dd_ddname.split('丨')
            if len(parts) != 3:
                sender.reply(format_msg('config_error', error=f'呆呆面板配置格式错误\n当前格式: {dd_ddname}\n正确格式: Host丨AppKey丨AppSecret'))
                exit(0)

            dd_url, app_key, app_secret = [p.strip() for p in parts]
            if not all([dd_url, app_key, app_secret]):
                sender.reply(format_msg('config_error', error='呆呆面板配置参数不完整'))
                exit(0)

            if not dd_url.startswith(('http://', 'https://')):
                sender.reply(format_msg('config_error', error=f'呆呆面板地址格式错误: {dd_url}'))
                exit(0)

            try:
                url = f'{dd_url}/api/open-api/token'
                data = {"app_key": app_key, "app_secret": app_secret}
                response = requests.post(url, json=data)
                if response.status_code == 200:
                    result = response.json()
                    access_token = result.get('data', {}).get('access_token')
                    if access_token:
                        return dd_url, access_token
                sender.reply(format_msg('config_error', error='获取呆呆面板Token失败'))
                exit(0)
            except Exception as e:
                sender.reply(format_msg('config_error', error=f'连接呆呆面板失败: {str(e)}'))
                exit(0)
        else:
            if not self.config['qlname']:
                sender.reply(format_msg('config_error', error='未配置青龙面板信息\n请填写:\n• 对接面板类型: 青龙\n• 对接面板配置: Host丨ClientID丨ClientSecret'))
                exit(0)

            parts = self.config['qlname'].split('丨')
            if len(parts) != 3:
                sender.reply(format_msg('config_error', error=f'青龙面板配置格式错误\n当前格式: {self.config["qlname"]}\n正确格式: Host丨ClientID丨ClientSecret'))
                exit(0)

            url, client_id, client_secret = [p.strip() for p in parts]
            if not all([url, client_id, client_secret]):
                sender.reply(format_msg('config_error', error='青龙配置参数不完整'))
                exit(0)

            try:
                token_url = f'{url}/open/auth/token?client_id={client_id}&client_secret={client_secret}'
                response = requests.get(token_url)
                if response.status_code == 200:
                    result = response.json()
                    if "token" in result.get('data', {}):
                        return url, result['data']['token']
                sender.reply(format_msg('config_error', error='获取青龙Token失败'))
                exit(0)
            except Exception as e:
                sender.reply(format_msg('config_error', error=f'连接青龙失败: {str(e)}'))
                exit(0)

    def _get_headers(self):
        """获取请求头"""
        return {
            "Authorization": f"Bearer {self.token}",
            "accept": "application/json",
            "Content-Type": "application/json"
        }

    def get_env_id(self, account):
        """获取环境变量ID（支持青龙/呆呆面板）"""
        headers = self._get_headers()

        if self.use_daidai:
            params = {"keyword": str(account), "page_size": 100}
            response = requests.get(f"{self.url}/api/envs", headers=headers, params=params).json()
            data_list = response.get('data', [])
            if isinstance(data_list, list):
                for env in data_list:
                    if env.get('name') == self.config['osname'] and str(account) in (env.get('remarks') or ''):
                        return env['id']
            return None
        else:
            url = f"{self.url}/open/envs"
            response = requests.get(url, headers=headers).json()

            if response['code'] == 200:
                for env in response['data']:
                    if env['name'] == self.config['osname'] and str(account) in (env.get('remarks') or ''):
                        return env['id']
            return None

    def add_or_update_env(self, account, value):
        """添加或更新环境变量（支持青龙/呆呆面板）"""
        env_id = self.get_env_id(account)
        auth_time = '2099-12-31' or str(datetime.now().date())
        mask_phone(account)

        data = {
            "value": value,
            "name": self.config['osname'],
            "remarks": f'电信:{account}丨用户:{userid}丨到期:{auth_time}丨电信管理'
        }

        headers = self._get_headers()

        if self.use_daidai:
            if self.config.get('panel_group'):
                data["group"] = self.config['panel_group']
            if env_id:
                requests.put(f"{self.url}/api/envs/{env_id}", headers=headers, json=data)
            else:
                requests.post(f"{self.url}/api/envs", headers=headers, json=data)
        else:
            if env_id:
                data["id"] = env_id
                requests.put(f"{self.url}/open/envs", headers=headers, json=data)
            else:
                requests.post(f"{self.url}/open/envs", headers=headers, json=[data])

    def delete_env(self, env_id):
        """删除环境变量（支持青龙/呆呆面板）"""
        if env_id:
            headers = self._get_headers()
            if self.use_daidai:
                requests.delete(f"{self.url}/api/envs/{env_id}", headers=headers)
            else:
                url = f"{self.url}/open/envs"
                requests.delete(url, headers=headers, json=[env_id])

class TelecomAPI:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Linux; Android 13; 22081212C) AppleWebKit/537.36 Chrome/104.0.5112.97 Mobile Safari/537.36"
        })
        self.session.mount('https://', DESAdapter())
        self.session.verify = False

    def login(self, phone, password):
        """账号登录"""
        alphabet = 'abcdef0123456789'
        uuid_parts = [''.join(random.sample(alphabet, 8)), ''.join(random.sample(alphabet, 4)),
                     '4' + ''.join(random.sample(alphabet, 3)), ''.join(random.sample(alphabet, 4)),
                     ''.join(random.sample(alphabet, 12))]
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        auth_cipher = f'iPhone 14 15.4.{uuid_parts[0]}{uuid_parts[1]}{phone}{timestamp}{password[:6]}0$$$0.'

        payload = {
            "headerInfos": {
                "code": "userLoginNormal", "timestamp": timestamp, "broadAccount": "", "broadToken": "",
                "clientType": "#11.3.0#channel50#iPhone 14 Pro Max#", "shopId": "20002", "source": "110003",
                "sourcePassword": "Sid98s", "token": "", "userLoginName": encode_phone(phone)
            },
            "content": {
                "attach": "test",
                "fieldData": {
                    "loginType": "4", "accountType": "", "loginAuthCipherAsymmertric": b64_encrypt(auth_cipher),
                    "deviceUid": uuid_parts[0] + uuid_parts[1] + uuid_parts[2], "phoneNum": encode_phone(phone),
                    "isChinatelecom": "0", "systemVersion": "15.4.0", "authentication": encode_phone(password)
                }
            }
        }

        try:
            resp = self.session.post('https://appgologin.189.cn:9031/login/client/userLoginNormal',
                                   json=payload, timeout=15)
            result = resp.json()
            login_data = result.get('responseData', {}).get('data')
            if login_data and login_data.get('loginSuccessResult'):
                return login_data['loginSuccessResult']
        except Exception as e:
            print(f"登录异常: {e}")
        return None

    def get_ticket(self, phone, user_id, token):
        """获取ticket"""
        url = 'https://appgologin.189.cn:9031/map/clientXML'
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        target_id = des_encrypt(user_id)

        data = f'<Request><HeaderInfos><Code>getSingle</Code><Timestamp>{timestamp}</Timestamp><BroadAccount></BroadAccount><BroadToken></BroadToken><ClientType>#9.6.1#channel50#iPhone 14 Pro Max#</ClientType><ShopId>20002</ShopId><Source>110003</Source><SourcePassword>Sid98s</SourcePassword><Token>{token}</Token><UserLoginName>{phone}</UserLoginName></HeaderInfos><Content><Attach>test</Attach><FieldData><TargetId>{target_id}</TargetId><Url>4a6862274835b451</Url></FieldData></Content></Request>'

        try:
            headers = {
                'User-Agent': 'CtClient;10.4.1;Android;13;22081212C;NTQzNzgx!#!MTgwNTg5',
                'Content-Type': 'application/xml'
            }
            resp = self.session.post(url, data=data, headers=headers, timeout=15)
            ticket_match = re.findall('<Ticket>(.*?)</Ticket>', resp.text)
            if ticket_match:
                return des_decrypt(ticket_match[0])
        except Exception as e:
            print(f"获取ticket异常: {e}")
        return None

    def get_sign(self, ticket):
        """获取sign"""
        url = f'https://wappark.189.cn/jt-sign/ssoHomLogin?ticket={ticket}'
        try:
            result = self.session.get(url, timeout=15).json()
            if result.get('resoultCode') == '0':
                return result.get('sign'), result.get('accId')
        except Exception as e:
            print(f"获取sign异常: {e}")
        return None, None

    def query_account_info(self, phone, password):
        """查询账号信息"""
        try:
            login_result = self.login(phone, password)
            if not login_result:
                return {"status": "error", "message": "登录失败"}

            ticket = self.get_ticket(phone, login_result['userId'], login_result['token'])
            if not ticket:
                return {"status": "error", "message": "获取ticket失败"}

            sign, acc_id = self.get_sign(ticket)
            if not sign:
                return {"status": "error", "message": "获取sign失败"}

            self.session.headers['sign'] = sign

            coin_result = self._query_coin(phone)
            sign_result = self._query_sign_days(phone)
            sign_status = self._check_sign_status(phone)
            pet_result = self._query_pet_info(phone)

            return {
                "status": "success", "coin": coin_result.get("coin", 0), "sign_days": sign_result.get("days", 0),
                "today_signed": sign_status.get("today_signed", False), "sign_message": sign_status.get("message", ""),
                "pet_level": pet_result.get("level", 0), "pet_growth": pet_result.get("growth_value", 0),
                "pet_full_growth": pet_result.get("full_growth_value", 0), "pet_progress": pet_result.get("progress_percentage", 0)
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _query_coin(self, phone):
        """查询金豆"""
        try:
            url = 'https://wappark.189.cn/jt-sign/api/home/userCoinInfo'
            resp = self.session.post(url, json={"para": encrypt_para({"phone": phone})}, timeout=15)
            data = resp.json()
            return {"status": "success", "coin": data.get("totalCoin", 0)} if data.get('code') != 401 else {"status": "error", "message": "sign过期", "coin": 0}
        except Exception as e:
            return {"status": "error", "message": str(e), "coin": 0}

    def _query_sign_days(self, phone):
        """查询签到天数"""
        try:
            now = datetime.now()
            value = {"phone": phone, "checkDate": f"{now.year}-{now.month:02d}"}
            url = 'https://wappark.189.cn/jt-sign/api/signInfo'
            resp = self.session.post(url, json={"para": encrypt_para(value)}, timeout=15)
            data = resp.json()
            if data.get("resoultCode") == "0":
                signed_days = [item for item in data["data"]["signInfo"] if item.get("state") == "Y"]
                return {"status": "success", "days": len(signed_days)}
            return {"status": "error", "message": data.get("message", "未知错误"), "days": 0}
        except Exception as e:
            return {"status": "error", "message": str(e), "days": 0}

    def _check_sign_status(self, phone):
        """检查签到状态"""
        try:
            timestamp = int(time.time() * 1000)
            value = {"phone": phone, "sysType": "", "date": str(timestamp)}
            url = 'https://wappark.189.cn/jt-sign/webSign/sign'
            resp = self.session.post(url, json={"encode": aes_encrypt(value)}, timeout=15)
            data = resp.json()

            msg = data.get("data", {}).get("msg", "")
            if "已签到" in msg or "不能重复签到" in msg:
                return {"status": "success", "today_signed": True, "message": msg}
            elif "签到成功" in msg:
                return {"status": "success", "today_signed": False, "message": msg}
            return {"status": "success", "today_signed": False, "message": msg}
        except Exception as e:
            return {"status": "error", "today_signed": False, "message": str(e)}

    def _query_pet_info(self, phone):
        """查询宠物信息"""
        try:
            url = 'https://wappark.189.cn/jt-sign/paradise/getParadiseInfo'
            resp = self.session.post(url, json={'para': encrypt_para({'phone': phone})}, timeout=15)
            data = resp.json()

            if data.get('resoultCode') == "0":
                level_info = data.get('userInfo', {}).get('levelInfoMap', {})
                level, growth, full_growth = level_info.get('level', 0), level_info.get('growthValue', 0), level_info.get('fullGrowthCoinValue', 0)
                return {
                    "status": "success", "level": level, "growth_value": growth, "full_growth_value": full_growth,
                    "progress_percentage": round((growth / full_growth * 100), 1) if full_growth > 0 else 0
                }
            return {"status": "error", "message": data.get('msg', '未知错误')}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_xbk_usercode(self, phone, ticket):
        """获取星播客usercode"""
        try:
            url = "https://xbk.189.cn/xbkapi/api/auth/jump"
            params = {
                "userID": ticket,
                "version": "9.3.3",
                "type": "room",
                "l": "renwu"
            }
            headers = {
                "User-Agent": "Mozilla/5.0 (Linux; U; Android 12; zh-cn; ONEPLUS A9000 Build/QKQ1.190716.003) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1"
            }

            response = self.session.get(url, params=params, headers=headers, allow_redirects=False)

            if response.status_code not in (301, 302, 303, 307, 308):
                return None

            location_header = response.headers.get("Location")
            if not location_header:
                return None

            from urllib.parse import urlparse, parse_qs
            parsed = urlparse(location_header)
            query_params = parse_qs(parsed.query)

            usercode_list = query_params.get("usercode", [])
            if not usercode_list:
                return None

            return usercode_list[0]

        except Exception as e:
            print(f"获取星播客usercode错误: {str(e)}")
            return None

    def get_xbk_usertoken(self, phone, usercode):
        """获取星播客usertoken"""
        try:
            url = "https://xbk.189.cn/xbkapi/api/auth/userinfo/codeToken"
            data = {"usercode": usercode}
            headers = {
                "User-Agent": "Mozilla/5.0 (Linux; U; Android 12; zh-cn; ONEPLUS A9000 Build/QKQ1.190716.003) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1"
            }

            response = self.session.post(url, data=data, headers=headers)
            response_json = response.json()

            if 'data' in response_json and 'token' in response_json['data']:
                token = response_json['data']['token']
                return token
            else:
                return None

        except Exception as e:
            print(f"获取星播客usertoken错误: {str(e)}")
            return None

    def get_xbk_win_list(self, phone, token):
        """查询星播客中奖记录"""
        try:
            url = "https://xbk.189.cn/xbkapi/active/v2/lottery/getMyWinList?page=1&give_status=200&activeCode="

            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; U; Android 12; zh-cn; ONEPLUS A9000 Build/QKQ1.190716.003) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1',
                'Authorization': 'Bearer ' + rsa_encrypt_long(token)
            }

            response = self.session.get(url, headers=headers)
            response_text = response.text
            result = json.loads(response_text)

            if 'data' not in result:
                return []

            items = result.get('data', [])
            return items

        except Exception as e:
            print(f"查询星播客奖品错误: {e}")
            return []


def _517_get_set_cookie_header(response):
    set_cookie = response.headers.get("Set-Cookie", "")
    raw_headers = getattr(getattr(response, "raw", None), "headers", None)
    if raw_headers:
        get_all = getattr(raw_headers, "get_all", None) or getattr(raw_headers, "getlist", None)
        if get_all:
            cookies = get_all("Set-Cookie")
            if cookies:
                set_cookie = "; ".join(cookies)
    return set_cookie

def _517_extract_reqparam(location):
    match = re.search(r"[?&]reqparam=([^&]+)", location or "")
    if not match:
        return ""
    return urllib.parse.unquote(match.group(1))

def _517_extract_newmallsession(set_cookie):
    match = re.search(r"(newmallsession=[^;]+;)", set_cookie or "")
    if not match:
        return ""
    return match.group(1)

def _517_get_query_param(url, key):
    parsed_url = urllib.parse.urlparse(url or "")
    query = urllib.parse.parse_qs(parsed_url.query, keep_blank_values=True)
    values = query.get(key)
    return values[0] if values else ""

def _517_normalize_cookie(cookie):
    return (cookie or "").strip().rstrip(";")

def _517_build_api_context(newmallsession, referer):
    token = _517_get_query_param(referer, "Token")
    channel = _517_get_query_param(referer, "channel") or "HGOKHD"
    cookie = _517_normalize_cookie(newmallsession)
    return {
        "channel": channel,
        "token": token,
        "referer": referer,
        "cookie": cookie,
        "headers": {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "appcode": "HGOKHD",
            "appCode": "HGOKHD",
            "Connection": "keep-alive",
            "Content-Type": "application/json;charset=UTF-8",
            "Cookie": cookie,
            "Host": "apps.telefen.com",
            "Referer": referer,
            "sec-ch-ua": "\"Google Chrome\";v=\"147\", \"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"147\"",
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "\"iOS\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "ssotoken": token,
            "SSOToken": token,
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1",
        },
    }

CARD_PIECES_517 = [
    (10000, "天翼云盘"),
    (10001, "天翼智铃"),
    (10002, "天翼智屏"),
    (10003, "通讯助理"),
    (10004, "云智手机"),
    (10005, "直连卫星"),
]

def _517_parse_piece_collection(data):
    biz_data = data.get("data") if isinstance(data, dict) else {}
    if not isinstance(biz_data, dict):
        biz_data = {}
    piece_list = biz_data.get("pieceList", []) or []
    piece_map = {}
    for piece in piece_list:
        if not isinstance(piece, dict):
            continue
        piece_id = int(piece.get("pieceId", 0) or 0)
        valid_count = int(piece.get("validPieceCount", 0) or 0)
        piece_map[piece_id] = {
            "pieceId": piece_id,
            "pieceName": piece.get("pieceName", ""),
            "validPieceCount": valid_count,
        }
    cards = []
    missing = []
    for piece_id, name in CARD_PIECES_517:
        item = piece_map.get(piece_id, {})
        available_count = int(item.get("validPieceCount", 0) or 0)
        cards.append({
            "pieceId": piece_id,
            "pieceName": item.get("pieceName") or name,
            "availableCount": available_count,
        })
        if available_count <= 0:
            missing.append(name)
    return {
        "cards": cards,
        "missing": missing,
        "is_all_collected": len(missing) == 0,
    }

def query_517_activity_status(phone, password, telecom_api):
    """查询517活动状态，返回结构化结果"""
    try:
        login_result = telecom_api.login(phone, password)
        if not login_result:
            return {"status": "error", "message": "登录失败"}

        ticket = telecom_api.get_ticket(phone, login_result['userId'], login_result['token'])
        if not ticket:
            return {"status": "error", "message": "获取ticket失败"}

        session = requests.Session()
        session.mount("https://", DESAdapter())
        session.verify = False
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Linux; Android 13; 22081212C Build/TKQ1.220829.002) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.97 Mobile Safari/537.36"
        })

        params = {
            "channel": "HGOKHD",
            "action": "2",
            "rdurl": "https://apps.telefen.com/mallactive/ck517?channel=HGOKHD",
            "promoid": "f15c4b971ecfa50b",
            "ticket": ticket,
            "utm_scha": "utm_ch-010001002009.utm_sch-hg_sy_yxtc-1.utm_af-1000000037.utm_as-456876200001.utm_sd1-S0076579",
        }
        headers = {
            "User-Agent": "CtClient;13.2.0;Android;14;22021211RC;",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Upgrade-Insecure-Requests": "1",
            "X-Requested-With": "com.ct.client",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
        }
        response = session.get(
            "https://apps.telefen.com/middleparse/api/access/ticket",
            params=params,
            headers=headers,
            allow_redirects=False,
            timeout=15,
        )

        if response.status_code not in (301, 302, 303, 307, 308):
            return {"status": "error", "message": f"517活动入口异常: {response.status_code}"}

        set_cookie = _517_get_set_cookie_header(response)
        location = response.headers.get("Location", "")
        reqparam = _517_extract_reqparam(location)
        newmallsession = _517_extract_newmallsession(set_cookie)

        merchants_location = ""
        if reqparam:
            try:
                dock_resp = session.get(
                    location if location else "https://m.telefen.com/MobileSSOv2/MerchantsDock.aspx",
                    headers=headers,
                    allow_redirects=False,
                    timeout=15,
                )
                merchants_location = dock_resp.headers.get("Location", "")
            except Exception:
                pass

        api_context = _517_build_api_context(newmallsession, merchants_location)
        if not api_context.get("token"):
            return {"status": "error", "message": "517活动Token获取失败"}

        try:
            page_headers = {
                "User-Agent": api_context["headers"]["User-Agent"],
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Cookie": api_context["headers"]["Cookie"],
                "Referer": location,
            }
            page_resp = session.get(
                api_context["referer"],
                headers=page_headers,
                allow_redirects=True,
                timeout=15,
            )
            page_set_cookie = _517_get_set_cookie_header(page_resp)
            page_newmallsession = _517_extract_newmallsession(page_set_cookie)
            if page_newmallsession:
                cookie = _517_normalize_cookie(page_newmallsession)
                api_context["cookie"] = cookie
                api_context["headers"]["Cookie"] = cookie
        except Exception:
            pass

        task_params = {
            "channel": api_context["channel"],
            "noload": "true",
            "activeCode": "2026517",
        }
        task_resp = session.get(
            "https://apps.telefen.com/mallactive/api/v26517/activity/home",
            params=task_params,
            headers=api_context["headers"],
            timeout=15,
        )
        try:
            task_data = task_resp.json()
        except Exception:
            task_data = None

        task_list = []
        unfinished_count = 0
        finished_count = 0
        if isinstance(task_data, dict) and task_data.get("errCode") == "0000":
            biz_data = task_data.get("data") or {}
            raw_tasks = biz_data.get("taskList", []) or [] if isinstance(biz_data, dict) else []
            for task in raw_tasks:
                if not isinstance(task, dict):
                    continue
                task_name = task.get("taskName", "")
                is_finished = task.get("isFinished", 0)
                completed_times = task.get("completedTimes", 0)
                max_times = task.get("maxTimes", 0)
                task_list.append({
                    "name": task_name,
                    "finished": is_finished == 1,
                    "progress": f"{completed_times}/{max_times}",
                })
                if is_finished == 1:
                    finished_count += 1
                else:
                    unfinished_count += 1

        piece_params = {"gameId": "10000"}
        piece_resp = session.get(
            "https://apps.telefen.com/mallactive/api/fragment/getMyPieceList",
            params=piece_params,
            headers=api_context["headers"],
            timeout=15,
        )
        try:
            piece_data = piece_resp.json()
        except Exception:
            piece_data = None

        total_chance_count = 0
        collection = {"cards": [], "missing": [], "is_all_collected": False}
        if isinstance(piece_data, dict):
            biz_data = piece_data.get("data") or {}
            if isinstance(biz_data, dict):
                total_chance_count = biz_data.get("totalChanceCount", 0) or 0
            collection = _517_parse_piece_collection(piece_data)

        has_composite = False
        try:
            comp_headers = dict(api_context["headers"])
            comp_headers["Origin"] = "https://apps.telefen.com"
            comp_resp = session.post(
                "https://apps.telefen.com/mallactive/api/fragment/getCompositeRecord",
                json={"gameId": "10000"},
                headers=comp_headers,
                timeout=15,
            )
            comp_data = comp_resp.json()
            comp_biz = comp_data.get("data") if isinstance(comp_data, dict) else None
            if isinstance(comp_biz, dict) and (
                comp_biz.get("commodityName") or comp_biz.get("compositeRecordId") is not None
                or comp_biz.get("id") is not None or comp_biz.get("compositeTime")
            ):
                has_composite = True
        except Exception:
            pass

        return {
            "status": "success",
            "task_list": task_list,
            "finished_count": finished_count,
            "unfinished_count": unfinished_count,
            "total_chance_count": total_chance_count,
            "collection": collection,
            "has_composite": has_composite,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


class PaymentHandler:
    def __init__(self):
        self.config = get_config()

    def process_payment(self, months, accounts_count=1, account=None):
        return True
    def _get_ma_pay_config(self):
        return {}

    def _process_free_auth(self, months, account=None):
        return True

    def _show_payment_options(self, total_money, total_coins, accounts_count, months, account=None, ma_pay_config=None):
        return True

    def _process_ma_pay(self, total_money, months, account=None, ma_pay_config=None):
        """在线处理"""
        if not ma_pay_config:
            sender.reply("❌ 在线处理配置异常，请检查配置")
            return False

        out_trade_no = f"DX{int(time.time())}{userid}"
        params = {
            'pid': ma_pay_config['pid'],
            'type': (ma_pay_config.get('type') or 'alipay,wxpay,qqpay').split(',')[0],
            'out_trade_no': out_trade_no,
            'name': f"{senderID}-电信授权-{str(total_money)}",
            'money': str(total_money),
            'param': userid
        }
        if ma_pay_config.get('notify_url'):
            params['notify_url'] = ma_pay_config['notify_url']
        if ma_pay_config.get('return_url'):
            params['return_url'] = ma_pay_config['return_url']

        params = {k: v for k, v in params.items() if v}
        sorted_params = sorted(params.items(), key=lambda x: x[0])
        sign_str = "&".join([f"{k}={v}" for k, v in sorted_params])
        sign = hashlib.md5((sign_str + ma_pay_config['key']).encode()).hexdigest().lower()
        params['sign'] = sign
        params['sign_type'] = 'MD5'

        gateway = ma_pay_config['gateway'].rstrip('/')
        submit_url = gateway + '/mapi.php'

        try:
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            response = requests.post(submit_url, data=params, headers=headers, timeout=10)
            if response.status_code != 200:
                sender.reply(f"❌ 创建支付订单失败，HTTP状态码: {response.status_code}")
                return False

            result = response.json()
            if result.get('code') != 1:
                sender.reply(f"❌ 创建支付订单失败: {result.get('msg', '未知错误')}")
                return False

            pay_url = result.get('payurl', '')
            if not pay_url:
                sender.reply("❌ 未获取到支付链接")
                return False

            qrcode_url = generate_qrcode(pay_url)
            pay_type = (ma_pay_config.get('type') or 'alipay,wxpay,qqpay').split(',')[0]
            if qrcode_url:
                send_qrcode_image(sender, qrcode_url, pay_type)
            else:
                sender.reply(f"=====在线处理=====\n🎫 商品: 电信插件授权\n💰 金额: {total_money}元\n⏰ 有效期: 5分钟\n------------------\n二维码生成失败，请点击链接完成支付:\n{pay_url}\n==================")

            for _ in range(60):
                result_input = sender.listen(5000)
                if result_input == 'q' or result_input == 'Q':
                    sender.reply("✅ 已取消支付")
                    return False

                check_url = gateway
                if '/xpay/epay/api.php' not in check_url:
                    check_url = f"{check_url}/xpay/epay/api.php"
                check_params = {
                    'act': 'order',
                    'pid': ma_pay_config['pid'],
                    'key': ma_pay_config['key'],
                    'out_trade_no': out_trade_no
                }
                try:
                    check_resp = requests.get(check_url, params=check_params, timeout=10)
                    check_result = check_resp.json()
                    if check_result.get('code') == 1 and check_result.get('status') == 1:
                        if account:
                            current_auth = '2099-12-31'
                            current_time = datetime.now().strftime("%Y-%m-%d")
                            if current_auth and current_auth > current_time:
                                auth_date = datetime.strptime(current_auth, "%Y-%m-%d")
                            else:
                                auth_date = datetime.now()
                            new_expiry = auth_date + timedelta(days=months * 30)
                            return new_expiry.strftime("%Y-%m-%d"), float(total_money), datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "在线处理"
                        current_date = datetime.now().date()
                        new_expiry = current_date + timedelta(days=months * 30)
                        return str(new_expiry), float(total_money), datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "在线处理"
                except:
                    continue

            sender.reply("❌ 支付超时,请重新发起支付!")
            return False
        except Exception as e:
            sender.reply(f"❌ 支付请求失败: {str(e)}")
            return False

    def _process_wechat_pay(self, total_money, accounts_count, months, account=None):
        return True

    def _process_coin_pay(self, total_coins, usercoin, months, account=None):
        return True

    def _parse_payment_result(self, result):
        return True

class TelecomManager:
    def __init__(self):
        self.ql = QingLongManager()
        self.api = TelecomAPI()
        self.payment = PaymentHandler()
        self.today = str(datetime.now().date())

    def login_account(self):
        """账号登录"""
        guide = f"=====电信账号登录=====\n请按格式输入: 手机号#密码\n🔰 支持批量登录，一行一个账号\n回复'q'退出操作\n=================="
        sender.reply(guide)

        account_info = sender.input(120000, 1, False)
        if not account_info or account_info.lower() == 'q':
            sender.reply("✅ 已取消登录")
            exit(0)

        lines = account_info.strip().split('\n')
        success_count, fail_count = 0, 0
        accounts = parse_accounts(uservalue) or []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            parts = line.split('#')
            if len(parts) != 2:
                fail_count += 1
                continue

            phone, password = parts
            if not re.match(r'^1[3-9]\d{9}$', phone):
                fail_count += 1
                continue

            if self.api.login(phone, password):
                sg.bucketSet('dd_dx_token', phone, line)
                if phone not in accounts:
                    accounts.append(phone)
                success_count += 1
            else:
                fail_count += 1

        if accounts:
            sg.bucketSet('dd_dx_user', userid, str(accounts))

        if len(lines) > 1:
            sender.reply(f"=====批量登录结果=====\n✅ 成功: {success_count}个账号\n❌ 失败: {fail_count}个账号\n💡 发送 电信管理 可管理账号\n==================")
        elif success_count == 1:
            phone = lines[0].split('#')[0]
            auth_status, auth_time = check_auth_status(phone)
            next_step = '发送 电信管理 可管理账号' if auth_status == "✅ 已授权" else '发送 电信管理 可进行授权'
            sender.reply(format_msg('login_success', phone=mask_phone(phone), status=auth_status, next_step=next_step))
        else:
            sender.reply("=====登录失败=====\n❌ 所有账号登录均失败\n==================")

    def manage_accounts(self):
        """账号管理"""
        accounts = parse_accounts(uservalue)
        if not accounts:
            sender.reply(format_msg('no_accounts', cmd='电信登录'))
            return

        menu_items = ["=====电信账号管理=====", "[0] 全部账号授权", "[99] 删除所有账号"]

        for i, account in enumerate(accounts, 1):
            auth_status, auth_time = check_auth_status(account)
            menu_items.append(f"[{i}] 账号: {mask_phone(account)}")
            menu_items.append(f"    授权: {auth_status} 到期: {auth_time}")

        menu_items.extend(["选择要管理的账号(输入数字)", "回复'q'退出操作", "=================="])
        sender.reply("\n".join(menu_items))

        choice = sender.input(120000, 1, False)
        if not choice or choice.lower() == 'q':
            sender.reply('✅ 已退出管理')
            return

        if choice == '0':
            self._batch_authorize(accounts)
        elif choice == '99':
            self._delete_all_accounts(accounts)
        else:
            try:
                index = int(choice) - 1
                if 0 <= index < len(accounts):
                    self._single_account_operation(accounts[index])
                else:
                    sender.reply("❌ 无效的账号编号")
            except ValueError:
                sender.reply("❌ 请输入有效的数字")

    def _batch_authorize(self, accounts):
        return True

    def _delete_all_accounts(self, accounts):
        """删除所有账号"""
        sender.reply("=====危险操作=====\n⚠️ 即将删除所有绑定的账号\n此操作不可恢复！\n确认删除? (Y/N)\n==================")

        if confirm_operation():
            try:
                for account in accounts:
                    env_id = self.ql.get_env_id(account)
                    if env_id:
                        self.ql.delete_env(env_id)
                    sg.bucketDel('dd_dx_token', account)
                    True

                sg.bucketDel('dd_dx_user', userid)
                sender.reply("=====删除完成=====\n✅ 已删除所有账号信息\n💡 如需重新使用，请重新绑定账号\n==================")
            except Exception as e:
                sender.reply(f"删除失败: {str(e)}")
        else:
            sender.reply("✅ 已取消删除")

    def _single_account_operation(self, account):
        """单账号操作"""
        auth_status, auth_time = check_auth_status(account)
        menu = f"=====账号操作菜单=====\n📱 选中账号: {mask_phone(account)}\n🔐 授权状态: {auth_status}\n📅 到期时间: {auth_time}\n[1] 授权续费\n[2] 删除账号\n[3] 查询信息\n选择操作(输入数字):\n=================="
        sender.reply(menu)

        operation = sender.input(120000, 1, False)
        if not operation:
            return

        if operation == '1':
            self._authorize_single_account(account)
        elif operation == '2':
            self._delete_single_account(account)
        elif operation == '3':
            self._query_single_account(account)
        else:
            sender.reply("❌ 无效的操作选项")

    def _authorize_single_account(self, account):
        return True

    def _delete_single_account(self, account):
        """删除单账号"""
        sender.reply(f"=====删除账号=====\n⚠️ 即将删除账号: {mask_phone(account)}\n此操作不可恢复！\n确认删除? (Y/N)\n==================")

        if confirm_operation():
            try:
                env_id = self.ql.get_env_id(account)
                if env_id:
                    self.ql.delete_env(env_id)

                sg.bucketDel('dd_dx_token', account)
                True

                accounts = parse_accounts(uservalue)
                accounts.remove(account)
                if accounts:
                    sg.bucketSet('dd_dx_user', userid, str(accounts))
                else:
                    sg.bucketDel('dd_dx_user', userid)

                sender.reply(f"=====删除成功=====\n✅ 已删除账号: {mask_phone(account)}\n==================")
            except Exception as e:
                sender.reply(f"删除失败: {str(e)}")
        else:
            sender.reply("✅ 已取消删除")

    def _query_single_account(self, account):
        """查询单账号"""
        auth_status, auth_time = check_auth_status(account)
        if auth_status != "✅ 已授权":
            sender.reply(f"=====账号未授权=====\n📱 账号: {mask_phone(account)}\n🔐 授权: {auth_status}\n⏰ 到期: {auth_time}\n⚠️ 该账号未授权或已过期\n💡 发送 电信管理 进行授权\n==================")
            return

        token = sg.bucketGet('dd_dx_token', account)
        if not token:
            sender.reply("❌ 账号信息不完整")
            return

        try:
            phone, password = token.split('#')

            sender.reply(f"""
=====账号查询选项=====
📱 账号: {mask_phone(account)}
🔐 授权状态: ✅ 已授权
⏰ 到期时间: {auth_time}

🔍 查询类型:
  [1] 基础信息查询
  [2] 本月话费抢购查询
  [3] 517活动查询

💡 请选择查询类型:
==================""")

            query_choice = sender.input(60000, 1, False)
            if not query_choice:
                sender.reply("⏰ 操作超时")
                return

            if query_choice == '1':
                result = self.api.query_account_info(phone, password)

                if result["status"] == "success":
                    today_sign = "✅" if result.get('today_signed') else "❌"
                    pet_level = result.get('pet_level', 0)
                    pet_progress = result.get('pet_progress', 0)

                    info_msg = f"""
=====基础信息查询结果=====
📱 账号: {mask_phone(account)}
🔐 授权状态: ✅ 已授权
⏰ 到期时间: {auth_time}

📊 账号数据:
   🪙 金豆数量: {result.get('coin', 0)}
   📅 本月签到: {result.get('sign_days', 0)}天
   🎯 今日签到: {today_sign}
   🐾 宠物等级: Lv.{pet_level}
   📈 升级进度: {result.get('pet_growth', 0)}/{result.get('pet_full_growth', 0)} ({pet_progress}%)
=================="""
                else:
                    info_msg = f"""
=====查询失败=====
📱 账号: {mask_phone(account)}
🔐 授权: ✅ 已授权
⏰ 到期: {auth_time}
❌ 错误: {result.get('message', '未知错误')}
💡 请检查账号状态或重新绑定
=================="""
                sender.reply(info_msg)

            elif query_choice == '2':
                result = self._query_single_payment_record(phone, password)

                if result["status"] == "success":
                    data = result["data"]
                    stats = data["stats"]

                    detail_msg = f"""
=====本月话费抢购查询结果=====
📱 账号: {mask_phone(account)}
🔐 授权状态: ✅ 已授权
⏰ 到期时间: {auth_time}

💰 话费统计:
   🪙 金豆抢兑: {stats['total_coin']:.2f}元 ({stats['coin_count']}次)
   🎁 等级权益: {stats['total_rights']:.2f}元 ({stats['rights_count']}次)
   🎯 抽奖获得: {stats['total_prize']:.2f}元 ({stats['prize_count']}次)
   🌟 星播客: {stats.get('total_xbk', 0):.2f}元 ({stats.get('xbk_count', 0)}次)
   📊 总计: {stats['total_amount']:.2f}元 ({stats['total_count']}次)"""

                    if stats['total_count'] > 0:
                        detail_msg += "\n\n📋 本月记录:"
                        all_records = []
                        all_records.extend(data['coin_payments'])
                        all_records.extend(data['rights_payments'])
                        all_records.extend(data['prize_payments'])
                        all_records.extend(data.get('xbk_payments', []))

                        all_records.sort(key=lambda x: x['date'], reverse=True)
                        for j, record in enumerate(all_records[:5], 1):
                            date_str = record['date'][:10] if record['date'] else '未知'
                            detail_msg += f"\n   {j}. {date_str} {record['title']} ({record['amount']:.2f}元)"

                    detail_msg += "\n=================="
                    sender.reply(detail_msg)

                else:
                    sender.reply(f"""
=====话费抢购查询失败=====
📱 账号: {mask_phone(account)}
🔐 授权: ✅ 已授权
⏰ 到期: {auth_time}
❌ 错误: {result.get('message', '未知错误')}
==================""")
            elif query_choice == '3':
                sender.reply(f"=====517活动查询中=====\n📱 账号: {mask_phone(account)}\n⏳ 正在查询517活动状态...\n==================")
                result = query_517_activity_status(phone, password, self.api)

                if result["status"] == "success":
                    task_info = ""
                    if result.get("task_list"):
                        task_info = f"\n📋 任务状态: 已完成{result['finished_count']}个 / 未完成{result['unfinished_count']}个"
                        for task in result["task_list"]:
                            status_icon = "✅" if task["finished"] else "❌"
                            task_info += f"\n   {status_icon} {task['name']} ({task['progress']})"
                    else:
                        task_info = "\n📋 任务状态: 暂无任务数据"

                    collection = result.get("collection", {})
                    card_info = "\n\n🃏 卡片收集:"
                    for card in collection.get("cards", []):
                        count = card.get("availableCount", 0)
                        icon = "✅" if count > 0 else "❌"
                        card_info += f"\n   {icon} {card['pieceName']} x{count}"

                    missing = collection.get("missing", [])
                    if missing:
                        card_info += f"\n   ⚠️ 缺少: {'、'.join(missing)}"
                    else:
                        card_info += "\n   🎉 已集齐所有卡片！"

                    extra_info = f"\n\n🎰 可用抽奖次数: {result.get('total_chance_count', 0)}"
                    if result.get("has_composite"):
                        extra_info += "\n🏆 合成状态: ✅ 已完成合成"
                    else:
                        if collection.get("is_all_collected"):
                            extra_info += "\n🏆 合成状态: 🟡 卡片已集齐，可合成"
                        else:
                            extra_info += "\n🏆 合成状态: ❌ 未合成（卡片未集齐）"

                    info_msg = f"""=====517活动查询结果=====
📱 账号: {mask_phone(account)}
🔐 授权状态: ✅ 已授权
⏰ 到期时间: {auth_time}
{task_info}{card_info}{extra_info}
=================="""
                    sender.reply(info_msg)
                else:
                    sender.reply(f"""=====517活动查询失败=====
📱 账号: {mask_phone(account)}
❌ 错误: {result.get('message', '未知错误')}
==================""")
            else:
                sender.reply("❌ 无效的选择")
                return
        except Exception as e:
            sender.reply(f"查询出错: {str(e)}")

    def query_accounts(self):
        """账号查询"""
        accounts = parse_accounts(uservalue)
        if not accounts:
            sender.reply(format_msg('no_accounts', cmd='电信登录'))
            return

        menu_items = ["=====电信查询=====", "🔍 快速选项:", "  [0] 查询全部账号", "  [9999] 批量快速查询", "  [9998] 本月话费抢购查询", "  [9997] 517活动查询", "", "📱 单独查询:"]

        for i, account in enumerate(accounts, 1):
            auth_status, _ = check_auth_status(account)
            status_icon = "✅" if auth_status == "✅ 已授权" else "⚠️" if "未授权" in auth_status else "❌"
            menu_items.append(f"  [{i}] {mask_phone(account)} {status_icon}")

        menu_items.extend(["", "💡 回复数字选择查询方式", "💡 回复'q'退出操作", "=================="])
        sender.reply("\n".join(menu_items))

        choice = sender.input(120000, 1, False)
        if not choice or choice.lower() == 'q':
            sender.reply('✅ 已退出查询')
            return

        if choice == '0':
            self._query_all_accounts(accounts)
        elif choice == '9999':
            self._batch_query_accounts(accounts)
        elif choice == '9998':
            self._query_payment_records(accounts)
        elif choice == '9997':
            self._query_517_activity(accounts)
        else:
            try:
                index = int(choice) - 1
                if 0 <= index < len(accounts):
                    self._query_single_account(accounts[index])
                else:
                    sender.reply("❌ 无效的账号编号")
            except ValueError:
                sender.reply("❌ 请输入有效的数字")

    def _query_all_accounts(self, accounts):
        """查询所有账号"""
        total_coin = 0
        for i, account in enumerate(accounts, 1):
            auth_status, auth_time = check_auth_status(account)

            if auth_status == "✅ 已授权":
                token = sg.bucketGet('dd_dx_token', account)
                if token:
                    try:
                        phone, password = token.split('#')
                        result = self.api.query_account_info(phone, password)

                        if result["status"] == "success":
                            coin = result.get('coin', 0)
                            total_coin += coin
                            today_sign = "✅" if result.get('today_signed') else "❌"

                            msg = format_msg('query_result',
                                           phone=mask_phone(account), auth=auth_status,
                                           coin=coin, days=result.get('sign_days', 0), today=today_sign)
                        else:
                            msg = f"=====账号{i}查询失败=====\n📱 账号: {mask_phone(account)}\n❌ 错误: {result.get('message')}\n=================="
                    except Exception as e:
                        msg = f"=====账号{i}查询异常=====\n📱 账号: {mask_phone(account)}\n❌ 异常: {str(e)}\n=================="
                else:
                    msg = f"=====账号{i}信息缺失=====\n📱 账号: {mask_phone(account)}\n❌ 账号信息不完整\n=================="
            else:
                msg = f"=====账号{i}未授权=====\n📱 账号: {mask_phone(account)}\n🔐 授权: {auth_status}\n💡 需要先进行授权\n=================="

            sender.reply(msg)
            time.sleep(1)  # 每个账号查询间隔1秒，确保数据准确性

    def _batch_query_accounts(self, accounts):
        """批量快速查询"""
        def query_single(account):
            auth_status, auth_time = check_auth_status(account)
            if auth_status != "✅ 已授权":
                return {'account': mask_phone(account), 'status': 'unauthorized', 'auth_status': auth_status, 'auth_time': auth_time}

            token = sg.bucketGet('dd_dx_token', account)
            if not token:
                return {'account': mask_phone(account), 'status': 'no_token', 'auth_status': auth_status, 'auth_time': auth_time}

            try:
                phone, password = token.split('#')
                result = self.api.query_account_info(phone, password)

                if result["status"] == "success":
                    return {
                        'account': mask_phone(account), 'status': 'success', 'coin': result.get('coin', 0),
                        'sign_days': result.get('sign_days', 0), 'today_signed': result.get('today_signed', False),
                        'pet_level': result.get('pet_level', 0), 'auth_status': auth_status, 'auth_time': auth_time
                    }
                else:
                    return {'account': mask_phone(account), 'status': 'error', 'message': result.get('message'), 'auth_status': auth_status, 'auth_time': auth_time}
            except Exception as e:
                return {'account': mask_phone(account), 'status': 'exception', 'message': str(e), 'auth_status': auth_status, 'auth_time': auth_time}

        results = []
        for account in accounts:
            result = query_single(account)
            results.append(result)
            time.sleep(1)  # 每个账号查询间隔1秒，确保数据准确性

        total_coin = sum(r['coin'] for r in results if r['status'] == 'success')
        success_count = len([r for r in results if r['status'] == 'success'])

        batch_result = ["=====批量查询结果====="]

        success_results = [r for r in results if r['status'] == 'success']
        failed_results = [r for r in results if r['status'] != 'success']

        if success_results:
            batch_result.append("✅ 查询成功:")
            for result in success_results:
                today_sign = "✅" if result.get('today_signed') else "❌"
                batch_result.append(f"📱 {result['account']}")
                batch_result.append(f"   💰 金豆:{result['coin']} | 📅 签到:{result['sign_days']}天 | 🎯 今日:{today_sign}")
                batch_result.append(f"   🐾 宠物:Lv.{result.get('pet_level', 0)} | ⏰ 到期:{result['auth_time']}")
                batch_result.append("")

        if failed_results:
            batch_result.append("❌ 查询失败:")
            for result in failed_results:
                reason = "未授权" if result['status'] == 'unauthorized' else "信息缺失" if result['status'] == 'no_token' else result.get('message', '查询失败')
                batch_result.append(f"📱 {result['account']} - {reason}")
            batch_result.append("")

        batch_result.extend([
            "📊 汇总统计:",
            f"   ✅ 成功: {success_count}个账号",
            f"   ❌ 失败: {len(failed_results)}个账号",
            f"   🪙 总金豆: {total_coin}",
            "=================="
        ])
        sender.reply("\n".join(batch_result))

    def _query_517_activity(self, accounts):
        """批量查询517活动状态"""
        sender.reply("=====517活动批量查询=====\n⏳ 正在查询所有账号的517活动状态...\n==================")

        for i, account in enumerate(accounts, 1):
            auth_status, auth_time = check_auth_status(account)

            if auth_status != "✅ 已授权":
                sender.reply(f"=====账号{i}未授权=====\n📱 账号: {mask_phone(account)}\n🔐 授权: {auth_status}\n💡 需要先进行授权\n==================")
                continue

            token = sg.bucketGet('dd_dx_token', account)
            if not token:
                sender.reply(f"=====账号{i}信息缺失=====\n📱 账号: {mask_phone(account)}\n❌ 账号信息不完整\n==================")
                continue

            try:
                phone, password = token.split('#')
                result = query_517_activity_status(phone, password, self.api)

                if result["status"] == "success":
                    collection = result.get("collection", {})
                    missing = collection.get("missing", [])

                    card_parts = []
                    for card in collection.get("cards", []):
                        card_parts.append(f"{card['pieceName']}x{card.get('availableCount', 0)}")
                    card_summary = "、".join(card_parts) if card_parts else "无数据"

                    if result.get("has_composite"):
                        composite_status = "✅ 已合成"
                    elif collection.get("is_all_collected"):
                        composite_status = "🟡 可合成"
                    else:
                        composite_status = "❌ 未集齐"

                    detail_msg = f"""=====账号{i} 517活动状态=====
📱 账号: {mask_phone(account)}
📋 任务: 已完成{result['finished_count']}个 / 未完成{result['unfinished_count']}个
🎰 抽奖次数: {result.get('total_chance_count', 0)}
🃏 卡片: {card_summary}
{"⚠️ 缺少: " + "、".join(missing) if missing else "🎉 已集齐！"}
🏆 合成: {composite_status}
=================="""
                    sender.reply(detail_msg)
                else:
                    sender.reply(f"=====账号{i} 517查询失败=====\n📱 账号: {mask_phone(account)}\n❌ 错误: {result.get('message', '未知错误')}\n==================")
            except Exception as e:
                sender.reply(f"=====账号{i} 517查询异常=====\n📱 账号: {mask_phone(account)}\n❌ 异常: {str(e)}\n==================")

            time.sleep(1)

    def _query_payment_records(self, accounts):
        return True

    def _query_single_payment_record(self, phone, password):
        return True

    def _get_coin_mall_records(self, accId):
        """获取金豆商城兑换记录"""
        try:
            url = 'https://wappark.189.cn/jt-sign/paradise/getCoinMallExchangetRecords'
            params = {'accId': accId, 'page': 0, 'size': 150}
            data = encrypt_para(json.dumps(params))

            res = self.api.session.post(url, data=json.dumps({'para': data}))
            return res.json().get('data', [])
        except Exception:
            return []

    def _get_rights_records(self, accId, sign=None):
        """获取权益兑换记录"""
        all_rights_records = []
        try:
            url = 'https://wappark.189.cn/jt-sign/paradise/getRightsExchangetRecords'
            params = {'accId': accId, 'page': 0, 'size': 100}
            data = encrypt_para(json.dumps(params))

            headers = {
                'Content-Type': 'application/json;charset=utf-8',
                'Referer': f'https://wappark.189.cn/resources/dist/recordsNew.html?ticket=$ticket$&type=2'
            }
            if sign:
                headers['sign'] = sign

            res = self.api.session.post(url, data=json.dumps({'para': data}), headers=headers)
            res_json = res.json()
            if res_json.get('resoultCode') == '0' or res_json.get('code') == 0:
                all_rights_records.extend(res_json.get('data', []))
        except Exception:
            pass

        try:
            prize_records = self._get_prize_records(accId, sign)
            for record in prize_records:
                win_title = record.get("winTitle", "")
                if "等级" in win_title or "LV" in win_title or "等级权益" in win_title:
                    all_rights_records.append(record)
        except Exception:
            pass

        return all_rights_records

    def _get_prize_records(self, accId, sign):
        """获取抽奖记录"""
        try:
            self.api.session.headers['sign'] = sign
            url = 'https://wappark.189.cn/jt-sign/webSign/getPrizeRecords'
            params = {'phone': accId, 'page': 0, 'size': 150}
            data = encrypt_para(json.dumps(params))

            res = self.api.session.post(url, data=json.dumps({'para': data}))
            return res.json().get('data', [])
        except Exception:
            return []

    def _analyze_payment_records(self, coin_records, rights_records, prize_records, xbk_records=None):
        return True

def admin_auth():
    return True
def sync_users():
    """同步已授权用户到面板"""
    if not sender.isAdmin():
        sender.reply("❌ 您没有权限执行此操作!")
        exit(0)

    sender.reply("=====电信同步=====\n⏳ 正在同步已授权用户到面板...\n==================")

    users = sg.bucketAllKeys('dd_dx_user')
    if not users:
        sender.reply("=====同步结果=====\n❌ 未找到任何绑定用户\n==================")
        return

    try:
        ql = QingLongManager()
    except Exception:
        sender.reply("❌ 连接面板失败")
        return

    success_count = 0
    skip_count = 0
    fail_count = 0

    for user in users:
        accountlist = sg.bucketGet('dd_dx_user', user)
        if not accountlist or accountlist == '' or accountlist == '{}':
            continue

        accounts = parse_accounts(accountlist)
        accounts = list(dict.fromkeys(accounts))

        for account in accounts:
            try:
                dqsj = str(datetime.now().date())
                accountVip = '2099-12-31'
                token = sg.bucketGet('dd_dx_token', account)

                if not accountVip or accountVip <= dqsj or not token:
                    skip_count += 1
                    continue

                ql.add_or_update_env(account, token)
                success_count += 1
            except Exception:
                fail_count += 1

    sender.reply(f"=====同步完成=====\n✅ 同步成功: {success_count}个账号\n⏭️ 跳过未授权: {skip_count}个账号\n❌ 同步失败: {fail_count}个账号\n==================")


def show_tutorial():
    """显示教程"""
    tutorial = f"""=====电信插件教程=====

🎯 【基本功能】
• 金豆余额查询
• 签到天数统计
• 宠物等级查询
• 批量账号操作

1️⃣ 绑定账号: 发送 电信登录
2️⃣ 使用授权: 发送 电信授权
3️⃣ 管理账号: 发送 电信管理
4️⃣ 查询信息: 发送 电信查询

💡 【注意事项】
• 登录格式: 手机号#密码
• 支持批量操作
• 授权到期自动清理

🆘 【常见问题】
Q: 登录失败？ A: 检查手机号密码
Q: 查询提示过期？ A: 重新绑定账号
=================="""
    sender.reply(tutorial)

def clean_expired():
    try:
        sender.reply('该管理项已取消，账号直接运行')
    except Exception:
        pass
    return None
def main():
    manager = TelecomManager()
    message = sender.getMessage()
    imtype = sender.getImtype()

    if '登录' in message or '登陆' in message:
        manager.login_account()
    elif '管理' in message:
        if uservalue:
            manager.manage_accounts()
        else:
            sender.reply(format_msg('no_accounts', cmd='电信登录'))
    elif '查询' in message:
        if uservalue:
            manager.query_accounts()
        else:
            sender.reply(format_msg('no_accounts', cmd='电信登录'))
    elif message == '电信清理':
        clean_expired()
    elif message == '电信授权':
        admin_auth()
    elif message == '电信教程':
        show_tutorial()
    elif message == '电信同步':
        sync_users()
    elif imtype == 'fake':
        users = sg.bucketAllKeys('dd_dx_user')
        today = str(datetime.now().date())
        for user in users:
            accountlist = sg.bucketGet('dd_dx_user', user)
            if not accountlist:
                continue
            accounts = parse_accounts(accountlist)
            for account in accounts:
                try:
                    auth_time = '2099-12-31'
                    phone = account[:3] + '****' + account[7:] if len(account) >= 11 else account
                    if not auth_time or auth_time <= today:
                        push_msg = f"""
=====电信账号通知=====
📱 账号: {phone}
📢 消息: ⏰ 定时检测提醒\n------------------\n❌ 授权已过期\n💡 请及时续费授权
=================="""
                        for platform in ['wb', 'tg', 'qq', 'qb', 'wx']:
                            try:
                                sg.push(platform, '', user, '', push_msg)
                            except:
                                pass
                    else:
                        try:
                            expire_date = datetime.strptime(auth_time, '%Y-%m-%d').date()
                            days_left = (expire_date - datetime.now().date()).days
                            if days_left <= 3:
                                push_msg = f"""
=====电信账号通知=====
📱 账号: {phone}
📢 消息: ⏰ 定时检测提醒\n------------------\n⚠️ 授权即将到期\n📅 到期时间: {auth_time}\n⏳ 剩余天数: {days_left}天\n💡 请及时续费授权
=================="""
                                for platform in ['wb', 'tg', 'qq', 'qb', 'wx']:
                                    try:
                                        sg.push(platform, '', user, '', push_msg)
                                    except:
                                        pass
                        except:
                            pass
                except:
                    continue
    else:
        sender.setContinue()

if __name__ == "__main__":
    main()
