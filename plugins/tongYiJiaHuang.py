# [title: 统一茄皇]
# [name: tongYiJiaHuang]
# [language: python]
# [class: 任务]
# [author: rujingxianghai]
# [version: v1.4]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(茄皇|qh)(登录|登陆)$|^登(录|陆)(茄皇|qh)$|^(茄皇|qh)(查询|管理|教程)$|^(查询|管理)(茄皇|qh)$|^茄皇$|^茄皇检测$]
# [cron: 18 9 * * *]
# [icon: https://api.iconify.design/lucide:apple.svg]
# [description: 统一梦时代茄皇的家，每日签到浇水领奖励；1.0.5：适配新版；1.0.4：适配新版活动]
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
    's_qh_qlname': form.string().title('设置对接容器').default('').description('面板容器参数，不填则使用默认配置'),
    's_qh_use_dumbpanel': form.boolean().title('使用DumbPanel').default(False).description('勾选使用DumbPanel面板，不勾选使用青龙面板'),
    's_qh_osname': form.string().title('青龙变量名').default('').description('青龙容器内茄皇的变量名'),
    's_qh_notify': form.string().title('通知渠道').default('').description('检测通知推送渠道'),
})
_CONFIG_FIELD_MAP = {
    ('s_qh', 'qlname'): 's_qh_qlname',
    ('s_qh', 'use_dumbpanel'): 's_qh_use_dumbpanel',
    ('s_qh', 'osname'): 's_qh_osname',
    ('s_qh', 'notify'): 's_qh_notify',
}

import json
import time
import requests
from datetime import datetime

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()
uservalue = sg.bucketGet(bucket='s_qh_user', key=userid)

PLUGIN_CONFIG = {'bucket': 's_qh', 'coin_key': 'dd_sign_points', 'name': '茄皇的家'}


def _get_ql_client():
    """Get panel client based on config switch"""
    osname = sg.bucketGet('s_qh', 'osname') or 'S_TYQH'
    qlname = sg.bucketGet('s_qh', 'qlname') or ''
    use_dp = str(sg.bucketGet('s_qh', 'use_dumbpanel') or '').lower() == 'true'

    if use_dp:
        return DumbPanelClient(osname, qlname) if qlname else DumbPanelClient(osname)
    else:
        return QingLongClient(osname, qlname) if qlname else QingLongClient(osname)


def update_ql_env(wid, account_info):
    """Update panel env variable, format: wid#phone"""
    wid_value = account_info.get('wid', '')
    phone_value = account_info.get('phone', '')
    if not wid_value or not phone_value:
        return False
    env_value = f"{wid_value}#{phone_value}"
    auth_time = '2099-12-31' or '未授权'
    ql = _get_ql_client()
    return ql.update_env(wid, env_value, f"茄皇:{mask_account(wid)}|到期:{auth_time}")


def delete_ql_env(wid):
    """Delete panel env variable"""
    ql = _get_ql_client()
    return ql.delete_env(wid)


def qh_login(wid, phone):
    """Login to QH, returns (success, token, user_data_or_error)"""
    url = "https://api.zhumanito.cn/api/login"
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf254162e) XWEB/18163 miniProgram/wx532ecb3bdaaf92f9",
        'Content-Type': "application/json;charset=UTF-8",
        'origin': 'https://h5.zhumanito.cn',
        'referer': 'https://h5.zhumanito.cn/'
    }
    payload = {"wid": wid, "wm_phone": phone}
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=10).json()
        if 'data' in response and 'token' in response['data'] and 'user' in response['data']:
            return True, response['data']['token'], response['data']['user']
        return False, None, response.get('msg', '登录失败')
    except Exception as e:
        return False, None, str(e)


