# [title: 【插件】-星妈]
# [name: chaJianXingMa]
# [language: python]
# [class: 任务]
# [author: huawei]
# [version: v1.2.0]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(星妈|xing ma)(登录|登陆)$|^登(录|陆)(星妈|xingma)$|^(星妈|xingma)(查询|管理)$|^(查询|管理)(星妈|xingma)$|^清理星妈$|^星妈一键运行$|^星妈$|^星妈清理$]
# [cron: 18 8,12,16 * * *]
# [icon: https://i.mji.rip/2025/07/11/2350538ac014afbea48b64409bd5931c.png]
# [description: 📱 <b>功能特色：</b>；• 多账号批量管理，支持无限绑定；• 自动签到 + 自动完成每日任务；• 智能token刷新，无需手动维护；💡 <b>核心指令：</b>；🔐 星妈登录 - 快速绑定账号；🚀 星妈一键运行 - 批量执行任务；🔄 版本1.0.0 稳定版，持续更新优化中]
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

from datetime import datetime
import time
import hashlib
import json
import re
import random
import requests

loginMessage = """
=====星妈优选登录=====
请输入您的access_token
支持批量登录，多个token用换行分隔
------------------
回复「q」退出绑定
=================="""


senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()

appid = "xmyx"
appKey = (
    sg.bucketGet(bucket="G_xmyx_config", key="appKey")
    or "TwUQ01lKS1Km5zlV2f7amsZc5EQYkTbv"
)


"""隐藏手机号的辅助函数"""


def mask_phone(phone):
    """将手机号进行脱敏处理"""
    if not phone or len(phone) < 7:
        return phone
    return f"{phone[:3]}****{phone[-4:]}"


def safe_int(value, default=0):
    """安全转换为整数"""
    try:
        return int(value) if value and str(value).strip().isdigit() else default
    except (ValueError, TypeError) as e:
        print(f"[WARN] safe_int转换失败: {value}, error: {str(e)}")
        return default


"""获取插件客户基础配置"""


def get_config():
    """动态获取插件配置（添加每月积分费用参数）"""
    try:
        price_str = sg.bucketGet(bucket="G_xmyx_config", key="price") or "0.88"
        price = float(price_str) if price_str.replace(".", "", 1).isdigit() else 0.88

        zsm = sg.bucketGet(bucket="G_xmyx_config", key="zsm") or ""

        points_per_month_str = (
            sg.bucketGet(bucket="G_xmyx_config", key="points_per_month")
            or "100"
        )
        points_per_month = (
            int(points_per_month_str) if points_per_month_str.isdigit() else 100
        )

        return {
            "price": price,
            "zsm": zsm,
            "points_per_month": points_per_month,  # 每月所需的积分数量
        }
    except Exception as e:
        sender.reply(f"❌ 配置获取失败: {str(e)}")
        return {"price": 0.88, "zsm": "", "points_per_month": 100}


""" 获取用户列表 输出用户列表[] """


def get_user_accounts(user_id=None):
    """获取用户账号列表（可指定用户ID）"""

    target_userid = user_id if user_id else userid
    uservalue = sg.bucketGet("G_xmyx_user", target_userid) or "[]"
    user_accounts = []

    if uservalue:
        try:
            accounts_list = json.loads(uservalue)
            if isinstance(accounts_list, list):
                user_accounts = accounts_list
            else:
                user_accounts = [str(accounts_list)]
        except json.JSONDecodeError:
            print(
                f"[WARN] 账号数据JSON解析失败，数据: {uservalue[:50] if uservalue else 'None'}..."
            )
            user_accounts = []

    return [str(acc) for acc in user_accounts if acc]  # 确保过滤掉空值


"""星妈登录 - 支持批量登录"""


