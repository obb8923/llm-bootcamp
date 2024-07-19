from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

#API 호출을 위한 환경변수 셋팅 (from .env file)
from dotenv import load_dotenv
import os

load_dotenv()

#pip install langchain langchain-openai
model = AzureChatOpenAI(
    azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT"), #gpt-4o is set by env
    temperature=1.0
)
# 챗봇 시작 메시지 입니다.
print("챗봇이 시작되었습니다. 대화를 종료하려면 'quit'을 입력해주세요")
# history 저장용 messages 초기화
messages=[SystemMessage(content="You are a helpful assistant. Answer all questions to the best of your ability.")]

# quit 을 응답할때 까지 무한 루프를 돕니다.
while(1):
    # 질문 받기
    print("You: ",end="")
    q=input()
    # 질문이 quit이면 루프를 빠져나옵니다.
    if(q=="quit"):
        break
    # 받은 질문을 history에 넣습니다.
    messages.append(HumanMessage(content=q))
    # history 를 invoke합니다.
    model_output=model.invoke(messages)
    # AI 답변 출력
    print("AI: ",end="")
    print(model_output.content)
    # history 에 답변을 저장합니다.
    messages.append(SystemMessage(content=model_output.content))

# 챗봇 종료 메시지 입니다.
print("챗봇을 종료합니다.")