def bind_account():
    """Bindaccounts - wid#phone format"""
    sender.reply(
        "=====茄皇登录=====\n"
        "支持批量登录，格式如下:\n"
        "wid#phone（多账号换行分隔）\n"
        "------------------\n"
        "例如: 11281234567#13345678900\n"
        "------------------\n"
        "💡 wid获取方式:小程序\"统一梦时代\"\n"
        "1.抓包搜索 \"wid\"或登录时抓login接口\n"
        "2.个人中心授权后点头像，复制\"客户编号\"\n"
        "------------------\n"
        "回复\"q\"退出操作\n"
        "=================="
    )
    input_text = sender.input(120000, 1, False)
    if not input_text:
        sender.reply("操作超时")
        return
    if input_text.lower() == 'q':
        sender.reply("已取消")
        return

    lines = [line.strip() for line in input_text.strip().split('\n') if line.strip()]
    account_list = []
    for line in lines:
        if '#' in line:
            parts = line.split('#')
            if len(parts) == 2 and len(parts[0]) > 5 and len(parts[1]) >= 7:
                account_list.append({'wid': parts[0].strip(), 'phone': parts[1].strip()})

    if not account_list:
        sender.reply("未检测到有效账号，格式应为 wid#phone")
        return

    sender.reply(f"正在登录 {len(account_list)} 个账号...")

    success_count = 0
    fail_count = 0
    success_accounts = []

    for idx, acc in enumerate(account_list):
        if idx > 0:
            time.sleep(2)
        wid = acc['wid']
        phone = acc['phone']
        try:
            success, token, result = qh_login(wid, phone)
            if not success:
                sender.reply(f"{mask_account(wid)} 登录失败: {result}")
                fail_count += 1
                continue

            current_value = sg.bucketGet('s_qh_user', userid)
            if not current_value:
                sg.bucketSet('s_qh_user', userid, str([wid]))
            else:
                accounts = _sg_literal(current_value)
                if wid not in accounts:
                    accounts.append(wid)
                    sg.bucketSet('s_qh_user', userid, str(accounts))

            account_info = {"wid": wid, "phone": phone}
            sg.bucketSet('s_qh_token', wid, json.dumps(account_info))

            success_count += 1
            success_accounts.append({'wid': wid, 'phone': phone, 'info': account_info})
            sender.reply(f"{mask_account(wid)} 登录成功")

        except Exception as e:
            sender.reply(f"{mask_account(wid)} 异常: {str(e)}")
            fail_count += 1

    sender.reply(
        f"=====登录完成=====\n"
        f"成功: {success_count}个\n"
        f"失败: {fail_count}个\n"
        f"=================="
    )

    if success_accounts:
        dqsj = datetime.now().strftime("%Y-%m-%d")
        need_auth = []
        for acc in success_accounts:
            wid = acc['wid']
            accountVip = '2099-12-31'
            if accountVip and accountVip > dqsj:
                sender.reply(f"{mask_account(wid)} 已授权，到期: {accountVip}")
                update_ql_env(wid, acc['info'])
            else:
                need_auth.append(acc)

        if need_auth:
            sender.reply(f"\n{len(need_auth)} 个账号需要授权")
            authorize_accounts([acc['wid'] for acc in need_auth])