def login():
    sender.reply(loginMessage)
    user_input = sender.input(120000, 1, False).strip()

    if user_input.lower() == "q":
        return

    tokens = []
    lines = user_input.replace("\r\n", "\n").split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue
        for sep in [",", ";", "|"]:
            if sep in line:
                tokens.extend([t.strip() for t in line.split(sep) if t.strip()])
                break
        else:
            if line:
                tokens.append(line)

    tokens = list(dict.fromkeys(tokens))

    if not tokens:
        sender.reply("❌ 未检测到有效的token，请重新输入")
        return

    success_count = 0
    fail_count = 0
    results = []

    sender.reply(f"🔄 正在验证 {len(tokens)} 个token，请稍候...")

    for i, access_token in enumerate(tokens, 1):
        try:
            client = XingMaYouXuanAuto(access_token)
            userInfo = client.get_user_info()

            if userInfo:
                user = userInfo.get("baseInfo") or {}
                mobile = (
                    user.get("mobile") or user.get("fullName") or user.get("openId")
                )

                if mobile:
                    save_account_info_silent(mobile, access_token)
                    success_count += 1
                    results.append(f"✅ [{i}] {mask_phone(mobile)} 登录成功")
                else:
                    fail_count += 1
                    results.append(f"❌ [{i}] 无法获取手机号")
            else:
                fail_count += 1
                token_hint = (
                    f"{access_token[:6]}..." if len(access_token) > 6 else access_token
                )
                results.append(f"❌ [{i}] {token_hint} token无效或过期")

            if i < len(tokens):
                time.sleep(0.5)

        except Exception as e:
            fail_count += 1
            token_hint = (
                f"{access_token[:6]}..." if len(access_token) > 6 else access_token
            )
            results.append(f"❌ [{i}] {token_hint} 验证失败: {str(e)[:20]}")

    result_msg = (
        f"""
=====批量登录结果=====
📊 总计: {len(tokens)} 个token
✅ 成功: {success_count} 个
❌ 失败: {fail_count} 个
------------------
"""
        + "\n".join(results)
        + """
------------------
发送"星妈管理"管理账号
发送"星妈查询"查询账号
=================="""
    )

    sender.reply(result_msg)


def save_account_info_silent(phone, token):
    """静默保存账号信息（不发送回复消息）"""
    accounts = get_user_accounts()

    if phone not in accounts:
        accounts.append(phone)
        sg.bucketSet("G_xmyx_user", userid, json.dumps(accounts))

    sg.bucketSet("G_xmyx_token", phone, token)


"""登录成功存储到数据桶"""


def save_account_info(phone, token):
    """保存账号信息"""
    accounts = get_user_accounts()  # 已经是列表，不需要eval

    if phone not in accounts:
        accounts.append(phone)
        sg.bucketSet("G_xmyx_user", userid, json.dumps(accounts))

    sg.bucketSet(f"G_xmyx_token", phone, token)
    success_msg = f"""
=====登录成功=====
📱 账号: {mask_phone(phone)}
✅ 状态: 添加成功
------------------
发送"星妈管理"管理账号
发送"星妈查询"查询账号"""
    sender.reply(success_msg)


"""星妈查询"""


def query_accounts():
    today = str(datetime.now().date())
    accounts = get_user_accounts()
    account_info_list = []

    for account in accounts:
        account_info = query_accounts_for_item(account, today)
        if account_info:
            account_info_list.append(account_info)

    final_msg = "=====账号信息汇总=====" + "\n".join(account_info_list) + "\n"
    sender.reply(final_msg)


"""星妈查询单个"""


def query_accounts_for_item(account, today):
    """获取单个账号信息"""
    token = sg.bucketGet(f"G_xmyx_token", account)
    if not token:
        return None

    client = XingMaYouXuanAuto(token)
    try:
        client.refresh_token()
    except Exception as e:
        print(f"[WARN] 查询前刷新token失败: {str(e)}")

    userInfo = client.get_user_info()
    user = {"scoreBalance": 0}
    if userInfo:
        user = userInfo.get("memberPoints")
        if not user:
            return None
        auth_data_str = '2099-12-31'
        if not auth_data_str:
            auth_status = "授权: ❌ 未授权"
        else:
            try:
                auth_data = json.loads(auth_data_str)
                expire_date = auth_data.get("expire_time")
                auth_status = (
                    f"到期时间: {expire_date}"
                    if expire_date and expire_date > today
                    else "授权: ❌ 未授权"
                )
            except Exception as e:
                print(f"[WARN] 查询单账号授权信息解析失败: {str(e)}")
                auth_status = "授权: ❌ 数据异常"
    else:
        auth_status = "❌ 登录态异常，请重新抓取"
        user["scoreBalance"] = 0

    return f"""
📱 账号: {mask_phone(account)}
💰 积分: {user.get("scoreBalance", "N/A")}
🔐 {auth_status}
=================="""


