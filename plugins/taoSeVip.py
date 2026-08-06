# [title: 桃色VIP]
# [name: taoSeVip]
# [language: python]
# [class: 任务]
# [author: rujingxianghai]
# [version: v1.4.2]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^桃色登录$|^登录桃色$|^桃色查询$|^桃色管理$|^桃色运行$|^桃色一键运行$|^桃色刷新$|^刷新桃色$|^桃色$|^桃色检测$|^桃色教程$]
# [cron: 18 8 * * *]
# [icon: https://y.gtimg.cn/music/photo_new/T053M0000011Juce2IQQ8j.jpg]
# [description: 更新日志：；1.0.0：初版，计划任务自行定时"桃色一键运行"(先刷新SSID，再运行任务)]
# [depe: ["requests"]]

import asyncio as _sg_asyncio
import os as _sg_os
import time as _sg_time
import types as _sg_types
import json as _sg_json
from threading import Thread as _sg_Thread
from sillygirl import Adapter as _SGAdapter, Bucket as _SGBucket, Sender as _SGSender, sender as _sg_sender, plugin
check_auth_status = lambda *args, **kwargs: "账号默认可用"
try: import ast as _sg_ast
except Exception: _sg_ast=None

_sg_loop = None

def _sg_get_loop():
    global _sg_loop
    if _sg_loop is not None and not _sg_loop.is_closed(): return _sg_loop
    box = {}
    def runner():
        loop = _sg_asyncio.new_event_loop(); _sg_asyncio.set_event_loop(loop); box["loop"] = loop; loop.run_forever()
    _sg_Thread(target=runner, daemon=True).start()
    while "loop" not in box: _sg_time.sleep(0.01)
    _sg_loop = box["loop"]; return _sg_loop

def _sg_run(value):
    if not _sg_asyncio.iscoroutine(value): return value
    return _sg_asyncio.run_coroutine_threadsafe(value, _sg_get_loop()).result()

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
    s = _SGSender(uuid or _sg_os.environ.get("SENDER_ID", "")); call = lambda name,*a,**k: _sg_run(getattr(s,name)(*a,**k))
    def wait(timeout=60000,*a,**k):
        try:
            reply = call("listen", {"timeout": int(timeout or 0)}); return _sg_run(reply.getContent()) if reply else ""
        except Exception: return ""
    return _sg_types.SimpleNamespace(getUserID=lambda:call("getUserId"),getUserId=lambda:call("getUserId"),getMessage=lambda:call("getContent"),getContent=lambda:call("getContent"),getUserName=lambda:call("getUserName"),getNickname=lambda:call("getUserName"),getChatID=lambda:call("getChatId"),getChatId=lambda:call("getChatId"),getImtype=lambda:call("getPlatform"),getPlatform=lambda:call("getPlatform"),getMessageID=lambda:call("getMessageId"),getPluginName=lambda:_sg_os.environ.get("PLUGIN_NAME",""),getPluginVersion=lambda:_sg_os.environ.get("PLUGIN_VERSION",""),isAdmin=lambda:bool(call("isAdmin")),reply=lambda m="":call("reply",str(m)),replyImage=lambda u="":call("reply",str(u) if str(u).startswith("[") else f"[CQ:image,file={u}]"),listen=wait,input=wait,waitInput=wait,setContinue=lambda *a,**k:call("continue_"),breakIn=lambda *a,**k:call("continue_"))

def _sg_bucket_get(bucket=None,key=None,default="",**kw):
    try:
        value=_SGBucket(str(kw.get("bucket",bucket) or ""))[str(kw.get("key",key) or "")]; return default if value in (None,"") and default not in (None,"") else (value if value is not None else "")
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
    item=a[0] if a and isinstance(a[0],dict) else {}; platform=item.get("imType") or item.get("platform") or kw.get("platform") or (a[0] if a else ""); group=item.get("groupCode") or item.get("group_id") or kw.get("group_id") or (a[1] if len(a)>1 else ""); user=item.get("userID") or item.get("user_id") or kw.get("userID") or (a[2] if len(a)>2 else ""); title=item.get("title") or kw.get("title") or (a[3] if len(a)>3 else ""); message=item.get("content") or item.get("message") or kw.get("content") or (a[4] if len(a)>4 else title); return _sg_run(_SGAdapter(str(platform or "")).push({"group_id":str(group or ""),"user_id":str(user or ""),"title":str(title or ""),"content":str(message or "")}))
