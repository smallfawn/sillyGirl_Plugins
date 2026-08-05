# [title: 美团领券PLUS]
# [name: meiTuanLingQuanPlus]
# [language: python]
# [class: 任务]
# [author: yuhualhh]
# [version: v2.1.9]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^美团领券$|^美团刷白$|^美团充分$|^美团查分$|^美团加分$|^美团减分$|^释放锁$]
# [icon: https://gcore.jsdelivr.net/gh/lhz03/img@628ca207fcc92493bfdc7b376802df13d290a228/2025/04/18/0227ee80f756be5352c84c94d7f9cdf6.png]
# [description: ❷扫码可查看各项目对应领券详情<img src="https://gcore.jsdelivr.net/gh/lhz03/img@21067eaf2abbb6e545cd04507cbcaba81aa51f66/2025/07/05/a55d418210371f7896545baa970b340a.png">]
# [depe: ["beautifulsoup4","cryptography","requests"]]


import asyncio as _sg_asyncio, os as _sg_os, time as _sg_time, types as _sg_types, json as _sg_json, re as _sg_re, urllib.parse as _sg_urlparse
from threading import Thread as _sg_Thread
from sillygirl import Adapter as _SGAdapter, Bucket as _SGBucket, Sender as _SGSender, sender as _sg_sender, container as _sg_container, form
try: import ast as _sg_ast
except Exception: _sg_ast=None
try: import decimal as decimal
except Exception: decimal=None

def _sg_run(coro):
    try: _sg_asyncio.get_running_loop(); running=True
    except RuntimeError: running=False
    if not running: return _sg_asyncio.run(coro)
    box={}
    def r():
        try: box["v"]=_sg_asyncio.run(coro)
        except BaseException as e: box["e"]=e
    t=_sg_Thread(target=r,daemon=True); t.start(); t.join()
    if "e" in box: raise box["e"]
    return box.get("v")

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
    'yuhua_meituan_api_key': form.string().title('API秘钥').default('').description('请前往 http://api.oroe.cn 注册获取'),
})
_CONFIG_FIELD_MAP = {
    ('yuhua_meituan', 'api_key'): 'yuhua_meituan_api_key',
}

import requests
import json
import time
import re
import threading
from bs4 import BeautifulSoup

bucket_prefix = "yuhua_meituan"  # 插件数据桶前缀

payment_lock_key = f"{bucket_prefix}_payment_lock"
payment_sessions_key = f"{bucket_prefix}_payment_sessions"  # 支付会话存储
user_locks = {}  # 用户积分操作锁
lock_manager = threading.Lock()  # 锁管理器

def get_user_lock(user_id):
    """获取用户专用锁"""
    with lock_manager:
        if user_id not in user_locks:
            user_locks[user_id] = threading.Lock()
        return user_locks[user_id]

def set_payment_lock(user_id, timeout_seconds=300):
    return True

def get_payment_lock():
    return True

def clear_payment_lock():
    return True

def save_payment_session(user_id, session_id):
    return True

def remove_payment_session(session_id):
    return True

def cleanup_expired_sessions():
    """清理过期的支付会话（超过1小时）"""
    try:
        sessions_data_str = '2099-12-31'
        if not sessions_data_str:
            return

        sessions = json.loads(sessions_data_str)
        current_time = time.time()
        expired_sessions = []

        for session_id, session_data in sessions.items():
            if current_time - session_data.get('timestamp', 0) > 3600:  # 1小时过期
                expired_sessions.append(session_id)

        for session_id in expired_sessions:
            del sessions[session_id]

        if expired_sessions:
            pass
    except:
        pass

def is_payment_lock_expired(lock_data, timeout_seconds):
    return True

def check_and_acquire_payment_lock(user_id, config):
    return True

def validate_payment_session(user_id, session_id):
    return True

