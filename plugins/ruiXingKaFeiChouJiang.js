// [title: 瑞幸咖啡抽奖]
// [name: ruiXingKaFeiChouJiang]
// [language: javascript]
// [class: 工具]
// [author: sillyGirl]
// [version: v2.0.0]
// [public: true]
// [disable: false]
// [admin: false]
// [rule: raw ^\s*(瑞幸|瑞幸咖啡|[Ll][Uu][Cc][Kk][Ii][Nn])\s*(查询|抽奖)?\s*$]
// [smallcat: true]
// [icon: https://api.iconify.design/lucide:bot.svg]
// [description: 从当前用户授权的 SmallCat 微信账号获取 wx.login CODE，并可提交业务接口和同步青龙]
// [depe: []]

const { container, plugin, sender: s, user } = require("sillygirl");

const config = new plugin.Form({
  enable: plugin.Form.boolean().title("是否启用").default(true),
  smallcat_id: plugin.Form.number().title("SmallCat 编号").default(1),
  appid: plugin.Form.string().title("目标小程序 AppID").default("wx21c7506e98a2fe75"),
  business_url: plugin.Form.string().title("业务接口 URL").description("留空时仅返回 wx.login CODE；填写后 POST code/openid/action").default(""),
  qinglong_id: plugin.Form.number().title("青龙容器编号").default(1),
  env_name: plugin.Form.string().title("青龙环境变量名").default("LUCKIN_TOKEN"),
});

async function main() {
  const cfg = normalize(await config.get());
  if (!cfg.enable) return s.reply("瑞幸咖啡抽奖插件未启用");
  try {
    if (!/^wx[0-9a-f]{16}$/i.test(cfg.appid)) throw new Error("请先在插件配置填写有效的小程序 AppID");
    const openids = await authorizedOpenids();
    if (!openids.length) throw new Error("当前用户没有授权 SmallCat 微信账号");
    const smallcat = new container.SmallCat({ id: cfg.smallcatId });
    const action = String(s.getContent() || "").trim();
    const rows = [];
    for (const openid of openids) {
      const result = await smallcat.getCode({ openid, appid: cfg.appid });
      if (result?.status === false) throw new Error(result.message || "SmallCat 取 CODE 失败");
      const code = result?.data?.code || result?.data?.wxCode || result?.code || result?.wxCode;
      if (!code) throw new Error(`SmallCat 返回缺少 CODE：${openid}`);
      const value = cfg.businessUrl ? await callBusiness(cfg.businessUrl, { code, openid, action }) : code;
      if (cfg.businessUrl) await upsertEnv(cfg, openid, value);
      rows.push(`${openid}：${String(value).slice(0, 500)}`);
    }
    return s.reply(["瑞幸咖啡抽奖处理完成", ...rows].join("\n"));
  } catch (error) {
    return s.reply(`瑞幸咖啡抽奖处理失败：${message(error)}`);
  }
}

async function authorizedOpenids() {
  const platform = String(s.getPlatform());
  const userId = String(s.getUserId());
  const values = await user.getUserList();
  const found = new Set();
  for (const item of Array.isArray(values) ? values : []) {
    if (item?.disabled || !item?.authorized) continue;
    if (String(item?.bindings?.[platform] || "") !== userId && !s.isAdmin()) continue;
    for (const openid of item?.bindings?.smallcat_openids || []) if (openid) found.add(String(openid));
  }
  return [...found];
}

async function callBusiness(url, payload) {
  const response = await fetch(url, { method: "POST", headers: { accept: "application/json", "content-type": "application/json" }, body: JSON.stringify(payload) });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data?.message || `HTTP ${response.status}`);
  return data?.token || data?.access_token || data?.data?.token || data?.data?.access_token || JSON.stringify(data?.data ?? data);
}

async function upsertEnv(cfg, openid, value) {
  const ql = new container.QingLong({ id: cfg.qinglongId });
  const values = await ql.getEnvs({ searchValue: cfg.envName });
  const rows = Array.isArray(values) ? values : Array.isArray(values?.data) ? values.data : [];
  const remarks = `ruiXingKaFeiChouJiang|${s.getPlatform()}:${s.getUserId()}|${openid}`;
  const current = rows.find((item) => item?.name === cfg.envName && String(item?.remarks || "") === remarks);
  if (current) return ql.updateEnv({ id: current.id ?? current._id, name: cfg.envName, value: String(value), remarks });
  return ql.createEnv({ name: cfg.envName, value: String(value), remarks });
}

function normalize(raw) {
  const value = raw || {};
  return { enable: value.enable !== false, smallcatId: Number(value.smallcat_id) || 1, appid: String(value.appid || "wx21c7506e98a2fe75").trim(), businessUrl: String(value.business_url || "").trim(), qinglongId: Number(value.qinglong_id) || 1, envName: String(value.env_name || "LUCKIN_TOKEN").trim() || "LUCKIN_TOKEN" };
}
function message(error) { return String(error?.message || error).replace(/[\r\n]+/g, " ").slice(0, 300); }

main();
