# [title: 小快手]
# [name: xiaoKuaiShou]
# [language: python]
# [class: 任务]
# [author: linzixuan]
# [version: v5.2.5]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^快手登录$|^快手登陆$|^快手查询$|^快手管理$|^快手教程$|^快手后台$|^快手分成$|^快手$]
# [cron: 0 0 8,10,22 * * *]
# [icon: http://5b0988e595225.cdn.sohucs.com/images/20190724/f8f8ace898584a2dbd3f20c2d2822c96.jpeg]
# [description: 小快手V5.0全新重构；✨ 支持极速版和普通版独立管理；📊 完善的后台管理和数据统计；🌐 支持代理IP配置；格式：备注#Cookie#Salt#代理信息]
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
    'dd_ks_dd_ks_qlname': form.string().title('设置对接容器').default('').description('你的变量需要添加到的容器？参数用丨分割'),
    'dd_ks_ks_fast_varname': form.string().title('极速版变量名称').default('').description('青龙容器内快手极速版的变量名'),
    'dd_ks_ks_normal_varname': form.string().title('普通版变量名称').default('').description('青龙容器内快手普通版的变量名'),
    'dd_ks_allow_proxy': form.boolean().title('是否允许填写代理').default(False).description('是否允许用户在提交时填写代理IP'),
    'dd_ks_share_rate': form.string().title('分成比例').default('').description('分成比例（0-100），例如55表示平台收取55%，仅分成模式生效'),
})
_CONFIG_FIELD_MAP = {
    ('dd_ks', 'dd_ks_qlname'): 'dd_ks_dd_ks_qlname',
    ('dd_ks', 'ks_fast_varname'): 'dd_ks_ks_fast_varname',
    ('dd_ks', 'ks_normal_varname'): 'dd_ks_ks_normal_varname',
    ('dd_ks', 'allow_proxy'): 'dd_ks_allow_proxy',
    ('dd_ks', 'share_rate'): 'dd_ks_share_rate',
}

import re
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
import requests
import time
import json
import hashlib

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()
uservalue = sg.bucketGet(bucket='dd_ks_user', key=userid)


def getusercontent():
    """获取用户配置"""
    dd_ks_qlname = sg.bucketGet('dd_ks', 'dd_ks_qlname') or ''
    ks_fast_varname = sg.bucketGet('dd_ks', 'ks_fast_varname') or 'ksToken_fast'
    ks_normal_varname = sg.bucketGet('dd_ks', 'ks_normal_varname') or 'ksToken'
    allow_proxy = sg.bucketGet('dd_ks', 'allow_proxy') or 'true'
    allow_proxy = allow_proxy.lower() == 'true'

    dd_managecommand = sg.bucketGet('dd_ks', 'dd_managecommand') or '快手管理'
    dd_querycommand = sg.bucketGet('dd_ks', 'dd_querycommand') or '快手查询'
    dd_signcommand = sg.bucketGet('dd_ks', 'dd_signcommand') or '快手登录'

    payment_mode = ('2099-12-31' or '月付').strip()
    if payment_mode not in ['月付', '天付', '分成']:
        payment_mode = '月付'

    ksVipmoney = Decimal(sg.bucketGet('dd_ks', 'ksVipmoney') or '1')
    ksDaymoney = Decimal(sg.bucketGet('dd_ks', 'ksDaymoney') or '0.05')
    kscoin = int(sg.bucketGet('dd_ks', 'kscoin') or '0')

    use_ma_pay = '2099-12-31' or 'false'
    use_ma_pay = use_ma_pay.lower() == 'true'

    share_rate = int(sg.bucketGet('dd_ks', 'share_rate') or '55')
    share_allow_coin_pay = '2099-12-31' or 'false'
    share_allow_coin_pay = share_allow_coin_pay.lower() == 'true'

    return (ks_fast_varname, ks_normal_varname, allow_proxy, dd_ks_qlname,
            dd_managecommand, dd_querycommand, dd_signcommand,
            payment_mode, ksVipmoney, ksDaymoney, kscoin, use_ma_pay, share_rate, share_allow_coin_pay)

