# [title: 泰康在线]
# [name: taiKangZaiXian]
# [language: python]
# [class: 任务]
# [author: mrconli]
# [version: v1.5.0]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^泰康(.*)|(.*)泰康$]
# [cron: 0 8 * * *]
# [icon: https://pp.myapp.com/ma_icon/0/icon_42327729_1745494497/256]
# [description: AI练手，自用；仅提交青龙”；<1.5.0更新(20250515)：优化查询显示，优化青龙提交；>；1.4.0更新(20250430)：增加红包记录查询]
# [depe: ["aiohttp","httpx","requests","urllib3"]]


import asyncio as _sg_asyncio
import os as _sg_os
import time as _sg_time
import types as _sg_types
import json as _sg_json
from threading import Thread as _sg_Thread
from sillygirl import Adapter as _SGAdapter, Bucket as _SGBucket, Sender as _SGSender, sender as _sg_sender, form
calculate_auth_time = lambda *args, **kwargs: "2099-12-31"
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

config = form({
    'mrconli_taikang_ql_config': form.string().title('对接青龙地址').default('').description('使用丨分割'),
    'mrconli_taikang_var_name': form.string().title('环境变量名').default('').description('青龙容器内的变量名，默认为：mrconli_tkzx'),
    'mrconli_taikang_is_proxy': form.string().title('是否启用代理').default('').description('True/False'),
    'mrconli_taikang_proxy_pool': form.string().title('代理池地址').default('').description('代理API服务地址'),
})
_CONFIG_FIELD_MAP = {
    ('mrconli', 'taikang.ql_config'): 'mrconli_taikang_ql_config',
    ('mrconli', 'taikang.var_name'): 'mrconli_taikang_var_name',
    ('mrconli', 'taikang.is_proxy'): 'mrconli_taikang_is_proxy',
    ('mrconli', 'taikang.proxy_pool'): 'mrconli_taikang_proxy_pool',
}

import httpx
import os
from urllib.parse import urlencode
from datetime import datetime
import urllib3
from decimal import Decimal  # 处理浮点数
import time  # 处理时间
import json  # 处理json数据
import asyncio
from functools import lru_cache
import requests


urllib3.disable_warnings()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

senderID = sg.getSenderID()  # 获取发送者QQ号
sender = sg.Sender(senderID)  # 获取发送者对象
userid = sender.getUserID()  # 存储当前发送者的用户 ID，与 senderID 类似，但通常用于内部标识
uservalue = sg.bucketGet(bucket='mrconli.taikang.user', key=userid)
today_date = datetime.now().date()
today_time = str(today_date)

MAX_RETRIES = 5  # 最大重试次数
IS_PROXY = sg.bucketGet('mrconli.taikang', 'is_proxy') or "False"  # 是否启用代理True
PROXY_API = sg.bucketGet('mrconli.taikang', 'proxy_pool') or "http://10.10.10.251:12306/help/proxy/original"
if not PROXY_API:
    raise ValueError("代理池地址未配置，请在插件设置中配参")
proxy = None  # 初始化全局代理变量





def task_api(config):
    result = {}
    try:
        host = config['url'].split('//', 1)[-1].split('/', 1)[0]
        headers = {
            "Host": host,
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.25(0x18001929) NetType/WIFI Language/zh_CN",
            "Referer": "https://servicewechat.com/wx9e3e7020c4a10356/185/page-frame.html"
        }
        headers.update(config.get('headerParam', {}))

        with httpx.Client(timeout=5) as client:
            url = config['url']
            if 'queryParam' in config:
                url += '?' + urlencode(config['queryParam'], doseq=True)

            data = None
            if 'body' in config:
                content_type = config.get('Content-Type') or 'application/x-www-form-urlencoded'
                headers['Content-Type'] = content_type

                if isinstance(config['body'], dict):
                    if 'json' in content_type:
                        data = json.dumps(config['body'])
                    else:
                        processed_body = {}
                        for k, v in config['body'].items():
                            if isinstance(v, (dict, list)):
                                processed_body[k] = json.dumps(v, ensure_ascii=False)
                            else:
                                processed_body[k] = v
                        data = urlencode(processed_body, doseq=True)
                else:
                    data = str(config['body'])

            response = client.request(
                method=config.get('method', 'POST'),
                url=url,
                headers=headers,
                data=data,
                timeout=5
            )

            result['status_code'] = response.status_code
            result['resp'] = {
                'statusCode': response.status_code,
                'body': response.text
            }

            try:
                result['result'] = response.json()
            except json.JSONDecodeError as e:
                print(f"[{config.get('fn', '')}] 非JSON响应: {str(e)}")
                result['result'] = response.text

    except Exception as e:
        print(f"请求失败: {str(e)}")
    return result