def _sg_notify(message,channels=None,*a,**k): return _sg_run(_sg_sender.pushAdmin(str(message),{"platforms":list(channels or [])} if channels else {}))
class _SGFacade:
    Sender=staticmethod(_sg_sender_sync); getSenderID=staticmethod(lambda:_sg_os.environ.get("SENDER_ID","")); getPluginName=staticmethod(lambda:_sg_os.environ.get("PLUGIN_NAME","")); bucketGet=staticmethod(_sg_bucket_get); bucketSet=staticmethod(_sg_bucket_set); bucketDel=staticmethod(_sg_bucket_del); bucketDelete=staticmethod(_sg_bucket_del); bucketAllKeys=staticmethod(_sg_bucket_keys); bucketKeys=staticmethod(_sg_bucket_keys); bucketAll=staticmethod(_sg_bucket_all); notifyMasters=staticmethod(_sg_notify); pushAdmin=staticmethod(_sg_notify); push=staticmethod(_sg_push); Push=staticmethod(_sg_push); reply=staticmethod(lambda m="":_sg_sender_sync().reply(m)); get=staticmethod(lambda k,default="":_sg_bucket_get(*(str(k).split(".",1) if "." in str(k) else ["otto",k]),default=default)); getParam=get; version=staticmethod(lambda:{"sn":_sg_os.environ.get("SILLYGIRL_VERSION","3.0.0"),"version":_sg_os.environ.get("SILLYGIRL_VERSION","3.0.0")}); port=staticmethod(lambda:_sg_os.environ.get("SILLYGIRL_PORT","8080")); sleep=staticmethod(lambda sec:_sg_time.sleep(float(sec or 0)))
sg=_SGFacade(); Sender=sg.Sender; getSenderID=sg.getSenderID; bucketGet=sg.bucketGet; bucketSet=sg.bucketSet; bucketAllKeys=sg.bucketAllKeys; notifyMasters=sg.notifyMasters

mask_account=lambda v: (str(v or "") if len(str(v or ""))<=7 else str(v or "")[:3]+"***"+str(v or "")[-4:])

config = plugin.Form({
    "enable": plugin.Form.boolean().title("是否启用").default(True),
    's_taose_wxpusher_app_token': plugin.Form.string().title('WxPusher AppToken').default('').description('不填则不推送'),
    's_taose_wxpusher_uids': plugin.Form.string().title('WxPusher推送UID，多个用英文逗号分隔').default('').description('扫码关注：https://img-upload.example.invalid/a2f034a9cb69badfe18e364d32be70ea.png'),
    's_taose_notify': plugin.Form.string().title('通知渠道').default('').description('检测通知推送渠道'),
})
_CONFIG_FIELD_MAP = {
    ('s_taose', 'wxpusher_app_token'): 's_taose_wxpusher_app_token',
    ('s_taose', 'wxpusher_uids'): 's_taose_wxpusher_uids',
    ('s_taose', 'notify'): 's_taose_notify',
}

import json
import requests
import time
import random
import string
from datetime import datetime

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()
uservalue = sg.bucketGet(bucket='s_taose_user', key=userid)

PLUGIN_CONFIG = {'bucket': 's_taose', 'coin_key': 'dd_sign_points', 'name': '桃色VIP'}

def _get_headers(cookies=''):
    return {
        "Host": "wxapp.lllac.com",
        "Connection": "keep-alive",
        "charset": "utf-8",
        "cookie": cookies,
        "User-Agent": "Mozilla/5.0 (Linux; Android 15; 2210132C Build/AQ3A.240812.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/130.0.6723.103 Mobile Safari/537.36 XWEB/1300473 MMWEBSDK/20240404 MMWEBID/1429 MicroMessenger/8.0.49.2600(0x2800313D) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android",
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip,compress,br,deflate",
        "Referer": "https://servicewechat.com/wxa11d535651f0f097/58/page-frame.html"
    }