def verify_account_fast(cookie_str):
    """验证极速版账号有效性"""
    cookie_str = cookie_str.replace('kpn=KUAISHOU', 'kpn=NEBULA')

    url = "https://nebula.kuaishou.com/rest/n/nebula/activity/earn/overview/basicInfo?source=bottom_guide_first"

    headers = {
        'Host': 'nebula.kuaishou.com',
        'User-Agent': 'kwai-android aegon/4.29.0',
        'Cookie': cookie_str,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        response = requests.get(url, headers=headers, timeout=12)
        result = response.json()

        if result.get('result') == 1 and result.get('data'):
            data = result['data']
            nickname = data.get('userData', {}).get('nickname', '未知')
            total_coin = data.get('totalCoin', 0)
            all_cash = data.get('allCash', 0)

            return True, {
                'nickname': nickname,
                'coin': total_coin,
                'cash': all_cash
            }
        else:
            return False, "账号验证失败"

    except Exception as e:
        return False, f"请求异常: {str(e)}"

def verify_account_normal(cookie_str, default_nickname='未知'):
    """验证普通版账号有效性"""
    cookie_str = cookie_str.replace('kpn=NEBULA', 'kpn=KUAISHOU')

    url = "https://encourage.kuaishou.com/rest/wd/encourage/account/basicInfo"

    headers = {
        'Host': 'encourage.kuaishou.com',
        'User-Agent': 'kwai-android aegon/4.27.0',
        'Cookie': cookie_str,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        result = response.json()

        if result.get('result') == 1 and result.get('data'):
            data = result['data']
            nickname = data.get('userData', {}).get('nickname') or default_nickname
            total_coin = data.get('coinAmount', 0)
            all_cash = data.get('cashAmountDisplay', 0)

            return True, {
                'nickname': nickname,
                'coin': total_coin,
                'cash': all_cash
            }
        else:
            return False, "账号验证失败"

    except Exception as e:
        return False, f"请求异常: {str(e)}"

def parse_cookies(cookie_str):
    """解析Cookie字符串为字典"""
    cookies = {}
    for item in cookie_str.split(';'):
        if '=' in item:
            key, value = item.strip().split('=', 1)
            cookies[key] = value
    return cookies

def msg_box(title, content, footer=""):
    """生成统一格式的消息框"""
    msg = f"====={title}=====\n{content}"
    if footer:
        msg += f"\n------------------\n{footer}"
    msg += "\n=================="
    return msg

def select_version(prompt="请选择版本"):
    """通用版本选择，返回 (version_choice, version_name, varname) 或 None"""
    menu = msg_box("选择快手版本", f"{prompt}\n------------------\n[1] 某手极速版\n[2] 某手普通版", "回复数字选择\n回复 q 退出")
    sender.reply(menu)
    choice = sender.input(120000, 1, False)
    if not choice or choice.lower() == 'q':
        return None
    if choice == '1':
        return ('1', "某手极速版", ks_fast_varname)
    elif choice == '2':
        return ('2', "某手普通版", ks_normal_varname)
    return None

def get_version_accounts(accounts, version_choice):
    """获取指定版本的账号列表"""
    result = []
    for acc in accounts:
        full_ck = sg.bucketGet('dd_ks_token', acc)
        if full_ck:
            info = parse_token(full_ck)
            if info and info['version'] == version_choice:
                result.append(acc)
    return result

def parse_token(full_ck):
    """
    解析token字符串
    新格式: 版本
    旧格式: 备注

    返回: {
        'version': '1' or '2',  # 1=极速版, 2=普通版
        'name': '备注',
        'cookie': 'cookie字符串',
        'salt': 'salt',
        'proxy': '代理信息' or None
    }
    """
    if not full_ck:
        return None

    parts = full_ck.split('#')

    if len(parts) >= 4 and parts[0] in ['1', '2']:
        return {
            'version': parts[0],
            'name': parts[1] if len(parts) >= 2 else '未知',
            'cookie': parts[2] if len(parts) >= 3 else None,
            'salt': parts[3] if len(parts) >= 4 else None,
            'proxy': parts[4] if len(parts) >= 5 else None
        }
    else:
        return {
            'version': '1',  # 默认极速版
            'name': parts[0] if len(parts) >= 1 else '未知',
            'cookie': parts[1] if len(parts) >= 2 else None,
            'salt': parts[2] if len(parts) >= 3 else None,
            'proxy': parts[3] if len(parts) >= 4 else None
        }

def token_to_qinglong_format(full_ck):
    """
    将token转换为青龙格式（去掉版本标识）
    新格式: 版本
    旧格式: 备注
    """
    if not full_ck:
        return full_ck

    token_info = parse_token(full_ck)
    if not token_info:
        return full_ck

    result = f"{token_info['name']}#{token_info['cookie']}#{token_info['salt']}"
    if token_info['proxy']:
        result += f"#{token_info['proxy']}"

    return result

def parse_proxy_to_url(proxy_str):
    """
    解析代理字符串为标准URL格式
    支持三种格式:
    1. IP|端口|用户名|密码|过期时间 -> http://用户名:密码@IP:端口
    2. socks5://账号:密码@ip:端口 -> socks5://账号:密码@ip:端口
    3. http://账号:密码@ip:端口 -> http://账号:密码@ip:端口

    返回: (proxy_url, proxy_type) 或 (None, error_msg)
    """
    if not proxy_str:
        return None, "代理信息为空"

    proxy_str = proxy_str.strip()

    if proxy_str.startswith('socks5://') or proxy_str.startswith('http://'):
        try:
            if proxy_str.startswith('socks5://'):
                protocol = 'socks5'
                rest = proxy_str[9:]
            else:
                protocol = 'http'
                rest = proxy_str[7:]

            if '@' not in rest:
                return None, "URL格式错误，缺少@符号"

            auth_part, host_part = rest.rsplit('@', 1)

            if ':' not in auth_part:
                return None, "URL格式错误，缺少用户名或密码"
            user, pwd = auth_part.split(':', 1)

            if ':' not in host_part:
                return None, "URL格式错误，缺少端口"
            ip, port = host_part.rsplit(':', 1)

            port_num = int(port)
            if port_num < 1 or port_num > 65535:
                return None, "端口无效"

            if not user or not pwd:
                return None, "用户名或密码为空"

            return f"{protocol}://{user}:{pwd}@{ip}:{port}", protocol
        except ValueError:
            return None, "URL格式解析失败"

    parts = proxy_str.split('|')
    if len(parts) == 5:
        ip, port, user, pwd, _ = parts
        try:
            port_num = int(port)
            if port_num < 1 or port_num > 65535:
                return None, "端口无效"
        except ValueError:
            return None, "端口必须是数字"

        if not user or not pwd:
            return None, "用户名或密码为空"

        return f"http://{user}:{pwd}@{ip}:{port}", "http"

    return None, "格式错误，不支持的代理格式"

def validate_proxy(proxy_str):
    """
    验证代理格式和连接
    支持三种格式:
    1. IP|端口|用户名|密码|过期时间
    2. socks5://账号:密码@ip:端口
    3. http://账号:密码@ip:端口
    """
    if not proxy_str:
        return False, "代理信息为空"

    proxy_url, result = parse_proxy_to_url(proxy_str)
    if proxy_url is None:
        return False, result

    proxy_type = result

    try:
        if proxy_type == 'socks5':
            proxies = {'http': proxy_url, 'https': proxy_url}
        else:
            proxies = {'http': proxy_url, 'https': proxy_url}

        r = requests.get("https://d.pcs.baidu.com/rest/2.0/pcs/file?method=locateupload",
            proxies=proxies, timeout=10,
            headers={'User-Agent': 'Mozilla/5.0'})
        if r.status_code == 200:
            try:
                d = r.json()
                if d.get('error_code', -1) == 0:
                    return True, f"✅ 代理验证通过(IP:{d.get('client_ip', '未知')}, 类型:{proxy_type})"
            except:
                pass
            return True, f"✅ 代理可用(类型:{proxy_type})"
        return False, f"代理连接失败({r.status_code})"
    except requests.exceptions.Timeout:
        return False, "代理连接超时"
    except requests.exceptions.ProxyError:
        return False, "代理连接失败"
    except Exception as e:
        return False, f"代理错误: {str(e)}"

def query_account_fast(cookie_str, proxy_str=None):
    """查询极速版账号详情"""
    cookie_str = cookie_str.replace('kpn=KUAISHOU', 'kpn=NEBULA')

    url = "https://nebula.kuaishou.com/rest/n/nebula/account/overview"

    headers = {
        'Host': 'nebula.kuaishou.com',
        'User-Agent': 'kwai-android aegon/4.29.0',
        'Cookie': cookie_str,
        'Accept': 'application/json, text/plain, */*'
    }

    proxies = None
    if proxy_str:
        proxy_url, proxy_type = parse_proxy_to_url(proxy_str)
        if proxy_url:
            proxies = {'http': proxy_url, 'https': proxy_url}

    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=12)
        result = response.json()

        if result.get('result') == 1 and result.get('data'):
            data = result['data']

            all_coin_records = []
            coin_page = data.get('coinAccountPage', {})
            if coin_page.get('data'):
                all_coin_records = coin_page['data']

            cash_records = []
            cash_page = data.get('cashAccountPage', {})
            if cash_page.get('data'):
                cash_records = cash_page['data'][:3]

            return {
                'success': True,
                'coinBalance': data.get('coinBalance', '0'),
                'cashBalance': data.get('cashBalance', '0'),
                'accumulativeAmount': data.get('accumulativeAmount', '0'),
                'accountState': data.get('accountState', 'UNKNOWN'),
                'coinRecords': all_coin_records[:5],  # 显示用（最近5条）
                'allCoinRecords': all_coin_records,   # 统计用（所有记录）
                'cashRecords': cash_records
            }
        return {'success': False, 'msg': '查询失败'}
    except Exception as e:
        return {'success': False, 'msg': str(e)}

def calculate_today_coins_fast(coin_records):
    return 0

def calculate_today_coins_normal(coin_records):
    return 0

def query_account_normal(cookie_str, proxy_str=None):
    """查询普通版账号详情"""
    cookie_str = cookie_str.replace('kpn=NEBULA', 'kpn=KUAISHOU')

    basic_url = "https://encourage.kuaishou.com/rest/wd/encourage/account/basicInfo"
    headers = {
        'Host': 'encourage.kuaishou.com',
        'User-Agent': 'kwai-android aegon/4.27.0',
        'Cookie': cookie_str,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    proxies = None
    if proxy_str:
        proxy_url, proxy_type = parse_proxy_to_url(proxy_str)
        if proxy_url:
            proxies = {'http': proxy_url, 'https': proxy_url}

    try:
        response = requests.get(basic_url, headers=headers, proxies=proxies, timeout=15)
        result = response.json()

        if result.get('result') != 1 or not result.get('data'):
            return {'success': False, 'msg': '查询失败'}

        data = result['data']
        coin_balance = data.get('coinAmount', 0)
        cash_balance = data.get('cashAmountDisplay', 0)
        nickname = data.get('userData', {}).get('nickname', '未知')

        coin_detail_url = "https://encourage.kuaishou.com/rest/wd/encourage/account/detail?sigCatVer=1&accountType=coin&cursor"
        coin_response = requests.get(coin_detail_url, headers=headers, proxies=proxies, timeout=10)
        coin_records = []
        all_coin_records = []
        if coin_response.status_code == 200:
            coin_result = coin_response.json()
            if coin_result.get('result') == 1 and coin_result.get('data', {}).get('datas'):
                all_coin_records = coin_result['data']['datas']  # 保存所有记录
                coin_records = all_coin_records[:5]

        cash_detail_url = "https://encourage.kuaishou.com/rest/wd/encourage/account/detail?sigCatVer=1&accountType=cash&cursor"
        cash_response = requests.get(cash_detail_url, headers=headers, proxies=proxies, timeout=10)
        cash_records = []
        if cash_response.status_code == 200:
            cash_result = cash_response.json()
            if cash_result.get('result') == 1 and cash_result.get('data', {}).get('datas'):
                cash_records = cash_result['data']['datas'][:3]

        return {
            'success': True,
            'coinBalance': coin_balance,
            'cashBalance': cash_balance,
            'nickname': nickname,
            'coinRecords': coin_records,  # 显示用（最近3条）
            'allCoinRecords': all_coin_records,  # 统计用（所有记录）
            'cashRecords': cash_records
        }
    except Exception as e:
        return {'success': False, 'msg': str(e)}

def query_accounts():
    """查询用户所有账号"""
    if not uservalue or len(uservalue) == 0:
        sender.reply("❌ 您还没有绑定账号\n请先使用 快手登录 绑定账号")
        return

    accounts = _sg_literal(uservalue)
    if not accounts:
        sender.reply("❌ 账号列表为空")
        return

    version_menu = """
=====选择查询版本=====
请选择要查询的版本
------------------
[1] 某手极速版
[2] 某手普通版
------------------
回复数字选择版本
回复"q"退出操作
=================="""
    sender.reply(version_menu)

    version_choice = sender.input(120000, 1, False)
    if not version_choice:
        sender.reply("⏰ 操作超时,已退出")
        return
    elif version_choice.lower() == 'q':
        sender.reply("✅ 已取消查询")
        return

    if version_choice not in ['1', '2']:
        sender.reply("❌ 无效的选择")
        return

    if version_choice == '1':
        version_name = "某手极速版"
        query_func = query_account_fast
    else:
        version_name = "某手普通版"
        query_func = query_account_normal

    version_accounts = []
    for account in accounts:
        full_ck = sg.bucketGet('dd_ks_token', account)
        if full_ck:
            token_info = parse_token(full_ck)
            if token_info and token_info['version'] == version_choice:
                version_accounts.append(account)

    if not version_accounts:
        sender.reply(f"❌ 您还没有绑定任何{version_name}账号")
        return

    account_list = f"====={version_name}账号列表=====\n"
    for idx, account in enumerate(version_accounts, 1):
        full_ck = sg.bucketGet('dd_ks_token', account)
        if full_ck:
            token_info = parse_token(full_ck)
            name = token_info['name'] if token_info else '未知'
            account_list += f"[{idx}] {name} (ID:{account})\n"
        else:
            account_list += f"[{idx}] ID:{account}\n"

    account_list += "------------------\n"
    account_list += "回复数字选择账号\n"
    account_list += "回复 0 查询所有账号\n"
    account_list += "回复 q 退出操作\n"
    account_list += "=================="
    sender.reply(account_list)

    account_choice = sender.input(120000, 1, False)
    if not account_choice:
        sender.reply("⏰ 操作超时,已退出")
        return
    elif account_choice.lower() == 'q':
        sender.reply("✅ 已取消查询")
        return

    try:
        account_idx = int(account_choice)
        if account_idx < 0 or account_idx > len(version_accounts):
            sender.reply(f"❌ 请输入 0-{len(version_accounts)} 之间的数字")
            return
    except:
        sender.reply("❌ 请输入数字")
        return

    if account_idx == 0:
        query_accounts_list = version_accounts
    else:
        query_accounts_list = [version_accounts[account_idx - 1]]

    for idx, account in enumerate(query_accounts_list, 1):
        full_ck = sg.bucketGet('dd_ks_token', account)
        if not full_ck:
            sender.reply(f"❌ 账号ID: {account}\n未找到Cookie信息")
            continue

        token_info = parse_token(full_ck)
        if not token_info or not token_info['cookie']:
            sender.reply(f"❌ 账号ID: {account}\nCookie格式错误")
            continue

        name = token_info['name']
        cookie = token_info['cookie']
        proxy_info = token_info['proxy']

        query_result = query_func(cookie, proxy_info)

        result_msg = f"====={version_name}查询结果=====\n"
        result_msg += f"📝 备注: {name}\n"
        result_msg += f"🆔 ID: {account}\n"

        if query_result['success']:
            if version_choice == '1':
                result_msg += f"💰 金币: {query_result['coinBalance']}\n"
                result_msg += f"💵 余额: {query_result['cashBalance']}元\n"
                result_msg += f"📊 累计: {query_result['accumulativeAmount']}元\n"

                if payment_mode == '分成':
                    is_paid, saved_revenue, saved_share = get_today_share_status(account)

                    if is_paid:
                        result_msg += f"💳 分成: 今日已结算({saved_share}元)\n"
                    else:
                        current_coins = float(query_result.get('coinBalance', 0))
                        manual_cash = detect_manual_cash_exchange(query_result.get('cashRecords', []))

                        if current_coins > 0 or manual_cash > 0:
                            current_revenue = round(current_coins / 10000, 2)
                            total_revenue = current_revenue + manual_cash
                            today_share = calculate_share_amount(total_revenue, share_rate)
                            if manual_cash > 0:
                                result_msg += f"💳 分成: 待结算(预计{today_share}元，含手动兑换{manual_cash}元)\n"
                            else:
                                result_msg += f"💳 分成: 待结算(预计{today_share}元)\n"
                        else:
                            result_msg += f"💳 分成: 待结算(预计0.0元)\n"
                else:
                    auth_status = '2099-12-31' or '未授权'
                    result_msg += f"🔐 授权: {auth_status}\n"

                if query_result.get('coinRecords'):
                    result_msg += "📝 金币明细(最近5条):\n"
                    for record in query_result['coinRecords']:
                        title = record.get('eventType', '未知')
                        amount = record.get('amount', '0')
                        date_str = ''
                        try:
                            create_time = record.get('createTime', '')
                            if create_time and isinstance(create_time, str):
                                parts = create_time.split('.')
                                if len(parts) >= 3:
                                    date_str = f"{parts[1]}-{parts[2].zfill(2)} "
                        except:
                            pass
                        try:
                            amt_val = float(amount)
                            symbol = '+' if amt_val >= 0 else ''
                        except:
                            symbol = '+'
                        result_msg += f"  • {date_str}{title}: {symbol}{amount}\n"

                if query_result.get('cashRecords'):
                    result_msg += "💸 现金明细(最近3条):\n"
                    for record in query_result['cashRecords']:
                        title = record.get('eventType', '未知')
                        amount = record.get('amount', '0')
                        date_str = ''
                        try:
                            create_time = record.get('createTime', '')
                            if create_time and isinstance(create_time, str):
                                parts = create_time.split('.')
                                if len(parts) >= 3:
                                    date_str = f"{parts[1]}-{parts[2].zfill(2)} "
                        except:
                            pass
                        result_msg += f"  • {date_str}{title}: {symbol}{amount}元\n"
            else:
                result_msg += f"💰 金币: {query_result['coinBalance']}\n"
                result_msg += f"💵 余额: {query_result['cashBalance']}元\n"

                if payment_mode == '分成':
                    is_paid, saved_revenue, saved_share = get_today_share_status(account)

                    if is_paid:
                        result_msg += f"💳 分成: 今日已结算({saved_share}元)\n"
                    else:
                        current_coins = float(query_result.get('coinBalance', 0))
                        manual_cash = detect_manual_cash_exchange(query_result.get('cashRecords', []))

                        if current_coins > 0 or manual_cash > 0:
                            current_revenue = round(current_coins / 10000, 2)
                            total_revenue = current_revenue + manual_cash
                            today_share = calculate_share_amount(total_revenue, share_rate)
                            if manual_cash > 0:
                                result_msg += f"💳 分成: 待结算(预计{today_share}元，含手动兑换{manual_cash}元)\n"
                            else:
                                result_msg += f"💳 分成: 待结算(预计{today_share}元)\n"
                        else:
                            result_msg += f"💳 分成: 待结算(预计0.0元)\n"
                else:
                    auth_status = '2099-12-31' or '未授权'
                    result_msg += f"🔐 授权: {auth_status}\n"

                if query_result.get('coinRecords'):
                    result_msg += "📝 金币明细(最近5条):\n"
                    for record in query_result['coinRecords']:
                        title = record.get('title', '未知')
                        amount = record.get('displayAmount', '0')
                        date_str = ''
                        try:
                            create_time = record.get('createTime', 0)
                            if create_time:
                                date_obj = datetime.fromtimestamp(create_time / 1000)
                                date_str = date_obj.strftime('%m-%d') + ' '
                        except:
                            pass
                        result_msg += f"  • {date_str}{title}: +{amount}\n"

                if query_result.get('cashRecords'):
                    result_msg += "💸 现金明细(最近3条):\n"
                    for record in query_result['cashRecords']:
                        title = record.get('title', '未知')
                        amount = record.get('displayAmount', '0')
                        direction = record.get('direction', 'IN')
                        symbol = '+' if direction == 'IN' else '-'
                        date_str = ''
                        try:
                            create_time = record.get('createTime', 0)
                            if create_time:
                                date_obj = datetime.fromtimestamp(create_time / 1000)
                                date_str = date_obj.strftime('%m-%d') + ' '
                        except:
                            pass
                        result_msg += f"  • {date_str}{title}: {symbol}{amount}元\n"
        else:
            result_msg += f"❌ 查询失败: {query_result.get('msg', '未知错误')}\n"

        result_msg += "=================="

        sender.reply(result_msg)

def bindaccount():
    """绑定账号 - 支持格式: 备注#cookie#salt 或 备注#cookie#salt#|端口|用户名|密码|过期时间"""

    version_menu = """
=====选择快手版本=====
请选择要登录的版本
------------------
[1] 某手极速版
[2] 某手普通版
------------------
回复数字选择版本
回复"q"退出操作
=================="""
    sender.reply(version_menu)

    version_choice = sender.input(120000, 1, False)
    if not version_choice:
        sender.reply("⏰ 操作超时,已退出")
        exit(0)
    elif version_choice.lower() == 'q':
        sender.reply("✅ 已取消登录")
        exit(0)

    if version_choice not in ['1', '2']:
        sender.reply("❌ 无效的选择")
        exit(0)

    if version_choice == '1':
        version_name = "某手极速版"
        target_varname = ks_fast_varname
    else:
        version_name = "某手普通版"
        target_varname = ks_normal_varname

    if allow_proxy:
        ck_guide = f"""
====={version_name}登录=====
请输入账号信息
📝 支持格式:
1. 备注#cookie#salt
2. 备注#cookie#salt#代理

🌐 代理格式支持:
• IP|端口|用户名|密码|过期时间
• socks5://账号:密码@IP:端口
• http://账号:密码@IP:端口
------------------
"""
    else:
        ck_guide = f"""
====={version_name}登录=====
请输入账号信息
📝 支持格式:
1. 备注#cookie#salt
2. 备注#cookie#salt#代理
------------------
"""
    sender.reply(ck_guide)

    while True:
        ck_input = sender.input(120000, 1, False)
        if not ck_input:
            sender.reply("⏰ 操作超时,已退出")
            exit(0)
        elif ck_input.lower() == 'q':
            sender.reply("✅ 已取消登录")
            exit(0)

        try:
            parts = ck_input.split('#')

            if len(parts) < 3:
                sender.reply("""
❌ 格式错误
------------------
正确格式: 备注
或: 备注#Cookie#Salt#代理信息""")
                exit(0)

            name = parts[0]
            ck = parts[1]
            salt_input = parts[2]
            proxy_input = parts[3] if len(parts) >= 4 else ""

            if proxy_input:
                proxy_valid, proxy_msg = validate_proxy(proxy_input)
                if not proxy_valid:
                    sender.reply(f"""
❌ 代理验证失败
------------------
{proxy_msg}
------------------
支持的代理格式:
1. IP|端口|用户名|密码|过期时间
   示例: 110.84.77.52|6855|user|pass|2025-12-19
2. socks5://账号:密码@IP:端口
   示例: socks5://user:pass@119.84.77.52:6855
3. http://账号:密码@IP:端口
   示例: http://user:pass@119.84.77.52:6855""")
                    exit(0)

                sender.reply(proxy_msg)

            if version_choice == '1':
                is_valid, result = verify_account_fast(ck)
            else:
                is_valid, result = verify_account_normal(ck, name)

            if is_valid:
                cookies = parse_cookies(ck)
                base_account = cookies.get('userId', 'unknown')
                if base_account == 'unknown':
                    sender.reply("❌ 无法获取账号信息")
                    exit(0)

                if payment_mode == '分成':
                    has_debt, total_debt, debts = check_uid_has_debt(base_account)
                    if has_debt:
                        debt_details = "\n".join([f"  • {d.get('date')}: {d.get('share_amount')}元" for d in debts[:5]])
                        if len(debts) > 5:
                            debt_details += f"\n  ... 共{len(debts)}条欠款记录"

                        sender.reply(f"""
=====无法提交=====
❌ 该快手账号存在未支付的分成欠款！

📝 欠款明细:
{debt_details}

💰 欠款总额: {total_debt}元
------------------
请先支付欠款后再提交账号
如需支付欠款，请检查配置
==================""")
                        exit(0)

                account = f"{base_account}_{version_choice}"

                nickname = result.get('nickname', name)
                coin = result.get('coin', 0)
                cash = result.get('cash', 0)

                full_ck = f"{version_choice}#{name}#{ck}#{salt_input}"
                if proxy_input:
                    full_ck += f"#{proxy_input}"

                is_new_account = False
                if len(uservalue) == 0:
                    is_new_account = True
                    sg.bucketSet('dd_ks_user', userid, str([account]))
                    sg.bucketSet('dd_ks_token', account, full_ck)
                    True
                else:
                    accounts = _sg_literal(uservalue)
                    if account not in accounts:
                        is_new_account = True
                        accounts.append(account)
                        sg.bucketSet('dd_ks_user', userid, str(accounts))
                        True
                    else:
                        is_new_account = False

                    sg.bucketSet('dd_ks_token', account, full_ck)

                accountVip = '2099-12-31'
                should_submit_to_qinglong = False

                if payment_mode == '分成':
                    should_submit_to_qinglong = True
                    auth_status = f'分成模式'
                elif payment_mode == '月付':
                    if accountVip and accountVip >= today_time:
                        should_submit_to_qinglong = True
                        auth_status = f'已授权至{accountVip}(月付)'
                    else:
                        should_submit_to_qinglong = False
                        auth_status = '未授权(月付)'
                else:
                    if accountVip and accountVip >= today_time:
                        should_submit_to_qinglong = True
                        auth_status = f'已授权至{accountVip}(天付)'
                    else:
                        should_submit_to_qinglong = False
                        auth_status = '未授权(天付)'

                if should_submit_to_qinglong:
                    qinglong_value = token_to_qinglong_format(full_ck)
                    Addenvs(osname=target_varname, value=qinglong_value, account=account, phone=name)

                action_type = "更新" if not is_new_account else "绑定"
                success_msg = f"""
====={action_type}成功=====
👤 昵称: {nickname}
🆔 账号ID: {account}
💰 金币数: {coin}
💵 余额: {cash}元
🔐 授权状态: {auth_status}
🌐 代理状态: {'已设置' if proxy_input else '未设置'}
------------------
提示: {'账号已添加至青龙' if should_submit_to_qinglong else '请先授权账号再使用'}
=================="""
                sender.reply(success_msg)
                break

            else:
                sender.reply(f"""
=====验证失败=====
❌ {result}
------------------
请检查Cookie是否有效!
==================""")
                exit(0)

        except Exception as e:
            sender.reply(f"""
=====绑定异常=====
请重试或检查配置
错误: {str(e)}
==================""")
            exit(0)

def seekql():
    """连接青龙"""
    if not dd_ks_qlname:
        sender.reply("❌ 未配置青龙信息")
        exit(0)

    qllist = dd_ks_qlname.split('丨')
    if len(qllist) != 3:
        sender.reply("❌ 青龙配置格式错误\n正确格式: Host丨ClientID丨ClientSecret")
        exit(0)

    QLurl, ClientID, ClientSecret = [x.strip() for x in qllist]

    if not all([QLurl, ClientID, ClientSecret]):
        sender.reply("❌ 青龙配置参数不完整")
        exit(0)

    if not QLurl.startswith(('http://', 'https://')):
        sender.reply("❌ 青龙地址格式错误")
        exit(0)

    qltoken = QLtoken(QLurl, ClientID, ClientSecret)
    return QLurl, qltoken

def QLtoken(QLurl, ClientID, ClientSecret):
    """获取青龙token"""
    try:
        url = f'{QLurl}/open/auth/token?client_id={ClientID}&client_secret={ClientSecret}'
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            result = response.json()
            if token := result.get('data', {}).get('token'):
                return token

        sender.reply("❌ 获取青龙Token失败")
        exit(0)
    except Exception as e:
        sender.reply(f"❌ 连接青龙失败: {str(e)}")
        exit(0)

def extract_base_account(account):
    """
    从复合键中提取基础账号ID
    例如: '123456_1' -> '123456'
    如果不是复合键格式，直接返回原值
    """
    if not account:
        return account

    if account.endswith('_1') or account.endswith('_2'):
        return account.rsplit('_', 1)[0]

    return account

def Addenvs(osname, value, account, phone):
    """添加/更新环境变量到青龙

    Args:
        osname: 变量名（如 ksToken_fast 或 ksToken）
        value: 变量值
        account: 账号ID（可能是复合键格式，如 123456_1）
        phone: 备注名称
    """
    url = f"{QLurl}/open/envs"
    headers = {"Authorization": f"Bearer {qltoken}", "Content-Type": "application/json"}

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200 or resp.json()['code'] != 200:
            sender.reply("❌ 获取青龙变量失败")
            return False

        base_account = extract_base_account(account)

        qlid = None
        for env in resp.json()['data']:
            if env['name'] == osname and env.get('value') == value:
                qlid = env['id']
                break

        if not qlid:
            for env in resp.json()['data']:
                remarks = env.get('remarks', '')
                if env['name'] == osname and f'快手:{base_account}丨' in remarks:
                    qlid = env['id']
                    break

        accountVip = '2099-12-31' or '未授权'
        remarks = f'快手:{base_account}丨用户:{userid}丨ID:{phone}丨授权至:{accountVip}'

        if qlid:
            data = {"value": value, "name": osname, "remarks": remarks, "id": qlid}
            resp = requests.put(url, headers=headers, json=data, timeout=10)
        else:
            data = [{"value": value, "name": osname, "remarks": remarks}]
            resp = requests.post(url, headers=headers, json=data, timeout=10)

        if resp.status_code == 200 and resp.json()['code'] == 200:
            return True

        sender.reply("❌ 提交青龙变量失败")
        return False

    except Exception as e:
        sender.reply(f"❌ 青龙操作异常: {str(e)}")
        return False

def get_payment_config():
    return {}

PAY_TYPE_NAMES = {
    'alipay': '支付宝',
    'wxpay': '微信支付',
    'qqpay': 'QQ钱包',
}

def generate_qrcode(url):
    """生成二维码图片"""
    try:
        from urllib.parse import quote
        encoded_url = quote(url, safe='')
        api_url = f"https://api.qrtool.cn/?text={encoded_url}"
        return api_url
    except:
        return None

class MaPay_Api:
    """在线处理API类"""
    def __init__(self, config):
        self.config = config

    def calculate_md5(self, text):
        """计算字符串的MD5值"""
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    def sort_dict_by_key(self, data):
        """对字典按照键名排序"""
        return dict(sorted(data.items(), key=lambda x: x[0]))

    def create_payment(self, amount, out_trade_no, name, user_id, pay_type=None, sitename=""):
        return True

    def query_order(self, out_trade_no=None, trade_no=None):
        """查询订单状态"""
        try:
            query_url = self.config['gateway']
            if query_url.endswith('/'):
                query_url = query_url[:-1]

            if '/xpay/epay/api.php' not in query_url:
                query_url = f"{query_url}/xpay/epay/api.php"

            params = {
                "act": "order",
                "pid": self.config['pid'],
                "key": self.config['key']
            }

            if trade_no:
                params["trade_no"] = trade_no
            elif out_trade_no:
                params["out_trade_no"] = out_trade_no
            else:
                return False, None, "必须提供商户订单号或系统订单号"

            response = requests.get(query_url, params=params, timeout=10)

            if response.status_code != 200:
                return False, None, f"查询订单失败，HTTP状态码: {response.status_code}"

            try:
                result = response.json()
            except:
                return False, None, "查询订单失败，返回数据格式错误"

            code = result.get('code', 0)
            msg = result.get('msg', '未知状态')

            if code == 1:
                order_status = result.get('status')
                if order_status == 1:
                    return True, result, "支付成功"
                else:
                    return True, result, "订单未支付"
            else:
                return False, None, msg

        except Exception as e:
            return False, None, f"查询订单异常: {str(e)}"

def poll_payment_status(out_trade_no, payment_config, max_tries=30):
    return True

def acquire_payment_lock(timeout=30):
    return True

def release_payment_lock():
    return True

def check_payment_lock_status():
    return True

def process_payment(amount, months, account_count=1):
    return True
def process_ma_pay(amount, months, account_count, payment_config, product_name='快手授权'):
    return True

def process_normal_pay(amount, months, account_count, payment_config, product_name='快手授权'):
    return True

def calculate_share_amount(revenue, share_rate):
    """计算分成金额

    Args:
        revenue: 收益金额
        share_rate: 分成比例（0-100）

    Returns:
        应付分成金额（保留一位小数）
    """
    result = Decimal(str(revenue)) * Decimal(str(share_rate)) / Decimal('100')
    return float(result.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP))

def detect_manual_cash_exchange(cash_records):
    """检测手动兑换的现金金额

    当天存在多次"金币兑换现金"记录时，第一次是自动兑换，后续的是手动兑换
    需要将手动兑换的金额计入分成

    Args:
        cash_records: 现金明细记录列表

    Returns:
        manual_exchange_amount: 手动兑换的总金额（元）
    """
    if not cash_records:
        return 0.0

    today = str(datetime.now().date())
    today_exchanges = []

    for record in cash_records:
        title = record.get('eventType') or record.get('title', '')

        if '金币兑换现金' in title or '兑换' in title:
            amount_str = record.get('amount') or record.get('displayAmount', '0')

            try:
                amount = float(amount_str)
            except:
                continue

            create_time = record.get('createTime')
            record_date = None

            if isinstance(create_time, str):
                parts = create_time.split('.')
                if len(parts) >= 3:
                    try:
                        year = int(parts[0])
                        month = int(parts[1])
                        day = int(parts[2])
                        record_date = f"{year}-{str(month).zfill(2)}-{str(day).zfill(2)}"
                    except:
                        pass
            elif isinstance(create_time, (int, float)):
                try:
                    date_obj = datetime.fromtimestamp(create_time / 1000)
                    record_date = str(date_obj.date())
                except:
                    pass

            if record_date == today and amount > 0:
                today_exchanges.append(amount)

    if len(today_exchanges) <= 1:
        return 0.0

    manual_total = sum(today_exchanges[1:])
    return round(manual_total, 2)

def get_today_share_status(account):
    """获取今日分成状态

    Returns:
        (is_paid, revenue, share_amount): 是否已支付、收益、分成金额
    """
    today = str(datetime.now().date())
    share_key = f"share_{account}_{today}"
    share_data = sg.bucketGet('dd_ks_share', share_key)

    if share_data:
        try:
            data = json.loads(share_data)
            return data.get('is_paid', False), data.get('revenue', 0), data.get('share_amount', 0)
        except:
            return False, 0, 0
    return False, 0, 0

def get_ks_uid_from_account(account):
    """从账号ID中提取快手userId

    账号格式: {userId}_{version}，例如: 123456_1
    返回: userId（不含版本号）
    """
    if not account:
        return None
    parts = account.rsplit('_', 1)
    return parts[0] if len(parts) >= 1 else account

def add_share_debt(account, revenue, share_amount, date=None):
    """添加分成欠款记录

    使用快手userId作为唯一标识，防止删除账号后重新提交逃避欠款
    数据桶: dd_ks_debt
    Key格式: debt_{ks_uid}_{date}
    """
    ks_uid = get_ks_uid_from_account(account)
    if not ks_uid:
        return

    if date is None:
        date = str(datetime.now().date())

    debt_key = f"debt_{ks_uid}_{date}"
    debt_data = {
        'ks_uid': ks_uid,
        'account': account,
        'date': date,
        'revenue': float(revenue),
        'share_amount': float(share_amount),
        'create_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    sg.bucketSet('dd_ks_debt', debt_key, json.dumps(debt_data))

def remove_share_debt(account, date=None):
    """删除分成欠款记录（用户支付后调用）"""
    ks_uid = get_ks_uid_from_account(account)
    if not ks_uid:
        return

    if date is None:
        date = str(datetime.now().date())

    debt_key = f"debt_{ks_uid}_{date}"
    sg.bucketDel('dd_ks_debt', debt_key)

def get_account_debts(account):
    """获取账号的所有欠款记录

    Returns:
        list: 欠款记录列表 [{'date': '2025-12-19', 'share_amount': 0.55}, ...]
    """
    ks_uid = get_ks_uid_from_account(account)
    if not ks_uid:
        return []

    return get_uid_debts(ks_uid)

def get_uid_debts(ks_uid):
    """根据快手userId获取所有欠款记录

    Returns:
        list: 欠款记录列表
    """
    if not ks_uid:
        return []

    debts = []
    today = datetime.now().date()
    for i in range(30):
        check_date = str(today - timedelta(days=i))
        debt_key = f"debt_{ks_uid}_{check_date}"
        debt_data = sg.bucketGet('dd_ks_debt', debt_key)
        if debt_data:
            try:
                data = json.loads(debt_data)
                debts.append(data)
            except:
                pass
    return debts

def get_total_debt_amount(account):
    """获取账号总欠款金额"""
    debts = get_account_debts(account)
    if not debts:
        return 0
    total = sum(Decimal(str(d.get('share_amount', 0))) for d in debts)
    return float(total.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP))

def check_uid_has_debt(ks_uid):
    """检查快手userId是否有欠款

    用于新账号提交时检查是否有历史欠款
    Returns:
        (has_debt, total_amount, debts): 是否有欠款、总金额、欠款列表
    """
    debts = get_uid_debts(ks_uid)
    if not debts:
        return False, 0, []

    total = sum(Decimal(str(d.get('share_amount', 0))) for d in debts)
    total = float(total.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP))
    return True, total, debts

