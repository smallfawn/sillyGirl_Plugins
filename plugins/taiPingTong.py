# [title: 太平通]
# [name: taiPingTong]
# [language: python]
# [class: 任务]
# [author: linzixuan]
# [version: v1.0.1]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^太平(上车|管理|查询|运行|教程)$]
# [icon: https://img1.baidu.com/it/u=35209519,2603388558&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=500]
# [description: 太平通账号登录、查询与任务运行]
# [depe: ["curl-cffi","requests","urllib3"]]

import asyncio as _sg_asyncio
import os as _sg_os
import time as _sg_time
import types as _sg_types
import json as _sg_json
from threading import Thread as _sg_Thread
from sillygirl import Adapter as _SGAdapter, Bucket as _SGBucket, Sender as _SGSender, sender as _sg_sender, plugin
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

config = plugin.Form({
    'bd_tptconfig_yxbf': plugin.Form.string().title('运行并发数').default('').description('设置管理员一键运行所有账号同时最多多少账号一起运行,默认1'),
    'bd_tptconfig_sdyx': plugin.Form.boolean().title('手动运行').default(False).description('是否允许用户手动执行任务(默认否)'),
    'bd_tptconfig_proxy_api': plugin.Form.string().title('代理API').default('').description('代理API地址,留空则不使用代理'),
})
_CONFIG_FIELD_MAP = {
    ('bd_tptconfig', 'yxbf'): 'bd_tptconfig_yxbf',
    ('bd_tptconfig', 'sdyx'): 'bd_tptconfig_sdyx',
    ('bd_tptconfig', 'proxy_api'): 'bd_tptconfig_proxy_api',
}

import concurrent.futures
import json
import random
import time
from datetime import datetime
import os

try:
    from curl_cffi import requests
except:
    import requests


