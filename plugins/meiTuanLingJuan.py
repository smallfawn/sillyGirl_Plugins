# [title: 美团领卷]
# [name: meiTuanLingJuan]
# [language: python]
# [class: 任务]
# [author: sky2022]
# [version: v1.4.4]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(美团领劵|美团领卷|美团领券|美团领卷余额查询)$]
# [icon: https://q6.itc.cn/images01/20240412/04c3902c5fba4ade86ca6082d064f855.jpeg]
# [description: 普通券种包含【20-6、25-9、33-10、37-11、60-30、28-13、38-18]
# [depe: ["requests"]]


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
    'bd_mtconfig_token': form.string().title('Token').default('').description('计费的token值，请找插件作者获取！'),
})
_CONFIG_FIELD_MAP = {
    ('bd_mtconfig', 'token'): 'bd_mtconfig_token',
}

import requests
import re
import json
from decimal import Decimal, InvalidOperation
import time
from urllib.parse import parse_qs, parse_qsl, unquote, urlencode, urlsplit, urlunsplit

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()  # Changed from userID to userid for consistency
usermessage = sender.getMessage()
zsm = sg.bucketGet('bd_mtconfig', 'zsm') or ''
try:
    money_str = sg.bucketGet('bd_mtconfig', 'money') or '0.2'
    money = Decimal(money_str.strip())
except (InvalidOperation, TypeError):
    money = Decimal('0.2')
token = sg.bucketGet('bd_mtconfig', 'token') or ''
is_free = sg.bucketGet('bd_mtconfig', 'is_free') == 'true'
use_ma_pay = '2099-12-31' == 'true'

use_point_pay = '2099-12-31' == 'true'
try:
    point_price = int(sg.bucketGet('bd_mtconfig', 'point_price') or '0')
except (ValueError, TypeError):
    point_price = 0

try:
    lock_timeout = int(sg.bucketGet('bd_mtconfig', 'lock_timeout') or '30')
except (ValueError, TypeError):
    lock_timeout = 30

FLASK_API_BASE = "https://mt.linzixuan.top/api"
COUPON_API_URL = f"{FLASK_API_BASE}/coupons"
TOKEN_API_URL = f"{FLASK_API_BASE}/token"

DEFAULT_UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

URL_CANDIDATE_PATTERN = re.compile(r"https?://[A-Za-z0-9\-._~:/?#\[\]@!$&'()*+,;=%]+", re.IGNORECASE)
TOKEN_QUERY_PATTERN = re.compile(r"(?:[?&])token=([^&#\s]+)", re.IGNORECASE)
TOKEN_HEAD_PATTERN = re.compile(r"[A-Za-z0-9._\-+/=]+")


def sanitize_meituan_token(raw_token):
    """清洗token，去除末尾脏字符，兼容URL编码"""
    if not raw_token:
        return ''

    token_text = raw_token.strip()
    for _ in range(2):
        decoded = unquote(token_text)
        if decoded == token_text:
            break
        token_text = decoded

    token_text = token_text.replace(' ', '+')
    head_match = TOKEN_HEAD_PATTERN.match(token_text)
    if not head_match:
        return ''
    return head_match.group(0)


def extract_meituan_login_data(raw_input):
    """从用户输入中稳健提取 token 和美团链接"""
    if not raw_input:
        return '', ''

    text = raw_input.strip().replace('&amp;', '&')
    queue = [text]
    seen = set()

    while queue:
        candidate = queue.pop(0).strip()
        if not candidate or candidate in seen:
            continue
        seen.add(candidate)

        url_matches = URL_CANDIDATE_PATTERN.findall(candidate)
        if candidate.lower().startswith('http') and candidate not in url_matches:
            url_matches.insert(0, candidate)

        for url in url_matches:
            cleaned_url = url.replace('&amp;', '&')

            token_match = TOKEN_QUERY_PATTERN.search(cleaned_url)
            if token_match:
                token_value = sanitize_meituan_token(token_match.group(1))
                if token_value:
                    return token_value, cleaned_url

            parsed = urlsplit(cleaned_url)
            if parsed.query:
                query_dict = parse_qs(parsed.query, keep_blank_values=True)
                token_list = query_dict.get('token') or query_dict.get('Token') or query_dict.get('TOKEN')
                if token_list:
                    token_value = sanitize_meituan_token(token_list[0])
                    if token_value:
                        return token_value, cleaned_url

                for key, values in query_dict.items():
                    key_lower = key.lower()
                    if 'url' in key_lower or 'redirect' in key_lower or 'target' in key_lower or 'jump' in key_lower:
                        for value in values:
                            value = value.strip()
                            if value:
                                queue.append(value)

        decoded_candidate = unquote(candidate)
        if decoded_candidate != candidate:
            queue.append(decoded_candidate)

    fallback_match = re.search(r"(?i)(?:^|[?&\s])token=([A-Za-z0-9._\-+/=%]+)", text)
    if fallback_match:
        token_value = sanitize_meituan_token(fallback_match.group(1))
        if token_value:
            return token_value, ''

    return '', ''


