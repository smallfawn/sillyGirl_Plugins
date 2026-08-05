# [title: m034_旧衣小二]
# [name: m034JiuYiXiaoEr]
# [language: python]
# [class: 任务]
# [author: mrconli]
# [version: v1.0.0]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^小二(.*)$]
# [cron: 34 7,16 * * *]
# [icon: https://api.iconify.design/lucide:bot.svg]
# [description: 小程序_旧衣小二，内置签到，签到得现金；1.0.0初版：支持代理及批量登录]
# [depe: ["requests","urllib3"]]


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
    'mrconli_jiuyixiaoer_is_proxy': form.boolean().title('是否启用代理').default(False).description('true/false'),
    'mrconli_jiuyixiaoer_proxy_pool': form.string().title('代理池地址').default('').description('代理API服务地址'),
})
_CONFIG_FIELD_MAP = {
    ('mrconli', 'jiuyixiaoer.is_proxy'): 'mrconli_jiuyixiaoer_is_proxy',
    ('mrconli', 'jiuyixiaoer.proxy_pool'): 'mrconli_jiuyixiaoer_proxy_pool',
}

scripts_name =  "小二"
bucket_prefix = "mrconli.jiuyixiaoer"

from datetime import datetime, timedelta  # 操作日期、时间以及时间间隔
import urllib3
from decimal import Decimal  # 处理浮点数
import time  # 处理时间
import json  # 处理json数据
import random
import requests


urllib3.disable_warnings()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

senderID = sg.getSenderID()  # 获取发送者QQ号
sender = sg.Sender(senderID)  # 获取发送者对象
userid = sender.getUserID()  # 存储当前发送者的用户 ID，与 senderID 类似，但通常用于内部标识
uservalue = sg.bucketGet(bucket=f'{bucket_prefix}.user', key=userid)
today_date = datetime.now().date()
today_time = str(today_date)


MAX_RETRIES = 10  # 最大重试次数
IS_PROXY = sg.bucketGet(bucket_prefix, 'is_proxy')  # 是否启用代理True
PROXY_API = sg.bucketGet(bucket_prefix, 'proxy_pool')
proxy = None  # 初始化全局代理变量


