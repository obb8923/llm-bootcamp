import streamlit as st
from openai import AzureOpenAI

str_api_key = "2374f2c1a634407387e2fb2fbba5e7fe"
str_api_version ="2024-02-01"
str_endpoint = "https://magicecoleai.openai.azure.com/"

client = AzureOpenAI(
    api_key = str_api_key,  #Azure Open AI Key
    api_version = str_api_version,  #Azue OpenAI API model
    azure_endpoint = str_endpoint #Azure Open AI end point(매직에꼴)
)

st.set_page_config(layout="wide")

# 제목 설정
st.title('ChatGPT - Simple Chatbot')

# 질문 입력
user_input = st.text_input('질문을 입력하세요:', '')

if user_input:
    context = [{"role": "user", "content": user_input}] 
    response = client.chat.completions.create(
            model="gpt-4o", 
            messages=context,
            temperature=0,
            top_p=0,
            seed=1234
        )
    # 응답 출력
    st.text_area('답변:', value=response.choices[0].message.content, height=200)
