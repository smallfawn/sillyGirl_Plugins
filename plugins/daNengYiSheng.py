# [title: 达能益生]
# [name: daNengYiSheng]
# [language: python]
# [class: 任务]
# [author: sillyGirl]
# [version: v1.0.1]
# [public: true]
# [admin: false]
# [rule: raw ^\s*(达能登录|达能登陆|登录达能|登陆达能|达能查询|查询达能|达能管理|管理达能|达能教程|达能一键运行)\s*$]
# [cron: 12 8,20 * * *]
# [priority: 20]
# [icon: https://api.iconify.design/lucide:bot.svg]
# [description: 达能益生账号绑定、查询、管理和每日任务]
# [depe: ["requests"]]

from __future__ import annotations

import asyncio
import json
import random
import time
from datetime import datetime
from typing import Any

import requests
from sillygirl import Bucket, form, sender as s

try:
    import ast as _sg_ast
except Exception:
    _sg_ast = None
try:
    import decimal as decimal
except Exception:
    decimal = None


BUCKET_USER = "S_DNYS_USER"
BUCKET_TOKEN = "S_DNYS_TOKEN"

DEFAULTS = {
    "enable": True,
    "cron_run": True,
    "verify_on_bind": True,
    "force_new_challenge": True,
    "request_timeout": 10,
}

plugin_config = form(
    {
        "enable": form.boolean().title("是否启用").default(True),
        "cron_run": form.boolean().title("定时自动运行").description("cron 触发时自动运行全部绑定账号").default(True),
        "verify_on_bind": form.boolean().title("绑定时校验账号").description("关闭后不请求接口校验，直接保存账号").default(True),
        "force_new_challenge": form.boolean().title("自动开启新挑战").description("运行任务时尝试开启/刷新挑战").default(True),
        "request_timeout": form.integer().title("请求超时秒数").min(3).max(60).default(10),
    }
)


def normalize_config(raw: Any) -> dict[str, Any]:
    cfg = dict(DEFAULTS)
    if isinstance(raw, dict):
        cfg.update(raw)
    cfg["enable"] = bool(cfg.get("enable", True))
    cfg["cron_run"] = bool(cfg.get("cron_run", True))
    cfg["verify_on_bind"] = bool(cfg.get("verify_on_bind", True))
    cfg["force_new_challenge"] = bool(cfg.get("force_new_challenge", True))
    try:
        cfg["request_timeout"] = max(3, min(60, int(cfg.get("request_timeout") or 10)))
    except Exception:
        cfg["request_timeout"] = 10
    return cfg


