# [title: 沪上阿姨]
# [name: huShangAYi]
# [language: python]
# [class: 任务]
# [author: mrconli]
# [version: v1.0.2]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^沪上(.*)|(.*)沪上$]
# [cron: 46 7 * * *]
# [icon: https://api.iconify.design/lucide:apple.svg]
# [description: 微信小程序-沪上阿姨，每日签到；指令：沪上(登录|登陆|上车|提交)、沪上查询、沪上管理；触发指令【沪上】你可以改成自己喜欢的文字；需要在计划任务添加 定时指令【沪上运行】 启用自处理 伪装管理员]
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
    'mrconli_hsay_notify': form.string().title('管理员通知').default('').description('如 qq,wx,tg 用英文“,”符号分割,不设默认qq'),
    'mrconli_hsay_yxbf': form.string().title('运行并发数').default('').description('并发阅读多少号，任务并发非抢购,默认5'),
    'mrconli_hsay_proxy': form.string().title('代理api').default('').description('号多或者报错才加代理，不加留空即可'),
})
_CONFIG_FIELD_MAP = {
    ('mrconli_hsay', 'notify'): 'mrconli_hsay_notify',
    ('mrconli_hsay', 'yxbf'): 'mrconli_hsay_yxbf',
    ('mrconli_hsay', 'proxy'): 'mrconli_hsay_proxy',
}

import requests, time, json, re
from datetime import datetime

try:
    import concurrent.futures
except:
    senderID = sg.getSenderID()
    sender = sg.Sender(senderID)
    sender.reply("请安装concurrent依赖，可用订阅里面的插件安装")
    exit(0)

def get_ip(url,ts):
    try:
        res = requests.get(url)
        if res.status_code == 200 and "白名单" not in res.text:
            print(f"获取到ip---{res.text}")
            proxy = {
                "https":f"http://{res.text}",
                "http":f"http://{res.text}"
            }
            return proxy
        elif "白名单" in res.text:
            print(res.text)
            sg.notifyMasters(f"[沪上阿姨代理异常通知]{res.text}",ts)
        else:
            return ""
    except:
        return ""

