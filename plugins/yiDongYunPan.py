# [title: 移动云盘]
# [name: yiDongYunPan]
# [language: python]
# [class: 任务]
# [author: yuhualhh]
# [version: v1.4.5]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^云盘(登录|查询|管理|兑换|一键抢兑|停止抢兑)$]
# [icon: https://gcore.jsdelivr.net/gh/lhz03/img@391e5db5571432ac74c20afa8e958ac83e32e7a3/2025/02/13/437a3d841eaea843d11f97941c33accb.png]
# [description: 移动云盘登录、Token刷新、云朵查询、兑换与账号管理]
# [depe: ["pycryptodome","requests"]]

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
    'yuhua_ydyp_ql_config': plugin.Form.string().title('对接容器').default('').description('各参数之间用中文符丨分割，例如: http://127.0.01:5700/丨abcdef-ghijk丨abcdefghijklmnopqrs_tuvw'),
    'yuhua_ydyp_var_name': plugin.Form.string().title('环境变量').default('').description('定义提交至容器的变量名称'),
    'yuhua_ydyp_bingfa': plugin.Form.string().title('抢兑并发').default('').description('不填默认20'),
    'yuhua_ydyp_debug_pwd': plugin.Form.string().title('调试模式').default('').description('非插件开发者无需理会'),
})
_CONFIG_FIELD_MAP = {
    ('yuhua_ydyp', 'ql_config'): 'yuhua_ydyp_ql_config',
    ('yuhua_ydyp', 'var_name'): 'yuhua_ydyp_var_name',
    ('yuhua_ydyp', 'bingfa'): 'yuhua_ydyp_bingfa',
    ('yuhua_ydyp', 'debug_pwd'): 'yuhua_ydyp_debug_pwd',
}

import re
import time
from datetime import datetime, timedelta, timezone
import requests
import json
import uuid
import random
import socket
import sys
import base64
scripts = "云盘"

def printf(msg, level='INFO'):
    c = 32 if level in ['INFO', 'DEBUG'] else 33 if level in ['WARN', 'WARNING'] else 31
    sys.stderr.write(f"\033[{c}m[{level}] {str(msg)}\033[0m\n")
    sys.stderr.flush()

debug_key = sg.bucketGet('yuhua_ydyp', 'debug_pwd') or ''
DEBUG = (debug_key == '123456789abcC@')
if DEBUG:
    printf("🔥🔥🔥 调试模式已开启，密钥验证通过 🔥🔥🔥", "WARN")
GLOBAL_SESSION = None

def get_global_session():
    global GLOBAL_SESSION
    if GLOBAL_SESSION is None:
        GLOBAL_SESSION = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=3)
        GLOBAL_SESSION.mount('http://', adapter)
        GLOBAL_SESSION.mount('https://', adapter)
        GLOBAL_SESSION.headers.update({
            'User-Agent': (
                'Mozilla/5.0 (Linux; Android 16; RMX5060 Build/BP2A.250605.015; wv) '
                'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/149.0.7827.13 '
                'Mobile Safari/537.36 MCloudApp/12.5.4 AppLanguage/zh-CN'
            )
        })
    return GLOBAL_SESSION

def close_global_session():
    global GLOBAL_SESSION
    if GLOBAL_SESSION is not None:
        GLOBAL_SESSION.close()
        GLOBAL_SESSION = None

CHINA_TZ = timezone(timedelta(hours=8))
_time_offset = None
_offset_expiry = 0
def get_ntp_time():
    global _time_offset, _offset_expiry
    now = time.time()
    if _time_offset is None or now > _offset_expiry:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.settimeout(2)
                s.sendto(b'\x1b' + 47 * b'\0', ('ntp.aliyun.com', 123))
                data, _ = s.recvfrom(1024)
                if data:
                    t = data[40:48]
                    secs = int.from_bytes(t[:4], 'big') - 2208988800
                    frac = int.from_bytes(t[4:], 'big')
                    ntp_time = secs + frac / 2**32
                    _time_offset = ntp_time - time.time()
                    _offset_expiry = time.time() + 600
        except (socket.timeout, OSError):
            if _time_offset is None: _time_offset = 0
            _offset_expiry = time.time() + 60
    return datetime.fromtimestamp(time.time() + _time_offset)
def get_china_time():
    return get_ntp_time().astimezone(CHINA_TZ)
def local_now():
    return get_china_time()