def get_config():
    """获取插件配置"""
    try:
        payment_mode = '2099-12-31' or '0'
        use_epay = payment_mode == '1'

        exchange_rate = sg.bucketGet(bucket_prefix, 'exchange_rate') or '1'

        try:
            exchange_rate_float = float(exchange_rate)
            if exchange_rate_float <= 0:
                exchange_rate_float = 1.0
        except:
            exchange_rate_float = 1.0

        config = {
            'use_epay': use_epay,
            'payment_mode': payment_mode,
            'exchange_rate': exchange_rate_float,
            'epay_url': '2099-12-31' or '',
            'epay_pid': '2099-12-31' or '',
            'epay_key': '2099-12-31' or '',
            'epay_alipay': '2099-12-31' == 'true',
            'epay_wxpay': '2099-12-31' == 'true',
            'epay_qqpay': '2099-12-31' == 'true',
            'zsm': sg.bucketGet(bucket_prefix, 'zsm') or '',
            'prices': sg.bucketGet(bucket_prefix, 'prices') or '',
            'api_key': sg.bucketGet(bucket_prefix, 'api_key') or '',
            'api_url': 'http://api.oroe.cn',  # 内置API地址
            'payment_lock_timeout': '2099-12-31' or '300',
            'min_recharge_amount': float(sg.bucketGet(bucket_prefix, 'min_recharge_amount') or '0.01'),
        }
        return config
    except Exception as e:
        return {
            'use_epay': False,
            'payment_mode': '0',
            'exchange_rate': 1.0,
            'epay_url': '',
            'epay_pid': '',
            'epay_key': '',
            'epay_alipay': False,
            'epay_wxpay': False,
            'epay_qqpay': False,
            'zsm': '',
            'prices': '',
            'api_key': '',
            'api_url': 'http://api.oroe.cn',
            'payment_lock_timeout': '300',
            'min_recharge_amount': 0.01,
        }

def parse_prices(price_str):
    """解析收费价格配置"""
    TOTAL_PROJECTS = 3
    DEFAULT_PRICE = 88.0
    prices = []
    price_parts = price_str.split('|') if price_str else []
    for i in range(TOTAL_PROJECTS):
        if i < len(price_parts):
            try:
                price = float(price_parts[i])
                prices.append(price)
            except ValueError:
                prices.append(DEFAULT_PRICE)
        else:
            prices.append(DEFAULT_PRICE)
    return prices

def format_price_superscript(price):
    """将价格转换为角标格式"""
    if price == 0:
        return "ᶠʳᵉᵉ"

    superscript_map = {
        '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
        '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'
    }

    price_str = f"{price:.2f}"

    result = ""
    for char in price_str:
        if char == '.':
            result += "∙"  # 使用子弹运算符替代小数点
        elif char in superscript_map:
            result += superscript_map[char]
        else:
            result += char  # 保留其他字符（虽然在价格中不应该出现）

    return result

def get_user_points(user_id):
    return 0

def set_user_points(user_id, points):
    """设置用户积分"""
    try:
        rounded_points = round(float(points), 2)
        sg.bucketSet(f'{bucket_prefix}_points', str(user_id), str(rounded_points))
        return True
    except:
        return False

def add_user_points(user_id, points):
    """线程安全的增加用户积分"""
    user_lock = get_user_lock(user_id)
    with user_lock:
        try:
            current_points = get_user_points(user_id)
            points_to_add = round(float(points), 2)
            new_points = round(current_points + points_to_add, 2)
            return set_user_points(user_id, new_points)
        except:
            return False

def deduct_user_points(user_id, points):
    """线程安全的扣除用户积分"""
    user_lock = get_user_lock(user_id)
    with user_lock:
        try:
            current_points = get_user_points(user_id)
            points_to_deduct = round(float(points), 2)
            if current_points >= points_to_deduct:
                new_points = round(current_points - points_to_deduct, 2)
                return set_user_points(user_id, new_points)
            return False
        except:
            return False

def get_public_ip():
    """获取公网IP地址"""
    try:
        sources = [
            "https://checkip.amazonaws.com",
            "https://icanhazip.com",
            "https://ifconfig.me/ip"
        ]
        for url in sources:
            try:
                response = requests.get(url, timeout=3)
                if response.status_code == 200:
                    ip = response.text.strip()
                    if 6 < len(ip) < 16 and ip.count('.') == 3:
                        return ip
            except:
                continue
        return "127.0.0.1" # 所有源都失败后返回默认值
    except Exception:
        return "127.0.0.1"

