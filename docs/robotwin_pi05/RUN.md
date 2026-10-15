# 首测运行合同

任务：`beat_block_hammer / demo_randomized / seed 100000`。规划器：用户批准的`gpt-6.1-sol / xhigh`。模型：原Sidney多任务SFT，H50/M10、absolute QPOS14。原预算：100 planner turns、4800秒、10000环境动作上限；不增加重置或筛选seed。

```bash
rpent --robot robotwin --vla-backend pi05 \
  --pi05-python "$PI05_PYTHON" --pi05-rlinf-repo "$ACCEPTED_RLINF" \
  --vla-model-path "$CONVERTED_SIDNEY_CHECKPOINT" \
  --task-name beat_block_hammer --task-config demo_randomized --seed 100000 \
  --cuda-device 4 --planner codex --model gpt-6.1-sol --reasoning-effort xhigh \
  --max-turns 100 --planner-timeout-s 4800 --max-episode-steps 10000 \
  --output-dir "$OUTPUT"
```

这三个模型参数指向已验收RLinf转换、源码和兼容解释器；不是任意原版openpi安装。具体版本与路径见REUSE.md。服务器部署目录保存完整argv、隔离运行环境和显卡绑定回执；公开仓库不包含登录认证。

本次使用深圳1物理4卡，CUDA与SAPIEN/EGL计算图形均核实际进程。5卡由原owner接续RLT，6/7卡原GRPO保留。策略先加载/预热，再启动仿真。图像、模型处理器、动作chunk和录制路径沿用旧链。

输出：`/data/chenyiteng/results/rpent/pi05-beat-block-hammer-s100000-g4-20261015/attempt-01`。

停止条件：原生成功、原预算耗尽或明确启动/执行异常。成功验收要求实际π0.5调用、环境`eval_success=true`、动作数、可解码视频、退出回执和GPU清场；planner自报finish不构成成功。结束后恢复原EXPO run/60000动作预算，并核恢复进度及实际推进。