def get_user_info(unionid):
    user_info = {
        'valid': False,
        'memberid': '',
        'token': '',
        'mobile': '',
        'name': ''
    }

    try:
        config = {
            'fn': 'getUserInfo',
            'method': 'POST',
            'url': 'https://m.tk.cn/member_api/',
            'body': {
                'api_s': 'member.userbind',
                'api_m': 'selectwxbindbybindid',
                'params': {
                    'platform': 'APPLET',
                    'fromid': '71672',
                    'bindid': unionid
                }
            }
        }
        response = task_api(config)
        if isinstance(response.get('result'), dict):
            res_data = response['result']
            if res_data.get('result') == 'success':
                user_info.update({
                    'valid': True,
                    'memberid': res_data['data']['memberid'],
                    'token': res_data['data']['token'],
                    'mobile': res_data['data']['pmemberuser']['membertmmobile'],
                    'name': res_data['data']['pmemberuser']['membertmrealname']
                })
                return user_info
            else:
                return None
        return user_info
    except Exception as e:
        print(f"获取用户信息异常：{str(e)}")
        return None


def main_page(unionid):
    user_info = get_user_info(unionid)
    memberid = user_info.get('memberid')
    token = user_info.get('token')
    mobile = user_info.get('mobile')
    name = user_info.get('name')
    try:
        config = {
            'fn': 'mainPage',
            'method': 'POST',
            'url': 'https://m.tk.cn/activity_execute/rest/membergoldbean/mainPage',
            'body': {
                'enc': False,
                'memberid': memberid,
                'token': token,
                'platform': 'WECHAT',
                'fromid': '71672'
            }
        }

        response = task_api(config)
        if isinstance(response.get('result'), dict):
            res_data = response['result']
            if res_data.get('error_code') in ['0', 0] and res_data.get('data') and 'allbeans' in res_data['data']:
                allbeans = res_data['data']['allbeans']

            else:
                err_msg = res_data.get('error_message') or res_data.get('message') or res_data.get('msg', '未知错误')
                print(f"查询金币失败：{err_msg}")
        return mobile, name, allbeans
    except Exception as e:
        print(f"主页面查询异常：{str(e)}")
        return {}

def get_coupon_list(unionid):
    user_info = get_user_info(unionid)
    memberid = user_info.get('memberid')
    token = user_info.get('token')
    """查询待领取红包列表"""
    try:
        config = {
            'fn': 'getCouponList',
            'method': 'POST',
            'url': 'https://m.tk.cn/member_api/',
            'body': {
                'api_s': 'member.coupon',
                'api_m': 'selectmembercouponlist',
                'params': {
                    'memberid': memberid,
                    'token': token,
                    'status': "1",  # 1-有效 2-已使用 3-已过期
                    'fromid': '67527'
                }
            }
        }

        response = task_api(config)
        if isinstance(response.get('result'), dict):
            res_data = response['result']
            if res_data.get('result') == 'success':
                coupons = res_data.get('data', {}).get('pmembercoupon', [])
                print(f"共{len(coupons)}个带领取：")
                for coupon in coupons:
                    print(f"待领红包: "
                          f"金额: {coupon.get('inventoryvalue','0.00')}元 "
                          f"有效期至: {coupon.get('voiddateend','未知日期')}")
                    dailingred = f"🍀【待领 {len(coupons)} 个红包】：\n"
                    dailingred_list = []
                    for coupon in coupons:
                        dailingred_list.append(f"🧧{coupon.get('couponname','未知')}: {coupon.get('inventoryvalue','0.00')}元\n⏰有效期至: {coupon.get('voiddateend','未知日期')}\n")
                    dailingred_show = "\n".join(dailingred_list)
                return dailingred, dailingred_show
            else:
                print(f"查询失败：{res_data.get('message', '未知错误')}")
                return ("", "")
        return ("", "")
    except Exception as e:
        print(f"优惠券查询异常：{str(e)}")
        return ("", "")