def push_notification(title, content):
    WXPUSHER_APP_TOKEN = sg.bucketGet('s_taose', 'wxpusher_app_token') or ''
    WXPUSHER_UIDS = sg.bucketGet('s_taose', 'wxpusher_uids') or ''

    if not WXPUSHER_APP_TOKEN or not WXPUSHER_UIDS:
        print("未配置WxPusher推送参数，跳过推送")
        return False

    try:
        uid_list = [uid.strip() for uid in WXPUSHER_UIDS.split(',') if uid.strip()]
        data = {
            "appToken": WXPUSHER_APP_TOKEN,
            "content": content,
            "summary": title,
            "contentType": 2,
            "uids": uid_list
        }
        response = requests.post("http://wxpusher.zjiecode.com/api/send/message", json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                return True
            print(f"推送失败：{result.get('msg', '未知错误')}")
        return False
    except Exception as e:
        print(f"推送异常：{str(e)}")
        return False

def push_task_statistics(stats_data):
    if not stats_data:
        return False

    current_time = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
    current_day = datetime.now().strftime("%Y年%m月%d日")

    push_content = f"""
    <div style="font-family: 'Microsoft YaHei', Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); overflow: hidden;">
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 20px; text-align: center;">
            <h2 style="margin: 0; font-size: 24px; font-weight: bold;">🍑 桃色VIP</h2>
        </div>
        <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); padding: 20px; margin: 15px; border-radius: 10px;">
            <h3 style="margin: 0 0 15px 0; text-align: center; color: white; font-size: 20px;">今日统计</h3>
            <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                <div style="flex: 1; min-width: 120px; background: rgba(255,255,255,0.95); padding: 15px; border-radius: 8px; text-align: center;">
                    <div style="color: #666; font-size: 14px; margin-bottom: 5px;">运行账号数</div>
                    <div style="font-size: 24px; font-weight: bold; color: #f5576c;">{len(stats_data['account_details'])}个</div>
                </div>
                <div style="flex: 1; min-width: 120px; background: rgba(255,255,255,0.95); padding: 15px; border-radius: 8px; text-align: center;">
                    <div style="color: #666; font-size: 14px; margin-bottom: 5px;">成功执行</div>
                    <div style="font-size: 24px; font-weight: bold; color: #28a745;">{stats_data['success_count']}个</div>
                </div>
            </div>
        </div>
        <div style="padding: 0 15px 15px 15px;">
            <h3 style="text-align: center; color: #333; font-size: 18px; margin-bottom: 15px;">账号明细</h3>
            <table style="width: 100%; border-collapse: collapse; background: #fff;">
                <thead>
                    <tr style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
                        <th style="padding: 12px 8px; text-align: center; color: white; font-size: 14px; border: 1px solid #ddd;">序号</th>
                        <th style="padding: 12px 8px; text-align: center; color: white; font-size: 14px; border: 1px solid #ddd;">账号</th>
                        <th style="padding: 12px 8px; text-align: center; color: white; font-size: 14px; border: 1px solid #ddd;">执行状态</th>
                        <th style="padding: 12px 8px; text-align: center; color: white; font-size: 14px; border: 1px solid #ddd;">豆子</th>
                    </tr>
                </thead>
                <tbody>
    """

    for idx, account in enumerate(stats_data['account_details'], 1):
        status_color = '#28a745' if account['status'] == '成功' else '#e74c3c'
        push_content += f"""
                    <tr style="background: #f8f9fa;">
                        <td style="padding: 10px 8px; text-align: center; border: 1px solid #ddd; font-size: 13px;">{idx}</td>
                        <td style="padding: 10px 8px; text-align: center; border: 1px solid #ddd; font-size: 13px;">{account['account']}</td>
                        <td style="padding: 10px 8px; text-align: center; border: 1px solid #ddd; font-size: 13px; color: {status_color}; font-weight: bold;">{account['status']}</td>
                        <td style="padding: 10px 8px; text-align: center; border: 1px solid #ddd; font-size: 13px;">{account['dou']}</td>
                    </tr>
        """

    push_content += f"""
                    <tr style="background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); font-weight: bold;">
                        <td colspan="2" style="padding: 12px 8px; text-align: center; border: 1px solid #ddd; font-size: 14px;">总计</td>
                        <td style="padding: 12px 8px; text-align: center; border: 1px solid #ddd; font-size: 14px; color: #28a745;">成功{stats_data['success_count']}个</td>
                        <td style="padding: 12px 8px; text-align: center; border: 1px solid #ddd; font-size: 14px;">-</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div style="display: flex; justify-content: center; align-items: center; background: #f8f9fa; padding: 15px; color: #6c757d; font-size: 12px; border-top: 1px solid #dee2e6;">
            <p style="margin: 0;">🍑 桃色VIP任务系统<br>统计时间: {current_time}</p>
        </div>
    </div>
    """

    return push_notification(f"🍑 桃色VIP {current_day}", push_content)

def login_with_account(username, password, skip_auth=False):
    try:
        session_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=32))

        response = requests.post(
            "https://wxapp.lllac.com/xqw/login.php",
            data={"act": "login", "u_name": username, "u_pass": password, "session_id": session_id},
            headers=_get_headers(f"SSID={session_id}")
        )

        if response.status_code != 200:
            raise Exception("登录请求失败")

        result = response.json()
        if result.get('error') != 0:
            raise Exception(result.get('msg', '登录失败'))

        sender.reply(f"✅ 账号 {username} 登录成功，正在获取用户信息...")

        sg.bucketSet('s_taose_pwd', username, password)

        global uservalue
        accounts = _sg_literal(uservalue or '[]')
        if username not in accounts:
            accounts.append(username)
            sg.bucketSet('s_taose_user', userid, str(accounts))
            uservalue = str(accounts)

        sg.bucketSet('s_taose_token', username, f"{username}#{password}#SSID={session_id}")

        return process_login(f"SSID={session_id}", username, skip_auth)

    except Exception as e:
        sender.reply(f"❌ 登录失败: {str(e)}")
        return False

