# [title: 捷停车]
# [name: jieTingChe]
# [language: python]
# [class: 任务]
# [author: huawei]
# [version: v1.5.3]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^捷停车登录$|^登录捷停车$|^捷停车查询$|^捷停车管理$|^捷停车$|^捷停车清理$|^捷停车上传$]
# [icon: https://free.picui.cn/free/2025/12/17/69418a3031112.png]
# [description: 捷停车小程序自动登录，支持验证码自动识别]
# [depe: ["requests"]]


import asyncio as _sg_asyncio
import os as _sg_os
import time as _sg_time
import types as _sg_types
import re as _sg_re
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

config = form({
    'G_JTC_ocr_api': form.string().title('ddddocr API地址').default('').description('验证码识别API地址，默认: http://1.94.118.234:8886/ocr'),
    'G_JTC_ql_config': form.string().title('青龙配置').default('').description('青龙面板配置信息，用|分隔'),
    'G_JTC_ql_envname': form.string().title('青龙变量名').default('').description('推送到青龙的变量名称'),
    'G_JTC_daidai_config': form.string().title('呆呆面板配置').default('').description('呆呆面板配置信息，用丨分隔'),
    'G_JTC_daidai_group': form.string().title('呆呆分组').default('').description('呆呆面板环境变量分组名称'),
    'G_JTC_use_daidai': form.boolean().title('使用呆呆面板').default(False).description('勾选=上传呆呆面板，不勾选=上传青龙面板(默认)'),
})
_CONFIG_FIELD_MAP = {
    ('G_JTC', 'ocr_api'): 'G_JTC_ocr_api',
    ('G_JTC', 'ql_config'): 'G_JTC_ql_config',
    ('G_JTC', 'ql_envname'): 'G_JTC_ql_envname',
    ('G_JTC', 'daidai_config'): 'G_JTC_daidai_config',
    ('G_JTC', 'daidai_group'): 'G_JTC_daidai_group',
    ('G_JTC', 'use_daidai'): 'G_JTC_use_daidai',
}

import json
import requests
import re
import time
import base64
import uuid
import warnings
from datetime import datetime
from decimal import Decimal
warnings.filterwarnings('ignore', message='Unverified HTTPS request')
try:
    HAS_UA_LIB = True
except:
    HAS_UA_LIB = False

HAS_HUAWEI_LIB = True

BUCKET_ACCOUNTS = 'jtc_accounts'
BUCKET_CONFIG = 'G_JTC'
PROJECT_NAME = '捷停车'
BASE_URL = "https://sytgate.jslife.com.cn"
senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()



def get_config() -> dict:
    ma_pay_switch_raw = '2099-12-31' or 'false'
    if isinstance(ma_pay_switch_raw, bool): ma_pay_switch = ma_pay_switch_raw
    elif ma_pay_switch_raw is None: ma_pay_switch = False
    else: ma_pay_switch = str(ma_pay_switch_raw).lower() == 'true'

    use_daidai_raw = sg.bucketGet(BUCKET_CONFIG, 'use_daidai') or 'false'
    if isinstance(use_daidai_raw, bool): use_daidai = use_daidai_raw
    elif use_daidai_raw is None: use_daidai = False
    else: use_daidai = str(use_daidai_raw).lower() == 'true'

    return {
        'ocr_api': sg.bucketGet(BUCKET_CONFIG, 'ocr_api') or 'http://1.94.118.234:8886/ocr',
        'price': Decimal(sg.bucketGet(BUCKET_CONFIG, 'price') or '0'),
        'coin': sg.bucketGet(BUCKET_CONFIG, 'coin') or '',
        'zsm': sg.bucketGet('dd_sign_config', 'zsm') or sg.bucketGet(BUCKET_CONFIG, 'zsm') or '',
        'ql_config': sg.bucketGet(BUCKET_CONFIG, 'ql_config') or '',
        'ql_envname': sg.bucketGet(BUCKET_CONFIG, 'ql_envname') or 'JT_TOKEN',
        'daidai_config': sg.bucketGet(BUCKET_CONFIG, 'daidai_config') or '',
        'daidai_group': sg.bucketGet(BUCKET_CONFIG, 'daidai_group') or PROJECT_NAME,
        'use_daidai': use_daidai,
        'ma_pay_switch': ma_pay_switch,
        'ma_pay_gateway': '2099-12-31' or '',
        'ma_pay_pid': '2099-12-31' or '',
        'ma_pay_key': '2099-12-31' or '',
        'ma_pay_type': '2099-12-31' or 'alipay,wxpay',
        'ma_pay_notify_url': '2099-12-31' or ''
    }

def get_user_accounts(user_id=None) -> dict:
    if not user_id: user_id = userid
    accounts_json = sg.bucketGet(BUCKET_ACCOUNTS, user_id) or "{}"
    try:
        return json.loads(accounts_json)
    except:
        return {}

def save_user_accounts(accounts, user_id=None):
    if not user_id: user_id = userid
    sg.bucketSet(BUCKET_ACCOUNTS, user_id, json.dumps(accounts, ensure_ascii=False))

