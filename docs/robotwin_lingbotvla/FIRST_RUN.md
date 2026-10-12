# 首条回合执行合同

用户2026-10-12已授权。先采用官方配置；网络、安装、资产路径和共享服务器GPU绑定的适配单独记录，不修改任务、seed或策略算法。

## 配置

| 项目 | 值 |
|---|---|
| 任务 / 场景 / seed | `beat_block_hammer / demo_randomized / 100000` |
| 原生语言 | `Catch the handheld medium claw hammer and use it on the block.` |
| RPent代码基线 | `161be6bfe7574c4b9770abd5b53617136127bb98`，我方文档在其后提交 |
| RLinf依赖 | 官方`release/v0.4`，解析到`05379a652d260735caf3337b48711c52dd128bdf` |
| RoboTwin / LingBot运行包 | `rlinf-robotwin-runtime==0.1.1` / `rlinf-lingbotvla==0.1.1` |
| cuRobo | 官方`v0.7.8`，`d64c4b005459db10c5dd867d8b30a87d5bda9bdb` |
| SAPIEN | 官方`3.0.0b1`；保持其渲染和物理设置 |
| LingBot检查点 | EEF-ckpt1500，revision `e727b46cd220b66981ea4d2fd9ba84adc189e2cc` |
| VLA契约 | eef16，head/left-wrist/right-wrist RGB，use_length50，默认10个去噪步，默认不compile |
| 规划器 | 官方Codex / GPT-5.5 / xhigh；实际认证请求已通过 |
| 记忆 | 官方默认HF profile；启动时记录实际同步到的文件和来源 |
| 预算 | max_turns100、planner_timeout_s4800、max_episode_steps10000 |
| 资源 | SZ3物理GPU4，UUID `GPU-6c7afe5c-5238-60af-3ce2-329b3497133c`；环境与VLA同卡 |
| 资产 | `/data/chenyiteng/datasets/rpent-robotwin-assets`；复用已有完整资产，官方校验通过，unmanaged/revision=null |
| 结果目录 | `/data/chenyiteng/results/rpent/robotwin-beat-block-hammer-s100000-g4-20261012/attempt-01` |

## 命令

在独立环境、GPU4恢复点/释放与本次渲染绑定检查通过后执行：

```bash
cd /data/chenyiteng/projects/rpent_robotwin_lingbotvla
source .venv-robotwin/bin/activate
export ROBOTWIN_ASSETS_PATH=/data/chenyiteng/datasets/rpent-robotwin-assets
export LINGBOT_MODEL_PATH=/data/chenyiteng/models/LingBot-VLA-RoboTwin-EEF-ckpt1500
rpent --robot robotwin \
  --task-name beat_block_hammer --task-config demo_randomized --seed 100000 \
  --cuda-device 4 \
  --planner codex --model gpt-5.5 --reasoning-effort xhigh \
  --max-turns 100 --planner-timeout-s 4800 --max-episode-steps 10000 \
  --output-dir /data/chenyiteng/results/rpent/robotwin-beat-block-hammer-s100000-g4-20261012/attempt-01
```

Codex临时认证、CUDA工具链、代理与单卡图形绑定由本次服务器启动环境提供，不写入公开凭据。CLI会继承运行环境并分别启动Env/VLA服务。官方toolkit在`close()`时尝试将记录帧写成`episode.mp4`；本次该导出报`expected bytes, NoneType found`，没有落盘连续视频，关键帧与原生状态完整。此限制见I18。

## 交接与验收

1. 刷新GPU4 RLT的request、driver PID/UID/start、namespace和最新完整checkpoint；保留恢复配置。其训练预算与算法不变。
2. 精确停止本卡driver，使用既有finally清理本namespace。确认driver、namespace actors和GPU4 C/G均释放，再启动RPent；其他卡和共享Ray保持原状。
3. 启动后同时核计算与图形实际绑定；记录模型加载、环境初始化、实际工具链、seed和动作计数。
4. 成功必须有原生`TASK_ENV.eval_success=true`及对应状态/轨迹；规划器文本和`finish`不替代原生结果。分别记录LingBot是否实际被调用、调用次数和工具链。
5. 停止条件为原生成功、官方预算耗尽、初始化/推理错误；越卡绑定按本次精确进程退出处理，保留错误证据。
6. 结束后核服务进程与C/G清场，保存完整服务器日志/视频及轻量结果；按原逐卡候补机制从保留checkpoint恢复RLT。

2026-10-12本合同已实际执行：attempt-01原生成功、exit0、95动作、两次LingBot调用，服务与GPU上下文已清场。详情见[RESULTS](RESULTS.md)。第2项旧driver的SIGTERM路径未写原生finished.json，本次以实际driver/namespace/C/G全释放的独立回执验收，未补造正常结束记录。
