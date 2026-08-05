# [title: 【插件】-森选质享]
# [name: chaJianSenXuanZhiXiang]
# [language: python]
# [class: 任务]
# [author: huawei]
# [version: v1.7.1]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(森选|sz)(登录|登陆|查询|管理|教程|清理|上传|一键运行)$]
# [cron: 15 22 * * *]
# [icon: https://api.iconify.design/lucide:apple.svg]
# [description: vx小程序【银辉助手】插件自带任务；指令：；森选登录：绑定账号(支持批量,每行备注#token)；森选上传：批量同步到青龙(管理员)；森选清理：清理过期账号(管理员)；森选教程：使用指南]
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
    'G_szyx_config_ql_config': form.string().title('青龙容器').default('').description('用丨分割三个参数'),
    'G_szyx_config_ql_envname': form.string().title('青龙变量名').default('G_SZYX').description('提交到青龙的变量名'),
})
_CONFIG_FIELD_MAP = {
    ('G_szyx_config', 'ql_config'): 'G_szyx_config_ql_config',
    ('G_szyx_config', 'ql_envname'): 'G_szyx_config_ql_envname',
}

from datetime import datetime
import requests
import os
import json
import re
import time
import hashlib
from typing import List, Dict, Any, Optional

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()


class SenxuanClient:
    """森选质享客户端"""

    def __init__(self, token_with_remark):
        if "#" in token_with_remark:
            self.remark, self.raw_token = token_with_remark.split("#", 1)
            self.remark = self.remark.strip()
            self.raw_token = self.raw_token.strip()
        else:
            self.raw_token = token_with_remark.strip()
            self.remark = "默认账号"

        if self.raw_token.lower().startswith("bearer "):
            self.token = self.raw_token  # 保留原有格式
        else:
            self.token = f"Bearer {self.raw_token}"  # 添加Bearer前缀

        self.base_url = "https://yb.yuanhukj.com/api/mobile"
        self.session = requests.Session()

        self.headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "content-type": "application/x-www-form-urlencoded",
            "Connection": "keep-alive",
            "Referer": "https://servicewechat.com/wx243e6a357085251f/4/page-frame.html",
            "authorization": self.token,
            "app-sign": "wx243e6a357085251f",
            "Host": "yb.yuanhukj.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf2541411) XWEB/16965",
            "xweb_xhr": "1",
        }
        self.session.headers.update(self.headers)

    def get_user_info(self):
        """获取用户信息"""
        try:
            url = f"{self.base_url}/account/user/overview?source_type=2314&source_from=2321&source_lang=zh_CN&currency_id=86&site_id="
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data.get("code") == 0 and data.get("data"):
                return data.get("data")
        except Exception as e:
            print(f"获取用户信息失败: {e}")
        return None

    def get_user_info_new(self):
        """获取用户详细信息"""
        url = f"{self.base_url}/account/user/overview_my"
        params = {
            "source_type": 2314,
            "source_from": 2321,
            "source_lang": "zh_CN",
            "currency_id": 86,
            "site_id": "",
            "isOrder": 1,
        }
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data.get("code") == 0 and data.get("data"):
                user_data = data.get("data")
                return user_data
            return None
        except Exception as e:
            return None

    def get_video_detail(self, vid: int) -> Optional[Dict[str, Any]]:
        """获取单个视频详情"""
        url = f"{self.base_url}/video/getOneVideo?source_type=2314&source_from=2321&source_lang=zh_CN&currency_id=86&site_id=&vid={vid}"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data.get("code") == 0 and data.get("data"):
                return data.get("data")
            return None
        except Exception as e:
            return None

    def add_user_view_num(self, vid: int) -> Dict[str, Any]:
        """记录用户观看视频"""
        url = f"{self.base_url}/video/addUserViewNum?source_type=2314&source_from=2321&source_lang=zh_CN&currency_id=86&site_id=&vid={vid}&playMode=0"
        body = {"baseVersion": "3.12.1", "playMode": 0}
        try:
            print(f"  正在记录观看，视频ID: {vid}")
            headers = {"Content-Type": "application/json"}
            response = self.session.post(url, json=body, headers=headers, timeout=10)
            response.raise_for_status()
            result = response.json()
            print(f"  记录观看结果: {result.get('msg')}")
            return result
        except Exception as e:
            print(f"  记录观看请求异常: {e}")
            return {"status": 500, "msg": str(e)}

    def video_job(self, vid: int, wait_time: int) -> Dict[str, Any]:
        """提交视频观看完成"""
        url = f"{self.base_url}/video/addVideoJob"

        start_time = int(time.time() * 1000)
        end_time = start_time + (wait_time * 1000) + 1000

        body = {
            "source_type": 2314,
            "source_from": 2321,
            "source_lang": "zh_CN",
            "currency_id": "86",
            "site_id": "",
            "vid": vid,
            "startTime": start_time,
            "endTime": end_time,
            "baseVersion": "3.12.1",
            "playMode": 0,
        }

        try:
            print(f"  开始播放 {wait_time}秒...")
            for i in range(wait_time, 0, -10):
                print(f"  剩余 {i} 秒...")
                time.sleep(min(10, i))
            print(f"  播放完成，提交中...")

            headers = {"Content-Type": "application/json"}
            response = self.session.post(url, json=body, headers=headers, timeout=10)
            response.raise_for_status()
            result = response.json()
            print(f"  提交结果: {result.get('msg')}")
            return result
        except Exception as e:
            print(f"  提交观看失败: {e}")
            return {"status": 500, "msg": str(e)}

    def add_video_job(self, vid: int, wait_time: int) -> Dict[str, Any]:
        """提交视频任务完成（同video_job）"""
        return self.video_job(vid, wait_time)

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
        """获取所有视频ID"""
        try:
            print("正在请求视频列表...")
            url = f"{self.base_url}/video/list?source_type=2314&source_from=2321&source_lang=zh_CN&currency_id=86&site_id=&page=1&limit=10&status=1&source=0&isXn=1"

            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("code") == 0 and data.get("data"):
                items = data.get("data", {}).get("items", [])
                if isinstance(items, list) and len(items) > 0:
                    video_ids = [video.get("id") for video in items if video.get("id")]
                    print(f"成功获取 {len(video_ids)} 个视频")
                    return video_ids

            print(f"获取视频列表失败: {data.get('msg')}")
            return []

        except Exception as e:
            print(f"请求视频列表异常: {e}")
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
            "playMode": 0,
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
        """提现 - 新接口（使用手机端请求头）"""
        url = f"{self.base_url}/pay/pay-payment-channel/addUserWithdraw"

        params = {
            "source_type": 2314,
            "source_from": 2321,
            "source_lang": "zh_CN",
            "currency_id": 86,
            "site_id": "",
        }

        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "app-sign": "wx4dff990a8fa3a1e7",
            "authorization": self.token,
            "charset": "utf-8",
            "referer": "https://servicewechat.com/wx4dff990a8fa3a1e7/3/page-frame.html",
            "user-agent": "Mozilla/5.0 (Linux; Android 14; Redmi K20 Pro Build/UKQ1.240624.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.180 Mobile Safari/537.36 XWEB/1380283 MMWEBSDK/20250904 MMWEBID/8960 MicroMessenger/8.0.65.2960(0x28004137) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android",
            "accept-encoding": "gzip, deflate, br",
        }

        try:
            print("正在提交提现申请...")
            response = self.session.post(url, data=params, headers=headers, timeout=10)
            response.raise_for_status()

            result = response.json()
            if result.get("code") == 0:
                data = result.get("data", {})
                process_result = data.get("processResult")
                if process_result == "success":
                    print(f"✅ 提现成功")
                    return {"success": True, "msg": "提现成功", "data": data}
                else:
                    reason = data.get("reason", "未知原因")
                    print(f"❌ 提现失败: {reason}")
                    return {"success": False, "msg": f"提现失败: {reason}"}
            else:
                msg = result.get("msg", "未知错误")
                print(f"❌ 提现失败: {msg}")
                return {"success": False, "msg": msg}
        except Exception as e:
            print(f"❌ 提现请求异常: {e}")
            return {"success": False, "msg": str(e)}

    def get_consume_record(self, page: int = 1, rows: int = 20) -> Dict[str, Any]:
        """获取奖励记录（新接口 - /api/mobile/pay/index/consumeRecord）"""
        try:
            url = f"{self.base_url}/pay/index/consumeRecord"
            params = {
                "source_type": 2314,
                "source_from": 2321,
                "source_lang": "zh_CN",
                "currency_id": 86,
                "site_id": "",
                "change_type": 0,
                "page": page,
                "rows": rows,
            }

            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("code") == 0 and data.get("data"):
                consume_data = data.get("data", {})
                items = consume_data.get("items", [])
                income = consume_data.get("income", 0)

                return {
                    "success": True,
                    "records": items,
                    "count": len(items),
                    "income": income,
                    "total": consume_data.get("total", 0),
                }
        except Exception as e:
            print(f"获取奖励记录失败: {e}")

        return {"success": False, "msg": "获取奖励记录失败"}

    def get_commission_info(self):
        """获取佣金信息"""
        try:
            url = f"{self.base_url}/account/commission?page=1&limit=5"
            response = self.session.get(url, timeout=10)
            if response.status_code == 404:
                return {"success": False, "msg": "佣金接口不可用"}
            response.raise_for_status()
            data = response.json()

            if data.get("code") == 0 and data.get("data"):
                commission_data = data.get("data", {})
                commission_list = commission_data.get(
                    "records", []
                ) or commission_data.get("list", [])
                return {
                    "success": True,
                    "records": commission_list,
                    "count": len(commission_list),
                }
        except Exception as e:
            print(f"获取佣金信息失败: {e}")

        return {"success": False, "msg": "获取佣金信息失败"}

    def run_daily_task(self) -> Dict[str, Any]:
        """运行每日任务"""
        results = {
            "video_count": 0,
            "success_videos": 0,
            "answer_videos": 0,
            "withdraw": None,
            "balance": 0,
            "commission": None,
        }

        try:
            user_info = self.get_user_info_new()
            if user_info:
                results["balance"] = float(
                    user_info.get("user_money", 0) or user_info.get("now_money", 0)
                )
                results["video_count"] = user_info.get("video_answer_not", 0)
                print(
                    f"账户余额: ¥{results['balance']}, 还需答题: {results['video_count']}个\n"
                )

            video_ids = self.get_video_ids()

            if not video_ids:
                print("没有获取到视频")
            else:
                print(f"\n获取到 {len(video_ids)} 个视频，开始处理...\n")

                for idx, vid in enumerate(video_ids, 1):
                    print(f"[{idx}/{len(video_ids)}] 处理视频 {vid}")

                    video_detail = self.get_video_detail(vid)
                    wait_time = 10  # 默认等待时间
                    reward_amount = 0  # 奖励金额

                    if video_detail:
                        wait_time = int(video_detail.get("wait_time", 10))
                        float(video_detail.get("je", 0))
                        print(f"视频等待时间: {wait_time}秒")

                    view_result = self.add_user_view_num(vid)
                    if view_result.get("status") == 500:
                        print(f"[x] 记录观看失败\n")
                        continue

                    job_result = self.add_video_job(vid, wait_time)
                    if job_result.get("code") == 0:
                        results["success_videos"] += 1
                        print(f"[✓] 任务完成")
                    else:
                        print(f"[x] 任务提交失败\n")
                        continue

                    reward_result = self.reward_user_small_change()
                    if reward_result.get("code") == 0:
                        results["answer_videos"] += 1
                        print(f"[✓] 奖励获取成功")
                    else:
                        print(f"[i] 本视频无奖励或不需要答题")

                    print()
                    time.sleep(1)


            commission_info = self.get_commission_info()
            if commission_info.get("success"):
                results["commission"] = commission_info

            user_info = self.get_user_info_new()
            if user_info:
                results["balance"] = float(
                    user_info.get("user_money", 0) or user_info.get("now_money", 0)
                )

        except Exception as e:
            print(f"运行任务出错: {e}")
            import traceback

            traceback.print_exc()

        return results

    def get_withdraw_records(self):
        """获取提现记录"""
        try:
            print("正在获取提现记录...")
            url = f"{self.base_url}/account/withdraw/records?page=1&limit=15"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("code") == 0 and data.get("data"):
                withdraw_data = data.get("data", {})
                withdraw_list = withdraw_data.get("records", []) or withdraw_data.get(
                    "list", []
                )
                return {
                    "success": True,
                    "records": withdraw_list,
                    "count": len(withdraw_list),
                }
        except Exception as e:
            print(f"获取提现记录失败: {e}")

        return {"success": False, "msg": "获取提现记录失败"}


