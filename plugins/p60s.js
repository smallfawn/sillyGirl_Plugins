// [title: 60s]
// [name: p60s]
// [language: nodejs]
// [class: 任务]
// [author: XiaoBo_]
// [version: v1.1.2]
// [public: true]
// [disable: false]
// [admin: false]
// [rule: ^(早报|新闻|60秒|60s)$|^(文字早报|文本早报)$|^(图文早报|图片早报)$|^早报数据$]
// [cron: 30 7 * * *]
// [icon: https://img.icons8.com/fluency/96/news.png]
// [description: 📰 60秒早报插件；📋 每日60秒早报插件，获取当日最新资讯；支持图文和纯文字两种展示方式，每天早上7:30自动推送；📝 使用命令：；• 早报 / 新闻 / 60秒 / 60s - 获取早报（根据配置显示图文或文字）；• 文字早报 / 文本早报 - 强制获取纯文字格式；• 图文早报 / 图片早报 - 强制获取图文格式；📊 数据来源：微信公众号：《每天100秒读懂世界》，官方权威数据，稳定实时]
// [depe: []]

const { sender } = require('sillygirl');

(async () => {
  const sgApi = require('sillygirl');
  const { sender: runtimeSender, Bucket: SGBucket, Adapter: SGAdapter } = sgApi;
  const { execFileSync } = require('node:child_process');
  const nodeCrypto = require('node:crypto');
  const __pending = [], __bucketCache = Object.create(null);
  let __userId = '', __userName = '', __platform = '', __content = '', __chatId = '', __isAdmin = false;
  function __bucketName(v) { return String(v || ''); }
  function __key(v) { return String(v || ''); }
  function __detectBuckets() {
    const names = new Set(['otto', 'qls']);
    try {
      const src = require('node:fs').readFileSync(process.argv[1] || '', 'utf8'); let m;
      for (const re of [/\b(?:bucketGet|bucketSet|bucketDel|bucketAllKeys|bucketKeys)\s*\(\s*['\"]([^'\"]+)['\"]/g, /\b(?:get|set|del)\s*\(\s*['\"]([^'\".]+)\.[^'\"]+['\"]/g]) while ((m = re.exec(src))) names.add(m[1]);
    } catch (_) {}
    return Array.from(names);
  }
  for (const name of __detectBuckets()) { try { __bucketCache[name] = await new SGBucket(name).getAll() || {}; } catch (_) { __bucketCache[name] ||= {}; } }
  if (runtimeSender) {
    __userId = await runtimeSender.getUserId().catch(() => ''); __userName = await runtimeSender.getUserName().catch(() => '');
    __platform = await runtimeSender.getPlatform().catch(() => ''); __content = await runtimeSender.getContent().catch(() => '');
    __chatId = await runtimeSender.getChatId().catch(() => ''); __isAdmin = await runtimeSender.isAdmin().catch(() => false);
  }
  function bucketGet(bucket, key, fallback = '') { const v = (__bucketCache[__bucketName(bucket)] || {})[__key(key)]; return v == null || v === '' ? fallback : v; }
  function bucketSet(bucket, key, value) { const b = __bucketName(bucket), k = __key(key); (__bucketCache[b] ||= {})[k] = value; __pending.push(new SGBucket(b).set(k, value).catch(() => {})); return true; }
  function bucketDel(bucket, key) { const b = __bucketName(bucket), k = __key(key); if (__bucketCache[b]) delete __bucketCache[b][k]; __pending.push(new SGBucket(b).delete(k).catch(() => {})); return true; }
  function bucketAllKeys(bucket) { return Object.keys(__bucketCache[__bucketName(bucket)] || {}); }
  function Bucket(name) { return { get: (key, fallback = '') => bucketGet(name, key, fallback), set: (key, value) => bucketSet(name, key, value), delete: (key) => bucketDel(name, key), keys: () => bucketAllKeys(name) }; }
  function GetUserID() { return __userId; } function GetUserId() { return __userId; } function GetUsername() { return __userName; } function GetUserName() { return __userName; }
  function GetImType() { return __platform; } function ImType() { return __platform; } function GetContent() { return __content; } function GetChatID() { return __chatId; } function GetChatId() { return __chatId; }
  function sendText(v) { if (runtimeSender?.reply) __pending.push(runtimeSender.reply(String(v ?? '')).catch(() => {})); } const SendText = sendText;
  function image(url) { return '[CQ:image,file=' + String(url || '') + ']'; } function sendImage(url) { sendText(image(url)); } const SendImage = sendImage;
  function sleep(ms) { Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, Math.max(0, Number(ms || 0))); } function Debug() { if (process.env.SILLYGIRL_DEBUG) console.log(...arguments); }
  function request(options, cb) { if (typeof options === 'string') options = { url: options }; options ||= {}; const target = options.url || options.URL; if (!target) return null; const method = String(options.method || options.Method || 'GET').toUpperCase(); const args = ['-sS', '-L', '--max-time', String(Math.ceil(Number(options.timeout || options.Timeout || 60000) / 1000) || 60), '-X', method]; for (const [k,v] of Object.entries(options.headers || options.Header || {})) args.push('-H', k + ': ' + v); const body = options.body ?? options.data ?? options.form ?? options.json; if (body != null && method !== 'GET') args.push('--data-raw', typeof body === 'string' ? body : JSON.stringify(body)); args.push(target); try { const text = execFileSync('curl', args, { encoding: 'utf8', maxBuffer: 50 * 1024 * 1024 }); const out = text.trim() ? JSON.parse(text) : {}; cb?.(null, null, null, text); return out; } catch (error) { cb?.(error, null, null, ''); return null; } }
  function __pushArgs(...args) { if (args.length === 1 && args[0] && typeof args[0] === 'object') { const i = args[0]; return { platform: i.imType || i.platform || i.type || '', group: i.groupCode || i.group_id || i.group || '', user: i.userID || i.user_id || i.user || '', title: i.title || '', content: i.content || i.message || i.msg || i.text || '' }; } return { platform: args[0] || '', group: args[1] || '', user: args[2] || '', title: args[3] || '', content: args[4] || args[3] || '' }; }
  function push(...args) { const i = __pushArgs(...args); try { __pending.push(new SGAdapter(String(i.platform || '')).push({ group_id: String(i.group || ''), user_id: String(i.user || ''), title: String(i.title || ''), content: String(i.content || i.title || '') }).catch(() => {})); } catch (_) {} return ''; }
  function sendTo(platform, user, content) { return push(platform, '', user, '', content); } function NotifyMasters(v, channels) { if (runtimeSender?.pushAdmin) __pending.push(runtimeSender.pushAdmin(String(v ?? ''), channels ? { platforms: Array.isArray(channels) ? channels : [channels] } : {}).catch(() => runtimeSender.reply(String(v ?? '')).catch(() => {}))); else sendText(v); }
  const notifyMasters = NotifyMasters, sendNotify = sendText, response = () => ({}), listen = () => '', input = () => '';
  function isAdmin() { return !!__isAdmin; } function get(key, fallback = '') { if (arguments.length >= 3) return bucketGet(arguments[0], arguments[1], arguments[2]); const t = String(key || ''); if (t.includes('.')) { const parts = t.split('.'); return bucketGet(parts.shift(), parts.join('.'), fallback); } return bucketGet('otto', t, fallback); }
  function set() { return arguments.length >= 3 ? bucketSet(arguments[0], arguments[1], arguments[2]) : bucketSet('otto', arguments[0], arguments[1]); } function del() { return arguments.length >= 2 ? bucketDel(arguments[0], arguments[1]) : bucketDel('otto', arguments[0]); } function keys(bucket = 'otto') { return bucketAllKeys(bucket); } function param(index = 1) { return String(__content || '').trim().split(/\s+/).filter(Boolean)[Number(index) || 0] || ''; }
  const CryptoJS = { MD5: (v) => ({ toString: () => nodeCrypto.createHash('md5').update(String(v ?? '')).digest('hex') }) };
  function qls(uid) { const name = String(uid || ''); for (const key of bucketAllKeys('qls')) { try { const item = JSON.parse(bucketGet('qls', key) || '{}'); if (!name || item.name === name || key === name || String(item.id || '') === name) return item; } catch (_) {} } return null; }
  function Qinglong(host, client_id, client_secret) { let token = ''; function tokenValue() { if (token) return token; const base = String(host || '').replace(/\/$/, ''); const data = request({ url: base + '/open/auth/token?client_id=' + encodeURIComponent(client_id || '') + '&client_secret=' + encodeURIComponent(client_secret || ''), dataType: 'json' }); token = (data && data.data && data.data.token) || (data && data.token) || ''; return token; } function ApiQL(path, body = '', method = 'get', query = '') { const base = String(host || '').replace(/\/$/, ''); const p = String(path || '').replace(/^\/+/, ''); const headers = {}; const tk = tokenValue(); if (tk) headers.Authorization = 'Bearer ' + tk; return request({ url: base + '/open/' + p + (query || ''), method: String(method || 'GET').toUpperCase(), headers, body: body || undefined, dataType: 'json' }); } return { ApiQL, token: tokenValue }; }
var API_URL = bucketGet("60s", "apiUrl") || "https://60s.aboutnb.com/v2/60s";
var OUTPUT_TYPE = bucketGet("60s", "outputType") !== "false";

function fetch60sNews() {
    var response = request({
        url: API_URL,
        dataType: "json"
    });
    return response.data;
}

function formatNewsText(newsData) {
    var text = "📰 每日60秒早报\n━━━━━━━━━━━━━━━\n";
    text += "📅 " + newsData.date + " " + newsData.day_of_week + "\n";
    text += "🌙 农历：" + newsData.lunar_date + "\n━━━━━━━━━━━━━━━\n\n";

    for (var i = 0; i < newsData.news.length; i++) {
        text += (i + 1) + ". " + newsData.news[i] + "\n\n";
    }

    text += "━━━━━━━━━━━━━━━\n☀️ " + newsData.tip + "\n";
    text += "━━━━━━━━━━━━━━━\n🔗 详情：" + newsData.link;
    return text;
}

function send60sNewsText() {
    sendText(formatNewsText(fetch60sNews()));
}

function send60sNewsImage() {
    sendImage(fetch60sNews().image);
}

var imType = ImType();
var content = GetContent().trim();

if (imType == "fake") {
        var pushGroups = bucketGet("60s", "push_groups")
        Debug(pushGroups)
        var pgs = pushGroups.split(",")
        var groups = []
        for (i = 0; i < pgs.length; i++) {
            groups[i] = {
                imType: pgs[i].slice(0, 2),
                groupCode: pgs[i].slice(8),
            }
        }
        for (var i = 0; i < groups.length; i++) {
            groups[i]["content"] = OUTPUT_TYPE ? image(fetch60sNews().image) : formatNewsText(fetch60sNews());
            push(groups[i])
        }

}else if (content == "早报" || content == "新闻" || content == "60秒" || content == "60s") {
    OUTPUT_TYPE ? send60sNewsImage() : send60sNewsText();
} else if (content == "文字早报" || content == "文本早报") {
    send60sNewsText();
} else if (content == "图文早报" || content == "图片早报") {
    send60sNewsImage();
} else if (content == "早报数据" && isAdmin()) {
    sendText(JSON.stringify(fetch60sNews(), null, 2));
}

  await Promise.allSettled(__pending);
})().catch(err => sender.reply(`插件执行异常：${err && err.stack ? err.stack : err}`));
