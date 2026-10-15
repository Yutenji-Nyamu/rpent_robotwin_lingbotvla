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

"""RoboTwin prompt bundle assembly."""

from __future__ import annotations

from collections.abc import Mapping

from robots.robotwin.prompts import evaluate as evaluate_parts
from robots.robotwin.prompts import explore as explore_parts
from robots.robotwin.prompts import user as user_parts
from rpent.prompt.utils import PromptNode


def system_prompt(
    variables: Mapping[str, object] | None = None,
) -> PromptNode:
    """Return the RoboTwin system prompt for the selected run mode."""
    if (variables or {}).get("mode", "eval") == "explore":
        prompt = explore_parts.system_prompt()
    else:
        prompt = evaluate_parts.system_prompt(variables)
    if (variables or {}).get("vla_backend") == "pi05":
        prompt = {
            key: value.replace("lingbot_act", "pi05_act")
            .replace("LingBot-VLA", "Sidney pi0.5")
            .replace("LingBot", "pi0.5")
            if isinstance(value, str)
            else value
            for key, value in prompt.items()
        }
        prompt["POLICY CONTRACT"] = (
            "The active policy is Sidney pi0.5: three RGB views and absolute QPOS14, "
            "H50/M10. Use pi05_act. Archived LingBot recipes describe another policy; "
            "their timing and policy success do not establish pi0.5 behavior. Reuse "
            "geometric observations only after verifying them in the current scene."
        )
    return prompt


def user_prompt(
    variables: Mapping[str, object] | None = None,
) -> PromptNode:
    prompt = {
        "CELL": user_parts.CELL,
        "BEGIN": user_parts.BEGIN,
    }
    if (variables or {}).get("mode", "eval") == "explore":
        prompt["EXPLORE MODE"] = explore_parts.USER_MODE
    return prompt


__all__ = ["system_prompt", "user_prompt"]