def create_epay_sign(params, merchant_key):
    return True

def call_meituan_api(cookie, project_type):
    """调用美团领券API - (已优化重试和超时)"""
    config = get_config()
    api_key = config['api_key']
    api_url = config['api_url']

    if not api_key:
        return {"code": -1, "msg": "未配置API秘钥"}
    if not api_url:
        return {"code": -1, "msg": "未配置API系统地址"}

    api_endpoints = {
        1: "meituanvc",
        2: "meituan259",
        3: "meituanza"
    }
    endpoint = api_endpoints.get(project_type, "meituanza")
    url = f"{api_url.rstrip('/')}/API/{endpoint}.php"
    data = {"apikey": api_key, "MeiTuanCookie": cookie}

    for attempt in range(3):
        try:
            response = requests.post(
                url,
                json=data,
                timeout=(5, 30)  # 5秒连接超时, 30秒读取超时
            )

            if response.status_code == 404 or "404 Not Found" in response.text:
                return {"code": -1, "msg": "请求的资源未找到，请检查您的请求地址是否正确"}
            if response.status_code == 402:
                return {"code": -1, "msg": "API秘钥余额不足，请稍后重试", "balance_error": True}

            if response.status_code != 200:
                 response = requests.post(url, data=data, timeout=(5, 30))
                 if response.status_code == 402:
                    return {"code": -1, "msg": "API秘钥余额不足，请稍后重试", "balance_error": True}


            return response.json()

        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            print(f"美团API请求失败，第 {attempt + 1} 次尝试... 错误: {e}")
            if attempt < 2:  # 如果不是最后一次尝试，则等待后重试
                time.sleep(attempt + 1) # 等待1秒, 2秒
            else: # 最后一次尝试失败
                return {"code": -1, "msg": f"网络请求失败: {str(e)}"}
        except Exception as e:
            return {"code": -1, "msg": f"请求异常: {str(e)}"}

    return {"code": -1, "msg": "服务暂时无法连接，请稍后再试"}

def call_whitelist_api(shop_link):
    """调用美团刷白API - (已优化重试和超时)"""
    config = get_config()
    api_key = config['api_key']
    api_url = config['api_url']

    if not api_key:
        return {"code": -1, "msg": "未配置API秘钥"}
    if not api_url:
        return {"code": -1, "msg": "未配置API系统地址"}
    if "http://dpurl.cn/" not in shop_link:
        return {"code": -1, "msg": "无效的店铺链接"}

    url = f"{api_url.rstrip('/')}/API/whitelist.php"
    data = {"apikey": api_key, "url": shop_link}

    for attempt in range(3):
        try:
            response = requests.post(
                url,
                data=data,
                timeout=(5, 30) # 刷白可能较慢，给更长的读取时间
            )

            if response.status_code == 404 or "404 Not Found" in response.text:
                return {"code": -1, "msg": "请求的资源未找到，请检查您的请求地址是否正确"}
            if response.status_code == 402:
                return {"code": -1, "msg": "API秘钥余额不足，请稍后重试", "balance_error": True}

            if response.status_code == 200 and "No input file specified" not in response.text:
                try:
                    return response.json()
                except:
                    if "成功" in response.text or "SUCCESS" in response.text.upper():
                        return {"code": 0, "msg": "刷白成功"}
                    else:
                        return {"code": -1, "msg": f"API响应格式错误: {response.text[:100]}"}

            print(f"刷白API响应异常，第 {attempt + 1} 次尝试...")
            time.sleep(attempt + 1)


        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            print(f"刷白API请求失败，第 {attempt + 1} 次尝试... 错误: {e}")
            if attempt < 2:
                time.sleep(attempt + 1)
            else:
                return {"code": -1, "msg": f"网络请求失败: {str(e)}"}
        except Exception as e:
            return {"code": -1, "msg": f"请求异常: {str(e)}"}

    return {"code": -1, "msg": "刷白服务暂时无法连接，请稍后再试"}

