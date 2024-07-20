import chardet
import csv
from langchain_core.documents import Document
import json
dicts = []
# 파일의 인코딩을 자동으로 감지합니다.
with open('data.csv', 'rb') as file:
    raw_data = file.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']

# 감지된 인코딩으로 파일을 엽니다.
with open('data.csv', 'r', encoding=encoding) as file:
    csv_dict_reader = csv.DictReader(file)
    
    # 첫 10개의 행만 읽어서 리스트에 추가
    for i, row in enumerate(csv_dict_reader):
        if i >= 20:
            break
        dicts.append(row)

# CSV 파일의 열 이름을 출력하여 확인합니다.
if dicts:
    print("CSV 파일의 헤더:", dicts[0].keys())
    print("!!")
    # print(dicts)
def convert_dicts_to_documents(dict_list):
    documents = []
    for item in dict_list:
        # 'content'와 'metadata'가 아니라 실제 CSV 열 이름을 사용해야 합니다.
        # 예를 들어, 'text'라는 열이 실제 내용이 있는 열일 수 있습니다.
        content = item.get('text', '')  # 'text'는 예시 열 이름입니다.
        metadata = item  # 필요한 경우, metadata를 정의할 수 있습니다.
        json_string = json.dumps(metadata, ensure_ascii=False)  # ensure_ascii=False는 한글 등의 비 ASCII 문자를 제대로 인코딩합니다.

        documents.append(Document(page_content=json_string , metadata={'source': 'data'}))
    return documents



def get_data():
    aa_result = convert_dicts_to_documents(dicts)
    return aa_result
    
