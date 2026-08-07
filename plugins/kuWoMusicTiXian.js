// [title: 酷我Music提现]
// [name: kuWoMusicTiXian]
// [language: javascript]
// [class: 任务]
// [author: sky2022]
// [version: v2.0.0]
// [public: true]
// [disable: false]
// [admin: false]
// [rule: ^(酷我酷我次数检测|酷我次数迁移)$]
// [icon: https://api.iconify.design/lucide:apple.svg]
// [description: 使用 SillyGirl 青龙内联客户端查找并运行对应业务任务]
// [depe: []]

const { container, plugin, sender: s } = require("sillygirl");

const config = new plugin.Form({
  enable: plugin.Form.boolean().title("是否启用").default(true),
  qinglong_id: plugin.Form.number().title("青龙容器编号").default(1),
  task_keyword: plugin.Form.string().title("青龙任务关键词").default("酷我Music提现"),
});

async function main() {
  try {
    const cfg = normalize(await config.get());
    if (!cfg.enable) return s.reply("酷我Music提现插件未启用");
    const ql = new container.QingLong({ id: cfg.qinglongId });
    const content = String(s.getContent() || "").trim();
    const tasks = await findTasks(ql, [content, cfg.taskKeyword]);
    if (!tasks.length) return s.reply(`未找到青龙任务：${cfg.taskKeyword}`);
    const ids = tasks.map((task) => task.id ?? task._id).filter((id) => id !== undefined && id !== null);
    if (!ids.length) throw new Error("匹配任务缺少 id");
    await ql.request("PUT", "/crons/run", ids);
    return s.reply(["酷我Music提现任务已触发", ...tasks.map((task) => `• ${task.name || task.command || task.id}`)].join("\n"));
  } catch (error) {
    return s.reply(`酷我Music提现执行失败：${message(error)}`);
  }
}

async function findTasks(ql, keywords) {
  const found = new Map();
  for (const keyword of [...new Set(keywords.map((value) => String(value || "").trim()).filter(Boolean))]) {
    const response = await ql.request("GET", "/crons", null, { searchValue: keyword });
    for (const task of unwrapList(response)) {
      const id = task?.id ?? task?._id;
      if (id === undefined || id === null) continue;
      const text = `${task.name || ""}\n${task.command || ""}`;
      if (text.includes(keyword) || keyword === String(keywords.at(-1))) found.set(String(id), task);
    }
  }
  return [...found.values()];
}

function unwrapList(value) {
  let current = value;
  for (let index = 0; index < 4 && current && !Array.isArray(current); index += 1) current = current.data ?? current.items ?? current.list;
  return Array.isArray(current) ? current : [];
}
function normalize(raw) {
  const value = raw || {};
  return { enable: value.enable !== false, qinglongId: Number(value.qinglong_id) || 1, taskKeyword: String(value.task_keyword || "酷我Music提现").trim() || "酷我Music提现" };
}
function message(error) { return String(error?.message || error).replace(/[\r\n]+/g, " ").slice(0, 300); }

main();