class YP:

    def __init__(self, cookie_str, phone='未知'):
        self.session = requests.Session()  # 为每个账号实例创建独立的 session
        self.token = None
        self.jwtToken = None
        self.total_amount = 0
        self.today_num = 0
        self.timestamp = str(int(round(time.time() * 1000)))
        self.cookies = {'sensors_stay_time': self.timestamp}
        self.ua = (
            'Mozilla/5.0 (Linux; Android 16; RMX5060 Build/BP2A.250605.015; wv) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/149.0.7827.13 '
            'Mobile Safari/537.36 MCloudApp/12.5.4 AppLanguage/zh-CN'
        )
        self.session.headers.update({'User-Agent': self.ua})  # 将UA设置到独立的 session 中
        parts = cookie_str.split("#")
        self.Authorization = parts[0].strip()
        self.account = phone or "未知"
        self.jwtHeaders = {
            'User-Agent': self.ua,
            'Accept': '*/*',
            'Host': 'caiyun.feixin.10086.cn:7071',
        }

    def close(self):
        if self.session:
            self.session.close()

    def send_request(self, url, headers=None, data=None, method='GET', cookies=None, retries=3):
        time.sleep(random.uniform(0.3, 0.7))
        for attempt in range(retries):
            try:
                if DEBUG:
                    printf("\n===== [REQUEST START] =====", "DEBUG")
                    printf(f"METHOD: {method} | URL: {url}", "DEBUG")
                    printf(f"HEADERS: {json.dumps(headers or {}, ensure_ascii=False)}", "DEBUG")
                    if data is not None:
                        printf(f"BODY(JSON): {json.dumps(data, ensure_ascii=False)}", "DEBUG")
                    if cookies is not None:
                        try:
                            printf(f"COOKIES: {json.dumps(cookies, ensure_ascii=False)}", "DEBUG")
                        except Exception:
                            printf(f"COOKIES: {str(cookies)}", "DEBUG")

                with self.session.request(method, url, headers=headers, json=data, cookies=cookies, timeout=15) as response:
                    if DEBUG:
                        printf(f"----- [RESPONSE - Attempt {attempt + 1}] -----", "DEBUG")
                        printf(f"STATUS: {response.status_code}", "DEBUG")
                        printf(f"RSP HEADERS: {json.dumps(dict(response.headers), ensure_ascii=False)}", "DEBUG")
                        try:
                            printf(f"RSP BODY: {json.dumps(response.json(), ensure_ascii=False)}", "DEBUG")
                        except Exception:
                            printf(f"RSP BODY: {response.text}", "DEBUG")
                        printf("===== [REQUEST END] =====\n", "DEBUG")

                    response.raise_for_status()
                    return response.json()
            except (requests.Timeout, requests.RequestException, Exception) as e:
                if DEBUG:
                    printf(f"⚠️ Attempt {attempt + 1} Failed: {str(e)}", "WARN")
                if attempt < retries - 1:
                    time.sleep(1)
                else:
                    return {"error": f"请求失败: {str(e)}"}

    def sso(self):
        url = 'https://orches.yun.139.com/orchestration/auth-rebuild/token/v1.0/querySpecToken'
        headers = {
            'Authorization': self.Authorization,
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Host': 'orches.yun.139.com'
        }
        data = {"account": self.account, "toSourceId": "001005"}
        ret = self.send_request(url, headers=headers, data=data, method='POST')
        if not ret:
            return False, "网络请求失败"
        if ret.get("error"):
            error_msg = ret["error"]
            if "请求失败" in error_msg:
                return False, f"网络请求异常: {error_msg}"
            else:
                return False, error_msg
        if ret.get('success'):
            self.token = ret['data']['token']
            return True, "ok"
        else:
            message = ret.get('message', '未知错误')
            if any(keyword in message.lower() for keyword in ['unauthorized', 'invalid', 'expired', '无效', '过期', '失效']):
                return False, f"CK已失效: {message}"
            else:
                return False, f"请求异常: {message}"

    def jwt(self):
        if not self.token:
            return False, "无可用 ssoToken"
        url = f"https://caiyun.feixin.10086.cn:7071/portal/auth/tyrzLogin.action?ssoToken={self.token}"
        ret = self.send_request(url=url, headers=self.jwtHeaders, method='POST')
        if not ret:
            return False, "返回数据为空"
        if ret.get("error"):
            return False, ret["error"]
        if ret.get('code') != 0:
            return False, ret.get('msg', '获取jwtToken失败')
        self.jwtToken = ret['result']['token']
        self.jwtHeaders['jwtToken'] = self.jwtToken
        self.cookies['jwtToken'] = self.jwtToken
        return True, "ok"

    def receive(self):
        url = "https://m.mcloud.139.com/ycloud/signin/page/infoV3?client=app"
        headers = {
            'Host': 'm.mcloud.139.com',
            'Connection': 'keep-alive',
            'sec-ch-ua-platform': '"Android"',
            'Cache-Control': 'no-cache',
            'sec-ch-ua': '"Android WebView";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'showLoading': 'true',
            'appVersion': '12.5.4.0',
            'User-Agent': self.ua,
            'jwtToken': self.jwtToken,
            'activityId': 'sign_in_3',
            'Accept': '*/*',
            'X-Requested-With': 'com.chinamobile.mcloud',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://m.mcloud.139.com/portal/mobilecloud/index.html?path=newsignin&sourceid=1097&enableShare=1&token=&targetSourceId=001005',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'zh,zh-CN;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        ret = self.send_request(url, headers=headers, cookies=self.cookies)
        if not ret:
            return False, "返回数据为空"
        if ret.get("error"):
            return False, ret["error"]
        if ret.get('code') == 0 and ret.get('msg') == 'success':
            self.total_amount = ret.get("result", {}).get("total", 0)
            self.to_receive = ret.get("result", {}).get("toReceive", 0)
            return True, f"当前云朵数量: {self.total_amount}"
        else:
            return False, ret.get('msg', '未知错误')

    def get_pending_prizes(self):
        if not self.jwtToken:
            return False, "无 jwtToken, 无法查询待领奖品"

        try:
            timestamp = str(int(time.time() * 1000))
            prize_url = f"https://caiyun.feixin.10086.cn/market/prizeApi/checkPrize/getUserPrizeLogPage?currPage=1&pageSize=15&_={timestamp}"

            ret = self.send_request(prize_url, headers=self.jwtHeaders, cookies=self.cookies)
            if not ret:
                return False, "返回数据为空"
            if ret.get("error"):
                return False, ret["error"]

            result = ret.get('result', {}).get('result', [])
            pending_prizes =[]

            for value in result:
                prize_name = value.get('prizeName')
                flag = value.get('flag')
                if flag == 1 and prize_name:  # flag=1表示待领取
                    expire_time = value.get('expireTime', '')
                    if expire_time and len(expire_time) >= 10:
                        expire_date = expire_time[:10].replace('-', '.')
                        prize_str = f"{prize_name},至{expire_date}失效"
                    else:
                        prize_str = prize_name
                    pending_prizes.append(prize_str)

            return True, pending_prizes

        except Exception as e:
            return False, f"查询待领奖品异常: {str(e)}"

    def get_today_cloud(self):
        if not self.jwtToken:
            return False, "无 jwtToken, 无法查询今日云朵"

        today_str = str(local_now().date())  # 北京时间的今日日期 (YYYY-MM-DD)
        total = 0
        page_number = 1
        page_size = 10  # 增大页面大小，减少请求次数

        while True:
            url = f"https://m.mcloud.139.com/ycloud/signin/public/cloudRecord?type=1&pageNumber={page_number}&pageSize={page_size}"
            headers = {
                'jwttoken': self.jwtToken,
                'Accept': '*/*'
            }
            ret = self.send_request(url, headers=headers, method='GET')
            if not ret:
                return False, "接口无响应"
            if ret.get("error"):
                return False, ret["error"]
            if ret.get('code') != 0:
                return False, ret.get('msg', '获取失败')

            result = ret.get("result", {})
            records = result.get("records", [])

            if not records:
                break

            page_today_total = 0
            has_today_record = False

            for item in records:
                insert_time = item.get('inserttime', '')
                if insert_time:
                    try:
                        from datetime import datetime, timezone, timedelta
                        if insert_time.endswith('+00:00'):
                            utc_time = datetime.fromisoformat(insert_time)
                        else:
                            utc_time = datetime.fromisoformat(insert_time.replace('Z', ''))
                            utc_time = utc_time.replace(tzinfo=timezone.utc)

                        beijing_tz = timezone(timedelta(hours=8))
                        beijing_time = utc_time.astimezone(beijing_tz)
                        day = str(beijing_time.date())
                    except Exception as e:
                        day = insert_time[:10]
                        print(f"时间解析失败: {insert_time}, 错误: {e}")  # 调试用
                else:
                    continue

                num = item.get('num', 0)
                if day == today_str and num > 0:
                    page_today_total += num
                    has_today_record = True
                elif day < today_str:
                    break

            total += page_today_total

            if not has_today_record:
                break

            current_page = result.get("current", page_number)
            total_pages = result.get("pages", 1)
            if current_page >= total_pages:
                break

            page_number += 1

            if page_number > 10:
                break

        self.today_num = total
        return True, f"今日云朵: {total}"

def gen_unique_id(prefix=""):
    timestamp = int(time.time() * 1_000_000)
    return f"{prefix}{timestamp}"

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()
uservalue = sg.bucketGet(bucket='yuhua_ydyp_user', key=userid)

def get_config():
    try:concurrent=max(1,min(int(sg.bucketGet('yuhua_ydyp','bingfa') or 20),50))
    except (TypeError,ValueError):concurrent=20
    return sg.bucketGet('yuhua_ydyp','var_name') or 'ydyp',sg.bucketGet('yuhua_ydyp','ql_config') or '','云盘管理','云盘查询','云盘登录',0,0,concurrent


def init_qinglong():
    if not ql_config:return '',''
    parts=ql_config.split('丨')
    if len(parts)!=3:return '',''
    url,client_id,secret=map(str.strip,parts)
    try:return url,get_ql_token(url,client_id,secret)
    except Exception as error:print(f'青龙连接失败: {error}');return '',''


def get_ql_token(url, client_id, client_secret):
    try:
        token_url = f'{url}/open/auth/token?client_id={client_id}&client_secret={client_secret}'
        session = get_global_session()
        with session.get(token_url, timeout=10) as r:
            if r.status_code != 200:
                raise Exception(f"请求失败: {r.status_code}")
            data = r.json()
        if "token" not in data.get('data', {}):
            raise Exception("获取token失败")
        return data['data']['token']
    except Exception as e:
        raise Exception(f"获取token失败: {str(e)}")

def add_to_qinglong(token_value, account, phone, target_user=None):
    if not ql_url or not ql_token:
        return False
    try:
        time.sleep(random.uniform(0.3, 0.8))
        url = f"{ql_url}/open/envs"
        headers = {
            "Authorization": f"Bearer {ql_token}",
            "Content-Type": "application/json"
        }
        session = get_global_session()
        session.headers.update(headers)
        with session.get(url, timeout=10) as r1:
            if r1.status_code != 200:
                raise Exception("获取变量失败")
            envs = r1.json().get('data', [])
        exists_id = None
        for env in envs:
            if env.get('name') == var_name and f"UID:{account}" in env.get('remarks', ''):
                exists_id = env.get('id')
                break
        remarks_user = target_user if target_user else userid
        data = {
            "name": var_name,
            "value": token_value,
            "remarks": f"UID:{account}丨用户:{remarks_user}丨手机:{phone}"
        }
        if exists_id:
            data['id'] = exists_id
            with session.put(url, json=data, timeout=10) as r2:
                if r2.status_code != 200:
                    raise Exception("更新变量失败")
        else:
            with session.post(url, json=[data], timeout=10) as r2:
                if r2.status_code != 200:
                    raise Exception("提交变量失败")
        return True
    except Exception as e:
        sender.reply(f"❌ 青龙操作失败: {str(e)}")
        return False

def delete_from_qinglong(account):
    if not ql_url or not ql_token:
        return False
    try:
        time.sleep(random.uniform(0.3, 0.8))
        url = f"{ql_url}/open/envs"
        headers = {
            "Authorization": f"Bearer {ql_token}"
        }
        session = get_global_session()
        session.headers.update(headers)
        with session.get(url, timeout=10) as resp:
            if resp.status_code != 200:
                raise Exception("获取变量失败")
            envs = resp.json().get('data', [])
        env_id = None
        for env in envs:
            if env.get('name') == var_name and f"UID:{account}" in env.get('remarks', ''):
                env_id = env.get('id')
                break
        if env_id:
            with session.delete(url, json=[env_id], timeout=10) as rdel:
                if rdel.status_code != 200:
                    raise Exception("删除变量失败")
        return True
    except Exception as e:
        sender.reply(f"❌ 青龙操作失败: {str(e)}")
        return False

def _enable_envs_in_qinglong(id_list):
    if not id_list:
        return False
    try:
        url = f"{ql_url}/open/envs/enable"
        headers = {
            "Authorization": f"Bearer {ql_token}",
            "Content-Type": "application/json"
        }
        session = get_global_session()
        session.headers.update(headers)
        with session.put(url, json=id_list, timeout=10) as resp:
            return resp.status_code == 200
    except Exception:
        return False

def login():
    login_guide = """
=====登录方式=====
[1] 短信登录
[2] Cookie登录
------------------
回复数字选择方式
回复"q"退出"""

    sender.reply(login_guide)
    choice = sender.input(60000, 0, False)

    if not choice:  # 如果超时未输入
        sender.reply("❌ 输入超时")
        return
    elif choice.lower() == 'q':  # 输入q时退出
        sender.reply("✅ 已退出操作")
        return

    try:
        if choice == '1':
            sms_login()
        elif choice == '666':
            password_login()
        elif choice == '2':
            cookie_login()
        else:
            sender.reply("❌ 无效的选择")
            return

    except Exception as e:
        sender.reply(f"❌ 登录失败: {str(e)}")
        return

def cookie_login():
    guide = """
=====账号登录=====
❶ 下载Via浏览器访问 yun.139.com/m/#/login 完成登录，左上角查看Cookies找到参数authorization的值『Basic xxxxx』
❷请勿点击退出将导致CK失效，多号用户请清软件数据重复操作，不用带『;』号，分隔『#』号是英文符，参数『Basic xxxxx』内的空格不能删
❸按如下格式发送
『参数值#手机号』 例: Basic xxxxx#110
------------------
回复"q"退出"""
    sender.reply(guide)
    user_input = sender.input(60000, 1, False)
    if not user_input:  # 如果超时未输入
        sender.reply("❌ 输入超时")
        return
    elif user_input.lower() == 'q':  # 输入q时退出
        sender.reply("✅ 已退出操作")
        return
    parts = user_input.split('#')
    auth_str = parts[0].strip()
    phone = parts[1].strip() if len(parts) > 1 else "未知"
    yp_check = YP(auth_str, phone=phone)
    ok, msg = yp_check.sso()
    yp_check.close()
    if not ok:
        sender.reply(f"❌ 登录失败: {msg}")
        return
    accounts = _sg_literal(uservalue or '[]')
    matched_uid = None
    for uid in accounts:
        old_phone = sg.bucketGet('yuhua_ydyp_phone', uid) or "未知"
        if old_phone == phone and phone != "未知":
            matched_uid = uid
            break
    if matched_uid:
        sg.bucketSet('yuhua_ydyp_token', matched_uid, user_input)
        try:
            sg.bucketDel('yuhua_ydyp_password', matched_uid)
        except Exception:
            pass
        phone = sg.bucketGet('yuhua_ydyp_phone', matched_uid) or "未知"
        phone_mask = phone[:3] + "****" + phone[-4:] if len(phone) >= 7 else phone
        if add_to_qinglong(user_input, matched_uid, phone):
            try:
                ql_envs = get_global_session().get(f"{ql_url}/open/envs", headers={"Authorization": f"Bearer {ql_token}"}, timeout=10)
                if ql_envs.status_code == 200:
                    items = ql_envs.json().get('data', [])
                    ids = [e.get('id') for e in items if e.get('name') == var_name and f"UID:{matched_uid}" in str(e.get('remarks',''))]
                    if ids:
                        _enable_envs_in_qinglong(ids)
            except Exception:
                pass
        sender.reply(f"""
=====登录成功=====
🤪 账号: {phone_mask}
✅ 状态: 更新成功
------------------
发送"{manage_cmd}"管理账号
发送"{query_cmd}"查询账号""")
        return
    unique_id = gen_unique_id()
    if unique_id not in accounts:
        accounts.append(unique_id)
        sg.bucketSet('yuhua_ydyp_user', userid, str(accounts))
    sg.bucketSet('yuhua_ydyp_token', unique_id, user_input)
    sg.bucketSet('yuhua_ydyp_phone', unique_id, phone)
    phone_mask = phone[:3] + "****" + phone[-4:] if len(phone) >= 7 else phone
    sender.reply(f"""
=====登录成功=====
🤪 账号: {phone_mask}
✅ 状态: 添加成功
------------------
发送"{manage_cmd}"管理账号
发送"{query_cmd}"查询账号""")




def _query_single_account(unique_id):
    phone=sg.bucketGet('yuhua_ydyp_phone',unique_id) or '未知';masked=phone[:3]+'****'+phone[-4:] if len(phone)>=7 else phone
    ok,credential,message=check_and_refresh_token(unique_id)
    if not ok and not credential:return f'{masked}：{message}'
    client=YP(credential,phone=phone)
    try:
        ok,message=client.sso()
        if not ok:return f'{masked}：{message}'
        if not client.jwt()[0]:return f'{masked}：获取 JWT 失败'
        if not client.receive()[0]:return f'{masked}：查询云朵失败'
        client.get_today_cloud();_,prizes=client.get_pending_prizes()
        return f'{masked}：当前云朵 {client.total_amount}，今日 {client.today_num}，待领奖品 '+('；'.join(prizes) if prizes else '暂无')
    finally:client.close()

def query_account():
    from concurrent.futures import ThreadPoolExecutor, as_completed

    if not uservalue:
        sender.reply(f"""
=====未绑定账号=====
❌ 未找到任何账号信息
💡 发送 {login_cmd} 绑定账号
==================""")
        return
    accounts = _sg_literal(uservalue)
    if not accounts:
        sender.reply(f"""
=====未绑定账号=====
❌ 未找到任何账号信息
💡 发送 {login_cmd} 绑定账号
==================""")
        return

    sender.reply("正在查询....")

    bf_num_local = bingfa

    with ThreadPoolExecutor(max_workers=bf_num_local) as executor:
        futures = {executor.submit(_query_single_account, acc_id): acc_id for acc_id in accounts}

        for future in as_completed(futures):
            try:
                result_msg = future.result()
                if result_msg:
                    sender.reply(result_msg)
            except Exception as e:
                sender.reply(f"❌ 查询某个账号时出错: {e}")

def manage_account():
    accounts=list(_sg_literal(sg.bucketGet('yuhua_ydyp_user',userid),[]))
    if not accounts:return sender.reply('未绑定账号，请发送【云盘登录】')
    rows=[]
    for i,account in enumerate(accounts,1):
        phone=sg.bucketGet('yuhua_ydyp_phone',account) or str(account);rows.append(f'{i}. {phone[:3]}****{phone[-4:]}')
    sender.reply('移动云盘账号：\n'+'\n'.join(rows)+'\n回复序号管理，q 退出');choice=sender.input(60000,0,False)
    if not choice or str(choice).lower()=='q':return
    try:show_account_menu(accounts[int(choice)-1])
    except (ValueError,IndexError):sender.reply('序号无效')


def show_account_menu(account):
    sender.reply('1. 云盘兑换\n2. 删除账号\nq. 退出');choice=sender.input(60000,0,False)
    if choice=='1':show_exchange_menu_ydyp(account)
    elif choice=='2':confirm_delete(account)


def confirm_delete(account):
    phone = sg.bucketGet('yuhua_ydyp_phone', account) or "未知"
    phone_mask = phone[:3] + "****" + phone[-4:] if len(phone) >= 7 else phone
    sender.reply(f"⚠️ 确认要删除账号 {phone_mask} 吗？(y/n)")
    confirm = sender.input(30000, 0, False)
    if not confirm:  # 如果超时未输入
        sender.reply("❌ 输入超时")
        return
    elif confirm.lower() == 'n':
        sender.reply("✅ 已退出操作")
        return
    elif confirm.lower() == 'q':  # 输入q时退出
        sender.reply("✅ 已退出操作")
        return
    elif confirm.lower() != 'y':
        sender.reply("❌ 无效的选择")
        return
    delete_account(account)

def delete_account(account):
    accounts=list(_sg_literal(sg.bucketGet('yuhua_ydyp_user',userid),[]))
    if account not in accounts:return sender.reply('未找到账号')
    accounts.remove(account);sg.bucketSet('yuhua_ydyp_user',userid,str(accounts)) if accounts else sg.bucketDel('yuhua_ydyp_user',userid)
    for bucket in ('yuhua_ydyp_token','yuhua_ydyp_phone','yuhua_ydyp_password','yuhua_ydyp_prize_regular','yuhua_ydyp_device_id'):sg.bucketDel(bucket,account)
    if ql_url and ql_token:delete_from_qinglong(account)
    sender.reply('账号已删除')






notified_accounts = set()


STOP_EXCHANGE = False

def fetch_device_id():
    url = "https://slw.h5cmpassport.com:9090/deviceprofile/v4"
    headers = {
        "Host": "slw.h5cmpassport.com:9090",
        "Connection": "keep-alive",
        "sec-ch-ua-platform": '"Android"',
        "User-Agent": "Mozilla/5.0 (Linux; Android 16; RMX5060 Build/BP2A.250605.015; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/148.0.7778.49 Mobile Safari/537.36 MCloudApp/12.6.0 AppLanguage/zh-CN",
        "sec-ch-ua": '"Chromium";v="148", "Android WebView";v="148", "Not/A)Brand";v="99"',
        "Content-Type": "application/json;charset=UTF-8",
        "sec-ch-ua-mobile": "?1",
        "Accept": "*/*",
        "Origin": "https://m.mcloud.139.com",
        "X-Requested-With": "com.chinamobile.mcloud",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://m.mcloud.139.com/portal/yunClound/index.html?path=National_v12giftPop&sourceid=1003&enableShare=1&token=",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh,zh-CN;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    data = '{"appId":"default","organization":"FXlyfmWg2AzwbrxDKSv5","ep":"anGhOHfzlh7WPt/KVxj2A4ycutn5Fey6wnwpSLdN0I4Rea71hM7BybZaBZ2KSKZLno56LTsBJR+8eMsoldq95m3wfJmB8ZY+S5kczO2BrK2wiGyRZntpKoaIyyo6LZcFFRF2fan559tmygQCNSC7T9m7xLMGr4y/pN35z1GPOns=","data":"fe99d81711e0806e60a7e54ead0aa4b51c59aabdef53ad876a3b6a1af6f803cc3b3ab7eeed62f0bb6ef3fe6632a305882332f606dc34ece012d4a3cbff8be6dd89012c246e5a98a060b5267fe1869b475460741671827c0e9ecf87798759736005dc5a62f772a6c11a176a837097e06a41f5971a6b65c221cce080854de3986be34ad3dab87b6c6fff1f71b6c9a8c578069aa2bb0e92565d4714cad13ec6990817eec7a3d08aedcaa40c5c13da1a0dd3854d632e9a1cbebf7d5ad86749cba74eee449090b7a0270a3799e190a2a27380c73af34fbd0063cc92a9bbefe1e8f877c36d3f96a9f6bc1ed7c66f253f3d8a50bd7e09e399090f8c83601d0eb0e92646193dc6626d66c8677b9f31988997f3cec2d576ccab233ded79785301c2741b191d62381fa47670229557096a656a523c1b6faaa2e8c919a7a8f7932dfefae408c8bb48afbfb1658a5467c70330155c67567db599b773e5b2a7fdbbfe267f69f409ff1704261f68c598dfb8af3f22ee11eee84e5990c44bd8221d14cbfdde87ad38964db45e1624598d51cfb0a90c035aed84b28dd0cd7e390077e1df9c70b6c924df56a48368e86e0355333edcfbbcb6b8be5c008055a536164028ae4f68b129918948e7acac96e00faecee3e81feeb3d37a575d79b67bee7aeff6dd981a8694fda665b0c3ca5c48a01f4ec47f68a3c65ea0e567fce308395703873fab3d3e0e03346ea2a365395cff54e79d8b24cc8c691a5c0a731857a1414c275203dad64ebfe1e3b3e1fd08c22fbf9ffe95753903f89ee87084c37fe012af911b8ad6e409e49d46a7cd3ef5959f7278dc7a7c44c9c5bc021366913afd2119f17e745e4909670db42b8f53341a38c7f3d077f5cb95b99a6533fd9d74aab2d3d0b11af8cecedb5ca7d4a5ba31fdcf4a86515b98120e14696f573b2a742c2208711ec464a394499986fd28cd6a8c737c2a2ed60439eb95eb4e597948ac4ca52a696ad14604f69067292567a969e6a7a5bfa15abb1614f03c386f7db400db4f5759e5291b01d9b002917361ba0f75c071ef0f185ab5e099eabc7eb5ecd43ddc37f64b7f9765f3ec1a23a240835edd672a0fc0bcfbadc1cabcdb63512bbb3dbf13770627b0fb6f7ef649f16990f1d6be3a769472af40d0f5021cddd073abcfe528d4d5b3710ead8ba9c54c75b858cfb4636ab66b0df9ac52fa5e5d6ebdde5e87f3072535548bfbcbf46e92af5eeb96f33b646fd7375d8caa246f22f659b469e4518733479db088cd6a492e252e6182048de77af3a929d44bb0fb20e2c9d871c3f20f3c139c4cabec0240a027ddd283d105e6ea6e107a0a00357c98f4bb77c1dee85f2ff971b4aa25b6ce7d373f06baa4c51f30c684e06b84210fa6bf65f049ad7ba77370621341090dbe3e28fc1347d5e0211662508a886f1a49a960a395138bbdf69114c3024f1b67974b2f717ad5c34f7825bd74301e9fdd7cc24af7e8646c93789f70495fcdba0722429d07e96c5f0c86cc6264426acc3540343b1920119479eac94da40ca3600198f45b1df7c2020c79d070e715a24e863d21b1eeafbfc18c0c3933e774bf064deb48d697acd438c7a4298235e8bafef31cebdbc49407b1562fd3e5a1c696887e67c069e8e75ed5744969c281bd67264f6c52403fb8d89b5fd06eee39480993d1d1523cae278dd75a0e5941141beb610870eb42b581a79429f9cdf5e95a3b9e3b682b655be76b32e0286327ae0cdd1745b6a70e26d84457269f516a1f5be15453759d9b46fc8ced01ea8d1f5ec9870878ef36d81ef0c73327c5899e9dc3cf95f392e5e003117d9cbaa76958307fe4b20944e54a83ca423fece80fafaf620726d2bc9d6fe9bea04002a9adeffa281de19cbcd25b9b2ab687c5d29a9e46d5ba06723cf21fd2a6e586ac269e341c2aa9","os":"web","encode":5,"compress":2}'
    try:
        session = get_global_session()
        resp = session.post(url, headers=headers, data=data, timeout=15)
        resp.raise_for_status()
        result = resp.json()
        if result.get('code') == 1100 and result.get('detail', {}).get('deviceId'):
            return True, result['detail']['deviceId']
        return False, f"获取deviceId失败: {result}"
    except Exception as e:
        return False, f"获取deviceId异常: {str(e)}"

def get_or_fetch_device_id(account_id):
    ok, result = fetch_device_id()
    if ok:
        return True, result
    return False, result

DDDDOCR_API = "http://ddddocr.250666.xyz/capcode"

def solve_slide_captcha(yp_obj, dev_id):
    try:
        slide_headers = dict(yp_obj.jwtHeaders)
        slide_headers.update({
            'Host': 'm.mcloud.139.com',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'deviceId': 'B' + dev_id if not dev_id.startswith('B') else dev_id,
            'appVersion': '12.5.4.0',
            'activityId': 'sign_in_3',
            'showLoading': 'true',
            'sec-ch-ua-platform': '"Android"',
            'sec-ch-ua': '"Android WebView";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'Accept': '*/*',
            'Origin': 'https://m.mcloud.139.com',
            'X-Requested-With': 'com.chinamobile.mcloud',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://m.mcloud.139.com/portal/mobilecloud/index.html?path=newsignin&sourceid=1097&enableShare=1&token=&targetSourceId=001005',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'zh,zh-CN;q=0.9,en-US;q=0.8,en;q=0.7'
        })
        slide_cookies = dict(yp_obj.cookies)

        resp = yp_obj.send_request(
            "https://m.mcloud.139.com/ycloud/auth-service/slide/getSlide",
            headers=slide_headers,
            cookies=slide_cookies,
            data={},
            method='POST'
        )

        if not resp or resp.get("code") != 0:
            if DEBUG:
                printf(f"getSlide失败: {resp}", "WARN")
            return None

        result = resp.get("result", {})
        puzzle_b64 = result.get("puzzle", "")
        picture_b64 = result.get("picture", "")

        if not puzzle_b64 or not picture_b64:
            if DEBUG:
                printf("getSlide响应中缺少图片数据", "WARN")
            return None

        try:
            ocr_resp = get_global_session().post(
                DDDDOCR_API,
                json={"slidingImage": puzzle_b64, "backImage": picture_b64, "simpleTarget": True},
                timeout=15
            )
            offset = int(float(ocr_resp.json().get("result", 257)))
            if DEBUG:
                printf(f"滑块识别偏移量: {offset}", "DEBUG")
            return offset
        except Exception as e:
            if DEBUG:
                printf(f"ddddocr识别失败: {e}, 使用默认偏移257", "WARN")
            return 257

    except Exception as e:
        if DEBUG:
            printf(f"滑块验证流程异常: {e}", "WARN")
        return None

def within_exchange_window():
    now = local_now()
    start0_pm = now.replace(hour=23, minute=50, second=0, microsecond=0)
    end0_am = now.replace(hour=0, minute=10, second=0, microsecond=0)
    start_8 = now.replace(hour=9, minute=50, second=0, microsecond=0)
    end_8 = now.replace(hour=10, minute=10, second=0, microsecond=0)
    start1 = now.replace(hour=11, minute=50, second=0, microsecond=0)
    end1 = now.replace(hour=12, minute=10, second=0, microsecond=0)
    start2 = now.replace(hour=15, minute=50, second=0, microsecond=0)
    end2 = now.replace(hour=16, minute=10, second=0, microsecond=0)
    start_20 = now.replace(hour=19, minute=50, second=0, microsecond=0)
    end_20 = now.replace(hour=20, minute=10, second=0, microsecond=0)
    return (now >= start0_pm) or (now <= end0_am) or \
           (start_8 <= now <= end_8) or \
           (start1 <= now <= end1) or \
           (start2 <= now <= end2) or \
           (start_20 <= now <= end_20)

def handle_yijian_qiangdui():
    if not sender.isAdmin():
        sender.reply("❌ 需要管理员权限")
        return
    if STOP_EXCHANGE:
        sender.reply("❌ 抢兑已被手动停止")
        return
    if not within_exchange_window():
        sender.reply("❌ 当前时间不在0,10,12,16,20点前后，无法执行云盘抢兑操作")
        return
    now = local_now()
    possible_targets =[
        now.replace(hour=0, minute=0, second=0, microsecond=0),
        now.replace(hour=8, minute=0, second=0, microsecond=0),
        now.replace(hour=12, minute=0, second=0, microsecond=0),
        now.replace(hour=16, minute=0, second=0, microsecond=0),
        now.replace(hour=20, minute=0, second=0, microsecond=0)
    ]
    if now.hour >= 23:
        target_time = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        future_targets =[t for t in possible_targets if t > now]
        if not future_targets:
            target_time = min(possible_targets)
        else:
            target_time = min(future_targets, key=lambda t: t - now)
    prize_bucket_key = 'yuhua_ydyp_prize_regular'
    prize_filter_logic = lambda prize: prize.get('groupId') != 10
    all_keys = sg.bucketAllKeys(prize_bucket_key)
    if not all_keys:
        sender.reply("❌ 暂无账号提交【福利专区】抢兑")
        return
    owner_map = {}
    all_users = sg.bucketAllKeys('yuhua_ydyp_user')
    for u in all_users:
        acc_list = _sg_literal(sg.bucketGet('yuhua_ydyp_user', u) or '[]')
        for ac in acc_list:
            owner_map[ac] = u
    concurrency_data = []
    fail_reasons =[]
    cleaned_invalid_accounts = 0
    for acc_id in all_keys:
        if STOP_EXCHANGE:
            sender.reply("❌ 云盘抢兑已被手动停止")
            return
        prize_name = sg.bucketGet(prize_bucket_key, acc_id)
        if not prize_name:
            try:
                sg.bucketDel(prize_bucket_key, acc_id)
            except Exception:
                pass
            cleaned_invalid_accounts += 1
            continue
        phone = sg.bucketGet('yuhua_ydyp_phone', acc_id) or "未知"
        phone_mask = phone[:3] + "****" + phone[-4:] if len(phone) >= 7 else phone
        if acc_id not in owner_map:
            try:
                sg.bucketDel(prize_bucket_key, acc_id)
            except Exception:
                pass
            cleaned_invalid_accounts += 1
            continue

        ok_ck, ck_str, ck_msg = check_and_refresh_token(acc_id)
        if not ok_ck and not ck_str:
            fail_reasons.append(f"【{phone_mask}】{ck_msg}")
            continue

        y = YP(ck_str, phone=phone)
        ok1, msg1 = y.sso()
        if not ok1:
            msg1_str = str(msg1)
            need_relogin = any(keyword in msg1_str.lower() for keyword in['unauthorized', 'invalid', 'expired', 'authorization']) or any(keyword in msg1_str for keyword in['无效', '过期', '失效'])
            if need_relogin:
                ok_force, ck_str_force, force_msg = check_and_refresh_token(acc_id, force=True)
                if ok_force and ck_str_force:
                    y.close()
                    y = YP(ck_str_force, phone=phone)
                    ok1, msg1 = y.sso()
                    if not ok1:
                        fail_reasons.append(f"【{phone_mask}】{msg1}")
                        continue
                else:
                    fail_reasons.append(f"【{phone_mask}】强制刷新失败: {force_msg}")
                    continue
            else:
                fail_reasons.append(f"【{phone_mask}】{msg1}")
                continue

        ok2, _ = y.jwt()
        if not ok2: fail_reasons.append(f"【{phone_mask}】jwt获取失败"); continue
        list_resp = y.send_request("https://m.mcloud.139.com/ycloud/signin/page/exchangeList", headers=y.jwtHeaders, cookies=y.cookies)
        if not list_resp or "result" not in list_resp:
            fail_reasons.append(f"【{phone_mask}】获取奖品列表失败"); continue
        found_pid = None
        cost = 9999999
        for _, arr in list_resp["result"].items():
            for it in arr:
                if prize_filter_logic(it) and it.get("prizeName") == prize_name:
                    found_pid = it.get("prizeId")
                    cost = it.get("pOrder", 9999999)
                    break
                if found_pid: break
        if not found_pid:
            fail_reasons.append(f"【{phone_mask}】未找到奖品 {prize_name}"); continue
        ok3, _ = y.receive()
        if not ok3:
            fail_reasons.append(f"【{phone_mask}】查询云朵失败"); continue
        if y.total_amount < cost:
            fail_reasons.append(f"【{phone_mask}】云朵不足 ({y.total_amount}/{cost})"); continue
        user_id = owner_map.get(acc_id, "")
        ok_dev, dev_id = get_or_fetch_device_id(acc_id)
        if not ok_dev:
            fail_reasons.append(f"【{phone_mask}】{dev_id}")
            continue
        concurrency_data.append((phone_mask, prize_name, found_pid, cost, y, user_id, acc_id, dev_id))
    now_str = now.strftime('%Y-%m-%d %H:%M:%S')
    notice = f"""🪁 插件【移动云盘】提醒
🧭 当前时间: {now_str}
📋 抢兑账号: {len(concurrency_data)}个
🏖️ 抢兑时间: {target_time.strftime('%H:%M:%S')}
"""
    sender.reply(notice)
    if cleaned_invalid_accounts > 0:
        sender.reply(f"🧹 已自动清理 {cleaned_invalid_accounts} 个无效账号的抢兑数据")
    if fail_reasons:
        sender.reply("以下账号不满足抢兑条件：\n" + "\n".join(fail_reasons))
    diff = (target_time - local_now()).total_seconds()
    if diff > 0:
        time.sleep(diff)
    if STOP_EXCHANGE:
        sender.reply("❌ 云盘抢兑已被手动停止"); return

    from concurrent.futures import ThreadPoolExecutor, as_completed

    def real_exchange(phone_mask, pname, pid, costnum, yobj, user_id, account_id, dev_id):
        import hashlib
        import urllib.parse

        target_deviceId = dev_id
        if not target_deviceId.startswith('B'):
            target_deviceId = 'B' + target_deviceId
        thumb_val = target_deviceId[1:]

        exchange_headers = dict(yobj.jwtHeaders)
        exchange_headers.update({
            'Host': 'm.mcloud.139.com',
            'Connection': 'keep-alive',
            'sec-ch-ua-platform': '"Android"',
            'Cache-Control': 'no-cache',
            'sec-ch-ua': '"Android WebView";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'deviceId': target_deviceId,
            'showLoading': 'true',
            'appVersion': '12.5.4.0',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 16; RMX5060 Build/BP2A.250605.015; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/149.0.7827.13 Safari/537.36 MCloudApp/12.5.4 AppLanguage/zh-CN',
            'activityId': 'sign_in_3',
            'Accept': '*/*',
            'X-Requested-With': 'com.chinamobile.mcloud',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://m.mcloud.139.com/portal/mobilecloud/index.html?path=newsignin&sourceid=1097&enableShare=1&token=&targetSourceId=001005',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'zh,zh-CN;q=0.9,en-US;q=0.8,en;q=0.7'
        })

        exchange_cookies = dict(yobj.cookies)
        account_md5 = hashlib.md5(yobj.account.encode('utf-8')).hexdigest()
        exchange_cookies[f".thumbcache_{account_md5}"] = urllib.parse.quote(thumb_val)

        for attempt in range(1, 6):
            if STOP_EXCHANGE:
                return (phone_mask, pname, False, "已被手动停止", user_id, account_id)
            puzzle_offset = solve_slide_captcha(yobj, dev_id)
            if puzzle_offset is None:
                puzzle_offset = 257
            exc_url = f"https://m.mcloud.139.com/ycloud/signin/page/exchangeV2?prizeId={pid}&client=app&clientVersion=12.5.4&puzzleOffset={puzzle_offset}&smsCode="
            resp = yobj.send_request(exc_url, headers=exchange_headers, cookies=exchange_cookies, method='GET')
            if resp and resp.get("code") == 0:
                return (phone_mask, pname, True, f"兑换成功(第{attempt}次)", user_id, account_id)
            else:
                if attempt < 5: time.sleep(0.5)
        msg = resp.get("msg", "兑换失败") if resp else "未知错误"
        if "活动太火爆啦" in msg or "锁定失败" in msg:
            msg += "。"
        return (phone_mask, pname, False, msg, user_id, account_id)

    bf_num_local = bingfa
    futures_map = {}
    with ThreadPoolExecutor(max_workers=bf_num_local) as exe:
        for (pm, pn, pd, ct, y, uid, acid, did) in concurrency_data:
            fut = exe.submit(real_exchange, pm, pn, pd, ct, y, uid, acid, did)
            futures_map[fut] = pm
        results =[]
        for fut in as_completed(futures_map): results.append(fut.result())
    succ_count = sum(1 for r in results if r[2] is True)
    fail_count = sum(1 for r in results if r[2] is False)
    fail_msgs =[f"🤪 账号: {r[0]}\n🎁 奖品: {r[1]}\n🪁 结果: {r[3]}" for r in results if not r[2]]
    detail_fail = "\n".join(fail_msgs) if fail_msgs else ""
    final_msg = f"""=====云盘抢兑统计=====
✨ 总抢兑数: {len(results)}
✅ 抢兑成功: {succ_count}
❌ 抢兑失败: {fail_count}
------------------
📝 失败详情:
{detail_fail if detail_fail else '无'}
=================="""
    sender.reply(final_msg)
    for (phone_mask, pname, ok, reason, user_id, account_id) in results:
        if ok is True:
            try:
                sg.bucketDel(prize_bucket_key, account_id)
            except Exception:
                pass
        if user_id:
            status_str = "成功" if ok else reason
            push_text = f"""=====云盘抢兑=====
🤪 账号: {phone_mask}
🎁 奖品: {pname}
🪁 结果：{status_str}
=================="""
            sg.push('qq', '', user_id, '', push_text)
            sg.push('qb', '', user_id, '', push_text)
            sg.push('wx', '', user_id, '', push_text)
            sg.push('gw', '', user_id, '', push_text)
            sg.push('sb', '', user_id, '', push_text)
            sg.push('wb', '', user_id, '', push_text)
            sg.push('tg', '', user_id, '', push_text)
            sg.push('tb', '', user_id, '', push_text)
            sg.push('qx', '', user_id, '', push_text)
            sg.push('xy', '', user_id, '', push_text)
            sg.push('ip', '', user_id, '', push_text)
        if not ok and ("非移动用户不可领奖" in str(reason) or "超过每月兑换限制" in str(reason) or "重复兑奖" in str(reason)):
            try:
                sg.bucketDel(prize_bucket_key, account_id)
            except Exception:
                pass
def exchange_entry_point():
    accounts=list(_sg_literal(sg.bucketGet('yuhua_ydyp_user',userid),[]))
    if not accounts:return sender.reply('未绑定账号，请发送【云盘登录】')
    if len(accounts)==1:return show_exchange_menu_ydyp(accounts[0])
    sender.reply('请选择兑换账号：\n'+'\n'.join(f'{i}. '+str(sg.bucketGet('yuhua_ydyp_phone',a) or a) for i,a in enumerate(accounts,1)))
    choice=sender.input(60000,0,False)
    if not choice or str(choice).lower()=='q':return
    try:show_exchange_menu_ydyp(accounts[int(choice)-1])
    except (ValueError,IndexError):sender.reply('序号无效')


def show_exchange_menu_ydyp(account):
    sender.reply("正在执行...")
    phone = sg.bucketGet('yuhua_ydyp_phone', account) or "未知"
    phone_mask = phone[:3] + "****" + phone[-4:] if len(phone) >= 7 else phone

    ok_ck, ck_str, ck_msg = check_and_refresh_token(account)
    if not ok_ck and not ck_str:
        sender.reply(f"【{phone_mask}】{ck_msg}")
        return

    yp = YP(ck_str, phone=phone)
    try:
        ok1, msg1 = yp.sso()
        if not ok1:
            msg1_str = str(msg1)
            need_relogin = any(keyword in msg1_str.lower() for keyword in['unauthorized', 'invalid', 'expired', 'authorization']) or any(keyword in msg1_str for keyword in ['无效', '过期', '失效'])
            if need_relogin:
                ok_force, ck_str_force, force_msg = check_and_refresh_token(account, force=True)
                if ok_force and ck_str_force:
                    yp.close()
                    yp = YP(ck_str_force, phone=phone)
                    ok1, msg1 = yp.sso()
                    if not ok1:
                        sender.reply(f"【{phone_mask}】{msg1}")
                        return
                else:
                    sender.reply(f"【{phone_mask}】强制刷新失败: {force_msg}")
                    return
            else:
                sender.reply(f"【{phone_mask}】{msg1}")
                return

        ok2, _ = yp.jwt()
        if not ok2: sender.reply(f"【{phone_mask}】jwt获取失败"); return
        ok3, _ = yp.receive()
        if not ok3: sender.reply(f"【{phone_mask}】查询云朵失败"); return
        list_url = "https://m.mcloud.139.com/ycloud/signin/page/exchangeList"
        r = yp.send_request(list_url, headers=yp.jwtHeaders, cookies=yp.cookies)
        if not r or "result" not in r: sender.reply(f"【{phone_mask}】获取奖品列表失败"); return
        all_prizes_raw =[]
        for _, arr in r["result"].items(): all_prizes_raw.extend(arr)
        all_prizes =[p for p in all_prizes_raw if p.get('groupId') != 10]
        if not all_prizes: sender.reply(f"【{phone_mask}】当前没有可兑换的奖品"); return
        product_display_list =[]
        for i, product in enumerate(all_prizes, 1):
            prize_name = product.get('prizeName', '未知奖品')
            cost = product.get('pOrder', 0)
            stock_status = "✅" if product.get('dailyRemainderCount', 0) > 0 else "❌"
            product_display_list.append(f"[{i}] {prize_name}\n    {stock_status} 消耗{cost}云朵")
        prize_regular = sg.bucketGet('yuhua_ydyp_prize_regular', account)
        prize_status_regular = f"🎁 福利专区: {prize_regular}" if prize_regular else "🎁 福利专区: 未设置"

        products_msg = f"""=====云盘兑换=====
🤪 用户账号: {phone_mask}
💰 当前云朵: {yp.total_amount}
{prize_status_regular}
------------------
{chr(10).join(product_display_list)}
------------------
+序号=提交抢兑, d=删除抢兑
单序号=立即兑换, q=退出操作"""
        sender.reply(products_msg)
        choice_str = sender.input(60000, 0, False)
        if not choice_str or choice_str.lower() == 'q': sender.reply("✅ 已退出操作"); return
        if choice_str.lower() == 'd':
            try:
                sg.bucketDel('yuhua_ydyp_prize_regular', account)
            except Exception:
                pass
            sender.reply(f"【{phone_mask}】福利专区抢兑目标已清除")
            return
        if choice_str.startswith('+'):
            try:
                choice_idx = int(choice_str[1:])
                if not (1 <= choice_idx <= len(all_prizes)): raise ValueError()
                selected_product = all_prizes[choice_idx - 1]
                p_input = selected_product.get("prizeName")
                sg.bucketSet('yuhua_ydyp_prize_regular', account, p_input)
                sender.reply(f"【{phone_mask}】福利专区抢兑目标已设置为: {p_input}")
            except (ValueError, IndexError):
                sender.reply("❌ 无效的选择")
            return
        try:
            choice_idx = int(choice_str)
            if not (1 <= choice_idx <= len(all_prizes)): raise ValueError()
            selected_product = all_prizes[choice_idx - 1]
            if selected_product.get('dailyRemainderCount', 0) <= 0:
                sender.reply(f"【{phone_mask}】兑换失败，该奖品已无库存")
                return
            found_pid = selected_product.get("prizeId")
            cost = selected_product.get("pOrder", 9999999)
            if yp.total_amount < cost:
                sender.reply(f"【{phone_mask}】云朵不足({yp.total_amount}/{cost})")
                return

            sender.reply("正在执行...")

            import hashlib
            import urllib.parse

            ok_dev, dev_id = get_or_fetch_device_id(account)
            if not ok_dev:
                sender.reply(f"【{phone_mask}】{dev_id}")
                return

            target_deviceId = dev_id
            if not target_deviceId.startswith('B'):
                target_deviceId = 'B' + target_deviceId
            thumb_val = target_deviceId[1:]

            exchange_headers = dict(yp.jwtHeaders)
            exchange_headers.update({
                'Host': 'm.mcloud.139.com',
                'Connection': 'keep-alive',
                'sec-ch-ua-platform': '"Android"',
                'Cache-Control': 'no-cache',
                'sec-ch-ua': '"Android WebView";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
                'sec-ch-ua-mobile': '?1',
                'deviceId': target_deviceId,
                'showLoading': 'true',
                'appVersion': '12.5.4.0',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 16; RMX5060 Build/BP2A.250605.015; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/149.0.7827.13 Safari/537.36 MCloudApp/12.5.4 AppLanguage/zh-CN',
                'activityId': 'sign_in_3',
                'Accept': '*/*',
                'X-Requested-With': 'com.chinamobile.mcloud',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': 'https://m.mcloud.139.com/portal/mobilecloud/index.html?path=newsignin&sourceid=1097&enableShare=1&token=&targetSourceId=001005',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'zh,zh-CN;q=0.9,en-US;q=0.8,en;q=0.7'
            })

            exchange_cookies = dict(yp.cookies)
            account_md5 = hashlib.md5(yp.account.encode('utf-8')).hexdigest()
            exchange_cookies[f".thumbcache_{account_md5}"] = urllib.parse.quote(thumb_val)

            puzzle_offset = solve_slide_captcha(yp, dev_id)
            if puzzle_offset is None:
                puzzle_offset = 257
            exc_url = f"https://m.mcloud.139.com/ycloud/signin/page/exchangeV2?prizeId={found_pid}&client=app&clientVersion=12.5.4&puzzleOffset={puzzle_offset}&smsCode="
            resp = yp.send_request(exc_url, headers=exchange_headers, cookies=exchange_cookies, method='GET')
            if resp and resp.get("code") == 0:
                sender.reply(f"【{phone_mask}】兑换【{selected_product.get('prizeName')}】成功")
            else:
                msg = resp.get("msg", "兑换失败") if resp else "未知错误"
                if "活动太火爆啦" in msg or "锁定失败" in msg:
                    msg += "。"
                sender.reply(f"【{phone_mask}】{msg}")
        except (ValueError, IndexError):
            sender.reply("❌ 无效的选择")
    finally:
        yp.close()

def stop_exchange():
    global STOP_EXCHANGE
    if not sender.isAdmin():
        sender.reply("❌ 需要管理员权限")
        return
    STOP_EXCHANGE = True
    sender.reply("✅ 已停止云盘抢兑")

def sms_login():
    def sanitize_message(message):
        sensitive_urls = ['http://yuhualhh.250666.xyz', 'https://yuhualhh.250666.xyz']
        sanitized = str(message)
        for url in sensitive_urls:
            sanitized = sanitized.replace(url, '****')
        return sanitized

    sender.reply("请输入手机号:")
    phone = sender.input(30000, 1, False)
    if not phone:
        sender.reply("❌ 输入超时")
        return
    phone = phone.strip()
    if phone.lower() == 'q':
        sender.reply("✅ 已退出操作")
        return
    if not re.match(r'^\d{11}$', phone):
        sender.reply("❌ 无效的输入")
        return

    try:
        php_api_url = "https://yuhualhh.250666.xyz/api/ydyp_sms_login.php"
        php_api_key = "yuhua666666"

        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'Content-Type': 'application/json',
            'X-API-KEY': php_api_key
        })

        if DEBUG:
            printf("===== [SMS LOGIN START] =====", "DEBUG")
            printf(f"PHONE: {phone}", "DEBUG")
            printf(f"PHP API URL: {php_api_url}", "DEBUG")

        sms_payload = {
            "action": "get_sms_code",
            "phone": phone
        }

        if DEBUG:
            printf("===== [PHP GET SMS CODE REQUEST] =====", "DEBUG")
            printf(f"URL: {php_api_url}", "DEBUG")
            printf(f"BODY(JSON): {json.dumps(sms_payload, ensure_ascii=False)}", "DEBUG")

        sms_resp = session.post(php_api_url, json=sms_payload, timeout=20)

        if DEBUG:
            printf("===== [PHP GET SMS CODE RESPONSE] =====", "DEBUG")
            printf(f"STATUS: {sms_resp.status_code}", "DEBUG")
            printf(f"RSP HEADERS: {json.dumps(dict(sms_resp.headers), ensure_ascii=False)}", "DEBUG")
            printf(f"RSP BODY: {sms_resp.text}", "DEBUG")

        sms_resp.raise_for_status()
        sms_data = sms_resp.json()

        if sms_data.get('code') != 0:
            sender.reply(sanitize_message(f"❌ 获取验证码失败: {sms_data.get('message', '未知错误')}"))
            return

        sender.reply("请输入验证码:")
        code = sender.input(60000, 0, False)
        if not code:
            sender.reply("❌ 输入超时")
            return
        if code.lower() == 'q':
            sender.reply("✅ 已退出操作")
            return
        code = code.strip()

        if DEBUG:
            printf(f"用户输入验证码: {code}", "DEBUG")

        login_payload = {
            "action": "login",
            "phone": phone,
            "code": code
        }

        if DEBUG:
            printf("===== [PHP LOGIN REQUEST] =====", "DEBUG")
            printf(f"URL: {php_api_url}", "DEBUG")
            printf(f"BODY(JSON): {json.dumps(login_payload, ensure_ascii=False)}", "DEBUG")

        login_resp = session.post(php_api_url, json=login_payload, timeout=20)

        if DEBUG:
            printf("===== [PHP LOGIN RESPONSE] =====", "DEBUG")
            printf(f"STATUS: {login_resp.status_code}", "DEBUG")
            printf(f"RSP HEADERS: {json.dumps(dict(login_resp.headers), ensure_ascii=False)}", "DEBUG")
            printf(f"RSP BODY: {login_resp.text}", "DEBUG")

        login_resp.raise_for_status()
        login_data = login_resp.json()

        if login_data.get('code') != 0:
            sender.reply(sanitize_message(f"❌ 登录失败: {login_data.get('message', '验证码不正确')}"))
            return

        data = login_data.get('data', {}) or {}
        ck_value = data.get('Authorization', '') or ''

        if DEBUG:
            printf(f"登录响应data: {json.dumps(data, ensure_ascii=False)}", "DEBUG")
            printf(f"直接从PHP响应中获取Authorization: {'成功' if ck_value else '失败'}", "DEBUG")

        time.sleep(random.uniform(0.2, 0.5))

        if not ck_value:
            sender.reply(sanitize_message("❌ 登录失败：无法获取Authorization值"))
            return

        if not ck_value.startswith('Basic '):
            ck_value = f"Basic {ck_value}"

        if DEBUG:
            printf(f"最终Authorization: {ck_value}", "DEBUG")

        user_input = f"{ck_value}#{phone}"

        yp_check = YP(ck_value, phone=phone)
        ok, msg = yp_check.sso()
        yp_check.close()

        if DEBUG:
            printf(f"Authorization校验结果: ok={ok}, msg={msg}", "DEBUG")

        if not ok:
            sender.reply(sanitize_message(f"❌ 登录校验失败: {msg}"))
            return

        accounts = _sg_literal(uservalue or '[]')
        matched_uid = None
        for uid in accounts:
            old_phone = sg.bucketGet('yuhua_ydyp_phone', uid) or "未知"
            if old_phone == phone:
                matched_uid = uid
                break

        if DEBUG:
            printf(f"匹配到已有账号UID: {matched_uid if matched_uid else '无'}", "DEBUG")

        if matched_uid:
            sg.bucketSet('yuhua_ydyp_token', matched_uid, user_input)
            try:
                sg.bucketDel('yuhua_ydyp_password', matched_uid)
            except Exception:
                pass
            if add_to_qinglong(user_input, matched_uid, phone):
                try:
                    ql_envs = get_global_session().get(f"{ql_url}/open/envs", headers={"Authorization": f"Bearer {ql_token}"}, timeout=10)
                    if ql_envs.status_code == 200:
                        items = ql_envs.json().get('data', [])
                        ids = [e.get('id') for e in items if e.get('name') == var_name and f"UID:{matched_uid}" in str(e.get('remarks',''))]
                        if ids:
                            _enable_envs_in_qinglong(ids)
                except Exception:
                    pass
            phone_mask = phone[:3] + "****" + phone[-4:]
            sender.reply(f"=====登录成功=====\n🤪 账号: {phone_mask}\n✅ 状态: 更新成功\n------------------\n发送\"{manage_cmd}\"管理账号\n发送\"{query_cmd}\"查询账号")
        else:
            new_id = gen_unique_id()
            if new_id not in accounts:
                accounts.append(new_id)
                sg.bucketSet('yuhua_ydyp_user', userid, str(accounts))
            sg.bucketSet('yuhua_ydyp_token', new_id, user_input)
            sg.bucketSet('yuhua_ydyp_phone', new_id, phone)
            phone_mask = phone[:3] + "****" + phone[-4:]
            sender.reply(f"=====登录成功=====\n🤪 账号: {phone_mask}\n✅ 状态: 添加成功\n------------------\n发送\"{manage_cmd}\"管理账号\n发送\"{query_cmd}\"查询账号")

        if DEBUG:
            printf("===== [SMS LOGIN END] =====", "DEBUG")

    except Exception as e:
        if DEBUG:
            printf(f"短信登录流程异常: {str(e)}", "ERROR")
        sender.reply(sanitize_message(f"❌ 短信登录流程出错: {str(e)}"))

