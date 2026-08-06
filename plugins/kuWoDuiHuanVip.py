# [title: 酷我兑换VIP]
# [name: kuWoDuiHuanVip]
# [language: python]
# [class: 任务]
# [author: sky2022]
# [version: v1.1.1]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^酷我兑换$]
# [icon: https://api.iconify.design/lucide:apple.svg]
# [description: 。]
# [depe: ["requests"]]

import asyncio as _sg_asyncio
import os as _sg_os
import time as _sg_time
import types as _sg_types
from threading import Thread as _sg_Thread
from sillygirl import Adapter as _SGAdapter, Bucket as _SGBucket, Sender as _SGSender, sender as _sg_sender
try:
    import ast as _sg_ast
except Exception:
    _sg_ast = None
try:
    import decimal as decimal
except Exception:
    decimal = None

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

config = None
_CONFIG_FIELD_MAP = {}

import requests
import json
import time
import uuid
import random

senderID = sg.getSenderID()
sender = sg.Sender(senderID)

MAX_RETRIES = 3  # 最大重试次数
RETRY_DELAY = 1  # 重试延迟(秒)
MAX_EXCHANGE_TIMES = 5  # 每日最大兑换次数

def recognize_captcha(image_base64: str) -> str:
    try:
        ocr_url = 'https://ddddor.linzixuan.top/classification'

        if ',' in image_base64:
            image_base64 = image_base64.split(',')[1]
        image_base64 = image_base64.replace('data:image/jpeg;base64,', '')
        image_base64 = image_base64.replace('data:image/png;base64,', '')

        data = {'image': image_base64}

        response = requests.post(
            ocr_url,
            json=data,
            timeout=10
        )

        result = response.json()
        if not result or 'result' not in result:
            raise Exception("验证码识别失败: 返回结果无效")

        return result['result'].strip()

    except Exception as e:
        print(f"验证码识别出错: {str(e)}")
        raise

def login(phone: str, password: str):
    retry_count = 0

    while retry_count < MAX_RETRIES:
        try:
            captcha_url = 'http://www.kuwo.cn/api/common/captcha/getcode'
            captcha_params = {
                'reqId': str(uuid.uuid4()),
                'httpsStatus': '1'
            }

            captcha_headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Encoding': 'gzip, deflate',
                'Content-Type': 'application/json',
                'Referer': 'http://www.kuwo.cn/',
                'Accept-Language': 'zh-CN,zh;q=0.9'
            }

            response = requests.get(
                captcha_url,
                params=captcha_params,
                headers=captcha_headers
            )

            if 'data' not in response.json():
                retry_count += 1
                print(f"[重试] 获取验证码失败，第{retry_count}次重试...")
                time.sleep(RETRY_DELAY)
                continue

            captcha_data = response.json()['data']
            image_data = captcha_data['img']
            token = captcha_data['token']

            verify_code = recognize_captcha(
                image_data.replace('data:image/jpeg;base64,', '')
            )

            if not verify_code:
                retry_count += 1
                print(f"[重试] 验证码识别失败，第{retry_count}次重试...")
                time.sleep(RETRY_DELAY)
                continue

            login_url = 'https://wapi.kuwo.cn/api/www/login/loginByKw'
            login_data = json.dumps({
                'userIp': 'www.kuwo.cn',
                'uname': phone,
                'password': password,
                'verifyCode': verify_code,
                'img': image_data,
                'verifyCodeToken': token
            })

            login_headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/json',
                'Origin': 'http://www.kuwo.cn',
                'Referer': 'http://www.kuwo.cn/',
                'Accept-Language': 'zh-CN,zh;q=0.9'
            }

            login_response = requests.post(
                login_url,
                params={'httpsStatus': '1'},
                data=login_data,
                headers=login_headers,
                timeout=10
            )

            result = login_response.json()

            if result.get('code') != 200:
                error_msg = result.get('msg', '未知错误')
                if "picture captcha error" in error_msg or "验证码错误" in error_msg:
                    retry_count += 1
                    print(f"[重试] 验证码错误，第{retry_count}次重试...")
                    time.sleep(RETRY_DELAY)
                    continue
                raise Exception(f"登录失败: {error_msg}")

            data = result['data']
            cookies = data['cookies']

            loginSid = cookies.get('websid')
            loginUid = cookies.get('userid')
            appUid = ''.join(random.choices('0123456789', k=10))

            return loginUid, loginSid, appUid

        except Exception as e:
            if retry_count < MAX_RETRIES - 1:
                retry_count += 1
                print(f"[重试] 登录失败，第{retry_count}次重试: {str(e)}")
                time.sleep(RETRY_DELAY)
                continue
            raise Exception(f"登录失败: {str(e)}")

    raise Exception("登录重试次数已用完")

