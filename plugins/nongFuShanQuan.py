# [title: 农夫山泉]
# [name: nongFuShanQuan]
# [language: python]
# [class: 任务]
# [author: sky2022]
# [version: v1.4.1]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^农夫(批量|管理|查询|运行|配置|版本|教程)$]
# [icon: https://uapis.cn/static/uploads/9b1643baac_q1mBS7qtm3iX.webp]
# [description: 介绍：农夫山泉插件 插件自带任务!；更新：V7.0适配新版API接口；更新：支持中奖实时通知；更新：支持并发运行任务]
# [depe: ["requests"]]

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
    'dd_nfsqconfig_yxbf': plugin.Form.string().title('运行并发数').default('').description('设置管理员一键运行所有账号同时最多多少账号一起运行,默认1'),
    'dd_nfsqconfig_notify': plugin.Form.string().title('管理员通知').default('').description('设置接受管理员通知的渠道，如 qq,wx,tg 用英文逗号分割,不设置不推送'),
    'dd_nfsqconfig_use_amap': plugin.Form.boolean().title('使用高德地图').default(False).description('开启则使用高德API解析地址(需配置key)，关闭则使用农夫山泉自带接口'),
    'dd_nfsqconfig_amap_key': plugin.Form.string().title('高德地图key').default('').description('申请地址：https://console.amap.com/dev/key/app，选择Web服务'),
    'dd_nfsqconfig_default_address': plugin.Form.string().title('默认地址').default('').description('设置默认运行地址，输入完整地址即可自动解析'),
    'dd_nfsqconfig_follow_lottery': plugin.Form.boolean().title('农夫跟抽').default(False).description('开启后，有人中一等奖时全部账号立即使用该经纬度地址进行抽奖'),
})
_CONFIG_FIELD_MAP = {
    ('dd_nfsqconfig', 'yxbf'): 'dd_nfsqconfig_yxbf',
    ('dd_nfsqconfig', 'notify'): 'dd_nfsqconfig_notify',
    ('dd_nfsqconfig', 'use_amap'): 'dd_nfsqconfig_use_amap',
    ('dd_nfsqconfig', 'amap_key'): 'dd_nfsqconfig_amap_key',
    ('dd_nfsqconfig', 'default_address'): 'dd_nfsqconfig_default_address',
    ('dd_nfsqconfig', 'follow_lottery'): 'dd_nfsqconfig_follow_lottery',
}

import json
import random
import time
import uuid
import hashlib
import urllib.parse
from datetime import datetime
from io import StringIO
import sys
import requests

BASE_URL = "https://sxs-consumer.nfsq.com.cn"
ADDRESS_URL = "https://sxs-consumer.nfsq.com.cn/geement.utils/api/v1/address/conversion/inverse"  # 经纬度逆地理编码
SCENE_LIST = ["SCENE-2510301509021", "SCENE-2510301508361"]
MAX_TOTAL_TRY = 8
DELAY_MIN, DELAY_MAX = 2, 4

def get_config(key, default=''):
    val = '2099-12-31'
    return val if val else default

def get_headers(apitoken, unique_id):
    return {
        "authority": "sxs-consumer.nfsq.com.cn",
        "apitoken": apitoken,
        "content-type": "application/json",
        "unique_identity": unique_id,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781 NetType/WIFI MiniProgramEnv/Windows",
        "xweb_xhr": "1"
    }

def parse_ck(ck):
    if "&" in ck:
        return ck.split('&', 1)
    else:
        return ck, str(uuid.uuid4())

def verify_token(apitoken, unique_id):
    headers = get_headers(apitoken, unique_id)
    url = f'{BASE_URL}/geement.usercenter/api/v1/user/seniority?sencodes=SEN2510301505321'
    try:
        r = requests.get(url, headers=headers, timeout=5)
        return r.json().get('code') == 200
    except:
        return False

def parse_address_by_amap(address):
    amap_key = get_config('amap_key')
    if not amap_key:
        return None
    try:
        url = f"https://restapi.amap.com/v3/geocode/geo?key={amap_key}&address={address}"
        res = requests.get(url, timeout=10).json()
        if res.get("status") == "1" and int(res.get("count", 0)) > 0:
            geo = res["geocodes"][0]
            loc = geo.get("location", "").split(",")
            return {
                "provice_name": geo.get("province", ""),
                "city_name": geo.get("city", "") or geo.get("province", ""),
                "area_name": geo.get("district", ""),
                "address": geo.get("formatted_address", ""),
                "longitude": float(loc[0]) if len(loc) == 2 else 0,
                "dimension": float(loc[1]) if len(loc) == 2 else 0
            }
    except:
        pass
    return None

def parse_address_by_nfsq(longitude, latitude):
    try:
        params = {"longitude": longitude, "dimension": latitude}
        res = requests.get(ADDRESS_URL, params=params, timeout=10).json()
        if res.get("code") == 200 and res.get("data"):
            data = res["data"]
            return {
                "provice_name": data.get("province", ""),
                "city_name": data.get("city", "") or data.get("province", ""),
                "area_name": data.get("district", ""),
                "address": data.get("address", ""),
                "longitude": float(longitude),
                "dimension": float(latitude)
            }
    except:
        pass
    return None