"""查询用户积分"""


def query_user_points(userid=None):
    """查询用户积分 - 根据图片数据结构适配"""
    if not userid:
        userid = sender.getUserID()

    points = sg.bucketGet("dd_sign_coin", userid) or "0"

    if points == "0":
        sign_key = f"sign_{userid}"
        sign_points = sg.bucketGet("dd_sign_coin", sign_key)
        if sign_points:
            points = sign_points

    config = get_config()

    sender.reply(
        f"📊 您的当前积分: {points}\n"
        f"💰 每账号每月积分: {config['points_per_month']}\n"
        f"👉 检查配置可充值积分"
    )


"""获取用户积分？"""


def get_user_points(userid=None):
    return 0


"""改用户积分"""


def set_user_points(userid, points):
    """设置用户积分 - 适配呆呆积分数据结构"""
    sg.bucketSet("dd_sign_coin", userid, str(points["dd_sign_coin"]))
    sg.bucketSet("dd_sign_points", userid, str(points["dd_sign_points"]))

    sign_key = f"sign_{userid}"
    sg.bucketSet("dd_sign_coin", sign_key, str(points["dd_sign_coin"]))
    return True


"""星妈管理"""


def manage():
    while True:
        accounts = get_user_accounts()  # 使用统一函数获取账号列表
        if not accounts:
            sender.reply("❌ 您尚未绑定任何账号，请先绑定")
            return

        authorized_count = 0
        unauthorized_accounts = []
        for account_id in accounts:
            auth_data_str = '2099-12-31'
            is_authorized = False
            if auth_data_str:
                try:
                    auth_data = json.loads(auth_data_str)
                    expire_date = auth_data.get("expire_time", "")
                    if expire_date and expire_date >= str(datetime.now().date()):
                        is_authorized = True
                except Exception as e:
                    print(f"[WARN] 管理页统计授权状态解析失败: {str(e)}")

            if is_authorized:
                authorized_count += 1
            else:
                unauthorized_accounts.append(account_id)

        account_list = []
        for i, account_id in enumerate(accounts, 1):
            auth_data_str = '2099-12-31'
            status = "❌"
            status_text = "未授权"
            if auth_data_str:
                try:
                    auth_data = json.loads(auth_data_str)
                    expire_date = auth_data.get("expire_time", "")
                    if expire_date and expire_date >= str(datetime.now().date()):
                        status = "✅"
                        status_text = f"已授权(到期:{expire_date})"
                    else:
                        status_text = f"已过期({expire_date})"
                except Exception as e:
                    print(f"[WARN] 管理页授权状态解析失败: {str(e)}")
                    status_text = "数据异常"

            account_list.append(
                f"[{i}] 📱 {mask_phone(account_id)} {status}{status_text}"
            )

        if accounts:
            account_list.append("\n[0] 所有账号授权（支付）")
        if unauthorized_accounts:
            account_list.append("[9999] 没有授权的账号授权（支付）")

        account_list_str = "\n".join(account_list)

        user_points = get_user_points()

        print(f"===={user_points}")

        sender.reply(f"""
=====星妈账号管理=====
🔢 绑定账号: {len(accounts)}个
✅ 已授权: {authorized_count}个
❌ 未授权: {len(accounts) - authorized_count}个
📊 当前积分: {user_points["total"]}
-------------------------
{account_list_str}
------------------
回复序号选择操作（q退出）
===================""")

        choice = sender.input(60000, 1, False)
        if choice.lower() == "q":
            sender.reply("已退出管理")
            return

        if choice == "0":
            sender.reply("您选择了所有账号授权")
            batch_authorize_accounts(accounts, "所有账号")
            return
        elif choice == "9999":
            sender.reply("您选择了没有授权的账号授权")
            for account_id in unauthorized_accounts:
                authorize_account(account_id)
            return
        elif not choice.isdigit():
            sender.reply("❌ 输入无效，请重新选择")
            continue

        selected_idx = int(choice) - 1
        if selected_idx < 0 or selected_idx >= len(accounts):
            sender.reply("❌ 序号无效，请重新选择")
            continue

        selected_account = accounts[selected_idx]
        sender.reply(
            f"你选择了账号: {mask_phone(selected_account)}\n[1] 授权账号\n[2] 删除账号"
        )
        op = sender.input(60000, 1, False)

        if op == "1":
            authorize_account(selected_account)
            return
        elif op == "2":
            delete_account(selected_account)
            return
        else:
            sender.reply("❌ 无效操作，请重新选择")
            continue


