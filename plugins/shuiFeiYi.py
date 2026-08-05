# [title: 水费易]
# [name: shuiFeiYi]
# [language: python]
# [class: 任务]
# [author: mrconli]
# [version: v1.0.0]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^水费易(.*)|(.*)水费易$]
# [cron: 18 6 * * *]
# [icon: https://api.iconify.design/lucide:bot.svg]
# [description: 青龙环境变量格式为“会员ID”；1.0.0初版：支持批量登录]
# [depe: ["pycryptodome", "requests", "urllib3"]]


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
    'mrconli_shuifeiyi_ql_config': form.string().title('对接青龙').default('').description('|'),
    'mrconli_shuifeiyi_var_name': form.string().title('环境变量名').default('').description('青龙容器内的变量名，默认为：m_dnys'),
    'mrconli_shuifeiyi_is_proxy': form.boolean().title('是否启用代理').default(False).description('true/false'),
    'mrconli_shuifeiyi_proxy_pool': form.string().title('代理池地址').default('').description('代理API服务地址'),
})
_CONFIG_FIELD_MAP = {
    ('mrconli', 'shuifeiyi.ql_config'): 'mrconli_shuifeiyi_ql_config',
    ('mrconli', 'shuifeiyi.var_name'): 'mrconli_shuifeiyi_var_name',
    ('mrconli', 'shuifeiyi.is_proxy'): 'mrconli_shuifeiyi_is_proxy',
    ('mrconli', 'shuifeiyi.proxy_pool'): 'mrconli_shuifeiyi_proxy_pool',
}

from datetime import datetime, timedelta  # 操作日期、时间以及时间间隔
import urllib3
from decimal import Decimal  # 处理浮点数
import requests  # 处理http请求
import time  # 处理时间
import json  # 处理json数据
import aiohttp
from functools import lru_cache
import uuid


urllib3.disable_warnings()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

senderID = sg.getSenderID()  # 获取发送者QQ号
sender = sg.Sender(senderID)  # 获取发送者对象
userid = sender.getUserID()  # 存储当前发送者的用户 ID，与 senderID 类似，但通常用于内部标识
uservalue = sg.bucketGet(bucket='mrconli.shuifeiyi.user', key=userid)
today_date = datetime.now().date()
today_time = str(today_date)
number = int(sg.bucketGet('mrconli.shuifeiyi', 'number') or 5)

MAX_RETRIES = 10  # 最大重试次数
IS_PROXY = sg.bucketGet('mrconli.shuifeiyi', 'is_proxy')  # 是否启用代理True
PROXY_API = sg.bucketGet('mrconli.shuifeiyi', 'proxy_pool') or 'https://api.mrconli.com/getProxy'
if not PROXY_API:
    raise ValueError("代理池地址未配置，请在插件设置中配参")
proxy = None  # 初始化全局代理变量


def update_proxy():
    """更新代理IP地址"""
    global proxy
    try:
        if not IS_PROXY or IS_PROXY == 'false':
            proxy = None
            return
        response = requests.get(PROXY_API, timeout=10)
        ip = response.text.strip()
        if "请先添加白名单" in ip:
            raise ValueError("请配置代理白名单")
        proxy = {
            'http': ip,
            'https': ip,
        }
    except Exception as e:
        sender.reply(f"❌ 代理获取失败: {str(e)}")
        proxy = None


def _send_request(method, url, **kwargs):
    """带代理重试的请求方法"""
    global proxy
    attempts = 0
    while attempts < MAX_RETRIES:
        try:
            if IS_PROXY == 'true':
                proxy = proxy if 'proxy' in globals() else None
                if not proxy:
                    update_proxy()
            kwargs['timeout'] = kwargs.get('timeout', 15)  # 默认超时时间 15 秒
            response = requests.request(
                method=method,
                url=url,
                proxies=proxy if IS_PROXY and proxy else None,
                **kwargs
            )
            response.raise_for_status()
            return response
        except (requests.exceptions.ProxyError, requests.exceptions.Timeout) as e:
            print(f"⚠️ 代理异常: {str(e)}")
            if IS_PROXY:
                update_proxy()
                attempts += 1
                print(f"🔄 重试请求 ({attempts}/{MAX_RETRIES})")
                time.sleep(2)
        except requests.exceptions.RequestException as e:
            print(f"🚨 请求失败: {str(e)}")
            raise
    raise Exception(f"请求失败，超过最大重试次数: {MAX_RETRIES}")


def mask_phone(phone):
    """手机号脱敏处理"""
    if not phone or len(phone) != 11:
        return phone
    return f"{phone[:3]}****{phone[7:]}"


import os
import json
import requests
import asyncio
from json.decoder import JSONDecodeError

headers = {
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://wbapp.ai.ipaiyun.cn',
        'Referer': 'https://wbapp.ai.ipaiyun.cn/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090a1b) XWEB/9129 Flue',
        'ipaistf': 'oUFK7XqVy1U=',
        'ipaiuvck': 'null',
        'isapp': '1',
        'content-type': 'application/json;charset=UTF-8',
        'IpaiYunPaaS': str(uuid.uuid4())
    }

def get_info(member_id):
    """获取账号信息"""
    try:
        response = _send_request(
            'POST',
            'https://memberapi.ai.ipaiyun.cn/MemberApp/GetShopMember',
            headers=headers,
            json={'memberID': member_id, 'compId': 60001}
        )
        response.raise_for_status()
        try:
            data = response.json()
        except JSONDecodeError as e:
            print(f"解析会员信息失败: 状态码[{response.status_code}] 响应内容: {response.text[:200]}")
            return None, None, None, None
        isSign = data.get('resultJson', {}).get('isSign')    # 是否签到  0未签   1已签
        shop_model = data.get('resultJson', {}).get('shopmodel', {})
        nick_name = shop_model.get('nickName', '未知用户')   #  昵称
        mobilePhone = shop_model.get('mobilePhone', '')   # 手机号
        integral = shop_model.get('integral', 0)     # 积分
        return nick_name, mobilePhone, integral, isSign

    except Exception as e:
        print(f"获取会员信息失败: {e}")
        return None, None, None, None

