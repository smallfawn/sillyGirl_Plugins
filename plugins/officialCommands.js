/**
 * @title 官方命令
 * @author sillyGirl
 * @version v1.0.4
 * @desc 提供时间、版本、更新、重启四个基础管理命令
 * @rule ^\s*(时间|版本|更新|重启)\s*$
 * @admin false
 * @priority 1
 * @public true
 * @class 工具
 * @depe []
 */

const {
  sender: s,
  Bucket,
  version: getSillyGirlVersion,
  restart: restartSillyGirl,
  update: updateSillyGirl,
  sillyGirlCreateSchema,
  SillyGirlPluginConfig,
} = require("sillygirl");

const DEFAULTS = {
  enable: true,
  update_timeout: 120,
};

const schema = sillyGirlCreateSchema.object({
  enable: sillyGirlCreateSchema.boolean().setTitle("是否启用").setDefault(true),
  update_timeout: sillyGirlCreateSchema.integer().setTitle("更新超时秒数").setMin(10).setMax(600).setDefault(120),
});

const pluginConfig = new SillyGirlPluginConfig(schema);

async function main() {
  const cmd = String(await s.getContent() || "").trim();
  if (cmd === "时间") return replyTime();
  if (cmd === "版本") return replyVersion();
  if (cmd === "重启") return restart();
  if (cmd === "更新") return update(await loadConfig());
}

async function loadConfig() {
  try {
    return normalizeConfig(await withTimeout(pluginConfig.get(), 5000, "读取官方命令插件配置超时"));
  } catch (error) {
    await s.reply("读取官方命令配置失败，使用默认配置继续：" + errorText(error));
    return normalizeConfig(DEFAULTS);
  }
}

async function replyTime() {
  const now = new Date();
  await s.reply([
    "当前时间",
    formatDate(now),
    `时间戳：${Math.floor(now.getTime() / 1000)}`,
    `时区：${Intl.DateTimeFormat().resolvedOptions().timeZone || "local"}`,
  ].join("\n"));
}

async function replyVersion() {
  const info = await getSillyGirlVersion();
  const bucket = new Bucket("sillyGirl");
  const current = String(info.current || "").trim() || "-";
  const latest = String(info.remote || "").trim() || current;
  const startedAt = await bucket.get("started_at", "");
  const text = [
    "SillyGirl 版本",
    `当前版本：${current}`,
    `最新版本：${latest || current}`,
  ];
  if (info.source) text.push(`来源：${info.source}`);
  if (startedAt) text.push(`启动时间：${startedAt}`);
  text.push(current && latest && normalizeVersion(current) !== normalizeVersion(latest) ? "状态：有新版本" : "状态：已是最新");
  await s.reply(text.join("\n"));
}

async function restart() {
  if (!(await s.isAdmin())) {
    await s.reply("仅管理员可用");
    return;
  }
  await s.reply("收到重启命令，1 秒后重启");
  await restartSillyGirl();
}

async function update(cfg) {
  await s.reply("收到更新命令，正在检查权限");

  if (!cfg.enable) {
    await s.reply("官方命令插件未启用，请先到插件配置开启");
    return;
  }

  if (!(await s.isAdmin())) {
    await s.reply("仅管理员可用");
    return;
  }

  await s.reply("开始更新 SillyGirl");

  try {
    if (typeof updateSillyGirl !== "function") {
      throw new Error("当前 SillyGirl 运行时未导出 update，请先升级主程序到 v0.2.3 或更新插件运行时");
    }
    const result = await withTimeout(
      updateSillyGirl({
        timeout: cfg.update_timeout,
        restart: true,
      }),
      (cfg.update_timeout + 15) * 1000,
      "更新执行超时"
    );
    const lines = [
      result.changed ? "更新完成" : "已经是最新版本",
      `来源：${result.repo || "-"}`,
      `版本：${result.before || "-"} -> ${result.after || "-"}`,
    ];
    const output = compactOutput(result.output);
    if (output) lines.push("输出：\n" + output);
    if (result.restarted) {
      lines.push("已触发自动重启，请等待 1-2 分钟后刷新页面");
    } else {
      lines.push("如需生效，请发送：重启");
    }
    await s.reply(lines.join("\n"));
  } catch (error) {
    await s.reply(
      "更新失败：" + errorText(error) + "\n" +
      "请确认当前版本已内置 curl，且 GitHub 加速地址可以访问 Release 文件。"
    );
  }
}

function normalizeConfig(input) {
  return Object.assign({}, DEFAULTS, input || {}, {
    enable: input && input.enable !== undefined ? Boolean(input.enable) : DEFAULTS.enable,
    update_timeout: clamp(Number(input && input.update_timeout || DEFAULTS.update_timeout), 10, 600),
  });
}

function clamp(value, min, max) {
  if (!Number.isFinite(value)) return min;
  return Math.max(min, Math.min(max, Math.floor(value)));
}

function normalizeVersion(value) {
  return String(value || "").trim().replace(/^refs\/tags\//, "").replace(/^[vV]/, "");
}

function formatDate(date) {
  const pad = (value) => String(value).padStart(2, "0");
  return [
    date.getFullYear(),
    "-",
    pad(date.getMonth() + 1),
    "-",
    pad(date.getDate()),
    " ",
    pad(date.getHours()),
    ":",
    pad(date.getMinutes()),
    ":",
    pad(date.getSeconds()),
  ].join("");
}

function compactOutput(value) {
  const text = String(value || "").trim();
  if (!text) return "";
  const lines = text.split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
  return lines.slice(-8).join("\n").slice(0, 1000);
}

function withTimeout(promise, timeoutMs, message) {
  return Promise.race([
    promise,
    new Promise((_, reject) => {
      setTimeout(() => reject(new Error(message || "执行超时")), Math.max(1000, timeoutMs));
    }),
  ]);
}

function errorText(error) {
  if (!error) return "未知错误";
  const detail = compactOutput(error.stderr || error.stdout);
  const message = String(error.message || error).trim();
  return detail ? `${message}\n${detail}` : message;
}

main().catch(async (error) => {
  try {
    await s.reply("官方命令异常：" + errorText(error));
  } catch (_) {
    console.error(error);
  }
});
