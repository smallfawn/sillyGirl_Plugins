// [title: 瑞幸咖啡抽奖]
// [name: ruiXingKaFeiChouJiang]
// [desc: SmallCat微信登录、瑞幸CAPI加密登录、活动校验、抽奖及中奖记录查询]
// [author: sillyGirl]
// [version: v2.1.0]
// [rule: raw ^\s*(瑞幸|瑞幸咖啡|[Ll][Uu][Cc][Kk][Ii][Nn])\s*(查询|抽奖)?\s*$]
// [status: true]
// [admin: false]
// [public: true]
// [priority: 50]
// [class: 工具]
// [icon: https://api.iconify.design/lucide:coffee.svg]
// [origin: plugins/__pycache__/ruiXingKaFeiChouJiang.cpython-314.pyc]
// [depe: ["undici"]]

const { container, plugin, sender: s, user } = require("sillygirl"),
  crypto = require("node:crypto");
let ProxyAgent;
try {
  ({ ProxyAgent } = require("undici"));
} catch (_) {}
const APP_ID = "wx21c7506e98a2fe75",
  APP_VERSION = "916",
  MINI_VERSION = "5572",
  AKV = "lk-wxmp-v5.3.22",
  CID = "230101",
  DK = 1,
  BRAND = "LK001",
  CAPI = "https://capi.lkcoffee.com",
  MKT = "https://mkt.lkcoffee.com",
  UA =
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.75(0x18004b34) NetType/WIFI Language/zh_CN";
const form = new plugin.Form({
  smallcat_id: plugin.Form.integer().title("SmallCat编号").min(1).default(1),
  api_key: plugin.Form.string().title("瑞幸CAPI AES秘钥").description("原PY从运行环境读取；需16/24/32字节").default(""),
  manual_openids: plugin.Form.string().title("手动openid，逗号分隔").default(""),
  account_selector: plugin.Form.string().title("执行账号序号/openid/昵称/全部").default(""),
  activity_no: plugin.Form.string().title("活动编号activityNo").default("CJ202607029027751995"),
  activity_id: plugin.Form.integer().title("活动ID兜底").min(1).default(1367),
  query_only: plugin.Form.boolean().title("仅查询").default(false),
  proxy_url: plugin.Form.string().title("业务代理").default(""),
  request_timeout: plugin.Form.integer().title("请求超时秒").min(5).max(120).default(20),
});
let cfg = {};
function rand(chars, n) {
  let out = "";
  for (let i = 0; i < n; i++) out += chars[Math.floor(Math.random() * chars.length)];
  return out;
}
function md5Words(v) {
  const d = crypto.createHash("md5").update(String(v)).digest(),
    out = [];
  for (let i = 0; i < 16; i += 4) out.push(String(Math.abs(d.readInt32BE(i))));
  return out.join("");
}
function aes(text, decrypt = false) {
  const key = Buffer.from(cfg.api_key);
  if (![16, 24, 32].includes(key.length)) throw new Error("瑞幸CAPI AES秘钥长度应为16/24/32字节");
  if (decrypt) {
    const input = Buffer.from(String(text).replace(/-/g, "+").replace(/_/g, "/"), "base64"),
      d = crypto.createDecipheriv(`aes-${key.length * 8}-ecb`, key, null);
    d.setAutoPadding(true);
    return Buffer.concat([d.update(input), d.final()]).toString();
  }
  const c = crypto.createCipheriv(`aes-${key.length * 8}-ecb`, key, null);
  c.setAutoPadding(true);
  return Buffer.concat([c.update(String(text)), c.final()])
    .toString("base64")
    .replace(/\+/g, "-")
    .replace(/\//g, "_");
}
function payload(data = {}, uid = "") {
  const body = { ...data, miniversion: MINI_VERSION },
    q = aes(JSON.stringify(body)),
    out = { cid: CID, q, dk: DK },
    parts = [`cid=${CID}`, `dk=${DK}`, `q=${q}`];
  if (uid) {
    out.uid = String(uid);
    parts.push(`uid=${uid}`);
  }
  out.sign = md5Words(parts.join(";") + cfg.api_key);
  return out;
}
function unpack(text) {
  const raw = String(text || "").trim();
  if (!raw) return {};
  let value;
  try {
    value = JSON.parse(raw.startsWith("{") ? raw : aes(raw, true));
  } catch (error) {
    throw new Error(`瑞幸响应解密失败：${raw.slice(0, 100)}`);
  }
  if (!value || typeof value !== "object") throw new Error("瑞幸响应不是JSON对象");
  return value;
}
async function dispatcher() {
  if (!cfg.proxy_url || !ProxyAgent) return;
  return new ProxyAgent(/^[a-z]+:\/\//i.test(cfg.proxy_url) ? cfg.proxy_url : `http://${cfg.proxy_url}`);
}
async function req(url, opt = {}) {
  const c = new AbortController(),
    timer = setTimeout(() => c.abort(), Number(cfg.request_timeout) * 1000),
    d = await dispatcher();
  try {
    const headers = { ...(opt.headers || {}) };
    let body;
    if (opt.form) {
      body = new URLSearchParams(opt.form).toString();
      headers["content-type"] ||= "application/x-www-form-urlencoded";
    }
    const r = await fetch(url, { method: opt.method || "GET", headers, body, signal: c.signal, dispatcher: d }),
      text = await r.text();
    if (r.status >= 400) throw new Error(`HTTP ${r.status}：${text.slice(0, 160)}`);
    return {
      text,
      data: (() => {
        try {
          return JSON.parse(text);
        } catch (_) {
          return null;
        }
      })(),
    };
  } finally {
    clearTimeout(timer);
    if (d?.close) await d.close().catch(() => {});
  }
}
function deep(obj, names, pattern) {
  if (typeof obj === "string") {
    try {
      if (/^[[{]/.test(obj.trim())) obj = JSON.parse(obj);
    } catch (_) {}
  }
  if (!obj || typeof obj !== "object") return "";
  for (const [k, v] of Object.entries(obj)) {
    if (
      names.map((x) => x.toLowerCase()).includes(k.toLowerCase()) &&
      typeof v === "string" &&
      (!pattern || pattern.test(v))
    )
      return v;
    const found = deep(v, names, pattern);
    if (found) return found;
  }
  return "";
}
function truthy(obj, key) {
  if (!obj || typeof obj !== "object") return false;
  for (const [k, v] of Object.entries(obj)) {
    if (k.toLowerCase() === key.toLowerCase() && /^(true|1|yes)$/i.test(String(v))) return true;
    if (truthy(v, key)) return true;
  }
  return false;
}
class Runner {
  constructor(account) {
    this.account = account;
    this.openid = String(account.openid || "");
    this.csid = crypto.randomUUID();
    this.blackBox = `uMPHR${Math.floor(Date.now() / 1000)}${rand("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", 12)}`;
    this.did = rand("abcdefghijklmnopqrstuvwxyz0123456789", 32);
    this.h5BlackBox = `uWPHA${Math.floor(Date.now() / 1000)}${rand("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", 12)}`;
    this.deviceId = rand("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/", 48);
    this.userId = "";
    this.uid = "";
    this.lkOpenid = "";
    this.authCode = "";
  }
  capiHeaders(mid = "") {
    const h = {
      "user-agent": UA,
      referer: `https://servicewechat.com/${APP_ID}/${APP_VERSION}/page-frame.html`,
      "content-type": "application/x-www-form-urlencoded",
      "x-lk-csid": this.csid,
      "x-lk-akv": AKV,
      "x-lkwx-sdkversion": "3.16.1",
      "x-lkwx-ostype": "ios",
      "accept-encoding": "gzip, deflate",
      connection: "keep-alive",
    };
    if (mid) h["x-lk-mid"] = String(mid);
    return h;
  }
  async capi(method, path, data = {}, mid = "", uid = "") {
    const p = payload(data, uid),
      url = new URL(`${CAPI}${path}`);
    let opt = { method, headers: this.capiHeaders(mid) };
    if (method === "GET") for (const [k, v] of Object.entries(p)) url.searchParams.set(k, v);
    else opt.form = p;
    const r = unpack((await req(url, opt)).text);
    if (Number(r.code) !== 1)
      throw new Error(`瑞幸接口失败：${r.msg || r.busiCode || JSON.stringify(r).slice(0, 200)}`);
    return r;
  }
  async login(code, phone) {
    const data = { code, isAuthorization: Boolean(phone), blackBox: this.blackBox, did: this.did, deptId: "" };
    if (phone?.iv && phone?.encryptedData) Object.assign(data, { iv: phone.iv, encryptedData: phone.encryptedData });
    if (phone?.phoneCode) data.phoneCode = phone.phoneCode;
    const r = await this.capi("POST", "/resource/m/user/wxminilogin", data),
      content = typeof r.content === "object" ? r.content : {};
    if (content.needAuthorized) throw new Error("NEED_PHONE");
    this.uid = String(r.uid || "");
    this.userId = String(content.userId || "");
    this.lkOpenid = String(content.openid || "");
    if (!this.userId || !this.lkOpenid)
      throw new Error(`瑞幸登录失败：${content.msg || r.msg || "未返回userId/openid"}`);
  }
  async auth() {
    const originUrl = `${MKT}/ladder/draw-series/11rgg68x?activityNo=${cfg.activity_no}&miniversion=${MINI_VERSION}&frommini=mini&brandType=${BRAND}&origin=27&userId=${this.userId}`,
      r = await this.capi(
        "GET",
        "/resource/m/open/getAuthCode",
        { originUrl, openAuthRms: { openId: this.lkOpenid, blackBox: this.blackBox, longitude: "", latitude: "" } },
        this.userId,
        this.uid,
      );
    this.authCode = String(r.content?.code || "");
    if (!this.authCode) throw new Error("getAuthCode未返回authCode");
  }
  h5() {
    return `${MKT}/ladder/draw-series/11rgg68x?activityNo=${cfg.activity_no}&miniversion=${MINI_VERSION}&frommini=mini&brandType=${BRAND}&origin=27&userId=${this.userId}&authCode=${this.authCode}&userType=0`;
  }
  async mkt(path, query) {
    const params = { ...query, _: Date.now() },
      url = new URL(`${MKT}${path}`);
    url.searchParams.set("queryParamsStr", JSON.stringify(params));
    const r = await req(url, {
        headers: {
          "user-agent": `${UA} miniProgram/${APP_ID}`,
          accept: "application/json, text/plain, */*",
          referer: this.h5(),
        },
      }),
      obj = r.data;
    if (!obj || typeof obj !== "object") throw new Error("H5接口未返回JSON");
    if (![1, null, undefined].includes(obj.code) && !obj.success)
      throw new Error(String(obj.msg || obj.busiCode || JSON.stringify(obj).slice(0, 200)));
    return obj;
  }
  async execute(code, phone, queryOnly) {
    await this.login(code, phone);
    await this.auth();
    await req(this.h5(), { headers: { "user-agent": `${UA} miniProgram/${APP_ID}` } });
    const checked = await this.mkt("/ladder/capi/resource/m/open/check", { loading: false, code: this.authCode });
    if (!checked.content?.checked) throw new Error(checked.msg || "活动校验未通过");
    const detail =
        (
          await this.mkt("/ladder/skcapi/resource/bff/v2/lotteryDraw/detail", {
            activityId: "",
            activityNo: cfg.activity_no,
            handleMsg: false,
          })
        ).content || {},
      activityId = detail.activityId || cfg.activity_id,
      status = detail.activityLotteryStatus,
      records = await this.records();
    if (queryOnly) return `活动：${cfg.activity_no}\nactivityId=${activityId}，状态=${status}\n${recordText(records)}`;
    const draw =
        (
          await this.mkt("/ladder/skcapi/resource/m/lotteryDraw/action", {
            blackBox: this.h5BlackBox,
            deviceId: this.deviceId,
            activityId: Number(activityId),
            activityNo: cfg.activity_no,
            origin: 14,
            handleMsg: false,
            version: Number(MINI_VERSION),
          })
        ).content || {},
      message = draw.prizeName || draw.notHitPrizeReasonMsg || draw.msg || "抽奖完成";
    return `${message}\n${recordText(await this.records())}`;
  }
  async records() {
    const r = await this.mkt("/ladder/skcapi/resource/bff/lotteryDraw/memberLotteryRecord", {
      activityNo: cfg.activity_no,
      pageIndex: 0,
      pageSize: 100,
    });
    return Array.isArray(r.content) ? r.content : [];
  }
}
function recordText(rows) {
  if (!rows.length) return "暂无中奖记录";
  return rows
    .slice(0, 20)
    .map(
      (x, i) =>
        `${i + 1}. ${x.prizeName || x.awardName || x.name || x.notHitPrizeReasonMsg || "记录"}${x.createTime || x.lotteryTime ? `｜${x.createTime || x.lotteryTime}` : ""}`,
    )
    .join("\n");
}
async function authorized() {
  const manual = String(cfg.manual_openids || "")
    .split(/[,，\s]+/)
    .filter(Boolean);
  if (manual.length) return manual.map((openid) => ({ openid, nickname: openid }));
  const platform = String(await s.getPlatform()),
    id = String(await s.getUserId()),
    rows = await user.getUserList(),
    out = [];
  for (const x of Array.isArray(rows) ? rows : []) {
    if (x?.disabled || !x?.authorized) continue;
    if (String(x?.bindings?.[platform] || "") !== id && !(await s.isAdmin())) continue;
    for (const openid of x?.bindings?.smallcat_openids || [])
      out.push({
        openid: String(openid),
        nickname: x.nickname || x.name || String(openid),
        proxyUrl: x.proxyUrl || "",
      });
  }
  return out;
}
async function choose(rows) {
  if (!rows.length) throw new Error("没有可用SmallCat微信账号");
  const sel = String(cfg.account_selector || "").trim();
  if (!sel) return [rows[0]];
  if (sel === "全部") return rows;
  if (/^\d+$/.test(sel) && rows[Number(sel) - 1]) return [rows[Number(sel) - 1]];
  const found = rows.find((x) => x.openid === sel || String(x.nickname).includes(sel));
  if (!found) throw new Error("执行账号选择无效");
  return [found];
}
async function getCode(sc, openid) {
  const raw = await sc.getCode({ openid, appid: APP_ID }),
    code = deep(raw, ["code", "wxcode", "wx_code", "loginCode"], /^[0-9A-Za-z_-]{8,4096}$/);
  if (!code) throw new Error(`SmallCat wx.login取码失败：${JSON.stringify(raw).slice(0, 300)}`);
  return code;
}
async function getPhone(sc, openid) {
  const raw = await sc.getPhoneNumber({ openid, appid: APP_ID }),
    iv = deep(raw, ["iv"], /.{8,4096}/),
    encryptedData = deep(raw, ["encryptedData", "encrypted_data"], /.{8,16384}/),
    phoneCode = deep(raw, ["phoneCode", "phone_code", "code"], /^[0-9A-Za-z_-]{8,4096}$/);
  if (iv && encryptedData) return { iv, encryptedData, phoneCode };
  if (phoneCode) return { iv: "", encryptedData: "", phoneCode };
  throw new Error(`${truthy(raw, "need_auth") ? "need_auth=true；" : ""}SmallCat手机号授权数据缺失`);
}
async function main() {
  try {
    cfg = (await form.get()) || {};
    if (!cfg.api_key) throw new Error("请在插件配置填写瑞幸CAPI AES秘钥；原PY从运行环境读取，空值会导致加密请求失效");
    const command = String((await s.getMsg()) || ""),
      queryOnly = Boolean(cfg.query_only) || /查询/i.test(command),
      sc = new container.SmallCat({ id: Number(cfg.smallcat_id) || 1 }),
      rows = await choose(await authorized()),
      out = [];
    for (const account of rows) {
      try {
        let runner = new Runner(account),
          code = await getCode(sc, account.openid);
        try {
          out.push(`${account.nickname}：${await runner.execute(code, null, queryOnly)}`);
        } catch (error) {
          if (!/NEED_PHONE|手机号授权|信息异常/.test(error.message)) throw error;
          const phone = await getPhone(sc, account.openid);
          runner = new Runner(account);
          code = await getCode(sc, account.openid);
          out.push(`${account.nickname}：${await runner.execute(code, phone, queryOnly)}`);
        }
      } catch (error) {
        out.push(`${account.nickname || account.openid}：${error.message}`);
      }
    }
    return s.reply(out.join("\n---\n"));
  } catch (error) {
    return s.reply(`瑞幸咖啡抽奖执行失败：${error?.message || error}`);
  }
}
main();
