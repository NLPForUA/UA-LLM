from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Tuple


@dataclass
class SessionUsage:
    requests: int
    prompt_tokens: int
    response_tokens: int
    total_tokens: int


class BaseProvider:
    def __init__(
        self,
        org_id,
        api_key,
        requests_limit=0,
        prompt_tokens_limit=0,
        total_tokens_limit=0,
    ):
        self.org_id = org_id
        self.api_key = api_key
        self.requests_limit = requests_limit
        self.prompt_tokens_limit = prompt_tokens_limit
        self.total_tokens_limit = total_tokens_limit
        self.session_requests = 0
        self.session_prompt_tokens = 0
        self.session_response_tokens = 0
        self.session_total_tokens = 0
        self.history = []

    def _get_model_list(self):
        raise NotImplementedError()

    def is_model_available(self, model_name):
        raise NotImplementedError()

    def get_model(self, model_name):
        raise NotImplementedError()

    def get_session_usage(self) -> Tuple[int, int, int, int]:
        return SessionUsage(
            requests=self.session_requests,
            prompt_tokens=self.session_prompt_tokens,
            response_tokens=self.session_response_tokens,
            total_tokens=self.session_total_tokens,
        )

    def exceed_requests_limit(self) -> bool:
        return self.requests_limit > 0 and self.session_requests >= self.requests_limit

    def exceed_prompt_tokens_limit(self) -> bool:
        return (
            self.prompt_tokens_limit > 0
            and self.session_prompt_tokens >= self.prompt_tokens_limit
        )

    def exceed_total_tokens_limit(self) -> bool:
        return (
            self.total_tokens_limit > 0
            and self.session_total_tokens >= self.total_tokens_limit
        )

    def exceed_limits(self) -> bool:
        if self.exceed_requests_limit():
            logging.info(
                f"Exceeded requests limit: {self.requests_limit}",
            )
            return True
        if self.exceed_prompt_tokens_limit():
            logging.info(
                f"Exceeded prompt tokens limit: {self.prompt_tokens_limit}",
            )
            return True
        if self.exceed_total_tokens_limit():
            logging.info(
                f"Exceeded total tokens limit: {self.total_tokens_limit}",
            )
            return True
        return False
