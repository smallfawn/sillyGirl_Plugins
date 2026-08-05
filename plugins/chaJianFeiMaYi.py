# [title: 【插件】-飞蚂蚁]
# [name: chaJianFeiMaYi]
# [language: python]
# [class: 任务]
# [author: huawei]
# [version: v1.1]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^蚂蚁登录$|^蚂蚁绑定$|^蚂蚁管理$|^蚂蚁查询$|^蚂蚁$|^蚂蚁教程$|^蚂蚁积分$|^蚂蚁一键运行$]
# [icon: https://api.iconify.design/lucide:apple.svg]
# [description: 飞蚂蚁APP插件；指令：；蚂蚁登录：绑定账号；蚂蚁查询：查询状态；蚂蚁教程：使用指南；蚂蚁一键运行：执行任务]
# [depe: ["requests"]]


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
    'G_fmy_config_ql_config': form.string().title('青龙配置').default(''),
    'G_fmy_config_ql_envname': form.string().title('变量名称').default('G_fmy'),
    'G_fmy_config_ql_var_name': form.string().title('飞蚂蚁变量名称').default('G_fmy'),
})
_CONFIG_FIELD_MAP = {
    ('G_fmy_config', 'ql_config'): 'G_fmy_config_ql_config',
    ('G_fmy_config', 'ql_envname'): 'G_fmy_config_ql_envname',
    ('G_fmy_config', 'ql_var_name'): 'G_fmy_config_ql_var_name',
}

import requests
import json
import time
from datetime import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def get_config():
    """获取配置信息"""
    try:
        config = {
            'ql_config': sg.bucketGet('G_fmy_config', 'ql_config') or '',
            'ql_envname': sg.bucketGet('G_fmy_config', 'ql_envname') or 'G_fmy',
            'ql_var_name': sg.bucketGet('G_fmy_config', 'ql_var_name') or 'G_fmy',
            'price': float(sg.bucketGet('G_fmy_config', 'price') or '0.88'),
            'zsm': sg.bucketGet('G_fmy_config', 'zsm') or '',
            'points_per_month': int(sg.bucketGet('G_fmy_config', 'points_per_month') or '100')
        }
        return config
    except Exception as e:
        print(f"配置获取失败: {str(e)}")
        return {
            'ql_config': '',
            'ql_envname': 'G_fmy',
            'ql_var_name': 'G_fmy',
            'price': 0.88,
            'zsm': '',
            'points_per_month': 100
        }

def get_user_points(user_id=None):
    return 0

def set_user_points(user_id, points):
    """设置用户积分"""
    sg.bucketSet('dd_sign_coin', user_id, str(points['dd_sign_coin']))
    sg.bucketSet('dd_sign_points', user_id, str(points['dd_sign_points']))
    sign_key = f"sign_{user_id}"
    sg.bucketSet('dd_sign_coin', sign_key, str(points['dd_sign_coin']))
    return True

def get_user_accounts(user_id=None):
    """获取用户账号列表"""
    if user_id is None:
        user_id = sg.getSenderID()

    print(f"获取用户账号，用户ID: {user_id}")
    uservalue = sg.bucketGet('G_fmy_user', user_id) or '[]'
    try:
        accounts = json.loads(uservalue)
        print(f"获取到的账号列表: {accounts}")
        return accounts
    except Exception as e:
        print(f"解析账号列表失败: {str(e)}")
        return []

