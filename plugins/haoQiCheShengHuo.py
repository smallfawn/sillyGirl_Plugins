# [title: 好奇车生活]
# [name: haoQiCheShengHuo]
# [language: python]
# [class: 任务]
# [author: sky2022]
# [version: V7.9]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^车生活(.*)$]
# [icon: https://api.iconify.design/lucide:apple.svg]
# [description: 。]
# [depe: ["requests"]]


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
    'dd_hqcsh_Qinglong': form.string().title('设置对接容器').default('').description('你的变量需要添加到的容器？参数用丨分割'),
    'dd_hqcsh_osname': form.string().title('提交到青龙的变量名').default('').description('青龙容器内车生活的变量名'),
})
_CONFIG_FIELD_MAP = {
    ('dd_hqcsh', 'Qinglong'): 'dd_hqcsh_Qinglong',
    ('dd_hqcsh', 'osname'): 'dd_hqcsh_osname',
}

import requests, time, json
from datetime import datetime, timedelta
import asyncio

try:
    pass
except:
    senderID = sg.getSenderID()
    sender = sg.Sender(senderID)
    sender.reply("请先安装concurrent依赖")
    exit(0)
ts_all = []


class JD:
    def __init__(self, user, sender):
        self.user = user
        self.sender = sender
        self.bz = None
        self.sqsj = None
        self.ck = None
        self.point = None
        self.gq_point = None
        if sg.bucketGet("dd_hqcsh", "delbtn") == "":
            sg.bucketSet('dd_hqcsh', "delbtn", "true")
        if '2099-12-31' == "":
            True
        self.hd = {
            'Host': 'channel.cheryfs.cn',
            'wxappid': '619669369294712832',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
            'tenantId': '619669306447261696',
            'activityId': '621883730893492225',
            'Accept': 'application/json,text/plain, */*',
        }
        self.hd2 = {
            'Host': 'channel.cheryfs.cn',
            'Connection': 'keep-alive',
            'wxappid': '619669369294712832',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
            'tenantId': '619669306447261696',
            'activityId': '620821692188483585',
            'requestUrl': 'https://channel.cheryfs.cn/archer/act/619669306447261696/619669369294712832/activity/luckydraw-detail/620821692188483585',
            'Accept': 'application/json, text/plain, */*',
            'timestamp': str(round(time.time() * 1000)),
            'assemblyName': '%E5%88%AE%E5%88%AE%E4%B9%90',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://channel.cheryfs.cn/archer/act/619669306447261696/619669369294712832/activity/luckydraw-detail/620821692188483585',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-us,en',
        }

    def login(self, ck):
        self.hd["accountId"] = ck
        url = "https://channel.cheryfs.cn/archer/activity-api/common/accountPointLeft?pointId=620415610219683840&showExpire=true&timeType=day&indexDay="
        res = requests.get(url, headers=self.hd).json()
        if res["code"] == 200:
            self.gq_point = res["message"]
            self.point = res["result"]

            return True
        else:
            self.sender.reply("url请求失败！")
            return False

    def reward(self, ck):
        url = "https://channel.cheryfs.cn/archer/activity-api/pointsmall/queryPointsMallCardList?isGroup=false"
        headers = {
            'Host': 'channel.cheryfs.cn',
            'Connection': 'keep-alive',
            'wxappid': '619669369294712832',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
            'tenantId': '619669306447261696',
            'activityId': '621950054462152705',
            'requestUrl': 'https://channel.cheryfs.cn/archer/act/619669306447261696/619669369294712832/activity/luckydraw-detail/620821692188483585',
            'Accept': 'application/json, text/plain, */*',
            'timestamp': str(round(time.time() * 1000)),
            'assemblyName': '%E5%88%AE%E5%88%AE%E4%B9%90',
            'sign': 'eff41a284067d208807fbd94740245c7',
            'accountId': ck,
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://channel.cheryfs.cn/archer/act/619669306447261696/619669369294712832/activity/pointsmall-detail/621911913692942337?miniopeonid=ad332eed2e5dcccab7b9fc5068569c234fd17d426a4c447150b81a64f2faca43d09133dc910a196f3cd3c7dd29a720bd881ce390a785e9319cfb5f8f9b9443ea690b18b7f55ff124887643066a6ffee24a3e8fa2756c9360fa3c4c7bef095bc52e1621178de3ec6cdc2a20d5e32105db676c324392d0d67c982795bb&xcxAppId=wx8c6e8a965158ad6c',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-us,en',
        }
        res = requests.get(url, headers=headers)
        if res.json()["success"] == True:
            list0 = []
            msg = "最新奖励id\n"
            for i in range(len(res.json()["result"]["全部"])):
                cardid = res.json()["result"]["全部"][i]["id"]
                cardname = res.json()["result"]["全部"][i]["cardName"]
                cardjf = res.json()["result"]["全部"][i]["exchangePointsValue"]
                listdata = {
                    "name": cardname,
                    "jf": cardjf,
                    "id": cardid
                }
                msg += f"奖励{cardname}:id[{cardid}]:需要积分{cardjf}\n"
                list0.append(listdata)
            print(f"======\n{msg}======")
            return list0

    def today(self, ck):
        url = "https://channel.cheryfs.cn/archer/activity-api/common/accountPointInfo"
        headers = {
            'Host': 'channel.cheryfs.cn',
            'Connection': 'keep-alive',
            'wxappid': '619669369294712832',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
            'tenantId': '619669306447261696',
            'activityId': '621950054462152705',
            'requestUrl': 'https://channel.cheryfs.cn/archer/act/619669306447261696/619669369294712832/activity/luckydraw-detail/620821692188483585',
            'Accept': 'application/json, text/plain, */*',
            'timestamp': str(round(time.time() * 1000)),
            'assemblyName': '%E5%88%AE%E5%88%AE%E4%B9%90',
            'sign': 'eff41a284067d208807fbd94740245c7',
            'accountId': ck,
            "Content-Length": "113",
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://channel.cheryfs.cn/archer/act/619669306447261696/619669369294712832/activity/pointsmall-detail/621911913692942337?miniopeonid=ad332eed2e5dcccab7b9fc5068569c234fd17d426a4c447150b81a64f2faca43d09133dc910a196f3cd3c7dd29a720bd881ce390a785e9319cfb5f8f9b9443ea690b18b7f55ff124887643066a6ffee24a3e8fa2756c9360fa3c4c7bef095bc52e1621178de3ec6cdc2a20d5e32105db676c324392d0d67c982795bb&xcxAppId=wx8c6e8a965158ad6c',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-us,en',
        }
        data = {"pointId": "620415610219683840", "accountId": "", "type": 2, "pageNumber": 1, "pageSize": 10,
                "startDate": "", "endDate": ""}
        res = requests.post(url, headers=headers, json=data).json()
        if res["code"] == 200:
            jf = 0
            for d in res["result"]["accountPointLogs"]:
                t = d["updateTime"].split(" ")[0]
                if t == datetime.now().strftime("%Y-%m-%d"):
                    jf += d["amount"]
            return jf

    def tj(self):
        tong = sg.bucketGet("dd_hqcsh", self.user)
        if tong == "":
            self.sender.reply("欢迎使用车生活系统, 请先设置您的备注名(1-6个字符)。退出输入'q'!")
            bz = self.sender.listen(180000)
            if bz == "q":
                self.sender.reply("退出！")
                exit(0)
            else:
                self.sender.reply(
                    f"{bz}， 你好!\n抓包: 好奇车生活小程序\n域名:channel.cheryfs.cn \n请求头里面的accountId数据\n说明: 一天50积分左右，月积分2000+可以抢e卡,现金....\n请在120s内发送你的accountId数据, 退出回复'q'!")
                ck = self.sender.listen(180000)
                if ck == "q":
                    self.sender.reply("退出！")
                    exit(0)
                else:
                    if self.login(ck):
                        cks = []
                        data = {
                            bz: {
                                "ck": ck,
                                "qd": self.sender.getImtype(),
                                "sqsj": datetime.now().strftime("%Y-%m-%d")

                            }
                        }
                        cks.append(data)
                        sg.bucketSet("dd_hqcsh", self.user, f"{cks}")
                        self.sender.reply("🔔登录成功!发送'车生活管理'对账号进行管理!")
                    else:
                        self.sender.reply("输入有误，退出！")
                        exit(0)
        else:
            self.sender.reply(f"欢迎使用车生活系统, 请先设置您的备注名(1-6个字符)，当前已有[{len(_sg_literal(tong))}]个账号。退出输入'q'!")
            bz = self.sender.listen(180000)
            if bz == "q":
                self.sender.reply("退出！")
                exit(0)
            else:
                self.sender.reply(
                    f"{bz}， 你好!\n抓包: 好奇车生活小程序\n域名:channel.cheryfs.cn \n请求头里面的accountId数据\n说明: 一天50积分左右，月积分2000+可以抢e卡,现金....\n请在120s内发送你的accountId数据, 退出回复'q'!")
                ck = self.sender.listen(180000)
                if ck == "q":
                    self.sender.reply("退出！")
                    exit(0)
                else:
                    if self.login(ck):
                        userdata = _sg_literal(tong)
                        for aaa in userdata:
                            for k, y in aaa.items():
                                if k == bz:
                                    aaa[k] = {'ck': ck, "qd": self.sender.getImtype(), 'sqsj': y["sqsj"]}
                                    sg.bucketSet("dd_hqcsh", self.user, f"{userdata}")
                                    self.sender.reply(f"[{k}]更新ck成功")
                                    exit(0)

                        data = {
                            bz: {
                                "ck": ck,
                                "qd": self.sender.getImtype(),
                                "sqsj": datetime.now().strftime("%Y-%m-%d")
                            }
                        }
                        userdata.append(data)
                        sg.bucketSet("dd_hqcsh", self.user, f"{userdata}")
                        self.sender.reply("🔔登录成功!发送'车生活管理'对账号进行管理!")
                    else:
                        self.sender.reply("输入有误，退出！")
                        exit(0)

    def cx(self):
        tong = sg.bucketGet("dd_hqcsh", self.user)
        if tong == "" or tong == "[]":
            self.sender.reply("您当前没有提交账号！")
            exit(0)
        else:
            tong = _sg_literal(tong)
            msg = ""
            a = 0
            current_date = datetime.now().strftime("%Y-%m-%d")

            for user in tong:
                key = list(user.keys())
                bz = key[a]
                if user[key[a - 1]].get("qd", None) is None:
                    user[bz] = {'ck': user[key[a - 1]]['ck'], "qd": self.sender.getImtype(),
                                'sqsj': user[key[a - 1]]["sqsj"]}
                    sg.bucketSet("dd_hqcsh", self.user, f"{tong}")

                ck = user[key[a - 1]]['ck']
                auth_date = user[key[a - 1]]['sqsj']

                if len(ck.split('#')) != 1:
                    ck = user[key[a - 1]]['ck'].split('#')[0]

                if auth_date <= current_date:
                    msg += f"备注：{bz}\n授权状态：已过期 ⚠️\n授权到期：{auth_date}\n======================\n"
                    continue

                if self.login(ck):
                    msg += f"备注：{bz}\n今日积分：{self.today(ck)}\n总积分：{self.point}\n授权状态：有效 ✅\n授权到期：{auth_date}\n======================\n"
                else:
                    msg += f"车生活账号{bz}失效，请及时更新CK\n--------\n"
            self.sender.reply(f"========车生活查询========\n{msg}")
            exit(0)

    def gl(self):
        tong = sg.bucketGet("dd_hqcsh", self.user)
        if tong == "" or tong == "[]":
            self.sender.reply("您当前没有提交账号！")
            exit(0)
        else:
            msg = f"======车生活管理======\n"
            d = _sg_literal(tong)
            account_map = {}  # 用于存储序号到账号信息的映射

            for i, user_data in enumerate(d, 1):  # 从1开始编号
                for bz, info in user_data.items():
                    msg += f"账号[{i}]：{bz}\n"
                    account_map[str(i)] = {
                        "bz": bz,
                        "ck": info["ck"],
                        "sqsj": info["sqsj"],
                        "index": i-1  # 保存原始索引
                    }

            self.sender.reply(f"{msg}\n\n请输入序号进行操作！---q退出")
            index = self.sender.listen(180000)

            if index == "q":
                self.sender.reply("退出！")
                exit(0)

            if index not in account_map:
                self.sender.reply("输入的序号不存在")
                exit(0)

            selected_account = account_map[index]
            self.bz = selected_account["bz"]
            self.ck = selected_account["ck"]
            self.sqsj = selected_account["sqsj"]

            if self.login(self.ck):
                msg = f"======车生活管理======\n账号：{self.bz}\n1、账号授权\n2、提交青龙\n3、删除账号\n====================\n回复序号,退出【q】！"
                self.sender.reply(msg)
                cz = self.sender.listen(120000)

                if cz == "q":
                    self.sender.reply("退出")
                    exit(0)
                elif cz == "1":
                    try:
                        if '2099-12-31' == "" or '2099-12-31' == "":
                            self.sender.reply(f"插件配参不完整，请管理员发送【车生活配置】设置授权金额")
                            exit(0)

                        if '2099-12-31' == "true":
                            userjf = sg.bucketGet('bd_jf', self.user)
                            if userjf == "":
                                userjf = 0

                        self.dssq(2, selected_account["index"])
                        ds = self.sender.listen(120000)
                        if ds == "q":
                            self.sender.reply("退出")
                            exit(0)

                    except Exception as e:
                        self.sender.reply(f"授权处理异常: {str(e)}")
                        exit(0)
                elif cz == "2":
                    ql_config = sg.bucketGet("dd_hqcsh", "Qinglong")
                    if ql_config:
                        ql_params = ql_config.split('丨')
                        if len(ql_params) == 3:
                            QLurl = ql_params[0]
                            ClientID = ql_params[1]
                            ClientSecret = ql_params[2]

                            osname = sg.bucketGet("dd_hqcsh", "osname")
                            if osname:
                                try:
                                    url = f'{QLurl}/open/auth/token?client_id={ClientID}&client_secret={ClientSecret}'
                                    token_res = requests.get(url).json()
                                    if token_res['code'] == 200:
                                        qltoken = token_res['data']['token']

                                        url = f"{QLurl}/open/envs"
                                        headers = {
                                            "Authorization": "Bearer" + ' ' + qltoken,
                                            "Content-Type": "application/json"
                                        }
                                        data = [{
                                            "value": self.ck,
                                            "name": osname,
                                            "remarks": f'车生活账号:{self.bz}丨用户:{self.user}'
                                        }]
                                        res = requests.post(url, headers=headers, json=data)
                                        if res.status_code == 200:
                                            self.sender.reply("✅变量已提交到青龙")
                                        else:
                                            self.sender.reply("❌提交青龙失败")
                                except Exception as e:
                                    self.sender.reply(f"提交青龙异常:{str(e)}")

                    msg = f'【好奇车生活】当前用户: {self.user}\n授权天数: {int(self.sqsj)}天\n到期时间: {self.sqsj}'
                    self.sender.reply(msg)
                    notify = sg.bucketGet('dd_hqcsh', 'notify')
                    if notify:
                        tsqd = notify.split(',')
                        sg.notifyMasters(msg, tsqd)

                elif cz == "3":
                    self.sc(selected_account["index"])
                else:
                    self.sender.reply("输入错误")
                    exit(0)
            else:
                self.sender.reply(f"[{self.bz}]账号失效")
                exit(0)

    def sc(self, index):
        """删除账号"""
        tong = sg.bucketGet("dd_hqcsh", self.user)
        if tong == "":
            self.sender.reply("当前没有账号")
            exit(0)
        else:
            self.sender.reply(f"确定删除【{self.bz}】，确定发送【y】\n退出【q】！")
            qd = self.sender.listen(120000)
            if qd == "q":
                self.sender.reply("取消")
                exit(0)
            elif qd == "y":
                try:
                    ql_config = sg.bucketGet("dd_hqcsh", "Qinglong")
                    if ql_config:
                        ql_params = ql_config.split('丨')
                        if len(ql_params) == 3:
                            QLurl = ql_params[0]
                            ClientID = ql_params[1]
                            ClientSecret = ql_params[2]

                            osname = sg.bucketGet("dd_hqcsh", "osname")
                            if osname:
                                url = f'{QLurl}/open/auth/token?client_id={ClientID}&client_secret={ClientSecret}'
                                token_res = requests.get(url).json()
                                if token_res['code'] == 200:
                                    qltoken = token_res['data']['token']

                                    url = f"{QLurl}/open/envs"
                                    headers = {
                                        "Authorization": "Bearer" + ' ' + qltoken
                                    }
                                    res = requests.get(url, headers=headers).json()

                                    if res['code'] == 200:
                                        for env in res['data']:
                                            if env['name'] == osname and f'车生活账号:{self.bz}丨用户:{self.user}' in env['remarks']:
                                                del_url = f"{QLurl}/open/envs"
                                                headers = {
                                                    "Authorization": "Bearer" + ' ' + qltoken,
                                                    "Content-Type": "application/json"
                                                }
                                                del_data = [env['id']]
                                                requests.delete(del_url, headers=headers, json=del_data)
                                                msg = f"已删除青龙变量\n"
                                                break
                except Exception as e:
                    msg = f"删除青龙变量异常:{str(e)}\n"

                tong = _sg_literal(tong)
                del tong[index]
                sg.bucketSet("dd_hqcsh", self.user, f"{tong}")
                self.sender.reply(f"删除【{self.bz}】成功")
            else:
                self.sender.reply("输入错误")
                exit(0)

    def pz(self):
        if self.sender.isAdmin():
            zsm = sg.bucketGet('dd_hqcsh', 'zsm')
            if zsm == '':
                pz1 = '未配置'
            else:
                pz1 = '已配置'

            sqje = '2099-12-31'
            if sqje == '':
                sqje = 3

            sqsj = '2099-12-31'
            if sqsj == '':
                sqsj = 30

            msg = f'========车生活配置========\n1、赞赏码({pz1})\n2、授权金额({sqje}元)\n3、授权时间({sqsj}天)\n====================\n回复序号,退出【q】！'
            self.sender.reply(msg)
            zh = self.sender.listen(60000)
            if zh == 'q' or zh == 'Q':
                self.sender.reply("退出！")
            elif zh is None:
                self.sender.reply(f'超时退出！')
            elif zh == '1':
                self.sender.reply('请发送您的wx机器人赞赏码:')
                pz = self.sender.listen(60000)
                if pz == 'q' or pz == 'Q':
                    self.sender.reply("退出！")
                elif pz is None:
                    self.sender.reply(f'超时退出！')
                else:
                    self.sender.replyImage(pz)
                    sg.bucketSet('dd_hqcsh', 'zsm', f'{pz}')
                    self.sender.reply('赞赏码配置成功!')
            elif zh == '2':
                self.sender.reply('设置授权金额:')
                pz = self.sender.listen(60000)
                if pz == 'q' or pz == 'Q':
                    self.sender.reply("退出！")
                elif pz is None:
                    self.sender.reply(f'超时退出！')
                else:
                    True
                    self.sender.reply(f'授权金额配置成功: {pz}元')
            elif zh == '3':
                self.sender.reply('设置授权时间:')
                pz = self.sender.listen(60000)
                if pz == 'q' or pz == 'Q':
                    self.sender.reply("退出！")
                elif pz is None:
                    self.sender.reply(f'超时退出！')
                else:
                    True
                    self.sender.reply(f'授权时间配置成功: {pz}天')
            else:
                self.sender.reply(f'输入有误!!')
        else:
            self.sender.reply("不是管理员")
            exit(0)

    def sq(self):
        """车生活授权"""
        if self.sender.isAdmin():
            msg = f'========车生活授权========\n1、一键授权所有用户\n2、单独授权用户\n======================\n回复序号,退出【q】！'
            self.sender.reply(msg)
            xz = self.sender.listen(60000)

            if xz == 'q' or xz == 'Q':
                self.sender.reply("退出！")
                return
            elif xz is None:
                self.sender.reply(f'超时退出！')
                return
            elif xz == '1':
                self.qbqbsq()
            elif xz == '2':
                msg = f'请输入需要授权的账号id\n通过给机器人发送myuid获得\n退出【q】！'
                self.sender.reply(msg)
                myuid = self.sender.listen(60000)
                if myuid == 'q' or myuid == 'Q':
                    self.sender.reply("退出！")
                elif myuid == 1:
                    self.qbqbsq()
                elif myuid is None:
                    self.sender.reply(f'超时退出！')
                else:
                    ts = sg.bucketGet('dd_hqcsh', myuid)
                    if ts == '' or ts == '{}':
                        self.sender.reply(f"车生活系统未查询到{myuid}的信息! 请先上车! ")
                    else:
                        ts = _sg_literal(ts)
                        n = 0
                        id_dict = {}
                        msg = '========车生活授权========\n'
                        msg += '0、授权所有账号\n======================\n'
                        for user in ts:
                            for k, y in user.items():
                                n += 1
                                id_dict[n] = {'bz': k, 'ck': y['ck'], 'sqsj': y['sqsj']}
                                msg += f'{n}、{k}\n授权时间: ⏰{y["sqsj"]}\n======================\n'
                        msg += f'回复序号选择账号,退出【q】！'
                        self.sender.reply(msg)
                        xz = self.sender.listen(60000)
                        xz_list = []
                        for k, y in id_dict.items():
                            xz_list.append(k)
                        if xz == 'q' or xz == 'Q':
                            self.sender.reply("退出！")
                        elif xz is None:
                            self.sender.reply(f'超时退出！')
                        elif xz == '0':
                            msg = f'请输入给所有账号授权的天数！！\n回复序号,退出【q】！'
                            self.sender.reply(msg)
                            sjts = self.sender.listen(60000)
                            if sjts == 'q' or sjts == 'Q':
                                self.sender.reply("退出！")
                            elif sjts is None:
                                self.sender.reply(f'超时退出！')
                            elif isinstance(int(sjts), int):
                                success_count = 0
                                for user in ts:
                                    for k, y in user.items():
                                        try:
                                            dqsj = datetime.now().strftime("%Y-%m-%d")
                                            if y['sqsj'] > dqsj:
                                                sqsj = datetime.strptime(y['sqsj'], "%Y-%m-%d")
                                                new_sqsj = sqsj + timedelta(days=int(sjts))
                                            else:
                                                new_sqsj = datetime.now() + timedelta(days=int(sjts))
                                            new_sqsj = new_sqsj.strftime("%Y-%m-%d")
                                            user[k]['sqsj'] = new_sqsj
                                            success_count += 1
                                        except:
                                            continue
                                sg.bucketSet('dd_hqcsh', myuid, f'{ts}')
                                msg = f"授权完成!\n成功授权: {success_count}个账号\n授权天数: {sjts}天"
                                self.sender.reply(msg)
                                notify = sg.bucketGet('dd_hqcsh', 'notify')
                                if notify:
                                    tsqd = notify.split(',')
                                    sg.notifyMasters(msg, tsqd)
                            else:
                                self.sender.reply(f'输入天数有误，退出！')
                        elif int(xz) in xz_list:
                            zh = id_dict[int(xz)]
                            self.bz = zh['bz']
                            self.ck = zh['ck']
                            self.sqsj = zh['sqsj']

                            msg = f'请输入给【{self.bz}】授权的天数！！\n回复序号,退出【q】！'
                            self.sender.reply(msg)
                            sjts = self.sender.listen(60000)
                            if sjts == 'q' or sjts == 'Q':
                                self.sender.reply("退出！")
                            elif sjts is None:
                                self.sender.reply(f'超时退出！')
                            elif isinstance(int(sjts), int):
                                dqsj = datetime.now().strftime("%Y-%m-%d")
                                if self.sqsj > dqsj:
                                    sqsj1 = datetime.strptime(self.sqsj, "%Y-%m-%d")
                                    new_sqsj = sqsj1 + timedelta(days=int(sjts))
                                else:
                                    sj = datetime.now()
                                    new_sqsj = sj + timedelta(days=int(sjts))
                                new_sqsj = new_sqsj.strftime("%Y-%m-%d")
                                for user in ts:
                                    for k, y in user.items():
                                        if k == self.bz:
                                            user[k]['sqsj'] = new_sqsj
                                            break
                                sg.bucketSet('dd_hqcsh', myuid, f'{ts}')
                                msg = f'当前用户: {myuid}\n授权用户: {self.bz}\n授权天数: {int(sjts)}天\n到期时间: {new_sqsj}'
                                self.sender.reply(msg)
                                notify = sg.bucketGet('dd_hqcsh', 'notify')
                                if notify:
                                    tsqd = notify.split(',')
                                    sg.notifyMasters(msg, tsqd)
                            else:
                                self.sender.reply(f'{sjts} 输入有误，退出！')
                        else:
                            self.sender.reply(f'{xz} 输入有误，退出！')
            else:
                self.sender.reply("不是管理员")
                exit(0)

    def qbqbsq(self):
        """一键授权所有用户"""
        try:
            ts = sg.bucketAllKeys('dd_hqcsh')
            if not ts:
                self.sender.reply("车生活系统未查询到任何用户信息!")
                return

            user_keys = [key for key in ts if key not in ['zsm', 'sqje', 'sqsj', 'Qinglong', 'osname', 'notify', 'delbtn', 'jfpay']]

            if not user_keys:
                self.sender.reply("车生活系统未查询到任何用户信息!")
                return

            self.sender.reply('请输入要给所有用户授权的天数！\n退出【q】！')
            sjts = self.sender.listen(60000)
            if sjts == 'q' or sjts == 'Q':
                self.sender.reply("退出！")
                return
            elif sjts is None:
                self.sender.reply(f'超时退出！')
                return

            try:
                sjts = int(sjts)
            except:
                self.sender.reply(f'输入的天数无效，必须是数字！')
                return

            success_count = 0
            fail_count = 0

            for myuid in user_keys:
                try:
                    user_data = sg.bucketGet('dd_hqcsh', myuid)
                    if not user_data or user_data == '[]':
                        continue

                    user_data = _sg_literal(user_data)
                    if not isinstance(user_data, list):
                        continue

                    modified = False
                    for user in user_data:
                        if not isinstance(user, dict):
                            continue

                        for k, y in user.items():
                            try:
                                if not isinstance(y, dict) or 'sqsj' not in y:
                                    continue

                                dqsj = datetime.now().strftime("%Y-%m-%d")
                                if y['sqsj'] > dqsj:
                                    sqsj = datetime.strptime(y['sqsj'], "%Y-%m-%d")
                                    new_sqsj = sqsj + timedelta(days=sjts)
                                else:
                                    new_sqsj = datetime.now() + timedelta(days=sjts)
                                new_sqsj = new_sqsj.strftime("%Y-%m-%d")

                                y['sqsj'] = new_sqsj
                                modified = True
                                success_count += 1

                                ql_config = sg.bucketGet("dd_hqcsh", "Qinglong")
                                if ql_config:
                                    ql_params = ql_config.split('丨')
                                    if len(ql_params) == 3:
                                        QLurl = ql_params[0]
                                        ClientID = ql_params[1]
                                        ClientSecret = ql_params[2]

                                        osname = sg.bucketGet("dd_hqcsh", "osname")
                                        if osname:
                                            url = f'{QLurl}/open/auth/token?client_id={ClientID}&client_secret={ClientSecret}'
                                            token_res = requests.get(url).json()
                                            if token_res['code'] == 200:
                                                qltoken = token_res['data']['token']

                                                url = f"{QLurl}/open/envs"
                                                headers = {
                                                    "Authorization": "Bearer" + ' ' + qltoken,
                                                    "Content-Type": "application/json"
                                                }
                                                check_res = requests.get(url, headers=headers).json()

                                                env_exists = False
                                                env_id = None

                                                if check_res['code'] == 200:
                                                    for env in check_res['data']:
                                                        if env['name'] == osname and f'车生活账号:{k}丨用户:{myuid}' in env['remarks']:
                                                            env_exists = True
                                                            env_id = env['id']
                                                            break

                                                if env_exists:
                                                    update_data = {
                                                        "id": env_id,
                                                        "value": y['ck'],
                                                        "name": osname,
                                                        "remarks": f'车生活账号:{k}丨用户:{myuid}'
                                                    }
                                                    res = requests.put(url, headers=headers, json=update_data)
                                                else:
                                                    create_data = [{
                                                        "value": y['ck'],
                                                        "name": osname,
                                                        "remarks": f'车生活账号:{k}丨用户:{myuid}'
                                                    }]
                                                    res = requests.post(url, headers=headers, json=create_data)

                                                if res.status_code != 200:
                                                    self.sender.reply(f"账号[{k}]提交青龙失败: {res.text}")
                                                else:
                                                    if env_exists:
                                                        self.sender.reply(f"账号[{k}]青龙变量更新成功")
                                                    else:
                                                        self.sender.reply(f"账号[{k}]青龙变量添加成功")
                            except Exception as e:
                                self.sender.reply(f"账号[{k}]提交青龙异常:{str(e)}")
                                fail_count += 1
                                continue

                    if modified:
                        sg.bucketSet('dd_hqcsh', myuid, str(user_data))

                except:
                    fail_count += 1
                    continue

            msg = f"一键授权完成!\n成功授权: {success_count}个账号\n授权失败: {fail_count}个账号\n授权天数: {sjts}天\n已同步更新青龙变量"
            self.sender.reply(msg)

            notify = sg.bucketGet('dd_hqcsh', 'notify')
            if notify:
                tsqd = notify.split(',')
                sg.notifyMasters(msg, tsqd)

        except Exception as e:
            self.sender.reply(f'一键授权发生错误: {str(e)}')

    def dssq(self, type, index):
        """打赏授权"""
        if type == 2:
            try:
                try:
                    pay_status = '2099-12-31'
                    if pay_status and pay_status == "true":
                        self.sender.reply("🔔目前有其他用户正在付款，请稍后再试！！")
                        return
                    True
                except:
                    pass

                sqsj = '2099-12-31'
                sqje = '2099-12-31'
                if sqsj == '':
                    sqsj = 30
                if sqje == '':
                    sqje = 3

                if float(sqje) == 0:
                    dqsj = datetime.now().strftime("%Y-%m-%d")
                    if str(self.sqsj) > str(dqsj):
                        sqsj1 = datetime.strptime(str(self.sqsj), "%Y-%m-%d")
                        new_sqsj = sqsj1 + timedelta(days=int(sqsj))
                        new_sqsj = new_sqsj.strftime("%Y-%m-%d")
                    else:
                        sj = datetime.now()
                        new_sqsj = sj + timedelta(days=int(sqsj))
                        new_sqsj = new_sqsj.strftime("%Y-%m-%d")

                    ts = sg.bucketGet('dd_hqcsh', self.user)
                    ts = _sg_literal(ts)
                    for k, y in ts[index].items():
                        if self.bz == k:
                            b = {}
                            b[f'{k}'] = {'ck': self.ck, 'qd': y["qd"], 'sqsj': new_sqsj}
                            ts[index] = b
                            sg.bucketSet('dd_hqcsh', self.user, f'{ts}')

                            self.submit_to_qinglong(k)

                            msg = f'【好奇车生活】当前用户: {self.user}\n授权天数: {int(sqsj)}天\n到期时间: {new_sqsj}'
                            self.sender.reply(msg)
                            notify = sg.bucketGet('dd_hqcsh', 'notify')
                            if notify:
                                tsqd = notify.split(',')
                                sg.notifyMasters(msg, tsqd)
                            True
                            return

                zsm = sg.bucketGet('dd_hqcsh', 'zsm')
                if zsm == '':
                    self.sender.reply('管理员还未配置二维码!')
                    True
                    return

                self.sender.replyImage(zsm)
                self.sender.reply(
                    f"请在120s内使用wx扫码付款\n每付款{sqje}元授权时间增加{sqsj}天!\n发起支付期间不要发其他无关内容！退出回复'q'退出！")
                waitPay = False
                True

                if waitPay == 'q':
                    self.sender.reply("退出付款！")
                elif isinstance(waitPay, dict) or isinstance(waitPay, str):
                    if isinstance(waitPay, str):
                        waitPay = json.loads(waitPay)
                    Time = waitPay['Time']
                    userName = waitPay['FromName']
                    Money = waitPay['Money']
                    waitPay['Type']
                    dqsj = datetime.now().strftime("%Y-%m-%d")
                    if str(self.sqsj) > str(dqsj):
                        sqsj1 = datetime.strptime(str(self.sqsj), "%Y-%m-%d")
                        new_sqsj = sqsj1 + timedelta(days=int(float(Money) / float(sqje) * int(sqsj)))
                        new_sqsj = new_sqsj.strftime("%Y-%m-%d")
                    else:
                        sj = datetime.now()
                        new_sqsj = sj + timedelta(days=int(float(Money) / float(sqje) * int(sqsj)))
                        new_sqsj = new_sqsj.strftime("%Y-%m-%d")
                    ts = sg.bucketGet('dd_hqcsh', self.user)
                    ts = _sg_literal(ts)
                    for k, y in ts[index].items():
                        if self.bz == k:
                            b = {}
                            b[f'{k}'] = {'ck': self.ck, 'qd': y["qd"], 'sqsj': new_sqsj}
                            ts[index] = b
                            sg.bucketSet('dd_hqcsh', self.user, f'{ts}')

                            ql_config = sg.bucketGet("dd_hqcsh", "Qinglong")
                            if ql_config:
                                ql_params = ql_config.split('丨')
                                if len(ql_params) == 3:
                                    QLurl = ql_params[0]
                                    ClientID = ql_params[1]
                                    ClientSecret = ql_params[2]

                                    osname = sg.bucketGet("dd_hqcsh", "osname")
                                    if osname:
                                        try:
                                            url = f'{QLurl}/open/auth/token?client_id={ClientID}&client_secret={ClientSecret}'
                                            token_res = requests.get(url).json()
                                            if token_res['code'] == 200:
                                                qltoken = token_res['data']['token']

                                                url = f"{QLurl}/open/envs"
                                                headers = {
                                                    "Authorization": "Bearer" + ' ' + qltoken,
                                                    "Content-Type": "application/json"
                                                }
                                                data = [{
                                                    "value": self.ck,
                                                    "name": osname,
                                                    "remarks": f'车生活账号:{k}丨用户:{self.user}'
                                                }]
                                                res = requests.post(url, headers=headers, json=data)
                                                if res.status_code == 200:
                                                    self.sender.reply("✅变量已提交到青龙")
                                                else:
                                                    self.sender.reply("❌提交青龙失败")
                                        except Exception as e:
                                            self.sender.reply(f"提交青龙异常:{str(e)}")

                            msg = f'【好奇车生活】当前用户: {userName}\n付款: {float(Money)}\n付款渠道：{self.sender.getImtype().upper()}\n授权id: {self.user}\n付款时间: {Time}\n授权天数: {int(float(Money) / float(sqje) * int(sqsj))}天\n到期时间: {new_sqsj}'
                            self.sender.reply(msg)
                            notify = sg.bucketGet('dd_hqcsh', 'notify')
                            if notify:
                                tsqd = notify.split(',')
                                sg.notifyMasters(msg, tsqd)
                            return

                self.submit_to_qinglong(k)

            except Exception as e:
                True
                self.sender.reply(f"{e}或者超时了！")

        else:
            jf = sg.bucketGet("bd_jf", self.user)
            zsm = sg.bucketGet('dd_hqcsh', 'zsm')
            sqsj = '2099-12-31'
            sqje = '2099-12-31'
            if sqsj == '':
                sqsj = 30
            if sqje == '':
                sqje = 3
            dqsj = str(datetime.now().strftime("%Y-%m-%d"))
            if int(jf) >= int(float(sqje) * 100):
                if str(self.sqsj) > dqsj:
                    self.sqsj = datetime.strptime(str(self.sqsj), "%Y-%m-%d")
                    new_sqsj = self.sqsj + timedelta(days=int(sqsj))
                    new_sqsj = new_sqsj.strftime("%Y-%m-%d")

                else:
                    sj = datetime.now()
                    new_sqsj = sj + timedelta(days=int(sqsj))
                    new_sqsj = new_sqsj.strftime("%Y-%m-%d")

                ts = sg.bucketGet('dd_hqcsh', self.user)
                ts = _sg_literal(ts)

                for k, y in ts[index].items():
                    if self.bz == k:
                        a = {}
                        a[f'{k}'] = {'ck': self.ck, 'sqsj': new_sqsj}
                        ts[index] = a
                        sg.bucketSet('dd_hqcsh', self.user, f'{ts}')
                        ql_config = sg.bucketGet("dd_hqcsh", "Qinglong")
                        if ql_config:
                            ql_params = ql_config.split('丨')
                            if len(ql_params) == 3:
                                QLurl = ql_params[0]
                                ClientID = ql_params[1]
                                ClientSecret = ql_params[2]

                                osname = sg.bucketGet("dd_hqcsh", "osname")
                                if osname:
                                    try:
                                        url = f'{QLurl}/open/auth/token?client_id={ClientID}&client_secret={ClientSecret}'
                                        token_res = requests.get(url).json()
                                        if token_res['code'] == 200:
                                            qltoken = token_res['data']['token']

                                            url = f"{QLurl}/open/envs"
                                            headers = {
                                                "Authorization": "Bearer" + ' ' + qltoken,
                                                "Content-Type": "application/json"
                                            }
                                            data = [{
                                                "value": self.ck,
                                                "name": osname,
                                                "remarks": f'车生活账号:{k}丨用户:{self.user}'
                                            }]
                                            res = requests.post(url, headers=headers, json=data)
                                            if res.status_code == 200:
                                                self.sender.reply("✅变量已提交到青龙")
                                            else:
                                                self.sender.reply("❌提交青龙失败")
                                    except Exception as e:
                                        self.sender.reply(f"提交青龙异常:{str(e)}")

                    msg = f'【好奇车生活】当前用户: {self.user}\n付款积分: {int(float(sqje) * 100)}\n付款渠道：{self.sender.getImtype().upper()}\n付款时间：{datetime.now()}\n授权id: {self.user}\n授权天数: {int(sqsj)}天\n到期时间: {new_sqsj}'
                    self.sender.reply(msg)
                    notify = sg.bucketGet('dd_hqcsh', 'notify')
                    if notify == '':
                        pass
                    else:
                        tsqd = notify.split(',')
                        sg.notifyMasters(msg, tsqd)
                    exit(0)
            else:
                self.sender.reply("积分不足，退出")
                exit(0)

    def jc(self):
        msg = f"抓包：车生活小程序\n域名：https://channel.cheryfs.cn/下请求头里面的accountId数据\n说明：一天50积分左右，月积分2000+，可以抢购兑换ek或者现金\n上车指令: 车生活上车\n管理指令: 车生活管理\n查询指令: 车生活查询\n入口指令: 车生活入口"
        self.sender.reply(msg)

    def rk(self):
        msg = "http://mcg888.yy2088.cn:18080/admin/images/gallery/1736328296136190264.jpg"
        self.sender.replyImage(msg)

    def QLtoken(self, QLurl, ClientID, ClientSecret):  # 获取青龙token
        try:
            url = f'{QLurl}/open/auth/token?client_id={ClientID}&client_secret={ClientSecret}'
            A = requests.get(url)
            if "token" in A.text:
                ql = A.content
                qlrequests = json.loads(ql)
                qltoken = qlrequests['data']['token']
                return qltoken
            else:
                self.sender.reply('链接青龙失败,请检查青龙配参！')
                exit(0)
        except Exception:
            self.sender.reply("链接青龙失败,请检查青龙配参！")
            exit(0)

    def Addenvs(self, QLurl, qltoken, osname, value, account):  # 添加青龙变量
        try:
            qlurl = f"{QLurl}/open/envs"
            data = [{
                "value": value,
                "name": osname,
                "remarks": f'车生活账号:{account}丨用户:{self.user}'
            }]
            headers = {
                "Authorization": "Bearer" + ' ' + qltoken,
                "accept": "application/json",
                "Content-Type": "application/json",
            }
            r = requests.post(qlurl, headers=headers, data=json.dumps(data))
            if "value must be unique" in r.text:
                return
            else:
                qlid = r.json()['data'][0]['id']
                return qlid
        except Exception:
            self.sender.reply("添加青龙变量错误,请稍后重试")
            exit(0)

    def submit_to_qinglong(self, account_name):
        """提交变量到青龙"""
        tong = sg.bucketGet("dd_hqcsh", self.user)
        if tong:
            tong = _sg_literal(tong)
            current_date = datetime.now().strftime("%Y-%m-%d")
            is_authorized = False

            for user in tong:
                for bz, info in user.items():
                    if bz == account_name:
                        if info['sqsj'] > current_date:
                            is_authorized = True
                        break

            if not is_authorized:
                self.sender.reply("❌账号未授权或授权已过期，无法提交到青龙")
                return

        ql_config = sg.bucketGet("dd_hqcsh", "Qinglong")
        if ql_config:
            ql_params = ql_config.split('丨')
            if len(ql_params) == 3:
                QLurl = ql_params[0]
                ClientID = ql_params[1]
                ClientSecret = ql_params[2]

                osname = sg.bucketGet("dd_hqcsh", "osname")
                if osname:
                    try:
                        url = f'{QLurl}/open/auth/token?client_id={ClientID}&client_secret={ClientSecret}'
                        token_res = requests.get(url).json()
                        if token_res['code'] == 200:
                            qltoken = token_res['data']['token']

                            url = f"{QLurl}/open/envs"
                            headers = {
                                "Authorization": "Bearer" + ' ' + qltoken,
                                "Content-Type": "application/json"
                            }
                            data = [{
                                "value": self.ck,
                                "name": osname,
                                "remarks": f'车生活账号:{account_name}丨用户:{self.user}'
                            }]
                            res = requests.post(url, headers=headers, json=data)
                            if res.status_code == 200:
                                self.sender.reply("✅变量已提交到青龙")
                            else:
                                self.sender.reply("❌提交青龙失败")
                    except Exception as e:
                        self.sender.reply(f"提交青龙异常:{str(e)}")
                else:
                    self.sender.reply("❌未配置变量名")
            else:
                self.sender.reply("❌青龙配置格式错误")
        else:
            self.sender.reply("❌未配置青龙参数")

    def check_auth(self):
        return True


if __name__ == "__main__":
    name = "好奇车生活"
    senderID = sg.getSenderID()
    sender = sg.Sender(senderID)
    user = sender.getUserID()
    JD = JD(user, sender)
    message = sender.getMessage()

    if "上车" in message:
        JD.tj()
    elif "管理" in message:
        JD.gl()
    elif "查询" in message:
        JD.cx()
    elif "配置" in message:
        JD.pz()
    elif "授权" in message:
        JD.sq()
    elif "教程" in message:
        JD.jc()
    elif "入口" in message:
        JD.rk()
    elif "检测" in message:
        JD.check_auth()
    elif '车生活版本'in message:
        if sender.isAdmin():
            sender.reply(
                f"🔔当前版本V7.8\n======================\n用户指令:\n上车指令: 车生活上车\n管理指令: 车生活管理\n查询指令: 车生活查询\n入口指令：车生活入口\n教程指令：车生活教程\n检测指令：车生活检测\n======================\n管理员指令:\n插件配置: 车生活配置\n账号授权: 车生活授权\n======================")
