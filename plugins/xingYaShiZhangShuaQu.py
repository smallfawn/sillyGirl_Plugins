# [title: 星芽时长刷取]
# [name: xingYaShiZhangShuaQu]
# [language: python]
# [class: 任务]
# [author: rujingxianghai]
# [version: v1.0.0]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(星芽|xydj)(刷时长)$|^(刷时长|刷取时长)(星芽|xydj)$|^星芽刷时长$]
# [icon: https://api.iconify.design/lucide:apple.svg]
# [description: 按分钟计费，快速刷取观看时长]
# [depe: ["requests"]]


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

def _sg_run(coro):
    try:
        _sg_asyncio.get_running_loop()
    except RuntimeError:
        return _sg_asyncio.run(coro)
    box={}
    def runner():
        try: box["v"]=_sg_asyncio.run(coro)
        except BaseException as e: box["e"]=e
    t=_sg_Thread(target=runner, daemon=True); t.start(); t.join()
    if "e" in box: raise box["e"]
    return box.get("v")

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

import os
import json
import time
import hashlib
import requests
import uuid

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()

PLUGIN_CONFIG = {
    'bucket': 's_xydj_duration',
    'name': '星芽时长刷取'
}

PAY_TYPE_NAMES = {
    'alipay': '支付宝',
    'wxpay': '微信支付',
    'qqpay': 'QQ钱包',
}


def get_user_config():
    """获取用户配置"""
    zsm = sg.bucketGet('s_xydj_duration', 'zsm') or ''
    price_per_minute = float(sg.bucketGet('s_xydj_duration', 'price_per_minute') or '0.01')
    ma_pay_switch = '2099-12-31' or 'false'

    return zsm, price_per_minute, ma_pay_switch

def generate_random_uuid():
    """生成随机UUID"""
    return str(uuid.uuid4())

def calculate_md5(text):
    """计算字符串的MD5值"""
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def sort_dict_by_key(data):
    """对字典按照键名排序"""
    return dict(sorted(data.items(), key=lambda x: x[0]))

def generate_qrcode(url):
    """生成二维码图片"""
    try:
        encoded_url = requests.utils.quote(url)
        api_url = f"https://api.qrtool.cn/?text={encoded_url}&size=300&level=M"
        return api_url
    except Exception as e:
        return None

def get_user_info_by_token(authorization, device_id):
    """通过authorization获取用户信息"""
    try:
        headers = {
            "Host": "speciesweb.whjzjx.cn",
            "pragma": "no-cache",
            "cache-control": "no-cache",
            "sec-ch-ua-platform": "Android",
            "authorization": authorization,
            "device_type": "TA-1361",
            "user_agent": "Mozilla/5.0 (Linux; Android 15; 2210132C Build/AQ3A.240912.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/130.0.6723.86 Mobile Safari/537.36 _dsbridge",
            "raw_channel": "default",
            "dev_token": "BR5G0PFyR-9NAkHgS1rSHb9OQ3MiEBxSDpv4-EZbrBjnMuxm5iYdf4ZUjcr9_LmAay6ZA10zo6p_mvCJPB30swIIDDvxiOqFf2Dtr05iL6kbzpkN4OaSGkXIanwRgb9FslgWBiRZIRV2nM3nrI_yccyFdRj0D0C8rc7AqCRRNtOM*",
            "accept": "application/json, text/plain, */*",
            "channel": "default",
            "device_id": device_id,
            "device_platform": "android",
            "app_version": "3.8.5",
            "device_brand": "nokia",
            "os_version": "15",
            "user-agent": "Mozilla/5.0 (Linux; Android 15; 2210132C Build/AQ3A.240912.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/130.0.6723.86 Mobile Safari/537.36 _dsbridge",
            "origin": "https://h5static.xingya.com.cn",
            "x-requested-with": "com.jz.xydj",
        }

        api_url = f"https://speciesweb.whjzjx.cn/v1/sign/info?device_id={device_id}"
        response = requests.get(api_url, headers=headers, timeout=10)

        if response.status_code == 200:
            result = response.json()
            if result.get("code") == "ok" and "data" in result:
                user_data = result["data"]
                return True, {
                    'user_id': user_data.get('account_id', ''),  # 修正字段名为account_id
                    'cash_remain': user_data.get('cash_remain', 0),
                    'species': user_data.get('species', 0)
                }
            else:
                return False, f"获取用户信息失败: {result.get('msg', '未知错误')}"
        else:
            return False, f"请求失败，状态码: {response.status_code}"

    except Exception as e:
        return False, f"获取用户信息异常: {str(e)}"

