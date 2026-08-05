# [title: m001_回收猿]
# [name: m001HuiShouYuan]
# [language: python]
# [class: 任务]
# [author: mrconli]
# [version: v1.4.0]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^回收猿(.*)$]
# [cron: 32 8,16 * * *]
# [icon: https://api.iconify.design/lucide:bot.svg]
# [description: ”；1.4.0更新：修复环境变量提交青龙bug；1.3.0更新：插件重构，去除手机号敏感信息，ck需要重新提交，非必要勿更新；1.0.0初版：支持批量登录]
# [depe: ["requests","urllib3"]]


import asyncio as _sg_asyncio
import os as _sg_os
import time as _sg_time
import types as _sg_types
import json as _sg_json
from threading import Thread as _sg_Thread
from sillygirl import Adapter as _SGAdapter, Bucket as _SGBucket, Sender as _SGSender, sender as _sg_sender, form
calculate_auth_time = lambda *args, **kwargs: "2099-12-31"
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

config = form({
    'mrconli_huishouyuan_ql_config': form.string().title('对接青龙').default('').description('|'),
    'mrconli_huishouyuan_var_name': form.string().title('环境变量名').default('').description('青龙容器内的变量名，默认为：hsy_username'),
    'mrconli_huishouyuan_is_proxy': form.boolean().title('是否启用代理').default(False).description('开启代理就勾选，其实不需要代理'),
    'mrconli_huishouyuan_proxy_pool': form.string().title('代理池地址').default('').description('代理API服务地址'),
})
_CONFIG_FIELD_MAP = {
    ('mrconli', 'huishouyuan.ql_config'): 'mrconli_huishouyuan_ql_config',
    ('mrconli', 'huishouyuan.var_name'): 'mrconli_huishouyuan_var_name',
    ('mrconli', 'huishouyuan.is_proxy'): 'mrconli_huishouyuan_is_proxy',
    ('mrconli', 'huishouyuan.proxy_pool'): 'mrconli_huishouyuan_proxy_pool',
}

batch_size = 50     #  每页账号数量
scripts_name =  "回收猿"
full_scripts_name =  "回收猿"
bucket_prefix = "mrconli.huishouyuan"


from datetime import datetime
from decimal import Decimal  # 处理浮点数
import requests  # 处理http请求
import time  # 处理时间
import json  # 处理json数据
import hashlib

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


senderID = sg.getSenderID()  # 获取发送者QQ号
sender = sg.Sender(senderID)  # 获取发送者对象
userid = sender.getUserID()  # 存储当前发送者的用户 ID，与 senderID 类似，但通常用于内部标识
uservalue = sg.bucketGet(bucket=f'{bucket_prefix}.user', key=userid)
today_date = datetime.now().date()
today_time = str(today_date)


MAX_RETRIES = 5  # 最大重试次数
IS_PROXY = sg.bucketGet(bucket_prefix, 'is_proxy')  # 是否启用代理True
PROXY_API = sg.bucketGet(bucket_prefix, 'proxy_pool') or "http://mrconli.com:12306"
proxy = None  # 初始化全局代理变量


def update_proxy():
    global proxy
    try:
        if not IS_PROXY or IS_PROXY == "false":
            proxy = None
            return
        response = requests.get(PROXY_API, timeout=15)
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
    if not phone or len(phone) != 11:
        return phone
    return f"{phone[:3]}****{phone[7:]}"



def get_sign(params):
    params_str = "&".join([f"{k}={v}" for k, v in params.items()]) + "UppwYkfBlk"
    encrypted_str = hashlib.md5(params_str.encode()).hexdigest()
    return encrypted_str



def get_user_balance(username):
    try:
        url = "https://www.52bjy.com/api/app/hsy.php"
        params = {
            "action": "user",
            "appkey": "1079fb245839e765",
            "merchant_id": "2",
            "method": "center",
            "username": username,
            "version": "2"
        }
        params["sign"] = get_sign(params)
        response = _send_request('GET', url, params=params).json()
        award_freeze_total = response['data']['award_freeze_total']    # 冻结中
        award_balance = response['data']['award_balance']    # 可提现
        award_check = response['data']['award_check']    # 提现中
        award_total = response['data']['award_total']    # 已提现
        award = response['data']['award']    # 余额
        all_award = round(float(award) + float(award_total), 2)
        msg = f"🧧 余额：{award}元\n💳 冻结中：{award_freeze_total}元\n🍀 可提现：{award_balance}元\n🔄 提现中：{award_check}元\n💰 已提现：{award_total}元\n📊 总收益：{all_award}元"
        print(msg)
        return True, msg
    except Exception as e:
            print(f"[获取用户余额]发生错误: {str(e)}")
            return False, None


