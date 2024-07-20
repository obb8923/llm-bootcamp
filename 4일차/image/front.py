import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import base64
import os
from dotenv import load_dotenv
from openai import OpenAI
import llm
# 환경 변수 로드
load_dotenv()

# Azure 설정
API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=API_KEY)

# Streamlit 앱 제목
st.title("Extract Text from Business Card Image")

name_query = st.text_input("검색할 이름을 입력하세요", "")
if st.button("조회"):
    if name_query:
        # Flask API에 요청 보내기
        response = requests.get(f"http://localhost:5000/show_member?name={name_query}")
        
        if response.status_code == 200:
            st.success("멤버를 찾았습니다!")
            st.json(response.json())
        elif response.status_code == 404:
            st.warning(f"'{name_query}' 이름의 멤버를 찾을 수 없습니다.")
        elif response.status_code == 400:
            st.error("이름을 입력해주세요.")
        else:
            st.error(f"오류가 발생했습니다: {response.text}")
    else:
        st.warning("이름을 입력해주세요.")
# 이미지 업로드
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
if uploaded_file is not None:
    # 이미지를 보여준다
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
    st.write("")

    # 이미지를 바이트로 전환 및 Base64 인코딩
    buf = BytesIO()
    image.save(buf, format="PNG")
    image_bytes = buf.getvalue()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    url = 'http://localhost:5000/add_member'  # API 서버의 엔드포인트 URL
    data = llm.do()
    response = requests.post(url, json=data)
    # data ={
    # 'company' :"apple",
    # 'owner_name':"sam kim",
    # 'mail' : "asd@goodmail.com",
    # 'job' : "doctor",
    # 'address' : "somewhere"
    # }


    # API 요청
#     response = client.chat.completions.create(
#         model=DEPLOYMENT,
#         messages=[
#             {
#                 "role": "user",
#                 "content": [
#                     {
#                         "type": "text",
#                         "text": "extract the text from the picture of this business card",
#                     },
#                     {
#                         "type": "text",
#                         "text": """Organize the extracted text in the following format and return it to json.
# {
# 'company': 'anycompanyname',
# 'name': ' anyname ',
# 'mail': 'example@gmail',
# 'job': 'anyjob',
# 'address': 'somewhere'}""",
#                     },
#                 ],
#             },
#             {
#                 "role": "system",
#                 "content": {"type": "image_base64", "image_base64": image_base64},
#             },
#         ],
#     )

#     # 결과 출력
#     st.write("Response from Azure OpenAI:")
#     st.write(response.json())
