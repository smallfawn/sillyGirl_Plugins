# [title: 酷我Music]
# [name: kuWoMusic]
# [language: python]
# [class: 任务]
# [author: sky2022]
# [version: v1.4.0]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^(酷我登录|酷我登陆|登陆酷我|登录酷我|酷我查询|查询酷我|酷我管理|管理酷我|酷我教程|酷我说明)$]
# [icon: https://api.iconify.design/lucide:apple.svg]
# [description: 酷我账号登录、金币查询、面板同步与管理]
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
    'dd_Kuwo_PluginsData_panel_type': plugin.Form.string().title('对接面板类型').default('').description('填写你当前使用的面板类型，支持：青龙、青龙面板、QL、呆呆、呆呆面板、Daidai'),
    'dd_Kuwo_PluginsData_panel_config': plugin.Form.string().title('对接面板配置').default('').description('统一填写面板对接参数。青龙：Host丨ClientID丨ClientSecret；呆呆：Host丨AppKey丨AppSecret；分隔符使用中文丨'),
    'dd_Kuwo_PluginsData_panel_group': plugin.Form.string().title('对接面板分组').default('').description('仅呆呆面板生效。填写后新增或更新变量时会同步写入 group 字段；留空则不处理分组'),
    'dd_Kuwo_PluginsData_osname': plugin.Form.string().title('面板变量名').default('').description('提交到面板中的酷我音乐变量名'),
})
_CONFIG_FIELD_MAP = {
    ('dd_Kuwo_PluginsData', 'panel_type'): 'dd_Kuwo_PluginsData_panel_type',
    ('dd_Kuwo_PluginsData', 'panel_config'): 'dd_Kuwo_PluginsData_panel_config',
    ('dd_Kuwo_PluginsData', 'panel_group'): 'dd_Kuwo_PluginsData_panel_group',
    ('dd_Kuwo_PluginsData', 'osname'): 'dd_Kuwo_PluginsData_osname',
}

import requests
import json
from datetime import datetime, timedelta, timezone
import random
import time

log = print

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()
uservalue = sg.bucketGet(bucket='dd_Kuwo_bind', key=userid) or ''

def normalize_panel_type(panel_type_value, legacy_use_daidai_value='false'):
    value = str(panel_type_value or '').strip().lower()
    if value in ('呆呆', '呆呆面板', 'daidai', 'dd'):
        return 'daidai'
    if value in ('青龙', '青龙面板', 'qinglong', 'ql'):
        return 'qinglong'
    if value:
        return ''

    legacy_value = str(legacy_use_daidai_value or '').strip().lower()
    if legacy_value == 'true':
        return 'daidai'
    return 'qinglong'

def QLtoken(QLurl, ClientID, ClientSecret):
    try:
        url = f'{QLurl}/open/auth/token?client_id={ClientID}&client_secret={ClientSecret}'
        A = requests.get(url)
        if "token" in A.text:
            ql = A.content
            qlrequests = json.loads(ql)
            qltoken = qlrequests['data']['token']
            return qltoken
    except Exception:
        sender.reply("链接青龙失败,请检查对接容器！")
        exit(0)

def seekdd():
    try:
        if not dd_Kuwo_ddname:
            sender.reply("=====配置错误=====\n未配置呆呆面板信息\n请在插件配置中填写:\n• 对接面板类型: 呆呆\n• 对接面板配置: Host丨AppKey丨AppSecret\n• 使用中文丨分隔\n==================")
            exit(0)

        ddlist = dd_Kuwo_ddname.split('丨')
        if len(ddlist) != 3:
            sender.reply(f"=====格式错误=====\n呆呆面板配置格式错误\n当前格式: {dd_Kuwo_ddname}\n正确格式:\nHost丨AppKey丨AppSecret\n==================")
            exit(0)

        DDurl = ddlist[0].strip()
        AppKey = ddlist[1].strip()
        AppSecret = ddlist[2].strip()

        if not all([DDurl, AppKey, AppSecret]):
            sender.reply("=====参数错误=====\n呆呆面板配置参数不完整\n请确保以下参数都已填写:\n• 面板地址(Host)\n• AppKey\n• AppSecret\n==================")
            exit(0)

        if not DDurl.startswith(('http://', 'https://')):
            sender.reply(f"=====地址错误=====\n呆呆面板地址格式错误\n当前地址: {DDurl}\n正确格式:\n• http://panel.example.com\n• https://panel.example.com\n==================")
            exit(0)

        try:
            ddtoken = DDtoken(DDurl=DDurl, AppKey=AppKey, AppSecret=AppSecret)
            return DDurl, ddtoken
        except Exception as e:
            raise Exception(f"获取Token失败: {str(e)}")

    except SystemExit:
        raise
    except Exception as e:
        sender.reply(f"=====连接失败=====\n无法连接呆呆面板\n请检查:\n1. 面板是否运行\n2. 网络是否正常\n3. 配置是否正确\n4. 错误信息: {str(e)}\n==================")
        exit(0)

