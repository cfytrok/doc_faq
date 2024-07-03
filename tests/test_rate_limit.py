import datetime
from unittest.mock import patch

import pytest
import streamlit as st
from openai.types.chat import ChatCompletion, ChatCompletionMessage
from openai.types.chat.chat_completion import Choice
from streamlit.testing.v1 import AppTest

def test_session_rate_limit(rag_chain):
    at = AppTest.from_file('app.py')
    at.secrets['OPENAI_API_KEY'] = 'myapikey'
    at.secrets['SESSION_TOKEN_LIMIT'] = '1/day'
    at.secrets['SYSTEM_TOKEN_LIMIT'] = '100/day'
    at.run()

    assert not at.main.error
    at.text_area('question').set_value('long question')
    at.run()
    assert at.main.error[0].value

def test_system_rate_limit(rag_chain):
    st.cache_resource.clear()
    at = AppTest.from_file('app.py')
    at.secrets['OPENAI_API_KEY'] = 'myapikey'
    at.secrets['SESSION_TOKEN_LIMIT'] = '100/day'
    at.secrets['SYSTEM_TOKEN_LIMIT'] = '1/day'
    at.run()

    assert not at.main.error
    at.text_area('question').set_value('long question')
    at.run()
    assert at.main.error[0].value