def get_mycoupon_list(unionid):
    user_info = get_user_info(unionid)
    memberid = user_info.get('memberid')
    token = user_info.get('token')
    try:
        config = {
            'fn': 'getCouponList',
            'method': 'POST',
            'url': 'https://m.tk.cn/member_api/',
            'body': {
                'api_s': 'member.coupon',
                'api_m': 'selectmembercouponlist',
                'params': {
                    'memberid': memberid,
                    'token': token,
                    'status': "2",  # 1-有效 2-已使用 3-已过期
                    'fromid': '67527'
                }
            }
        }

        response = task_api(config)
        if isinstance(response.get('result'), dict):
            res_data = response['result']
            if res_data.get('result') == 'success':
                coupons = res_data.get('data', {}).get('pmembercoupon', [])
                total = 0.0
                for coupon in coupons:
                    try:
                        total += float(coupon.get('inventoryvalue', '0.00'))
                    except:
                        pass
                print(f"共找到{len(coupons)}条已领红包记录，显示前5条")
                for coupon in coupons[:5]:
                    print(f"已领红包: "
                          f"金额: {coupon.get('inventoryvalue','0.00')}元 "
                          f"发放时间: {coupon.get('verifydate','未知日期')}")
                print(f"已领红包总金额: {total:.2f}元")
                huizongred_total = f"===================\n💰️累计 {len(coupons)} 个红包，共 {total:.2f} 元\n"
                yilingred_total = "\n🍃【已领红包】(近5条):\n"
                yilingred_list = []
                for coupon in coupons[:5]:
                    yilingred_list.append(f"🧧{coupon.get('couponname','未知')}: {coupon.get('inventoryvalue','0.00')}元\n⏰领取时间: {coupon.get('verifydate','未知日期')}\n")
                yilingred_show = "\n".join(yilingred_list)
                return yilingred_total, yilingred_show, huizongred_total
            else:
                print(f"查询失败：{res_data.get('message', '未知错误')}")
                return ("", "")
        return ("", "")
    except Exception as e:
        print(f"优惠券查询异常：{str(e)}")
        return ("", "")


def bind():
    sender.reply(
        "=====泰康账号登录=====\n"
        "📝 请输入登录参数:unionid\n"
        "抓包: 进小程序捉https://m.tk.cn/wechat_item/rest/xcx/login把返回里的unionid\n"
        "=====================\n"
        "⭐ 输入q退出操作\n"
    )
    unionid = sender.input(120000, 1, False)
    if unionid == '':
        sender.reply('输入超时！')
        exit(0)
    elif unionid.lower() == 'q':
        sender.reply('退出操作！')
        exit(0)
    user_info = get_user_info(unionid)

    memberid = user_info.get('memberid')
    mobile = user_info.get('mobile')
    name = user_info.get('name')

    if mobile is None:
        sender.reply('登录失败，无法获取账户信息')
        exit(0)
    try:
        try:
            accounts = json.loads(str(uservalue)) if uservalue else []
        except (json.JSONDecodeError, TypeError):
            return
        account = f"{memberid}"
        if account not in accounts:
            dlzt = "登录"
            accounts.append(account)
            sg.bucketSet('mrconli.taikang.user', userid, json.dumps(accounts))
        else:
            dlzt = "更新"
            add_to_qinglong(unionid, account, userid)
        sg.bucketSet('mrconli.taikang.token', account, unionid)
        sg.bucketSet('mrconli.taikang.mobile', account, mobile)
        success_msg = f"""
====={dlzt}成功=====
📱 账号: {mobile}
------------------
发送"{manage_cmd}"管理账号
发送"{query_cmd}"查询账号
"""
        sender.reply(success_msg)
        return mobile, name
    except Exception as e:
        sender.reply(f"❌ 处理登录失败: {str(e)}")
        exit(0)



def query():
    accounts = _sg_literal(uservalue or '[]')
    if not accounts:
        sender.reply(
            '\n=====泰康账号查询=====\n❌ 未找到任何账号\n------------------\n💡 发送"泰康登录"绑定账号\n===================')
        return
    if len(accounts) > 1:
        menu = "=====请选择查询账号=====\n"
        menu += "[0] 查询全部账号\n"
        for idx, acc in enumerate(accounts, 1):
            menu += f"[{idx}] {acc[:3]}****{acc[-4:]}\n"
        menu += "=======================\n⚠️ 请回复数字序号(输入q退出)"
        sender.reply(menu)

        choice = sender.input(30000, 1, False)
        if choice.lower() == 'q':
            sender.reply('已取消查询')
            return
        if not choice.isdigit():
            sender.reply('输入格式错误，请回复数字')
            return

        choice = int(choice)
        if choice < 0 or choice > len(accounts):
            sender.reply('选择超出范围，已取消查询')
            return
    else:
        choice = 1  # 单个账号直接查询

    if choice == 0:
        target_accounts = accounts
        sender.reply('正在查询全部账号...')
    else:
        target_accounts = [accounts[choice - 1]]
        sender.reply('正在查询泰康，请耐心等待...')

    for account in target_accounts:

        try:
            accountVip = '2099-12-31'
            Token = sg.bucketGet('mrconli.taikang.token', account)
            if not Token:
                sender.reply(f'【{account}】Token获取失败')
                continue
            if not accountVip:
                sender.reply(f'【{account}】账号未授权')
            elif accountVip < today_time:
                sender.reply(f'【{account}】云授权过期')
            else:
                mobile, name, balance = main_page(Token)
                dailingred, dailingred_show = get_coupon_list(Token)
                yilingred_total, yilingred_show,huizongred_total = get_mycoupon_list(Token)
                if mobile is None:
                    sender.reply('查询失败，无法获取账户信息')
                    continue
                sender.reply(
                    "=====泰康账号详情=====\n"
                    f"📱 账号: {mobile}\n"
                    f"👤 实名: {'* * '+name[-1] if name else '***'}\n"
                    f"💰 金币: {balance}\n"
                    f"⏰ 授权期限: {accountVip}\n"
                    "===================\n"
                    f"{dailingred}{dailingred_show}"
                    f"{yilingred_total}{yilingred_show}"
                    f"{huizongred_total}"
                    "===================\n"
                    )
        except Exception as e:
            sender.reply(f'【{mobile}】查询出错: {str(e)}')


