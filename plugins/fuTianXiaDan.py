# [title: 福田下单]
# [name: fuTianXiaDan]
# [language: python]
# [class: 任务]
# [author: rujingxianghai]
# [version: v1.0]
# [public: true]
# [disable: false]
# [admin: false]
# [rule: ^福田下单$|^福田物流查询$]
# [icon: https://images.mingming.dev/file/7c1c97c112588fbf7c0db.png]
# [description: 呆呆出品；福田下单插件；指令：福田下单、福田物流查询；功能如下：；1. 支持单账号和多账号批量下单；2.支持在线搜索自定义商品并选择下单；3.支持在线添加自定义地址下单；4.支持查询订单物流信息；4.]
# [depe: ["requests", "urllib3"]]


import asyncio as _sg_asyncio, os as _sg_os, time as _sg_time, types as _sg_types, json as _sg_json, re as _sg_re, urllib.parse as _sg_urlparse
from threading import Thread as _sg_Thread
from sillygirl import Adapter as _SGAdapter, Bucket as _SGBucket, Sender as _SGSender, sender as _sg_sender, container as _sg_container
try:
    import ast as _sg_ast
except Exception:
    _sg_ast = None
try:
    import decimal as decimal
except Exception:
    decimal = None

def _sg_run(coro):
    try:
        _sg_asyncio.get_running_loop()
    except RuntimeError:
        return _sg_asyncio.run(coro)
    box={}
    def runner():
        try: box["v"]=_sg_asyncio.run(coro)
        except BaseException as e: box["e"]=e
    t=_sg_Thread(target=runner, daemon=True); t.start(); t.join()
    if "e" in box: raise box["e"]
    return box.get("v")

def _sg_literal(value, default=None):
    if isinstance(value,(list,dict,tuple,set,int,float,bool)) or value is None:
        return value if value is not None else ([] if default is None else default)
    text=str(value or "").strip()
    if not text: return [] if default is None else default
    for parser in (_sg_json.loads, (_sg_ast.literal_eval if _sg_ast else None)):
        if parser:
            try: return parser(text)
            except Exception: pass
    return [] if default is None else default

def _sg_sender_sync(uuid=""):
    s=_SGSender(uuid or _sg_os.environ.get("SENDER_ID", ""))
    def call(name,*a,**k): return _sg_run(getattr(s,name)(*a,**k))
    def listen(timeout=60000,*a,**k):
        try:
            r=call("listen", {"timeout": int(timeout or 0)})
            return _sg_run(r.getContent()) if r else ""
        except Exception: return ""
    return _sg_types.SimpleNamespace(
        getUserID=lambda:call("getUserId"), getUserId=lambda:call("getUserId"), getMessage=lambda:call("getContent"), getContent=lambda:call("getContent"),
        getUserName=lambda:call("getUserName"), getNickname=lambda:call("getUserName"), getChatID=lambda:call("getChatId"), getChatId=lambda:call("getChatId"),
        getImtype=lambda:call("getPlatform"), getPlatform=lambda:call("getPlatform"), getMessageID=lambda:call("getMessageId"), getPluginName=lambda:_sg_os.environ.get("PLUGIN_NAME",""), getPluginVersion=lambda:_sg_os.environ.get("PLUGIN_VERSION",""),
        isAdmin=lambda:bool(call("isAdmin")), reply=lambda msg="":call("reply", str(msg)), replyImage=lambda url="":call("reply", str(url) if str(url).startswith("[") else f"[CQ:image,file={url}]"),
        listen=listen, input=listen, waitInput=listen, setContinue=lambda *a,**k:call("continue_"), breakIn=lambda *a,**k:call("continue_"))

def _sg_bucket_get(bucket=None,key=None,default="",**kw):
    try:
        v=_SGBucket(str(kw.get("bucket",bucket) or ""))[str(kw.get("key",key) or "")]
        return default if v in (None,"") and default not in (None,"") else (v if v is not None else "")
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
    i=a[0] if a and isinstance(a[0],dict) else {}; platform=i.get("imType") or i.get("platform") or kw.get("platform") or (a[0] if a else ""); group=i.get("groupCode") or i.get("group_id") or kw.get("group_id") or (a[1] if len(a)>1 else ""); user=i.get("userID") or i.get("user_id") or kw.get("userID") or (a[2] if len(a)>2 else ""); title=i.get("title") or kw.get("title") or (a[3] if len(a)>3 else ""); content=i.get("content") or i.get("message") or kw.get("content") or (a[4] if len(a)>4 else title)
    return _sg_run(_SGAdapter(str(platform or "")).push({"group_id":str(group or ""),"user_id":str(user or ""),"title":str(title or ""),"content":str(content or "")}))