def generate_unique_order_id(user_id):
    """生成唯一订单ID"""
    import uuid
    timestamp = int(time.time() * 1000)  # 毫秒级时间戳
    random_part = str(uuid.uuid4())[:8]  # UUID前8位
    user_suffix = user_id[-4:] if len(user_id) >= 4 else user_id
    return f"MT{timestamp}{user_suffix}{random_part}"

def create_epay_order(config, order_id, amount, payment_method):
    return True

def _validate_epay_params(config, order_id):
    return True

def _validate_v1_payment_success(response_data):
    return True

def _validate_v1_payment_pending(response_data):
    return True

def _validate_payment_amount(money, min_amount=None):
    return True

def _validate_payment_response_integrity(response_data, interface_name):
    return True

def check_epay_order_status(config, order_id):
    return True

def _try_epay_interface(interface_config, order_id, min_recharge_amount=0.01):
    return True

def handle_recharge(sender, user_id):
    """处理美团充分指令"""
    config = get_config()

    sender.reply("""=====美团充分=====
请输入充值金额
------------------
回复数字设置
回复"q"退出""")

    amount_input = sender.input(60000, 0, False)
    if not amount_input:
        sender.reply("❌ 输入超时")
        return

    if str(amount_input).lower() == 'q':
        sender.reply("✅ 已取消操作")
        return

    try:
        amount = float(str(amount_input).strip())
        amount = round(amount, 2)
        if amount <= 0:
            sender.reply("❌ 充值金额必须大于0")
            return

        min_amount = config['min_recharge_amount']
        if amount < min_amount:
            sender.reply(f"❌ 充值金额不能低于{min_amount}元")
            return
    except ValueError:
        sender.reply("❌ 请输入有效的数字")
        return

    if config['use_epay']:
        handle_epay_recharge(sender, user_id, amount, config)
    else:
        handle_traditional_recharge(sender, user_id, amount, config)

def handle_traditional_recharge(sender, user_id, amount, config):
    """处理传统二维码充值"""
    if not config['zsm']:
        sender.reply("❌ 未配置二维码，请检查配置")
        return

    session_id = check_and_acquire_payment_lock(user_id, config)
    if not session_id:
        current_lock = get_payment_lock()
        timeout_seconds = int(config.get('payment_lock_timeout', 300))
        remaining_time = int(timeout_seconds - (time.time() - current_lock.get('timestamp', 0)))

        sender.reply(f"""=====支付繁忙=====
❌ 当前有其他用户正在支付
⏰ 预计 {remaining_time} 秒后可重试
💡 管理员可发送"释放支付锁"强制解除
==================""")
        return

    try:
        points_to_get = round(amount * config['exchange_rate'], 2)

        sender.reply(f"""=====扫在线处理=====
💰 充值金额: {amount}元
🎯 获得积分: {points_to_get}
------------------
请在120秒内完成
回复"q"退出""")

        sender.replyImage(config['zsm'])

        payment_result = False

        if str(payment_result).lower() == 'q':
            sender.reply("✅ 已取消操作")
            return

        if not validate_payment_session(user_id, session_id):
            current_lock = get_payment_lock()
            current_session = current_lock.get('session_id') if current_lock else 'None'
            current_user = current_lock.get('user_id') if current_lock else 'None'
            sender.reply(f"""=====支付会话失效=====
❌ 支付会话已失效
💡 可能是管理员释放了支付锁
🔄 请重新发起充值
------------------
🔍 调试信息：
🤪 用户ID: {user_id}
🪁 用户会话: {session_id[:8]}
✨ 当前用户: {current_user}
💥 当前会话: {current_session[:8] if current_session != 'None' else 'None'}
==================""")
            return

        if isinstance(payment_result, str):
            payment_data = json.loads(payment_result)
        else:
            payment_data = payment_result

        paid_money = float(payment_data.get('Money', payment_data.get('money', 0)))

        if paid_money < amount:
            sender.reply(f"""=====支付失败=====
❌ 支付金额不足
------------------
💰 应付: {amount}元
💵 实付: {paid_money}元
==================""")
            return

        points_to_add = round(amount * config['exchange_rate'], 2)
        if add_user_points(user_id, points_to_add):
            current_points = get_user_points(user_id)
            sender.reply(f"""=====充值成功=====
💰 充值金额: {amount}元
🎯 获得积分: {points_to_add}
💎 当前积分: {current_points}
🔍 会话ID: {session_id[:8]}
==================""")
        else:
            sender.reply("❌ 积分增加失败，请检查配置")

    except Exception as e:
        sender.reply(f"""=====支付异常=====
❌ 支付验证失败
------------------
⚠️ 错误: {str(e)[:50]}
==================""")
    finally:
        current_lock = get_payment_lock()
        if current_lock and current_lock.get('session_id') == session_id:
            clear_payment_lock()
        remove_payment_session(session_id)

