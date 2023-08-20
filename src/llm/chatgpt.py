from __future__ import annotations

from enum import Enum

from llm.base_llm import BaseLLM
from providers.openai_provider import OpenaiProvider


class PromptStrategy(Enum):
    NONE = 'none'
    SYSTEM_FIRST = 'system_first'
    SYSTEM_LAST = 'system_last'


class ChatGPT(BaseLLM):
    def __init__(self, provider: OpenaiProvider, generation, version):
        self.provider = provider
        self.generation = generation
        self.version = version

    def predict(
            self,
            prompt: str,
            system_message: str,
            prompt_strategy: PromptStrategy,
    ) -> str:
        messages = [{'role': 'user', 'content': prompt}]
        if system_message:
            if prompt_strategy == PromptStrategy.SYSTEM_FIRST:
                messages = [
                    {'role': 'system', 'content': system_message},
                ] + messages
            else:
                messages.append({'role': 'system', 'content': system_message})
        completion = self.provider.chat_completion(
            model=self.generation,
            prompt=prompt,
        )
        if completion == -1:
            return 'Failed to call OpenAI API, exceeded limits'
        return completion.choices[0].message.content
