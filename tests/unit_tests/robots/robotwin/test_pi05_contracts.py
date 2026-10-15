# Copyright 2026 The RPent Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Offline observation, action and prompt boundaries for the pi0.5 adapter."""

from types import SimpleNamespace

import numpy as np
import pytest

from robots.robotwin import robot_spec
from robots.robotwin.pi05 import Pi05VLAClient, policy_input, runtime_contract
from robots.robotwin.primitives import RoboTwinPrimitives
from robots.robotwin.prompt_bundle import system_prompt


def observation():
    return {
        "views": {
            name: {"rgb": np.full((16, 16, 3), i, dtype=np.uint8)}
            for i, name in enumerate(("head", "left_wrist", "right_wrist"))
        },
        "robot_state": {"qpos_target14": np.arange(14, dtype=np.float64)},
        "task_language": "native instruction",
    }


def test_input_keeps_camera_pixels_joint_order_and_native_instruction():
    packed = policy_input(observation())
    assert packed["main_images"].shape == (1, 16, 16, 3)
    assert packed["wrist_images"].shape == (1, 2, 16, 16, 3)
    assert (packed["wrist_images"][0, 0] == 1).all()
    assert (packed["wrist_images"][0, 1] == 2).all()
    np.testing.assert_array_equal(packed["states"], np.arange(14)[None])
    assert packed["task_descriptions"] == ["native instruction"]


def test_eef_state_cannot_be_used_as_pi05_state():
    obs = observation()
    obs["robot_state"]["qpos_target14"] = np.zeros(16)
    with pytest.raises(ValueError, match="qpos_target14"):
        policy_input(obs)


@pytest.mark.parametrize("shape", [(50, 16), (49, 14)])
def test_client_rejects_incompatible_policy_actions(shape):
    rpc = SimpleNamespace(call=lambda *args, **kwargs: {"action": np.zeros(shape)})
    with pytest.raises(RuntimeError, match="invalid actions"):
        Pi05VLAClient(rpc).infer(observation())


def test_client_checks_backend_identity():
    rpc = SimpleNamespace(call=lambda *args, **kwargs: {"runtime": "lingbotvla"})
    with pytest.raises(RuntimeError, match="metadata mismatch"):
        Pi05VLAClient(rpc).validate_contract()
    rpc.call = lambda *args, **kwargs: runtime_contract()
    Pi05VLAClient(rpc).validate_contract()


def test_pi05_executes_qpos_and_stops_after_native_success():
    status = {"eval_success": False, "take_action_cnt": 0, "step_lim": 100}
    env = SimpleNamespace(
        last_info={"episode_status": status}, execution_capabilities={}
    )
    calls = []

    def step(actions, *, action_type, return_all_frames):
        calls.append((actions, action_type))
        status.update(eval_success=True, take_action_cnt=3)
        return {}, None, None, None, {"episode_status": status, "executed_actions": 3}

    env.chunk_step = step
    model = SimpleNamespace(infer=lambda obs: np.zeros((50, 14)))
    primitive = RoboTwinPrimitives(
        env=env,
        model=model,
        seed=100000,
        check_cancelled=lambda: None,
        vla_backend="pi05",
    )
    primitive._build_lingbot_observation = observation
    result = primitive.pi05_act(chunks=4, prompt="ignored planner text")
    assert len(calls) == 1 and calls[0][1] == "qpos"
    assert result.data["executed_steps"] == 3
    assert result.data["stop_reason"] == "native_success"
    assert result.data["prompt"] == "native instruction"
    with pytest.raises(ValueError, match="LingBot backend"):
        primitive.lingbot_act(chunks=1)


def test_prompt_names_match_active_backend():
    lingbot = str(system_prompt({"vla_backend": "lingbot"}))
    pi05 = str(system_prompt({"vla_backend": "pi05"}))
    assert "lingbot_act" in lingbot and "pi05_act" not in lingbot
    assert "pi05_act" in pi05 and "lingbot_act" not in pi05
    assert "QPOS14" in pi05 and "another policy" in pi05


def test_pi05_startup_warms_policy_before_environment_and_cleans_on_failure(
    monkeypatch, tmp_path
):
    order = []
    daemon = SimpleNamespace(poll=lambda: None)
    events = SimpleNamespace(emit=lambda event: None)
    monkeypatch.setattr(
        robot_spec, "_spawn_vla_server", lambda *args: (daemon, ("localhost", 1234))
    )
    monkeypatch.setattr(
        robot_spec,
        "_wait_for_tcp",
        lambda *args, **kwargs: order.append("policy_ready"),
    )
    monkeypatch.setattr(Pi05VLAClient, "validate_contract", lambda self: None)
    monkeypatch.setattr(
        robot_spec, "stop_owned_daemons", lambda owned, events: order.append("cleanup")
    )

    def fail_env(*args, **kwargs):
        order.append("environment")
        raise RuntimeError("simulator unavailable")

    monkeypatch.setattr(robot_spec, "try_spawn_server", fail_env)
    with pytest.raises(RuntimeError, match="simulator unavailable"):
        robot_spec._init_runtime(
            SimpleNamespace(vla_backend="pi05"), tmp_path, events, None
        )
    assert order == ["policy_ready", "environment", "cleanup"]
