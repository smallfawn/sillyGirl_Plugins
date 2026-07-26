/**
 * @title 青龙管理
 * @author sillyGirl
 * @version v1.0.0
 * @desc 青龙面板管理脚本 - 管理面板、环境变量等
 * @rule ^(?:青龙|面板列表|面板状态|变量列表|变量详情|新建变量|修改变量|修改变量备注|删除变量|启用变量|禁用变量|通知)
 * @admin true
 * @priority 1
 * @public true
 * @class 工具
 */

const { sender: s, QingLong, Bucket, console } = require("sillygirl");

const MAX_PANEL_SCAN = 50;

async function main() {
  if (!(await s.isAdmin())) {
    await s.reply("仅管理员可用");
    return;
  }

  const cmd = String(await s.getContent() || "").trim();
  if (!cmd || cmd === "青龙") {
    await s.reply(menuText());
    return;
  }

  if (cmd === "面板列表") {
    await listPanels();
    return;
  }

  if (cmd === "面板状态") {
    await panelStatus();
    return;
  }

  const ql = await firstAvailablePanel();
  let match;

  match = cmd.match(/^变量列表\s*(.*)$/);
  if (match) return listEnvs(ql, match[1]);

  match = cmd.match(/^变量详情\s*(\d+)$/);
  if (match) return getEnvDetail(ql, match[1]);

  match = cmd.match(/^新建变量\s+([^\s=]+)=([^\s]+)(?:\s+(.+))?$/);
  if (match) return createEnv(ql, match[1], match[2], match[3] || "");

  match = cmd.match(/^修改变量\s*(\d+)\s+([^\s=]+)=(.+)$/);
  if (match) return updateEnv(ql, match[1], match[2], match[3]);

  match = cmd.match(/^修改变量备注\s*(\d+)\s+(.+)$/);
  if (match) return updateEnvRemark(ql, match[1], match[2]);

  match = cmd.match(/^删除变量\s+([\d,，\s]+)$/);
  if (match) return deleteEnvs(ql, match[1]);

  match = cmd.match(/^启用变量\s+([\d,，\s]+)$/);
  if (match) return toggleEnvs(ql, match[1], true);

  match = cmd.match(/^禁用变量\s+([\d,，\s]+)$/);
  if (match) return toggleEnvs(ql, match[1], false);

  match = cmd.match(/^通知\s+(.+?)\s*[|｜]\s*(.+)$/);
  if (match) return sendNotify(ql, match[1], match[2]);

  await s.reply(menuText());
}

function menuText() {
  return [
    "青龙管理",
    "面板列表 | 面板状态",
    "变量列表[关键词] | 变量详情<ID>",
    "新建变量 名称=值[备注]",
    "修改变量<ID> 名称=值",
    "修改变量备注<ID> 备注",
    "删除变量<ID1,ID2>",
    "启用变量<ID1,ID2> | 禁用变量<ID1,ID2>",
    "通知 标题|内容",
  ].join("\n");
}

async function readPanels() {
  const bucket = new Bucket("sillyGirl");
  const raw = await bucket.get("qinglong_panels", []);
  if (Array.isArray(raw)) return raw;
  if (typeof raw !== "string" || !raw.trim()) return [];
  const text = raw.startsWith("o:") ? raw.slice(2) : raw;
  const panels = JSON.parse(text);
  return Array.isArray(panels) ? panels : [];
}

async function listPanels() {
  try {
    const panels = await readPanels();
    if (!panels.length) {
      await s.reply("未添加面板,请在管理后台添加");
      return;
    }
    const lines = ["面板列表(" + panels.length + "个)"];
    panels.forEach((panel, index) => {
      const status = panel.status === "online" ? "在线" : "离线";
      lines.push("#" + (index + 1) + " " + (panel.name || "未命名") + " " + status);
      lines.push(panel.address || "-");
      if (panel.message) lines.push(panel.message);
    });
    await s.reply(lines.join("\n"));
  } catch (error) {
    await s.reply("获取失败:" + errorText(error));
  }
}

async function panelStatus() {
  const lines = ["检测中.."];
  let count = 0;
  for (let i = 1; i <= MAX_PANEL_SCAN; i++) {
    try {
      const ql = new QingLong({ id: i });
      const envs = await ql.getEnvs();
      lines.push("#" + i + " " + (ql.name || ql.address || "青龙面板") + " 在线 变量:" + asArray(envs).length);
      count++;
    } catch (error) {
      if (count === 0) continue;
      break;
    }
  }
  await s.reply(count ? lines.join("\n") : "未添加面板");
}

async function firstAvailablePanel() {
  for (let i = 1; i <= MAX_PANEL_SCAN; i++) {
    try {
      const ql = new QingLong({ id: i });
      await ql.getEnvs();
      return ql;
    } catch (error) {}
  }
  throw new Error("无可用青龙面板");
}

