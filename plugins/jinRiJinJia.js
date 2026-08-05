// [title: 今日金价]
// [name: jinRiJinJia]
// [language: nodejs]
// [class: 任务]
// [author: 974566903@qq.com]
// [version: v1.7]
// [public: true]
// [disable: false]
// [admin: false]
// [rule: ^今日金价$|^金价监控设置$|^金价监控通知$]
// [icon: https://pic2.ziyuan.wang/user/974566903/2025/08/jj_ab8218111b3f2.jpg]
// [description: 关键词：今日金价，可查询基础金价、国内金店报价；新增关键词：金价监控通知|金价监控设置；温馨提示：金价监控通知需要设置计划任务,多群推送；2月21日更新接口]
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
async function main() {
    const command = GetContent();

    if (command === "今日金价") {
        await getCurrentGoldPrice();
    } else if (command === "金价监控设置") {
        await setupGoldPriceMonitor();
    } else if (command === "金价监控通知") {
        await checkGoldPriceAndNotify();
    }
}

async function getCurrentGoldPrice() {
    let goldSilverMsg = await request({
        url: "https://i.jzj9999.com/res/quote/pq.json?m_t1774784547561=",
        headers: {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf254173b) XWEB/19201",
        },
        method: "get",
        dataType: "json",
        timeOut: 30000
    });

    let shopMsg = await request({
        url: "https://api.lolimi.cn/API/huangj/api.php",
        headers: {
            "Content-Type": "application/json"
        },
        method: "get",
        dataType: "json",
        timeOut: 30000
    });

    let baseGoldInfo = [];
    let silverTaxedInfo = null;
    let updateTime = "";

    if (goldSilverMsg && goldSilverMsg.result === 0 && goldSilverMsg.items && goldSilverMsg.items.length > 0) {
        const goldItem = goldSilverMsg.items.find(item => item.code === "Au99.99");
        const silverItem = goldSilverMsg.items.find(item => item.code === "JZJ_ag");

        if (goldItem) {
            baseGoldInfo.push(`
商品：黄金
回购价：${goldItem.bidprice}
销售价：${goldItem.askprice}
最高价：${goldItem.high}
最低价：${goldItem.low}`);
            updateTime = formatTimestamp(goldItem.stime);
        }

        if (silverItem) {
            silverTaxedInfo = `
商品：白银（含税）
回购价：${silverItem.bidprice}
销售价：${silverItem.askprice}
最高价：${silverItem.high}
最低价：${silverItem.low}`;
        }
    }

    let targetShops = ["内地周大福", "内地六福珠宝", "周六福"];
    let shopInfo = [];
    let shopUpdateTime = "";

    if (shopMsg && shopMsg["国内十大金店"] && shopMsg["国内十大金店"].length > 0) {
        for (let shop of shopMsg["国内十大金店"]) {
            if (targetShops.includes(shop.品牌)) {
                shopInfo.push(`
{${shop.品牌}}
黄金价格: ${shop.黄金价格} ${shop.单位}`);

                if (shop.报价时间 && shop.报价时间 > shopUpdateTime) {
                    shopUpdateTime = shop.报价时间;
                }
            }
        }

        if (shopInfo.length > 0 && shopUpdateTime) {
            shopInfo.push(`
报价时间: ${shopUpdateTime}`);
        }
    }

    let finalOutput = "今日金价信息汇总";

    if (baseGoldInfo.length > 0 || silverTaxedInfo) {
        finalOutput += "\n\n=== 基础金价数据 ===";
        if (baseGoldInfo.length > 0) {
            finalOutput += baseGoldInfo.join("");
        }
        if (silverTaxedInfo) {
            finalOutput += `\n${silverTaxedInfo}`;
        }
        if (updateTime) {
             finalOutput += `\n实时时间：${updateTime}`;
        }
    }

    if (shopInfo.length > 0) {
        finalOutput += "\n\n=== 国内金店报价 ===" + shopInfo.join("");
    }

    if (finalOutput === "今日金价信息汇总") {
        finalOutput += "\n\n暂无最新金价、银价及金店报价数据，接口请求失败或数据格式异常";
    }

    sendText(finalOutput);
}