def save_share_record(account, revenue, share_amount, is_paid=False, coins=None):
    """保存分成记录"""
    today = str(datetime.now().date())
    share_key = f"share_{account}_{today}"

    share_data = {
        'account': account,
        'date': today,
        'coins': float(coins) if coins else 0,  # 今日金币数
        'revenue': float(revenue),  # 折合现金
        'share_amount': float(share_amount),
        'is_paid': is_paid,
        'pay_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S") if is_paid else None
    }

    sg.bucketSet('dd_ks_share', share_key, json.dumps(share_data))

    if not is_paid and share_amount > 0:
        add_share_debt(account, revenue, share_amount, today)
    elif is_paid:
        remove_share_debt(account, today)

def process_share_payment(account, revenue, share_rate, coins=None):
    return True

def check_share_authorization(account, version_choice):
    return True

def manage_accounts():
    """账号管理功能"""
    if not uservalue or len(uservalue) == 0:
        sender.reply("❌ 您还没有绑定任何账号\n请先发送 快手登录 进行账号绑定")
        return

    accounts = _sg_literal(uservalue)

    version_menu = """
=====选择快手版本=====
请选择要管理的版本
------------------
[1] 某手极速版
[2] 某手普通版
------------------
回复数字选择版本
回复 q 退出操作
=================="""
    sender.reply(version_menu)

    version_choice = sender.input(120000, 1, False)
    if not version_choice:
        sender.reply("⏰ 操作超时,已退出")
        return
    elif version_choice.lower() == 'q':
        sender.reply("✅ 已取消管理")
        return

    if version_choice not in ['1', '2']:
        sender.reply("❌ 无效的选择")
        return

    if version_choice == '1':
        version_name = "某手极速版"
        target_varname = ks_fast_varname
    else:
        version_name = "某手普通版"
        target_varname = ks_normal_varname

    version_accounts = []
    for account in accounts:
        full_ck = sg.bucketGet('dd_ks_token', account)
        if full_ck:
            token_info = parse_token(full_ck)
            if token_info and token_info['version'] == version_choice:
                version_accounts.append(account)

    if not version_accounts:
        sender.reply(f"❌ 您还没有绑定任何{version_name}账号")
        return

    account_list = f"""
====={version_name}账号管理=====
------------------
[0] 🎯 批量授权所有账号
------------------
"""

    for idx, account in enumerate(version_accounts, 1):
        full_ck = sg.bucketGet('dd_ks_token', account)
        if full_ck:
            token_info = parse_token(full_ck)
            name = token_info['name'] if token_info else '未知'
            account_list += f"[{idx}] {name}\n------------------\n"
        else:
            account_list += f"[{idx}] 未知\n------------------\n"

    account_list += "回复数字选择账号\n回复 0 批量管理所有账号\n回复 q 退出操作\n=================="
    sender.reply(account_list)

    choice = sender.input(120000, 1, False)
    if not choice:
        sender.reply("⏰ 操作超时,已退出")
        return
    elif choice.lower() == 'q':
        sender.reply("✅ 已取消管理")
        return

    try:
        choice_idx = int(choice)
        if choice_idx < 0 or choice_idx > len(version_accounts):
            sender.reply(f"❌ 请输入 0-{len(version_accounts)} 之间的数字")
            return
    except:
        sender.reply("❌ 请输入正确的数字")
        return

    if choice_idx == 0:
        if payment_mode == '天付':
            time_unit = '天数'
            time_example = '30'
        else:
            time_unit = '月数'
            time_example = '1'

        auth_guide = f"""
=====批量授权设置=====
版本: {version_name}
账号数量: {len(version_accounts)}个
------------------
请输入授权{time_unit}(如:{time_example})
回复数字设置{time_unit}
回复 q 退出操作
=================="""
        sender.reply(auth_guide)

        months = sender.input(120000, 1, False)
        if not months:
            sender.reply("⏰ 操作超时,已退出")
            return
        elif months.lower() == 'q':
            sender.reply("✅ 已取消授权")
            return

        try:
            months = int(months)
            if months <= 0:
                time_unit = '天数' if payment_mode == '天付' else '月数'
                sender.reply(f"❌ 授权{time_unit}必须大于0")
                return
        except:
            sender.reply("❌ 请输入正确的数字")
            return

        if payment_mode == '天付':
            unit_price = ksDaymoney
            time_unit = '天'
        else:
            unit_price = ksVipmoney
            time_unit = '月'

        total_money = Decimal(months) * unit_price * len(version_accounts)

        time_unit_display = '天' if payment_mode == '天付' else '月'
        confirm_msg = f"""
=====批量授权确认=====
📱 版本: {version_name}
📊 账号数量: {len(version_accounts)}个
⏰ 授权时长: {months}{time_unit_display}/每个账号
💰 总计金额: {total_money}元
------------------
确认批量授权？
[y] 确认授权
[n] 取消操作
=================="""
        sender.reply(confirm_msg)

        confirm = sender.input(120000, 1, False)
        if not confirm or confirm.lower() not in ['y', 'yes', '是', 'Y']:
            sender.reply("✅ 已取消授权")
            return

        pay_success, pay_msg = process_payment(float(total_money), months, len(version_accounts))
        if not pay_success:
            sender.reply(f"❌ {pay_msg}")
            return

        if payment_mode == '天付':
            days = months
        else:
            days = months * 30

        success_count = 0
        fail_count = 0

        for account in version_accounts:
            try:
                full_ck = sg.bucketGet('dd_ks_token', account)
                if not full_ck:
                    fail_count += 1
                    continue

                current_auth = '2099-12-31'
                today = datetime.now().date()

                if current_auth and current_auth > str(today):
                    auth_date = datetime.strptime(current_auth, "%Y-%m-%d").date()
                    new_auth_date = auth_date + timedelta(days=days)
                else:
                    new_auth_date = today + timedelta(days=days)

                new_auth = new_auth_date.strftime("%Y-%m-%d")

                True

                token_info = parse_token(full_ck)
                name = token_info['name'] if token_info else account
                qinglong_value = token_to_qinglong_format(full_ck)
                Addenvs(osname=target_varname, value=qinglong_value, account=account, phone=name)

                success_count += 1
            except Exception as e:
                fail_count += 1
                print(f"授权账号 {account} 失败: {str(e)}")

        time_unit_display = '天' if payment_mode == '天付' else '月'
        result_msg = f"""
=====授权完成=====
{pay_msg}
------------------
📱 版本: {version_name}
📊 账号数量: {len(version_accounts)}个
✅ 成功: {success_count} 个
❌ 失败: {fail_count} 个
⏰ 授权时长: {months} {time_unit_display}
💰 支付金额: {total_money} 元
=================="""
        sender.reply(result_msg)

    else:
        account = version_accounts[choice_idx - 1]
        full_ck = sg.bucketGet('dd_ks_token', account)

        if not full_ck:
            sender.reply("❌ 未找到账号信息")
            return

        token_info = parse_token(full_ck)
        name = token_info['name'] if token_info else '未知'
        auth_status = '2099-12-31' or '未授权'

        account_info = f"""
=====账号详情=====
📱 账号: {name}
🆔 ID: {account}
🔐 授权: {auth_status}
📱 版本: {version_name}
==================
[1] 授权账号
[2] 删除账号
------------------
回复数字选择功能
回复 q 退出操作
=================="""
        sender.reply(account_info)

        action = sender.input(120000, 1, False)
        if not action:
            sender.reply("⏰ 操作超时,已退出")
            return
        elif action.lower() == 'q':
            sender.reply("✅ 已退出")
            return

        if action == '1':
            if payment_mode == '天付':
                time_unit = '天数'
                time_example = '30'
            else:
                time_unit = '月数'
                time_example = '1'

            auth_guide = f"""
=====设置授权时长=====
📱账号: {name}
📱版本: {version_name}
------------------
请输入授权{time_unit}(如:{time_example})
回复数字设置{time_unit}
回复 q 退出操作
=================="""
            sender.reply(auth_guide)

            months = sender.input(120000, 1, False)
            if not months:
                sender.reply("⏰ 操作超时,已退出")
                return
            elif months.lower() == 'q':
                sender.reply("✅ 已取消授权")
                return

            try:
                months = int(months)
                if months <= 0:
                    time_unit = '天数' if payment_mode == '天付' else '月数'
                    sender.reply(f"❌ 授权{time_unit}必须大于0")
                    return
            except:
                sender.reply("❌ 请输入正确的数字")
                return

            if payment_mode == '天付':
                unit_price = ksDaymoney
                time_unit = '天'
            else:
                unit_price = ksVipmoney
                time_unit = '月'

            money = Decimal(months) * unit_price

            confirm_msg = f"""
=====授权确认=====
📱 账号: {name}
📱 版本: {version_name}
⏰ 授权: {months}{time_unit}
💰 金额: {money}元
------------------
确认授权？
[y] 确认授权
[n] 取消操作
=================="""
            sender.reply(confirm_msg)

            confirm = sender.input(120000, 1, False)
            if not confirm or confirm.lower() not in ['y', 'yes', '是', 'Y']:
                sender.reply("✅ 已取消授权")
                return

            pay_success, pay_msg = process_payment(float(money), months, 1)
            if not pay_success:
                sender.reply(f"❌ {pay_msg}")
                return

            if payment_mode == '天付':
                days = months
            else:
                days = months * 30

            current_auth = '2099-12-31'
            today = datetime.now().date()

            if current_auth and current_auth > str(today):
                auth_date = datetime.strptime(current_auth, "%Y-%m-%d").date()
                new_auth_date = auth_date + timedelta(days=days)
            else:
                new_auth_date = today + timedelta(days=days)

            new_auth = new_auth_date.strftime("%Y-%m-%d")

            True

            qinglong_value = token_to_qinglong_format(full_ck)
            Addenvs(osname=target_varname, value=qinglong_value, account=account, phone=name)

            result_msg = f"""
=====授权完成=====
{pay_msg}
------------------
📱 账号: {name}
📱 版本: {version_name}
⏰ 授权至: {new_auth}
💰 支付金额: {money}元
=================="""
            sender.reply(result_msg)

        elif action == '2':
            if payment_mode == '分成':
                debts = get_account_debts(account)
                if debts:
                    total_debt = sum(Decimal(str(d.get('share_amount', 0))) for d in debts) if debts else Decimal('0')
                    total_debt = float(total_debt.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP))
                    debt_details = "\n".join([f"  • {d.get('date')}: {d.get('share_amount')}元" for d in debts[:5]])
                    if len(debts) > 5:
                        debt_details += f"\n  ... 共{len(debts)}条欠款记录"

                    sender.reply(f"""
=====无法删除=====
❌ 该账号存在未支付的分成欠款！

📝 欠款明细:
{debt_details}

💰 欠款总额: {total_debt}元
------------------
请先支付欠款后再删除账号
发送"快手分成"进行结算
==================""")
                    return

            confirm_msg = f"""
=====警告=====
确定要删除账号吗？
账号: {name}
此操作不可恢复！
------------------
[y] 确认删除
[n] 取消操作
=================="""
            sender.reply(confirm_msg)

            confirm = sender.input(120000, 1, False)
            if not confirm or confirm.lower() not in ['y', 'yes', '是', 'Y']:
                sender.reply("✅ 已取消删除")
                return

            accounts.remove(account)
            sg.bucketDel('dd_ks_token', account)
            True

            if len(accounts) == 0:
                sg.bucketDel('dd_ks_user', userid)
            else:
                sg.bucketSet('dd_ks_user', userid, str(accounts))

            deleted_ql = False
            if payment_mode == '分成':
                if token_info and token_info.get('version') == '1':
                    deleted_ql = delete_account_in_qinglong(account, ks_fast_varname)
                elif token_info and token_info.get('version') == '2':
                    deleted_ql = delete_account_in_qinglong(account, ks_normal_varname)
                else:
                    deleted_ql = delete_account_in_qinglong(account, ks_fast_varname) or \
                                 delete_account_in_qinglong(account, ks_normal_varname)

            ql_status = "青龙变量已删除" if deleted_ql else ("青龙变量删除失败，请手动删除" if payment_mode == '分成' else "")

            sender.reply(f"""
=====删除成功=====
账号 {name} 已删除
{ql_status}
==================""")
        else:
            sender.reply("❌ 无效的选择")
            return

