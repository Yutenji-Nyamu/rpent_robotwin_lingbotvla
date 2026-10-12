# 粗粒度计划与首跑合同草案

本页前三阶段已由用户授权执行。2026-10-12首条官方任务原生成功；阶段4、5保留为后续讨论，没有追加运行。当前结果见[RESULTS](RESULTS.md)。

## 阶段

1. **上下文与仓库**：已完成服务器克隆、基线固定、同族结果整理及讨论文档。
2. **运行条件准备（完成）**：复用现有资产与工具链，按官方`.[robotwin]`建立独立环境；EEF模型34文件24.3GB完整，规划器CLI/SDK与实际回合均通过。
3. **一条官方任务闭环（成功）**：同卡启动环境和LingBot，官方敲块seed100000达成原生成功，95动作，正常退出并清场。状态、关键帧及日志完整；连续视频导出失败，单列为I18。
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
| 规划器 | 官方Codex / GPT-5.5 / xhigh；认证与实际回合通过 |
| 预算 | 沿用官方复现例max_turns100、planner_timeout_s4800、max_episode_steps10000 |
| 输出 | 建议源码下`logs/`或服务器独立results目录；run.log、两项服务日志、transcript、原生status和可用录像 |
| 成功条件 | 最新原生`TASK_ENV.eval_success == true`，保留实际seed和动作计数；planner的`finish`只代表结束规划 |
| 停止条件 | 原生成功、达到约定步数/规划时限、初始化/推理错误；若发现越卡C/G上下文，停止本次精确进程并核验绑定 |

不将普通RoboTwin QPOS检查点替换到这条EEF接口。现有资产是否符合支持的snapshot要先查；按原安装器复用完整资产，不重复搬运。模型目录需包含配置、norm_stats与qwen_base。

## 已执行的官方命令

以下将GPU设为物理4并显式写出官方复现参数。实际调用、原生成功与单卡C/G已验证；完整命令含output-dir及私有启动环境位置见[FIRST_RUN](FIRST_RUN.md)。

```bash
cd /data/chenyiteng/projects/rpent_robotwin_lingbotvla
source .venv-robotwin/bin/activate
export ROBOTWIN_ASSETS_PATH=/data/chenyiteng/datasets/rpent-robotwin-assets
export LINGBOT_MODEL_PATH=/data/chenyiteng/models/LingBot-VLA-RoboTwin-EEF-ckpt1500
rpent --robot robotwin \
  --task-name beat_block_hammer --task-config demo_randomized --seed 100000 \
  --cuda-device 4 \
  --planner codex --model gpt-5.5 --reasoning-effort xhigh \
  --max-turns 100 --planner-timeout-s 4800 --max-episode-steps 10000
```

资产已通过官方runtime的目录校验及实际成功回合；它是复用现成资源的完整unmanaged目录，revision为null，不声称等同固定HF snapshot的全部字节。模型目录完整并已实际加载推理。本次单seed成功不等于复现历史62.4%；复现需另外匹配分支、记忆和评估协议。

## GPU4交接

23:20交接前核到CP375完整；精确停止原driver后，旧namespace与GPU4 C/G清空，RPent才启动。RPent退出清场后，通过原逐卡owner恢复CP375，仅改恢复点和输出路径。为更新其内存中的slot4请求，原CPU owner按既有机制受控重启；其他卡driver/actors及共享Ray保持。详见操作流水和交还回执。