def add_viewing_duration(authorization, device_id, user_id, duration_minutes):
    """增加观看时长"""
    try:
        headers = {
            "x-app-id": "7",
            "authorization": authorization,
            "platform": "1",
            "manufacturer": "Xiaomi",
            "version_name": "3.8.3.1",
            "user_agent": "Mozilla/5.0 (Linux; Android 15; 2210132C Build/AQ3A.240812.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/131.0.6778.260 Mobile Safari/537.36",
            "app_version": "3.8.3.1",
            "device_platform": "android",
            "personalized_recommend_status": "1",
            "device_type": "2210132C",
            "device_brand": "Xiaomi",
            "os_version": "15",
            "channel": "default",
            "raw_channel": "default",
            "uuid": f"randomUUID_{generate_random_uuid()}",
            "device_id": device_id,
            "ab_id": "",
            "support_h265": "1",
            "font_scale": "1.0",
            "content-type": "application/json; charset=utf-8"
        }

        current_timestamp = int(time.time() * 1000)

        duration_seconds = duration_minutes * 60

        request_body = [
            {
                "event_id": "action_episode_view",
                "page_id": "page_drama_detail",
                "eventType": "action",
                "event_type": "action",
                "timestamp": current_timestamp,
                "user_id": str(user_id),
                "login_status": True,
                "retry": 0,
                "device_id": device_id,
                "device_type": "Xiaomi",
                "phone_version": "2210132C",
                "os_type": 1,
                "os_name": "15",
                "version": "3.8.3.1",
                "package_name": "com.jz.xydj",
                "app_id": "7",
                "channel": "default",
                "raw_channel": "default",
                "font_scale": 1.0,
                "define_args": json.dumps({
                    "page": "page_drama_detail",
                    "theater_id": "4328",
                    "theater_number": "1",
                    "theater_duration": str(duration_seconds),
                    "lock": "0",
                    "complete": "0",
                    "show_id": "7de1f4a3cfb04c93bb31c11f7e896ad8",
                    "classification_id": "0",
                    "position": "4",
                    "entrance_scene": "0",
                    "entrance": "5",
                    "top_classification_id": "1",
                    "top_classification_name": "剧场",
                    "ab_id": "",
                    "last_page": "page_drama_detail"
                })
            }
        ]

        response = requests.post(
            "https://xingya-track.shytkjgs.com/receive",
            headers=headers,
            json=request_body,
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()
            if result.get("code") == "ok":
                return True, f"成功增加 {duration_minutes} 分钟观看时长"
            else:
                return False, f"增加时长失败: {result.get('msg', '未知错误')}"
        else:
            return False, f"请求失败，状态码: {response.status_code}"

    except Exception as e:
        return False, f"增加观看时长异常: {str(e)}"

def create_mapi_payment(config, amount, out_trade_no, name, user_id, pay_type, sitename=""):
    return True

def query_mapi_order(config, order_no, is_trade_no=False):
    """查询订单状态"""
    try:
        api_url = config['gateway']
        if api_url.endswith('/'):
            api_url = api_url[:-1]

        query_url = f"{api_url}/xpay/epay/api.php"

        params = {
            'act': 'order',
            'pid': config['pid'],
            'key': config['key']
        }

        if is_trade_no:
            params['trade_no'] = order_no
        else:
            params['out_trade_no'] = order_no

        response = requests.get(query_url, params=params, timeout=10)

        if response.status_code != 200:
            return False, None, f"查询订单失败，HTTP状态码: {response.status_code}"

        try:
            result = response.json()
        except:
            return False, None, "查询订单失败，返回数据格式错误"

        code = result.get('code', 0)
        msg = result.get('msg', '未知状态')

        if code == 1:  # 查询成功
            status = result.get('status', 0)
            if status == 1:  # 支付成功
                return True, result, "支付成功"
            else:
                return True, result, "订单未支付"
        else:
            return False, result, msg

    except Exception as e:
        return False, None, f"查询订单异常: {str(e)}"

def poll_mapi_payment_status(config, order_no, max_tries=30):
    return True

def handle_mapay_order(project, duration_minutes, money, pay_type=None):
    return True

def pay_order_wxpay(project, duration_minutes, money):
    return True

def process_duration_purchase():
    """处理时长使用流程"""
    sender.reply("""
=====星芽时长刷取=====
💡 输入您的账号信息和刷取时长
回复"q"随时退出操作
==================""")

    sender.reply("请输入您的账号信息（格式: authorization#device_id）:")
    account_input = sender.input(120000, 1, False)
    if not account_input:
        sender.reply("⏰ 操作超时,已退出")
        return
    elif account_input.lower() == 'q':
        sender.reply("✅ 已取消操作")
        return

    if '#' not in account_input:
        sender.reply("""
=====格式错误=====
❌ 账号信息格式不正确
------------------
请使用格式: authorization#device_id
例如: eyJhbGc...#87387123-7A4D-4B6A-912A
==================""")
        return

    try:
        authorization, device_id = account_input.split('#', 1)
        authorization = authorization.strip()
        device_id = device_id.strip()

        if not authorization or not device_id:
            sender.reply("""
=====格式错误=====
❌ authorization或device_id不能为空
------------------
请检查输入格式是否正确
==================""")
            return
    except ValueError:
        sender.reply("""
=====格式错误=====
❌ 账号信息格式不正确
------------------
请使用格式: authorization#device_id
==================""")
        return

    sender.reply("正在验证账号信息...")
    success, user_info = get_user_info_by_token(authorization, device_id)

    if not success:
        sender.reply(f"""
=====验证失败=====
❌ {user_info}
------------------
请检查authorization和device_id是否正确
==================""")
        return

    user_id = user_info['user_id']
    if not user_id:
        sender.reply("""
=====验证失败=====
❌ 无法获取用户ID
------------------
请确认账号信息是否正确
==================""")
        return

    sender.reply(f"""
=====账号验证成功=====
👤 用户ID: {user_id}
💰 现金余额: {user_info.get('cash_remain', 0)}元
🪙 金币数量: {user_info.get('species', 0)}
==================""")

    sender.reply("请输入需要刷取的时长（分钟）:")
    duration_input = sender.input(120000, 1, False)
    if not duration_input:
        sender.reply("⏰ 操作超时,已退出")
        return
    elif duration_input.lower() == 'q':
        sender.reply("✅ 已取消操作")
        return

    try:
        duration_minutes = int(duration_input)
        if duration_minutes <= 0:
            sender.reply("❌ 时长必须大于0分钟")
            return
    except ValueError:
        sender.reply("❌ 请输入有效的数字")
        return

    zsm, price_per_minute, ma_pay_switch = get_user_config()

    total_price = duration_minutes * price_per_minute

    available_payments = []

    if ma_pay_switch.lower() == 'true':
        ma_pay_type = '2099-12-31' or ''
        ma_pay_pid = '2099-12-31' or ''
        ma_pay_key = '2099-12-31' or ''
        ma_pay_gateway = '2099-12-31' or ''

        if ma_pay_gateway and ma_pay_pid and ma_pay_key:
            pay_types_str = ma_pay_type.strip()
            if not pay_types_str:
                pay_types_str = "alipay,wxpay"  # 默认支付方式

            pay_types = [p.strip() for p in pay_types_str.split(',') if p.strip()]
            for pay_type in pay_types:
                name = PAY_TYPE_NAMES.get(pay_type, pay_type)
                available_payments.append((name, f"mapay_{pay_type}"))
        else:
            if zsm:
                available_payments.append(("微信支付", "wxpay"))
    else:
        if zsm:
            available_payments.append(("微信支付", "wxpay"))

    if not available_payments:
        sender.reply("""
=====使用失败=====
❌ 未配置任何支付方式
------------------
请检查配置配置支付方式
==================""")
        return

    if len(available_payments) == 1:
        payment_name, payment_type = available_payments[0]
    else:
        payment_menu = f"""
=====选择支付方式=====
⏱️ 刷取时长: {duration_minutes}分钟
💰 总金额: {total_price:.2f}元
💸 单价: {price_per_minute:.2f}元/分钟
------------------------"""

        for i, (name, _) in enumerate(available_payments, 1):
            payment_menu += f"""
[{i}] {name}"""

        payment_menu += """
------------------------
回复数字选择方式
回复"q"退出操作
=================="""

        sender.reply(payment_menu)

        pay_choice = sender.input(120000, 1, False)
        if not pay_choice or pay_choice.lower() == 'q':
            sender.reply("✅ 已取消使用")
            return

        try:
            choice_index = int(pay_choice) - 1
            if not (0 <= choice_index < len(available_payments)):
                sender.reply("❌ 无效的选择")
                return

            payment_name, payment_type = available_payments[choice_index]
        except ValueError:
            sender.reply("❌ 请输入有效的数字")
            return

    if payment_type == "wxpay":
        if pay_order_wxpay('星芽时长刷取', duration_minutes, total_price):
            sender.reply("✅ 支付成功，正在刷取时长...")
            success, message = add_viewing_duration(authorization, device_id, user_id, duration_minutes)

            if success:
                sender.reply(f"""
=====刷取成功=====
✅ {message}
👤 用户ID: {user_id}
⏱️ 刷取时长: {duration_minutes}分钟
💰 支付金额: {total_price:.2f}元
==================""")
            else:
                sender.reply(f"""
=====刷取失败=====
❌ {message}
------------------
💡 支付已完成，请检查配置处理
==================""")

    elif payment_type.startswith("mapay_"):
        actual_pay_type = payment_type[6:]

        result = handle_mapay_order('星芽时长刷取', duration_minutes, total_price, actual_pay_type)

        if result:
            sender.reply("✅ 支付成功，正在刷取时长...")
            success, message = add_viewing_duration(authorization, device_id, user_id, duration_minutes)

            if success:
                sender.reply(f"""
=====刷取成功=====
✅ {message}
👤 用户ID: {user_id}
⏱️ 刷取时长: {duration_minutes}分钟
💰 支付金额: {total_price:.2f}元
==================""")
            else:
                sender.reply(f"""
=====刷取失败=====
❌ {message}
------------------
💡 支付已完成，请检查配置处理
==================""")

def show_tutorial():
    """显示使用教程"""
    tutorial = """
=====星芽时长刷取教程=====
1. 获取账号信息:
  • authorization: 星芽APP的登录令牌
  • device_id: 设备唯一标识符

2. 获取方法:
  • 使用抓包工具（如HttpCanary）
  • 登录星芽短剧APP
  • 找到任意API请求的请求头

3. 账号信息格式:
  • 格式: authorization#device_id
  • 示例: eyJhbGciOiJIUz...#87387123-7A4D-4B6A

4. 使用流程:
  • 发送指令触发插件
  • 输入账号信息（authorization#device_id）
  • 输入需要刷取的时长（分钟）
  • 选择支付方式并完成支付
  • 系统自动刷取时长

5. 计费规则:
  • 按分钟计费
  • 当前价格: 每分钟 XXX 元

6. 支付方式:
  • 支持支付宝/微信支付
  • 支付完成后立即刷取

7. 注意事项:
  • 确保账号信息格式正确
  • 使用#号分隔两个参数
  • 时长立即生效
  • 刷取失败支持退款

如有问题请检查配置
=================="""
    sender.reply(tutorial)

def main():
    usermessage = sender.getMessage()

    if '时长' in usermessage or '刷取' in usermessage:
        if '教程' in usermessage or '帮助' in usermessage:
            show_tutorial()
        else:
            process_duration_purchase()
    else:
        sender.setContinue()

if __name__ == "__main__":
    main()