def push_notification(user, account, message):
    """推送消息到各个平台"""
    push_msg = f"""
=====快手账号通知=====
🆔 账号: {account}
📢 消息: {message}
=================="""

    platforms = ['wb', 'tg', 'qq', 'qb', 'wx']
    for platform in platforms:
        try:
            sg.push(platform, '', user, '', push_msg)
        except:
            pass

def disable_account_in_qinlong(account, target_varname):
    """在青龙中禁用账号"""
    try:
        url = f"{QLurl}/open/envs"
        headers = {"Authorization": f"Bearer {qltoken}", "Content-Type": "application/json"}

        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200 or resp.json()['code'] != 200:
            return False

        base_account = extract_base_account(account)

        qlid = None
        for env in resp.json()['data']:
            remarks = env.get('remarks', '')
            if target_varname == env['name'] and f'快手:{base_account}丨' in remarks:
                qlid = env['id']
                break

        if qlid:
            disable_url = f"{QLurl}/open/envs/disable"
            data = [qlid]
            resp = requests.put(disable_url, headers=headers, json=data, timeout=10)

            if resp.status_code == 200 and resp.json()['code'] == 200:
                return True

        return False
    except Exception as e:
        print(f"禁用账号失败: {str(e)}")
        return False

def delete_account_in_qinglong(account, target_varname):
    """在青龙中删除账号变量"""
    try:
        url = f"{QLurl}/open/envs"
        headers = {"Authorization": f"Bearer {qltoken}", "Content-Type": "application/json"}

        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200 or resp.json()['code'] != 200:
            return False

        base_account = extract_base_account(account)

        qlid = None
        for env in resp.json()['data']:
            remarks = env.get('remarks', '')
            if target_varname == env['name'] and f'快手:{base_account}丨' in remarks:
                qlid = env['id']
                break

        if qlid:
            delete_url = f"{QLurl}/open/envs"
            resp = requests.delete(delete_url, headers=headers, json=[qlid], timeout=10)

            if resp.status_code == 200 and resp.json()['code'] == 200:
                return True

        return False
    except Exception as e:
        print(f"删除青龙变量失败: {str(e)}")
        return False

