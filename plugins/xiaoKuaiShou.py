# [title: 小快手]
# [name: xiaoKuaiShou]
# [language: python]
# [class: 任务]
# [author: linzixuan]
# [version: v1.2.6]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^快手(登录|登陆|查询|管理|教程)?$]
# [icon: http://5b0988e595225.cdn.sohucs.com/images/20190724/f8f8ace898584a2dbd3f20c2d2822c96.jpeg]
# [description: 快手极速版与普通版账号登录、查询、面板同步及管理]
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
    'dd_ks_dd_ks_qlname': plugin.Form.string().title('设置对接容器').default('').description('你的变量需要添加到的容器？参数用丨分割'),
    'dd_ks_ks_fast_varname': plugin.Form.string().title('极速版变量名称').default('').description('青龙容器内快手极速版的变量名'),
    'dd_ks_ks_normal_varname': plugin.Form.string().title('普通版变量名称').default('').description('青龙容器内快手普通版的变量名'),
    'dd_ks_allow_proxy': plugin.Form.boolean().title('是否允许填写代理').default(False).description('是否允许用户在提交时填写代理IP'),
})
_CONFIG_FIELD_MAP = {
    ('dd_ks', 'dd_ks_qlname'): 'dd_ks_dd_ks_qlname',
    ('dd_ks', 'ks_fast_varname'): 'dd_ks_ks_fast_varname',
    ('dd_ks', 'ks_normal_varname'): 'dd_ks_ks_normal_varname',
    ('dd_ks', 'allow_proxy'): 'dd_ks_allow_proxy',
}

import requests
import time
import json

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()
uservalue = sg.bucketGet(bucket='dd_ks_user', key=userid)

def getusercontent():
    return (
        sg.bucketGet('dd_ks','ks_fast_varname') or 'ksToken_fast',
        sg.bucketGet('dd_ks','ks_normal_varname') or 'ksToken',
        str(sg.bucketGet('dd_ks','allow_proxy') or 'true').lower()=='true',
        sg.bucketGet('dd_ks','dd_ks_qlname') or '',
        '快手管理','快手查询','快手登录'
    )

def verify_account_fast(cookie_str):
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
    cookies = {}
    for item in cookie_str.split(';'):
        if '=' in item:
            key, value = item.strip().split('=', 1)
            cookies[key] = value
    return cookies


def parse_token(full_ck):
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

def query_account_normal(cookie_str, proxy_str=None):
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
    accounts=list(_sg_literal(sg.bucketGet('dd_ks_user',userid),[]))
    if not accounts:
        sender.reply('❌ 尚未绑定账号，请先发送 快手登录')
        return
    sender.reply('选择版本：[1] 极速版 [2] 普通版；q 退出')
    version=sender.input(120000,1,False)
    if version not in ('1','2'):return
    selected=[]
    for account in accounts:
        info=parse_token(sg.bucketGet('dd_ks_token',account) or '')
        if info and info['version']==version:selected.append((account,info))
    if not selected:
        sender.reply('❌ 该版本没有账号')
        return
    sender.reply('=====账号列表=====\n'+'\n'.join(f'[{i}] {x[1]["name"]} ({x[0]})' for i,x in enumerate(selected,1))+'\n[0] 全部')
    choice=sender.input(120000,1,False)
    try:index=int(choice)
    except:return
    targets=selected if index==0 else selected[index-1:index]
    for account,info in targets:
        result=(query_account_fast if version=='1' else query_account_normal)(info['cookie'],info['proxy'])
        if not result.get('success'):
            sender.reply(f'❌ {info["name"]}: {result.get("msg","查询失败")}')
            continue
        text=f'=====快手查询=====\n📝 {info["name"]}\n🆔 {account}\n💰 金币: {result.get("coinBalance",0)}\n💵 余额: {result.get("cashBalance",0)}元'
        if version=='1':text+=f'\n📊 累计: {result.get("accumulativeAmount",0)}元'
        sender.reply(text+'\n==================')

