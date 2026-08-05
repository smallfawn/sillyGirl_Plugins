# [title: 太平通]
# [name: taiPingTong]
# [language: python]
# [class: 任务]
# [author: linzixuan]
# [version: V6.60]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^太平(管理|查询|配置|运行|教程|检测).*$]
# [icon: https://img1.baidu.com/it/u=35209519,2603388558&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=500]
# [description: 介绍：《太平通插件指令说明》  插件自带任务!；地址：https://www.yuque.com/yuqueyonghulzdzov/fuzugi/xxdck3s248edagql?singleDoc#；更新：运行时账号火爆通知用户；更新：到期前三天自动检测通知用户；更新：支持自定义教程地址链接；更新：新增火爆推送用户开关功能；更新：新增代理IP功能；更新：修复验证码登录，现已支持验证码登录！]
# [depe: ["requests", "urllib3"]]


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
    'bd_tptconfig_yxbf': form.string().title('运行并发数').default('').description('设置管理员一键运行所有账号同时最多多少账号一起运行,默认1'),
    'bd_tptconfig_notify': form.string().title('管理员通知').default('').description('设置接受管理员通知的渠道，如 qq,wx,tg  用英文逗号分割,不设置不推送'),
    'bd_tptconfig_wxpusher': form.string().title('WxPusher任务日志汇总推送').default('').description('首先关注https://wxpusher.zjiecode.com/wxuser/?type=1&id=74454#/follow 然后获取自己的UID配置'),
    'bd_tptconfig_sdyx': form.boolean().title('手动运行').default(False).description('是否允许用户手动执行任务(默认否)'),
    'bd_tptconfig_jcurl': form.string().title('教程链接').default('').description('自定义抓包教程链接,不填则使用默认链接'),
    'bd_tptconfig_hbtz': form.boolean().title('火爆推送').default(False).description('是否开启账号火爆时推送给用户(默认否)'),
    'bd_tptconfig_proxy_api': form.string().title('代理API').default('').description('代理API地址,留空则不使用代理'),
    'bd_tptconfig_wxpusher_app_token': form.string().title('WxPusher AppToken').default('').description('不填则不推送WxPusher日志'),
})
_CONFIG_FIELD_MAP = {
    ('bd_tptconfig', 'yxbf'): 'bd_tptconfig_yxbf',
    ('bd_tptconfig', 'notify'): 'bd_tptconfig_notify',
    ('bd_tptconfig', 'wxpusher'): 'bd_tptconfig_wxpusher',
    ('bd_tptconfig', 'sdyx'): 'bd_tptconfig_sdyx',
    ('bd_tptconfig', 'jcurl'): 'bd_tptconfig_jcurl',
    ('bd_tptconfig', 'hbtz'): 'bd_tptconfig_hbtz',
    ('bd_tptconfig', 'proxy_api'): 'bd_tptconfig_proxy_api',
    ('bd_tptconfig', 'wxpusher_app_token'): 'bd_tptconfig_wxpusher_app_token',
}

import concurrent.futures
import json
import random
import time
from datetime import datetime, timedelta
import os

try:
    from curl_cffi import requests
except:
    import requests

def ts_qb(data, wxpusher_alluid, name, arg1, arg2):
    api_url = 'https://wxpusher.zjiecode.com/api/send/message'
    app_token = sg.bucketGet('bd_tptconfig', 'wxpusher_app_token') or ''
    if not app_token:
        return False

    sorted_data = sorted(data, key=lambda x: x['序号'])

    table_content = ''
    for row in sorted_data:
        if row['arg1'] == '0' or row['arg2'] == '0':
            arg1_value = '🔔账号异常'
            arg2_value = '🔔请打开APP'
        else:
            arg1_value = row['arg1']
            arg2_value = row['arg2']

        table_content += f"<tr><td style='border: 1px solid #ccc; padding: 6px;'>{row['序号']}</td><td style='border: 1px solid #ccc; padding: 6px;'>{row['用户']}</td><td style='border: 1px solid #ccc; padding: 6px;'>{arg1_value}</td><td style='border: 1px solid #ccc; padding: 6px;'>{arg2_value}</td></tr>"

    table_html = f"<table style='border-collapse: collapse;'><tr style='background-color: #f2f2f2;'><th style='border: 1px solid #ccc; padding: 8px;'>🆔</th><th style='border: 1px solid #ccc; padding: 8px;'>{name}</th><th style='border: 1px solid #ccc; padding: 8px;'>{arg1}</th><th style='border: 1px solid #ccc; padding: 8px;'>{arg2}</th></tr>{table_content}</table>"

    params = {
        "appToken": app_token,
        'content': table_html,
        'contentType': 3,  # 表格类型
        'topicIds': [],  # 接收消息的用户ID列表，为空表示发送给所有用户
        "summary": f'太平通日志推送',
        "uids": [wxpusher_alluid],
    }

    response = requests.post(api_url, json=params)

    notify = sg.bucketGet('bd_tptconfig', 'notify')

    if response.status_code == 200:
        result = response.json()
        if result['code'] == 1000:
            if notify:
                tsqd = notify.split(',')
                sg.notifyMasters(f"🎉wxpusher推送成功", tsqd)
        else:
            if notify:
                tsqd = notify.split(',')
                sg.notifyMasters(f'💔wxpusher推送失败，错误信息：{result["msg"]}', tsqd)
            else:
                sender.reply(f'💔wxpusher推送失败，错误信息：{result["msg"]}')
    else:
        if notify:
            tsqd = notify.split(',')
            sg.notifyMasters('⛔wxpusher推送请求失败', tsqd)
        else:
            sender.reply('⛔️wxpusher推送请求失败')


