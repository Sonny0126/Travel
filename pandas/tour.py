import pandas as pd
import re
import os

def parse_tour_sites_from_txt(file_path):
    """
    TXT 파일에서 관광지 정보를 읽고 Pandas 데이터프레임으로 변환하는 함수
    """
    if not os.path.exists(file_path):
        print(f"❌ 오류: '{file_path}' 파일을 찾을 수 없습니다.")
        return {}

    with open(file_path, "r", encoding="utf-8") as file:
        data = file.read().strip().split("================================================================================")

    tourist_spots = {}  # 관광지 정보를 저장할 딕셔너리

    for entry in data:
        entry = entry.strip()
        if not entry:
            continue

        # 정규표현식을 사용하여 필드 추출
        def extract_field(field_name, text):
            match = re.search(rf"{field_name}:\s*(.*)", text)
            return match.group(1).strip() if match else "정보 없음"

        # 관광지 정보 추출
        spot_name = extract_field("이름", entry)
        location = extract_field("주소", entry)
        phone = extract_field("전화번호", entry)
        website = extract_field("웹사이트", entry)
        entrance_fee = extract_field("입장료", entry)
        operating_hours = extract_field("운영시간", entry)

        # 'nan' 값을 '정보 없음'으로 처리
        if phone.lower() == "nan":
            phone = "정보 없음"

        # 관광지 정보를 딕셔너리에 저장
        if spot_name != "정보 없음":
            tourist_spots[spot_name] = {
                "location": location,
                "phone": phone,
                "website": website,
                "entrance_fee": entrance_fee,
                "operating_hours": operating_hours
            }

    return tourist_spots

def search_tourist_spot(tourist_spots, query):
    """
    사용자 입력이 관광지명과 정확히 일치하면 해당 정보를 반환
    """
    extracted_spot_name = re.sub(r"[^가-힣a-zA-Z0-9 ]", "", query).strip()  # 특수문자 제거

    # 1차 검색 (정확한 명칭 포함 여부)
    matching_spots = [spot for spot in tourist_spots if extracted_spot_name in spot]

    # 2차 검색 (부분 일치 허용)
    if not matching_spots:
        matching_spots = [spot for spot in tourist_spots if extracted_spot_name.lower() in spot.lower()]

    if matching_spots:
        spot_name = matching_spots[0]  # 첫 번째 매칭된 결과 선택
        info = tourist_spots[spot_name]
        response = (
            f"🏕 {spot_name}\n"
            f"📍 위치: {info['location']}\n"
            f"📞 연락처: {info['phone']}\n"
            f"🌐 홈페이지: {info['website']}\n"
            f"💰 입장료: {info['entrance_fee']}\n"
            f"🕒 운영 시간: {info['operating_hours']}"
        )
        return response
    return "❌ 해당 관광지 정보를 찾을 수 없습니다."

# 실행 예제
file_path = "tour.txt"  # 파일명 설정
tourist_spots = parse_tour_sites_from_txt(file_path)

# 예제 검색 실행
queries = ["만정캠핑장", "송도스포츠캠핑장", "함허동천(야영장)"]
for query in queries:
    response = search_tourist_spot(tourist_spots, query)
    print(response)