def DDtoken(DDurl, AppKey, AppSecret):
    try:
        url = f'{DDurl}/api/open-api/token'
        data = {"app_key": AppKey, "app_secret": AppSecret}
        response = requests.post(url, json=data)

        if response.status_code != 200:
            sender.reply(f"=====请求失败=====\n呆呆面板API请求失败\n状态码: {response.status_code}\n请检查:\n• API地址是否正确\n• 面板是否正常运行\n==================")
            exit(0)

        result = response.json()
        access_token = result.get('data', {}).get('access_token')
        if access_token:
            return access_token
        else:
            sender.reply("=====认证失败=====\n获取Token失败\n请检查:\n• AppKey是否正确\n• AppSecret是否正确\n• 应用是否有权限\n==================")
            exit(0)

    except requests.exceptions.RequestException as e:
        sender.reply(f"=====网络错误=====\n连接呆呆面板失败\n错误信息: {str(e)}\n==================")
        exit(0)
    except SystemExit:
        raise
    except Exception as e:
        sender.reply(f"=====系统错误=====\n处理请求时出错\n错误信息: {str(e)}\n==================")
        exit(0)

def get_dd_headers(content_type="application/json"):
    return {
        "Authorization": f"Bearer {panel_token}",
        "accept": "application/json",
        "Content-Type": content_type
    }

def dd_allenvs(osname, account):
    url = f"{panel_url}/api/envs"
    headers = get_dd_headers()
    params = {"keyword": str(account), "page_size": 100}
    response = requests.get(url=url, headers=headers, params=params).json()

    data_list = response.get('data', [])
    if isinstance(data_list, list):
        for envs in data_list:
            envname = envs.get('name', '')
            remarks = envs.get('remarks', '')
            if remarks is None:
                continue
            if osname == envname and str(account) in remarks:
                return envs['id']
        return None
    else:
        sender.reply("=====连接失败=====\n连接呆呆面板获取变量失败\n==================")
        exit(0)

def dd_delenvs(id):
    if id is None:
        return
    url = f"{panel_url}/api/envs/{id}"
    headers = get_dd_headers()
    requests.delete(url, headers=headers)

def DDcreate(osname, value, account, phone):
    try:
        url = f"{panel_url}/api/envs"

        data = {
            "value": value,
            "name": osname,
            "remarks": f'酷我:{account}丨用户:{userid}丨手机:{phone}'
        }
        if panel_group:
            data["group"] = panel_group

        headers = get_dd_headers()
        response = requests.post(url, headers=headers, json=data)

        if response.status_code not in (200, 201):
            sender.reply(f"=====添加变量失败=====\n请求失败\n状态码: {response.status_code}\n==================")
            return False

        result = response.json()
        resp_data = result.get('data')
        if resp_data:
            return True
        return False

    except SystemExit:
        raise
    except Exception as e:
        sender.reply(f"=====系统错误=====\n添加变量失败\n错误信息: {str(e)}\n==================")
        return False

def DDupdate(osname, value, account, env_id, phone):
    url = f"{panel_url}/api/envs/{env_id}"

    data = {
        "value": value,
        "name": osname,
        "remarks": f'酷我:{account}丨用户:{userid}丨手机:{phone}'
    }
    if panel_group:
        data["group"] = panel_group

    headers = get_dd_headers()
    response = requests.put(url, headers=headers, json=data)

    if response.status_code == 200:
        return True
    else:
        sender.reply("=====更新失败=====\n更新变量失败,请稍后重试\n==================")
        return False

