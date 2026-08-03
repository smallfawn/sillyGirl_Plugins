r"""
/**
 * @title 瑞幸咖啡抽奖
 * @author sillyGirl
 * @version v1.0.0
 * @desc 从 SmallCat 读取微信账号，完成瑞幸小程序登录、活动校验、抽奖和中奖记录查询
 * @rule raw ^\s*(瑞幸|瑞幸咖啡|[Ll][Uu][Cc][Kk][Ii][Nn])\s*(查询|抽奖)?\s*$
 * @admin false
 * @priority 10
 * @public true
 * @class 工具
 * @depe ["requests","cryptography"]
 */
"""

from __future__ import annotations

import asyncio
import base64
import hashlib
import json
import os
import random
import re
import string
import time
import uuid
from typing import Any
from urllib.parse import urlencode

from sillygirl import SmallCat, SillyGirlPluginConfig, sender as s, sillyGirlCreateSchema

APP_ID = "wx21c7506e98a2fe75"
APP_VERSION = "916"
MINI_VERSION = "5572"
AKV = "lk-wxmp-v5.3.22"
API_KEY = "CJQjAc1hYieC4QYb"
CID = "230101"
DK = 1
BRAND_TYPE = "LK001"

DEFAULT_ACTIVITY_NO = "CJ202607029027751995"
DEFAULT_ACTIVITY_ID = 1367
CAPI_BASE = "https://capi.lkcoffee.com"
MKT_BASE = "https://mkt.lkcoffee.com"

UA_CAPI = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 "
    "MicroMessenger/8.0.75(0x18004b34) NetType/WIFI Language/zh_CN"
)
UA_MKT = UA_CAPI + f" miniProgram/{APP_ID}"

DEFAULTS = {
    "enable": True,
    "smallcat_id": 1,
    "account_selector": "",
    "activity_no": DEFAULT_ACTIVITY_NO,
    "activity_id": DEFAULT_ACTIVITY_ID,
    "query_only": False,
    "proxy_url": "",
    "request_timeout": 20,
    "debug": False,
}

schema = sillyGirlCreateSchema.object(
    {
        "enable": sillyGirlCreateSchema.boolean().setTitle("是否启用").setDefault(True),
        "smallcat_id": (
            sillyGirlCreateSchema.integer()
            .setTitle("smallcat 编号")
            .setDescription("后台 smallcat 页面里的编号，从 1 开始；AUTH 直接使用面板配置")
            .setMin(1)
            .setDefault(1)
        ),
        "account_selector": (
            sillyGirlCreateSchema.string()
            .setTitle("执行账号")
            .setDescription("留空取首个可用账号；可填序号、openid、昵称；填“全部”执行全部账号")
            .setDefault("")
        ),
        "activity_no": (
            sillyGirlCreateSchema.string()
            .setTitle("活动编号 activityNo")
            .setDescription("默认使用内置的幸运星期三活动；活动更新后可在这里覆盖")
            .setDefault(DEFAULT_ACTIVITY_NO)
        ),
        "activity_id": (
            sillyGirlCreateSchema.integer()
            .setTitle("活动 ID")
            .setDescription("活动详情未返回 activityId 时使用的兜底值")
            .setMin(1)
            .setDefault(DEFAULT_ACTIVITY_ID)
        ),
        "query_only": (
            sillyGirlCreateSchema.boolean()
            .setTitle("仅查询")
            .setDescription("开启后只查询活动和中奖记录，不提交抽奖；命令“瑞幸 查询”也会临时开启")
            .setDefault(False)
        ),
        "proxy_url": (
            sillyGirlCreateSchema.string()
            .setTitle("业务请求代理")
            .setDescription("留空使用 SmallCat 账号 proxyUrl；支持 http/https 代理")
            .setDefault("")
        ),
        "request_timeout": (
            sillyGirlCreateSchema.integer()
            .setTitle("请求超时秒数")
            .setMin(5)
            .setMax(90)
            .setDefault(20)
        ),
        "debug": sillyGirlCreateSchema.boolean().setTitle("调试日志").setDefault(False),
    }
)
plugin_config = SillyGirlPluginConfig(schema)

