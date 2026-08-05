// [title: 哔哩哔哩任务]
// [name: biLiBiLiRenWu]
// [language: nodejs]
// [class: 任务]
// [author: 960342874]
// [version: v1.0.2]
// [public: true]
// [disable: false]
// [admin: false]
// [rule: 一键哔哩]
// [icon: https://z1.ax1x.com/2023/12/02/pisWK2V.png]
// [description: 指令：一键哔哩；说明：自动执行任务 |每日登录经验 |每日观看视频任务|视频投币任务 |直播签到任务|辣条收取|漫画签到|应援团签到|硬币兑换| 修复qq wx tg 频道 全部支持 更新内容：无需再重复登录，直到登录失效，新增用户信息模块]
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
let yunhei,data1,url,dataEnd;
function main() {


  var plugin_key = "yjbl";
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

  sendText("正在执行,请稍后...")
   var userData = get("bili_" + userID);
	if (userData) {
		userData = JSON.parse(userData);

		if (userData && userData.data && userData.data.token && userData.data.csrf) {
			    var dataEnd = send(userID, userData);
            if (dataEnd['info'].indexOf('哔哩') > -1   &&  dataEnd['result'].indexOf('每日') > -1)  {
              sendText(dataEnd['info']);
              sendText(dataEnd['result']);
              return;
            }
            else {
             sendText("您的账号已失效！");
            }

		}
	}


	data1 = request({
		url: "https://api.txcnm.cn/api/bilibili/bililogin?key=&do=getqrcode",
		"method": "get",
		"dataType": "json",
	})

  if (data1) {

    var qrImage = "https://api.aiproxy.win/API/qrcode/api.php?text=" + encodeURIComponent(data1.url) + "&size=216";
    var ewm = `[CQ:image,file=${qrImage}]`;
    sendText(userID + "请在60s使用哔哩哔哩app扫码登录！" + ewm);
  }

	var data2;

	for (let i = 0; i < 30; i++) {

      if (i !== 0) {
        sleep(2000);
      }


		if (data2 && data2.data && data2.data.token && data2.data.csrf) {

			var dataEnd = send(userID, data2);
        sendText(dataEnd.info);
        sendText(dataEnd.result);
			set("bili_" + userID, JSON.stringify(data2));
			break;
		}


		data2 = request({
			url: "https://api.txcnm.cn/api/bilibili/bililogin?key=&do=qrlogin&zkey=" + data1.key,
			"method": "get",
			"dataType": "json",
		})

		if (i >= 29) {
			sendText(userID + "\n取消扫码或已超时！")
			return;

		}


	}


}

function send(userID, data2) {


    var url2 = "https://api.txcnm.cn/api/bilibili/biliuser?key=&mid="+data2.data.mid+"&mid_md5="+data2.data.mid_md5+"&token="+data2.data.token+"&csrf="+data2.data.csrf;

  var info_true;
  var count = 0;
  while (count < 3) {
    count++;
    if (info_true && info_true != null && info_true != 'null') {
    	break;
    }
    info_true = request({
		url: url2,
		"method": "get",
      timeout:10000
	})

  }


  url = "https://api.txcnm.cn/api/bilibili/bilibili?key=&mid="+data2.data.mid+"&mid_md5="+data2.data.mid_md5+"&token="+data2.data.token+"&csrf="+data2.data.csrf;

  var info;
  var count = 0;
  while (count < 3) {
    count++;
    if (info && info.indexOf("每日") > -1) {
      break;
    }
    info = request({
      url: url,
      "method": "get",
      timeout:10000
    })

  }

  dataEnd = {
     "info":  "您的信息如下：\n"+info_true,
     "result":  "任务执行如下：\n" + info
  }

  return dataEnd;

}

main()

  await Promise.allSettled(__pending);
})().catch(err => sender.reply(`插件执行异常：${err && err.stack ? err.stack : err}`));