def get_config():
    try:

        coin_bucket = sg.bucketGet('mrconli.taikang', 'coin_bucket') or 'dd_sign_points'
        sg.bucketSet('mrconli.taikang', 'coin_bucket', coin_bucket)  # 确保配置项存在
        var_name = sg.bucketGet('mrconli.taikang', 'var_name') or "mrconli_tkzx"
        if not var_name:
            print("未配置变量名，使用默认值: mrconli_tkzx")
            var_name = 'mrconli_tkzx'
            sg.bucketSet('mrconli.taikang', 'var_name', var_name)
        ql_config = sg.bucketGet('mrconli.taikang', 'ql_config')
        ql_params = ql_config.split('丨')
        if len(ql_params) == 3:
            ql_host = ql_params[0]
            ql_client_id = ql_params[1]
            ql_client_secret = ql_params[2]
        else:
            print("青龙配置不完整，请检查配置")
        manage_cmd = sg.bucketGet('mrconli.taikang', 'manage_cmd') or '泰康管理'
        query_cmd = sg.bucketGet('mrconli.taikang', 'query_cmd') or '泰康查询'
        login_cmd = sg.bucketGet('mrconli.taikang', 'login_cmd') or '泰康登录'
        try:
            price = Decimal(sg.bucketGet('mrconli.taikang', 'price') or '1')
            if price < 0:
                raise ValueError("价格不能为负数")
        except (ValueError, decimal.InvalidOperation):
            print("价格配置无效，使用默认值: 1")
            price = Decimal('1')
            sg.bucketSet('mrconli.taikang', 'price', '1')
        try:
            coin_price = int(sg.bucketGet('mrconli.taikang', 'coin') or '0')
            if coin_price < 0:
                raise ValueError("积分不能为负数")
        except ValueError:
            print("积分配置无效，使用默认值: 0")
            coin_price = 0
            sg.bucketSet('mrconli.taikang', 'coin', '0')
        return (var_name, ql_host, ql_client_id, ql_client_secret, manage_cmd, query_cmd, login_cmd, price, coin_price)
    except Exception as e:
        error_msg = f"获取配置失败: {str(e)}"
        print(error_msg)
        sender.reply(f"❌ {error_msg}")
        raise


def init_qinglong():
    try:
        ql_config = sg.bucketGet('mrconli.taikang', 'ql_config')
        ql_params = ql_config.split('丨')
        if len(ql_params) == 3:
            ql_host = ql_params[0]
            ql_client_id = ql_params[1]
            ql_client_secret = ql_params[2]
        else:
            print("青龙配置不完整，请检查配置")
            exit(0)
        if not ql_host.endswith('/'):
            ql_host += '/'
        token = get_ql_token(ql_host, ql_client_id, ql_client_secret)
        return ql_host, token
    except Exception as e:
        sender.reply(f"❌ 连接青龙失败: {str(e)}")
        exit(0)


def get_ql_token(url, client_id, client_secret):
    try:
        if not url.endswith('/'):
            url += '/'
        r = requests.get(f'{url}open/auth/token?client_id={client_id}&client_secret={client_secret}')
        if r.status_code != 200:
            raise Exception(f"请求失败: {r.status_code}")
        data = r.json()
        if "token" not in data.get('data', {}):
            raise Exception("获取token失败")
        return data['data']['token']
    except Exception as e:
        raise Exception(f"获取token失败: {str(e)}")


