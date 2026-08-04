r"""
/**
 * @title 美团Code登录
 * @author sillyGirl
 * @version v1.1.1
 * @desc 从 SmallCat 读取微信账号和 wx.login CODE，本地生成 mtgsig/siua/dfpid，换取美团 MT_TOKEN；可选同步青龙/呆呆
 * @rule raw ^\s*(美团|[Mm][Ee][Ii][Tt][Uu][Aa][Nn])\s*(登录|取[Tt]oken)?\s*([^\s]+)?\s*$
 * @admin true
 * @priority 10
 * @public true
 * @class 工具
 * @depe ["cryptography","httpx","pycryptodome"]
 */
"""

from __future__ import annotations

import asyncio
import base64
import gzip
import hashlib
import json
import os
import random
import re
import secrets
import struct
import time
import urllib.parse
import zlib
from collections import OrderedDict
from typing import Any, Dict, Iterable, List, MutableMapping, Optional, Sequence, Tuple

from sillygirl import Container, form, sender as s, utils

ct = Container()

# JSGuard 固定参数。签名、siua、dfpid 均在本文件内生成。
MTG_BASE64_ALPHABET = "ZmserbBoHQtNP+wOcza/LpngG8yJq42KWYj0DSfdikx3VT16IlUAFM97hECvuRX5"
MURMUR_M = 1540483477
MEITUAN_APPID = "wxde8ac0a21135c07d"
LOGIN_URL = "https://open.meituan.com/user/v1/weappsilentlogin"

DEFAULTS = {
    "enable": True,
    "smallcat_id": 1,
    "account_mode": "authorized",
    "manual_openids": "",
    "account_selector": "",
    "proxy_url": "",
    "request_timeout": 25,
    "sync_panel": "none",
    "sync_qinglong": False,
    "qinglong_id": 1,
    "daidai_id": 1,
    "ql_env_name": "MT_TOKEN",
    "ql_remarks": "",
    "debug": False,
}

plugin_config = form(
    {
        "enable": form.boolean().title("是否启用").default(True),
        "smallcat_id": (
            form.integer()
            .title("smallcat 编号")
            .description("后台 smallcat 页面里的编号，从 1 开始；AUTH 使用面板配置")
            .widget("smallcat-panel")
            .min(1)
            .default(1)
        ),
        "account_mode": (
            form.string()
            .title("openid 获取模式")
            .description("普通用户授权：只读取已授权本插件的账号；手动填写：按下方 openid 读取，留空读取 SmallCat 全部账号")
            .options(["authorized", "manual"])

            .default("authorized")
        ),
        "manual_openids": (
            form.string()
            .title("手动 openid")
            .description("仅手动填写模式生效；多个用逗号、空格或换行分隔；留空读取全部账号")
            .widget("textarea")
            .default("")
        ),
        "account_selector": (
            form.string()
            .title("执行账号")
            .description("留空取首个可用账号；可填序号、openid、昵称；填“全部”执行全部账号")
            .default("")
        ),
        "proxy_url": (
            form.string()
            .title("业务请求代理")
            .description("默认留空直连；仅在明确需要时填写 http/https 代理")
            .default("")
        ),
        "request_timeout": (
            form.integer().title("请求超时秒数").min(5).max(90).default(25)
        ),
        "sync_panel": (
            form.select([
                {"label": "不同步", "value": "none"},
                {"label": "同步青龙", "value": "qinglong"},
                {"label": "同步呆呆", "value": "daidai"},
            ]).title("同步目标").description("青龙/呆呆容器编号会根据后台容器列表动态渲染").default("none")
        ),
        "qinglong_id": (
            form.integer().title("青龙编号").description("后台青龙页面里的编号，从 1 开始").widget("qinglong-panel").min(1).default(1)
        ),
        "daidai_id": (
            form.integer().title("呆呆编号").description("后台呆呆页面里的编号，从 1 开始").widget("daidai-panel").min(1).default(1)
        ),
        "ql_env_name": form.string().title("环境变量名").default("MT_TOKEN"),
        "ql_remarks": (
            form.string().title("变量备注").description("留空自动使用账号名称或 userId").default("")
        ),
        "debug": form.boolean().title("调试日志").default(False),
    }
)
# 配置扫描先执行上面的 form；第三方依赖放在其后，首次安装依赖前也能导出表单。
import httpx

class _Undefined:
    pass


UNDEFINED = _Undefined()


def js_json(value: Any) -> str:
    """按 JSON.stringify 的常见输出格式生成紧凑 JSON。"""
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def js_str(value: Any) -> str:
    """模拟 JS String(value) 的常用分支，避免 Python True/None 格式和 JS 不一致。"""
    if value is UNDEFINED:
        return "undefined"
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, (dict, list, tuple)):
        if isinstance(value, dict):
            return "[object Object]"
        return ",".join(js_str(x) for x in value)
    return str(value)


def js_encode_uri_component(value: Any) -> str:
    """模拟 encodeURIComponent，保留 JS 默认安全字符 -_.!~*'()。"""
    return urllib.parse.quote(js_str(value), safe="-_.!~*'()")


def mtg_fixed_encode(value: Any) -> str:
    """jsguard.js 的 fe()：encodeURIComponent 后再转义 ! ' ( ) *。"""
    return urllib.parse.quote(js_str(value), safe="-_.~")


def bytes_from_js_uri(value: Any) -> List[int]:
    """jsguard.js 的 ce()：encodeURIComponent 后把 %XX 还原成字节。"""
    encoded = js_encode_uri_component(value)
    out: List[int] = []
    i = 0
    while i < len(encoded):
        if encoded[i] == "%":
            out.append(int(encoded[i + 1 : i + 3], 16))
            i += 3
        else:
            out.append(ord(encoded[i]))
            i += 1
    return out


def parse_query_like_js(query: str, missing_as_undefined: bool = False) -> List[List[str]]:
    """模拟 ne()：split('&') 再 split('=')，只取 split 后的第 2 段作为 value。"""
    if not query:
        return []
    result: List[List[str]] = []
    for item in query.split("&"):
        parts = item.split("=")
        if len(parts) < 1:
            continue
        key = urllib.parse.unquote(parts[0].replace("+", " "))
        if len(parts) == 1:
            result.append([key, "undefined" if missing_as_undefined else ""])
        else:
            value = urllib.parse.unquote(parts[1].replace("+", " "))
            result.append([key, value])
    return result