def batch_login():
    global uservalue
    sender.reply(
        f"======={login_cmd}=======\n"
        "📝 请输入ck参数: 备注#username\n"
        "说明:\n"
        "  1.无需抓包，提交会员名即可登录\n"
        "  2.支持批量，一个账号一行 \n"
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
            parts = account.split('#')
            if len(parts) != 2:
                fail_count += 1
                error_reasons.append('❌ ck格式不正确')
                continue
            remark, token = parts
            success, msg =  get_user_balance(token)
            if not success:
                fail_count += 1
                error_reasons.append("❌ 登录认证失败")
                continue
            if success:
                phone = str(token)
                success_count += 1
                sg.bucketSet(f'{bucket_prefix}.token', phone, token)
                sg.bucketSet(f'{bucket_prefix}.remark', phone, remark)
                current_accounts = _sg_literal(sg.bucketGet(f'{bucket_prefix}.user', userid) or '[]')
                if phone not in current_accounts:
                    add_count += 1
                    status = f"✅ {remark} 登录成功"
                    current_accounts.append(phone)
                    sg.bucketSet(f'{bucket_prefix}.user', userid, json.dumps(current_accounts, ensure_ascii=False))
                else:
                    update_count += 1
                    status = f"✅ {remark} 更新成功"
                    accountVip = '2099-12-31'
                    if not accountVip or accountVip < today_time:
                        sender.reply("⚠️ 账号未授权或授权已过期，环境变量未提交青龙...")
                    else:
                        add_to_qinglong(token, phone, userid)
            else:
                print("登录失败")
                fail_count += 1
                error_reasons.append(f"❌ {account} 登录认证失败")
                continue

            uservalue = json.dumps(current_accounts)

            progress = f"[{index}/{total}] {status}"
            sender.reply(progress)
        except Exception as e:
            fail_count += 1
            error_msg = f"无效账号: {account}：{e}"
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
        total_pages = (len(accounts) + batch_size - 1) // batch_size
        for page in range(total_pages):
            start_idx = page * batch_size
            end_idx = min((page + 1) * batch_size, len(accounts))
            menu = f"==请选择查询账号(第{page + 1}/{total_pages}页)==\n[0] 查询全部账号\n------------------\n"
            for idx in range(start_idx, end_idx):
                acc = accounts[idx]
                remark = sg.bucketGet(f'{bucket_prefix}.remark', acc)
                menu += f"[{idx + 1}] {remark} \n"
            menu += "====================\n⚠️ 请回复数字序号(输入q退出)\n💡 支持多选，如：1,3,4,7\n💡 支持范围选择，如：1-3,5-6,8"
            if total_pages > 1:
                menu += f"\n📊 当前页：{start_idx + 1}-{end_idx}，共{len(accounts)}个账号"
            sender.reply(menu)

        choice = sender.input(30000, 1, False)
        if not choice:
            sender.reply('❌ 输入超时！')
            return
        if choice.lower() == 'q':
            sender.reply('已取消查询')
            return

        if '-' in choice:
            ranges = [r.strip() for r in choice.split(',')]
            target_accounts = []

            for range_str in ranges:
                if '-' in range_str:
                    range_parts = range_str.split('-')
                    if len(range_parts) != 2:
                        sender.reply('❌ 范围格式错误，请使用如"1-3"的格式')
                        return

                    start_str, end_str = range_parts[0].strip(), range_parts[1].strip()
                    if not start_str.isdigit() or not end_str.isdigit():
                        sender.reply('❌ 范围格式错误，起始和结束必须是数字')
                        return

                    start_num, end_num = int(start_str), int(end_str)
                    if start_num < 1 or end_num > len(accounts) or start_num > end_num:
                        sender.reply(f'❌ 范围超出有效范围：1-{len(accounts)}')
                        return

                    for i in range(start_num, end_num + 1):
                        target_accounts.append(accounts[i - 1])
                else:
                    if not range_str.isdigit():
                        sender.reply(f'❌ 输入格式错误："{range_str}"不是有效数字')
                        return

                    c_num = int(range_str)
                    if c_num == 0:
                        target_accounts = accounts
                        break
                    elif 1 <= c_num <= len(accounts):
                        target_accounts.append(accounts[c_num - 1])
                    else:
                        sender.reply(f'❌ 选择超出范围：{c_num}')
                        return

            if target_accounts == accounts:
                sender.reply(f'正在查询全部{scripts_name}账号...')
            else:
                sender.reply(f'正在查询选中的{len(target_accounts)}个账号...')
        elif ',' in choice or '，' in choice:
            choices = [c.strip() for c in choice.split(',')]
            target_accounts = []

            for c in choices:
                if not c.isdigit():
                    sender.reply(f'❌ 输入格式错误："{c}"不是有效数字')
                    return

                c_num = int(c)
                if c_num == 0:
                    target_accounts = accounts
                    break
                elif 1 <= c_num <= len(accounts):
                    target_accounts.append(accounts[c_num - 1])
                else:
                    sender.reply(f'❌ 选择超出范围：{c_num}')
                    return

            if target_accounts == accounts:
                sender.reply(f'正在查询全部{scripts_name}账号...')
            else:
                sender.reply(f'正在查询选中的{len(target_accounts)}个账号...')
        else:
            if not choice.isdigit():
                sender.reply('输入格式错误，请回复数字')
                return

            choice_num = int(choice)
            if choice_num < 0 or choice_num > len(accounts):
                sender.reply('选择超出范围，已取消查询')
                return

            if choice_num == 0:
                target_accounts = accounts
                sender.reply(f'正在查询全部{scripts_name}账号...')
            else:
                target_accounts = [accounts[choice_num - 1]]
    else:
        target_accounts = accounts
    for account in target_accounts:
        try:
            accountVip = '2099-12-31'
            token = sg.bucketGet(f'{bucket_prefix}.token', account)
            remark = sg.bucketGet(f'{bucket_prefix}.remark', account)
            if not token:
                sender.reply(f'❌ 【{mask_phone(account)}】ck获取失败')
                continue
            if not accountVip:
                sender.reply(f'❌ 【{mask_phone(account)}】账号未授权')
            elif accountVip < today_time:
                sender.reply(f'❌ 【{mask_phone(account)}】云授权过期')
            else:
                success, msg =  get_user_balance(token)
                if not success:
                    sender.reply(f'❌ 【{mask_phone(remark)}】查询失败')
                    continue
                sender.reply(f"""
====={full_scripts_name}详情=====
👤 账号：{remark}
{msg}
⏰ 授权到期：{accountVip}
==================""")
        except Exception as e:
            sender.reply(f'❌ 【{mask_phone(account)}】查询出错: {str(e)}')


def cron_task():
    if imtype != 'fake':
        return
    try:
        users = sg.bucketAllKeys(f'{bucket_prefix}.user')
        for user in users:
            accounts = _sg_literal(sg.bucketGet(f'{bucket_prefix}.user', user) or '[]')
            for account in accounts:
                try:
                    auth = '2099-12-31'
                    remark = sg.bucketGet(f'{bucket_prefix}.remark', account)
                    if auth and auth <= today:
                        delete_from_qinglong(account)
                        notify_user(user, account, f"{remark}账号授权已过期,环境变量已删除,请及时续费")
                        continue
                except Exception as e:
                    print(f"处理账号 {account} 出错: {str(e)}")
                    continue
    except Exception as e:
        print(f"定时任务出错: {str(e)}")


def notify_user(user, account, message):
    try:
        notify_msg = f"""
====={full_scripts_name}账号通知=====
📱 账号: {account}
📢 消息: {message}
=================="""
        sg.push('qq', '', user, '', notify_msg)
        sg.push('wx', '', user, '', notify_msg)
        sg.push('tg', '', user, '', notify_msg)
        sg.push('qx', '', user, '', notify_msg)
        sg.push('ipad', '', user, '', notify_msg)
    except Exception as e:
        print(f"发送通知失败: {str(e)}")

def get_config():
    try:
        var_name = sg.bucketGet(bucket_prefix, 'var_name') or "hsy_username"
        if not var_name:
            print("未配置变量名，使用默认值: hsy_username")
            var_name = 'hsy_username'
            sg.bucketSet(bucket_prefix, 'var_name', var_name)
        ql_config = sg.bucketGet(bucket_prefix, 'ql_config')
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
        return (var_name, ql_host, ql_client_id, ql_client_secret, manage_cmd, query_cmd, login_cmd, price, coin_price)
    except Exception as e:
        error_msg = f"获取配置失败: {str(e)}"
        print(error_msg)
        sender.reply(f"❌ {error_msg}")
        raise


def init_qinglong():
    try:
        ql_config = sg.bucketGet(bucket_prefix, 'ql_config')
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
                elif env['name'] == var_name and env['value'] == token:  # 重复值检测
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
            "remarks": f"{full_scripts_name}账号:{account}丨用户:{username}丨授权时间:{auth_time}",
        }
        max_retries = 3
        for attempt in range(max_retries):
            response = requests.post(url, headers=headers, json=[data])
            if response.status_code == 200:
                new_ids = [item['id'] for item in response.json().get('data', [])]
                sg.bucketSet(f'{bucket_prefix}.env_id', account, json.dumps(new_ids))
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




