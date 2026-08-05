# [title: 【插件】-森选直播]
# [name: chaJianSenXuanZhiBo]
# [language: python]
# [class: 任务]
# [author: huawei]
# [version: v1.5.3]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^森选直播(登录|登陆)$|^登(录|陆)森选直播$|^森选直播(查询|管理)$|^(查询|管理)森选直播$|^森选直播$|^森选直播教程$|^森选直播清理$|^森选订阅$|^森选推送$]
# [icon: https://api.iconify.design/lucide:apple.svg]
# [description: 森选直播账号绑定、开播订阅和红包任务提醒。]
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
    'G_SXZB_ql_config': form.string().title('设置对接容器').default('').description('你的变量需要添加到的容器？参数用丨分割，这个符号是中文的竖(直接复制)'),
    'G_SXZB_var_name': form.string().title('青龙变量名').default('').description('提交到青龙面板的环境变量名称'),
    'G_SXZB_push_admins': form.string().title('管理员列表').default('').description('接收推送报告的管理员QQ/微信号'),
    'G_SXZB_push_message': form.string().title('推送文字').default('').description('开播推送的自定义文字，不填使用默认文字'),
})
_CONFIG_FIELD_MAP = {
    ('G_SXZB', 'ql_config'): 'G_SXZB_ql_config',
    ('G_SXZB', 'var_name'): 'G_SXZB_var_name',
    ('G_SXZB', 'push_admins'): 'G_SXZB_push_admins',
    ('G_SXZB', 'push_message'): 'G_SXZB_push_message',
}

from datetime import datetime
import requests
import os
import json
import re
import time
import random
import hashlib
from typing import List, Dict, Any

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()

