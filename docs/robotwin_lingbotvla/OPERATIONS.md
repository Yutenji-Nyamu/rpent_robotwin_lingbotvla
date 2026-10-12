# 逐项操作记录

时间均为深圳时间（UTC+8）。源码、环境、资产、模型和完整运行记录放服务器；本地只留小型文档和操作脚本。凭据值不进入文档或日志。

| 时间 | 操作 | 结果与落点 |
|---|---|---|
| 2026-10-12 本轮开始 | 接受用户执行授权 | 官方 `beat_block_hammer / demo_randomized / seed 100000`；LingBot EEF专用检查点；先一条成功推理；公开派生仓库；逐项记操作、归纳问题。 |
| 21:24 | 固定host-key SSH登录普通账户并核验身份 | 深圳3、chenyiteng、UID20001、h100-gpu01。 |
| 21:24 | 读取逐卡owner、plan、status和GPU计算/图形占用 | GPU4仍为既有RLT候补；其driver及三项C/C/C+G进程存活。本轮尚未切换。其他卡保持原任务。 |
| 21:24 | 读取磁盘和软件资产目录 | 服务器数据卷约4.6TiB可用；已有 `/data/chenyiteng/datasets/robotwin-assets`。 |
| 21:24 | 复用服务器网络说明并做三个GET探测 | GitHub、Hugging Face模型API、PyPI均HTTP200；沿用共享7890规则代理，未修改共享配置。 |
| 21:25 | 核对旧环境和官方安装文档 | 旧环境torch2.11.0+cu129、SAPIEN3.0.1；官方RPent要求torch2.7.1依赖链与SAPIEN3.0.0b1。建立独立环境，旧环境保持原状。 |
| 21:26 | 核对Codex认证可用性 | 服务器codex-cli0.154.0但未登录；本机当前登录缓存存在。按官方认证文档复用现有登录，不记录任何token。 |
| 21:27 | 使用Yutenji-Nyamu非交互凭据调用GitHub forks API | 公开fork已创建，名称 `Yutenji-Nyamu/rpent_robotwin_lingbotvla`，parent为RLinf/RPent，保留所有分支；默认main。 |
| 21:29 | 服务器GitHub SSH账户核验 | 返回 `Hi Yutenji-Nyamu`；后续源码与文档可直接由服务器发布，无需本地克隆。 |

完整机器回执与后续安装/运行日志：`/data/chenyiteng/deployment-20261012/rpent-robotwin-g4/`。本地本轮轻量核验输出位于原DETAILS证据目录，文件名 `launch-inventory.out`、`prerequisites.out`、`install-detail.out`。