def add_to_qinglong(token, account, username):
    try:
        url = f"{ql_host}/open/envs"
        headers = {
            "Authorization": f"Bearer {ql_token}",
            "Content-Type": "application/json"
        }

        existing_ids = []
        duplicate_vars = []
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            for env in response.json().get('data', []):
                if env['name'] == var_name and env.get('remarks', '') and account in env.get('remarks', ''):
                    existing_ids.append(env['id'])
                elif env['value'] == token:  # 新增重复值检测
                    duplicate_vars.append(env['id'])

        if duplicate_vars:
            del_response = requests.delete(url, json=duplicate_vars, headers=headers)
            if del_response.status_code != 200:
                raise Exception(f"删除冲突变量失败: {del_response.text}")

        if existing_ids:
            del_response = requests.delete(url, json=existing_ids, headers=headers)
            if del_response.status_code != 200:
                raise Exception(f"删除旧变量失败: {del_response.text}")

        auth_time = '2099-12-31' or '未授权'
        data = {
            "name": var_name,
            "value": token,
            "remarks": f"泰康账号:{account}丨用户:{userid}丨授权时间:{auth_time}",
        }

        max_retries = 3
        for attempt in range(max_retries):
            response = requests.post(url, headers=headers, json=[data])
            if response.status_code == 200:
                new_ids = [item['id'] for item in response.json().get('data', [])]
                sg.bucketSet('mrconli.taikang.env_id', account, json.dumps(new_ids))
                return True
            elif response.status_code == 500 and "SequelizeUniqueConstraintError" in response.text:
                print(f"🔄 检测到唯一性冲突，正在重试 ({attempt+1}/{max_retries})")
                time.sleep(1)

        error_detail = response.json().get('message') or response.text
        raise Exception(f"操作失败：多次尝试后仍存在唯一性冲突 | {error_detail} [HTTP {response.status_code}]")

    except Exception as e:
        error_msg = f"青龙操作失败: {str(e)}"
        print(error_msg)
        sender.reply(f"❌ {error_msg}")
        return False


def enable_in_qinglong(env_ids):
    try:
        url = f"{ql_url}/open/envs/enable"
        headers = {
            "Authorization": f"Bearer {ql_token}",
            "Content-Type": "application/json"
        }
        response = requests.put(url, headers=headers, data=json.dumps(env_ids))
        if response.status_code == 200:
            rjson = response.json()
            if rjson.get('code') == 200:
                return True
            else:
                sender.reply(f"❌ 启用环境变量失败: {rjson.get('message')}")
                return False
        else:
            raise Exception(f"{response.status_code}")
    except Exception as e:
        sender.reply(f"❌ 启用环境变量失败: {str(e)}")
        return False


def disable_in_qinglong(env_ids):
    try:
        url = f"{ql_url}/open/envs/disable"
        headers = {
            "Authorization": f"Bearer {ql_token}",
            "Content-Type": "application/json"
        }
        response = requests.put(url, headers=headers, data=json.dumps(env_ids))
        if response.status_code == 200:
            rjson = response.json()
            if rjson.get('code') == 200:
                return True
            else:
                sender.reply(f"❌ 禁用环境变量失败: {rjson.get('message')}")
                return False
        else:
            raise Exception(f"{response.status_code}")
    except Exception as e:
        sender.reply(f"❌ 禁用环境变量失败: {str(e)}")
        return False


