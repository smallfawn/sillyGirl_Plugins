# [title: 夸克推广]
# [name: kuaKeTuiGuang]
# [language: python]
# [class: 任务]
# [author: rujingxianghai]
# [version: v1.0.0]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^我要看(.+)$|^夸克清理$|^夸克登录$]
# [icon: https://api.iconify.design/lucide:apple.svg]
# [description: 使用方法：发送"我要看XXXX"进行搜索；推广方法：关注公众号"蜂小推"，邀请码：15999112，申请夸克网盘推广项目即可]
# [depe: ["httpx","requests"]]
# [staticmethod: def get_pwd_id(share_url: str) -> str:]


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
    'quark_search_cookies': form.string().title('夸克网盘Cookie').default('').description('夸克网盘的Cookie字符串'),
    'quark_search_save_folder': form.string().title('保存文件夹名称').default('').description('转存时的保存文件夹名称，留空则随机生成'),
    'quark_search_share_option': form.string().title('分享选项').default('').description('1=公开永久 2=公开1天 3=公开7天 4=公开30天 5=加密永久 6=加密1天 7=加密7天 8=加密30天'),
    'quark_search_search_api': form.string().title('搜索API地址').default('').description('搜索API，自建项目：https://github.com/fish2018/pansou'),
    'quark_search_clean_folder_id': form.string().title('清理文件夹ID').default('').description('需要清理的文件夹ID，留空则不启用清理功能'),
})
_CONFIG_FIELD_MAP = {
    ('quark_search', 'cookies'): 'quark_search_cookies',
    ('quark_search', 'save_folder'): 'quark_search_save_folder',
    ('quark_search', 'share_option'): 'quark_search_share_option',
    ('quark_search', 'search_api'): 'quark_search_search_api',
    ('quark_search', 'clean_folder_id'): 'quark_search_clean_folder_id',
}

import asyncio
import re
import httpx
import random
import json
import time
import requests
import uuid
from datetime import datetime
from typing import List, Dict, Union, Tuple, Any

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()
imtype = sender.getImtype()
username = sender.getUserName()

def get_timestamp(length: int = 13) -> str:
    """获取时间戳"""
    timestamp = int(time.time() * 1000)  # 毫秒时间戳
    return str(timestamp)[:length]


def generate_random_code(length: int = 4) -> str:
    """生成随机码"""
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])


def generate_qrcode(url):
    """生成二维码图片

    Args:
        url: 要生成二维码的URL

    Returns:
        str: 二维码API的URL
    """
    try:
        encoded_url = requests.utils.quote(url)
        api_url = f"https://api.qrtool.cn/?text={encoded_url}&size=300&level=M"
        return api_url
    except Exception as e:
        return None


def parse_datetime(dt_str: str) -> str:
    """解析日期时间字符串，返回日期部分"""
    try:
        if dt_str == "0001-01-01T00:00:00Z":
            return "未知"
        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d")
    except:
        return "未知"