class ATM_tpt:
    def __init__(self, u, s):
        self.black_box = None
        self.code = None
        self.phone = None
        self.user = u
        self.sender = s
        self.usid = None
        self.ck = None
        self.name = None
        self.sqsj = None

    def set_name(self):
        self.sender.reply("欢迎使用太平系统, 请先设置您的备注名(1-6个字符)。退出输入'q'!")
        name = self.sender.listen(60000)
        if name == 'q' or name == 'Q':
            self.sender.reply("退出！")
            return False
        elif name is None:
            self.sender.reply(f'超时退出！')
            return False
        else:
            if len(name) > 6 or len(name) < 1:
                self.sender.reply("备注名不符合要求，退出！")
                return False
            else:
                return name

    def tpsc(self):
        self.name = self.set_name()
        if self.name:
            jcurl = sg.bucketGet('bd_tptconfig', 'jcurl')
            if jcurl == '':
                jcurl = 'https://www.yuque.com/yuqueyonghulzdzov/fuzugi/xvy3lp28apxnpvoq?singleDoc#'

            self.sender.reply(f"""=====太平通登录方式=====
1️⃣ 短信验证码登录
2️⃣ CK直接登录
========================
请回复序号选择登录方式
退出请回复【q】
========================""")
            qmdl = self.sender.listen(60000)
            if qmdl == 'q' or qmdl == 'Q':
                self.sender.reply("退出！")
            elif qmdl is None:
                self.sender.reply(f'超时退出！')
            elif qmdl == '1':
                self.dx_login()
            elif qmdl == '2':
                self.ck_login()
            else:
                self.sender.reply(f'输入有误!!')

    def gl_login(self):
        try:
            xx_url = 'https://ecustomer.cntaiping.com/tpayms/app/tpay/account/getAcct'
            headers = {
                'Host': 'ecustomer.cntaiping.com',
                'x-ac-black-box': '',
                'x-ac-token-ticket': self.ck,
                'x-ac-channel-id': 'KHT',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept': 'application/json;charset=UTF-8',
                'Origin': 'https://ecustomercdn.itaiping.com',
                'User-Agent': "Mozilla/5.0 (Linux; Android 13; Pixel 4 XL Build/TP1A.220905.004; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/119.0.6045.163 Mobile Safari/537.36;yuangongejia#android#kehutong;webank/h5face;webank/1.0;netType:NETWORK_WIFI;appVersion:334;packageName:com.cntaiping.tpapp",
                'Connection': 'keep-alive',
                'Referer': 'https://ecustomercdn.itaiping.com/',
                'x-ac-mc-type': 'gateway.user'
            }
            r = requests.get(xx_url, headers=headers)
            success = r.json().get('success', None)
            if success:
                return '✅有效'
            else:
                return '❌失效'
        except Exception as e:
            return f'⛔{e}'

    def tpgl(self):
        ts = sg.bucketGet('bd_tptcks', self.user)
        if ts == '' or ts == '{}':
            self.sender.reply("太平系统未查询到您的信息! 请先上车! ")
        else:
            ts = _sg_literal(ts)
            n = 0
            id_dict = {}
            msg = """=====太平账号管理=====\n"""
            zhszt = {}
            for k, y in ts.items():
                n += 1
                self.ck = y['ck']
                id_dict[n] = {'usid': k, 'name': y['name'], 'ck': y['ck'], 'sqsj': y['sqsj']}
                zhzt = self.gl_login()
                if y['sqsj'] <= datetime.now().strftime("%Y-%m-%d"):
                    msg += f"""📱 账号{n}：{y["name"]}
🔐 状态: {zhzt}
⏰ 授权: {y["sqsj"]}(已到期)
------------------------\n"""
                else:
                    msg += f"""📱 账号{n}：{y["name"]}
🔐 状态: {zhzt}
⏰ 授权: {y["sqsj"]}
------------------------\n"""
                zhszt[n] = {'zhzt': zhzt}

            msg += """请回复序号选择账号
退出请回复【q】
========================"""
            self.sender.reply(msg)
            xz = self.sender.listen(60000)
            xz_list = []
            for k, y in id_dict.items():
                xz_list.append(k)
            if xz == 'q' or xz == 'Q':
                self.sender.reply("退出！")
            elif xz is None:
                self.sender.reply(f'超时退出！')
            elif int(xz) in xz_list:
                zh = id_dict[int(xz)]
                self.usid = zh['usid']
                self.ck = zh['ck']
                self.name = zh['name']
                self.sqsj = zh['sqsj']
                zhzt = zhszt[int(xz)]['zhzt']
                if '有效' in zhzt:
                    self.gl_zh()
                else:
                    self.sender.reply(f'你都失效了！先去上车更新一下吧！')

            else:
                self.sender.reply(f'输入有误，退出！')

    def gl_zh(self):
        """管理账号"""
        msg = f"""=====账号管理面板=====
📱 当前账号: {self.name}

1️⃣ 账号授权
2️⃣ 任务运行
3️⃣ 删除账号
========================

请回复序号选择操作
退出请回复【q】"""
        self.sender.reply(msg)
        xz = self.sender.listen(60000)
        if xz == 'q' or xz == 'Q':
            self.sender.reply("退出！")
        elif xz is None:
            self.sender.reply(f'超时退出！')
        elif xz == '1':
            self.gl_sq()
        elif xz == '2':
            self.gl_yx()
        elif xz == '3':
            self.gl_sc()
        else:
            self.sender.reply(f'输入有误，退出！')

    def gl_sq(self):
        """账号授权"""
        try:
            sqje = '2099-12-31'
            sqsj = '2099-12-31'
            if sqje == '':
                sqje = '6.6'
            if sqsj == '':
                sqsj = '30'

            if float(sqje) == 0:
                self.sender.reply(f"""=====免费授权=====
⏰ 授权时长: {sqsj}天

请输入需要开通的月数
退出请回复【q】
========================""")
                xz = self.sender.listen(60000)

                if xz == 'q' or xz == 'Q':
                    self.sender.reply("退出！")
                    return

                try:
                    if not xz.isdigit():
                        self.sender.reply("❌ 请输入正确的数字！")
                        return

                    months = int(xz)
                    if months <= 0:
                        self.sender.reply("❌ 月数必须大于0！")
                        return

                    try:
                        if self.sqsj <= datetime.now().strftime("%Y-%m-%d"):
                            new_sqsj = datetime.now() + timedelta(days=int(sqsj) * months)
                        else:
                            sqsj1 = datetime.strptime(self.sqsj, "%Y-%m-%d")
                            new_sqsj = sqsj1 + timedelta(days=int(sqsj) * months)
                        new_sqsj = new_sqsj.strftime("%Y-%m-%d")

                        ts = sg.bucketGet('bd_tptcks', self.user)
                        if ts:
                            ts = _sg_literal(ts)
                            ts[self.usid]['sqsj'] = new_sqsj
                            sg.bucketSet('bd_tptcks', self.user, f'{ts}')

                            msg = f"""=====授权开通成功=====
👤 用户: {self.name}
💰 费用: 免费
🆔 授权ID: {self.user}
⏰ 授权天数: {int(sqsj) * months}天
📅 到期时间: {new_sqsj}
========================"""
                            self.sender.reply(msg)

                            notify = sg.bucketGet('bd_tptconfig', 'notify')
                            if notify:
                                tsqd = notify.split(',')
                                sg.notifyMasters(msg, tsqd)
                        else:
                            self.sender.reply("❌ 获取用户信息失败，请检查配置")

                    except Exception as e:
                        self.sender.reply(f"❌ 授权处理发生错误: {str(e)}")

                except ValueError as e:
                    self.sender.reply(f"❌ 输入处理错误: {str(e)}")
                return

            jfkt = sg.bucketGet('bd_tptconfig', 'jfkt')
            if jfkt.lower() == 'true':
                jfsl = sg.bucketGet('bd_tptconfig', 'jfsl') or '1000'
                self.sender.reply(f"""=====授权开通方式=====
1️⃣ 付费开通
   💰 {sqje}元/{sqsj}天

2️⃣ 积分开通
   🎯 {jfsl}积分/30天

请回复序号选择方式
退出请回复【q】
========================""")

                xz = self.sender.listen(60000)
                if xz == 'q' or xz == 'Q':
                    self.sender.reply("退出！")
                    return

                if xz == '2':
                    self.jf_kt()
                    return
                elif xz != '1':
                    self.sender.reply("输入有误，退出！")
                    return

            self.sender.reply(f"""=====付费开通授权=====
💰 单价: {sqje}元/月
⏰ 时长: 每月{sqsj}天

请输入需要开通的月数
退出请回复【q】
========================""")
            xz = self.sender.listen(60000)

            if xz == 'q' or xz == 'Q':
                self.sender.reply("退出！")
                return

            try:
                if not xz.isdigit():
                    self.sender.reply("❌ 请输入正确的数字！")
                    return

                months = int(xz)
                if months <= 0:
                    self.sender.reply("❌ 月数必须大于0！")
                    return

                total = float(sqje) * months

                self.sender.reply(f"""=====确认订单信息=====
🎫 商品: 太平通授权
📅 时长: {months}个月
💰 单价: {sqje}元/月
💳 总价: {total:.2f}元

确认请回复【y】
取消请回复【n】
========================""")

                confirm = self.sender.listen(60000)
                if confirm is None:
                    self.sender.reply("❌ 超时退出！")
                    return
                elif confirm.lower() == 'n':
                    self.sender.reply("已取消支付！")
                    return
                elif confirm.lower() != 'y':
                    self.sender.reply("输入有误，已取消！")
                    return

                pay_result = self.zf(total, months)

                if pay_result is True:
                    try:
                        if self.sqsj <= datetime.now().strftime("%Y-%m-%d"):
                            new_sqsj = datetime.now() + timedelta(days=int(sqsj) * months)
                        else:
                            sqsj1 = datetime.strptime(self.sqsj, "%Y-%m-%d")
                            new_sqsj = sqsj1 + timedelta(days=int(sqsj) * months)
                        new_sqsj = new_sqsj.strftime("%Y-%m-%d")

                        ts = sg.bucketGet('bd_tptcks', self.user)
                        if ts:
                            ts = _sg_literal(ts)
                            ts[self.usid]['sqsj'] = new_sqsj
                            sg.bucketSet('bd_tptcks', self.user, f'{ts}')

                            msg = f"""=====授权开通成功=====
👤 用户: {self.name}
💰 付款: {total:.2f}元
💳 渠道: {self.sender.getImtype().upper()}
🆔 授权ID: {self.user}
⏰ 授权天数: {int(sqsj) * months}天
📅 到期时间: {new_sqsj}
========================"""
                            self.sender.reply(msg)

                            notify = sg.bucketGet('bd_tptconfig', 'notify')
                            if notify:
                                tsqd = notify.split(',')
                                sg.notifyMasters(msg, tsqd)
                        else:
                            self.sender.reply("❌ 获取用户信息失败，请检查配置")

                    except Exception as e:
                        self.sender.reply(f"❌ 授权处理发生错误: {str(e)}")

            except ValueError as e:
                self.sender.reply(f"❌ 输入处理错误: {str(e)}")

        except Exception as e:
            self.sender.reply(f"❌ 授权处理发生错误: {str(e)}")

    def gl_yx(self):
        """运行账号"""
        sdyx = sg.bucketGet('bd_tptconfig', 'sdyx')
        if sdyx == '':
            sdyx = 'false'
        if sdyx == 'false':
            self.sender.reply("""=====运行失败=====
❌ 管理员未开启手动运行
========================""")
        elif sdyx == 'true':
            if self.sqsj <= datetime.now().strftime("%Y-%m-%d"):
                self.sender.reply(f"""=====运行失败=====
📱 账号: {self.name}
❌ 授权已过期，请及时续费
========================""")
            else:
                tpt = TPT(self.user, 'qd', self.name, self.ck, self.usid, 1)
                tpt.main()

    def gl_sc(self):
        """删除账号"""
        self.sender.reply(f"""=====删除账号确认=====
📱 账号: {self.name}

⚠️ 删除后将清空所有授权信息
确认请回复【y】
取消请回复【n】
========================""")
        zh = self.sender.listen(60000)
        if zh == 'n' or zh == 'N':
            self.sender.reply("已取消删除")
        elif zh is None:
            self.sender.reply("❌ 超时退出")
        elif zh == 'y' or zh == 'Y':
            ts = sg.bucketGet('bd_tptcks', self.user)
            ts = _sg_literal(ts)
            del ts[f'{self.usid}']
            sg.bucketSet('bd_tptcks', self.user, f'{ts}')
            self.sender.reply(f"""=====删除账号成功=====
📱 账号: {self.name}
✅ 状态: 已删除
========================""")
        else:
            self.sender.reply("❌ 输入有误")

    def dssq(self):
        """打赏授权"""
        try:
            status = False
            if status == "True" or status or status == "true":
                self.sender.reply("⚠️ 目前有其他用户正在付款，请稍后再试！")
            else:
                zsm = sg.bucketGet('bd_tptconfig', 'wxzsm')
                sqje = '2099-12-31'
                sqsj = '2099-12-31'
                if zsm == '':
                    self.sender.reply("❌ 管理员未配置二维码！")
                    return
                if sqje == '':
                    sqje = '6.6'
                if sqsj == '':
                    sqsj = '30'

                jfkt = sg.bucketGet('bd_tptconfig', 'jfkt')
                if jfkt.lower() == 'true':
                    jfsl = sg.bucketGet('bd_tptconfig', 'jfsl') or '1000'
                    user_jf = int(sg.bucketGet('dd_sign_points', self.user) or '0')

                    msg = f"""=====选择支付方式====="""
                    if zsm != '':
                        msg += f"""
1️⃣ 微信支付
   💰 {sqje}元/{sqsj}天"""
                    if jfkt == 'true':
                        msg += f"""
2️⃣ 积分支付
   🎯 {jfsl}积分/{sqsj}天
   💫 当前积分: {user_jf}"""
                    msg += """

请回复序号选择方式
退出请回复【q】
========================"""

                    self.sender.reply(msg)
                    choice = self.sender.listen(60000)

                    if choice == 'q' or choice == 'Q':
                        self.sender.reply("已取消支付")
                        return

                    elif choice == '1' and zsm != '':
                        self.sender.replyImage(zsm)
                        self.sender.reply(f"""=====微信扫在线处理=====
💰 单价: {sqje}元/{sqsj}天
⏰ 有效期: 120秒

请使用微信扫码完成支付
支付期间请勿发送其他内容
取消支付请回复【q】
========================""")

                        waitPay = False
                        if waitPay == 'q':
                            self.sender.reply("已取消支付")
                        elif isinstance(waitPay, dict) or isinstance(waitPay, str):
                            try:
                                Money = 0
                                Time = ''
                                if isinstance(waitPay, str):
                                    try:
                                        waitPay = json.loads(waitPay)
                                        if isinstance(waitPay, dict) and waitPay.get('type') == '微信收款':
                                            Money = float(waitPay.get('money', 0))
                                            Time = waitPay.get('time', '')
                                            waitPay = {
                                                "Money": Money,
                                                "Time": Time
                                            }
                                    except:
                                        if "二维码赞赏到账" in waitPay:
                                            try:
                                                amount = waitPay.split("收款金额￥")[1].split("\n")[0]
                                                time = waitPay.split("到账时间")[1].split("\n")[0]
                                                waitPay = {
                                                    "Money": float(amount),
                                                    "Time": time.strip()
                                                }
                                            except Exception as e:
                                                self.sender.reply(f"❌ 解析收款信息失败: {str(e)}")
                                                return

                                Money = float(waitPay.get('Money') or waitPay.get('money', 0))
                                days = int(float(Money) / float(sqje) * int(sqsj))
                                self._update_auth_time(days)

                            except Exception as e:
                                self.sender.reply(f"❌ 支付处理失败: {str(e)}")
                                return

                    elif choice == '2' and jfkt == 'true':
                        if user_jf < int(jfsl):
                            self.sender.reply(f"""=====积分不足=====
👤 当前积分: {user_jf}
📍 需要积分: {jfsl}
========================""")
                            return

                        self.sender.reply(f"""=====积分开通确认=====
💫 消耗积分: {jfsl}
⏰ 授权时长: {sqsj}天

确认请回复【y】
取消请回复【n】
========================""")
                        confirm = self.sender.listen(60000)

                        if confirm.lower() == 'y':
                            new_jf = user_jf - int(jfsl)
                            sg.bucketSet('dd_sign_points', self.user, str(new_jf))

                            self._update_auth_time(int(sqsj))

                            self.sender.reply(f"""=====积分开通成功=====
💫 扣除积分: {jfsl}
💰 剩余积分: {new_jf}
========================""")
                        else:
                            self.sender.reply("已取消支付")
                    else:
                        self.sender.reply("❌ 输入有误")

        except Exception as e:
            self.sender.reply(f"❌ 支付处理失败: {str(e)}")

    def _update_auth_time(self, days):
        """更新授权时间的辅助方法"""
        try:
            dqsj = datetime.now().strftime("%Y-%m-%d")
            if self.sqsj > dqsj:
                self.sqsj = datetime.strptime(self.sqsj, "%Y-%m-%d")
                new_sqsj = self.sqsj + timedelta(days=days)
            else:
                sj = datetime.now()
                new_sqsj = sj + timedelta(days=days)
            new_sqsj = new_sqsj.strftime("%Y-%m-%d")

            ts = sg.bucketGet('bd_tptcks', self.user)
            ts = _sg_literal(ts)
            ts[self.usid] = {'name': self.name, 'ck': self.ck, 'sqsj': new_sqsj}
            sg.bucketSet('bd_tptcks', self.user, f'{ts}')

            msg = f"""=====授权开通成功=====
👤 用户: {self.name}
🆔 授权ID: {self.usid}
⏰ 授权天数: {days}天
📅 到期时间: {new_sqsj}
========================"""
            self.sender.reply(msg)

            notify = sg.bucketGet('bd_tptconfig', 'notify')
            if notify:
                tsqd = notify.split(',')
                sg.notifyMasters(msg, tsqd)

        except Exception as e:
            self.sender.reply(f"❌ 授权更新失败: {str(e)}")

    def tpcx(self):
        ts = sg.bucketGet('bd_tptcks', self.user)
        if ts == '' or ts == '{}':
            self.sender.reply("❌ 太平系统未查询到您的信息! 请先上车!")
        else:
            ts = _sg_literal(ts)
            msg = """=====太平通账号查询=====\n"""
            n = 0
            for k, y in ts.items():
                n += 1
                self.ck = y['ck']
                self.usid = k
                self.name = y['name']
                self.sqsj = y['sqsj']

                zhzt = self.gl_login()
                if '有效' in zhzt:
                    if self.sqsj <= datetime.now().strftime("%Y-%m-%d"):
                        msg += f"""📱 账号{n}：{self.name}
🔐 状态: {zhzt}
⏰ 授权: {self.sqsj} (已过期)
------------------------\n"""
                    else:
                        tpt = TPT(self.user, 'qd', self.name, self.ck, self.usid, 1)
                        coins = tpt.cx()
                        if isinstance(coins, tuple):
                            dqjb, jrjb, llzx, hyyd, rcrw = coins
                            msg += f"""📱 账号{n}：{self.name}
🔐 状态: {zhzt}
💰 今日金币: {jrjb}
💎 当前金币: {dqjb}
⏰ 授权: {self.sqsj}
------------------------\n"""
                        else:
                            msg += f"""📱 账号{n}：{self.name}
🔐 状态: {zhzt}
⚠️ 查询失败，账号可能火爆
⏰ 授权: {self.sqsj}
------------------------\n"""
                else:
                    msg += f"""📱 账号{n}：{self.name}
🔐 状态: {zhzt}
❌ 账号已失效
⏰ 授权: {self.sqsj}
------------------------\n"""
            msg += """⚠️ 温馨提示：
• 账号火爆请打开APP解决
• 一机一号抓包，多号共用会黑
========================"""
            self.sender.reply(msg)

    def get_tptcks(self):
        try:
            if self.sender.isAdmin():
                ts = sg.bucketAllKeys('bd_tptcks')
                kong = 0
                wsqzhs = {}
                start_zhs = {}
                for i in ts:
                    ts_data = sg.bucketGet('bd_tptcks', f'{i}')
                    ts_data = _sg_literal(ts_data)
                    if ts_data == {}:
                        kong += 1
                        sg.bucketDel('bd_tptcks', f'{i}')
                        continue
                    else:
                        for k, y in ts_data.items():
                            ck = y['ck']
                            name = y['name']
                            sqsj = y['sqsj']
                            if sqsj > datetime.now().strftime("%Y-%m-%d"):
                                start_zhs[k] = {
                                    'name': name,
                                    'ck': ck,
                                    'user': i
                                }
                            else:
                                wsqzhs[i] = k
                                continue

                for k, y in wsqzhs.items():
                    ts_data = sg.bucketGet('bd_tptcks', f'{k}')
                    ts_data = _sg_literal(ts_data)
                    del ts_data[f'{y}']
                    sg.bucketSet('bd_tptcks', f'{k}', f'{ts_data}')

                return start_zhs, kong, wsqzhs
        except Exception as e:
            return e

    def tpyx(self):
        try:
            get_tptcks = self.get_tptcks()
            if isinstance(get_tptcks, tuple):
                tptcks, kong, wsqzhs = get_tptcks
                yxbf = sg.bucketGet('bd_tptconfig', 'yxbf')
                if yxbf == '':
                    yxbf = 1

                with concurrent.futures.ThreadPoolExecutor(max_workers=int(yxbf)) as executor:
                    notify = sg.bucketGet('bd_tptconfig', 'notify')
                    if notify == '':
                        self.sender.reply(
                            f"🔔共获取到{len(tptcks)}个账号！\n🔔删除未授权账号{len(wsqzhs)}个! \n🔔删除空账号{kong}个!\n🔔开始{yxbf}线程运行所有账号!")
                    else:
                        tsqd = notify.split(',')
                        self.sender.reply(
                            f"🔔共获取到{len(tptcks)}个账号！\n🔔删除未授权账号{len(wsqzhs)}个! \n🔔删除空账号{kong}个!\n🔔开始{yxbf}线程运行所有账号!")
                        sg.notifyMasters(
                            f"🔔共获取到{len(tptcks)}个账号！\n🔔删除未授权账号{len(wsqzhs)}个! \n🔔删除空账号{kong}个!\n🔔开始{yxbf}线程运行所有账号!",
                            tsqd)

                    results = []
                    for k, y in tptcks.items():
                        tpt = TPT(y['user'], 'qd', y['name'], y['ck'], k, 1)
                        future = executor.submit(tpt.main)
                        results.append(future)
                        time.sleep(0.5)
                        continue

                    a = 0
                    ts_all = []
                    for future in concurrent.futures.as_completed(results):
                        a += 1
                        if a % 100 == 1 and a != 1:
                            wxpusher_alluid = sg.bucketGet('bd_tptconfig', 'wxpusher')
                            if wxpusher_alluid == '':
                                pass
                            else:
                                ts_qb(ts_all, wxpusher_alluid, '用户', '今日金币', '当前金币')
                                ts_all = []

                        result = future.result()
                        if isinstance(result, tuple):
                            if len(result) == 3:
                                name, jrjb, dqjb = result
                                ts = {
                                    '序号': a,
                                    '用户': name,
                                    'arg1': jrjb,
                                    'arg2': f'{int(dqjb)}({int(dqjb) / 100}元)'
                                }
                                ts_all.append(ts)
                                continue
                            elif len(result) == 2:
                                name, yc = result
                                ts = {
                                    '序号': a,
                                    '用户': name,
                                    'arg1': yc,
                                    'arg2': yc
                                }
                                ts_all.append(ts)
                                continue
                            else:
                                continue
                        else:
                            continue

                    wxpusher_alluid = sg.bucketGet('bd_tptconfig', 'wxpusher')
                    if wxpusher_alluid == '':
                        pass
                    else:
                        ts_qb(ts_all, wxpusher_alluid, '用户', '今日金币', '当前金币')

                notify = sg.bucketGet('bd_tptconfig', 'notify')
                if notify == '':
                    self.sender.reply(
                        f'🔔所有账号运行完毕！')
                else:
                    tsqd = notify.split(',')
                    self.sender.reply(
                        f'🔔所有账号运行完毕！')
                    sg.notifyMasters(
                        f'🔔所有账号运行完毕！', tsqd)
            else:
                self.sender.reply(f'🔔获取ck错误:\n🔔{get_tptcks}')
        except Exception as e:
            self.sender.reply(f'运行错误: {e}')

    def tppz(self):
        wxzsm = sg.bucketGet('bd_tptconfig', 'wxzsm')
        pz1 = '已配置' if wxzsm else '未配置'

        sqje = '2099-12-31' or '6.6'
        sqsj = '2099-12-31' or '30'
        sdyx = sg.bucketGet('bd_tptconfig', 'sdyx') or 'false'
        yxbf = sg.bucketGet('bd_tptconfig', 'yxbf') or '1'
        notify = sg.bucketGet('bd_tptconfig', 'notify')
        pz2 = '已配置' if notify else '未配置'
        wxpusher = sg.bucketGet('bd_tptconfig', 'wxpusher')
        pz3 = '已配置' if wxpusher else '未配置'

        msg = f"""=====太平通配置管理=====
1️⃣ 赞赏码 ({pz1})
2️⃣ 授权金额 ({sqje}元)
3️⃣ 授权时间 ({sqsj}天)
4️⃣ 手动运行 ({sdyx})
5️⃣ 运行并发 ({yxbf})
6️⃣ 管理通知 ({pz2})
7️⃣ WxPusher ({pz3})

请回复序号选择配置项
退出请回复【q】
========================"""
        self.sender.reply(msg)
        zh = self.sender.listen(60000)
        if zh == 'q' or zh == 'Q':
            self.sender.reply("已取消操作")
        elif zh is None:
            self.sender.reply("❌ 超时退出")
        elif zh == '1':
            self.sender.reply("""=====赞赏码配置=====
请发送微信赞赏码图片
退出请回复【q】
========================""")
            pz = self.sender.listen(60000)
            if pz == 'q' or pz == 'Q':
                self.sender.reply("已取消操作")
            elif pz is None:
                self.sender.reply("❌ 超时退出")
            else:
                self.sender.replyImage(pz)
                sg.bucketSet('bd_tptconfig', 'wxzsm', f'{pz}')
                self.sender.reply("""=====配置成功=====
✅ 赞赏码已更新
========================""")
        elif zh == '2':
            self.sender.reply("""=====授权金额配置=====
请输入每月授权金额
退出请回复【q】
========================""")
            pz = self.sender.listen(60000)
            if pz == 'q' or pz == 'Q':
                self.sender.reply("已取消操作")
            elif pz is None:
                self.sender.reply("❌ 超时退出")
            else:
                True
                self.sender.reply(f"""=====配置成功=====
✅ 授权金额: {pz}元/月
========================""")
        elif zh == '3':
            self.sender.reply("""=====授权时间配置=====
请输入每月授权天数
退出请回复【q】
========================""")
            pz = self.sender.listen(60000)
            if pz == 'q' or pz == 'Q':
                self.sender.reply("已取消操作")
            elif pz is None:
                self.sender.reply("❌ 超时退出")
            else:
                True
                self.sender.reply(f"""=====配置成功=====
✅ 授权时间: {pz}天/月
========================""")
        elif zh == '4':
            self.sender.reply("""=====手动运行配置=====
请输入是否允许用户手动运行
true: 允许
false: 禁止

退出请回复【q】
========================""")
            pz = self.sender.listen(60000)
            if pz == 'q' or pz == 'Q':
                self.sender.reply("已取消操作")
            elif pz is None:
                self.sender.reply("❌ 超时退出")
            else:
                sg.bucketSet('bd_tptconfig', 'sdyx', f'{pz}')
                status = "允许" if pz.lower() == 'true' else "禁止"
                self.sender.reply(f"""=====配置成功=====
✅ 手动运行: {status}
========================""")
        elif zh == '5':
            self.sender.reply("""=====并发数配置=====
请输入最大并发运行数量
退出请回复【q】
========================""")
            pz = self.sender.listen(60000)
            if pz == 'q' or pz == 'Q':
                self.sender.reply("已取消操作")
            elif pz is None:
                self.sender.reply("❌ 超时退出")
            else:
                sg.bucketSet('bd_tptconfig', 'yxbf', f'{pz}')
                self.sender.reply(f"""=====配置成功=====
✅ 最大并发: {pz}
========================""")
        elif zh == '6':
            self.sender.reply("""=====通知渠道配置=====
请输入通知渠道，用英文逗号分隔
支持渠道: qq,wx,tg
不设置则不推送

退出请回复【q】
========================""")
            pz = self.sender.listen(60000)
            if pz == 'q' or pz == 'Q':
                self.sender.reply("已取消操作")
            elif pz is None:
                self.sender.reply("❌ 超时退出")
            else:
                sg.bucketSet('bd_tptconfig', 'notify', f'{pz}')
                self.sender.reply(f"""=====配置成功=====
✅ 通知渠道: {pz}
========================""")
        elif zh == '7':
            self.sender.reply("""=====WxPusher配置=====
请输入WxPusher的UID
退出请回复【q】
========================""")
            pz = self.sender.listen(60000)
            if pz == 'q' or pz == 'Q':
                self.sender.reply("已取消操作")
            elif pz is None:
                self.sender.reply("❌ 超时退出")
            else:
                sg.bucketSet('bd_tptconfig', 'wxpusher', f'{pz}')
                self.sender.reply(f"""=====配置成功=====
✅ WxPusher UID: {pz}
========================""")
        else:
            self.sender.reply("❌ 输入有误")

    def tpsq(self):
        msg = f"""=====太平通授权管理=====
1️⃣ 一键授权所有用户
2️⃣ 单独授权用户

请回复序号选择操作
退出请回复【q】
========================"""
        self.sender.reply(msg)
        xz = self.sender.listen(60000)

        if xz == 'q' or xz == 'Q':
            self.sender.reply("已取消操作")
            return
        elif xz is None:
            self.sender.reply("❌ 超时退出")
            return
        elif xz == '1':
            self.qbqbsq()
        elif xz == '2':
            msg = f"""=====用户授权=====
请输入需要授权的账号ID
(可通过发送myuid获取)

退出请回复【q】
========================"""
            self.sender.reply(msg)
            myuid = self.sender.listen(60000)
            if myuid == 'q' or myuid == 'Q':
                self.sender.reply("已取消操作")
            elif myuid == 1:
                self.qbqbsq()
            elif myuid is None:
                self.sender.reply("❌ 超时退出")
            else:
                ts = sg.bucketGet('bd_tptcks', myuid)
                if ts == '' or ts == '{}':
                    self.sender.reply(f"""=====查询失败=====
❌ 未找到用户 {myuid} 的信息
请确认ID是否正确
========================""")
                else:
                    ts = _sg_literal(ts)
                    n = 0
                    id_dict = {}
                    msg = """=====选择授权账号=====
0️⃣ 授权所有账号
------------------------\n"""
                    for k, y in ts.items():
                        n += 1
                        self.ck = y['ck']
                        self.usid = k
                        self.name = y['name']
                        self.sqsj = y['sqsj']
                        id_dict[n] = {'usid': self.usid, 'name': self.name, 'ck': self.ck, 'sqsj': self.sqsj}
                        msg += f"""📱 账号{n}：{y["name"]}
⏰ 授权: {self.sqsj}
------------------------\n"""
                    msg += """请回复序号选择账号
退出请回复【q】
========================"""
                    self.sender.reply(msg)
                    xz = self.sender.listen(60000)
                    xz_list = []
                    for k, y in id_dict.items():
                        xz_list.append(k)
                    if xz == 'q' or xz == 'Q':
                        self.sender.reply("已取消操作")
                    elif xz is None:
                        self.sender.reply("❌ 超时退出")
                    elif xz == '0':
                        msg = f"""=====批量授权=====
请输入授权天数
退出请回复【q】
========================"""
                        self.sender.reply(msg)
                        sjts = self.sender.listen(60000)
                        if sjts == 'q' or sjts == 'Q':
                            self.sender.reply("已取消操作")
                        elif sjts is None:
                            self.sender.reply("❌ 超时退出")
                        elif isinstance(int(sjts), int):
                            success_count = 0
                            for k, y in ts.items():
                                try:
                                    dqsj = datetime.now().strftime("%Y-%m-%d")
                                    if y['sqsj'] > dqsj:
                                        sqsj = datetime.strptime(y['sqsj'], "%Y-%m-%d")
                                        new_sqsj = sqsj + timedelta(days=int(sjts))
                                    else:
                                        new_sqsj = datetime.now() + timedelta(days=int(sjts))
                                    new_sqsj = new_sqsj.strftime("%Y-%m-%d")
                                    ts[k]['sqsj'] = new_sqsj
                                    success_count += 1
                                except:
                                    continue
                            sg.bucketSet('bd_tptcks', myuid, f'{ts}')
                            msg = f"""=====授权完成=====
✅ 成功授权: {success_count}个账号
⏰ 授权天数: {sjts}天
========================"""
                            self.sender.reply(msg)
                            notify = sg.bucketGet('bd_tptconfig', 'notify')
                            if notify:
                                tsqd = notify.split(',')
                                sg.notifyMasters(msg, tsqd)
                        else:
                            self.sender.reply("❌ 天数格式错误")
                    elif int(xz) in xz_list:
                        zh = id_dict[int(xz)]
                        self.usid = zh['usid']
                        self.ck = zh['ck']
                        self.name = zh['name']
                        self.sqsj = zh['sqsj']

                        msg = f"""=====账号授权=====
📱 账号: {self.name}

请输入授权天数
退出请回复【q】
========================"""
                        self.sender.reply(msg)
                        sjts = self.sender.listen(60000)
                        if sjts == 'q' or sjts == 'Q':
                            self.sender.reply("已取消操作")
                        elif sjts is None:
                            self.sender.reply("❌ 超时退出")
                        elif isinstance(int(sjts), int):
                            dqsj = datetime.now().strftime("%Y-%m-%d")
                            if self.sqsj > dqsj:
                                self.sqsj = datetime.strptime(self.sqsj, "%Y-%m-%d")
                                new_sqsj = self.sqsj + timedelta(days=int(sjts))
                                new_sqsj = new_sqsj.strftime("%Y-%m-%d")
                            else:
                                sj = datetime.now()
                                new_sqsj = sj + timedelta(days=int(sjts))
                                new_sqsj = new_sqsj.strftime("%Y-%m-%d")
                            ts = sg.bucketGet('bd_tptcks', f'{myuid}')
                            ts = _sg_literal(ts)
                            for k, y in ts.items():
                                if self.usid == k:
                                    ts[f'{k}'] = {'name': self.name, 'ck': self.ck, 'sqsj': new_sqsj}
                                    sg.bucketSet('bd_tptcks', f'{myuid}', f'{ts}')
                                    msg = f"""=====授权成功=====
👤 用户ID: {myuid}
📱 账号: {self.name}
🆔 授权ID: {self.usid}
⏰ 授权天数: {int(sjts)}天
📅 到期时间: {new_sqsj}
========================"""
                                    self.sender.reply(msg)
                                    break
                                else:
                                    continue
                        else:
                            self.sender.reply("❌ 天数格式错误")
                    else:
                        self.sender.reply("❌ 输入有误")

    def qbqbsq(self):
        """一键授权所有用户"""
        try:
            ts = sg.bucketAllKeys('bd_tptcks')
            if not ts:
                self.sender.reply("""=====查询失败=====
❌ 未找到任何用户信息
========================""")
                return

            self.sender.reply("""=====批量授权=====
请输入授权天数
退出请回复【q】
========================""")
            sjts = self.sender.listen(60000)
            if sjts == 'q' or sjts == 'Q':
                self.sender.reply("已取消操作")
                return
            elif sjts is None:
                self.sender.reply("❌ 超时退出")
                return

            try:
                sjts = int(sjts)
            except:
                self.sender.reply("❌ 天数格式错误")
                return

            success_count = 0
            fail_count = 0

            for myuid in ts:
                user_data = sg.bucketGet('bd_tptcks', myuid)
                if user_data == '' or user_data == '{}':
                    continue

                user_data = _sg_literal(user_data)
                for usid, info in user_data.items():
                    dqsj = datetime.now().strftime("%Y-%m-%d")
                    if info['sqsj'] > dqsj:
                        sqsj = datetime.strptime(info['sqsj'], "%Y-%m-%d")
                        new_sqsj = sqsj + timedelta(days=sjts)
                    else:
                        new_sqsj = datetime.now() + timedelta(days=sjts)
                    new_sqsj = new_sqsj.strftime("%Y-%m-%d")

                    try:
                        user_data[usid]['sqsj'] = new_sqsj
                        sg.bucketSet('bd_tptcks', myuid, f'{user_data}')
                        success_count += 1
                    except:
                        fail_count += 1

            msg = f"""=====批量授权完成=====
✅ 成功授权: {success_count}个账号
❌ 授权失败: {fail_count}个账号
⏰ 授权天数: {sjts}天
========================"""
            self.sender.reply(msg)

            notify = sg.bucketGet('bd_tptconfig', 'notify')
            if notify:
                tsqd = notify.split(',')
                sg.notifyMasters(msg, tsqd)

        except Exception as e:
            self.sender.reply(f"❌ 批量授权失败: {str(e)}")

    def jf_kt(self):
        """积分开通授权"""
        try:
            jfsl = sg.bucketGet('bd_tptconfig', 'jfsl')
            sqsj = '2099-12-31'
            if not jfsl:
                jfsl = '1000'
            if not sqsj:
                sqsj = '30'

            user_jf = sg.bucketGet('dd_sign_points', self.user) or '0'
            try:
                user_jf = int(user_jf)
                jfsl = int(jfsl)
            except:
                self.sender.reply("❌ 积分格式错误")
                return

            self.sender.reply(f"""=====积分开通授权=====
💫 当前积分: {user_jf}
💰 开通费用: {jfsl}积分/{sqsj}天

请输入需要开通的月数
退出请回复【q】
========================""")

            months = self.sender.listen(60000)
            if months == 'q' or months == 'Q':
                self.sender.reply("已取消操作")
                return

            try:
                months = int(months)
                if months <= 0:
                    self.sender.reply("❌ 月数必须大于0！")
                    return

                total_points = jfsl * months
                if user_jf < total_points:
                    self.sender.reply(f"""=====积分不足=====
👤 当前积分: {user_jf}
📍 需要积分: {total_points}
========================""")
                    return

                self.sender.reply(f"""=====积分开通确认=====
💫 消耗积分: {total_points}
⏰ 授权时长: {int(sqsj) * months}天

确认请回复【y】
取消请回复【n】
========================""")
                confirm = self.sender.listen(60000)

                if confirm and confirm.lower() == 'y':
                    new_jf = user_jf - total_points
                    sg.bucketSet('dd_sign_points', self.user, str(new_jf))

                    if self.sqsj <= datetime.now().strftime("%Y-%m-%d"):
                        new_sqsj = datetime.now() + timedelta(days=int(sqsj) * months)
                    else:
                        sqsj1 = datetime.strptime(self.sqsj, "%Y-%m-%d")
                        new_sqsj = sqsj1 + timedelta(days=int(sqsj) * months)
                    new_sqsj = new_sqsj.strftime("%Y-%m-%d")

                    ts = _sg_literal(sg.bucketGet('bd_tptcks', self.user))
                    ts[self.usid]['sqsj'] = new_sqsj
                    sg.bucketSet('bd_tptcks', self.user, f'{ts}')

                    msg = f"""=====积分开通成功=====
💫 扣除积分: {total_points}
💰 剩余积分: {new_jf}
⏰ 授权天数: {int(sqsj) * months}天
📅 到期时间: {new_sqsj}
========================"""
                    self.sender.reply(msg)

                    notify = sg.bucketGet('bd_tptconfig', 'notify')
                    if notify:
                        tsqd = notify.split(',')
                        admin_msg = f"""=====积分开通通知=====
👤 用户: {self.user}
{msg}"""
                        sg.notifyMasters(admin_msg, tsqd)

                else:
                    self.sender.reply("已取消支付")

            except ValueError:
                self.sender.reply("❌ 请输入正确的数字！")

        except Exception as e:
            self.sender.reply(f"❌ 积分开通出错: {str(e)}")

    def zf(self, total, months):
        """支付处理"""
        try:
            if total == 0:
                self.sender.reply(f"""=====支付成功=====
✅ 金额: 0.00元
💫 状态: 已完成
========================""")
                return True

            wxzsm = sg.bucketGet('bd_tptconfig', 'wxzsm')
            if not wxzsm:
                self.sender.reply("❌ 管理员未配置二维码!")
                return False

            self.sender.reply(f"""=====微信扫在线处理=====
🎫 商品: 太平通授权
📅 时长: {months}个月
💳 应付: {total:.2f}元

请使用微信扫码完成支付
取消支付请回复【q】
========================""")
            self.sender.replyImage(wxzsm)  # 显示二维码

            status = False
            if status == "True" or status or status == "true":
                self.sender.reply("⚠️ 目前有其他用户正在付款，请稍后再试！")
                return False

            result = False  # 等待120秒

            if isinstance(result, str) and result.lower() == 'q':
                self.sender.reply('❌ 已取消支付')
                return False
            elif result is None:  # 超时处理
                self.sender.reply('❌ 支付超时，已退出')
                return False

            try:
                if isinstance(result, dict):
                    if result.get('type') == '微信赞赏':
                        Money = float(result.get('money', 0))
                        Time = result.get('time', '')
                        From = result.get('from_name', '')
                    elif result.get('type') == '微信收款':
                        Money = float(result.get('money', 0))
                        Time = result.get('time', '')
                        From = result.get('from_name', '')
                    else:
                        Money = float(result.get('Money', 0))
                        Time = result.get('Time', '')
                        From = ''
                else:
                    try:
                        result = json.loads(result)
                        if result.get('type') == '微信赞赏':
                            Money = float(result.get('money', 0))
                            Time = result.get('time', '')
                            From = result.get('from_name', '')
                        elif result.get('type') == '微信收款':
                            Money = float(result.get('money', 0))
                            Time = result.get('time', '')
                            From = result.get('from_name', '')
                        else:
                            Money = float(result.get('Money', 0))
                            Time = result.get('Time', '')
                            From = ''
                    except:
                        self.sender.reply("❌ 无法解析支付结果")
                        return False

                if abs(Money - total) < 0.000001:  # 使用浮点数比较
                    self.sender.reply(f"""=====支付成功=====
💰 金额: {Money:.2f}元
⏰ 时间: {Time}
✨ 状态: 已完成
========================""")
                    return True
                else:
                    self.sender.reply(f"""=====支付金额错误=====
💰 应付: {total:.2f}元
💳 实付: {Money:.2f}元
👤 付款人: {From}

❗ 请稍后核对支付记录！
========================""")
                    return False

            except Exception as e:
                self.sender.reply(f"❌ 支付处理失败: {str(e)}")
                return False

        except Exception as e:
            self.sender.reply(f"❌ 支付处理出错: {str(e)}")
            return False

    def dx_login(self):
        """短信验证码登录"""
        try:
            import uuid
            import urllib3

            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

            def generate_device_id():
                """生成设备ID"""
                return f"{uuid.uuid4().hex[:8]}-{uuid.uuid4().hex[:12]}-{uuid.uuid4().hex[:8]}-{uuid.uuid4().hex[:7]}-{uuid.uuid4().hex[:12]}"

            self.sender.reply(f"""=====短信验证码登录=====
🔔{self.name},你好！
请输入手机号码
退出请回复【q】
========================""")
            phone = self.sender.listen(60000)
            if phone == 'q' or phone == 'Q':
                self.sender.reply("退出！")
                return
            elif phone is None:
                self.sender.reply(f'超时退出！')
                return
            elif len(phone) != 11 or not phone.isdigit():
                self.sender.reply("❌ 请输入11位手机号码")
                return

            self.phone = phone

            device_id = generate_device_id()

            common_headers = {
                'Accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Origin': 'https://ecustomercdn.itaiping.com',
                'Referer': 'https://ecustomercdn.itaiping.com/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36',
                'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
                'x-ac-device-id': device_id,
                'anonymousId': device_id,
                'x-ac-channel-id': 'KHT',
                'x-ac-mc-type': 'gateway.user',
                'x-ac-utm': '11810',
                'x-ac-live-room': '',
                'x-ac-sourceutm': '',
                'x-ac-token-ticket': ''
            }

            session = requests.Session()
            session.verify = False

            try:
                self.sender.reply("🔄 正在初始化登录服务...")
                start_url = 'https://ecustomer.cntaiping.com/userms/anonymous/startup/notify'

                response = session.get(start_url, headers=common_headers, timeout=30)
                if response.status_code != 200:
                    self.sender.reply("❌ 启动通知失败")
                    return

                switch_url = 'https://ecustomer.cntaiping.com/userms/unifiedLogin/captcha/switch/v2'
                switch_headers = common_headers.copy()
                switch_headers['Content-Type'] = 'application/json; charset=utf-8'

                switch_data = {
                    "mobile": phone,
                    "internatCode": "0086",
                    "businessCode": "LOGIN"
                }

                response = session.post(switch_url, json=switch_data, headers=switch_headers, timeout=30)
                if response.status_code != 200:
                    self.sender.reply("❌ 验证码配置检查失败")
                    return

                self.sender.reply("📱 正在发送短信验证码...")
                sms_url = 'https://ecustomer.cntaiping.com/commonms/unifiedLogin/msg/verifyCodeSms'

                sms_data = {
                    "mobile": phone,
                    "internatCode": "0086",
                    "businessCode": "LOGIN",
                    "serviceType": "KHTBASIC",
                    "type": "QUICKLOGON"
                }

                response = session.post(sms_url, json=sms_data, headers=switch_headers, timeout=30)

                if response.status_code == 200:
                    result = response.json()
                    if result.get('success') or result.get('code') == '0000':
                        self.sender.reply("✅ 验证码发送成功！")
                    else:
                        self.sender.reply(f"❌ 验证码发送失败: {result.get('message', '未知错误')}")
                        return
                else:
                    self.sender.reply("❌ 验证码发送请求失败")
                    return

                retry_count = 3
                while retry_count > 0:
                    self.sender.reply("""=====验证码验证=====
请输入收到的6位验证码
退出请回复【q】
========================""")

                    code = self.sender.listen(60000)
                    if code == 'q' or code == 'Q':
                        self.sender.reply("退出！")
                        return
                    elif code is None:
                        self.sender.reply(f'超时退出！')
                        return
                    elif len(code) != 6 or not code.isdigit():
                        self.sender.reply("❌ 请输入6位数字验证码")
                        continue

                    login_url = 'https://ecustomer.cntaiping.com/userms/anonymous/auth/unifiedLog/loginByMobileVerifyCode/v1'

                    login_data = {
                        "phone": phone,
                        "internatCode": "0086",
                        "verificationcode": code,
                        "x_agentcode": "1762724346751963136",
                        "userSysType": "UNIFORM_USER",
                        "userSource": "TPT_WEB"
                    }

                    response = session.post(login_url, json=login_data, headers=switch_headers, timeout=30)

                    if response.status_code == 200:
                        result = response.json()

                        if result.get('success') and result.get('code') == "0000":
                            auth_token = result.get('data', {}).get('authToken')
                            user_id = result.get('data', {}).get('userId')

                            if auth_token and user_id:
                                self.usid = user_id
                                self.ck = auth_token

                                ts = sg.bucketGet('bd_tptcks', self.user)
                                if not ts:
                                    data = {
                                        f'{self.usid}': {
                                            'name': self.name,
                                            'ck': self.ck,
                                            'sqsj': f'{datetime.now().strftime("%Y-%m-%d")}'
                                        }
                                    }
                                    sg.bucketSet('bd_tptcks', self.user, f'{data}')
                                    self.sender.reply(f'{self.name}>>>🔔首次登录成功!发送【太平管理】对账号进行管理!')
                                else:
                                    ts = _sg_literal(ts)
                                    if self.usid in ts:
                                        for k, y in ts.items():
                                            if self.usid == k:
                                                ts[f'{k}'] = {'name': self.name, 'ck': self.ck, 'sqsj': y['sqsj']}
                                                sg.bucketSet('bd_tptcks', self.user, f'{ts}')
                                                self.sender.reply(f'{self.name}>>>🔔更新账号成功！发送【太平管理】对账号进行管理!')
                                                break
                                    else:
                                        ts[f'{self.usid}'] = {
                                            'name': self.name,
                                            'ck': self.ck,
                                            'sqsj': f'{datetime.now().strftime("%Y-%m-%d")}'
                                        }
                                        sg.bucketSet('bd_tptcks', self.user, f'{ts}')
                                        self.sender.reply(f'{self.name}>>>🔔新增登录成功!发送【太平管理】对账号进行管理!')
                                return
                            else:
                                self.sender.reply("❌ 登录响应数据不完整")
                                return
                        else:
                            error_msg = result.get('message', result.get('desc', '未知错误'))
                            if "验证码" in error_msg:
                                retry_count -= 1
                                if retry_count > 0:
                                    self.sender.reply(f"❌ 验证码错误，还有{retry_count}次机会")
                                    continue
                                else:
                                    self.sender.reply("❌ 验证码错误次数过多，请稍后重试")
                                    return
                            else:
                                self.sender.reply(f"❌ 登录失败: {error_msg}")
                                return
                    else:
                        self.sender.reply("❌ 登录请求失败")
                        return

            except requests.exceptions.RequestException as e:
                self.sender.reply(f"❌ 网络请求异常: {str(e)}")
                return
            except Exception as e:
                self.sender.reply(f"❌ 登录过程中发生错误: {str(e)}")
                return

        except Exception as e:
            self.sender.reply(f"❌ 登录过程异常: {str(e)}")

    def get_token(self):
        try:
            url = "https://ecustomer.cntaiping.com/userms/anonymous/auth/unifiedLog/loginByMobileVerifyCode/v1"

            payload = {
                "phone": f"{self.phone}",
                "internatCode": "0086",
                "verificationcode": f"{self.code}",
                "x_agentcode": "",
                "userSysType": "UNIFORM_USER",
                "userSource": "TPT_WEB"
            }

            headers = {
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
                'Accept-Encoding': "gzip, deflate, br, zstd",
                'sec-ch-ua': "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Microsoft Edge\";v=\"126\"",
                'x-ac-channel-id': "KHT",
                'x-ac-device-id': "2905f0b73df93c-05f7e12b4e0a4e-4c657b58-2359296-1905f0b73e0edb",
                'x-ac-utm': "11180",
                'x-ac-sourceutm': "",
                'sec-ch-ua-mobile': "?0",
                'anonymousId': "1905f0b73df93c-05f7e12b4e0a4e-4c657b58-2359296-1905f0b73e0edb",
                'Content-Type': "application/json; charset=utf-8",
                'x-ac-mc-type': "gateway.user",
                'x-ac-black-box': self.black_box,
                'x-ac-live-room': "",
                'x-ac-token-ticket': "",
                'sec-ch-ua-platform': "\"Windows\"",
                'Origin': "https://ecustomercdn.itaiping.com",
                'Sec-Fetch-Site': "cross-site",
                'Sec-Fetch-Mode': "cors",
                'Sec-Fetch-Dest': "empty",
                'Referer': "https://ecustomercdn.itaiping.com/",
                'Accept-Language': "zh-CN,zh;q=0.9"
            }

            r = requests.post(url, json=payload, headers=headers)

            success = r.json().get('success', None)
            if success:
                self.usid = r.json()['data']['userId']
                self.ck = r.json()['data']['authToken']
                return True
            else:
                self.sender.reply(f"❌登录失败!\n{r.json().get('desc', None)}")
                return False
        except Exception as e:
            self.sender.reply(f'⛔登录异常!\n{e}')
            return False

    def ck_login(self):
        jcurl = sg.bucketGet('bd_tptconfig', 'jcurl')
        if jcurl == '':
            jcurl = 'https://www.yuque.com/yuqueyonghulzdzov/fuzugi/xvy3lp28apxnpvoq?singleDoc#'

        self.sender.reply(f"""=====太平通CK登录=====
👤 {self.name}，您好!

📖 抓包教程: {jcurl}
🎯 抓包应用: 太平通APP
🔍 抓包域名: ecustomer.cntaiping.com
🎫 抓包参数: x-ac-token-ticket

💰 收益说明:
- 每天约100金币 ≈ 1RMB
- 可兑换话费、e卡、会员等

⚠️ 注意事项:
- 一机一号抓包
- 多号共用设备会被封禁

请在120秒内发送您的x-ac-token-ticket
退出请回复'q'
========================""")

        ck = self.sender.input(120000, 1000, False)
        if ck == 'q' or ck == 'Q':
            self.sender.reply("退出！")

        elif ck is None:
            self.sender.reply(f'超时退出！')

        elif 'ey' in ck:
            xx_url = 'https://ecustomer.cntaiping.com/tpayms/app/tpay/account/getAcct'
            headers = {
                'Host': 'ecustomer.cntaiping.com',
                'x-ac-black-box': '',
                'x-ac-token-ticket': ck,
                'x-ac-channel-id': 'KHT',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept': 'application/json;charset=UTF-8',
                'Origin': 'https://ecustomercdn.itaiping.com',
                'User-Agent': "Mozilla/5.0 (Linux; Android 13; Pixel 4 XL Build/TP1A.220905.004; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/119.0.6045.163 Mobile Safari/537.36;yuangongejia#android#kehutong;webank/h5face;webank/1.0;netType:NETWORK_WIFI;appVersion:334;packageName:com.cntaiping.tpapp",
                'Connection': 'keep-alive',
                'Referer': 'https://ecustomercdn.itaiping.com/',
                'x-ac-mc-type': 'gateway.user'
            }
            try:
                r = requests.get(xx_url, headers=headers)
                success = r.json().get('success', None)
                if success:
                    usid = r.json()["data"]["userId"]
                    ts = sg.bucketGet('bd_tptcks', self.user)
                    if not ts:
                        data = {
                            f'{usid}': {
                                'name': self.name,
                                'ck': ck,
                                'sqsj': f'{datetime.now().strftime("%Y-%m-%d")}'
                            }
                        }
                        sg.bucketSet('bd_tptcks', self.user, f'{data}')
                        self.sender.reply(f"{self.name}>>>🔔登录成功!发送'太平管理'对账号进行管理!")
                    else:
                        ts = _sg_literal(ts)
                        if usid in ts:
                            for k, y in ts.items():
                                if usid == k:
                                    ts[f'{k}'] = {'name': self.name, 'ck': ck, 'sqsj': y['sqsj']}
                                    sg.bucketSet('bd_tptcks', self.user, f'{ts}')
                                    self.sender.reply(f"{self.name}>>>🔔更新成功！发送'太平管理'对账号进行管理!")
                                    break
                                else:
                                    continue
                        else:
                            ts[f'{usid}'] = {
                                'name': self.name,
                                'ck': ck,
                                'sqsj': f'{datetime.now().strftime("%Y-%m-%d")}'
                            }
                            sg.bucketSet('bd_tptcks', self.user, f'{ts}')
                            self.sender.reply(f"{self.name}>>>🔔登录成功!发送'太平管理'对账号进行管理!")
                else:
                    msg = r.json()['msg']
                    self.sender.reply(f'{self.name}登录失败>>>{msg}')
            except Exception as e:
                self.sender.reply(f'{self.name}登录错误>>>{e}')
        else:
            self.sender.reply(f'输入有误，退出！')

    def tpjc(self):
        """定时太平检测 - 检查所有用户的授权过期情况"""
        try:
            if not self.sender.isAdmin():
                self.sender.reply("❌ 此功能仅限管理员使用")
                return

            all_users = sg.bucketAllKeys('bd_tptcks')
            if not all_users:
                self.sender.reply("""=====检测完成=====
📊 检测结果: 无用户数据
========================""")
                return

            total_accounts = 0
            expired_accounts = []
            expiring_accounts = []
            normal_accounts = 0

            current_date = datetime.now()

            for user_id in all_users:
                user_data = sg.bucketGet('bd_tptcks', user_id)
                if not user_data or user_data == '{}':
                    continue

                try:
                    user_data = _sg_literal(user_data)
                    for account_id, account_info in user_data.items():
                        total_accounts += 1
                        account_name = account_info.get('name', '未知')
                        expire_date_str = account_info.get('sqsj', '')

                        if expire_date_str:
                            expire_date = datetime.strptime(expire_date_str, "%Y-%m-%d")
                            days_left = (expire_date - current_date).days

                            if days_left < 0:
                                expired_accounts.append({
                                    'user_id': user_id,
                                    'account_name': account_name,
                                    'expire_date': expire_date_str,
                                    'days_overdue': abs(days_left)
                                })
                            elif 0 <= days_left <= 3:
                                expiring_accounts.append({
                                    'user_id': user_id,
                                    'account_name': account_name,
                                    'expire_date': expire_date_str,
                                    'days_left': days_left
                                })
                            else:
                                normal_accounts += 1

                except Exception as e:
                    print(f"处理用户 {user_id} 数据时出错: {e}")
                    continue

            notification_count = 0
            for account in expiring_accounts:
                try:
                    msg = f"""⚠️ 授权即将到期提醒 ⚠️

📱 账号: {account['account_name']}
⏰ 剩余时间: {account['days_left']}天
📅 到期时间: {account['expire_date']}

请及时续费以免影响使用！
发送【太平管理】进行续费操作"""

                    sg.push('wb', '', account['user_id'], '', msg)
                    sg.push('tg', '', account['user_id'], '', msg)
                    sg.push('qq', '', account['user_id'], '', msg)
                    sg.push('qb', '', account['user_id'], '', msg)
                    sg.push('wx', '', account['user_id'], '', msg)
                    notification_count += 1

                except Exception as e:
                    print(f"通知用户 {account['user_id']} 失败: {e}")

            report = f"""=====太平通授权检测报告=====
📊 检测时间: {current_date.strftime('%Y-%m-%d %H:%M:%S')}
📈 总账号数: {total_accounts}个
✅ 正常账号: {normal_accounts}个
⚠️ 即将过期: {len(expiring_accounts)}个
❌ 已过期: {len(expired_accounts)}个
📤 发送通知: {notification_count}条

"""

            if expiring_accounts:
                report += "⚠️ 即将过期账号:\n"
                for account in expiring_accounts:
                    report += f"• {account['account_name']} (剩余{account['days_left']}天)\n"
                report += "\n"

            if expired_accounts:
                report += "❌ 已过期账号:\n"
                for account in expired_accounts:
                    report += f"• {account['account_name']} (过期{account['days_overdue']}天)\n"
                report += "\n"

            report += "========================"

            self.sender.reply(report)

            notify = sg.bucketGet('bd_tptconfig', 'notify')
            if notify:
                tsqd = notify.split(',')
                sg.notifyMasters(report, tsqd)

        except Exception as e:
            error_msg = f"❌ 检测过程中发生错误: {str(e)}"
            self.sender.reply(error_msg)
            print(f"太平检测错误: {e}")