def parse_address(address):
    use_amap = get_config('use_amap', 'false').lower() == 'true'

    if use_amap:
        return parse_address_by_amap(address)
    else:
        amap_key = get_config('amap_key')
        if amap_key:
            try:
                url = f"https://restapi.amap.com/v3/geocode/geo?key={amap_key}&address={address}"
                res = requests.get(url, timeout=10).json()
                if res.get("status") == "1" and int(res.get("count", 0)) > 0:
                    loc = res["geocodes"][0].get("location", "").split(",")
                    if len(loc) == 2:
                        return parse_address_by_nfsq(loc[0], loc[1])
            except:
                pass
        if "," in address:
            parts = address.split(",")
            if len(parts) == 2:
                try:
                    return parse_address_by_nfsq(float(parts[0]), float(parts[1]))
                except:
                    pass
        return None

def get_location_data(user_info=None):
    if user_info and all([user_info.get(k) for k in ['province', 'city', 'district', 'address', 'longitude', 'latitude']]):
        return {
            "provice_name": user_info['province'],
            "city_name": user_info['city'],
            "area_name": user_info['district'],
            "address": user_info['address'],
            "longitude": float(user_info['longitude']),
            "dimension": float(user_info['latitude'])
        }

    default_address = get_config('default_address')
    if default_address:
        return parse_address(default_address)

    return None

def notify_masters(msg):
    notify = get_config('notify')
    if notify:
        sg.notifyMasters(msg, notify.split(','))

def pushplus_notify(title, content):
    token = ""
    topic = "1"  # 群组编码
    try:
        url = "http://www.pushplus.plus/send"
        data = {
            "token": token,
            "title": title,
            "content": content,
            "template": "html",
            "topic": topic  # 推送到群组
        }
        res = requests.post(url, json=data, timeout=10).json()
        return res.get('code') == 200
    except:
        return False

def parse_payment_result(result):
    return True

def get_payment_config():
    return {}

def generate_qrcode(url):
    try:
        encoded_url = urllib.parse.quote(url, safe='')
        return f"https://api.qrtool.cn/?text={encoded_url}"
    except:
        return None

