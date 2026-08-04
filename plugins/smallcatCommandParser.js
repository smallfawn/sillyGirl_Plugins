/**
 * @title smallcat口令解析
 * @author sillyGirl
 * @version v1.1.4
 * @desc 输入“解析：小程序口令/短链”，通过 SmallCat 内联客户端返回小程序信息
 * @rule ^\s*解析[:：]\s*(.+)\s*$
 * @admin false
 * @priority 10
 * @public true
 * @class 工具
 * @depe []
 */

const {
  sender: s,
  console,
  form,
  container,
} = require('sillygirl');


const DEFAULTS = {
  enable: true,
  smallcat_id: 1,
  openid: "",
  scene: 23,
};

const pluginConfig = new form({
  enable: form.boolean().title("是否启用").default(true),
  smallcat_id: form.integer()
    .title("smallcat 编号")
    .description("后台 smallcat 页面中的编号，从 1 开始；地址读取该面板配置")
    .widget("smallcat-panel")
    .min(1)
    .default(DEFAULTS.smallcat_id),
  openid: form.string()
    .title("手动 openid")
    .description("多个用逗号、空格或换行分隔，解析时使用第一个；留空则读取 SmallCat 全部账号并使用第一个可用账号")
    .default(""),
  scene: form.integer()
    .title("解析场景值")
    .description("传给 /wx/translatelink 的 scene，默认 23")
    .min(1)
    .default(DEFAULTS.scene),
});

async function main() {
  const content = String(await s.getContent() || "").trim();
  const matched = content.match(/^\s*解析[:：]\s*([\s\S]+?)\s*$/);
  if (!matched) return;

  const command = String(matched[1] || "").trim();
  if (!command) {
    await s.reply("请输入要解析的小程序口令，例如：解析：#小程序://名称/路径");
    return;
  }

  const cfg = normalizeConfig(await pluginConfig.get());
  if (!cfg.enable) {
    await s.reply("smallcat口令解析插件未启用，请先到插件配置开启");
    return;
  }

  try {
    validateConfig(cfg);
    const result = await translateLink(cfg, command);
    await s.reply(formatResult(result));
  } catch (error) {
    await s.reply("smallcat口令解析失败：" + errorText(error));
  }
}

function normalizeConfig(input) {
  const cfg = Object.assign({}, DEFAULTS, input || {});
  cfg.enable = input && input.enable !== undefined ? Boolean(input.enable) : DEFAULTS.enable;
  cfg.smallcat_id = positiveInt(cfg.smallcat_id, DEFAULTS.smallcat_id);
  cfg.openid = String(cfg.openid || "").trim();
  cfg.scene = positiveInt(cfg.scene, DEFAULTS.scene);
  return cfg;
}

function validateConfig(cfg) {
  if (!Number.isInteger(cfg.smallcat_id) || cfg.smallcat_id < 1) throw new Error("smallcat 编号必须从 1 开始");
}

async function translateLink(cfg, command) {
  const sm = new container.SmallCat({ id: cfg.smallcat_id });
  const openid = await resolveOpenid(sm, cfg);
  const payload = await sm.translateLink({
    openid,
    link: command,
    scene: cfg.scene,
  });
  if (payload && payload.status === false) {
    throw new Error(responseMessage(payload) || "smallcat 接口返回失败状态");
  }
  return payload && Object.prototype.hasOwnProperty.call(payload, "data") ? payload.data : payload;
}

async function resolveOpenid(sm, cfg) {
  const manual = splitOpenids(cfg.openid);
  if (manual.length) return manual[0];

  const payload = await sm.request("GET", "/api/accounts");
  const account = accountItems(payload).find((item) => item && !item.disabled && String(item.openid || item.openId || "").trim());
  if (!account) throw new Error("SmallCat 全部账号中没有有效 openid");
  return String(account.openid || account.openId).trim();
}

function splitOpenids(value) {
  return [...new Set(String(value || "").split(/[,，;；\s]+/).map((item) => item.trim()).filter(Boolean))];
}

function accountItems(payload) {
  const queue = [payload];
  while (queue.length) {
    const value = queue.shift();
    if (Array.isArray(value)) return value;
    if (!value || typeof value !== "object") continue;
    for (const key of ["data", "list", "items", "accounts", "users", "value"]) {
      if (value[key] !== undefined) queue.push(value[key]);
    }
  }
  return [];
}

