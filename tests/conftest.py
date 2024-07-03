from unittest.mock import patch

import pytest
from streamlit.testing.v1 import AppTest


@pytest.fixture
def rag_chain():
    with patch('rag_chain.get_rag_chain') as mock:
        mock.return_value.invoke.return_value = 'bar'
        yield mock

@pytest.fixture
def at():
    at = AppTest.from_file('app.py')
    at.secrets['OPENAI_API_KEY'] = 'system_api_key'
    at.secrets['SESSION_TOKEN_LIMIT'] = '10000/day'
    at.secrets['SYSTEM_TOKEN_LIMIT'] = '100000/7day'
    return at