from __future__ import annotations

import logging
from time import sleep
from typing import List

import openai

from providers.base_provider import BaseProvider


class OpenAIProvider(BaseProvider):
    def __init__(self, org_id: str, api_key: str):
        super().__init__(org_id, api_key)
        openai.api_key = self.api_key
        openai.organization = self.org_id

    def _get_model_list(self) -> openai.openai_object.OpenAIObject:
        return openai.Model.list()

    def is_model_available(self, model_name) -> bool:
        return self.get_model(model_name) is not None

    def get_model(self, model_name) -> openai.api_resources.model.Model:
        model_list = self._get_model_list()

        if "data" not in model_list:
            raise Exception("Failed to get model list from OpenAI")

        models_data = model_list["data"]
        for model_data in models_data:
            if model_data["id"] == model_name:
                return model_data

        return None

    def chat_completion(
        self, model: str, messages: List[dict], temperature: float = 0.9
    ) -> openai.ChatCompletion:
        if self.exceed_limits():
            logging.info(
                f"Failed to call OpenAI API, exceeded limits: "
                f"{self.get_session_usage()}",
            )
            return -1

        max_retry = 5
        retry = 0
        while retry < max_retry:
            try:
                completion = openai.ChatCompletion.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    request_timeout=60,
                )
            except Exception as e:
                if e:
                    print(e)
                    print("Failed to call OpenAI API, retrying in 10 seconds")
                    sleep(10)
                    retry += 1
                    continue
                else:
                    raise e

            self.history.append((model, messages, completion))
            self.session_requests += 1
            self.session_prompt_tokens += completion.usage.prompt_tokens
            self.session_response_tokens += completion.usage.completion_tokens
            self.session_total_tokens += completion.usage.total_tokens

            return completion

        raise Exception("Failed to call OpenAI API, exceeded retry limit")