class SenxuanClient:
    """森选直播客户端"""
    def __init__(self, token_with_remark):
        if '#' in token_with_remark:
            self.remark, self.raw_token = token_with_remark.split('#', 1)
            self.remark = self.remark.strip()
            self.raw_token = self.raw_token.strip()
        else:
            self.raw_token = token_with_remark.strip()
            self.remark = "默认账号"

        if self.raw_token.lower().startswith("bearer "):
            self.token = self.raw_token  # 保留原有格式
        else:
            self.token = f"Bearer {self.raw_token}"  # 添加Bearer前缀

        self.base_url = "https://n03.sentezhenxuan.com/api"
        self.session = requests.Session()

        self.headers = {
            "Accept-Encoding": "gzip,compress,br,deflate",
            "content-type": "application/json",
            "Connection": "keep-alive",
            "Referer": "https://servicewechat.com/wx890e6dc32d83d24c/1/page-frame.html",
            "Authori-zation": self.token,  # 使用带Bearer前缀的token
            "Host": "n03.sentezhenxuan.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF",
            "Cb-lang": "zh-CN",
            "Form-type": "routine-sxfengshang",
            "xweb_xhr": "1"
        }
        self.session.headers.update(self.headers)

    def get_user_info(self):
        """获取用户信息"""
        url = f"{self.base_url}/user/detail"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data.get("status") == 200 and data.get("data"):
                return data.get("data")
            return None
        except Exception as e:
            print(f"获取用户信息失败: {e}")
            try:
                commission_url = f"{self.base_url}/spread/commission/0?page=1&limit=5"
                comm_response = self.session.get(commission_url, timeout=10)
                comm_data = comm_response.json()
                if comm_data.get("status") == 200:
                    user_transactions = comm_data.get("data", {}).get("list", [])
                    if user_transactions and len(user_transactions) > 0:
                        uid = user_transactions[0].get("uid")
                        if uid:
                            return {"id": uid, "nickname": self.remark}
            except:
                pass
            return None

    def get_user_info_new(self):
        """获取用户详细信息"""
        url = f"{self.base_url}/updateTxInfo"
        try:
            print("正在获取用户详细信息...")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data.get("status") == 200 and data.get("data"):
                return data.get("data")
            return None
        except Exception as e:
            print(f"获取用户详细信息失败: {e}")
            return None

    def get_video_detail(self, vid: int) -> Dict[str, Any]:
        """获取单个视频详情"""
        url = f"{self.base_url}/video/getOneVideo?vid={vid}"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data.get("status") == 200 and data.get("data"):
                return data.get("data")
            return None
        except Exception as e:
            return None

    def add_user_view_num(self, vid: int) -> Dict[str, Any]:
        """记录用户观看视频"""
        url = f"{self.base_url}/video/addUserViewNum"
        body = {
            "vid": vid,
            "baseVersion": "3.10.2",
            "playMode": 0
        }
        try:
            print(f"  正在记录观看，视频ID: {vid}")
            response = self.session.post(url, json=body, timeout=10)
            response.raise_for_status()
            result = response.json()
            print(f"  记录观看结果: {result.get('msg')}")
            return result
        except Exception as e:
            print(f"  记录观看请求异常: {e}")
            return {"status": 500, "msg": str(e)}

    def video_job(self, vid: int, wait_time: int) -> Dict[str, Any]:
        """提交视频观看完成"""
        url = f"{self.base_url}/video/videoJob"

        start_time = int(time.time() * 1000)
        end_time = start_time + (wait_time * 1000) + 1000

        body = {
            "vid": vid,
            "startTime": start_time,
            "endTime": end_time,
            "baseVersion": "3.10.2",
            "playMode": 0
        }

        try:
            print(f"  等待 {wait_time} 秒...")
            time.sleep(wait_time)

            print(f"  正在提交观看完成...")
            response = self.session.post(url, json=body, timeout=10)
            response.raise_for_status()
            result = response.json()
            print(f"  提交观看完成: {result.get('msg')}")
            return result
        except Exception as e:
            print(f"  提交观看完成失败: {e}")
            return {"status": 500, "msg": str(e)}

    def reward_user_small_change(self) -> Dict[str, Any]:
        """获取答题奖励"""
        url = f"{self.base_url}/video/rewardUserSmallChange"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            result = response.json()
            return result
        except Exception as e:
            return {"status": 500, "msg": str(e)}

    def get_video_ids(self) -> List[int]:
        """一次性获取所有视频ID"""
        try:
            print("正在请求视频列表...")
            url = f"{self.base_url}/video/list?page=1&limit=50&status=1&source=0&isXn=1"

            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()

            if data.get("status") == 200 and data.get("data"):
                video_list = data.get("data")
                if isinstance(video_list, list) and len(video_list) > 0:
                    video_ids = [video.get("id") for video in video_list if video.get("id")]
                    print(f"成功获取 {len(video_ids)} 个视频")
                    return video_ids

            print(f"获取失败: {data.get('msg')}")
            return []

        except Exception as e:
            print(f"请求异常: {e}")
            return []

    def watch_video(self, vid: int) -> Dict[str, Any]:
        """刷视频 - 使用原脚本逻辑"""
        url = f"{self.base_url}/video/videoJob"

        end_time = int(time.time() * 1000)
        start_time = end_time - 80000  # 假设观看了约80秒

        body = {
            "vid": vid,
            "startTime": start_time,
            "endTime": end_time,
            "baseVersion": "3.5.8",
            "playMode": 0
        }

        try:
            print(f"正在刷视频，ID: {vid}")
            response = self.session.post(url, json=body, timeout=10)
            response.raise_for_status()

            result = response.json()
            print(f"刷视频结果: {result.get('msg')}")
            return result
        except Exception as e:
            print(f"刷视频请求异常: {e}")
            return {"status": 500, "msg": str(e)}

    def withdraw(self) -> Dict[str, Any]:
        """提现 - 使用原脚本逻辑"""
        url = f"{self.base_url}/userTx?"

        try:
            print("正在尝试提现...")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            result = response.json()
            print(f"提现结果: {result.get('msg')}")
            return result
        except Exception as e:
            print(f"提现请求异常: {e}")
            return {"status": 500, "msg": str(e)}

    def get_commission_info(self):
        """获取佣金信息"""
        url = f"{self.base_url}/spread/commission/0?page=1&limit=5"
        try:
            print("正在获取佣金信息...")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("status") == 200 and data.get("data"):
                commission_data = data.get("data", {})
                commission_list = commission_data.get("list", [])
                return {
                    "success": True,
                    "records": commission_list,
                    "count": len(commission_list)
                }
            return {"success": False, "msg": data.get("msg", "未知错误")}
        except Exception as e:
            print(f"获取佣金信息失败: {e}")
            return {"success": False, "msg": str(e)}

    def run_daily_task(self) -> Dict[str, Any]:
        """运行每日任务 - 已禁用"""
        return {
            "video_count": 0,
            "success_videos": 0,
            "answer_videos": 0,
            "withdraw": None,
            "balance": 0,
            "commission": None
        }

    def get_withdraw_records(self):
        """获取提现记录 - 使用专用接口"""
        url = f"{self.base_url}/spread/commission/1?page=1&limit=15"
        try:
            print("正在获取提现记录...")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("status") == 200 and data.get("data"):
                withdraw_data = data.get("data", {})
                withdraw_list = withdraw_data.get("list", [])
                return {
                    "success": True,
                    "records": withdraw_list,
                    "count": len(withdraw_list)
                }
            return {"success": False, "msg": data.get("msg", "未知错误")}
        except Exception as e:
            print(f"获取提现记录失败: {e}")
            return {"success": False, "msg": str(e)}

def get_config():
    """获取插件配置"""
    try:
        price_str = sg.bucketGet(bucket='G_SXZB', key='price') or '0.88'
        price = float(price_str) if price_str.replace('.', '', 1).isdigit() else 0.88
        zsm = sg.bucketGet(bucket='G_SXZB', key='zsm') or ''
        points_per_month_str = sg.bucketGet(bucket='G_SXZB', key='points_per_month') or '100'
        points_per_month = int(points_per_month_str) if points_per_month_str.isdigit() else 100

        return {
            'price': price,
            'zsm': zsm,
            'points_per_month': points_per_month
        }
    except:
        return {'price': 0.88, 'zsm': '', 'points_per_month': 100}

