# 问题和处理

| 问题 | 依据与处理 | 状态 |
|---|---|---|
| EEF16与QPOS14不是同一动作空间 | 独立π0.5接口继承旧absolute QPOS链，保留LingBot | 已实现；原生115动作成功 |
| 既有环境版本不同 | RPent旧成功环境Torch2.7.1/SAPIEN3.0.0b1；SZ1 π0.5环境Torch2.11.0/SAPIEN3.0.1。分别保留已验收依赖，先核服务隔离与最小新增依赖 | 环境隔离完成 |
| 原RPent视频导出失败 | 新隔离环境沿用EnvState.save原入口保存3帧MP4成功；本次不改录制源码 | 本轮MP4失败；正确环境依赖修复与CPU编解码通过 |
| GitHub默认known_hosts缺失 | 使用已有专用known_hosts与固定Yutenji账户key；不跳过host-key校验 | 已解决，公开仓库已克隆 |
| SZ3 SSH channel超时 | 已有公开仓库与完整基线，改在SZ1准备，不影响现役实验 | 已绕开 |
| cuRobo Git取数停留 | 已存在同commit d64c4b0源码缓存；精确结束本次安装进程组，复用缓存；RLinf保持05379a6固定源码 | 安装完成 |
| 新RPC依赖覆盖旧模型依赖 | HF2.2不符合transformers4.57.6的<1要求；新cryptography与旧OpenSSL组合也触发导入异常。隔离环境将旧模型site-packages置于新增RPC包之前，只从新环境补缺失包；旧目录只读 | 模型类导入与真实GPU加载/预热通过 |
| 新增pi05_act与旧schema快照不同 | 补充新工具条目，保留LingBot既有schema与默认工具集合；另测后端工具互斥 | 复测通过，全量1226 passed / 6 skipped |

不以进程存活、工具finish或模型声称完成替代原生成功。

| 旧GPT-5.5被当前账户拒绝 | 实际SDK请求HTTP400；查可用模型后由用户批准GPT-6.1-Sol/xhigh | 新模型实际请求返回ok |
| SZ1首次cuRobo扩展编译 | 沿用官方依赖，实时核nvcc和对象文件进展；产物留部署缓存复用 | 五个扩展编译完成，环境RPC就绪 |



实际录像结论：第一轮连续MP4失败；原因是官方保存端缺imageio-ffmpeg，PyAV codec=None。此前CPU测试用策略环境是覆盖遗漏。已补robotwin依赖，在正确环境CPU编码+解码3帧通过；本轮连续帧已丢失，只有12张关键帧。