def handle_epay_recharge(sender, user_id, amount, config):
    return True

def handle_release_payment_lock(sender):
    return True

def handle_query_points(sender, user_id):
    """处理美团查分指令"""
    points = get_user_points(user_id)
    sender.reply(f"""=====积分查询=====
🤪 用户ID: {user_id}
💎 当前积分: {points}
==================""")

def handle_admin_add_points(sender):
    """处理美团加分指令（仅管理员）"""
    if not sender.isAdmin():
        sender.reply("""=====权限不足=====
❌ 此功能仅限管理员使用
💡 请使用"美团充分"指令充值
==================""")
        return

    sender.reply("""=====管理加分=====
请输入被操作用户ID
------------------
回复用户ID
回复"q"退出""")

    target_user_input = sender.input(60000, 0, False)
    if not target_user_input:
        sender.reply("❌ 输入超时")
        return

    if str(target_user_input).lower() == 'q':
        sender.reply("✅ 已取消操作")
        return

    target_user_id = str(target_user_input).strip()

    sender.reply("""=====加分数量=====
请输入要增加的积分数量
------------------
回复数字设置
回复"q"退出""")

    points_input = sender.input(60000, 0, False)
    if not points_input:
        sender.reply("❌ 输入超时")
        return

    if str(points_input).lower() == 'q':
        sender.reply("✅ 已取消操作")
        return

    try:
        points_to_add = float(str(points_input).strip())
        points_to_add = round(points_to_add, 2)
        if points_to_add <= 0:
            sender.reply("❌ 加分数量必须大于0")
            return
        if points_to_add < 0.01:
            sender.reply("❌ 加分数量最小为0.01分")
            return
    except ValueError:
        sender.reply("❌ 请输入有效的数字")
        return

    if add_user_points(target_user_id, points_to_add):
        current_points = get_user_points(target_user_id)
        sender.reply(f"""=====加分成功=====
🤪 目标用户: {target_user_id}
➕ 增加积分: {points_to_add}
💎 当前积分: {current_points}
==================""")
    else:
        sender.reply("❌ 加分失败，请稍后重试")