def get_user_info(cookies):
    try:
        response = requests.get(
            "https://wxapp.lllac.com/xqw/user_home_v2.php?act=home&channel=tsvip&qudao=normal&cid_most=&gid_most=&version=30&od_count=",
            headers=_get_headers(cookies)
        )

        if response.status_code != 200:
            raise Exception("获取用户信息失败")

        result = response.json()
        if result.get('error') != 0:
            raise Exception(result.get('msg', '获取用户信息失败'))

        return {
            'username': result.get('user_name', '未知'),
            'rank': result.get('user_rank', '未知'),
            'point': result.get('user_point', '0'),
            'dou': result.get('user_dou', '0'),
            'next_rank': result.get('next_rank', '未知'),
            'next_point': result.get('next_point', '0'),
            'bar': result.get('bar', '0')
        }
    except Exception as e:
        raise Exception(f"获取用户信息失败: {str(e)}")

def sign_account(cookies):
    try:
        ssid = cookies.split('=')[1] if '=' in cookies else cookies
        response = requests.get(
            f"https://wxapp.lllac.com/xqw/user_mall.php?act=signToday&ssid={ssid}&spm=x.user",
            headers=_get_headers(cookies)
        )

        if response.status_code != 200:
            raise Exception("签到请求失败")

        return response.json()
    except Exception as e:
        raise Exception(f"签到失败: {str(e)}")