def push_encoded_pairs(target: List[List[str]], source: Any, object_mode: bool = False) -> None:
    """模拟 te()：把 query 数组或 data 对象转成签名前的 key/value。"""
    if object_mode:
        if not isinstance(source, MutableMapping):
            return
        for key, value in source.items():
            if value is UNDEFINED:
                target.append([mtg_fixed_encode(key), "undefined"])
            elif value is None:
                target.append([mtg_fixed_encode(key), "null"])
            elif isinstance(value, (dict, list, tuple)):
                target.append([mtg_fixed_encode(key), mtg_fixed_encode(js_json(value))])
            else:
                target.append([mtg_fixed_encode(key), mtg_fixed_encode(value)])
    else:
        for key, value in source or []:
            target.append([mtg_fixed_encode(key), mtg_fixed_encode(value)])


def parse_url_by_jsguard_regex(url: str) -> Tuple[str, str]:
    """按 jsguard.js 的 URL 正则取 path/query，保持它只签 path 不签 host。"""
    matched = re.match(
        r"^(?:([A-Za-z]+):)?(\/{0,3})([0-9.\-A-Za-z]+)(?::(\d+))?(?:\/([^?#]*))?(?:\?([^#]*))?(?:#(.*))?$",
        url or "",
    )
    path = "/"
    query = ""
    if matched:
        if matched.group(5):
            path += matched.group(5)
        if matched.group(6):
            query = matched.group(6)
    return path, query


def build_signed_request_bytes(
    method: str,
    url: str,
    data: Any = None,
    header: Optional[Dict[str, Any]] = None,
) -> Tuple[List[int], Dict[str, Any]]:
    """还原 mtgsig 的请求规范化逻辑，输出参与 ge() 的字节数组。"""
    method = (method or "GET").upper()
    header = header or {}
    path, query = parse_url_by_jsguard_regex(url or "")
    query_pairs = parse_query_like_js(query)

    signed_pairs: List[List[str]] = []
    form_body = ""

    is_form = False
    if method != "GET":
        for key, value in header.items():
            if key.lower() == "content-type" and value and str(value).lower().startswith("application/x-www-form-urlencoded"):
                is_form = True
                break

    if method == "GET":
        if isinstance(data, MutableMapping) and len(data) > 0:
            push_encoded_pairs(signed_pairs, data, object_mode=True)
            if query_pairs:
                rest: "OrderedDict[str, Any]" = OrderedDict()
                for key, value in parse_query_like_js(query, missing_as_undefined=True):
                    if key not in data:
                        rest[key] = value
                push_encoded_pairs(signed_pairs, rest, object_mode=True)
        else:
            push_encoded_pairs(signed_pairs, query_pairs, object_mode=False)
    else:
        push_encoded_pairs(signed_pairs, query_pairs, object_mode=False)
        if is_form:
            if isinstance(data, str):
                form_body = data
            elif isinstance(data, MutableMapping):
                temp = []
                for key, value in data.items():
                    temp.append(js_encode_uri_component(key) + "=" + js_encode_uri_component(value))
                form_body = "&".join(temp)

    signed_pairs.sort(key=lambda item: (item[0], item[1]))
    normalized_query = "&".join([key + "=" + value for key, value in signed_pairs])
    signed_bytes = bytes_from_js_uri(method + " " + path + " " + normalized_query)

    if (not is_form) and method != "GET" and data is not None:
        body = data if isinstance(data, str) else js_json(data)
        signed_bytes.extend(bytes_from_js_uri(body)[:16200])

    if form_body:
        signed_bytes.extend(bytes_from_js_uri(form_body)[:16200])

    debug = {
        "method": method,
        "path": path,
        "query": normalized_query,
        "is_form": is_form,
        "form_body": form_body,
        "signed_len": len(signed_bytes),
    }
    return signed_bytes, debug


def u32(value: int) -> int:
    return value & 0xFFFFFFFF


def int_to_be4(value: int) -> List[int]:
    """jsguard.js 的 ie()：uint32 转大端 4 字节。"""
    value = u32(value)
    return [(value >> 24) & 255, (value >> 16) & 255, (value >> 8) & 255, value & 255]


def hex_to_bytes_loose(hex_text: str) -> List[int]:
    """jsguard.js 的 re()：每 2 个 hex 转 1 字节；奇数长度最后 1 位也 parseInt。"""
    return [int(hex_text[i : i + 2], 16) for i in range(0, len(hex_text), 2)]


def bytes_to_hex(byte_values: Iterable[int]) -> str:
    return "".join(f"{item & 255:02x}" for item in byte_values)


def js_multiply_m(value: int) -> int:
    """模拟 JS 里 1540483477 的 32 位乘法拆半实现。"""
    value = u32(value)
    return u32(MURMUR_M * (value & 0xFFFF) + (((MURMUR_M * ((value >> 16) & 0xFFFF)) & 0xFFFF) << 16))


def mtg_hash_ge(byte_values: Sequence[int], seed: int) -> int:
    """还原 jsguard.js 的 ge()，类似 MurmurHash2 但末尾额外 xor 常量。"""
    remain = len(byte_values)
    value = u32(seed ^ remain)
    index = 0

    while remain >= 4:
        block = (
            (byte_values[index] & 255)
            | ((byte_values[index + 1] & 255) << 8)
            | ((byte_values[index + 2] & 255) << 16)
            | ((byte_values[index + 3] & 255) << 24)
        )
        block = js_multiply_m(block)
        value = u32(js_multiply_m(value) ^ js_multiply_m(block ^ (block >> 24)))
        remain -= 4
        index += 4

    if remain == 3:
        value ^= (byte_values[index + 2] & 255) << 16
    if remain >= 2:
        value ^= (byte_values[index + 1] & 255) << 8
    if remain >= 1:
        value = js_multiply_m(value ^ (byte_values[index] & 255))

    value = js_multiply_m(value ^ (value >> 13))
    return u32((value ^ (value >> 15)) ^ MURMUR_M)