def get_config():
    """获取插件配置"""
    try:
        price_str = sg.bucketGet(bucket="G_szyx_config", key="price") or "0.88"
        price = float(price_str) if price_str.replace(".", "", 1).isdigit() else 0.88
        zsm = sg.bucketGet(bucket="G_szyx_config", key="zsm") or ""
        points_per_month_str = (
            sg.bucketGet(bucket="G_szyx_config", key="points_per_month")
            or "100"
        )
        points_per_month = (
            int(points_per_month_str) if points_per_month_str.isdigit() else 100
        )
        ql_config = sg.bucketGet(bucket="G_szyx_config", key="ql_config") or ""
        ql_envname = (
            sg.bucketGet(bucket="G_szyx_config", key="ql_envname") or "S_SZYX"
        )
        return {
            "price": price,
            "zsm": zsm,
            "points_per_month": points_per_month,
            "ql_config": ql_config,
            "ql_envname": ql_envname,
        }
    except Exception as e:
        sender.reply(f"❌ 配置获取失败: {str(e)}")
        return {
            "price": 0.88,
            "zsm": "",
            "points_per_month": 100,
            "ql_config": "",
            "ql_envname": "S_SZYX",
        }


def get_ql_token(url: str, cid: str, sec: str) -> str:
    """获取青龙Token"""
    try:
        resp = requests.get(
            f"{url}/open/auth/token",
            params={"client_id": cid, "client_secret": sec},
            timeout=10,
        )
        data = resp.json()
        if data.get("code") == 200:
            return data["data"]["token"]
    except:
        pass
    return ""


