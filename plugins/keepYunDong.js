// [title: Keep运动]
// [name: keepYunDong]
// [language: javascript]
// [class: 任务]
// [author: sillyGirl]
// [version: v1.0.1]
// [public: true]
// [disable: false]
// [admin: false]
// [rule: ^(Keep|keep)(登录|登陆|管理|查询|清理|授权|教程)$|^(登录|登陆|管理|查询|清理)(Keep|keep)$]
// [icon: https://api.iconify.design/lucide:bot.svg]
// [description: Keep Token 绑定、青龙同步、账号查询与清理]
// [depe: []]

const { container, plugin, sender: s } = require("sillygirl");

const config = new plugin.Form({
  enable: plugin.Form.boolean().title("是否启用").default(true),
  qinglong_id: plugin.Form.number().title("青龙容器编号").default(1),
  env_name: plugin.Form.string().title("脚本环境变量名").default("KEEP_TOKEN"),
});

async function main() {
  try {
    const cfg = normalize(await config.get());
    if (!cfg.enable) return s.reply("Keep运动插件未启用");
    const content = String(s.getContent() || "").toLowerCase();
    const ql = new container.QingLong({ id: cfg.qinglongId });

    if (content.includes("教程") || content.includes("授权")) {
      return s.reply("发送 Keep登录，然后按“备注#Token”提交；只有 Token 时可直接发送 Token，多账号换行。");
    }
    if (content.includes("查询") || content.includes("管理")) return showAccounts(ql, cfg.envName);
    if (content.includes("清理")) return removeAccounts(ql, cfg.envName);
    if (content.includes("登录") || content.includes("登陆")) {
      s.reply("请发送 Keep Token，格式：备注#Token；多账号可换行，输入 q 取消。");
      return s.listen({
        rules: ["raw ^([\\s\\S]+)$"],
        timeout: 60000,
        user_id: s.getUserId(),
        chat_id: s.getChatId(),
        handle: (next) => {
          const value = String(next.param(1) || "").trim();
          if (/^q$/i.test(value)) return "已取消";
          return saveAccounts(ql, cfg.envName, value, next);
        },
      });
    }
  } catch (error) {
    return s.reply(`Keep处理失败：${message(error)}`);
  }
}

async function saveAccounts(ql, envName, input, replySender) {
  try {
    const rows = parseRows(input);
    const owner = ownerKey(replySender);
    const current = onlyNamed(await ql.getEnvs({ searchValue: envName }), envName);
    let created = 0;
    let updated = 0;
    for (const row of rows) {
      const existing = current.find((item) => ownedBy(item, owner) && (remarkOf(item) === row.remark || item.value === row.token));
      const remarks = `${owner}|${row.remark}`;
      if (existing) {
        await ql.updateEnv({ id: envId(existing), name: envName, value: row.token, remarks });
        updated += 1;
      } else {
        await ql.createEnv({ name: envName, value: row.token, remarks });
        created += 1;
      }
    }
    return replySender.reply(`Keep账号同步完成：新增 ${created}，更新 ${updated}`);
  } catch (error) {
    return replySender.reply(`Keep提交失败：${message(error)}`);
  }
}

async function showAccounts(ql, envName) {
  const owner = ownerKey(s);
  const all = onlyNamed(await ql.getEnvs({ searchValue: envName }), envName);
  const visible = s.isAdmin() ? all : all.filter((item) => ownedBy(item, owner));
  if (!visible.length) return s.reply("没有找到你的 Keep 账号");
  return s.reply([`Keep账号：${visible.length} 个`, ...visible.map((item, index) => `${index + 1}. ${remarkOf(item) || "未备注"}${item.status ? "（已禁用）" : ""}`)].join("\n"));
}

async function removeAccounts(ql, envName) {
  const owner = ownerKey(s);
  const all = onlyNamed(await ql.getEnvs({ searchValue: envName }), envName);
  const ids = all.filter((item) => s.isAdmin() || ownedBy(item, owner)).map(envId).filter(Boolean);
  if (!ids.length) return s.reply("没有可清理的 Keep 账号");
  await ql.deleteEnvs(ids);
  return s.reply(`已清理 ${ids.length} 个 Keep 账号`);
}

function parseRows(input) {
  const rows = String(input).split(/\r?\n/).map((row) => row.trim()).filter(Boolean);
  if (!rows.length) throw new Error("Token 为空");
  return rows.map((row, index) => {
    const cut = row.indexOf("#");
    const remark = cut >= 0 ? row.slice(0, cut).trim() : `账号${index + 1}`;
    const token = cut >= 0 ? row.slice(cut + 1).trim() : row;
    if (!remark || !token || token.length < 8) throw new Error(`第 ${index + 1} 行格式错误`);
    return { remark, token };
  });
}

function onlyNamed(value, name) {
  const rows = Array.isArray(value) ? value : Array.isArray(value?.data) ? value.data : [];
  return rows.filter((item) => item?.name === name);
}

function ownerKey(sender) {
  return `Keep|${sender.getPlatform()}:${sender.getUserId()}`;
}

function ownedBy(item, owner) {
  return String(item?.remarks || item?.remark || "").startsWith(`${owner}|`);
}

function remarkOf(item) {
  return String(item?.remarks || item?.remark || "").split("|").slice(2).join("|");
}

function envId(item) {
  return item?.id || item?._id;
}

function normalize(raw) {
  const value = raw || {};
  const envName = String(value.env_name || "KEEP_TOKEN").trim();
  if (!/^[A-Za-z_][A-Za-z0-9_]*$/.test(envName)) throw new Error("环境变量名格式错误");
  return { enable: value.enable !== false, qinglongId: Number(value.qinglong_id) || 1, envName };
}

function message(error) {
  return String(error?.message || error).replace(/[\r\n]+/g, " ").slice(0, 300);
}

main();
