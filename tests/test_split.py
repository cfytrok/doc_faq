from langchain_core.documents import Document

from splitter import split_md


def test_split_headers():
    text = """# Header 1
## Header 2
### Header 3
### Header 4
text"""
    docs = [Document(text, metadata={"source": "example.md"})]
    splits = split_md(docs, 100, 0)
    assert len(splits) == 2
    assert splits[0].page_content == """# Header 1  
## Header 2  
### Header 3"""
    assert splits[1].metadata == {'Header 1': 'Header 1', 'Header 2': 'Header 2', 'Header 3': 'Header 4',
                                  'source': 'example.md'}


def test_slit_chunks():
    text = "123"
    docs = [Document(text, metadata={"source": "example.md"})]
    splits = split_md(docs, 2, 1)
    assert len(splits) == 2
    assert splits[0].page_content == "12"
    assert splits[1].page_content == "23"
