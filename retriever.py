from pathlib import Path

import streamlit as st
from git import Repo
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from sys import platform
if platform == "linux" or platform == "linux2":
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

from splitter import split_md


@st.cache_resource(show_spinner=True)
def load_data():
    repo_url = "https://github.com/StarRocks/starrocks/"
    repo_path = Path("./repos/starrocks")

    _pull_repo(repo_path, repo_url)
    docs = _load_docs(repo_path / "docs" / "en")
    splits = split_md(docs, 1200, 50)
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
    return vectorstore

def _pull_repo(repo_path, repo_url):
    if (repo_path / ".git").exists():
        repo = Repo(repo_path)
        origin = repo.remotes.origin
        origin.pull()
    else:
        Repo.clone_from(repo_url, repo_path)


def _load_docs(doc_path):
    loader = DirectoryLoader(doc_path, glob="introduction/**/*.md", show_progress=True,
                             loader_cls=TextLoader)
    docs = loader.load()
    for doc in docs:
        doc.metadata["source"] = _format_source(doc.metadata["source"], doc_path)
    return docs


def _format_source(source: str, doc_path):
    """
    >>> _format_source("repos/starrocks/docs/en/introduction/overview.md", Path("repos/starrocks/docs/en/"))
    'http://docs.starrocks.io/docs/introduction/overview'
    """
    source = Path(source).relative_to(doc_path).with_suffix('')
    return 'http://docs.starrocks.io/docs/' + source.as_posix()