def PluginsData():
    panel_type=normalize_panel_type(sg.bucketGet('dd_Kuwo_PluginsData','panel_type') or '',sg.bucketGet('dd_Kuwo_PluginsData','use_daidai') or 'false')
    raw=(sg.bucketGet('dd_Kuwo_PluginsData','panel_config') or '').strip()
    osname=sg.bucketGet('dd_Kuwo_PluginsData','osname') or 'Kuwo'
    group=(sg.bucketGet('dd_Kuwo_PluginsData','panel_group') or '').strip()
    if not panel_type or not raw:
        sender.reply('❌ 请配置面板类型和面板参数')
        raise SystemExit
    parts=[x.strip() for x in raw.split('丨')]
    if len(parts)!=3:
        sender.reply('❌ 面板配置格式应为 Host丨ID丨Secret')
        raise SystemExit
    if panel_type=='daidai':return '','','',0,osname,0,True,raw,group
    return parts[0],parts[1],parts[2],0,osname,0,False,'',group

def recognize_captcha(image_base64: str) -> str:
    try:
        ocr_url = 'https://ddddocr.linzixuan.work/classification'

        if ',' in image_base64:
            image_base64 = image_base64.split(',')[1]
        image_base64 = image_base64.replace('data:image/jpeg;base64,', '')
        image_base64 = image_base64.replace('data:image/png;base64,', '')

        data = {'image': image_base64}

        response = requests.post(
            ocr_url,
            json=data,
            timeout=10
        )

        result = response.json()
        if not result or 'result' not in result:
            raise Exception("验证码识别失败: 返回结果无效")

        return result['result'].strip()  # 返回result字段的值

    except Exception:
        raise

def login(value):
    try:
        values = value.split('#')
        if len(values) != 2:
            return "登录参数格式错误", "登录失败", False

        phone = values[0]
        password = values[1]

        captcha_url = 'http://www.kuwo.cn/api/common/captcha/getcode'
        captcha_params = {
            'reqId': 'bb7dd120-d1b7-11ef-b9c9-9dd176f54932',
            'httpsStatus': '1'
        }

        captcha_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/json',
            'Referer': 'http://www.kuwo.cn/',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }

        response = requests.get(
            captcha_url,
            params=captcha_params,
            headers=captcha_headers
        )

        if 'data' not in response.json():
            raise Exception("获取验证码失败")

        captcha_data = response.json()['data']
        image_data = captcha_data['img']
        token = captcha_data['token']

        verify_code = recognize_captcha(
            image_data.replace('data:image/jpeg;base64,', '')
        )

        login_url = 'https://wapi.kuwo.cn/api/www/login/loginByKw'
        login_data = json.dumps({
            'userIp': 'www.kuwo.cn',
            'uname': phone,
            'password': password,
            'verifyCode': verify_code,
            'img': image_data,
            'verifyCodeToken': token
        })

        login_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Origin': 'http://www.kuwo.cn',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'http://www.kuwo.cn/',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }

        login_response = requests.post(
            login_url,
            params={'httpsStatus': '1'},
            data=login_data,
            headers=login_headers,
            timeout=10
        )

        result = login_response.json()
        if result.get('code') != 200:
            raise Exception(f"登录失败: {result.get('msg', '未知错误')}")

        cookies = result['data']['cookies']
        username = cookies.get('uname3', phone)
        loginSid = cookies.get('websid')
        loginUid = cookies.get('userid')

        appUid = result['data'].get('uid', loginUid)
        devId = ''.join(random.choices('0123456789abcdef', k=16))

        token = f"{appUid}#{devId}#{loginSid}#{phone}"

        sg.bucketSet(bucket='dd_Kuwo_login', key=username, value=value)

        return username, loginSid, token

    except Exception as e:
        return f"登录异常: {str(e)}", "登录异常", False