def refresh_account_ssid(account):
    try:
        cookie_str = sg.bucketGet('s_taose_token', account)
        if not cookie_str:
            return f"❌ 账号 {account} 未找到登录信息"

        parts = cookie_str.split('#')
        if len(parts) < 2:
            return f"❌ 账号 {account} 登录信息不完整"

        username, password = parts[0], parts[1]
        session_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=32))

        response = requests.post(
            "https://wxapp.lllac.com/xqw/login.php",
            data={"act": "login", "u_name": username, "u_pass": password, "session_id": session_id},
            headers=_get_headers(f"SSID={session_id}")
        )

        if response.status_code != 200:
            return f"❌ 账号 {account} 刷新SSID失败: 请求错误"

        result = response.json()
        if result.get('error') != 0:
            return f"❌ 账号 {account} 刷新SSID失败: {result.get('msg', '登录失败')}"

        sg.bucketSet('s_taose_token', account, f"{username}#{password}#SSID={session_id}")
        return f"✅ 账号 {account} SSID已更新"

    except Exception as e:
        return f"❌ 账号 {account} 刷新SSID失败: {str(e)}"

def _get_cookies(account):
    cookie_str = sg.bucketGet('s_taose_token', account)
    if not cookie_str:
        return None
    parts = cookie_str.split('#')
    return parts[2] if len(parts) >= 3 else cookie_str

def login():
    try:
        global uservalue
        uservalue = sg.bucketGet(bucket='s_taose_user', key=userid)
        accounts = _sg_literal(uservalue or '[]')

        if accounts:
            account_list = "=====已绑定账号====="
            for i, account in enumerate(accounts, 1):
                auth_time = '2099-12-31'
                account_list += f"\n[{i}] {account} ({auth_time})"
            account_list += "\n=================\n选择序号刷新SSID\n输入账号进行登录\n回复\"q\"退出"

            sender.reply(account_list)
            choice = sender.listen(60000)

            if not choice or choice == 'q':
                sender.reply("✅ 已退出登录流程")
                return

            try:
                index = int(choice) - 1
                if 0 <= index < len(accounts):
                    selected = accounts[index]
                    password = sg.bucketGet('s_taose_pwd', selected)
                    if not password:
                        sender.reply("⚠️ 未找到该账号的密码记录，请重新输入密码:")
                        password = sender.listen(60000)
                        if not password or password == 'q':
                            sender.reply("✅ 已退出登录流程")
                            return
                    login_with_account(selected, password)
                    return
            except ValueError:
                pass

            sender.reply("请输入密码:\n回复\"q\"退出")
            password = sender.listen(60000)
            if not password or password == 'q':
                sender.reply("✅ 已退出登录流程")
                return
            login_with_account(choice, password)
        else:
            sender.reply("请输入账号:\n回复\"q\"退出")
            username = sender.listen(60000)
            if not username or username == 'q':
                sender.reply("✅ 已退出登录流程")
                return

            sender.reply("请输入密码:\n回复\"q\"退出")
            password = sender.listen(60000)
            if not password or password == 'q':
                sender.reply("✅ 已退出登录流程")
                return

            login_with_account(username, password)
    except Exception as e:
        sender.reply(f"❌ 登录流程出错: {str(e)}")

def process_login(cookies, username, skip_auth=False):
    try:
        auth_time = '2099-12-31'
        current_date = str(datetime.now().date())
        is_authorized = auth_time and auth_time > current_date

        if skip_auth:
            return True
        elif is_authorized:
            sender.reply(
                f"=====登录成功=====\n"
                f"📱 账号: {username}\n"
                f"📅 授权到期: {auth_time}\n"
                f"✅ 账号已更新\n"
                f"=================="
            )
            return True
        else:
            return authorize_accounts([username])
    except Exception as e:
        sender.reply(f"❌ 处理登录失败: {str(e)}")
        return False

def query_taose():
    try:
        accounts = _sg_literal(uservalue or '[]')
        if not accounts:
            sender.reply("❌ 您还没有绑定桃色账号")
            return

        for account in accounts:
            cookies = _get_cookies(account)
            if not cookies:
                continue

            try:
                user_info = get_user_info(cookies)
                auth_time = '2099-12-31'
                sender.reply(
                    f"=====账号信息=====\n"
                    f"📱 账号: {mask_account(account)}\n"
                    f"👤 昵称: {user_info['username']}\n"
                    f"🎖️ 等级: {user_info['rank']}\n"
                    f"📈 成长值: {user_info['point']}\n"
                    f"💰 豆子: {user_info['dou']}\n"
                    f"📅 到期: {auth_time}\n"
                    f"=================="
                )
            except Exception as e:
                sender.reply(f"❌ 账号 {mask_account(account)} 查询失败: {str(e)}")
    except Exception as e:
        sender.reply(f"❌ 查询失败: {str(e)}")

