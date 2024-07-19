from langchain_core.tools import tool
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.pydantic_v1 import BaseModel, Field
from langchain.memory import ConversationBufferMemory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from dotenv import load_dotenv
from datetime import datetime
import pytz
import requests
import os

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools.tavily_search import TavilySearchResults

from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor


#도시의 현재 시각
@tool
def get_time_from_city(city_name):

    """Get the current time for the given city name."""

    geolocator = Nominatim(user_agent="timezone_finder")
    location = geolocator.geocode(city_name)
    
    if not location:
        return None
    
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lng=location.longitude, lat=location.latitude)
    
    if timezone_str:        
        # # Get the timezone for the city
        timezone_info = pytz.timezone(timezone_str)

        # Get the current time in the timezone
        now = datetime.now(timezone_info)
        current_time = now.isoformat()

        return {"current_time":current_time}


    else:
        return None



#도시의 현재 날씨
class CityName(BaseModel):
    city_name: str = Field(description="City Name String")

@tool(args_schema=CityName)
def get_weather_in_city(city_name):

    """Get the current weather info for the given city name."""

    geolocator = Nominatim(user_agent="weather_checker")
    location = geolocator.geocode(city_name)
    
    if not location:
        return None

    params = {
        "lat": location.latitude,
        "lon": location.longitude,
        "units": "metric",
        "lang":  "en",
        "appid": os.getenv("WEATHER_API_KEY")
    }
    url = "https://api.openweathermap.org/data/2.5/weather?{}".format("&".join([f"{k}={v}" for k, v in params.items()]))
    response = requests.get(url).json()

    return_data = {
        "country": response["sys"]["country"],
        "region": response["name"],
        "weather_main": response["weather"][0]["main"],
        "weather_description": response["weather"][0]["description"],
        "current_temperature_celsius": response["main"]["temp"],
        "feel_like_temperature_celsius": response["main"]["feels_like"],
        "max_temperature_celsius": response["main"]["temp_max"],
        "min_temperature_celsius": response["main"]["temp_min"],
        "humidity": response["main"]["humidity"],
        "cloudiness": response["clouds"]["all"],
        "wind": response["wind"]["speed"]
    }

    return return_data


def ask_something(agent, query):

    print(f"User : {query}")

    agent_output = agent.invoke(
        {"input": query}
    )

    #print(agent_output)
    print(f"LLM : {agent_output}")


    return


def init_agent(tools):

    prompt_template = ChatPromptTemplate.from_messages([
        ("system","You are an helpful AI assistant that helps people to give the best answer for questions in Korean"),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human","{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])

    azure_model = AzureChatOpenAI(
        azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_version = os.getenv("OPENAI_API_VERSION")
    )


    #Agent의 생성
    agent = create_tool_calling_agent(azure_model, tools, prompt_template)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=10)


    memory = ConversationBufferMemory(
            chat_memory=InMemoryChatMessageHistory(),        
            return_messages=True
        )

    load_context_runnable = RunnablePassthrough().assign(
        chat_history=RunnableLambda(lambda x:memory.chat_memory.messages)
    )

    def save_context(agent_output):
        memory.chat_memory.add_user_message(agent_output["input"])
        memory.chat_memory.add_ai_message(agent_output["output"])
        return agent_output["output"]

    save_context_runnable = RunnableLambda(save_context)

    agent_chain = load_context_runnable | agent_executor | save_context_runnable

    return agent_chain



if __name__ == "__main__":

    load_dotenv()

    #Wikipedia 툴
    api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=500)
    wikipedia_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

    #Tavily 툴(검색 엔진)
    tavily_tool = TavilySearchResults(max_results=2)

    tools = [
        tavily_tool,
        wikipedia_tool,
        get_time_from_city,
        get_weather_in_city
    ]

    agent_chain  = init_agent(tools)

    # human_inputs = [
    #     "안녕, 나는 샘이라고 해",
    #     "아이폰을 개발한 회사의 본사가 있는 도시의 현재 시각을 알려줘",
    #     "내 이름이 뭐라고 그랬지?"
    # ]
    

    # for input in human_inputs:
    #     ask_something(agent_chain, input)
    
    while(1):
    # 질문 받기
        print("You: ",end="")
        q=input()
        # 질문이 quit이면 루프를 빠져나옵니다.
        if(q=="quit"):
            break

        ask_something(agent_chain,q)
    # 챗봇 종료 메시지 입니다.
    print("챗봇을 종료합니다.")


    
    