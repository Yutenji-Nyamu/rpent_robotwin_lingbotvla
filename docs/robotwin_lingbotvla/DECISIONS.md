# 决策记录

2026-10-12；用“已定/建议/待定/完成”区分意向与实际执行。

| 编号 | 状态 | 决策与依据 |
|---|---|---|
| D01 | 已定 | 项目名 `rpent_robotwin_lingbotvla`，目标方向为深圳3机物理4卡上的RPent—RoboTwin—LingBot-VLA。 |
| D02 | 已更新 | 初始讨论阶段已完成；用户明确“开始工作”，授权按官方流程完成一条成功推理，继续维护Markdown上下文。 |
| D03 | 已定并完成 | 用户要求源码尽量放服务器、删除本地克隆；服务器仓库已核对465个跟踪文件与基线提交，本地源码已删除。 |
| D04 | 已定 | 本地只留小型上下文/索引；环境、资产、模型、完整日志和录像放服务器。 |
| D05 | 已完成 | 保留上游历史、Apache-2.0许可和归属；`upstream`指向RLinf/RPent，建立独立`codex/robotwin-lingbotvla-context-20261012`分支。 |
| D06 | 已定 | 用户接受官方示例`beat_block_hammer`、`demo_randomized`、seed100000，先一条成功推理，不另筛seed。 |
| D07 | 建议 | 先用固定main实现验证工程链；论文复现另用明确的`reproduce/robotwin`及配套数据。 |
| D08 | 已定并创建 | 用户明确同意公开fork `Yutenji-Nyamu/rpent_robotwin_lingbotvla`；2026-10-12 21:27创建成功，parent=RLinf/RPent，保留全部分支及许可。 |
| D09 | 已完成 | 官方Codex / GPT-5.5 / xhigh及既有复现预算；复用当前登录到本次私有tmpfs，CLI/SDK与原生回合均成功，结束后删除临时认证缓存。 |
| D10 | 已完成交接 | 启动前保存CP375与原配置，精确释放GPU4；结束后通过原逐卡owner恢复CP375。仅重启CPU owner以载入slot4新请求，其他卡driver/actors与共享Ray保持。 |
| D11 | 已完成 | RPent环境C+G与LingBot C均实测只在GPU4，退出后均清场。CLI变量、renderer回执和实际C/G列表一并留存。 |
| D12 | 已完成 | 独立官方环境及EEF检查点完整，复用现成资产、CUDA和网络线路；模型/方法不变。首回合约462秒含冷启动，观察合计显存约16GiB。 |
| D13 | 已定 | 原生成功以states记录为准；单seed结果不外推成功率。官方连续视频导出失败如实保留，提供真实关键帧，不追加GPU重跑。 |

公开发布时保留LICENSE和原README归属，新增项目说明及已审过的轻量文档；凭据、模型、数据、缓存、完整日志和录像不进入公开仓库。
