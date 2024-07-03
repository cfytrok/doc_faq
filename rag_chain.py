from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

from retriever import load_data


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an assistant for question-answering tasks. "
                   "Use the following pieces of retrieved context to answer the question. "
                   "If you don't know the answer, just say that you don't know. "
                   "Use three sentences maximum and keep the answer concise. "
                   "Answer in the same language in which the question was asked."
                   "Provide links to the source documents."),
        ("human", "{question}"),
        ("system", "Context: "
                   "{context}")
    ]
)


def format_docs(docs):
    return "\n\n".join(f'{doc.metadata}\n{doc.page_content}' for doc in docs)


def get_rag_chain(openai_api_key: str, model: str):
    llm = ChatOpenAI(model=model, api_key=openai_api_key)
    retriever = load_data().as_retriever()
    return (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    )