def qd(member_id):
    """单个账号签到"""
    nick_name, phone, integral, isSign = get_info(member_id)
    if isSign == 1:
        sender.reply(f"⚠️ 账号[ {mask_phone(phone)} ]已签到，无需重复签到...")
        return
    else:
        response = _send_request(
            'POST',
            'https://memberapi.ai.ipaiyun.cn/MemberApp/MemberSign',
            headers=headers,
            json={'memberID': member_id, 'compId': 60001}
        )
        res = response.json()
        msg = res.get('message')
        sender.reply(f"✅ 账号[ {mask_phone(phone)} ]执行成功，结果：{msg}")
        return


def sms_login():
    sender.reply("短信登录暂不可用，请使用 ck登录")
    return None

def bind():
    """选择登录方式"""
    sender.reply(
        "=====水费易登录=====\n"
        "1. 短信验证码登录\n"
        "2. ck登录（可批量）\n"
        "=====================\n"
        "📝 请输入数字选择登录方式\n"
        "⭐ 输入q退出操作\n"
    )
    choice = sender.input(60000, 1, False)
    if choice == 'q' or choice == 'Q':
        sender.reply('❌ 已退出登录操作')
        return
    if not choice:
        sender.reply('❌ 输入超时！')
        return
    if choice == '1':
        sms_login()
    elif choice == '2':
        batch_login()


def batch_login():
    """批量登录函数"""
    global uservalue
    sender.reply(
        "=======水费易登录=======\n"
        "📝 请输入会员ID：\n"
        "说明: 支持批量，一行一号 \n"
        "=====================\n"
        "⭐ 输入q退出操作\n"
    )
    success_count = 0
    add_count = 0
    update_count = 0
    fail_count = 0
    error_reasons = []

    accounts_str = sender.input(120000, 1, False)
    if accounts_str == 'q':
        sender.reply('❌ 已退出登录操作！')
        return
    if not accounts_str:
        sender.reply('❌ 输入超时！')
        return
    accounts = [line.strip() for line in accounts_str.split('\n') if line.strip()]

    total = len(accounts)
    if total == 0:
        sender.reply("❌ 未检测到有效账号信息")
        return

    sender.reply(f"🔍 共检测到 {total} 个账号，开始批量登录...")

    for index, account in enumerate(accounts, 1):
        try:
            nick_name, phone, integral, isSign = get_info(account)
            if phone:
                success_count += 1
                sg.bucketSet('mrconli.shuifeiyi.token', phone, account)
                current_accounts = _sg_literal(sg.bucketGet('mrconli.shuifeiyi.user', userid) or '[]')
                if phone not in current_accounts:
                    add_count += 1
                    status = "✅ 登录成功..."
                    current_accounts.append(phone)
                    sg.bucketSet('mrconli.shuifeiyi.user', userid, json.dumps(current_accounts, ensure_ascii=False))
                else:
                    update_count += 1
                    status = "✅ 更新成功..."
                    accountVip = '2099-12-31'
                    if not accountVip or accountVip < today_time:
                        sender.reply(f"⚠️ 账号未授权或授权已过期，环境变量未提交青龙...")
                    else:
                        add_to_qinglong(account, phone, userid)
                uservalue = json.dumps(current_accounts)
            else:
                fail_count += 1
                status = "❌ 登录失败！"
                error_reasons.append(f"{account}: 认证失败")
            progress = f"[{index}/{total}] {mask_phone(phone)} {status}"
            sender.reply(progress)
        except Exception as e:
            fail_count += 1
            error_msg = f"无效账号: {account}"
            error_reasons.append(error_msg)
            sender.reply(f"⚠️ 第{index}个账号处理失败: {error_msg}")
        time.sleep(2)

    report = (
        f"📊 登录完成\n"
        f"✅ 执行成功: {success_count} 个\n"
        f"➕ 添加: {add_count} 个\n"
        f"🔄 更新: {update_count} 个\n"
        f"✖️ 失败: {fail_count} 个\n"
        f"------------------------\n"
        f"发送“{manage_cmd}”管理账号\n"
        f"发送“{query_cmd}”查询账号\n"
    )

    if error_reasons:
        report += "\n❌ 失败原因:\n" + "\n".join(error_reasons[:5])
        if len(error_reasons) > 5:
            report += f"\n...等{len(error_reasons)-5}个错误"
    sender.reply(report)

def query():
    accounts = _sg_literal(uservalue or '[]')
    if not accounts:
        sender.reply(
            '\n=====水费易账号查询=====\n❌ 未找到任何账号\n------------------\n💡 发送"水费易登录"绑定账号\n===================')
        return
    if len(accounts) > 1:
        menu = "=====请选择查询账号=====\n[0] 查询全部账号\n------------------\n"
        for idx, acc in enumerate(accounts, 1):
            menu += f"[{idx}] {acc[:3]}****{acc[-4:]}\n"
        menu += "=======================\n⚠️ 请回复数字序号(输入q退出)"
        sender.reply(menu)

        choice = sender.input(30000, 1, False)
        if choice.lower() == 'q':
            sender.reply('已取消查询')
            return
        if not choice.isdigit():
            sender.reply('输入格式错误，请回复数字')
            return

        choice = int(choice)
        if choice < 0 or choice > len(accounts):
            sender.reply('选择超出范围，已取消查询')
            return
    else:
        choice = 1  # 单个账号直接查询

    if choice == 0:
        target_accounts = accounts
        sender.reply('正在查询全部账号...')
    else:
        target_accounts = [accounts[choice - 1]]
        sender.reply('正在查询水费易，请耐心等待...')

    for account in target_accounts:
        try:
            accountVip = '2099-12-31'
            token = sg.bucketGet('mrconli.shuifeiyi.token', account)
            if not token:
                sender.reply(f'【{mask_phone(account)}】token获取失败')
                continue
            if not accountVip:
                sender.reply(f'【{mask_phone(account)}】账号未授权')
            elif accountVip < today_time:
                sender.reply(f'【{mask_phone(account)}】云授权过期')
            else:
                nick_name, phone, integral, isSign = get_info(token)
                if not phone:
                    sender.reply(f'❌ 【{mask_phone(account)}】token失效，请重新登录...')
                    continue
                sender.reply(f"""
=====水费易账号详情=====
📱 账号：{mask_phone(phone)}
👤 昵称：{nick_name}
🔥 会员ID：{token}
🍀 积分：{integral}
⏰ 授权到期：{accountVip}
==================""")
        except Exception as e:
            sender.reply(f'❌ 【{mask_phone(account)}】查询出错: {str(e)}')