def delete_from_qinglong(account):
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


def perform_batch_auth(selected_accounts, days=None):
    try:
        sender.reply('该管理项已取消，账号直接运行')
    except Exception:
        pass
    return None
def manage_accounts():
    accounts = _sg_literal(sg.bucketGet(bucket=f'{bucket_prefix}.user', key=userid))
    if not accounts:
        sender.reply(f"""
=====账号管理=====
❌ 未找到任何账号
------------------
💡 发送"{login_cmd}"绑定账号
==================""")
        return
    total_pages = (len(accounts) + batch_size - 1) // batch_size

    for page in range(total_pages):
        start_idx = page * batch_size
        end_idx = min((page + 1) * batch_size, len(accounts))

        account_list = f"""
=====账号列表(第{page + 1}/{total_pages}页)=====
批量操作:
[00] 授权全部账号
[01] 删除全部账号
[02] 查看全部账号ck
------------------
账号列表:"""
        for i in range(start_idx, end_idx):
            account = accounts[i]
            sg.bucketGet(f'{bucket_prefix}.token', account)
            remark = sg.bucketGet(f'{bucket_prefix}.remark', account)
            auth = '2099-12-31'
            auth_status = "✅ 已授权" if auth and auth > today else "❌ 未授权"
            account_list += f"\n[{i + 1}] {remark}\n    {auth_status}"
            if auth and auth > today:
                account_list += f"\n    授权到期: {auth}"
        account_list += "\n------------------\n回复数字选择账号详细管理\n回复'1,3'多选账号批量授权\n回复'1-3,5-6,8'范围选择\n回复'q'退出"
        if total_pages > 1:
            account_list += f"\n📊 当前页：{start_idx + 1}-{end_idx}，共{len(accounts)}个账号"
        sender.reply(account_list)


    choice = sender.listen(60000)

    if not choice:
        sender.reply("❌ 操作超时")
        return
    elif choice == 'q' or choice == 'Q':
        sender.reply("✅ 已取消操作")
        return
    try:
        if choice == '01':
            for account in accounts:
                delete_account(account)
            sg.bucketSet(f'{bucket_prefix}.user', userid, '[]')
            sender.reply("✅ 已删除全部账号")
        elif choice == '02':
            for account in accounts:
                show_ck(account)
        elif choice == '00':
            selected_accounts = accounts
            perform_batch_auth(selected_accounts, days=None)
        elif '-' in choice:
            try:
                ranges = [r.strip() for r in choice.split(',')]
                selected_indices = []

                for range_str in ranges:
                    if '-' in range_str:
                        range_parts = range_str.split('-')
                        if len(range_parts) != 2:
                            sender.reply("❌ 范围格式错误，请使用如'1-3'的格式")
                            return

                        start_str, end_str = range_parts[0].strip(), range_parts[1].strip()
                        if not start_str.isdigit() or not end_str.isdigit():
                            sender.reply("❌ 范围格式错误，起始和结束必须是数字")
                            return

                        start_num, end_num = int(start_str), int(end_str)
                        if start_num < 1 or end_num > len(accounts) or start_num > end_num:
                            sender.reply(f"❌ 范围超出有效范围：1-{len(accounts)}")
                            return

                        for i in range(start_num, end_num + 1):
                            selected_indices.append(i - 1)
                    else:
                        if not range_str.isdigit():
                            sender.reply(f"❌ 输入格式错误：'{range_str}'不是有效数字")
                            return

                        c_num = int(range_str)
                        if c_num == 0:
                            selected_indices = list(range(len(accounts)))
                            break
                        elif 1 <= c_num <= len(accounts):
                            selected_indices.append(c_num - 1)
                        else:
                            sender.reply(f"❌ 选择超出范围：{c_num}")
                            return

                if not selected_indices:
                    sender.reply("❌ 未找到有效的账号序号")
                    return

                selected_accounts = [accounts[idx] for idx in selected_indices]
                if len(selected_indices) == len(accounts):
                    sender.reply("正在为全部账号进行批量授权...")
                else:
                    sender.reply(f"正在为选中的{len(selected_accounts)}个账号进行批量授权...")
                perform_batch_auth(selected_accounts, days=None)
            except ValueError:
                sender.reply("❌ 无效的范围格式")

        elif ',' in choice or '，' in choice:
            try:
                choices = [c.strip() for c in choice.replace('，', ',').split(',')]
                selected_indices = []

                for c in choices:
                    if not c.isdigit():
                        sender.reply(f"❌ 输入格式错误：'{c}'不是有效数字")
                        return

                    c_num = int(c)
                    if c_num == 0:
                        selected_indices = list(range(len(accounts)))
                        break
                    elif 1 <= c_num <= len(accounts):
                        selected_indices.append(c_num - 1)
                    else:
                        sender.reply(f"❌ 选择超出范围：{c_num}")
                        return

                if not selected_indices:
                    sender.reply("❌ 未找到有效的账号序号")
                    return

                selected_accounts = [accounts[idx] for idx in selected_indices]
                if len(selected_indices) == len(accounts):
                    sender.reply("正在为全部账号进行批量授权...")
                else:
                    sender.reply(f"正在为选中的{len(selected_accounts)}个账号进行批量授权...")
                perform_batch_auth(selected_accounts, days=None)
            except ValueError:
                sender.reply("❌ 无效的选择格式，请使用数字逗号分隔")
        else:
            try:
                index = int(choice) - 1
                if 0 <= index < len(accounts):
                    show_account_menu(accounts[index])
                else:
                    sender.reply("❌ 无效的序号")
            except ValueError:
                sender.reply("❌ 无效的输入")

    except Exception as e:
        sender.reply(f"❌ 操作失败: {str(e)}")


