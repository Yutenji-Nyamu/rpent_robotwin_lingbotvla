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

完整机器回执与后续安装/运行日志：`/data/chenyiteng/deployment-20261012/rpent-robotwin-g4/`。本地本轮轻量核验输出位于原DETAILS证据目录，文件名 `launch-inventory.out`、`prerequisites.out`、`install-detail.out`。