def recognize_captcha(image_url: str, ocr_api: str) -> str:
    try:
        r = requests.get(image_url, timeout=10, verify=False)
        if r.status_code != 200: return ""
        base64_img = base64.b64encode(r.content).decode()
        api_resp = requests.post(ocr_api, data={"image": base64_img, "probability": False, "png_fix": False}, timeout=10, verify=False)
        result = api_resp.json()
        if result.get("code") == 200 and result.get("data"):
            return result.get("data", "").strip()
        return ""
    except Exception:
        return ""

def generate_timestamp() -> str:
    return str(int(time.time() * 1000))

def get_app_headers(uc_id: str) -> dict:
    return {
        "User-Agent": "okhttp/4.10.0",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/json; charset=utf-8",
        "UC_ID": uc_id,
        "applicationVersion": "60400"
    }

def get_verify_image(telephone: str, device_id: str, uc_id: str) -> dict:
    try:
        params = {
            "applictionType": "APP",
            "applictionVersion": "60400",
            "privacyVersion": "1.0",
            "telephone": telephone,
            "telephoneType": 1,
            "timestamp": generate_timestamp(),
            "verifyType": "VERIFY_LOGIN",
            "version": "V1.0"
        }
        r = requests.post(f"{BASE_URL}/core-gateway/user/login/verify/image", json=params, headers=get_app_headers(uc_id), timeout=10, verify=False)
        result = r.json()
        return result.get("obj", {}) if result.get("success") else {}
    except:
        return {}

def send_sms_code(telephone: str, key: str, captcha_code: str, device_id: str, uc_id: str) -> bool:
    try:
        params = {
            "applictionType": "APP",
            "applictionVersion": "60400",
            "privacyVersion": "1.0",
            "telephone": telephone,
            "telephoneType": 1,
            "timestamp": generate_timestamp(),
            "verifyType": "VERIFY_LOGIN",
            "version": "V1.0"
        }
        if captcha_code:
            params["captchaCode"] = captcha_code
        if key:
            params["key"] = key
        r = requests.post(f"{BASE_URL}/core-gateway/user/login/sms/push", json=params, headers=get_app_headers(uc_id), timeout=10, verify=False)
        return r.json().get("success", False)
    except:
        return False

def login_with_sms(telephone: str, msg_code: str, device_id: str, uc_id: str) -> dict:
    try:
        params = {
            "appSource": "A3",
            "applictionType": "APP",
            "applictionVersion": "60400",
            "deviceId": device_id,
            "osType": "ANDROID",
            "privacyVersion": "1.0",
            "sceneSource": "LOGIN",
            "telephone": telephone,
            "telephoneType": 1,
            "timestamp": generate_timestamp(),
            "userSource": "A3",
            "userType": "APP_JTC",
            "verificationCode": msg_code
        }
        r = requests.post(f"{BASE_URL}/core-gateway/user/login/app_login", json=params, headers=get_app_headers(uc_id), timeout=10, verify=False)
        result = r.json()
        if result.get("success") and result.get("obj"):
            user_info = result.get("obj", {})
            user_id = user_info.get("userId", "")
            token = user_info.get("token", "")
            return {
                "user_id": user_id,
                "telephone": user_info.get("telephone", telephone),
                "nickName": user_info.get("nickName", ""),
                "token": token,
                "deviceId": device_id
            }
        return {}
    except:
        return {}