# 配置扫描会设置 SILLYGIRL_CONFIG_REGISTER_ONLY；SillyGirlPluginConfig 在上面写出
# schema 后直接结束进程。第三方业务依赖必须放在它后面，否则首次安装尚未装依赖时，
# import 会抢先报错，后台只能检测到配置代码却拿不到配置表单。
import requests
import urllib3
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class PhoneAuthorizationRequired(RuntimeError):
    pass


def now_ms() -> int:
    return int(time.time() * 1000)


def mask_phone(value: Any) -> str:
    return re.sub(r"(1\d{2})\d{4}(\d{4})", r"\1****\2", str(value or ""))


def compact_json(value: Any, limit: int = 500) -> str:
    try:
        text = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    except Exception:
        text = str(value)
    return text if len(text) <= limit else text[:limit] + "..."


def aes_ecb_encrypt(data: bytes, key: bytes) -> bytes:
    pad_len = 16 - len(data) % 16
    padded = data + bytes([pad_len]) * pad_len
    encryptor = Cipher(algorithms.AES(key), modes.ECB()).encryptor()
    return encryptor.update(padded) + encryptor.finalize()


def aes_ecb_decrypt(data: bytes, key: bytes) -> bytes:
    decryptor = Cipher(algorithms.AES(key), modes.ECB()).decryptor()
    output = decryptor.update(data) + decryptor.finalize()
    if not output:
        raise ValueError("AES 解密结果为空")
    pad_len = output[-1]
    if pad_len < 1 or pad_len > 16 or output[-pad_len:] != bytes([pad_len]) * pad_len:
        raise ValueError("AES PKCS#7 padding 异常")
    return output[:-pad_len]


def aes_encrypt_urlsafe(text: str) -> str:
    encrypted = aes_ecb_encrypt(text.encode("utf-8"), API_KEY.encode("utf-8"))
    return base64.b64encode(encrypted).decode("ascii").replace("+", "-").replace("/", "_")


def aes_decrypt_urlsafe(text: str) -> str:
    encoded = str(text or "").replace("-", "+").replace("_", "/")
    encoded += "=" * (-len(encoded) % 4)
    decrypted = aes_ecb_decrypt(base64.b64decode(encoded), API_KEY.encode("utf-8"))
    return decrypted.decode("utf-8")


def md5_words(value: Any) -> str:
    digest = hashlib.md5(str(value).encode("utf-8")).digest()
    words = []
    for index in range(0, 16, 4):
        number = int.from_bytes(digest[index : index + 4], "big", signed=True)
        words.append(str(abs(number)))
    return "".join(words)


def build_payload(data: dict[str, Any] | None, uid: str = "") -> dict[str, Any]:
    body = dict(data or {})
    body.setdefault("miniversion", MINI_VERSION)
    plain = json.dumps(body, ensure_ascii=False, separators=(",", ":"))
    q = aes_encrypt_urlsafe(plain)
    payload: dict[str, Any] = {"cid": CID, "q": q, "dk": DK}
    sign_parts = [f"cid={CID}", f"dk={DK}", f"q={q}"]
    if uid:
        payload["uid"] = str(uid)
        sign_parts.append(f"uid={uid}")
    payload["sign"] = md5_words(";".join(sign_parts) + API_KEY)
    return payload


def decrypt_capi_response(text: str) -> dict[str, Any]:
    value = str(text or "").strip()
    if not value:
        return {}
    if value.startswith("{"):
        parsed = json.loads(value)
    else:
        try:
            parsed = json.loads(aes_decrypt_urlsafe(value))
        except Exception as exc:
            raise RuntimeError(f"瑞幸响应解密失败：{value[:100]}") from exc
    if not isinstance(parsed, dict):
        raise RuntimeError("瑞幸响应不是 JSON 对象")
    return parsed