def push_to_ql(account_id: str, expire: str, ql_config: str, envname: str) -> bool:
    """推送单个账号到青龙"""
    try:
        parts = ql_config.split("丨")
        if len(parts) != 3:
            return False
        url, cid, sec = parts[0].strip(), parts[1].strip(), parts[2].strip()
    except:
        return False
    token = get_ql_token(url, cid, sec)
    if not token:
        return False
    token_with_remark = sg.bucketGet("G_szyx_token", account_id)
    if not token_with_remark:
        return False
    if "#" in token_with_remark:
        remark, raw_token = token_with_remark.split("#", 1)
        remark, raw_token = remark.strip(), raw_token.strip()
    else:
        raw_token, remark = token_with_remark.strip(), "默认账号"
    value = f"{remark}#{raw_token}"
    remarks = f"森选:{remark}|账号:{account_id}|到期:{expire}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    try:
        resp = requests.get(
            f"{url}/open/envs",
            headers=headers,
            params={"searchValue": envname},
            timeout=10,
        )
        envs = resp.json().get("data", [])
        existing = next(
            (
                e
                for e in envs
                if e.get("name") == envname and account_id in e.get("remarks", "")
            ),
            None,
        )
        if existing:
            env_id = existing.get("_id") or existing.get("id")
            requests.put(
                f"{url}/open/envs",
                headers=headers,
                json={
                    "id": env_id,
                    "name": envname,
                    "value": value,
                    "remarks": remarks,
                },
                timeout=10,
            )
        else:
            requests.post(
                f"{url}/open/envs",
                headers=headers,
                json=[{"name": envname, "value": value, "remarks": remarks}],
                timeout=10,
            )
        return True
    except:
        return False


def delete_from_ql(account_id: str, ql_config: str, envname: str) -> bool:
    """从青龙删除账号"""
    try:
        parts = ql_config.split("丨")
        if len(parts) != 3:
            return False
        url, cid, sec = parts[0].strip(), parts[1].strip(), parts[2].strip()
    except:
        return False
    token = get_ql_token(url, cid, sec)
    if not token:
        return False
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    try:
        resp = requests.get(
            f"{url}/open/envs",
            headers=headers,
            params={"searchValue": envname},
            timeout=10,
        )
        envs = resp.json().get("data", [])
        existing = next(
            (
                e
                for e in envs
                if e.get("name") == envname and account_id in e.get("remarks", "")
            ),
            None,
        )
        if existing:
            env_id = existing.get("_id") or existing.get("id")
            requests.delete(
                f"{url}/open/envs", headers=headers, json=[env_id], timeout=10
            )
        return True
    except:
        return False


def get_user_accounts(user_id=None):
    """获取用户账号列表"""
    if user_id is None:
        user_id = userid

    uservalue = sg.bucketGet("G_szyx_user", user_id) or "[]"
    user_accounts = []

    if uservalue:
        try:
            accounts_list = json.loads(uservalue)
            if isinstance(accounts_list, list):
                user_accounts = accounts_list
            else:
                user_accounts = [str(accounts_list)]
        except json.JSONDecodeError:
            user_accounts = []

    return [str(acc) for acc in user_accounts]


def get_user_points(user_id=None):
    return 0


def set_user_points(user_id, points):
    """设置用户积分 - 适配呆呆积分数据结构"""
    sg.bucketSet("dd_sign_coin", user_id, str(points["dd_sign_coin"]))
    sg.bucketSet("dd_sign_points", user_id, str(points["dd_sign_points"]))

    sign_key = f"sign_{user_id}"
    sg.bucketSet("dd_sign_coin", sign_key, str(points["dd_sign_coin"]))
    return True


def verify_commission_api_rs256(token: str) -> Dict[str, Any]:
    """验证RS256 Token（新小程序）"""
    try:
        import base64

        parts = token.split(".")
        if len(parts) != 3:
            return {"success": False, "msg": "Token格式错误"}

        payload = parts[1]
        padding = 4 - len(payload) % 4
        if padding != 4:
            payload += "=" * padding

        decoded = base64.urlsafe_b64decode(payload)
        data = json.loads(decoded)

        exp = data.get("exp")
        if exp:
            from datetime import datetime

            exp_time = datetime.fromtimestamp(exp)
            if datetime.now() > exp_time:
                return {"success": False, "msg": "Token已过期"}

        user_id = data.get("id") or data.get("user_id")

        return {"success": True, "user_id": user_id, "data": data}
    except Exception as e:
        return {"success": False, "msg": str(e)}


def verify_commission_api(token: str) -> Dict[str, Any]:
    """使用佣金接口验证token有效性"""
    rs256_result = verify_commission_api_rs256(token)
    if rs256_result["success"]:
        return rs256_result

    try:
        url = "https://yb.yuanhukj.com/api/mobile/account/commission?page=1&limit=5"
        headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "content-type": "application/json",
            "Connection": "keep-alive",
            "Referer": "https://servicewechat.com/wx243e6a357085251f/4/page-frame.html",
            "authorization": token,
            "app-sign": "wx243e6a357085251f",
            "Host": "yb.yuanhukj.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf2541411) XWEB/16965",
            "Cb-lang": "zh-CN",
            "xweb_xhr": "1",
            "Accept": "*/*",
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()

        if data.get("code") == 0 and data.get("data"):
            user_id = None
            commission_data = data.get("data", {})
            user_transactions = commission_data.get(
                "records", []
            ) or commission_data.get("list", [])
            if user_transactions and len(user_transactions) > 0:
                user_id = user_transactions[0].get("uid") or user_transactions[0].get(
                    "user_id"
                )

            return {"success": True, "user_id": user_id, "data": data}
        else:
            return {"success": False, "msg": data.get("msg", "未知错误"), "data": data}
    except Exception as e:
        return {"success": False, "msg": str(e), "error": e}


def validate_token(token_with_remark):
    """验证Token有效性并返回账号信息"""
    try:
        if "#" in token_with_remark:
            remark, raw_token = token_with_remark.split("#", 1)
            remark = remark.strip()
            token = raw_token.strip()
        else:
            token = token_with_remark.strip()
            remark = "默认账号"

        if len(token) < 10:  # 合理的最小长度
            return False, {"error": "Token格式错误，长度不足"}

        if token.lower().startswith("bearer "):
            full_token = token
        else:
            full_token = f"Bearer {token}"

        commission_result = verify_commission_api(full_token)
        if commission_result["success"]:
            account_id = commission_result.get("user_id")
            if account_id:
                return True, {"account_id": str(account_id), "nickname": remark}
            timestamp = int(time.time() * 1000)
            account_id = f"szyx_{hashlib.md5(str(timestamp).encode()).hexdigest()[:10]}"
            return True, {"account_id": str(account_id), "nickname": remark}

        return False, {
            "error": f"佣金API验证失败: {commission_result.get('msg', '未知错误')}"
        }

    except Exception as e:
        return False, {"error": f"验证失败: {str(e)}"}


