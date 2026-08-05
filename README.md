# SillyGirl Plugins

SillyGirl 单文件插件集合。每个插件只保留一个英文文件名的 `.js` / `.py` 源文件；中文展示名继续写在头部 `[title: xxx]`。不再携带旧桥接或额外面板脚本之类的附带文件。

插件按 SillyGirl 插件源结构组织：

```text
plugins/englishName.js
plugins/englishName.py
```

插件源不提供 `package.json`。插件依赖写在脚本头部注释里，使用 `[depe: ...]` 声明依赖数组，例如：

```js
// [title: getPrinterStatus]
// [name: getPrinterStatus]
// [depe: ["ipp"]]
```

Action 会在提交插件后自动扫描依赖并回写 `[depe: ...]`：

| 插件类型 | 扫描工具 | 结果 |
|----------|----------|------|
| NodeJS | `madge` | 写入 `[depe: ["包名"]]` |
| Python | `pipreqs` | 写入 `[depe: ["包名"]]` |

`publicFileIndex.json` 也会同步写入 `dependencies` 字段，格式固定为数组。SillyGirl 的依赖管理会展示识别到的依赖，由用户手动点击安装或卸载。

定时运行不写在脚本注释里。需要定时执行时，在 SillyGirl 的“定时任务”里选择对应脚本和命令。

## 运行时约定

- NodeJS/Python 插件优先使用 SillyGirl 内联函数：`sender`、`Bucket`、`container`、`utils`、`form`；新增代码不要再封装重复运行时。
- Python 插件统一按 Python 3.12 运行时维护；不要使用 Python 3.13/3.14 专属语法或标准库 API。
- 青龙/呆呆/smallcat 容器能力走 `container` 或运行时兼容封装读取后台容器配置，不再随插件安装额外文件。
- 新增或维护插件只写 `[title: xxx]`、`[name: 文件名]`、`[rule: xxx]`、`[depe: [...]]` 这类头部注释；不再写 at 符号元数据或 param 注释。
- 仓库内不放私钥、WxPusher AppToken、接口签名 Token；确实需要时放到插件配置表单。
- 插件需要持久化文本、JSON、CSV 等数据时，统一写入傻妞存储桶，不直接读写本地文件。

## 插件清单

`publicFileIndex.json` 由 `scripts/generate-public-file-index.mjs` 自动生成，当前插件文件均为英文文件名；安装页展示中文名来自 `[title: xxx]`，文件 basename 来自 `[name: 文件名]`。

| 示例插件 | 文件 | 状态 | 说明 |
|------|------|------|------|
| ipChange | `plugins/ipChange.js` | 可用 | 使用傻妞存储桶保存上次 IP，使用 NodeJS 内置 `http/https` 查询公网 IP |
| getPrinterStatus | `plugins/getPrinterStatus.js` | 可用 | 使用 `ipp` 查询打印机状态和提交测试图片打印任务，需要手动安装 `ipp` 依赖 |
| upsListen | `plugins/upsListen.js` | 可用 | 使用 NodeJS 内置 `net` 查询 NUT 服务 |
| 青龙管理 | `plugins/qinglongManage.js` | 可用 | 管理青龙面板状态、环境变量和系统通知 |
| 官方命令 | `plugins/officialCommands.js` | 可用 | 支持 `时间`、`版本`、`我是谁`、`更新`、`升级`、`重启` |
| smallcat登录 | `plugins/smallcat.js` | 可用 | 支持普通用户授权账号或手动 openid；手动留空时列出全部 SmallCat 账号 |
| 饿了么Code登录 | `plugins/elemeCodeLogin.js` | 可用 | 支持普通用户授权账号或手动 openid；`饿了么登录 CODE` 可直接换 Cookie 并同步容器变量 |
| 沪上阿姨签到 | `plugins/husheng.js` | 可用 | 支持普通用户授权账号或手动 openid；完成会员登录、手机号绑定、小满活动授权及每日签到 |
| 瑞幸咖啡抽奖 | `plugins/luckin.py` | 可用 | 支持普通用户授权账号或手动 openid；完成瑞幸登录、活动校验、抽奖及中奖记录查询 |
| 美团Code登录 | `plugins/meituan.py` | 可用 | 支持普通用户授权账号或手动 openid；本地生成签名参数后换取 `MT_TOKEN` |

## 兼容差异

SillyGirl 使用 `sender.pushAdmin(content, options)` 推送管理员；定时任务也可以继续使用 `sender.reply()`，实际投递目标取决于任务 Sender 的平台和接收人配置。

配置表单统一使用 SillyGirl v2 链式写法：`const config = new form({ token: form.string().title("Token").default("") })`，插件安装时会自动注册到后台「插件配置」。