def random_text(chars: str, length: int) -> str:
    return "".join(random.choice(chars) for _ in range(length))


def generate_blackbox(prefix: str = "uMPHR") -> str:
    return f"{prefix}{int(time.time())}{random_text(string.ascii_letters + string.digits, 12)}"


def generate_did() -> str:
    return random_text(string.ascii_lowercase + string.digits, 32)


def generate_device_id() -> str:
    return random_text(string.ascii_letters + string.digits + "+/", 48)


def clean_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def decode_json_strings(value: Any, depth: int = 0) -> Any:
    if depth > 8 or not isinstance(value, str):
        return value
    text = value.strip()
    if not text.startswith(("{", "[")):
        return value
    try:
        return decode_json_strings(json.loads(text), depth + 1)
    except Exception:
        return value


def decode_json_tree(value: Any, depth: int = 0) -> Any:
    if depth > 10:
        return value
    decoded = decode_json_strings(value, depth)
    if decoded is not value:
        return decode_json_tree(decoded, depth + 1)
    if isinstance(value, list):
        return [decode_json_tree(item, depth + 1) for item in value]
    if isinstance(value, dict):
        return {key: decode_json_tree(item, depth + 1) for key, item in value.items()}
    return value


def response_message(payload: Any) -> str:
    value = decode_json_tree(payload)
    if not isinstance(value, dict):
        return str(value or "")
    for key in ("message", "msg", "errmsg", "errMsg", "error"):
        if value.get(key):
            return clean_text(value[key] if not isinstance(value[key], (dict, list)) else compact_json(value[key], 300))
    nested = value.get("data")
    return response_message(nested) if nested is not None and nested is not value else ""


def unwrap_smallcat(payload: Any) -> Any:
    value = decode_json_tree(payload)
    if not isinstance(value, dict):
        return value
    if "status" in value:
        if value.get("status") is False:
            raise RuntimeError(response_message(value) or "SmallCat 接口返回失败状态")
        if "data" in value:
            return decode_json_tree(value["data"])
    if "code" in value and "data" in value and str(value.get("code")) in {"0", "200", "201"}:
        return decode_json_tree(value["data"])
    return value


def find_deep_value(value: Any, keys: tuple[str, ...], pattern: str = "", depth: int = 0) -> str:
    if depth > 12 or value is None:
        return ""
    decoded = decode_json_strings(value, depth)
    if decoded is not value:
        return find_deep_value(decoded, keys, pattern, depth + 1)
    expected = {key.lower() for key in keys}
    if isinstance(value, dict):
        for key, item in value.items():
            if key.lower() not in expected or isinstance(item, (dict, list)) or item is None:
                continue
            text = str(item).strip()
            if text and (not pattern or re.fullmatch(pattern, text)):
                return text
        for item in value.values():
            found = find_deep_value(item, keys, pattern, depth + 1)
            if found:
                return found
    elif isinstance(value, list):
        for item in value:
            found = find_deep_value(item, keys, pattern, depth + 1)
            if found:
                return found
    return ""


def has_deep_truthy(value: Any, expected_key: str, depth: int = 0) -> bool:
    if depth > 12 or value is None:
        return False
    decoded = decode_json_strings(value, depth)
    if decoded is not value:
        return has_deep_truthy(decoded, expected_key, depth + 1)
    if isinstance(value, dict):
        for key, item in value.items():
            if key.lower() == expected_key.lower() and as_bool(item):
                return True
            if has_deep_truthy(item, expected_key, depth + 1):
                return True
    elif isinstance(value, list):
        return any(has_deep_truthy(item, expected_key, depth + 1) for item in value)
    return False