async function setupGoldPriceMonitor() {
    let goldSilverMsg = await request({
        url: "https://i.jzj9999.com/res/quote/pq.json?m_t1774784547561=",
        headers: {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf254173b) XWEB/19201",
        },
        method: "get",
        dataType: "json",
        timeOut: 30000
    });

    if (!goldSilverMsg || goldSilverMsg.result !== 0 || !goldSilverMsg.items || goldSilverMsg.items.length === 0) {
        sendText("获取金价数据失败，请稍后重试");
        return;
    }

    const goldItem = goldSilverMsg.items.find(item => item.code === "Au99.99");
    if (!goldItem) {
        sendText("未找到黄金数据");
        return;
    }

    const currentHighPrice = parseFloat(goldItem.high);
    const currentAskPrice = parseFloat(goldItem.askprice);

    sendText(`当前金价信息：
商品：黄金(Au99.99)
销售价：${goldItem.askprice}
最高价：${goldItem.high}
最低价：${goldItem.low}

请输入您要监控的目标价格\n当金价最高价超过此价格时会发送群通知📢\n\n输入Q/q退出设置`);

    const targetPriceInput = input(60000);

    if (!targetPriceInput || targetPriceInput === "") {
        sendText("操作已取消或超时");
        return;
    }

    if (targetPriceInput.toLowerCase() === 'q') {
        sendText("已取消金价监控设置");
        return;
    }

    const targetPrice = parseFloat(targetPriceInput);
    if (isNaN(targetPrice)) {
        sendText("输入的价格无效，请输入一个有效的数字");
        return;
    }

    bucketSet("gold_price_monitor", "target_price", targetPrice.toString());
    bucketSet("gold_price_monitor", "current_high_price", currentHighPrice.toString());
    bucketSet("gold_price_monitor", "current_ask_price", currentAskPrice.toString());
    bucketSet("gold_price_monitor", "last_notification_time", Date.now().toString());

    sendText(`✅ 金价监控设置成功！
当前金价最高价：${currentHighPrice}
您设置的监控价格：${targetPrice}
当金价最高价超过 ${targetPrice} 时|将会发送群通知`);
}

async function checkGoldPriceAndNotify() {
    let goldSilverMsg = await request({
        url: "https://i.jzj9999.com/res/quote/pq.json?m_t1774784547561=",
        headers: {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf254173b) XWEB/19201",
        },
        method: "get",
        dataType: "json",
        timeOut: 30000
    });

    if (!goldSilverMsg || goldSilverMsg.result !== 0 || !goldSilverMsg.items || goldSilverMsg.items.length === 0) {
        sendText("获取金价数据失败，请稍后重试");
        return;
    }

    const goldItem = goldSilverMsg.items.find(item => item.code === "Au99.99");
    if (!goldItem) {
        sendText("未找到黄金数据");
        return;
    }

    const currentHighPrice = parseFloat(goldItem.high);
    const targetPriceStr = bucketGet("gold_price_monitor", "target_price");

    if (!targetPriceStr) {
        sendText(`当前金价信息：
商品：黄金(Au99.99)
销售价：${goldItem.askprice}
最高价：${goldItem.high}
最低价：${goldItem.low}

您尚未设置金价监控价格，请先使用"金价监控设置"命令设置监控价格。`);
        return;
    }

    const targetPrice = parseFloat(targetPriceStr);
    if (isNaN(targetPrice)) {
        sendText(`当前金价信息：
商品：黄金(Au99.99)
销售价：${goldItem.askprice}
最高价：${goldItem.high}
最低价：${goldItem.low}

您设置的监控价格无效，请重新使用"金价监控设置"命令设置监控价格。`);
        return;
    }

    if (currentHighPrice > targetPrice) {
        let response = `🚨 金价提醒 🚨
金价已超过您的监控价格！

📈 当前金价(Au99.99):
销售价：${goldItem.askprice}
最高价：${goldItem.high}
最低价：${goldItem.low}

🎯 您设置的监控价格：${targetPrice}
⏰ 更新时间：${formatTimestamp(goldItem.stime)}

请及时关注金价变化！`;

        const lastNotificationTimeStr = bucketGet("gold_price_monitor", "last_notification_time") || "0";
        const lastNotificationTime = parseInt(lastNotificationTimeStr);
        const currentTime = Date.now();

        if (currentTime - lastNotificationTime > 600000) {
            bucketSet("gold_price_monitor", "last_notification_time", currentTime.toString());

            const groupId = bucketGet("A_goldT", "group_id");
            if (!groupId || groupId === "") {
                response += `\n⚠️ 未配置群ID，无法发送群通知`;
                sendText(response);
            } else {
                const groupIds = groupId.split('#').filter(id => id.trim() !== '');

                if (groupIds.length === 0) {
                    response += `\n⚠️ 未配置有效的群ID，无法发送群通知`;
                    sendText(response);
                } else {
                    let successCount = 0;

                    for (const singleGroupId of groupIds) {
                        const trimmedGroupId = singleGroupId.trim();
                        if (trimmedGroupId) {
                            try {
                                push({
                                    imType: "wx",
                                    groupCode: trimmedGroupId,
                                    content: response
                                });
                                successCount++;
                            } catch (error) {
                                console.error(`发送群通知到群 ${trimmedGroupId} 失败:`, error);
                            }
                        }
                    }

                    response += `\n✅ 已发送金价提醒通知到 ${successCount} 个群组`;
                    sendText(response);
                }
            }
        } else {
            response += `\nℹ️ 距离上次通知不足10分钟，本次不重复发送群通知`;
            sendText(response);
        }
    } else {
        sendText(`当前金价信息：
商品：黄金(Au99.99)
销售价：${goldItem.askprice}
最高价：${goldItem.high}
最低价：${goldItem.low}

您设置的监控价格：${targetPrice}

✅ 当前金价未超过监控价格，无需发送通知`);
    }
}