class NFSQ:
    def __init__(self, user, name, ck, usid):
        self.user = user
        self.name = name
        self.ck = ck
        self.usid = usid
        self.apitoken, self.unique_id = parse_ck(ck)
        self.headers = get_headers(self.apitoken, self.unique_id)

    def check_login(self):
        url = f"{BASE_URL}/geement.usercenter/api/v1/user/seniority?sencodes=SEN2510301505321"
        try:
            res = requests.get(url, headers=self.headers, timeout=5).json()
            return res.get('code') == 200
        except:
            return False

    def do_tasks(self):
        url = f'{BASE_URL}/geement.marketingplay/api/v1/task?pageNum=1&pageSize=10&task_status=2&status=1&group_id=2510301511011&is_db=1'
        try:
            h = self.headers.copy()
            h["content-type"] = "application/x-www-form-urlencoded"
            res = requests.get(url, headers=h, timeout=10).json()
            if res.get("code") == 200:
                tasks = res.get("data", [])
                print("🎯 扫描任务状态...")
                done = 0
                for t in tasks:
                    if t.get('complete_status') == 0:
                        self._join_task(t['id'], t['name'])
                        done += 1
                        time.sleep(1)
                if done == 0:
                    print("👌 任务已全部完成")
        except Exception as e:
            print(f"❌ 获取任务出错: {e}")

    def _join_task(self, task_id, name):
        action_time = time.strftime("%Y-%m-%d %H:%M:%S")
        url = f'{BASE_URL}/geement.marketingplay/api/v1/task/join'
        params = {"action_time": action_time, "task_id": task_id}
        try:
            h = self.headers.copy()
            h["content-type"] = "application/x-www-form-urlencoded"
            res = requests.get(url, headers=h, params=params, timeout=10).json()
            if res.get('success'):
                print(f"✅ {name}: 完成")
            elif "已参与" in str(res.get("msg", "")):
                print(f"⏩ {name}: 已完成")
            else:
                print(f"❌ {name}: {res.get('msg', '未知错误')}")
        except Exception as e:
            print(f"❌ {name}: {e}")

    def receive_prize(self, log_id, goods_type=None):
        url = f"{BASE_URL}/geement.actjextra/api/v1/act/win/goods/youzan/receive"
        if goods_type == 160:
            url = f"{BASE_URL}/geement.actjextra/api/v1/act/win/goods/160goods/receive"
        try:
            h = self.headers.copy()
            h["content-type"] = "application/x-www-form-urlencoded"
            res = requests.post(url, headers=h, data=f"log_ids={log_id}", timeout=10).json()
            if res.get('code') == 200:
                print("🎁 奖品自动核销成功!")
            elif "160goods" not in url:
                url2 = f"{BASE_URL}/geement.actjextra/api/v1/act/win/goods/160goods/receive"
                requests.post(url2, headers=h, data=f"log_ids={log_id}", timeout=10)
        except:
            pass

    def lottery_once(self, scene_code, i, location_data):
        url = f"{BASE_URL}/geement.marketinglottery/api/v1/marketinglottery"
        try:
            payload = {**location_data, "code": scene_code}
            res = requests.post(url, headers=self.headers, json=payload, timeout=10).json()

            if res.get('success'):
                prize = res.get('data', {}).get('prizedto')
                if prize:
                    name = prize.get('prize_name', '未知')
                    level = prize.get('prize_level', '')
                    icon = "🚨 欧皇!" if "一等奖" in str(level) else "🎉 中奖!"
                    print(f"{icon} [场景{scene_code[-5:]}] 第{i}次: [{level}] {name}")

                    goods = prize.get('goods', [])
                    if goods:
                        self.receive_prize(goods[0].get('log_id'), goods[0].get('goods_type'))

                    if "一等奖" in str(level):
                        self._send_win_notify(level, name, location_data)
                else:
                    print(f"💨 未中奖 [场景{scene_code[-5:]}] 第{i}次")
                return True
            else:
                msg = res.get('msg', '未知')
                if "请登录" in str(msg) or "token" in str(msg).lower():
                    print(f"🚫 Token失效，停止运行 ({msg})")
                    return "INVALID_TOKEN"
                if "不足" in str(msg) or "资格" in str(msg):
                    return False
                if "达到最大" in str(msg) or "上限" in str(msg):
                    print(f"🛑 每日额度已满 ({msg})")
                    return "STOP_ALL"
                print(f"⭕ 异常: {msg}")
                return True
        except Exception as e:
            print(f"❌ 抽奖出错: {e}")
            return True

    def _send_win_notify(self, level, name, location_data):
        msg = f"🎈农夫山泉中奖通知\n用户: {self.user}\n账号: {self.name}\n中奖: [{level}] {name}\n时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        notify_masters(msg)

        if "一等奖" in str(level):
            pushplus_content = f"""
            <h2>🎉 农夫山泉一等奖中奖通知</h2>
            <p><b>账号:</b> {self.name}</p>
            <p><b>奖品:</b> [{level}] {name}</p>
            <p><b>地址:</b> {location_data.get('provice_name', '')}{location_data.get('city_name', '')}{location_data.get('area_name', '')}</p>
            <p><b>经纬度:</b> {location_data.get('longitude', '')},{location_data.get('dimension', '')}</p>
            <p><b>时间:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            """
            pushplus_notify("🎉农夫山泉一等奖", pushplus_content)

        if "一等奖" in str(level) and get_config('follow_lottery', 'false').lower() == 'true':
            self._trigger_follow_lottery(location_data)

    def _trigger_follow_lottery(self, location_data):
        print(f"🔥 触发跟抽! 经纬度: {location_data['longitude']},{location_data['dimension']}")
        notify_masters(f"🔥 农夫跟抽触发!\n中奖账号: {self.name}\n经纬度: {location_data['longitude']},{location_data['dimension']}\n正在为所有账号跟抽...")

        today = datetime.now().strftime("%Y-%m-%d")
        all_users = [] or []

        success_count = 0
        for user_key in all_users:
            if user_key == self.user:
                continue  # 跳过当前用户（已经中奖了）

            user_data = '2099-12-31'
            if not user_data:
                continue

            try:
                accounts = _sg_literal(user_data)
                for usid, info in accounts.items():
                    if info.get('sqsj', '') <= today:
                        continue

                    ck = info.get('ck', '')
                    if not ck:
                        continue

                    try:
                        apitoken, unique_id = parse_ck(ck)
                        headers = get_headers(apitoken, unique_id)

                        for scene in SCENE_LIST:
                            url = f"{BASE_URL}/geement.marketinglottery/api/v1/marketinglottery"
                            payload = {**location_data, "code": scene}
                            res = requests.post(url, headers=headers, json=payload, timeout=10).json()

                            if res.get('success'):
                                prize = res.get('data', {}).get('prizedto')
                                if prize:
                                    prize_name = prize.get('prize_name', '未知')
                                    prize_level = prize.get('prize_level', '')
                                    print(f"🎯 跟抽[{info['name']}]: [{prize_level}] {prize_name}")

                                    goods = prize.get('goods', [])
                                    if goods:
                                        log_id = goods[0].get('log_id')
                                        goods_type = goods[0].get('goods_type')
                                        receive_url = f"{BASE_URL}/geement.actjextra/api/v1/act/win/goods/youzan/receive"
                                        if goods_type == 160:
                                            receive_url = f"{BASE_URL}/geement.actjextra/api/v1/act/win/goods/160goods/receive"
                                        h = headers.copy()
                                        h["content-type"] = "application/x-www-form-urlencoded"
                                        requests.post(receive_url, headers=h, data=f"log_ids={log_id}", timeout=10)

                                    if "一等奖" in str(prize_level):
                                        notify_masters(f"🎉 跟抽大奖!\n账号: {info['name']}\n奖品: [{prize_level}] {prize_name}")

                                    success_count += 1
                                break  # 一个账号只抽一次
                            time.sleep(0.5)
                    except:
                        continue
            except:
                continue

        print(f"✅ 跟抽完成，共 {success_count} 个账号参与")
        notify_masters(f"✅ 跟抽完成，共 {success_count} 个账号参与抽奖")

    def run_lottery(self, location_data):
        print(f"🚀 开始双通道混合抽奖 (上限 {MAX_TOTAL_TRY} 次)...")
        current_try = 0
        while current_try < MAX_TOTAL_TRY:
            current_try += 1
            scene_active = False
            for scene in SCENE_LIST:
                result = self.lottery_once(scene, current_try, location_data)
                if result == "INVALID_TOKEN":
                    return False
                if result == "STOP_ALL":
                    print("🛑 触发每日上限，停止运行")
                    return True
                if result is True:
                    scene_active = True
                    break
            if not scene_active:
                print("💤 所有场景资格不足，结束")
                break
            time.sleep(random.randint(DELAY_MIN, DELAY_MAX))
        return True

    def query_prizes(self):
        url = f'{BASE_URL}/geement.actjextra/api/v1/act/win/goods/simple?act_codes=ACT2510301507191%2CACT2510301505581'
        try:
            res = requests.get(url, headers=self.headers, timeout=10).json()
            if res.get("success") or res.get("code") == 200:
                data = res.get("data") or []
                if not data:
                    print("📭 暂无中奖记录")
                    return
                for i in data[:5]:
                    level = i.get("win_prize_level", '')
                    name = i.get('win_prize_name', '')
                    scan_time = i.get('scan_time', '')
                    if ("一等奖" in str(level) or "特等奖" in str(level)) and "十一等奖" not in str(level):
                        print(f"🌈{level} {name}")
                    else:
                        print(f"🎁{level} {name} ({scan_time})")
            else:
                print(f"❌ 查询失败: {res.get('msg', '未知错误')}")
        except Exception as e:
            print(f"❌ 查询出错: {e}")

    def main(self):
        try:
            print(f"\n============= 🌊 {self.name} =============")
            if not self.check_login():
                print("🚫 Token已失效，请重新抓包!")
                return False

            ts = '2099-12-31'
            user_info = _sg_literal(ts).get(self.usid, {}) if ts else {}
            location_data = get_location_data(user_info)

            if not location_data:
                print("⚠️ 请先配置运行地址!")
                return False

            print(f"📍 运行地址: {location_data['provice_name']}{location_data['city_name']}{location_data['area_name']}")

            print("\n----------- 📝 每日任务 -----------")
            self.do_tasks()
            time.sleep(1)

            print("\n----------- 🎲 双通道抽奖 -----------")
            self.run_lottery(location_data)

            print("\n----------- 🎁 中奖查询 -----------")
            self.query_prizes()

            print(f"\n============= 🏁 {self.name} 结束 =============\n")
            return True
        except Exception as e:
            print(f"\n❌ 运行出错: {e}")
            return False