def verify_token(token):
    """验证token"""
    headers = {
        "host": "openapp.fmy90.com",
        "device-model": "microsoft",
        "device-version": "Windows 10 x64",
        "xweb_xhr": "1",
        "authorization": f"bearer {token}",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c33)XWEB/13839",
        "content-type": "application/json;charset=utf8",
        "accept": "*/*",
        "sec-fetch-site": "cross-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://servicewechat.com/wx501990400906c9ff/450/page-frame.html",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9"
    }

    params = {
        "type": "1",
        "version": "V2.00.01",
        "platformKey": "F2EE24892FBF66F0AFF8C0EB532A9394",
        "mini_scene": "1256",
        "partner_ext_infos": ""
    }

    try:
        beans_url = "https://openapp.fmy90.com/user/new/beans/info"
        beans_response = requests.get(beans_url, headers=headers, params=params, timeout=10)
        beans_data = beans_response.json()

        if beans_data.get("code") == 200:
            total_beans = beans_data.get("data", {}).get("totalCount", "0")

            info_url = "https://openapp.fmy90.com/user/info"
            info_response = requests.get(info_url, headers=headers, params=params, timeout=10)
            info_data = info_response.json()

            if info_data.get("code") == 200 and info_data.get("data"):
                user = info_data.get("data", {}).get("user", {})
                return True, {
                    "phone": user.get("mobile", ""),
                    "username": user.get("userName", "未知用户"),
                    "beans": str(total_beans)
                }
            else:
                return True, {
                    "phone": "",
                    "username": "未知用户",
                    "beans": str(total_beans)
                }

        try:
            import base64
            import json

            token_parts = token.split('.')
            if len(token_parts) >= 2:
                payload = token_parts[1]
                padding = '=' * (4 - len(payload) % 4) if len(payload) % 4 != 0 else ''
                decoded = base64.b64decode(payload + padding).decode('utf-8')
                jwt_data = json.loads(decoded)

                uid = jwt_data.get('uid', '')

                if uid:
                    return True, {
                        "phone": str(uid),
                        "username": "JWT用户",
                        "beans": "0"
                    }
        except Exception as jwt_error:
            print(f"JWT解析失败: {str(jwt_error)}")

        return False, None
    except Exception as e:
        print(f"验证失败: {str(e)}")
        return False, None

def update_qinglong_env(token, account_info):
    """更新青龙面板环境变量"""
    print("青龙面板上传已禁用，仅保存在数据桶中")
    return True

def is_admin():
    """检查当前用户是否为管理员"""
    sender_id = sg.getSenderID()
    sender = sg.Sender(sender_id)
    if sender.isAdmin():
        return True

    admin_list = sg.bucketGet('G_fmy_config', 'admin_list') or ''
    admin_list = admin_list.split(',')
    return sender_id in admin_list or sender_id == '1603960061'  # 默认作者ID为管理员

