from __future__ import annotations

import logging
import os
from time import sleep
from typing import Iterable

import replicate

from providers.base_provider import BaseProvider


class ReplicateProvider(BaseProvider):
    def __init__(self, api_key: str):
        super().__init__(None, api_key)
        os.environ["REPLICATE_API_TOKEN"] = api_key

    def _get_model_list(self) -> list:
        raise NotImplementedError

    def is_model_available(self, model_name) -> bool:
        raise NotImplementedError

    def get_model(self, model_name) -> dict:
        raise NotImplementedError

    def generate(self, model: str, message: str, temperature: float = 0.9) -> Iterable:
        if self.exceed_limits():
            logging.info(
                f"Failed to call Cohere API, exceeded limits: "
                f"{self.get_session_usage()}",
            )
            return -1

        max_retry = 5
        retry = 0
        while retry < max_retry:
            try:
                response = replicate.run(
                    model, input={"prompt": message, "temperature": temperature}
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

            response = ["".join(response).strip()]

            self.history.append((model, message, response))
            self.session_requests += 1

            print(response)

            return response

        raise Exception("Failed to call Replicate API, exceeded retry limit")