def _sg_notify(msg,channels=None,*a,**k): return _sg_run(_sg_sender.pushAdmin(str(msg), {"platforms":list(channels or [])} if channels else {}))
class _SGFacade:
    Sender=staticmethod(_sg_sender_sync); getSenderID=staticmethod(lambda:_sg_os.environ.get("SENDER_ID","")); getPluginName=staticmethod(lambda:_sg_os.environ.get("PLUGIN_NAME","")); bucketGet=staticmethod(_sg_bucket_get); bucketSet=staticmethod(_sg_bucket_set); bucketDel=staticmethod(_sg_bucket_del); bucketDelete=staticmethod(_sg_bucket_del); bucketAllKeys=staticmethod(_sg_bucket_keys); bucketKeys=staticmethod(_sg_bucket_keys); bucketAll=staticmethod(_sg_bucket_all); notifyMasters=staticmethod(_sg_notify); pushAdmin=staticmethod(_sg_notify); push=staticmethod(_sg_push); Push=staticmethod(_sg_push); reply=staticmethod(lambda msg="":_sg_sender_sync().reply(msg)); get=staticmethod(lambda key,default="":_sg_bucket_get(*(str(key).split(".",1) if "." in str(key) else ["otto",key]), default=default)); getParam=get; version=staticmethod(lambda:{"sn":_sg_os.environ.get("SILLYGIRL_VERSION","3.0.0"),"version":_sg_os.environ.get("SILLYGIRL_VERSION","3.0.0")}); port=staticmethod(lambda:_sg_os.environ.get("SILLYGIRL_PORT","8080")); sleep=staticmethod(lambda sec:_sg_time.sleep(float(sec or 0)))
sg=_SGFacade(); Sender=sg.Sender; getSenderID=sg.getSenderID; bucketGet=sg.bucketGet; bucketSet=sg.bucketSet; bucketAllKeys=sg.bucketAllKeys; notifyMasters=sg.notifyMasters

def mask_account(value):
    value=str(value or ""); return value if len(value)<=7 else value[:3]+"***"+value[-4:]
def generate_qrcode_url(text): return "https://api.qrserver.com/v1/create-qr-code/?size=260x260&data="+_sg_urlparse.quote(str(text or ""))
def get_pay_config(): return {}
class MaPayClient:
    def create_order(self,*a,**k): return {"error":"","status":True,"data":None}
    def is_paid(self,*a,**k): return True
def calculate_auth_time(*a,**k): return "2099-12-31"
def check_auth_status(*a,**k): return "账号默认可用"
_check_auth_status=check_auth_status
def select_accounts(sender,user_bucket,user_id,*a,**k):
    raw=sg.bucketGet(user_bucket,user_id,[]); raw=_sg_literal(raw,[]) if isinstance(raw,str) else raw
    if isinstance(raw,dict): raw=list(raw.keys()) or list(raw.values())
    return (raw if isinstance(raw,list) else []), (raw if isinstance(raw,list) else [])
def process_authorization(*a,**k): return True
def process_coin_payment(*a,**k): return True
def admin_auth_all_accounts(*a,**k): return True
def admin_auth_by_user(*a,**k): return True
def get_user_points(user_id=None,bucket="dd_sign_points"):
    try: return int(sg.bucketGet(bucket,user_id or sg.getSenderID()) or 0)
    except Exception: return 0
def update_user_points(user_id=None,points=0,bucket="dd_sign_points"): return sg.bucketSet(bucket,user_id or sg.getSenderID(),str(points))
def _sg_panel_id(config=None):
    if isinstance(config,dict): config=config.get("id") or config.get("ID") or config.get("index") or config.get("name")
    m=_sg_re.search(r"\d+", str(config or "")); return int(m.group(0)) if m else 1
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

config = None
_CONFIG_FIELD_MAP = {}

import requests
import json
import urllib3
import urllib.parse
from typing import Dict, Any, List, Optional

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

senderID = sg.getSenderID()
sender = sg.Sender(senderID)
userid = sender.getUserID()
usermessage = sender.getMessage()