def check_auth_expiry():
    """定时检查授权到期状态（每天10点执行）"""
    if payment_mode not in ['月付', '天付']:
        return

    current_hour = datetime.now().hour
    if current_hour != 10:
        return

    all_users = sg.bucketAllKeys('dd_ks_user')
    if not all_users:
        return

    today = str(datetime.now().date())
    expired_count = 0
    notified_count = 0

    for user in all_users:
        try:
            accountlist = sg.bucketGet('dd_ks_user', user)
            if not accountlist:
                continue

            accounts = _sg_literal(accountlist)
            if isinstance(accounts, str):
                accounts = [accounts]

            user_expired_accounts = []

            for account in accounts:
                try:
                    auth_date = '2099-12-31'

                    if auth_date and auth_date <= today:
                        full_ck = sg.bucketGet('dd_ks_token', account)
                        if full_ck:
                            token_info = parse_token(full_ck)
                            name = token_info['name'] if token_info else account
                            version = token_info.get('version', '1') if token_info else '1'
                            version_name = '极速版' if version == '1' else '普通版'

                            disabled_fast = disable_account_in_qinlong(account, ks_fast_varname)
                            disabled_normal = disable_account_in_qinlong(account, ks_normal_varname)

                            if disabled_fast or disabled_normal:
                                expired_count += 1
                                user_expired_accounts.append({
                                    'name': name,
                                    'version': version_name,
                                    'auth_date': auth_date
                                })
                except Exception as e:
                    print(f"处理账号 {account} 时出错: {str(e)}")
                    continue

            if user_expired_accounts:
                mode_name = '月付' if payment_mode == '月付' else '天付'
                account_details = ''.join([
                    f"  • {acc['name']}({acc['version']}) - 到期日:{acc['auth_date']}"
                    for acc in user_expired_accounts
                ])

                notification = f"""
⚠️ 授权到期通知
------------------
💳 模式: {mode_name}
📅 检测日期: {today}
🔒 已停用账号: {len(user_expired_accounts)}个

{account_details}
------------------
💡 您的账号授权已到期，青龙变量已自动停用
📝 请及时续费以继续使用服务

续费方式: 发送 快手管理 进行续费操作
------------------
提示: 续费后账号将自动恢复运行"""

                push_notification(user, "授权到期", notification)
                notified_count += 1

        except Exception as e:
            print(f"处理用户 {user} 时出错: {str(e)}")
            continue

    if expired_count > 0:
        log_msg = f"""
=====授权到期检测完成=====
检测时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
支付模式: {payment_mode}
------------------
已停用账号: {expired_count}个
通知用户: {notified_count}个
=================="""
        print(log_msg)