def show_account_menu(account):
    auth = '2099-12-31'
    remark = sg.bucketGet(f'{bucket_prefix}.remark', account)
    auth_status = "✅ 已授权" if auth and auth > today else "❌ 未授权"
    auth_info = f"\n    到期: {auth}" if auth and auth > today else ""
    menu = f"""
=====账号操作=====
📱 账号: {remark}
🔐 状态: {auth_status}{auth_info}
------------------
[1] 授权账号
[2] 删除账号
[3] 查看账号ck
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
            show_ck(account)
        else:
            sender.reply("❌ 无效的选择")
    except Exception as e:
        sender.reply(f"❌ 操作失败: {str(e)}")


def auth_account(account):
    try:
        price = Decimal(sg.bucketGet(bucket_prefix, 'price') or '1')   #  每月价格
        coin_bucket = sg.bucketGet(bucket_prefix, 'coin_bucket') or 'dd_sign_points'
        user_coin = sg.bucketGet(coin_bucket, userid) or '0'
        user_coin = Decimal(user_coin)  # 使用 Decimal 处理大数值
        month_coin = Decimal(coin_price)  # 从配置获取每月所需积分
        remark = sg.bucketGet(f'{bucket_prefix}.remark', account)
        token = sg.bucketGet(f'{bucket_prefix}.token', account)

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
            if token:
                add_to_qinglong(token, account, userid)  # 强制更新变量
            else:
                sender.reply("⚠️ token获取失败，请检查配置")
            env_id_str = sg.bucketGet(f'{bucket_prefix}.env_id', account)
            if env_id_str:
                env_ids = json.loads(env_id_str)
                enable_in_qinglong(env_ids)
            sender.reply(f"""