def normalize_accounts(payload: Any) -> list[dict[str, Any]]:
    value = unwrap_smallcat(payload)
    if isinstance(value, dict):
        value = value.get("accounts") or value.get("items") or value.get("list") or value.get("value") or value.get("data")
    if isinstance(value, dict):
        value = value.get("items") or value.get("list") or value.get("data")
    accounts = []
    for item in value if isinstance(value, list) else []:
        if not isinstance(item, dict):
            continue
        account = dict(item)
        account["openid"] = str(item.get("openid") or item.get("openId") or item.get("userKey") or "").strip()
        account["proxyUrl"] = str(item.get("proxyUrl") or item.get("proxy_url") or "").strip()
        account["disabled"] = as_bool(item.get("disabled"))
        if account["openid"]:
            accounts.append(account)
    return accounts


def select_accounts(accounts: list[dict[str, Any]], selector: str) -> list[dict[str, Any]]:
    enabled = [account for account in accounts if not account.get("disabled")]
    if not enabled:
        raise RuntimeError("SmallCat 用户列表没有可用账号")
    text = str(selector or "").strip()
    if not text:
        return [enabled[0]]
    if text.lower() in {"all", "全部", "所有"}:
        return enabled
    if text.isdigit():
        index = int(text) - 1
        if index < 0 or index >= len(enabled):
            raise RuntimeError(f"SmallCat 可用账号序号 {text} 不存在")
        return [enabled[index]]
    lower = text.lower()
    for account in enabled:
        values = (
            account.get("openid"),
            account.get("displayName"),
            account.get("nickname"),
            account.get("name"),
            account.get("remark"),
        )
        if any(str(value or "").strip().lower() == lower for value in values):
            return [account]
    raise RuntimeError(f"SmallCat 未找到账号：{text}")


def account_name(account: dict[str, Any]) -> str:
    return str(
        account.get("displayName")
        or account.get("nickname")
        or account.get("name")
        or account.get("remark")
        or account.get("openid")
        or "账号"
    ).strip()


def history_summary(records: Any, error: str = "") -> str:
    if error:
        return f"历史中奖记录查询失败：{mask_phone(error)}"
    if not isinstance(records, list) or not records:
        return "历史中奖记录：暂无"
    parts = []
    for item in records[:3]:
        if not isinstance(item, dict):
            continue
        prize = (
            item.get("prizeName")
            or item.get("couponName")
            or item.get("name")
            or item.get("prizeDesc")
            or item.get("title")
        )
        when = item.get("createTime") or item.get("receiveTime") or item.get("winTime") or ""
        if prize:
            parts.append(f"{prize}({when})" if when else str(prize))
    if not parts:
        return f"历史中奖记录：{len(records)} 条，未识别奖品名"
    suffix = f" 等 {len(records)} 条" if len(records) > len(parts) else ""
    return "历史中奖记录：" + "；".join(parts) + suffix


def draw_summary(message: str, records: Any = None, records_error: str = "") -> str:
    text = clean_text(message)
    history = history_summary(records or [], records_error)
    if not text:
        return history
    if "很遗憾" in text or "没有抽中" in text or "未中奖" in text:
        return f"未中奖：{text}\n{history}"
    if "次数上限" in text or "不可再参加" in text:
        return f"今日已达参与次数上限：{text}\n{history}"
    return f"抽奖结果：{text}\n{history}"


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    return str(value or "").strip().lower() in {"1", "true", "yes", "on"}


def positive_int(value: Any, fallback: int) -> int:
    try:
        number = int(value)
        return number if number > 0 else fallback
    except Exception:
        return fallback


def normalize_config(raw: Any) -> dict[str, Any]:
    source = raw if isinstance(raw, dict) else {}
    config = dict(DEFAULTS)
    config.update(source)
    config["enable"] = True if "enable" not in source else as_bool(source.get("enable"))
    config["smallcat_id"] = positive_int(config.get("smallcat_id"), 1)
    config["account_selector"] = str(config.get("account_selector") or "").strip()
    config["activity_no"] = str(config.get("activity_no") or DEFAULT_ACTIVITY_NO).strip()
    config["activity_id"] = positive_int(config.get("activity_id"), DEFAULT_ACTIVITY_ID)
    config["query_only"] = as_bool(config.get("query_only"))
    config["proxy_url"] = str(config.get("proxy_url") or "").strip()
    config["request_timeout"] = max(5, min(positive_int(config.get("request_timeout"), 20), 90))
    config["debug"] = as_bool(config.get("debug"))
    if not re.fullmatch(r"[A-Za-z0-9_-]{8,100}", config["activity_no"]):
        raise RuntimeError("activity_no 格式异常")
    return config


