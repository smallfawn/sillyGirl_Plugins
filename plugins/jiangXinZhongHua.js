// [title: 匠心中华]
// [name: jiangXinZhongHua]
// [language: javascript]
// [class: 任务]
// [author: huawei]
// [version: v2.0.0]
// [public: true]
// [disable: false]
// [admin: false]
// [rule: ^匠心登录$|^登录匠心$|^匠心管理$|^管理匠心$|^匠心查询$|^查询匠心$|^匠心物流$|^物流匠心$|^匠心兑换$|^兑换匠心$|^匠心批量兑换$|^匠心批量地址$|^匠心$|^匠心教程$|^匠心清理$|^匠心上传$|^匠心地址$|^匠心注销$|^匠心CK$]
// [icon: https://api.iconify.design/lucide:apple.svg]
// [description: 匠心中华凭证绑定、青龙同步、账号查询与清理]
// [depe: []]

const { container, plugin, sender: s } = require("sillygirl");

const config = new plugin.Form({
  enable: plugin.Form.boolean().title("是否启用").default(true),
  qinglong_id: plugin.Form.number().title("青龙容器编号").default(1),
  env_name: plugin.Form.string().title("脚本环境变量名").default("JIANGXIN_CK"),
});

async function main() {
  try {
    const cfg = normalize(await config.get());
    if (!cfg.enable) return s.reply("匠心中华插件未启用");
    const content = String(s.getContent() || "").trim();
    const ql = new container.QingLong({ id: cfg.qinglongId });
    if (/教程|说明/.test(content)) return s.reply("发送登录指令后提交原始凭证；可用 备注::凭证 添加备注，多账号换行。");
    if (/查询|管理|检测|统计|订单查询|上传|同步|刷新|后台/.test(content)) return showAccounts(ql, cfg.envName);
    if (/清理|删除/.test(content)) return removeAccounts(ql, cfg.envName);
    if (/登录|登陆|绑定|上车|提交|CK|ck/.test(content)) {
      s.reply("请发送原始账号凭证；可用 备注::凭证 添加备注，多账号换行，输入 q 取消。");
      return s.listen({
        rules: ["raw ^([\\s\\S]+)$"], timeout: 60000,
        user_id: s.getUserId(), chat_id: s.getChatId(),
        handle: (next) => {
          const value = String(next.param(1) || "").trim();
          if (/^q$/i.test(value)) return "已取消";
          return saveAccounts(ql, cfg.envName, value, next);
        },
      });
    }
    return s.reply("匠心中华：请使用登录、查询、管理或清理指令");
  } catch (error) {
    return s.reply(`匠心中华处理失败：${message(error)}`);
  }
}

async function saveAccounts(ql, envName, input, replySender) {
  try {
    const rows = parseRows(input);
    const owner = ownerKey(replySender);
    const current = onlyNamed(await ql.getEnvs({ searchValue: envName }), envName);
    let created = 0, updated = 0;
    for (const row of rows) {
      const existing = current.find((item) => ownedBy(item, owner) && (remarkOf(item) === row.remark || item.value === row.value));
      const remarks = `${owner}|${row.remark}`;
      if (existing) {
        await ql.updateEnv({ id: envId(existing), name: envName, value: row.value, remarks });
        updated += 1;
      } else {
        await ql.createEnv({ name: envName, value: row.value, remarks });
        created += 1;
      }
    }
    return replySender.reply(`匠心中华同步完成：新增 ${created}，更新 ${updated}`);
  } catch (error) {
    return replySender.reply(`匠心中华提交失败：${message(error)}`);
  }
}

async function showAccounts(ql, envName) {
  const owner = ownerKey(s);
  const all = onlyNamed(await ql.getEnvs({ searchValue: envName }), envName);
  const visible = s.isAdmin() ? all : all.filter((item) => ownedBy(item, owner));
  if (!visible.length) return s.reply("没有找到你的匠心中华账号");
  return s.reply([`匠心中华账号：${visible.length} 个`, ...visible.map((item, index) => `${index + 1}. ${remarkOf(item) || "未备注"}${item.status ? "（已禁用）" : ""}`)].join("\n"));
}

async function removeAccounts(ql, envName) {
  const owner = ownerKey(s);
  const all = onlyNamed(await ql.getEnvs({ searchValue: envName }), envName);
  const ids = all.filter((item) => s.isAdmin() || ownedBy(item, owner)).map(envId).filter(Boolean);
  if (!ids.length) return s.reply("没有可清理的匠心中华账号");
  await ql.deleteEnvs(ids);
  return s.reply(`已清理 ${ids.length} 个匠心中华账号`);
}

function parseRows(input) {
  const values = String(input).split(/\r?\n/).map((row) => row.trim()).filter(Boolean);
  if (!values.length) throw new Error("凭证为空");
  return values.map((value, index) => {
    const cut = value.indexOf("::");
    const remark = cut >= 0 ? value.slice(0, cut).trim() : `账号${index + 1}`;
    const payload = cut >= 0 ? value.slice(cut + 2).trim() : value;
    if (!remark || !payload) throw new Error(`第 ${index + 1} 行格式错误`);
    return { remark, value: payload };
  });
}

function onlyNamed(value, name) {
  const rows = Array.isArray(value) ? value : Array.isArray(value?.data) ? value.data : [];
  return rows.filter((item) => item?.name === name);
}
function ownerKey(sender) { return "jiangXinZhongHua|" + sender.getPlatform() + ":" + sender.getUserId(); }
function ownedBy(item, owner) { return String(item?.remarks || item?.remark || "").startsWith(owner + "|"); }
function remarkOf(item) { return String(item?.remarks || item?.remark || "").split("|").slice(2).join("|"); }
function envId(item) { return item?.id || item?._id; }
function normalize(raw) {
  const value = raw || {};
  const envName = String(value.env_name || "JIANGXIN_CK").trim();
  if (!/^[A-Za-z_][A-Za-z0-9_]*$/.test(envName)) throw new Error("环境变量名格式错误");
  return { enable: value.enable !== false, qinglongId: Number(value.qinglong_id) || 1, envName };
}
function message(error) { return String(error?.message || error).replace(/[\r\n]+/g, " ").slice(0, 300); }

main();
