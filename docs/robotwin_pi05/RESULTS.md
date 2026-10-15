# 首个RPent＋π0.5成功回合

2026-10-15，深圳1物理GPU4。任务`beat_block_hammer / demo_randomized / seed100000`；规划器`GPT-6.1-Sol/xhigh`，原Sidney多任务π0.5检查点，H50/M10、absolute QPOS14。

| 核验项 | 结果 |
|---|---|
| 原生成功 | `eval_success=true` |
| 退出 | `terminated=true`、`truncated=false`、进程exit0 |
| π0.5调用 | 3次，执行50+50+15=115动作 |
| 其他动作原语 | 0次；没有重置或换seed |
| 规划器调用链 | 实际Codex app-server、MCP工具、π0.5 RPC、RoboTwin反馈 |
| 规划器计时 | SDK约119.9秒；agent约126.6秒，不包含首次依赖编译和启动 |
| 验证 | 全量1226 passed/6 skipped；最后专项21 passed；pre-commit通过 |
| 视频 | 本轮连续MP4未保存；12张三相机关键帧可用 |

这是一个工程闭环成功例，不是成功率对比，也不能据此证明RPent比纯π0.5更好。三次动作都来自冻结π0.5，planner负责分段调用与观察确认。

服务器完整产物：`/data/chenyiteng/results/rpent/pi05-beat-block-hammer-s100000-g4-20261015/attempt-01`。

公开证据位于服务器仓库的`docs/robotwin_pi05/evidence/`：`result.json`、`actions.jsonl`和`keyframes.jpg`。关键帧分别对应0、50、100、115动作，三列为头部、左腕、右腕；不是连续视频。

录像失败原因与修复：官方robotwin extra缺少imageio-ffmpeg，ImageIO回退PyAV时codec为空，触发`expected bytes, NoneType found`。已补依赖，并在实际官方环境验证编码/解码；原回合的内存连续帧已随进程退出，不能恢复。此前CPU检查使用了策略环境，未覆盖实际保存端，已记录该遗漏。

资源交还：RPent已清场，RLT5已按精确身份和namespace退出，EXPO原run重启；实际恢复与推进回执见GPU_HANDOFF.md。