class QingLongAPI:
    def __init__(self, url, client_id, client_secret):
        self.base_url = url.rstrip('/')
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None

    def login(self):
        try:
            url = f"{self.base_url}/open/auth/token?client_id={self.client_id}&client_secret={self.client_secret}"
            r = requests.get(url, timeout=10)
            data = r.json()
            if data.get('code') == 200:
                self.token = data['data']['token']
                return True, "登录成功"
            return False, data.get('message', '登录失败')
        except Exception as e:
            return False, str(e)

    def get_envs(self, name=None):
        if not self.token: return []
        try:
            url = f"{self.base_url}/open/envs"
            if name: url += f"?searchValue={name}"
            r = requests.get(url, headers={"Authorization": f"Bearer {self.token}"}, timeout=10)
            return r.json().get('data', []) if r.json().get('code') == 200 else []
        except:
            return []

    def add_env(self, name, value, remarks=""):
        if not self.token: return False, "未登录"
        try:
            r = requests.post(f"{self.base_url}/open/envs", json=[{"name": name, "value": value, "remarks": remarks}], headers={"Authorization": f"Bearer {self.token}"}, timeout=10)
            return r.json().get('code') == 200, r.json().get('message', '')
        except Exception as e:
            return False, str(e)

    def update_env(self, env_id, name, value, remarks=""):
        if not self.token: return False, "未登录"
        try:
            r = requests.put(f"{self.base_url}/open/envs", json={"id": env_id, "name": name, "value": value, "remarks": remarks}, headers={"Authorization": f"Bearer {self.token}"}, timeout=10)
            return r.json().get('code') == 200, r.json().get('message', '')
        except Exception as e:
            return False, str(e)

def get_ql_config():
    ql_str = sg.bucketGet(bucket='G_SXZB', key='ql_config') or ''
    if '丨' in ql_str:
        parts = ql_str.split('丨')
        return {
            'url': parts[0].strip() if len(parts) > 0 else '',
            'client_id': parts[1].strip() if len(parts) > 1 else '',
            'client_secret': parts[2].strip() if len(parts) > 2 else ''
        }
    return {'url': '', 'client_id': '', 'client_secret': ''}

def upload_to_qinglong():
    if not sender.isAdmin():
        sender.reply("❌ 仅管理员可使用此功能")
        return
    ql_config = get_ql_config()
    if not all([ql_config['url'], ql_config['client_id'], ql_config['client_secret']]):
        sender.reply("❌ 青龙配置不完整，请先配置青龙地址、ClientID、ClientSecret")
        return
    all_users = sg.bucketKeys(bucket='G_sxzb_user') or []
    if not all_users:
        sender.reply("❌ 没有找到任何账号")
        return
    sender.reply("⏳ 正在连接青龙...")
    ql = QingLongAPI(ql_config['url'], ql_config['client_id'], ql_config['client_secret'])
    success, msg = ql.login()
    if not success:
        sender.reply(f"❌ 青龙连接失败: {msg}")
        return
    tokens = []
    for user in all_users:
        accounts = get_user_accounts(user)
        for account_id in accounts:
            auth_data = '2099-12-31'
            if not auth_data: continue
            try:
                auth_info = json.loads(auth_data)
                expire_date = auth_info.get('expire_time', '')
                if expire_date and datetime.strptime(expire_date, "%Y-%m-%d").date() < datetime.now().date(): continue
            except: continue
            token_data = sg.bucketGet('G_sxzb_token', account_id)
            if token_data: tokens.append(token_data)
    if not tokens:
        sender.reply("❌ 没有找到有效授权的账号")
        return
    env_name = "G_SXZB_TOKEN"
    env_value = "\n".join(tokens)
    existing = ql.get_envs(env_name)
    target_env = next((e for e in existing if e.get('name') == env_name), None)
    if target_env:
        success, msg = ql.update_env(target_env['id'], env_name, env_value, f"森选Token-{len(tokens)}个")
        action = "更新"
    else:
        success, msg = ql.add_env(env_name, env_value, f"森选Token-{len(tokens)}个")
        action = "添加"
    if success:
        sender.reply(f"✅ 上传青龙成功！\n📦 变量名: {env_name}\n👥 账号数: {len(tokens)}个\n🔄 操作: {action}")
    else:
        sender.reply(f"❌ 上传失败: {msg}")

def auto_upload_qinglong(account_id=None):
    """自动上传token到青龙面板，统一变量名，通过remarks区分账号，返回(成功状态, 消息)"""
    ql_config = get_ql_config()
    if not all([ql_config['url'], ql_config['client_id'], ql_config['client_secret']]):
        return False, "青龙配置未完成"

    ql = QingLongAPI(ql_config['url'], ql_config['client_id'], ql_config['client_secret'])
    success, msg = ql.login()
    if not success:
        return False, f"青龙登录失败: {msg}"

    env_name = "G_SXZB_TOKEN"

    if account_id:
        token_data = sg.bucketGet('G_sxzb_token', account_id)
        if not token_data:
            return False, "Token数据缺失"

        if '#' in token_data:
            remark = token_data.split('#', 1)[0].strip()
        else:
            remark = "默认账号"

        auth_data = '2099-12-31'
        if auth_data:
            try:
                auth_info = json.loads(auth_data)
                expire_time = auth_info.get('expire_time', '未知')
            except:
                expire_time = '未知'
        else:
            expire_time = '未知'

        remarks = f"森选直播:{account_id}丨用户:{userid}丨到期:{expire_time}丨备注:{remark}"

        all_envs = ql.get_envs(env_name)
        existing_env = None
        for env in all_envs:
            env_remarks = env.get('remarks', '')
            env_envname = env.get('name', '')
            if env_envname == env_name and account_id in env_remarks:
                existing_env = env
                break

        if existing_env:
            success, msg = ql.update_env(existing_env['id'], env_name, token_data, remarks)
            if success:
                return True, f"已更新到青龙"
            else:
                return False, f"青龙更新失败: {msg}"
        else:
            success, msg = ql.add_env(env_name, token_data, remarks)
            if success:
                return True, f"已上传到青龙"
            else:
                return False, f"青龙添加失败: {msg}"

    return False, "未指定账号ID"