class TPT:
    def __init__(self, u, qd, n, c, uid, qyinfo):
        self.qd = qd
        self.user = u
        self.qyinfo = qyinfo
        self.usid = uid
        self.name = n
        self.ck = c
        self.llzx = None
        self.hyyd = None
        self.ydlisturl = None
        self.zldatas = []
        self.ydname = None
        self.ydid = None
        self.taskid = None
        self.rwname = None
        self.joinPoint = None
        self.htid = None
        self.validDate = None
        try:
            user_data = sg.bucketGet('bd_tptcks', u)
            if user_data:
                user_data = _sg_literal(user_data)
                self.sqsj = user_data[str(uid)]['sqsj']
            else:
                self.sqsj = None
        except:
            self.sqsj = None
        self.headers = {
            'Host': 'ecustomer.cntaiping.com',
            'x-ac-black-box': 'jWPVu1713323931keU0txvxzkc',
            'x-ac-token-ticket': self.ck,
            'x-ac-channel-id': 'KHT',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'application/json;charset=UTF-8',
            'Origin': 'https://ecustomercdn.itaiping.com',
            'User-Agent': "Mozilla/5.0 (Linux; Android 13; Pixel 4 XL Build/TP1A.220905.004; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/119.0.6045.163 Mobile Safari/537.36;yuangongejia#android#kehutong;webank/h5face;webank/1.0;netType:NETWORK_WIFI;appVersion:334;packageName:com.cntaiping.tpapp",
            'Connection': 'keep-alive',
            'Referer': 'https://ecustomercdn.itaiping.com/',
            'x-ac-mc-type': 'gateway.user',
            'Content-Type': 'application/json'
        }

    def get_proxy(self):
        """获取代理IP"""
        try:
            proxy_api = sg.bucketGet('bd_tptconfig', 'proxy_api')
            if not proxy_api:
                return None

            try:
                import requests as requests_original
                r = requests_original.get(proxy_api, timeout=10)
            except:
                r = requests.get(proxy_api, timeout=10)

            if r.status_code == 200:
                try:
                    data = r.text.strip()
                    if not data:
                        print("[太平通]代理API返回空数据")
                        return None

                    proxy_list = []
                    for line in data.split('\r\n'):
                        if ':' in line:
                            ip, port = line.split(':')
                            proxy_str = f'http://{ip}:{port}'
                            proxy_list.append({
                                'http': proxy_str,
                                'https': proxy_str
                            })

                    if proxy_list:
                        return random.choice(proxy_list)
                    else:
                        print("[太平通]未找到可用代理")
                        return None

                except Exception as e:
                    print(f"[太平通]解析代理返回数据失败: {e}")
                    return None
            else:
                print(f"[太平通]获取代理失败,状态码: {r.status_code}")
                return None
        except Exception as e:
            print(f"[太平通]获取代理发生错误: {e}")
            return None

    def _make_request(self, method, url, **kwargs):
        """统一的请求方法"""
        try:
            use_proxy = False
            if 'campaignsms/couponAndsign' in url:  # 签到任务
                use_proxy = True
            elif 'campaignsms/goldParty' in url:  # 金币任务
                use_proxy = True
            elif 'campaignsms/coinBubble' in url:  # 金币气泡
                use_proxy = True

            max_retries = 3 if use_proxy else 1  # 使用代理时最多重试3次
            retry_count = 0

            while retry_count < max_retries:
                try:
                    if use_proxy and retry_count < max_retries - 1:  # 最后一次重试不使用代理
                        proxies = self.get_proxy()  # 每次重试都获取新的代理
                        if proxies:
                            kwargs['proxies'] = proxies
                            kwargs['timeout'] = 15
                    else:
                        kwargs['timeout'] = 10
                        if 'proxies' in kwargs:
                            del kwargs['proxies']

                    if method.lower() == 'get':
                        r = requests.get(url, **kwargs)
                    else:
                        r = requests.post(url, **kwargs)

                    if r.status_code == 200:
                        return r
                    else:
                        print(f"[太平通]请求失败,状态码: {r.status_code}")

                except Exception as e:
                    error_msg = str(e).lower()
                    if "timeout" in error_msg:
                        print(f"[太平通]第{retry_count + 1}次请求超时,尝试更换代理")
                    elif "proxy" in error_msg:
                        print(f"[太平通]第{retry_count + 1}次代理连接失败,尝试更换代理")
                    else:
                        print(f"[太平通]第{retry_count + 1}次请求错误: {e}")

                    if retry_count == max_retries - 1:
                        return None

                retry_count += 1
                if retry_count < max_retries:
                    time.sleep(2)  # 重试前等待2秒

            return None

        except Exception as e:
            print(f"[太平通]请求发生未预期错误: {e}")
            return None

    def sign(self):
        try:
            r = requests.post(
                "https://ecustomer.cntaiping.com/campaignsms/couponAndsign",
                headers=self.headers,
                json={}
            )
            self.headers[
                'User-Agent'] = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;yuangongejia#ios#kehutong#CZBIOS'
            r = requests.post(
                "https://ecustomer.cntaiping.com/campaignsms/couponAndsign",
                headers=self.headers,
                json={}
            )
            success = r.json().get('success', None)
            if success:
                self.headers[
                    'User-Agent'] = "Mozilla/5.0 (Linux; Android 13; Pixel 4 XL Build/TP1A.220905.004; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/119.0.6045.163 Mobile Safari/537.36;yuangongejia#android#kehutong;webank/h5face;webank/1.0;netType:NETWORK_WIFI;appVersion:334;packageName:com.cntaiping.tpapp"
                return True
            elif not success and '已过期' in r.text:
                return '失效'
            else:
                return False
        except Exception as e:
            return e

    def get_rwlist(self):
        try:
            r = self._make_request(
                'post',
                "https://ecustomer.cntaiping.com/campaignsms/goldParty/task/list",
                headers=self.headers,
                json={
                    'activityNumber': 'goldCoinParty',
                    'rewardFlag': '1',
                    'openMsgRemind': 0,
                }
            )
            success = r.json().get('success', None)
            if success:
                data = r.json()['data']['taskList']
                return data
            else:
                return False
        except Exception as e:
            return e

    def finish(self):
        try:
            r = self._make_request(
                'post',
                "https://ecustomer.cntaiping.com/campaignsms/goldParty/task/finish",
                headers=self.headers,
                json={'taskIds': [self.taskid], })
            success = r.json().get('success', None)
            if success:
                return True
            else:
                return False
        except Exception as e:
            return e

    def add(self):
        try_count = 2
        while try_count > 0:
            try:
                r = self._make_request(
                    'post',
                    "https://ecustomer.cntaiping.com/campaignsms/goldParty/goldCoin/add",
                    headers=self.headers,
                    json={
                        'taskIds': [self.taskid]
                    }
                )
                success = r.json().get('success', None)
                if success:
                    return True
                elif '已经获取' in r.text:
                    return False
                elif not success and '火爆' in r.text:
                    try_count -= 1
                    if try_count == 0:
                        return False
                    self.headers['User-Agent'] = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;yuangongejia#ios#kehutong#CZBIOS'
                    continue
                else:
                    return False
            except Exception as e:
                return e

    def run_rw(self):
        data = self.get_rwlist()
        if isinstance(data, list):
            for i in data:
                time.sleep(random.randint(1, 3))
                taskStatus = i['taskStatus']
                self.taskid = i['taskId']
                self.rwname = i['name']
                if taskStatus == 2:
                    pass
                elif taskStatus == 0 and self.rwname != '浏览资讯':
                    if self.finish() is True:
                        time.sleep(random.randint(1, 3))
                        if self.add() is True:
                            time.sleep(random.randint(1, 3))
                        else:
                            return False
                    else:
                        return False
                elif taskStatus == 1 and self.rwname != '浏览资讯':
                    self.add()
                    time.sleep(random.randint(1, 3))
            return True
        else:
            return False

    def get_ydlist(self):
        try:
            r = self._make_request(
                'post',
                self.ydlisturl,
                headers=self.headers,
                json={
                    "plugInId": "701b3099297148a8ba979ad9c982b561",
                    "trackDesc": "赚金币任务",
                    "city": "1",
                    "pageSize": 20,
                    "type": "GENERAL_PLUGIN"
                }
            )
            success = r.json().get('success', None)
            if success:
                data = r.json()['data']
                return data
            else:
                return False
        except Exception as e:
            return e

    def coinInfoV2(self):
        try:
            r = self._make_request(
                'post',
                "https://ecustomer.cntaiping.com/informationms/app/v2/article/web/coinInfoV2",
                headers=self.headers,
                json={
                    'articleId': self.ydid,
                    'source': 'TPT',
                    'detailUrl': f'https://ecustomercdn.itaiping.com/static/newscontent/#/info?articleId={self.ydid}&source=TPT&x_utmId=10013&x_businesskey=articleId',
                    'deviceId': '',
                    'version': 'V2'
                }
            )
            success = r.json().get('success', None)
            if success:
                return True
            else:
                return False
        except Exception as e:
            return e

    def zl(self):
        try:
            for i in self.zldatas:
                time.sleep(random.randint(1, 3))
                r = self._make_request(
                    'post',
                    "https://ecustomer.cntaiping.com/informationms/app/v2/article/web/coinInfoV2",
                    headers={
                        'Host': 'ecustomer.cntaiping.com',
                        'accept': 'application/json', 'x-ac-channel-id': 'KHT',
                        'x-ac-black-box': 'iWPVl1701438414PrzwzjCHQw1',
                        'x-ac-mc-type': 'gateway.user',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309092b) XWEB/9105 Flue',
                        'x-ac-token-ticket': '',
                        'content-type': 'application/json',
                        'Origin': 'https://ecustomercdn.itaiping.com',
                        'Sec-Fetch-Site': 'cross-site',
                        'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty',
                        'Referer': 'https://ecustomercdn.itaiping.com/',
                        'Accept-Language': 'zh-CN,zh;q=0.9'
                    },
                    json=i
                )
                success = r.json().get('success', None)
                if success:
                    return True
                else:
                    return False
        except Exception as e:
            return e

    def gold(self):
        try:
            r = self._make_request(
                'post',
                "https://ecustomer.cntaiping.com/informationms/app/v2/read/gold",
                headers=self.headers,
                json={
                    "articleId": self.ydid,
                    "source": "TPT"
                }
            )
            success = r.json().get('success', None)
            if success:
                return True
            else:
                return False
        except Exception as e:
            return e

    def queryList(self):
        try:
            r = self._make_request(
                'post',
                'https://ecustomer.cntaiping.com/campaignsms/coinBubble/queryList',
                headers=self.headers,
                json={}
            )
            success = r.json().get('success', None)
            if success:
                data = r.json()['data']
                if data:
                    return True
                else:
                    return '没有待领取金币'
            else:
                return r.json()['msg']
        except Exception as e:
            return e

    def getAllCoins(self):
        try_count = 2
        while try_count > 0:
            try:
                r = self._make_request(
                    'post',
                    "https://ecustomer.cntaiping.com/campaignsms/coinBubble/getAllCoins",
                    headers=self.headers,
                    json={}
                )
                success = r.json().get('success', None)
                if success:
                    return True
                elif not success and '火爆' in r.text:
                    try_count -= 1
                    if try_count == 0:
                        return False
                    self.headers['User-Agent'] = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;yuangongejia#ios#kehutong#CZBIOS'
                    continue
                else:
                    return r.json()['msg']
            except Exception as e:
                return e

    def getShareInfo(self):
        try:
            r = self._make_request(
                'post',
                "https://ecustomer.cntaiping.com/informationms/app/v2/share/getShareInfo",
                headers=self.headers,
                json={
                    "articleId": self.ydid,
                    "source": "TPT",
                    "shareFlag": True
                }
            )
            success = r.json().get('success', None)
            if success:
                return r.json()['data']['tagUrl']
            else:
                return False
        except Exception as e:
            return e

    def run_yd(self):
        n = 0
        data = self.get_ydlist()
        if isinstance(data, list):
            for i in range(len(data)):
                time.sleep(random.randint(1, 3))
                n += 1
                d = data[i]['cell']['0'][0]
                self.ydname = d['title']
                self.ydid = d['contentId']

                if self.llzx < 14:
                    if self.coinInfoV2() is True:
                        time.sleep(random.randint(1, 3))
                        if self.gold() is True:
                            time.sleep(random.randint(1, 3))
                        else:
                            return False
                    else:
                        return False
                getShareInfo = self.getShareInfo()
                if isinstance(getShareInfo, str):
                    shareCode = getShareInfo.split('shareCode=')[1].split('&')[0]
                    articleId = getShareInfo.split('articleId=')[1].split('&')[0]
                    zldata = {
                        'articleId': articleId,
                        'source': 'TPT',
                        'detailUrl': getShareInfo,
                        'deviceId': '',
                        "shareCode": shareCode,
                        'version': 'V2'
                    }
                    self.zldatas.append(zldata)
                else:
                    return False
            return True
        else:
            return False

    def queryUserPoints(self):
        try:
            r = self._make_request(
                'post',
                "https://ecustomer.cntaiping.com/campaignsms/integral/queryUserPoints",
                headers=self.headers,
                json={
                    "sourceOrganId": "932"
                }
            )
            success = r.json().get('success', None)
            if success:
                return r.json()['data']['scoreAccountInfo']['availableScore']
            else:
                return False
        except Exception as e:
            return e

    def is_in_current_month(self):
        date = datetime.strptime(self.validDate, '%Y-%m-%d 00:00:00')
        current_date = datetime.now()
        return date.year == current_date.year and date.month == current_date.month

    def cx(self):
        try:
            r = self._make_request(
                'post',
                'https://ecustomer.cntaiping.com/campaignsms/integral/queryIntegralDetailList',
                headers=self.headers,
                json={
                    'pageNo': 1,
                    'pageSize': 100,
                    'typePo': '3',
                }
            )
            success = r.json().get('success', None)
            if success:
                dqjb = self.queryUserPoints()
                data = r.json()['data']['list']
                today = datetime.now().strftime('%Y-%m-%d')
                coins = 0
                llzx = 0
                hyyd = 0
                rcrw = 0
                for i in data:
                    coin = i['num']
                    effectDate = i['effectDate']
                    memo = i['memo']
                    if effectDate == today:
                        if memo == '浏览资讯':
                            llzx += 1
                        elif memo == '好友阅读':
                            hyyd += 1
                        elif memo in ['给太平树浇水', '分享海报', '回执签收', '邀请注册']:
                            rcrw += 1
                        coins += coin
                        continue
                    else:
                        break
                return dqjb, coins, llzx, hyyd, rcrw
            else:
                return r.json()['msg']
        except Exception as e:
            return e

    def exhibitionTopic(self):
        try:
            r = self._make_request(
                'post',
                "https://ecustomer.cntaiping.com/campaignsms/tPkTopicAppointment/exhibitionTopic",
                headers=self.headers,
                json={
                    "pageNo": 1,
                    "pageSize": 200
                }
            )
            success = r.json().get('success', None)
            if success:
                return r.json()['data']
            else:
                msg = r.json()['msg']
                return msg
        except Exception as e:
            return e

    def standInLineTopic(self):
        try:
            r = self._make_request(
                'post',
                "https://ecustomer.cntaiping.com/campaignsms/tPkTopicAppointment/standInLineTopic",
                headers=self.headers,
                json={
                    "joinPoint": self.joinPoint,
                    "id": self.htid,
                    "dataFrom": 0
                }
            )
            success = r.json().get('success', None)
            print(r.json())
            if success:
                return True
            else:
                msg = r.json()['msg']
                return msg
        except Exception as e:
            return e

    def main(self):
        try:
            jrjb = 0
            dqjb = 0

            sign = self.sign()
            if sign is True:
                cxjg = self.cx()
                if isinstance(cxjg, tuple):
                    dqjb, jrjb, self.llzx, self.hyyd, rcrw = cxjg
                    if self.queryList() is True:
                        self.getAllCoins()
                    sender.reply(f'🔔开始运行: {self.name}\n💰今日金币: {jrjb}\n💰当前金币: {dqjb}')
                else:
                    sender.reply(f'🔔{self.name}: 查询金币时异常\n🔔{cxjg}')
                    return self.name, '异常'

                exhibitionTopic = self.exhibitionTopic()
                if isinstance(exhibitionTopic, list):
                    for i in exhibitionTopic:
                        self.htid = i['id']
                        self.joinPoint = i['joinWin']
                        isParticipateIn = i['isParticipateIn']
                        prizeStatus = i['prizeStatus']
                        if isParticipateIn is None and prizeStatus == 0:
                            self.standInLineTopic()
                            time.sleep(random.randint(5, 10))
                            continue
                        else:
                            continue

                a = 0
                while True:
                    cxjg = self.cx()
                    if isinstance(cxjg, tuple):
                        dqjb, jrjb, self.llzx, self.hyyd, rcrw = cxjg
                    else:
                        sender.reply(f'🔔{self.name}: 查询金币时异常\n🔔{cxjg}')
                        return self.name, '异常'
                    a += 1
                    if rcrw < 3:
                        if not self.run_rw():
                            cxjg_end = self.cx()
                            if isinstance(cxjg_end, tuple):
                                dqjb_end, jrjb_end = cxjg_end[0], cxjg_end[1]
                                if jrjb_end < 10:
                                    msg = f"⚠️ 账号【{self.name}】运行异常，今日金币为{jrjb_end}，请打开太平通APP后再试！"

                                    hbtz = sg.bucketGet('bd_tptconfig', 'hbtz')
                                    if hbtz and hbtz.lower() == 'true':
                                        try:
                                            if self.user:  # 确保self.user存在
                                                push_msg = f"🔔账号【{self.name}】运行异常，今日金币为{jrjb_end}，请打开太平通APP后再试！"

                                                sg.push('wb', '', self.user, '', push_msg)
                                                sg.push('tg', '', self.user, '', push_msg)
                                                sg.push('qq', '', self.user, '', push_msg)
                                                sg.push('qb', '', self.user, '', push_msg)
                                                sg.push('wx', '', self.user, '', push_msg)

                                        except Exception as e:
                                            print(f"通知用户失败: {e}")

                                    if sender.getUserID() != self.user:
                                        sender.reply(msg)

                                    sender.reply(f'🎉运行完成: {self.name}\n💰今日金币: {jrjb_end}(账号火爆)\n💰当前金币: {dqjb_end}')
                                    return self.name, '火爆'
                            sender.reply(f'🎉运行完成: {self.name}\n💰今日金币: {jrjb}\n💰当前金币: {dqjb}')
                            return self.name, jrjb, dqjb

                    if self.llzx >= 14 and self.hyyd >= 6:
                        sender.reply(f'🎉运行完成: {self.name}\n💰今日金币: {jrjb}\n💰当前金币: {dqjb}')
                        return self.name, jrjb, dqjb

                    elif a >= 3:
                        sender.reply(f'🎉运行完成: {self.name}\n💰今日金币: {jrjb}\n💰当前金币: {dqjb}')
                        return self.name, jrjb, dqjb
                    else:
                        self.ydlisturl = f"https://ecustomer.cntaiping.com/informationms/app/config/get/{a}"
                        self.run_yd()
                        a = 0
                        for zl_data in self.zldatas:
                            a += 1
                            time.sleep(random.randint(1, 3))
                            r = self._make_request(
                                'post',
                                "https://ecustomer.cntaiping.com/informationms/app/v2/article/web/coinInfoV2",
                                headers={
                                    'Host': 'ecustomer.cntaiping.com',
                                    'accept': 'application/json', 'x-ac-channel-id': 'KHT',
                                    'x-ac-black-box': 'iWPVl1701438414PrzwzjCHQw1',
                                    'x-ac-mc-type': 'gateway.user',
                                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309092b) XWEB/9105 Flue',
                                    'x-ac-token-ticket': '',
                                    'content-type': 'application/json',
                                    'Origin': 'https://ecustomercdn.itaiping.com',
                                    'Sec-Fetch-Site': 'cross-site',
                                    'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty',
                                    'Referer': 'https://ecustomercdn.itaiping.com/',
                                    'Accept-Language': 'zh-CN,zh;q=0.9'
                                },
                                json=zl_data
                            )
                            success = r.json().get('success', None)
                            if success:
                                pass
                            else:
                                return False
                        self.zldatas = []
                        if self.queryList() is True:
                            self.getAllCoins()
                        continue
                else:
                    sender.reply(f'🔔{self.name}: 运行任务时异常\n🔔{sign}')
                    return self.name, sign

            try:
                if self.sqsj:
                    sqsj_date = datetime.strptime(self.sqsj, "%Y-%m-%d")
                    now = datetime.now()
                    days_left = (sqsj_date - now).days

                    if 0 <= days_left <= 3:
                        msg = f"⚠️ 账号【{self.name}】授权即将到期!\n剩余时间: {days_left}天\n到期时间: {self.sqsj}\n请及时续费以免影响使用"

                        if self.user:
                            try:
                                user_sender = sg.Sender(self.user)
                                user_sender.reply(msg)
                            except:
                                pass

                    elif days_left < 0:
                        msg = f"⚠️ 账号【{self.name}】授权已经过期!\n到期时间: {self.sqsj}\n请及时续费以继续使用"

                        if self.user:
                            try:
                                user_sender = sg.Sender(self.user)
                                user_sender.reply(msg)
                            except:
                                pass

            except Exception as e:
                print(f"检查授权到期时发生错误: {e}")

            sender.reply(f'🎉运行完成: {self.name}\n💰今日金币: {jrjb}\n💰当前金币: {dqjb}')
            return self.name, jrjb, dqjb

        except Exception as e:
            sender.reply(f'🔔{self.name}: 运行任务时异常\n🔔{e}')
            return self.name, e


