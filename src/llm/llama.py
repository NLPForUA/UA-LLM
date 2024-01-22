from __future__ import annotations

from enum import Enum

from llm.base_llm import BaseLLM
from providers.replicate_provider import ReplicateProvider


class PromptStrategy(Enum):
    NONE = "none"
    SYSTEM_FIRST = "system_first"
    SYSTEM_LAST = "system_last"


class LLaMa(BaseLLM):
    def __init__(
        self,
        provider: ReplicateProvider,
        model_generation: str,
        model_version: str = "",
        temperature: float = 0.9,
    ):
        self.provider = provider
        self.model_generation = model_generation
        self.model_version = model_version
        self.model_name = (
            f"{self.model_generation}-{self.model_version}"
            if self.model_version
            else self.model_generation
        )
        self.temperature = temperature
        print(f"Using model {self.model_name} with temperature {self.temperature}")

    def predict(
        self,
        prompt: str,
        system_message: str,
        prompt_strategy: PromptStrategy,
    ) -> str:
        response = self.provider.generate(
            model=self.model_name,
            message=prompt,
            temperature=self.temperature,
        )
        if response == -1:
            return "Failed to call Replicate API, exceeded limits"
        return response[0]
