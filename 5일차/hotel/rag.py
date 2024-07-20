from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
import os
import aa

get_array=aa.get_data()
load_dotenv()
def kk():
    get_array=aa.get_data()

embedding_model=AzureOpenAIEmbeddings(
    model="text-embedding-3-small"
)
chroma = Chroma("vector_store")
vector_store = chroma.from_documents(
        # documents=recursive_splitted_document,
        documents=get_array,
        embedding=embedding_model
    )


similarity_retriever = vector_store.as_retriever(search_type="similarity")
mmr_retriever = vector_store.as_retriever(search_type="mmr")
similarity_score_retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold", 
        search_kwargs={"score_threshold": 0.2}
    )

retriever = similarity_retriever


#---------------------------------------------------------------------

#Generate

template_str = """
You are an assistant for question-answering tasks. 
Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that you don't know. 
Use three sentences maximum and keep the answer concise.
Answer for the question in Korean.

Question: {question} 

Context: {context} 

Answer:""".strip()


prompt_template = ChatPromptTemplate.from_template(template_str)

azure_model = AzureChatOpenAI(
    azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT"),
)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt_template
    | azure_model
    | StrOutputParser()
)

def do(param):
    chain_output = rag_chain.invoke(param)
    return chain_output

# chain_output = rag_chain.invoke("제천시에 있는 호텔 3개 추천해줘")
# print(chain_output)