def query_accounts():
    """Query account info"""
    if not uservalue:
        sender.reply("=====未绑定账号=====\n❌ 未找到账号\n💡 发送 茄皇登录 绑定\n==================")
        return

    accounts = _sg_literal(uservalue)
    account_list = "\n========选择账号=======\n[0] 全部账号"
    for i, wid in enumerate(accounts, 1):
        auth_time = '2099-12-31'
        if not auth_time:
            auth_status = '未授权'
        elif auth_time < str(datetime.now().date()):
            auth_status = '已过期'
        else:
            auth_status = f'到期:{auth_time}'
        account_list += f"\n[{i}]{mask_account(wid)}({auth_status})"
    account_list += "\n=====================\n支持多选，用逗号分隔\n回复\"q\"退出\n====================="
    sender.reply(account_list)

    choice = sender.input(120000, 1, False)
    if not choice or choice.lower() == 'q':
        sender.reply("✅ 已退出")
        return

    try:
        if choice == '0':
            selected = accounts.copy()
        else:
            selected = [
                accounts[int(idx.strip()) - 1]
                for idx in choice.split(',')
                if idx.strip().isdigit() and 0 <= int(idx.strip()) - 1 < len(accounts)
            ]

        if not selected:
            sender.reply("❌ 未选择有效账号")
            return

        sender.reply(f"✅ 已选择 {len(selected)} 个账号，正在查询...")
        for i, wid in enumerate(selected, 1):
            if i > 1:
                time.sleep(2)
            try:
                auth_time = '2099-12-31'
                auth_status = '已授权' if auth_time and auth_time >= str(datetime.now().date()) else '未授权'

                user_info_text = ""
                account_info_str = sg.bucketGet('s_qh_token', wid)
                if account_info_str:
                    try:
                        account_info = json.loads(account_info_str)
                        phone = account_info.get('phone', '')
                        if phone:
                            login_success, token, user_data = qh_login(wid, phone)
                            if login_success and isinstance(user_data, dict):
                                user_info_text = (
                                    f"\n💧 水滴: {user_data.get('water_num', 0)}"
                                    f"\n☀️ 阳光: {user_data.get('sun_num', 0)}"
                                    f"\n🌱 种子: {user_data.get('seed_num', 0)}"
                                    f"\n🍎 果实: {user_data.get('fruit_num', 0)}"
                                )
                    except:
                        pass

                sender.reply(
                    f"=====账号信息[{i}/{len(selected)}]=====\n"
                    f"📱 账号: {mask_account(wid)}\n"
                    f"🏷 状态: {auth_status}\n"
                    f"📅 到期: {auth_time or '未授权'}{user_info_text}\n"
                    f"=================="
                )
            except Exception as e:
                sender.reply(f"=====查询失败=====\n❌ 错误: {str(e)}\n==================")

        sender.reply("✅ 查询完成")
    except Exception as e:
        sender.reply(f"❌ 查询失败: {str(e)}")


def manage_account():
    """Manage accounts - authorize/delete/submit to panel"""
    if not uservalue:
        sender.reply("=====未绑定账号=====\n❌ 未找到账号\n==================")
        return

    accounts = _sg_literal(uservalue)
    sender.reply(
        "=====账号管理=====\n"
        "[1] 授权账号\n"
        "[2] 删除账号\n"
        "[3] 提交青龙\n"
        "------------------\n"
        "回复数字选择\n"
        "回复\"q\"退出\n"
        "=================="
    )
    choice = sender.input(120000, 1, False)
    if not choice or choice.lower() == 'q':
        sender.reply("✅ 已退出")
        return

    account_list = "\n========选择账号=======\n[0] 全部账号"
    for i, wid in enumerate(accounts, 1):
        auth_time = '2099-12-31'
        if not auth_time:
            auth_status = '未授权'
        elif auth_time < str(datetime.now().date()):
            auth_status = '已过期'
        else:
            auth_status = f'到期:{auth_time}'
        account_list += f"\n[{i}]{mask_account(wid)}({auth_status})"
    account_list += "\n=====================\n支持多选，用逗号分隔\n回复\"q\"退出\n====================="
    sender.reply(account_list)

    account_choice = sender.input(120000, 1, False)
    if not account_choice or account_choice.lower() == 'q':
        sender.reply("✅ 已退出")
        return

    if account_choice == '0':
        selected = accounts.copy()
    else:
        selected = [
            accounts[int(idx.strip()) - 1]
            for idx in account_choice.split(',')
            if idx.strip().isdigit() and 0 <= int(idx.strip()) - 1 < len(accounts)
        ]

    if not selected:
        sender.reply("❌ 未选择有效账号")
        return

    sender.reply(f"✅ 已选择 {len(selected)} 个账号")

    if choice == '1':
        authorize_accounts(selected)
    elif choice == '2':
        sender.reply("=====确认删除=====\n⚠️ 此操作不可恢复\n回复 y 确认删除\n==================")
        confirm = sender.input(120000, 1, False)
        if confirm and confirm.lower() == 'y':
            for wid in selected:
                if wid in accounts:
                    accounts.remove(wid)
                sg.bucketDel('s_qh_token', wid)
                True
                delete_ql_env(wid)

            if accounts:
                sg.bucketSet('s_qh_user', userid, str(accounts))
            else:
                sg.bucketDel('s_qh_user', userid)
            sender.reply(f"✅ 已删除 {len(selected)} 个账号")
        else:
            sender.reply("✅ 已取消")
    elif choice == '3':
        success = 0
        for wid in selected:
            try:
                account_info = json.loads(sg.bucketGet('s_qh_token', wid))
                auth_time = '2099-12-31'
                if auth_time and auth_time >= str(datetime.now().date()):
                    if update_ql_env(wid, account_info):
                        success += 1
            except:
                pass
        sender.reply(
            f"=====提交结果=====\n"
            f"✅ 成功: {success}个\n"
            f"❌ 失败: {len(selected) - success}个\n"
            f"=================="
        )