if __name__ == '__main__':
    senderID = sg.getSenderID()
    sender = sg.Sender(senderID)
    user = sender.getUserID()
    message = sender.getMessage()
    atm_tpt = ATM_tpt(user, sender)
    if message == '太平上车':
        atm_tpt.tpsc()
    elif message == '太平管理':
        atm_tpt.tpgl()
    elif message == '太平查询':
        atm_tpt.tpcx()
    elif message == '太平运行':
        if sender.isAdmin():
            atm_tpt.tpyx()
    elif message == '太平配置':
        if sender.isAdmin():
            atm_tpt.tppz()
    elif message == '太平教程':
        jcurl = sg.bucketGet('bd_tptconfig', 'jcurl')
        if jcurl == '':
            jcurl = 'https://www.yuque.com/yuqueyonghulzdzov/fuzugi/xvy3lp28apxnpvoq?singleDoc#'

        sender.reply(f"""=====太平通使用教程=====
验证码登录和抓包登录二选一
💰 收益说明:
- 每天约100金币 ≈ 1RMB
- 可兑换话费、e卡、会员等

📖 详细教程: {jcurl}

🔑 常用指令:
- 太平上车: 添加账号
- 太平管理: 管理账号
- 太平查询: 查询收益
========================""")
    elif message == '太平版本':
        if sender.isAdmin():
            sender.reply(
                f"""=====太平通插件信息=====
📌 当前版本: V6.60

🆕 更新内容:
• 支持批量授权用户
• 新增火爆推送通知
• 新增授权过期提醒
• 新增定时检测功能
• 支持积分开通功能
• 新增代理IP功能
• 修复验证码登录

📱 用户指令:
• 太平上车: 添加账号
• 太平管理: 管理账号
• 太平查询: 查询收益

⚙️ 管理员指令:
• 太平配置: 插件配置
• 太平运行: 一键运行
• 太平授权: 账号授权
• 太平检测: 授权过期检测
========================""")
    elif message == '太平授权':
        if sender.isAdmin():
            atm_tpt.tpsq()
    elif message == '太平检测':
        if sender.isAdmin():
            atm_tpt.tpjc()
    else:
        exit(0)