class ATM_nfsq:
    def __init__(self, user, sender):
        self.user = user
        self.sender = sender
        self.usid = None
        self.ck = None
        self.name = None
        self.sqsj = None

    def _get_user_input(self, timeout=60000, allow_quit=True):
        result = self.sender.listen(timeout)
        if result is None:
            self.sender.reply("⏰ 超时退出！")
            return None
        if allow_quit and result.lower() == 'q':
            self.sender.reply("✅ 已退出")
            return None
        return result

    def _get_user_data(self):
        data = '2099-12-31'
        return _sg_literal(data) if data and data != '{}' else None

    def _save_user_data(self, data):
        """保存用户数据"""
    def _check_token(self, ck):
        try:
            apitoken, unique_id = parse_ck(ck)
            return verify_token(apitoken, unique_id)
        except:
            return False

    def nfsc(self):
        self.sender.reply("欢迎使用农夫山泉系统，请先设置备注名(1-6字符)，退出输入'q'")
        name = self._get_user_input()
        if not name:
            return
        if len(name) > 6 or len(name) < 1:
            self.sender.reply("❌ 备注名不符合要求！")
            return

        self.sender.reply(f"""{name}! 你好!
抓包微信小程序: 农夫山泉生肖水
域名: sxs-consumer.nfsq.com.cn
请求头获取: apitoken
格式: 直接发送apitoken即可
请在120s内发送，退出回复'q'""")

        ck = self.sender.input(120000, 1000, False)
        if not ck or ck.lower() == 'q':
            self.sender.reply("已退出！")
            return

        try:
            apitoken, unique_id = parse_ck(ck)
            if not verify_token(apitoken, unique_id):
                self.sender.reply(f"❌ {name} Token验证失败，请检查后重试！")
                return

            data = self._get_user_data() or {}
            existing_usid = next((k for k, v in data.items() if v['name'] == name), None)

            if existing_usid:
                data[existing_usid]['ck'] = ck
                self._save_user_data(data)
                self.sender.reply(f"✅ {name} 更新成功！发送'农夫管理'管理账号")
            else:
                new_usid = str(uuid.uuid4())
                data[new_usid] = {'name': name, 'ck': ck, 'sqsj': datetime.now().strftime("%Y-%m-%d")}
                self._save_user_data(data)
                self.sender.reply(f"✅ {name} 登录成功！发送'农夫管理'管理账号")
        except ValueError as e:
            self.sender.reply(f"❌ {e}")
        except Exception as e:
            self.sender.reply(f"❌ 登录错误: {e}")

    def nfplsc(self):
        self.sender.reply("""========批量登录========
📝 格式说明:
每行一个账号，格式为: 备注名#apitoken
例如:
账号1#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
账号2#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
账号3#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

⚠️ 注意事项:
1. 备注名1-6个字符
2. 使用#号分隔备注名和token
3. 每行一个账号
4. 请在120s内发送，退出回复'q'
======================
请发送账号信息:""")

        content = self.sender.input(120000, 1000, False)
        if not content or content.lower() == 'q':
            self.sender.reply("已退出！")
            return

        lines = content.strip().split('\n')
        if not lines:
            self.sender.reply("❌ 未检测到账号信息！")
            return

        data = self._get_user_data() or {}
        success_count = 0
        fail_count = 0
        result_msg = "========批量登录结果========\n"

        for line in lines:
            line = line.strip()
            if not line or line.lower() == 'q':
                continue

            if '#' not in line:
                result_msg += f"❌ 格式错误: {line[:20]}...\n"
                fail_count += 1
                continue

            parts = line.split('#', 1)
            if len(parts) != 2:
                result_msg += f"❌ 格式错误: {line[:20]}...\n"
                fail_count += 1
                continue

            name = parts[0].strip()
            ck = parts[1].strip()

            if len(name) > 6 or len(name) < 1:
                result_msg += f"❌ {name}: 备注名不符合要求(1-6字符)\n"
                fail_count += 1
                continue

            try:
                apitoken, unique_id = parse_ck(ck)
                if not verify_token(apitoken, unique_id):
                    result_msg += f"❌ {name}: Token验证失败\n"
                    fail_count += 1
                    continue

                existing_usid = next((k for k, v in data.items() if v['name'] == name), None)

                if existing_usid:
                    data[existing_usid]['ck'] = ck
                    result_msg += f"✅ {name}: 更新成功\n"
                else:
                    new_usid = str(uuid.uuid4())
                    data[new_usid] = {'name': name, 'ck': ck, 'sqsj': datetime.now().strftime("%Y-%m-%d")}
                    result_msg += f"✅ {name}: 登录成功\n"

                success_count += 1
            except Exception as e:
                result_msg += f"❌ {name}: {str(e)[:30]}\n"
                fail_count += 1

        if success_count > 0:
            self._save_user_data(data)

        result_msg += f"======================\n📊 成功: {success_count}个\n📊 失败: {fail_count}个\n发送'农夫管理'管理账号"
        self.sender.reply(result_msg)

    def nfgl(self):
        data = self._get_user_data()
        if not data:
            self.sender.reply("❌ 未找到账号信息，请先上车！")
            return

        today = datetime.now().strftime("%Y-%m-%d")
        msg = "========农夫管理========\n0、一键授权所有账号\n9999、一键运行所有账号\n======================\n"
        id_map = {}
        status_map = {}

        for i, (usid, info) in enumerate(data.items(), 1):
            self.ck = info['ck']
            status = '✅有效' if self._check_token(info['ck']) else '❌失效'
            expired = "(已到期)" if info['sqsj'] <= today else ""
            msg += f"{i}、{info['name']}\n状态: {status}\n授权: ⏰{info['sqsj']}{expired}\n======================\n"
            id_map[i] = {'usid': usid, **info}
            status_map[i] = status

        msg += "回复序号选择账号，退出【q】"
        self.sender.reply(msg)

        choice = self._get_user_input()
        if not choice:
            return

        if choice == '9999':
            self._run_all_accounts(data)
        elif choice == '0':
            self._batch_auth(data)
        elif choice.isdigit() and int(choice) in id_map:
            acc = id_map[int(choice)]
            self.usid, self.ck, self.name, self.sqsj = acc['usid'], acc['ck'], acc['name'], acc['sqsj']
            if '有效' in status_map[int(choice)]:
                self._manage_account()
            else:
                self.sender.reply("❌ 账号已失效，请先更新！")
        else:
            self.sender.reply("❌ 输入有误！")

    def _manage_account(self):
        self.sender.reply(f"""========账号管理========
账号: {self.name}
1、账号授权
2、任务运行
3、删除账号
4、设置地址
======================
回复序号，退出【q】""")

        choice = self._get_user_input()
        if not choice:
            return

        actions = {'1': self._auth_account, '2': self._run_account, '3': self._delete_account, '4': self._set_address}
        if choice in actions:
            actions[choice]()
        else:
            self.sender.reply("❌ 输入有误！")

    def _run_account(self):
        today = datetime.now().strftime("%Y-%m-%d")
        if self.sqsj <= today:
            self.sender.reply(f"❌ {self.name} 授权已到期，请先续费！")
            return

        self.sender.reply(f"🎮 开始为【{self.name}】运行任务...")

        old_stdout = sys.stdout
        output = StringIO()
        sys.stdout = output

        try:
            nfsq = NFSQ(self.user, self.name, self.ck, self.usid)
            nfsq.main()
            self.sender.reply(output.getvalue())
        except Exception as e:
            self.sender.reply(f"❌ 运行出错: {e}")
        finally:
            sys.stdout = old_stdout
            output.close()

    def _run_all_accounts(self, data):
        yxbf = int(get_config('yxbf', '1'))
        today = datetime.now().strftime("%Y-%m-%d")
        valid = [(usid, info) for usid, info in data.items() if info['sqsj'] > today]

        self.sender.reply(f"🎮 开始运行\n⚡ 并发: {yxbf}\n✅ 有效账号: {len(valid)}个")

        for usid, info in valid:
            old_stdout = sys.stdout
            output = StringIO()
            sys.stdout = output
            try:
                nfsq = NFSQ(self.user, info['name'], info['ck'], usid)
                nfsq.main()
                self.sender.reply(output.getvalue())
            except Exception as e:
                self.sender.reply(f"❌ {info['name']} 出错: {e}")
            finally:
                sys.stdout = old_stdout
                output.close()
            time.sleep(1)

        self.sender.reply(f"🎉 运行完成，共 {len(valid)} 个账号")

    def _delete_account(self):
        self.sender.reply(f"确认删除【{self.name}】？(y/n)")
        if self._get_user_input(allow_quit=False) == 'y':
            data = self._get_user_data()
            del data[self.usid]
            self._save_user_data(data)
            self.sender.reply(f"✅ {self.name} 删除成功！")
        else:
            self.sender.reply("已取消")

    def _set_address(self):
        self.sender.reply("请输入详细地址(如:广东省广州市天河区xxx)，退出【q】")
        address = self._get_user_input()
        if not address:
            return

        amap_key = get_config('amap_key')
        if not amap_key:
            self.sender.reply("❌ 请先配置高德地图API key")
            return

        try:
            url = f"https://restapi.amap.com/v3/geocode/geo?key={amap_key}&address={address}"
            res = requests.get(url, timeout=10).json()
            if res["status"] == "1" and int(res["count"]) > 0:
                geo = res["geocodes"][0]
                loc = geo.get("location", "").split(",")
                addr_info = {
                    'province': geo.get("province", ""),
                    'city': geo.get("city", "") or geo.get("province", ""),
                    'district': geo.get("district", ""),
                    'address': geo.get("formatted_address", ""),
                    'longitude': loc[0] if len(loc) == 2 else "",
                    'latitude': loc[1] if len(loc) == 2 else ""
                }

                data = self._get_user_data()
                data[self.usid].update(addr_info)
                self._save_user_data(data)

                self.sender.reply(f"""✅ 地址设置成功!
📍 {addr_info['province']}{addr_info['city']}{addr_info['district']}
📍 {addr_info['address']}
📍 经纬度: {addr_info['longitude']},{addr_info['latitude']}""")
            else:
                self.sender.reply("❌ 地址解析失败")
        except Exception as e:
            self.sender.reply(f"❌ 设置失败: {e}")

    def _auth_account(self):
        sqje = get_config('sqje', '6.6')
        sqsj = int(get_config('sqsj', '30'))
        jfsl = int(get_config('jfsl', '200'))

        if self.sender.isAdmin():
            self.sender.reply(f"=====管理员授权=====\n每月{sqsj}天\n请输入月数，退出【q】")
            months = self._get_user_input()
            if not months or not months.isdigit() or int(months) <= 0:
                self.sender.reply("❌ 输入无效！")
                return
            self._do_auth(int(months), sqsj, is_admin=True)
        else:
            user_points = int(sg.bucketGet('dd_sign_points', self.user) or '0')
            zsm, use_ma_pay, _ = get_payment_config()

            pay_menu = "=====授权开通====="
            option_num = 1
            options_map = {}

            if zsm:
                pay_menu += f"\n{option_num}️⃣ 微信支付: {sqje}元/{sqsj}天"
                options_map[str(option_num)] = 'wechat'
                option_num += 1

            if use_ma_pay:
                pay_menu += f"\n{option_num}️⃣ 在线处理: {sqje}元/{sqsj}天"
                options_map[str(option_num)] = 'ma'
                option_num += 1

            if jfsl > 0:
                pay_menu += f"\n{option_num}️⃣ 积分支付: {jfsl}积分/{sqsj}天"
                pay_menu += f"\n   💫 当前积分: {user_points}"
                options_map[str(option_num)] = 'points'

            pay_menu += "\n------------------\n回复数字选择方式\n退出【q】"

            if not options_map:
                self.sender.reply("❌ 未配置任何支付方式，请检查配置！")
                return

            self.sender.reply(pay_menu)
            choice = self._get_user_input()
            if not choice or choice not in options_map:
                self.sender.reply("❌ 输入无效！")
                return

            selected_pay = options_map[choice]

            self.sender.reply("请输入月数，退出【q】")
            months = self._get_user_input()
            if not months or not months.isdigit() or int(months) <= 0:
                self.sender.reply("❌ 输入无效！")
                return

            months = int(months)

            if selected_pay == 'points':
                total = jfsl * months
                if self._points_pay(total, sqsj * months):
                    self._do_auth(months, sqsj)
            elif selected_pay == 'wechat':
                total = float(sqje) * months
                if self._wechat_pay(total, sqsj * months):
                    self._do_auth(months, sqsj)
            elif selected_pay == 'ma':
                _, _, ma_pay_config = get_payment_config()
                total = float(sqje) * months
                if self._ma_pay(total, sqsj * months, ma_pay_config):
                    self._do_auth(months, sqsj)

    def _batch_auth(self, data):
        return True

    def _do_auth(self, months, sqsj, is_admin=False):
        return True

    def _wechat_pay(self, total, days):
        if total == 0:
            return True

        zsm = get_config('wxzsm')
        if not zsm:
            self.sender.reply("❌ 未配置二维码，请检查配置！")
            return False

        if False:
            self.sender.reply("⚠️ 当前有人正在支付，请稍后再试！")
            return False

        self.sender.reply(f"""=====微信扫在线处理=====
🎫 商品: 农夫山泉授权
📅 时长: {days}天
💰 金额: {total:.2f}元
------------------
请使用微信扫在线处理
回复"q"取消支付""")
        self.sender.replyImage(zsm)

        result = False
        if str(result).lower() == 'q' or result is None:
            self.sender.reply("❌ 已取消支付" if str(result).lower() == 'q' else "❌ 支付超时")
            return False

        money, pay_time, from_name = parse_payment_result(result)
        if round(money, 1) >= round(total, 1):
            self.sender.reply(f"""=====支付成功=====
💰 金额: {money}元
⏰ 时间: {pay_time}
{f'👤 付款人: {from_name}' if from_name else ''}""")
            return True
        else:
            self.sender.reply(f"❌ 金额错误！应付: {round(total, 1)}元，实付: {round(money, 1)}元\n请稍后重试！")
            return False

    def _ma_pay(self, total, days, ma_pay_config):
        senderID = sg.getSenderID()
        out_trade_no = f"NFSQ{int(time.time())}{self.user}"

        params = {
            'pid': ma_pay_config['pid'],
            'type': ma_pay_config['type'].split(',')[0] if ma_pay_config.get('type') else 'alipay',
            'out_trade_no': out_trade_no,
            'name': f"{senderID}-农夫山泉授权-{total}",
            'money': str(total),
            'notify_url': ma_pay_config['notify_url'] or '',
            'return_url': ma_pay_config['return_url'] or '',
            'param': self.user
        }

        sorted_params = sorted(params.items(), key=lambda x: x[0])
        sign_str = "&".join([f"{k}={v}" for k, v in sorted_params])
        sign = hashlib.md5((sign_str + ma_pay_config['key']).encode()).hexdigest().lower()
        params['sign'] = sign
        params['sign_type'] = 'MD5'

        gateway = ma_pay_config['gateway'].rstrip('/')
        mapi_url = f"{gateway}/mapi.php"

        try:
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            response = requests.post(mapi_url, data=params, headers=headers, timeout=10)

            if response.status_code != 200:
                self.sender.reply(f"❌ 创建支付订单失败，状态码: {response.status_code}")
                return False

            result = response.json()
            if result.get('code') == 1:
                payurl = result.get('payurl', '')
                if not payurl:
                    self.sender.reply("❌ 未获取到支付链接")
                    return False

                qrcode_url = generate_qrcode(payurl)
                pay_type = ma_pay_config['type'].split(',')[0] if ma_pay_config.get('type') else 'alipay'
                pay_type_names = {'alipay': '支付宝', 'wxpay': '微信', 'qqpay': 'QQ钱包'}
                pay_type_name = pay_type_names.get(pay_type, pay_type)

                if qrcode_url:
                    self.sender.replyImage(qrcode_url)
                    self.sender.reply(f"""=====在线处理=====
🎫 商品: 农夫山泉授权
📅 时长: {days}天
💰 金额: {total}元
------------------
请使用【{pay_type_name}】扫在线处理
回复"q"取消支付""")
                else:
                    self.sender.reply(f"支付链接: {payurl}\n请复制到浏览器完成支付")

                for i in range(60):  # 最多等待5分钟
                    check_url = f"{gateway}/xpay/epay/api.php" if '/xpay/epay/api.php' not in gateway else gateway
                    check_params = {
                        'act': 'order',
                        'pid': ma_pay_config['pid'],
                        'key': ma_pay_config['key'],
                        'out_trade_no': out_trade_no
                    }

                    try:
                        check_resp = requests.get(check_url, params=check_params, timeout=10)
                        check_result = check_resp.json()

                        if check_result.get('code') == 1 and check_result.get('status') == 1:
                            self.sender.reply(f"""=====支付成功=====
🎫 商品: 农夫山泉授权
💰 金额: {total}元
📅 时长: {days}天""")
                            return True
                    except:
                        pass

                    user_input = self.sender.listen(5000)
                    if user_input and user_input.lower() == 'q':
                        self.sender.reply("✅ 已取消支付")
                        return False

                self.sender.reply("❌ 支付超时，请重新发起支付！")
                return False
            else:
                msg = result.get('msg', '未知错误')
                self.sender.reply(f"❌ 创建订单失败: {msg}")
                return False
        except Exception as e:
            self.sender.reply(f"❌ 支付请求失败: {e}")
            return False

    def _points_pay(self, total, days):
        user_points = int(sg.bucketGet('dd_sign_points', self.user) or '0')
        if user_points < total:
            self.sender.reply(f"❌ 积分不足！当前: {user_points}，需要: {int(total)}")
            return False

        self.sender.reply(f"""=====积分支付确认=====
💰 当前积分: {user_points}
💵 消耗积分: {int(total)}
📦 授权时长: {days}天
确认支付？[y]确认 [n]取消""")

        confirm = self._get_user_input(allow_quit=False)
        if confirm and confirm.lower() == 'y':
            new_balance = user_points - int(total)
            sg.bucketSet('dd_sign_points', self.user, str(new_balance))
            self.sender.reply(f"✅ 支付成功！剩余积分: {new_balance}")
            return True
        self.sender.reply("已取消")
        return False

    def nfcx(self):
        data = self._get_user_data()
        if not data:
            self.sender.reply("❌ 未找到账号信息，请先上车！")
            return

        today = datetime.now().strftime("%Y-%m-%d")
        msg = "========农夫查询========\n"
        for usid, info in data.items():
            self.ck = info['ck']
            status = '✅有效' if self._check_token(info['ck']) else '❌失效'
            expired = "(已到期)" if info['sqsj'] <= today else ""
            msg += f"账号: {info['name']}\n状态: {status}\n授权: ⏰{info['sqsj']}{expired}\n"

            if '有效' in status:
                prizes = self._query_prizes_list(info['ck'])
                if prizes:
                    msg += "-------近5条中奖-------\n"
                    for p in prizes[:5]:
                        level = p.get("win_prize_level", '')
                        name = p.get('win_prize_name', '')
                        if ("一等奖" in str(level) or "特等奖" in str(level)) and "十一等奖" not in str(level):
                            msg += f"🌈{level} {name}\n"
                        else:
                            msg += f"🎁{level} {name}\n"
                else:
                    msg += "📭 暂无中奖记录\n"
            msg += "======================\n"
        self.sender.reply(msg)

    def _query_prizes_list(self, ck):
        try:
            apitoken, unique_id = parse_ck(ck)
            headers = get_headers(apitoken, unique_id)
            url = f'{BASE_URL}/geement.actjextra/api/v1/act/win/goods/simple?act_codes=ACT2510301507191%2CACT2510301505581'
            res = requests.get(url, headers=headers, timeout=10).json()
            if res.get("success") or res.get("code") == 200:
                return res.get("data") or []
        except:
            pass
        return []

    def nfpz(self):
        configs = [
            ('wxzsm', '赞赏码'),
            ('sqje', '授权金额'),
            ('sqsj', '授权时间'),
            ('yxbf', '运行并发'),
            ('notify', '管理员通知'),
            ('jfsl', '积分单价'),
            ('amap_key', '高德地图key'),
            ('default_address', '默认地址'),
        ]

        msg = "========农夫配置========\n"
        for i, (key, name) in enumerate(configs, 1):
            val = get_config(key) or '未配置'
            if key in ['wxzsm', 'amap_key']:
                val = '已配置' if val != '未配置' else '未配置'
            msg += f"{i}、{name}({val})\n"
        msg += "======================\n回复序号修改，退出【q】"

        self.sender.reply(msg)
        choice = self._get_user_input()
        if not choice or not choice.isdigit():
            return

        idx = int(choice) - 1
        if 0 <= idx < len(configs):
            key, name = configs[idx]

            if key == 'default_address':
                self.sender.reply("请输入完整地址(如: 广东省广州市天河区珠江新城123号)：")
                val = self._get_user_input()
                if val:
                    location = parse_address_by_amap(val)
                    if location:
                        True
                        self.sender.reply(f"""✅ 地址设置成功！
📍 省份: {location['provice_name']}
📍 城市: {location['city_name']}
📍 区域: {location['area_name']}
📍 详细: {location['address']}
📍 经纬度: {location['longitude']},{location['dimension']}""")
                    else:
                        self.sender.reply("❌ 地址解析失败，请检查高德key是否配置正确！")
            else:
                self.sender.reply(f"请输入新的{name}：")
                val = self._get_user_input()
                if val:
                    True
                    self.sender.reply(f"✅ {name}设置成功！")

    def nfyx(self):
        yxbf = int(get_config('yxbf', '1'))
        all_keys = []
        if not all_keys:
            self.sender.reply("❌ 没有用户数据！")
            return

        today = datetime.now().strftime("%Y-%m-%d")
        total_valid = 0

        for uid in all_keys:
            data = '2099-12-31'
            if not data or data == '{}':
                continue
            data = _sg_literal(data)
            for usid, info in data.items():
                if info['sqsj'] > today:
                    total_valid += 1

        self.sender.reply(f"🎮 开始运行\n⚡ 并发: {yxbf}\n✅ 有效账号: {total_valid}个")

        for uid in all_keys:
            data = '2099-12-31'
            if not data or data == '{}':
                continue
            data = _sg_literal(data)
            for usid, info in data.items():
                if info['sqsj'] <= today:
                    continue
                old_stdout = sys.stdout
                output = StringIO()
                sys.stdout = output
                try:
                    nfsq = NFSQ(uid, info['name'], info['ck'], usid)
                    nfsq.main()
                    self.sender.reply(output.getvalue())
                except Exception as e:
                    self.sender.reply(f"❌ {info['name']} 出错: {e}")
                finally:
                    sys.stdout = old_stdout
                    output.close()
                time.sleep(1)

        self.sender.reply("🎉 全部运行完成！")

    def nfsq(self):
        self.sender.reply("""========农夫授权========
1、一键授权所有用户
2、单独授权用户
======================
回复序号，退出【q】""")

        choice = self._get_user_input()
        if choice == '1':
            self._admin_batch_auth()
        elif choice == '2':
            self._admin_single_auth()

    def _admin_batch_auth(self):
        return True

    def _admin_single_auth(self):
        return True

