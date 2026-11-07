# MoviePilot-Plugins（个人自用镜像）

> 本仓库是 **个人自用的 MoviePilot V2 插件镜像库**，不是上游官方仓库。
> 收录当前 NAS 上正在使用的 **34 个插件**源码快照，用于在插件原作者停更 / 上游删库后
> 仍能重装这些插件。**所有插件的版权与署名归各原作者**，本仓库只做原样归档。

## 为什么有这个仓库

MoviePilot 的官方插件市场（`jxxghp/MoviePilot-Plugins`）会随大版本演进而移除旧插件。
本项目把日常在用的 V2 插件全部钉在本地索引里，避免「上游删了 → 重装不了」。

## 怎么用

MoviePilot → 设置 → 插件市场 → 仓库地址，添加：

```text
https://github.com/Enderiose/moviepilot-plugins
```

`PLUGIN_MARKET` 支持多个地址，用英文逗号分隔，可同时保留官方市场。

> ⚠️ MoviePilot **只读取仓库的 `main` 分支**（源码里 raw 地址硬编码为 `main`），
> 因此本仓库的索引与插件必须留在 `main` 分支上。

## 插件清单

| 插件 ID | 名称 | 版本 | 作者 | 上游 |
|---|---|---|---|---|
| `AdaptiveIntroSkip` | 自适应IntroSkip | 1.7.8 | honue | [honue](https://github.com/honue) |
| `AutoBackup` | 自动备份 | 2.1.4 | thsrite | [thsrite](https://github.com/thsrite) |
| `AutoDiagnosis` | 自动诊断 | 1.9 | InfinityPacer | [InfinityPacer](https://github.com/InfinityPacer) |
| `AutoSignIn` | 站点自动签到 | 2.9.15 | thsrite | [thsrite](https://github.com/thsrite) |
| `BrushFlowLowFreq` | 站点刷流（低频版） | 4.3.3 | jxxghp,InfinityPacer | [InfinityPacer](https://github.com/InfinityPacer) |
| `CloudflareSpeedTest` | Cloudflare IP优选 | 1.5.1 | thsrite | [thsrite](https://github.com/thsrite) |
| `CustomHosts` | 自定义Hosts | 1.2.2 | thsrite | [thsrite](https://github.com/thsrite) |
| `DailyWord` | 每日一言 | 1.2 | jxxghp | [jxxghp](https://github.com/jxxghp) |
| `DoubanSync` | 豆瓣想看 | 2.1.1 | jxxghp,dwhmofly | [jxxghp](https://github.com/jxxghp) |
| `DouBanWatching` | 豆瓣书影音档案 | 1.9.9 | honue | [honue](https://github.com/honue) |
| `EmbyActorSync` | Emby剧集演员同步 | 1.5 | thsrite | [thsrite](https://github.com/thsrite) |
| `EmbyMetaRefresh` | Emby元数据刷新 | 2.3.3 | thsrite | [thsrite](https://github.com/thsrite) |
| `EmbyMetaTag` | Emby媒体标签 | 1.6 | thsrite | [thsrite](https://github.com/thsrite) |
| `IyuuAuth` | IYUU站点绑定 | 1.2 | jxxghp | [jxxghp](https://github.com/jxxghp) |
| `IYUUAutoSeed` | IYUU自动辅种 | 2.22 | jxxghp,CKun | [jxxghp](https://github.com/jxxghp) |
| `LibraryScraper` | 媒体库刮削 | 2.1.4 | jxxghp | [jxxghp](https://github.com/jxxghp) |
| `MediaCoverGenerator` | Emby媒体库封面生成 | 0.9.7 | 呀哈哈 | [MoviePilot-Plugins](https://github.com/justzerock/MoviePilot-Plugins) |
| `MediaServerMsg` | 媒体库服务器通知 | 1.8.6 | jxxghp | [jxxghp](https://github.com/jxxghp) |
| `MediaServerRefresh` | 媒体库服务器刷新 | 1.3.3 | jxxghp | [jxxghp](https://github.com/jxxghp) |
| `MoviePilotUpdateNotify` | MoviePilot更新推送 | 2.3.1 | thsrite | [thsrite](https://github.com/thsrite) |
| `MPServerStatus` | MoviePilot服务监控 | 1.4 | jxxghp | [jxxghp](https://github.com/jxxghp) |
| `PersonMeta` | 演职人员刮削 | 2.2.5 | jxxghp | [jxxghp](https://github.com/jxxghp) |
| `PluginAutoUpgrade` | 插件自动升级 | 2.4.2 | hotlcc | [hotlcc](https://github.com/hotlcc) |
| `RemoteIdentifiers` | 共享识别词 | 2.4.1 | honue | [honue](https://github.com/honue) |
| `ShortPlayMonitor` | 短剧刮削 | 4.0.4 | thsrite | [thsrite](https://github.com/thsrite) |
| `SiteDailyStatistic` | 站点每日数据统计 | 4.0 | Xiang | [xiangt920](https://github.com/xiangt920) |
| `SqlExecute` | Sql执行器 | 1.4 | thsrite | [thsrite](https://github.com/thsrite) |
| `SubscribeGroup` | 订阅规则自动填充 | 2.8.7 | thsrite | [thsrite](https://github.com/thsrite) |
| `SubscribeReminder` | 订阅提醒 | 1.5 | thsrite | [thsrite](https://github.com/thsrite) |
| `SubscribeStatistic` | 订阅下载统计 | 1.6 | thsrite | [thsrite](https://github.com/thsrite) |
| `TorrentTransfer` | 自动转移做种 | 1.10.3 | jxxghp | [jxxghp](https://github.com/jxxghp) |
| `TorrentTransferEnhanced` | 转移做种增强 | 0.1 | jxxghp,cancelpt | [cancelpt](https://github.com/cancelpt) |
| `TrendingShow` | 流行趋势轮播 | 1.3 | jxxghp | [jxxghp](https://github.com/jxxghp) |
| `WeWorkIPPW` | 企微配置IPpw版 | 2.4.2 | suraxiuxiu | [MoviePilot-Plugins](https://github.com/suraxiuxiu/MoviePilot-Plugins) |

## 目录结构

```text
moviepilot-plugins/
├── plugins.v2/<插件ID小写>/   # V2 插件源码（单文件 __init__.py 或含子模块）
├── package.v2.json            # V2 插件市场索引（版本 / 描述 / 作者 / 图标 / history）
├── icons/                     # 索引里以文件名引用的图标
└── LICENSE                    # GPL-3.0（继承上游）
```

与上游 `jxxghp/MoviePilot-Plugins` 保持同构，便于直接当第三方仓库使用。

## 版本与更新

索引里的 `version` 与各插件 `__init__.py` 中的 `plugin_version` **一一对应**，
`history` 只记录一条归档说明（上游历史已不可考），不影响安装与升级判断。

新增 / 更新插件时：

1. 把插件源码放进 `plugins.v2/<插件ID小写>/`（目录名必须是主类名的小写）
2. 同步修改 `package.v2.json` 里对应的 `version` 与 `history`
3. 图标：能外链就写完整 URL；只写文件名时，文件要放进 `icons/`

## 合规声明

（摘自上游 `jxxghp/MoviePilot-Plugins`）

> 第三方仓库建议 fork 本项目并保留相同目录和索引结构。MoviePilot 插件市场只读取
> GitHub 仓库的 `main` 分支；仓库地址通过 `PLUGIN_MARKET` 配置，多个地址用逗号分隔。
>
> 请勿开发用于破解 MoviePilot 用户认证，或提供色情、赌博等违法违规内容的插件。

## 许可

本仓库整体沿用上游许可 **GPL-3.0**（见 `LICENSE`）。
各插件著作权归其原作者，`package.v2.json` 中 `author` / 上表「上游」列已标注出处；
如原作者要求移除某个插件，请提 issue，会立即删除对应目录与索引条目。
