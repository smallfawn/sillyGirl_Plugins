// [title: 众安健康]
// [name: zhongAnJianKang]
// [language: javascript]
// [class: 任务]
// [author: 97610325]
// [version: v1.7.0]
// [public: true]
// [disable: false]
// [admin: false]
// [rule: ^众安管理$|^管理众安$|^众安查询$|^查询众安$|^众安登录$|^登录众安$|^众安$|^众安清理$|^清理众安$]
// [icon: https://nos.netease.com/ysf/82b362badc596b99e5c3ad437973a560.jpg]
// [description: 众安健康 Token 绑定、青龙同步、账号查询与清理]
// [depe: []]

const { container, plugin, sender: s } = require("sillygirl");

const config = new plugin.Form({
  enable: plugin.Form.boolean().title("是否启用").default(true),
  qinglong_id: plugin.Form.number().title("青龙容器编号").default(1),
  env_name: plugin.Form.string().title("脚本环境变量名").default("ZHONGAN_TOKEN"),
});

async function main() {
  try {
    const cfg = normalize(await config.get());
    if (!cfg.enable) return s.reply("众安健康插件未启用");
    const content = String(s.getContent() || "").trim();
    const ql = new container.QingLong({ id: cfg.qinglongId });

    if (/查询|管理/.test(content)) return showAccounts(ql, cfg.envName);
    if (/清理/.test(content)) return removeAccounts(ql, cfg.envName);
    if (/登录/.test(content)) {
      s.reply("请发送众安 Token，格式：备注#Token；多账号可换行，输入 q 取消。");
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
    return s.reply("指令：众安登录 / 众安查询 / 众安清理");
  } catch (error) {
    return s.reply(`众安健康处理失败：${message(error)}`);
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
    return replySender.reply(`众安账号同步完成：新增 ${created}，更新 ${updated}`);
  } catch (error) {
    return replySender.reply(`众安提交失败：${message(error)}`);
  }
}

async function showAccounts(ql, envName) {
  const owner = ownerKey(s);
  const all = onlyNamed(await ql.getEnvs({ searchValue: envName }), envName);
  const visible = s.isAdmin() ? all : all.filter((item) => ownedBy(item, owner));
  if (!visible.length) return s.reply("没有找到你的众安健康账号");
  return s.reply([`众安健康账号：${visible.length} 个`, ...visible.map((item, index) => `${index + 1}. ${remarkOf(item) || "未备注"}${item.status ? "（已禁用）" : ""}`)].join("\n"));
}

async function removeAccounts(ql, envName) {
  const owner = ownerKey(s);
  const all = onlyNamed(await ql.getEnvs({ searchValue: envName }), envName);
  const ids = all.filter((item) => s.isAdmin() || ownedBy(item, owner)).map(envId).filter(Boolean);
  if (!ids.length) return s.reply("没有可清理的众安健康账号");
  await ql.deleteEnvs(ids);
  return s.reply(`已清理 ${ids.length} 个众安健康账号`);
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
  return `众安|${sender.getPlatform()}:${sender.getUserId()}`;
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
  const envName = String(value.env_name || "ZHONGAN_TOKEN").trim();
  if (!/^[A-Za-z_][A-Za-z0-9_]*$/.test(envName)) throw new Error("环境变量名格式错误");
  return { enable: value.enable !== false, qinglongId: Number(value.qinglong_id) || 1, envName };
}

function message(error) {
  return String(error?.message || error).replace(/[\r\n]+/g, " ").slice(0, 300);
}

main();
