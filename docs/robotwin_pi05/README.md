# RPent × RoboTwin × π0.5

2026-10-15。用户授权先整理方案，切口清晰后直接实现、测试、推送；GPU优先级为本次测试 > EXPO > 原RLT候补。

目标：把已验收的Sidney多任务π0.5接入已跑通的RPent，先完成一个真实闭环。仓库继续使用`Yutenji-Nyamu/rpent_robotwin_lingbotvla`，新增独立分支`codex/robotwin-pi05-20261015`，不改旧LingBot结果。

源码、环境、模型和完整产物放服务器。本地仅小型文档与操作脚本。

- [两条既有链路与复用合同](REUSE.md)
- [架构、Codex含义与移植切口](DESIGN.md)
- [实施与验收计划](PLAN.md)
- [GPU优先级与交接](GPU_HANDOFF.md)
- [逐项操作](OPERATIONS.md)
- [问题与处理](ISSUES.md)
- [首个成功结果](RESULTS.md)
- [当前执行](EXECUTION.md)
- [首测命令与停止条件](RUN.md)

历史入口：[首条LingBot成功结果](../robotwin_lingbotvla/RESULTS.md)、[最初Sidney推理账本](REUSE.md)。这些本地跨项目链接在服务器公开副本中改为可访问来源。