def delete_from_qinglong(account):
    try:
        url = f"{ql_url}/open/envs"
        headers = {
            "Authorization": f"Bearer {ql_token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception("获取变量失败")
        env_id = None
        for env in response.json()['data']:
            if env['name'] == var_name and account in env.get('remarks', ''):
                env_id = env['id']
                break
        if env_id:
            response = requests.delete(url, headers=headers, json=[env_id])
            if response.status_code != 200:
                raise Exception("删除变量失败")
        return True
    except Exception as e:
        sender.reply(f"❌ 青龙操作失败: {str(e)}")
        return False


def manage_accounts():
    accounts = _sg_literal(uservalue)
    if not accounts:
        sender.reply(f"""
=====账号管理=====
❌ 未找到任何账号
------------------
💡 发送"{login_cmd}"绑定账号
==================""")
        return

    account_list = """
=====账号列表=====
批量操作:
[00] 授权全部账号
[01] 删除全部账号
------------------
账号列表:"""
    for i, account in enumerate(accounts, 1):
        token = sg.bucketGet('mrconli.taikang.token', account)
        auth = '2099-12-31'
        mobile = sg.bucketGet('mrconli.taikang.mobile', account)
        auth_status = "✅ 已授权" if auth and auth > today else "❌ 未授权"
        username = f"{account}"
        account_list += f"\n[{i}] {mobile}\n    {auth_status}"
        if auth and auth > today:
            account_list += f"\n    授权到期: {auth}"
    account_list += "\n------------------\n回复数字选择账号\n回复'q'退出"

    sender.reply(account_list)
    choice = sender.listen(60000)

    if not choice:
        sender.reply("❌ 操作超时")
        return
    elif choice == 'q':
        sender.reply("✅ 已取消操作")
        return

    try:
        if choice == '01':
            accounts.copy()
            for account in accounts:
                delete_account(account)
            sg.bucketSet('mrconli.taikang.user', userid, '[]')
            sender.reply("✅ 已删除全部账号")

        elif choice == '00':
            sender.reply("请输入授权天数:")
            days = sender.listen(60000)
            if not days:
                sender.reply("❌ 操作超时")
                return
            elif days == 'q':
                sender.reply("✅ 已取消授权")
                return
            coin_bucket = sg.bucketGet('mrconli.taikang', 'coin_bucket') or 'dd_sign_points'
            coin_price = int(sg.bucketGet('mrconli.taikang', 'coin') or '0')  # 确保获取最新积分价格

            try:
                days = int(days)
                if days <= 0:
                    raise ValueError("天数必须大于0")

                pay_choice = '1'
                if coin_price > 0:
                    user_coin = Decimal(sg.bucketGet('coin_bucket', userid) or '0')
                    auth_guide = f"""
=====批量授权方式=====
[1] 微信支付
[2] 积分支付 (当前积分: {user_coin})
--------------------
💰 积分比例: {coin_price}积分/月
回复数字选择方式"""
                    sender.reply(auth_guide)
                    pay_choice = sender.listen(60000)
                    if pay_choice not in ['1', '2']:
                        sender.reply("❌ 无效的支付方式")
                        return

                if pay_choice == '1':
                    amount = price * (Decimal(days) / 30) * len(accounts)
                    amount = amount.quantize(Decimal('0.01'), rounding='ROUND_UP')
                    if process_payment(amount, days):
                        success_count = 0
                        for account in accounts:
                            calculate_auth_time(account, days / 30)
                            True
                            token = sg.bucketGet('mrconli.taikang.token', account)
                            username = account
                            if token and username:
                                add_to_qinglong(token, account, username)

                            success_count += 1
                        sender.reply(f"""
=====批量授权成功=====
💰 支付: {amount}元
⏰ 时长: {days}天
✅ 成功: {success_count}个账号
====================""")

                elif pay_choice == '2':
                    coin_bucket = sg.bucketGet('mrconli.taikang', 'coin_bucket') or 'dd_sign_points'
                    user_coin = Decimal(sg.bucketGet(coin_bucket, userid) or '0')
                    months = days / 30
                    if months != int(months):
                        sender.reply("❌ 积分支付需整月授权")
                        return
                    months = int(months)
                    need_coin = coin_price * months * len(accounts)
                    if user_coin < need_coin:
                        sender.reply(f"""
=====积分不足=====
❌ 积分余额不足
------------------
💰 所需积分: {need_coin}
💵 当前积分: {user_coin}
====================""")
                        return

                    new_coin = user_coin - need_coin
                    sg.bucketSet(coin_bucket, userid, str(new_coin))
                    success_count = 0
                    for account in accounts:
                        calculate_auth_time(account, months)
                        True
                        token = sg.bucketGet('mrconli.taikang.token', account)
                        username = account
                        if token and username:
                            add_to_qinglong(token, account, username)

                        success_count += 1
                    sender.reply(f"""
=====批量授权成功=====
💰 消耗: {need_coin}积分
⏰ 时长: {days}天
✅ 成功: {success_count}个账号
💵 剩余: {new_coin}积分
====================""")

                for account in accounts:
                    env_id_str = sg.bucketGet('mrconli.taikang.env_id', account)
                    if env_id_str:
                        env_ids = json.loads(env_id_str)
                        enable_in_qinglong(env_ids)

            except ValueError as ve:
                sender.reply(f"❌ 无效的输入: {str(ve)}")
            except Exception as e:
                sender.reply(f"❌ 批量授权失败: {str(e)}")

        else:
            index = int(choice) - 1
            if 0 <= index < len(accounts):
                show_account_menu(accounts[index])
            else:
                sender.reply("❌ 无效的序号")

    except Exception as e:
        sender.reply(f"❌ 操作失败: {str(e)}")


def show_account_menu(account):
    token = sg.bucketGet('mrconli.taikang.token', account)
    auth = '2099-12-31'
    if len(token) == 32:
        username = f"Token...{token[-6:]}"
    else:
        username = f"{account}"
    auth_status = "✅ 已授权" if auth and auth > today else "❌ 未授权"
    auth_info = f"\n    到期: {auth}" if auth and auth > today else ""
    menu = f"""
=====账号操作=====
📱 账号: {username[:3]}****{username[-4:]}
🔐 状态: {auth_status}{auth_info}
------------------
[1] 授权账号
[2] 删除账号
------------------
回复数字选择操作
回复"q"退出"""
    sender.reply(menu)
    choice = sender.listen(60000)
    if not choice:
        sender.reply("❌ 操作超时")
        return
    elif choice == 'q':
        sender.reply("✅ 已取消操作")
        return
    try:
        if choice == '1':
            auth_account(account)
        elif choice == '2':
            delete_account(account)
        else:
            sender.reply("❌ 无效的选择")
    except Exception as e:
        sender.reply(f"❌ 操作失败: {str(e)}")


def auth_account(account):
    try:
        coin_bucket = sg.bucketGet('mrconli.taikang', 'coin_bucket') or 'dd_sign_points'
        user_coin = sg.bucketGet(coin_bucket, userid) or '0'
        user_coin = Decimal(user_coin)  # 使用 Decimal 处理大数值
        month_coin = Decimal(coin_price)  # 从配置获取每月所需积分
        if month_coin <= 0:
            auth_guide = """
=====授权方式=====
[1] 微信支付
------------------
回复数字选择方式
回复"q"退出"""
        else:
            auth_guide = f"""
=====授权方式=====
[1] 微信支付
[2] 积分支付 (当前积分: {user_coin})
------------------
💰 积分比例: {month_coin}积分/月
回复数字选择方式
回复"q"退出"""
        sender.reply(auth_guide)
        choice = sender.listen(60000)
        if not choice:
            sender.reply("❌ 操作超时")
            return False
        elif choice == 'q':
            sender.reply("✅ 已取消授权")
            return False
        if choice == '1':
            sender.reply("请输入授权天数:")
            days = sender.listen(60000)
            if not days:
                sender.reply("❌ 操作超时")
                return False
            elif days == 'q':
                sender.reply("✅ 已取消授权")
                return False
            days = int(days)
            if days <= 0:
                raise ValueError()
            amount = price * (Decimal(days) / Decimal(30))
            amount = Decimal(str(amount)).quantize(Decimal('0.01'), rounding='ROUND_UP')
            if amount < Decimal('0.01'):
                amount = Decimal('0.01')
            payment_success = process_payment(amount, days)  # 处理支付
            if payment_success:  # 只有在支付成功的情况下才进行授权
                auth_time = calculate_auth_time(account, days / 30)
                True
                token = sg.bucketGet('mrconli.taikang.token', account)
                username = account  # 假设account存储的是手机号
                if token and username:
                    add_to_qinglong(token, account, username)  # 强制更新变量
                else:
                    sender.reply("⚠️ 令牌获取失败，请检查配置")
                env_id_str = sg.bucketGet('mrconli.taikang.env_id', account)
                if env_id_str:
                    env_ids = json.loads(env_id_str)
                    enable_in_qinglong(env_ids)
                sender.reply(f"""
=====授权成功=====
📱 账号: {account}
💰 支付: {amount}元
⏰ 时长: {days}天
📅 到期: {auth_time}
==================""")
                return True
            else:
                sender.reply("❌ 支付未成功，授权未完成")
                return False
        elif choice == '2' and month_coin > 0:  # 只有积分支付开启时才处理
            sender.reply("请输入授权月数:")
            months = sender.listen(60000)
            if not months:
                sender.reply("❌ 操作超时")
                return False
            elif months == 'q':
                sender.reply("✅ 已取消授权")
                return False
            months = int(months)
            if months <= 0:
                raise ValueError()
            need_coin = month_coin * months
            if user_coin < need_coin:
                sender.reply(f"""
=====积分不足=====
❌ 积分余额不足
------------------
💰 所需积分: {need_coin}
💵 当前积分: {user_coin}
==================""")
                return False
            new_coin = user_coin - need_coin
            sg.bucketSet('coin_bucket', userid, str(new_coin))
            auth_time = calculate_auth_time(account, months)
            True
            token = sg.bucketGet('mrconli.taikang.token', account)
            username = account  # 假设account存储的是手机号
            if token and username:
                add_to_qinglong(token, account, username)  # 强制更新变量
            else:
                sender.reply("⚠️ 令牌获取失败，请检查配置")

            env_id_str = sg.bucketGet('mrconli.taikang.env_id', account)
            if env_id_str:
                env_ids = json.loads(env_id_str)
                enable_in_qinglong(env_ids)
            sender.reply(f"""
=====授权成功=====
📱 账号: {account}
💰 消耗: {need_coin}积分
⏰ 时长: {months}月
📅 到期: {auth_time}
------------------
💵 剩余: {new_coin}积分
==================""")
            return True
        else:
            sender.reply("❌ 无效的选择")
    except ValueError:
        sender.reply("❌ 无效的数值")
    except Exception as e:
        sender.reply(f"❌ 授权失败: {str(e)}")
    return False


def process_payment(amount, days):
    return True

def clean_expired():
    try:
        sender.reply('该管理项已取消，账号直接运行')
    except Exception:
        pass
    return None
def cron_task():
    if imtype != 'fake':
        return
    try:
        users = sg.bucketAllKeys('mrconli.taikang.user')
        for user in users:
            accounts = _sg_literal(sg.bucketGet('mrconli.taikang.user', user) or '[]')
            for account in accounts:
                try:
                    token = sg.bucketGet('mrconli.taikang.token', account)
                    if not token:
                        continue
                    auth = '2099-12-31'
                    if auth and auth <= today:
                        env_id_str = sg.bucketGet('mrconli.taikang.env_id', account)
                        if env_id_str:
                            env_ids = json.loads(env_id_str)
                            disable_in_qinglong(env_ids)
                        notify_user(user, account, "授权已过期,环境变量已禁用,请及时续费")
                        continue
                except Exception as e:
                    print(f"处理账号 {account} 出错: {str(e)}")
                    continue
    except Exception as e:
        print(f"定时任务出错: {str(e)}")


def notify_user(user, account, message):
    try:
        notify_msg = f"""
=====账号通知=====
📱 账号: {account}
📢 消息: {message}
=================="""
        sg.push('qq', '', user, '', notify_msg)
        sg.push('wx', '', user, '', notify_msg)
        sg.push('tg', '', user, '', notify_msg)
    except Exception as e:
        print(f"发送通知失败: {str(e)}")




def log_operation(operation, user, account, status, message=''):
    try:
        log = {
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'operation': operation,
            'user': user,
            'account': account,
            'status': status,
            'message': message
        }
        logs = _sg_literal(sg.bucketGet('mrconli.taikang.logs', 'operations') or '[]')
        logs.append(log)
        if len(logs) > 1000:  # 只保留最近1000条
            logs = logs[-1000:]
        sg.bucketSet('mrconli.taikang.logs', 'operations', str(logs))
    except Exception as e:
        print(f"记录日志失败: {str(e)}")


def admin_auth():
    try:
        sender.reply('该管理项已取消，账号直接运行')
    except Exception:
        pass
    return None






def delete_account(account):
    try:
        if not delete_from_qinglong(account):
            raise Exception("从青龙删除变量失败")
        sg.bucketDel('mrconli.taikang.token', account)
        True
        sg.bucketDel('mrconli.taikang.env_id', account)
        try:
            accounts = json.loads(str(uservalue)) if uservalue else []
        except (json.JSONDecodeError, TypeError) as e:
            print(f"用户列表解析失败: {str(e)}")
            accounts = []

        if account in accounts:
            accounts.remove(account)
            try:
                sg.bucketSet('mrconli.taikang.user', userid, json.dumps(accounts, ensure_ascii=False))
            except Exception as e:
                raise Exception(f"用户列表更新失败: {str(e)}")
        sender.reply(f"""
=====删除成功=====
📱 账号: {account}
✅ 状态: 已删除
==================""")
        log_operation('delete_account', userid, account, 'success')
        return True
    except Exception as e:
        error_msg = f"删除账号失败: {str(e)}"
        sender.reply(f"❌ {error_msg}")
        log_operation('delete_account', userid, account, 'failed', str(e))
        return False




@lru_cache(maxsize=100)
def cached_bucket_get(bucket, key):
    return sg.bucketGet(bucket, key)


login_data = globals().get("login_data", {})





def tutorial():
    tutorial_text = (
        "=====泰康教程=====\n"
        "🌟 基础指令:\n"
        "1. 泰康登录 - 绑定账号\n"
        "2. 泰康查询 - 查看状态\n"
        "3. 泰康管理 - 管理账号\n"
        "4. 泰康授权 - 管理员授权账号\n"
        "4. 泰康清理 - 管理员清理过期\n"
        "-------------------\n"
        "🚩 收益说明:\n"
        "▸ 呆瓜为每日自动运行签到\n"
        "▸ 每礼拜可领一个低保0.3红包\n"
        "▸ 需要实名、绑定微信\n"
        "-------------------\n"
        "⚠️ 注意事项:\n"
        "1. 建议私聊登录更安全\n"
        "2. 需要手动提现\n"
        "=================="
    )
    sender.reply(tutorial_text)


def main():
    message = sender.getMessage()
    if '登录' in message:
        bind()
    elif '管理' in message:
        manage_accounts()
    elif '查询' in message:
        query()
    elif '教程' in message:
        tutorial()
    elif message == '泰康清理':
        clean_expired()
    elif message == '泰康授权' and sender.isAdmin():
        admin_auth()
    else:
        sender.setContinue()


if __name__ == "__main__":
    try:
        var_name, ql_host, ql_client_id, ql_client_secret, manage_cmd, query_cmd, login_cmd, price, coin_price = get_config()
        ql_url, ql_token = init_qinglong()
        imtype = sender.getImtype()
        today = str(datetime.now().date())
        if imtype == 'fake':
            cron_task()
        else:
            main()
    except Exception as e:
        sender.reply(f"❌ 运行出错: {str(e)}")
