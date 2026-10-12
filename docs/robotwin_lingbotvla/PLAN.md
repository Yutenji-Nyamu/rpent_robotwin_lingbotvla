# 粗粒度计划与首跑合同草案

本页已由用户授权执行。2026-10-12正在安装独立运行环境并下载EEF检查点；首回合尚未执行。

## 阶段

1. **上下文与仓库**：已完成服务器克隆、基线固定、同族结果整理及讨论文档。
2. **运行条件准备**：复用兼容的现有资产与工具链，按官方`.[robotwin]`建立独立环境；下载EEF专用检查点并核验规划器。下载及安装执行中。
3. **一条官方任务闭环**：同卡启动环境和LingBot，完成观察→工具调用→环境反馈→原生成功/失败→日志和录像→退出清场。首任务已定敲块、官方seed100000。
4. **同seed对照**：使用同一LingBot检查点、任务语言、场景和动作预算，对比原生LingBot与Harness；先找可复用基线入口，再确定最小改动。
5. **扩大评估或方法讨论**：决定是否运行完整C2R、记忆消融或失败恢复对比。RoboTwin训练数据导出和RL不属于已跑通能力。

## 首跑应继承的官方配置

| 项 | 已授权首跑配置 |
|---|---|
| 源码 | RPent `161be6bfe7574c4b9770abd5b53617136127bb98` |
| 资源 | 深圳3机物理GPU4；环境和VLA同卡；CPU规划客户端访问所选模型服务 |
| 环境 | Python3.11；`uv pip install -e ".[robotwin]"`，独立环境 |
| runtime | `rlinf-robotwin-runtime==0.1.1`、`rlinf-lingbotvla==0.1.1`、cuRobo v0.7.8、RLinf release/v0.4；官方要求SAPIEN3.0.0b1 |
| 检查点 | `RLinf/LingBot-VLA-RoboTwin-EEF-ckpt1500`，revision `e727b46cd220b66981ea4d2fd9ba84adc189e2cc` |
| 模型契约 | `robotwin_eef`、三路RGB、eef16状态/动作、use_length50；仓库VLA launcher默认10个去噪步 |
| 任务 | 已定`beat_block_hammer`，`demo_randomized`，官方表seed100000及对应task_language |
| 规划器 | 官方Codex / GPT-5.5 / xhigh；认证实际调用待验证 |
| 预算 | 沿用官方复现例max_turns100、planner_timeout_s4800、max_episode_steps10000 |
| 输出 | 建议源码下`logs/`或服务器独立results目录；run.log、两项服务日志、transcript、原生status和可用录像 |
| 成功条件 | 最新原生`TASK_ENV.eval_success == true`，保留实际seed和动作计数；planner的`finish`只代表结束规划 |
| 停止条件 | 原生成功、达到约定步数/规划时限、初始化/推理错误；若发现越卡C/G上下文，停止本次精确进程并核验绑定 |

不将普通RoboTwin QPOS检查点替换到这条EEF接口。现有资产是否符合支持的snapshot要先查；按原安装器复用完整资产，不重复搬运。模型目录需包含配置、norm_stats与qwen_base。

## 官方命令的单卡改写（待执行）

以下将GPU设为物理4并显式写出官方复现参数。CLI登录已确认，模型实际调用和显存仍待运行验证。先完成既有RLT逐卡退出和图形隔离配置，再运行。

```bash
cd /data/chenyiteng/projects/rpent_robotwin_lingbotvla
source .venv-robotwin/bin/activate
export ROBOTWIN_ASSETS_PATH=/data/chenyiteng/datasets/robotwin-assets
export LINGBOT_MODEL_PATH=/data/chenyiteng/models/LingBot-VLA-RoboTwin-EEF-ckpt1500
rpent --robot robotwin \
  --task-name beat_block_hammer --task-config demo_randomized --seed 100000 \
  --cuda-device 4 \
  --planner codex --model gpt-5.5 --reasoning-effort xhigh \
  --max-turns 100 --planner-timeout-s 4800 --max-episode-steps 10000
```

资产目录已存在待官方校验，模型目录正在下载。当前main执行这条命令也不等于复现历史62.4%；复现需另外匹配分支、记忆和评估协议。

## GPU4交接

20:37现场的RLT已有CP350；以后切换时重新定位最新完整CP、driver PID/UID/start、namespace和候补request。只处理本卡目标，复用原逐卡owner/回执，核验driver、namespace及C/G释放。原任务继续作为逐卡候补；RPent退出清场后再交还。此处没有创建新owner或监控。