if __name__ == '__main__':
    senderID = sg.getSenderID()
    sender = sg.Sender(senderID)
    user = sender.getUserID()
    message = sender.getMessage()

    atm = ATM_nfsq(user, sender)

    commands = {
        '农夫上车': atm.nfsc,
        '农夫批量': atm.nfplsc,
        '农夫管理': atm.nfgl,
        '农夫查询': atm.nfcx,
        '农夫运行': lambda: atm.nfyx() if sender.isAdmin() else None,
        '农夫配置': lambda: atm.nfpz() if sender.isAdmin() else None,
        '农夫授权': lambda: atm.nfsq() if sender.isAdmin() else None,
        '农夫版本': lambda: sender.reply("""当前版本V7.0
🔔功能介绍:
1、V7.0适配新版API接口
2、支持批量授权用户
3、支持中奖实时通知
4、支持并发运行任务
5、支持自定义地址
======================
📱用户指令: 农夫上车/批量/管理/查询
⚙️管理员: 农夫配置/运行/授权
======================
🎯每日任务:
✨ 每日签到
🎲 双通道混合抽奖
📝 中奖查询""") if sender.isAdmin() else None,
        '农夫教程': lambda: sender.reply("""📖 农夫山泉使用教程
🔍 抓包说明:
1、打开微信小程序：农夫山泉生肖水
2、抓包域名: sxs-consumer.nfsq.com.cn
3、请求头获取: apitoken
4、数据有效期为三天！

💡 使用说明:
• 发送【农夫上车】绑定单个账号
• 发送【农夫批量】绑定多个账号
• 发送【农夫批量】批量绑定账号
• 发送【农夫管理】管理账号
• 发送【农夫查询】查询状态

✨ 功能介绍:
• 每日签到任务
• 双通道混合抽奖
• 中奖实时推送
• 奖品自动核销

📝 批量登录格式:
每行一个账号: 备注名#apitoken
例如:
账号1#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
账号2#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...""")
    }

    if message in commands:
        cmd = commands[message]
        if cmd:
            cmd()