def mtg_crc32_gn(byte_values: Sequence[int]) -> int:
    """还原 jsguard.js 的 Gn()：CRC32 表算法，但最终 xor 常量是 0x12477cdf。"""
    table: List[int] = []
    for item in range(256):
        value = item
        for _ in range(8):
            value = ((value >> 1) ^ 0xEDB88320) if (value & 1) else (value >> 1)
        table.append(u32(value))

    crc = 0xFFFFFFFF
    for item in byte_values:
        crc = u32(table[(crc ^ (item & 255)) & 255] ^ (crc >> 8))
    return u32(0x12477CDF ^ crc)


def md5_word_array(byte_values: Sequence[int]) -> List[int]:
    """还原 Ae.md5Array() 的结果：MD5 digest 按 little-endian 拆 4 个 uint32。"""
    digest = hashlib.md5(bytes(byte_values)).digest()
    return list(struct.unpack("<4I", digest))


def md5_hex_from_words(words: Sequence[int]) -> str:
    """还原 Ae.md5ToHex()：每个 uint32 按 little-endian 输出 hex。"""
    out: List[int] = []
    for word in words:
        word = u32(word)
        out.extend([word & 255, (word >> 8) & 255, (word >> 16) & 255, (word >> 24) & 255])
    return bytes_to_hex(out)


def mtg_custom_base64(byte_values: Sequence[int]) -> str:
    """还原 mtgsig a5 使用的自定义 Base64。"""
    result: List[str] = []
    full_len = len(byte_values) - len(byte_values) % 3
    for index in range(0, full_len, 3):
        block = ((byte_values[index] & 255) << 16) + ((byte_values[index + 1] & 255) << 8) + (byte_values[index + 2] & 255)
        result.append(
            MTG_BASE64_ALPHABET[(block >> 18) & 63]
            + MTG_BASE64_ALPHABET[(block >> 12) & 63]
            + MTG_BASE64_ALPHABET[(block >> 6) & 63]
            + MTG_BASE64_ALPHABET[block & 63]
        )

    remain = len(byte_values) - full_len
    if remain == 1:
        one = byte_values[-1] & 255
        result.append(MTG_BASE64_ALPHABET[one >> 2] + MTG_BASE64_ALPHABET[(one << 4) & 63] + "==")
    elif remain == 2:
        two = ((byte_values[-2] & 255) << 8) + (byte_values[-1] & 255)
        result.append(
            MTG_BASE64_ALPHABET[two >> 10]
            + MTG_BASE64_ALPHABET[(two >> 4) & 63]
            + MTG_BASE64_ALPHABET[(two << 2) & 63]
            + "="
        )
    return "".join(result)


def mtg_rc4_variant(key: Sequence[int], text: str) -> List[int]:
    """还原 a5 内层 RC4 变体：KSA 多加固定 31。"""
    state = list(range(256))
    j = 0
    for i in range(256):
        j = (j + state[i] + (key[i % len(key)] & 255) + 31) % 256
        state[i], state[j] = state[j], state[i]

    i = 0
    j = 0
    out: List[int] = []
    for ch in text:
        i = (i + 1) % 256
        j = (j + state[i]) % 256
        state[i], state[j] = state[j], state[i]
        out.append(ord(ch) ^ state[(state[i] + state[j]) % 256])
    return out


def build_qn(
    appid: str,
    openid: str = "",
    timestamp_ms: Optional[int] = None,
    init_timestamp_ms: Optional[int] = None,
    seq: int = 1,
    route: str = "",
    b9: str = "00102",
    b11: str = "",
    b10: Any = UNDEFINED,
    account_info: Any = UNDEFINED,
) -> "OrderedDict[str, Any]":
    """按 JS 插入顺序构造 JSON.stringify(qn) 的对象。"""
    now_ms = int(time.time() * 1000) if timestamp_ms is None else int(timestamp_ms)
    init_ms = now_ms if init_timestamp_ms is None else int(init_timestamp_ms)
    qn: "OrderedDict[str, Any]" = OrderedDict()
    qn["b7"] = init_ms // 1000
    if account_info is UNDEFINED:
        account_info = {"miniProgram": {"appId": appid or ""}}
    if account_info is not None:
        qn["b1"] = account_info
    qn["b6"] = openid or ""
    qn["b8"] = int(seq)
    qn["b12"] = appid or ""
    if b11:
        qn["b11"] = b11
    qn["b2"] = route or ""
    qn["b9"] = b9
    if b10 is not UNDEFINED:
        qn["b10"] = b10
    return qn


