// [title: m096_太平洋汽车]
// [name: m096TaiPingYangQiChe]
// [language: javascript]
// [class: 任务]
// [author: sillyGirl]
// [version: v1.5.0]
// [public: true]
// [disable: false]
// [admin: false]
// [rule: ^太平洋(.*)|(.*)洋汽车$]
// [icon: https://api.iconify.design/lucide:bot.svg]
// [description: 接收账号#密码#openid并同步到青龙环境变量]
// [depe: []]

const { container, plugin, sender: s } = require("sillygirl");

const config = new plugin.Form({
  enable: plugin.Form.boolean().title("是否启用").default(true),
  qinglong_id: plugin.Form.number().title("青龙容器编号").default(1),
  env_name: plugin.Form.string().title("脚本环境变量名").default("PC_AUTO"),
});

async function main() {
  const cfg = normalize(await config.get());
  if (!cfg.enable) return s.reply("太平洋汽车插件未启用");
  const content = String(s.getContent() || "").trim();
  const ql = new container.QingLong({ id: cfg.qinglongId });

  try {
    if (/查询|管理/.test(content)) return showAccounts(ql, cfg.envName);
    if (/清理|删除/.test(content)) return removeOwnAccounts(ql, cfg.envName);

    const inline = content.match(/^太平洋(?:登录|登陆|提交)?\s+(.+)$/s)?.[1]?.trim();
    if (inline) return saveAccounts(ql, cfg.envName, inline, s);
    if (/登录|登陆|提交/.test(content)) {
      s.reply("请发送：账号#密码#openid；多账号可换行，输入 q 取消。");
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

    return s.reply("指令：太平洋登录 / 太平洋查询 / 太平洋清理");
  } catch (error) {
    return s.reply(`太平洋汽车处理失败：${message(error)}`);
  }
}

async function saveAccounts(ql, envName, input, replySender) {
  try {
    const accounts = parseAccounts(input);
    const current = onlyNamed(await ql.getEnvs({ searchValue: envName }), envName);
    const owner = ownerKey(replySender);
    let created = 0;
    let updated = 0;

    for (const account of accounts) {
      const value = `${account.name}#${account.password}#${account.openid}`;
      const existing = current.find((item) => firstField(item.value) === account.name && ownedBy(item, owner));
      if (existing) {
        await ql.updateEnv({ id: envId(existing), name: envName, value, remarks: owner });
        updated += 1;
      } else {
        await ql.createEnv({ name: envName, value, remarks: owner });
        created += 1;
      }
    }
    return replySender.reply(`太平洋汽车提交完成：新增 ${created}，更新 ${updated}`);
  } catch (error) {
    return replySender.reply(`提交失败：${message(error)}`);
  }
}

async function showAccounts(ql, envName) {
  const owner = ownerKey(s);
  const all = onlyNamed(await ql.getEnvs({ searchValue: envName }), envName);
  const visible = s.isAdmin() ? all : all.filter((item) => ownedBy(item, owner));
  if (!visible.length) return s.reply("没有找到你的太平洋汽车账号");
  return s.reply([`太平洋汽车账号：${visible.length} 个`, ...visible.map((item, index) => `${index + 1}. ${mask(firstField(item.value))}${item.status ? "（已禁用）" : ""}`)].join("\n"));
}

async function removeOwnAccounts(ql, envName) {
  const owner = ownerKey(s);
  const all = onlyNamed(await ql.getEnvs({ searchValue: envName }), envName);
  const targets = all.filter((item) => s.isAdmin() || ownedBy(item, owner));
  const ids = targets.map(envId).filter(Boolean);
  if (!ids.length) return s.reply("没有可清理的太平洋汽车账号");
  await ql.deleteEnvs(ids);
  return s.reply(`已清理 ${ids.length} 个太平洋汽车账号`);
}

function parseAccounts(input) {
  const rows = String(input).split(/\r?\n/).map((row) => row.trim()).filter(Boolean);
  if (!rows.length) throw new Error("账号数据为空");
  return rows.map((row, index) => {
    const [name, password, openid, ...extra] = row.split("#").map((part) => part.trim());
    if (!name || !password || !openid || extra.length) throw new Error(`第 ${index + 1} 行格式应为：账号#密码#openid`);
    return { name, password, openid };
  });
}

function onlyNamed(value, name) {
  const rows = Array.isArray(value) ? value : Array.isArray(value?.data) ? value.data : [];
  return rows.filter((item) => item?.name === name);
}

function ownerKey(sender) {
  return `太平洋汽车|${sender.getPlatform()}:${sender.getUserId()}`;
}

function ownedBy(item, owner) {
  return String(item?.remarks || item?.remark || "") === owner;
}

function envId(item) {
  return item?.id || item?._id;
}

function firstField(value) {
  return String(value || "").split("#", 1)[0];
}

function mask(value) {
  const text = String(value || "");
  if (text.length <= 4) return `${text[0] || "*"}***`;
  return `${text.slice(0, 2)}****${text.slice(-2)}`;
}

function normalize(raw) {
  const value = raw || {};
  const envName = String(value.env_name || "PC_AUTO").trim();
  if (!/^[A-Za-z_][A-Za-z0-9_]*$/.test(envName)) throw new Error("环境变量名格式错误");
  return { enable: value.enable !== false, qinglongId: Number(value.qinglong_id) || 1, envName };
}

function message(error) {
  return String(error?.message || error).replace(/[\r\n]+/g, " ").slice(0, 300);
}

main();
