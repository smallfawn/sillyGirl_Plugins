//[title: 实时天气]
//[name: shiShiTianQi]
//[language: nodejs]
//[class: 工具]
//[author: XiaoBo_]
//[version: v1.1.0]
//[public: true]
//[disable: false]
//[admin: false]
//[rule: ^(天气|今天天气)$|^(.+)(天气)$]
//[icon: https://img.icons8.com/fluency/96/sun.png]
//[description: 查询实时天气、温度、湿度、风力和日出日落；支持“天气”及“北京天气”]
// [depe: []]

const { sender: s, form } = require("sillygirl");

const config = new form({
  city: form.string().title("默认城市").default("北京"),
});

async function main() {
  const content = String(await s.getContent()).trim();
  const conf = await config.get();
  const namedCity = content.match(/^(.+)天气$/)?.[1];
  const city = namedCity && namedCity !== "今天" ? namedCity : (conf.city || "北京");
  const url = `https://wttr.in/${encodeURIComponent(city)}?format=j1&lang=zh`;
  const response = await fetch(url, { signal: AbortSignal.timeout(15000) });
  if (!response.ok) throw new Error(`天气接口 HTTP ${response.status}`);

  const data = await response.json();
  const current = data.current_condition?.[0];
  const today = data.weather?.[0];
  if (!current || !today) throw new Error("天气接口数据不完整");
  const place = data.nearest_area?.[0]?.areaName?.[0]?.value || city;
  const desc = current.lang_zh?.[0]?.value || current.weatherDesc?.[0]?.value || "未知";
  const astro = today.astronomy?.[0] || {};
  await s.reply([
    `📍 ${place}：${desc}`,
    `🌡️ ${current.temp_C}℃（体感 ${current.FeelsLikeC}℃）  ${today.mintempC}~${today.maxtempC}℃`,
    `💧 湿度 ${current.humidity}%  💨 ${current.winddir16Point || ""} ${current.windspeedKmph}km/h`,
    `🌅 ${astro.sunrise || "--"}  🌇 ${astro.sunset || "--"}`,
  ].join("\n"));
}

main().catch((error) => s.reply(`天气查询失败：${error.message}`));