"""授权账号"""


def format_target_label(target_label):
    """格式化支付展示目标，手机号脱敏，其它批量标签原样显示"""
    target_text = str(target_label or "").strip()
    if not target_text:
        return "账号"
    return mask_phone(target_text) if target_text.isdigit() else target_text


def handle_authorize_payment(target_label, months, account_count=1):
    return True


def authorize_account(account_id):
    return True


def batch_authorize_accounts(account_ids, title):
    return True


"""微信付款"""


def wechat_payment_flow(account_id, months, amount, config, phone):
    return True


"""积分付款"""


def point_payment_flow(account_id, months, required_points, config):
    return True


"""付款结算"""


def parse_payment_result(raw_data):
    return True


"""完成授权"""


def complete_authorization(account_id, months, masked_phone):
    return True


"""删除账号"""


def delete_account(account_id):
    """删除账号"""
    accounts = get_user_accounts()  # 使用统一函数获取账号列表

    sender.reply(f"""
=====删除账号确认=====
确认删除账号 {mask_phone(account_id)} 吗？
请回复 [Y] 确认
回复 [N] 取消
==================""")
    user_confirm = sender.input(120000, 1, False).strip().lower()

    if user_confirm != "y":
        sender.reply("✅ 已取消删除操作")
        return

    try:
        sg.bucketDel(bucket="G_xmyx_token", key=account_id)
        True

        if account_id in accounts:
            accounts.remove(account_id)
            if accounts:
                sg.bucketSet(
                    bucket="G_xmyx_user", key=userid, value=json.dumps(accounts)
                )
            else:
                sg.bucketDel(bucket="G_xmyx_user", key=userid)

        sender.reply("✅ 账号删除成功")

    except Exception as e:
        sender.reply(f"❌ 删除失败: {str(e)}")


"""免费授权"""


def free_authorize_account(account_id, months, user_id, masked_phone):
    return True


def admin_authorize_account():
    return True
def xm_auto_run():
    authorized_accounts = []
    auth_keys = [] or []
    print(f"-----{auth_keys}----")
    for account_id in auth_keys:
        auth_data_str = '2099-12-31'
        if not auth_data_str:
            continue

        try:
            auth_data = json.loads(auth_data_str)
            expire_date = auth_data.get("expire_time")

            if expire_date:
                try:
                    expire_date = datetime.strptime(expire_date, "%Y-%m-%d").date()
                    if datetime.now().date() <= expire_date:
                        authorized_accounts.append(account_id)
                except Exception as e:
                    print(f"[WARN] 授权日期格式无效，跳过账号 {account_id}: {str(e)}")
        except Exception as e:
            print(f"[WARN] 授权信息格式错误，跳过账号 {account_id}: {str(e)}")

    if not authorized_accounts:
        sender.reply("❌ 没有已授权的账号")
        return

    run_results = []
    skip_results = []  # 用于记录跳过的账号
    total_earned = 0

    """到了这里才是开始执行"""
    for account_id in authorized_accounts:
        access_token = sg.bucketGet("G_xmyx_token", account_id)

        if not access_token:
            skip_results.append(account_id)
            continue

        client = XingMaYouXuanAuto(access_token)
        formatted_phone = mask_phone(account_id)

        userInfo_before = client.get_user_info() or {}
        member_points_before = userInfo_before.get("memberPoints", {})
        score_before = (
            member_points_before.get("scoreBalance", 0) if member_points_before else 0
        )

        print(f"=====当前手机号：{mask_phone(account_id)}=====")
        sign_success = client.signin()
        sign_result = "✅" if sign_success else "❌"

        taskList = client.get_task_list() or []
        task_count = len(taskList)
        if task_count > 0:
            run_task(taskList, client, account_id)
            task_result = f"✅完成{task_count}任务"
        else:
            task_result = "⏩无任务"

        try:
            client.refresh_token()
            time.sleep(1)
        except Exception as e:
            print(f"刷新token失败，但不影响任务执行: {str(e)}")

        userInfo_after = client.get_user_info() or {}
        member_points_after = userInfo_after.get("memberPoints", {})
        score_after = (
            member_points_after.get("scoreBalance", 0) if member_points_after else 0
        )
        earned_this_run = max(0, score_after - score_before)
        total_earned += earned_this_run

        run_results.append(f"📱 {formatted_phone}: {sign_result}签到 | {task_result}")

    success_count = len(run_results)
    skip_count = len(skip_results)

    result_msg = f"""🚀 星妈任务汇总 📊
====================
✅ 成功账号: {success_count}个
❌ 失败账号: {skip_count}个
💰 积分收益: {total_earned}
===================="""

    sender.reply(result_msg)


