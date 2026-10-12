# 逐项操作记录

时间均为深圳时间（UTC+8）。源码、环境、资产、模型和完整运行记录放服务器；本地只留小型文档和操作脚本。凭据值不进入文档或日志。

| 时间 | 操作 | 结果与落点 |
|---|---|---|
| 2026-10-12 本轮开始 | 接受用户执行授权 | 官方 `beat_block_hammer / demo_randomized / seed 100000`；LingBot EEF专用检查点；先一条成功推理；公开派生仓库；逐项记操作、归纳问题。 |
| 21:24 | 固定host-key SSH登录普通账户并核验身份 | 深圳3、chenyiteng、UID20001、h100-gpu01。 |
| 21:24 | 读取逐卡owner、plan、status和GPU计算/图形占用 | GPU4仍为既有RLT候补；其driver及三项C/C/C+G进程存活。本轮尚未切换。其他卡保持原任务。 |
| 21:24 | 读取磁盘和软件资产目录 | 服务器数据卷约4.6TiB可用；已有 `/data/chenyiteng/datasets/robotwin-assets`。 |
| 21:24 | 复用服务器网络说明并做三个GET探测 | GitHub、Hugging Face模型API、PyPI均HTTP200；沿用共享7890规则代理，未修改共享配置。 |
| 21:25 | 核对旧环境和官方安装文档 | 旧环境torch2.11.0+cu129、SAPIEN3.0.1；官方RPent要求torch2.7.1依赖链与SAPIEN3.0.0b1。建立独立环境，旧环境保持原状。 |
| 21:26 | 核对Codex认证可用性 | 服务器codex-cli0.154.0但未登录；本机当前登录缓存存在。按官方认证文档复用现有登录，不记录任何token。 |
| 21:27 | 使用Yutenji-Nyamu非交互凭据调用GitHub forks API | 公开fork已创建，名称 `Yutenji-Nyamu/rpent_robotwin_lingbotvla`，parent为RLinf/RPent，保留所有分支；默认main。 |
| 21:29 | 服务器GitHub SSH账户核验 | 返回 `Hi Yutenji-Nyamu`；后续源码与文档可直接由服务器发布，无需本地克隆。 |
| 21:31 | 启动官方安装与EEF模型下载 | 独立`.venv-robotwin`；复用已有CUDA12.9/NVCC；编译限定H100架构9.0、8个CPU编译作业。下载固定revision，所有文件在服务器。 |
| 21:33 | 核验Codex登录 | 本次私有tmpfs目录权限700、认证文件600；`codex login status`返回ChatGPT已登录，凭据不写入仓库。 |
| 21:36 | 同一模型文件小范围比较既有下载线路 | 7890约193KB/s、7897约663KB/s；HF镜像约24KB/s且超时。仅本次下载切换7897，保持已有断点；共享代理配置未修改。 |
| 21:38 | Codex GPT-5.5/xhigh最小认证请求 | 返回`RPENT_AUTH_OK`且exit0；模型目录刷新有一次超时提示，但实际指定模型请求成功。 |
| 21:42 | 复用既有WAN项目aria2下载方式 | 沿用服务器现成二进制、7897线路、2文件×8分段；将6个HF部分文件原位迁入本次下载暂存，复用约2.60GB已下载字节。模型与revision保持不变。 |
| 21:44 | 文档检查与公开推送 | 8份Markdown、PROJECT_CONTEXT入口及环境忽略规则；相对链接、参数、敏感内容与git diff检查通过。提交`b99be7c`已在公开main及本次分支，RPent运行源码未改。 |
| 21:48 | 调整本次模型分段下载并发 | 2文件增至4文件，每文件仍8分段；保留`.aria2`续传状态。实测总速率约8–10MiB/s；未更改共享线路和运行协议。 |
| 21:52 | 复用完整RoboTwin资产并修正目录布局 | 官方runtime 0.1.1的wheel只有471KB，读取其真实校验与路径规则。已有完整背景/对象/机器人资源；旧embodiment软链接使cuRobo推导根目录错误。建立本次独立目录，复用大目录软链接，仅复制7份小配置（18,288字节），原资产保持原状。官方`download_assets`直接跳过下载，左右URDF和碰撞配置路径均存在。 |
| 21:58 | 记录安装网络故障并保留缓存 | Git HTTPS低速后尝试7897；cuRobo fetch发生TLS中断，安装退出1。仅影响本次独立环境安装，Torch/CUDA已下载缓存保留。 |
| 22:01 | Git依赖转SSH，重试原官方版本 | SSH `ls-remote`核验RLinf `05379a6`和cuRobo `d64c4b0`；仅本次Git环境做URL传输改写。精确结束本次遗留Git取数进程；22:02安装已进入PyPI依赖解析。 |
| 22:08 | PyPI镜像重试 | PyPI metadata在三次重试后超时，按官方教程使用Aliyun默认源与Tsinghua附加源；Git和包版本约束不变。 |
| 22:11 | 记录uv解压权限故障 | RLinf官方源码wheel已构建，解压缓存时`gr00t/utils.py`报Permission denied。未扩大权限或改动共享挂载。 |
| 22:25 | 定位解压与分片失败 | wheel无重复项/异常文件权限；缓存和各NVMe数据目录均UID20001可写，同一wheel顺序解压821文件通过。两个Qwen分片为TLS握手中断；四个主模型分片已完成。 |
| 22:26 | 缩小解压并发并继续Qwen断点 | 本次安装仅设`UV_CONCURRENT_INSTALLS=1`，这是uv官方的安装/解压线程参数；保留所有包版本及缓存。四个完整分片移入模型目录，剩余两片沿既有7897线路、2文件×8分段续传。 |
| 22:29 | 分开HF入口与CDN下载线路 | 同一HEAD请求：HF经7897发生TLS EOF，经7890返回302；国内两镜像直接访问HTTP200。安装已越过RLinf wheel解压；Qwen采用7890解析公开下载地址、7897续传CDN，签名URL通过stdin给下载器，不写入仓库。 |
| 22:33 | Qwen续传退回可用7890 | 7897的新CDN连接同样TLS失败；仅两个剩余分片切回7890，初始持续吞吐约2.4–2.6MiB/s，完成的主模型文件保持原位。 |
| 22:34 | 准备SAPIEN b1单卡绑定 | 对实际下载包读取`Scene.__init__`，与已验收3.0.1方案所要求的初始化源码一致；b1的RenderSystem接口支持device字符串。复制既有bootstrap/runtime至本次deployment，仅改版本检查、清单路径与回执目录。旧NVIDIA profile、marker、旧任务代码不变；此步骤未创建GPU上下文。 |
| 22:42 | 核验依赖编译进展 | SAPIEN、Torch/CUDA等依赖已下载，cuRobo按官方v0.7.8使用CUDA12.9编译H100扩展；官方运行环境仍待完整安装退出码。 |
| 22:48 | 调整余下两分片的连接分配 | 同区间实测7890约101KB/s、7897 TLS失败、镜像约53KB/s。两文件各16分段续传，总32连接与此前4文件×8相同；持续总吞吐仍约2.4MiB/s，没有把瞬时峰值当成稳定速率。 |
| 22:53 | 官方环境安装完成并做CPU预检 | 安装exit0；`uv pip check`、`rpent --help`、规划器导入均exit0。freeze共294行；Torch2.7.1、SAPIEN3.0.0b1、cuRobo0.7.8、RLinf0.4.0；未改官方版本约束。 |
| 23:02 | 补充NVIDIA profile现场审计 | 首次CPU bootstrap以exit78指出旧清单之后新增的Norm/DSRL四条规则。逐条核对均为各自专用DSO匹配，与本次唯一预加载marker不相交；仅更新本次manifest的已审计清单。随后新环境bootstrap通过，Ray未初始化、未创建GPU上下文。 |
| 23:03–23:05 | 准备官方HF记忆库 | 旧环境HF客户端首个metadata请求SSL EOF；新安装环境显式统一大小写代理变量后，完整取得`RLinf/RPent-memory`的`robotwin/**`：107文件、170,980字节、revision `7db66088d06d04ae097682332a09704f13e6fc0c`。官方CLI默认同步仍启用。 |
| 23:04 | 官方`rpent-check-llm`返回未登录 | 同一环境下`codex login status`成功；源码定位到检查器只查默认登录文件，忽略本次私有CODEX_HOME。凭据不复制到全局HOME，不修改原检查器。 |
| 23:05 | 刷新GPU4 RLT恢复点 | 原driver PID2925701/UID20001/start776290524，12个本namespace actors；GPU4三个C/C/C+G进程仍正常。最新完整checkpoint为375，`complete=true`；继续运行，尚未借卡。 |
| 23:07 | 官方SDK实际调用通过 | 直接使用原`build_probe_config`/`run_probe_turn`核验真实认证；GPT-5.5返回`ok`，约23.7秒。只省略不识别CODEX_HOME的可选文件存在性预检查，实际服务端认证正常，RPent源码不变。 |
| 23:20 | 模型下载完成 | 固定revision共34文件、24,326,925,903字节，6个大分片全部完成并移入正式模型目录；完整性按下载完成状态、文件清单/大小及后续原生加载验证，未重复做全量散列。 |
| 23:20–23:21 | 精确释放GPU4 RLT | 保存CP375、原实配和环境；向PID2925701/UID20001/start776290524发SIGTERM。随后原driver消失、12个namespace actors清空、GPU4 C/G为空，旧owner记RLT_EXITED。此次中断未留下原生finished.json，保留SIGTERM/actor-kill日志；用上述现场证据写本次独立释放回执，不补造原生结束记录。 |
| 23:22 | 启动首条官方任务 | `attempt-01`，原任务/场景/seed/预算/EEF模型不变；主进程2779504，环境2779782，LingBot服务2779783。官方记忆同步直接复用107个缓存文件。 |
| 23:24 | 仿真服务与图形绑定核验 | Env RPC开始监听；SAPIEN绑定回执核到逻辑CUDA0=物理GPU4 UUID，实际nvidia-smi为环境C+G约2.5GiB，仅在4卡。LingBot仍加载权重，尚未宣称动作或原生成功。 |
| 23:25 | LingBot加载完成并进入官方规划器 | 两服务就绪，原生环境已reset；GPT-5.5/xhigh通过RPent Codex SDK调用，官方记忆流程保留。 |
| 23:26–23:27 | 规划器读取指南、场景及任务记忆 | 原生任务语言与seed核对；读取记录在服务器run.log与transcript。没有人工插入动作坐标或修改记忆。 |
| 23:28:31 | 第一段LingBot结束 | 官方EEF模型实际推理，执行50步；eval_success=false，累计50。 |
| 23:28:52 | 规划器调用左夹爪闭合 | set_gripper left=0，执行15步，累计65；原生尚未成功。 |
| 23:29:31 | 规划器调用抬升原语 | move_to执行8步，cuRobo返回Success，累计73；原生尚未成功。 |
| 23:29:58 | 第二段LingBot触发原生成功 | 请求50步，实际22步即native_success；eval_success=true，actual_seed100000，累计95。 |
| 23:30:06 | 官方收尾导出 | 配方与transcript写入；episode.mp4报expected bytes, NoneType found，未落盘连续视频。记录I18，保留5组三路RGB与states，不补造录像。 |
| 23:30:11 | 主进程正常退出 | wrapper原始回执exit0。Env/VLA parent-watch随后清场。 |
| 23:37 | 复核结果和进程清场 | states有reset+4次状态推进；本次namespace无残留、GPU4 C/G为空；写attempt-01-cleanup.json。GPU5–7原进程未变。 |
| 23:39 | 按原逐卡机制恢复RLT | 原配置只改resume_dir与两处logger输出；完整CP375。精确停止并重启CPU owner以载入slot4新request，其余slot原样保留；共享Ray和其他卡driver/actors不动。新driver339321，namespace rlt-sz3-g4-after-rpent-1012。 |
| 23:41 | 删除本次临时Codex认证缓存 | 确认无进程使用该CODEX_HOME后，仅删除本次/dev/shm/rpent-codex-20001-20261012-g4；494项临时文件，回查不存在。默认用户登录缓存保持。 |
| 23:42–23:44 | 导出轻量原生证据和关键帧 | 本地证据助手首读误用records键退出，按实际states.json的steps键修正；只读重导成功，未影响原始回合。15张PNG共907,135字节及小JSON；大日志与模型不回传。 |
| 23:43–23:48 | 核验RLT恢复与绑定 | driver日志明确Resuming CP375并进入rollout；12个本namespace actors存活，Actor/Rollout/Env实际C/C/C+G均仅GPU4，其他卡原PID未变。此时尚不宣称完成新一轮学习。 |
| 23:45–23:48 | 恢复同族图服务并新增成功关键帧页 | 旧8192服务已退出；同端口启动localhost只读文件白名单服务。曲线页、关键帧页、最终PNG均HTTP200，最终图已实际查看；已请求在应用浏览器打开。 |
| 23:48–本轮结束 | 更新并发布结果上下文 | 新增RESULTS，更新README/决策/计划/执行/合同/问题/操作/证据索引及根交接；核验Markdown链接、敏感内容、精确提交清单和运行源码未改后发布；最终提交由Git回执记录。 |

完整机器回执与后续安装/运行日志：`/data/chenyiteng/deployment-20261012/rpent-robotwin-g4/`。本地本轮轻量核验输出位于原DETAILS证据目录，文件名 `launch-inventory.out`、`prerequisites.out`、`install-detail.out`。