def user_qd():
    accounts = _sg_literal(uservalue or '[]')
    if not accounts:
        sender.reply(
            '\n=====水费易账号签到=====\n❌ 未找到任何账号\n------------------\n💡 发送"水费易登录"绑定账号\n===================')
        return
    if len(accounts) > 1:
        menu = "=====请选择签到账号=====\n[0] 签到全部账号\n------------------\n"

        for idx, acc in enumerate(accounts, 1):
            menu += f"[{idx}] {acc[:3]}****{acc[-4:]}\n"
        menu += "=======================\n⚠️ 请回复数字序号(输入q退出)"
        sender.reply(menu)

        choice = sender.input(30000, 1, False)
        if choice.lower() == 'q':
            sender.reply('已取消查询')
            return
        if not choice.isdigit():
            sender.reply('输入格式错误，请回复数字')
            return

        choice = int(choice)
        if choice < 0 or choice > len(accounts):
            sender.reply('选择超出范围，已取消查询')
            return
    else:
        choice = 1  # 单个账号直接查询

    if choice == 0:
        target_accounts = accounts
        sender.reply('正在执行签到全部账号...')
    else:
        target_accounts = [accounts[choice - 1]]
        sender.reply('正在执行签到，请耐心等待...')

    for account in target_accounts:
        try:
            accountVip = '2099-12-31'
            token = sg.bucketGet('mrconli.shuifeiyi.token', account)
            if not token:
                sender.reply(f'【{mask_phone(account)}】token获取失败')
                continue
            if not accountVip:
                sender.reply(f'【{mask_phone(account)}】账号未授权')
            elif accountVip < today_time:
                sender.reply(f'【{mask_phone(account)}】云授权过期')
            else:
                qd(token)
        except Exception as e:
            sender.reply(f'❌ 【{mask_phone(account)}】查询出错: {str(e)}')


def all_qd():
    """所有用户签到功能"""
    try:
        users = sg.bucketAllKeys('mrconli.shuifeiyi.user')
        for user in users:
            try:
                accounts = json.loads(sg.bucketGet('mrconli.shuifeiyi.user', user)) if sg.bucketGet('mrconli.shuifeiyi.user', user) else []
            except json.JSONDecodeError as e:
                print(f"解析用户数据失败：{str(e)}")
                accounts = []
            for account in accounts:
                token = sg.bucketGet('mrconli.shuifeiyi.token', account)
                qd(token)    # 调用签到函数
    except Exception as e:
        sender.reply(f"❌ 签到失败: {str(e)}")


def get_config():
    """获取插件配置"""
    try:
        sg.bucketGet('mrconli.shuifeiyi', 'coin_bucket') or 'dd_sign_points'
        var_name = sg.bucketGet('mrconli.shuifeiyi', 'var_name') or "m_dnys"
        if not var_name:
            print("未配置变量名，使用默认值: m_dnys")
            var_name = 'm_dnys'
            sg.bucketSet('mrconli.shuifeiyi', 'var_name', var_name)
        ql_config = sg.bucketGet('mrconli.shuifeiyi', 'ql_config')
        if not ql_config:
            raise ValueError("青龙配置未设置")
        ql_params = ql_config.split('丨')
        if len(ql_params) != 3:
            raise ValueError("青龙配置格式错误，应为 地址丨ClientID丨ClientSecret")
        if len(ql_params) == 3:
            ql_host = ql_params[0]
            ql_client_id = ql_params[1]
            ql_client_secret = ql_params[2]
        else:
            print("青龙配置不完整，请检查配置")
        manage_cmd = sg.bucketGet('mrconli.shuifeiyi', 'manage_cmd') or '水费易管理'
        query_cmd = sg.bucketGet('mrconli.shuifeiyi', 'query_cmd') or '水费易查询'
        login_cmd = sg.bucketGet('mrconli.shuifeiyi', 'login_cmd') or '水费易登录'
        try:
            price = Decimal(sg.bucketGet('mrconli.shuifeiyi', 'price') or '1')
            if price < 0:
                raise ValueError("价格不能为负数")
        except (ValueError, decimal.InvalidOperation):
            print("价格配置无效，使用默认值: 1")
            price = Decimal('1')
            sg.bucketSet('mrconli.shuifeiyi', 'price', '1')
        try:
            coin_price = int(sg.bucketGet('mrconli.shuifeiyi', 'coin') or '0')
            if coin_price < 0:
                raise ValueError("积分不能为负数")
        except ValueError:
            print("积分配置无效，使用默认值: 0")
            coin_price = 0
            sg.bucketSet('mrconli.shuifeiyi', 'coin', '0')
        try:
            show_records = int(sg.bucketGet('mrconli.shuifeiyi', 'show_records') or '3')
            if show_records < 1:
                raise ValueError("显示记录数不能小于1")
        except ValueError:
            print("显示记录数配置无效，使用默认值: 3")
            show_records = 3
            sg.bucketSet('mrconli.shuifeiyi', 'show_records', '3')
        return (var_name, ql_host, ql_client_id, ql_client_secret, manage_cmd, query_cmd, login_cmd, price, coin_price,
                show_records, show_records)
    except Exception as e:
        error_msg = f"获取配置失败: {str(e)}"
        print(error_msg)
        sender.reply(f"❌ {error_msg}")
        raise