def parse_command(content: str) -> dict[str, bool]:
    match = re.fullmatch(r"\s*(瑞幸|瑞幸咖啡|luckin)\s*(查询|抽奖)?\s*", str(content or ""), re.IGNORECASE)
    if not match:
        raise RuntimeError("命令格式：瑞幸 [查询|抽奖]")
    return {"query_only": str(match.group(2) or "") == "查询"}


class LuckinRunner:
    def __init__(self, account: dict[str, Any], config: dict[str, Any]) -> None:
        self.account = account
        self.openid = str(account.get("openid") or "")
        self.activity_no = str(config["activity_no"])
        self.activity_id_default = int(config["activity_id"])
        self.timeout = int(config["request_timeout"])
        self.debug = bool(config["debug"])
        self.lines: list[str] = []
        self.session = requests.Session()
        self.session.verify = False
        proxy_url = str(config.get("proxy_url") or account.get("proxyUrl") or "").strip()
        if proxy_url:
            self.session.proxies.update({"http": proxy_url, "https": proxy_url})
        self.reset_identity()

    def reset_identity(self) -> None:
        self.csid = str(uuid.uuid4())
        self.blackbox = generate_blackbox("uMPHR")
        self.did = generate_did()
        self.h5_blackbox = generate_blackbox("uWPHA")
        self.device_id = generate_device_id()
        self.user_id = ""
        self.uid = ""
        self.luckin_openid = ""
        self.auth_code = ""

    def log(self, message: str, level: str = "INFO") -> None:
        line = f"[{level}] {mask_phone(message)}"
        self.lines.append(line)
        if self.debug:
            print(line, flush=True)

    def capi_headers(self, mid: str = "") -> dict[str, str]:
        headers = {
            "User-Agent": UA_CAPI,
            "Referer": f"https://servicewechat.com/{APP_ID}/{APP_VERSION}/page-frame.html",
            "content-type": "application/x-www-form-urlencoded",
            "X-LK-CSID": self.csid,
            "X-LK-AKV": AKV,
            "x-lkwx-sdkversion": "3.16.1",
            "x-lkwx-ostype": "ios",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }
        if mid:
            headers["X-LK-MID"] = str(mid)
        return headers

    def capi_request(
        self,
        method: str,
        path: str,
        data: dict[str, Any] | None = None,
        mid: str = "",
        uid: str = "",
    ) -> dict[str, Any]:
        payload = build_payload(data or {}, uid=uid)
        request_args: dict[str, Any] = {"headers": self.capi_headers(mid), "timeout": self.timeout}
        if method.upper() == "GET":
            request_args["params"] = payload
        else:
            request_args["data"] = payload
        response = self.session.request(method.upper(), CAPI_BASE + path, **request_args)
        if response.status_code >= 400:
            raise RuntimeError(f"瑞幸接口 HTTP {response.status_code}：{response.text[:160]}")
        obj = decrypt_capi_response(response.text)
        if obj.get("code") != 1:
            message = obj.get("msg") or obj.get("busiCode") or compact_json(obj, 200)
            raise RuntimeError(f"瑞幸接口失败：{message}")
        return obj

    def login(self, wx_code: str, phone_info: dict[str, str] | None = None) -> dict[str, Any]:
        data: dict[str, Any] = {
            "code": wx_code,
            "isAuthorization": bool(phone_info),
            "blackBox": self.blackbox,
            "did": self.did,
            "deptId": "",
        }
        if phone_info:
            if phone_info.get("iv") and phone_info.get("encryptedData"):
                data["iv"] = phone_info["iv"]
                data["encryptedData"] = phone_info["encryptedData"]
            if phone_info.get("phoneCode"):
                data["phoneCode"] = phone_info["phoneCode"]
        obj = self.capi_request("POST", "/resource/m/user/wxminilogin", data)
        content = obj.get("content") if isinstance(obj.get("content"), dict) else {}
        if content.get("needAuthorized"):
            raise PhoneAuthorizationRequired("瑞幸登录需要手机号授权：needAuthorized=true")
        self.uid = str(obj.get("uid") or "")
        self.user_id = str(content.get("userId") or "")
        self.luckin_openid = str(content.get("openid") or "")
        if not self.user_id or not self.luckin_openid:
            message = content.get("msg") or obj.get("msg") or "未返回 userId/openid"
            if "信息异常" in str(message):
                raise PhoneAuthorizationRequired(f"瑞幸登录需要手机号授权：{message}")
            raise RuntimeError(f"瑞幸登录失败：{message}")
        return content

    def get_auth_code(self) -> str:
        origin_url = (
            f"{MKT_BASE}/ladder/draw-series/11rgg68x"
            f"?activityNo={self.activity_no}&miniversion={MINI_VERSION}"
            f"&frommini=mini&brandType={BRAND_TYPE}&origin=27&userId={self.user_id}"
        )
        data = {
            "originUrl": origin_url,
            "openAuthRms": {
                "openId": self.luckin_openid,
                "blackBox": self.blackbox,
                "longitude": "",
                "latitude": "",
            },
        }
        obj = self.capi_request("GET", "/resource/m/open/getAuthCode", data, mid=self.user_id, uid=self.uid)
        content = obj.get("content") if isinstance(obj.get("content"), dict) else {}
        self.auth_code = str(content.get("code") or "").strip()
        if not self.auth_code:
            raise RuntimeError("getAuthCode 未返回 authCode")
        return self.auth_code

    def h5_url(self) -> str:
        return (
            f"{MKT_BASE}/ladder/draw-series/11rgg68x"
            f"?activityNo={self.activity_no}&miniversion={MINI_VERSION}"
            f"&frommini=mini&brandType={BRAND_TYPE}&origin=27"
            f"&userId={self.user_id}&authCode={self.auth_code}&userType=0"
        )

    def mkt_headers(self) -> dict[str, str]:
        return {
            "User-Agent": UA_MKT,
            "Accept": "application/json, text/plain, */*",
            "Referer": self.h5_url(),
        }

    def mkt_request(self, path: str, query: dict[str, Any]) -> dict[str, Any]:
        params = dict(query or {})
        params["_"] = now_ms()
        query_text = json.dumps(params, ensure_ascii=False, separators=(",", ":"))
        url = f"{MKT_BASE}{path}?{urlencode({'queryParamsStr': query_text})}"
        response = self.session.get(url, headers=self.mkt_headers(), timeout=self.timeout)
        if response.status_code >= 400:
            raise RuntimeError(f"H5 接口 HTTP {response.status_code}：{response.text[:160]}")
        try:
            obj = response.json()
        except Exception as exc:
            raise RuntimeError(f"H5 接口未返回 JSON：HTTP {response.status_code} {response.text[:160]}") from exc
        if not isinstance(obj, dict):
            raise RuntimeError("H5 接口响应不是 JSON 对象")
        if obj.get("code") not in (1, None) and not obj.get("success"):
            raise RuntimeError(str(obj.get("msg") or obj.get("busiCode") or compact_json(obj, 200)))
        return obj

    def open_and_check(self) -> dict[str, Any]:
        response = self.session.get(self.h5_url(), headers={"User-Agent": UA_MKT}, timeout=self.timeout)
        if response.status_code >= 400:
            raise RuntimeError(f"活动页面 HTTP {response.status_code}")
        obj = self.mkt_request("/ladder/capi/resource/m/open/check", {"loading": False, "code": self.auth_code})
        content = obj.get("content") if isinstance(obj.get("content"), dict) else {}
        if not content.get("checked"):
            raise RuntimeError(str(obj.get("msg") or "open/check 未通过"))
        return content

    def activity_detail(self, activity_id: str = "") -> dict[str, Any]:
        obj = self.mkt_request(
            "/ladder/skcapi/resource/bff/v2/lotteryDraw/detail",
            {"activityId": activity_id, "activityNo": self.activity_no, "handleMsg": False},
        )
        return obj.get("content") if isinstance(obj.get("content"), dict) else {}

    def draw(self, activity_id: Any) -> dict[str, Any]:
        obj = self.mkt_request(
            "/ladder/skcapi/resource/m/lotteryDraw/action",
            {
                "blackBox": self.h5_blackbox,
                "deviceId": self.device_id,
                "activityId": int(activity_id),
                "activityNo": self.activity_no,
                "origin": 14,
                "handleMsg": False,
                "version": int(MINI_VERSION),
            },
        )
        return obj.get("content") if isinstance(obj.get("content"), dict) else {}

    def my_records(self) -> list[Any]:
        obj = self.mkt_request(
            "/ladder/skcapi/resource/bff/lotteryDraw/memberLotteryRecord",
            {"activityNo": self.activity_no, "pageIndex": 0, "pageSize": 100},
        )
        content = obj.get("content")
        return content if isinstance(content, list) else []

    def safe_records(self) -> tuple[list[Any], str]:
        try:
            return self.my_records(), ""
        except Exception as exc:
            return [], str(exc)

    def execute(self, wx_code: str, phone_info: dict[str, str] | None, query_only: bool) -> str:
        self.login(wx_code, phone_info)
        self.log("瑞幸登录成功" + ("，手机号授权数据已提交" if phone_info else ""), "SUCCESS")
        self.get_auth_code()
        self.log("已获取 authCode")
        self.open_and_check()
        self.log("活动校验通过")
        detail = self.activity_detail("")
        activity_id = detail.get("activityId") or self.activity_id_default
        status = detail.get("activityLotteryStatus")
        records, records_error = self.safe_records()
        if query_only:
            return f"活动查询：activityId={activity_id}，状态={status}\n{history_summary(records, records_error)}"
        self.log(f"开始抽奖（activityId={activity_id}，状态={status}）")
        result = self.draw(activity_id)
        message = result.get("prizeName") or result.get("notHitPrizeReasonMsg") or result.get("msg") or ""
        records, records_error = self.safe_records()
        if message:
            return draw_summary(str(message), records, records_error)
        if records:
            return history_summary(records)
        return f"抽奖完成，但未识别奖品，活动状态 {status}\n{history_summary(records, records_error)}"

    def close(self) -> None:
        self.session.close()


