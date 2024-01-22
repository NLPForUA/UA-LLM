from __future__ import annotations

from enum import Enum

from llm.base_llm import BaseLLM
from providers.openai_provider import OpenAIProvider


class PromptStrategy(Enum):
    NONE = "none"
    SYSTEM_FIRST = "system_first"
    SYSTEM_LAST = "system_last"


class ChatGPT(BaseLLM):
    def __init__(
        self,
        provider: OpenAIProvider,
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
        messages = [{"role": "user", "content": prompt}]
        if system_message:
            if prompt_strategy == PromptStrategy.SYSTEM_FIRST:
                messages = [
                    {"role": "system", "content": system_message},
                ] + messages
            else:
                messages.append({"role": "system", "content": system_message})
        completion = self.provider.chat_completion(
            model=self.model_name,
            messages=messages,
            temperature=self.temperature,
        )
        if completion == -1:
            return "Failed to call OpenAI API, exceeded limits"
        return completion.choices[0].message.content
