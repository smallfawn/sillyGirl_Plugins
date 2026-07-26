/**
 * @title smallcat登录
 * @author sillyGirl
 * @version v1.0.1
 * @desc 通过 smallcat 二维码扫码登录和删除已保存账号
 * @rule ^\s*sm(登录|退出)(?:\s+(.+))?\s*$
 * @admin false
 * @priority 10
 * @public true
 * @class 工具
 * @depe []
 */

const {
  sender: s,
  SmallCat,
  sillyGirlCreateSchema,
  SillyGirlPluginConfig,
  sleep,
  console,
  utils,
} = require("sillygirl");

const DEFAULTS = {
  enable: true,
  smallcat_id: 1,
  login_type: 1,
  login_timeout: 180,
  poll_interval: 3,
  default_display_name: "",
};

const schema = sillyGirlCreateSchema.object({
  enable: sillyGirlCreateSchema.boolean().setTitle("是否启用").setDefault(true),
  smallcat_id: sillyGirlCreateSchema.integer().setTitle("smallcat 编号").setDescription("后台 smallcat 页面里的编号，从 1 开始").setDefault(1),
  login_type: sillyGirlCreateSchema.integer().setTitle("登录类型").setDescription("传给 smallcat createQr/addUser 的 type，默认 1").setDefault(1),
  login_timeout: sillyGirlCreateSchema.integer().setTitle("扫码超时秒数").setMin(30).setMax(600).setDefault(180),
  poll_interval: sillyGirlCreateSchema.integer().setTitle("轮询间隔秒数").setMin(1).setMax(10).setDefault(3),
  default_display_name: sillyGirlCreateSchema.string().setTitle("默认备注").setDescription("sm登录 后面没写备注时使用；仍为空则由 smallcat 决定").setDefault(""),
});

const pluginConfig = new SillyGirlPluginConfig(schema);

async function main() {
  const cfg = normalizeConfig(await pluginConfig.get());
  if (!cfg.enable) {
    await s.reply("smallcat登录插件未启用，请先到插件配置开启");
    return;
  }

  const content = String(await s.getContent() || "").trim();
  const matched = content.match(/^sm(登录|退出)(?:\s+(.+))?$/);
  if (!matched) return;

  const action = matched[1];
  const arg = String(matched[2] || "").trim();
  const sm = new SmallCat({ id: cfg.smallcat_id });

  try {
    if (action === "登录") {
      await login(sm, cfg, arg);
      return;
    }
    await logout(sm, cfg, arg);
  } catch (error) {
    await s.reply(`smallcat${action}失败：${errorText(error)}`);
  }
}

async function login(sm, cfg, displayNameArg) {
  const displayName = displayNameArg || cfg.default_display_name;
  const created = unwrap(await sm.createQr({ type: cfg.login_type }));
  const uuid = firstString(created, ["uuid", "qrUUID", "qruuid"]);
  const qrcodeUrl = firstString(created, ["qrcodeUrl", "qrCodeDataUrl", "qr_url", "url"]);
  if (!uuid) {
    throw new Error(`createQr 未返回 uuid；返回字段=${Object.keys(created || {}).join(",") || "-"}`);
  }

  await s.reply([
    "smallcat扫码登录",
    `编号：${cfg.smallcat_id}`,
    `UUID：${uuid}`,
    `请在 ${cfg.login_timeout} 秒内扫码确认`,
    qrcodeUrl ? utils.image(qrcodeUrl) : "二维码链接未返回，请在 smallcat 控制台查看",
  ].join("\n"));

  const deadline = Date.now() + cfg.login_timeout * 1000;
  let lastState = "";
  while (Date.now() < deadline) {
    await sleep(cfg.poll_interval * 1000);
    const checked = unwrap(await sm.checkQr(uuid));
    const state = firstString(checked, ["state", "status"]);
    const code = firstString(checked, ["wxCode", "wx_code", "code"]);
    if (state && state !== lastState) {
      lastState = state;
      if (state === "scanned") await s.reply("已扫码，请在手机上确认登录");
    }
    if (isExpiredState(state)) {
      await s.reply(`smallcat扫码已结束：${state}`);
      return;
    }
    if (isConfirmed(checked, state, code)) {
      if (!code) throw new Error("扫码已确认，但 checkQr 未返回 code");
      const saved = await sm.addUser({
        code,
        type: cfg.login_type,
        displayName,
      });
      const result = unwrap(saved);
      await s.reply(formatLoginSuccess(result, displayName));
      return;
    }
  }

  await s.reply("smallcat扫码登录超时，请重新发送 sm登录");
}

async function logout(sm, cfg, arg) {
  const openid = extractOpenid(arg);
  if (!openid) {
    const payload = await sm.userList();
    const accounts = normalizeAccounts(unwrap(payload));
    if (!accounts.length) {
      await s.reply("当前 smallcat 没有已保存账号");
      return;
    }
    await s.reply([
      "请指定要退出的 openid：",
      "sm退出 OPENID",
      "",
      ...accounts.slice(0, 10).map((item, index) => `${index + 1}. ${accountName(item)} ${item.openid}`),
      accounts.length > 10 ? `... 还有 ${accounts.length - 10} 个` : "",
    ].filter(Boolean).join("\n"));
    return;
  }

  if (typeof sm.request !== "function") {
    throw new Error("当前 SillyGirl 版本不支持 SmallCat.request，请先更新主程序");
  }
  const result = await sm.request("POST", "/api/accounts/delete", { openid });
  const unwrapped = unwrap(result);
  await s.reply(formatLogoutSuccess(unwrapped, openid, cfg));
}