def check_share_payment_status():
    return True

def handle_share_payment():
    return True

def handle_withdraw():
    """快手提现(精简版)"""
    if not uservalue: return sender.reply("❌ 未绑定账号")
    accs = _sg_literal(uservalue)
    fa = [a for a in accs if sg.bucketGet('dd_ks_token', a) and parse_token(sg.bucketGet('dd_ks_token', a)).get('version') == '1']
    if not fa: return sender.reply("❌ 无极速版账号")

    lst = "=====极速版提现=====\n[0] 批量提现\n"
    for i, a in enumerate(fa, 1):
        tk = sg.bucketGet('dd_ks_token', a)
        n = parse_token(tk)['name'] if tk else a
        lst += f"[{i}] {n}\n"
    sender.reply(lst + "回复数字选择")

    c = sender.input(120000, 1, False)
    if not c or c.lower() == 'q': return sender.reply("已退出")
    try: ci = int(c)
    except: return sender.reply("❌ 无效")
    if ci < 0 or ci > len(fa): return sender.reply("❌ 无效")

    sender.reply("[1]微信 [2]支付宝")
    cc = sender.input(60000, 1, False)
    ch, cn = ("WECHAT", "微信") if cc == '1' else ("ALIPAY", "支付宝") if cc == '2' else (None, None)
    if not ch: return sender.reply("❌ 无效")

    sender.reply("[1]0.5元 [2]10元 [3]15元 [4]20元 [5]30元 [6]50元")
    ac = sender.input(60000, 1, False)
    am = {'1': 0.5, '2': 10, '3': 15, '4': 20, '5': 30, '6': 50}.get(ac)
    if not am: return sender.reply("❌ 无效")

    tas = fa if ci == 0 else [fa[ci - 1]]
    sc, fc = 0, 0
    for a in tas:
        tk = sg.bucketGet('dd_ks_token', a)
        ti = parse_token(tk) if tk else None
        if not ti: fc += 1; continue
        success, msg = auto_withdraw(ti['cookie'], am)
        if success: sc += 1; sender.reply(f"✅ {ti['name']} {msg}")
        else: fc += 1; sender.reply(f"❌ {ti['name']} {msg}")
    sender.reply(f"提现完成: 成功{sc}个 失败{fc}个")