def bindaccount():
    """森选登录绑定(支持单个或批量)"""
    sender.reply(
        "=====森选登录=====\n单个：粘贴Token\n批量：换行分割，每行 备注#token\n\n💡 回复q退出"
    )

    ck_input = sender.input(300000, 1, False).strip()
    if ck_input.lower() == "q":
        return

    lines = [l.strip() for l in ck_input.split("\n") if l.strip()]

    if len(lines) > 1:
        sender.reply(f"🔄 检测到 {len(lines)} 条数据，开始批量验证...")
        success_cnt, fail_cnt = 0, 0
        accounts = get_user_accounts()

        for i, line in enumerate(lines, 1):
            if "#" in line:
                remark, token = line.split("#", 1)
                remark, token = remark.strip(), token.strip()
            else:
                token, remark = line.strip(), f"账号{i}"

            if token.lower().startswith("bearer "):
                token = token[7:].strip()
            token = token.strip("\"'").strip()

            if len(token) < 20:
                fail_cnt += 1
                continue

            is_valid, result = validate_token(f"{remark}#{token}")
            if not is_valid:
                fail_cnt += 1
                continue

            account_id = result.get("account_id", f"szyx_{i}")
            sg.bucketSet("G_szyx_token", str(account_id), f"{remark}#{token}")
            if account_id not in accounts:
                accounts.append(account_id)
            success_cnt += 1

        sg.bucketSet("G_szyx_user", userid, json.dumps(accounts))
        sender.reply(
            f"✅ 批量绑定完成\n成功: {success_cnt}个\n失败: {fail_cnt}个\n\n下一步: 发『森选管理』授权\n⚠️ 每天请用手机端手动提现，电脑端无法到账"
        )
        return

    access_token = ck_input.strip()
    if access_token.lower().startswith("bearer "):
        access_token = access_token[7:].strip()
    access_token = access_token.strip("\"'").strip()

    if len(access_token) < 20:
        sender.reply("❌ Token过短")
        return

    is_valid, result = validate_token(f"验证中#{access_token}")
    if not is_valid:
        sender.reply(f"❌ Token验证失败: {result.get('error', '无效Token')}")
        return

    sender.reply("✅ Token有效\n请输入备注(如：张三)\n回复q取消")
    remark_input = sender.input(120000, 1, False).strip()
    if not remark_input or remark_input.lower() == "q":
        sender.reply("❌ 已取消")
        return

    remark = remark_input.strip()
    account_id = result.get("account_id", "unknown")
    sg.bucketSet("G_szyx_token", str(account_id), f"{remark}#{access_token}")
    accounts = get_user_accounts()
    if account_id not in accounts:
        accounts.append(account_id)
    sg.bucketSet("G_szyx_user", userid, json.dumps(accounts))

    sender.reply(
        f"✅ 绑定成功\n备注: {remark}\nID: {account_id}\n下一步: 发『森选管理』授权\n⚠️ 每天请用手机端手动提现，电脑端无法到账"
    )


def authorize_account(account_id):
    return True


def wechat_payment_flow(account_id, months, amount, config, nickname):
    return True


def point_payment_flow(account_id, months, required_points):
    return True


def parse_payment_result(raw_data):
    return True


def complete_authorization(account_id, months, display_name):
    return True


def delete_account(account_id):
    """删除账号"""
    accounts = get_user_accounts()

    sender.reply(f"""
=====删除账号确认=====
确认删除账号 {account_id} 吗？
请回复 [Y] 确认
回复 [N] 取消
==================""")
    user_confirm = sender.input(120000, 1, False).strip().lower()

    if user_confirm != "y":
        sender.reply("✅ 已取消删除操作")
        return

    try:
        sg.bucketDel(bucket="G_szyx_token", key=account_id)
        True

        if account_id in accounts:
            accounts.remove(account_id)
            if accounts:
                sg.bucketSet(
                    bucket="G_szyx_user", key=userid, value=json.dumps(accounts)
                )
            else:
                sg.bucketDel(bucket="G_szyx_user", key=userid)

        sender.reply("✅ 账号删除成功")

    except Exception as e:
        sender.reply(f"❌ 删除失败: {str(e)}")


def batch_delete_accounts(accounts):
    """批量删除账号"""
    if not accounts:
        sender.reply("❌ 没有账号可删除")
        return

    account_list = []
    for i, acc_id in enumerate(accounts, 1):
        token_data = sg.bucketGet("G_szyx_token", acc_id) or ""
        remark = token_data.split("#")[0].strip() if "#" in token_data else "默认账号"
        account_list.append(f"[{i}] {remark}")

    list_str = "\n".join(account_list)
    sender.reply(
        f"=====批量删除=====\n{list_str}\n\n输入要删除的序号(多个用逗号分隔)\n如: 1,2,3 或 全部\n💡 回复q退出"
    )

    choice = sender.input(60000, 1, False).strip()
    if not choice or choice.lower() == "q":
        sender.reply("✅ 已取消")
        return

    to_delete = []
    if choice == "全部":
        to_delete = accounts[:]
    else:
        try:
            indices = [
                int(x.strip()) - 1 for x in choice.split(",") if x.strip().isdigit()
            ]
            to_delete = [accounts[i] for i in indices if 0 <= i < len(accounts)]
        except:
            sender.reply("❌ 输入格式错误")
            return

    if not to_delete:
        sender.reply("❌ 未选择有效账号")
        return

    sender.reply(f"⚠️ 确认删除 {len(to_delete)} 个账号？\n回复 Y 确认 / N 取消")
    confirm = sender.input(60000, 1, False).strip().lower()
    if confirm != "y":
        sender.reply("✅ 已取消")
        return

    success_cnt, fail_cnt = 0, 0
    remaining = [a for a in accounts if a not in to_delete]

    for acc_id in to_delete:
        try:
            sg.bucketDel("G_szyx_token", acc_id)
            True
            success_cnt += 1
        except:
            fail_cnt += 1

    if remaining:
        sg.bucketSet("G_szyx_user", userid, json.dumps(remaining))
    else:
        sg.bucketDel("G_szyx_user", userid)

    sender.reply(f"✅ 批量删除完成\n成功: {success_cnt}个\n失败: {fail_cnt}个")


def batch_authorize_accounts(unauthorized_accounts):
    return True


def batch_wechat_payment(accounts, months, amount, config):
    return True


def batch_point_payment(accounts, months, required_points):
    return True


