from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableParallel
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

#chain을 실행하면 {"joke":비트 소재의 농담, "ananlysis":농담에 대한 평가} 의 형태로 출력되도록 함수를 구현하세요.
#조건 : Runnable Primitives에서 학습한 내용을 반드시 코드에 적용하세요.
#가급적 다른 코드는 수정하지 마세요.
def make_composed_chain(joke_prompt, analysis_prompt, model, output_parser):
    joke_chain = joke_prompt | model | {'joke': output_parser}
    analysis_chain = analysis_prompt | model | {'analysis': output_parser}
    
    def combine_chain(input):
        joke_result = joke_chain.invoke(input)
        analysis_result = analysis_chain.invoke(joke_result)
        return {**joke_result, **analysis_result}

    chain = RunnableLambda(combine_chain)
    return chain

# joke_result와 analysis_result는 각각 딕셔너리입니다.
# {**joke_result, **analysis_result}는 두 딕셔너리를 하나의 딕셔너리로 병합합니다.
# ** 구문은 딕셔너리의 키-값 쌍을 풀어헤쳐 새로운 딕셔너리를 만들 때 사용됩니다.

if __name__ == "__main__":
    load_dotenv()

    joke_prompt = ChatPromptTemplate.from_template("tell me a joke about {topic} in Korean")
    analysis_prompt = ChatPromptTemplate.from_template("is this a funny joke? {joke}")

    model = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_version=os.getenv("OPENAI_API_VERSION")
    )
    output_parser =  StrOutputParser()

    chain = make_composed_chain(joke_prompt, analysis_prompt, model, output_parser)

    print(chain.invoke({"topic": "beets"}))