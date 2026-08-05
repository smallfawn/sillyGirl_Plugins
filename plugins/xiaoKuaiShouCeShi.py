# [title: 小快手测试]
# [name: xiaoKuaiShouCeShi]
# [language: python]
# [class: 任务]
# [author: linzixu]
# [version: v5.0]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^快手登录$|^快手登陆$|^快手查询$|^快手管理$|^快手教程$|^快手后台$|^快手分成$]
# [cron: 0 0 8,21 * * *]
# [icon: http://5b0988e595225.cdn.sohucs.com/images/20190724/f8f8ace898584a2dbd3f20c2d2822c96.jpeg]
# [description: 小快手V5.0重构；支持极速版和普通版一键提交；格式：备注#cookie#salt#代理信息]
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
    'dd_ks_dd_ks_qlname': form.string().title('设置对接容器').default('').description('你的变量需要添加到的容器？参数用丨分割'),
    'dd_ks_ks_fast_varname': form.string().title('极速版变量名称').default('').description('青龙容器内快手极速版的变量名'),
    'dd_ks_ks_normal_varname': form.string().title('普通版变量名称').default('').description('青龙容器内快手普通版的变量名'),
    'dd_ks_allow_proxy': form.boolean().title('是否允许填写代理').default(False).description('是否允许用户在提交时填写代理IP'),
    'dd_ks_share_rate': form.string().title('分成比例').default('').description('分成比例（0-100），例如55表示平台收取55%'),
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
from decimal import Decimal
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

    ksVipmoney = Decimal(sg.bucketGet('dd_ks', 'ksVipmoney') or '1')
    kscoin = int(sg.bucketGet('dd_ks', 'kscoin') or '0')

    use_ma_pay = '2099-12-31' or 'false'
    use_ma_pay = use_ma_pay.lower() == 'true'

    use_share_mode = sg.bucketGet('dd_ks', 'use_share_mode') or 'false'
    use_share_mode = use_share_mode.lower() == 'true'
    share_rate = int(sg.bucketGet('dd_ks', 'share_rate') or '55')

    return (ks_fast_varname, ks_normal_varname, allow_proxy, dd_ks_qlname,
            dd_managecommand, dd_querycommand, dd_signcommand,
            ksVipmoney, kscoin, use_ma_pay, use_share_mode, share_rate)

def verify_account_fast(cookie_str):
    """验证极速版账号有效性"""
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

