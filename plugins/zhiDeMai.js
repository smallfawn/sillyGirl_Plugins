// [title: 值得买]
// [name: zhiDeMai]
// [language: nodejs]
// [class: 任务]
// [author: chuan85]
// [version: v1.0.0]
// [public: true]
// [disable: false]
// [admin: false]
// [rule: ^zdm$]
// [icon: https://www.smzdm.com/favicon.ico]
// [description: 什么值得买3小时好价（TOP20），指令“zdm”]
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
function main() {
    request({
        url: "https://suzhi.fun/api/post/list",
        headers: {
            "Content-Type": "application/json"
        },
        method: "POST",
        body: JSON.stringify({"s": "0002001"}),
        dataType: "json",
        timeOut: 10000 // 10秒超时
    }, function (error, response, header, body) {
        if (error || response.statusCode !== 200) {
            sendText("请求失败，请稍后再试。");
            return;
        }

        if (!body.data || !body.data.l) {
            sendText("没有找到价格信息。");
            return;
        }

        const items = Object.keys(body.data.l).slice(0, 20);
        let content = "";

        items.forEach((key, index) => {
            const t = body.data.l[key].t;
            const u = body.data.l[key].u;
            const ls = body.data.l[key].ls;
            content += `${index + 1}.${t}【${ls}】\n${u}\n\n`;
        });

        sendText(content);
    });
}

main();

  await Promise.allSettled(__pending);
})().catch(err => sender.reply(`插件执行异常：${err && err.stack ? err.stack : err}`));
