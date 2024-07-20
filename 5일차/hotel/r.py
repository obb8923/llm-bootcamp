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
l = [{'명칭': '라비치호텔', '우편번호': '54003.0', '관리자': '', '전화번호': '063-442-2700', '주소': '전북특별자치도 군산시 비응남로 36', '위도': '35.9383172811', '경도': '126.5266334756', '개요': '라비치호텔은 비응항에서 바다전경이 가장 좋은  호텔식 숙박업소이다. 세상에서 가장 긴 방조제 새만금, 새로운 서해안 시대를 예고하는 이곳에 대규모 관광타운이 조성되고 있 다. 새만금방조제의 북쪽 관문인 비응항 중심에 위치하고 있으며, 유람선 선착장과 항구가 바로 앞에 있다. 아침에는 방조제 위 로 떠오르는 일출이 있고, 저녁에는 수평선 너머로 지는 해넘이를 볼 수 있어 인기가 높다. 시설에서도 최상을 자랑한다. 객실마다 커플용 PC 및 월풀욕조등 최고의 서비스를 제공하고 있다. 모든 객실이 바다를 향해 나 있다는 것도 장점 중 하나다. 그래서 일출을 볼 수 있는 방과 일몰을 볼 수 있는 방을 선택할 수도 있다. 주변 먹거리로는 신선한 해산물을 즐기실 수 있는 회센터 및 어시장, 음식점들이 바로 있어 보다 저렴하고 맛있게 바다향을 한껏 담아갈 수 있다.', '숙박 종류': '0.0', '문의 및 안내': '', '규모': '7층' }]
get_array=aa.get_data(l)

def dodo(param):
    get_array=aa.get_data(param)


load_dotenv()

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

chain_output = rag_chain.invoke("제천시에 있는 호텔 3개 추천해줘")
print(chain_output)