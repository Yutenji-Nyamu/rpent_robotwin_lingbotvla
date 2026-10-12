# 讨论：RPent 能为我们运行什么

## 名称与定位

官方 README 原文将 RPent 展开为 **Recursive Physical Agent**，中文可译为“递归物理智能体”。其项目标题为“面向物理世界的智能体基础设施”。这里的递归指交互、观察反馈、反思和记忆再利用的循环；官方没有在所查说明中逐字解释 `RPent` 的字母拼接，不另编命名故事。

RPent 是框架名，第一篇对应论文是 **Harness VLA: Steering Frozen VLAs into Reliable Manipulation Primitives via Memory-Guided Agents**，arXiv `2607.08448`。v1为2026-07-09，本轮阅读的v5为2026-09-24。

## 论文的核心机制

VLA 已学会不少局部操作，但任务目标、物体布局或接触状态变化后，整段端到端执行可能失败。Harness VLA 让规划器读当前画面与任务，先定位目标、摆好接近姿态，再调用冻结 VLA 完成抓取等接触操作；之后观察结果，决定继续、重新摆位或重试。

固定工具库分工如下：解析式运动处理移动、姿态调整、夹爪与释放；冻结 VLA 处理较难用显式控制写稳的接触阶段。RoboTwin 对应调用名为 `lingbot_act`。VLA 权重在这些执行过程中保持冻结。

记忆有两层：任务记忆保存成功步骤及阶段结构；全局记忆保存跨任务经验、失败原因和恢复方法。探索允许重置试错；正式评估使用已有记忆，按当前场景重新定位，成功由仿真原生判定。记忆更新与VLA参数训练是两回事。

对我们最直接的价值是观察“何时调用 VLA、何时重新摆位、如何恢复失败”，并形成可检查的动作与规划轨迹。它提供代理执行与评估基础，当前不能据此声称已具备本项目的 LingBot-VLA 在线RL训练链。

## 原文结果与当前教程分开看

| 来源与配置 | RoboTwin C2R 成功率 |
|---|---:|
| 论文/官方论文说明：原生 LingBot-VLA | 50.4% |
| 论文/官方论文说明：Harness VLA + Opus-4.7 | 58.4% |
| 当前教程：`reproduce/robotwin` + GPT-5.5 xhigh | 62.4%，156/250 |

当前教程的250条由50任务、每任务5个官方验证seed组成，另有58失败、36超时。后一个数字是不同规划器的复现配置，不能直接写成论文中同一组58.4%的替代值。

C2R = clean-to-randomized：用干净场景成功轨迹形成先验，在随机背景、杂物、光照和桌高下评估。`task-specific/*_s0`的文件名后缀是记忆槽位，不保证来源场景实际seed=0；当前场景几何须重新定位。官方已经提供任务seed表，首跑直接使用，不自行增加专家筛种子流程。

## 仓库结构（本轮基线）

| 目录/入口 | 作用 |
|---|---|
| `rpent/cli/` | `rpent`命令、交互入口、记忆命令 |
| `rpent/planner/` | API、Claude Code、Codex等规划器适配 |
| `rpent/session/`、`rpent/prompt/` | 会话生命周期、任务运行与提示构建 |
| `rpent/tools/`、`rpent/memory/` | 工具调度、观察、记忆访问与合并 |
| `rpent/robots/` | 机器人注册、通用运行时、Env/VLA公共接口 |
| `robots/robotwin/` | 本项目的具体环境、LingBot、原语与提示实现 |
| `rpent/dashboard/`、`rpent/evaluation/` | 实时页面与评估结果 |
| `rpent/flywheel/` | 当前LIBERO轨迹采集与LeRobot导出 |
| `robots/libero/`、`robocasa/`、`robodojo/`等 | 其他仿真集成；真实机器人另有Franka、Dual Franka、YAM入口 |
| `docs/source-en/`、`docs/source-zh/` | 上游成对的中英文使用文档 |
| `tests/`、`requirements/`、`pyproject.toml` | 检查、依赖和可选安装集合 |
| `docs/robotwin_lingbotvla/` | 我们新增的讨论、决策与执行记录 |

`robots/robotwin/robot_spec.py`定义参数、服务启动、相机/动作契约和资源生命周期；`env_server.py`/`rlinf_env.py`对接RLinf的RoboTwin环境；`vla_server.py`/`vla_client.py`对接LingBot服务；`primitives.py`/`tools.py`提供动作、观察与定位；`prompts/`区分探索和评估；`eval/demo_randomized.json`给出50任务的seed与语言。

## 能跑到哪一层

| 工作 | 目前依据 | 我们的安排 |
|---|---|---|
| 单任务 RoboTwin + 冻结 LingBot + 规划器 | 官方已有完整入口 | 首个目标，建议敲块 |
| Dashboard、工具调用与原生成功判定 | 当前实现与文档齐全 | 首回合同时留证据 |
| 50任务×5seed C2R评估 | 官方表及复现分支已提供 | 单任务跑通后再确定预算 |
| 记忆读取、探索、失败恢复 | RoboTwin已接入记忆与探索模式 | 先复用发布记忆，随后再讨论自建 |
| 同seed原生LingBot与Harness比较 | 可复用同一模型、环境接口 | 第二阶段先核对现有基线入口，避免重写 |
| 将轨迹转为训练数据再SFT/RL | 当前Flywheel教程明确只覆盖LIBERO，训练在RLinf | RoboTwin导出/训练列为后续接入，不承诺开箱即用 |

## 版本选择

先跑通当前固定main基线，有新版依赖安装与服务实现。若目标变为复现62.4%，应切到 `reproduce/robotwin` 并核对配套记忆与检查点；该分支本轮解析为 `d07fe33e65105920f5d2bedb275869b871f997ec`。HF `reproduce/memory`保留历史布局，不能未经核验就把历史代码和最新记忆任意拼接。

## 一手来源

- [RPent README](https://github.com/RLinf/RPent)。
- [Harness VLA v5](https://arxiv.org/html/2607.08448v5)。
- [官方论文说明与结果](https://rpent.readthedocs.io/en/latest/rst_source/resources/harnessvla.html)。
- [RoboTwin教程](https://rpent.readthedocs.io/en/latest/rst_source/simulators/robotwin.html)。
- [架构说明](https://rpent.readthedocs.io/en/latest/rst_source/development/architecture.html)。
- [Flywheel适用范围](https://rpent.readthedocs.io/en/latest/rst_source/guides/flywheel.html)。

源码结论来自服务器仓库固定的 `161be6bf`，并核对了调用方；上述网页为2026-10-12读取。论文摘要页和HTML对RoboCasa增益数字有差异，本项目暂以最相关的RoboTwin结果展开，不把这些不同数值混用。