def get_user_accounts(user_id=None):
    if user_id is None: user_id = userid
    uservalue = sg.bucketGet('G_sxzb_user', user_id) or '[]'
    try:
        accounts_list = json.loads(uservalue)
        return [str(acc) for acc in accounts_list] if isinstance(accounts_list, list) else [str(accounts_list)]
    except:
        return []

def get_user_points(user_id=None):
    return 0

def set_user_points(user_id, points):
    """设置用户积分 - 适配呆呆积分数据结构"""
    sg.bucketSet('dd_sign_coin', user_id, str(points['dd_sign_coin']))
    sg.bucketSet('dd_sign_points', user_id, str(points['dd_sign_points']))

    sign_key = f"sign_{user_id}"
    sg.bucketSet('dd_sign_coin', sign_key, str(points['dd_sign_coin']))
    return True

def verify_live_api(token: str) -> Dict[str, Any]:
    """使用直播接口验证token有效性"""
    url = "https://yh.sentezhenxuan.com/api/mobile/shop-live/room/getLiveRoomActivity"
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "authorization": token,
        "app-sign": "wx1b482e08a5617509",
        "referer": "https://servicewechat.com/wx1b482e08a5617509/7/page-frame.html",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF"
    }
    params = {
        "source_type": 2314,
        "source_from": 2321,
        "source_lang": "zh_CN",
        "currency_id": 86,
        "site_id": "",
        "roomId": 2781
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("code") == 0:
            user_id = None
            try:
                import base64
                token_without_bearer = token.replace("Bearer ", "").replace("bearer ", "")
                payload = token_without_bearer.split('.')[1]
                padding = len(payload) % 4
                if padding:
                    payload += '=' * (4 - padding)
                decoded = base64.b64decode(payload)
                jwt_data = json.loads(decoded)
                user_id = jwt_data.get('id')
            except:
                pass

            return {
                "success": True,
                "user_id": user_id,
                "data": data
            }
        else:
            return {
                "success": False,
                "msg": data.get('msg', '未知错误'),
                "data": data
            }
    except Exception as e:
        return {
            "success": False,
            "msg": str(e),
            "error": e
        }

def validate_token(token_with_remark):
    """验证Token有效性并返回账号信息"""
    try:
        if '#' in token_with_remark:
            remark, raw_token = token_with_remark.split('#', 1)
            remark = remark.strip()
            token = raw_token.strip()
        else:
            token = token_with_remark.strip()
            remark = "默认账号"

        if len(token) < 10:  # 合理的最小长度
            return False, {'error': 'Token格式错误，长度不足'}

        if token.lower().startswith("bearer "):
            full_token = token
        else:
            full_token = f"Bearer {token}"

        live_result = verify_live_api(full_token)
        if live_result["success"]:
            account_id = live_result.get("user_id")
            if account_id:
                return True, {
                    'account_id': str(account_id),
                    'nickname': remark
                }
            timestamp = int(time.time() * 1000)
            account_id = f"sxzb_{hashlib.md5(str(timestamp).encode()).hexdigest()[:10]}"
            return True, {
                'account_id': str(account_id),
                'nickname': remark
            }

        return False, {'error': f'直播API验证失败: {live_result.get("msg", "未知错误")}'}

    except Exception as e:
        return False, {'error': f'验证失败: {str(e)}'}

def bindaccount():
    """森选登录绑定 - 支持批量登录"""
    welcome_msg = """
=====森选直播登录=====
请按格式输入: 备注#authorization
示例: 张三#eyJ0eXAiOi...

🔰 支持批量登录，一行一个账号
示例:
张三#eyJ0eXAiOi...
李四#eyJ0eXAiOi...

⚠️ 复制token时请勿包含Bearer前缀
------------------
回复「q」退出绑定
=================="""
    sender.reply(welcome_msg)
    ck_input = sender.input(120000, 1, False).strip()
    if ck_input.lower() == 'q':
        sender.reply("✅ 已取消登录")
        return

    account_lines = ck_input.strip().split('\n')
    is_batch = len(account_lines) > 1

    if is_batch:
        sender.reply("⏳ 正在处理批量登录请求，请稍候...")

    success_count = 0
    fail_count = 0
    failed_accounts = []
    accounts = get_user_accounts()
    last_success_info = None

    for line in account_lines:
        line = line.strip()
        if not line:
            continue

        if '#' not in line:
            fail_count += 1
            failed_accounts.append({'account': line[:20] + '...' if len(line) > 20 else line, 'reason': '格式错误(缺少#分隔)'})
            continue

        remark, access_token = line.split('#', 1)
        remark = remark.strip()
        access_token = access_token.strip()

        if access_token.lower().startswith("bearer "):
            access_token = access_token[7:].strip()
        access_token = access_token.strip('"\'').strip()

        if len(access_token) < 20:
            fail_count += 1
            failed_accounts.append({'account': remark, 'reason': 'Token长度过短'})
            continue

        token_with_remark = f"{remark}#{access_token}"

        is_valid, result = validate_token(token_with_remark)
        if not is_valid:
            fail_count += 1
            error_msg = result.get('error', '未知错误')
            failed_accounts.append({'account': remark, 'reason': error_msg[:30]})
            continue

        account_id = result.get('account_id', "unknown")

        sg.bucketSet(bucket='G_sxzb_token', key=str(account_id), value=token_with_remark)

        if account_id not in accounts:
            accounts.append(account_id)

        auth_data = '2099-12-31'
        if auth_data:
            try:
                auto_upload_qinglong(account_id)
            except:
                pass

        success_count += 1
        last_success_info = {'account_id': account_id, 'remark': remark}

    if accounts:
        sg.bucketSet('G_sxzb_user', userid, json.dumps(accounts))

    if is_batch:
        result_msg = f"""
=====批量登录结果=====
✅ 成功: {success_count}个账号
❌ 失败: {fail_count}个账号"""

        if failed_accounts:
            result_msg += "\n------------------\n⚠️ 失败账号详情:"
            for idx, fail_info in enumerate(failed_accounts[:5], 1):
                result_msg += f"\n{idx}. {fail_info['account']}\n   原因: {fail_info['reason']}"
            if len(failed_accounts) > 5:
                result_msg += f"\n...还有{len(failed_accounts)-5}个失败"

        result_msg += "\n------------------\n💡 发送「森选直播管理」可管理账号\n=================="
        sender.reply(result_msg)
    elif success_count == 1 and last_success_info:
        sender.reply(f"""
✅ 登录成功
🆔 账号ID: {last_success_info['account_id']}
🏷️ 备注: {last_success_info['remark']}

发送「森选直播管理」进行账号授权""")
    else:
        sender.reply("❌ 登录失败")

def query_account_status():
    """查询账号状态"""
    accounts = get_user_accounts()

    if not accounts:
        sender.reply("❌ 您尚未绑定任何账号，请先绑定")
        return

    all_results = []

    for idx, account_id in enumerate(accounts, 1):
        token_with_remark = sg.bucketGet('G_sxzb_token', account_id)
        if not token_with_remark:
            all_results.append(f"账号 {idx}: ❌ Token缺失")
            continue

        if '#' in token_with_remark:
            remark, token = token_with_remark.split('#', 1)
            remark = remark.strip()
            token = token.strip()
        else:
            token = token_with_remark.strip()
            remark = "默认账号"

        display_name = remark

        result_msg = f"------ 森选详情 [{idx}] ------\n"
        result_msg += f"📱 账号: {display_name}\n"

        auth_data = '2099-12-31'
        expire_date = "未知"
        if auth_data:
            try:
                auth_info = json.loads(auth_data)
                expire_date = auth_info.get('expire_time', '未知')
                result_msg += f"🔐 授权状态: ✅ 已授权\n"
                result_msg += f"📅 到期时间: {expire_date}\n"

                if expire_date != "未知":
                    try:
                        expire_date_obj = datetime.strptime(expire_date, "%Y-%m-%d").date()
                        today = datetime.now().date()
                        days_left = (expire_date_obj - today).days

                        if days_left < 0:
                            result_msg += "⚠️ 🚨 授权已过期，即将自动删除！\n"
                        elif days_left < 4:
                            result_msg += f"⚠️ 🔥 授权即将到期！还有{days_left}天\n"
                            result_msg += "💡 过期自动删除账号！\n"
                    except:
                        pass
            except:
                result_msg += "🔐 授权状态: ✅ 已授权\n"
                result_msg += "📅 到期时间: 未知\n"
        else:
            result_msg += "🔐 授权状态: ❌ 未授权\n"

        try:
            client = SenxuanClient(token_with_remark)
            withdraw_info = client.get_withdraw_records()

            if withdraw_info and withdraw_info.get("success") and withdraw_info.get("records"):
                withdraw_records = withdraw_info.get("records")
                total_amount = sum(float(r.get("number", "0")) for r in withdraw_records)

                result_msg += f"💰 成功领取: {len(withdraw_records)}笔, 总计: {total_amount:.2f}元\n"

                if withdraw_records:
                    result_msg += "------ 🎁任务完成🎁 ------\n"
                    for record in withdraw_records[:5]:
                        amount = record.get("number", "0")
                        add_time = record.get("add_time", "未知")
                        result_msg += f"现金{amount}元-{add_time}\n"
            elif token:
                bearer_token = f"Bearer {token}" if not token.lower().startswith("bearer ") else token
                live_result = verify_live_api(bearer_token)
                if live_result.get("success"):
                    result_msg += "✅ Token有效\n"
                else:
                    result_msg += "❌ 你掉CK了,发森选管理更新CK\n"
        except Exception as e:
            result_msg += f"❌ 查询失败: {str(e)[:50]}\n"

        all_results.append(result_msg)

    final_result = "\n".join(all_results) + "\n------------------------"
    sender.reply(final_result)

def show_tutorial():
    """显示使用教程"""
    tutorial = """
=====森选直播使用教程=====
1️⃣ 「森选直播登录」绑定账号
   - 获取方法：微信小程序【银鱼质亨】直播间
   - 抓取域名：yh.sentezhenxuan.com
   - 抓取字段：authorization (去除Bearer前缀)
   - 格式：备注#token (例如：我的账号#eyJ0eXAiOi...)

2️⃣ 「森选直播管理」进行账号授权
   - 支持微信支付或积分支付
   - 可更新账号token（token过期时使用）
   - 授权后可自动抢直播间红包

3️⃣ 「森选直播查询」查询账号状态
   - 查看账号授权状态
   - 查看到期时间
   - 查看token有效性

👉 手动抓包教程:
1. 打开微信小程序【银鱼质亨】
2. 进入直播间页面
3. 使用抓包工具监听请求
4. 找到yh.sentezhenxuan.com域名请求
5. 推荐URL: /api/mobile/shop-live/room/getLiveRoomActivity
6. 复制请求头中的authorization值
7. 使用"备注#token"格式添加账号
   例如：张三#eyJ0eXAiOi...

💡 Token失效问题处理:
1. 在「森选直播管理」中选择账号后，选择"更新账号"
2. 重新打开小程序直播间并抓包获取新token
3. 输入新token（可保留原备注）
4. 系统会自动验证token有效性
=================="""
    sender.reply(tutorial)

def sz_manage():
    """账号管理 - 支持批量授权合并支付"""
    accounts = get_user_accounts()
    if not accounts:
        sender.reply("❌ 您还没有绑定账号，请先发送【森选直播登录】绑定")
        return

    authorized_count = 0
    unauthorized_accounts = []
    account_list = []

    for idx, account_id in enumerate(accounts, 1):
        token_data = sg.bucketGet('G_sxzb_token', account_id)
        if not token_data:
            continue

        remark = "默认账号"
        if '#' in token_data:
            remark = token_data.split('#', 1)[0].strip()

        auth_data = '2099-12-31'
        if auth_data:
            authorized_count += 1
            try:
                auth_info = json.loads(auth_data)
                expire_date = auth_info.get('expire_time', '未知')
                expire_date_obj = datetime.strptime(expire_date, "%Y-%m-%d").date()
                today = datetime.now().date()
                days_left = (expire_date_obj - today).days
                if days_left >= 0:
                    status = f"✅已授权({days_left}天)"
                else:
                    status = "⚠️已过期"
            except:
                status = "✅已授权"
        else:
            unauthorized_accounts.append(account_id)
            status = "❌未授权"

        account_list.append(f"[{idx}] {remark} {status}")

    batch_options = []
    if len(accounts) > 0:
        batch_options.append("[0] 授权所有账号")
    if unauthorized_accounts:
        batch_options.append("[9999] 授权未授权账号")

    if batch_options:
        account_list.append("")
        account_list.extend(batch_options)

    account_list_str = "\n".join(account_list)
    user_points = get_user_points()

    menu_msg = f"""=====森选直播管理=====
🔢 绑定账号: {len(accounts)}个
✅ 已授权: {authorized_count}个
❌ 未授权: {len(unauthorized_accounts)}个
💎 当前积分: {user_points['total']}
-------------------------
{account_list_str}
------------------
回复序号选择账号操作（q退出）
=================="""

    sender.reply(menu_msg)
    choice = sender.input(60000, 1, False).strip()

    if choice.lower() == 'q':
        sender.reply("✅ 已退出管理")
        return

    if choice == '0':
        batch_authorize_accounts(accounts)
        return
    elif choice == '9999':
        batch_authorize_accounts(unauthorized_accounts)
        return

    if not choice.isdigit():
        sender.reply("❌ 输入无效")
        return

    selected_idx = int(choice) - 1
    if selected_idx < 0 or selected_idx >= len(accounts):
        sender.reply("❌ 序号无效")
        return

    account_id = accounts[selected_idx]
    token_data = sg.bucketGet('G_sxzb_token', account_id)
    remark = "默认账号"
    if token_data and '#' in token_data:
        remark = token_data.split('#', 1)[0].strip()

    sender.reply(f"""你选择了账号: {remark}
[1] 授权账号
[2] 更新token
[3] 删除账号
回复q退出""")

    op = sender.input(60000, 1, False).strip()

    if op == '1':
        _handle_authorize_single(account_id)
    elif op == '2':
        _handle_update_token_single(account_id, remark)
    elif op == '3':
        _handle_delete_account_single(account_id, remark)

def batch_authorize_accounts(target_accounts):
    return True

def _batch_wechat_payment(accounts, months, amount, config):
    return True

def _batch_points_payment(accounts, months, required_points):
    return True

def _handle_authorize_single(account_id):
    return True

def _process_wechat_payment(account_id, config):
    return True

def _process_points_payment(account_id, config):
    return True

def _handle_update_token_single(account_id, old_remark):
    """处理更新token"""
    sg.bucketGet('G_sxzb_token', account_id)

    sender.reply(f"""=====更新Token=====
📱 账号: {old_remark}
------------------
请输入新的token:
格式: 备注#token
或直接输入token(保留原备注)
------------------
回复「q」取消更新
==================""")

    new_token_input = sender.input(120000, 1, False).strip()
    if new_token_input.lower() == 'q':
        sender.reply("✅ 已取消更新")
        return

    if '#' in new_token_input:
        new_remark, new_token = new_token_input.split('#', 1)
        new_remark = new_remark.strip()
        new_token = new_token.strip()
    else:
        new_remark = old_remark
        new_token = new_token_input.strip()

    if new_token.lower().startswith("bearer "):
        new_token = new_token[7:].strip()

    token_with_remark = f"{new_remark}#{new_token}"
    is_valid, result = validate_token(token_with_remark)

    if not is_valid:
        sender.reply(f"❌ Token验证失败: {result.get('error', '未知错误')}")
        return

    sg.bucketSet('G_sxzb_token', account_id, token_with_remark)
    sender.reply(f"""✅ 更新成功
📱 账号: {new_remark}
🔑 Token已更新""")

def _handle_delete_account_single(account_id, remark):
    """处理删除账号"""
    sg.bucketGet('G_sxzb_token', account_id)

    sender.reply(f"""=====确认删除=====
📱 账号: {remark}
⚠️ 删除后无法恢复
------------------
确认删除请回复「确认」
回复「q」取消删除
==================""")

    confirm = sender.input(30000, 1, False).strip()
    if confirm != "确认":
        sender.reply("✅ 已取消删除")
        return

    sg.bucketDel('G_sxzb_token', account_id)
    True
    accounts = get_user_accounts()
    if account_id in accounts:
        accounts.remove(account_id)
    sg.bucketSet('G_sxzb_user', userid, json.dumps(accounts))

    sender.reply(f"✅ 删除成功\n📱 账号: {remark}")

def admin_authorize_account():
    return True
def sz_clean_accounts():
    """清理未授权和授权过期的森选直播账号"""
    if not sender.isAdmin():
        sender.reply("""
=====权限不足=====
❌ 您没有权限执行此操作
==================""")
        return

    users = sg.bucketAllKeys(bucket='G_sxzb_user')

    if not users:
        sender.reply("""
=====清理结果=====
❌ 未找到任何绑定账号
==================""")
        return

    sender.reply(f"""
=====开始清理=====
📊 共找到: {len(users)}个用户
⏳ 清理中请稍候...
==================""")

    cleaned_count = 0
    failed_count = 0
    today = datetime.now().date()

    for user in users:
        try:
            accountlist = sg.bucketGet(bucket='G_sxzb_user', key=f'{user}')
            if not accountlist:
                continue

            accounts = json.loads(accountlist)
            if not isinstance(accounts, list):
                accounts = [accounts]

            valid_accounts = []

            for account_id in accounts:
                should_delete = False
                auth_data_str = '2099-12-31'

                if not auth_data_str:
                    should_delete = True
                else:
                    try:
                        auth_data = json.loads(auth_data_str)
                        expire_date = auth_data.get('expire_time')

                        if expire_date:
                            expire_date_obj = datetime.strptime(expire_date, "%Y-%m-%d").date()
                            if expire_date_obj < today:
                                should_delete = True
                    except:
                        should_delete = True

                if should_delete:
                    try:
                        sg.bucketDel(bucket='G_sxzb_token', key=account_id)
                        True
                        cleaned_count += 1
                    except:
                        failed_count += 1
                else:
                    valid_accounts.append(account_id)

            if valid_accounts:
                sg.bucketSet(bucket='G_sxzb_user', key=user, value=json.dumps(valid_accounts))
            else:
                sg.bucketDel(bucket='G_sxzb_user', key=user)

        except Exception as e:
            failed_count += 1
            continue

    total_processed = cleaned_count + failed_count
    if total_processed > 0:
        efficiency = (cleaned_count / total_processed) * 100
        result_msg = f"""
=====清理完成=====
✅ 成功清理: {cleaned_count}个账号
❌ 清理失败: {failed_count}个账号
📊 清理效率: {efficiency:.1f}%
=================="""
    else:
        result_msg = f"""
=====清理完成=====
✅ 未发现需要清理的账号
所有账号均为有效授权状态
=================="""

    sender.reply(result_msg)

def get_random_ua():
    """生成随机UA"""
    versions = ['126.0.0.0', '127.0.0.0', '128.0.0.0', '129.0.0.0', '130.0.0.0', '131.0.0.0', '132.0.0.0']
    wechat_versions = ['7.0.20.1781', '7.0.21.1800', '7.0.22.1850']
    return f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.choice(versions)} Safari/537.36 MicroMessenger/{random.choice(wechat_versions)} NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF"

