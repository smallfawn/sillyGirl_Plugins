// [title: ipChange]
// [name: ipchange]
// [language: javascript]
// [class: 工具]
// [author: smallfawn]
// [version: v1.0.1]
// [public: true]
// [admin: true]
// [rule: ^(IP|IP查询)$]
// [priority: 0]
// [icon: https://api.iconify.design/lucide:bot.svg]
// [description: IP变动通知]
// [depe: []]
// [origin: smallfawn/Bncr_Plugins]

const http = require("http");
const https = require("https");
const {
  sender: s,
  Bucket,
  console,
} = require('sillygirl');

const getIPApi = "https://4.ipw.cn/";
const db = new Bucket("smallfawnDB");

function requestText(url, timeout = 10000) {
  return new Promise((resolve, reject) => {
    const client = url.startsWith("https:") ? https : http;
    const req = client.get(url, (res) => {
      let data = "";
      res.setEncoding("utf8");
      res.on("data", (chunk) => {
        data += chunk;
      });
      res.on("end", () => {
        if (res.statusCode < 200 || res.statusCode >= 300) {
          reject(new Error(`HTTP ${res.statusCode}`));
          return;
        }
        resolve(data);
      });
    });
    req.setTimeout(timeout, () => {
      req.destroy(new Error("请求超时"));
    });
    req.on("error", reject);
  });
}

async function getIP() {
  return String(await requestText(getIPApi)).trim();
}

async function checkIPChange() {
  const newIP = await getIP();
  if (!newIP) return "IP查询失败";

  const oldIP = await db.get("ip", "");
  if (!oldIP) {
    await db.set("ip", newIP);
    return `首次记录IP：${newIP}`;
  }

  if (oldIP !== newIP) {
    await db.set("ip", newIP);
    return `IP已变动，当前IP为：${newIP}`;
  }

  return `当前IP为：${newIP}`;
}

async function main() {
  const message = await checkIPChange();
  await s.reply(message);
}

main().catch((error) => {
  console.error(error);
});
