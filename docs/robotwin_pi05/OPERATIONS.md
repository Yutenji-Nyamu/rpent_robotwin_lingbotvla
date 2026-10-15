# 逐项操作记录

时间为2026-10-15深圳时间；机器JSON回执用于精确时间/身份。

| 阶段 | 操作 | 结果 |
|---|---|---|
| 上下文 | 读取PROJECT_CONTEXT、HANDOFF、RPent结果、Sidney首次推理及RLinf转换账本 | 锁定两条已有验收链；不重新转换模型 |
| 现场 | 固定host-key Paramiko普通账户登录SZ1 | chenyiteng/UID1003/admin；当前EXPO占4/5，GRPO占6/7，准备期均保持 |
| 资产 | 核本机模型/环境、容量与原owner请求 | 两套Sidney模型与旧环境完整可见，data约501GiB、home85GiB可用；RLT5候补CP100 |
| 资料 | OpenAI Docs核对SDK说明 | Python SDK控制真实Codex app-server，经JSON-RPC；云模型与本地工具分层 |
| 网络 | 尝试读取SZ3已有RPent源码 | SSH channel超时；转为在目标SZ1从已公开仓库克隆，不需要再次下载模型 |
| Git | 默认SSH连接GitHub因未指定既有known_hosts而失败 | 定位既有Yutenji账户key和专用known_hosts；官方HTTPS meta核Github公开指纹，使用现成非交互身份，不改全局SSH配置 |
| Git准备 | 在SZ1克隆既有公开仓库，创建独立分支，配置repo-local core.sshCommand和upstream | 账户回执Hi Yutenji-Nyamu；基线1b641df；本地不克隆 |
| 源码 | 读取RPent贡献、robot/verify/docs技能及模型、工具、提示、RPC调用双方 | 选择现有RoboTwin qpos入口，新增隔离π0.5服务；旧env/model转换不重写 |
| EXPO恢复 | 查train_expo_formal.py与当前checkpoint.json | 原run/checkpoint-latest.pt存在；保存模型/core/replay/cadence/RNG/progress；--resume验证完整状态与预算 |
| 安装 | 新建服务器.venv-robotwin，采用官方robotwin依赖；另建deployment/pi05-runtime，通过pth只读复用旧模型环境 | 不改旧环境，不创建GPU上下文 |
| 网络复用 | cuRobo SSH fetch停留且同d64c4b0源码已缓存 | 精确结束本次安装进程组；改用同commit本地缓存与固定RLinf05379a6源码归档，不改版本 |
| 接入 | 新增pi05服务、CLI后端选项、pi05_act、工具筛选和提示上下文 | π0.5固定H50/M10/QPOS14，LingBot保持默认；先预热再环境 |
| 专项CPU检查 | pytest tests/unit_tests/robots/robotwin -q | 13 passed / 1 skipped；真实仿真待依赖完成 |
| 全量CPU检查 | pytest tests/unit_tests -q | 1219 passed / 5 skipped / 1 failed；新增工具导致旧快照差异，更新对应项，待复测 |
| 视频 | 沿用EnvState.save保存3帧MP4 | 成功写出；不新写录制路径 |
| 旧模型导入 | 完整导入OpenPI模型类 | 检出HF2.2与transformers4.57.6冲突；独立环境固定HF0.36.2、OmegaConf2.3.1、filelock3.32.3，原环境不变 |

详细回执：`/data/chenyiteng/deployment-20261015/rpent-pi05-g4`。本地小助手：`local_scripts/rpent_pi05_20261015/`；密码仅在进程。

- 安装完成：官方仿真环境296包兼容性通过；资产与SAPIEN绑定接口核验通过。
- 模型环境：旧site-packages优先，解决HF及cryptography/OpenSSL混装冲突；不修改旧环境。
- 验证：1226 passed / 6 skipped；pre-commit通过。
- 规划器：GPT-5.5实际HTTP400不支持；用户选择GPT-6.1-Sol/xhigh，实际SDK请求返回ok。
- Memory：复用官方RLinf/RPent-memory robotwin/**，107文件170980字节，revision 47f301ef33bf8d0e8c770342f16b3c39c6a0e8c1。
- 现场：EXPO仍占4/5，检查点340回合47810物理动作1151更新；GRPO6/7保持。

- 交卡：精确停止CPU owner并保留子任务，只将4卡释放门指向本次EXPO返回runtime；5/6/7字段原样保留，重启既有owner。
- EXPO：按PID/UID/start精确SIGTERM；原pair owner确认exit143、清场成功。回执后1.43秒启动RPent。
- RLT5：原候补请求派发，CP100恢复并进入rollout；暂不声称产生新的学习检查点。
- 策略：真实权重加载及warmup成功，RPC监听；仿真首次编译cuRobo扩展，已核正在产生对象文件。

- cuRobo首次编译：tensor_step、kinematics_fused、line_search、geom、lbfgs_step五个扩展完成，环境RPC监听。
- RLT指标边界：采样/回放已推进，update_step仍0，不能记作新的参数学习结果。

- 原生结果：3次pi05_act，50+50+15=115动作，eval_success=true、terminated、非truncated、exit0；无几何动作和重置。
- 导出：4组×3相机关键帧，states/recipe/transcript完整。
- 录像诊断：实际官方环境缺imageio-ffmpeg，PyAV收到codec=None。此前检查使用策略环境，覆盖遗漏。robotwin extra补imageio-ffmpeg0.6.0；实际官方环境CPU写入并解码3帧240×320 MP4成功，不是回合录像。
- 交还：精确停止RLT5，核namespace和4/5卡C/G清场；原EXPO pair owner恢复同run/预算；6/7槽位与GPU进程保持。
- EXPO恢复回执：resume_verified，340回合、47810动作、1152更新，恢复pending_calls=4，正在推进恢复后学习。

- 交还核验：EXPO已从1152更新推进到1153，pending_calls 4→3；4/5仅返回EXPO，6/7原PID集合不变。
- 临时认证：私有tmpfs认证目录在确认无使用进程后删除；凭据未进入仓库。