class ATM_tpt:
    def __init__(self, user, sender):
        self.user, self.sender = user, sender
        self.usid = self.ck = self.name = None

    def set_name(self):
        self.sender.reply("欢迎使用太平系统, 请先设置您的备注名(1-6个字符)。退出输入'q'!")
        name = self.sender.listen(60000)
        if name == 'q' or name == 'Q':
            self.sender.reply("退出！")
            return False
        elif name is None:
            self.sender.reply('超时退出！')
            return False
        else:
            if len(name) > 6 or len(name) < 1:
                self.sender.reply("备注名不符合要求，退出！")
                return False
            else:
                return name

    def tpsc(self):
        self.name = self.set_name()
        if not self.name: return
        self.sender.reply("太平通登录方式：\n1. 短信验证码登录\n2. CK 登录\n回复 q 退出")
        choice = self.sender.listen(60000)
        if choice == '1': self.dx_login()
        elif choice == '2': self.ck_login()
        elif choice in ('q', 'Q'): self.sender.reply('已退出')
        else: self.sender.reply('输入无效或已超时')

    def gl_login(self):
        try:
            xx_url = 'https://ecustomer.cntaiping.com/tpayms/app/tpay/account/getAcct'
            headers = {
                'Host': 'ecustomer.cntaiping.com',
                'x-ac-black-box': '',
                'x-ac-token-ticket': self.ck,
                'x-ac-channel-id': 'KHT',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept': 'application/json;charset=UTF-8',
                'Origin': 'https://ecustomercdn.itaiping.com',
                'User-Agent': "Mozilla/5.0 (Linux; Android 13; Pixel 4 XL Build/TP1A.220905.004; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/119.0.6045.163 Mobile Safari/537.36;yuangongejia#android#kehutong;webank/h5face;webank/1.0;netType:NETWORK_WIFI;appVersion:334;packageName:com.cntaiping.tpapp",
                'Connection': 'keep-alive',
                'Referer': 'https://ecustomercdn.itaiping.com/',
                'x-ac-mc-type': 'gateway.user'
            }
            r = requests.get(xx_url, headers=headers)
            success = r.json().get('success', None)
            if success:
                return '✅有效'
            else:
                return '❌失效'
        except Exception as e:
            return f'⛔{e}'

    def tpgl(self):
        data = _sg_literal(sg.bucketGet('bd_tptcks', self.user), {})
        if not data: return self.sender.reply('未找到账号，请先发送【太平上车】')
        accounts, rows = list(data.items()), []
        for index, (usid, account) in enumerate(accounts, 1):
            self.ck = account.get('ck', '')
            rows.append(f"{index}. {account.get('name', usid)} {self.gl_login()}")
        self.sender.reply('太平通账号：\n' + '\n'.join(rows) + '\n回复序号管理，q 退出')
        choice = self.sender.listen(60000)
        if choice in ('q', 'Q', None, ''): return
        try: usid, account = accounts[int(choice) - 1]
        except (ValueError, IndexError): return self.sender.reply('输入无效')
        self.usid, self.ck, self.name = usid, account.get('ck', ''), account.get('name', usid)
        self.gl_zh()

    def gl_zh(self):
        self.sender.reply(f'{self.name}：\n1. 运行任务\n2. 删除账号\n回复 q 退出')
        choice = self.sender.listen(60000)
        if choice == '1': self.gl_yx()
        elif choice == '2': self.gl_sc()
        elif choice not in ('q', 'Q', None, ''): self.sender.reply('输入无效')


    def gl_yx(self):
        if sg.bucketGet('bd_tptconfig', 'sdyx') == 'false': return self.sender.reply('管理员未开启手动运行')
        return TPT(self.user, 'qd', self.name, self.ck, self.usid, 1).main()

    def gl_sc(self):
        self.sender.reply(f'确认删除账号【{self.name}】？回复 y 确认')
        if self.sender.listen(60000) not in ('y', 'Y'): return self.sender.reply('已取消')
        data = _sg_literal(sg.bucketGet('bd_tptcks', self.user), {})
        data.pop(str(self.usid), None)
        sg.bucketSet('bd_tptcks', self.user, str(data))
        self.sender.reply('账号已删除')



    def tpcx(self):
        data = _sg_literal(sg.bucketGet('bd_tptcks', self.user), {})
        if not data: return self.sender.reply('未找到账号，请先发送【太平上车】')
        rows = []
        for index, (usid, account) in enumerate(data.items(), 1):
            self.ck = account.get('ck', ''); name = account.get('name', usid); status = self.gl_login()
            if '有效' not in status:
                rows.append(f'{index}. {name} {status}'); continue
            result = TPT(self.user, 'qd', name, self.ck, usid, 1).cx()
            rows.append(f'{index}. {name} 今日 {result[1]}，当前 {result[0]}' if isinstance(result, tuple) else f'{index}. {name} 查询失败')
        self.sender.reply('太平通账号查询：\n' + '\n'.join(rows))

    def get_tptcks(self):
        accounts = {}
        for user in sg.bucketAllKeys('bd_tptcks'):
            for usid, item in _sg_literal(sg.bucketGet('bd_tptcks', user), {}).items():
                if item.get('ck'): accounts[str(usid)] = {'name': item.get('name', usid), 'ck': item['ck'], 'user': user}
        return accounts

    def tpyx(self):
        accounts = self.get_tptcks()
        if not accounts: return self.sender.reply('没有可运行的太平通账号')
        try: workers = max(1, int(sg.bucketGet('bd_tptconfig', 'yxbf') or 1))
        except ValueError: workers = 1
        self.sender.reply(f'共 {len(accounts)} 个账号，使用 {workers} 线程运行')
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(TPT(item['user'], 'qd', item['name'], item['ck'], usid, 1).main) for usid, item in accounts.items()]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        success = sum(isinstance(result, tuple) and len(result) == 3 for result in results)
        self.sender.reply(f'运行完成：成功 {success}，异常 {len(results) - success}')






    def dx_login(self):
        try:
            import uuid
            import urllib3

            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

            def generate_device_id():
                return f"{uuid.uuid4().hex[:8]}-{uuid.uuid4().hex[:12]}-{uuid.uuid4().hex[:8]}-{uuid.uuid4().hex[:7]}-{uuid.uuid4().hex[:12]}"

            self.sender.reply(f"""=====短信验证码登录=====
🔔{self.name},你好！
请输入手机号码
退出请回复【q】
========================""")
            phone = self.sender.listen(60000)
            if phone == 'q' or phone == 'Q':
                self.sender.reply("退出！")
                return
            elif phone is None:
                self.sender.reply('超时退出！')
                return
            elif len(phone) != 11 or not phone.isdigit():
                self.sender.reply("❌ 请输入11位手机号码")
                return

            self.phone = phone

            device_id = generate_device_id()

            common_headers = {
                'Accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Origin': 'https://ecustomercdn.itaiping.com',
                'Referer': 'https://ecustomercdn.itaiping.com/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36',
                'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
                'x-ac-device-id': device_id,
                'anonymousId': device_id,
                'x-ac-channel-id': 'KHT',
                'x-ac-mc-type': 'gateway.user',
                'x-ac-utm': '11810',
                'x-ac-live-room': '',
                'x-ac-sourceutm': '',
                'x-ac-token-ticket': ''
            }

            session = requests.Session()
            session.verify = False

            try:
                self.sender.reply("🔄 正在初始化登录服务...")
                start_url = 'https://ecustomer.cntaiping.com/userms/anonymous/startup/notify'

                response = session.get(start_url, headers=common_headers, timeout=30)
                if response.status_code != 200:
                    self.sender.reply("❌ 启动通知失败")
                    return

                switch_url = 'https://ecustomer.cntaiping.com/userms/unifiedLogin/captcha/switch/v2'
                switch_headers = common_headers.copy()
                switch_headers['Content-Type'] = 'application/json; charset=utf-8'

                switch_data = {
                    "mobile": phone,
                    "internatCode": "0086",
                    "businessCode": "LOGIN"
                }

                response = session.post(switch_url, json=switch_data, headers=switch_headers, timeout=30)
                if response.status_code != 200:
                    self.sender.reply("❌ 验证码配置检查失败")
                    return

                self.sender.reply("📱 正在发送短信验证码...")
                sms_url = 'https://ecustomer.cntaiping.com/commonms/unifiedLogin/msg/verifyCodeSms'

                sms_data = {
                    "mobile": phone,
                    "internatCode": "0086",
                    "businessCode": "LOGIN",
                    "serviceType": "KHTBASIC",
                    "type": "QUICKLOGON"
                }

                response = session.post(sms_url, json=sms_data, headers=switch_headers, timeout=30)

                if response.status_code == 200:
                    result = response.json()
                    if result.get('success') or result.get('code') == '0000':
                        self.sender.reply("✅ 验证码发送成功！")
                    else:
                        self.sender.reply(f"❌ 验证码发送失败: {result.get('message', '未知错误')}")
                        return
                else:
                    self.sender.reply("❌ 验证码发送请求失败")
                    return

                retry_count = 3
                while retry_count > 0:
                    self.sender.reply("""=====验证码验证=====
请输入收到的6位验证码
退出请回复【q】
========================""")

                    code = self.sender.listen(60000)
                    if code == 'q' or code == 'Q':
                        self.sender.reply("退出！")
                        return
                    elif code is None:
                        self.sender.reply('超时退出！')
                        return
                    elif len(code) != 6 or not code.isdigit():
                        self.sender.reply("❌ 请输入6位数字验证码")
                        continue

                    login_url = 'https://ecustomer.cntaiping.com/userms/anonymous/auth/unifiedLog/loginByMobileVerifyCode/v1'

                    login_data = {
                        "phone": phone,
                        "internatCode": "0086",
                        "verificationcode": code,
                        "x_agentcode": "1762724346751963136",
                        "userSysType": "UNIFORM_USER",
                        "userSource": "TPT_WEB"
                    }

                    response = session.post(login_url, json=login_data, headers=switch_headers, timeout=30)

                    if response.status_code == 200:
                        result = response.json()

                        if result.get('success') and result.get('code') == "0000":
                            auth_token = result.get('data', {}).get('authToken')
                            user_id = result.get('data', {}).get('userId')

                            if auth_token and user_id:
                                self.usid = user_id
                                self.ck = auth_token

                                ts = sg.bucketGet('bd_tptcks', self.user)
                                if not ts:
                                    data = {
                                        f'{self.usid}': {
                                            'name': self.name,
                                            'ck': self.ck,
                                            'sqsj': f'{datetime.now().strftime("%Y-%m-%d")}'
                                        }
                                    }
                                    sg.bucketSet('bd_tptcks', self.user, f'{data}')
                                    self.sender.reply(f'{self.name}>>>🔔首次登录成功!发送【太平管理】对账号进行管理!')
                                else:
                                    ts = _sg_literal(ts)
                                    if self.usid in ts:
                                        for k, y in ts.items():
                                            if self.usid == k:
                                                ts[f'{k}'] = {'name': self.name, 'ck': self.ck, 'sqsj': y['sqsj']}
                                                sg.bucketSet('bd_tptcks', self.user, f'{ts}')
                                                self.sender.reply(f'{self.name}>>>🔔更新账号成功！发送【太平管理】对账号进行管理!')
                                                break
                                    else:
                                        ts[f'{self.usid}'] = {
                                            'name': self.name,
                                            'ck': self.ck,
                                            'sqsj': f'{datetime.now().strftime("%Y-%m-%d")}'
                                        }
                                        sg.bucketSet('bd_tptcks', self.user, f'{ts}')
                                        self.sender.reply(f'{self.name}>>>🔔新增登录成功!发送【太平管理】对账号进行管理!')
                                return
                            else:
                                self.sender.reply("❌ 登录响应数据不完整")
                                return
                        else:
                            error_msg = result.get('message', result.get('desc', '未知错误'))
                            if "验证码" in error_msg:
                                retry_count -= 1
                                if retry_count > 0:
                                    self.sender.reply(f"❌ 验证码错误，还有{retry_count}次机会")
                                    continue
                                else:
                                    self.sender.reply("❌ 验证码错误次数过多，请稍后重试")
                                    return
                            else:
                                self.sender.reply(f"❌ 登录失败: {error_msg}")
                                return
                    else:
                        self.sender.reply("❌ 登录请求失败")
                        return

            except requests.exceptions.RequestException as e:
                self.sender.reply(f"❌ 网络请求异常: {str(e)}")
                return
            except Exception as e:
                self.sender.reply(f"❌ 登录过程中发生错误: {str(e)}")
                return

        except Exception as e:
            self.sender.reply(f"❌ 登录过程异常: {str(e)}")


    def ck_login(self):
        self.sender.reply('请在 120 秒内发送 x-ac-token-ticket，回复 q 退出')
        ck = self.sender.input(120000, 1000, False)
        if ck in ('q', 'Q', None, ''): return self.sender.reply('已退出')
        try:
            response = requests.get('https://ecustomer.cntaiping.com/tpayms/app/tpay/account/getAcct', headers={'x-ac-token-ticket': ck, 'x-ac-channel-id': 'KHT', 'x-ac-mc-type': 'gateway.user', 'User-Agent': 'Mozilla/5.0'}, timeout=20).json()
            if not response.get('success'): return self.sender.reply(f"登录失败：{response.get('message') or response.get('msg') or '凭证无效'}")
            usid = str(response['data']['userId']); data = _sg_literal(sg.bucketGet('bd_tptcks', self.user), {})
            data[usid] = {'name': self.name, 'ck': ck, 'sqsj': '2099-12-31'}
            sg.bucketSet('bd_tptcks', self.user, str(data)); self.sender.reply(f'账号【{self.name}】登录成功')
        except Exception as error: self.sender.reply(f'登录失败：{error}')