async function listEnvs(ql, search) {
  try {
    search = String(search || "").trim();
    const envs = search ? await ql.getEnvs(search) : await ql.getEnvs();
    const list = asArray(envs);
    if (!list.length) {
      await s.reply(search ? "未找到[" + search + "]" : "暂无变量");
      return;
    }
    const lines = ["变量列表(" + list.length + "条)" + (search ? "[" + search + "]" : "")];
    list.forEach((env) => {
      const status = Number(env.status) === 0 ? "启用" : "禁用";
      const value = truncate(env.value || "空", 20);
      lines.push("#" + envId(env) + " " + (env.name || "") + " " + status);
      lines.push(value + (env.remarks ? " " + env.remarks : ""));
    });
    await s.reply(lines.join("\n"));
  } catch (error) {
    await s.reply("获取失败:" + errorText(error));
  }
}

async function getEnvDetail(ql, id) {
  try {
    const env = await ql.getEnvById(Number(id));
    if (!env) {
      await s.reply("未找到ID:" + id);
      return;
    }
    const lines = [
      "变量详情",
      "ID:" + envId(env) + " " + (env.name || ""),
      "值:" + (env.value || "空"),
      "状态:" + (Number(env.status) === 0 ? "已启用" : "已禁用"),
    ];
    if (env.remarks) lines.push("备注:" + env.remarks);
    await s.reply(lines.join("\n"));
  } catch (error) {
    await s.reply("获取失败:" + errorText(error));
  }
}

async function createEnv(ql, name, value, remarks) {
  try {
    const result = await ql.createEnv({ name, value, remarks });
    const created = firstItem(result) || {};
    const lines = ["创建成功", name + "=" + truncate(value, 30)];
    if (remarks) lines.push("备注:" + remarks);
    if (envId(created) !== "-") lines.push("ID:" + envId(created));
    await s.reply(lines.join("\n"));
  } catch (error) {
    await s.reply("创建失败:" + errorText(error));
  }
}

async function updateEnv(ql, id, name, value) {
  try {
    await ql.updateEnv({ id: Number(id), name, value });
    await s.reply("更新成功\nID:" + id + " " + name + "=" + truncate(value, 30));
  } catch (error) {
    await s.reply("更新失败:" + errorText(error));
  }
}

async function updateEnvRemark(ql, id, remarks) {
  try {
    const env = await ql.getEnvById(Number(id));
    if (!env) {
      await s.reply("未找到ID:" + id);
      return;
    }
    await ql.updateEnv({
      id: Number(id),
      name: env.name,
      value: env.value,
      remarks,
    });
    await s.reply("备注已更新\nID:" + id + " 备注:" + remarks);
  } catch (error) {
    await s.reply("更新失败:" + errorText(error));
  }
}

async function deleteEnvs(ql, idsText) {
  const ids = parseIds(idsText);
  if (!ids.length) {
    await s.reply("请提供ID");
    return;
  }
  try {
    await ql.deleteEnvs(ids);
    await s.reply("已删除" + ids.length + "个 ID:" + ids.join(","));
  } catch (error) {
    await s.reply("删除失败:" + errorText(error));
  }
}

async function toggleEnvs(ql, idsText, enable) {
  const ids = parseIds(idsText);
  if (!ids.length) {
    await s.reply("请提供ID");
    return;
  }
  const actionText = enable ? "启用" : "禁用";
  try {
    if (enable) await ql.enableEnvs(ids);
    else await ql.disableEnvs(ids);
    await s.reply("已" + actionText + ids.length + "个 ID:" + ids.join(","));
  } catch (error) {
    await s.reply(actionText + "失败:" + errorText(error));
  }
}

async function sendNotify(ql, title, content) {
  try {
    await ql.systemNotify(title, content);
    await s.reply("通知已发送\n" + title + "\n" + content);
  } catch (error) {
    await s.reply("发送失败:" + errorText(error));
  }
}

function parseIds(value) {
  return String(value || "")
    .split(/[,，\s]+/)
    .map((item) => Number(item.trim()))
    .filter((item) => Number.isInteger(item));
}

function asArray(value) {
  if (Array.isArray(value)) return value;
  if (value && Array.isArray(value.data)) return value.data;
  if (value && value.data && Array.isArray(value.data.data)) return value.data.data;
  return [];
}

function firstItem(value) {
  const list = asArray(value);
  return list.length ? list[0] : value;
}

function envId(env) {
  return String(env && (env.id ?? env._id ?? env.ID) || "-");
}

function truncate(value, length) {
  value = String(value || "");
  return value.length > length ? value.slice(0, length) + ".." : value;
}

function errorText(error) {
  return error && error.message ? error.message : String(error);
}

main().catch(async (error) => {
  try {
    await s.reply("异常:" + errorText(error));
  } catch (_) {
    console.error("青龙管理异常:", error);
  }
});
