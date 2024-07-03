from typing import Iterable

from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter, Language

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]


def split_md(docs: Iterable[Document], chunk_size: int = 1200, chunk_overlap: int = 50):
    md_header_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on, strip_headers=False)
    md_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.MARKDOWN, chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    result_docs = []
    for doc in docs:
        md_header_splits = md_header_splitter.split_text(doc.page_content)
        header_and_markdown_split = md_splitter.split_documents(md_header_splits)
        for split in header_and_markdown_split:
            split.metadata |= doc.metadata
            result_docs.append(split)

    return result_docs
