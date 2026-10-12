# RPent × RoboTwin × LingBot-VLA

项目名：`rpent_robotwin_lingbotvla`。当前阶段：2026-10-12首条官方任务已原生成功，`eval_success=true`、seed100000、95动作、exit0。详细结果见[RESULTS](RESULTS.md)。

2026-10-12 用户指定先讨论，在深圳3机物理4卡上跑通 RPent 的 RoboTwin—LingBot-VLA 路径；仓库拟公开，维护讨论、决策及粗细粒度执行文档。随后明确要求源码及有体积的内容尽量放服务器，删除本地克隆。

## 当前落点

- 服务器源码：`/data/chenyiteng/projects/rpent_robotwin_lingbotvla`。
- 上游：`https://github.com/RLinf/RPent.git`，remote 名 `upstream`。
- 基线：`161be6bfe7574c4b9770abd5b53617136127bb98`（2026-10-12 读取）。
- 分支：`codex/robotwin-lingbotvla-context-20261012`。
- 服务器专题：源码下 `docs/robotwin_lingbotvla/`；本目录只保留这些小型 Markdown 文档的本地副本。
- 公开派生仓库：[Yutenji-Nyamu/rpent_robotwin_lingbotvla](https://github.com/Yutenji-Nyamu/rpent_robotwin_lingbotvla)，已创建，保留上游历史与许可。
- 本地源码克隆已删除；模型、资产、环境和完整运行日志保存在服务器。本地仅文档、操作脚本及约0.91MB关键帧预览。

## 阅读顺序

1. [讨论：名称、论文、仓库结构与可跑内容](DISCUSSION.md)。
2. [决策：已定事项和待定项](DECISIONS.md)。
3. [计划：阶段目标、候选命令和验收](PLAN.md)。
4. [执行：当前进展和下一步](EXECUTION.md)。
5. [细节：现场证据、曲线口径和来源](DETAILS.md)。
6. [逐项操作流水](OPERATIONS.md)与[问题和解决](ISSUES.md)。
7. [首条回合配置、命令、资源和验收](FIRST_RUN.md)。
8. [首回合结果、原生证据与关键帧](RESULTS.md)。

## 最近现场

2026-10-12 23:30（深圳）：RPent首回合成功，LingBot调用2次，另有闭合夹爪/抬升两项动作原语；环境与VLA实际C/G均在物理4卡，退出后全部清场。23:39原逐卡候补链启动RLT，从CP375继续，原预算与方法保持。连续MP4导出失败，已保留5组三路相机关键帧、原生状态及完整日志。

20:37历史快照：GPU4的敲块RLT Clean候补362轮，R350固定评估17/20；前一项π0 DSRL U τ3无trick完成300轮，最终12/12，exit0，清场无错误，CP300保留。

[同族曲线页面](http://127.0.0.1:8192/)包含 DSRL 六条参照与 RLT Clean/DVCA；训练滑动20、固定评估原点，支持曲线勾选和全屏。现场以后应重新读取，不把此快照当作持续更新。
