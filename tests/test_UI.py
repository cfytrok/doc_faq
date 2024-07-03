import datetime
from unittest.mock import patch

import pytest
import streamlit as st
from openai.types.chat import ChatCompletion, ChatCompletionMessage
from openai.types.chat.chat_completion import Choice
from streamlit.testing.v1 import AppTest

def test_sidebar(at):
    at.run()
    api_key = at.sidebar.text_input('openai_api_key')
    assert api_key.value == ''
    assert 'Get an OpenAI API key' in at.sidebar.markdown[0].value
    assert 'View the source code' in at.sidebar.markdown[1].value
    api_key.set_value('foo')
    at.run()
    assert api_key.value == 'foo'


def test_question(rag_chain, at):
    at.run()
    assert at.text_area('question').value == ''
    at.text_area('question').set_value('foo')
    at.run()
    assert at.main.markdown[0].value == 'bar'


def test_choose_model(at):
    at.run()
    model = at.sidebar.selectbox('model')
    assert model.value == 'gpt-3.5-turbo'
    model.set_value('gpt-4o')
    at.run()
    assert at.sidebar.error[0].value

    at.sidebar.text_input('openai_api_key').set_value('foo')
    at.run()
    assert model.value == 'gpt-4o'
    at.run()
    assert not at.sidebar.error

def test_api_key(rag_chain, at):
    at.run()
    at.text_area('question').set_value('foo')
    at.run()
    assert rag_chain.call_args.args[0] == 'system_api_key'
    at.sidebar.text_input('openai_api_key').set_value('user_api_key')
    at.run()
    assert rag_chain.call_args.args[0] == 'user_api_key'
    assert at.sidebar.text_input('openai_api_key').value == 'user_api_key'