async def get_wx_code(smallcat: SmallCat, openid: str) -> str:
    raw = await smallcat.getCode({"openid": openid, "appid": APP_ID})
    payload = unwrap_smallcat(raw)
    code = find_deep_value(payload, ("code", "wxcode", "wx_code", "loginCode"), r"[0-9A-Za-z_-]{8,4096}")
    if not code:
        raise RuntimeError("SmallCat wx.login 取码失败：" + (response_message(raw) or compact_json(raw, 400)))
    return code


async def get_phone_info(smallcat: SmallCat, openid: str) -> dict[str, str]:
    try:
        raw = await smallcat.getPhoneNumber({"openid": openid, "appid": APP_ID})
    except Exception as exc:
        raise RuntimeError(f"SmallCat 手机号授权失败：{exc}") from exc
    payload = unwrap_smallcat(raw)
    iv = find_deep_value(payload, ("iv",), r".{8,4096}")
    encrypted_data = find_deep_value(payload, ("encryptedData", "encrypted_data"), r".{8,16384}")
    phone_code = find_deep_value(payload, ("phoneCode", "phone_code", "code"), r"[0-9A-Za-z_-]{8,4096}")
    if iv and encrypted_data:
        return {"iv": iv, "encryptedData": encrypted_data, "phoneCode": phone_code}
    if phone_code:
        return {"iv": "", "encryptedData": "", "phoneCode": phone_code}
    prefix = "need_auth=true；" if has_deep_truthy(raw, "need_auth") else ""
    raise RuntimeError(prefix + "SmallCat 响应缺少 iv/encryptedData 或手机号临时 code：" + compact_json(raw, 700))