class TPT:
    def __init__(self, u, qd, n, c, uid, qyinfo):
        self.qd = qd
        self.user = u
        self.qyinfo = qyinfo
        self.usid = uid
        self.name = n
        self.ck = c
        self.llzx = None
        self.hyyd = None
        self.ydlisturl = None
        self.zldatas = []
        self.ydname = None
        self.ydid = None
        self.taskid = None
        self.rwname = None
        self.joinPoint = None
        self.htid = None
        self.validDate = None
        try:
            user_data = sg.bucketGet('bd_tptcks', u)
            if user_data:
                user_data = _sg_literal(user_data)
                self.sqsj = user_data[str(uid)]['sqsj']
            else:
                self.sqsj = None
        except:
            self.sqsj = None
        self.headers = {
            'Host': 'ecustomer.cntaiping.com',
            'x-ac-black-box': 'jWPVu1713323931keU0txvxzkc',
            'x-ac-token-ticket': self.ck,
            'x-ac-channel-id': 'KHT',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'application/json;charset=UTF-8',
            'Origin': 'https://ecustomercdn.itaiping.com',
            'User-Agent': "Mozilla/5.0 (Linux; Android 13; Pixel 4 XL Build/TP1A.220905.004; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/119.0.6045.163 Mobile Safari/537.36;yuangongejia#android#kehutong;webank/h5face;webank/1.0;netType:NETWORK_WIFI;appVersion:334;packageName:com.cntaiping.tpapp",
            'Connection': 'keep-alive',
            'Referer': 'https://ecustomercdn.itaiping.com/',
            'x-ac-mc-type': 'gateway.user',
            'Content-Type': 'application/json'
        }

    def get_proxy(self):
        try:
            proxy_api = sg.bucketGet('bd_tptconfig', 'proxy_api')
            if not proxy_api:
                return None

            try:
                import requests as requests_original
                r = requests_original.get(proxy_api, timeout=10)
            except:
                r = requests.get(proxy_api, timeout=10)

            if r.status_code == 200:
                try:
                    data = r.text.strip()
                    if not data:
                        print("[太平通]代理API返回空数据")
                        return None

                    proxy_list = []
                    for line in data.split('\r\n'):
                        if ':' in line:
                            ip, port = line.split(':')
                            proxy_str = f'http://{ip}:{port}'
                            proxy_list.append({
                                'http': proxy_str,
                                'https': proxy_str
                            })

                    if proxy_list:
                        return random.choice(proxy_list)
                    else:
                        print("[太平通]未找到可用代理")
                        return None

                except Exception as e:
                    print(f"[太平通]解析代理返回数据失败: {e}")
                    return None
            else:
                print(f"[太平通]获取代理失败,状态码: {r.status_code}")
                return None
        except Exception as e:
            print(f"[太平通]获取代理发生错误: {e}")
            return None

    def _make_request(self, method, url, **kwargs):
        try:
            use_proxy = False
            if 'campaignsms/couponAndsign' in url:  # 签到任务
                use_proxy = True
            elif 'campaignsms/goldParty' in url:  # 金币任务
                use_proxy = True
            elif 'campaignsms/coinBubble' in url:  # 金币气泡
                use_proxy = True

            max_retries = 3 if use_proxy else 1  # 使用代理时最多重试3次
            retry_count = 0

            while retry_count < max_retries:
                try:
                    if use_proxy and retry_count < max_retries - 1:  # 最后一次重试不使用代理
                        proxies = self.get_proxy()  # 每次重试都获取新的代理
                        if proxies:
                            kwargs['proxies'] = proxies
                            kwargs['timeout'] = 15
                    else:
                        kwargs['timeout'] = 10
                        if 'proxies' in kwargs:
                            del kwargs['proxies']

                    if method.lower() == 'get':
                        r = requests.get(url, **kwargs)
                    else:
                        r = requests.post(url, **kwargs)

                    if r.status_code == 200:
                        return r
                    else:
                        print(f"[太平通]请求失败,状态码: {r.status_code}")

                except Exception as e:
                    error_msg = str(e).lower()
                    if "timeout" in error_msg:
                        print(f"[太平通]第{retry_count + 1}次请求超时,尝试更换代理")
                    elif "proxy" in error_msg:
                        print(f"[太平通]第{retry_count + 1}次代理连接失败,尝试更换代理")
                    else:
                        print(f"[太平通]第{retry_count + 1}次请求错误: {e}")

                    if retry_count == max_retries - 1:
                        return None

                retry_count += 1
                if retry_count < max_retries:
                    time.sleep(2)  # 重试前等待2秒

            return None

        except Exception as e:
            print(f"[太平通]请求发生未预期错误: {e}")
            return None

    def sign(self):
        try:
            r = requests.post(
                "https://ecustomer.cntaiping.com/campaignsms/couponAndsign",
                headers=self.headers,
                json={}
            )
            self.headers[
                'User-Agent'] = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;yuangongejia#ios#kehutong#CZBIOS'
            r = requests.post(
                "https://ecustomer.cntaiping.com/campaignsms/couponAndsign",
                headers=self.headers,
                json={}
            )
            success = r.json().get('success', None)
            if success:
                self.headers[
                    'User-Agent'] = "Mozilla/5.0 (Linux; Android 13; Pixel 4 XL Build/TP1A.220905.004; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/119.0.6045.163 Mobile Safari/537.36;yuangongejia#android#kehutong;webank/h5face;webank/1.0;netType:NETWORK_WIFI;appVersion:334;packageName:com.cntaiping.tpapp"
                return True
            elif not success and '已过期' in r.text:
                return '失效'
            else:
                return False
        except Exception as e:
            return e

    def get_rwlist(self):
        try:
            r = self._make_request(
                'post',
                "https://ecustomer.cntaiping.com/campaignsms/goldParty/task/list",
                headers=self.headers,
                json={
                    'activityNumber': 'goldCoinParty',
                    'rewardFlag': '1',
                    'openMsgRemind': 0,
                }
            )
            success = r.json().get('success', None)
            if success:
                data = r.json()['data']['taskList']
                return data
            else:
                return False
        except Exception as e:
            return e

    def finish(self):
        try:
            r = self._make_request(
                'post',
                "https://ecustomer.cntaiping.com/campaignsms/goldParty/task/finish",
                headers=self.headers,
                json={'taskIds': [self.taskid], })
            success = r.json().get('success', None)
            if success:
                return True
            else:
                return False
        except Exception as e:
            return e

    def add(self):
        try_count = 2
        while try_count > 0:
            try:
                r = self._make_request(
                    'post',
                    "https://ecustomer.cntaiping.com/campaignsms/goldParty/goldCoin/add",
                    headers=self.headers,
                    json={
                        'taskIds': [self.taskid]
                    }
                )
                success = r.json().get('success', None)
                if success:
                    return True
                elif '已经获取' in r.text:
                    return False
                elif not success and '火爆' in r.text:
                    try_count -= 1
                    if try_count == 0:
                        return False
                    self.headers['User-Agent'] = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;yuangongejia#ios#kehutong#CZBIOS'
                    continue
                else:
                    return False
            except Exception as e:
                return e

    def run_rw(self):
        data = self.get_rwlist()
        if isinstance(data, list):
            for i in data:
                time.sleep(random.randint(1, 3))
                taskStatus = i['taskStatus']
                self.taskid = i['taskId']
                self.rwname = i['name']
                if taskStatus == 2:
                    pass
                elif taskStatus == 0 and self.rwname != '浏览资讯':
                    if self.finish() is True:
                        time.sleep(random.randint(1, 3))
                        if self.add() is True:
                            time.sleep(random.randint(1, 3))
                        else:
                            return False
                    else:
                        return False
                elif taskStatus == 1 and self.rwname != '浏览资讯':
                    self.add()
                    time.sleep(random.randint(1, 3))
            return True
        else:
            return False

    def get_ydlist(self):
        try:
            r = self._make_request(
                'post',
                self.ydlisturl,
                headers=self.headers,
                json={
                    "plugInId": "701b3099297148a8ba979ad9c982b561",
                    "trackDesc": "赚金币任务",
                    "city": "1",
                    "pageSize": 20,
                    "type": "GENERAL_PLUGIN"
                }
            )
            success = r.json().get('success', None)
            if success:
                data = r.json()['data']
                return data
            else:
                return False
        except Exception as e:
            return e

    def coinInfoV2(self):
        try:
            r = self._make_request(
                'post',
                "https://ecustomer.cntaiping.com/informationms/app/v2/article/web/coinInfoV2",
                headers=self.headers,
                json={
                    'articleId': self.ydid,
                    'source': 'TPT',
                    'detailUrl': f'https://ecustomercdn.itaiping.com/static/newscontent/#/info?articleId={self.ydid}&source=TPT&x_utmId=10013&x_businesskey=articleId',
                    'deviceId': '',
                    'version': 'V2'
                }
            )
            success = r.json().get('success', None)
            if success:
                return True
            else:
                return False
        except Exception as e:
            return e

    def zl(self):
        try:
            for i in self.zldatas:
                time.sleep(random.randint(1, 3))
                r = self._make_request(
                    'post',
                    "https://ecustomer.cntaiping.com/informationms/app/v2/article/web/coinInfoV2",
                    headers={
                        'Host': 'ecustomer.cntaiping.com',
                        'accept': 'application/json', 'x-ac-channel-id': 'KHT',
                        'x-ac-black-box': 'iWPVl1701438414PrzwzjCHQw1',
                        'x-ac-mc-type': 'gateway.user',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309092b) XWEB/9105 Flue',
                        'x-ac-token-ticket': '',
                        'content-type': 'application/json',
                        'Origin': 'https://ecustomercdn.itaiping.com',
                        'Sec-Fetch-Site': 'cross-site',
                        'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty',
                        'Referer': 'https://ecustomercdn.itaiping.com/',
                        'Accept-Language': 'zh-CN,zh;q=0.9'
                    },
                    json=i
                )
                success = r.json().get('success', None)
                if success:
                    return True
                else:
                    return False
        except Exception as e:
            return e

    def gold(self):
        try:
            r = self._make_request(
                'post',
                "https://ecustomer.cntaiping.com/informationms/app/v2/read/gold",
                headers=self.headers,
                json={
                    "articleId": self.ydid,
                    "source": "TPT"
                }
            )
            success = r.json().get('success', None)
            if success:
                return True
            else:
                return False
        except Exception as e:
            return e

    def queryList(self):
        try:
            r = self._make_request(
                'post',
                'https://ecustomer.cntaiping.com/campaignsms/coinBubble/queryList',
                headers=self.headers,
                json={}
            )
            success = r.json().get('success', None)
            if success:
                data = r.json()['data']
                if data:
                    return True
                else:
                    return '没有待领取金币'
            else:
                return r.json()['msg']
        except Exception as e:
            return e

    def getAllCoins(self):
        try_count = 2
        while try_count > 0:
            try:
                r = self._make_request(
                    'post',
                    "https://ecustomer.cntaiping.com/campaignsms/coinBubble/getAllCoins",
                    headers=self.headers,
                    json={}
                )
                success = r.json().get('success', None)
                if success:
                    return True
                elif not success and '火爆' in r.text:
                    try_count -= 1
                    if try_count == 0:
                        return False
                    self.headers['User-Agent'] = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;yuangongejia#ios#kehutong#CZBIOS'
                    continue
                else:
                    return r.json()['msg']
            except Exception as e:
                return e

    def getShareInfo(self):
        try:
            r = self._make_request(
                'post',
                "https://ecustomer.cntaiping.com/informationms/app/v2/share/getShareInfo",
                headers=self.headers,
                json={
                    "articleId": self.ydid,
                    "source": "TPT",
                    "shareFlag": True
                }
            )
            success = r.json().get('success', None)
            if success:
                return r.json()['data']['tagUrl']
            else:
                return False
        except Exception as e:
            return e

    def run_yd(self):
        n = 0
        data = self.get_ydlist()
        if isinstance(data, list):
            for i in range(len(data)):
                time.sleep(random.randint(1, 3))
                n += 1
                d = data[i]['cell']['0'][0]
                self.ydname = d['title']
                self.ydid = d['contentId']

                if self.llzx < 14:
                    if self.coinInfoV2() is True:
                        time.sleep(random.randint(1, 3))
                        if self.gold() is True:
                            time.sleep(random.randint(1, 3))
                        else:
                            return False
                    else:
                        return False
                getShareInfo = self.getShareInfo()
                if isinstance(getShareInfo, str):
                    shareCode = getShareInfo.split('shareCode=')[1].split('&')[0]
                    articleId = getShareInfo.split('articleId=')[1].split('&')[0]
                    zldata = {
                        'articleId': articleId,
                        'source': 'TPT',
                        'detailUrl': getShareInfo,
                        'deviceId': '',
                        "shareCode": shareCode,
                        'version': 'V2'
                    }
                    self.zldatas.append(zldata)
                else:
                    return False
            return True
        else:
            return False

    def queryUserPoints(self):
        try:
            r = self._make_request(
                'post',
                "https://ecustomer.cntaiping.com/campaignsms/integral/queryUserPoints",
                headers=self.headers,
                json={
                    "sourceOrganId": "932"
                }
            )
            success = r.json().get('success', None)
            if success:
                return r.json()['data']['scoreAccountInfo']['availableScore']
            else:
                return False
        except Exception as e:
            return e

    def is_in_current_month(self):
        date = datetime.strptime(self.validDate, '%Y-%m-%d 00:00:00')
        current_date = datetime.now()
        return date.year == current_date.year and date.month == current_date.month

    def cx(self):
        try:
            r = self._make_request(
                'post',
                'https://ecustomer.cntaiping.com/campaignsms/integral/queryIntegralDetailList',
                headers=self.headers,
                json={
                    'pageNo': 1,
                    'pageSize': 100,
                    'typePo': '3',
                }
            )
            success = r.json().get('success', None)
            if success:
                dqjb = self.queryUserPoints()
                data = r.json()['data']['list']
                today = datetime.now().strftime('%Y-%m-%d')
                coins = 0
                llzx = 0
                hyyd = 0
                rcrw = 0
                for i in data:
                    coin = i['num']
                    effectDate = i['effectDate']
                    memo = i['memo']
                    if effectDate == today:
                        if memo == '浏览资讯':
                            llzx += 1
                        elif memo == '好友阅读':
                            hyyd += 1
                        elif memo in ['给太平树浇水', '分享海报', '回执签收', '邀请注册']:
                            rcrw += 1
                        coins += coin
                        continue
                    else:
                        break
                return dqjb, coins, llzx, hyyd, rcrw
            else:
                return r.json()['msg']
        except Exception as e:
            return e

    def exhibitionTopic(self):
        try:
            r = self._make_request(
                'post',
                "https://ecustomer.cntaiping.com/campaignsms/tPkTopicAppointment/exhibitionTopic",
                headers=self.headers,
                json={
                    "pageNo": 1,
                    "pageSize": 200
                }
            )
            success = r.json().get('success', None)
            if success:
                return r.json()['data']
            else:
                msg = r.json()['msg']
                return msg
        except Exception as e:
            return e

    def standInLineTopic(self):
        try:
            r = self._make_request(
                'post',
                "https://ecustomer.cntaiping.com/campaignsms/tPkTopicAppointment/standInLineTopic",
                headers=self.headers,
                json={
                    "joinPoint": self.joinPoint,
                    "id": self.htid,
                    "dataFrom": 0
                }
            )
            success = r.json().get('success', None)
            print(r.json())
            if success:
                return True
            else:
                msg = r.json()['msg']
                return msg
        except Exception as e:
            return e

    def main(self):
        try:
            jrjb = 0
            dqjb = 0

            sign = self.sign()
            if sign is True:
                cxjg = self.cx()
                if isinstance(cxjg, tuple):
                    dqjb, jrjb, self.llzx, self.hyyd, rcrw = cxjg
                    if self.queryList() is True:
                        self.getAllCoins()
                    sender.reply(f'🔔开始运行: {self.name}\n💰今日金币: {jrjb}\n💰当前金币: {dqjb}')
                else:
                    sender.reply(f'🔔{self.name}: 查询金币时异常\n🔔{cxjg}')
                    return self.name, '异常'

                exhibitionTopic = self.exhibitionTopic()
                if isinstance(exhibitionTopic, list):
                    for i in exhibitionTopic:
                        self.htid = i['id']
                        self.joinPoint = i['joinWin']
                        isParticipateIn = i['isParticipateIn']
                        prizeStatus = i['prizeStatus']
                        if isParticipateIn is None and prizeStatus == 0:
                            self.standInLineTopic()
                            time.sleep(random.randint(5, 10))
                            continue
                        else:
                            continue

                a = 0
                while True:
                    cxjg = self.cx()
                    if isinstance(cxjg, tuple):
                        dqjb, jrjb, self.llzx, self.hyyd, rcrw = cxjg
                    else:
                        sender.reply(f'🔔{self.name}: 查询金币时异常\n🔔{cxjg}')
                        return self.name, '异常'
                    a += 1
                    if rcrw < 3:
                        if not self.run_rw():
                            cxjg_end = self.cx()
                            if isinstance(cxjg_end, tuple):
                                dqjb_end, jrjb_end = cxjg_end[0], cxjg_end[1]
                                if jrjb_end < 10:
                                    msg = f"⚠️ 账号【{self.name}】运行异常，今日金币为{jrjb_end}，请打开太平通APP后再试！"


                                    if sender.getUserID() != self.user:
                                        sender.reply(msg)

                                    sender.reply(f'🎉运行完成: {self.name}\n💰今日金币: {jrjb_end}(账号火爆)\n💰当前金币: {dqjb_end}')
                                    return self.name, '火爆'
                            sender.reply(f'🎉运行完成: {self.name}\n💰今日金币: {jrjb}\n💰当前金币: {dqjb}')
                            return self.name, jrjb, dqjb

                    if self.llzx >= 14 and self.hyyd >= 6:
                        sender.reply(f'🎉运行完成: {self.name}\n💰今日金币: {jrjb}\n💰当前金币: {dqjb}')
                        return self.name, jrjb, dqjb

                    elif a >= 3:
                        sender.reply(f'🎉运行完成: {self.name}\n💰今日金币: {jrjb}\n💰当前金币: {dqjb}')
                        return self.name, jrjb, dqjb
                    else:
                        self.ydlisturl = f"https://ecustomer.cntaiping.com/informationms/app/config/get/{a}"
                        self.run_yd()
                        a = 0
                        for zl_data in self.zldatas:
                            a += 1
                            time.sleep(random.randint(1, 3))
                            r = self._make_request(
                                'post',
                                "https://ecustomer.cntaiping.com/informationms/app/v2/article/web/coinInfoV2",
                                headers={
                                    'Host': 'ecustomer.cntaiping.com',
                                    'accept': 'application/json', 'x-ac-channel-id': 'KHT',
                                    'x-ac-black-box': 'iWPVl1701438414PrzwzjCHQw1',
                                    'x-ac-mc-type': 'gateway.user',
                                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309092b) XWEB/9105 Flue',
                                    'x-ac-token-ticket': '',
                                    'content-type': 'application/json',
                                    'Origin': 'https://ecustomercdn.itaiping.com',
                                    'Sec-Fetch-Site': 'cross-site',
                                    'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty',
                                    'Referer': 'https://ecustomercdn.itaiping.com/',
                                    'Accept-Language': 'zh-CN,zh;q=0.9'
                                },
                                json=zl_data
                            )
                            success = r.json().get('success', None)
                            if success:
                                pass
                            else:
                                return False
                        self.zldatas = []
                        if self.queryList() is True:
                            self.getAllCoins()
                        continue
                else:
                    sender.reply(f'🔔{self.name}: 运行任务时异常\n🔔{sign}')
                    return self.name, sign


            sender.reply(f'🎉运行完成: {self.name}\n💰今日金币: {jrjb}\n💰当前金币: {dqjb}')
            return self.name, jrjb, dqjb

        except Exception as e:
            sender.reply(f'🔔{self.name}: 运行任务时异常\n🔔{e}')
            return self.name, e

if __name__ == '__main__':
    sender = sg.Sender(sg.getSenderID()); user, message = sender.getUserID(), sender.getMessage(); plugin = ATM_tpt(user, sender)
    if message == '太平上车': plugin.tpsc()
    elif message == '太平管理': plugin.tpgl()
    elif message == '太平查询': plugin.tpcx()
    elif message == '太平运行' and sender.isAdmin(): plugin.tpyx()
    elif message == '太平教程': sender.reply('发送【太平上车】添加账号；【太平管理】运行或删除账号；【太平查询】查询收益。')
    else: sender.setContinue()
