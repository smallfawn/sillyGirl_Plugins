// [title: 夸克推广]
// [name: kuaKeTuiGuang]
// [language: javascript]
// [class: 任务]
// [author: sillyGirl]
// [version: v2.0.0]
// [public: true]
// [disable: false]
// [admin: false]
// [rule: ^我要看(.+)$|^夸克清理$|^夸克登录$]
// [icon: https://api.iconify.design/lucide:bot.svg]
// [description: 生成限定夸克网盘分享域名的资源检索入口]
// [depe: []]

const { plugin, sender: s } = require("sillygirl");

const config = new plugin.Form({
  enable: plugin.Form.boolean().title("是否启用").default(true),
  search_url: plugin.Form.string().title("搜索地址模板").description("使用 {query} 代入 URL 编码后的关键词").default("https://www.bing.com/search?q=site%3Apan.quark.cn%2Fs+{query}"),
});

async function main() {
  const cfg = await config.get() || {};
  if (cfg.enable === false) return s.reply("夸克推广插件未启用");
  const content = String(s.getContent() || "").trim();
  if (content === "夸克登录") return s.reply("夸克资源搜索不需要登录。");
  if (content === "夸克清理") return s.reply("当前实现不保存搜索记录。");
  const query = String(s.param(1) || content.replace(/^我要看/, "")).trim();
  if (!query) return s.reply("格式：我要看资源名");
  const template = String(cfg.search_url || "").trim();
  if (!template.includes("{query}")) return s.reply("搜索地址模板缺少 {query}");
  return s.reply(`夸克资源检索：${query}\n${template.replaceAll("{query}", encodeURIComponent(query))}`);
}

main();
