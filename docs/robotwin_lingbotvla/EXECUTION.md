# 当前执行与下一步

2026-10-12，深圳时间。

## 本轮执行进展（22:29）

用户已授权官方任务首回合、EEF检查点下载及公开派生仓库。公开fork已创建，服务器保留`upstream`并新增固定账户`origin`；上游基线`161be6bf`，我方首批文档提交`b99be7c`已发布到main及本次独立分支。

官方独立环境安装已越过Git与RLinf wheel构建/解压阶段，正在补齐依赖；版本约束保持官方，网络与mergerfs解压问题逐项记录。LingBot四个主分片已完整，其余两个Qwen分片续传中。复用已有RoboTwin完整资产，新建轻量目录修正cuRobo路径，官方校验通过；资产为unmanaged，revision未作同一性声明。Codex GPT-5.5/xhigh实际认证请求已通过。GPU4原RLT继续运行，准备结束后才交接；RPent原生回合尚未启动。

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

## 仍待执行

- 完成独立环境与固定revision检查点；资产目录与规划器实际认证请求已验证。
- 刷新GPU4恢复点并执行精确交接、绑定核验与首回合。
- 发布已审过的轻量文档和必要服务器启动配置；以原生成功、记录与清场回执验收。

22:29尚未运行RPent仿真或训练；环境安装和模型下载进行中。RPent运行源码未改；新增内容为文档和轻量操作脚本。首回合合同见[FIRST_RUN](FIRST_RUN.md)。
