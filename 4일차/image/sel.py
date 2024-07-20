import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image_path):
    """이미지를 전처리하는 함수"""
    image = Image.open(image_path)
    # 이미지를 그레이스케일로 변환
    image = image.convert('L')
    # 이미지 대비 조정
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)
    # 이미지 이진화
    image = image.point(lambda x: 0 if x < 128 else 255)
    return image

def extract_text_from_image(image_path, lang='kor+eng'):
    """이미지에서 텍스트를 추출하는 함수"""
    image = preprocess_image(image_path)
    text = pytesseract.image_to_string(image, lang=lang)
    return text

# 이미지 경로 설정
image_path = "tabak.jpg"  # 이미지 파일 경로를 여기에 설정

def dodo():
    print("dodo")
    extracted_text = extract_text_from_image(image_path)  # 'kor' 언어 코드를 사용하여 한국어 텍스트 추출
    return extracted_text
    