def 蚂蚁授权():
    """管理员授权操作"""
    sender = sg.Sender(sg.getSenderID())

    if not is_admin():
        sender.reply("❌ 您没有管理员权限！")
        return

    sender.reply("""
=====管理员授权操作=====
[1] 指定用户授权
[2] 批量授权所有用户
------------------
请回复对应数字：""")

    choice = sender.input(60000, 1, False)

    if choice == '1':
        sender.reply("请输入用户微信ID:")
        target_userid = sender.input(60000, 1, False)

        accounts = get_user_accounts(target_userid)
        if not accounts:
            sender.reply(f"❌ 未找到用户 {target_userid} 的账号")
            return

        account_list = []
        for i, account_id in enumerate(accounts, 1):
            account_data = sg.bucketGet('G_fmy_accounts', account_id)
            if account_data:
                account_info = json.loads(account_data)
                remark = account_info['phone']  # 备注存储在phone字段
                auth_status = account_info['auth_status']
                status = "已授权" if auth_status['is_authorized'] else "未授权"
                expire_time = auth_status['expire_time'] or "无"
                account_list.append(f"[{i}] 备注: {remark} \n 状态: {status} \n 到期时间: {expire_time}")
            else:
                account_list.append(f"[{i}] 数据异常")

        account_list_str = "\n".join(account_list)
        sender.reply(f"""
=====用户账号列表=====
用户ID: {target_userid}
{account_list_str}
------------------
[0] 授权所有账号
或回复序号选择单个账号
===================""")

        choice = sender.input(60000, 1, False)
        if not choice.isdigit():
            sender.reply("❌ 输入无效")
            return

        sender.reply("请输入授权月数 (1-12):")
        months = sender.input(60000, 1, False)
        if not months.isdigit() or int(months) < 1 or int(months) > 12:
            sender.reply("❌ 月数必须为1-12之间的整数")
            return

        months = int(months)
        success_count = 0

        if choice == '0':
            for account_id in accounts:
                if admin_authorize_account(account_id, months, target_userid):
                    success_count += 1

            sender.reply(f"✅ 批量授权完成！成功授权 {success_count}/{len(accounts)} 个账号")
        else:
            idx = int(choice) - 1
            if idx < 0 or idx >= len(accounts):
                sender.reply("❌ 序号无效")
                return

            if admin_authorize_account(accounts[idx], months, target_userid):
                sender.reply("✅ 授权成功！")
            else:
                sender.reply("❌ 授权失败！")

    elif choice == '2':
        sender.reply("请输入授权月数 (1-12):")
        months = sender.input(60000, 1, False)
        if not months.isdigit() or int(months) < 1 or int(months) > 12:
            sender.reply("❌ 月数必须为1-12之间的整数")
            return

        months = int(months)
        success_count = 0
        total_count = 0

        users = sg.bucketAllKeys('G_fmy_user')
        if not users:
            sender.reply("❌ 未找到任何用户")
            return

        for user_id in users:
            accounts = get_user_accounts(user_id)
            for account_id in accounts:
                total_count += 1
                if admin_authorize_account(account_id, months, user_id):
                    success_count += 1

        sender.reply(f"✅ 批量授权完成！成功授权 {success_count}/{total_count} 个账号")

    elif choice == '3':
        show_config()
    elif choice == '4':
        set_config()
    elif choice == '5':
        add_admin()
    else:
        sender.reply("❌ 无效选择")

def set_config():
    sender.reply("该管理项已取消，请在插件配置中修改参数")


def add_admin():
    sender.reply("管理员权限沿用傻妞后台管理员配置")

def admin_authorize_account(account_id, months, user_id):
    return True
def delete_account(account_id):
    """删除账号"""
    sender = sg.Sender(sg.getSenderID())

    account_data = sg.bucketGet('G_fmy_accounts', account_id)
    if not account_data:
        sender.reply("❌ 账号数据无效")
        return

    account_info = json.loads(account_data)
    remark = account_info['phone']  # 备注存储在phone字段

    sender.reply(f"""
=====删除账号确认=====
确认删除账号 {remark} 吗？
请回复 [Y] 确认
回复 [N] 取消
==================""")

    confirm = sender.input(60000, 1, False).strip().lower()
    if confirm != 'y':
        sender.reply("✅ 已取消删除")
        return

    try:
        sg.bucketDel('G_fmy_accounts', account_id)

        user_id = sender.getUserID()
        accounts = get_user_accounts(user_id)
        if account_id in accounts:
            accounts.remove(account_id)
            if accounts:
                sg.bucketSet('G_fmy_user', user_id, json.dumps(accounts))
            else:
                sg.bucketDel('G_fmy_user', user_id)

        sender.reply(f"""
✅ 账号删除成功
📝 备注：{remark}
===================""")
    except Exception as e:
        sender.reply(f"❌ 删除失败: {str(e)}")