def should_retry_phone(error: Exception) -> bool:
    if isinstance(error, PhoneAuthorizationRequired):
        return True
    text = str(error)
    return any(flag in text for flag in ("needAuthorized", "需要手机号授权", "信息异常"))


async def run_account(
    smallcat: SmallCat,
    account: dict[str, Any],
    config: dict[str, Any],
    query_only: bool,
) -> dict[str, Any]:
    runner = LuckinRunner(account, config)
    label = account_name(account)
    runner.log(f"▶ 账号：{label}")
    try:
        wx_code = await get_wx_code(smallcat, runner.openid)
        runner.log("wx.login code 获取成功", "SUCCESS")
        try:
            summary = await asyncio.to_thread(runner.execute, wx_code, None, query_only)
        except Exception as first_error:
            if not should_retry_phone(first_error):
                raise
            runner.log(f"普通登录要求手机号授权：{first_error}", "WARNING")
            phone_info = await get_phone_info(smallcat, runner.openid)
            mode = "iv/encryptedData" if phone_info.get("iv") else "phoneCode"
            runner.log(f"手机号授权数据获取成功（{mode}）", "SUCCESS")
            wx_code = await get_wx_code(smallcat, runner.openid)
            runner.log("重试 wx.login code 获取成功", "SUCCESS")
            runner.reset_identity()
            summary = await asyncio.to_thread(runner.execute, wx_code, phone_info, query_only)
        first_line = summary.splitlines()[0] if summary else "执行完成"
        level = "WARNING" if any(word in first_line for word in ("未中奖", "上限")) else "SUCCESS"
        runner.log(first_line, level)
        for line in summary.splitlines()[1:]:
            runner.log(line)
        return {"success": True, "account": label, "summary": summary, "lines": runner.lines}
    except Exception as exc:
        message = mask_phone(exc)
        runner.log(f"执行异常：{message}", "ERROR")
        return {"success": False, "account": label, "error": message, "lines": runner.lines}
    finally:
        runner.close()


