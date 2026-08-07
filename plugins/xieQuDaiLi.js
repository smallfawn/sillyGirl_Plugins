// [title: 携趣代理]
// [name: xieQuDaiLi]
// [language: javascript]
// [class: 工具]
// [author: sillyGirl]
// [version: v2.0.0]
// [public: true]
// [disable: false]
// [admin: true]
// [rule: ^携趣$|^携趣删白$|^携趣余量$|^携趣管理$|^携趣配置$|^xqfk$]
// [icon: https://api.iconify.design/lucide:bot.svg]
// [description: 调用携趣控制台生成的提取、余量和删白 API]
// [depe: []]

const { plugin, sender: s } = require("sillygirl");

const config = new plugin.Form({
  enable: plugin.Form.boolean().title("是否启用").default(true),
  extract_url: plugin.Form.string().title("代理提取 URL").default(""),
  balance_url: plugin.Form.string().title("余量查询 URL").default(""),
  delete_white_url: plugin.Form.string().title("删除白名单 URL").default(""),
});

async function main() {
  const cfg = await config.get() || {};
  if (cfg.enable === false) return s.reply("携趣代理插件未启用");
  if (!s.isAdmin()) return s.reply("仅管理员可用");
  const content = String(s.getContent() || "").trim();
  if (/管理|配置|xqfk/i.test(content)) {
    return s.reply([
      `代理提取：${cfg.extract_url ? "已配置" : "未配置"}`,
      `余量查询：${cfg.balance_url ? "已配置" : "未配置"}`,
      `删除白名单：${cfg.delete_white_url ? "已配置" : "未配置"}`,
    ].join("\n"));
  }
  const url = content === "携趣余量" ? cfg.balance_url : content === "携趣删白" ? cfg.delete_white_url : cfg.extract_url;
  if (!url) return s.reply("请先在插件配置填写对应的携趣 API URL");
  try {
    const response = await fetch(String(url), { headers: { accept: "application/json,text/plain,*/*" } });
    const text = await response.text();
    if (!response.ok) throw new Error(`HTTP ${response.status}: ${text.slice(0, 200)}`);
    return s.reply(`携趣返回：\n${text.slice(0, 1800)}`);
  } catch (error) {
    return s.reply(`携趣请求失败：${message(error)}`);
  }
}

function message(error) {
  return String(error?.message || error).replace(/[\r\n]+/g, " ").slice(0, 300);
}

main();