function normalizeConfig(input) {
  const cfg = Object.assign({}, DEFAULTS, input || {});
  cfg.smallcat_id = positiveInt(cfg.smallcat_id, DEFAULTS.smallcat_id);
  cfg.login_type = positiveInt(cfg.login_type, DEFAULTS.login_type);
  cfg.login_timeout = clamp(Number(cfg.login_timeout || DEFAULTS.login_timeout), 30, 600);
  cfg.poll_interval = clamp(Number(cfg.poll_interval || DEFAULTS.poll_interval), 1, 10);
  cfg.default_display_name = String(cfg.default_display_name || "").trim();
  return cfg;
}

function positiveInt(value, fallback) {
  const number = Number(value);
  return Number.isInteger(number) && number > 0 ? number : fallback;
}

function clamp(value, min, max) {
  if (!Number.isFinite(value)) return min;
  return Math.max(min, Math.min(max, Math.floor(value)));
}

function unwrap(payload) {
  if (!payload || typeof payload !== "object") return { value: payload };
  if (Object.prototype.hasOwnProperty.call(payload, "status")) {
    if (payload.status === false) throw new Error(responseMessage(payload) || "smallcat 接口业务状态失败");
    if (Object.prototype.hasOwnProperty.call(payload, "data")) return unwrapData(payload.data);
  }
  if (Object.prototype.hasOwnProperty.call(payload, "code") && Object.prototype.hasOwnProperty.call(payload, "data")) {
    const code = String(payload.code);
    if (!["0", "200", "201"].includes(code)) throw new Error(responseMessage(payload) || `接口业务状态异常：${code}`);
    return unwrapData(payload.data);
  }
  return payload;
}

function unwrapData(data) {
  if (data && typeof data === "object" && !Array.isArray(data)) return data;
  if (typeof data === "string" && /^[\s]*[\[{]/.test(data)) {
    try {
      const decoded = JSON.parse(data);
      return decoded && typeof decoded === "object" && !Array.isArray(decoded) ? decoded : { value: decoded };
    } catch (_) {}
  }
  return { value: data };
}

function firstString(payload, keys) {
  const value = nestedValue(payload, keys);
  if (typeof value === "string") return value.trim();
  if (typeof value === "number" || typeof value === "boolean") return String(value);
  return "";
}

function nestedValue(payload, keys) {
  const wanted = new Set(keys);
  const lower = new Set(keys.map((key) => String(key).toLowerCase()));
  if (payload && typeof payload === "object") {
    if (Array.isArray(payload)) {
      for (const item of payload) {
        const found = nestedValue(item, keys);
        if (found !== undefined && found !== null && found !== "") return found;
      }
      return null;
    }
    for (const [key, value] of Object.entries(payload)) {
      if ((wanted.has(key) || lower.has(String(key).toLowerCase())) && value !== undefined && value !== null && value !== "") return value;
    }
    for (const value of Object.values(payload)) {
      const found = nestedValue(value, keys);
      if (found !== undefined && found !== null && found !== "") return found;
    }
  }
  return null;
}

function isConfirmed(payload, state, code) {
  if (code) return true;
  if (payload && payload.isConfirmed === true) return true;
  return ["confirmed", "success", "ok", "done"].includes(String(state || "").toLowerCase());
}

function isExpiredState(state) {
  return ["expired", "canceled", "cancelled", "timeout"].includes(String(state || "").toLowerCase());
}

function normalizeAccounts(payload) {
  let values = payload && (payload.value ?? payload.data ?? payload.list ?? payload.items);
  if (values && typeof values === "object" && !Array.isArray(values)) {
    values = values.data || values.list || values.items;
  }
  return (Array.isArray(values) ? values : [])
    .filter((item) => item && typeof item === "object")
    .map((item) => Object.assign({}, item, {
      openid: String(item.openid || item.openId || item.id || "").trim(),
    }))
    .filter((item) => item.openid);
}

function accountName(item) {
  return String(item.displayName || item.remark || item.nickname || item.name || "未命名").trim();
}

function extractOpenid(value) {
  const text = String(value || "").trim();
  if (!text) return "";
  const match = text.match(/(?:openid[:：=]\s*)?([A-Za-z0-9_-]{8,})/);
  return match ? match[1] : "";
}

function formatLoginSuccess(result, displayName) {
  const openid = firstString(result, ["openid", "openId"]);
  const message = responseMessage(result);
  return [
    "smallcat登录成功",
    openid ? `openid：${openid}` : "",
    displayName ? `备注：${displayName}` : "",
    message ? `message：${message}` : "",
  ].filter(Boolean).join("\n");
}

function formatLogoutSuccess(result, openid) {
  const message = responseMessage(result);
  return [
    "smallcat退出成功",
    `openid：${openid}`,
    message ? `message：${message}` : "",
  ].filter(Boolean).join("\n");
}

function responseMessage(payload) {
  const value = nestedValue(payload, ["message", "msg", "error", "errmsg", "errMsg"]);
  if (value && typeof value === "object") return JSON.stringify(value).slice(0, 300);
  return String(value || "").trim().slice(0, 300);
}

function errorText(error) {
  return error && error.message ? String(error.message) : String(error || "");
}

main().catch(async (error) => {
  try {
    await s.reply("smallcat登录异常：" + errorText(error));
  } catch (_) {
    console.error("smallcat登录异常", error);
  }
});