def get_live_room_list():
    """获取直播间列表"""
    url = "https://yh.sentezhenxuan.com/api/mobile/shop-live/room/getLiveRoomList"
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "app-sign": "wx1b482e08a5617509",
        "user-agent": get_random_ua()
    }
    params = {
        "source_type": 2314,
        "source_from": 2321,
        "source_lang": "zh_CN",
        "currency_id": 86,
        "site_id": ""
    }
    try:
        r = requests.get(url, headers=headers, params=params, timeout=10)
        data = r.json()
        return data.get("data", []) if data.get("code") == 0 else []
    except:
        return []

def get_all_authorized_users():
    return True

def sz_subscribe():
    """用户订阅/取消订阅开播提醒"""
    current_status = sg.bucketGet('G_sxzb_subscribe', userid) or 'on'

    if current_status == 'on':
        sg.bucketSet('G_sxzb_subscribe', userid, 'off')
        sender.reply("✅ 已关闭订阅")
    else:
        sg.bucketSet('G_sxzb_subscribe', userid, 'on')
        sender.reply("""✅ 订阅成功！

🔔 开播后将自动推送通知
⚠️ 请及时抓包更新token

👉 发送「森选直播管理」更新token
👉 再次发送「森选订阅」可关闭""")

def sz_push():
    """手动触发推送（自动模式）"""
    custom_msg = sg.bucketGet('G_SXZB', 'push_message') or ''
    subscribers = get_subscribers()

    if not subscribers:
        sender.reply("❌ 没有用户订阅，无需推送")
        return

    if custom_msg:
        message = custom_msg

        success_count = 0
        push_errors = []

        for user_id in subscribers:
            push_success = False
            try:
                sg.push('wx', '', user_id, '', message)
                push_success = True
            except Exception as wx_err:
                push_errors.append(f"WX-{user_id}: {str(wx_err)[:30]}")

            try:
                sg.push('qq', '', user_id, '', message)
                push_success = True
            except Exception as qq_err:
                push_errors.append(f"QQ-{user_id}: {str(qq_err)[:30]}")

            if push_success:
                success_count += 1

        report = f"""✅ 自定义文字推送完成
👥 订阅用户: {len(subscribers)}个
📧 推送成功: {success_count}次
📝 推送内容:
{message}"""

        if push_errors:
            report += "\n------------------\n⚠️ 推送错误:\n" + "\n".join([f"• {e}" for e in push_errors[:5]])

        sender.reply(report)

        admin_list = sg.bucketGet('G_SXZB', 'push_admins') or ''
        if admin_list:
            admins = [a.strip() for a in admin_list.split(',') if a.strip()]
            try:
                sg.notifyMasters(report, admins)
            except:
                pass
        return

    clean_old_push_records()
    rooms = get_live_room_list()
    today = datetime.now().strftime('%Y-%m-%d')
    active_rooms = [r for r in rooms if r.get('start_time', '').startswith(today) and r.get('status') == '0' and '测' not in r.get('title', '')]

    if not active_rooms:
        sender.reply("❌ 当前没有今天开播的直播间")
        return

    success_count = 0
    pushed_rooms = []
    push_errors = []

    for room in active_rooms:
        push_key = f"room_{room['id']}_{today}"
        if sg.bucketGet('G_sxzb_pushed', push_key):
            continue

        message = f"""🔴 森选直播开播提醒

📺 直播间: {room.get('title', '未知')}
🕐 开播时间: {room.get('start_time', '未知')}
👤 主播: {room.get('anchor_name', '未知')}

⚠️ Token可能失效，请及时抽包更新！
👉 发送「森选直播管理」更新token"""

        room_success = 0
        for user_id in subscribers:
            push_success = False
            try:
                sg.push('wx', '', user_id, '森选直播开播', message)
                push_success = True
            except Exception as wx_err:
                push_errors.append(f"WX-{user_id}: {str(wx_err)[:30]}")

            try:
                sg.push('qq', '', user_id, '森选直播开播', message)
                push_success = True
            except Exception as qq_err:
                push_errors.append(f"QQ-{user_id}: {str(qq_err)[:30]}")

            if push_success:
                room_success += 1

        sg.bucketSet('G_sxzb_pushed', push_key, 'true')
        success_count += room_success
        pushed_rooms.append(room['title'])

    room_list = '\n'.join([f"• {r}" for r in pushed_rooms])
    report = f"""✅ 直播间开播推送完成
📺 直播间: {len(pushed_rooms)}个
👥 订阅用户: {len(subscribers)}个
📧 推送次数: {success_count}次
------------------
{room_list}"""

    if push_errors:
        report += "\n------------------\n⚠️ 推送错误:\n" + "\n".join([f"• {e}" for e in push_errors[:5]])

    sender.reply(report)

    admin_list = sg.bucketGet('G_SXZB', 'push_admins') or ''
    if admin_list:
        admins = [a.strip() for a in admin_list.split(',') if a.strip()]
        try:
            sg.notifyMasters(report, admins)
        except:
            pass