def authorize_accounts(selected_accounts):
    return True

def run_account(account):
    try:
        cookies = _get_cookies(account)
        if not cookies:
            return f"❌ 账号 {account} 未找到登录信息"

        user_info = get_user_info(cookies)
        if not user_info:
            return f"❌ 账号 {account} 获取用户信息失败"

        sign_result = sign_account(cookies)

        sign_status = "✅ 签到成功"
        sign_reward = ""
        if sign_result.get('error') == 0:
            if sign_result.get('msg') == '今日已签到':
                sign_status = "⏰ 今日已签到"
            else:
                if sign_result.get('day'):
                    sign_reward = f"\n📅 已签到: {sign_result.get('day')}天"

        return (
            f"===== 运行结果 =====\n"
            f"📱 账号: {mask_account(account)}\n"
            f"💰 豆子: {user_info['dou']}\n"
            f"{sign_status}{sign_reward}\n"
            f"================="
        )
    except Exception as e:
        return f"❌ 账号 {account} 运行失败: {str(e)}"

def run_user_accounts():
    try:
        accounts = _sg_literal(uservalue or '[]')
        if not accounts:
            return "❌ 您还没有绑定桃色账号"

        account_list = "=====账号列表=====\n[0] 全部账号\n"
        for i, account in enumerate(accounts, 1):
            auth_time = '2099-12-31'
            account_list += f"[{i}] {mask_account(account)} ({auth_time})\n"
        account_list += "------------------\n请选择要运行的账号\n多账号逗号分隔\n回复\"q\"退出"

        sender.reply(account_list)
        choice = sender.listen(60000)

        if not choice or choice == 'q':
            return "✅ 已退出运行流程"

        selected = []
        if choice == '0':
            selected = accounts[:]
        else:
            try:
                indices = [int(x.strip()) - 1 for x in choice.split(',')]
                for idx in indices:
                    if 0 <= idx < len(accounts):
                        selected.append(accounts[idx])
            except ValueError:
                return "❌ 无效的选择格式"

        if not selected:
            return "❌ 未选择有效账号"

        for account in selected:
            auth_time = '2099-12-31'
            if auth_time and auth_time > str(datetime.now().date()):
                sender.reply(run_account(account))
            else:
                sender.reply(f"❌ 账号 {mask_account(account)} 未授权或已过期")

    except Exception as e:
        return f"❌ 运行失败: {str(e)}"

def refresh_all_ssids():
    try:
        auth_accounts = []
        all_users = sg.bucketAllKeys('s_taose_user')

        for uid in all_users:
            user_accounts = _sg_literal(sg.bucketGet('s_taose_user', uid) or '[]')
            for account in user_accounts:
                auth_time = '2099-12-31'
                if auth_time and auth_time > str(datetime.now().date()):
                    auth_accounts.append(account)

        if not auth_accounts:
            return "⚠️ 未找到任何已授权账号"

        success_count = sum(1 for acc in auth_accounts if "✅" in refresh_account_ssid(acc))
        return f"✅ 已刷新 {success_count}/{len(auth_accounts)} 个账号的SSID"

    except Exception as e:
        return f"❌ 刷新SSID失败: {str(e)}"