def init_qinglong():
    """初始化青龙连接"""
    try:
        ql_config = sg.bucketGet('mrconli.shuifeiyi', 'ql_config')
        if not ql_config:
            raise ValueError("青龙配置未设置")
        ql_host, ql_client_id, ql_client_secret = ql_config.split('丨')
        if not ql_host or not ql_client_id or not ql_client_secret:
            print("青龙配置不完整，请检查配置")
            exit(0)
        if not ql_host.endswith('/'):
            ql_host += '/'
        token = get_ql_token(ql_host, ql_client_id, ql_client_secret)
        return ql_host, token
    except Exception as e:
        sender.reply(f"❌ 连接青龙失败: {str(e)}")
        exit(0)


def get_ql_token(url, client_id, client_secret):
    """获取青龙token"""
    try:
        if not url.endswith('/'):
            url += '/'
        r = requests.get(f'{url}open/auth/token?client_id={client_id}&client_secret={client_secret}')
        if r.status_code != 200:
            raise Exception(f"请求失败: {r.status_code}")
        data = r.json()
        if "token" not in data.get('data', {}):
            raise Exception("获取token失败")
        return data['data']['token']
    except Exception as e:
        raise Exception(f"获取token失败: {str(e)}")


def add_to_qinglong(token, account, username):
    """添加变量到青龙"""
    try:
        url = f"{ql_host}/open/envs"
        headers = {
            "Authorization": f"Bearer {ql_token}",
            "Content-Type": "application/json"
        }

        existing_ids = []
        duplicate_vars = []
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            for env in response.json().get('data', []):
                if env['name'] == var_name and env.get('remarks', '') and account in env.get('remarks', ''):
                    existing_ids.append(env['id'])
                elif env['value'] == token:  # 新增重复值检测
                    duplicate_vars.append(env['id'])

        if duplicate_vars:
            del_response = requests.delete(url, json=duplicate_vars, headers=headers)
            if del_response.status_code != 200:
                raise Exception(f"删除冲突变量失败: {del_response.text}")

        if existing_ids:
            del_response = requests.delete(url, json=existing_ids, headers=headers)
            if del_response.status_code != 200:
                raise Exception(f"删除旧变量失败: {del_response.text}")

        auth_time = '2099-12-31' or '未授权'
        data = {
            "name": var_name,
            "value": token,
            "remarks": f"水费易账号:{account}丨用户:{userid}丨授权时间:{auth_time}",
        }

        max_retries = 3
        for attempt in range(max_retries):
            response = requests.post(url, headers=headers, json=[data])
            if response.status_code == 200:
                new_ids = [item['id'] for item in response.json().get('data', [])]
                sg.bucketSet('mrconli.shuifeiyi.env_id', account, json.dumps(new_ids))
                return True
            elif response.status_code == 500 and "SequelizeUniqueConstraintError" in response.text:
                print(f"🔄 检测到唯一性冲突，正在重试 ({attempt+1}/{max_retries})")
                time.sleep(1)

        error_detail = response.json().get('message') or response.text
        raise Exception(f"操作失败：多次尝试后仍存在唯一性冲突 | {error_detail} [HTTP {response.status_code}]")

    except Exception as e:
        error_msg = f"青龙操作失败: {str(e)}"
        print(error_msg)
        sender.reply(f"❌ {error_msg}")
        return False


def enable_in_qinglong(env_ids):
    """启用环境变量"""
    try:
        url = f"{ql_url}/open/envs/enable"
        headers = {
            "Authorization": f"Bearer {ql_token}",
            "Content-Type": "application/json"
        }
        response = requests.put(url, headers=headers, data=json.dumps(env_ids))
        if response.status_code == 200:
            rjson = response.json()
            if rjson.get('code') == 200:
                return True
            else:
                sender.reply(f"❌ 启用环境变量失败: {rjson.get('message')}")
                return False
        else:
            raise Exception(f"{response.status_code}")
    except Exception as e:
        sender.reply(f"❌ 启用环境变量失败: {str(e)}")
        return False


def disable_in_qinglong(env_ids):
    """禁用环境变量"""
    try:
        url = f"{ql_url}/open/envs/disable"
        headers = {
            "Authorization": f"Bearer {ql_token}",
            "Content-Type": "application/json"
        }
        response = requests.put(url, headers=headers, data=json.dumps(env_ids))
        if response.status_code == 200:
            rjson = response.json()
            if rjson.get('code') == 200:
                return True
            else:
                sender.reply(f"❌ 禁用环境变量失败: {rjson.get('message')}")
                return False
        else:
            raise Exception(f"{response.status_code}")
    except Exception as e:
        sender.reply(f"❌ 禁用环境变量失败: {str(e)}")
        return False