def normalize_meituan_link(link, token_value):
    """规范化链接，确保提交给后端的是干净 token"""
    if token_value and not link:
        return f"https://i.meituan.com/mttouch/page/account?{urlencode({'token': token_value})}"

    if not link:
        return ''

    cleaned_link = link.replace('&amp;', '&')
    parsed = urlsplit(cleaned_link)
    query_pairs = parse_qsl(parsed.query, keep_blank_values=True)

    new_pairs = []
    token_replaced = False
    for key, value in query_pairs:
        if key.lower() == 'token':
            new_pairs.append((key, token_value))
            token_replaced = True
        else:
            new_pairs.append((key, value))

    if token_value and not token_replaced:
        new_pairs.append(('token', token_value))

    normalized_query = urlencode(new_pairs, doseq=True)
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, normalized_query, parsed.fragment))

def check_token_balance():
    """检查token余额"""
    try:
        headers = {'Content-Type': 'application/json'}
        data = {'token': token}
        response = requests.post(f"{TOKEN_API_URL}/balance", headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                return result.get('data', {}).get('balance', 0)
        return 0
    except Exception as e:
        sender.reply(f"检查token余额失败，请检查接口是否正常！")
        return 0

def deduct_token(amount=0.15):
    """扣除token"""
    try:
        headers = {'Content-Type': 'application/json'}
        data = {
            'token': token,
            'amount': amount,
            'force_charge': not is_free  # 根据是否免费模式决定是否强制收费
        }

        response = requests.post(f"{TOKEN_API_URL}/deduct", headers=headers, json=data, timeout=10)

        if response.status_code == 200:
            result = response.json()
            return result.get('success', False)
        return False
    except Exception as e:
        sender.reply(f"扣除token失败")
        return False


def fetch_coupons_from_flask_api(mt_cookie):
    """通过Flask API领取券"""
    try:
        headers = {'Content-Type': 'application/json'}
        data = {
            'mt_cookie': mt_cookie,
            'token': token,
            'free_mode': is_free
        }
        response = requests.post(f"{COUPON_API_URL}/fetch", headers=headers, json=data, timeout=60)
        try:
            result = response.json()
            response_data = result.get('data', {})
            if response_data.get('compensation'):
                add_user_tickets(userid, 1, 'normal')
                sender.reply(response_data.get('compensation_message', '未领到目标券，已自动补偿'))
                sender.reply(f"💳 当前剩余次数: {get_user_tickets(userid, 'normal')}次")
            if result.get('success'):
                coupons = response_data.get('coupons', [])
                details = response_data.get('details', [])
                for detail in details:
                    if detail.get('success'):
                        sender.reply(f"✅ {detail.get('name')} 领取成功")
                    else:
                        sender.reply(f"❌ {detail.get('message')}")
                return coupons
            else:
                error_message = result.get('message', '未知错误')
                sender.reply(f"❌ {error_message}")
                return []
        except json.JSONDecodeError:
            sender.reply(f"❌ Flask API请求失败：HTTP {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        sender.reply(f"❌ 网络请求出错：{str(e)}")
        return []
    except Exception as e:
        sender.reply(f"❌ 处理过程出错：{str(e)}")
        return []


def get_user_tickets(user_id, ticket_type='normal'):
    """获取用户剩余次数"""
    bucket_key = f'mt_user_tickets_{ticket_type}'
    tickets = sg.bucketGet(bucket_key, str(user_id)) or '0'
    return int(tickets)

def add_user_tickets(user_id, count=1, ticket_type='normal'):
    """增加用户次数"""
    bucket_key = f'mt_user_tickets_{ticket_type}'
    current = get_user_tickets(user_id, ticket_type)
    sg.bucketSet(bucket_key, str(user_id), str(current + count))

def use_user_ticket(user_id, ticket_type='normal'):
    """使用一次次数，如果有次数则返回True，否则返回False"""
    bucket_key = f'mt_user_tickets_{ticket_type}'
    current = get_user_tickets(user_id, ticket_type)
    if current > 0:
        sg.bucketSet(bucket_key, str(user_id), str(current - 1))
        return True
    return False

def process_payment(custom_price=None):
    return True
def refund_token(amount):
    headers = {'Content-Type': 'application/json'}
    data = {'token': token, 'amount': float(amount)}
    try:
        response = requests.post(f"{TOKEN_API_URL}/refund", headers=headers, json=data, timeout=10)
        return response.status_code == 200 and response.json().get('success')
    except Exception as e:
        sender.reply("Token返还失败，请检查配置")
        return False

if __name__ == "__main__":
    if '美团加白' in usermessage:
        sender.replyImage("https://i.mji.rip/2025/07/20/13f99df7dea6158d4feed5a699861c57.png")
        sender.reply("请发送您需要加白的账号店铺链接")

        shop_link = sender.input(120000, 1, False)

        if shop_link == "error":
            sender.reply("输入超时，退出任务")
            exit()

        try:
            headers = {'Content-Type': 'application/json'}
            data = {'shop_link': shop_link}

            response = requests.post(f"{COUPON_API_URL}/white", headers=headers, json=data, timeout=30)

            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    sender.reply("✅ 刷白成功！")
                else:
                    sender.reply(f"❌ {result.get('message')}")
            else:
                sender.reply(f"❌ Flask API请求失败：HTTP {response.status_code}")

        except requests.exceptions.RequestException as e:
            sender.reply(f"网络请求出错：{str(e)}")
        except Exception as e:
            sender.reply(f"处理过程出错：{str(e)}")

    elif '领卷余额查询' in usermessage:
        if not token:
            sender.reply("❌ 未配置Token值，请检查配置")
            exit(0)

        balance = check_token_balance()
        if balance >= 0:
            sender.reply(f"""=====Token余额=====
💰 当前余额: {balance}
==================""")
        else:
            sender.reply("❌ 查询余额失败，请检查配置")

    elif '美团' in usermessage:
        if not token:
            sender.reply("❌ 未配置Token值，请检查配置")
            exit(0)

        balance = check_token_balance()
        if balance < 0.2:
            sender.reply("❌ Token余额不足，请检查配置")
            exit(0)

        if not is_free:
            if not (zsm or use_ma_pay or (use_point_pay and point_price > 0)):
                sender.reply("❌ 未配置收款方式，请检查配置")
                exit(0)

            if money <= 0 and not (use_point_pay and point_price > 0):
                sender.reply("❌ 未配置领券价格，请检查配置")
                exit(0)

        sender.replyImage("https://img.cdn1.vip/i/6a032ef4e7f50_1778593524.webp")
        sender.reply("""=====美团领券=====
普通套券[28-18、38-15等]
------------------
请发送美团账号链接
==================""")
        mt = sender.input(120000, 1, False)

        if mt == "error":
            sender.reply("输入超时，退出任务")
            exit()

        meituan_token, extracted_link = extract_meituan_login_data(mt)
        if not meituan_token:
            sender.reply("❌ 未识别到有效token，请重新提交完整美团账号链接")
            exit()

        mt_clean = normalize_meituan_link(extracted_link, meituan_token)
        if not mt_clean:
            mt_clean = normalize_meituan_link('', meituan_token)

        if mt_clean != mt.strip():
            sender.reply("ℹ️ 已自动清洗链接参数，继续为您领取")

        sender.reply(f"""=====选择领取方式=====
1️⃣ 普通券种领取
   📦 包含普通套券[20-6、25-9、33-10、37-11、60-30、28-13、38-18]
   💰 价格: {money}元

------------------
回复数字选择方式
回复"q"退出操作
==================""")

        choice = sender.input(60000, 1, False)

        if choice == 'q' or choice == 'Q':
            sender.reply("✅ 已取消操作")
            exit()

        if choice == '1':
            proceed_with_coupon = False  # 标记是否继续领券流程
            need_compensation = False  # 标记是否需要补偿次数
            ticket_type = 'normal'  # 普通券种

            if not is_free and not sender.isAdmin():
                proceed_with_coupon, need_compensation = process_payment(money)
                used_ticket_payment = proceed_with_coupon and not need_compensation
            else:
                proceed_with_coupon = True  # 免费模式或管理员，直接标记可以继续领券
                used_ticket_payment = False
                need_compensation = False

            if proceed_with_coupon:
                try:
                    all_coupons = fetch_coupons_from_flask_api(mt_clean)

                    if all_coupons:

                        if len(all_coupons) == 1:
                            success_msg = f"""🎉 ========「领券成功」======== 🎉
✨ 恭喜您成功领取到以下优惠券：

{all_coupons[0]}

🎊 ========================== 🎊"""
                        else:
                            success_msg = f"""🎉 ========「领券汇总结果」======== 🎉
✨ 恭喜您成功领取到 {len(all_coupons)} 张优惠券：

"""
                            for i, coupon in enumerate(all_coupons, 1):
                                success_msg += f"{i:2d}. {coupon}\n"
                            success_msg += "\n🎊 ============================ 🎊"

                        sender.reply(success_msg)
                    else:
                        if (need_compensation and not is_free) or used_ticket_payment:
                            add_user_tickets(userid, 1, ticket_type)
                            sender.reply(f"""=====领券失败补偿=====
✅ 已补偿一次普通券种次数
💳 当前剩余次数: {get_user_tickets(userid, ticket_type)}次
==================""")

                except Exception as e:
                    sender.reply(f"处理过程出错：{str(e)}")
                    if (need_compensation and not is_free) or used_ticket_payment:
                        add_user_tickets(userid, 1, ticket_type)
                        sender.reply(f"""=====领券失败补偿=====
✅ 已补偿一次普通券种次数
💳 当前剩余次数: {get_user_tickets(userid, ticket_type)}次
==================""")

        else:
            sender.reply("❌ 输入无效，已取消操作")
