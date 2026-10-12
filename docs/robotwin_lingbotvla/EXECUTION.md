# 当前执行与下一步

2026-10-12，深圳时间。

## 本轮执行结果（23:45）

官方首任务`beat_block_hammer/demo_randomized/100000`的attempt-01原生成功：`eval_success=true`，95动作，exit0；两次LingBot推理执行72步，闭合夹爪/抬升原语23步。完整配置与状态链见[RESULTS](RESULTS.md)。

官方独立环境、24.3GB EEF模型34文件、复用资产、官方记忆107文件及Codex SDK均已通过实际回合。GPU计算/图形仅物理4卡，退出后精确namespace与GPU4清场；23:39原逐卡候补机制从CP375恢复RLT。私有认证缓存已删除，环境、模型和完整结果保留服务器。

连续视频收尾导出失败；15张三路相机关键帧和原生状态完整，已提供[交互预览](http://127.0.0.1:8192/rpent-success/)。运行源码与官方任务协议未改，没有为补视频追加第二个回合。公开fork保留upstream、原历史与许可；本次结果文档续写在原独立分支后发布到main。

逐项过程见[OPERATIONS](OPERATIONS.md)，遇到的问题见[ISSUES](ISSUES.md)。以下20:37内容保留为本轮执行前的历史现场。

## 已完成

- 读取工作区约定与DSRL专题，按固定host-key用普通账户核验深圳3机身份。
- 20:36/20:37只读读取GPU4 owner/slot、DSRL完成回执、TensorBoard、恢复点和C/G进程绑定。
- 重新读取τ3/τ4和RLT近期续跑曲线；复用已验收的同族历史，生成单列大图、可勾选页面、原始CSV与摘要。
- 核对官方论文、README、RoboTwin教程、依赖、模型契约、记忆与Flywheel适用范围。
- 在服务器克隆`RPent`，固定`161be6bf`，建立独立分支。读取跟踪文件共465项，初始工作区干净。
- 按用户后续要求删除本次本地源码克隆；删除前确认服务器提交一致、本地无dirty。删除约12.14MB，路径回查已不存在。
- 新增6份小型Markdown上下文；服务器仓库为主，本地仅保留小文档副本及必要索引。

## 现场结果

| 对象 | 20:37核验结论 |
|---|---|
| GPU4当前 | π0.5敲块RLT Clean，恢复CP325后已到362轮，最近完整CP350 |
| RLT最近固定评估 | R350：Clean17/20；同族DVCA历史R350为11/20，当前在GPU5候补CP350 |
| GPU4前项 | π0 DSRL U τ3，无trick，adjust_bottle，完整300轮，最终12/12 |
| 完成凭证 | finished.json exit_code=0，cleanup_error=null；CP300存在，TB step299 |
| GPU绑定 | RLT Actor、Rollout和环境分别为C/C/C+G，CUDA/EGL均4；本次PID均属于chenyiteng |
| 磁盘 | `/data/chenyiteng`所在卷约4.6TiB可用（20:36快照） |

DSRL在10-12 15:57:38退出，RLT约23秒后由原逐卡调度接替；本轮没有执行切换。准确时间由完成与started_at回执换算，见DETAILS。

## 后续讨论项

- 下次GPU回合前处理官方连续视频导出错误，先用已有图像做CPU导出验证。
- 确定是否做同seed纯LingBot对照；继承同检查点、语言、场景和动作预算，先找官方可复用入口。
- 是否扩大评估或复现论文分数，另行讨论；本轮不自动扩展。

本轮“一条官方成功推理”已完成。连续视频缺口已单列；原始成功记录不因导出失败改写。首回合合同见[FIRST_RUN](FIRST_RUN.md)。
