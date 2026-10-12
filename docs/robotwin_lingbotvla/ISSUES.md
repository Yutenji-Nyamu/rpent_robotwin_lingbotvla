# 问题与解决

| 编号 | 问题与依据 | 处理 | 状态 |
|---|---|---|---|
| I01 | 用户本地空间有限，初始源码克隆在Windows | 服务器保留完整仓库；精确删除本次本地克隆，仅留轻量文档 | 完成 |
| I02 | 旧共享环境SAPIEN3.0.1不同于RPent官方3.0.0b1，Torch亦不同 | 新建 `.venv-robotwin`，执行官方 `uv pip install -e '.[robotwin]'`；复用兼容资产和工具链 | 安装及CPU依赖/CLI/导入检查通过 |
| I03 | 沙箱中的Windows GCM无法使用wincredman，非交互credential fill失败 | 以同一固定账户脚本通过批准的宿主权限重试；无账户弹窗；fork创建成功 | 已解决 |
| I04 | 服务器Codex已安装但未登录 | 复用当前本机登录到本次私有临时认证目录；GPT-5.5/xhigh实际响应`RPENT_AUTH_OK`；官方RPent SDK亦实际回复`ok` | CLI和SDK实际认证均通过 |
| I05 | GPU4有RLT候补，CUDA变量不能独自证明图形绑定 | 保存CP375后精确交接；实际Env C+G与VLA C仅4卡；RPent结束清场后原候补恢复 | 已完成 |
| I06 | 默认模型HTTP下载速度较慢；官方镜像小范围实测更慢 | 按实测复用既有7897/7890与aria2，保留2.60GB断点；未改变公共代理、模型或revision | 34文件24.3GB完整，原生加载推理成功 |
| I07 | 安装日志长时间只显示Python环境 | 查本次uv文件句柄，确认正在写Torch/CUDA依赖，而非挂起；保留正在进行的下载，随后进入RLinf git依赖获取 | 有实际进度 |
| I08 | 旧SAPIEN图形bootstrap明确限定3.0.1，不兼容官方3.0.0b1契约 | 官方b1的Scene初始化源码与旧方案要求一致，RenderSystem同样支持device字符串；仅复制bootstrap并调整版本guard与本次清单路径，保留旧profile/marker和官方物理/渲染配置 | 实际renderer回执与C/G仅4卡，原生成功 |
| I09 | 现成资产目录的embodiment是跨目录软链接；官方`load_curobo_config`先resolve再推导根目录，得到不存在的URDF路径 | 建立独立asset root，复制7份小配置，背景/对象/URDF/mesh继续链接现成文件；用官方函数检查目录与左右臂路径均通过。作为unmanaged完整资产复用，revision=null，不冒称固定snapshot已校验 | 已解决 |
| I10 | GitHub HTTPS依赖获取慢且TLS中断：RLinf一度约12分钟仅10MB，cuRobo重试报`gnutls_handshake` | 复用已验证的Yutenji-Nyamu SSH认证；仅本次安装进程将GitHub HTTPS URL改走SSH。官方ref核验：RLinf release/v0.4=`05379a6`，cuRobo v0.7.8=`d64c4b0`，源码版本保持。精确清理本次uv退出后遗留的4个Git进程 | 22:02已进入普通PyPI依赖解析 |
| I11 | PyPI多个metadata响应超时，重试3次后lz4导致安装退出2 | 使用RPent官方教程提供的Aliyun默认源和Tsinghua附加源，保留Git SSH与所有版本约束 | 完整安装及实际回合通过 |
| I12 | uv已构建RLinf wheel，但缓存解压一处文件Permission denied；同一未修改wheel顺序解压821文件通过，缓存各分支目录属主与写权限正常 | 仅本次安装设置`UV_CONCURRENT_INSTALLS=1`减少解压并发；不修改共享挂载/权限，不变更包版本 | 完整安装通过；并发根因尚未完全确认 |
| I13 | 两个Qwen分片首次aria2请求发生TLS握手中断，其余四个主模型分片完整；随后7897的新CDN连接也失效 | 只续传未完成两片，复用原HF部分文件，完成分片移入模型目录；22:33退回实测可用7890 | 两片完整，模型加载及推理通过 |
| I14 | 复用的旧graphics manifest早于现有Norm/DSRL四条NVIDIA规则；新进程按原安全检查exit78 | 只读检查四条规则均为不匹配本次marker的独立DSO，补入本次manifest审计清单，服务器原profile不改 | CPU及实际单卡C/G均通过 |
| I15 | 用旧HF客户端预取官方记忆库时metadata请求SSL EOF | 改用已安装的官方环境客户端，显式统一大小写代理；相同官方repo、pattern、local_dir | 107文件完整，约171KB |
| I16 | `rpent-check-llm`误报missing_api_key；`_has_cli_login`只查默认路径，忽略CODEX_HOME | 同环境CLI登录成功；直接调用未修改的官方SDK probe完成真实请求，不搬迁凭据到全局、不改RPent源码 | GPT-5.5实际返回ok |
| I17 | 受控SIGTERM之后原RLT未写finished.json，不能以正常完成回执验收这次中断 | 保留真实SIGTERM和Ray actor-kill日志；重新核验精确driver已退出、旧namespace无活actor、GPU4无C/G、既有owner为RLT_EXITED；独立记录释放证据 | GPU4释放已实证，CP375保留用于恢复 |
| I18 | 首回合原生成功后，官方`EnvState.save`记录`failed to save artifact episode.mp4: expected bytes, NoneType found`；输出无MP4 | 保留完整状态、日志与15张关键帧；未伪造连续录像，也未为补录追加GPU回合。下次运行前应定位编码器并用既有图像做CPU导出复验 | 原生成功成立；连续视频导出未解决 |
| I19 | 旧本机8192同族图HTTP服务已退出，访问被拒绝 | 在同端口恢复只读预览，限定曲线与关键帧文件，不公开操作日志或认证资料 | 本轮预览已恢复 |

技术故障以原始错误与实际解决结果记录；安装成功、服务启动、动作执行和任务原生成功分别验收。

I12参数依据：[uv concurrent-installs](https://docs.astral.sh/uv/reference/settings/#concurrent-installs)。