def update_proxy():
    """更新代理IP地址"""
    global proxy
    try:
        if not IS_PROXY or IS_PROXY == "false":
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
            if IS_PROXY:
                proxy = proxy if 'proxy' in globals() else None
                if not proxy:
                    update_proxy()
            kwargs['timeout'] = kwargs.get('timeout', 15)  # 默认超时时间 15 秒
            response = requests.request(
                method=method,
                url=url,
                proxies=proxy if IS_PROXY and proxy else None,
                verify=False,
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


def get_headers():
    """获取请求头信息"""
    return {
        'Host': 'jiuyixiaoer.fzjingzhou.com',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf2541113) XWEB/16771',
        'xweb_xhr': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'platform': 'MP-WEIXIN',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://servicewechat.com/wx426d52c8130b8559/5/page-frame.html',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }

def get_user_info(token):
    """获取用户信息"""
    update_proxy()
    url = 'https://jiuyixiaoer.fzjingzhou.com/api/Person/index'
    headers = get_headers()
    data = {
        'token': token
    }

    try:
        response = _send_request('POST', url, headers=headers, data=data).json()
        data = response['data']
        phone = data['mobile']
        msg = f"📱 账号: {mask_phone(data['mobile'])}\n👤 昵称: {data['nickname']}\n🌸 环保币: {data['score']}"
        print(msg)
        return True, phone, msg
    except Exception as e:
        print(f"请求异常: {str(e)}")
        return False, None, str(e)

def sign_in(token):
    """签到功能"""
    url = 'https://jiuyixiaoer.fzjingzhou.com/api/Person/sign'
    headers = get_headers()
    data = {
        'token': token
    }

    try:
        response = _send_request('POST', url, headers=headers, data=data).json()
        if response['code'] == 1000:
            msg = f"签到成功！获得积分: {response['data']}"
            return True, msg
        elif response['code'] == 1001:
            msg = f"{response['msg']}！"
            return True, msg
        else:
            msg = f"签到异常: {response['msg']}"
            return False, msg
    except Exception as e:
        print(f"请求异常: {str(e)}")
        return False, str(e)


def run(token):
    """主函数"""
    update_proxy()
    success, msg = sign_in(token)
    if success:
        return True, msg
    else:
        return False, msg


def batch_login():
    """批量登录函数"""
    global uservalue
    sender.reply(
        f"======={login_cmd}=======\n"
        "📝 请输入ck参数: token\n"
        "说明:\n"
        "  支持批量，一个账号一行\n"
        "  示例: 6f5873fd3b249a955151e692d5e02e1393d80e28\n"
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
            success, phone, msg = get_user_info(account)
            if not success:
                fail_count += 1
                error_reasons.append(f"❌ {mask_phone(account)} 登录认证失败")
                continue
            if not phone:
                fail_count += 1
                error_reasons.append(f"❌ 账户{mask_phone(account)}绑定手机号为空")
                continue
            if success and phone:
                success_count += 1
                phone = str(phone)
                sg.bucketSet(f'{bucket_prefix}.token', phone, account)
                current_accounts = _sg_literal(sg.bucketGet(f'{bucket_prefix}.user', userid) or '[]')
                if phone not in current_accounts:
                    add_count += 1
                    status = f"✅ {mask_phone(phone)} 登录成功"
                    current_accounts.append(phone)
                    sg.bucketSet(f'{bucket_prefix}.user', userid, json.dumps(current_accounts, ensure_ascii=False))
                else:
                    update_count += 1
                    status = f"✅ {mask_phone(phone)} 更新成功"
                    accountVip = '2099-12-31'
                    if not accountVip or accountVip < today_time:
                        sender.reply(f"⚠️ 账号未授权或授权已过期")
            uservalue = json.dumps(current_accounts)

            progress = f"[{index}/{total}] {status}"
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
            f'\n==={query_cmd}===\n❌ 未找到任何账号\n------------------\n💡 发送"{login_cmd}"绑定账号\n===================')
        return
    if len(accounts) > 1:
        menu = "=====请选择查询账号=====\n[0] 查询全部账号\n------------------\n"
        for idx, acc in enumerate(accounts, 1):
            menu += f"[{idx}] {mask_phone(acc)}\n"
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
        sender.reply(f'正在查询全部{scripts_name}账号...')
    else:
        target_accounts = [accounts[choice - 1]]

    for account in target_accounts:
        try:
            accountVip = '2099-12-31'
            token = sg.bucketGet(f'{bucket_prefix}.token', account)
            if not token:
                sender.reply(f'❌ 【{mask_phone(account)}】ck获取失败')
                continue
            if not accountVip:
                sender.reply(f'❌ 【{mask_phone(account)}】账号未授权')
            elif accountVip < today_time:
                sender.reply(f'❌ 【{mask_phone(account)}】云授权过期')
            else:
                sender.reply(f'正在查询{scripts_name}账号[{mask_phone(account)}]，请耐心等待...')
                success, phone, msg = get_user_info(token)
                if not success:
                    sender.reply(f'❌ 查询失败')
                    continue
                sender.reply(f"""
====={scripts_name}账号详情=====
{msg}
⏰ 授权到期：{accountVip}
===================""")
        except Exception as e:
            sender.reply(f'❌ 【{mask_phone(account)}】查询出错: {str(e)}')


def cron_task():
    """定时任务处理"""
    if imtype != 'fake':
        return
    try:
        users = sg.bucketAllKeys(f'{bucket_prefix}.user')
        for user in users:
            accounts = _sg_literal(sg.bucketGet(f'{bucket_prefix}.user', user) or '[]')
            for account in accounts:
                try:
                    auth = '2099-12-31'
                    if auth and auth <= today:
                        notify_user(user, account, "授权已过期,请及时续费")
                        continue
                    token = sg.bucketGet(f'{bucket_prefix}.token', account)
                    if not token:
                        notify_user(user, account, "ck获取失败,请及时绑定")
                        continue
                    success, phone, msg = sign_in(token)
                    notify_user(user, account, msg)
                    continue
                except Exception as e:
                    print(f"处理账号 {account} 出错: {str(e)}")
                    continue
    except Exception as e:
        print(f"定时任务出错: {str(e)}")


def user_run():
    accounts = _sg_literal(uservalue or '[]')
    if not accounts:
        sender.reply(
            f'\n==={scripts_name}运行===\n❌ 未找到任何账号\n------------------\n💡 发送"{login_cmd}"绑定账号\n===================')
        return
    if len(accounts) > 1:
        menu = "=====请选择运行账号=====\n[0] 运行全部账号\n------------------\n"
        for idx, acc in enumerate(accounts, 1):
            menu += f"[{idx}] {mask_phone(acc)}\n"
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
        sender.reply('正在运行全部账号...')
    else:
        target_accounts = [accounts[choice - 1]]

    for account in target_accounts:
        try:
            token = sg.bucketGet(f'{bucket_prefix}.token', account)
            if not token:
                sender.reply(f'❌ 【{mask_phone(account)}】token获取失败')
                continue
            accountVip = '2099-12-31'
            if not accountVip:
                sender.reply(f'❌ 【{mask_phone(account)}】账号未授权')
                continue
            elif accountVip < today_time:
                sender.reply(f'❌ 【{mask_phone(account)}】云授权过期')
                continue
            else:
                success, msg = run(token)
                if not success:
                    sender.reply(f'❌ 账号[{mask_phone(account)}]：{msg}')
                    continue
                sender.reply(f'✅ 账号[{mask_phone(account)}]：{msg}')
                continue
        except Exception as e:
            sender.reply(f'❌ 账号[{mask_phone(account)}]运行出错: {str(e)}')

def all_run():
    """所有用户运行函数"""
    success_count = 0
    faild_count = 0
    unvip = 0
    all_accounts = []
    users = sg.bucketAllKeys(bucket=f'{bucket_prefix}.user') or []

    if not users:
        sender.reply('❌ 未找到任何账号')
        return

    for user in users:
        accountlist = sg.bucketGet(bucket=f'{bucket_prefix}.user', key=user)
        if accountlist:
            all_accounts.extend(_sg_literal(accountlist))

    sender.reply(f'{scripts_name}正在一键运行{len(all_accounts)}个账号，请耐心等待...')

    total_count = len(all_accounts)
    success_count = 0
    failed_count = 0

    for account in all_accounts:
        try:
            token = sg.bucketGet(f'{bucket_prefix}.token', account)
            if not token:
                faild_count += 1
                print(f'【{mask_phone(account)}】access-token获取失败')
                continue
            accountVip = '2099-12-31'
            if not accountVip:
                unvip += 1
                sender.reply(f'❌ 【{mask_phone(account)}】账号未授权')
                continue
            elif accountVip < today_time:
                unvip += 1
                sender.reply(f'❌ 【{mask_phone(account)}】云授权过期')
                continue
            else:
                success, msg = run(token)
                if not success:
                    faild_count += 1
                    continue
                success_count += 1
                return True
        except Exception as e:
            failed_count += 1
            print(f'【{account}】运行出错: {str(e)}')
            return False
        finally:
            print(f"防黑号，随机延时...")
            time.sleep(random.uniform(5, 9))

    sender.reply(f"""
====={scripts_name}运行统计=====
⋄ 总账号数：{total_count}
⋄ 未授权：{unvip}
⋄ 成功执行：{success_count}
⋄ 执行失败：{failed_count}
==================""")


def notify_user(user, account, message):
    """发送用户通知"""
    try:
        notify_msg = f"""
====={scripts_name}账号通知=====
📱 账号: {account}
📢 签到结果: {message}
=================="""
        sg.push('qq', '', user, '', notify_msg)
        sg.push('wx', '', user, '', notify_msg)
        sg.push('tg', '', user, '', notify_msg)
        sg.push('qx', '', user, '', notify_msg)
        sg.push('ipad', '', user, '', notify_msg)

    except Exception as e:
        print(f"发送通知失败: {str(e)}")

def get_config():
    """获取插件配置"""
    try:
        manage_cmd = sg.bucketGet(bucket_prefix, 'manage_cmd') or f'{scripts_name}管理'
        query_cmd = sg.bucketGet(bucket_prefix, 'query_cmd') or f'{scripts_name}查询'
        login_cmd = sg.bucketGet(bucket_prefix, 'login_cmd') or f'{scripts_name}登录'
        try:
            price = Decimal(sg.bucketGet(bucket_prefix, 'price') or '1')
            if price < 0:
                raise ValueError("价格不能为负数")
        except (ValueError, decimal.InvalidOperation):
            print("价格配置无效，使用默认值: 1")
            price = Decimal('1')
            sg.bucketSet(bucket_prefix, 'price', '1')
        try:
            coin_price = int(sg.bucketGet(bucket_prefix, 'coin') or '0')
            if coin_price < 0:
                raise ValueError("积分不能为负数")
        except ValueError:
            print("积分配置无效，使用默认值: 0")
            coin_price = 0
            sg.bucketSet(bucket_prefix, 'coin', '0')
        return (manage_cmd, query_cmd, login_cmd, price, coin_price)
    except Exception as e:
        error_msg = f"获取配置失败: {str(e)}"
        print(error_msg)
        raise


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
        auth = '2099-12-31'
        auth_status = "✅ 已授权" if auth and auth > today else "❌ 未授权"
        account_list += f"\n[{i}] {mask_phone(account)}\n    {auth_status}"
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
            for account in accounts:
                delete_account(account)
            sg.bucketSet(f'{bucket_prefix}.user', userid, '[]')
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
            coin_bucket = sg.bucketGet(bucket_prefix, 'coin_bucket') or 'dd_sign_points'
            coin_price = int(sg.bucketGet(bucket_prefix, 'coin') or '0')  # 确保获取最新积分价格

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
                            success_count += 1
                        sender.reply(f"""
=====批量授权成功=====
💰 支付: {amount}元
⏰ 时长: {days}天
✅ 成功: {success_count}个账号
====================""")

                elif pay_choice == '2':
                    coin_bucket = sg.bucketGet(bucket_prefix, 'coin_bucket') or 'dd_sign_points'
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
                        success_count += 1
                    sender.reply(f"""
=====批量授权成功=====
💰 消耗: {need_coin}积分
⏰ 时长: {days}天
✅ 成功: {success_count}个账号
💵 剩余: {new_coin}积分
====================""")
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
    auth = '2099-12-31'
    auth_status = "✅ 已授权" if auth and auth > today else "❌ 未授权"
    auth_info = f"\n    到期: {auth}" if auth and auth > today else ""
    menu = f"""
=====账号操作=====
📱 账号: {mask_phone(account)}
🔐 状态: {auth_status}{auth_info}
------------------
[1] 授权账号
[2] 删除账号
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
        else:
            sender.reply("❌ 无效的选择")
    except Exception as e:
        sender.reply(f"❌ 操作失败: {str(e)}")


def auth_account(account):
    """账号授权"""
    try:
        price = Decimal(sg.bucketGet(bucket_prefix, 'price') or '1')   #  每月价格
        coin_bucket = sg.bucketGet(bucket_prefix, 'coin_bucket') or 'dd_sign_points'
        user_coin = sg.bucketGet(coin_bucket, userid) or '0'
        user_coin = Decimal(user_coin)  # 使用 Decimal 处理大数值
        month_coin = Decimal(coin_price)  # 从配置获取每月所需积分

        if price == 0:
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
            auth_time = calculate_auth_time(account, days / 30)
            True
            sender.reply(f"""
=====授权成功=====
📱 账号: {mask_phone(account)}
⏰ 时长: {days}天
📅 到期: {auth_time}
==================""")
            return True
        if month_coin <= 0:
            auth_guide = """
=====授权方式=====
[1] 微信支付
------------------
💰 现金比例: {price}元/30天
回复数字选择方式
回复"q"退出"""
        else:
            auth_guide = f"""
=====授权方式=====
[1] 微信支付
[2] 积分支付 (当前积分: {user_coin})
------------------
💰 现金比例: {price}元/30天
🌸 积分比例: {month_coin}积分/月
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

            if amount == 0:
                auth_time = calculate_auth_time(account, days / 30)
                True
                sender.reply(f"""
=====授权成功=====
📱 账号: {mask_phone(account)}
⏰ 时长: {days}天
📅 到期: {auth_time}
==================""")
                return True

            if amount != 0:
                payment_success = process_payment(amount, days)  # 处理支付
                if payment_success:  # 只有在支付成功的情况下才进行授权
                    auth_time = calculate_auth_time(account, days / 30)
                    True
                    sender.reply(f"""
    =====授权成功=====
    📱 账号: {mask_phone(account)}
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
            sender.reply(f"""
=====授权成功=====
📱 账号: {mask_phone(account)}
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
        logs = _sg_literal(sg.bucketGet(f'{bucket_prefix}.logs', 'operations') or '[]')
        logs.append(log)
        if len(logs) > 1000:  # 只保留最近1000条
            logs = logs[-1000:]
        sg.bucketSet(f'{bucket_prefix}.logs', 'operations', str(logs))
    except Exception as e:
        print(f"记录日志失败: {str(e)}")


def admin_auth():
    try:
        sender.reply('该管理项已取消，账号直接运行')
    except Exception:
        pass
    return None
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
        users = sg.bucketAllKeys(f'{bucket_prefix}.user')
        success = 0
        failed = 0
        for user in users:
            accounts = _sg_literal(sg.bucketGet(f'{bucket_prefix}.user', user) or '[]')
            for account in accounts:
                try:
                    calculate_auth_time(account, days / 30)
                    True
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
    accounts = _sg_literal(sg.bucketGet(f'{bucket_prefix}.user', user_id) or '[]')
    if not accounts:
        sender.reply("❌ 未找到该用户的账号")
        return
    account_list = """
=====账号列表=====
[0] 授权全部账号"""
    for i, account in enumerate(accounts, 1):
        auth = '2099-12-31'
        status = "✅ 已授权" if auth and auth > today else "❌ 未授权"
        account_list += f"\n[{i}] {mask_phone(account)}\n    {status}"
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
            sender.reply(f"""
=====授权成功=====
📱 账号: {mask_phone(account)}
⏰ 时长: {days}天
📅 到期: {auth_time}
==================""")
            log_operation('auth', user_id, account, 'success')
    except ValueError:
        sender.reply("❌ 无效的输入")
    except Exception as e:
        sender.reply(f"❌ 授权失败: {str(e)}")
        log_operation('auth', user_id, account, 'failed', str(e))


def delete_account(account):
    """删除账号"""
    try:
        sg.bucketDel(f'{bucket_prefix}.token', account)
        True
        sg.bucketDel(f'{bucket_prefix}.env_id', account)

        try:
            accounts = _sg_literal(uservalue or "[]")
        except (json.JSONDecodeError, TypeError) as e:
            print(f"用户列表解析失败: {str(e)}")

        if account in accounts:
            accounts.remove(account)
            try:
                sg.bucketSet(f'{bucket_prefix}.user', userid, json.dumps(accounts, ensure_ascii=False))
            except Exception as e:
                raise Exception(f"用户列表更新失败: {str(e)}")
        sender.reply(f"""
=====删除成功=====
📱 账号: {mask_phone(account)}
✅ 状态: 已删除
==================""")
        log_operation('delete_account', userid, account, 'success')
        return True
    except Exception as e:
        error_msg = f"删除账号失败: {str(e)}"
        sender.reply(f"❌ {error_msg}")
        log_operation('delete_account', userid, account, 'failed', str(e))
        return False

def tutorial():
    """显示使用教程"""
    tutorial_text = (
        f"====={scripts_name}教程=====\n"
        "📝 入口：\n"
        "    #小程序://旧衣小二/50M70rbP2pd50nz\n"
        "🌟 基础指令:\n"
        f"1. {scripts_name}登录 - 绑定账号\n"
        f"2. {scripts_name}查询 - 查看状态\n"
        f"3. {scripts_name}管理 - 管理账号\n"
        f"4. {scripts_name}授权 - 管理员授权账号\n"
        f"5. {scripts_name}清理 - 管理员清理过期\n"
        f"6. {scripts_name}教程 - 显示本教程\n"
        f"7. {scripts_name}运行 - 运行任务\n"
        f"8. {scripts_name}一键运行 - 管理员一键运行任务\n"
        "-------------------\n"
        "🚩 收益说明:\n"
        "▸ 签到获取积分、现金奖励\n"
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
    elif '教程' in message:
        tutorial()
    elif message == f"{scripts_name}运行":
        user_run()
    elif message == f"{scripts_name}一键运行" and sender.isAdmin():
        all_run()
    elif message == f'{scripts_name}清理':
        if sender.isAdmin():
            clean_expired()
        else:
            sender.reply("❌ 您不是管理员，无法执行此操作")
    elif message == f'{scripts_name}授权':
        if sender.isAdmin():
            admin_auth()
        else:
            sender.reply("❌ 您不是管理员，无法执行此操作")


if __name__ == "__main__":
    try:
        manage_cmd, query_cmd, login_cmd, price, coin_price = get_config()
        imtype = sender.getImtype()
        today = str(datetime.now().date())
        if imtype == 'fake':
            cron_task()
            all_run()
        else:
            main()
    except Exception as e:
        sender.reply(f"❌ 运行出错: {str(e)}")