def run_all_accounts():
    try:
        refresh_result = refresh_all_ssids()
        sender.reply(f"正在刷新所有账号SSID...\n{refresh_result}")

        all_users = sg.bucketAllKeys('s_taose_user')
        if not all_users:
            sender.reply("❌ 未找到任何用户")
            return

        sender.reply("开始运行所有已授权账号...")

        stats_data = {'account_details': [], 'success_count': 0, 'fail_count': 0}

        for uid in all_users:
            user_accounts = _sg_literal(sg.bucketGet('s_taose_user', uid) or '[]')
            for account in user_accounts:
                auth_time = '2099-12-31'
                if not (auth_time and auth_time > str(datetime.now().date())):
                    continue

                try:
                    cookies = _get_cookies(account)
                    if not cookies:
                        raise Exception("无登录信息")

                    user_info = get_user_info(cookies)
                    if not user_info:
                        raise Exception("获取信息失败")

                    sign_account(cookies)
                    stats_data['account_details'].append({
                        'account': mask_account(account),
                        'status': '成功',
                        'dou': user_info.get('dou', '0')
                    })
                    stats_data['success_count'] += 1
                    sender.reply(run_account(account))
                except Exception as e:
                    stats_data['account_details'].append({
                        'account': mask_account(account),
                        'status': '失败',
                        'dou': '0'
                    })
                    stats_data['fail_count'] += 1
                    sender.reply(f"❌ 账号 {account} 运行失败: {str(e)}")

        sender.reply("✅ 所有账号运行完成")

        if stats_data['account_details']:
            push_task_statistics(stats_data)

    except Exception as e:
        sender.reply(f"❌ 运行失败: {str(e)}")

def refresh_user_accounts():
    try:
        accounts = _sg_literal(uservalue or '[]')
        if not accounts:
            return "❌ 您还没有绑定桃色账号"

        account_list = "=====账号列表=====\n[0] 全部账号\n"
        for i, account in enumerate(accounts, 1):
            auth_time = '2099-12-31'
            account_list += f"[{i}] {mask_account(account)} ({auth_time})\n"
        account_list += "------------------\n请选择要刷新SSID的账号\n多账号逗号分隔\n回复\"q\"退出"

        sender.reply(account_list)
        choice = sender.listen(60000)

        if not choice or choice == 'q':
            return "✅ 已退出刷新流程"

        selected = []
        if choice == '0':
            selected = accounts[:]
        else:
            try:
                indices = [int(x.strip()) - 1 for x in choice.split(',')]
                for idx in indices:
                    if 0 <= idx < len(accounts):
                        selected.append(accounts[idx])
            except ValueError:
                return "❌ 无效的选择格式"

        if not selected:
            return "❌ 未选择有效账号"

        sender.reply("开始刷新账号SSID...")
        for account in selected:
            sender.reply(refresh_account_ssid(account))

        return "✅ SSID刷新完成"

    except Exception as e:
        return f"❌ 刷新失败: {str(e)}"

def manage_taose():
    try:
        accounts = _sg_literal(uservalue or '[]')
        if not accounts:
            sender.reply("❌ 您还没有绑定桃色账号")
            return

        sender.reply(
            "=====管理选项=====\n"
            "[1] 账号授权\n"
            "[2] 账号删除\n"
            "[3] 运行账号\n"
            "------------------\n"
            "回复数字选择操作\n"
            "回复\"q\"退出"
        )
        option = sender.listen(60000)

        if not option or option == 'q':
            sender.reply("✅ 已退出管理流程")
            return

        if option not in ['1', '2', '3']:
            sender.reply("❌ 无效的选择")
            return

        action_name = {'1': '授权', '2': '删除', '3': '运行'}[option]

        account_list = "=====账号列表=====\n[0] 全部账号"
        for i, account in enumerate(accounts, 1):
            auth_time = '2099-12-31'
            account_list += f"\n[{i}] {mask_account(account)} ({auth_time})"
        account_list += f"\n------------------\n请选择要{action_name}的账号\n多账号逗号分隔\n回复\"q\"退出"

        sender.reply(account_list)
        choice = sender.listen(60000)

        if not choice or choice == 'q':
            sender.reply("✅ 已退出管理流程")
            return

        selected = []
        if choice == '0':
            selected = accounts[:]
        else:
            try:
                indices = [int(x.strip()) - 1 for x in choice.split(',')]
                for idx in indices:
                    if 0 <= idx < len(accounts):
                        selected.append(accounts[idx])
            except ValueError:
                sender.reply("❌ 无效的选择格式")
                return

        if not selected:
            sender.reply("❌ 未选择有效账号")
            return

        if option == '1':
            authorize_accounts(selected)

        elif option == '2':
            confirm_msg = "=====删除确认=====\n即将删除以下账号:\n"
            for acc in selected:
                auth_time = '2099-12-31'
                confirm_msg += f"- {mask_account(acc)} ({auth_time})\n"
            confirm_msg += "------------------\n⚠️ 数据及授权无法恢复\n回复\"y\"确认删除"

            sender.reply(confirm_msg)
            confirm = sender.listen(60000)

            if not confirm or confirm.lower() != 'y':
                sender.reply("✅ 已取消删除")
                return

            success = 0
            for acc in selected:
                try:
                    accounts.remove(acc)
                    sg.bucketSet('s_taose_token', acc, '')
                    True
                    sg.bucketDel('s_taose_pwd', acc)
                    success += 1
                except:
                    continue

            if accounts:
                sg.bucketSet('s_taose_user', userid, str(accounts))
            else:
                sg.bucketDel('s_taose_user', userid)

            sender.reply(f"✅ 已成功删除 {success}/{len(selected)} 个账号")

        else:
            for acc in selected:
                auth_time = '2099-12-31'
                if auth_time and auth_time > str(datetime.now().date()):
                    sender.reply(run_account(acc))
                else:
                    sender.reply(f"❌ 账号 {mask_account(acc)} 未授权或已过期")

    except Exception as e:
        sender.reply(f"❌ 管理失败: {str(e)}")