def format_result(result: dict[str, Any]) -> str:
    if result.get("success"):
        tail = "结果：成功 | " + str(result.get("summary") or "执行完成").replace("\n", " | ")
    else:
        tail = "结果：失败 | " + str(result.get("error") or "未知错误")
    return "\n".join([*result.get("lines", []), tail])


async def main() -> None:
    config = normalize_config(await plugin_config.get())
    if not config["enable"]:
        await s.reply("瑞幸咖啡抽奖插件未启用")
        return
    try:
        command = parse_command(str(await s.getContent() or ""))
        query_only = bool(config["query_only"] or command["query_only"])
        smallcat = SmallCat({"id": config["smallcat_id"]})
        accounts = select_accounts(normalize_accounts(await smallcat.userList()), config["account_selector"])
        mode = "查询" if query_only else "抽奖"
        await s.reply(f"瑞幸咖啡{mode}开始：SmallCat #{config['smallcat_id']}，账号 {len(accounts)} 个")
        results = []
        for account in accounts:
            results.append(await run_account(smallcat, account, config, query_only))
        await s.reply("\n\n".join(format_result(result) for result in results))
    except Exception as exc:
        await s.reply("瑞幸咖啡执行失败：" + mask_phone(exc))


if os.environ.get("LUCKIN_PLUGIN_TEST") != "1":
    asyncio.run(main())
