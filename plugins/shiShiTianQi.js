// [title: 实时天气]
// [name: shiShiTianQi]
// [language: nodejs]
// [class: 任务]
// [author: XiaoBo_]
// [version: v2.0.0]
// [public: true]
// [disable: false]
// [admin: false]
// [rule: ^(天气|今天天气)$|^(.+)(天气)$]
// [icon: https://img.icons8.com/fluency/96/sun.png]
// [description: 天气查询插件，基于 60s API 的天气查询插件，支持实时天气查询、空气质量、日出日落时间、生活指数等详细功能；数据来自官方/权威源头，确保稳定与实时；QQ平台自动显示emoji图标；使用命令：天气 / 今天天气 - 查询默认城市详细天气，上海天气 / 北京天气 - 查询指定城市详细天气；配置说明：可在参数中设置"默认城市"，如设置为"上海"，则"天气"指令会查询上海天气，指令中的城市名会覆盖默认城市设置；数据来源：60s API，官方权威数据，稳定实时]
// [depe: []]

const { sender } = require('sillygirl');

(async () => {
const sg=require('sillygirl'),{sender:runtimeSender,Bucket:SGBucket,Adapter:SGAdapter}=sg,{execFileSync}=require('node:child_process'),nodeCrypto=require('node:crypto');
const __pending=[],__bucketCache=Object.create(null);let __userId='',__userName='',__platform='',__content='',__chatId='',__isAdmin=false;
function __bucketName(v){return String(v||'')}function __key(v){return String(v||'')}function __detectBuckets(){const names=new Set(['otto','qls']);try{const src=require('node:fs').readFileSync(process.argv[1]||'','utf8');let m;for(const re of [/\b(?:bucketGet|bucketSet|bucketDel|bucketAllKeys|bucketKeys)\s*\(\s*['"]([^'"]+)['"]/g,/\b(?:get|set|del)\s*\(\s*['"]([^'".]+)\.[^'"]+['"]/g])while((m=re.exec(src)))names.add(m[1])}catch(_){}return Array.from(names)}
for(const name of __detectBuckets()){try{__bucketCache[name]=await new SGBucket(name).getAll()||{}}catch(_){__bucketCache[name]||={}}}
if(runtimeSender){__userId=await runtimeSender.getUserId().catch(()=>'');__userName=await runtimeSender.getUserName().catch(()=>'');__platform=await runtimeSender.getPlatform().catch(()=>'');__content=await runtimeSender.getContent().catch(()=>'');__chatId=await runtimeSender.getChatId().catch(()=>'');__isAdmin=await runtimeSender.isAdmin().catch(()=>false)}
function bucketGet(b,k,f=''){const v=(__bucketCache[__bucketName(b)]||{})[__key(k)];return v==null||v===''?f:v}function bucketSet(b,k,v){(__bucketCache[__bucketName(b)]||={})[__key(k)]=v;__pending.push(new SGBucket(b).set(k,v).catch(()=>{}));return true}function bucketDel(b,k){if(__bucketCache[__bucketName(b)])delete __bucketCache[__bucketName(b)][__key(k)];__pending.push(new SGBucket(b).delete(k).catch(()=>{}));return true}function bucketAllKeys(b){return Object.keys(__bucketCache[__bucketName(b)]||{})}function Bucket(n){return{get:(k,f='')=>bucketGet(n,k,f),set:(k,v)=>bucketSet(n,k,v),delete:k=>bucketDel(n,k),keys:()=>bucketAllKeys(n)}}
function GetUserID(){return __userId}const GetUserId=GetUserID;function GetUsername(){return __userName}const GetUserName=GetUsername;function GetImType(){return __platform}const ImType=GetImType;function GetContent(){return __content}function GetChatID(){return __chatId}const GetChatId=GetChatID;
function sendText(v){if(runtimeSender?.reply)__pending.push(runtimeSender.reply(String(v??'')).catch(()=>{}))}const SendText=sendText;function image(u){return '[CQ:image,file='+String(u||'')+']'}function sendImage(u){sendText(image(u))}const SendImage=sendImage;function sleep(ms){Atomics.wait(new Int32Array(new SharedArrayBuffer(4)),0,0,Math.max(0,Number(ms||0)))}function Debug(){if(process.env.SILLYGIRL_DEBUG)console.log(...arguments)}
function request(o,cb){if(typeof o==='string')o={url:o};o||={};const target=o.url||o.URL;if(!target)return null;const method=String(o.method||o.Method||'GET').toUpperCase(),args=['-sS','-L','--max-time',String(Math.ceil(Number(o.timeout||o.Timeout||60000)/1000)||60),'-X',method];for(const[k,v]of Object.entries(o.headers||o.Header||{}))args.push('-H',k+': '+v);const body=o.body??o.data??o.form??o.json;if(body!=null&&method!=='GET')args.push('--data-raw',typeof body==='string'?body:JSON.stringify(body));args.push(target);try{const text=execFileSync('curl',args,{encoding:'utf8',maxBuffer:50*1024*1024});let out=text;try{out=text.trim()?JSON.parse(text):{}}catch(_){}cb?.(null,null,null,text);return out}catch(e){cb?.(e,null,null,'');return null}}
function __pushArgs(...a){if(a.length===1&&a[0]&&typeof a[0]==='object'){const i=a[0];return{platform:i.imType||i.platform||i.type||'',group:i.groupCode||i.group_id||i.group||'',user:i.userID||i.user_id||i.user||'',title:i.title||'',content:i.content||i.message||i.msg||i.text||''}}return{platform:a[0]||'',group:a[1]||'',user:a[2]||'',title:a[3]||'',content:a[4]||a[3]||''}}
function push(...a){const i=__pushArgs(...a);try{__pending.push(new SGAdapter(String(i.platform||'')).push({group_id:String(i.group||''),user_id:String(i.user||''),title:String(i.title||''),content:String(i.content||i.title||'')}).catch(()=>{}))}catch(_){}return''}function sendTo(p,u,c){return push(p,'',u,'',c)}function NotifyMasters(v,ch){if(runtimeSender?.pushAdmin)__pending.push(runtimeSender.pushAdmin(String(v??''),ch?{platforms:Array.isArray(ch)?ch:[ch]}:{}).catch(()=>runtimeSender.reply(String(v??'')).catch(()=>{})));else sendText(v)}
const notifyMasters=NotifyMasters,sendNotify=sendText,response=()=>({}),listen=()=>'',input=()=>'';function isAdmin(){return!!__isAdmin}function get(k,f=''){if(arguments.length>=3)return bucketGet(arguments[0],arguments[1],arguments[2]);const t=String(k||'');if(t.includes('.')){const p=t.split('.');return bucketGet(p.shift(),p.join('.'),f)}return bucketGet('otto',t,f)}function set(){return arguments.length>=3?bucketSet(arguments[0],arguments[1],arguments[2]):bucketSet('otto',arguments[0],arguments[1])}function del(){return arguments.length>=2?bucketDel(arguments[0],arguments[1]):bucketDel('otto',arguments[0])}function keys(b='otto'){return bucketAllKeys(b)}function param(i=1){return String(__content||'').trim().split(/\s+/).filter(Boolean)[Number(i)||0]||''}
const CryptoJS={MD5:v=>({toString:()=>nodeCrypto.createHash('md5').update(String(v??'')).digest('hex')})};function qls(uid){const name=String(uid||'');for(const key of bucketAllKeys('qls'))try{const item=JSON.parse(bucketGet('qls',key)||'{}');if(!name||item.name===name||key===name||String(item.id||'')===name)return item}catch(_){}return null}function Qinglong(host,client_id,client_secret){let token='';function tokenValue(){if(token)return token;const base=String(host||'').replace(/\/$/,'');const d=request({url:base+'/open/auth/token?client_id='+encodeURIComponent(client_id||'')+'&client_secret='+encodeURIComponent(client_secret||''),dataType:'json'});return token=(d&&d.data&&d.data.token)||(d&&d.token)||''}function ApiQL(path,body='',method='get',query=''){const base=String(host||'').replace(/\/$/,''),p=String(path||'').replace(/^\/+/,''),headers={},tk=tokenValue();if(tk)headers.Authorization='Bearer '+tk;return request({url:base+'/open/'+p+(query||''),method:String(method||'GET').toUpperCase(),headers,body:body||undefined,dataType:'json'})}return{ApiQL,token:tokenValue}}
const DEFAULT_CITY=bucketGet('weather_config','default_city','北京')||'北京', API_URL=bucketGet('weather_config','api_url','https://api.vvhan.com/api/weather')||'https://api.vvhan.com/api/weather', USE_EMOJI=bucketGet('weather_config','use_emoji','true')!=='false', TIMEOUT=Number(bucketGet('weather_config','timeout','10000'))||10000;
function main() {
    const content = GetContent(); // 获取用户消息
    const userInput = content.trim();

    if (userInput === "天气" || userInput === "今天天气") {
        queryWeather(DEFAULT_CITY || null); // 查询详细天气，使用默认城市
        return;
    }

    const cityWeatherMatch = userInput.match(/^(.+)天气$/);
    if (cityWeatherMatch) {
        const cityName = cityWeatherMatch[1].trim();
        if (cityName && cityName !== "今天") {
            queryWeather(cityName); // 查询指定城市的详细天气
            return;
        }
    }
}

function queryWeather(cityName) {
    let requestUrl = API_URL;
    if (cityName) {
        requestUrl += "?query=" + encodeURIComponent(cityName);
    }

    if (USE_EMOJI) {
        if (cityName) {
            sendText("🔍 正在查询 " + cityName + " 的天气信息...");
        } else {
            sendText("🔍 正在查询天气信息...");
        }
    } else {
        if (cityName) {
            sendText("正在查询 " + cityName + " 的天气信息...");
        } else {
            sendText("正在查询天气信息...");
        }
    }

    request({
        url: requestUrl,
        method: "get",
        headers: {
            "Content-Type": "application/json;charset=UTF-8",
            "User-Agent": "sillyGirl-Weather-Plugin/2.0"
        },
        timeOut: TIMEOUT
    }, function(error, response, header, body) {
        if (error) {
            if (USE_EMOJI) {
                sendText("❌ 网络请求失败：" + error);
            } else {
                sendText("网络请求失败：" + error);
            }
            return;
        }

        try {
            const data = JSON.parse(body);

            if (data.code === 200) {
                Debug(JSON.stringify(data));
                formatDetailedWeather(data.data);
            } else {
                Debug(JSON.stringify(data));
                if (USE_EMOJI) {
                    sendText("❌ 查询失败：" + data.message + "\n错误码：" + data.code);
                } else {
                    sendText("查询失败：" + data.message + "\n错误码：" + data.code);
                }
            }
        } catch (e) {
            if (USE_EMOJI) {
                sendText("❌ 数据解析失败：" + e);
            } else {
                sendText("数据解析失败：" + e);
            }
        }
    });
}

function formatDetailedWeather(data) {
    const location = data.location;
    const weather = data.weather;
    const airQuality = data.air_quality;
    const sunrise = data.sunrise;
    const lifeIndices = data.life_indices;

    if (USE_EMOJI) {
        let message = "📍 " + location.city + " · " + weather.updated.split(" ")[0] + "\n";
        message += "━━━━━━━━━━━━━━━━\n\n";

        message += "【天气概况】\n";
        message += "🌥 天气：" + weather.condition + "\n";
        message += "🌡 温度：" + weather.temperature + "°C\n";
        message += "💨 风向风力：" + weather.wind_direction + " " + weather.wind_power + "级\n";
        message += "💧 相对湿度：" + weather.humidity + "%\n";
        message += "🌀 气压：" + weather.pressure + "hPa\n";
        message += "☔ 降水量：" + weather.precipitation + "mm\n";

        if (airQuality) {
            message += "\n【空气质量】\n";
            message += "🍃 质量等级：" + airQuality.quality + " (AQI: " + airQuality.aqi + ")\n";
            message += "📊 PM2.5：" + airQuality.pm25 + " | PM10：" + airQuality.pm10 + "\n";
            message += "🏙 城市排名：" + airQuality.rank + "/" + airQuality.total_cities + "\n";
        }

        message += "\n【日出日落】\n";
        message += "🌅 日出：" + sunrise.sunrise_desc + "\n";
        message += "🌇 日落：" + sunrise.sunset_desc + "\n";

        if (data.alerts && data.alerts.length > 0) {
            message += "\n⚠ 【天气预警】\n";
            for (let i = 0; i < data.alerts.length; i++) {
                message += data.alerts[i] + "\n";
            }
        }

        if (lifeIndices && lifeIndices.length > 0) {
            message += "\n【生活指数】\n";

            const importantIndices = ["clothes", "umbrella", "sports", "carwash", "cold", "ultraviolet"];

            for (let i = 0; i < lifeIndices.length; i++) {
                const index = lifeIndices[i];
                if (importantIndices.indexOf(index.key) !== -1) {
                    const icon = getLifeIndexIcon(index.key);
                    message += icon + " " + index.name + "：" + index.level + "\n";
                    message += "   " + index.description + "\n";
                }
            }
        }

        sendText(message);
    } else {
        let message = "【" + location.city + "】" + weather.updated.split(" ")[0] + "\n";
        message += "━━━━━━━━━━━━━━━━\n\n";

        message += "【天气概况】\n";
        message += "天气：" + weather.condition + "\n";
        message += "温度：" + weather.temperature + "°C\n";
        message += "风向风力：" + weather.wind_direction + " " + weather.wind_power + "级\n";
        message += "相对湿度：" + weather.humidity + "%\n";
        message += "气压：" + weather.pressure + "hPa\n";
        message += "降水量：" + weather.precipitation + "mm\n";

        if (airQuality) {
            message += "\n【空气质量】\n";
            message += "质量等级：" + airQuality.quality + " (AQI: " + airQuality.aqi + ")\n";
            message += "PM2.5：" + airQuality.pm25 + " | PM10：" + airQuality.pm10 + "\n";
            message += "城市排名：" + airQuality.rank + "/" + airQuality.total_cities + "\n";
        }

        message += "\n【日出日落】\n";
        message += "日出：" + sunrise.sunrise_desc + "\n";
        message += "日落：" + sunrise.sunset_desc + "\n";

        if (data.alerts && data.alerts.length > 0) {
            message += "\n【天气预警】\n";
            for (let i = 0; i < data.alerts.length; i++) {
                message += data.alerts[i] + "\n";
            }
        }

        if (lifeIndices && lifeIndices.length > 0) {
            message += "\n【生活指数】\n";

            const importantIndices = ["clothes", "umbrella", "sports", "carwash", "cold", "ultraviolet"];

            for (let i = 0; i < lifeIndices.length; i++) {
                const index = lifeIndices[i];
                if (importantIndices.indexOf(index.key) !== -1) {
                    message += index.name + "：" + index.level + "\n";
                    message += "   " + index.description + "\n";
                }
            }
        }

        sendText(message);
    }
}

function getLifeIndexIcon(key) {
    const iconMap = {
        "clothes": "👔",
        "umbrella": "☂",
        "sports": "🏃",
        "carwash": "🚗",
        "cold": "🤧",
        "ultraviolet": "☀",
        "tourism": "✈",
        "comfort": "😊",
        "makeup": "💄",
        "mood": "😄",
        "morning": "🌄",
        "fish": "🎣",
        "sunglasses": "🕶",
        "sunscreen": "🧴",
        "traffic": "🚦",
        "allergy": "🤧",
        "airconditioner": "❄",
        "drying": "👕"
    };
    return iconMap[key] || "📌";
}

main();

  await Promise.allSettled(__pending);
})().catch(err => sender.reply(`插件执行异常：${err && err.stack ? err.stack : err}`));