def run_single_account_task(account_id):
    """运行单个账号的任务"""
    token_with_remark = sg.bucketGet("G_szyx_token", account_id)
    if not token_with_remark:
        sender.reply("❌ 账号Token缺失，无法运行任务")
        return

    if "#" in token_with_remark:
        remark, token = token_with_remark.split("#", 1)
        remark = remark.strip()
    else:
        token_with_remark.strip()
        remark = "默认账号"

    display_name = remark

    sender.reply(f"⏳ 任务执行中\n账号: {display_name}")

    try:
        client = SenxuanClient(token_with_remark)
        result = client.run_daily_task()

        success_videos = result.get("success_videos", 0)
        result.get("video_count", 0)

        user_info = client.get_user_info_new()
        balance = "未知"
        if user_info:
            balance_value = float(user_info.get("user_money", 0))
            balance = f"¥{balance_value:.2f}"

        result_msg = f"森选任务结果\n账号: {display_name}\n视频: {success_videos}个\n余额: {balance}"

        sender.reply(result_msg)

    except Exception as e:
        err_msg = str(e)
        if len(err_msg) > 100:
            err_msg = err_msg[:97] + "..."
        sender.reply(f"❌ 任务运行失败: {err_msg}")


def sz_manage():
    """账号管理"""
    accounts = get_user_accounts()

    if not accounts:
        sender.reply("❌ 您尚未绑定任何账号，请先绑定")
        return

    authorized_count = 0
    unauthorized_accounts = []
    for account_id in accounts:
        auth_data = '2099-12-31'
        if auth_data:
            authorized_count += 1
        else:
            unauthorized_accounts.append(account_id)

    account_list = []
    for i, account_id in enumerate(accounts, 1):
        token_with_remark = sg.bucketGet("G_szyx_token", account_id) or ""
        if "#" in token_with_remark:
            remark, token = token_with_remark.split("#", 1)
            remark = remark.strip()
        else:
            token = token_with_remark
            remark = "默认账号"

        auth_data = '2099-12-31'
        status = "✅" if auth_data else "❌"
        status_text = "已授权" if auth_data else "未授权"

        account_list.append(f"[{i}] {remark} {status}{status_text}")

    if accounts:
        account_list.append("\n[0] 所有账号授权（支付）")
        account_list.append("[8888] 批量删除账号")
    if unauthorized_accounts:
        account_list.append("[9999] 没有授权的账号授权（合并支付）")

    account_list_str = "\n".join(account_list)

    user_points = get_user_points()

    sender.reply(f"""
=====森选质享账号管理=====
🔢 绑定账号: {len(accounts)}个
✅ 已授权: {authorized_count}个
❌ 未授权: {len(accounts) - authorized_count}个
📊 当前积分: {user_points["total"]}
-------------------------
{account_list_str}
------------------
回复序号选择操作（q退出）
===================""")

    choice = sender.input(60000, 1, False)
    if choice.lower() == "q":
        sender.reply("已退出管理")
        return

    if choice == "0":
        sender.reply("您选择了所有账号授权")
        for account_id in accounts:
            authorize_account(account_id)
        return
    elif choice == "8888":
        batch_delete_accounts(accounts)
        return
    elif choice == "9999":
        sender.reply("您选择了没有授权的账号授权（合并支付）")
        batch_authorize_accounts(unauthorized_accounts)
        return
    elif not choice.isdigit():
        sender.reply("❌ 输入无效")
        return

    selected_idx = int(choice) - 1
    if selected_idx < 0 or selected_idx >= len(accounts):
        sender.reply("❌ 序号无效")
        return

    selected_account = accounts[selected_idx]

    token_with_remark = sg.bucketGet("G_szyx_token", selected_account) or ""
    if "#" in token_with_remark:
        remark, token = token_with_remark.split("#", 1)
        remark = remark.strip()
    else:
        remark = "默认账号"

    sender.reply(
        f"你选择了账号: {remark}\n[1] 授权账号\n[2] 任务运行\n[3] 更新账号\n[4] 删除账号"
    )
    op = sender.input(60000, 1, False)

    if op == "1":
        authorize_account(selected_account)
    elif op == "2":
        run_single_account_task(selected_account)
    elif op == "3":
        update_account_token(selected_account, remark)
    elif op == "4":
        delete_account(selected_account)


def update_account_token(account_id, old_remark):
    """更新账号的token"""
    sender.reply(f"请输入新的token (格式：备注#token 或直接输入token):")
    new_token_input = sender.input(120000, 1, False)

    if not new_token_input or new_token_input.lower() == "q":
        sender.reply("❌ 已取消更新")
        return

    if "#" in new_token_input:
        remark, access_token = new_token_input.split("#", 1)
        remark = remark.strip()
    else:
        access_token = new_token_input.strip()
        remark = old_remark

    token_with_remark = f"{remark}#{access_token}"

    is_valid, result = validate_token(token_with_remark)

    if is_valid:
        sg.bucketSet(
            bucket="G_szyx_token", key=account_id, value=token_with_remark
        )
        sender.reply(f"✅ Token更新成功！账号备注: {remark}")

        if isinstance(result, dict) and result.get("nickname"):
            sender.reply(f"✅ 验证成功: {result.get('nickname', '未知用户')}")
    else:
        sender.reply(f"❌ Token验证失败: {result}\n请重新获取有效的Token")