def process_login(config: dict) -> bool:
    try:
        sender.reply("请输入手机号：")
        telephone = sender.listen(60000)
        if not telephone:
            sender.reply("感谢使用！")
            return False
        telephone = telephone.strip()
        if not telephone:
            sender.reply("❌ 未收到手机号")
            return False
        if telephone.lower() == 'q':
            sender.reply("✅ 已取消")
            return False
        if not re.match(r'^1[3-9]\d{9}$', telephone):
            sender.reply("❌ 手机号格式不正确，请输入11位手机号")
            return False

        device_id = str(uuid.uuid4()).replace('-', '')
        uc_id = device_id
        ocr_api = config.get('ocr_api', '')

        verify_data = get_verify_image(telephone, device_id, uc_id)
        if not verify_data:
            sender.reply("❌ 获取验证图片失败，请稍后重试")
            return False

        key = verify_data.get("key", "")
        is_verify_image = verify_data.get("isVerifyImage", "1") == "1"
        url = verify_data.get("url", "")

        captcha_code = ""
        if is_verify_image and url:
            for captcha_attempt in range(1, 4):
                if captcha_attempt == 1:
                    sender.reply("🔍 正在识别验证码...")
                    captcha_code = recognize_captcha(url, ocr_api)
                    if captcha_code:
                        sender.reply(f"✅ 识别成功: {captcha_code}")
                    else:
                        sender.reply(f"⚠️ 自动识别失败\n请输入图片验证码（剩余{4-captcha_attempt}次机会）：")
                        captcha_code = sender.listen(60000)
                        if not captcha_code:
                            sender.reply("感谢使用！")
                            return False
                        captcha_code = captcha_code.strip()
                else:
                    sender.reply(f"请重新输入图片验证码（剩余{4-captcha_attempt}次机会）：")
                    captcha_code = sender.listen(60000)
                    if not captcha_code:
                        sender.reply("感谢使用！")
                        return False
                    captcha_code = captcha_code.strip()

                if not captcha_code:
                    sender.reply("❌ 验证码不能为空")
                    if captcha_attempt == 3:
                        sender.reply("❌ 验证码输入失败次数过多，请重新开始")
                        return False
                    continue
                if captcha_code.lower() == 'q':
                    sender.reply("✅ 已取消")
                    return False
                if len(captcha_code) != 4:
                    sender.reply("❌ 验证码格式错误（应为4位）")
                    if captcha_attempt == 3:
                        sender.reply("❌ 验证码输入失败次数过多，请重新开始")
                        return False
                    continue

                if send_sms_code(telephone, key, captcha_code, device_id, uc_id):
                    break
                else:
                    if captcha_attempt == 3:
                        sender.reply("❌ 图片验证码错误次数过多，请重新开始")
                        return False
                    sender.reply("❌ 图片验证码错误")
        else:
            sender.reply("✅ 账号已注册，无需图片验证")
            if not send_sms_code(telephone, key, captcha_code, device_id, uc_id):
                sender.reply("❌ 短信发送失败，请稍后重试")
                return False

        sender.reply("✅ 短信发送成功！\n请输入收到的验证码（有效期3分钟）：")
        for sms_attempt in range(1, 4):
            if sms_attempt > 1:
                sender.reply(f"请重新输入短信验证码（剩余{4-sms_attempt}次机会）：")

            msg_code = sender.listen(180000)
            if not msg_code:
                sender.reply("感谢使用！")
                return False
            msg_code = msg_code.strip()
            if not msg_code:
                sender.reply("❌ 验证码输入超时")
                return False
            if msg_code.lower() == 'q':
                sender.reply("✅ 已取消")
                return False
            if len(msg_code) != 6:
                sender.reply("❌ 验证码格式错误（应为6位）")
                if sms_attempt == 3:
                    sender.reply("❌ 短信验证码输入失败次数过多")
                    return False
                continue

            sender.reply("🔐 正在验证登录...")
            user_info = login_with_sms(telephone, msg_code, device_id, uc_id)
            if user_info and user_info.get("user_id"):
                user_id = user_info.get("user_id")
                phone = user_info.get("telephone", telephone)
                token = user_info.get("token", "")
                user_accounts = get_user_accounts()

                existing_account_id = None
                for acc_id, acc in user_accounts.items():
                    if acc.get('phone') == phone:
                        existing_account_id = acc_id
                        break

                if existing_account_id:
                    user_accounts[existing_account_id]['data'] = f"{user_id}#{token}"
                    user_accounts[existing_account_id]['nickName'] = user_info.get("nickName", "")
                    user_accounts[existing_account_id]['bind_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    save_user_accounts(user_accounts)
                    masked_phone = phone[:3] + "****" + phone[-4:] if len(phone) == 11 else phone
                    panel_msg = ""
                    auth_status = user_accounts[existing_account_id].get('auth_status', {})
                    expire_time = auth_status.get('expire_time', '')
                    is_valid = auth_status.get('is_authorized', False) and expire_time and datetime.strptime(expire_time, '%Y-%m-%d').date() >= datetime.now().date()
                    if is_valid:
                        panel_ok = sync_to_panel(existing_account_id, phone, expire_time, config)
                        pn = get_panel_name(config)
                        if is_panel_configured(config):
                            panel_msg = f"\n🔄 {pn}同步: 成功" if panel_ok else f"\n⚠️ {pn}同步: 失败"
                    sender.reply(f"✅ 账号更新成功！\n📱 账号: {masked_phone}{panel_msg}\n\n您可以发送「捷停车管理」进行授权")
                else:
                    account_id = str(uuid.uuid4())
                    user_accounts[account_id] = {
                        "phone": phone,
                        "data": f"{user_id}#{token}",
                        "nickName": user_info.get("nickName", ""),
                        "bind_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        "auth_status": {"is_authorized": False, "expire_time": ""}
                    }
                    save_user_accounts(user_accounts)
                    masked_phone = phone[:3] + "****" + phone[-4:] if len(phone) == 11 else phone
                    sender.reply(f"✅ 登录成功！\n📱 账号: {masked_phone}\n\n您可以发送「捷停车管理」进行授权")
                return True
            else:
                if sms_attempt == 3:
                    sender.reply("❌ 短信验证码错误次数过多")
                    return False
                sender.reply("❌ 短信验证码错误")

        return False
    except Exception as e:
        sender.reply(f"❌ 登录异常: {str(e)}")
        return False

def query_accounts() -> bool:
    try:
        user_accounts = get_user_accounts()
        if not user_accounts:
            sender.reply("您还没有绑定任何捷停车账号\n请发送「捷停车登录」进行绑定")
            return False

        for account_id, account in user_accounts.items():
            phone = account.get('phone', '未知')
            masked_phone = phone[:3] + "****" + phone[-4:] if len(phone) == 11 else phone
            account_data = account.get('data', '')
            auth_status = account.get('auth_status', {})
            is_authorized = auth_status.get('is_authorized', False)
            expire_time = auth_status.get('expire_time', '')

            balance_info = query_balance(account_data)
            total_coin = balance_info.get('data', {}).get('accountAmt', 0) if balance_info.get('success') else 0

            today = datetime.now().strftime("%Y-%m-%d")
            today_coin = 0
            recent_records = []
            try:
                parts = account_data.split('#')
                if len(parts) >= 2:
                    user_id = parts[0]
                    url = f"{BASE_URL}/base-gateway/integral/v2/user/page/new"
                    data = {"userId": user_id, "valueType": "", "pageIndex": 1, "pageSize": 100}
                    r = requests.post(url, json=data, timeout=10, verify=False)
                    if r.status_code == 200:
                        result = r.json()
                        if result.get('success') and result.get('data'):
                            records = result['data'].get('data', [])
                            for record in records:
                                create_time = record.get('createTime', '')
                                value_type = record.get('valueType', '')
                                integral_value = int(record.get('integralValue', 0))
                                if value_type == 'ADD':
                                    if create_time.startswith(today):
                                        today_coin += integral_value
                                    if len(recent_records) < 5:
                                        date_str = create_time[:10] if len(create_time) >= 10 else create_time
                                        recent_records.append(f"领取 {integral_value}停车币-{date_str}")
            except:
                pass

            auth_msg = f"✅ 已授权\n📅 到期时间: 到期: {expire_time}" if is_authorized else "❌ 未授权"
            msg = "=====捷停车详情========\n"
            msg += f"📱 账号: {masked_phone}\n"
            msg += f"🔐 授权状态: {auth_msg}\n"
            msg += f"💰 总币: {total_coin}元，今日币：{today_coin}\n"
            if recent_records:
                msg += "===== 🎁任务完成🎁 =====\n"
                msg += "\n".join(recent_records) + "\n"
            msg += "===================="
            sender.reply(msg)

        return True
    except Exception as e:
        sender.reply(f"❌ 查询失败: {str(e)}")
        return False

def query_balance(account_data: str) -> dict:
    try:
        parts = account_data.split('#')
        if len(parts) < 2:
            return {"success": False}
        user_id = parts[0]
        url = f"{BASE_URL}/base-gateway/integral/v2/balance/query"
        data = {"userId": user_id, "signType": "MD5", "reqSource": "APP_JTC", "applictionType": "APP", "applictionVersion": "60408", "timestamp": str(int(time.time() * 1000)), "sign": "E8E4E0E6C6A619AA09869E875B78697D", "nonce": str(uuid.uuid4()).upper()}
        r = requests.post(url, json=data, timeout=10, verify=False)
        return r.json() if r.status_code == 200 else {"success": False}
    except:
        return {"success": False}

def cleanup_expired_data() -> bool:
    try:
        try:
            users = sg.bucketAllKeys(bucket=BUCKET_ACCOUNTS) or []
        except:
            users = []
        if not users:
            sender.reply("❌ 无用户数据")
            return False

        sender.reply("🔍 正在检查所有用户账号状态...")
        config = get_config()
        current_date = datetime.now().date()
        total_accounts, expired_count, warning_count, notified_users = 0, 0, 0, 0

        for uid in users:
            user_accounts = get_user_accounts(uid)
            if not user_accounts: continue
            expired_ids, warning_phones = [], []

            for account_id, account in user_accounts.items():
                total_accounts += 1
                phone = account.get('phone', '')
                auth_status = account.get('auth_status', {})
                expire_str = auth_status.get('expire_time', '')
                is_authorized = auth_status.get('is_authorized', False)

                if not is_authorized or not expire_str:
                    expired_ids.append((account_id, phone, "未授权"))
                    continue
                try:
                    expire_date = datetime.strptime(expire_str, '%Y-%m-%d').date()
                    days_left = (expire_date - current_date).days
                    if days_left < 0:
                        expired_ids.append((account_id, phone, f"已过期{abs(days_left)}天"))
                    elif days_left <= 3:
                        masked = phone[:3] + "****" + phone[-4:] if len(phone) == 11 else phone
                        warning_phones.append((masked, f"剩余{days_left}天"))
                except:
                    expired_ids.append((account_id, phone, "授权异常"))

            for account_id, phone, reason in expired_ids:
                if phone:
                    delete_from_panel(phone, config)
                if account_id in user_accounts:
                    del user_accounts[account_id]
                expired_count += 1
            if expired_ids:
                save_user_accounts(user_accounts, uid)

            if warning_phones:
                warning_count += len(warning_phones)
                account_msgs = [f"📱 {p}\n⚠️ 授权即将过期({r})，请续费" for p, r in warning_phones]
                notify_msg = "=====捷停车账号通知=====\n" + "\n-------------------\n".join(account_msgs) + "\n====================\n发送「捷停车管理」续费"
                push_ok = False
                try:
                    sg.push('wx', '', uid, '账号状态提醒', notify_msg)
                    push_ok = True
                except: pass
                try:
                    sg.push('qq', '', uid, '账号状态提醒', notify_msg)
                    push_ok = True
                except: pass
                if push_ok: notified_users += 1

        sender.reply(
            f"=====清理报告=====\n"
            f"📊 检查用户数: {len(users)}个\n"
            f"📱 检查账号数: {total_accounts}个\n"
            f"🗑️ 清理过期: {expired_count}个\n"
            f"⚠️ 即将过期: {warning_count}个\n"
            f"📤 已推送用户: {notified_users}个\n"
            f"===================="
        )
        return True
    except Exception as e:
        sender.reply(f"❌ 清理失败: {str(e)}")
        return False

def parse_account_selection(choice_str: str, max_index: int) -> list:
    if not choice_str or not choice_str.strip():
        return None
    choice_str = choice_str.strip()
    selected_indices = set()
    try:
        parts = choice_str.split(',')
        for part in parts:
            part = part.strip()
            if not part:
                continue
            if '-' in part:
                range_parts = part.split('-')
                if len(range_parts) != 2:
                    return None
                start = int(range_parts[0].strip())
                end = int(range_parts[1].strip())
                if start < 1 or end < 1 or start > max_index or end > max_index:
                    return None
                if start > end:
                    return None
                for i in range(start - 1, end):
                    selected_indices.add(i)
            else:
                num = int(part)
                if num < 1 or num > max_index:
                    return None
                selected_indices.add(num - 1)
        return sorted(list(selected_indices))
    except (ValueError, AttributeError):
        return None

def process_auth(account_id: str, config: dict) -> bool:
    return True

def batch_auth(config: dict) -> bool:
    return True

def batch_manage(config: dict) -> bool:
    try:
        user_accounts = get_user_accounts()
        if not user_accounts:
            sender.reply("您还没有绑定任何捷停车账号\n请发送「捷停车登录」进行绑定")
            return False

        user_coin = Decimal(sg.bucketGet('dd_sign_points', userid) or '0')
        authorized_count = sum(1 for acc in user_accounts.values() if acc.get('auth_status', {}).get('is_authorized', False))
        unauthorized_count = len(user_accounts) - authorized_count

        account_ids = list(user_accounts.keys())
        account_lines = []
        for i, account_id in enumerate(account_ids, 1):
            phone = user_accounts[account_id].get('phone', '未知')
            masked_phone = phone[:3] + "****" + phone[-4:] if len(phone) == 11 else phone
            auth_status = user_accounts[account_id].get('auth_status', {})
            is_authorized = auth_status.get('is_authorized', False)
            expire_time = auth_status.get('expire_time', '')
            auth_msg = f"✅ 到期:{expire_time}" if is_authorized else "❌ 未授权"
            account_lines.append(f"[{i}] 📱 {masked_phone}\n {auth_msg}")

        account_list = "\n".join(account_lines)
        sender.reply(
            "=====账号管理=====\n"
            f"📱 绑定账号: {len(user_accounts)}个\n"
            f"✅ 已授权: {authorized_count}个\n"
            f"❌ 未授权: {unauthorized_count}个\n"
            f"💰 当前积分: {user_coin}\n"
            "--------------------\n"
            f"{account_list}\n"
            "[0] 全部授权\n"
            "[00] 未授权账号\n"
            "[9998] 删除所有账号\n"
            "--------------------\n"
            "💡 批量选择示例:\n"
            "   范围选择: 3-6\n"
            "   多个选择: 1,4,6\n"
            "   混合选择: 1,3-5,8\n"
            "回复序号选择操作 (q退出)\n"
            "=================="
        )

        choice = sender.listen(120000)
        if not choice:
            sender.reply("感谢使用！")
            return False
        choice = choice.strip()
        if not choice:
            sender.reply("⏰ 操作超时")
            return False

        if choice == 'q':
            sender.reply("✅ 已取消")
            return False

        to_manage_ids = []
        if choice == '0':
            to_manage_ids = account_ids
        elif choice == '00':
            to_manage_ids = [aid for aid in account_ids if not user_accounts[aid].get('auth_status', {}).get('is_authorized', False)]
            if not to_manage_ids:
                sender.reply("✅ 所有账号都已授权")
                return False
        elif choice == '9998':
            sender.reply("⚠️ 确认删除所有账号吗？\n回复 [Y] 确认删除\n回复 [N] 取消")
            confirm = sender.listen(60000)
            if not confirm or confirm.strip().lower() != 'y':
                sender.reply("✅ 已取消")
                return False
            sg.bucketDel(BUCKET_ACCOUNTS, userid)
            sender.reply("✅ 删除成功！\n所有账号已删除")
            return True
        else:
            selected_indices = parse_account_selection(choice, len(account_ids))
            if selected_indices is None:
                sender.reply("❌ 选择格式无效！\n请使用正确格式:\n单个: 3\n范围: 3-6\n多个: 1,4,6\n混合: 1,3-5,8")
                return False
            if not selected_indices:
                sender.reply("❌ 未选择任何账号")
                return False
            to_manage_ids = [account_ids[idx] for idx in selected_indices]

        sender.reply("====操作选项====\n[1] 授权\n[2] 删除\n[0] 返回\n================\n请选择操作：")
        op = sender.listen(60000)
        if not op:
            sender.reply("感谢使用！")
            return False
        op = op.strip()
        if not op:
            sender.reply("⏰ 操作超时")
            return False

        if op == '0':
            sender.reply("✅ 已返回")
            return False

        if op == '1':
            if len(to_manage_ids) == 1:
                return process_auth(to_manage_ids[0], config)
            return process_batch_payment(to_manage_ids, user_accounts, config)
        elif op == '2':
            delete_count = 0
            panel_deleted_count = 0
            pn = get_panel_name(config)
            for account_id in to_manage_ids:
                phone = user_accounts[account_id].get('phone', '')
                if phone:
                    if delete_from_panel(phone, config):
                        panel_deleted_count += 1
                del user_accounts[account_id]
                delete_count += 1
            save_user_accounts(user_accounts)
            panel_msg = f"\n🔄 {pn}变量已删除: {panel_deleted_count}个" if is_panel_configured(config) and panel_deleted_count > 0 else ""
            sender.reply(f"✅ 删除成功！\n已删除 {delete_count} 个账号{panel_msg}")
        else:
            sender.reply("❌ 无效选择")

        return True
    except Exception as e:
        sender.reply(f"❌ 管理异常: {str(e)}")
        return False

def process_batch_payment(account_ids: list, user_accounts: dict, config: dict) -> bool:
    return True




def get_ql_token(host: str, client_id: str, client_secret: str) -> str:
    try:
        url = f'{host}/open/auth/token?client_id={client_id}&client_secret={client_secret}'
        print(f"[DEBUG] 请求青龙token: {url[:80]}...")
        r = requests.get(url, timeout=10, verify=False)
        print(f"[DEBUG] Token响应: status={r.status_code}")
        if r.status_code == 200:
            result = r.json()
            print(f"[DEBUG] Token结果: code={result.get('code')}, message={result.get('message', 'None')}")
            token = result.get('data', {}).get('token', '')
            if token:
                print(f"[SUCCESS] 获取token成功: {token[:20]}...")
                return token
            else:
                print(f"[ERROR] Token为空: {result}")
        else:
            print(f"[ERROR] Token请求失败: HTTP {r.status_code}, body={r.text[:200]}")
    except Exception as e:
        print(f"[ERROR] 获取token异常: {str(e)}")
    return ""

def delete_from_qinglong(phone: str, ql_config: str, ql_envname: str) -> bool:
    if not ql_config or not ql_envname or not phone:
        return False
    try:
        configs = ql_config.split('丨') if '丨' in ql_config else ql_config.split('|')
        if len(configs) < 3:
            print("[ERROR] 青龙配置格式错误")
            return False
        host, client_id, client_secret = configs[0].strip(), configs[1].strip(), configs[2].strip()
        ql_token = get_ql_token(host, client_id, client_secret)
        if not ql_token:
            print("[ERROR] 获取青龙token失败")
            return False
        headers = {'Authorization': f'Bearer {ql_token}', 'Content-Type': 'application/json'}
        envs_r = requests.get(f'{host}/open/envs', headers=headers, params={'searchValue': ql_envname}, timeout=10, verify=False)
        if envs_r.status_code != 200:
            print(f"[ERROR] 查询青龙变量失败: HTTP {envs_r.status_code}")
            return False
        envs = envs_r.json().get('data', [])
        deleted = False
        for env in envs:
            if env.get('name') == ql_envname and phone in str(env.get('remarks', '')):
                env_id = env.get('_id') or env.get('id')
                if env_id:
                    try:
                        del_r = requests.delete(f'{host}/open/envs', headers=headers, json=[env_id], timeout=10, verify=False)
                        if del_r.status_code == 200:
                            print(f"[SUCCESS] 删除青龙变量成功: phone={phone}, id={env_id}")
                            deleted = True
                        else:
                            print(f"[ERROR] 删除青龙变量失败: {del_r.text}")
                    except Exception as e:
                        print(f"[ERROR] 删除青龙变量异常: {str(e)}")
        return deleted
    except Exception as e:
        print(f"[ERROR] 删除青龙变量异常: {str(e)}")
        return False

def push_to_qinglong(account_id: str, phone: str, expire_date: str, ql_config: str, ql_envname: str, user_id: str = None) -> bool:
    if not ql_config or not ql_envname:
        print(f"[ERROR] 青龙配置为空: ql_config={bool(ql_config)}, ql_envname={ql_envname}")
        return False
    try:
        user_accounts = get_user_accounts(user_id)
        if account_id not in user_accounts:
            print(f"[ERROR] 账号ID不存在: {account_id}")
            return False

        account = user_accounts[account_id]
        env_value = account.get('data', '')
        print(f"[DEBUG] 账号数据: account_id={account_id}, phone={phone}")
        print(f"[DEBUG] env_value={env_value[:50] if env_value else 'None'}...")

        if not env_value or '#' not in env_value:
            print(f"[ERROR] env_value格式错误: {env_value}")
            return False

        configs = ql_config.split('丨') if '丨' in ql_config else ql_config.split('|')
        print(f"[DEBUG] 解析青龙配置: 分段数={len(configs)}")
        if len(configs) < 3:
            print(f"[ERROR] 青龙配置格式错误，需要3段，实际{len(configs)}段")
            return False

        host, client_id, client_secret = configs[0].strip(), configs[1].strip(), configs[2].strip()
        print(f"[DEBUG] 青龙地址: {host}")
        print(f"[DEBUG] ClientID: {client_id[:10]}...")

        ql_token = get_ql_token(host, client_id, client_secret)
        if not ql_token:
            print("[ERROR] 获取青龙token失败")
            return False
        print(f"[DEBUG] 获取token成功: {ql_token[:20]}...")

        headers = {'Authorization': f'Bearer {ql_token}', 'Content-Type': 'application/json'}

        try:
            print(f"[DEBUG] 查询已存在变量: searchValue={ql_envname}")
            envs_r = requests.get(f'{host}/open/envs', headers=headers, params={'searchValue': ql_envname}, timeout=10, verify=False)
            print(f"[DEBUG] 查询响应: status={envs_r.status_code}")
            if envs_r.status_code == 200:
                envs = envs_r.json().get('data', [])
                print(f"[DEBUG] 找到{len(envs)}个变量")
                for env in envs:
                    if env.get('name') == ql_envname and phone in str(env.get('remarks', '')):
                        env_id = env.get('_id') or env.get('id')
                        if env_id:
                            try:
                                del_r = requests.delete(f'{host}/open/envs', headers=headers, json=[env_id], timeout=10, verify=False)
                                print(f"[INFO] 删除旧变量: id={env_id}, status={del_r.status_code}")
                            except Exception as del_err:
                                print(f"[WARNING] 删除旧变量失败: {del_err}")
        except Exception as query_err:
            print(f"[WARNING] 查询变量失败: {query_err}")

        masked_phone = phone[:3] + "****" + phone[-4:] if len(phone) == 11 else phone
        remarks = f"捷停车:{phone}|用户:{userid}|手机:{masked_phone}|到期:{expire_date}|捷停车管理"
        data = [{'name': ql_envname, 'value': env_value, 'remarks': remarks}]

        print(f"[DEBUG] 添加新变量: name={ql_envname}, value长度={len(env_value)}")
        add_r = requests.post(f'{host}/open/envs', headers=headers, json=data, timeout=10, verify=False)
        print(f"[DEBUG] 添加响应: status={add_r.status_code}")

        if add_r.status_code != 200:
            print(f"[ERROR] 添加变量失败: HTTP {add_r.status_code}, body={add_r.text[:200]}")
            return False

        result = add_r.json()
        print(f"[DEBUG] 添加结果: code={result.get('code')}, message={result.get('message', 'None')}")

        if result.get('code') != 200:
            print(f"[ERROR] 添加变量失败: {result.get('message', '未知错误')}")
            return False

        new_ids = []
        for item in result.get('data', []):
            new_id = item.get('_id') or item.get('id')
            if new_id:
                new_ids.append(new_id)

        print(f"[DEBUG] 准备启用变量: ids={new_ids}")
        if new_ids:
            try:
                enable_r = requests.put(f'{host}/open/envs/enable', headers=headers, json=new_ids, timeout=10, verify=False)
                print(f"[INFO] 启用变量: status={enable_r.status_code}, ids={new_ids}")
            except Exception as enable_err:
                print(f"[WARNING] 启用变量失败: {enable_err}")

        print(f"[SUCCESS] 推送青龙成功: {phone}")
        return True
    except Exception as e:
        import traceback
        print(f"[ERROR] 推送青龙异常: {str(e)}")
        print(f"[ERROR] 异常堆栈: {traceback.format_exc()}")
        return False



def get_daidai_client(config: dict):
    if DadaiPanelClient is None: return None
    daidai_config = config.get('daidai_config', '')
    if not daidai_config: return None
    ql_envname = config.get('ql_envname', 'JT_TOKEN')
    config.get('daidai_group', PROJECT_NAME)
    try:
        client = DadaiPanelClient(ql_envname, daidai_config, project_name=PROJECT_NAME)
        return client if client.is_configured() else None
    except:
        return None

def push_to_daidai(account_id: str, phone: str, expire_date: str, config: dict, user_id: str = None) -> bool:
    client = get_daidai_client(config)
    if not client: return False
    try:
        user_accounts = get_user_accounts(user_id)
        if account_id not in user_accounts: return False
        account = user_accounts[account_id]
        env_value = account.get('data', '')
        if not env_value or '#' not in env_value: return False
        remarks = f"捷停车:{phone}|用户:{userid}|到期:{expire_date}"
        return client.update_env(username=phone, env_value=env_value, remark=remarks)
    except:
        return False

def delete_from_daidai(phone: str, config: dict) -> bool:
    client = get_daidai_client(config)
    if not client: return False
    try:
        return client.delete_env(phone)
    except:
        return False

def sync_to_panel(account_id: str, phone: str, expire_date: str, config: dict, user_id: str = None) -> bool:
    if config.get('use_daidai'):
        return push_to_daidai(account_id, phone, expire_date, config, user_id)
    ql_config = config.get('ql_config', '')
    ql_envname = config.get('ql_envname', 'JT_TOKEN')
    if ql_config:
        return push_to_qinglong(account_id, phone, expire_date, ql_config, ql_envname, user_id)
    return False

def delete_from_panel(phone: str, config: dict) -> bool:
    if config.get('use_daidai'):
        return delete_from_daidai(phone, config)
    ql_config = config.get('ql_config', '')
    ql_envname = config.get('ql_envname', 'JT_TOKEN')
    if ql_config:
        return delete_from_qinglong(phone, ql_config, ql_envname)
    return False

def get_panel_name(config: dict) -> str:
    return "呆呆" if config.get('use_daidai') else "青龙"

def is_panel_configured(config: dict) -> bool:
    if config.get('use_daidai'):
        return bool(config.get('daidai_config'))
    return bool(config.get('ql_config'))














def upload_all_to_qinglong() -> bool:
    if not sender.isAdmin():
        sender.reply("❌ 您没有管理员权限！")
        return False
    config = get_config()
    pn = get_panel_name(config)
    if not is_panel_configured(config):
        sender.reply(f"❌ 未配置{pn}面板！\n请先配置对应面板信息")
        return False

    use_daidai = config.get('use_daidai', False)

    if use_daidai:
        sender.reply("🔄 正在同步数据到呆呆面板...")
        try: users = sg.bucketAllKeys(bucket=BUCKET_ACCOUNTS) or []
        except: users = []
        success_count, skip_count = 0, 0
        for uid in users:
            ua = get_user_accounts(uid)
            for aid, acc in ua.items():
                auth_st = acc.get('auth_status', {})
                if not auth_st.get('is_authorized', False): skip_count += 1; continue
                et = auth_st.get('expire_time', '')
                if et:
                    try:
                        if datetime.strptime(et, '%Y-%m-%d').date() < datetime.now().date(): skip_count += 1; continue
                    except: pass
                ev = acc.get('data', '')
                if not ev or '#' not in ev: skip_count += 1; continue
                ph = acc.get('phone', '')
                if sync_to_panel(aid, ph, et, config): success_count += 1
        sender.reply(f"✅ 呆呆同步完成！\n🔄 推送成功: {success_count}个\n⏭️ 跳过: {skip_count}个")
        return True

    ql_config = config.get('ql_config', '')
    ql_envname = config.get('ql_envname', 'JT_TOKEN')
    sender.reply("🔄 正在获取青龙面板变量...")
    configs = ql_config.split('丨') if '丨' in ql_config else ql_config.split('|')
    if len(configs) < 3: sender.reply("❌ 青龙配置格式错误"); return False
    host, client_id, client_secret = configs[0].strip(), configs[1].strip(), configs[2].strip()
    ql_token = get_ql_token(host, client_id, client_secret)
    if not ql_token: sender.reply("❌ 获取青龙token失败"); return False
    headers = {'Authorization': f'Bearer {ql_token}', 'Content-Type': 'application/json'}
    try:
        envs_r = requests.get(f'{host}/open/envs', headers=headers, params={'searchValue': ql_envname}, timeout=10, verify=False)
        if envs_r.status_code != 200: sender.reply(f"❌ 获取青龙变量失败: HTTP {envs_r.status_code}"); return False
        ql_envs = [env for env in envs_r.json().get('data', []) if env.get('name') == ql_envname]
    except Exception as e: sender.reply(f"❌ 获取青龙变量异常: {e}"); return False
    ql_phones = {}
    for env in ql_envs:
        remarks = env.get('remarks', '')
        env_id = env.get('_id') or env.get('id')
        if '捷停车:' in remarks:
            phone = remarks.split('捷停车:')[1].split('|')[0].strip()
            if phone and env_id: ql_phones[phone] = env_id
    sender.reply(f"📊 青龙变量数: {len(ql_envs)}\n🔍 识别手机号: {len(ql_phones)}个\n🔄 正在匹配本地数据...")
    try: users = sg.bucketAllKeys(bucket=BUCKET_ACCOUNTS) or []
    except: users = []
    update_count, add_count, skip_count, fail_count = 0, 0, 0, 0
    for user_id in users:
        user_accounts = get_user_accounts(user_id)
        for account_id, account in user_accounts.items():
            phone = account.get('phone', '')
            auth_status = account.get('auth_status', {})
            if not auth_status.get('is_authorized', False): skip_count += 1; continue
            expire_time = auth_status.get('expire_time', '')
            if expire_time:
                try:
                    if datetime.strptime(expire_time, '%Y-%m-%d').date() < datetime.now().date(): skip_count += 1; continue
                except: pass
            env_value = account.get('data', '')
            if not env_value or '#' not in env_value: skip_count += 1; continue
            masked_phone = phone[:3] + "****" + phone[-4:] if len(phone) == 11 else phone
            remarks = f"捷停车:{phone}|用户:{user_id}|手机:{masked_phone}|到期:{expire_time}|捷停车管理"
            if phone in ql_phones:
                try:
                    update_data = {'id': ql_phones[phone], 'name': ql_envname, 'value': env_value, 'remarks': remarks}
                    r = requests.put(f'{host}/open/envs', headers=headers, json=update_data, timeout=10, verify=False)
                    if r.status_code == 200 and r.json().get('code') == 200: update_count += 1
                    else: fail_count += 1
                except: fail_count += 1
            else:
                try:
                    add_data = [{'name': ql_envname, 'value': env_value, 'remarks': remarks}]
                    r = requests.post(f'{host}/open/envs', headers=headers, json=add_data, timeout=10, verify=False)
                    if r.status_code == 200 and r.json().get('code') == 200: add_count += 1
                    else: fail_count += 1
                except: fail_count += 1
    sender.reply(f"✅ 青龙同步完成！\n📊 原有变量: {len(ql_envs)}\n🔄 更新: {update_count}\n➕ 新增: {add_count}\n⏭️ 跳过: {skip_count}\n❌ 失败: {fail_count}")
    return True

def main():
    try:
        config = get_config()
        command = sender.getMessage()

        if command == "捷停车登录" or command == "登录捷停车":
            process_login(config)
        elif command == "捷停车查询":
            query_accounts()
        elif command == "捷停车管理":
            batch_manage(config)
        elif command == "捷停车授权":
            batch_auth(config)
        elif command == "捷停车清理":
            if not sender.isAdmin():
                sender.reply("❌ 您没有管理员权限！")
                return
            cleanup_expired_data()
        elif command == "捷停车上传":
            upload_all_to_qinglong()
        else:
            sender.reply("未知指令，请发送「捷停车管理」查看账号管理")
    except Exception as e:
        sender.reply(f"❌ 执行异常: {str(e)}")

if __name__ == "__main__":
    main()