def run_task(taskList, client, account_id):
    """执行任务列表中的所有任务"""
    if not taskList or not isinstance(taskList, list):
        print("没有可执行的任务或任务列表格式错误")
        return

    for task in taskList:
        try:
            if not task.get("taskName") or not task.get("taskType"):
                print(f"任务数据不完整: {task}")
                continue

            if re.search(r"使用任意商品", task.get("taskName", "")):
                print(f"跳过任务: {task.get('taskName')}")  # 可选：打印日志
                continue  # 跳过当前任务，继续下一个

            client.tofinish(task["taskName"], task["taskType"])

            wait_time = random.randint(2, 5)
            print(f"等待 {wait_time} 秒后完成任务...")
            time.sleep(wait_time)

            client.complete_task(task["taskName"], task["taskType"])

            time.sleep(1)

            task_interval = random.randint(3, 6)
            print(f"任务间隔 {task_interval} 秒...")
            time.sleep(task_interval)

        except Exception as e:
            print(f"执行任务失败: {str(e)}, 任务: {task.get('taskName', '未知任务')}")
            continue


class XingMaYouXuanAuto:
    def __init__(self, assess_token):
        self.token = assess_token
        self.uservalue = get_user_accounts()

        self.headers = {
            "Host": "www.feihevip.com",
            "token": assess_token,
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.48(0x1800302b) NetType/4G Language/zh_CN",
            "Referer": "https://servicewechat.com/wx4205ec55b793245e/215/page-frame.html",
            "fhAppid": appid,
            "source": "1",
        }

    """"获取签名配置"""

    def get_signature(self):
        fh_nonce_str = self.getFhNonceStr({"length": 16})
        fh_timestamp = self.get_timestamp()
        data = "{}"
        sign_string = f"fhAppid{appid}fhNonceStr{fh_nonce_str}fhTimestamp{fh_timestamp}{data}{appKey}"
        return {
            "fhNonceStr": fh_nonce_str,
            "fhTimestamp": str(fh_timestamp),
            "fhSign": hashlib.md5(sign_string.encode("utf-8")).hexdigest().upper(),
        }

    """获取刷新token的签名配置"""

    def get_signature2(self):
        fh_nonce_str = self.getFhNonceStr({"length": 16})
        fh_timestamp = self.get_timestamp()
        sign_string = f"fhAppidxmhfhNonceStr{fh_nonce_str}fhTimestamp{fh_timestamp}98d9fe9b613a479dbcb111ca261e3ce1"
        return {
            "fhNonceStr": fh_nonce_str,
            "fhTimestamp": str(fh_timestamp),
            "fhSign": hashlib.md5(sign_string.encode("utf-8")).hexdigest().upper(),
        }

    def get_timestamp(self):
        return int(str(int(time.time() * 1000))[:10])

    def getFhNonceStr(self, t=None):
        t = t or {}
        config = {
            "length": t.get("length"),
            "numeric": t["numeric"] if "numeric" in t else True,  # 默认 True
            "letters": t["letters"] if "letters" in t else True,  # 默认 True
            "special": t.get("special", False),  # 默认 False
            "exclude": t["exclude"]
            if "exclude" in t and isinstance(t["exclude"], list)
            else [],
        }

        length = config["length"]
        if length is None:
            return ""  # 如果未指定 length，返回空字符串（JS 原逻辑）

        char_pool = ""
        if config["numeric"]:
            char_pool += "0123456789"
        if config["letters"]:
            char_pool += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        if config["special"]:
            char_pool += "!$%^&*()_+|~-=`{}[]:;<>?,./"

        for excluded_char in config["exclude"]:
            char_pool = char_pool.replace(excluded_char, "")

        result = ""
        for _ in range(length):
            r = random.randint(0, len(char_pool) - 1)
            result += char_pool[r]

        return result

    def get_user_info(self):
        try:
            signature = self.get_signature()
            _headers = {**self.headers, **signature}

            res = requests.post(
                url="https://www.feihevip.com/api/starMember/getMemberInfo",
                headers=_headers,
                json={},
                timeout=(5, 30),
            )
            res = res.json()

            if res is not None and res.get("code") == "200" and res.get("data"):
                data = res.get("data", {})
                return data
            else:
                print(f"⛔️ 查询用户信息失败! {res.get('msg')}\n")
        except Exception as e:
            self.ck_status = False
            print(f"⛔️ 查询用户信息失败! {e}")

    def complete_task(self, task_name, task_type):
        try:
            max_retries = 3
            for attempt in range(1, max_retries + 1):
                try:
                    signature = self.get_signature()
                    res = requests.get(
                        url=f"https://www.feihevip.com/api/member/signin/completeTask?taskType={task_type}",
                        headers={**self.headers, **signature},
                        json={},
                        timeout=(5, 30),
                    )
                    res = res.json()
                    print(
                        f"[星妈]完成任务----{task_name}--- 尝试 {attempt}/{max_retries}"
                    )

                    if res.get("code") == "200":
                        if res.get("data"):
                            point = res["data"].get("awardSendPoints", 0)
                            print(f"✅ 完成任务: {task_name}, 获取积分: {point}分\n")
                        else:
                            print(f"✅ 任务: {task_name} 已完成，请勿重复执行\n")
                        return True
                    else:
                        print(
                            f"⚠️ 完成任务: {task_name} 失败! {res.get('msg')}，尝试 {attempt}/{max_retries}\n"
                        )
                        if attempt < max_retries:
                            time.sleep(2)
                            continue
                        return False
                except Exception as e:
                    print(f"⚠️ 完成任务请求异常: {str(e)}，尝试 {attempt}/{max_retries}")
                    if attempt < max_retries:
                        time.sleep(2)
                        continue
                    raise e
            return False
        except Exception as e:
            self.ck_status = False
            print(f"⛔️ 完成任务{task_name}失败! {e}")
            return False

    def get_task_list(self):
        try:
            max_retries = 3
            for attempt in range(1, max_retries + 1):
                try:
                    signature = self.get_signature()
                    res = requests.get(
                        url="https://www.feihevip.com/api/member/signin/getTaskList",
                        headers={**self.headers, **signature},
                        json={},
                        timeout=(5, 30),
                    )
                    res = res.json()

                    if res.get("code") == "200" and len(res.get("data", [])) > 0:
                        print(f"✅ 成功获取 {len(res['data'])} 个任务")
                        return res["data"]
                    else:
                        if attempt < max_retries:
                            time.sleep(2)
                            continue
                except Exception as e:
                    if attempt < max_retries:
                        time.sleep(2)
                        continue
                    raise e
            return []
        except Exception as e:
            self.ck_status = False
            print(f"⛔️ 获取任务失败! {e}")
            return []

    def signin(self):
        try:
            max_retries = 3
            for attempt in range(1, max_retries + 1):
                try:
                    signature = self.get_signature()
                    _header = {**self.headers, **signature}
                    res = requests.post(
                        url="https://www.feihevip.com/api/member/signin/sign",
                        headers=_header,
                        json={},
                        timeout=(5, 30),
                    )
                    print(f"[星妈]今日签到----{res}---")
                    res = res.json()

                    if res.get("code") == "200":
                        print(f"✅ 签到成功!\n")

                        try:
                            info_res = requests.get(
                                url="https://www.feihevip.com/api/member/signin/getSignInfo?signType=1",
                                headers=_header,
                                json={},
                                timeout=(5, 30),
                            )
                            info_data = info_res.json()
                            print(f"签到结果{info_data}")
                            sign_pop = info_data.get("data", {}).get("signPop")
                            point = sign_pop[0]["signPoint"] if sign_pop else 0
                            print(f"✅ 签到获得积分: {point}分\n")
                        except Exception as e:
                            print(f"⚠️ 获取签到积分信息失败: {str(e)}")

                        return True
                    else:
                        res.get("msg")
                        if attempt < max_retries:
                            time.sleep(2)
                            continue
                        return False
                except Exception as e:
                    if attempt < max_retries:
                        time.sleep(2)
                        continue
                    raise e
            return False
        except Exception as e:
            self.ck_status = False
            print(f"⛔️ 执行任务今日签到失败! {e}")
            return False

    def tofinish(self, task_name, task_type):
        try:
            max_retries = 2
            for attempt in range(1, max_retries + 1):
                try:
                    signature = self.get_signature()
                    res = requests.get(
                        url=f"https://www.feihevip.com/api/member/signin/tofinish?taskType={task_type}",
                        headers={**self.headers, **signature},
                        json={},
                        timeout=(5, 30),
                    )
                    res = res.json()


                    if res.get("code") == "200":
                        print(f"🚀 开始执行任务: {task_name}\n")
                        return True
                    else:
                        if attempt < max_retries:
                            time.sleep(2)
                            continue
                        return False
                except Exception as e:
                    if attempt < max_retries:
                        time.sleep(2)
                        continue
                    raise e
            return False
        except Exception as e:
            self.ck_status = False
            print(f"⛔️ 执行任务{task_name}失败! {e}")
            return False

    """刷新token"""

    def refresh_token(self):
        try:
            signature = self.get_signature2()
            options = {
                "url": "https://mom.feihe.com/program/token/refreshToken",
                "type": "get",
                "headers": {
                    "Host": "mom.feihe.com",
                    "token": self.token,
                    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.48(0x1800302b) NetType/4G Language/zh_CN",
                    "Referer": "https://servicewechat.com/wx4205ec55b793245e/215/page-frame.html",
                    "fhAppid": "xmh",
                    "source": "1",
                    **signature,
                },
            }

            response = requests.get(
                options["url"], headers=options["headers"], timeout=(5, 30)
            )
            result = response.json()
            new_token = result.get("data")

            if new_token:
                self.token = new_token
                self.headers["token"] = new_token
                print("🎉 刷新 token 成功")
                return new_token

            print("⚠️ 刷新 token 失败，返回数据中无token")
            return None
        except Exception as e:
            print(f"⛔️ 刷新 Token 失败: {e}")
            return None


"""主程序运行"""
try:
    usermessage = sender.getMessage()
except AttributeError:
    usermessage = ""

if re.search(r"星妈登录", usermessage):
    login()
elif re.search(r"星妈管理", usermessage):
    manage()
elif re.search(r"星妈查询", usermessage):
    query_accounts()
elif re.search(r"星妈一键运行", usermessage):
    xm_auto_run()
elif re.search(r"星妈教程", usermessage):
    sender.reply(
        "=====使用教程=====\n"
        "1. 「星妈登录」绑定账号\n"
        "2. 「星妈管理」进行账号授权\n"
        "3. 「星妈一键运行」执行所有账号任务\n"
        "4. 「星妈查询」查看账号状态\n"
        "===================="
    )
elif re.search(r"我的星妈积分$", usermessage):
    query_user_points()
elif re.search(r"星妈授权$", usermessage) and sender.isAdmin():
    admin_authorize_account()
else:
    sender.setContinue()