def bindaccount():
    sender.reply('选择版本：[1] 极速版 [2] 普通版；q 退出')
    version=sender.input(120000,1,False)
    if version not in ('1','2'):return
    sender.reply('发送：备注#Cookie#Salt'+('#代理（可选）' if allow_proxy else ''))
    raw=sender.input(120000,1,False)
    if not raw or raw.lower()=='q':return
    parts=raw.split('#',3)
    if len(parts)<3:
        sender.reply('❌ 格式错误')
        return
    name,cookie,salt=parts[:3];proxy=parts[3] if len(parts)>3 and allow_proxy else ''
    if proxy:
        ok,msg=validate_proxy(proxy)
        if not ok:
            sender.reply(f'❌ {msg}')
            return
    ok,result=(verify_account_fast(cookie) if version=='1' else verify_account_normal(cookie,name))
    if not ok:
        sender.reply(f'❌ 验证失败：{result}')
        return
    base=parse_cookies(cookie).get('userId')
    if not base:
        sender.reply('❌ Cookie 中缺少 userId')
        return
    account=f'{base}_{version}'
    full=f'{version}#{name}#{cookie}#{salt}'+(f'#{proxy}' if proxy else '')
    accounts=list(_sg_literal(sg.bucketGet('dd_ks_user',userid),[]))
    is_new=account not in accounts
    sg.bucketSet('dd_ks_user',userid,str(list(dict.fromkeys(accounts+[account]))))
    sg.bucketSet('dd_ks_token',account,full)
    value=token_to_qinglong_format(full)
    synced=Addenvs(ks_fast_varname if version=='1' else ks_normal_varname,value,account,name)
    sender.reply(f'✅ {"绑定" if is_new else "更新"}成功：{result.get("nickname",name)}\n金币: {result.get("coin",0)} 余额: {result.get("cash",0)}元\n面板: {"已同步" if synced else "未同步"}')

def seekql():
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
    if not account:
        return account

    if account.endswith('_1') or account.endswith('_2'):
        return account.rsplit('_', 1)[0]

    return account

def Addenvs(osname, value, account, phone):
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

        remarks = f'快手:{base_account}丨用户:{userid}丨ID:{phone}'

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

def manage_accounts():
    accounts=list(_sg_literal(sg.bucketGet('dd_ks_user',userid),[]))
    if not accounts:
        sender.reply('❌ 没有账号')
        return
    sender.reply('=====快手管理=====\n'+'\n'.join(f'[{i}] {a}' for i,a in enumerate(accounts,1))+'\n回复序号；q退出')
    choice=sender.input(120000,1,False)
    if not str(choice).isdigit():return
    i=int(choice)-1
    if i not in range(len(accounts)):return
    account=accounts[i];raw=sg.bucketGet('dd_ks_token',account) or '';info=parse_token(raw)
    sender.reply('[1] 查看配置 [2] 同步面板 [3] 删除账号')
    action=sender.input(120000,1,False)
    if action=='1':sender.reply(raw or '❌ 无配置')
    elif action=='2' and info:
        synced=Addenvs(ks_fast_varname if info['version']=='1' else ks_normal_varname,token_to_qinglong_format(raw),account,info['name'])
        sender.reply('✅ 同步成功' if synced else '❌ 同步失败')
    elif action=='3':
        sender.reply('确认删除请回复 y')
        if sender.input(60000,1,False).lower()=='y':
            accounts.remove(account);sg.bucketSet('dd_ks_user',userid,str(accounts));sg.bucketDel('dd_ks_token',account);delete_account_in_qinglong(account);sender.reply('✅ 已删除')



def delete_account_in_qinglong(account, target_varname):
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















def main():
    global ks_fast_varname,ks_normal_varname,allow_proxy,dd_ks_qlname,QLurl,qltoken
    ks_fast_varname,ks_normal_varname,allow_proxy,dd_ks_qlname,_,_,_=getusercontent()
    QLurl,qltoken=seekql()
    msg=sender.getMessage()
    if '登录' in msg or '登陆' in msg:bindaccount()
    elif '查询' in msg:query_accounts()
    elif '管理' in msg:manage_accounts()
    elif '教程' in msg or msg=='快手':sender.reply('快手登录：绑定账号\n快手查询：查询收益\n快手管理：查看、同步或删除账号')
    else:sender.setContinue()

if __name__ == "__main__":
    main()