def 蚂蚁管理():
    """飞蚂蚁账号管理"""
    sender = sg.Sender(sg.getSenderID())
    userid = sender.getUserID()
    accounts = get_user_accounts(userid)

    print(f"用户ID: {userid}")
    print(f"账号列表: {accounts}")

    if not accounts:
        sender.reply("❌ 您尚未绑定任何账号，请先发送「蚂蚁登录」进行绑定")
        return

    account_list = []
    valid_accounts = []
    for i, account_id in enumerate(accounts, 1):
        account_data = sg.bucketGet('G_fmy_accounts', account_id)
        if account_data:
            account_info = json.loads(account_data)
            remark = account_info['phone']  # 备注存储在phone字段
            auth_status = account_info['auth_status']

            if auth_status['is_authorized']:
                status = f"✅ 已授权（到期: {auth_status['expire_time']}）"
            else:
                status = "❌ 未授权"

            account_list.append(f"[{len(valid_accounts) + 1}] {remark} {status}")
            valid_accounts.append(account_id)
        else:
            accounts.remove(account_id)
            sg.bucketSet('G_fmy_user', userid, json.dumps(accounts))

    account_list_str = "\n".join(account_list)

    sender.reply(f"""
=====飞蚂蚁账号管理=====
🔢 绑定账号: {len(valid_accounts)}个
-------------------------
{account_list_str}
------------------
回复序号选择操作（q退出）
===================""")

    choice = sender.input(60000, 1, False)
    if choice.lower() == 'q':
        return

    if not choice.isdigit():
        sender.reply("❌ 输入无效")
        return

    idx = int(choice) - 1
    if idx < 0 or idx >= len(valid_accounts):
        sender.reply("❌ 序号无效")
        return

    selected_account = valid_accounts[idx]
    account_data = sg.bucketGet('G_fmy_accounts', selected_account)
    if not account_data:
        sender.reply("❌ 账号数据无效")
        return

    account_info = json.loads(account_data)
    remark = account_info['phone']  # 备注存储在phone字段

    sender.reply(f"""
已选择账号: {remark}
[1] 授权账号
[2] 更新数据
[3] 删除账号
------------------
请回复对应数字：""")

    op = sender.input(60000, 1, False)

    if op == '1':
        authorize_account(selected_account)
    elif op == '2':
        update_account_data(selected_account)
    elif op == '3':
        delete_account(selected_account)
    else:
        sender.reply("❌ 无效选择")

def authorize_account(account_id):
    return True

def show_account_info(account_id):
    """显示账号详细信息"""
    sender = sg.Sender(sg.getSenderID())
    account_data = sg.bucketGet('G_fmy_accounts', account_id)
    if not account_data:
        sender.reply("❌ 账号数据无效")
        return

    account_info = json.loads(account_data)
    success, user_info = verify_token(account_info['token'])

    beans_info = "获取失败"
    if success:
        beans_info = user_info['beans']

    sender.reply(f"""
=====账号信息=====
📝 备注：{account_info['phone']}
💰 豆子数量：{beans_info}
👤 微信ID：{account_info['wx_id']}
🕒 绑定时间：{account_info['bind_time']}
🔑 授权状态：{'已授权' if account_info['auth_status']['is_authorized'] else '未授权'}
⏰ 到期时间：{account_info['auth_status']['expire_time'] or '未授权'}
===================""")

def 蚂蚁教程():
    """飞蚂蚁使用教程"""
    sender = sg.Sender(sg.getSenderID())
    config = get_config()

    tutorial = f"""
=====飞蚂蚁使用教程=====

【功能介绍】
飞蚂蚁是一款步数兑换平台，可以将步数兑换为豆子，再用豆子兑换各种奖励。

【指令列表】
1. 蚂蚁登录 - 绑定飞蚂蚁账号
2. 蚂蚁管理 - 管理已绑定账号
3. 蚂蚁查询 - 查询账号状态
4. 蚂蚁授权 - 管理员授权操作
5. 蚂蚁教程 - 显示本教程
6. 蚂蚁积分 - 查询积分

【获取Token教程】
1. 打开微信小程序"飞蚂蚁"
2. 登录您的账号
3. 使用抓包工具获取请求头中的authorization值
4. 复制完整的token（bearer后面的部分）
5. 登录时输入格式：token#备注名称
   例如：eyJ0eXA...#张三的账号

【授权说明】
- 每月授权需要{config['points_per_month']}积分
- 授权后可同步至青龙面板
- 授权有效期按月计算

【积分获取】
- 可通过付款获取积分
- 当前汇率：¥{config['price']:.2f} = {config['points_per_month']}积分

【
如有问题，请检查配置
=================="""

    sender.reply(tutorial)

