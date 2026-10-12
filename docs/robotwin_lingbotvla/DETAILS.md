# 细粒度证据与后续接续

## 服务器位置

- RPent：`/data/chenyiteng/projects/rpent_robotwin_lingbotvla`。
- 主上下文目录：`docs/robotwin_lingbotvla/`。
- 活跃逐卡队列：`/data/chenyiteng/deployment-20261008/bc-signal-tau-v1`。
- GPU4当前request：`/data/chenyiteng/deployment-20261011/dsrl-pi0-u-tau1234-v1/fallback-g4.json`。
- RLT当前run：`/data/chenyiteng/results/rlinf-rlt/rlt-sz3-g4-after-pi0-u300-1011`。
- DSRL τ3 run：`/data/chenyiteng/results/rlinf-dsrl-pi0-single/pi0-u-tau3-notrick-sz3-g4-r300-1011`。

2026-10-12 20:36 owner存活；GPU4 phase=`RLT_RUNNING`，driver PID2925701、UID20001、start776290524。该身份仅为历史快照，后续动作前重读。20:37计算PID3028918/3028925、C+G PID3028927，CUDA/EGL均4，namespace为上述RLT run名。

DSRL τ3 `finished.json`时间戳1791791858.884251、exit_code0、cleanup_error=null；slot started_at1791791881.6458972。τ4本轮直接读取的完成回执为exit_code15，并有SIGTERM日志，属于此前主动停止；旧交接写exit143是另一层退出表述，本记录保留本次直接读到的值，不改称自然完成。

## 同族对照口径

- DSRL新组均为π0、adjust_bottle、N4、H50/C20、ODE4/U侧ODE2、B256、warmup500、UTD20，无chunk dropout/alpha schedule。τ1/2目标400轮；τ3/4目标300轮，τ4在258轮停止。
- τ1/2及旧Clean/U曲线取10-12 16:46已结束实验完整快照；τ3/4重新从服务器递归读取TensorBoard。历史Clean/U只是历史参照，不是本轮同时新跑的对照。
- 固定评估不平滑，DSRL每点12条；训练采集滑动20。横轴为真实TB step+1。
- 四个新τ共同最近5个固定评估轮次为195/208/221/234/247；均值τ1/2/3/4=96.67/91.67/95.00/90.00%。τ3正常收束且表现较好，未证明优于τ1。
- RLT为π0.5敲块，N8；按当前恢复链拼接：旧Clean取R≤325，再接当前续跑；DVCA仅保留将被恢复的CP350范围。未采用的旧尾段不混入。
- RLT共同最近5个评估轮次250/275/300/325/350，Clean/DVCA均值73%/69%；R350分别85%/55%。单seed、少量每点评估不足以归因稳定方法优势。

## 本地轻量证据

证据目录：`E:/Codex/home/visualizations/2026/10/12/01a13016-35a3-7502-b449-6730a72b78b1`。

- `sz3-initial.out`：owner、slot、GPU与DSRL完成回执。
- `sz3-curves.out`：当前RLT、τ3/τ4 TensorBoard、checkpoint和绑定。
- `rlt-parent-curves.out`：恢复来源目录的近期曲线。
- `remote-repo.out`：服务器仓库路径、提交、分支、文件数与remote。
- `family-summary.json`、`family-curves.csv`：数值与原始绘图点。
- `families-overview.png`、`dsrl-*.png/svg`、`rlt-*.png/svg`、`index.html`：静态图与交互页面。
- 预览：`http://127.0.0.1:8192/`；只是本地快照展示，无服务器训练控制。

只读脚本在Windows `local_scripts/rpent_context_20261012/`，沿用既有固定指纹SSH helper和TensorBoard读取方式。密码只进入认证进程，未写入任何文件。

## 源码核对点

均相对服务器仓库基线`161be6bf`：

- `README.md`：RPent全称、定位、支持入口与论文。
- `pyproject.toml`：robotwin可选依赖与CLI入口。
- `robots/robotwin/robot_spec.py`：eef16、三相机、50长度、服务启动与`CUDA_VISIBLE_DEVICES`设置。
- `robots/robotwin/vla_server.py`：LingBot官方服务、默认去噪步10。
- `robots/robotwin/rlinf_env.py`：RLinf环境扩展、exact seed、qpos14/ee16校验。
- `robots/robotwin/eval/demo_randomized.json`：50任务×5seed及任务语言。
- `docs/source-en/rst_source/simulators/robotwin.rst`：Python3.11、SAPIEN3、检查点revision、原生成功判定与历史复现。
- `docs/source-en/rst_source/guides/flywheel.rst`：当前LIBERO采集/导出，RLinf训练。

文档检查采用上游`docs-check`说明，对独立Markdown做路径、语义和参数检查。本轮没有修改Sphinx源码或模型运行代码，未新增测试或运行训练测试。

## 2026-10-12首回合证据追加

当前结果见[RESULTS](RESULTS.md)。服务器部署回执根：`/data/chenyiteng/deployment-20261012/rpent-robotwin-g4/`。

- 环境/下载：`cpu-preflight.json`、`environment-freeze.txt`、`model-complete.json`、`asset-reuse.json`、`memory-prefetch.json`。
- 执行：`attempt-01-argv.json`、`attempt-01-started.json`、`attempt-01-main.json`、`attempt-01-exit.json`、`attempt-01-result.json`。
- 单卡/退出：`attempt-01-gpu-latest.json`、`graphics-scope/receipts/`、`attempt-01-cleanup.json`、`private-auth-cleanup.json`。
- RLT交接：`rlt-stop-requested.json`、`rlt-released-for-rpent.json`、`rlt-return-prepared.json`、`rlt-return-started.json`、`rlt-return-verified.json`。
- 完整运行记录：`/data/chenyiteng/results/rpent/robotwin-beat-block-hammer-s100000-g4-20261012/attempt-01`。
- 本地轻量预览：[关键帧](http://127.0.0.1:8192/rpent-success/)，15张图约0.91MB；非连续录像。源码、模型、环境和大日志仍只在服务器。

这些是历史回执；以后GPU或训练状态仍须重新现场核验。