def build_mtgsig(
    method: str,
    url: str,
    data: Any = None,
    header: Optional[Dict[str, Any]] = None,
    *,
    appid: str = MEITUAN_APPID,
    openid: str = "",
    dfpid: str = "",
    siua: str = "",
    timestamp_ms: Optional[int] = None,
    init_timestamp_ms: Optional[int] = None,
    seq: int = 1,
    route: str = "",
    env_code: int = 119,
    b9: str = "00102",
    b11: str = "",
    b10: Any = UNDEFINED,
    account_info: Any = UNDEFINED,
) -> Tuple["OrderedDict[str, Any]", Dict[str, Any]]:
    """生成 mtgsig 对象，并返回调试信息。"""
    if timestamp_ms is None:
        timestamp_ms = int(time.time() * 1000)
    timestamp_ms = int(timestamp_ms)
    if not dfpid:
        dfpid = make_dfpid(timestamp_ms=timestamp_ms)

    request_bytes, req_debug = build_signed_request_bytes(method, url, data, header)
    qn = build_qn(
        appid=appid,
        openid=openid,
        timestamp_ms=timestamp_ms,
        init_timestamp_ms=init_timestamp_ms,
        seq=seq,
        route=route,
        b9=b9,
        b11=b11,
        b10=b10,
        account_info=account_info,
    )
    qn_text = js_json(qn)

    timestamp_low = u32(timestamp_ms)
    timestamp_bytes = int_to_be4(timestamp_low)
    md5_seed = hashlib.md5(bytes(bytes_from_js_uri(siua) + timestamp_bytes)).hexdigest()
    key_bytes = hex_to_bytes_loose(md5_seed[:15])
    key_bytes[7] = (int(env_code) ^ mtg_crc32_gn(timestamp_bytes)) & 255
    key_bytes.extend(timestamp_bytes)
    key_bytes.extend(int_to_be4(mtg_crc32_gn(key_bytes)))

    a5 = mtg_custom_base64(key_bytes + mtg_rc4_variant(key_bytes, qn_text))

    request_hash = mtg_hash_ge(request_bytes, timestamp_ms)
    a5_hash = mtg_hash_ge(bytes_from_js_uri(a5), timestamp_ms)
    a4_mix_words = [
        request_hash,
        a5_hash,
        u32(request_hash ^ timestamp_low),
        u32(request_hash ^ a5_hash ^ timestamp_low),
    ]
    a4 = bytes_to_hex(int_to_be4(request_hash) + int_to_be4(a5_hash) + hex_to_bytes_loose(md5_hex_from_words(a4_mix_words)))

    a1 = "1.2"
    x0 = 3
    d1_raw = a1 + str(timestamp_ms) + dfpid + a4 + str(u32(a5_hash)) + md5_seed + appid
    d1_words = md5_word_array(bytes_from_js_uri(d1_raw))
    rotate_like = u32((timestamp_low << x0) | (timestamp_low << (32 - x0)))
    d1_words[0] = u32(d1_words[0] ^ rotate_like)
    d1_words[1] = u32(d1_words[1] ^ a5_hash)
    d1_words[2] = u32(d1_words[2] ^ a5_hash ^ rotate_like)
    d1_words[3] = u32(d1_words[3] ^ d1_words[0])
    d1 = md5_hex_from_words(d1_words)

    mtgsig: "OrderedDict[str, Any]" = OrderedDict()
    mtgsig["a1"] = a1
    mtgsig["a2"] = timestamp_ms
    mtgsig["a3"] = dfpid
    mtgsig["a4"] = a4
    mtgsig["a5"] = a5
    mtgsig["a6"] = siua
    mtgsig["a7"] = appid
    mtgsig["x0"] = x0
    mtgsig["d1"] = d1

    debug = {
        "request": req_debug,
        "qn": qn,
        "qn_json": qn_text,
        "key_hex": bytes_to_hex(key_bytes),
        "request_hash": request_hash,
        "a5_hash": a5_hash,
        "md5_seed": md5_seed,
        "d1_raw": d1_raw,
    }
    return mtgsig, debug


def build_windows_system_object(
    *,
    model: str = "microsoft",
    brand: str = "microsoft",
    platform: str = "windows",
    system: str = "Windows Unknown x64",
    version: str = "4.1.11.24",
    sdk_version: str = "3.16.1",
    language: str = "zh_CN",
    network_type: str = "wifi",
    screen_width: int = 414,
    screen_height: int = 780,
    window_width: int = 414,
    window_height: int = 780,
    pixel_ratio: int = 1,
    scene: int = 1256,
    route: str = "index/pages/mt/mt",
) -> "OrderedDict[str, Any]":
    """构造 JSGuard 常见 Windows 小程序指纹对象，用于本地 dfpid 和 siua。"""
    return OrderedDict(
        [
            ("accelerometer", []),
            ("albumAuthorized", True),
            ("BatteryInfo", OrderedDict([("errMsg", "getBatteryInfo:ok"), ("isCharging", True), ("level", 100)])),
            ("batteryLevel", None),
            ("Beacons", None),
            ("benchmarkLevel", -1),
            ("bluetoothEnabled", False),
            ("brand", brand),
            ("brightness", 0.5),
            ("cameraAuthorized", True),
            ("compass", []),
            ("deviceOrientation", None),
            ("devicePixelRatio", pixel_ratio),
            ("enableDebug", False),
            ("errMsg", "getSystemInfo:ok"),
            ("fontSizeSetting", None),
            ("language", language),
            ("LaunchOptionsSync", OrderedDict([("path", route), ("scene", scene)])),
            ("locationAuthorized", True),
            ("locationEnabled", True),
            ("locationReducedAccuracy", None),
            ("microphoneAuthorized", True),
            ("model", model),
            ("networkType", network_type),
            ("notificationAlertAuthorized", None),
            ("notificationAuthorized", True),
            ("notificationBadgeAuthorized", None),
            ("notificationSoundAuthorized", None),
            ("pixelRatio", pixel_ratio),
            ("platform", platform),
            ("safeArea", OrderedDict([("left", 0), ("right", screen_width), ("top", 0), ("bottom", screen_height), ("width", screen_width), ("height", screen_height)])),
            ("screenHeight", screen_height),
            ("screenTop", None),
            ("screenWidth", screen_width),
            ("SDKVersion", sdk_version),
            ("statusBarHeight", 20),
            ("system", system),
            ("version", version),
            ("wifiEnabled", True),
            ("WifiInfo", None),
            ("windowHeight", window_height),
            ("windowWidth", window_width),
            ("screenRecord", None),
            ("isPrivacy", 1),
            ("hasSystemProxy", -1),
            ("captureRecord", "[]"),
        ]
    )


def make_jsguard_random_letters() -> str:
    """按 JSGuard 里 An() 的 Math.random 表达式生成 7 位本地随机大写串。"""
    letters: List[str] = []
    for _ in range(7):
        letters.append(chr(random.randrange(25) | ord("A")))
    return "".join(letters)


def make_local_dfpid(
    timestamp_ms: Optional[int] = None,
    *,
    openid: str = "",
    system_object: Optional["OrderedDict[str, Any]"] = None,
    random_letters: Optional[str] = None,
) -> str:
    """纯算法生成 JSGuard 本地 dfpid/localId，对应 jsguard.js 的 An()。"""
    now_ms = int(time.time() * 1000) if timestamp_ms is None else int(timestamp_ms)
    timestamp_sec = round(now_ms / 1000)
    if random_letters is None:
        random_letters = make_jsguard_random_letters()
    else:
        random_letters = (random_letters.upper() + "AAAAAAA")[:7]
    if system_object is None:
        system_object = build_windows_system_object()

    md5_input = OrderedDict(
        [
            ("model", system_object.get("model")),
            ("system", system_object),
            ("timestamp", timestamp_sec),
            ("openid", openid or ""),
        ]
    )
    digest = hashlib.md5(js_json(md5_input).encode("utf-8")).hexdigest()
    base = f"{now_ms}{random_letters}{digest}"
    crc_prefix = str(zlib.crc32(base.encode("utf-8")) & 0xFFFFFFFF)[:4]
    return base + crc_prefix