def delete_from_qinglong(account):
    """从青龙删除变量"""
    try:
        url = f"{ql_url}/open/envs"
        headers = {
            "Authorization": f"Bearer {ql_token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception("获取变量失败")
        env_id = None
        for env in response.json()['data']:
            if env['name'] == var_name and env.get('remarks', '') and account in env.get('remarks', ''):
                env_id = env['id']
                break
        if env_id:
            response = requests.delete(url, headers=headers, json=[env_id])
            if response.status_code != 200:
                raise Exception("删除变量失败")
        return True
    except Exception as e:
        sender.reply(f"❌ 青龙操作失败: {str(e)}")
        return False


def manage_accounts():
    """管理账号"""
    accounts = _sg_literal(uservalue or "[]")
    if not accounts:
        sender.reply(f"""
=====账号管理=====
❌ 未找到任何账号
------------------
💡 发送"{login_cmd}"绑定账号
==================""")
        return

    account_list = """
=====账号列表=====
批量操作:
[00] 授权全部账号
[01] 删除全部账号
------------------
账号列表:"""
    for i, account in enumerate(accounts, 1):
        token = sg.bucketGet('mrconli.shuifeiyi.token', account)
        auth = '2099-12-31'
        auth_status = "✅ 已授权" if auth and auth > today else "❌ 未授权"
        username = f"{account}"
        account_list += f"\n[{i}] {username[:3]}****{username[-4:]}\n    {auth_status}"
        if auth and auth > today:
            account_list += f"\n    授权到期: {auth}"
    account_list += "\n------------------\n回复数字选择账号\n回复'q'退出"

    sender.reply(account_list)
    choice = sender.listen(60000)

    if not choice:
        sender.reply("❌ 操作超时")
        return
    elif choice == 'q':
        sender.reply("✅ 已取消操作")
        return

    try:
        if choice == '01':
            accounts.copy()
            for account in accounts:
                delete_account(account)
            sg.bucketSet('mrconli.shuifeiyi.user', userid, '[]')
            sender.reply("✅ 已删除全部账号")

        elif choice == '00':
            sender.reply("📝 请输入授权天数(如使用积分兑换，必须为30的倍数):")
            days = sender.listen(60000)
            if not days:
                sender.reply("❌ 操作超时")
                return
            elif days == 'q':
                sender.reply("✅ 已取消授权")
                return
            coin_bucket = sg.bucketGet('mrconli.shuifeiyi', 'coin_bucket') or 'dd_sign_points'
            coin_price = int(sg.bucketGet('mrconli.shuifeiyi', 'coin') or '0')  # 确保获取最新积分价格

            try:
                days = int(days)
                if days <= 0:
                    raise ValueError("天数必须大于0")

                pay_choice = '1'
                if coin_price > 0:
                    user_coin = Decimal(sg.bucketGet('coin_bucket', userid) or '0')
                    auth_guide = f"""
=====批量授权方式=====
[1] 微信支付
[2] 积分支付 (当前积分: {user_coin})
--------------------
💰 积分比例: {coin_price}积分/月
回复数字选择方式"""
                    sender.reply(auth_guide)
                    pay_choice = sender.listen(60000)
                    if pay_choice not in ['1', '2']:
                        sender.reply("❌ 无效的支付方式")
                        return

                if pay_choice == '1':
                    amount = price * (Decimal(days) / 30) * len(accounts)
                    amount = amount.quantize(Decimal('0.01'), rounding='ROUND_UP')
                    if process_payment(amount, days):
                        success_count = 0
                        for account in accounts:
                            calculate_auth_time(account, days / 30)
                            True
                            token = sg.bucketGet('mrconli.shuifeiyi.token', account)
                            username = account
                            if token and username:
                                add_to_qinglong(token, account, username)

                            success_count += 1
                        sender.reply(f"""
=====批量授权成功=====
💰 支付: {amount}元
⏰ 时长: {days}天
✅ 成功: {success_count}个账号
====================""")

                elif pay_choice == '2':
                    coin_bucket = sg.bucketGet('mrconli.shuifeiyi', 'coin_bucket') or 'dd_sign_points'
                    user_coin = Decimal(sg.bucketGet(coin_bucket, userid) or '0')
                    months = days / 30
                    if months != int(months):
                        sender.reply("❌ 积分支付需整月授权")
                        return
                    months = int(months)
                    need_coin = coin_price * months * len(accounts)
                    if user_coin < need_coin:
                        sender.reply(f"""
=====积分不足=====
❌ 积分余额不足
------------------
💰 所需积分: {need_coin}
💵 当前积分: {user_coin}
====================""")
                        return

                    new_coin = int(user_coin - need_coin)
                    sg.bucketSet(coin_bucket, userid, str(new_coin))
                    success_count = 0
                    for account in accounts:
                        calculate_auth_time(account, months)
                        True
                        token = sg.bucketGet('mrconli.shuifeiyi.token', account)
                        username = account
                        if token and username:
                            add_to_qinglong(token, account, username)

                        success_count += 1
                    sender.reply(f"""
=====批量授权成功=====
💰 消耗: {need_coin}积分
⏰ 时长: {days}天
✅ 成功: {success_count}个账号
💵 剩余: {new_coin}积分
====================""")

                for account in accounts:
                    env_id_str = sg.bucketGet('mrconli.shuifeiyi.env_id', account)
                    if env_id_str:
                        env_ids = json.loads(env_id_str)
                        enable_in_qinglong(env_ids)

            except ValueError as ve:
                sender.reply(f"❌ 无效的输入: {str(ve)}")
            except Exception as e:
                sender.reply(f"❌ 批量授权失败: {str(e)}")

        else:
            index = int(choice) - 1
            if 0 <= index < len(accounts):
                show_account_menu(accounts[index])
            else:
                sender.reply("❌ 无效的序号")

    except Exception as e:
        sender.reply(f"❌ 操作失败: {str(e)}")


def show_account_menu(account):
    """显示账号操作菜单"""
    token = sg.bucketGet('mrconli.shuifeiyi.token', account)
    auth = '2099-12-31'
    username = f"{account}"
    auth_status = "✅ 已授权" if auth and auth > today else "❌ 未授权"
    auth_info = f"\n    到期: {auth}" if auth and auth > today else ""
    menu = f"""
=====账号操作=====
📱 账号: {username[:3]}****{username[-4:]}
🔐 状态: {auth_status}{auth_info}
------------------
[1] 授权账号
[2] 删除账号
[3] 运行签到
------------------
回复数字选择操作
回复"q"退出"""
    sender.reply(menu)
    choice = sender.listen(60000)
    if not choice:
        sender.reply("❌ 操作超时")
        return
    elif choice == 'q':
        sender.reply("✅ 已取消操作")
        return
    try:
        if choice == '1':
            auth_account(account)
        elif choice == '2':
            delete_account(account)
        elif choice == '3':
            qd(token)
        else:
            sender.reply("❌ 无效的选择")
    except Exception as e:
        sender.reply(f"❌ 操作失败: {str(e)}")


def auth_account(account):
    """账号授权"""
    try:
        coin_bucket = sg.bucketGet('mrconli.shuifeiyi', 'coin_bucket') or 'dd_sign_points'
        user_coin = sg.bucketGet(coin_bucket, userid) or '0'
        user_coin = Decimal(user_coin)  # 使用 Decimal 处理大数值
        month_coin = Decimal(coin_price)  # 从配置获取每月所需积分
        if month_coin <= 0:
            auth_guide = """
=====授权方式=====
[1] 微信支付
------------------
回复数字选择方式
回复"q"退出"""
        else:
            auth_guide = f"""
=====授权方式=====
[1] 微信支付
[2] 积分支付 (当前积分: {user_coin})
------------------
💰 积分比例: {month_coin}积分/月
回复数字选择方式
回复"q"退出"""
        sender.reply(auth_guide)
        choice = sender.listen(60000)
        if not choice:
            sender.reply("❌ 操作超时")
            return False
        elif choice == 'q':
            sender.reply("✅ 已取消授权")
            return False
        if choice == '1':
            sender.reply("📝 请输入授权天数:")
            days = sender.listen(60000)
            if not days:
                sender.reply("❌ 操作超时")
                return False
            elif days == 'q':
                sender.reply("✅ 已取消授权")
                return False
            days = int(days)
            if days <= 0:
                raise ValueError()
            amount = price * (Decimal(days) / Decimal(30))
            amount = Decimal(str(amount)).quantize(Decimal('0.01'), rounding='ROUND_UP')
            if amount < Decimal('0.01'):
                amount = Decimal('0.01')
            payment_success = process_payment(amount, days)  # 处理支付
            if payment_success:  # 只有在支付成功的情况下才进行授权
                auth_time = calculate_auth_time(account, days / 30)
                True
                token = sg.bucketGet('mrconli.shuifeiyi.token', account)
                username = account  # 假设account存储的是手机号
                if token and username:
                    add_to_qinglong(token, account, username)  # 强制更新变量
                else:
                    sender.reply("⚠️ 令牌获取失败，请检查配置")
                env_id_str = sg.bucketGet('mrconli.shuifeiyi.env_id', account)
                if env_id_str:
                    env_ids = json.loads(env_id_str)
                    enable_in_qinglong(env_ids)
                sender.reply(f"""
=====授权成功=====
📱 账号: {account[:3]}****{account[-4:]}
💰 支付: {amount}元
⏰ 时长: {days}天
📅 到期: {auth_time}
==================""")
                return True
            else:
                sender.reply("❌ 支付未成功，授权未完成")
                return False
        elif choice == '2' and month_coin > 0:  # 只有积分支付开启时才处理
            sender.reply("📝 授权月数:")
            months = sender.listen(60000)
            if not months:
                sender.reply("❌ 操作超时")
                return False
            elif months == 'q':
                sender.reply("✅ 已取消授权")
                return False
            months = int(months)
            if months <= 0:
                raise ValueError()
            need_coin = month_coin * months
            if user_coin < need_coin:
                sender.reply(f"""
=====积分不足=====
❌ 积分余额不足
------------------
💰 所需积分: {need_coin}
💵 当前积分: {user_coin}
==================""")
                return False
            new_coin = int(user_coin - need_coin)
            sg.bucketSet(coin_bucket, userid, str(new_coin))
            auth_time = calculate_auth_time(account, months)
            True
            token = sg.bucketGet('mrconli.shuifeiyi.token', account)
            username = account  # 假设account存储的是手机号
            if token and username:
                add_to_qinglong(token, account, username)  # 强制更新变量
            else:
                sender.reply("⚠️ 令牌获取失败，请检查配置")

            env_id_str = sg.bucketGet('mrconli.shuifeiyi.env_id', account)
            if env_id_str:
                env_ids = json.loads(env_id_str)
                enable_in_qinglong(env_ids)
            sender.reply(f"""
=====授权成功=====
📱 账号: {account[:3]}****{account[-4:]}
💰 消耗: {need_coin}积分
⏰ 时长: {months}月
📅 到期: {auth_time}
------------------
💵 剩余: {new_coin}积分
==================""")
            return True
        else:
            sender.reply("❌ 无效的选择")
    except ValueError:
        sender.reply("❌ 无效的数值")
    except Exception as e:
        sender.reply(f"❌ 授权失败: {str(e)}")
    return False


def process_payment(amount, days):
    return True

def clean_expired():
    try:
        sender.reply('该管理项已取消，账号直接运行')
    except Exception:
        pass
    return None
def cron_task():
    """定时任务处理"""
    if imtype != 'fake':
        return
    try:
        users = sg.bucketAllKeys('mrconli.shuifeiyi.user')
        for user in users:
            accounts = _sg_literal(sg.bucketGet('mrconli.shuifeiyi.user', user) or '[]')
            for account in accounts:
                try:
                    token = sg.bucketGet('mrconli.shuifeiyi.token', account)
                    if not token:
                        continue
                    auth = '2099-12-31'
                    if auth and auth <= today:
                        env_id_str = sg.bucketGet('mrconli.shuifeiyi.env_id', account)
                        if env_id_str:
                            env_ids = json.loads(env_id_str)
                            disable_in_qinglong(env_ids)
                        notify_user(user, account, "授权已过期,环境变量已禁用,请及时续费")
                        continue
                except Exception as e:
                    print(f"处理账号 {account} 出错: {str(e)}")
                    continue
    except Exception as e:
        print(f"定时任务出错: {str(e)}")


def notify_user(user, account, message):
    """发送用户通知"""
    try:
        notify_msg = f"""
=====账号通知=====
📱 账号: {account}
📢 消息: {message}
=================="""
        sg.push('qq', '', user, '', notify_msg)
        sg.push('wx', '', user, '', notify_msg)
        sg.push('tg', '', user, '', notify_msg)
    except Exception as e:
        print(f"发送通知失败: {str(e)}")


def retry_on_error(func, retries=3, delay=1):
    """错误重试装饰器"""

    def wrapper(*args, **kwargs):
        for i in range(retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if i == retries - 1:
                    raise e
                time.sleep(delay)
        return None

    return wrapper


def log_operation(operation, user, account, status, message=''):
    """记录操作日志"""
    try:
        log = {
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'operation': operation,
            'user': user,
            'account': account,
            'status': status,
            'message': message
        }
        logs = _sg_literal(sg.bucketGet('mrconli.shuifeiyi.logs', 'operations') or '[]')
        logs.append(log)
        if len(logs) > 1000:  # 只保留最近1000条
            logs = logs[-1000:]
        sg.bucketSet('mrconli.shuifeiyi.logs', 'operations', str(logs))
    except Exception as e:
        print(f"记录日志失败: {str(e)}")


def admin_auth():
    try:
        sender.reply('该管理项已取消，账号直接运行')
    except Exception:
        pass
    return None
def update_qinglong_env():
    """更新全部青龙环境变量"""
    sender.reply("正在更新全部账号的青龙环境变量...")
    users = sg.bucketAllKeys('mrconli.shuifeiyi.user')
    total_users = len(users)
    total_accounts = 0
    success = 0
    failed = 0
    for user in users:
        accounts = _sg_literal(sg.bucketGet('mrconli.shuifeiyi.user', user) or '[]')
        for account in accounts:
            total_accounts += 1
            try:
                token = sg.bucketGet('mrconli.shuifeiyi.token', account)
                if token:
                    add_to_qinglong(token, account, user)
                env_ids_str = sg.bucketGet('mrconli.shuifeiyi.env_id', account)
                if env_ids_str:
                    env_ids = json.loads(env_ids_str)
                    enable_in_qinglong(env_ids)
                success += 1
            except Exception as e:
                failed += 1
    sender.reply(f"""
=====更新青龙完成=====
共计: {total_users}个用户{total_accounts}个账号
------------------
✅ 成功: {success}个账号
❌ 失败: {failed}个账号
==================""")


def auth_all_users():
    """一键授权所有用户"""
    sender.reply("""
=====批量授权=====
📝 请输入授权天数
------------------
回复数字设置天数
回复"q"退出""")
    try:
        days = sender.listen(60000)
        if not days or days == 'q':
            sender.reply("✅ 已取消授权")
            return
        days = int(days)
        if days <= 0:
            raise ValueError()
        users = sg.bucketAllKeys('mrconli.shuifeiyi.user')
        success = 0
        failed = 0
        for user in users:
            accounts = _sg_literal(sg.bucketGet('mrconli.shuifeiyi.user', user) or '[]')
            for account in accounts:
                try:
                    calculate_auth_time(account, days / 30)
                    True
                    token = sg.bucketGet('mrconli.shuifeiyi.token', account)
                    if token:
                        phone = account[:3] + '*' * 4 + account[7:]
                        add_to_qinglong(token, account, phone)
                    env_ids_str = sg.bucketGet('mrconli.shuifeiyi.env_id', account)
                    if env_ids_str:
                        env_ids = json.loads(env_ids_str)
                        enable_in_qinglong(env_ids)
                    success += 1
                    log_operation('batch_auth', user, account, 'success')
                except Exception as e:
                    failed += 1
                    log_operation('batch_auth', user, account, 'failed', str(e))
        sender.reply(f"""
=====授权完成=====
✅ 成功: {success}个账号
❌ 失败: {failed}个账号
⏰ 授权: {days}天
==================""")
    except ValueError:
        sender.reply("❌ 无效的天数")
    except Exception as e:
        sender.reply(f"❌ 授权失败: {str(e)}")


def auth_specific_user():
    """指定用户授权"""
    sender.reply("""
=====指定授权=====
📝 请输入用户ID
(发送myuid可获取ID)
------------------
回复"q"退出""")
    user_id = sender.listen(60000)
    if not user_id or user_id == 'q':
        return
    accounts = _sg_literal(sg.bucketGet('mrconli.shuifeiyi.user', user_id) or '[]')
    if not accounts:
        sender.reply("❌ 未找到该用户的账号")
        return
    account_list = """
=====账号列表=====
[0] 授权全部账号"""
    for i, account in enumerate(accounts, 1):
        auth = '2099-12-31'
        status = "✅ 已授权" if auth and auth > today else "❌ 未授权"
        account_list += f"\n[{i}] {account[:3]}****{account[-4:]}\n    {status}"
    account_list += """
------------------
回复数字选择账号
回复"q"退出"""
    sender.reply(account_list)
    choice = sender.listen(60000)
    if not choice or choice == 'q':
        return
    try:
        sender.reply("""
=====设置授权时间=====
📝 请输入授权天数
------------------
回复数字设置天数
回复"q"退出""")
        days = sender.listen(60000)
        if not days or days == 'q':
            return
        days = int(days)
        if days <= 0:
            raise ValueError()
        if choice == '0':
            for account in accounts:
                try:
                    auth_time = calculate_auth_time(account, days / 30)
                    True
                    token = sg.bucketGet('mrconli.shuifeiyi.token', account)
                    if token:
                        phone = account[:3] + '*' * 4 + account[7:]
                        add_to_qinglong(token, account, phone)
                    env_ids_str = sg.bucketGet('mrconli.shuifeiyi.env_id', account)
                    if env_ids_str:
                        env_ids = json.loads(env_ids_str)
                        enable_in_qinglong(env_ids)
                    log_operation('auth', user_id, account, 'success')
                except Exception as e:
                    log_operation('auth', user_id, account, 'failed', str(e))
            sender.reply(f"✅ 已授权所有账号 {days}天")
        else:
            index = int(choice) - 1
            if not 0 <= index < len(accounts):
                raise ValueError()
            account = accounts[index]
            auth_time = calculate_auth_time(account, days / 30)
            True
            token = sg.bucketGet('mrconli.shuifeiyi.token', account)
            if token:
                phone = account[:3] + '*' * 4 + account[7:]
                add_to_qinglong(token, account, phone)
            env_ids_str = sg.bucketGet('mrconli.shuifeiyi.env_id', account)
            if env_ids_str:
                env_ids = json.loads(env_ids_str)
                enable_in_qinglong(env_ids)
            sender.reply(f"""
=====授权成功=====
📱 账号: {account[:3]}****{account[-4:]}
⏰ 时长: {days}天
📅 到期: {auth_time}
==================""")
            log_operation('auth', user_id, account, 'success')
    except ValueError:
        sender.reply("❌ 无效的输入")
    except Exception as e:
        sender.reply(f"❌ 授权失败: {str(e)}")
        log_operation('auth', user_id, account, 'failed', str(e))


def check_account_status(self, token):
    """检查账号状态"""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    data = {
        "service": "media",
        "api": "lottery/queryActivityAwardRecordList",
        "data": {
            "uid": "30a7f9016d224fc2a8367200cbbab62a",
            "content": "null"}
    }
    response = _send_request(
        'POST',
        "https://app.eyh.cn/gateway/api",
        json=data,
        headers=headers
    )
    return response


def delete_account(account):
    """删除账号"""
    try:
        if not delete_from_qinglong(account):
            raise Exception("从青龙删除变量失败")
        sg.bucketDel('mrconli.shuifeiyi.token', account)
        True
        sg.bucketDel('mrconli.shuifeiyi.env_id', account)
        try:
            accounts = _sg_literal(uservalue or "[]")
        except (json.JSONDecodeError, TypeError) as e:
            print(f"用户列表解析失败: {str(e)}")

        if account in accounts:
            accounts.remove(account)
            try:
                sg.bucketSet('mrconli.shuifeiyi.user', userid, json.dumps(accounts, ensure_ascii=False))
            except Exception as e:
                raise Exception(f"用户列表更新失败: {str(e)}")
        sender.reply(f"""
=====删除成功=====
📱 账号: {account[:3]}****{account[-4:]}
✅ 状态: 已删除
==================""")
        log_operation('delete_account', userid, account, 'success')
        return True
    except Exception as e:
        error_msg = f"删除账号失败: {str(e)}"
        sender.reply(f"❌ {error_msg}")
        log_operation('delete_account', userid, account, 'failed', str(e))
        return False


async def async_request(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            return await response.json()


@lru_cache(maxsize=100)
def cached_bucket_get(bucket, key):
    return sg.bucketGet(bucket, key)


login_data = globals().get("login_data", {})


async def async_add_to_qinglong(token):
    return add_to_qinglong(token, globals().get("userid", ""), globals().get("userid", ""))

async def async_login():
    token = await async_request("https://app.eyh.cn/gateway/api", login_data)
    if token:
        await async_add_to_qinglong(token)


def tutorial():
    """显示水费易使用教程"""
    tutorial_text = (
        "[CQ:image,file=https://bbs.sillygirl.cn/assets/files/2025-06-17/1750162614-990316-567139274dae9a67a5e369f51a18fcda.webp]"
        "=====水费易教程=====\n"
        "📝 入口:\n"
        "    微信搜索服务号：水费易\n"
        "    点击[积分换购]，登录后点击[我的]，左上角显示[会员ID]\n"
        "🌟 基础指令:\n"
        "1. 水费易登录 - 绑定账号\n"
        "2. 水费易查询 - 查看状态\n"
        "3. 水费易签到 - 执行签到\n"
        "4. 水费易管理 - 管理账号\n"
        "5. 水费易授权 - 管理员授权账号\n"
        "6. 水费易清理 - 管理员清理过期\n"
        "7. 水费易一键签到 - 管理员一键签到\n"
        "-------------------\n"
        "🚩 收益说明:\n"
        "▸ 呆瓜为每日自动运行签到任务\n"
        "▸ 积分换实物\n"
        "=================="
    )
    sender.reply(tutorial_text)


def main():
    """主函数"""
    message = sender.getMessage()
    if '登录' in message or '登陆' in message or '上车' in message:
        batch_login()
    elif '管理' in message:
        manage_accounts()
    elif '查询' in message:
        query()
    elif message =="水费易签到" or message =="签到水费易":
        user_qd()
    elif message =="水费易一键签到" and sender.isAdmin():
        all_qd()
    elif '教程' in message:
        tutorial()
    elif message == '水费易清理':
        clean_expired()
    elif message == '水费易授权' and sender.isAdmin():
        admin_auth()


if __name__ == "__main__":
    try:
        var_name, ql_host, ql_client_id, ql_client_secret, manage_cmd, query_cmd, login_cmd, price, coin_price, show_records, show_records = get_config()
        ql_url, ql_token = init_qinglong()
        imtype = sender.getImtype()
        today = str(datetime.now().date())
        if imtype == 'fake':
            all_qd()
            cron_task()
        else:
            main()
    except Exception as e:
        sender.reply(f"❌ 运行出错: {str(e)}")
