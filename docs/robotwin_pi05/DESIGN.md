# 架构与移植设计

## RPent里的Codex是什么

是实际Codex运行时。官方Python包`openai-codex`通过JSON-RPC控制本机Codex app-server；RPent在其外侧提供机器人任务、提示、记忆和MCP工具。Codex再调用云端模型，因此“有Codex进程”和“内部经API调用模型”同时成立。

链路：云端大模型 ↔ 服务器Codex app-server ↔ RPent MCP工具 ↔ 环境/策略服务。桌面UI不属于这条执行链；具体planner配置与工具暴露以本次固定RPent源码为准。

依据：[官方Codex SDK](https://learn.chatgpt.com/docs/codex-sdk)，2026-10-15已读取；本项目`rpent/planner/codex.py`。

## π0.5切口

主要差异不是模型文件名，而是原生接口：LingBot接受eef16并输出EEF动作，Sidney π0.5接受qpos14并输出absolute关节目标。新增可选择的π0.5服务/工具，使用已验收模型包装器和原生QPOS执行，不把14维数值冒充EEF16，也不重新转换权重。

复用同一RoboTwin任务状态、成功标志、观察及几何原语；保留LingBot默认入口。新增`--vla-backend pi05`、`--pi05-python`、`--pi05-rlinf-repo`；策略服务用独立解释器复用旧RLinf，环境服务仍用官方RPent环境。

修改切口：`robots/robotwin/pi05.py`负责三相机/QPOS14打包、既有get_model/predict_action_batch与统一RPC；`robot_spec.py`负责选择后端、生命周期与先模型预热后仿真；`primitives.py`共用原动作循环，只区分ee/qpos；`toolkit.py`只注册选定策略的工具；`prompt_bundle.py`保持任务策略并替换模型工具名称，明确旧LingBot配方不能证明π0.5效果。对应CPU契约测试覆盖像素/状态顺序、维度拒绝、原生成功提前停止、互斥工具与失败清理。

状态一致性来源：旧RoboTwin的`joint_action.vector`与RPent的`qpos_target14`都由`get_left_arm_jointState() + get_right_arm_jointState()`组成。数值不做EEF转换，也不再次归一化。图像保持原始RGB，由旧模型处理器负责尺寸与归一化。

## 已确定边界

- 首测继承RPent任务`beat_block_hammer/demo_randomized/seed100000`，不自行筛成功seed。
- 规划器采用用户确认的Codex/GPT-6.1-Sol/xhigh与原预算；当前账户拒绝旧GPT-5.5，6.1-Sol实际SDK请求已返回ok（11.33秒）。这是相对旧LingBot回合的一项配置变化。
- 使用未训练的多任务SFT检查点；只验证工程链，不把一次成功归因于新方法。
- 继承原生动作chunk执行，原生成功可提前停止；明确区分请求步数与实际步数。
- 必须有π0.5实际调用证据，纯几何工具完成不能充当π0.5集成验收。
