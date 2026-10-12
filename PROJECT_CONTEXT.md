# RoboTwin–LingBot-VLA reproduction context

This public fork preserves [RLinf/RPent](https://github.com/RLinf/RPent), its history, original README and Apache-2.0 license. Our goal is to run one native-success episode with the official RoboTwin example and LingBot EEF checkpoint before considering broader experiments.

- Start here: [discussion, decisions, plan and execution records](docs/robotwin_lingbotvla/README.md).
- First task: `beat_block_hammer`, `demo_randomized`, seed `100000`.
- Source baseline: `161be6bfe7574c4b9770abd5b53617136127bb98`.
- Checkpoint: `RLinf/LingBot-VLA-RoboTwin-EEF-ckpt1500`, revision `e727b46cd220b66981ea4d2fd9ba84adc189e2cc`.
- Setup and large artifacts live on the execution server. Only reviewed source and lightweight documentation belong in this repository.
- Current state: environment/model preparation in progress; a successful RPent robot episode has not yet been demonstrated. See the execution record for updates.

The original upstream README remains the general project introduction. Task success is the environment's native `TASK_ENV.eval_success`, recorded separately from planner completion.
