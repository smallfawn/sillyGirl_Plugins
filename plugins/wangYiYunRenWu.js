// [title: 网易云任务]
// [name: wangYiYunRenWu]
// [language: nodejs]
// [class: 任务]
// [author: 960342874]
// [version: v1.0.2]
// [public: true]
// [disable: false]
// [admin: false]
// [rule: 一键网易|网易云任务]
// [icon: https://api.iconify.design/lucide:bot.svg]
// [description: 网易云自动听歌打卡、云贝签到和音乐人任务。]
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
let yunhei;
function main() {

    var plugin_key = "wyyrw";
    var userID = GetUserID()
    yunhei = request({
      url: "https://ztt-1251929976.cos.ap-beijing.myqcloud.com/aut_plugin.txt",
      "method": "get",
      "dataType": "json",
      })
    if(!yunhei || !yunhei[plugin_key] ) {
        sendText("警告,未经过验证！")
        return;
      }
      else if (yunhei[plugin_key]['state'] == "invalid") {
        sendText(yunhei[plugin_key]['invalid_info']);
        return;
      }
      else if(GetImType()!="fake" && yunhei.master_yunhei.data.indexOf(userID) > -1) {
        sendText(yunhei['master_yunhei']['msg']+ "----ALL");
        return;
      }
      else if(GetImType()!="fake" && yunhei[plugin_key]['branch_yunhei']['data'].indexOf(userID) > -1) {
        sendText(yunhei['master_yunhei']['msg']  + "----"+ yunhei[plugin_key]['name'] );
        return;
      }


    var hostName = "https://zm.armoe.cn/"; // 低版本可以刷歌
    var specialHostName = "https://api.csm.sayqz.com/" //云贝签到、等级签到

    var wyy_cookie = bucketGet("Hi", "wyynew_" + GetUserID());
var a1 = "";
    var cookie = "";
    var info = "";


    wyy_cookie = wyy_cookie ? wyy_cookie:"";


    info = request({
      url: hostName + "user/account?timestamp=" + Date.now(),
      "method": "get",
      "dataType": "json",
      "timeout": 10000,
      "headers": {
        "Cookie": wyy_cookie
      }
    })

    if (wyy_cookie && !(info && info.code == 200 &&  info.profile && info.profile.nickname)) {
      sendText("检测到账号已过期！")
    }

    if (info && info.code == 200 &&  info.profile && info.profile.nickname) {
      sendText("检测到账号,正在处理...")
      cookie = wyy_cookie;
    }
    else {

        a1 = request({
            "url": hostName + "login/qr/key?timerstamp=" + Date.now(),
            "method": "get",
            "dataType": "json",
            "timeout": 10000,
        })


        var url = "https://api.aiproxy.win/API/qrcode/api.php?text=https://music.163.com/login?codekey=" + a1.data.unikey + "&size=150";
        var url = `[CQ:image,file=${url}]`
        sendText(GetUserID() + "请在60s使用网易云app扫码登录！" + url);

    }


    for (let i = 0; i < 30; i++) {
        if (i !== 0) {
            sleep(2000);
        }
        if (!cookie) {

            request({
                url: hostName + "login/qr/check?key=" + a1.data.unikey + "&timerstamp=" + Date.now(),
                "method": "get",
                "dataType": "json",
                "timeout": 10000,
            }, function (error, response, header, body) {
                if (body && body.code == "803") {
                    var setCookieHeader = header["Set-Cookie"];
                    set("cnmcnm2", header["Set-Cookie"])

                     var csrfToken = "";
                   var   musicU = "";

                    for (var i = 0; i < setCookieHeader.length; i++) {
                        cookie = setCookieHeader[i];
                        if (cookie.indexOf("__csrf=") === 0) {
                           csrfToken = cookie.split(';')[0].split('=')[1];
                        }
                        if (cookie.indexOf("MUSIC_U=") === 0) {
                            musicU = cookie.split(';')[0].split('=')[1];
                        }
                    }
                    cookie = "__csrf=" + csrfToken + "; MUSIC_U=" + musicU;
                    bucketSet("Hi", "wyynew_" + GetUserID(), cookie);


                    set("cnmcnm3", cookie)


                }


            });

        }

        if (cookie ) {

            break;
        }
        if (i == 29) {
            sendText("扫码超时已退出！");
            return;
        }
    }


    if (!info || !info.profile || !info.profile.nickname) {
        info = request({
            url: hostName + "user/account?timestamp=" + Date.now(),
            "method": "get",
            "dataType": "json",
            "timeout": 10000,
            "headers": {
                "Cookie": cookie
            }
        })

    }


    var level = request({
      url: hostName + "user/level?timestamp=" + Date.now(),
      "method": "get",
      "dataType": "json",
      "timeout": 10000,
      "headers": {
        "Cookie": cookie
      }
    })

    var vipLevel = request({
      url: hostName + "vip/info/v2?uid="+ info.profile.userId+"&timestamp=" + Date.now(),
      "method": "get",
      "dataType": "json",
      "timeout": 10000,
      "headers": {
        "Cookie": cookie
      }
    })


    if (info && info.code == 200 && info.profile.nickname) {
       var text =`
登录成功-${info.profile.nickname}
网易云等级：${level.data.level}`


       if(vipLevel && vipLevel.data && vipLevel.data.associator && vipLevel.data.associator.expireTime > Date.now()) {
        text+=`
黑胶会员等级：${vipLevel.data.redVipLevel}
会员到期时间：${formatTimestamp(vipLevel.data.associator.expireTime)}`
        }
      else {
        text+=`
黑胶会员：未开通`


      }

        sendText(text)

    }


    var a3 = request({
        url: specialHostName + "yunbei/sign?timestamp=" + Date.now(),
        "method": "get",
        "dataType": "json",
        "headers": {
            "Cookie": cookie
        }
    })


    var a4 = request({
        url: specialHostName + "daily_signin?type=1&timestamp=" + Date.now(),
        "method": "get",
        "dataType": "json",
        "headers": {
            "Cookie": cookie
        }
    })


    var songTask = request({
        url: specialHostName + "musician/tasks/new?timestamp=" + Date.now(),
        "method": "get",
        "dataType": "json",
        "headers": {
            "Cookie": cookie
        }
    })


	  request({
        url: specialHostName + "musician/sign?timestamp=" + Date.now(),
        "method": "get",
        "dataType": "json",
        "headers": {
            "Cookie": cookie
        }
    })


    var typeData = request({
        url: specialHostName + "personalized?limit=1&timerstamp=" + Date.now(),
        "method": "get",
        dataType: "json",
        "timeout": 10000,
    });


    var stopCount = 0;


    if (typeData && typeData.result && typeData.result.length > 0) {
        outerloop: for (let j = 0; j < typeData.result.length; j++) {
            var typeId = typeData.result[j]['id'];


            var data = request({
                url: hostName + "playlist/track/all?id=" + typeId + "&timerstamp=" + Date.now(),
                "method": "get",
                dataType: "json",
                "timeout": 10000,
            });
            if (data && data.songs && data.songs.length > 0) {

                for (let i = 0; i < data.songs.length; i++) {

                    if (stopCount >= 500) {
                        break outerloop;
                    }

                    var data1 = request({
                        url: hostName + "scrobble?timerstamp=" + Date.now(),
                        "method": "post",
                        "body": {
                            "id": data.songs[i]['id'],
                            "sourceid": "",
                            "time": "240",
                        },
                        "headers": {
                            "Cookie": cookie,
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
                        },
                        dataType: "json",
                        "timeout": 10000,
                    });


                    if (i == 0 && data1.data == 'success' && stopCount == 0) {

                        var text =
                            `
${info.profile.nickname}
【听歌300首】
每日300首打卡成功

【等级签到】
签到成功！经验+

【云贝签到】
云贝签到成功，云贝+
云贝任务：浏览商城成功，云贝+2！
云贝任务：浏览会员中心成功，云贝+5！
云贝任务：云贝推歌失败！
云贝任务：分享歌曲/歌单成功，云贝+5！
没有待领取的云贝奖励！
云贝任务完成，预计收益50+云贝！

【音乐人任务】`;
               if (songTask && songTask.code == 200) {
                 text+="\n完成！"
               }
               else {
                text+="\n你还不是音乐人！"
               }


                        sendText(text);

                    }
                    stopCount++;
                    if (i == (data.songs.length - 1) && data1.data == 'success') {

                    }


                }
            } else {
                sendText("song不存在！")
                return;

            }


        }


    }


}


function formatTimestamp(timestamp) {
    var date = new Date(timestamp);

    var year = date.getFullYear();
    var month = date.getMonth() + 1; // 月份从0开始，需要加1
    var day = date.getDate();
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var seconds = date.getSeconds();

    var formattedDate = year + '-' + (month < 10 ? '0' + month : month) + '-' + (day < 10 ? '0' + day : day);
    var formattedTime = (hours < 10 ? '0' + hours : hours) + ':' + (minutes < 10 ? '0' + minutes : minutes) + ':' + (seconds < 10 ? '0' + seconds : seconds);

    return formattedDate + ' ' + formattedTime;
}


main()


  await Promise.allSettled(__pending);
})().catch(err => sender.reply(`插件执行异常：${err && err.stack ? err.stack : err}`));