function formatResult(payload) {
  const launchConfig = parseJSONObject(firstValue(payload, ["launch_config"]));
  const source = launchConfig ? { payload, launchConfig } : payload;
  const appID = firstText(source, ["app_id", "appid", "appId"]);
  const appUserName = firstText(source, ["app_user_name", "appUserName"]);
  const title = firstText(source, ["page_title", "nick_name", "nickname", "title"]);
  const path = firstText(source, ["entry_url", "entryUrl", "path"]);
  const deepLink = firstText(source, ["deep_link_url", "deepLinkURL", "deepLinkUrl"]);
  const scene = firstText(source, ["scene", "host_scene", "hostScene"]);
  const sceneNote = firstText(source, ["scene_note", "sceneNote"]);
  const errCode = firstNumber(source, ["errcode", "errCode"]);
  const errMessage = firstText(source, ["errmsg", "errMsg", "err_wording"]);

  if (errCode !== null && errCode !== 0) {
    throw new Error(errMessage || `smallcat 解析错误码：${errCode}`);
  }

  const lines = ["smallcat口令解析成功"];
  if (title) lines.push(`名称：${title}`);
  if (appID) lines.push(`appid：${appID}`);
  if (appUserName) lines.push(`原始ID：${appUserName}`);
  if (path) lines.push(`路径：${path}`);
  if (deepLink) lines.push(`DeepLink：${deepLink}`);
  if (scene) lines.push(`场景：${scene}`);
  if (sceneNote) lines.push(`场景说明：${sceneNote}`);
  if (lines.length === 1) lines.push("返回：" + compactJSON(payload, 1800));
  return lines.join("\n");
}

function firstValue(payload, keys) {
  const wanted = new Set(keys.map((key) => String(key).toLowerCase()));
  const queue = [payload];
  while (queue.length) {
    const current = queue.shift();
    if (!current || typeof current !== "object") continue;
    for (const [key, value] of Object.entries(current)) {
      if (wanted.has(String(key).toLowerCase()) && value !== undefined && value !== null && value !== "") {
        return value;
      }
    }
    for (const value of Object.values(current)) {
      if (value && typeof value === "object") queue.push(value);
    }
  }
  return null;
}

function firstText(payload, keys) {
  const value = firstValue(payload, keys);
  if (value === null || value === undefined || typeof value === "object") return "";
  return String(value).trim();
}

function firstNumber(payload, keys) {
  const value = firstValue(payload, keys);
  if (value === null || value === undefined || value === "") return null;
  const number = Number(value);
  return Number.isFinite(number) ? number : null;
}

function parseJSONObject(value) {
  if (value && typeof value === "object" && !Array.isArray(value)) return value;
  if (typeof value !== "string" || !value.trim()) return null;
  try {
    const parsed = JSON.parse(value);
    return parsed && typeof parsed === "object" && !Array.isArray(parsed) ? parsed : null;
  } catch (_) {
    return null;
  }
}

function responseMessage(payload) {
  const value = firstValue(payload, ["message", "msg", "error", "errmsg", "errMsg"]);
  if (value && typeof value === "object") return compactJSON(value, 300);
  return String(value || "").trim().slice(0, 300);
}

function compactJSON(value, limit) {
  let text;
  try {
    text = JSON.stringify(value);
  } catch (_) {
    text = String(value || "");
  }
  return text.length > limit ? text.slice(0, limit) + "..." : text;
}

function positiveInt(value, fallback) {
  const number = Number(value);
  return Number.isInteger(number) && number > 0 ? number : fallback;
}

function errorText(error) {
  return error && error.message ? String(error.message).trim() : String(error || "未知错误").trim();
}

if (globalThis.__SMALLCAT_COMMAND_PARSER_TEST__) {
  module.exports = { normalizeConfig, resolveOpenid, splitOpenids, accountItems };
} else {
  main().catch(async (error) => {
    try {
      await s.reply("smallcat口令解析异常：" + errorText(error));
    } catch (_) {
      console.error("smallcat口令解析异常", error);
    }
  });
}