def bind():
    sender.reply('请输入 手机号#密码；q退出')
    value=sender.input(120000,1,False)
    if not value or value.lower()=='q':return
    if len(value.split('#'))!=2:
        sender.reply('❌ 格式错误')
        return
    phone=value.split('#',1)[0]
    account,_,token=login(value)
    if token is False:
        sender.reply(str(account));return
    accounts=list(_sg_literal(sg.bucketGet('dd_Kuwo_bind',userid),[]));is_new=account not in accounts
    sg.bucketSet('dd_Kuwo_bind',userid,str(list(dict.fromkeys(accounts+[account]))));sg.bucketSet('dd_Kuwo_account',account,token);sg.bucketSet('dd_Kuwo_login',account,value)
    synced=Addenvs(osname=osname,value=value,account=account,phone=phone)
    sender.reply(f'✅ {"绑定" if is_new else "更新"}成功；面板'+('已同步' if synced else '同步失败'))

def Administration():
    accounts=list(_sg_literal(sg.bucketGet('dd_Kuwo_bind',userid),[]))
    if not accounts:
        sender.reply('❌ 未绑定酷我账号')
        return
    sender.reply('=====酷我管理=====\n'+'\n'.join(f'[{i}] {a}' for i,a in enumerate(accounts,1))+'\n回复序号；q退出')
    choice=sender.input(120000,1,False)
    if not str(choice).isdigit():return
    i=int(choice)-1
    if i not in range(len(accounts)):return
    account=accounts[i];token=sg.bucketGet('dd_Kuwo_account',account) or '';login_value=sg.bucketGet('dd_Kuwo_login',account) or ''
    sender.reply('[1] 查询 [2] 同步面板 [3] 查看登录配置 [4] 删除账号')
    action=sender.input(120000,1,False)
    if action=='1':query_one(account,token)
    elif action=='2':sender.reply('✅ 同步成功' if login_value and Addenvs(osname=osname,value=login_value,account=account,phone=login_value.split('#',1)[0]) else '❌ 同步失败')
    elif action=='3':sender.reply(login_value or '❌ 未保存登录配置')
    elif action=='4':
        sender.reply('确认删除请回复 y')
        if (sender.input(60000,1,False) or '').lower()=='y':
            env_id=allenvs(osname=osname,account=str(account))
            if env_id:delenvs(id=env_id)
            accounts.remove(account);sg.bucketSet('dd_Kuwo_bind',userid,str(accounts));sg.bucketDel('dd_Kuwo_account',account);sg.bucketDel('dd_Kuwo_login',account);sender.reply('✅ 已删除')

def query_withdraw_history(token):
    try:
        values = token.split('#')
        if len(values) != 4:
            return "获取账号信息失败"

        loginUid = values[0]
        loginSid = values[2]

        url = "https://integralapi.kuwo.cn/api/v1/online/sign/v1/withdrawDetails"
        params = {
            'loginUid': loginUid,
            'loginSid': loginSid,
            'pn': '1',  # 第一页
            'rn': '2'   # 只获取最近2条记录
        }

        headers = {
            'Host': 'integralapi.kuwo.cn',
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://h5app.kuwo.cn',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_7_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 KWMusic/11.1.2.0',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9'
        }

        response = requests.get(url, params=params, headers=headers)
        if response.status_code != 200:
            return "查询失败，请稍后重试"

        data = response.json()
        if data.get('code') != 200:
            return f"查询失败: {data.get('msg', '未知错误')}"

        records = data.get('data', {}).get('list', [])
        if not records:
            return "暂无提现记录"

        result = "=====提现记录=====\n"
        for record in records:
            status = record.get('status')
            status_text = {
                '0': '处理中',
                '1': '成功',
                '2': '失败'
            }.get(str(status), '未知状态')

            amount = record.get('amount', 0)
            date_str = record.get('dateTime', '')
            if date_str:
                try:
                    dt = datetime.strptime(date_str.split('.')[0], '%Y-%m-%dT%H:%M:%S')
                    beijing_tz = timezone(timedelta(hours=8))
                    dt = dt.replace(tzinfo=timezone.utc).astimezone(beijing_tz)
                    date_time = dt.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    date_time = date_str.replace('T', ' ').split('.')[0]
            else:
                date_time = '未知时间'

            result += (
                f"💰 金额: {amount}元\n"
                f"⏰ 时间: {date_time}\n"
                f"📝 状态: {status_text}\n"
                "-------------------\n"
            )
        return result.rstrip("-------------------\n") + "\n=================="

    except Exception as e:
        return f"查询提现记录失败: {str(e)}"

