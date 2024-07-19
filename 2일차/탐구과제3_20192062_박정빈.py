from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

#API 호출을 위한 환경변수 셋팅 (from .env file)
from dotenv import load_dotenv
import os

load_dotenv()

# import
from langchain.memory import ConversationBufferMemory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

#pip install langchain langchain-openai
model = AzureChatOpenAI(
    azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT"), #gpt-4o is set by env
    temperature=1.0
)
# 챗봇 시작 메시지 입니다.
print("챗봇이 시작되었습니다. 대화를 종료하려면 'quit'을 입력해주세요")
# history 저장용 messages 초기화
messages=[SystemMessage(content="You are a helpful assistant. Answer all questions to the best of your ability.")]
# 메모리 초기화
memory = ConversationBufferMemory(
            chat_memory=InMemoryChatMessageHistory(),
            return_messages=True #대화 기록이 메시지 객체(HumanMessage, AIMessage등)의 리스트로 반환
        )
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Answer all questions to the best of your ability."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

output_parser = StrOutputParser()

chain = prompt | model | output_parser
# quit 을 응답할때 까지 무한 루프를 돕니다.
while(1):
    # 질문 받기
    print("You: ",end="")
    q=input()
    # 질문이 quit이면 루프를 빠져나옵니다.
    if(q=="quit"):
        break

    #기존의 메모리를 읽어
    chat_history = memory.chat_memory.messages

    # 실행
    output = chain.invoke({
        "input": q,
        "chat_history": chat_history        
    })
    
    # AI 답변 출력
    print("AI: ",end="")
    print(output)

    # 메모리에 사용자 입력과 AI 응답 추가
    memory.chat_memory.add_user_message(q)
    memory.chat_memory.add_ai_message(output)
    
# 챗봇 종료 메시지 입니다.
print("챗봇을 종료합니다.\n\nhistory:")
print(memory.chat_memory)

