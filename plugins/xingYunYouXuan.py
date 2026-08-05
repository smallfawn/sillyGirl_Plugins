# [title: 星韵优选]
# [name: xingYunYouXuan]
# [language: python]
# [class: 任务]
# [author: rujingxianghai]
# [version: v1.2.0]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(星韵|xingyun|xyyx)(登录|登陆)$|^登(录|陆)(星韵|xingyun|xyyx)$|^(星韵|xingyun|xyyx)(查询|管理|检测|教程|清理|上传)$|^(查询|管理)(星韵|xingyun|xyyx)$]
# [cron: 18 9 * * *]
# [icon: https://api.iconify.design/lucide:apple.svg]
# [description: 星韵优选小程序(日0.1)；活动入口：#小程序://星韵优选/kt8xm5WOSI0Z6ri；功能：打卡签到、视频任务]
# [depe: ["requests"]]


import asyncio as _sg_asyncio
import os as _sg_os
import time as _sg_time
import types as _sg_types
import json as _sg_json
import re as _sg_re
from threading import Thread as _sg_Thread
from sillygirl import Adapter as _SGAdapter, Bucket as _SGBucket, Sender as _SGSender, sender as _sg_sender, container as _sg_container, form
check_auth_status = lambda *args, **kwargs: "账号默认可用"
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
    's_xyyx_qlname': form.string().title('设置对接容器').default('').description('面板容器参数，不填则使用默认配置'),
    's_xyyx_use_daipanel': form.boolean().title('使用呆呆面板').default(False).description('勾选使用呆呆面板，不勾选使用青龙面板'),
    's_xyyx_panel_group': form.string().title('呆呆面板分组').default('').description('填写后新增/更新变量时同步写入 group 字段，留空则不处理'),
    's_xyyx_osname': form.string().title('青龙变量名').default('S_XYYX').description('青龙容器内的变量名'),
    's_xyyx_notify': form.string().title('通知渠道').default('').description('检测通知推送渠道'),
})
_CONFIG_FIELD_MAP = {
    ('s_xyyx', 'qlname'): 's_xyyx_qlname',
    ('s_xyyx', 'use_daipanel'): 's_xyyx_use_daipanel',
    ('s_xyyx', 'panel_group'): 's_xyyx_panel_group',
    ('s_xyyx', 'osname'): 's_xyyx_osname',
    ('s_xyyx', 'notify'): 's_xyyx_notify',
}

import os
import json
import time
import requests
from datetime import datetime

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()
uservalue = sg.bucketGet(bucket='s_xyyx_user', key=userid)

PLUGIN_CONFIG = {'bucket': 's_xyyx', 'coin_key': 'dd_sign_points', 'name': '星韵优选'}




def _get_ql_client():
    osname = sg.bucketGet('s_xyyx', 'osname') or 'S_XYYX'
    qlname = sg.bucketGet('s_xyyx', 'qlname') or ''
    use_dp = str(sg.bucketGet('s_xyyx', 'use_daipanel') or '').lower() == 'true'

    if use_dp:
        if qlname:
            return DumbPanelClient(osname, qlname)
        return DumbPanelClient(osname)
    else:
        if qlname:
            return QingLongClient(osname, qlname)
        return QingLongClient(osname)


def update_ql_env(account, account_info):
    env_value = account_info.get('token', '')
    if not env_value:
        return False
    auth_time = '2099-12-31' or '未授权'
    panel_group = (sg.bucketGet('s_xyyx', 'panel_group') or '').strip()
    ql = _get_ql_client()
    return ql.update_env(
        account,
        env_value,
        f"星韵优选:{mask_account(account)}|用户:{userid}|到期:{auth_time}",
        group=panel_group,
    )


def delete_ql_env(account):
    ql = _get_ql_client()
    return ql.delete_env(account)