def withdraw_query(cookie):
    """查询提现额度信息"""
    url = "https://nebula.kuaishou.com/rest/n/nebula/account/withdraw"
    headers = {
        "Connection": "keep-alive",
        "cookie": cookie,
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            resp = response.json()
            if resp.get('result') == 1:
                return resp
        return None
    except Exception as e:
        return None

def withdraw_info(cookie):
    """绑定信息查询，返回 provider 列表"""
    url = "https://www.kuaishoupay.com/pay/account/h5/withdraw/withdraw_info"
    headers = {
        "cookie": cookie,
    }
    data = {
        "account_group_key": "NEBULA_CASH_ACCOUNT",
        "providers": "",
        "bind_page_type": "3",
        "source": "COMMON_WITHDRAW_PAGE",
        "amount": "300"
    }

    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        if response.status_code == 200:
            resp = json.loads(response.text)
            if resp.get('code') == "SUCCESS":
                providers = resp.get("withdraw_provider_infos", [])
                ticket = resp.get("ticket", "")
                return providers, ticket
        return [], ""
    except Exception as e:
        return [], ""

def withdraw_apply(cookie, fen, biz_content, provider="WECHAT", bank_id="", bank_token="", ticket=""):
    """提现申请"""
    url = "https://www.kuaishoupay.com/pay/account/h5/withdraw/apply"
    headers = {
        "cookie": cookie,
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    if isinstance(biz_content, dict):
        biz_content_str = json.dumps(biz_content, ensure_ascii=False, separators=(",", ":"))
    else:
        biz_content_str = str(biz_content)

    data = {
        "account_group_key": "NEBULA_CASH_ACCOUNT",
        "mobile_code": "",
        "fen": fen,
        "provider": provider,
        "total_fen": fen,
        "commission_fen": "0",
        "third_account": provider,
        "attach": "",
        "biz_content": biz_content_str,
        "session_id": "",
        "bank_id": bank_id,
        "bank_token": bank_token,
        "skip_show_third_bind_info": "false",
        "agree_sign_policy": "false",
        "ticket": ticket
    }

    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        if response.status_code == 200:
            resp = json.loads(response.text)
            if resp.get('code') == "SUCCESS":
                return True, resp.get('msg', '提现成功')
            else:
                return False, resp.get('msg', response.text)
        return False, f"HTTP请求失败: {response.status_code}"
    except Exception as e:
        return False, f"请求异常: {str(e)}"

def auto_withdraw(cookie, target_amount=None):
    """自动提现

    Args:
        cookie: 用户cookie
        target_amount: 目标提现金额，None表示自动匹配最高档位

    Returns:
        (success, message)
    """
    withdraw_resp = withdraw_query(cookie)
    if not withdraw_resp:
        return False, "查询提现额度失败"

    data = withdraw_resp.get("data", {})
    try:
        en_withdraw_amount = float(str(data.get("enWithdrawAmount", "0") or "0"))
        en_withdraw_list = [float(x) for x in data.get("enWithdrawList", [])]

        if target_amount is not None:
            if target_amount not in en_withdraw_list or target_amount > en_withdraw_amount:
                return False, f"金额 {target_amount} 元不可用或余额不足"
            final_amount = target_amount
        else:
            candidates = [x for x in en_withdraw_list if x <= en_withdraw_amount]
            if not candidates:
                return False, "余额不足或无可提现档位"
            final_amount = max(candidates)

        withdraw_list = data.get("withdrawList", [])
        target_item = None
        for item in withdraw_list:
            try:
                if float(str(item.get("amount", "0"))) == final_amount and not item.get("disabled", False):
                    target_item = item
                    break
            except Exception:
                continue

        if not target_item:
            return False, "未找到匹配的提现档位"

        biz_content_raw = target_item.get("bizContent")
        biz_content = biz_content_raw if isinstance(biz_content_raw, str) else (biz_content_raw or {})
        fen = str(int(round(final_amount * 100)))

    except Exception as e:
        return False, f"处理提现数据失败: {str(e)}"

    providers, ticket = withdraw_info(cookie)
    if not providers:
        return False, "绑定信息查询失败"

    provider_map = {p.get("provider"): p for p in providers}

    priority = ["WECHAT", "ALIPAY", "UNION_PAY_BANK"]

    provider_icon_map = {
        "WECHAT": "💚微信",
        "ALIPAY": "💙支付宝",
        "UNION_PAY_BANK": "💳银行卡"
    }

    for provider in priority:
        cfg = provider_map.get(provider)
        if not cfg:
            continue

        if not cfg.get("has_bind", False) and provider != "UNION_PAY_BANK":
            continue

        if provider == "UNION_PAY_BANK" and not cfg.get("has_bind", False):
            continue

        bank_id = cfg.get("bank_bind_infos", [{}])[0].get("bank_id", "") if provider == "UNION_PAY_BANK" else ""
        bank_token = cfg.get("bank_bind_infos", [{}])[0].get("bank_token", "") if provider == "UNION_PAY_BANK" else ""

        provider_icon = provider_icon_map.get(provider, provider)

        success, msg = withdraw_apply(cookie, fen=fen, biz_content=biz_content, provider=provider,
                                      bank_id=bank_id, bank_token=bank_token, ticket=ticket)
        if success:
            return True, f"{provider_icon} 提现 {final_amount} 元成功"

    return False, "所有可用渠道均提现失败或未绑定"

def admin_panel():
    """快手后台管理"""
    if not sender.isAdmin():
        sender.reply("❌ 您没有权限访问后台")
        return
    sender.reply(msg_box("快手后台", "[1] 授权管理\n[2] 分成统计\n[3] 清理账号\n[4] 删除用户账号\n[5] 释放支付锁", "回复数字选择"))
    c = sender.input(60000, 1, False)
    if c == '1': admin_authorization()
    elif c == '2': admin_share_statistics()
    elif c == '3': admin_clean_accounts()
    elif c == '4': admin_delete_user_account()
    elif c == '5': admin_release_payment_lock()
    else: sender.reply("已退出")

def admin_authorization():
    return True

def admin_share_statistics():
    """分成统计(精简版)"""
    if payment_mode != '分成': return sender.reply("❌ 未启用分成模式")
    today = str(datetime.now().date())
    users = sg.bucketAllKeys('dd_ks_user')
    if not users: return sender.reply("❌ 无用户")

    pc, uc, tr, ts = 0, 0, 0.0, 0.0
    for u in users:
        try:
            al = sg.bucketGet('dd_ks_user', u)
            if not al: continue
            accs = _sg_literal(al) if isinstance(_sg_literal(al), list) else [_sg_literal(al)]
            for acc in accs:
                d = sg.bucketGet('dd_ks_share', f"share_{acc}_{today}")
                if d:
                    try:
                        data = json.loads(d)
                        if data.get('is_paid'): pc += 1; tr += float(data.get('revenue', 0)); ts += float(data.get('share_amount', 0))
                        else: uc += 1
                    except: pass
        except: continue
    sender.reply(f"📊今日分成统计({today})\n比例:{share_rate}%\n总收益:{tr:.2f}元 总分成:{ts:.2f}元\n已结算:{pc}个 未结算:{uc}个")

def admin_clean_accounts():
    """清理过期账号(精简版)"""
    users = sg.bucketAllKeys('dd_ks_user')
    if not users: return sender.reply("❌ 无账号")
    sender.reply(f"🔄 清理中...共{len(users)}个用户")
    cc, today = 0, str(datetime.now().date())
    for u in users:
        try:
            al = sg.bucketGet('dd_ks_user', u)
            if not al: continue
            accs = _sg_literal(al) if isinstance(_sg_literal(al), list) else [_sg_literal(al)]
            va = []
            for acc in accs:
                auth = '2099-12-31'
                if not auth or auth <= today:
                    try: disable_account_in_qinlong(acc, ks_fast_varname); disable_account_in_qinlong(acc, ks_normal_varname)
                    except: pass
                    True; cc += 1
                else: va.append(acc)
            if va: sg.bucketSet('dd_ks_user', u, str(list(dict.fromkeys(va))))
            else: sg.bucketDel('dd_ks_user', u)
        except: continue
    sender.reply(f"✅清理完成: 已清理{cc}个账号")

def admin_delete_user_account():
    """管理员删除用户账号(用于处理主动结算未通过插件导致的账号无法删除问题)"""
    sender.reply("请输入用户ID:")
    uid = sender.input(60000, 1, False)
    if not uid or uid.lower() == 'q': return sender.reply("已退出")

    al = sg.bucketGet('dd_ks_user', uid)
    if not al: return sender.reply(f"❌ 未找到用户{uid}")

    try:
        accs = _sg_literal(al) if isinstance(_sg_literal(al), list) else [_sg_literal(al)]
    except:
        return sender.reply("❌ 账号数据格式错误")

    if not accs: return sender.reply("❌ 该用户无账号")

    sender.reply(msg_box("选择版本", "[1] 极速版 [2] 普通版", "回复数字"))
    vc = sender.input(60000, 1, False)
    if vc not in ['1', '2']: return sender.reply("已退出")
    vn, tv = ("极速版", ks_fast_varname) if vc == '1' else ("普通版", ks_normal_varname)

    version_accs = []
    for acc in accs:
        tk = sg.bucketGet('dd_ks_token', acc)
        if tk:
            ti = parse_token(tk)
            if ti and ti['version'] == vc:
                version_accs.append((acc, ti['name']))

    if not version_accs: return sender.reply(f"❌ 该用户无{vn}账号")

    lst = f"====={vn}账号列表=====\n用户ID: {uid}\n------------------\n"
    for i, (acc, name) in enumerate(version_accs, 1):
        lst += f"[{i}] {name} (ID:{acc})\n"
    lst += "------------------\n回复数字选择要删除的账号\n回复 q 退出\n=================="
    sender.reply(lst)

    c = sender.input(60000, 1, False)
    if not c or c.lower() == 'q': return sender.reply("已退出")

    try:
        ci = int(c)
        if ci < 1 or ci > len(version_accs): return sender.reply("❌ 无效选择")
    except:
        return sender.reply("❌ 请输入数字")

    acc, name = version_accs[ci - 1]

    sender.reply(msg_box("确认删除", f"账号: {name}\nID: {acc}\n用户: {uid}\n\n此操作将强制删除账号\n不检查分成欠款！", "[y] 确认删除 [n] 取消"))
    confirm = sender.input(60000, 1, False)
    if not confirm or confirm.lower() not in ['y', 'yes', '是']: return sender.reply("✅ 已取消删除")

    try:
        accs.remove(acc)

        sg.bucketDel('dd_ks_token', acc)
        True

        share_count = 0
        for i in range(30):
            check_date = str(datetime.now().date() - timedelta(days=i))
            share_key = f"share_{acc}_{check_date}"
            if sg.bucketGet('dd_ks_share', share_key):
                sg.bucketDel('dd_ks_share', share_key)
                share_count += 1

        debt_count = 0
        ks_uid = get_ks_uid_from_account(acc)
        if ks_uid:
            for i in range(30):
                check_date = str(datetime.now().date() - timedelta(days=i))
                debt_key = f"debt_{ks_uid}_{check_date}"
                if sg.bucketGet('dd_ks_debt', debt_key):
                    sg.bucketDel('dd_ks_debt', debt_key)
                    debt_count += 1

        deleted_ql = delete_account_in_qinglong(acc, tv)

        if accs:
            sg.bucketSet('dd_ks_user', uid, str(accs))
        else:
            sg.bucketDel('dd_ks_user', uid)

        ql_msg = "✅ 青龙变量已删除" if deleted_ql else "⚠️ 青龙变量删除失败，请手动删除"
        share_msg = f"\n✅ 已删除{share_count}条分成记录" if share_count > 0 else ""
        debt_msg = f"\n✅ 已删除{debt_count}条欠款记录" if debt_count > 0 else ""
        sender.reply(f"✅ 删除成功\n账号: {name}\nID: {acc}\n用户: {uid}\n{ql_msg}{share_msg}{debt_msg}")
    except Exception as e:
        sender.reply(f"❌ 删除失败: {str(e)}")

def admin_release_payment_lock():
    return True

def main():
    """主函数"""
    global ks_fast_varname, ks_normal_varname, allow_proxy, dd_ks_qlname, QLurl, qltoken, today_time
    global payment_mode, ksVipmoney, ksDaymoney, kscoin, share_rate, share_allow_coin_pay

    ks_fast_varname, ks_normal_varname, allow_proxy, dd_ks_qlname, dd_managecommand, dd_querycommand, dd_signcommand, \
    payment_mode, ksVipmoney, ksDaymoney, kscoin, use_ma_pay, share_rate, share_allow_coin_pay = getusercontent()

    QLurl, qltoken = seekql()
    today_time = str(datetime.now().date())
    msg = sender.getMessage()

    imtype = sender.getImtype()
    if imtype == 'fake':
        check_share_payment_status()
        check_auth_expiry()
        return

    if '登录' in msg or '登陆' in msg:
        bindaccount()
    elif '查询' in msg:
        query_accounts()
    elif '管理' in msg:
        manage_accounts()
    elif '分成' in msg:
        handle_share_payment()
    elif '后台' in msg:
        admin_panel()
    elif '提现' in msg:
        handle_withdraw()
    elif '教程' in msg:
        sender.reply("📚快手教程\n• 快手登录-绑定账号\n• 快手查询-查询收益\n• 快手管理-账号授权\n• 快手提现-极速版提现\n• 快手分成-分成结算\n格式:备注#Cookie#Salt#代理\n代理:IP|端口|用户名|密码|过期时间")
    else:
        sender.setContinue()

if __name__ == "__main__":
    main()
