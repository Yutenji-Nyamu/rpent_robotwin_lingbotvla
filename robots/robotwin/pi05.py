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

"""Sidney RoboTwin pi0.5 adapter over the previously validated RLinf policy."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import numpy as np

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from rpent.robots.components.vla_client_base import BaseVLAClient
from rpent.robots.components.vla_facade_base import BaseVLAFacade

SOURCE_REVISION = "e49e2ab6c11f07511573b67261bd129e88d0a416"


def runtime_contract() -> dict[str, Any]:
    """Describe the converted checkpoint's native observation/action contract."""
    return {
        "runtime": "rlinf_sidney_pi05",
        "policy_name": "pi05_sidney_robotwin",
        "camera_order": ["head", "left_wrist", "right_wrist"],
        "state_layout": "qpos14",
        "action_layout": "qpos14",
        "use_length": 50,
        "num_steps": 10,
        "source_revision": SOURCE_REVISION,
    }


def policy_input(observation: dict[str, Any]) -> dict[str, Any]:
    """Map RPent observations to the accepted RLinf batch input without transforms."""
    views = observation["views"]
    state = np.asarray(observation["robot_state"]["qpos_target14"], dtype=np.float32)
    if state.shape != (14,) or not np.isfinite(state).all():
        raise ValueError("pi0.5 requires finite absolute qpos_target14 state")
    images = [
        np.asarray(views[name]["rgb"]) for name in runtime_contract()["camera_order"]
    ]
    for image in images:
        if image.ndim != 3 or image.shape[-1] != 3 or image.dtype != np.uint8:
            raise ValueError("pi0.5 cameras must contain uint8 HWC RGB images")
    return {
        "main_images": images[0][None],
        "wrist_images": np.stack(images[1:])[None],
        "extra_view_images": None,
        "states": state[None],
        "task_descriptions": [observation["task_language"]],
    }


class Pi05VLAClient(BaseVLAClient):
    """Use the common RPC transport for the isolated pi0.5 service."""

    def validate_contract(self) -> None:
        actual = self._client.call("vla.get_metadata")
        if actual != runtime_contract():
            raise RuntimeError(f"pi0.5 runtime metadata mismatch: {actual!r}")

    def infer(self, observation: dict[str, Any]) -> np.ndarray:
        """Return one absolute QPOS14 action chunk."""
        actions = np.asarray(
            self.predict(policy_input(observation))["action"], dtype=np.float64
        )
        if actions.shape != (50, 14) or not np.isfinite(actions).all():
            raise RuntimeError(f"pi0.5 returned invalid actions: {actions.shape}")
        return actions


class Pi05VLAFacade(BaseVLAFacade):
    """Load the existing RLinf conversion and retain its model/data processors."""

    def __init__(self, model_path: Path, rlinf_repo: Path, seed: int):
        import torch
        from omegaconf import OmegaConf

        sys.path.insert(0, str(rlinf_repo))
        from rlinf.models.embodiment.openpi import get_model

        manifest = json.loads((model_path / "conversion_manifest.json").read_text())
        if manifest["source_revision"] != SOURCE_REVISION:
            raise ValueError("Expected the accepted Sidney pi05_robotwin conversion")
        config = OmegaConf.load(
            rlinf_repo / "examples/embodiment/config/model/pi0_5.yaml"
        )
        config.model_path = str(model_path)
        config.num_action_chunks = 50
        config.action_dim = 14
        config.num_steps = 10
        config.openpi.config_name = "pi05_sidney_robotwin"
        config.openpi.num_images_in_input = 3
        config.openpi.action_chunk = 50
        config.openpi.num_steps = 10
        config.openpi.noise_level = 0.3
        config.openpi.train_expert_only = True
        torch.backends.cuda.enable_cudnn_sdp(False)
        torch.manual_seed(seed)
        self.model = get_model(config).to("cuda:0").eval()
        # Reuse the accepted RGB/QPOS dummy warmup, preserving evaluation RNG.
        with torch.random.fork_rng(devices=[0]), torch.inference_mode():
            self.model.predict_action_batch(
                {
                    "main_images": torch.zeros((1, 224, 224, 3), dtype=torch.uint8),
                    "wrist_images": torch.zeros((1, 2, 224, 224, 3), dtype=torch.uint8),
                    "extra_view_images": None,
                    "states": torch.zeros((1, 14)),
                    "task_descriptions": ["adjust the bottle"],
                },
                mode="eval",
                compute_values=False,
            )
        self.calls = 0
        super().__init__()

    def _register_rpc(self):
        super()._register_rpc()
        self._rpc["vla.get_metadata"] = runtime_contract

    def predict(self, obs, options=None):
        """Run the accepted ODE evaluation and output unnormalized native actions."""
        import torch

        if options:
            raise ValueError("pi0.5 uses the fixed H50/M10 evaluation contract")
        inputs = {
            key: torch.as_tensor(value, device="cuda:0")
            if isinstance(value, np.ndarray)
            else value
            for key, value in obs.items()
        }
        with torch.inference_mode():
            actions, _ = self.model.predict_action_batch(
                inputs, mode="eval", compute_values=False
            )
        self.calls += 1
        return {"action": actions[0].detach().cpu().numpy(), "policy_call": self.calls}


def spawn_server(args, output_dir):
    """Use RPent's owned-daemon lifecycle with an isolated policy interpreter."""
    from robots.robotwin.robot_spec import _parse_vla_endpoint, _resolve_cuda_devices
    from rpent.utils.config import get_repo_root
    from rpent.utils.daemon import ProcessDaemon, pick_free_port

    if args.vla_endpoint is not None:
        return None, _parse_vla_endpoint(args.vla_endpoint)
    for option in ("vla_model_path", "pi05_python", "pi05_rlinf_repo"):
        value = getattr(args, option, None)
        if not value or not Path(value).exists():
            raise ValueError(
                f"--{option.replace('_', '-')} must identify an existing path"
            )
    _, device = _resolve_cuda_devices(args)
    host, port = "127.0.0.1", pick_free_port()
    daemon = ProcessDaemon(
        "pi05_vla_server",
        [
            args.pi05_python,
            str(get_repo_root() / "robots/robotwin/pi05.py"),
            "--model-path",
            args.vla_model_path,
            "--rlinf-repo",
            args.pi05_rlinf_repo,
            "--seed",
            str(args.seed),
            "--port",
            str(port),
            "--parent-watch",
        ],
        env_overrides={
            "PYTHONPATH": str(get_repo_root()),
            **({"CUDA_VISIBLE_DEVICES": device} if device is not None else {}),
        },
        log_path=str(output_dir / "pi05_vla_server.log"),
    )
    daemon.start()
    return daemon, (host, port)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-path", type=Path, required=True)
    parser.add_argument("--rlinf-repo", type=Path, required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--parent-watch", action="store_true")
    args = parser.parse_args()
    facade = Pi05VLAFacade(args.model_path, args.rlinf_repo, args.seed)
    facade.serve(
        transport="http",
        host="127.0.0.1",
        port=args.port,
        parent_watch=args.parent_watch,
    )


if __name__ == "__main__":
    main()