def make_dfpid(
    timestamp_ms: Optional[int] = None,
    seed: str = "PYMTGSIG",
    *,
    openid: str = "",
    system_object: Optional["OrderedDict[str, Any]"] = None,
) -> str:
    """兼容旧调用名；现在返回 JSGuard An() 风格的纯算法本地 dfpid。"""
    letters = (seed.upper().replace("_", "") + "AAAAAAA")[:7]
    return make_local_dfpid(timestamp_ms=timestamp_ms, openid=openid, system_object=system_object, random_letters=letters)


def make_session_id(platform: str = "windows", mmp: bool = False) -> str:
    """纯算法生成 JSGuard sessionId，对应 Ze.getSessionId()。"""
    hex_chars = list("0123456789abcdef")
    values = [secrets.choice(hex_chars) for _ in range(36)]
    values[14] = "4"
    values[19] = hex_chars[(int(values[19], 16) & 3) | 8]
    values[8] = values[13] = values[18] = values[23] = ""
    raw_uuid32 = "".join(values)
    if mmp:
        return raw_uuid32 + "55"
    platform_index = {
        "android": 0,
        "ios": 1,
        "devtools": 2,
        "windows": 3,
        "mac": 4,
        "ohos": 5,
    }.get((platform or "").lower(), 9)
    return raw_uuid32 + "0" + str(platform_index)


def aes_cbc_pkcs7_encrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
    """AES-CBC-PKCS7 加密；优先用 pycryptodome，缺失时回退 cryptography。"""
    pad_len = 16 - (len(data) % 16)
    padded = data + bytes([pad_len]) * pad_len
    try:
        from Crypto.Cipher import AES  # type: ignore

        return AES.new(key, AES.MODE_CBC, iv).encrypt(padded)
    except Exception:
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes  # type: ignore

        encryptor = Cipher(algorithms.AES(key), modes.CBC(iv)).encryptor()
        return encryptor.update(padded) + encryptor.finalize()


def build_dfp_system_array(system_object: "OrderedDict[str, Any]") -> List[Any]:
    """按 vt.system 固定字段顺序，把 system 对象压成 siua 里的数组结构。"""
    fields = [
        "accelerometer", "albumAuthorized", "BatteryInfo", "batteryLevel", "Beacons",
        "benchmarkLevel", "bluetoothEnabled", "brand", "brightness", "cameraAuthorized",
        "compass", "deviceOrientation", "devicePixelRatio", "enableDebug", "errMsg",
        "fontSizeSetting", "language", "LaunchOptionsSync", "locationAuthorized",
        "locationEnabled", "locationReducedAccuracy", "microphoneAuthorized", "model",
        "networkType", "notificationAlertAuthorized", "notificationAuthorized",
        "notificationBadgeAuthorized", "notificationSoundAuthorized", "pixelRatio",
        "platform", "safeArea", "screenHeight", "screenTop", "screenWidth", "SDKVersion",
        "statusBarHeight", "system", "version", "wifiEnabled", "WifiInfo", "windowHeight",
        "windowWidth", "screenRecord", "isPrivacy", "hasSystemProxy", "captureRecord",
    ]
    battery_fields = ["errMsg", "isCharging", "level"]
    safe_area_fields = ["left", "right", "top", "bottom", "width", "height"]
    wifi_fields = ["SSID", "BSSID", "autoJoined", "signalStrength", "justJoined", "secure", "frequency"]

    result: List[Any] = []
    for field in fields:
        value = system_object.get(field)
        if isinstance(value, str) and field in {"BatteryInfo", "safeArea", "WifiInfo", "LaunchOptionsSync"}:
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                pass
        if field == "LaunchOptionsSync" and isinstance(value, MutableMapping):
            result.append(js_json(OrderedDict([("path", value.get("path")), ("scene", value.get("scene"))])))
        elif field == "BatteryInfo" and isinstance(value, MutableMapping):
            result.append([value.get(item) for item in battery_fields])
        elif field == "safeArea" and isinstance(value, MutableMapping):
            result.append([value.get(item) for item in safe_area_fields])
        elif field == "WifiInfo" and isinstance(value, MutableMapping):
            result.append([value.get(item) for item in wifi_fields])
        else:
            result.append(value)
    return result