def 蚂蚁查询():
    """查询账号状态"""
    sender = sg.Sender(sg.getSenderID())
    userid = sender.getUserID()
    accounts = get_user_accounts(userid)

    if not accounts:
        sender.reply("❌ 您尚未绑定任何账号，请先发送「蚂蚁登录」进行绑定")
        return

    status_list = []
    for i, account_id in enumerate(accounts, 1):
        account_data = sg.bucketGet('G_fmy_accounts', account_id)
        if account_data:
            account_info = json.loads(account_data)
            remark = account_info['phone']  # 备注存储在phone字段

            success, user_info = verify_token(account_info['token'])

            if success:
                beans = user_info['beans']
                auth_status = "✅ 已授权" if account_info['auth_status']['is_authorized'] else "❌ 未授权"
                expire_time = account_info['auth_status']['expire_time'] or "未授权"

                status_list.append(f"账号{i}: {remark}\n豆子: {beans}\n状态: {auth_status}\n到期: {expire_time}\n")
            else:
                status_list.append(f"账号{i}: {remark}\n状态: ❌ Token已失效\n")
        else:
            status_list.append(f"账号{i}: 数据异常\n")

    status_str = "\n".join(status_list)

    sender.reply(f"""
=====账号状态查询=====
{status_str}
发送「蚂蚁管理」可管理账号
===================""")

def parse_payment_result(raw_data):
    return True

def point_payment_flow(account_id, months, required_points, remark):
    return True

def wechat_payment_flow(account_id, months, amount, config, remark):
    return True

def query_user_points():
    """查询用户积分"""
    sender = sg.Sender(sg.getSenderID())
    points = get_user_points(sender.getUserID())
    config = get_config()

    sender.reply(
        f"📊 您的当前积分: {points['total']}\n"
        f"💰 每账号每月积分: {config['points_per_month']}\n"
        f"检查配置可充值积分"
    )

def show_config():
    """查看配置"""
    sender = sg.Sender(sg.getSenderID())
    config = get_config()
    admin_list = sg.bucketGet('G_fmy_config', 'admin_list') or '无'

    ql_config = config['ql_config']
    if ql_config and '丨' in ql_config:
        parts = ql_config.split('丨')
        if len(parts) >= 3:
            masked_config = f"{parts[0]}丨{'*' * 8}丨{'*' * 8}"
        else:
            masked_config = "格式错误"
    else:
        masked_config = "未设置"

    sender.reply(f"""
=====当前配置=====
青龙面板配置：{masked_config}
环境变量名称：{config['ql_envname']}
飞蚂蚁变量名称：{config['ql_var_name']}
积分单价：{config['price']}
二维码：{'已设置' if config['zsm'] else '未设置'}
每月所需积分：{config['points_per_month']}
管理员列表：{admin_list}
===================""")