def query_one(account, token):
    if not token:
        sender.reply(f'❌ {account}: Token不存在');return
    point,today=cx(token)
    if isinstance(point,str):
        sender.reply(f'❌ {account}: {point}');return
    values=token.split('#');phone=values[3] if len(values)>3 else str(account);masked=phone[:3]+'****'+phone[-4:]
    sender.reply(f'=====酷我账号=====\n📱 {masked}\n💰 当前金币: {point}\n✨ 今日收益: {today}\n{query_withdraw_history(token)}')

def query():
    accounts=list(_sg_literal(sg.bucketGet('dd_Kuwo_bind',userid),[]))
    if not accounts:
        sender.reply('❌ 未绑定酷我账号');return
    for account in accounts:query_one(account,sg.bucketGet('dd_Kuwo_account',account) or '')

def cx(token):
    try:
        values = token.split('#')
        if len(values) != 4:
            return "登录参数格式错误", 0

        appuid = values[0]
        devid = values[1]
        loginSid = values[2]
        values[3]

        url = "https://integralapi.kuwo.cn/api/v1/online/sign/new/todayStatus"
        headers = {
            'Host': 'integralapi.kuwo.cn',
            'Accept': '*/*',
            'Cookie': f'tmeAppID=kwplayer;loginSid={loginSid};ct=1;newdevicelevel=0;deviceScore=0;loginUid={appuid};cv=11120;chid=TJ;os_ver=17.7.2;user={devid};nettype=WiFi;appUid={appuid}',
            'User-Agent': 'KWPlayer/11.1.2 (iPhone; iOS 17.7.2; Scale/3.00)',
            'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }

        params = {
            'uuid': devid,
            'newver': '3',
            'corp': 'kuwo',
            'uid': appuid,
            'loginSid': loginSid,
            'plat': 'ip',
            'source': 'kwplayer_ip_11.1.2.0_TJ.ipa',
            'loginUid': appuid,
            'prod': 'kwplayer_ip_11.1.2.0',
            'user': devid,
            'locationid': '1'
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            return f"HTTP错误: {response.status_code}", 0

        r = response.json()
        if r.get('code') != 200:
            return f"查询失败: {r.get('msg', '未知错误')}", 0

        remain_score = r['data']['remainScore']  # 总金币

        detail_url = "https://integralapi.kuwo.cn/api/v1/online/sign/v1/earningSignIn/userGoldDetail"
        detail_headers = {
            'Host': 'integralapi.kuwo.cn',
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://h5app.kuwo.cn',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_7_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 KWMusic/11.1.2.0',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9'
        }

        today_coin = 0
        page = 1
        has_more = True
        beijing_tz = timezone(timedelta(hours=8))
        today = datetime.now(beijing_tz).strftime("%Y-%m-%d")

        while has_more:
            detail_params = {
                'userId': appuid,
                'loginSid': loginSid,
                'pn': str(page),
                'rn': '50'
            }

            detail_response = requests.get(detail_url, headers=detail_headers, params=detail_params)
            if detail_response.status_code != 200:
                break

            detail_data = detail_response.json()
            if detail_data.get('code') != 200:
                break

            records = detail_data.get('data', {}).get('list', [])
            if not records:
                break

            found_today = False
            for item in records:
                date_str = item.get('dateTime', '')
                if date_str:
                    try:
                        utc_time = datetime.strptime(date_str.split('.')[0], '%Y-%m-%dT%H:%M:%S')
                        utc_time = utc_time.replace(tzinfo=timezone.utc)
                        beijing_time = utc_time.astimezone(beijing_tz)
                        record_date = beijing_time.strftime("%Y-%m-%d")

                        if record_date == today:
                            found_today = True
                            amount = int(item.get('amount', 0))
                            if amount > 0:  # 只计算正数（收入）
                                today_coin += amount
                    except:
                        continue

            if not found_today:
                has_more = False
            else:
                page += 1

        return remain_score, today_coin

    except Exception as e:
        return f"查询异常: {str(e)}", 0


def Addenvs(osname, value, account, phone):
    if use_daidai:
        env_id = dd_allenvs(osname, account)
        if env_id is None:
            return DDcreate(osname, value, account, phone)
        else:
            return DDupdate(osname, value, account, env_id, phone)

    try:
        url = f"{QLurl}/open/envs"
        headers = {
            "Authorization": "Bearer" + ' ' + qltoken,
            "accept": "application/json"
        }
        response = requests.get(url=url, headers=headers).json()
        qlid = None

        if response['code'] == 200:
            envslist = response['data']
            for envs in envslist:
                remarks = envs.get('remarks', '')
                if remarks and account in remarks and osname == envs['name']:
                    qlid = envs['id']
                    break
        else:
            sender.reply('连接青龙获取变量失败')
            return False

        if qlid is None:
            return QLzt(osname, value, account, phone)
        else:
            return QLupdate(osname, value, account, qlid, phone)
    except Exception as e:
        sender.reply(f'添加/更新青龙变量失败: {str(e)}')
        return False

def QLzt(osname, value, account, phone):
    try:
        url = f"{QLurl}/open/envs"
        data = [{
            "value": value,
            "name": osname,
            "remarks": f'酷我:{account}丨用户:{userid}丨手机:{phone}'
        }]
        headers = {
            "Authorization": f"Bearer {qltoken}",
            "accept": "application/json",
            "Content-Type": "application/json",
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code != 200:
            sender.reply("添加变量失败")
            return False

        result = response.json()
        if "value must be unique" in response.text:
            return True

        if result.get('code') == 200:
            return True
        else:
            sender.reply(f"添加变量失败: {result.get('message', '未知错误')}")
            return False

    except Exception as e:
        sender.reply(f"添加青龙变量错误: {str(e)}")
        return False

def QLupdate(osname, value, account, qlid, phone):
    try:
        url = f"{QLurl}/open/envs"
        data = {
            "value": value,
            "name": osname,
            "remarks": f'酷我:{account}丨用户:{userid}丨手机:{phone}',
            "id": qlid
        }
        headers = {
            "Authorization": f"Bearer {qltoken}",
            "accept": "application/json",
            "Content-Type": "application/json",
        }

        response = requests.put(url, headers=headers, data=json.dumps(data))
        if response.status_code != 200:
            sender.reply('更新变量失败')
            return False

        result = response.json()
        if result.get('code') == 200:
            return True
        else:
            sender.reply(f"更新变量失败: {result.get('message', '未知错误')}")
            return False

    except Exception as e:
        sender.reply(f'更新变量失败: {str(e)}')
        return False

def allenvs(osname, account):
    if use_daidai:
        return dd_allenvs(osname, account)

    url = f"{QLurl}/open/envs"
    headers = {
        "Authorization": "Bearer" + ' ' + qltoken,
        "accept": "application/json"
    }
    response = requests.get(url=url, headers=headers).json()
    qlid = None
    if response['code'] == 200:
        envslist = response['data']
        for envs in envslist:
            envname = envs['name']
            remarks = envs['remarks']
            if remarks is None:
                continue
            if osname == envname and str(account) in remarks:
                qlid = envs['id']
                break
        return qlid
    else:
        sender.reply('连接青龙获取变量失败')
        exit(0)

def delenvs(id):
    if id is None:
        return
    if use_daidai:
        dd_delenvs(id)
        return
    url = f"{QLurl}/open/envs"
    headers = {
        "Authorization": "Bearer" + ' ' + qltoken,
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    data = [id]
    requests.delete(url, headers=headers, json=data).json()






def tutorial():
    sender.reply('=====酷我教程=====\n酷我登录：绑定账号\n酷我查询：查询金币和提现记录\n酷我管理：查询、同步或删除账号\n==================')





QLurl,ClientID,ClientSecret,_,osname,_,use_daidai,dd_Kuwo_ddname,panel_group=PluginsData()
panel_url=panel_token=qltoken=''
if use_daidai:panel_url,panel_token=seekdd()
else:qltoken=QLtoken(QLurl,ClientID,ClientSecret)
usermessage=sender.getMessage()
if usermessage in ['酷我登录','酷我登陆','登陆酷我','登录酷我']:bind()
elif usermessage in ['酷我管理','管理酷我']:Administration()
elif usermessage in ['酷我查询','查询酷我']:query()
elif usermessage in ['酷我教程','酷我说明']:tutorial()
