from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_openai import AzureChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
#API 호출을 위한 환경변수 셋팅 (from .env file)
from dotenv import load_dotenv
import os

load_dotenv()

#pip install langchain langchain-openai
model = AzureChatOpenAI(
    azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT"), #gpt-4o is set by env
    temperature=1.0
)

# Define your desired data structure.
class Joke(BaseModel):
    city:str = Field(description="city name")
output_parser = JsonOutputParser(pydantic_object=Joke)


prompt_template = ChatPromptTemplate.from_template(
"""
Extract city information by analyzing the following questions
If you can't find it, save it as 'unfound'

question:{content}

{format_instructions}
"""
).partial(format_instructions=output_parser.get_format_instructions())



# tmpContent ="제s천시에 있는 호텔 1개 추천" 

# prompt_value = prompt_template.invoke({"content":tmpContent})

# model_output = model.invoke(prompt_value)

# output = output_parser.invoke(model_output)

def do(tmpContent):
    prompt_value = prompt_template.invoke({"content":tmpContent})
    model_output = model.invoke(prompt_value)
    output = output_parser.invoke(model_output)
    print(output)
    return output