def exchange_vip(loginUid: str, loginSid: str, appUid: str) -> bool:
    url = "https://integralapi.kuwo.cn/api/v1/online/sign/getExchangeAward"
    params = {
        'loginUid': loginUid,
        'loginSid': loginSid,
        'appUid': appUid,
        'platform': 'ar',
        'source': 'kwplayer_ar_11.1.4.1_hw.apk',
        'version': '11.1.4.1',
        'quotaId': '13',
        'exchangeType': 'vip',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 14; POCO F2 Pro Build/UQ1A.240105.004; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/121.0.6167.101 Mobile Safari/537.36/ kuwopage',
        'Origin': 'https://h5app.kuwo.cn',
        'X-Requested-With': 'cn.kuwo.player',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        r_json = response.json()
        if '成功' in response.text:
            sender.reply(f'✅ 账号 {loginUid} 已成功兑换1个月酷我VIP')
            return True
        else:
            description = r_json['data'].get('description', '未知错误')
            sender.reply(f'❌ 账号 {loginUid} {description}')
            return False

    except Exception as e:
        sender.reply(f'❌ 账号 {loginUid} 兑换VIP失败: {str(e)}')
        return False

def main():
    try:
        sender.reply(
            "=====酷我兑换VIP=====\n"
            "📝 请输入账号信息:\n"
            "格式: 手机号#密码\n"
            "⚠️ 建议私聊操作\n"
            "⭐ 输入q退出操作\n"
            "==================="
        )

        login_info = sender.input(120000, 1, False)
        if not login_info:
            sender.reply('输入超时！')
            return
        elif login_info.lower() == 'q':
            sender.reply('已取消操作')
            return

        try:
            phone, password = login_info.split('#')
            if len(phone) != 11:
                sender.reply('手机号格式错误')
                return
        except:
            sender.reply('输入格式错误！需要手机号#密码格式')
            return

        try:
            loginUid, loginSid, appUid = login(phone, password)
        except Exception as e:
            sender.reply(f"登录失败: {str(e)}")
            return

        sender.reply(
            "=====兑换设置=====\n"
            "📝 请输入兑换次数(1-5):\n"
            "⚠️ 每日最多兑换5次\n"
            "⭐ 输入q退出操作\n"
            "==================="
        )

        exchange_times = sender.input(60000, 1, False)
        if not exchange_times:
            sender.reply('输入超时！')
            return
        elif exchange_times.lower() == 'q':
            sender.reply('已取消操作')
            return

        try:
            exchange_times = int(exchange_times)
            if exchange_times < 1 or exchange_times > MAX_EXCHANGE_TIMES:
                sender.reply(f'兑换次数必须在1-{MAX_EXCHANGE_TIMES}之间')
                return
        except:
            sender.reply('兑换次数必须是数字')
            return

        for i in range(exchange_times):
            try:
                exchange_vip(loginUid, loginSid, appUid)
                time.sleep(1)  # 添加延迟避免请求过快
            except Exception as e:
                sender.reply(f"❌ 兑换出错: {str(e)}")

    except Exception as e:
        sender.reply(f"操作失败: {str(e)}")

main()