def clean_old_push_records():
    """清理旧的推送记录（保留今天的）"""
    today = datetime.now().strftime('%Y-%m-%d')
    all_keys = sg.bucketAllKeys(bucket='G_sxzb_pushed') or []
    for key in all_keys:
        if today not in key:
            sg.bucketDel(bucket='G_sxzb_pushed', key=key)

def get_subscribers():
    """获取所有订阅用户（所有已授权用户默认订阅）"""
    authorized_users = get_all_authorized_users()
    subscribers = []
    for user_id in authorized_users:
        subscribe_status = sg.bucketGet('G_sxzb_subscribe', user_id) or 'on'
        if subscribe_status == 'on':
            subscribers.append(user_id)
    return subscribers


try:
    usermessage = sender.getMessage()
except AttributeError:
    usermessage = ""

if re.search(r'森选直播登录', usermessage):
    bindaccount()
elif re.search(r'森选直播管理', usermessage):
    sz_manage()
elif re.search(r'森选直播查询', usermessage):
    query_account_status()
elif re.search(r'森选直播教程', usermessage):
    show_tutorial()
elif re.search(r'森选直播授权$', usermessage) and sender.isAdmin():
    admin_authorize_account()
elif re.search(r'森选直播清理', usermessage) and sender.isAdmin():
    sz_clean_accounts()
elif re.search(r'森选订阅', usermessage):
    sz_subscribe()
elif re.search(r'森选推送', usermessage):
    sz_push()
else:
    sender.setContinue()