def sz_auto_run():
    """一键运行所有已授权账号任务"""
    authorized_accounts = []
    all_accounts = []  # 所有账号，包括已过期的
    auth_keys = [] or []

    expired_accounts = []
    expiring_soon_accounts = []  # 即将过期的账号（3天内）

    today = datetime.now().date()
    for account_id in auth_keys:
        auth_data_str = '2099-12-31'
        if not auth_data_str:
            continue

        all_accounts.append(account_id)
        try:
            auth_data = json.loads(auth_data_str)
            expire_date = auth_data.get("expire_time")

            if expire_date:
                try:
                    expire_date_obj = datetime.strptime(expire_date, "%Y-%m-%d").date()
                    days_diff = (expire_date_obj - today).days

                    if days_diff < 0:  # 已过期
                        expired_accounts.append(
                            {
                                "account_id": account_id,
                                "auth_data": auth_data,
                                "days_expired": abs(days_diff),
                            }
                        )
                    elif days_diff <= 3:  # 3天内即将过期
                        expiring_soon_accounts.append(
                            {
                                "account_id": account_id,
                                "auth_data": auth_data,
                                "days_remaining": days_diff,
                            }
                        )
                        authorized_accounts.append(account_id)  # 仍然可以运行任务
                    else:
                        authorized_accounts.append(account_id)
                except:
                    pass  # 忽略无效日期格式的账号
        except:
            pass  # 忽略格式错误的授权信息

    if not authorized_accounts and not expired_accounts:
        sender.reply("❌ 没有已授权的账号")
        return

    is_simple_mode = True

    run_results = []
    skip_results = []  # 用于记录跳过的账号
    failed_accounts = []  # 用于记录失败的账号
    success_accounts = []  # 用于记录成功的账号
    ck_invalid_accounts = []  # 用于记录CK失效的账号
    total_success_videos = 0

    if authorized_accounts:
        sender.reply(f"⛳ 开始处理 {len(authorized_accounts)} 个授权账号，请稍候...")

        for account_id in authorized_accounts:
            token_with_remark = sg.bucketGet("G_szyx_token", account_id)
            if not token_with_remark:
                skip_results.append(account_id)
                continue

            if "#" in token_with_remark:
                remark, raw_token = token_with_remark.split("#", 1)
                remark = remark.strip()
            else:
                token_with_remark.strip()
                remark = "默认账号"

            display_name = remark

            try:
                client = SenxuanClient(token_with_remark)
                result = client.run_daily_task()

                success_videos = result.get("success_videos", 0)
                result.get("answer_videos", 0)
                total_success_videos += success_videos

                user_info = client.get_user_info_new()
                balance = "未知"
                if user_info:
                    balance_value = float(user_info.get("user_money", 0))
                    balance = f"¥{balance_value:.2f}"

                videos_msg = f"✅{success_videos}个视频"
                balance_msg = f" | 余额{balance}"

                success_accounts.append(display_name)

                if not is_simple_mode:
                    run_results.append(
                        f"👤 {display_name}:\n   {videos_msg}{balance_msg}"
                    )
            except Exception as e:
                err_msg = str(e)
                if len(err_msg) > 50:
                    err_msg = err_msg[:47] + "..."

                failed_accounts.append(display_name)

                is_ck_invalid = any(
                    keyword in err_msg
                    for keyword in [
                        "token",
                        "authorization",
                        "auth",
                        "invalid",
                        "expired",
                        "unauthorized",
                        "401",
                        "403",
                        "验证",
                        "失效",
                        "过期",
                    ]
                )

                if is_ck_invalid:
                    ck_invalid_accounts.append(display_name)
                    try:
                        auth_data_str = sg.bucketGet(
                            "G_szyx_auth", key=account_id
                        )
                        if auth_data_str:
                            auth_data = json.loads(auth_data_str)
                            user_id = auth_data.get("userid")
                            if user_id:
                                push_msg = f"森选CK失效提醒\n账号: {remark}\n原因: {err_msg}\n请到『森选管理』更新CK"

                                try:
                                    sg.push(
                                        "wx",
                                        "",
                                        user_id,
                                        "森选质享CK失效通知",
                                        push_msg,
                                    )
                                except:
                                    pass
                                try:
                                    sg.push(
                                        "qq",
                                        "",
                                        user_id,
                                        "森选质享CK失效通知",
                                        push_msg,
                                    )
                                except:
                                    pass
                    except Exception as push_err:
                        print(f"发送CK失效通知失败: {push_err}")

                if not is_simple_mode:
                    run_results.append(
                        f"👤 {display_name}:\n   ❌ 运行失败 ({err_msg})"
                    )

        if is_simple_mode:
            result_msg = "森选一键运行汇总"
            result_msg += (
                f"\n成功: {len(success_accounts)} 失败: {len(failed_accounts)}"
            )
            if ck_invalid_accounts:
                result_msg += f"\nCK失效: {len(ck_invalid_accounts)}"
            if skip_results:
                result_msg += f"\n跳过: {len(skip_results)}"
            result_msg += f"\n完成视频: {total_success_videos}"
            if failed_accounts:
                sample = "、".join(failed_accounts[:5])
                suffix = "..." if len(failed_accounts) > 5 else ""
                result_msg += f"\n失败账号: {sample}{suffix}"
        else:
            result_msg = "🚀 森选质享任务运行报告 📊\n====================\n"
            result_msg += "\n".join(run_results)

            summary = f"\n\n🎬 本次完成: {total_success_videos}个视频"

            if skip_results:
                summary += f"\n⚠ 跳过账号: {len(skip_results)}个 (Token缺失)"

            result_msg += summary + "\n==================="

        sender.reply(result_msg)

    if expired_accounts or expiring_soon_accounts:
        time.sleep(1)

        if expired_accounts:
            expired_msg = "⚠️ 以下账号已过期，无法执行任务:\n"
            for acc in expired_accounts:
                account_id = acc["account_id"]
                days_expired = acc["days_expired"]
                auth_data = acc["auth_data"]

                token_with_remark = (
                    sg.bucketGet("G_szyx_token", account_id) or ""
                )
                if "#" in token_with_remark:
                    remark, _ = token_with_remark.split("#", 1)
                    remark = remark.strip()
                else:
                    remark = "默认账号"

                expired_msg += f"👤 {remark}: 已过期{days_expired}天\n"

                try:
                    user_id = auth_data.get("userid")
                    if user_id:
                        push_msg = f"森选账号过期\n账号: {remark}\n已过期: {days_expired}天\n如需续费请检查配置"

                        try:
                            sg.push(
                                "wx", "", user_id, "森选质享账号过期通知", push_msg
                            )
                        except:
                            pass
                        try:
                            sg.push(
                                "qq", "", user_id, "森选质享账号过期通知", push_msg
                            )
                        except:
                            pass
                except Exception as e:
                    print(f"发送过期通知失败: {e}")

            sender.reply(expired_msg)

        if expiring_soon_accounts:
            expiring_msg = "⏰ 以下账号即将过期，请及时续费:\n"
            for acc in expiring_soon_accounts:
                account_id = acc["account_id"]
                days_remaining = acc["days_remaining"]
                auth_data = acc["auth_data"]

                token_with_remark = (
                    sg.bucketGet("G_szyx_token", account_id) or ""
                )
                if "#" in token_with_remark:
                    remark, _ = token_with_remark.split("#", 1)
                    remark = remark.strip()
                else:
                    remark = "默认账号"

                expiring_msg += f"👤 {remark}: 还剩{days_remaining}天过期\n"

                try:
                    user_id = auth_data.get("userid")
                    if user_id:
                        push_msg = f"森选账号即将到期\n账号: {remark}\n剩余: {days_remaining}天\n请及时续费"

                        try:
                            sg.push(
                                "wx", "", user_id, "森选质享账号即将过期", push_msg
                            )
                        except:
                            pass
                        try:
                            sg.push(
                                "qq", "", user_id, "森选质享账号即将过期", push_msg
                            )
                        except:
                            pass
                except Exception as e:
                    print(f"发送即将过期通知失败: {e}")

            sender.reply(expiring_msg)


def admin_authorize_account():
    return True