def build_siua(
    *,
    appid: str = MEITUAN_APPID,
    openid: str = "",
    dfpid: str = "",
    localid: str = "",
    filetime_ms: Optional[int] = None,
    timestamp_ms: Optional[int] = None,
    session_id: str = "",
    route: str = "index/pages/mt/mt",
    scene: int = 1256,
    platform: str = "windows",
    ext: Optional[List[Any]] = None,
    system_object: Optional["OrderedDict[str, Any]"] = None,
) -> str:
    """生成 a6/siua：w1.6 + AES-CBC(gzip(JSON数组))。"""
    now_ms = int(time.time() * 1000) if timestamp_ms is None else int(timestamp_ms)
    if filetime_ms is None:
        filetime_ms = now_ms
    if system_object is None:
        system_object = build_windows_system_object(route=route, scene=scene, platform=platform)
    if not localid:
        localid = make_local_dfpid(timestamp_ms=filetime_ms, openid=openid, system_object=system_object)
    if not dfpid:
        dfpid = localid
    if not session_id:
        session_id = make_session_id(platform=platform)
    if ext is None:
        ext = [0, 1, 2, 0, 4]
    system_array = build_dfp_system_array(system_object)

    plain_array = [
        appid,
        dfpid,
        int(filetime_ms),
        "2.5.0",
        localid,
        system_array,
        round(now_ms / 1000),
        ext,
        session_id,
    ]
    plain = js_json(plain_array).encode("utf-8")
    gz = gzip.compress(plain, compresslevel=6, mtime=now_ms // 1000)
    encrypted = aes_cbc_pkcs7_encrypt(gz, b"z7Jut6Ywr2Pe5Nhx", b"0807060504030201")
    return "w1.6" + base64.b64encode(encrypted).decode("ascii")


def build_pure_identity(
    *,
    appid: str = MEITUAN_APPID,
    openid: str = "",
    timestamp_ms: Optional[int] = None,
    filetime_ms: Optional[int] = None,
    route: str = "index/pages/mt/mt",
    scene: int = 1256,
    platform: str = "windows",
    random_letters: Optional[str] = None,
    session_id: str = "",
) -> "OrderedDict[str, Any]":
    """一次性生成纯本地 dfpid/localId/sessionId/siua，避免 dfpid 和 siua 不一致。"""
    now_ms = int(time.time() * 1000) if timestamp_ms is None else int(timestamp_ms)
    file_ms = now_ms if filetime_ms is None else int(filetime_ms)
    system_object = build_windows_system_object(route=route, scene=scene, platform=platform)
    localid = make_local_dfpid(
        timestamp_ms=file_ms,
        openid=openid,
        system_object=system_object,
        random_letters=random_letters,
    )
    sid = session_id or make_session_id(platform=platform)
    siua = build_siua(
        appid=appid,
        openid=openid,
        dfpid=localid,
        localid=localid,
        filetime_ms=file_ms,
        timestamp_ms=now_ms,
        session_id=sid,
        route=route,
        scene=scene,
        platform=platform,
        system_object=system_object,
    )
    return OrderedDict(
        [
            ("dfpid", localid),
            ("localid", localid),
            ("filetime_ms", file_ms),
            ("timestamp_ms", now_ms),
            ("session_id", sid),
            ("siua", siua),
            ("system_object", system_object),
        ]
    )




# ============================== SillyGirl 适配层 ==============================


def clean_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def compact_json(value: Any, limit: int = 500) -> str:
    try:
        text = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    except Exception:
        text = str(value)
    return text if len(text) <= limit else text[:limit] + "..."


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
        return clean_text(value)
    for key in ("message", "msg", "errmsg", "errMsg", "error"):
        item = value.get(key)
        if item not in (None, "", False):
            return clean_text(item if not isinstance(item, (dict, list)) else compact_json(item, 400))
    nested = value.get("data")
    return response_message(nested) if nested is not None and nested is not value else ""


def smallcat_error(payload: Any) -> str:
    value = decode_json_tree(payload)
    if not isinstance(value, dict):
        return response_message(value)
    outer = ""
    for key in ("message", "msg", "errmsg", "errMsg", "error"):
        if value.get(key):
            outer = clean_text(value[key] if not isinstance(value[key], (dict, list)) else compact_json(value[key], 400))
            break
    nested = response_message(value.get("data")) if "data" in value else ""
    if outer and nested and nested != outer:
        return outer + "：" + nested
    return outer or nested or "SmallCat 接口返回失败状态"


def unwrap_smallcat(payload: Any) -> Any:
    value = decode_json_tree(payload)
    if not isinstance(value, dict):
        return value
    if "status" in value:
        if value.get("status") is False:
            raise RuntimeError(smallcat_error(value))
        if "data" in value:
            return decode_json_tree(value["data"])
    if "code" in value and "data" in value and str(value.get("code")) in {"0", "200", "201"}:
        return decode_json_tree(value["data"])
    return value


def find_deep_value(value: Any, keys: Sequence[str], pattern: str = "", depth: int = 0) -> str:
    if depth > 12 or value is None:
        return ""
    decoded = decode_json_strings(value, depth)
    if decoded is not value:
        return find_deep_value(decoded, keys, pattern, depth + 1)
    expected = {key.lower() for key in keys}
    if isinstance(value, dict):
        for key, item in value.items():
            if str(key).lower() not in expected or isinstance(item, (dict, list)) or item is None:
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


def normalize_config(raw: Any) -> Dict[str, Any]:
    source = raw if isinstance(raw, dict) else {}
    config = dict(DEFAULTS)
    config.update(source)
    config["enable"] = True if "enable" not in source else as_bool(source.get("enable"))
    config["smallcat_id"] = positive_int(config.get("smallcat_id"), 1)
    config["account_mode"] = "manual" if config.get("account_mode") == "manual" else "authorized"
    config["manual_openids"] = str(config.get("manual_openids") or "").strip()
    config["account_selector"] = str(config.get("account_selector") or "").strip()
    config["proxy_url"] = str(config.get("proxy_url") or "").strip()
    config["request_timeout"] = max(5, min(positive_int(config.get("request_timeout"), 25), 90))
    raw_sync_panel = str(config.get("sync_panel") or "").strip()
    config["sync_panel"] = raw_sync_panel if raw_sync_panel in {"none", "qinglong", "daidai"} else ("qinglong" if as_bool(config.get("sync_qinglong")) else "none")
    config["sync_qinglong"] = config["sync_panel"] == "qinglong"
    config["qinglong_id"] = positive_int(config.get("qinglong_id"), 1)
    config["daidai_id"] = positive_int(config.get("daidai_id"), 1)
    config["ql_env_name"] = str(config.get("ql_env_name") or "MT_TOKEN").strip() or "MT_TOKEN"
    config["ql_remarks"] = clean_text(config.get("ql_remarks"))
    config["debug"] = as_bool(config.get("debug"))
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]{0,63}", config["ql_env_name"]):
        raise RuntimeError("环境变量名格式异常")
    return config


def parse_command(content: str) -> Dict[str, str]:
    matched = re.fullmatch(
        r"\s*(?:美团|meituan)\s*(?:登录|取token)?\s*([^\s]+)?\s*",
        str(content or ""),
        re.IGNORECASE,
    )
    if not matched:
        raise RuntimeError("命令格式：美团，或 美团登录 CODE")
    code = str(matched.group(1) or "").strip()
    if len(code) > 4096:
        raise RuntimeError("CODE 长度异常")
    return {"code": code}


def normalize_accounts(payload: Any) -> List[Dict[str, Any]]:
    value = unwrap_smallcat(payload)
    if isinstance(value, dict):
        value = value.get("accounts") or value.get("items") or value.get("list") or value.get("value") or value.get("data")
    if isinstance(value, dict):
        value = value.get("items") or value.get("list") or value.get("data")
    accounts: List[Dict[str, Any]] = []
    for item in value if isinstance(value, list) else []:
        if not isinstance(item, dict):
            continue
        account = dict(item)
        account["openid"] = str(item.get("openid") or item.get("openId") or item.get("userKey") or "").strip()
        account["disabled"] = as_bool(item.get("disabled"))
        if account["openid"]:
            accounts.append(account)
    return accounts


def split_openids(value: Any) -> set[str]:
    return {item for item in re.split(r"[,，;；\s]+", str(value or "")) if item}


