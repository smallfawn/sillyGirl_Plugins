//[title: 网抑云热评]
//[name: wangYiYunRePing]
//[language: nodejs]
//[class: 娱乐]
//[author: qw21560]
//[version: v1.1.0]
//[public: true]
//[disable: false]
//[admin: false]
//[rule: ^网抑云$]
//[icon: https://api.iconify.design/lucide:music.svg]
//[description: 随机返回一条网易云热评]
// [depe: []]

const { sender: s } = require("sillygirl");

async function main() {
  const response = await fetch("http://api.yujn.cn/api/wyrp.php", {
    signal: AbortSignal.timeout(10000),
  });
  if (!response.ok) throw new Error(`热评接口 HTTP ${response.status}`);
  const text = (await response.text()).trim();
  await s.reply(text || "热评接口返回为空");
}

main().catch((error) => s.reply(`获取热评失败：${error.message}`));
