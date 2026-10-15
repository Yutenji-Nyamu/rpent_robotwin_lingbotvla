# 两条既有链路与复用合同

## π0.5来源

- 原始模型：`SidneyXie/pi05_robotwin`，revision `e49e2ab6c11f07511573b67261bd129e88d0a416`。
- 首次原生推理：2026-09-02/03，LeRobot v0.6.0 `30da8e687a6dfc617fcd94afc367ac7071c376ce`，隔离Python3.10 typing兼容。调瓶子5个有效回合5/5，订书机5个有效回合2/5；不是完整基准结果。
- 模型合同：H50/M10、三路RGB、14D absolute QPOS、checkpoint自带mean/std、内部32D padding；不引入delta动作或重复归一化。
- 后续已验收RLinf转换：813/813 key、零missing/unexpected/shape mismatch、逐tensor相等；同输入/提示/noise下与LeRobot动作对齐，B=1原生环境闭环通过。
- 服务器现成模型：`/data/chenyiteng/models/lerobot/sidney-pi05-robotwin-e49e2ab`及`/data/chenyiteng/models/rlinf-native/sidney-pi05-robotwin-e49e2ab`。
- 现成环境：`/home/chenyiteng/venvs/rlinf-7d07-openpi-robotwin`；先从当前已验收包装器导出实际配置，实施前锁定代码与调用链。

## RPent来源

- 已验收公开HEAD `1b641dfc4fa5f8127b999376975e62006287cc6d`，上游运行基线`161be6bfe7574c4b9770abd5b53617136127bb98`。
- 2026-10-12：`beat_block_hammer/demo_randomized/100000`原生成功，95动作、两次LingBot、exit0。
- 复用规划器、MCP工具调用、原生成功判定、记忆读取、观察/执行/退出链。
- 有意变化：VLA与相应状态/动作接口由LingBot EEF16换为π0.5 QPOS14；Python运行时隔离复用，不污染在跑训练环境。
- 旧连续MP4导出失败；本次原编码入口CPU验证通过，无需修改，再使用原录制帧，不新写逐控制步取图机制。

## 必须逐项保留

旧模型加载、相机顺序和尺寸变换、状态排列、tokenizer、mean/std、M10、H50、环境动作解释与成功判定。只新增RPent接入层；不混入DVCA、Attn、额外M5、RL或训练权重。

初始化/并行/录像选择须引用已验收入口。首测B=1；GPU环境与策略优先同物理4卡。模型冻结，先按旧链预热再建仿真，沿用已有单卡计算/图形绑定。


本次锁定RLinf包装器HEAD：1d015a2aa03ec8132d8207ba47a2be3dbe1d9591，服务器sidney-pi05-current-rlinf工作树clean。官方RPent环境与旧模型环境分离：官方Torch2.7.1/SAPIEN3.0.0b1；策略服务读取旧Torch2.11.0+cu129/Transformers4.57.6，优先旧site-packages，新venv只补RPC依赖。