class FutianOrderBot:

    def __init__(self):
        self.session = requests.Session()
        self.base_url = "http://wap.365autogo.com/mobile/api"

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 11; V1986A Build/RP1A.200720.012; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'language': 'zh-CN',
            'cityId': '622',
            'osVersion': '11',
            'unique': 'android-19dcfd0b281e9a03',
            'channel': 'channel_1',
            'os': 'android',
            'appkey': 'ef1fc57c13007e33',
            'appVersion': '4.9.0',
            'X-Requested-With': 'com.foton.suichexing.mobile',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        self.session.headers.update(self.headers)
        self.session.timeout = 30
        self.user_session = None
        self.user_id = None
        self.shipping_address = {}
        self.phone = None  # 添加手机号属性

    def login(self, phone: str, password: str) -> bool:
        """登录账号"""
        self.phone = phone  # 保存手机号
        login_url = f"{self.base_url}/user/login"

        login_param = {
            "loginName": phone,
            "password": password
        }

        data = {'param': json.dumps(login_param, separators=(',', ':'))}

        try:
            response = self.session.post(login_url, data=data, verify=False)
            response.raise_for_status()
            result = response.json()

            if result.get("stateCode") == 0:
                data = result.get("data", {})
                self.user_session = data.get('userSession')
                self.user_id = data.get('id')
                self.session.headers.update({
                    'userId': str(self.user_id),
                    'userSession': self.user_session
                })
                return True
            else:
                sender.reply(f"❌ 账号 {phone} 登录失败: {result.get('message', '未知错误')}")
                return False
        except Exception as e:
            sender.reply(f"❌ 账号 {phone} 登录异常: {str(e)}")
            return False

    def search_products(self, search_word: str, page: int = 1, page_count: int = 15) -> Dict[str, Any]:
        """搜索商品"""
        search_url = f"{self.base_url}/product/search"

        search_param = {
            "searchWord": search_word,
            "sort": 0,
            "page": page,
            "pageCount": page_count
        }
        param_json = json.dumps(search_param, separators=(',', ':'), ensure_ascii=False)
        param_encoded = urllib.parse.quote(param_json, safe='')
        full_url = f"{search_url}?param={param_encoded}"

        try:
            response = self.session.get(full_url, verify=False)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e), "stateCode": -1}

    def display_search_results(self, search_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """显示搜索结果"""
        if search_result.get("stateCode") != 0:
            sender.reply(f"❌ 搜索失败: {search_result.get('message', '未知错误')}")
            return []

        data = search_result.get("data", {})
        items = data.get("items", [])
        total = data.get("total", 0)

        if not items:
            sender.reply("❌ 没有找到相关商品")
            return []

        result_text = f"🔍 搜索结果 (共 {total} 个商品):\n" + "-" * 40 + "\n"

        for i, item in enumerate(items, 1):
            goods = item.get("goods", {})
            name = item.get("name", "未知商品")
            point_price = goods.get("point", 0)
            cash_price = goods.get("price", "0.00")
            stock = goods.get("availableStock", 0)
            sellable = item.get("sellable", False)

            status = "✅ 可使用" if sellable and stock > 0 else "❌ 不可使用"

            result_text += f"{i:2d}. {name}\n"
            result_text += f"    💰 积分: {point_price} | 现金: ¥{cash_price}\n"
            result_text += f"    📦 库存: {stock} | {status}\n"
            result_text += "-" * 40 + "\n"

        sender.reply(result_text)
        return items

    def clear_and_add_to_cart(self, goods_id: int, quantity: int = 1) -> bool:
        """清空购物车并添加商品"""
        cart_url = f"{self.base_url}/cart/show"
        try:
            response = self.session.get(cart_url, verify=False)
            cart_result = response.json()

            if cart_result.get("stateCode") == 0:
                baskets = cart_result.get("data", {}).get("baskets", [])
                if baskets:
                    self._clear_cart(baskets)

            return self._add_to_cart(goods_id, quantity)
        except Exception as e:
            sender.reply(f"❌ 购物车操作失败: {str(e)}")
            return False

    def _clear_cart(self, baskets: list):
        """清空购物车"""
        clear_url = f"{self.base_url}/cart/removeGoods"
        remove_items = []

        for basket in baskets:
            basket_id = basket.get('id')
            items = basket.get('items', [])
            for item in items:
                item_id = item.get('id')
                remove_items.append({"basketItemId": item_id, "basketId": basket_id})

        if remove_items:
            param_data = json.dumps(remove_items, separators=(',', ':'))
            data = {'param': param_data}
            try:
                self.session.post(clear_url, data=data, verify=False)
            except:
                pass

    def _add_to_cart(self, goods_id: int, quantity: int) -> bool:
        """添加商品到购物车"""
        add_url = f"{self.base_url}/cart/addGoods"
        add_items = [{"goodsId": goods_id, "number": quantity, "type": 1}]

        param_data = json.dumps(add_items, separators=(',', ':'))
        data = {'param': param_data}

        try:
            response = self.session.post(add_url, data=data, verify=False)
            result = response.json()
            return result.get("stateCode") == 0
        except:
            return False

    def clear_user_addresses(self):
        """清空用户所有收货地址"""
        try:
            address_list_url = f"{self.base_url}/user/consignees"
            response = self.session.get(address_list_url, verify=False)
            result = response.json()

            if result.get("stateCode") == 0:
                addresses = result.get("data", [])
                if addresses:
                    for address in addresses:
                        address_id = address.get("id")
                        if address_id:
                            self.delete_shipping_address(address_id)
                    sender.reply(f"✅ 已清空 {len(addresses)} 个收货地址")
                else:
                    sender.reply("ℹ️  暂无收货地址需要清空")
            else:
                sender.reply("❌ 获取地址列表失败")
        except Exception as e:
            sender.reply(f"❌ 清空地址异常: {str(e)}")

    def clear_shopping_cart(self):
        """清空购物车"""
        try:
            cart_url = f"{self.base_url}/cart/show"
            response = self.session.get(cart_url, verify=False)
            cart_result = response.json()

            if cart_result.get("stateCode") == 0:
                baskets = cart_result.get("data", {}).get("baskets", [])
                if baskets:
                    self._clear_cart(baskets)
                    sender.reply("✅ 购物车已清空")
                else:
                    sender.reply("ℹ️  购物车本来就是空的")
            else:
                sender.reply("❌ 获取购物车失败")
        except Exception as e:
            sender.reply(f"❌ 清空购物车异常: {str(e)}")

    def get_region_list(self, parent_id: int = 0) -> List[Dict[str, Any]]:
        """获取地区列表"""
        region_url = f"{self.base_url}/region/findChild"
        region_param = {"id": parent_id}
        region_param_json = json.dumps(region_param, separators=(',', ':'))
        region_param_encoded = urllib.parse.quote(region_param_json, safe='')
        region_full_url = f"{region_url}?param={region_param_encoded}"

        try:
            response = self.session.get(region_full_url, verify=False)
            region_result = response.json()

            if region_result.get("stateCode") == 0:
                return region_result.get("data", [])
            else:
                sender.reply(f"❌ 获取地区列表失败: {region_result.get('message', '未知错误')}")
                return []
        except Exception as e:
            sender.reply(f"❌ 获取地区列表异常: {str(e)}")
            return []

    def interactive_region_selection(self) -> Optional[int]:
        """交互式选择地区"""

        sender.reply("🌏 请选择省份/直辖市:")
        provinces = self.get_region_list(0)
        if not provinces:
            sender.reply("❌ 获取省份列表失败")
            return None

        province_text = "-" * 25 + "\n"
        for i, province in enumerate(provinces, 1):
            province_text += f"{i:2d}. {province.get('name')}\n"
        province_text += "-" * 25
        sender.reply(province_text)

        province_choice = sender.input(60000, 1, False)
        if not province_choice:
            sender.reply("⏰ 输入超时")
            return None

        try:
            choice_num = int(province_choice)
            if 1 <= choice_num <= len(provinces):
                selected_province = provinces[choice_num - 1]
            else:
                sender.reply(f"❌ 请输入 1-{len(provinces)} 之间的数字")
                return None
        except ValueError:
            sender.reply("❌ 请输入有效的数字")
            return None

        sender.reply(f"✅ 已选择: {selected_province.get('name')}")

        sender.reply("🏙️ 请选择城市/地区:")
        cities = self.get_region_list(selected_province.get('id'))
        if not cities:
            sender.reply("❌ 获取城市列表失败")
            return None

        city_text = "-" * 25 + "\n"
        for i, city in enumerate(cities, 1):
            city_text += f"{i:2d}. {city.get('name')}\n"
        city_text += "-" * 25
        sender.reply(city_text)

        city_choice = sender.input(60000, 1, False)
        if not city_choice:
            sender.reply("⏰ 输入超时")
            return None

        try:
            choice_num = int(city_choice)
            if 1 <= choice_num <= len(cities):
                selected_city = cities[choice_num - 1]
            else:
                sender.reply(f"❌ 请输入 1-{len(cities)} 之间的数字")
                return None
        except ValueError:
            sender.reply("❌ 请输入有效的数字")
            return None

        sender.reply(f"✅ 已选择: {selected_city.get('name')}")

        districts = self.get_region_list(selected_city.get('id'))
        if not districts:
            sender.reply("ℹ️  该城市无下级区域")
            return selected_city.get('id')

        sender.reply("🏘️ 请选择区/县:")
        district_text = "-" * 25 + "\n"
        for i, district in enumerate(districts, 1):
            district_text += f"{i:2d}. {district.get('name')}\n"
        district_text += "-" * 25
        sender.reply(district_text)

        district_choice = sender.input(60000, 1, False)
        if not district_choice:
            sender.reply("⏰ 输入超时")
            return None

        try:
            choice_num = int(district_choice)
            if 1 <= choice_num <= len(districts):
                selected_district = districts[choice_num - 1]
            else:
                sender.reply(f"❌ 请输入 1-{len(districts)} 之间的数字")
                return None
        except ValueError:
            sender.reply("❌ 请输入有效的数字")
            return None

        sender.reply(f"✅ 已选择: {selected_district.get('name')}")

        subdistricts = self.get_region_list(selected_district.get('id'))
        if subdistricts:
            sender.reply("🏢 请选择街道/乡镇:")
            subdistrict_text = "-" * 25 + "\n"
            for i, subdistrict in enumerate(subdistricts, 1):
                subdistrict_text += f"{i:2d}. {subdistrict.get('name')}\n"
            subdistrict_text += "-" * 25
            sender.reply(subdistrict_text)

            subdistrict_choice = sender.input(60000, 1, False)
            if not subdistrict_choice:
                sender.reply("⏰ 输入超时")
                return None

            try:
                choice_num = int(subdistrict_choice)
                if 1 <= choice_num <= len(subdistricts):
                    selected_subdistrict = subdistricts[choice_num - 1]
                else:
                    sender.reply(f"❌ 请输入 1-{len(subdistricts)} 之间的数字")
                    return None
            except ValueError:
                sender.reply("❌ 请输入有效的数字")
                return None

            sender.reply(f"✅ 已选择: {selected_subdistrict.get('name')}")
            return selected_subdistrict.get('id')
        else:
            return selected_district.get('id')

    def get_cart_token(self) -> Optional[str]:
        """获取购物车令牌"""
        cart_show_url = f"{self.base_url}/asyncCheckout/show"

        try:
            response = self.session.get(cart_show_url, verify=False)
            response.raise_for_status()
            result = response.json()

            if result.get("stateCode") == 0:
                return result.get("data", {}).get("cartToken")
            else:
                sender.reply(f"❌ 获取购物车令牌失败: {result.get('message', '未知错误')}")
                return None
        except Exception as e:
            sender.reply(f"❌ 获取购物车令牌异常: {str(e)}")
            return None

    def create_shipping_address(self) -> int:
        """创建收货地址"""
        address_url = f"{self.base_url}/user/addConsignees"

        region_id = self.shipping_address.get("region_id", 1355)

        address_param = {
            "alias": self.shipping_address.get("alias", self.shipping_address.get("name", "默认地址")),
            "address": self.shipping_address.get("address", ""),
            "mobile": self.shipping_address["mobile"],
            "name": self.shipping_address["name"],
            "defaulted": False,
            "regionId": region_id,
            "type": 0
        }

        param_data = json.dumps(address_param, separators=(',', ':'), ensure_ascii=False)
        data = {'param': param_data}
        headers = self.session.headers.copy()
        headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'

        try:
            response = self.session.post(address_url, data=data, headers=headers, verify=False)
            result = response.json()
            if result.get("stateCode") == 0:
                return result.get("data", {}).get("id")
        except:
            pass
        return None

    def get_image_verify_code(self) -> Dict[str, Any]:
        """获取图形验证码"""
        verify_url = f"{self.base_url}/global/createImageVerifyCode"
        param = {"type": "VERIFYCODE_IMAGE_USEPOINT"}
        param_json = json.dumps(param, separators=(',', ':'))
        param_encoded = urllib.parse.quote(param_json, safe='')
        full_url = f"{verify_url}?param={param_encoded}"

        try:
            response = self.session.get(full_url, verify=False)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e), "stateCode": -1}

    def send_sms_verify_code(self, img_verify_code: str) -> Dict[str, Any]:
        """发送短信验证码"""
        sms_url = f"{self.base_url}/asyncCheckout/sendLoginNameSMS"
        param = {
            "loginName": self.phone,
            "imgVerifyCode": img_verify_code
        }
        data = {'param': json.dumps(param, separators=(',', ':'))}

        try:
            response = self.session.post(sms_url, data=data, verify=False)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e), "stateCode": -1}

    def verify_sms_code(self, sms_code: str) -> Dict[str, Any]:
        """验证短信验证码"""
        verify_url = f"{self.base_url}/asyncCheckout/checkPoint"
        param = {
            "loginName": self.phone,
            "verifyCode": sms_code
        }
        param_json = json.dumps(param, separators=(',', ':'))
        param_encoded = urllib.parse.quote(param_json, safe='')
        full_url = f"{verify_url}?param={param_encoded}"

        try:
            response = self.session.get(full_url, verify=False)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e), "stateCode": -1}

    def update_cart_data(self, address_id: int, point_payment: int) -> Dict[str, Any]:
        """更新购物车数据"""
        update_url = f"{self.base_url}/asyncCheckout/update"

        cart_token = self.get_cart_token()
        if not cart_token:
            return {"error": "获取购物车令牌失败", "stateCode": -1}

        region_id = self.shipping_address.get("region_id", 1355)

        update_param = {
            "consigneeId": address_id,
            "coupons": [{"basketId": 1, "couponIds": []}],
            "deliveryModeId": -1,
            "paymentModeType": 2,
            "remarks": [],
            "payableAmount": "0.00",
            "invoice": {"status": 0, "type": 0},
            "cartToken": cart_token,
            "pointPayment": point_payment,
            "balance": "",
            "enterpriseCode": "",
            "loginName": "",
            "regionId": region_id
        }

        param_data = json.dumps(update_param, separators=(',', ':'), ensure_ascii=False)
        data = {'param': param_data}
        headers = self.session.headers.copy()
        headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'

        try:
            response = self.session.post(update_url, data=data, headers=headers, verify=False)
            return response.json()
        except Exception as e:
            return {"error": str(e), "stateCode": -1}

    def verify_point_payment(self, point_payment: int) -> bool:
        """验证积分支付"""
        if point_payment <= 4000:
            return True

        verify_result = self.get_image_verify_code()
        if verify_result.get("stateCode") != 0:
            sender.reply("❌ 获取图形验证码失败")
            return False

        image_data = verify_result.get('data', {}).get('base64')
        if not image_data:
            sender.reply("❌ 获取验证码图片失败")
            return False

        try:
            convert_url = "https://uapis.cn/api/baseimg.php"
            response = requests.post(convert_url, data={"imageData": image_data})
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 200:
                    image_url = result.get("img")
                    if image_url:
                        sender.replyImage(image_url)
                    else:
                        sender.reply("❌ 图片转换失败")
                        return False
                else:
                    sender.reply("❌ 图片转换失败")
                    return False
            else:
                sender.reply("❌ 图片转换服务异常")
                return False
        except Exception as e:
            sender.reply(f"❌ 图片转换异常: {str(e)}")
            return False

        sender.reply("请输入图形验证码：")
        img_code = sender.input(60000, 1, False)
        if not img_code:
            sender.reply("⏰ 输入超时")
            return False

        sms_result = self.send_sms_verify_code(img_code)
        if sms_result.get("stateCode") != 0:
            sender.reply("❌ 发送短信验证码失败")
            return False

        sender.reply("✅ 短信验证码已发送，请输入：")
        sms_code = sender.input(60000, 1, False)
        if not sms_code:
            sender.reply("⏰ 输入超时")
            return False

        verify_result = self.verify_sms_code(sms_code)
        if verify_result.get("stateCode") != 0:
            sender.reply("❌ 短信验证码验证失败")
            return False

        update_result = self.update_cart_data(self.shipping_address.get("id"), point_payment)
        if update_result.get("stateCode") != 0:
            sender.reply("❌ 更新购物车数据失败")
            return False

        sender.reply("✅ 积分验证成功")
        return True

    def create_order(self, address_id: int, point_payment: int) -> Dict[str, Any]:
        """创建订单"""
        if not self.verify_point_payment(point_payment):
            return {"error": "积分验证失败", "stateCode": -1}

        cart_token = self.get_cart_token()
        if not cart_token:
            return {"error": "获取购物车令牌失败", "stateCode": -1}

        create_order_url = f"{self.base_url}/asyncCheckout/createOrder"

        region_id = self.shipping_address.get("region_id", 1355)

        order_param = {
            "consigneeId": address_id,
            "coupons": [{"basketId": 1, "couponIds": []}],
            "deliveryModeId": 290000003,
            "paymentModeType": 2,
            "remarks": [],
            "payableAmount": "0.00",
            "invoice": {"status": 0, "type": 0},
            "cartToken": cart_token,
            "pointPayment": point_payment,
            "balance": "",
            "enterpriseCode": "",
            "loginName": "",
            "regionId": region_id,
            "isPresell": False
        }

        param_data = json.dumps(order_param, separators=(',', ':'), ensure_ascii=False)
        data = {'param': param_data}
        headers = self.session.headers.copy()
        headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'

        try:
            response = self.session.post(create_order_url, data=data, headers=headers, verify=False)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def delete_shipping_address(self, address_id: int):
        """删除收货地址"""
        delete_url = f"{self.base_url}/user/consignees/del"
        delete_param = {"id": address_id}

        param_data = json.dumps(delete_param, separators=(',', ':'))
        data = {'param': param_data}
        headers = self.session.headers.copy()
        headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'

        try:
            self.session.post(delete_url, data=data, headers=headers, verify=False)
        except:
            pass

    def get_order_list(self, status: str = "0", page: int = 1, page_count: int = 15) -> Dict[str, Any]:
        """获取订单列表"""
        order_url = f"{self.base_url}/order/list"

        order_param = {
            "status": status,  # "0"表示全部订单
            "page": page,
            "pageCount": page_count,
            "startOrderCreateTime": "",
            "endOrderCreateTime": "",
            "mix": ""
        }

        param_json = json.dumps(order_param, separators=(',', ':'), ensure_ascii=False)
        param_encoded = urllib.parse.quote(param_json, safe='')
        full_url = f"{order_url}?param={param_encoded}"

        try:
            response = self.session.get(full_url, verify=False)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e), "stateCode": -1}

    def display_order_list(self, order_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """显示订单列表并返回订单数据"""
        if order_result.get("stateCode") != 0:
            sender.reply(f"❌ 获取订单列表失败: {order_result.get('message', '未知错误')}")
            return []

        data = order_result.get("data", {})
        items = data.get("items", [])
        total = data.get("total", 0)

        if not items:
            sender.reply("❌ 暂无订单记录")
            return []

        result_text = f"📋 订单列表 (共 {total} 个订单):\n" + "=" * 50 + "\n"

        for i, order in enumerate(items, 1):
            order_number = order.get("orderNumber", "未知")
            order_status = order.get("orderStatusName", "未知状态")
            create_time = order.get("orderCreateTime", "未知时间")
            payable_amount = order.get("payableAmount", "0.00")
            merchant_name = order.get("merchantName", "未知商家")

            product_list = order.get("productList", [])
            product_names = []
            for product in product_list:
                product_names.append(product.get("name", "未知商品"))

            product_display = " | ".join(product_names) if product_names else "无商品信息"

            status_color = "🟢" if order.get("orderStatus") == 5 else "🟡" if order.get("orderStatus") == 4 else "🔵"

            result_text += f"{i:2d}. {status_color} 订单号: {order_number}\n"
            result_text += f"    📅 下单时间: {create_time}\n"
            result_text += f"    📦 商品: {product_display}\n"
            result_text += f"    💰 支付金额: ¥{payable_amount} | 🏪 商家: {merchant_name}\n"
            result_text += f"    📊 状态: {order_status}\n"
            result_text += "-" * 50 + "\n"

        sender.reply(result_text)
        return items

    def get_order_logistics(self, order_id: str) -> Dict[str, Any]:
        """获取订单物流信息"""
        logistics_url = f"{self.base_url}/order/packages"

        logistics_param = {"orderId": order_id}

        param_json = json.dumps(logistics_param, separators=(',', ':'), ensure_ascii=False)
        param_encoded = urllib.parse.quote(param_json, safe='')
        full_url = f"{logistics_url}?param={param_encoded}"

        try:
            response = self.session.get(full_url, verify=False)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e), "stateCode": -1}

    def display_logistics(self, logistics_result: Dict[str, Any]):
        """显示物流信息"""
        if logistics_result.get("stateCode") != 0:
            sender.reply(f"❌ 获取物流信息失败: {logistics_result.get('message', '未知错误')}")
            return

        data = logistics_result.get("data", [])

        if not data:
            sender.reply("❌ 暂无物流信息")
            return

        result_text = f"🚚 物流信息:\n" + "=" * 40 + "\n"

        for i, package in enumerate(data, 1):
            express_info = package.get("express", {})
            express_name = express_info.get("name", "未知快递")
            express_number = express_info.get("number", "无运单号")
            logistics_status = package.get("logistics", "无物流状态")
            sign_status = package.get("sign", 0)

            sign_text = "✅ 已签收" if sign_status == 1 else "📦 未签收"

            result_text += f"包裹 {i}:\n"
            result_text += f"  🚚 快递公司: {express_name}\n"
            result_text += f"  📋 运单号: {express_number}\n"
            result_text += f"  📍 最新状态: {logistics_status}\n"
            result_text += f"  ✉️  签收状态: {sign_text}\n"

            product_list = package.get("productList", [])
            if product_list:
                result_text += f"  📦 包裹商品:\n"
                for product in product_list:
                    name = product.get("name", "未知商品")
                    count = product.get("count", 1)
                    result_text += f"    - {name} × {count}\n"

            result_text += "-" * 40 + "\n"

        sender.reply(result_text)