def update_account_data(account_id):
    """更新账号数据"""
    sender = sg.Sender(sg.getSenderID())

    account_data = sg.bucketGet('G_fmy_accounts', account_id)
    if not account_data:
        sender.reply("❌ 账号数据无效")
        return

    account_info = json.loads(account_data)
    remark = account_info['phone']  # 备注存储在phone字段

    auth_status = account_info['auth_status']
    if not auth_status['is_authorized']:
        sender.reply(f"""
⚠️ 此账号未授权
请先使用「授权账号」功能进行授权
===================""")
        return

    is_expired = False
    try:
        expire_time = datetime.strptime(auth_status['expire_time'], "%Y-%m-%d %H:%M:%S")
        if expire_time < datetime.now():
            is_expired = True
    except:
        is_expired = True

    if is_expired:
        sender.reply(f"""
⚠️ 此账号授权已过期
授权到期时间: {auth_status['expire_time']}
请先使用「授权账号」功能续费
===================""")
        return

    sender.reply(f"""
=====更新账号数据=====
账号备注: {remark}
授权到期: {auth_status['expire_time']}
------------------
请输入新的token：""")

    new_token = sender.input(120000, 1, False).strip()
    if not new_token:
        sender.reply("❌ 输入为空，已取消更新")
        return

    success, user_info = verify_token(new_token)
    if not success:
        sender.reply("❌ 无效的token，验证失败")
        return

    if user_info and user_info.get('phone'):
        account_info['phone'] = user_info['phone']

    account_info['token'] = new_token

    sg.bucketSet('G_fmy_accounts', account_id, json.dumps(account_info))

    if update_qinglong_env(new_token, account_info):
        sender.reply(f"""
✅ 数据更新成功！
📝 备注: {account_info['phone']}
📅 授权到期: {auth_status['expire_time']}
🤖 已保存在数据桶中
===================""")
    else:
        sender.reply(f"""
✅ 数据更新成功！
📝 备注: {account_info['phone']}
📅 授权到期: {auth_status['expire_time']}
❗ 数据保存失败
===================""")

def 蚂蚁登录():
    """飞蚂蚁账号登录绑定"""
    sender = sg.Sender(sg.getSenderID())
    user_id = sender.getUserID()

    sender.reply(f"""
=====飞蚂蚁登录=====
请输入token：
------------------
(输入q取消操作)
===================""")

    token_input = sender.input(120000, 1, False)
    if token_input.lower() == 'q':
        sender.reply("✅ 已取消登录")
        return

    token = token_input.strip()
    if not token:
        sender.reply("❌ 输入为空，登录失败")
        return

    success, user_info = verify_token(token)
    if not success:
        sender.reply("❌ 无效的token，验证失败")
        return

    phone = user_info.get('phone', '')
    username = user_info.get('username', '未知用户')
    beans = user_info.get('beans', '0')

    if not phone:
        sender.reply("请输入备注名称：")
        remark = sender.input(60000, 1, False).strip()
        if not remark:
            remark = "未命名账号"
    else:
        remark = phone

    account_id = f"fmy_{int(time.time())}_{user_id[-6:]}"

    accounts = get_user_accounts(user_id)

    account_info = {
        "token": token,
        "phone": remark,
        "username": username,
        "beans": beans,
        "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "wx_id": user_id,
        "auth_status": {
            "is_authorized": False,
            "expire_time": None,
            "last_auth_time": None
        }
    }

    sg.bucketSet('G_fmy_accounts', account_id, json.dumps(account_info))

    accounts.append(account_id)
    sg.bucketSet('G_fmy_user', user_id, json.dumps(accounts))

    sender.reply(f"""
✅ 绑定成功！
📝 备注: {remark}
💰 豆子: {beans}
------------------
🔹 发送「蚂蚁管理」可授权和管理账号
🔹 发送「蚂蚁查询」可查询账号状态
===================""")

def 蚂蚁一键运行():
    """执行任务"""
    sender = sg.Sender(sg.getSenderID())
    user_id = sender.getUserID()

    accounts = get_user_accounts(user_id)
    if not accounts:
        sender.reply("❌ 您尚未绑定任何账号，请先发送「蚂蚁登录」进行绑定")
        return

    sender.reply(f"⏳ 正在为{len(accounts)}个账号执行任务，请稍候...")

    results = []
    success_count = 0
    failed_count = 0

    for account_id in accounts:
        account_data = sg.bucketGet('G_fmy_accounts', account_id)
        if not account_data:
            failed_count += 1
            results.append("❌ 账号数据异常")
            continue

        account_info = json.loads(account_data)
        token = account_info["token"]
        remark = account_info["phone"]

        if not account_info['auth_status']['is_authorized']:
            results.append(f"⚠️ 账号[{remark}]未授权，跳过任务")
            failed_count += 1
            continue

        is_expired = False
        try:
            expire_time = datetime.strptime(account_info['auth_status']['expire_time'], "%Y-%m-%d %H:%M:%S")
            if expire_time < datetime.now():
                is_expired = True
        except:
            is_expired = True

        if is_expired:
            results.append(f"⚠️ 账号[{remark}]授权已过期，跳过任务")
            failed_count += 1
            continue

        result = execute_ant_tasks(token, remark)
        results.append(f"📱 账号[{remark}]:" + result)

        if "任务执行异常" in result or "登录状态异常" in result or "登录验证失败" in result:
            failed_count += 1
        else:
            success_count += 1

    result_text = "\n\n".join(results)
    sender.reply(f"""
=====飞蚂蚁任务执行结果=====
✅ 成功: {success_count}个账号
❌ 失败: {failed_count}个账号
------------------
{result_text}
===================""")

