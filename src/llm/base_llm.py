from __future__ import annotations

from enum import Enum


class PromptStrategy(Enum):
    NONE = "none"
    SYSTEM_FIRST = "system_first"
    SYSTEM_LAST = "system_last"


class BaseLLM:
    def predict(self, prompt: str) -> str:
        raise NotImplementedError()