def authorize_accounts(wids):
    return True


def _process_qrcode_payment(project, months, money):
    return True


def _process_mapay_payment(project, months, money, pay_type='alipay'):
    return True


def ks_auth():
    return True


def show_tutorial():
    """Show usage tutorial"""
    sender.reply(
        "=====茄皇教程=====\n"
        "用户指令:\n"
        "• 茄皇登录 - 批量绑定茄皇账号\n"
        "• 茄皇查询 - 查询账号状态和资源信息\n"
        "• 茄皇管理 - 授权/删除/提交青龙\n"
        "• 茄皇教程 - 查看本教程\n"
        "------------------\n"
        "管理员指令:\n"
        "• 茄皇授权 - 管理员按天数授权\n"
        "• 茄皇检测 - 检测过期账号并清理\n"
        "------------------\n"
        "登录格式:\n"
        "wid#phone（每行一个账号）\n"
        "例如: 11287477859#18150271020\n"
        "------------------\n"
        "wid获取方式:\n"
        "入口：小程序\"统一梦时代\"\n"
        "个人中心授权后点头像，复制\"客户编号\"\n"
        "------------------\n"
        "功能说明:\n"
        "• 账号绑定: 保存wid和phone到系统\n"
        "• 状态查询: 查看水滴/阳光/种子/果实等\n"
        "• 授权管理: 付费使用插件功能\n"
        "• 青龙提交: 自动提交到青龙容器\n"
        "• 过期检测: 自动清理过期账号\n"
        "------------------\n"
        "使用流程:\n"
        "1. 发送\"茄皇登录\"绑定账号\n"
        "2. 发送\"茄皇查询\"查看账号状态\n"
        "3. 发送\"茄皇管理\"选择授权账号\n"
        "4. 选择授权时长并完成支付\n"
        "5. 系统自动提交到青龙容器\n"
        "6. 等待定时任务自动执行签到\n"
        "=================="
    )


def main():
    """Main entry point"""
    msg = sender.getMessage()

    if '登录' in msg or '登陆' in msg:
        bind_account()
    elif '查询' in msg and ('茄皇' in msg or 'qh' in msg.lower()):
        query_accounts()
    elif '管理' in msg and ('茄皇' in msg or 'qh' in msg.lower()):
        manage_account()
    elif '教程' in msg and ('茄皇' in msg or 'qh' in msg.lower()):
        show_tutorial()
    elif '茄皇授权' in msg:
        ks_auth()
    elif '茄皇检测' in msg:
        if not sender.isAdmin():
            sender.reply("❌ 仅限管理员")
            return
        sender.reply("🔍 正在检测...")
        result = check_auth_status(
            's_qh', 's_qh_user', 's_qh_auth', 's_qh_token',
            '茄皇的家', delete_ql_callback=delete_ql_env
        )
        sender.reply(result)
    elif sender.getImtype() == 'fake':
        try:
            result = check_auth_status(
                's_qh', 's_qh_user', 's_qh_auth', 's_qh_token',
                '茄皇的家', delete_ql_callback=delete_ql_env
            )
            sg.notifyMasters(result)
        except:
            pass
    else:
        sender.setContinue()


if __name__ == "__main__":
    main()