class QuarkAutoSaveAndShare:
    """夸克网盘自动转存并分享类"""

    def __init__(self, cookies: str) -> None:
        """
        初始化

        Args:
            cookies: 夸克网盘的cookie字符串
        """
        if not cookies or not cookies.strip():
            raise ValueError("cookies不能为空")
        self.cookies: str = cookies.strip()
        self.headers: Dict[str, str] = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/94.0.4606.71 Safari/537.36 Core/1.94.225.400 QQBrowser/12.2.5544.400',
            'origin': 'https://pan.quark.cn',
            'referer': 'https://pan.quark.cn/',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': self.cookies,
        }

    @staticmethod
    def get_pwd_id(share_url: str) -> str:
        """从分享链接提取pwd_id"""
        return share_url.split('?')[0].split('/s/')[-1]

    async def get_stoken(self, pwd_id: str, password: str = '') -> Tuple[str, str]:
        """获取stoken，返回(stoken, error_message)"""
        params = {
            'pr': 'ucpro',
            'fr': 'pc',
            'uc_param_str': '',
            '__dt': random.randint(100, 9999),
            '__t': get_timestamp(13),
        }
        api = "https://drive-pc.quark.cn/1/clouddrive/share/sharepage/token"
        data = {"pwd_id": pwd_id, "passcode": password}
        async with httpx.AsyncClient() as client:
            timeout = httpx.Timeout(60.0, connect=60.0)
            response = await client.post(api, json=data, params=params, headers=self.headers, timeout=timeout)
            json_data = response.json()
            if json_data['status'] == 200 and json_data['data']:
                stoken = json_data["data"]["stoken"]
                return stoken, ''
            else:
                error_msg = json_data.get('message', '获取stoken失败')
                return '', error_msg

    async def get_detail(self, pwd_id: str, stoken: str, pdir_fid: str = '0') -> Tuple[
        str, List[Dict[str, Union[int, str]]]]:
        """获取分享文件详情"""
        api = "https://drive-pc.quark.cn/1/clouddrive/share/sharepage/detail"
        page = 1
        file_list: List[Dict[str, Union[int, str]]] = []

        async with httpx.AsyncClient() as client:
            while True:
                params = {
                    'pr': 'ucpro',
                    'fr': 'pc',
                    'uc_param_str': '',
                    "pwd_id": pwd_id,
                    "stoken": stoken,
                    'pdir_fid': pdir_fid,
                    'force': '0',
                    "_page": str(page),
                    '_size': '50',
                    '_sort': 'file_type:asc,updated_at:desc',
                    '__dt': random.randint(200, 9999),
                    '__t': get_timestamp(13),
                }

                timeout = httpx.Timeout(60.0, connect=60.0)
                response = await client.get(api, headers=self.headers, params=params, timeout=timeout)
                json_data = response.json()

                is_owner = json_data['data']['is_owner']
                _total = json_data['metadata']['_total']
                if _total < 1:
                    return is_owner, file_list

                _size = json_data['metadata']['_size']
                _count = json_data['metadata']['_count']

                _list = json_data["data"]["list"]

                for file in _list:
                    d: Dict[str, Union[int, str]] = {
                        "fid": file["fid"],
                        "file_name": file["file_name"],
                        "file_type": file["file_type"],
                        "dir": file["dir"],
                        "pdir_fid": file["pdir_fid"],
                        "include_items": file["include_items"] if "include_items" in file else '',
                        "share_fid_token": file["share_fid_token"],
                        "status": file["status"]
                    }
                    file_list.append(d)
                if _total <= _size or _count < _size:
                    return is_owner, file_list

                page += 1

    async def create_dir(self, pdir_name: str, pdir_fid: str = '0') -> Union[str, None]:
        """创建文件夹，返回文件夹ID。如果文件夹已存在，则返回已存在文件夹的ID"""
        params = {
            'pr': 'ucpro',
            'fr': 'pc',
            'uc_param_str': '',
            '__dt': random.randint(100, 9999),
            '__t': get_timestamp(13),
        }

        json_data = {
            'pdir_fid': pdir_fid,
            'file_name': pdir_name,
            'dir_path': '',
            'dir_init_lock': False,
        }

        async with httpx.AsyncClient() as client:
            timeout = httpx.Timeout(60.0, connect=60.0)
            response = await client.post('https://drive-pc.quark.cn/1/clouddrive/file', params=params,
                                         json=json_data, headers=self.headers, timeout=timeout)
            json_data = response.json()
            if json_data["code"] == 0:
                return json_data["data"]["fid"]
            elif json_data["code"] == 23008:
                folder_id = await self.find_folder_by_name(pdir_name, pdir_fid)
                return folder_id
            else:
                return None

    async def get_share_save_task_id(self, pwd_id: str, stoken: str, first_ids: List[str],
                                     share_fid_tokens: List[str], to_pdir_fid: str = '0') -> str:
        """获取转存任务ID"""
        task_url = "https://drive.quark.cn/1/clouddrive/share/sharepage/save"
        params = {
            "pr": "ucpro",
            "fr": "pc",
            "uc_param_str": "",
            "__dt": random.randint(600, 9999),
            "__t": get_timestamp(13),
        }
        data = {
            "fid_list": first_ids,
            "fid_token_list": share_fid_tokens,
            "to_pdir_fid": to_pdir_fid,
            "pwd_id": pwd_id,
            "stoken": stoken,
            "pdir_fid": "0",
            "scene": "link"
        }

        async with httpx.AsyncClient() as client:
            timeout = httpx.Timeout(60.0, connect=60.0)
            response = await client.post(task_url, json=data, headers=self.headers, params=params, timeout=timeout)
            json_data = response.json()
            if json_data.get('code') == 0 and json_data.get('data'):
                return json_data['data']['task_id']
            else:
                raise Exception(f"获取转存任务ID失败：{json_data.get('message', '未知错误')}")

    async def submit_task(self, task_id: str, retry: int = 50) -> Dict[str, Any]:
        """提交转存任务并等待完成"""
        for i in range(retry):
            await asyncio.sleep(random.randint(500, 1000) / 1000)
            submit_url = (f"https://drive-pc.quark.cn/1/clouddrive/task?pr=ucpro&fr=pc&uc_param_str=&task_id={task_id}"
                          f"&retry_index={i}&__dt=21192&__t={get_timestamp(13)}")

            async with httpx.AsyncClient() as client:
                timeout = httpx.Timeout(60.0, connect=60.0)
                response = await client.get(submit_url, headers=self.headers, timeout=timeout)
                json_data = response.json()

            if json_data['message'] == 'ok':
                if json_data['data']['status'] == 2:
                    return json_data
            else:
                if json_data['code'] == 32003 and 'capacity limit' in json_data['message']:
                    raise Exception("转存失败，网盘容量不足！")
                elif json_data['code'] == 41013:
                    raise Exception("网盘文件夹不存在！")

        raise Exception("转存任务超时")

    async def get_sorted_file_list(self, pdir_fid='0', page='1', size='100', fetch_total='false',
                                   sort='') -> Dict[str, Any]:
        """获取文件列表"""
        params = {
            'pr': 'ucpro',
            'fr': 'pc',
            'uc_param_str': '',
            'pdir_fid': pdir_fid,
            '_page': page,
            '_size': size,
            '_fetch_total': fetch_total,
            '_fetch_sub_dirs': '1',
            '_sort': sort,
            '__dt': random.randint(100, 9999),
            '__t': get_timestamp(13),
        }

        async with httpx.AsyncClient() as client:
            timeout = httpx.Timeout(60.0, connect=60.0)
            response = await client.get('https://drive-pc.quark.cn/1/clouddrive/file/sort', params=params,
                                        headers=self.headers, timeout=timeout)
            json_data = response.json()
            return json_data

    async def find_folder_by_name(self, folder_name: str, parent_fid: str = '0') -> Union[str, None]:
        """根据文件夹名称查找文件夹ID"""
        page = 1
        while True:
            file_list_data = await self.get_sorted_file_list(pdir_fid=parent_fid, page=str(page),
                                                             size='50', fetch_total='true',
                                                             sort='file_type:asc,file_name:asc')
            if not file_list_data.get('data') or not file_list_data['data'].get('list'):
                break

            for item in file_list_data['data']['list']:
                if item.get('dir') and item.get('file_name') == folder_name:
                    return item['fid']

            _total = file_list_data['metadata']['_total']
            _size = file_list_data['metadata']['_size']
            _page = file_list_data['metadata']['_page']

            if _size * _page >= _total:
                break
            page += 1

        return None

    async def get_share_task_id(self, fid: str, file_name: str, url_type: int = 1,
                                expired_type: int = 2, password: str = '') -> str:
        """获取分享任务ID"""
        json_data = {
            "fid_list": [fid],
            "title": file_name,
            "url_type": url_type,
            "expired_type": expired_type
        }
        if url_type == 2:
            if password:
                json_data["passcode"] = password
            else:
                json_data["passcode"] = generate_random_code()

        params = {
            'pr': 'ucpro',
            'fr': 'pc',
            'uc_param_str': '',
        }

        async with httpx.AsyncClient() as client:
            timeout = httpx.Timeout(60.0, connect=60.0)
            response = await client.post('https://drive-pc.quark.cn/1/clouddrive/share', params=params,
                                         json=json_data, headers=self.headers, timeout=timeout)
            json_data = response.json()
            if json_data.get('code') == 0 and json_data.get('data'):
                return json_data['data']['task_id']
            else:
                raise Exception(f"获取分享任务ID失败：{json_data.get('message', '未知错误')}")

    async def get_share_id(self, task_id: str) -> str:
        """获取分享ID"""
        params = {
            'pr': 'ucpro',
            'fr': 'pc',
            'uc_param_str': '',
            'task_id': task_id,
            'retry_index': '0',
        }
        async with httpx.AsyncClient() as client:
            timeout = httpx.Timeout(60.0, connect=60.0)
            response = await client.get('https://drive-pc.quark.cn/1/clouddrive/task', params=params,
                                        headers=self.headers, timeout=timeout)
            json_data = response.json()
            if json_data.get('message') == 'ok' and json_data.get('data'):
                return json_data['data']['share_id']
            else:
                raise Exception(f"获取分享ID失败：{json_data.get('message', '未知错误')}")

    async def submit_share(self, share_id: str) -> Tuple[str, str]:
        """提交分享并获取分享链接"""
        params = {
            'pr': 'ucpro',
            'fr': 'pc',
            'uc_param_str': '',
        }

        json_data = {
            'share_id': share_id,
        }
        async with httpx.AsyncClient() as client:
            timeout = httpx.Timeout(60.0, connect=60.0)
            response = await client.post('https://drive-pc.quark.cn/1/clouddrive/share/password', params=params,
                                         json=json_data, headers=self.headers, timeout=timeout)
            json_data = response.json()
            if json_data.get('code') == 0 and json_data.get('data'):
                share_url = json_data['data']['share_url']
                title = json_data['data']['title']
                if 'passcode' in json_data['data']:
                    share_url = share_url + f"?pwd={json_data['data']['passcode']}"
                return share_url, title
            else:
                raise Exception(f"获取分享链接失败：{json_data.get('message', '未知错误')}")

    async def list_all_items_in_folder(self, folder_id: str) -> List[Dict[str, Any]]:
        """获取指定文件夹内的所有条目（文件和文件夹）"""
        all_items = []
        current_page = 1
        items_per_page = 50

        async with httpx.AsyncClient() as client:
            while True:
                params = {
                    'pr': 'ucpro',
                    'fr': 'pc',
                    'uc_param_str': '',
                    'pdir_fid': folder_id,
                    '_page': str(current_page),
                    '_size': str(items_per_page),
                    '_fetch_total': '1',
                    '_fetch_sub_dirs': '0',
                    '_sort': 'created_at:asc',
                    '__dt': random.randint(100, 9999),
                    '__t': get_timestamp(13),
                }

                timeout = httpx.Timeout(60.0, connect=60.0)
                response = await client.get('https://drive-pc.quark.cn/1/clouddrive/file/sort',
                                           params=params, headers=self.headers, timeout=timeout)
                json_data = response.json()

                if json_data.get('code') == 0 and json_data.get('status') == 200:
                    data_node = json_data.get('data', {})
                    if data_node is None:
                        break

                    data_list = data_node.get('list', [])
                    metadata = json_data.get('metadata', {})
                    current_page_item_count = metadata.get('_count', len(data_list))
                    total_items = metadata.get('_total')

                    if not data_list and current_page_item_count == 0:
                        break

                    for item in data_list:
                        item_type = "文件夹" if item.get('dir') is True else "文件"
                        created_at_ms = item.get('created_at')
                        timestamp_to_use_ms = created_at_ms or item.get('l_created_at') or item.get('operated_at')

                        if timestamp_to_use_ms is None:
                            itime_s = item.get('itime')
                            if itime_s is not None:
                                try:
                                    timestamp_to_use_ms = int(itime_s) * 1000
                                except ValueError:
                                    continue
                            else:
                                continue

                        item_info = {
                            "fid": item.get('fid'),
                            "file_name": item.get('file_name'),
                            "itime_ms": timestamp_to_use_ms,
                            "type": item_type,
                        }

                        if all(value is not None for key, value in item_info.items() if key != 'type'):
                            all_items.append(item_info)

                    if total_items is not None:
                        if current_page * items_per_page >= total_items:
                            break
                    elif current_page_item_count < items_per_page:
                        break

                    current_page += 1
                    await asyncio.sleep(0.5)
                else:
                    break

        return all_items

    async def delete_items(self, item_fids: List[str]) -> bool:
        """删除指定的文件或文件夹"""
        if not item_fids:
            return True

        params = {
            'pr': 'ucpro',
            'fr': 'pc',
            'uc_param_str': '',
            '__dt': random.randint(100, 9999),
            '__t': get_timestamp(13),
        }

        json_data = {
            "action_type": 2,
            "filelist": item_fids,
            "exclude_fids": []
        }

        async with httpx.AsyncClient() as client:
            timeout = httpx.Timeout(60.0, connect=60.0)
            response = await client.post('https://drive-pc.quark.cn/1/clouddrive/file/delete',
                                        params=params, json=json_data, headers=self.headers, timeout=timeout)
            json_data = response.json()
            if json_data.get('code') == 0 and json_data.get('status') == 200:
                return True
            else:
                return False

    async def clean_expired_items(self, folder_id: str, expire_seconds: int) -> Dict[str, Any]:
        """清理过期的文件和文件夹"""
        all_items = await self.list_all_items_in_folder(folder_id)

        if not all_items:
            return {"success": True, "deleted_count": 0, "message": "文件夹为空或获取列表失败"}

        items_to_delete_fids = []
        items_to_delete_details = []
        current_timestamp_seconds = int(time.time())

        for item_obj in all_items:
            item_fid = item_obj.get('fid')
            item_name = item_obj.get('file_name')
            item_timestamp_ms = item_obj.get('itime_ms')
            item_type = item_obj.get('type', '未知')

            if not (item_fid and item_name and item_timestamp_ms is not None):
                continue

            try:
                item_creation_timestamp_ms = int(item_timestamp_ms)
                item_creation_timestamp_seconds = item_creation_timestamp_ms // 1000
            except ValueError:
                continue

            item_age_seconds = current_timestamp_seconds - item_creation_timestamp_seconds

            if item_age_seconds > expire_seconds:
                items_to_delete_fids.append(item_fid)
                age_hours = item_age_seconds // 3600
                age_minutes = (item_age_seconds % 3600) // 60
                items_to_delete_details.append(f"{item_name} ({item_type}, {age_hours}小时{age_minutes}分钟)")

        if items_to_delete_fids:
            delete_success = await self.delete_items(items_to_delete_fids)
            if delete_success:
                return {
                    "success": True,
                    "deleted_count": len(items_to_delete_fids),
                    "deleted_items": items_to_delete_details,
                    "message": f"成功清理 {len(items_to_delete_fids)} 个过期文件夹"
                }
            else:
                return {
                    "success": False,
                    "deleted_count": 0,
                    "message": "删除请求失败"
                }
        else:
            return {
                "success": True,
                "deleted_count": 0,
                "message": "未发现符合清理条件的项目"
            }

    async def auto_save_and_share(self, share_url: str, save_folder_name: str = None,
                                  url_type: int = 1, expired_type: int = 2,
                                  password: str = '') -> Tuple[str, str]:
        """
        自动转存并分享

        Args:
            share_url: 输入的分享链接
            save_folder_name: 保存文件夹名称（如果为None，则使用时间戳）
            url_type: 分享链接类型 1=公开 2=加密
            expired_type: 分享有效期 1=永久 2=1天 3=7天 4=30天
            password: 分享密码（如果url_type=2且password为空，则随机生成）

        Returns:
            (分享链接, 错误信息)，如果成功则错误信息为空字符串
        """
        match_password = re.search("pwd=(.*?)(?=$|&)", share_url)
        input_password = match_password.group(1) if match_password else ""
        pwd_id = self.get_pwd_id(share_url).split("#")[0]

        if not pwd_id:
            return '', '分享链接格式错误，无法提取pwd_id'

        stoken, error_msg = await self.get_stoken(pwd_id, input_password)
        if not stoken:
            return '', f'分享链接失效或已过期：{error_msg}'

        is_owner, data_list = await self.get_detail(pwd_id, stoken)

        if not data_list:
            return '', '分享链接中没有文件或文件夹'

        if is_owner == 1:
            return '', '该文件已经是您网盘中的文件，无需转存'

        if save_folder_name is None:
            save_folder_name = f"转存_{get_timestamp(10)}"

        save_folder_id = await self.create_dir(save_folder_name)
        if not save_folder_id:
            return '', '创建保存文件夹失败'

        fid_list = [i["fid"] for i in data_list]
        share_fid_token_list = [i["share_fid_token"] for i in data_list]

        try:
            task_id = await self.get_share_save_task_id(pwd_id, stoken, fid_list,
                                                         share_fid_token_list, save_folder_id)

            await self.submit_task(task_id)
        except Exception as e:
            return '', f'转存失败：{str(e)}'

        await asyncio.sleep(2)

        first_item = data_list[0]

        if len(data_list) == 1 and first_item['dir']:
            share_folder_name = first_item['file_name']
            target_folder_id = await self.find_folder_by_name(share_folder_name, save_folder_id)
            if not target_folder_id:
                await asyncio.sleep(2)
                target_folder_id = await self.find_folder_by_name(share_folder_name, save_folder_id)
            if not target_folder_id:
                return '', f'无法找到转存后的文件夹：{share_folder_name}'
        else:
            target_folder_id = save_folder_id
            share_folder_name = save_folder_name

        try:
            share_task_id = await self.get_share_task_id(target_folder_id, share_folder_name,
                                                         url_type=url_type, expired_type=expired_type,
                                                         password=password)

            await asyncio.sleep(1)
            share_id = await self.get_share_id(share_task_id)

            final_share_url, title = await self.submit_share(share_id)

            return final_share_url, ''
        except Exception as e:
            return '', f'分享失败：{str(e)}'