async def load_smallcat_accounts(smallcat: SmallCat, config: Dict[str, Any]) -> List[Dict[str, Any]]:
    wanted = split_openids(config["manual_openids"]) if config["account_mode"] == "manual" else await authorized_openids()
    payload = await smallcat.request("GET", "/api/accounts")
    accounts = normalize_accounts(payload)
    return [account for account in accounts if account["openid"] in wanted] if wanted else accounts


async def authorized_openids() -> set[str]:
    users = await utils.userList()
    allowed: set[str] = set()
    for user in users if isinstance(users, list) else []:
        if not isinstance(user, dict) or user.get("disabled") or not user.get("authorized"):
            continue
        bindings = user.get("bindings") if isinstance(user.get("bindings"), dict) else {}
        for openid in bindings.get("smallcat_openids") or []:
            value = str(openid or "").strip()
            if value:
                allowed.add(value)
    if not allowed:
        raise RuntimeError("没有普通用户授权的 SmallCat 账号")
    return allowed


def select_accounts(accounts: List[Dict[str, Any]], selector: str) -> List[Dict[str, Any]]:
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
    expected = text.lower()
    for account in enabled:
        values = (
            account.get("openid"), account.get("displayName"), account.get("nickname"),
            account.get("name"), account.get("remark"),
        )
        if any(str(value or "").strip().lower() == expected for value in values):
            return [account]
    raise RuntimeError(f"SmallCat 未找到账号：{text}")


def account_name(account: Dict[str, Any]) -> str:
    return str(
        account.get("displayName") or account.get("nickname") or account.get("name")
        or account.get("remark") or account.get("openid") or "账号"
    ).strip()


def _login_params() -> "OrderedDict[str, Any]":
    return OrderedDict(
        [
            ("sdkVersion", "4.1.11.24"),
            ("utm_medium", "windows"),
            ("sdkType", "wxmp"),
            ("login_sdk_version", "6.18.4"),
            ("appName", "group"),
            ("risk_app", "214"),
            ("risk_partner", "0"),
            ("risk_platform", "13"),
            ("risk_smsPrefixId", "0"),
            ("risk_smsTemplateId", "0"),
            ("version_name", "10.26.1"),
        ]
    )


async def get_wx_code(smallcat: SmallCat, openid: str) -> str:
    raw = await smallcat.getCode({"openid": openid, "appid": MEITUAN_APPID})
    try:
        payload = unwrap_smallcat(raw)
    except Exception as exc:
        raise RuntimeError(f"SmallCat wx.login 取码失败：{exc}") from exc
    code = find_deep_value(payload, ("code", "wxcode", "wx_code", "loginCode"), r"[0-9A-Za-z_-]{8,4096}")
    if not code:
        raise RuntimeError("SmallCat wx.login 响应缺少 code：" + compact_json(raw, 600))
    return code


def build_login_request(code: str) -> Tuple[str, bytes, Dict[str, str], Dict[str, Any]]:
    params = _login_params()
    payload: "OrderedDict[str, Any]" = OrderedDict(
        [("code", code), ("device_type", "microsoft"), ("device_os", "微信小程序")]
    )
    full_url = LOGIN_URL + "?" + urllib.parse.urlencode(params)
    identity = build_pure_identity(appid=MEITUAN_APPID, route="index/pages/mt/mt", scene=1256)
    sign_header = OrderedDict([("content-type", "application/x-www-form-urlencoded")])
    mtgsig, debug = build_mtgsig(
        "POST", full_url, payload, sign_header,
        appid=MEITUAN_APPID, openid="",
        dfpid=identity["dfpid"], siua=identity["siua"],
        timestamp_ms=identity["timestamp_ms"], init_timestamp_ms=identity["filetime_ms"],
        seq=1, route="index/pages/mt/mt", env_code=119, b9="00102", b11="",
    )
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI "
            "MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) "
            "UnifiedPCWindowsWechat(0xf2541b18) XWEB/20005"
        ),
        "Content-Type": "application/x-www-form-urlencoded",
        "mtgsig": js_json(mtgsig),
        "Referer": f"https://servicewechat.com/{MEITUAN_APPID}/1555/page-frame.html",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }
    body = urllib.parse.urlencode(payload).encode("utf-8")
    return full_url, body, headers, {"identity": identity, "signature": debug}


def create_http_client(proxy_url: str, timeout: int):
    options: Dict[str, Any] = {"timeout": float(timeout), "verify": False}
    if proxy_url:
        options["proxy"] = proxy_url
    try:
        return httpx.AsyncClient(**options)
    except TypeError:
        proxy = options.pop("proxy", "")
        if proxy:
            options["proxies"] = proxy
        return httpx.AsyncClient(**options)


async def meituan_code_login(code: str, proxy_url: str = "", timeout: int = 25, debug_enabled: bool = False) -> Dict[str, Any]:
    full_url, body, headers, debug = build_login_request(code)
    try:
        async with create_http_client(proxy_url.strip(), timeout) as client:
            response = await client.post(full_url, content=body, headers=headers)
    except Exception as exc:
        return {"ok": False, "stage": "weappsilentlogin", "error": f"登录请求异常：{exc}"}
    try:
        data = response.json()
    except Exception:
        return {
            "ok": False,
            "stage": "weappsilentlogin",
            "error": f"登录返回非 JSON：HTTP {response.status_code} {clean_text(response.text)[:240]}",
        }
    if not isinstance(data, dict):
        return {"ok": False, "stage": "weappsilentlogin", "error": "登录响应不是 JSON 对象：" + compact_json(data, 300)}
    inner = data.get("data") if isinstance(data.get("data"), dict) else {}
    user_id = inner.get("userId")
    token = str(inner.get("token") or "").strip()
    open_id = str(data.get("openId") or "").strip()
    union_id = str(data.get("unionId") or "").strip()
    if not token:
        message = data.get("msg") or data.get("message")
        if not message and open_id:
            message = "已返回 openId/unionId，但未下发 token；通常为当前出口网络触发限制，默认应保持直连"
        result = {
            "ok": False,
            "stage": "weappsilentlogin",
            "error": clean_text(message) or compact_json(data, 500),
            "openId": open_id,
            "unionId": union_id,
            "raw": data,
        }
        if debug_enabled:
            result["debug"] = {"http_status": response.status_code, **debug["signature"]}
        return result
    result = {
        "ok": True,
        "stage": "meituan",
        "userId": user_id,
        "token": token,
        "mtToken": token,
        "openId": open_id,
        "unionId": union_id,
        "account": str(user_id or open_id),
        "cookie": token,
        "code": code,
    }
    if debug_enabled:
        result["debug"] = {"http_status": response.status_code, **debug["signature"]}
    return result


