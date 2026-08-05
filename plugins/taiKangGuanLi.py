# [title: 泰康管理]
# [name: taiKangGuanLi]
# [language: python]
# [class: 任务]
# [author: rujingxianghai]
# [version: v3.0]
# [public: true]
# [disable: false]
# [admin: true]
# [rule: ^(泰康|tk)(登录|登陆)$|^登(录|陆)(泰康|tk)$|^(泰康|tk)(查询|管理|检测|教程)$]
# [cron: 0 5 * * *]
# [icon: https://y.gtimg.cn/music/photo_new/T053M000002Qqrye0oyZSp.jpg]
# [description: 泰康青龙变量管理插件]
# [depe: ["pycryptodome","requests","urllib3"]]


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
    's_tkzx_qlname': form.string().title('设置对接容器').default('').description('面板容器参数，不填则使用默认配置'),
    's_tkzx_use_daipanel': form.boolean().title('使用呆呆面板').default(False).description('勾选使用呆呆面板，不勾选使用青龙面板'),
    's_tkzx_panel_group': form.string().title('呆呆面板分组').default('').description('填写后新增/更新变量时同步写入group字段，留空则不处理'),
    's_tkzx_osname': form.string().title('青龙变量名').default('').description('青龙容器内泰康的变量名'),
    's_tkzx_notify': form.string().title('通知渠道').default('').description('检测通知推送渠道'),
})
_CONFIG_FIELD_MAP = {
    ('s_tkzx', 'qlname'): 's_tkzx_qlname',
    ('s_tkzx', 'use_daipanel'): 's_tkzx_use_daipanel',
    ('s_tkzx', 'panel_group'): 's_tkzx_panel_group',
    ('s_tkzx', 'osname'): 's_tkzx_osname',
    ('s_tkzx', 'notify'): 's_tkzx_notify',
}

import os
import json
import time
import hashlib
import random
import base64
import string
import requests
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()
uservalue = sg.bucketGet(bucket='s_tkzx_user', key=userid)

PLUGIN_CONFIG = {'bucket': 's_tkzx', 'coin_key': 'dd_sign_points', 'name': '泰康'}


