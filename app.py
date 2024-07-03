import os

import streamlit as st

from rag_chain import get_rag_chain
from rate_limit import system_rate_limit, make_rate_limit, num_tokens_from_string, RateLimitError

def limit_requests(question: str):
    if 'session_limit' not in st.session_state:
        st.session_state['session_limit'] = make_rate_limit("session_limit", st.secrets['SESSION_TOKEN_LIMIT'])

    try:
        num_tokens = num_tokens_from_string(question, "gpt-3.5-turbo")
        st.session_state['session_limit'](num_tokens)
        system_rate_limit()(num_tokens)
    except RateLimitError:
        st.error("Free tokens have run out. Please try again later or enter your OpenAI API Key in the sidebar.")
        st.stop()


with st.sidebar:
    model = st.selectbox("Model", ["gpt-3.5-turbo", "gpt-4o"], key='model')
    if model == "gpt-4o" and not st.session_state['openai_api_key']:
        st.error("Please enter your OpenAI API Key to use gpt-4o model.")
        model = "gpt-3.5-turbo"

    user_openai_api_key = st.text_input("OpenAI API Key", key="openai_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"

question = st.text_area("Ask me a question about StarRocks!", key='question')

if question:
    if not user_openai_api_key:
        limit_requests(question)
    rag_chain = get_rag_chain(user_openai_api_key or st.secrets['OPENAI_API_KEY'], model)
    answer = rag_chain.invoke(question)
    st.write(answer)