def verify_token(session_token):
    try:
        headers = {
            "Host": "gzpengru.weimbo.com",
            "Connection": "keep-alive",
            "3rdsession": session_token,
            "content-type": "application/json",
            "User-Agent": "Mozilla/5.0 (Linux; Android 13; M2012K11AC Build/TKQ1.220829.002; wv) AppleWebKit/537.36 MicroMessenger/8.0.45.2400",
            "Referer": "https://servicewechat.com/wxc86c9aecdb67f876/9/page-frame.html"
        }

        payload = {"action": "userInfoData"}
        response = requests.post(
            "https://gzpengru.weimbo.com/api/index.php?ackey=GZYTAPPLET",
            headers=headers,
            json=payload,
            timeout=10
        )

        data = response.json()
        if data and data.get("Status"):
            user_data = data.get("Data", {})
            user_info = user_data.get("user", {})
            user_name = user_info.get("name", "未知")
            user_id_str = user_info.get("id", "")
            user_id = user_id_str.replace("ID：", "").replace("ID:", "").strip() if user_id_str else ""
            jifen = user_data.get("u_money", {}).get("jifen", 0)
            return True, {"name": user_name, "jifen": jifen, "user_id": user_id}
        else:
            return False, {"error": data.get("Message", "Token无效")}
    except Exception as e:
        return False, {"error": str(e)}


