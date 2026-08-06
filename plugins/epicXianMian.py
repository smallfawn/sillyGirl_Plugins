# [title: Epic限免]
# [name: epicXianMian]
# [language: python]
# [class: 任务]
# [author: buzhi]
# [version: v1.0.2]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(epic|EPIC|Epic)限免$|^(epic|EPIC|Epic)限免?$]
# [icon: https://api.iconify.design/lucide:bot.svg]
# [description: Epic限免]
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
import datetime

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
senderType = sender.getImtype()
mess = sender.getMessage()

def get_free_games() -> dict:
    timestamp = datetime.datetime.timestamp(datetime.datetime.now())
    games = {"timestamp": timestamp, "free_now": [], "free_next": []}
    base_store_url = "https://store.epicgames.com"
    api_url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?country=CN"
    resp = requests.get(api_url, timeout=30)
    for element in resp.json()["data"]["Catalog"]["searchStore"]["elements"]:
        if promotions := element["promotions"]:
            game = {}
            game["title"] = element["title"]
            game["images"] = element["keyImages"]
            game["origin_price"] = element["price"]["totalPrice"]["fmtPrice"][
                "originalPrice"
            ]
            game["discount_price"] = element["price"]["totalPrice"]["fmtPrice"][
                "discountPrice"
            ]
            game["store_url"] = (
                f"{base_store_url}/p/{element['catalogNs']['mappings'][0]['pageSlug']}"
                if element["catalogNs"]["mappings"]
                else base_store_url
            )
            if offers := promotions["promotionalOffers"]:
                game["start_date"] = offers[0]["promotionalOffers"][0]["startDate"]
                game["end_date"] = offers[0]["promotionalOffers"][0]["endDate"]
                games["free_now"].append(game)
            if offers := promotions["upcomingPromotionalOffers"]:
                game["start_date"] = offers[0]["promotionalOffers"][0]["startDate"]
                game["end_date"] = offers[0]["promotionalOffers"][0]["endDate"]
                games["free_next"].append(game)
    return games

def get_msg(games: dict):
    if games:
        content = """
- ## Epic 本周限免"""
        for game in games["free_now"]:
            if game["discount_price"] == "0":
                content += f"""
- 游戏名：{game['title']}
    原价：{game['origin_price']}
    折扣价：{game['discount_price']}
    时间：{datetime.datetime.strftime(datetime.datetime.strptime(game["start_date"],'%Y-%m-%dT%H:%M:%S.%fZ') + datetime.timedelta(hours=8),'%Y年%m月%d日')} - {datetime.datetime.strftime(datetime.datetime.strptime(game["end_date"],'%Y-%m-%dT%H:%M:%S.%fZ') + datetime.timedelta(hours=8),'%Y年%m月%d日')}
    使用链接：{game['store_url']}
"""
        content += """
- ## Epic 下周限免"""
        for game in games["free_next"]:
            if game["discount_price"] == "0":
                content += f"""
- 游戏名：{game['title']}
    原价：{game['origin_price']}
    折扣价：{game['discount_price']}
    时间：{datetime.datetime.strftime(datetime.datetime.strptime(game["start_date"],'%Y-%m-%dT%H:%M:%S.%fZ') + datetime.timedelta(hours=8),'%Y年%m月%d日')} - {datetime.datetime.strftime(datetime.datetime.strptime(game["end_date"],'%Y-%m-%dT%H:%M:%S.%fZ') + datetime.timedelta(hours=8),'%Y年%m月%d日')}
    使用链接：{game['store_url']}
"""
    return content

if __name__ == "__main__":
    games = get_free_games()
    content = get_msg(games)
    sender.reply(content)
