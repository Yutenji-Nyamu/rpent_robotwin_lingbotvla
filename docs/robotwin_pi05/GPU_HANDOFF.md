# 深圳1机4/5卡交接

本轮用户明确授权：RPent+π0.5 > EXPO > 原RLT；准备完才撤EXPO，单卡测试时另一卡接RLT，测试结束EXPO放回。尽量缩短真正空闲时间。

首次现场：普通账户chenyiteng/UID1003/admin；GPU4 UUID `GPU-9200fbe8-fdd0-93ae-c221-5f0e9d318bf5`，GPU5 UUID `GPU-3bbde6c0-3ddc-ec10-1d69-c3bc7855704e`。EXPO同一driver2359273占4(C+G)/5(C)；6/7是GRPO，保持原状。操作前重新核PID/UID/start、owner、恢复点与C/G。

- 原逐卡owner：`/data/chenyiteng/deployment-20261008/bc-signal-tau-v1/ops/owner.py`。
- 原EXPO：`/data/chenyiteng/results/expo-editor-u-tau2-sz1-g45-60000-1013`，原60000动作预算。
- 原EXPO pair_owner及已有退出/释放回执继续复用；不新增第二套常驻调度。
- 原4/5 fallback由`deployment-20261013/expo-editor-u-tau123-v1/fallback-g4.json`、`fallback-g5.json`定位；5卡为放风扇RLT，当前候补完整CP100。

实施前先定位EXPO原生保存/恢复契约。仅在配置、启动器、测试环境及恢复链全部准备好后停止目标driver；核精确进程/C/G释放，紧接着启动RPent4与RLT5。交还时保存RLT5最新完整恢复点、释放本任务进程，恢复原EXPO双卡；其他槽位逐项保持。

实际交接：EXPO2359273正常保存退出143并由原pair owner清场；释放回执后1.43秒启动RPent835996。π0.5服务836065、仿真839011的C/C+G均在物理4卡。RLT5 driver836717从CP100恢复并推进rollout，update_step仍0。

RPent原生成功后退出0，4卡清空；RLT5按精确身份SIGTERM并清空namespace/5卡。EXPO返回driver866004、pair owner865943、原逐卡owner866005；4/5重新WAIT_EXTERNAL，释放门为本次expo-return/runtime/released.json；5卡未来fallback为rlt-return-g5.json，仍从最新完整CP100恢复，4卡原fallback未变。6/7计划字段与GPU进程逐项未变。

恢复证据：原EXPO同run/60000预算，resume_verified确认47810动作、1152更新、4个pending calls。最终推进回执在部署目录expo-return-verification.json。

最终核验：EXPO已完成恢复后的第1153次更新（恢复点1152），pending_calls由4降到3；已证明实际学习推进。4/5卡只有EXPO driver866004的计算上下文，当前学习阶段无图形上下文；6/7原进程完全一致。临时Codex认证已确认无进程使用后清理。