class DNYX:
    def __init__(self, remark: str, token: str, open_id: str, union_id: str, cfg: dict[str, Any]):
        self.session = requests.Session()
        self.base_url = "https://api.digital4danone.com.cn"
        self.remark = remark
        self.token = token
        self.openId = open_id
        self.unionId = union_id
        self.ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        self.current_task_date = None
        self.force_new_challenge = bool(cfg.get("force_new_challenge", True))
        self.timeout = int(cfg.get("request_timeout", 10))

    def get_headers(self) -> dict[str, str]:
        return {
            "User-Agent": self.ua,
            "mini-path": "%2Fpages%2Fmine%2Fmine",
            "source": "wechat_default",
            "Content-Type": "application/json",
            "sdk": "3.3.5",
            "xweb_xhr": "1",
            "privacySource": "base",
            "platform": "wechat",
            "X-Access-Token": self.token,
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://servicewechat.com/wx28fabbff88261f5f/93/page-frame.html",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }

    def common_get(self, path: str) -> dict[str, Any]:
        response = self.session.get(f"{self.base_url}{path}", headers=self.get_headers(), timeout=self.timeout)
        return response.json()

    def common_post(self, path: str, data: Any | None = None) -> dict[str, Any]:
        response = self.session.post(
            f"{self.base_url}{path}",
            headers=self.get_headers(),
            data=json.dumps(data) if data is not None else None,
            timeout=self.timeout,
        )
        return response.json()

    def open_new_challenge(self) -> tuple[bool, str]:
        headers = self.get_headers()
        headers.update(
            {
                "mini-path": "%2Fpages%2Fchallenge3%2Fchallenge3",
                "sdk": "3.8.9",
                "Referer": "https://servicewechat.com/wx28fabbff88261f5f/91/page-frame.html",
            }
        )
        try:
            response = self.session.post(
                f"{self.base_url}/healthyaging/danone/wx/ha/selfcare/openChallenge",
                headers=headers,
                data=json.dumps({}),
                timeout=self.timeout,
            )
            result = response.json()
            if result.get("code") == 200:
                return True, "✅ 已成功开启新一轮挑战"
            return False, f"⚠️ 开启挑战失败: {result.get('message', '未知错误')}"
        except Exception as exc:
            return False, f"❌ 开启新一轮挑战异常: {exc}"

    def execute_task(self, rule_id: Any, task_id: Any, task_name: str = "", rule_ids: list[Any] | None = None, task_data_value: Any = None) -> tuple[bool, str]:
        payload = {
            "ruleIds": rule_ids or [rule_id],
            "taskDataCode": "Auto",
            "taskDataValue": task_data_value,
            "userTaskDetailId": task_id,
        }
        try:
            res = self.common_post("/healthyaging/danone/wx/clockin/clickIn", payload)
            if res.get("code") == 200:
                return True, f"✅ 执行 {task_name or '任务'} 成功"
            return False, f"⚠️ 执行 {task_name or '任务'} 失败: {res.get('message', '未知错误')}"
        except Exception as exc:
            return False, f"❌ 执行 {task_name or '任务'} 异常: {exc}"

    def execute_task_by_type(self, task: dict[str, Any]) -> tuple[bool, str]:
        try:
            rule_ids: list[Any] = []
            task_data_value = None
            view_code = task.get("viewCode")
            option_list = task.get("optionList") or []
            rule_list = task.get("ruleList") or []

            if view_code == "PICKER":
                opt = next((o for o in option_list if o.get("checkinStatus") == 1), None)
                if opt:
                    rule_ids = [opt.get("id")]
                    task_data_value = opt.get("name")
            elif view_code == "WATER":
                if option_list:
                    opt = option_list[-1]
                    rule_ids = [opt.get("id")]
                    task_data_value = opt.get("name")
            elif view_code == "MULTI":
                opts = [o for o in option_list if o.get("checkinStatus") == 1]
                if opts:
                    rule_ids = [o.get("id") for o in opts]
                    task_data_value = ",".join(str(o.get("name", "")) for o in opts)
            elif rule_list and rule_list[0].get("id"):
                rule_ids = [rule_list[0].get("id")]
            else:
                rule_ids = [task.get("id")]

            rule_ids = [x for x in rule_ids if x]
            if not rule_ids:
                rule_ids = [task.get("id")]

            return self.execute_task(
                rule_id=rule_ids[0],
                task_id=task.get("userTaskDetailId"),
                task_name=task.get("simpleName", ""),
                rule_ids=rule_ids,
                task_data_value=task_data_value,
            )
        except Exception as exc:
            return False, f"❌ 执行 {task.get('simpleName', '任务')} 异常: {exc}"

    def get_user_tasks(self) -> list[str]:
        retry_count = 0
        results: list[str] = []
        while retry_count < 2:
            try:
                res = self.common_get("/healthyaging/danone/wx/ha/selfcare/getCalendar")
                should_open = self.force_new_challenge
                if res.get("code") == 200 and res.get("result", {}).get("taskCalendarList"):
                    task_list = res["result"]["taskCalendarList"]
                    today_task = next((t for t in task_list if t.get("istoday")), None)
                    if today_task:
                        self.current_task_date = today_task.get("taskDate")
                        results.append(f"✅ 获取 {self.current_task_date} 任务成功")
                        has_unfinished = False
                        for task in today_task.get("taskDetailsVoList") or []:
                            if task.get("status") == 1:
                                _, msg = self.execute_task_by_type(task)
                                results.append(msg)
                                time.sleep(random.uniform(1.0, 2.0))
                                has_unfinished = True
                            else:
                                results.append(f"✅ 已完成 {task.get('simpleName', '')}")
                        should_open = should_open or bool(today_task.get("istoday") and has_unfinished)
                    else:
                        results.append("🔍 今日无可用任务")
                else:
                    results.append("🔍 今日无可用任务")

                if should_open:
                    time.sleep(1.5)
                    success, msg = self.open_new_challenge()
                    results.append(msg)
                    if success:
                        retry_count += 1
                        time.sleep(1.0)
                        continue
                break
            except Exception as exc:
                results.append(f"❌ 任务获取异常: {exc}")
                break
        return results

    def report_event(self) -> tuple[bool, str]:
        payload = {
            "content": "挑战页-浏览",
            "name": "maievent-page-view",
            "type": "view",
            "mobile": "",
            "openId": self.openId,
            "unionId": self.unionId,
            "page": "/pages/challenge3/challenge3",
            "source": "wechat-default",
            "sdk": "ha-default",
        }
        try:
            res = self.common_post("/healthyaging/danone/wx/config/eventReport", payload)
            if res.get("code") == 200:
                return True, "✅ 事件上报成功"
            return False, f"⚠️ 事件上报失败: {res.get('message', '未知错误')}"
        except Exception as exc:
            return False, f"❌ 事件上报异常: {exc}"

    def get_challenge_id(self) -> Any:
        res = self.common_get("/healthyaging/danone/wx/ha/selfcare/getCalendar")
        return res.get("result", {}).get("lastChallengeId")

    def submit_question(self, data: dict[str, Any], title: str) -> tuple[bool, str]:
        res = self.common_post("/healthyaging/danone/wx/ha/csq/submit", data)
        if res.get("code") != 200:
            return False, f"⚠️ 提交问题失败: {res.get('message', '未知错误')}"
        p = {
            "page": "/pages/challenge3/challenge3",
            "content": "挑战页-自护力调研弹窗-点击",
            "name": "maievent-page-operate",
            "mobile": "",
            "openId": self.openId,
            "unionId": self.unionId,
            "source": "wechat-default",
            "sdk": "wechat-default",
        }
        res1 = self.common_post("/healthyaging/danone/wx/config/eventReport", p)
        if res1.get("code") == 200:
            return True, f"✅ 提交问题[{title}]成功"
        return False, f"⚠️ 问题事件上报失败: {res1.get('message', '未知错误')}"

    def get_question(self) -> tuple[bool, str]:
        data = {"answers": [{"questionId": "159", "value": ["1014"]}], "csqId": 10, "challengeId": 167616}
        try:
            challenge_id = self.get_challenge_id()
            if challenge_id:
                data["challengeId"] = challenge_id
            res = self.common_get("/healthyaging/danone/wx/ha/csq/get?type=feedback_v3")
            ques = res.get("result", {}).get("csqQuestionList") or []
            if ques:
                q = ques[0]
                data["answers"][0]["questionId"] = q.get("id")
                if q.get("optionList"):
                    data["answers"][0]["value"][0] = q["optionList"][0].get("id")
                data["csqId"] = res.get("result", {}).get("csqId", data["csqId"])
                return self.submit_question(data, q.get("title", "问题"))
            return True, "✅ 无需提交问题"
        except Exception as exc:
            return False, f"❌ 问题处理异常: {exc}"

    def run(self) -> list[str]:
        results: list[str] = []
        _, msg = self.get_question()
        results.append(msg)
        _, msg = self.report_event()
        results.append(msg)
        results.extend(self.get_user_tasks())
        return results

    def verify(self) -> bool:
        try:
            res = self.common_get("/healthyaging/danone/wx/ha/selfcare/getCalendar")
            return res.get("code") == 200
        except Exception:
            return False


async def ask(prompt: str, timeout: int = 120000) -> str:
    await s.reply(prompt)
    child = await s.listen({"timeout": timeout})
    if not child:
        return ""
    return (await child.getContent() or "").strip()


async def load_accounts(user_id: str) -> list[str]:
    raw = await Bucket(BUCKET_USER).get(user_id, "[]")
    if isinstance(raw, list):
        return [str(x) for x in raw]
    try:
        value = json.loads(str(raw or "[]"))
        return [str(x) for x in value] if isinstance(value, list) else []
    except Exception:
        try:
            import ast
            value = ast.literal_eval(str(raw or "[]"))
            return [str(x) for x in value] if isinstance(value, list) else []
        except Exception:
            return []


async def save_accounts(user_id: str, accounts: list[str]) -> None:
    await Bucket(BUCKET_USER).set(user_id, json.dumps(accounts, ensure_ascii=False))


async def load_account_info(account_key: str) -> dict[str, Any] | None:
    raw = await Bucket(BUCKET_TOKEN).get(account_key, "")
    if isinstance(raw, dict):
        return raw
    try:
        data = json.loads(str(raw or ""))
        return data if isinstance(data, dict) else None
    except Exception:
        return None


async def save_account_info(account_key: str, info: dict[str, Any]) -> None:
    await Bucket(BUCKET_TOKEN).set(account_key, json.dumps(info, ensure_ascii=False))


async def delete_account_info(account_key: str) -> None:
    await Bucket(BUCKET_TOKEN).delete(account_key)


def account_key_of(open_id: str, union_id: str) -> str:
    return f"{open_id}_{union_id}"


def parse_account_lines(text: str) -> list[dict[str, str]]:
    accounts: list[dict[str, str]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or "#" not in line:
            continue
        parts = [x.strip() for x in line.split("#")]
        if len(parts) == 4 and all(parts):
            accounts.append({"remark": parts[0], "token": parts[1], "openId": parts[2], "unionId": parts[3]})
    return accounts


async def bind_account(user_id: str, cfg: dict[str, Any]) -> None:
    text = await ask(
        "=====达能益生登录=====\n"
        "请按格式发送账号信息，支持多行批量：\n"
        "备注#X-Access-Token#openId#unionId\n\n"
        "例：张三#token123#openid456#unionid789\n"
        "回复 q 退出",
        120000,
    )
    if not text:
        await s.reply("⏰ 操作超时，已退出")
        return
    if text.lower() == "q":
        await s.reply("✅ 已取消登录")
        return

    parsed = parse_account_lines(text)
    if not parsed:
        await s.reply("❌ 未检测到有效账号，请按：备注#token#openId#unionId")
        return

    current = await load_accounts(user_id)
    success = 0
    fail = 0
    lines: list[str] = []
    for acc in parsed:
        key = account_key_of(acc["openId"], acc["unionId"])
        try:
            if cfg.get("verify_on_bind", True):
                client = DNYX(acc["remark"], acc["token"], acc["openId"], acc["unionId"], cfg)
                if not client.verify():
                    fail += 1
                    lines.append(f"❌ {acc['remark']} - 账号验证失败")
                    continue
            if key not in current:
                current.append(key)
            await save_account_info(
                key,
                {
                    "token": acc["token"],
                    "openId": acc["openId"],
                    "unionId": acc["unionId"],
                    "remark": acc["remark"],
                    "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                },
            )
            success += 1
            lines.append(f"✅ {acc['remark']} - 登录成功")
        except Exception as exc:
            fail += 1
            lines.append(f"❌ {acc['remark']} - 异常：{exc}")
        time.sleep(0.2)

    await save_accounts(user_id, current)
    await s.reply(
        "=====批量登录完成=====\n"
        f"📊 总数：{len(parsed)}个\n✅ 成功：{success}个\n❌ 失败：{fail}个\n"
        "==================\n"
        + "\n".join(lines)
        + "\n==================\n💡 发送 达能查询 / 达能管理"
    )


async def choose_accounts(user_id: str, title: str = "选择账号", allow_all: bool = True) -> list[str]:
    accounts = await load_accounts(user_id)
    if not accounts:
        await s.reply("=====未绑定账号=====\n❌ 未找到任何账号信息\n💡 发送 达能登录 绑定\n==================")
        return []

    msg = f"========{title}======="
    if allow_all:
        msg += "\n[0] 全部账号"
    for i, key in enumerate(accounts, 1):
        info = await load_account_info(key) or {}
        msg += f"\n[{i}] {info.get('remark') or key}"
    msg += "\n=====================\n支持多选，如 1,2,3；回复 q 退出"
    choice = await ask(msg, 120000)
    if not choice or choice.lower() == "q":
        await s.reply("✅ 已退出操作")
        return []
    if allow_all and choice.strip() == "0":
        return accounts.copy()
    selected: list[str] = []
    for idx in choice.split(","):
        idx = idx.strip()
        if idx.isdigit():
            pos = int(idx) - 1
            if 0 <= pos < len(accounts):
                selected.append(accounts[pos])
    if not selected:
        await s.reply("❌ 未选择有效账号")
    return selected


async def query_accounts(user_id: str) -> None:
    selected = await choose_accounts(user_id, "选择查询账号")
    if not selected:
        return
    await s.reply(f"✅ 已选择 {len(selected)} 个账号，正在查询...")
    lines: list[str] = []
    for idx, key in enumerate(selected, 1):
        info = await load_account_info(key)
        if not info:
            lines.append(f"[{idx}] {key}：账号信息异常")
            continue
        lines.append(
            f"=====账号信息[{idx}/{len(selected)}]=====\n"
            f"📝 备注：{info.get('remark')}\n"
            f"🔑 Token：{mask_text(info.get('token'))}\n"
            f"🆔 openId：{mask_text(info.get('openId'))}\n"
            f"🆔 unionId：{mask_text(info.get('unionId'))}\n"
            f"🕒 添加时间：{info.get('create_time', '-') }\n"
            "=================="
        )
    await reply_chunks("\n".join(lines))


async def manage_account(user_id: str, cfg: dict[str, Any]) -> None:
    accounts = await load_accounts(user_id)
    if not accounts:
        await s.reply("=====未绑定账号=====\n❌ 未找到任何账号信息\n💡 发送 达能登录 绑定\n==================")
        return
    action = await ask("=====账号管理=====\n[1] 删除账号\n[2] 执行任务\n------------------\n回复数字选择功能\n回复 q 退出", 120000)
    if not action or action.lower() == "q":
        await s.reply("✅ 已退出操作")
        return
    selected = await choose_accounts(user_id, "选择账号")
    if not selected:
        return
    if action == "1":
        confirm = await ask("⚠️ 确认删除所选账号？回复 y 确认，其他取消", 120000)
        if confirm.lower() != "y":
            await s.reply("✅ 已取消删除")
            return
        removed = 0
        for key in selected:
            if key in accounts:
                accounts.remove(key)
            await delete_account_info(key)
            removed += 1
        await save_accounts(user_id, accounts)
        await s.reply(f"✅ 已删除 {removed}/{len(selected)} 个账号")
        return
    if action == "2":
        await run_selected(selected, cfg)
        return
    await s.reply("❌ 无效选择")


async def run_selected(account_keys: list[str], cfg: dict[str, Any]) -> tuple[int, int]:
    success = 0
    fail = 0
    for idx, key in enumerate(account_keys, 1):
        info = await load_account_info(key)
        if not info:
            fail += 1
            await s.reply(f"❌ [{idx}/{len(account_keys)}] {key}：账号信息异常")
            continue
        remark = str(info.get("remark") or key)
        try:
            client = DNYX(remark, str(info.get("token")), str(info.get("openId")), str(info.get("unionId")), cfg)
            results = client.run()
            success += 1
            await reply_chunks("\n".join([f"=====任务执行：{remark}====="] + results + ["===================="]))
        except Exception as exc:
            fail += 1
            await s.reply(f"❌ 账号执行失败：{remark}，错误：{exc}")
        if idx < len(account_keys):
            await asyncio.sleep(1.5)
    return success, fail


async def run_all_accounts(current_user_id: str, cfg: dict[str, Any], cron_mode: bool = False) -> None:
    if not cron_mode and not await s.isAdmin():
        await s.reply("=====权限不足=====\n❌ 此功能仅限管理员使用\n==================")
        return
    user_bucket = Bucket(BUCKET_USER)
    all_user_data = await user_bucket.getAll()
    account_keys: list[str] = []
    for _, raw in (all_user_data or {}).items():
        for key in await parse_accounts_from_raw(raw):
            if key not in account_keys:
                account_keys.append(key)
    if not account_keys:
        await s.reply("❌ 未找到任何账号")
        return
    await s.reply(f"🔄 开始运行达能益生账号，共 {len(account_keys)} 个")
    success, fail = await run_selected(account_keys, cfg)
    await s.reply(f"=====一键运行完成=====\n📊 总账号数：{len(account_keys)}个\n🎯 执行成功：{success}个\n❌ 执行失败：{fail}个\n==================")


async def parse_accounts_from_raw(raw: Any) -> list[str]:
    if isinstance(raw, list):
        return [str(x) for x in raw]
    try:
        value = json.loads(str(raw or "[]"))
        return [str(x) for x in value] if isinstance(value, list) else []
    except Exception:
        try:
            import ast
            value = ast.literal_eval(str(raw or "[]"))
            return [str(x) for x in value] if isinstance(value, list) else []
        except Exception:
            return []


async def show_tutorial() -> None:
    await s.reply(
        "=====达能益生教程=====\n"
        "用户指令：\n"
        "• 达能登录 - 绑定账号\n"
        "• 达能管理 - 删除账号/执行任务\n"
        "• 达能查询 - 查询账号\n"
        "• 达能教程 - 查看教程\n"
        "管理员指令：\n"
        "• 达能一键运行 - 运行所有账号\n"
        "登录格式：备注#X-Access-Token#openId#unionId\n"
        "获取参数：打开达能益生小程序，抓 api.digital4danone.com.cn 请求里的 X-Access-Token/openId/unionId\n"
        "说明：账号直接运行，无需额外授权"
    )


def mask_text(value: Any, keep: int = 4) -> str:
    text = str(value or "")
    if len(text) <= keep * 2:
        return text[:2] + "***" if text else "-"
    return text[:keep] + "***" + text[-keep:]


async def reply_chunks(text: str, size: int = 1800) -> None:
    text = str(text or "")
    if len(text) <= size:
        await s.reply(text)
        return
    for i in range(0, len(text), size):
        await s.reply(text[i : i + size])
        await asyncio.sleep(0.2)


async def main() -> None:
    cfg = normalize_config(await plugin_config.get())
    if not cfg.get("enable"):
        await s.reply("达能益生插件未启用，请先到插件配置开启")
        return

    message = (await s.getContent() or "").strip()
    user_id = await s.getUserId()

    if not message:
        if cfg.get("cron_run"):
            await run_all_accounts(str(user_id), cfg, cron_mode=True)
        return

    if "登录" in message or "登陆" in message:
        await bind_account(str(user_id), cfg)
    elif "管理" in message:
        await manage_account(str(user_id), cfg)
    elif "查询" in message:
        await query_accounts(str(user_id))
    elif "一键运行" in message:
        await run_all_accounts(str(user_id), cfg)
    elif "教程" in message:
        await show_tutorial()


asyncio.run(main())