def password_login():
    def sanitize_message(message):
        sensitive_urls = ['http://yuhualhh.250666.xyz', 'https://yuhualhh.250666.xyz']
        sanitized = str(message)
        for url in sensitive_urls:
            sanitized = sanitized.replace(url, '****')
        return sanitized

    sender.reply("请输入手机号:")
    phone = sender.input(30000, 1, False)
    if not phone:
        sender.reply("❌ 输入超时")
        return
    phone = phone.strip()
    if phone.lower() == 'q':
        sender.reply("✅ 已退出操作")
        return
    if not re.match(r'^\d{11}$', phone):
        sender.reply("❌ 无效的输入")
        return

    sender.reply("请输入密码:")
    password = sender.input(60000, 1, False)
    if not password:
        sender.reply("❌ 输入超时")
        return
    password = password.strip()
    if password.lower() == 'q':
        sender.reply("✅ 已退出操作")
        return
    if password == '':
        sender.reply("❌ 密码不能为空")
        return

    try:
        php_api_url = "https://yuhualhh.250666.xyz/api/ydyp_sms_login.php"
        php_api_key = "yuhua666666"

        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'Content-Type': 'application/json',
            'X-API-KEY': php_api_key
        })

        if DEBUG:
            printf("===== [PASSWORD LOGIN START] =====", "DEBUG")
            printf(f"PHONE: {phone}", "DEBUG")
            printf(f"PHP API URL: {php_api_url}", "DEBUG")

        login_payload = {
            "action": "account_login",
            "phone": phone,
            "password": password
        }

        if DEBUG:
            printf("===== [PHP PASSWORD LOGIN REQUEST] =====", "DEBUG")
            printf(f"URL: {php_api_url}", "DEBUG")
            printf(f"BODY(JSON): {json.dumps({'action': 'account_login', 'phone': phone, 'password': '******'}, ensure_ascii=False)}", "DEBUG")

        login_resp = session.post(php_api_url, json=login_payload, timeout=20)

        if DEBUG:
            printf("===== [PHP PASSWORD LOGIN RESPONSE] =====", "DEBUG")
            printf(f"STATUS: {login_resp.status_code}", "DEBUG")
            printf(f"RSP HEADERS: {json.dumps(dict(login_resp.headers), ensure_ascii=False)}", "DEBUG")
            printf(f"RSP BODY: {login_resp.text}", "DEBUG")

        login_resp.raise_for_status()
        login_data = login_resp.json()

        if login_data.get('code') != 0:
            sender.reply(sanitize_message(f"❌ 登录失败: {login_data.get('message', '账号或密码不正确')}"))
            return

        data = login_data.get('data', {}) or {}
        ck_value = data.get('Authorization', '') or ''

        if DEBUG:
            printf(f"登录响应data: {json.dumps(data, ensure_ascii=False)}", "DEBUG")
            printf(f"直接从PHP响应中获取Authorization: {'成功' if ck_value else '失败'}", "DEBUG")

        time.sleep(random.uniform(0.2, 0.5))

        if not ck_value:
            sender.reply(sanitize_message("❌ 登录失败：无法获取Authorization值"))
            return

        if not ck_value.startswith('Basic '):
            ck_value = f"Basic {ck_value}"

        if DEBUG:
            printf(f"最终Authorization: {ck_value}", "DEBUG")

        user_input = f"{ck_value}#{phone}"

        yp_check = YP(ck_value, phone=phone)
        ok, msg = yp_check.sso()
        yp_check.close()

        if DEBUG:
            printf(f"Authorization校验结果: ok={ok}, msg={msg}", "DEBUG")

        if not ok:
            sender.reply(sanitize_message(f"❌ 登录校验失败: {msg}"))
            return

        accounts = _sg_literal(uservalue or '[]')
        matched_uid = None
        for uid in accounts:
            old_phone = sg.bucketGet('yuhua_ydyp_phone', uid) or "未知"
            if old_phone == phone:
                matched_uid = uid
                break

        if DEBUG:
            printf(f"匹配到已有账号UID: {matched_uid if matched_uid else '无'}", "DEBUG")

        if matched_uid:
            sg.bucketSet('yuhua_ydyp_token', matched_uid, user_input)
            sg.bucketSet('yuhua_ydyp_password', matched_uid, password)
            if add_to_qinglong(user_input, matched_uid, phone):
                try:
                    ql_envs = get_global_session().get(f"{ql_url}/open/envs", headers={"Authorization": f"Bearer {ql_token}"}, timeout=10)
                    if ql_envs.status_code == 200:
                        items = ql_envs.json().get('data', [])
                        ids = [e.get('id') for e in items if e.get('name') == var_name and f"UID:{matched_uid}" in str(e.get('remarks',''))]
                        if ids:
                            _enable_envs_in_qinglong(ids)
                except Exception:
                    pass
            phone_mask = phone[:3] + "****" + phone[-4:]
            sender.reply(f"=====登录成功=====\n🤪 账号: {phone_mask}\n✅ 状态: 更新成功\n------------------\n发送\"{manage_cmd}\"管理账号\n发送\"{query_cmd}\"查询账号")
        else:
            new_id = gen_unique_id()
            if new_id not in accounts:
                accounts.append(new_id)
                sg.bucketSet('yuhua_ydyp_user', userid, str(accounts))
            sg.bucketSet('yuhua_ydyp_token', new_id, user_input)
            sg.bucketSet('yuhua_ydyp_phone', new_id, phone)
            sg.bucketSet('yuhua_ydyp_password', new_id, password)
            phone_mask = phone[:3] + "****" + phone[-4:]
            sender.reply(f"=====登录成功=====\n🤪 账号: {phone_mask}\n✅ 状态: 添加成功\n------------------\n发送\"{manage_cmd}\"管理账号\n发送\"{query_cmd}\"查询账号")

        if DEBUG:
            printf("===== [PASSWORD LOGIN END] =====", "DEBUG")

    except Exception as e:
        if DEBUG:
            printf(f"账密登录流程异常: {str(e)}", "ERROR")
        sender.reply(sanitize_message(f"❌ 账密登录流程出错: {str(e)}"))