=====授权成功=====
📱 账号: {remark}
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
                if token:
                    add_to_qinglong(token, account, userid)  # 强制更新变量
                else:
                    sender.reply("⚠️ 令牌获取失败，请检查配置")
                env_id_str = sg.bucketGet(f'{bucket_prefix}.env_id', account)
                if env_id_str:
                    env_ids = json.loads(env_id_str)
                    enable_in_qinglong(env_ids)
                sender.reply(f"""
=====授权成功=====
📱 账号: {remark}
⏰ 时长: {days}天
📅 到期: {auth_time}
==================""")
                return True

            if amount != 0:
                payment_success = process_payment(amount, days)  # 处理支付
                if payment_success:  # 只有在支付成功的情况下才进行授权
                    auth_time = calculate_auth_time(account, days / 30)
                    True
                    if token:
                        add_to_qinglong(token, account, userid)  # 强制更新变量
                    else:
                        sender.reply("⚠️ 令牌获取失败，请检查配置")
                    env_id_str = sg.bucketGet(f'{bucket_prefix}.env_id', account)
                    if env_id_str:
                        env_ids = json.loads(env_id_str)
                        enable_in_qinglong(env_ids)
                    sender.reply(f"""
    =====授权成功=====
    📱 账号: {remark}
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
            if token:
                add_to_qinglong(token, account, userid)  # 强制更新变量
            else:
                sender.reply("⚠️ 令牌获取失败，请检查配置")
            env_id_str = sg.bucketGet(f'{bucket_prefix}.env_id', account)
            if env_id_str:
                env_ids = json.loads(env_id_str)
                enable_in_qinglong(env_ids)
            sender.reply(f"""
=====授权成功=====
📱 账号: {remark}
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


def log_operation(operation, user, account, status, message=''):
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






def delete_account(account):
    try:
        if not delete_from_qinglong(account):
            raise Exception("从青龙删除变量失败")
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

def show_ck(account):
    token = sg.bucketGet(f'{bucket_prefix}.token', account)
    if token:
        sender.reply(f"""
====={full_scripts_name}账号ck=====
📱 账号: {mask_phone(account)}
🔑 CK: {token}
====================""")
    else:
        sender.reply(f"❌ {full_scripts_name}账号未绑定ck")


def tutorial():
    f"""显示{full_scripts_name}使用教程"""
    tutorial_text = (
        f"====={full_scripts_name}教程=====\n"
        "📝 入口:\n"
         "    #小程序://回收猿旧衣服回收/7Jz5jz1MtjDzemI\n"
         "    [CQ:image,file=https://bbs.sillygirl.cn/assets/files/2026-05-03/1777772546-550270-qq20260503-094145.png]\n"
        "-------------------\n"
        "🌟 基础指令:\n"
        f"1. {scripts_name}登录 - 绑定账号\n"
        f"2. {scripts_name}查询 - 查看状态\n"
        f"3. {scripts_name}时长 - 刷新时长\n"
        f"4. {scripts_name}管理 - 管理账号\n"
        f"5. {scripts_name}授权 - 管理员授权账号\n"
        f"6. {scripts_name}清理 - 管理员清理过期\n"
        "-------------------\n"
        "🚩 收益说明:\n"
        "▸ 签到领现金，满1可提现\n"
        "=================="
    )
    sender.reply(tutorial_text)


def main():
    message = sender.getMessage()
    if '登录' in message or '登陆' in message or '上车' in message:
        batch_login()
    elif '管理' in message:
        manage_accounts()
    elif '查询' in message:
        query()
    elif '教程' in message:
        tutorial()
    elif '清理' in message:
        if sender.isAdmin():
            clean_expired()
        else:
            sender.reply("❌ 您不是管理员，无法执行此操作")
    elif '授权' in message:
        if sender.isAdmin():
            admin_auth()
        else:
            sender.reply("❌ 您不是管理员，无法执行此操作")


if __name__ == "__main__":
    try:
        var_name, ql_host, ql_client_id, ql_client_secret, manage_cmd, query_cmd, login_cmd, price, coin_price = get_config()
        ql_url, ql_token = init_qinglong()
        imtype = sender.getImtype()
        today = str(datetime.now().date())
        if imtype == 'fake':
            cron_task()
        else:
            main()
    except Exception as e:
        sender.reply(f"❌ 运行出错: {str(e)}")