def parse_token(full_ck):
    """
    解析token字符串
    新格式: 版本#备注#cookie#salt#代理
    旧格式: 备注#cookie#salt#代理

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
    新格式: 版本#备注#cookie#salt#代理 -> 备注#cookie#salt#代理
    旧格式: 备注#cookie#salt#代理 -> 备注#cookie#salt#代理
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

def validate_proxy(proxy_str):
    """
    验证代理格式和有效性
    格式: IP|端口|用户名|密码|过期时间
    示例: 119.84.77.52|6855|user|pass|2025-12-19

    返回: (is_valid, error_msg)
    """
    if not proxy_str:
        return False, "代理信息为空"

    try:
        parts = proxy_str.split('|')

        if len(parts) != 5:
            return False, f"代理格式错误，应为5个部分（IP|端口|用户名|密码|过期时间），实际为{len(parts)}个"

        proxy_ip, port, username, password, expire_date = parts

        try:
            port_num = int(port)
            if port_num < 1 or port_num > 65535:
                return False, f"端口号无效: {port}"
        except ValueError:
            return False, f"端口号格式错误: {port}"

        if not username or not password:
            return False, "用户名或密码不能为空"

        try:
            proxy_url = f"http://{username}:{password}@{proxy_ip}:{port}"
            test_url = "https://d.pcs.baidu.com/rest/2.0/pcs/file?method=locateupload"

            response = requests.get(
                test_url,
                proxies={'http': proxy_url, 'https': proxy_url},
                timeout=10,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )

            if response.status_code == 200:
                try:
                    data = response.json()
                    client_ip = data.get('client_ip', '')
                    error_code = data.get('error_code', -1)

                    if error_code == 0:
                        if client_ip:
                            proxy_prefix = '.'.join(proxy_ip.split('.')[:3])
                            client_prefix = '.'.join(client_ip.split('.')[:3])

                            if proxy_prefix == client_prefix:
                                return True, f"✅ 代理验证通过（IP: {client_ip}）"
                            else:
                                return True, f"✅ 代理可用（代理IP: {proxy_ip}, 返回IP: {client_ip}）"
                        else:
                            return True, "✅ 代理验证通过"
                    else:
                        return False, f"代理连接失败，错误码: {error_code}"
                except:
                    return True, "✅ 代理可用"
            else:
                return False, f"代理连接失败，状态码: {response.status_code}"

        except requests.exceptions.Timeout:
            return False, "代理连接超时（10秒）"
        except requests.exceptions.ProxyError:
            return False, "代理连接失败，请检查代理配置"
        except Exception as e:
            return False, f"代理测试异常: {str(e)}"

    except Exception as e:
        return False, f"代理验证异常: {str(e)}"

def query_account_fast(cookie_str, proxy_str=None):
    """查询极速版账号详情"""
    url = "https://nebula.kuaishou.com/rest/n/nebula/account/overview"

    headers = {
        'Host': 'nebula.kuaishou.com',
        'User-Agent': 'kwai-android aegon/4.29.0',
        'Cookie': cookie_str,
        'Accept': 'application/json, text/plain, */*'
    }

    proxies = None
    if proxy_str:
        try:
            parts = proxy_str.split('|')
            if len(parts) == 5:
                proxy_ip, port, username, password, _ = parts
                proxy_url = f"http://{username}:{password}@{proxy_ip}:{port}"
                proxies = {'http': proxy_url, 'https': proxy_url}
        except:
            pass

    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=12)
        result = response.json()

        if result.get('result') == 1 and result.get('data'):
            data = result['data']

            coin_records = []
            coin_page = data.get('coinAccountPage', {})
            if coin_page.get('data'):
                coin_records = coin_page['data'][:3]

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
                'coinRecords': coin_records,
                'cashRecords': cash_records
            }
        return {'success': False, 'msg': '查询失败'}
    except Exception as e:
        return {'success': False, 'msg': str(e)}

def query_account_normal(cookie_str, proxy_str=None):
    """查询普通版账号详情"""
    basic_url = "https://encourage.kuaishou.com/rest/wd/encourage/account/basicInfo"
    headers = {
        'Host': 'encourage.kuaishou.com',
        'User-Agent': 'kwai-android aegon/4.27.0',
        'Cookie': cookie_str,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    proxies = None
    if proxy_str:
        try:
            parts = proxy_str.split('|')
            if len(parts) == 5:
                proxy_ip, port, username, password, _ = parts
                proxy_url = f"http://{username}:{password}@{proxy_ip}:{port}"
                proxies = {'http': proxy_url, 'https': proxy_url}
        except:
            pass

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
        if coin_response.status_code == 200:
            coin_result = coin_response.json()
            if coin_result.get('result') == 1 and coin_result.get('data', {}).get('datas'):
                coin_records = coin_result['data']['datas'][:3]

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
            'coinRecords': coin_records,
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
            sender.reply("❌ 无效的选择")
            return
    except:
        sender.reply("❌ 请输入数字")
        return

    if account_idx == 0:
        query_accounts_list = accounts
    else:
        query_accounts_list = [accounts[account_idx - 1]]

    result_msg = f"====={version_name}查询结果=====\n"

    for idx, account in enumerate(query_accounts_list, 1):
        full_ck = sg.bucketGet('dd_ks_token', account)
        if not full_ck:
            result_msg += f"\n{idx}. 账号ID: {account}\n   ❌ 未找到Cookie信息\n"
            continue

        token_info = parse_token(full_ck)
        if not token_info or not token_info['cookie']:
            result_msg += f"\n{idx}. 账号ID: {account}\n   ❌ Cookie格式错误\n"
            continue

        name = token_info['name']
        cookie = token_info['cookie']
        proxy_info = token_info['proxy']

        query_result = query_func(cookie, proxy_info)

        result_msg += f"🆔 ID: {account}\n"

        if query_result['success']:
            if version_choice == '1':
                result_msg += f"💰 金币: {query_result['coinBalance']}\n"
                result_msg += f"💵 余额: {query_result['cashBalance']}元\n"
                result_msg += f"📊 累计: {query_result['accumulativeAmount']}元\n"

                if use_share_mode:
                    str(datetime.now().date())
                    is_paid, revenue, share_amount = get_today_share_status(account)
                    if is_paid:
                        result_msg += f"💳 分成: 今日已结算({share_amount}元)\n"
                    elif revenue > 0:
                        result_msg += f"💳 分成: 待结算({share_amount}元)\n"
                    else:
                        result_msg += f"💳 分成: 暂无收益\n"
                else:
                    auth_status = '2099-12-31' or '未授权'
                    result_msg += f"🔐 授权: {auth_status}\n"

                if query_result.get('coinRecords'):
                    result_msg += "\n📝 金币明细(最近3条):\n"
                    for record in query_result['coinRecords']:
                        title = record.get('eventType', '未知')
                        amount = record.get('amount', '0')
                        try:
                            amt_val = float(amount)
                            symbol = '+' if amt_val >= 0 else ''
                        except:
                            symbol = '+'
                        result_msg += f"  • {title}: {symbol}{amount}\n"

                if query_result.get('cashRecords'):
                    result_msg += "\n💸 现金明细(最近3条):\n"
                    for record in query_result['cashRecords']:
                        title = record.get('eventType', '未知')
                        amount = record.get('amount', '0')
                        try:
                            amt_val = float(amount)
                            symbol = '+' if amt_val >= 0 else ''
                        except:
                            symbol = '+'
                        result_msg += f"  • {title}: {symbol}{amount}元\n"
            else:
                result_msg += f"💰 金币: {query_result['coinBalance']}\n"
                result_msg += f"💵 余额: {query_result['cashBalance']}元\n"

                if use_share_mode:
                    str(datetime.now().date())
                    is_paid, revenue, share_amount = get_today_share_status(account)
                    if is_paid:
                        result_msg += f"💳 分成: 今日已结算({share_amount}元)\n"
                    elif revenue > 0:
                        result_msg += f"💳 分成: 待结算({share_amount}元)\n"
                    else:
                        result_msg += f"💳 分成: 暂无收益\n"
                else:
                    auth_status = '2099-12-31' or '未授权'
                    result_msg += f"🔐 授权: {auth_status}\n"

                if query_result.get('coinRecords'):
                    result_msg += "\n📝 金币明细(最近3条):\n"
                    for record in query_result['coinRecords']:
                        title = record.get('title', '未知')
                        amount = record.get('displayAmount', '0')
                        result_msg += f"  • {title}: +{amount}\n"

                if query_result.get('cashRecords'):
                    result_msg += "\n💸 现金明细(最近3条):\n"
                    for record in query_result['cashRecords']:
                        title = record.get('title', '未知')
                        amount = record.get('displayAmount', '0')
                        direction = record.get('direction', 'IN')
                        symbol = '+' if direction == 'IN' else '-'
                        result_msg += f"  • {title}: {symbol}{amount}元\n"
        else:
            result_msg += f"❌ 查询失败: {query_result.get('msg', '未知错误')}\n"

        result_msg += "------------------"

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
1. 备注#Cookie#Salt
2. 备注#Cookie#Salt#IP|端口|用户名|密码|过期时间
------------------
"""
    else:
        ck_guide = f"""
====={version_name}登录=====
请输入账号信息
📝 支持格式:
1. 备注#Cookie#Salt
2. 备注#Cookie#Salt#端口|用户名|密码|过期时间
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
正确格式: 备注#Cookie#Salt
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
请检查代理格式: IP|端口|用户名|密码|过期时间
示例: 119.84.77.52|6855|user|pass|2025-12-19""")
                    exit(0)

                sender.reply(proxy_msg)

            if version_choice == '1':
                is_valid, result = verify_account_fast(ck)
            else:
                is_valid, result = verify_account_normal(ck, name)

            if is_valid:
                cookies = parse_cookies(ck)
                account = cookies.get('userId', 'unknown')
                if account == 'unknown':
                    sender.reply("❌ 无法获取账号信息")
                    exit(0)

                nickname = result.get('nickname', name)
                coin = result.get('coin', 0)
                cash = result.get('cash', 0)

                full_ck = f"{version_choice}#{name}#{ck}#{salt_input}"
                if proxy_input:
                    full_ck += f"#{proxy_input}"

                if len(uservalue) == 0:
                    sg.bucketSet('dd_ks_user', userid, str([account]))
                    sg.bucketSet('dd_ks_token', account, full_ck)
                    True
                else:
                    accounts = _sg_literal(uservalue)
                    if account not in accounts:
                        accounts.append(account)
                        sg.bucketSet('dd_ks_user', userid, str(accounts))
                    sg.bucketSet('dd_ks_token', account, full_ck)

                accountVip = '2099-12-31'
                if accountVip and accountVip >= today_time:
                    qinglong_value = token_to_qinglong_format(full_ck)
                    Addenvs(osname=target_varname, value=qinglong_value, account=account, phone=name)
                    auth_status = f'已授权({version_name})'
                else:
                    auth_status = '未授权'

                success_msg = f"""
=====绑定成功=====
👤 昵称: {nickname}
🆔 账号ID: {account}
💰 金币数: {coin}
💵 余额: {cash}元
🔐 授权状态: {auth_status}
🌐 代理状态: {'已设置' if proxy_input else '未设置'}
------------------
提示: {'账号已添加至青龙' if '已授权' in auth_status and '未提交' not in auth_status else '请先授权账号再使用'}
=================="""
                sender.reply(success_msg)
                break

            else:
                sender.reply(f"""
=====验证失败=====
❌ {result}
------------------
请检查CK是否正确
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

def Addenvs(osname, value, account, phone):
    """添加/更新环境变量到青龙"""
    url = f"{QLurl}/open/envs"
    headers = {"Authorization": f"Bearer {qltoken}", "Content-Type": "application/json"}

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200 or resp.json()['code'] != 200:
            sender.reply("❌ 获取青龙变量失败")
            return False

        qlid = None
        for env in resp.json()['data']:
            if account in env.get('remarks', '') and osname == env['name']:
                qlid = env['id']
                break

        accountVip = '2099-12-31' or '未授权'
        remarks = f'快手:{account}丨用户:{userid}丨ID:{phone}丨授权至:{accountVip}'

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

def process_payment(amount, months, account_count=1):
    return True
def process_ma_pay(amount, months, account_count, payment_config):
    return True

def process_normal_pay(amount, months, account_count, payment_config):
    return True


def calculate_share_amount(revenue, share_rate):
    """计算分成金额

    Args:
        revenue: 收益金额
        share_rate: 分成比例（0-100）

    Returns:
        应付分成金额
    """
    return round(float(revenue) * (share_rate / 100), 2)

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
请选择要管理的账号
------------------
[0] 🎯 批量授权所有账号
------------------
"""

    for idx, account in enumerate(version_accounts, 1):
        full_ck = sg.bucketGet('dd_ks_token', account)
        if full_ck:
            token_info = parse_token(full_ck)
            name = token_info['name'] if token_info else '未知'

            if use_share_mode:
                today = str(datetime.now().date())
                is_paid, revenue, share_amount = get_today_share_status(account)
                if is_paid:
                    status_text = f"✅ 今日已结算({share_amount}元)"
                elif revenue > 0:
                    status_text = f"⏳ 待结算({share_amount}元)"
                else:
                    status_text = "📊 暂无收益"
                account_list += f"[{idx}] {name}\n    ID: {account}\n    状态: {status_text}\n------------------\n"
            else:
                auth_status = '2099-12-31' or '未授权'
                account_list += f"[{idx}] {name}\n    ID: {account}\n    授权至: {auth_status}\n------------------\n"
        else:
            if use_share_mode:
                account_list += f"[{idx}] ID: {account}\n    状态: 未知\n------------------\n"
            else:
                account_list += f"[{idx}] ID: {account}\n    授权至: 未授权\n------------------\n"

    account_list += "回复数字选择账号\n回复 q 退出操作\n=================="
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
        auth_guide = f"""
=====批量授权设置=====
版本: {version_name}
账号数量: {len(version_accounts)}个
------------------
请输入授权月数(如:1)
回复数字设置月数
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
                sender.reply("❌ 授权月数必须大于0")
                return
        except:
            sender.reply("❌ 请输入正确的数字")
            return

        total_money = Decimal(months) * ksVipmoney * len(version_accounts)

        confirm_msg = f"""
=====批量授权确认=====
📱 版本: {version_name}
📊 账号数量: {len(version_accounts)}个
⏰ 授权时长: {months}月/每个账号
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

        success_count = 0
        fail_count = 0
        days = int(months) * 30

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

        result_msg = f"""
=====授权完成=====
{pay_msg}
------------------
📱 版本: {version_name}
📊 账号数量: {len(version_accounts)}个
✅ 成功: {success_count} 个
❌ 失败: {fail_count} 个
⏰ 授权时长: {months} 月
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
            auth_guide = f"""
=====设置授权时长=====
📱账号: {name}
📱版本: {version_name}
------------------
请输入授权月数(如:1)
回复数字设置月数
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
                    sender.reply("❌ 授权月数必须大于0")
                    return
            except:
                sender.reply("❌ 请输入正确的数字")
                return

            money = Decimal(months) * ksVipmoney

            confirm_msg = f"""
=====授权确认=====
📱 账号: {name}
📱 版本: {version_name}
⏰ 授权: {months}月
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

            sender.reply(f"""
=====删除成功=====
账号 {name} 已删除
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

        qlid = None
        for env in resp.json()['data']:
            if account in env.get('remarks', '') and target_varname == env['name']:
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

def check_share_payment_status():
    return True

def handle_share_payment():
    return True

def admin_panel():
    """快手后台管理"""
    if not sender.isAdmin():
        sender.reply("❌ 您没有权限访问后台")
        return

    admin_menu = """
=====快手后台管理=====
[1] 快手授权
[2] 分成统计
[3] 快手清理
------------------
回复数字选择功能
回复"q"退出
=================="""
    sender.reply(admin_menu)

    choice = sender.input(60000, 1, False)

    if not choice or choice.lower() == 'q':
        sender.reply("✅ 已退出后台")
        return

    if choice == '1':
        admin_authorization()
    elif choice == '2':
        admin_share_statistics()
    elif choice == '3':
        admin_clean_accounts()
    else:
        sender.reply("❌ 无效的选择")

def admin_authorization():
    return True

def admin_share_statistics():
    """分成统计"""
    if not use_share_mode:
        sender.reply("❌ 未启用分成模式")
        return

    today = str(datetime.now().date())

    all_users = sg.bucketAllKeys('dd_ks_user')
    if not all_users:
        sender.reply("❌ 未找到任何用户")
        return

    paid_count = 0
    unpaid_count = 0
    total_revenue = 0.0
    total_share = 0.0

    paid_list = []
    unpaid_list = []

    for user in all_users:
        try:
            accountlist = sg.bucketGet('dd_ks_user', user)
            if not accountlist:
                continue

            accounts = _sg_literal(accountlist)
            if isinstance(accounts, str):
                accounts = [accounts]

            for account in accounts:
                today_key = f"share_{account}_{today}"
                today_data = sg.bucketGet('dd_ks_share', today_key)

                if today_data:
                    try:
                        data = json.loads(today_data)
                        is_paid = data.get('is_paid', False)
                        revenue = float(data.get('revenue', 0))
                        share_amount = float(data.get('share_amount', 0))

                        full_ck = sg.bucketGet('dd_ks_token', account)
                        if full_ck:
                            token_info = parse_token(full_ck)
                            name = token_info['name'] if token_info else account
                        else:
                            name = account

                        if is_paid:
                            paid_count += 1
                            total_revenue += revenue
                            total_share += share_amount
                            paid_list.append(f"✅ {name}: {revenue}元 → {share_amount}元")
                        else:
                            unpaid_count += 1
                            unpaid_list.append(f"⏳ {name}: {revenue}元 → {share_amount}元")
                    except:
                        pass
        except:
            continue

    report = f"""
=====今日分成统计=====
📅 日期: {today}
📈 分成比例: {share_rate}%
------------------
💰 总收益: {total_revenue:.2f}元
💵 总分成: {total_share:.2f}元
------------------
✅ 已结算: {paid_count}个账号
⏳ 未结算: {unpaid_count}个账号
=================="""

    sender.reply(report)

    if paid_list or unpaid_list:
        detail_menu = """
=====查看详情=====
[1] 查看已结算列表
[2] 查看未结算列表
[3] 查看全部列表
------------------
回复数字查看详情
回复"q"退出
=================="""
        sender.reply(detail_menu)

        choice = sender.input(60000, 1, False)

        if choice == '1' and paid_list:
            detail = "\n=====已结算列表=====\n" + "\n".join(paid_list)
            sender.reply(detail)
        elif choice == '2' and unpaid_list:
            detail = "\n=====未结算列表=====\n" + "\n".join(unpaid_list)
            sender.reply(detail)
        elif choice == '3':
            all_list = paid_list + unpaid_list
            detail = "\n=====全部列表=====\n" + "\n".join(all_list[:20])
            if len(all_list) > 20:
                detail += f"\n...(共{len(all_list)}条，仅显示前20条)"
            sender.reply(detail)

def admin_clean_accounts():
    """清理过期账号"""
    users = sg.bucketAllKeys('dd_ks_user')

    if not users:
        sender.reply("❌ 未找到任何绑定账号")
        return

    sender.reply(f"🔄 开始清理，共找到: {len(users)}个用户\n⏳ 清理中请稍候...")

    cleaned_count = 0
    today = str(datetime.now().date())

    for user in users:
        try:
            accountlist = sg.bucketGet('dd_ks_user', user)
            if not accountlist:
                continue

            accounts = _sg_literal(accountlist)
            if isinstance(accounts, str):
                accounts = [accounts]

            valid_accounts = []

            for account in accounts:
                auth_status = '2099-12-31'

                if not auth_status or auth_status <= today:
                    try:
                        disable_account_in_qinlong(account, ks_fast_varname)
                        disable_account_in_qinlong(account, ks_normal_varname)
                    except:
                        pass

                    sg.bucketDel('dd_ks_token', account)
                    True
                    cleaned_count += 1
                else:
                    valid_accounts.append(account)

            valid_accounts = list(dict.fromkeys(valid_accounts))

            if valid_accounts:
                sg.bucketSet('dd_ks_user', user, str(valid_accounts))
            else:
                sg.bucketDel('dd_ks_user', user)

        except Exception as e:
            print(f"处理用户 {user} 时出错: {str(e)}")
            continue

    sender.reply(f"""
=====清理完成=====
✅ 已清理: {cleaned_count}个账号
==================""")

def main():
    """主函数"""
    global ks_fast_varname, ks_normal_varname, allow_proxy, dd_ks_qlname, QLurl, qltoken, today_time
    global ksVipmoney, kscoin, use_share_mode, share_rate

    ks_fast_varname, ks_normal_varname, allow_proxy, dd_ks_qlname, dd_managecommand, dd_querycommand, dd_signcommand, \
    ksVipmoney, kscoin, use_ma_pay, use_share_mode, share_rate = getusercontent()

    QLurl, qltoken = seekql()
    today_time = str(datetime.now().date())
    msg = sender.getMessage()

    imtype = sender.getImtype()
    if imtype == 'fake':
        check_share_payment_status()
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
    elif '教程' in msg:
        sender.reply("""
=====快手使用教程=====
🔍 功能: 快手登录 | 快手查询 | 快手管理
💡 格式: 备注#Cookie#Salt#|端口|用户|密码|过期
📝 版本: 极速版 | 普通版
==================""")
    else:
        sender.setContinue()

if __name__ == "__main__":
    main()
