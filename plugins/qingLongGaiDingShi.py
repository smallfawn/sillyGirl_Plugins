# [title: 青龙改定时]
# [name: qingLongGaiDingShi]
# [language: python]
# [class: 任务]
# [author: sn_jmh]
# [version: v1.0.9]
# [public: true]
# [disable: false]
# [admin: true]
# [rule: ^改$]
# [cron: 0 16 * * *]
# [icon: https://api.iconify.design/lucide:bot.svg]
# [description: 批量调整青龙脚本定时表达式。]
# [depe: ["requests"]]

import asyncio as _sg_asyncio
import os as _sg_os
import time as _sg_time
import types as _sg_types
from threading import Thread as _sg_Thread
from sillygirl import Adapter as _SGAdapter, Bucket as _SGBucket, Sender as _SGSender, sender as _sg_sender, plugin

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

config = plugin.Form({
    "enable": plugin.Form.boolean().title("是否启用").default(True),
    'sn_jmh_add_js': plugin.Form.string().title('脚本名字').default('').description('多个用英文逗号分割，6dylan6_jdpro/jd_zzhb.js。'),
    'sn_jmh_add_time': plugin.Form.string().title('时间增加几').default('').description('填写数字。默认是1。'),
    'sn_jmh_ds_Container': plugin.Form.string().title('指定容器').default('').description('绑定的容器名用英文逗号分割。'),
    'sn_jmh_version': plugin.Form.boolean().title('青龙版本').default(False).description('默认高版本,勾选为低版本。'),
    'sn_jmh_SN_QLS': plugin.Form.string().title('青龙地址和秘钥').default('').description('[{"name":"青龙1","host":"http://192.168.8.1:5700","client_id":"xxx","client_secret":"xxx"}]。json格式,sillyGirl2.5.5版本以后的必须填写。'),
})
_CONFIG_FIELD_MAP = {
    ('sn_jmh', 'add_js'): 'sn_jmh_add_js',
    ('sn_jmh', 'add_time'): 'sn_jmh_add_time',
    ('sn_jmh', 'ds_Container'): 'sn_jmh_ds_Container',
    ('sn_jmh', 'version'): 'sn_jmh_version',
    ('sn_jmh', 'SN_QLS'): 'sn_jmh_SN_QLS',
}

import json
import sys
import time
import requests

token = None
host = None
groupCode = ""
add_js = sg.bucketGet("sn_jmh", "add_js")

add_js_list = add_js.split(',')
add_time = sg.bucketGet("sn_jmh", "add_time")
if add_time == "":
    add_time = 1

QLS = sg.bucketGet("sn_jmh", "SN_QLS")

ql_Container = sg.bucketGet("sn_jmh", "ds_Container")
version = sg.bucketGet("sn_jmh", "version")
bucket = ['pinQQ', 'pinQB', 'pinWX', 'pinWB', 'pinTG', 'pinMQ']
imType = ['qq', 'qb', 'wx', 'wb', 'tg', 'tb', 'mq']

def printf(msg):
    print(msg)
    sys.stdout.flush()

def run_matching_names(data, ql):
    ql_list = ql.replace("'", "").split(",")
    matching_items = []

    for item in data:
        if item["name"] in ql_list:
            matching_items.append(item)  # 将匹配项添加到列表中

    if len(matching_items) > 0:
        print(f"指定:[{len(matching_items)}]个容器")
        return matching_items
    else:
        sg.notifyMasters("通知\n填写指定容器错误，将运行全部容器。", imType)
        return False
def get_token(host, client_id, client_secret):
    try:
        url = f"{host}/open/auth/token?client_id={client_id}&client_secret={client_secret}"
        response = requests.get(url)
        response.raise_for_status()
        token = response.json()["data"]["token"]
        return token
    except requests.exceptions.RequestException as e:
        printf(f"获取令牌失败:{e}")
        return None

def Get_Status(host, token , search):
    try:
        url = f"{host}/open/crons?searchValue={search}"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response_json = json.loads(response.text)
        data_value = response_json.get("data", None)
        return data_value

    except requests.exceptions.RequestException as e:
        printf(f"获取状态失败: {e}")
        return False

def set_cron_schedule(host, token, task_id, task_name, command, schedule, labels):
    try:
        url = f"{host}/open/crons"
        payload = {
            "id": task_id,
            "name": task_name,
            "command": command,
            "schedule": schedule,
            "labels": labels
        }
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.put(url, headers=headers, json=payload)
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        print("设置任务调度时间失败:", e)

def change_time(status_list):
    try:
        if version == "true":
            status = status_list[0]
            task_id = status['id']
            task_name = status['name']
            command = status['command']
            schedule = status['schedule']
            labels = status['labels']
        else:
            task_id = status_list['data'][0]['id']
            task_name = status_list['data'][0]['name']
            command = status_list['data'][0]['command']
            schedule = status_list['data'][0]['schedule']
            labels = status_list['data'][0]['labels']
        schedule_parts = schedule.split(" ")
        if len(schedule_parts) >= 5:
            new_minute = int(schedule_parts[0]) + int(add_time)
            print(new_minute)
            if int(new_minute) >= 60:
                sg.notifyMasters(f"通知\n[{task_name}]\n第一个时间大于或等于60,请到青龙重新设置", imType)
                printf("第一个时间大于或等于60,请到青龙重新设置")
            else:
                printf("第一个时间正常.")
                new_schedule = f"{new_minute} {' '.join(schedule_parts[1:])}"
                set_cron_schedule(host, token, task_id, task_name, command, new_schedule, labels)
                sg.notifyMasters(f"通知\n[{task_name}]\n原时间:{schedule}\n现时间:{new_schedule}", imType)
                printf("设置时间成功")
        else:
            print("定时获取错误")

    except Exception as e:
        print(f"发生错误: {e}")

def run():
    global host
    global token
    try:
        if QLS:
            data = json.loads(QLS)
            if ql_Container != "":
                data = run_matching_names(data, ql_Container)
            for item in data:
                host = item['host']
                printf(f"运行【{item['name']}】容器")
                token = get_token(item["host"], item["client_id"], item["client_secret"])
                for js in add_js_list:
                    status = Get_Status(item["host"], token, js)
                    printf(f"js:{js}")
                    printf(f"data_dict:{status}")
                    change_time(status)
        else:
            print("您没有绑定青龙容器。")
    except Exception as e:
        print(f"主程序发生异常: {e}")

if __name__ == '__main__':
    if QLS:
        run()
        print("已设置青龙地址")
    else:
        print("没有设置青龙地址")
        sg.notifyMasters("通知\n未设置青龙地址结束。", imType)