async function checkGoldPrice() {
    try {
        const targetPriceStr = bucketGet("gold_price_monitor", "target_price");
        if (!targetPriceStr) return;

        const targetPrice = parseFloat(targetPriceStr);
        if (isNaN(targetPrice)) return;

        let goldSilverMsg = await request({
            url: "https://i.jzj9999.com/res/quote/pq.json?m_t1774784547561=",
            headers: {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf254173b) XWEB/19201",
            },
            method: "get",
            dataType: "json",
            timeOut: 30000
        });

        if (!goldSilverMsg || goldSilverMsg.result !== 0 || !goldSilverMsg.items || goldSilverMsg.items.length === 0) {
            console.log("获取金价数据失败");
            return;
        }

        const goldItem = goldSilverMsg.items.find(item => item.code === "Au99.99");
        if (!goldItem) {
            console.log("未找到黄金数据");
            return;
        }

        const currentHighPrice = parseFloat(goldItem.high);

        if (currentHighPrice > targetPrice) {
            const lastNotificationTimeStr = bucketGet("gold_price_monitor", "last_notification_time") || "0";
            const lastNotificationTime = parseInt(lastNotificationTimeStr);
            const currentTime = Date.now();

            if (currentTime - lastNotificationTime > 600000) {
                bucketSet("gold_price_monitor", "last_notification_time", currentTime.toString());

                const groupId = bucketGet("A_goldT", "group_id");
                if (!groupId || groupId === "") {
                    console.log("未配置群ID，无法发送群通知");
                    return;
                }

                const groupIds = groupId.split('#').filter(id => id.trim() !== '');

                if (groupIds.length === 0) {
                    console.log("未配置有效的群ID，无法发送群通知");
                    return;
                }

                for (const singleGroupId of groupIds) {
                    const trimmedGroupId = singleGroupId.trim();
                    if (trimmedGroupId) {
                        const notificationMessage = `🚨 金价提醒 🚨
金价已超过您的监控价格！

📈 当前金价(Au99.99):
销售价：${goldItem.askprice}
最高价：${goldItem.high}
最低价：${goldItem.low}

🎯 您设置的监控价格：${targetPrice}
⏰ 更新时间：${formatTimestamp(goldItem.stime)}

请及时关注金价变化！`;

                        try {
                            push({
                                imType: "wx",
                                groupCode: trimmedGroupId,
                                content: notificationMessage
                            });
                            console.log("金价监控通知已发送到群：" + trimmedGroupId);
                        } catch (error) {
                            console.error(`发送群通知到群 ${trimmedGroupId} 失败:`, error);
                        }
                    }
                }
            }
        }
    } catch (error) {
        console.error("检查金价时发生错误:", error);
    }
}

function formatTimestamp(timestamp) {
    if (!timestamp) return "";
    const date = new Date(parseInt(timestamp) * 1000);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

main();

  await Promise.allSettled(__pending);
})().catch(err => sender.reply(`插件执行异常：${err && err.stack ? err.stack : err}`));