class TaikangOnline:
    """泰康在线API"""

    def __init__(self, union_id=None, open_id=None):
        self.base_url = "https://m.tk.cn"
        self.device_id = 'WC39ZUyXRgdExSj90tOeGomyOuuFeIVfnoBh4K6/N2S6+cPQvxZzEMpX4YkYGt7bl61lJVmGniEtWjSm22hAKQUL4jL6rQD4StL/WmrP2Tauiuo9Z2Nzm4Q==1487577677129'
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.8(0x13080812) XWEB/1216'
        self.session = requests.Session()
        self.union_id = union_id
        self.open_id = open_id
        self.account_name = mask_account(union_id) if union_id else "未知账户"

        self.session.headers.update({
            'Connection': 'keep-alive',
            'xweb_xhr': '1',
            'user-agent': self.user_agent,
            'accept': '*/*',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://servicewechat.com/wx9e3e7020c4a10356/280/page-frame.html',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        })

    def md5(self, text):
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    def generate_uuid(self):
        chars = "0123456789abcdef"
        u = [random.choice(chars) for _ in range(36)]
        u[14] = "4"
        u[19] = chars[3 & int(u[19], 16) | 8]
        u[8] = u[13] = u[18] = u[23] = "-"
        return ''.join(u)

    def encrypt(self, plain_text, key="EEue2kxI0oh2GBJh"):
        cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
        padded_data = pad(plain_text.encode('utf-8'), AES.block_size)
        encrypted = cipher.encrypt(padded_data)
        return encrypted.hex().upper()

    def get_sign(self):
        client_id = 'ytngbmji'
        non_str = self.generate_uuid()
        timestamp = int(time.time() * 1000)
        t = 60000 * (timestamp // 60000)
        md5_key = 'f2fc9b5e36E90745AB79'
        sign = self.md5(self.md5(f"{client_id}{non_str}{t}{md5_key}"))
        body = {"clientId": client_id, "nonStr": non_str, "timestamp": timestamp, "sign": sign}
        return self.encrypt(json.dumps(body), 'xdh3OmA5gEMMy0Mz')

    def get_f_sign(self):
        client_id = 'zehsmfluqja'
        timestamp = int(time.time() * 1000)
        non_str = str(timestamp) + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        t = 60000 * (timestamp // 60000)
        md5_key = 'd0ZGEyNGM4MmI3ODZOVE'
        sign = self.md5(self.md5(f"{client_id}{non_str}{t}{md5_key}"))
        body = {"clientId": client_id, "nonStr": non_str, "timestamp": timestamp, "sign": sign}
        return self.encrypt(json.dumps(body), 'xdh3OmA5gEMMy0Mz')

    def common_json_post(self, url, data):
        try:
            response = self.session.post(
                f"{self.base_url}{url}", json=data,
                headers={'content-type': 'application/json'}, timeout=30
            )
            time.sleep(2)
            return response.json()
        except:
            return None

    def common_json_sign_post(self, url, data):
        try:
            response = self.session.post(
                f"{self.base_url}{url}", json=data,
                headers={'content-type': 'application/json', 'Signature': self.get_sign()},
                timeout=30
            )
            time.sleep(2)
            return response.json()
        except:
            return None

    def common_text_post(self, url, data):
        try:
            response = self.session.post(
                f"{self.base_url}{url}", data=data,
                headers={'content-type': 'application/x-www-form-urlencoded'}, timeout=30
            )
            time.sleep(2)
            return response.json()
        except:
            return None

    def get_member_info(self, union_id):
        url = '/member_api/'
        params = f'api_s=member.userbind&api_m=selectwxbindbybindid&params=%7B%22platform%22%3A%22APPLET%22%2C%22fromid%22%3A%2271672%22%2C%22bindid%22%3A%22{union_id}%22%7D'
        response = self.common_text_post(url, params)
        if response and response.get('data'):
            return response['data'].get('token'), response['data'].get('memberid')
        return None, None

    def get_nickname(self, member_id, token):
        body = {"memberId": member_id, "token": token}
        response = self.common_json_post(
            '/activity_execute/rest/membergoldbean/getMemberGoldbeanNickName',
            {"enc": True, "encData": self.encrypt(json.dumps(body))}
        )
        if response and response.get('data'):
            return response['data'].get('nickName', '')
        return ''

    def get_points(self, member_id, token, nickname, open_id):
        body = {
            "memberid": member_id, "token": token, "coordinate": "",
            "platform": "WECHAT",
            "nickName": base64.b64encode(nickname.encode('utf-8')).decode('utf-8'),
            "openId": open_id, "fromid": "71672", "deviceId": self.device_id
        }
        response = self.common_json_sign_post(
            '/activity_execute/rest/membergoldbean/mainPage',
            {"enc": True, "encData": self.encrypt(json.dumps(body))}
        )
        if response and response.get('data'):
            return response['data'].get('allbeans', 0)
        return 0

    def get_points_info(self):
        try:
            token, member_id = self.get_member_info(self.union_id)
            if not token or not member_id:
                return None
            nickname = self.get_nickname(member_id, token)
            return self.get_points(member_id, token, nickname, self.open_id)
        except:
            return None

    def sign_in(self, member_id, token, union_id, nickname):
        body = {
            "memberid": member_id, "token": token, "unionid": union_id,
            "deviceId": self.device_id, "fromid": "71672", "platform": "WECHAT",
            "coordinate": "",
            "nickName": base64.b64encode(nickname.encode('utf-8')).decode('utf-8')
        }
        response = self.common_json_post(
            '/activity_execute/rest/membergoldbean/sign',
            {"enc": True, "encData": self.encrypt(json.dumps(body))}
        )
        if response and response.get('error_code') == 0:
            return True
        return False

    def walking_challenge(self, member_id, token):
        body = {
            "platform": "WECHAT", "memberId": member_id,
            "token": token, "openStatus": "Y"
        }
        self.common_json_sign_post(
            '/promotion/activity_execute/rest/springOuting/openChallenge',
            {"enc": True, "encData": self.encrypt(json.dumps(body))}
        )
        for task_num in ['dailyOneK', 'dailyFiveK', 'dailyTenK']:
            body = {
                "platform": "WECHAT", "memberId": member_id, "token": token,
                "fromId": "71672", "deviceId": self.device_id, "taskNum": task_num
            }
            self.common_json_sign_post(
                '/promotion/activity_execute/rest/springOuting/draw',
                {"enc": True, "encData": self.encrypt(json.dumps(body))}
            )

    def answer_question(self, member_id, token, union_id, open_id):
        body = {
            "memberId": member_id, "token": token, "unionId": union_id,
            "xcxOpenId": open_id, "fromId": "72474", "platform": "APPLET"
        }
        response = self.common_json_sign_post(
            '/promotion/activity_execute/rest/tk/answer/mainPage',
            {"enc": True, "encData": self.encrypt(json.dumps(body))}
        )
        if not response or not response.get('data'):
            return
        answer = response['data']['questionDetail']['answer']
        body = {
            "memberId": member_id, "token": token, "result": answer,
            "deviceId": self.device_id, "os": "weapp", "platform": "APPLET", "fromId": "72474"
        }
        self.common_json_sign_post(
            '/promotion/activity_execute/rest/tk/answer/answer',
            {"enc": True, "encData": self.encrypt(json.dumps(body))}
        )
        body = {
            "memberId": member_id, "token": token, "eventType": "ANSWER",
            "activityCode": "membergoldbean", "activityId": "",
            "assignmentId": "", "assignmentType": ""
        }
        self.common_json_post(
            '/activity_execute/rest/noseEvent/saveNoseEventLog',
            {"enc": True, "encData": self.encrypt(json.dumps(body))}
        )

    def execute_tasks(self, member_id, token):
        body = {"memberid": member_id, "token": token, "platform": "WECHAT"}
        response = self.common_json_post(
            '/activity_execute/rest/membergoldbean/queryTask',
            {"enc": True, "encData": self.encrypt(json.dumps(body))}
        )
        if not response or not response.get('data'):
            return
        for task in response['data']:
            if task.get('status') == "Y":
                continue
            body = {
                "memberId": member_id, "token": token,
                "eventType": task['taskCode'], "activityCode": "membergoldbean",
                "activityId": "", "assignmentId": "", "assignmentType": ""
            }
            self.common_json_post(
                '/activity_execute/rest/noseEvent/saveNoseEventLog',
                {"enc": True, "encData": self.encrypt(json.dumps(body))}
            )
            if task.get('taskToken'):
                self.common_json_post(
                    '/activity_execute/rest/callback/taskCallBack',
                    {"memberId": member_id, "taskToken": task['taskToken']}
                )


def get_user_content():
    osname = sg.bucketGet('s_tkzx', 'osname') or 'S_TKRS'
    qlname = sg.bucketGet('s_tkzx', 'qlname') or ''
    Vipmoney = float(sg.bucketGet('s_tkzx', 'Vipmoney') or '1')
    coin = int(sg.bucketGet('s_tkzx', 'coin') or '0')
    return osname, qlname, Vipmoney, coin


def _get_ql_client():
    """获取面板客户端，根据开关决定使用青龙或呆呆面板"""
    osname = sg.bucketGet('s_tkzx', 'osname') or 'S_TKRS'
    qlname = sg.bucketGet('s_tkzx', 'qlname') or ''
    use_dp = str(sg.bucketGet('s_tkzx', 'use_daipanel') or '').lower() == 'true'

    if use_dp:
        return DumbPanelClient(osname, qlname) if qlname else DumbPanelClient(osname)
    else:
        return QingLongClient(osname, qlname) if qlname else QingLongClient(osname)


def update_ql_env(account, account_info):
    """更新面板环境变量（青龙/呆呆面板 通用）"""
    union_id = account_info.get('unionId', '')
    open_id = account_info.get('openId', '')
    if not union_id or not open_id:
        return False
    env_value = f'{union_id}#{open_id}'
    auth_time = '2099-12-31' or '未授权'
    panel_group = (sg.bucketGet('s_tkzx', 'panel_group') or '').strip()
    ql = _get_ql_client()
    return ql.update_env(
        account, env_value,
        f"泰康:{mask_account(account)}|到期:{auth_time}",
        group=panel_group,
    )


def delete_ql_env(account):
    """删除面板环境变量（青龙/呆呆面板 通用）"""
    ql = _get_ql_client()
    return ql.delete_env(account)


def bind_account():
    """绑定账号"""
    sender.reply(
        "=====泰康登录=====\n"
        "请输入泰康数据\n"
        "格式: unionId#openId\n"
        "------------------\n"
        "回复\"q\"退出\n"
        "=================="
    )
    input_data = sender.input(120000, 1, False)
    if not input_data:
        sender.reply("⏰ 操作超时")
        return
    if input_data.lower() == 'q':
        sender.reply("✅ 已取消")
        return

    if '#' not in input_data or input_data.count('#') != 1:
        sender.reply(
            "=====格式错误=====\n"
            "❌ 请输入正确的数据格式\n"
            "格式: unionId#openId\n"
            "=================="
        )
        return

    parts = input_data.split('#')
    union_id = parts[0].strip()
    open_id = parts[1].strip()

    if not union_id or not open_id:
        sender.reply(
            "=====数据不完整=====\n"
            "❌ unionId和openId不能为空\n"
            "=================="
        )
        return

    tk = TaikangOnline(union_id, open_id)
    member_info = tk.get_member_info(union_id)
    if not member_info or not member_info[0]:
        sender.reply(
            "=====数据无效=====\n"
            "❌ 无法验证数据有效性\n"
            "请检查unionId和openId是否正确\n"
            "=================="
        )
        return

    accounts = _sg_literal(uservalue) if uservalue else []
    is_new = union_id not in accounts

    token_data = json.dumps({"unionId": union_id, "openId": open_id})
    sg.bucketSet(bucket='s_tkzx_token', key=union_id, value=token_data)

    if is_new:
        accounts.append(union_id)
        sg.bucketSet(bucket='s_tkzx_user', key=userid, value=str(accounts))

    auth_time = '2099-12-31'
    ql_status = "⚠️ 未授权，未提交青龙"
    if auth_time and auth_time >= str(datetime.now().date()):
        try:
            account_info = json.loads(token_data)
            update_ql_env(union_id, account_info)
            ql_status = "✅ 已提交青龙"
        except:
            ql_status = "❌ 青龙提交失败"

    status = '添加' if is_new else '更新'
    sender.reply(
        f"=====绑定成功=====\n"
        f"📱 账号: {mask_account(union_id)}\n"
        f"🔐 状态: ✅ 已{status}\n"
        f"📦 青龙: {ql_status}\n"
        f"⏰ 发送 泰康管理 可管理账号\n"
        f"=================="
    )


def query_accounts():
    """查询账号"""
    if not uservalue:
        sender.reply("=====未绑定账号=====\n❌ 未找到账号\n💡 发送 泰康登录 绑定\n==================")
        return

    accounts = _sg_literal(uservalue)

    account_list = "\n========选择账号=======\n[0] 全部账号"
    for i, account in enumerate(accounts, 1):
        auth_time = '2099-12-31'
        if not auth_time:
            auth_status = '未授权'
        elif auth_time < str(datetime.now().date()):
            auth_status = '已过期'
        else:
            auth_status = f'到期:{auth_time}'
        account_list += f"\n[{i}]{mask_account(account)}({auth_status})"
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
                if idx.strip().isdigit() and 0 < int(idx.strip()) <= len(accounts)
            ]

        if not selected:
            sender.reply("❌ 未选择有效账号")
            return

        sender.reply(f"✅ 已选择 {len(selected)} 个账号，正在查询...")

        for i, account in enumerate(selected, 1):
            try:
                token_data = sg.bucketGet('s_tkzx_token', account)
                if not token_data:
                    sender.reply(f"=====查询失败=====\n❌ {mask_account(account)} 数据丢失\n==================")
                    continue
                account_info = json.loads(token_data)
                auth_time = '2099-12-31'
                if auth_time and auth_time >= str(datetime.now().date()):
                    auth_status = '✅ 已授权'
                else:
                    auth_status = '⚠️ 未授权' if not auth_time else '❌ 已过期'

                tk = TaikangOnline(account_info.get('unionId'), account_info.get('openId'))
                points = tk.get_points_info()
                points_text = f"\n💎 当前积分: {points}" if points is not None else ""

                sender.reply(
                    f"=====账号信息[{i}/{len(selected)}]=====\n"
                    f"📱 账号: {mask_account(account)}\n"
                    f"🏷 状态: {auth_status}\n"
                    f"📅 到期: {auth_time or '未授权'}{points_text}\n"
                    f"=================="
                )
            except Exception as e:
                sender.reply(f"=====查询失败=====\n❌ {mask_account(account)}: {str(e)}\n==================")

        sender.reply("✅ 查询完成")
    except Exception as e:
        sender.reply(f"❌ 查询失败: {str(e)}")


def manage_account():
    """管理账号"""
    if not uservalue:
        sender.reply("=====未绑定账号=====\n❌ 未找到账号\n==================")
        return

    accounts = _sg_literal(uservalue)
    osname, qlname, Vipmoney, coin = get_user_content()

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

    if choice == '1':
        account_list = "\n========选择账号=======\n[0] 全部账号"
        for i, account in enumerate(accounts, 1):
            auth_time = '2099-12-31'
            if not auth_time:
                auth_status = '未授权'
            elif auth_time < str(datetime.now().date()):
                auth_status = '已过期'
            else:
                auth_status = f'到期:{auth_time}'
            account_list += f"\n[{i}]{mask_account(account)}({auth_status})"
        account_list += "\n=====================\n支持多选，用逗号分隔\n回复\"q\"退出\n====================="
        sender.reply(account_list)

        acc_choice = sender.input(120000, 1, False)
        if not acc_choice or acc_choice.lower() == 'q':
            sender.reply("✅ 已退出")
            return

        if acc_choice == '0':
            selected = accounts.copy()
        else:
            selected = [
                accounts[int(idx.strip()) - 1]
                for idx in acc_choice.split(',')
                if idx.strip().isdigit() and 0 < int(idx.strip()) <= len(accounts)
            ]

        if not selected:
            sender.reply("❌ 未选择有效账号")
            return

        account_infos = []
        for account in selected:
            try:
                token_data = sg.bucketGet('s_tkzx_token', account)
                if token_data:
                    account_infos.append({
                        'account': account,
                        'info': json.loads(token_data)
                    })
            except:
                pass

        if not account_infos:
            sender.reply("❌ 没有有效账号")
            return

        sender.reply(
            f"✅ {len(account_infos)} 个有效账号\n"
            f"=====设置授权时长=====\n"
            f"请输入授权月数(如:1)\n"
            f"回复\"q\"退出\n"
            f"=================="
        )
        months_input = sender.input(120000, 1, False)
        if not months_input or months_input.lower() == 'q':
            sender.reply("✅ 已取消")
            return

        try:
            months = int(months_input)
            if months <= 0:
                sender.reply("❌ 月数必须大于0")
                return
        except ValueError:
            sender.reply("❌ 请输入有效数字")
            return

        total_money = len(account_infos) * months * Vipmoney

        pay_config = get_pay_config()
        available = []
        if pay_config['qr_pay_switch']:
            available.append(("扫在线处理", "qrcode"))
        if pay_config['ma_pay_switch']:
            pay_types = pay_config.get('pay_types', {})
            if pay_types:
                for pay_key, pay_name in pay_types.items():
                    available.append((f"{pay_name}(在线处理)", f"mapay_{pay_key}"))
        if coin > 0:
            available.append(("积分兑换", "coin"))

        if not available:
            sender.reply("❌ 未配置支付方式，请检查配置在默认配置中开启")
            return

        pay_menu = f"=====选择支付方式=====\n💰 总价: {total_money}元({len(account_infos)}个×{months}月×{Vipmoney}元)\n"
        for idx, (name, _) in enumerate(available, 1):
            pay_menu += f"[{idx}] {name}\n"
        pay_menu += "------------------\n回复数字选择\n回复\"q\"退出\n=================="
        sender.reply(pay_menu)

        pay_choice = sender.input(120000, 1, False)
        if not pay_choice or pay_choice.lower() == 'q':
            sender.reply("✅ 已取消")
            return

        try:
            pay_idx = int(pay_choice) - 1
            if pay_idx < 0 or pay_idx >= len(available):
                sender.reply("❌ 无效选择")
                return
        except ValueError:
            sender.reply("❌ 请输入数字")
            return

        pay_name, pay_type = available[pay_idx]
        paid = False

        if pay_type == "qrcode":
            paid = _process_qrcode_payment('泰康授权', months, total_money)
        elif pay_type.startswith("mapay_"):
            actual_type = pay_type.replace("mapay_", "")
            paid = _process_mapay_payment('泰康授权', months, total_money, actual_type)
        elif pay_type == "coin":
            total_coin = len(account_infos) * months * coin
            user_coins = int(sg.bucketGet('dd_sign_points', userid) or '0')
            if user_coins < total_coin:
                sender.reply(
                    f"=====积分不足=====\n"
                    f"❌ 当前: {user_coins}\n"
                    f"💰 需要: {total_coin}\n"
                    f"=================="
                )
                return
            sg.bucketSet('dd_sign_points', userid, str(user_coins - total_coin))
            paid = True

        if not paid:
            return

        success_list = []
        fail_list = []
        for item in account_infos:
            try:
                account = item['account']
                info = item['info']
                new_expire = calculate_auth_time('s_tkzx_auth', account, months=months)
                True
                update_ql_env(account, info)
                success_list.append(f"{mask_account(account)} → {new_expire}")
            except Exception as e:
                fail_list.append(f"{mask_account(item['account'])} {str(e)}")

        result = "=====授权完成=====\n"
        result += f"✅ 成功: {len(success_list)}个\n"
        if success_list:
            result += '\n'.join(success_list) + '\n'
        if fail_list:
            result += f"❌ 失败: {len(fail_list)}个\n"
            result += '\n'.join(fail_list) + '\n'
        result += "=================="
        sender.reply(result)

    elif choice == '2':
        account_list = "\n========选择账号======="
        for i, account in enumerate(accounts, 1):
            account_list += f"\n[{i}]{mask_account(account)}"
        account_list += "\n=====================\n支持多选，用逗号分隔\n回复\"q\"退出\n====================="
        sender.reply(account_list)

        del_choice = sender.input(120000, 1, False)
        if not del_choice or del_choice.lower() == 'q':
            sender.reply("✅ 已退出")
            return

        selected = [
            accounts[int(idx.strip()) - 1]
            for idx in del_choice.split(',')
            if idx.strip().isdigit() and 0 < int(idx.strip()) <= len(accounts)
        ]

        if not selected:
            sender.reply("❌ 未选择有效账号")
            return

        sender.reply(
            f"=====确认删除=====\n"
            f"⚠️ 将删除 {len(selected)} 个账号\n"
            f"此操作不可恢复！\n"
            f"[y] 确认删除\n"
            f"[n] 取消操作\n"
            f"=================="
        )
        confirm = sender.input(120000, 1, False)
        if not confirm or confirm.lower() != 'y':
            sender.reply("✅ 已取消")
            return

        success_list = []
        fail_list = []
        for account in selected:
            try:
                delete_ql_env(account)
                sg.bucketDel(bucket='s_tkzx_token', key=account)
                True
                if account in accounts:
                    accounts.remove(account)
                success_list.append(mask_account(account))
            except Exception as e:
                fail_list.append(f"{mask_account(account)} {str(e)}")

        if accounts:
            sg.bucketSet(bucket='s_tkzx_user', key=userid, value=str(accounts))
        else:
            sg.bucketDel(bucket='s_tkzx_user', key=userid)

        result = "=====删除完成=====\n"
        result += f"✅ 成功: {len(success_list)}个\n"
        if fail_list:
            result += f"❌ 失败: {len(fail_list)}个\n"
            result += '\n'.join(fail_list) + '\n'
        result += "=================="
        sender.reply(result)

    elif choice == '3':
        success_list = []
        fail_list = []
        for account in accounts:
            try:
                token_data = sg.bucketGet('s_tkzx_token', account)
                if not token_data:
                    fail_list.append(f"{mask_account(account)} 数据丢失")
                    continue
                account_info = json.loads(token_data)
                auth_time = '2099-12-31'
                if not auth_time or auth_time < str(datetime.now().date()):
                    fail_list.append(f"{mask_account(account)} 未授权")
                    continue
                update_ql_env(account, account_info)
                success_list.append(mask_account(account))
            except Exception as e:
                fail_list.append(f"{mask_account(account)} {str(e)}")

        result = "=====提交完成=====\n"
        result += f"✅ 成功: {len(success_list)}个\n"
        if fail_list:
            result += f"❌ 失败: {len(fail_list)}个\n"
            result += '\n'.join(fail_list) + '\n'
        result += "=================="
        sender.reply(result)


def _process_qrcode_payment(project, months, money):
    return True


def _process_mapay_payment(project, months, money, pay_type='alipay'):
    return True


def show_tutorial():
    """显示教程"""
    sender.reply(
        '=====泰康教程=====\n'
        '用户指令:\n'
        '1. 泰康登录 - 绑定账号\n'
        '2. 泰康查询 - 查询积分和授权状态\n'
        '3. 泰康管理 - 授权、删除、提交面板\n'
        '4. 泰康教程 - 查看说明\n'
        '------------------\n'
        '管理员指令:\n'
        '1. 泰康授权 - 批量授权\n'
        '2. 泰康检测 - 检测过期并清理\n'
        '------------------\n'
        '绑定输入:\n'
        'unionId#openId\n'
        '=================='
    )


def ks_auth():
    return True


def main():
    """主入口"""
    msg = sender.getMessage()

    if '登录' in msg or '登陆' in msg:
        bind_account()
    elif '查询' in msg and '泰康' in msg:
        query_accounts()
    elif '管理' in msg and '泰康' in msg:
        manage_account()
    elif '教程' in msg and '泰康' in msg:
        show_tutorial()
    elif '泰康授权' in msg:
        ks_auth()
    elif '泰康检测' in msg or '检测泰康' in msg:
        if not sender.isAdmin():
            sender.reply("❌ 仅限管理员")
            return
        sender.reply("🔍 正在检测...")
        result = check_auth_status(
            's_tkzx', 's_tkzx_user', 's_tkzx_auth', 's_tkzx_token',
            '泰康', delete_ql_callback=delete_ql_env
        )
        sender.reply(result)
    elif sender.getImtype() == 'fake':
        try:
            result = check_auth_status(
                's_tkzx', 's_tkzx_user', 's_tkzx_auth', 's_tkzx_token',
                '泰康', delete_ql_callback=delete_ql_env
            )
            sg.notifyMasters(result)
        except:
            pass
    else:
        sender.setContinue()


if __name__ == "__main__":
    main()