def query_account_status():
    """查询账号状态"""
    accounts = get_user_accounts()

    if not accounts:
        sender.reply("❌ 您尚未绑定任何账号，请先绑定")
        return

    for idx, account_id in enumerate(accounts, 1):
        token_with_remark = sg.bucketGet("G_szyx_token", account_id)
        if not token_with_remark:
            sender.reply(f"账号 {idx}: ❌ Token缺失")
            continue

        if "#" in token_with_remark:
            remark, token = token_with_remark.split("#", 1)
            remark = remark.strip()
            token = token.strip()
        else:
            token = token_with_remark.strip()
            remark = "默认账号"

        display_name = remark

        result_msg = f"森选查询\n账号: {display_name}\n"

        auth_data = '2099-12-31'
        expire_date = "未知"

        if auth_data:
            try:
                auth_info = json.loads(auth_data)
                expire_date = auth_info.get("expire_time", "未知")
                result_msg += f"授权: 已授权\n到期: {expire_date}\n"

                if expire_date != "未知":
                    try:
                        expire_date_obj = datetime.strptime(
                            expire_date, "%Y-%m-%d"
                        ).date()
                        today = datetime.now().date()
                        days_left = (expire_date_obj - today).days

                        if days_left < 0:
                            result_msg += "提醒: 授权已过期(将清理)\n"
                        elif days_left < 4:
                            result_msg += f"提醒: 即将到期({days_left}天)\n"
                    except:
                        pass
            except:
                result_msg += "授权: 已授权\n到期: 未知\n"
        else:
            result_msg += "授权: 未授权\n"

        try:
            client = SenxuanClient(token_with_remark)

            consume_info = client.get_consume_record(page=1, rows=20)

            if (
                consume_info
                and consume_info.get("success")
                and consume_info.get("records")
            ):
                records = consume_info.get("records") or []

                reward_records = [
                    r for r in records if "提现" not in r.get("record_title", "")
                ]
                withdraw_records = [
                    r for r in records if "提现" in r.get("record_title", "")
                ]
                reward_income = sum(
                    float(r.get("record_money", 0)) for r in reward_records
                )

                result_msg += f"今日奖励: ¥{reward_income:.2f}\n奖励记录: {len(reward_records)}条\n"

                if reward_records:
                    result_msg += "最近奖励:\n"
                    for i, record in enumerate(reward_records[:3]):
                        record_title = record.get("record_title", "未知")
                        record_money = record.get("record_money", 0)
                        record_time = record.get("record_time", "未知")
                        result_msg += f"- ¥{record_money} {record_title} {str(record_time)[:10]}\n"

                if withdraw_records:
                    withdraw_total = sum(
                        float(r.get("record_money", 0)) for r in withdraw_records
                    )
                    result_msg += f"提现: {len(withdraw_records)}笔  合计: ¥{withdraw_total:.2f}\n"
                    for i, record in enumerate(withdraw_records[:3]):
                        record_money = record.get("record_money", 0)
                        record_time = record.get("record_time", "未知")
                        result_msg += f"- ¥{record_money} {str(record_time)[:10]}\n"
                else:
                    result_msg += "提现: 暂无\n"
            else:
                commission_info = client.get_commission_info()
                if (
                    commission_info
                    and commission_info.get("success")
                    and commission_info.get("records")
                ):
                    records = commission_info.get("records") or []

                    withdraw_records = [
                        r for r in records if r.get("type") == "user_tx"
                    ]

                    total_amount = 0
                    for record in withdraw_records:
                        try:
                            amount = float(record.get("number", "0"))
                            total_amount += amount
                        except:
                            pass

                    result_msg += (
                        f"提现: {len(withdraw_records)}笔  合计: ¥{total_amount:.2f}\n"
                    )

                    if withdraw_records:
                        result_msg += "最近提现:\n"

                        for i, record in enumerate(withdraw_records[:5]):
                            amount = record.get("number", "0")
                            add_time = record.get("add_time", "未知")
                            result_msg += f"现金{amount}元-{add_time}\n"
                else:
                    if token:
                        bearer_token = (
                            f"Bearer {token}"
                            if not token.lower().startswith("bearer ")
                            else token
                        )
                        commission_result = verify_commission_api(bearer_token)
                        if commission_result.get("success"):
                            data = commission_result.get("data", {})
                            if data and data.get("list"):
                                records = data["list"]

                                withdraw_records = [
                                    r for r in records if r.get("type") == "user_tx"
                                ]

                                total_amount = 0
                                for record in withdraw_records:
                                    try:
                                        amount = float(record.get("number", "0"))
                                        total_amount += amount
                                    except:
                                        pass

                                result_msg += f"提现: {len(withdraw_records)}笔  合计: ¥{total_amount:.2f}\n"

                                if withdraw_records:
                                    result_msg += "最近提现:\n"

                                    for i, record in enumerate(withdraw_records[:5]):
                                        amount = record.get("number", "0")
                                        add_time = record.get("add_time", "未知")
                                        result_msg += f"现金{amount}元-{add_time}\n"
                        else:
                            result_msg += "状态: CK可能失效(去森选管理更新)\n"

        except Exception as e:
            result_msg += f"❌ 查询失败: {str(e)[:50]}\n"

        sender.reply(result_msg.strip())


def show_tutorial():
    """显示使用教程"""
    tutorial = """森选质享教程
📱 入口: #小程序://银辉云选/mpcwyYtMQegcNjc

🔑 抓包获取Token
域名: yb.yuanhukj.com
字段: authorization (去掉Bearer)
格式: 备注#token

📋 指令说明
森选登录 - 绑定账号
森选管理 - 授权/更新Token
森选查询 - 查积分余额
森选运行 - 执行任务(管理员)
森选青龙 - 导出青龙配置

💡 Token失效→森选管理→更新账号"""
    sender.reply(tutorial)


def sz_export_qinglong():
    """导出已授权账号到青龙格式"""
    accounts = get_user_accounts()
    if not accounts:
        sender.reply("❌ 您尚未绑定任何账号")
        return

    today = datetime.now().date()
    valid_tokens = []
    expired_count = 0
    unauthorized_count = 0

    for account_id in accounts:
        token_with_remark = sg.bucketGet("G_szyx_token", account_id)
        if not token_with_remark:
            continue

        if "#" in token_with_remark:
            remark, token = token_with_remark.split("#", 1)
            remark, token = remark.strip(), token.strip()
        else:
            token, remark = token_with_remark.strip(), "默认账号"

        auth_data_str = '2099-12-31'
        if not auth_data_str:
            unauthorized_count += 1
            continue

        try:
            auth_data = json.loads(auth_data_str)
            expire_date = auth_data.get("expire_time")
            if expire_date:
                expire_date_obj = datetime.strptime(expire_date, "%Y-%m-%d").date()
                if expire_date_obj < today:
                    expired_count += 1
                    continue
        except:
            unauthorized_count += 1
            continue

        valid_tokens.append(f"{remark}#{token}")

    if not valid_tokens:
        msg = "❌ 没有有效的已授权账号可导出"
        if expired_count:
            msg += f"\n⏰ 已过期: {expired_count}个"
        if unauthorized_count:
            msg += f"\n🔒 未授权: {unauthorized_count}个"
        sender.reply(msg)
        return

    env_value = "\n".join(valid_tokens)
    result_msg = f"""森选青龙配置
环境变量名: S_SZYX
格式: 备注#token
有效账号: {len(valid_tokens)}个"""
    if expired_count:
        result_msg += f"\n已过期: {expired_count}个(已跳过)"
    if unauthorized_count:
        result_msg += f"\n未授权: {unauthorized_count}个(已跳过)"
    result_msg += f"\n\n复制以下内容到青龙:\n{env_value}"

    sender.reply(result_msg)