class LT:
    def __init__(self, user, sender):
        self.user = user
        self.sender = sender
        self.tongname = "mrconli_hsay_token"
        self.tongconfig = "mrconli_hsay"
        self.xwid = None
        self.dlapi = sg.bucketGet(self.tongconfig,"proxy")
        ts = sg.bucketGet(self.tongconfig,"notify")
        if ts == "":
            self.ts = f'{["qq"]}'
        else:
            self.ts = ts.split(",")
        self.msg = ""
        self.userts = ""
        self.erro_msg = ""
    def login(self,ck):
        url = "https://webapi.qmai.cn/web/catering/crm/personal-info?appid=wxd92a2d29f8022f40"
        headers = {
            "Host": "webapi.qmai.cn",
            "Connection": "keep-alive",
            "promotion-code": "",
            "work-wechat-userid": "",
            "store-id": "201424",
            "Accept-Language": "zh-CN",
            "work-staff-id": "",
            "scene": "1178",
            "Qm-From-Type": "catering",
            "multi-store-id": "60808",
            "Qm-User-Token": ck,
            "work-staff-name": "",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090b11) XWEB/9129",
            "qz-gtd": "",
            "Qm-From": "wechat",
            "Content-Type": "application/json",
            "Accept": "v=1.0",
            "channelCode": "",
            "xweb_xhr": "1",
            "gdt-vid": "",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://servicewechat.com/wxd92a2d29f8022f40/314/page-frame.html",
            "Accept-Encoding": "gzip, deflate, br"
        }
        res = requests.get(url, headers=headers).json()
        if res["code"] == "0":
            phone = res["data"]["mobilePhone"]
            return phone
        else:
            return False


    def card(self, ck):
        url = "https://webapi.qmai.cn/web/catering/crm/coupon/list"
        headers = {
            "Host": "webapi.qmai.cn",
            "Connection": "keep-alive",
            "store-id": "201424",
            "Accept-Language": "zh-CN",
            "scene": "1256",
            "Qm-From-Type": "catering",
            "multi-store-id": "60808",
            "Qm-User-Token": ck,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B)",
            "Content-Type": "application/json",
            "Accept": "v=1.0",
        }

        data = {
            "pageNo": 1,
            "pageSize": 50,
            "useStatus": 0,
            "appid": "wxd92a2d29f8022f40"
        }

        try:
            if self.dlapi != "":
                proxy = get_ip(self.dlapi, self.ts)
                res = requests.post(url, headers=headers, json=data, proxies=proxy, timeout=10)
            else:
                res = requests.post(url, headers=headers, json=data, timeout=10)

            res_json = res.json()

            if res_json["code"] == "0" and "data" in res_json:
                coupons = res_json["data"].get("data", [])
                msg = ""
                for i in coupons:
                    expire_time = i.get("endAt", "未知")
                    title = i.get("title", "未知券名")
                    msg += f"[{title}] 过期时间: {expire_time}\n"

                total = res_json["data"].get("total", 0)
                return total, msg
            else:
                return 0, f"查询失败: {res_json.get('message', '未知错误')}"

        except Exception as e:
            print(f"优惠券查询异常: {str(e)}")
            return 0, f"查询异常: {str(e)}"

    def daycoin(self,ck):
        url = "https://webapi.qmai.cn/web/catering/crm/points-info"
        headers = {
            "Host": "webapi.qmai.cn",
            "Connection": "keep-alive",
            "Content-Length": "30",
            "promotion-code": "",
            "work-wechat-userid": "",
            "store-id": "201424",
            "Accept-Language": "zh-CN",
            "work-staff-id": "",
            "scene": "1178",
            "Qm-From-Type": "catering",
            "multi-store-id": "60808",
            "Qm-User-Token": ck,
            "work-staff-name": "",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090b11) XWEB/9129",
            "qz-gtd": "",
            "Qm-From": "wechat",
            "Content-Type": "application/json",
            "Accept": "v=1.0",
            "channelCode": "",
            "xweb_xhr": "1",
            "gdt-vid": "",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://servicewechat.com/wxd92a2d29f8022f40/314/page-frame.html",
            "Accept-Encoding": "gzip, deflate, br"
        }
        data = {"appid":"wxd92a2d29f8022f40"}
        res = requests.post(url, headers=headers,json=data).json()
        if res["code"] == "0":
            coins = res["data"]["totalPoints"]
            return coins
        else:
            return 0

    def sign(self,phone,ck):
        url = "https://webapi.qmai.cn/web/cmk-center/sign/takePartInSign"
        headers = {
            "Host": "webapi.qmai.cn",
            "Connection": "keep-alive",
            "Content-Length": "65",
            "Qm-From": "wechat",
            "Accept": "v=1.0",
            "Qm-User-Token": ck,
            "xweb_xhr": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090b11) XWEB/9129",
            "Qm-From-Type": "catering",
            "Content-Type": "application/json",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://servicewechat.com/wxd92a2d29f8022f40/314/page-frame.html",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }
        data = {"activityId":"1004435002421583872","appid":"wxd92a2d29f8022f40"}
        try:
            time.sleep(1.5)
            res = requests.post(url,headers=headers,data=json.dumps(data)).json()
            if res["status"]:
                for i in res["data"]["rewardDetailList"]:
                    if i["rewardName"] == "积分奖励":
                        self.msg += f"{phone[:3]}***{phone[7:]}:获得积分{i['sendNum']}\n"
                        return f"获得积分{i['sendNum']}"
                    else:
                        self.msg += f'{phone[:3]}***{phone[7:]}:获得{res["data"]["rewardDetailList"][0]["rewardName"]}\n'
                        try:
                            sg.push(self.userts,"",self.user,"沪上阿姨",f"[沪上阿姨]领取签到奖励：{phone}---"+res["data"]["rewardDetailList"][0]["rewardShowExtra"]["expiredDateStr"])
                        except:
                            print("领取错误")
                        return res["data"]["rewardDetailList"][0]["rewardName"]
            elif res["code"] == 0 and "已签到" in res["message"]:
                self.msg += f"{phone[:3]}***{phone[7:]}:已签到\n"
                return True
            else:
                self.msg += f"{phone[:3]}***{phone[7:]}:异常，可能过期\n"
                return False
        except Exception as e:
            try:
                if self.dlapi != "":
                    proxy = get_ip(self.dlapi,self.ts)
                else:
                    proxy = ""
                res = requests.post(url, headers=headers, data=json.dumps(data), proxies=proxy).json()
                if res["status"]:
                    for i in res["data"]["rewardDetailList"]:
                        if i["rewardName"] == "积分奖励":
                            self.msg += f"{phone[:3]}***{phone[7:]}:获得积分{i['sendNum']}\n"
                            return f"获得积分{i['sendNum']}"
                        else:
                            self.msg += f'{phone[:3]}***{phone[7:]}:获得{res["data"]["rewardDetailList"][0]["rewardName"]}\n'
                            try:
                                sg.push(self.userts, "", self.user, "沪上阿姨", f"[沪上阿姨]领取签到奖励：{phone}---" +
                                                res["data"]["rewardDetailList"])
                            except:
                                print("领取错误")
                            return res["data"]["rewardDetailList"][0]["rewardName"]
                elif res["code"] == 0 and "已签到" in res["message"]:
                    self.msg += f"{phone[:3]}***{phone[7:]}:已签到\n"
                    return True
                else:
                    self.msg += f"{phone[:3]}***{phone[7:]}:异常，可能过期\n"
                    return False
            except:
                print(f"{phone}异常{e}")
                self.erro_msg += f"{phone[:3]}***{phone[7:]}签到异常（代理）\n"


    def signnum(self, ck):
        url = "https://webapi.qmai.cn/web/cmk-center/sign/userSignStatistics"
        headers = {
            "Host": "webapi.qmai.cn",
            "Connection": "keep-alive",
            "store-id": "201424",
            "Accept-Language": "zh-CN",
            "scene": "1256",
            "Qm-From-Type": "catering",
            "multi-store-id": "60808",
            "Qm-User-Token": ck,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B)",
            "Content-Type": "application/json",
            "Accept": "v=1.0",
        }

        data = {
            "activityId": "1004435002421583872",
            "appid": "wxd92a2d29f8022f40"
        }

        try:
            if self.dlapi != "":
                proxy = get_ip(self.dlapi, self.ts)
                res = requests.post(url, headers=headers, json=data, proxies=proxy, timeout=10)
            else:
                res = requests.post(url, headers=headers, json=data, timeout=10)

            res_json = res.json()

            if res_json.get("status") and "data" in res_json:
                signs = res_json["data"].get("signDays", 0)
                next_reward = "暂无"

                if res_json["data"].get("nextRewardList"):
                    next_rewards = res_json["data"]["nextRewardList"][0].get("rewardList", [])
                    if next_rewards:
                        next_days = res_json["data"].get("nextSignDays", 0)
                        next_reward = f'{next_rewards[0]["rewardName"]}差{next_days}天'
                return signs, next_reward
            else:
                print(f"签到统计响应异常: {res_json}")
                return 0, "获取失败"

        except Exception as e:
            print(f"签到统计异常: {str(e)}")
            return 0, f"查询异常: {str(e)}"

    def tj(self):
        tong = sg.bucketGet(self.tongname, self.user)
        self.sender.reply(
            f"【沪上阿姨】请发送小程序抓的Qm-User-Token\n---按q退出")
        token = self.sender.listen(180000)
        if token == "q" or token == "":
            self.sender.reply("退出")
            exit(0)
        else:
            if self.login(token):
                phone = self.login(token)
                if tong == "":
                    t = []
                    d = {}
                    d[phone] = {
                        "token":token,
                        "qd": self.sender.getImtype(),
                        "sqsj": datetime.now().strftime("%Y-%m-%d")
                    }
                    t.append(d)
                    sg.bucketSet(self.tongname, self.user, f"{t}")
                    self.sender.reply(f"账号{phone[:3]}***{phone[7:]}提交成功，发送【沪上查询】查看")
                    exit(0)
                else:
                    tong1 = _sg_literal(tong)
                    for t in tong1:
                        for k, y in t.items():
                            if k == phone:
                                t[k] = {
                                    "token": token,
                                    "qd": self.sender.getImtype(),
                                    "sqsj": datetime.now().strftime("%Y-%m-%d")
                                }
                                sg.bucketSet(self.tongname,self.user,f"{tong1}")
                                self.sender.reply(f"{phone[:3]}***{phone[7:]}更新成功")
                                exit(0)
                    d = {}
                    d[phone] = {
                        "token": token,
                        "qd": self.sender.getImtype(),
                        "sqsj": datetime.now().strftime("%Y-%m-%d")
                    }
                    tong1.append(d)
                    sg.bucketSet(self.tongname, self.user, f"{tong1}")
                    self.sender.reply(f"账号{phone[:3]}***{phone[7:]}提交成功，发送【沪上查询】查看")
                    exit(0)
            else:
                self.sender.reply("token错误或失效，退出")
                exit(0)


    def cx(self):
        tong = sg.bucketGet(self.tongname, self.user)
        if tong == "":
            self.sender.reply("当前没有账号")
            exit(0)
        else:
            tong1 = _sg_literal(tong)
            msg = ""
            for sj in tong1:
                for k,y in sj.items():
                    ck = y["token"]
                    self.userts = y["qd"]
                    phone = k
                    if self.login(ck):
                        if self.sign(phone,ck):
                            qd = "✅"
                        else:
                            qd = "❎"
                        try:
                            num,card = self.card(ck)
                        except:
                            num,card = None,None
                        try:
                            if self.signnum(ck):
                                signs,next = self.signnum(ck)
                            else:
                                signs,next = "",""
                        except:
                            signs, next = "", ""
                        msg += f"📱手机号：{phone[:3]}***{phone[7:]}\n👛当前积分：{self.daycoin(ck)}\n📒累计签到：{signs}天\n🏷️签到状态：{qd}\n🚩目标：{next}\n🎫优惠券数量：{num}\n---------------------------\n"
                    else:
                        msg += f"【登陆失败】\n📱手机号：{phone[:3]}***{phone[7:]}token失效\n------------------------\n"
                    time.sleep(1)
            self.sender.reply(f"=======沪上查询=======\n{msg}\n🔔更多操作发送【沪上管理】")
            exit(0)

    def gl(self):
        tong = sg.bucketGet(self.tongname, self.user)
        if tong == "":
            self.sender.reply("当前没有账号")
            exit(0)
        else:
            try:
                tong1 = _sg_literal(tong)
                msg = ""
                a = 1
                for sj in tong1:
                    for k, y in sj.items():
                        ck = y["token"]
                        phone = k
                        if self.login(ck):
                            msg += f"[{a}]:{phone[:3]}***{phone[7:]}\n"
                            a += 1
                        else:
                            msg += f"【登陆失败】\n📱手机号：{phone[:3]}***{phone[7:]}token失效\n------\n"

                self.sender.reply(f"=======沪上管理=======\n{msg}\n------------------------\n👉请发送数字序号，发送q退出")
                index = self.sender.listen(180000)

                if not index.isdigit():
                    self.sender.reply("请输入正确的数字序号")
                    exit(0)

                index = int(index)
                if index <= 0 or index > len(tong1):
                    self.sender.reply("序号超出范围")
                    exit(0)

                index = index - 1
                msg = ""

                curr_account = list(tong1[index].items())[0]
                k, y = curr_account

                ck = y["token"]
                self.userts = y["qd"]

                if self.login(ck):
                    if self.sign(k,ck):
                        qd = "✅"
                    else:
                        qd = "❎"
                    try:
                        num,card = self.card(ck)
                    except:
                        num,card = 0,"获取失败"

                    msg += f"\n📱手机号：{k[:3]}***{k[7:]}\n👛当前积分：{self.daycoin(ck)}\n🏷️签到状态：{qd}\n🎫优惠券数量：{num}\n------------------------\n"
                else:
                    msg += f"📱手机号：{k[:3]}***{k[7:]}token失效\n------------------------\n"

                self.sender.reply(f"=======沪上管理=======\n{msg}1. 查看优惠券\n2. 删除账号\n\n👉请发送数字序号，发送q退出")
                choice = self.sender.listen(180000)
                if choice == "q" or choice == "":
                    self.sender.reply("退出")
                    exit(0)
                elif choice == "1":
                    try:
                        num, card = self.card(ck)
                        self.sender.reply(f"=======优惠券列表=======\n{card}")
                    except Exception as e:
                        self.sender.reply(f"获取优惠券失败:{str(e)}")
                elif choice == "2":
                    self.sc(index)
                else:
                    self.sender.reply("输入错误，退出")
                    exit(0)
            except Exception as e:
                self.sender.reply(f"操作异常:{str(e)}")
                exit(0)

    def sc(self, index):
        self.sender.reply(f"是否删除账号，y/n。\n---n退出")
        y = self.sender.listen(180000)
        if y == "n" or y == "":
            self.sender.reply("退出")
            exit(0)
        elif "y" == y:
            tong1 = _sg_literal(sg.bucketGet(self.tongname, self.user))
            del tong1[index]
            sg.bucketSet(self.tongname, self.user, f"{tong1}")
            if sg.bucketGet(self.tongname, self.user) == "[]":
                sg.bucketDel(self.tongname, self.user)
            self.sender.reply("删除成功，拜拜~")
            exit(0)
        else:
            self.sender.reply("输入错误，退出")
            exit(0)

    def run(self):
        if self.sender.isAdmin():
            users = sg.bucketAllKeys(self.tongname)
            cks = 0
            for usid in users:
                for i in _sg_literal(sg.bucketGet(self.tongname, usid)):
                    cks += 1
            results = []
            bfs = sg.bucketGet(self.tongconfig, "yxbf")
            if bfs == "":
                bfs = 5
            else:
                bfs = int(bfs)
            sg.notifyMasters(f"🔔[沪上阿姨]🔔\n当前账号数{cks}，并发{bfs}运行中---", self.ts)
            with concurrent.futures.ThreadPoolExecutor(max_workers=bfs) as executor:
                for usid in users:
                    for i in _sg_literal(sg.bucketGet(self.tongname, usid)):
                        self.user = usid
                        for k, y in i.items():
                            ck = y["token"]
                            self.userts = y["qd"]
                            if self.login(ck):
                                future = executor.submit(self.sign(k,ck))
                                results.append(future)
                            else:
                                continue
            sg.notifyMasters(f"🔔[沪上阿姨]运行完毕\n", self.ts)
            exit(0)

if __name__ == "__main__":
    senderID = sg.getSenderID()
    sender = sg.Sender(senderID)
    user = sender.getUserID()
    JD = LT(user, sender)
    message = sender.getMessage()
    if "提交" in message or "上车" in message or "登录" in message or "登陆" in message:
        JD.tj()
    elif "查询" in message:
        JD.cx()
    elif "运行" in message:
        JD.run()
    elif "管理" in message:
        JD.gl()