try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

def aes_encrypt(data, key):
    if not HAS_CRYPTO:
        return None
    key_bytes = key.encode('utf-8')
    if not isinstance(data, str):
        data = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    encrypted = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    return base64.b64encode(encrypted).decode('utf-8')

def do_native_token_refresh(account_id, phone, current_auth):
    if not HAS_CRYPTO:
        return False, "未安装pycryptodome依赖，跳过原生刷新"

    url = 'https://user-njs.yun.139.com/user/auth/refreshToken'
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.47(0x18002f2c) NetType/WIFI Language/zh_CN miniProgram/wx4e4ed37286c816c2',
        'x-yun-tid': str(uuid.uuid4()),
        'Authorization': current_auth,
        'x-yun-api-version': 'v1',
        'x-yun-module-type': '100',
        'x-yun-op-type': '1',
        'x-yun-app-channel': '10214200',
        'x-yun-client-info': '||8||||||||||||',
        'hcy-cool-flag': '1',
    }

    encrypted_data = aes_encrypt({'phoneNumber': phone}, 'c7lXOigXahPnTViq')
    if not encrypted_data:
        return False, "加密手机号失败"

    try:
        session = get_global_session()
        resp = session.post(url, headers=headers, json={'data': encrypted_data}, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        code = str(data.get('code', ''))

        if code in ('0', '00', '000', '0000') or data.get('success'):
            raw_token = data.get('data', {}).get('token')
            expire_time = data.get('data', {}).get('expireTime')

            if raw_token:
                new_auth_str = f"mobile:{phone}:{raw_token}"
                new_auth = f"Basic {base64.b64encode(new_auth_str.encode('utf-8')).decode('utf-8')}"

                new_ck_str = f"{new_auth}#{phone}"
                sg.bucketSet('yuhua_ydyp_token', account_id, new_ck_str)

                try:
                    expire_seconds = int(float(expire_time))
                except Exception:
                    expire_seconds = 2592000
                expires_at = int(time.time() * 1000) + expire_seconds * 1000
                sg.bucketSet('yuhua_ydyp_token_expire', account_id, str(expires_at))

                add_to_qinglong(new_ck_str, account_id, phone)

                return True, new_ck_str

        return False, data.get('message') or data.get('msg') or "未知错误"
    except Exception as e:
        return False, str(e)

def check_and_refresh_token(account_id, force=False):
    ck_str = sg.bucketGet('yuhua_ydyp_token', account_id)
    if not ck_str:
        return False, None, "未找到CK"

    parts = ck_str.split('#')
    current_auth = parts[0].strip()
    phone = parts[1].strip() if len(parts) > 1 else "未知"

    if phone == "未知":
        phone = sg.bucketGet('yuhua_ydyp_phone', account_id) or "未知"

    if not re.match(r'^\d{11}$', phone):
        return True, ck_str, "手机号无效，跳过刷新"

    expire_str = sg.bucketGet('yuhua_ydyp_token_expire', account_id)
    now_ms = int(time.time() * 1000)

    need_refresh = force
    if not need_refresh:
        if not expire_str:
            need_refresh = True
        else:
            try:
                expires_at = int(expire_str)
                if expires_at - now_ms < 86400000:
                    need_refresh = True
            except Exception:
                need_refresh = True

    if need_refresh:
        ok, result = do_native_token_refresh(account_id, phone, current_auth)
        if ok:
            return True, result, "原生刷新成功"
        else:
            relogin_ok, relogin_msg = _try_auto_password_relogin(account_id)
            if relogin_ok:
                new_ck = sg.bucketGet('yuhua_ydyp_token', account_id)
                sg.bucketSet('yuhua_ydyp_token_expire', account_id, str(now_ms + 2592000000))
                return True, new_ck, "账密兜底刷新成功"
            else:
                return False, ck_str, f"刷新失败: {result} / {relogin_msg}"

    return True, ck_str, "Token状态良好"

def _try_auto_password_relogin(account_id):
    def sanitize_message(message):
        sensitive_urls = ['http://yuhualhh.250666.xyz', 'https://yuhualhh.250666.xyz']
        sanitized = str(message)
        for url in sensitive_urls:
            sanitized = sanitized.replace(url, '****')
        return sanitized

    phone = sg.bucketGet('yuhua_ydyp_phone', account_id) or ""
    password = sg.bucketGet('yuhua_ydyp_password', account_id) or ""

    if not re.match(r'^\d{11}$', phone):
        return False, "未找到可续期手机号"
    if password == "":
        return False, "未找到账密续期信息"

    try:
        php_api_url = "https://yuhualhh.250666.xyz/api/ydyp_sms_login.php"
        php_api_key = "yuhua666666"

        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'Content-Type': 'application/json',
            'X-API-KEY': php_api_key
        })

        relogin_payload = {
            "action": "password_relogin",
            "phone": phone,
            "password": password
        }

        if DEBUG:
            printf("===== [AUTO PASSWORD RELLOGIN REQUEST] =====", "DEBUG")
            printf(f"URL: {php_api_url}", "DEBUG")
            printf(f"BODY(JSON): {json.dumps({'action': 'password_relogin', 'phone': phone, 'password': '******'}, ensure_ascii=False)}", "DEBUG")

        relogin_resp = session.post(php_api_url, json=relogin_payload, timeout=20)

        if DEBUG:
            printf("===== [AUTO PASSWORD RELLOGIN RESPONSE] =====", "DEBUG")
            printf(f"STATUS: {relogin_resp.status_code}", "DEBUG")
            printf(f"RSP HEADERS: {json.dumps(dict(relogin_resp.headers), ensure_ascii=False)}", "DEBUG")
            printf(f"RSP BODY: {relogin_resp.text}", "DEBUG")

        relogin_resp.raise_for_status()
        relogin_data = relogin_resp.json()

        if relogin_data.get('code') != 0:
            return False, sanitize_message(relogin_data.get('message', '账密续期失败'))

        data = relogin_data.get('data', {}) or {}
        ck_value = data.get('Authorization', '') or ''
        if not ck_value:
            return False, "账密续期失败：未获取到Authorization"

        if not ck_value.startswith('Basic '):
            ck_value = f"Basic {ck_value}"

        yp_check = YP(ck_value, phone=phone)
        ok, msg = yp_check.sso()
        yp_check.close()
        if not ok:
            return False, sanitize_message(msg)

        user_input = f"{ck_value}#{phone}"
        sg.bucketSet('yuhua_ydyp_token', account_id, user_input)

        if add_to_qinglong(user_input, account_id, phone):
            try:
                ql_envs = get_global_session().get(f"{ql_url}/open/envs", headers={"Authorization": f"Bearer {ql_token}"}, timeout=10)
                if ql_envs.status_code == 200:
                    items = ql_envs.json().get('data', [])
                    ids = [e.get('id') for e in items if e.get('name') == var_name and f"UID:{account_id}" in str(e.get('remarks',''))]
                    if ids:
                        _enable_envs_in_qinglong(ids)
            except Exception:
                pass

        return True, "ok"
    except Exception as e:
        return False, sanitize_message(str(e))


def main():
    try:
        message=sender.getMessage().strip()
        if message=='云盘一键抢兑':
            if sender.isAdmin():handle_yijian_qiangdui()
            else:sender.reply('需要管理员权限')
        elif message=='云盘停止抢兑':stop_exchange()
        elif '登录' in message:login()
        elif '兑换' in message:exchange_entry_point()
        elif '管理' in message:manage_account()
        elif '查询' in message:query_account()
        else:sender.setContinue()
    except Exception as error:sender.reply(f'运行出错：{error}')
    finally:close_global_session()


if __name__ == "__main__":
    var_name,ql_config,manage_cmd,query_cmd,login_cmd,price,coin_price,bingfa=get_config();ql_url,ql_token=init_qinglong();main()