def handle_admin_deduct_points(sender):
    """处理美团减分指令（仅管理员）"""
    if not sender.isAdmin():
        sender.reply("""=====权限不足=====
❌ 此功能仅限管理员使用
💡 请使用"美团充分"指令充值
==================""")
        return

    sender.reply("""=====管理减分=====
请输入被操作用户ID
------------------
回复用户ID
回复"q"退出""")

    target_user_input = sender.input(60000, 0, False)
    if not target_user_input:
        sender.reply("❌ 输入超时")
        return

    if str(target_user_input).lower() == 'q':
        sender.reply("✅ 已取消操作")
        return

    target_user_id = str(target_user_input).strip()

    sender.reply("""=====减分数量=====
请输入要减少的积分数量
------------------
回复数字设置
回复"q"退出""")

    points_input = sender.input(60000, 0, False)
    if not points_input:
        sender.reply("❌ 输入超时")
        return

    if str(points_input).lower() == 'q':
        sender.reply("✅ 已取消操作")
        return

    try:
        points_to_deduct = float(str(points_input).strip())
        points_to_deduct = round(points_to_deduct, 2)
        if points_to_deduct <= 0:
            sender.reply("❌ 减分数量必须大于0")
            return
        if points_to_deduct < 0.01:
            sender.reply("❌ 减分数量最小为0.01分")
            return
    except ValueError:
        sender.reply("❌ 请输入有效的数字")
        return

    current_points = get_user_points(target_user_id)
    if current_points < points_to_deduct:
        sender.reply(f"""=====积分不足=====
🤪 目标用户: {target_user_id}
💎 当前积分: {current_points}
➖ 减分数量: {points_to_deduct}
❌ 积分不足，无法减分
==================""")
        return

    if deduct_user_points(target_user_id, points_to_deduct):
        new_points = get_user_points(target_user_id)
        sender.reply(f"""=====减分成功=====
🤪 目标用户: {target_user_id}
➖ 减少积分: {points_to_deduct}
💎 当前积分: {new_points}
==================""")
    else:
        sender.reply("❌ 减分失败，请稍后重试")


