from __future__ import annotations


class BaseLLM:
    def predict(self, prompt: str) -> str:
        raise NotImplementedError()