def search_resources(keyword: str, api_base_url: str) -> List[Dict]:
    """搜索资源

    Args:
        keyword: 搜索关键词
        api_base_url: API基础地址

    Returns:
        资源列表
    """
    try:
        url = f"{api_base_url.rstrip('/')}/api/search"
        data = {
            "kw": keyword,
            "cloud_types": ["quark"]
        }
        response = requests.post(url, json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0 and result.get('data'):
                merged = result['data'].get('merged_by_type', {})
                return merged.get('quark', [])
        return []
    except Exception as e:
        print(f"搜索失败: {str(e)}")
        return []


def retry_selection(resources: List[Dict], cookies: str, save_folder: str, share_option: str, keyword: str = ''):
    """重新让用户选择资源"""
    page = 1
    sender.reply(format_resource_list(resources, page))
    sender.reply(f'请输入【】中您需要的资源序号: (建议选最新的!)')

    while True:
        choice = sender.input(60000, 1, False)
        if not choice:
            break

        choice = choice.strip()

        if choice == '0':
            total_pages = (len(resources) + 9) // 10
            if page < total_pages:
                page += 1
                sender.reply(format_resource_list(resources, page))
                sender.reply(f'请输入【】中您需要的资源序号: (建议选最新的!)')
            else:
                sender.reply('已经是最后一页了')
            continue

        if choice == '00':
            if page > 1:
                page -= 1
                sender.reply(format_resource_list(resources, page))
                sender.reply(f'请输入【】中您需要的资源序号: (建议选最新的!)')
            else:
                sender.reply('已经是第一页了')
            continue

        try:
            idx = int(choice)
            if 1 <= idx <= len(resources):
                resource = resources[idx - 1]
                handle_resource(resource, cookies, save_folder, share_option, keyword, resources)
                break
            else:
                sender.reply(f'请输入1-{len(resources)}之间的数字')
        except ValueError:
            sender.reply('请输入有效的数字')


def format_resource_list(resources: List[Dict], page: int = 1, per_page: int = 10) -> str:
    """格式化资源列表

    Args:
        resources: 资源列表
        page: 页码（从1开始）
        per_page: 每页数量

    Returns:
        格式化后的字符串
    """
    if not resources:
        return "未找到相关资源"

    total = len(resources)
    start = (page - 1) * per_page
    end = min(start + per_page, total)
    page_resources = resources[start:end]
    total_pages = (total + per_page - 1) // per_page

    lines = []
    for idx, resource in enumerate(page_resources, start=start + 1):
        note = resource.get('note', '未知')
        if len(note) > 30:
            note = note[:30] + '...'
        dt = parse_datetime(resource.get('datetime', ''))
        lines.append(f"【{idx}】{note}")
        lines.append(f"资源时间:{dt}")
        lines.append("----------")

    result = "\n".join(lines)

    if total_pages > 1:
        result += f"\n【0】下一页(当前第{page}/{total_pages}页)"

    return result


def handle_search(keyword: str):
    """处理搜索请求"""
    cookies = sg.bucketGet('quark_search', 'cookies') or ''
    save_folder = sg.bucketGet('quark_search', 'save_folder') or ''
    share_option = sg.bucketGet('quark_search', 'share_option') or '1'
    search_api = sg.bucketGet('quark_search', 'search_api') or 'https://so.252035.xyz'

    if not cookies:
        sender.reply('配置错误：夸克网盘Cookie未设置')
        return

    if not search_api:
        sender.reply('配置错误：搜索API地址未设置')
        return

    sender.reply('正在为您检索中...')
    resources = search_resources(keyword, search_api)

    if not resources:
        sender.reply('未找到相关资源')
        return

    session_key = f'search_results_{userid}'
    sg.bucketSet('quark_search', session_key, json.dumps({
        'resources': resources,
        'keyword': keyword,
        'cookies': cookies,
        'save_folder': save_folder,
        'share_option': share_option
    }))

    page = 1
    sender.reply(format_resource_list(resources, page))

    sender.reply(f'请输入【】中您需要的资源序号: (建议选最新的!)')

    while True:
        choice = sender.input(60000, 1, False)
        if not choice:
            break

        choice = choice.strip()

        if choice == '0':
            total_pages = (len(resources) + 9) // 10
            if page < total_pages:
                page += 1
                sender.reply(format_resource_list(resources, page))
                sender.reply(f'请输入【】中您需要的资源序号: (建议选最新的!)')
            else:
                sender.reply('已经是最后一页了')
            continue

        if choice == '00':
            if page > 1:
                page -= 1
                sender.reply(format_resource_list(resources, page))
                sender.reply(f'请输入【】中您需要的资源序号: (建议选最新的!)')
            else:
                sender.reply('已经是第一页了')
            continue

        try:
            idx = int(choice)
            if 1 <= idx <= len(resources):
                resource = resources[idx - 1]
                handle_resource(resource, cookies, save_folder, share_option, keyword, resources)
                break
            else:
                sender.reply(f'请输入1-{len(resources)}之间的数字')
        except ValueError:
            sender.reply('请输入有效的数字')


def handle_resource(resource: Dict, cookies: str, save_folder: str, share_option: str, keyword: str = '', resources: List[Dict] = None):
    """处理资源转存和分享"""
    share_url = resource.get('url', '')
    password = resource.get('password', '')

    if password:
        share_url = f"{share_url}?pwd={password}"

    if not share_url:
        sender.reply('资源链接无效')
        if resources:
            retry_selection(resources, cookies, save_folder, share_option, keyword)
        return

    share_option = share_option or '1'
    if share_option in ['5', '6', '7', '8']:
        url_type = 2  # 加密
        expired_map = {'5': 1, '6': 2, '7': 3, '8': 4}
        expired_type = expired_map.get(share_option, 1)
        password = ''
    else:
        url_type = 1  # 公开
        expired_map = {'1': 1, '2': 2, '3': 3, '4': 4}
        expired_type = expired_map.get(share_option, 1)
        password = ''

    save_folder_name = save_folder if save_folder else None

    try:
        display_keyword = keyword if keyword else resource.get('note', '资源')
        sender.reply(f'正在为您加载:{display_keyword}')

        manager = QuarkAutoSaveAndShare(cookies=cookies)

        final_share_url, error_msg = asyncio.run(manager.auto_save_and_share(
            share_url=share_url,
            save_folder_name=save_folder_name,
            url_type=url_type,
            expired_type=expired_type,
            password=password
        ))

        if not final_share_url:
            sender.reply(f'❌ {error_msg}')
            if resources:
                sender.reply('请重新选择其他资源：')
                retry_selection(resources, cookies, save_folder, share_option, keyword)
            return

        qr_url = generate_qrcode(final_share_url)

        if qr_url:
            sender.replyImage(qr_url)

        sender.reply(f'请长摁扫码保存资源到夸克网盘观看 如果资源货不对版、空文件夹 请更换选项!')
        sender.reply('⚠️ 本服务仅提供搜索，不存储、不上传任何内容，所有资源均来自第三方网盘，请用户自行判断资源真实性和安全性，请勿轻信或点击广告，谨防受骗！')

    except Exception as e:
        sender.reply(f'❌ 处理失败：{str(e)}')
        if resources:
            sender.reply('请重新选择其他资源：')
            retry_selection(resources, cookies, save_folder, share_option, keyword)


def handle_clean():
    """处理清理请求"""
    cookies = sg.bucketGet('quark_search', 'cookies') or ''
    clean_folder_id = sg.bucketGet('quark_search', 'clean_folder_id') or ''
    clean_expire_minutes = sg.bucketGet('quark_search', 'clean_expire_minutes') or '60'

    if not cookies:
        sender.reply('配置错误：夸克网盘Cookie未设置')
        return

    if not clean_folder_id:
        sender.reply('配置错误：清理文件夹ID未设置')
        return

    try:
        expire_minutes = int(clean_expire_minutes)
        expire_seconds = expire_minutes * 60
    except ValueError:
        sender.reply('配置错误：清理过期时间格式无效')
        return

    try:
        sender.reply(f'正在清理文件夹，过期时间：{expire_minutes}分钟...')

        manager = QuarkAutoSaveAndShare(cookies=cookies)

        result = asyncio.run(manager.clean_expired_items(clean_folder_id, expire_seconds))

        if result['success']:
            if result['deleted_count'] > 0:
                result.get('deleted_items', [])
            else:
                sender.reply(f'清理完成！{result["message"]}')
        else:
            sender.reply(f'清理失败：{result["message"]}')

    except Exception as e:
        sender.reply(f'清理失败：{str(e)}')


def cookiejar_to_string(cookiejar):
    """将cookiejar转换为字符串"""
    cookie_string = ""
    for cookie in cookiejar:
        cookie_string += cookie.name + "=" + cookie.value + "; "
    return cookie_string.strip('; ')


def poll_qrcode_status(token: str, max_wait_seconds: int = 120) -> Union[str, None]:
    """轮询二维码扫码状态并获取cookie"""
    start_time = time.time()

    while True:
        if time.time() - start_time > max_wait_seconds:
            return None

        try:
            request_id = str(uuid.uuid4())
            url = f'https://uop.quark.cn/cas/ajax/getServiceTicketByQrcodeToken?client_id=532&v=1.2&token={token}&request_id={request_id}'
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                re_data = response.json()

                if re_data['status'] == 2000000:
                    service_ticket = re_data['data']['members']['service_ticket']
                    info_url = f'https://pan.quark.cn/account/info?st={service_ticket}&lw=scan'
                    info_response = requests.get(info_url, timeout=10)

                    if info_response.status_code == 200:
                        quark_cookie = cookiejar_to_string(info_response.cookies)
                        return quark_cookie
                    else:
                        return None

                elif re_data['status'] == 50004002:
                    return None

                elif re_data['status'] == 50004001:
                    time.sleep(2)
                    continue
                else:
                    time.sleep(2)
                    continue
            else:
                time.sleep(2)
                continue

        except Exception as e:
            time.sleep(2)
            continue

    return None


def handle_login():
    """处理登录请求"""
    try:
        request_id = str(uuid.uuid4())
        token_url = f'https://uop.quark.cn/cas/ajax/getTokenForQrcodeLogin?client_id=532&v=1.2&request_id={request_id}'
        response = requests.get(token_url, timeout=10)

        if response.status_code != 200:
            sender.reply('获取登录token失败，请稍后重试')
            return

        token_data = response.json()
        if token_data.get('status') != 2000000:
            sender.reply('获取登录token失败，请稍后重试')
            return

        token = token_data['data']['members']['token']

        qr_data = f'https://su.quark.cn/4_eMHBJ?token={token}&client_id=532&ssb=weblogin&uc_param_str=&uc_biz_str=S%3Acustom%7COPT%3ASAREA%400%7COPT%3AIMMERSIVE%401%7COPT%3ABACK_BTN_STYLE%400'
        qr_url = generate_qrcode(qr_data)

        if not qr_url:
            sender.reply('生成二维码失败，请稍后重试')
            return

        sender.replyImage(qr_url)
        sender.reply('请在3分钟内，使用【夸克APP】扫描二维码登录...')

        cookie = poll_qrcode_status(token, max_wait_seconds=180)

        if cookie:
            sg.bucketSet('quark_search', 'cookies', cookie)
            sender.reply('登录成功！Cookie已保存！')
        else:
            sender.reply('登录失败：二维码已过期或扫码超时，请重试！')

    except Exception as e:
        sender.reply(f'登录失败：{str(e)}')


message = sender.getMessage()

if message.strip() == '夸克清理':
    if sender.isAdmin():
        handle_clean()
    else:
        sender.reply('❌ 您没有权限执行此操作!')
elif message.strip() == '夸克登录':
    if sender.isAdmin():
        handle_login()
    else:
        sender.reply('❌ 您没有权限执行此操作!')
else:
    match = re.match(r'^我要看(.+)$', message)
    if match:
        keyword = match.group(1).strip()
        if keyword:
            handle_search(keyword)
        else:
            sender.reply('请输入要搜索的关键词')
    else:
        sender.reply('格式错误，请使用：我要看XXXX、夸克清理 或 夸克登录')