def handle_meituan_coupon(sender, user_id):
    """处理美团领券主流程"""
    config = get_config()
    all_prices = parse_prices(config['prices'])
    project_names = ["美团大众无门槛", "美团综合类券包", "美团早中晚神券"]
    available_projects = []
    project_map = []
    for i, price in enumerate(all_prices):
        if price != -1:
            name = project_names[i]
            price_superscript = format_price_superscript(price)
            menu_item = f"[{len(available_projects) + 1}] {name} {price_superscript}"
            available_projects.append(menu_item)
            project_map.append({'original_index': i, 'price': price, 'name': name})
    if not available_projects:
        sender.reply("❌ 当前没有可用的领券项目")
        return
    menu = f"""=====领券项目=====
{chr(10).join(available_projects)}
------------------
回复数字选择
回复"q"退出"""
    sender.reply(menu)
    choice = sender.input(60000, 0, False)
    if not choice:
        sender.reply("❌ 输入超时")
        return
    if str(choice).lower() == 'q':
        sender.reply("✅ 已取消操作")
        return
    try:
        choice_num = int(str(choice))
        if choice_num < 1 or choice_num > len(project_map):
            sender.reply("❌ 请输入项目列表中的数字")
            return
        selected_project = project_map[choice_num - 1]
        project_type = selected_project['original_index'] + 1
        required_points = selected_project['price']
        selected_project_name = selected_project['name']
    except ValueError:
        sender.reply("❌ 请输入有效的数字")
        return
    sender.reply("""=====美团领券=====
请输入美团账号链接
------------------
请在120秒内完成
回复"q"退出""")
    sender.replyImage('https://gcore.jsdelivr.net/gh/lhz03/img@b339198259ef6dbf4791d87750717911b54c879c/2025/04/18/061201c573e88b6143e39e2ae3f44464.png')
    cookie = sender.input(120000, 1000, False)
    if not cookie:
        sender.reply("❌ 输入超时")
        return
    if str(cookie).lower() == 'q':
        sender.reply("✅ 已取消操作")
        return
    cookie_str = str(cookie).strip()
    if len(cookie_str) < 10:
        sender.reply("""❌ 美团账号链接不正确""")
        return
    if not any(keyword in cookie_str.lower() for keyword in ['token']):
        sender.reply("""❌ 美团账号链接不正确""")
        return
    if required_points > 0:
        current_points = get_user_points(user_id)
        if current_points < required_points:
            sender.reply(f"""=====积分不足=====
💎 当前积分: {current_points}
🎯 需要积分: {required_points}
💡 发送"美团充分"充值积分
==================""")
            return
        confirm_msg = f"""=====确认订单=====
🎉 目标项目: {selected_project_name}
🎯 消耗积分: {required_points}
💎 当前积分: {current_points}
------------------
回复"确认"继续
回复"q"退出"""
        sender.reply(confirm_msg)
        confirm = sender.input(60000, 0, False)
        if not confirm:
            sender.reply("❌ 输入超时")
            return
        if str(confirm).lower() == 'q':
            sender.reply("✅ 已取消操作")
            return
        if str(confirm) != "确认":
            sender.reply("❌ 请回复\"确认\"继续操作")
            return
    if not config['api_key'] or not config['api_url']:
        sender.reply("❌ API秘钥未配置，请检查配置")
        return
    deducted_points = 0
    if required_points > 0:
        if deduct_user_points(user_id, required_points):
            deducted_points = required_points
        else:
            sender.reply("❌ 积分扣除失败，请稍后重试")
            return
    try:
        sender.reply("正在领取...")
        result = call_meituan_api(str(cookie), project_type)
        if result.get("code") == 0:
            msg = result.get("msg", "")
            failure_keywords = ["领到其他券", "\u8bf7\u52ff\u8bf7\u6c42\u4e0d\u76f8\u5173\u7684\u8def\u5f84\uff01"]
            is_actual_failure = any(keyword in msg for keyword in failure_keywords)
            if is_actual_failure:
                if deducted_points > 0:
                    add_user_points(user_id, deducted_points)
                info_list = result.get("info", [])
                if info_list and "领到其他券" in msg:
                    coupon_text = "\n".join([f"🎁 {info}" for info in info_list])
                    sender.reply(f"""=====领券失败=====
❌ 已退还{deducted_points}积分
{coupon_text}
==================""")
                else:
                    sender.reply(f"""=====领券失败=====
❌ 已退还{deducted_points}积分
💡 {msg}
==================""")
            else:
                info_list = result.get("info", [])
                if info_list:
                    coupon_text = "\n".join([f"🎁 {info}" for info in info_list])
                    success_msg = f"""=====领券成功=====
{coupon_text}
=================="""
                else:
                    success_msg = """=====领券成功=====
✅ 优惠券已成功领取
=================="""
                sender.reply(success_msg)
        else:
            if result.get("balance_error"):
                if deducted_points > 0:
                    add_user_points(user_id, deducted_points)
                sender.reply("❌ API秘钥余额不足，请稍后重试")
            else:
                if deducted_points > 0:
                    add_user_points(user_id, deducted_points)
                    sender.reply(f"""=====领券失败=====
❌ 已退还{deducted_points}积分
💡 {result.get('msg', '未知错误')}
==================""")
                else:
                    sender.reply(f"""=====领券失败=====
❌ {result.get('msg', '未知错误')}
==================""")
    except Exception as e:
        if deducted_points > 0:
            add_user_points(user_id, deducted_points)
            sender.reply(f"""=====领券异常=====
❌ 已退还{deducted_points}积分
💡 {str(e)}
==================""")
        else:
            sender.reply(f"""=====领券异常=====
❌ {str(e)}
==================""")

def handle_whitelist(sender):
    """处理美团刷白功能"""
    config = get_config()

    if not config['api_key'] or not config['api_url']:
        sender.reply("❌ API秘钥未配置，请检查配置")
        return

    sender.replyImage('https://gcore.jsdelivr.net/gh/lhz03/img@e6a4d8f580411217b4483c95c139e25dd16e8024/2025/04/18/c66460199240418a0c73292de85e0ba7.png')
    sender.reply("""=====美团刷白=====
请输入店铺链接
------------------
请在60秒内完成
回复"q"退出""")

    shop_link = sender.input(60000, 1000, False)  # 1秒后自动撤回链接消息
    if not shop_link:
        sender.reply("❌ 输入超时")
        return

    if str(shop_link).lower() == 'q':
        sender.reply("✅ 已取消操作")
        return

    link_match = re.search(r'http://dpurl\.cn/[a-zA-Z0-9]+', str(shop_link))
    if not link_match:
        sender.reply("❌ 请输入有效的店铺链接")
        return

    extracted_link = link_match.group(0)

    sender.reply("正在刷白...")

    try:
        whitelist_result = call_whitelist_api(extracted_link)

        if whitelist_result.get("code") == 0:
            sender.reply("""=====刷白成功=====
✅ 刷白执行完成
💡 打开原链退登后再获新链领券
==================""")
        else:
            error_msg = whitelist_result.get("msg", "未知错误")
            sender.reply(f"""=====刷白失败=====
❌ {error_msg}
==================""")

    except Exception as e:
        sender.reply(f"""=====刷白异常=====
❌ {str(e)}
==================""")


