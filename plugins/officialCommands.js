/**
 * @title 官方命令
 * @author sillyGirl
 * @version v1.0.0
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
  restart: restartSillyGirl,
  update: updateSillyGirl,
  sillyGirlCreateSchema,
  SillyGirlPluginConfig,
} = require("sillygirl");

const DEFAULTS = {
  enable: true,
  update_mode: "auto",
  app_dir: "",
  git_remote: "origin",
  git_branch: "",
  docker_socket: "/var/run/docker.sock",
  docker_watchtower_image: "containrrr/watchtower:latest",
  update_timeout: 120,
  restart_after_update: false,
};

const schema = sillyGirlCreateSchema.object({
  enable: sillyGirlCreateSchema.boolean().setTitle("是否启用").setDefault(true),
  update_mode: sillyGirlCreateSchema.string()
    .setTitle("更新模式")
    .setEnum(["auto", "git", "docker"])
    .setEnumNames(["自动", "源码 Git", "Docker"])
    .setDefault("auto"),
  app_dir: sillyGirlCreateSchema.string()
    .setTitle("SillyGirl 源码目录")
    .setDescription("源码 Git 部署时填写 sillyGirl 主程序仓库目录；留空会自动探测常见目录。")
    .setDefault(""),
  git_remote: sillyGirlCreateSchema.string().setTitle("Git Remote").setDefault("origin"),
  git_branch: sillyGirlCreateSchema.string()
    .setTitle("Git 分支")
    .setDescription("留空使用当前分支的 upstream；没有 upstream 时默认 main。")
    .setDefault(""),
  docker_socket: sillyGirlCreateSchema.string()
    .setTitle("Docker Socket")
    .setDescription("Docker 更新需要部署时挂载 /var/run/docker.sock。")
    .setDefault("/var/run/docker.sock"),
  docker_watchtower_image: sillyGirlCreateSchema.string()
    .setTitle("Watchtower 镜像")
    .setDefault("containrrr/watchtower:latest"),
  update_timeout: sillyGirlCreateSchema.integer().setTitle("更新超时秒数").setMin(10).setMax(600).setDefault(120),
  restart_after_update: sillyGirlCreateSchema.boolean().setTitle("更新后自动重启").setDefault(false),
});

const pluginConfig = new SillyGirlPluginConfig(schema);

async function main() {
  const cfg = normalizeConfig(await pluginConfig.get());
  if (!cfg.enable) return s.reply("官方命令插件未启用，请先到插件配置开启");

  const cmd = String(await s.getContent() || "").trim();
  if (cmd === "时间") return replyTime();
  if (cmd === "版本") return replyVersion();
  if (cmd === "重启") return restart();
  if (cmd === "更新") return update(cfg);
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
  const bucket = new Bucket("sillyGirl");
  const current = await firstValue(bucket, ["version", "compiled_at"], "-");
  const latest = await firstValue(bucket, ["remote_version", "latest_version"], current);
  const startedAt = await bucket.get("started_at", "");
  const text = [
    "SillyGirl 版本",
    `当前版本：${current}`,
    `最新版本：${latest || current}`,
  ];
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
  if (!(await s.isAdmin())) {
    await s.reply("仅管理员可用");
    return;
  }

  await s.reply("开始更新 SillyGirl");

  try {
    const result = await updateSillyGirl({
      mode: cfg.update_mode,
      appDir: cfg.app_dir,
      gitRemote: cfg.git_remote,
      gitBranch: cfg.git_branch,
      dockerSocket: cfg.docker_socket,
      dockerWatchtowerImage: cfg.docker_watchtower_image,
      timeout: cfg.update_timeout,
      restart: cfg.restart_after_update,
    });
    if (result.mode === "docker") {
      const lines = [
        "Docker 更新已启动",
        `容器：${String(result.repo || "").replace(/^docker:/, "")}`,
        `镜像：${result.before || "-"}`,
      ];
      const output = compactOutput(result.output);
      if (output) lines.push(output);
      lines.push("稍后容器会由 Watchtower 自动重建，请等待 1-2 分钟后刷新页面。");
      await s.reply(lines.join("\n"));
      return;
    }
    const lines = [
      result.changed ? "更新完成" : "已经是最新代码",
      `目录：${result.repo}`,
      `提交：${result.before} -> ${result.after}`,
    ];
    const output = compactOutput(result.output);
    if (output) lines.push("输出：\n" + output);
    if (result.restarted) {
      lines.push("已配置更新后自动重启，1 秒后重启");
    } else {
      lines.push("如需生效，请发送：重启");
    }
    await s.reply(lines.join("\n"));
  } catch (error) {
    await s.reply(
      "更新失败：" + errorText(error) + "\n" +
      "源码部署请检查 Git 仓库目录；Docker 部署请确认已挂载 /var/run/docker.sock。"
    );
  }
}

async function firstValue(bucket, keys, fallback) {
  for (const key of keys) {
    const value = await bucket.get(key, "");
    if (value !== undefined && value !== null && String(value).trim()) return String(value).trim();
  }
  return fallback;
}

function normalizeConfig(input) {
  return Object.assign({}, DEFAULTS, input || {}, {
    enable: input && input.enable !== undefined ? Boolean(input.enable) : DEFAULTS.enable,
    update_mode: ["auto", "git", "docker"].includes(String(input && input.update_mode || "")) ? String(input.update_mode) : DEFAULTS.update_mode,
    app_dir: String(input && input.app_dir || DEFAULTS.app_dir).trim(),
    git_remote: String(input && input.git_remote || DEFAULTS.git_remote).trim() || DEFAULTS.git_remote,
    git_branch: String(input && input.git_branch || DEFAULTS.git_branch).trim(),
    docker_socket: String(input && input.docker_socket || DEFAULTS.docker_socket).trim() || DEFAULTS.docker_socket,
    docker_watchtower_image: String(input && input.docker_watchtower_image || DEFAULTS.docker_watchtower_image).trim() || DEFAULTS.docker_watchtower_image,
    update_timeout: clamp(Number(input && input.update_timeout || DEFAULTS.update_timeout), 10, 600),
    restart_after_update: Boolean(input && input.restart_after_update),
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