def execute_ant_tasks(token, remark):
    """执行单个账号的任务"""
    if not token.lower().startswith("bearer "):
        token = f"bearer {token}"

    session = requests.Session()
    session.verify = False  # 禁用SSL验证

    headers = {
        "Host": "openapp.fmy90.com",
        "Connection": "keep-alive",
        "device-model": "microsoft",
        "device-version": "Windows 10 x64",
        "xweb_xhr": "1",
        "authorization": token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c33)XWEB/13839",
        "content-type": "application/json;charset=UTF-8",
        "Accept": "*/*",
        "sec-fetch-site": "cross-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "Referer": "https://servicewechat.com/wx501990400906c9ff/450/page-frame.html",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }

    base_payload = {
        "version": "V2.00.01",
        "platformKey": "F2EE24892FBF66F0AFF8C0EB532A9394",
        "mini_scene": 1256,
        "partner_ext_infos": ""
    }

    params = {
        "type": "1",
        "version": "V2.00.01",
        "platformKey": "F2EE24892FBF66F0AFF8C0EB532A9394",
        "mini_scene": "1256",
        "partner_ext_infos": ""
    }

    results = []
    max_retries = 3
    beans_before = "0"

    try:
        retry_count = 0
        while retry_count < max_retries:
            try:
                beans_url = "https://openapp.fmy90.com/user/new/beans/info"
                beans_response = session.get(beans_url, headers=headers, params=params, timeout=15)
                beans_data = beans_response.json()

                if beans_data.get("code") == 200:
                    beans_before = beans_data.get("data", {}).get("totalCount", "0")
                    results.append(f"💰 账户豆子: {beans_before}")
                    break
                else:
                    retry_count += 1
                    if retry_count >= max_retries:
                        return f"❌ 登录状态异常: {beans_data.get('message', '未知错误')}"
                    time.sleep(2)
            except Exception as e:
                retry_count += 1
                if retry_count >= max_retries:
                    return f"❌ 登录验证失败: {str(e)[:50]}"
                time.sleep(2)

        try:
            bet_url = "https://openapp.fmy90.com/active/pool/bet"
            bet_payload = base_payload.copy()
            body_str = json.dumps(bet_payload, separators=(',', ':'))

            headers["Content-Length"] = str(len(body_str))
            bet_response = session.post(bet_url, headers=headers, data=body_str, timeout=15)
            bet_data = bet_response.json()

            if bet_data.get("code") == 200 or "已投" in bet_data.get('message', ''):
                bet_status = "✅ 成功"
            else:
                bet_status = f"❌ 失败 ({bet_data.get('code')})"

            bet_msg = bet_data.get('message', '无返回信息')
            results.append(f"🎲 投注功能: {bet_status}\n结果: {bet_msg}")
        except Exception as e:
            results.append(f"🎲 投注功能: ❌ 异常\n结果: {str(e)[:30]}")

        time.sleep(1)

        try:
            sign_url = "https://openapp.fmy90.com/sign/new/do"
            sign_payload = base_payload.copy()
            body_str = json.dumps(sign_payload, separators=(',', ':'))

            headers["Content-Length"] = str(len(body_str))
            sign_response = session.post(sign_url, headers=headers, data=body_str, timeout=15)
            sign_data = sign_response.json()

            if sign_data.get("code") == 200 or "已" in sign_data.get('message', '') and "签到" in sign_data.get('message', ''):
                sign_status = "✅ 成功"
            else:
                sign_status = f"❌ 失败 ({sign_data.get('code')})"

            sign_msg = sign_data.get('message', '无返回信息')
            data = sign_data.get('data', {})
            sign_red_amount = data.get('sign_red_amount', 0) if data else 0
            detail = f"获得红包: {sign_red_amount}" if sign_red_amount > 0 else ""
            results.append(f"📝 签到功能: {sign_status}\n结果: {sign_msg} {detail}")
        except Exception as e:
            results.append(f"📝 签到功能: ❌ 异常\n结果: {str(e)[:30]}")

        time.sleep(1)

        exchange_results = []
        for i in range(1, 4):
            try:
                exchange_url = "https://openapp.fmy90.com/step/exchange"
                exchange_payload = base_payload.copy()
                exchange_payload["steps"] = 20000
                exchange_payload["exchangeType"] = "bean"
                body_str = json.dumps(exchange_payload, separators=(',', ':'))

                headers["Content-Length"] = str(len(body_str))
                exchange_response = session.post(exchange_url, headers=headers, data=body_str, timeout=15)
                exchange_data = exchange_response.json()

                if exchange_data.get("code") == 200 or "最多兑换" in exchange_data.get('message', ''):
                    exchange_status = "✅ 成功"
                else:
                    exchange_status = f"❌ 失败 ({exchange_data.get('code')})"

                exchange_msg = exchange_data.get('message', '无返回信息')
                exchange_results.append(f"第{i}次: {exchange_status} - {exchange_msg}")

                if i < 3:
                    time.sleep(3)
            except Exception as e:
                exchange_results.append(f"第{i}次: ❌ 异常 - {str(e)[:30]}")

        results.append(f"👟 步数兑换:\n" + "\n".join(exchange_results))

        time.sleep(3)

        try:
            beans_url = "https://openapp.fmy90.com/user/new/beans/info"
            beans_response = session.get(beans_url, headers=headers, params=params, timeout=15)
            beans_data = beans_response.json()

            info_url = "https://openapp.fmy90.com/user/info"
            info_response = session.get(info_url, headers=headers, params=params, timeout=10)

            beans_after = beans_before
            if beans_data.get("code") == 200:
                beans_after = beans_data.get("data", {}).get("totalCount", beans_before)

            try:
                beans_gain = int(beans_after) - int(beans_before)
                gain_text = f"+{beans_gain}" if beans_gain > 0 else str(beans_gain)
            except:
                gain_text = "未知"

            results.append(f"💰 当前豆子: {beans_after} (变化: {gain_text})")
        except Exception as e:
            results.append(f"💰 当前豆子: {beans_before} (查询失败: {str(e)[:30]})")

        if len(results) > 0:
            return "\n\n" + "\n\n".join(results)
        else:
            return "❌ 任务执行失败: 未能完成任何任务"

    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()[:200]
        return f"❌ 任务执行异常: {str(e)[:50]}\n{error_msg}"

sender = sg.Sender(sg.getSenderID())
message = sender.getMessage().strip()
if message in ["蚂蚁登录", "蚂蚁绑定"]:
    蚂蚁登录()
elif message == "蚂蚁管理":
    蚂蚁管理()
elif message == "蚂蚁查询":
    蚂蚁查询()
elif message == "蚂蚁授权":
    蚂蚁授权()
elif message == "蚂蚁教程":
    蚂蚁教程()
elif message == "蚂蚁积分":
    query_user_points()
elif message == "蚂蚁一键运行":
    蚂蚁一键运行()