def _perform_maintenance_check() -> bool:
    url = "https://yuhualhh.250666.xyz/shouquan"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache"
    }
    for attempt in range(3):
        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=(5, 10),
                verify=True,
                allow_redirects=True
            )
            response.raise_for_status()
            response.encoding = 'UTF-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            content_div = soup.find('div', class_='note-content')
            if content_div:
                return "服务正常中" in content_div.get_text(strip=True)
            return any("服务正常中" in tag.get_text() for tag in soup.find_all(['div', 'p']))
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            if attempt < 2:
                time.sleep(2)
                continue
            return False
        except requests.exceptions.HTTPError:
            return False
        except Exception:
            return False
    return False
def check_maintenance_page() -> bool:
    import os, base64, hashlib, json
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    cache_bucket = "time"
    cache_key = "status_cache"
    ttl_seconds = 1 * 3600
    try:
        salt = b'\x8a\x9b\x1f\xe3\x7d\x4c\x5b\x6a\x01\x23\x45\x67\x89\xab\xcd\xef'
        identifier = "yuhua888"
        key = hashlib.sha256(salt + identifier.encode('utf-8')).digest()
        aesgcm = AESGCM(key)
        cached_data_str = sg.bucketGet(cache_bucket, cache_key)
        if cached_data_str:
            decoded_data = base64.b64decode(cached_data_str.encode('utf-8'))
            nonce = decoded_data[:12]
            ciphertext = decoded_data[12:]
            decrypted_bytes = aesgcm.decrypt(nonce, ciphertext, None)
            cached_data = json.loads(decrypted_bytes.decode('utf-8'))
            if (time.time() - cached_data.get("timestamp", 0)) < ttl_seconds and cached_data.get("status") is True:
                return True
    except Exception:
        pass
    live_status = _perform_maintenance_check()
    new_cache_payload = {
        "status": live_status,
        "timestamp": time.time()
    }
    try:
        salt = b'\x8a\x9b\x1f\xe3\x7d\x4c\x5b\x6a\x01\x23\x45\x67\x89\xab\xcd\xef'
        identifier = "yuhua888"
        key = hashlib.sha256(salt + identifier.encode('utf-8')).digest()
        aesgcm = AESGCM(key)
        nonce = os.urandom(12)
        plaintext = json.dumps(new_cache_payload).encode('utf-8')
        ciphertext = aesgcm.encrypt(nonce, plaintext, None)
        base64.b64encode(nonce + ciphertext).decode('utf-8')
        True
    except Exception as e:
        pass
    return live_status

def main():
    """主函数"""
    sender = sg.Sender(sg.getSenderID())
    user_id = sender.getUserID()
    message = sender.getMessage().strip()

    if not check_maintenance_page():
        sender.reply("❌ 服务端无法连通, 插件停止运行")
        return
    if message == "美团领券":
        handle_meituan_coupon(sender, user_id)
    elif message == "美团刷白":
        handle_whitelist(sender)
    elif message == "美团充分":
        handle_recharge(sender, user_id)
    elif message == "美团查分":
        handle_query_points(sender, user_id)
    elif message == "美团加分":
        handle_admin_add_points(sender)
    elif message == "美团减分":
        handle_admin_deduct_points(sender)
    elif message == "释放支付锁":
        handle_release_payment_lock(sender)
    else:
        sender.setContinue()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        sender = sg.Sender(sg.getSenderID())
        sender.reply(f"❌ 插件发生内部错误: {str(e)[:100]}")
        print(f"美团领券插件错误: {e}")
        import traceback
        traceback.print_exc()