def sz_upload_qinglong():
    """管理员批量上传所有账号到青龙"""
    if not sender.isAdmin():
        sender.reply("❌ 仅管理员可用")
        return
    cfg = get_config()
    if not cfg["ql_config"]:
        sender.reply("❌ 未配置青龙面板\n请在插件参数中配置【青龙容器】")
        return
    parts = cfg["ql_config"].split("丨")
    if len(parts) != 3:
        sender.reply(
            "❌ 青龙配置格式错误\n格式: http://ip:5700丨ClientID丨ClientSecret"
        )
        return
    host, cid, sec = parts[0].strip(), parts[1].strip(), parts[2].strip()
    ql_token = get_ql_token(host, cid, sec)
    if not ql_token:
        sender.reply("❌ 获取青龙Token失败，请检查配置")
        return
    sender.reply("🔄 正在获取青龙变量...")
    headers = {
        "Authorization": f"Bearer {ql_token}",
        "Content-Type": "application/json",
    }
    envname = cfg["ql_envname"]
    try:
        envs_r = requests.get(
            f"{host}/open/envs",
            headers=headers,
            params={"searchValue": envname},
            timeout=10,
        )
        ql_envs = [
            env for env in envs_r.json().get("data", []) if env.get("name") == envname
        ]
    except Exception as e:
        sender.reply(f"❌ 获取变量失败: {e}")
        return
    ql_accounts = {}
    for env in ql_envs:
        remarks = env.get("remarks", "")
        env_id = env.get("_id") or env.get("id")
        if "账号:" in remarks:
            acc_id = remarks.split("账号:")[1].split("|")[0].strip()
            if acc_id and env_id:
                ql_accounts[acc_id] = env_id
    sender.reply(f"📊 青龙变量: {len(ql_envs)}个\n🔍 识别账号: {len(ql_accounts)}个")
    try:
        users = sg.bucketAllKeys(bucket="G_szyx_user") or []
    except:
        users = []
    update_cnt, add_cnt, skip_cnt, fail_cnt = 0, 0, 0, 0
    today = datetime.now().date()
    for uid in users:
        accounts = get_user_accounts(uid)
        for account_id in accounts:
            auth_data_str = '2099-12-31'
            if not auth_data_str:
                skip_cnt += 1
                continue
            try:
                auth_data = json.loads(auth_data_str)
                expire = auth_data.get("expire_time", "")
                if expire and datetime.strptime(expire, "%Y-%m-%d").date() < today:
                    skip_cnt += 1
                    continue
            except:
                skip_cnt += 1
                continue
            token_with_remark = sg.bucketGet("G_szyx_token", account_id)
            if not token_with_remark:
                skip_cnt += 1
                continue
            if "#" in token_with_remark:
                remark, raw_token = token_with_remark.split("#", 1)
                remark, raw_token = remark.strip(), raw_token.strip()
            else:
                raw_token, remark = token_with_remark.strip(), "默认账号"
            value = f"{remark}#{raw_token}"
            remarks = f"森选:{remark}|账号:{account_id}|用户:{uid}|到期:{expire}"
            if account_id in ql_accounts:
                try:
                    r = requests.put(
                        f"{host}/open/envs",
                        headers=headers,
                        json={
                            "id": ql_accounts[account_id],
                            "name": envname,
                            "value": value,
                            "remarks": remarks,
                        },
                        timeout=10,
                    )
                    if r.status_code == 200 and r.json().get("code") == 200:
                        update_cnt += 1
                    else:
                        fail_cnt += 1
                except:
                    fail_cnt += 1
            else:
                try:
                    r = requests.post(
                        f"{host}/open/envs",
                        headers=headers,
                        json=[{"name": envname, "value": value, "remarks": remarks}],
                        timeout=10,
                    )
                    if r.status_code == 200 and r.json().get("code") == 200:
                        add_cnt += 1
                    else:
                        fail_cnt += 1
                except:
                    fail_cnt += 1
    sender.reply(
        f"✅ 同步完成\n📊 青龙原有: {len(ql_envs)}\n🔄 更新: {update_cnt}\n➕ 新增: {add_cnt}\n⏭️ 跳过: {skip_cnt}\n❌ 失败: {fail_cnt}"
    )


def sz_clean_accounts():
    """清理未授权和授权过期的森选账号"""
    if not sender.isAdmin():
        sender.reply("❌ 您没有权限执行此操作")
        return

    users = sg.bucketAllKeys(bucket="G_szyx_user")
    if not users:
        sender.reply("❌ 未找到任何绑定账号")
        return

    sender.reply(f"""
=====开始清理=====
📊 共找到: {len(users)}个用户
清理中请稍候...
==================""")

    cleaned_count = 0
    failed_count = 0
    today = datetime.now().date()

    for user in users:
        try:
            accountlist = sg.bucketGet(bucket="G_szyx_user", key=f"{user}")
            if not accountlist:
                continue

            accounts = json.loads(accountlist)
            if not isinstance(accounts, list):
                accounts = [accounts]

            valid_accounts = []

            for account_id in accounts:
                should_delete = False
                auth_data_str = sg.bucketGet(
                    bucket="G_szyx_auth", key=account_id
                )

                if not auth_data_str:
                    should_delete = True
                else:
                    try:
                        auth_data = json.loads(auth_data_str)
                        expire_date = auth_data.get("expire_time")

                        if expire_date:
                            expire_date_obj = datetime.strptime(
                                expire_date, "%Y-%m-%d"
                            ).date()
                            if expire_date_obj < today:
                                should_delete = True
                    except:
                        should_delete = True

                if should_delete:
                    try:
                        sg.bucketDel(bucket="G_szyx_token", key=account_id)
                        True
                        cleaned_count += 1
                    except:
                        failed_count += 1
                else:
                    valid_accounts.append(account_id)

            if valid_accounts:
                sg.bucketSet(
                    bucket="G_szyx_user", key=user, value=json.dumps(valid_accounts)
                )
            else:
                sg.bucketDel(bucket="G_szyx_user", key=user)

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


try:
    usermessage = sender.getMessage()
except AttributeError:
    usermessage = ""

if re.search(r"(森选|sz)登(录|陆)", usermessage):
    bindaccount()
elif re.search(r"(森选|sz)管理", usermessage):
    sz_manage()
elif re.search(r"(森选|sz)查询", usermessage):
    query_account_status()
elif re.search(r"(森选|sz)一键运行", usermessage) and sender.isAdmin():
    sz_auto_run()
elif re.search(r"(森选|sz)教程", usermessage):
    show_tutorial()
elif re.search(r"(森选|sz)授权$", usermessage) and sender.isAdmin():
    admin_authorize_account()
elif re.search(r"(森选|sz)清理", usermessage) and sender.isAdmin():
    sz_clean_accounts()
elif re.search(r"(森选|sz)上传", usermessage) and sender.isAdmin():
    sz_upload_qinglong()
else:
    sender.setContinue()