def bind_account():
    sender.reply(
        "=====星韵优选登录=====\n"
        "请输入3rdsession凭证\n"
        "------------------\n"
        "支持批量登录(换行分隔)\n"
        "回复\"q\"退出\n"
        "=================="
    )

    input_text = sender.input(120000, 1, False)
    if not input_text:
        sender.reply("⏰ 操作超时")
        return
    if input_text.lower() == 'q':
        sender.reply("✅ 已取消")
        return

    lines = [line.strip() for line in input_text.split('\n') if line.strip()]
    success_count = 0
    fail_count = 0
    results = []

    for line in lines:
        session_token = line.strip()
        if not session_token:
            continue

        is_valid, info = verify_token(session_token)

        if is_valid:
            account_id = info.get('user_id', '')
            if not account_id:
                results.append("❌ 获取用户ID失败")
                fail_count += 1
                continue

            current_uservalue = sg.bucketGet(bucket='s_xyyx_user', key=userid)
            user_accounts = []
            if current_uservalue:
                try:
                    user_accounts = _sg_literal(current_uservalue)
                except:
                    user_accounts = []

            if account_id not in user_accounts:
                user_accounts.append(account_id)

            sg.bucketSet('s_xyyx_user', userid, str(user_accounts))

            token_info = {
                'token': session_token,
                'user_id': account_id,
                'name': info.get('name', '未知'),
                'jifen': info.get('jifen', 0),
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            sg.bucketSet('s_xyyx_token', account_id, json.dumps(token_info, ensure_ascii=False))

            results.append(f"✅ ID:{account_id} {info.get('name', '未知')} 积分:{info.get('jifen', 0)}")
            success_count += 1
        else:
            results.append(f"❌ {info.get('error', '验证失败')}")
            fail_count += 1

    result_text = "\n".join(results[:10])
    if len(results) > 10:
        result_text += f"\n... 共{len(results)}条"

    sender.reply(
        f"=====登录完成=====\n"
        f"✅ 成功: {success_count}个\n"
        f"❌ 失败: {fail_count}个\n"
        f"------------------\n"
        f"{result_text}\n"
        f"------------------\n"
        f"💡 发送\"星韵管理\"授权\n"
        f"=================="
    )


def query_accounts():
    if not uservalue:
        sender.reply("=====未绑定账号=====\n❌ 未找到账号\n💡 发送 星韵登录 绑定\n==================")
        return

    try:
        accounts = _sg_literal(uservalue)
    except:
        sender.reply("❌ 账号数据异常")
        return

    if not accounts:
        sender.reply("=====未绑定账号=====\n❌ 未找到账号\n💡 发送 星韵登录 绑定\n==================")
        return

    account_list = "\n========选择账号=======\n[0] 全部账号"
    for i, account in enumerate(accounts, 1):
        auth_time = '2099-12-31'
        if not auth_time:
            auth_status = '未授权'
        elif auth_time < str(datetime.now().date()):
            auth_status = '已过期'
        else:
            auth_status = f'到期:{auth_time}'

        try:
            token_info = json.loads(sg.bucketGet('s_xyyx_token', account) or '{}')
            name = token_info.get('name', '未知')
        except:
            name = '未知'

        account_list += f"\n[{i}] {name}({auth_status})"

    account_list += "\n=====================\n支持多选，用逗号分隔\n回复\"q\"退出\n====================="
    sender.reply(account_list)

    choice = sender.input(120000, 1, False)
    if not choice or choice.lower() == 'q':
        sender.reply("✅ 已退出")
        return

    selected_accounts = []
    if choice == '0':
        selected_accounts = accounts
    else:
        try:
            indices = [int(x.strip()) for x in choice.split(',') if x.strip().isdigit()]
            for idx in indices:
                if 1 <= idx <= len(accounts):
                    selected_accounts.append(accounts[idx - 1])
        except:
            sender.reply("❌ 选择格式错误")
            return

    if not selected_accounts:
        sender.reply("❌ 未选择有效账号")
        return

    results = []
    for account in selected_accounts:
        try:
            token_info = json.loads(sg.bucketGet('s_xyyx_token', account) or '{}')
            token = token_info.get('token', '')

            if not token:
                results.append(f"❌ {mask_account(account)} Token不存在")
                continue

            is_valid, info = verify_token(token)

            if is_valid:
                auth_time = '2099-12-31'
                if not auth_time:
                    auth_status = '未授权'
                elif auth_time < str(datetime.now().date()):
                    auth_status = '已过期'
                else:
                    auth_status = f'到期:{auth_time}'

                results.append(
                    f"📱 {info.get('name', '未知')}\n"
                    f"   积分: {info.get('jifen', 0)}\n"
                    f"   授权: {auth_status}"
                )

                token_info['name'] = info.get('name', token_info.get('name', '未知'))
                token_info['jifen'] = info.get('jifen', token_info.get('jifen', 0))
                token_info['update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                sg.bucketSet('s_xyyx_token', account, json.dumps(token_info, ensure_ascii=False))
            else:
                results.append(f"❌ {mask_account(account)} Token已失效")
        except Exception:
            results.append(f"❌ {mask_account(account)} 查询异常")

    result_text = "\n------------------\n".join(results)
    sender.reply(
        f"=====查询结果=====\n"
        f"------------------\n"
        f"{result_text}\n"
        f"=================="
    )


def manage_account():
    if not uservalue:
        sender.reply("=====未绑定账号=====\n❌ 未找到账号\n==================")
        return

    try:
        accounts = _sg_literal(uservalue)
    except:
        sender.reply("❌ 账号数据异常")
        return

    sender.reply(
        "=====星韵管理=====\n"
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

    if choice == '1':
        authorize_accounts(accounts)
    elif choice == '2':
        delete_accounts(accounts)
    elif choice == '3':
        submit_to_qinglong(accounts)
    else:
        sender.reply("❌ 无效选择")


def select_accounts_menu(accounts, action_name):
    account_list = f"\n========选择{action_name}=======\n[0] 全部账号"
    for i, account in enumerate(accounts, 1):
        auth_time = '2099-12-31'
        if not auth_time:
            auth_status = '未授权'
        elif auth_time < str(datetime.now().date()):
            auth_status = '已过期'
        else:
            auth_status = f'到期:{auth_time}'

        try:
            token_info = json.loads(sg.bucketGet('s_xyyx_token', account) or '{}')
            name = token_info.get('name', '未知')
        except:
            name = '未知'

        account_list += f"\n[{i}] {name}({auth_status})"

    account_list += "\n=====================\n支持多选，用逗号分隔\n回复\"q\"退出\n====================="
    sender.reply(account_list)

    choice = sender.input(120000, 1, False)
    if not choice or choice.lower() == 'q':
        return None

    selected = []
    if choice == '0':
        selected = accounts
    else:
        try:
            indices = [int(x.strip()) for x in choice.split(',') if x.strip().isdigit()]
            for idx in indices:
                if 1 <= idx <= len(accounts):
                    selected.append(accounts[idx - 1])
        except:
            pass

    return selected


def authorize_accounts(accounts):
    return True


def delete_accounts(accounts):
    selected = select_accounts_menu(accounts, "删除账号")
    if not selected:
        sender.reply("✅ 已取消")
        return

    sender.reply(f"⚠️ 确认删除 {len(selected)} 个账号?\n回复\"确认\"删除，其他取消")
    confirm = sender.input(60000, 1, False)

    if confirm != "确认":
        sender.reply("✅ 已取消")
        return

    success_count = 0
    for account in selected:
        try:
            delete_ql_env(account)
            sg.bucketDel('s_xyyx_token', account)
            True
            if account in accounts:
                accounts.remove(account)
            success_count += 1
        except:
            pass

    if accounts:
        sg.bucketSet('s_xyyx_user', userid, str(accounts))
    else:
        sg.bucketDel('s_xyyx_user', userid)

    sender.reply(f"✅ 删除完成，成功 {success_count} 个")


def submit_to_qinglong(accounts):
    selected = select_accounts_menu(accounts, "提交青龙")
    if not selected:
        sender.reply("✅ 已取消")
        return

    valid_accounts = []
    for account in selected:
        auth_time = '2099-12-31'
        if auth_time and auth_time >= str(datetime.now().date()):
            try:
                token_info = json.loads(sg.bucketGet('s_xyyx_token', account) or '{}')
                if token_info.get('token'):
                    valid_accounts.append({'account': account, 'info': token_info})
            except:
                pass

    if not valid_accounts:
        sender.reply("❌ 没有已授权且有效的账号")
        return

    success_count = 0
    for acc in valid_accounts:
        if update_ql_env(acc['account'], acc['info']):
            success_count += 1

    sender.reply(f"✅ 提交完成，成功 {success_count}/{len(valid_accounts)} 个")






def ks_auth():
    return True


def show_tutorial():
    sender.reply(
        "=====星韵优选教程=====\n"
        "📱 活动入口:\n"
        "#小程序://星韵优选/kt8xm5WOSI0Z6ri\n"
        "------------------\n"
        "用户指令:\n"
        "1. 星韵登录 - 绑定账号\n"
        "2. 星韵查询 - 查询积分和状态\n"
        "3. 星韵管理 - 授权、删除、提交面板\n"
        "4. 星韵教程 - 查看说明\n"
        "------------------\n"
        "管理员指令:\n"
        "1. 星韵授权 - 批量授权\n"
        "2. 星韵检测 - 检测过期并清理\n"
        "------------------\n"
        "绑定输入:\n"
        "3rdsession凭证\n"
        "支持换行批量绑定\n"
        "=================="
    )


def main():
    msg = sender.getMessage()

    if '登录' in msg or '登陆' in msg:
        bind_account()
    elif '查询' in msg and ('星韵' in msg or 'xyyx' in msg.lower()):
        query_accounts()
    elif '管理' in msg and ('星韵' in msg or 'xyyx' in msg.lower()):
        manage_account()
    elif '教程' in msg and ('星韵' in msg or 'xyyx' in msg.lower()):
        show_tutorial()
    elif '星韵授权' in msg or 'xyyx授权' in msg.lower():
        ks_auth()
    elif '星韵检测' in msg or 'xyyx检测' in msg.lower():
        if not sender.isAdmin():
            sender.reply("❌ 仅限管理员")
            return
        sender.reply("🔍 正在检测...")
        result = check_auth_status(
            's_xyyx', 's_xyyx_user', 's_xyyx_auth', 's_xyyx_token',
            '星韵优选', delete_ql_callback=delete_ql_env
        )
        sender.reply(result)
    elif sender.getImtype() == 'fake':
        try:
            result = check_auth_status(
                's_xyyx', 's_xyyx_user', 's_xyyx_auth', 's_xyyx_token',
                '星韵优选', delete_ql_callback=delete_ql_env
            )
            sg.notifyMasters(result)
        except:
            pass
    else:
        sender.setContinue()


if __name__ == "__main__":
    main()
