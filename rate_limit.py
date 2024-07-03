import os

import streamlit as st
import tiktoken
from limits import storage, strategies, parse


class RateLimitError(Exception):
    pass


def num_tokens_from_string(string: str, model_name: str) -> int:
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def make_rate_limit(name, limit_string):
    memory_storage = storage.MemoryStorage()
    moving_window = strategies.MovingWindowRateLimiter(memory_storage)
    limit_item = parse(limit_string)

    def f(num_tokens: int):
        if not moving_window.hit(limit_item, name, cost=num_tokens):
            raise RateLimitError
        return

    return f


@st.cache_resource
def system_rate_limit():
    return make_rate_limit('system_limit', st.secrets['SYSTEM_TOKEN_LIMIT'])