def ks_auth():
    return True

def show_tutorial():
    sender.reply(
        "=====桃色VIP教程=====\n"
        "📱 用户指令:\n"
        "• 桃色登录 - 绑定桃色账号\n"
        "• 桃色查询 - 查询账号状态和豆子信息\n"
        "• 桃色管理 - 授权/删除账号\n"
        "• 桃色运行 - 运行已授权账号任务\n"
        "• 桃色刷新 - 刷新账号SSID\n"
        "• 桃色教程 - 查看本教程\n"
        "------------------\n"
        "🔧 管理员指令:\n"
        "• 桃色授权 - 管理员按天数授权\n"
        "• 桃色检测 - 检测过期账号并清理\n"
        "• 桃色一键运行 - 运行所有用户任务\n"
        "------------------\n"
        "💡 登录说明:\n"
        "📝 输入账号和密码进行登录\n"
        "📝 支持选择已绑定账号刷新SSID\n"
        "------------------\n"
        "📝 账号获取方式:\n"
        "入口：#小程序://桃色VIP/xxxxx\n"
        "注：打开小程序，用微信登录\n"
        "然后在个人中心设置密码\n"
        "这个修改密码入口时有时无，只有自己多试一下，不行就注销再试\n"
        "=================="
    )

def main():
    try:
        msg = sender.getMessage()

        if '桃色教程' in msg:
            show_tutorial()
        elif '桃色查询' in msg:
            query_taose()
        elif '桃色管理' in msg:
            manage_taose()
        elif '桃色登录' in msg or '登录桃色' in msg:
            login()
        elif '桃色运行' in msg:
            result = run_user_accounts()
            if result:
                sender.reply(result)
        elif '桃色一键运行' in msg:
            if not sender.isAdmin():
                sender.reply("❌ 该指令仅管理员可用")
                return
            run_all_accounts()
        elif '桃色刷新' in msg or '刷新桃色' in msg:
            result = refresh_user_accounts()
            if result:
                sender.reply(result)
        elif '桃色授权' in msg:
            ks_auth()
        elif '桃色检测' in msg:
            if not sender.isAdmin():
                sender.reply("❌ 仅限管理员")
                return
            sender.reply("🔍 正在检测...")
            sender.reply(check_auth_status())
        elif sender.getImtype() == 'fake':
            try:
                sg.notifyMasters(check_auth_status())
            except:
                pass
        else:
            sender.setContinue()

    except Exception as e:
        sender.reply(f"❌ 运行出错: {str(e)}")

if __name__ == "__main__":
    main()