def process_accounts_login(accounts_text: str) -> List[Dict[str, str]]:
    """处理账号信息"""
    accounts = []
    lines = accounts_text.strip().split('\n')

    for line in lines:
        line = line.strip()
        if '#' in line:
            parts = line.split('#', 1)
            if len(parts) == 2:
                phone = parts[0].strip()
                password = parts[1].strip()
                if phone and password:
                    accounts.append({"phone": phone, "password": password})

    return accounts


def show_main_menu():
    """显示主菜单"""
    sender.reply("""
🚀 福田下单系统 🚀
1️⃣ 开始下单
0️⃣ 退出""")


def show_logistics_menu():
    """显示物流查询菜单"""
    sender.reply("""
🚚 福田物流查询 🚚
1️⃣ 查看所有订单
2️⃣ 查看待收货订单
3️⃣ 查看已完成订单
0️⃣ 退出""")


def handle_logistics_query():
    """处理物流查询"""
    sender.reply("""
📱 账号登录 📱
请输入账号信息，格式：手机号#密码
回复 'q' 退出
""")

    account_input = sender.input(120000, 1, False)
    if not account_input:
        sender.reply("⏰ 输入超时")
        return

    if account_input.lower() == 'q':
        sender.reply("👋 已退出")
        return

    if '#' not in account_input:
        sender.reply("❌ 账号格式错误，请使用：手机号#密码")
        return

    parts = account_input.split('#', 1)
    if len(parts) != 2:
        sender.reply("❌ 账号格式错误，请使用：手机号#密码")
        return

    phone = parts[0].strip()
    password = parts[1].strip()

    if not phone or not password:
        sender.reply("❌ 手机号或密码不能为空")
        return

    bot = FutianOrderBot()
    sender.reply(f"🔐 正在登录账号: {phone}")

    if not bot.login(phone, password):
        sender.reply("❌ 登录失败，无法查询订单")
        return

    sender.reply(f"✅ 账号 {phone} 登录成功")

    sender.reply(f"🧹 正在清空账号 {phone} 的地址和购物车...")
    bot.clear_user_addresses()
    bot.clear_shopping_cart()

    while True:
        show_logistics_menu()
        choice = sender.input(60000, 1, False)

        if not choice or choice == "q" or choice == "0":
            sender.reply("👋 感谢使用，再见！")
            break
        elif choice == "1":
            status = "0"  # 全部订单
            sender.reply("🔍 正在获取全部订单...")
        elif choice == "2":
            status = "4"  # 待收货
            sender.reply("🔍 正在获取待收货订单...")
        elif choice == "3":
            status = "5"  # 已完成
            sender.reply("🔍 正在获取已完成订单...")
        else:
            sender.reply("❌ 无效选择，请重新输入")
            continue

        order_result = bot.get_order_list(status=status)
        orders = bot.display_order_list(order_result)

        if not orders:
            continue

        while True:
            sender.reply(f"请选择订单查看物流 (1-{len(orders)})：\n回复 'b' 返回主菜单，回复 'q' 退出")
            logistics_choice = sender.input(60000, 1, False)

            if not logistics_choice:
                sender.reply("⏰ 输入超时，已退出")
                return

            if logistics_choice.lower() == 'q':
                sender.reply("👋 已退出")
                return

            if logistics_choice.lower() == 'b':
                break

            try:
                choice_num = int(logistics_choice)
                if 1 <= choice_num <= len(orders):
                    selected_order = orders[choice_num - 1]
                    order_id = str(selected_order.get("id"))
                    order_number = selected_order.get("orderNumber", "未知订单号")

                    sender.reply(f"🔍 正在查询订单 {order_number} 的物流信息...")
                    logistics_result = bot.get_order_logistics(order_id)
                    bot.display_logistics(logistics_result)

                    sender.reply("查询完成，请继续选择订单查询或返回主菜单")
                else:
                    sender.reply(f"❌ 请输入 1-{len(orders)} 之间的数字")

            except ValueError:
                sender.reply("❌ 请输入有效的数字")


