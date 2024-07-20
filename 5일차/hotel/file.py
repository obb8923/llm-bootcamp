import pandas as pd
import mysql.connector
import numpy as np

# Load the Excel file
file_path = 'data.xlsx'
data = pd.read_excel(file_path)

# Print the original column names to debug
print("Original columns:", data.columns)

# Create a mapping from Korean column names to English column names
column_mapping = {
    '명칭': 'place_name',
    '우편번호': 'postal_code',
    '관리자': 'manager',
    '전화번호': 'phone_number',
    '주소': 'address',
    '위도': 'latitude',
    '경도': 'longitude',
    '개요': 'overview',
    '숙박 종류': 'accommodation_type',
    '문의 및 안내': 'inquiry_and_information',
    '규모': 'scale',
    '수용 가능 인원': 'capacity',
    '객실 수': 'number_of_rooms',
    '객실 유형': 'room_types',
    '주차 가능': 'parking_available',
    '조리 가능': 'cooking_allowed',
    '체크인': 'check_in_time',
    '체크아웃': 'check_out_time',
    '예약 안내': 'reservation_guide',
    '예약 안내 홈페이지': 'website',
    '픽업서비스': 'pickup_service',
    '식음료장': 'dining_facilities',
    '부대 시설': 'additional_facilities',
    '세미나': 'seminar_facilities',
    '스포츠시설': 'sports_facilities',
    '사우나실': 'sauna',
    '뷰티 시설': 'beauty_facilities',
    '노래방': 'karaoke',
    '바베큐장': 'barbecue_area',
    '캠프화이어': 'campfire',
    '자전거대여': 'bicycle_rental',
    '휘트니스센터': 'fitness_center',
    '공용 PC실': 'public_pc_room',
    '공용 샤워실': 'public_shower_room',
    '상세정보': 'detailed_information',
    '환불규정': 'refund_policy'
}

# Rename the columns in the dataframe
data.rename(columns=column_mapping, inplace=True)

# Print the renamed columns to debug
print("Renamed columns:", data.columns)

# Replace NaN values with None
data = data.replace({np.nan: None})

# Ensure the columns are in the correct order
expected_columns = list(column_mapping.values())
data = data[expected_columns]

# Establish MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Juniverse325!",
    database="board"
)

cursor = db.cursor()

# Insert data into the table
for _, row in data.iterrows():
    sql = """
    INSERT INTO accommodations (
    place_name,
    postal_code, manager, phone_number,
    address, latitude,
    longitude, overview,
    accommodation_type,
    inquiry_and_information,
    scale, capacity,
    number_of_rooms,
    room_types,
    parking_available,
    cooking_allowed,
    check_in_time,
    check_out_time,
    reservation_guide,
    website,
    pickup_service,
    dining_facilities,
    additional_facilities,
    seminar_facilities,
    sports_facilities,
    sauna,
    beauty_facilities,
    karaoke,
    barbecue_area,
    campfire,
    bicycle_rental,
    fitness_center,
    public_pc_room,
    public_shower_room,
    detailed_information,
    refund_policy
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
    %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, tuple(row))
    db.commit()

cursor.close()
db.close()
