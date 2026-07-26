# SillyGirl Plugins

从 `smallfawn/Bncr_Plugins` 迁移到 SillyGirl 的插件集合。

插件按 SillyGirl 插件源结构组织：

```text
plugins/插件名.js
```

插件源不提供 `package.json`。`publicFileIndex.json` 会从脚本 `require()` 中生成依赖信息，`dependencies` 使用和 `package.json` 一样的对象格式，默认版本为 `latest`，例如：

```json
{
  "dependencies": {
    "ipp": "latest"
  }
}
```

SillyGirl 的依赖管理会展示识别到的依赖，由用户手动点击安装或卸载。

定时运行不写在脚本注释里。需要定时执行时，在 SillyGirl 的“定时任务”里选择对应脚本和命令。

## 已迁移

| 插件 | 文件 | 状态 | 说明 |
|------|------|------|------|
| ipChange | `plugins/ipChange.js` | 已适配 | 使用 `Bucket("smallfawnDB")` 保存上次 IP，使用 NodeJS 内置 `http/https` 查询公网 IP |
| getPrinterStatus | `plugins/getPrinterStatus.js` | 已适配 | 使用 `ipp` 查询打印机状态和提交测试图片打印任务，需要手动安装 `ipp` 依赖 |
| upsListen | `plugins/upsListen.js` | 已适配 | 使用 NodeJS 内置 `net` 查询 NUT 服务 |
| 青龙管理 | `plugins/qinglongManage.js` | 已适配 | 管理青龙面板状态、环境变量和系统通知 |
| 官方命令 | `plugins/officialCommands.js` | 已适配 | 支持 `时间`、`版本`、`更新`、`重启` 四个基础命令 |

## 兼容差异

BNCR 的 `sysMethod.pushAdmin()` 没有直接等价的 SillyGirl NodeJS 脚本 API。已迁移插件在定时任务里使用 `sender.reply()` 发送通知；实际投递目标取决于 SillyGirl 定时任务 Sender 的平台配置。

配置表单统一使用 SillyGirl 运行时导出的 `sillyGirlCreateSchema` / `SillyGirlPluginConfig`，插件安装时会自动注册到后台「插件配置」。