if __name__ == "__main__":
    if usermessage == '福田下单':
        while True:
            show_main_menu()
            choice = sender.input(60000, 1, False)

            if choice == "0" or choice == "q":
                sender.reply("👋 感谢使用，再见！")
                break
            elif choice == "1":
                sender.reply("""
📱 账号登录 📱
请输入账号信息，格式：手机号#密码
多个账号请每行一个
例如：
13800138000#password1
13800138001#password2

回复 'q' 退出
""")

                accounts_input = sender.input(120000, 1, False)
                if not accounts_input:
                    sender.reply("⏰ 输入超时")
                    break

                if accounts_input.lower() == 'q':
                    sender.reply("👋 已退出")
                    break

                accounts = process_accounts_login(accounts_input)
                if not accounts:
                    sender.reply("❌ 未识别到有效账号信息")
                    break

                bots = []
                for i, account in enumerate(accounts, 1):
                    bot = FutianOrderBot()

                    if bot.login(account['phone'], account['password']):
                        sender.reply(f"✅ 账号 {account['phone']} 登录成功")

                        sender.reply(f"🧹 正在清空账号 {account['phone']} 的地址和购物车...")
                        bot.clear_user_addresses()
                        bot.clear_shopping_cart()

                        bots.append(bot)
                    else:
                        sender.reply(f"❌ 账号 {account['phone']} 登录失败")

                if not bots:
                    sender.reply("❌ 没有账号登录成功，无法继续")
                    break


                sender.reply("""
📦 收货信息 📦
请输入收货人姓名：
回复 'q' 退出
""")

                name = sender.input(60000, 1, False)
                if not name:
                    sender.reply("⏰ 输入超时")
                    break

                if name.lower() == 'q':
                    sender.reply("👋 已退出")
                    break

                sender.reply("📞 请输入收货人手机号：\n回复 'q' 退出")
                mobile = sender.input(60000, 1, False)
                if not mobile:
                    sender.reply("⏰ 输入超时")
                    break

                if mobile.lower() == 'q':
                    sender.reply("👋 已退出")
                    break

                temp_bot = bots[0] if bots else FutianOrderBot()
                region_id = temp_bot.interactive_region_selection()
                if not region_id:
                    sender.reply("❌ 地区选择失败")
                    break

                sender.reply("🏠 请输入详细地址（街道门牌号等）：\n回复 'q' 退出")
                detail_address = sender.input(60000, 1, False)
                if not detail_address:
                    sender.reply("⏰ 输入超时")
                    break

                if detail_address.lower() == 'q':
                    sender.reply("👋 已退出")
                    break

                shipping_info = {
                    "name": name.strip(),
                    "mobile": mobile.strip(),
                    "address": detail_address.strip(),
                    "region_id": region_id,
                    "alias": name.strip()
                }

                for bot in bots:
                    bot.shipping_address = shipping_info

                sender.reply(f"""
✅ 收货信息确认：
👤 姓名：{name}
📞 手机：{mobile}
🏠 地址：{detail_address}
""")

                while True:
                    sender.reply("""
🔍 商品搜索 🔍
请输入要搜索的商品名称：
回复 'q' 退出
""")

                    search_word = sender.input(60000, 1, False)
                    if not search_word:
                        sender.reply("⏰ 输入超时")
                        break

                    if search_word.lower() == 'q':
                        sender.reply("👋 已退出")
                        break

                    sender.reply(f"🔍 正在搜索：{search_word}")

                    search_result = bots[0].search_products(search_word)
                    items = bots[0].display_search_results(search_result)

                    if not items:
                        sender.reply("❌ 没有找到商品，请重新搜索")
                        continue

                    sender.reply(f"请选择商品 (1-{len(items)})：\n回复 'q' 退出")
                    choice = sender.input(60000, 1, False)

                    if not choice:
                        sender.reply("⏰ 输入超时")
                        break

                    if choice.lower() == 'q':
                        sender.reply("👋 已退出")
                        break

                    try:
                        choice_num = int(choice)
                        if 1 <= choice_num <= len(items):
                            selected_item = items[choice_num - 1]
                            goods = selected_item.get("goods", {})

                            if not selected_item.get("sellable", False):
                                sender.reply("❌ 该商品当前不可使用，请选择其他商品")
                                continue

                            if goods.get("availableStock", 0) <= 0:
                                sender.reply("❌ 该商品库存不足，请选择其他商品")
                                continue

                            name = selected_item.get('name')
                            point_price = goods.get('point', 0)
                            goods_id = goods.get('id')
                            min_purchase_num = goods.get('minPurchaseNum', 1)

                            sender.reply(f"""
✅ 已选择商品：{name}
💰 积分价格：{point_price} 积分
🔢 起购数量：{min_purchase_num}

确认选择此商品吗？(y/n)
回复 'q' 退出
""")

                            confirm = sender.input(60000, 1, False)

                            if not confirm:
                                sender.reply("⏰ 输入超时")
                                break

                            if confirm.lower() == 'q':
                                sender.reply("👋 已退出")
                                break

                            if confirm and confirm.lower() in ['y', 'yes', '是']:
                                success_count = 0
                                for i, bot in enumerate(bots, 1):
                                    try:
                                        sender.reply(f"📦 账号 {i} 正在下单...")

                                        if not bot.clear_and_add_to_cart(goods_id, min_purchase_num):
                                            sender.reply(f"❌ 账号 {i} 购物车操作失败")
                                            continue

                                        address_id = bot.create_shipping_address()
                                        if not address_id:
                                            sender.reply(f"❌ 账号 {i} 创建收货地址失败")
                                            continue

                                        order_result = bot.create_order(address_id, point_price)
                                        if order_result.get("stateCode") != 0:
                                            sender.reply(f"❌ 账号 {i} 下单失败: {order_result.get('message', '未知错误')}")
                                            bot.delete_shipping_address(address_id)
                                            continue

                                        order_data = order_result.get("data", {})
                                        order_number = order_data.get("orderNumber") or order_data.get("orderNo")

                                        sender.reply(f"🎉 账号 {i} 下单成功！订单号：{order_number}")
                                        success_count += 1

                                        bot.delete_shipping_address(address_id)

                                    except Exception as e:
                                        sender.reply(f"❌ 账号 {i} 下单异常：{str(e)}")

                                sender.reply(f"""
🎊 批量下单完成！
✅ 成功：{success_count} 个账号
❌ 失败：{len(bots) - success_count} 个账号
📦 商品：{name}
💰 积分：{point_price} 积分/单
""")
                                break
                            else:
                                sender.reply("❌ 已取消选择")
                                continue
                        else:
                            sender.reply(f"❌ 请输入 1-{len(items)} 之间的数字")
                    except ValueError:
                        sender.reply("❌ 请输入有效的数字")

                    break
                break
            else:
                sender.reply("❌ 无效的选择，已退出")
                break
    elif usermessage == '福田物流查询':
        handle_logistics_query()
    else:
        sender.setContinue()
