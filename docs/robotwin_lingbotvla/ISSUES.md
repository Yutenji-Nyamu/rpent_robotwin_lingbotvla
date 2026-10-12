# 问题与解决

| 编号 | 问题与依据 | 处理 | 状态 |
|---|---|---|---|
| I01 | 用户本地空间有限，初始源码克隆在Windows | 服务器保留完整仓库；精确删除本次本地克隆，仅留轻量文档 | 完成 |
| I02 | 旧共享环境SAPIEN3.0.1不同于RPent官方3.0.0b1，Torch亦不同 | 新建 `.venv-robotwin`，执行官方 `uv pip install -e '.[robotwin]'`；复用兼容资产和工具链 | 准备中 |
| I03 | 沙箱中的Windows GCM无法使用wincredman，非交互credential fill失败 | 以同一固定账户脚本通过批准的宿主权限重试；无账户弹窗；fork创建成功 | 已解决 |
| I04 | 服务器Codex已安装但未登录 | 复用当前本机登录到本次私有临时认证目录；GPT-5.5/xhigh实际响应`RPENT_AUTH_OK`、exit0 | 认证已验证，RPent SDK整链待跑 |
| I05 | GPU4仍有RLT候补，CUDA变量不能独自证明图形绑定 | 环境和模型准备期间继续RLT；运行前按精确driver/namespace回收，复用既有GPU隔离方案并同时核C/G | 待执行 |
| I06 | 默认模型HTTP下载速度较慢；官方镜像小范围实测更慢 | 实测选择已有7897；复用既有aria2分段下载，保留2.60GB断点。未改变公共代理、模型或revision | 下载中 |
| I07 | 安装日志长时间只显示Python环境 | 查本次uv文件句柄，确认正在写Torch/CUDA依赖，而非挂起；保留正在进行的下载，随后进入RLinf git依赖获取 | 有实际进度 |
| I08 | 旧SAPIEN图形bootstrap明确限定3.0.1，不兼容官方3.0.0b1契约 | 官方b1的Scene初始化源码与旧方案要求一致，RenderSystem同样支持device字符串；仅复制bootstrap并调整版本guard与本次清单路径，保留旧profile/marker和官方物理/渲染配置 | 静态核验通过，实际C/G绑定待首跑 |
| I09 | 现成资产目录的embodiment是跨目录软链接；官方`load_curobo_config`先resolve再推导根目录，得到不存在的URDF路径 | 建立独立asset root，复制7份小配置，背景/对象/URDF/mesh继续链接现成文件；用官方函数检查目录与左右臂路径均通过。作为unmanaged完整资产复用，revision=null，不冒称固定snapshot已校验 | 已解决 |
| I10 | GitHub HTTPS依赖获取慢且TLS中断：RLinf一度约12分钟仅10MB，cuRobo重试报`gnutls_handshake` | 复用已验证的Yutenji-Nyamu SSH认证；仅本次安装进程将GitHub HTTPS URL改走SSH。官方ref核验：RLinf release/v0.4=`05379a6`，cuRobo v0.7.8=`d64c4b0`，源码版本保持。精确清理本次uv退出后遗留的4个Git进程 | 22:02已进入普通PyPI依赖解析 |
| I11 | PyPI多个metadata响应超时，重试3次后lz4导致安装退出2 | 使用RPent官方教程提供的Aliyun默认源和Tsinghua附加源，保留Git SSH与所有版本约束 | 22:08开始重试 |
| I12 | uv已构建RLinf wheel，但缓存解压一处文件Permission denied；同一未修改wheel顺序解压821文件通过，缓存各分支目录属主与写权限正常 | 仅本次安装设置`UV_CONCURRENT_INSTALLS=1`减少解压并发；不修改共享挂载/权限，不变更包版本 | RLinf解压已通过，完整安装继续；并发根因尚未完全确认 |
| I13 | 两个Qwen分片首次aria2请求发生TLS握手中断，其余四个主模型分片完整；随后7897的新CDN连接也失效 | 只续传未完成两片，复用原HF部分文件，完成分片移入模型目录；22:33退回实测可用7890 | 续传中，约2.4–2.6MiB/s |

技术故障以原始错误与实际解决结果记录；安装成功、服务启动、动作执行和任务原生成功分别验收。

I12参数依据：[uv concurrent-installs](https://docs.astral.sh/uv/reference/settings/#concurrent-installs)。
