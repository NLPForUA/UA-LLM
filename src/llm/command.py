from __future__ import annotations

from llm.base_llm import BaseLLM, PromptStrategy
from providers.cohere_provider import CohereProvider


class Command(BaseLLM):
    def __init__(
        self,
        provider: CohereProvider,
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
        print(response.generations[0].text)

        if response == -1:
            return "Failed to call OpenAI API, exceeded limits"
        return response.generations[0].text