def env_items(payload: Any) -> List[Dict[str, Any]]:
    value = decode_json_tree(payload)
    if isinstance(value, dict):
        value = value.get("data", value)
    if isinstance(value, dict):
        value = value.get("items") or value.get("list") or value.get("data") or []
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


async def sync_panel_env(config: Dict[str, Any], result: Dict[str, Any], label: str) -> str:
    if config["sync_panel"] == "daidai":
        return await sync_env(config, ct.DaiDai({"id": config["daidai_id"]}), result, label)
    return await sync_env(config, ct.QingLong({"id": config["qinglong_id"]}), result, label)


async def sync_env(config: Dict[str, Any], panel: Any, result: Dict[str, Any], label: str) -> str:
    env_name = config["ql_env_name"]
    query = env_name if config["sync_panel"] == "daidai" else {"searchValue": env_name}
    envs = [item for item in env_items(await panel.getEnvs(query)) if str(item.get("name") or "") == env_name]
    identity = str(result.get("userId") or result.get("openId") or "").strip()
    remark = config["ql_remarks"] or label or identity or "美团Code登录"
    existing = None
    for item in envs:
        old_remark = str(item.get("remarks") or item.get("remark") or "")
        if old_remark == remark or (identity and identity in old_remark):
            existing = item
            break
    env = {"name": env_name, "value": result["token"], "remarks": remark}
    if existing:
        env_id = existing.get("id") if existing.get("id") is not None else existing.get("_id")
        if env_id in (None, ""):
            raise RuntimeError(f"已有{sync_panel_label(config)}变量缺少 id/_id")
        env["id"] = env_id
        await panel.updateEnv(env)
        try:
            if config["sync_panel"] == "daidai":
                await panel.enableEnv(env_id)
            else:
                await panel.enableEnvs([env_id])
        except Exception:
            pass
        return "已更新"
    await panel.createEnv(env)
    return "已创建"


def sync_panel_label(config: Dict[str, Any]) -> str:
    return "呆呆" if config.get("sync_panel") == "daidai" else "青龙"


def mask_identifier(value: Any, keep: int = 5) -> str:
    text = str(value or "")
    if len(text) <= keep * 2:
        return text
    return text[:keep] + "***" + text[-keep:]


async def run_account(smallcat: SmallCat, account: Dict[str, Any], config: Dict[str, Any]) -> str:
    label = account_name(account)
    lines = [f"[INFO] ▶ 账号：{label}"]
    try:
        code = await get_wx_code(smallcat, str(account.get("openid") or ""))
        lines.append(f"[SUCCESS] {label}：wx.login code 获取成功")
        result = await meituan_code_login(code, config["proxy_url"], config["request_timeout"], config["debug"])
        if not result.get("ok"):
            raise RuntimeError(str(result.get("error") or "美团登录失败"))
        lines.append(f"[SUCCESS] {label}：美团登录成功，userId={result.get('userId') or '未知'}")
        if result.get("openId"):
            lines.append("openId：" + mask_identifier(result["openId"]))
        lines.append("MT_TOKEN：" + str(result["token"]))
        if config["sync_panel"] != "none":
            try:
                action = await sync_panel_env(config, result, label)
                lines.append(f"[SUCCESS] {sync_panel_label(config)}：{action} {config['ql_env_name']}")
            except Exception as exc:
                lines.append(f"[WARNING] {sync_panel_label(config)}同步失败：{exc}")
        if config["debug"]:
            signature = result.get("debug") or {}
            lines.append("[DEBUG] signed_len=" + str((signature.get("request") or {}).get("signed_len", "")))
        lines.append("结果：成功")
    except Exception as exc:
        lines.append(f"[ERROR] 执行异常：{exc}")
        lines.append(f"结果：失败 | {exc}")
    return "\n".join(lines)


async def run_direct_code(code: str, config: Dict[str, Any]) -> str:
    lines = ["[INFO] ▶ CODE 来源：命令参数"]
    result = await meituan_code_login(code, config["proxy_url"], config["request_timeout"], config["debug"])
    if not result.get("ok"):
        return "\n".join([*lines, f"[ERROR] 美团登录失败：{result.get('error')}", f"结果：失败 | {result.get('error')}"])
    lines.append(f"[SUCCESS] 美团登录成功，userId={result.get('userId') or '未知'}")
    lines.append("MT_TOKEN：" + str(result["token"]))
    if config["sync_panel"] != "none":
        try:
            action = await sync_panel_env(config, result, str(result.get("account") or "命令参数"))
            lines.append(f"[SUCCESS] {sync_panel_label(config)}：{action} {config['ql_env_name']}")
        except Exception as exc:
            lines.append(f"[WARNING] {sync_panel_label(config)}同步失败：{exc}")
    lines.append("结果：成功")
    return "\n".join(lines)


async def main() -> None:
    if not await s.isAdmin():
        await s.reply("仅管理员可用")
        return
    config = normalize_config(await plugin_config.get())
    if not config["enable"]:
        await s.reply("美团Code登录插件未启用")
        return
    try:
        command = parse_command(str(await s.getContent() or ""))
        if command["code"]:
            await s.reply("美团 CODE 登录开始（来源：命令参数）")
            await s.reply(await run_direct_code(command["code"], config))
            return
        smallcat = ct.SmallCat({"id": config["smallcat_id"]})
        accounts = select_accounts(await load_smallcat_accounts(smallcat, config), config["account_selector"])
        await s.reply(f"美团 CODE 登录开始：SmallCat #{config['smallcat_id']}，账号 {len(accounts)} 个")
        outputs = []
        for account in accounts:
            outputs.append(await run_account(smallcat, account, config))
        await s.reply("\n\n".join(outputs))
    except Exception as exc:
        await s.reply("美团Code登录执行失败：" + str(exc))


if os.environ.get("MEITUAN_PLUGIN_TEST") != "1":
    asyncio.run(main())
