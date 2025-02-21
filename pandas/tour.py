import pandas as pd
import json
import re
import os

def parse_tour_sites_from_txt(file_path):
    """
    TXT 파일에서 관광지 정보를 읽고 Pandas 데이터프레임으로 변환하는 함수
    """
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)  # JSON 파일 읽기

    result = []  # 관광지 정보를 저장할 리스트
    tourist_spots = {}  # 관광지 정보를 저장할 딕셔너리

    for entry in data:
        prompt = entry.get("prompt", "")  # 'prompt' 필드에서 데이터 가져오기

        # 정규표현식을 사용하여 특정 필드 값 추출하는 함수
        def extract_field(field_name, text):
            match = re.search(rf"{field_name}:\s*(.*)", text)  # 필드명과 일치하는 값 찾기
            return match.group(1).strip() if match else "정보 없음"  # 값이 없으면 '정보 없음' 반환

        # 관광지 정보 필드 추출
        spot_name = extract_field("Spot Name", prompt)
        location = extract_field("Location", prompt)
        phone = extract_field("Phone", prompt)
        website = extract_field("Website", prompt)
        entrance_fee = extract_field("Entrance Fee", prompt)
        operating_hours = extract_field("Operating Hours", prompt)

        # HTML 태그 제거 (<a>, <br> 등)
        website = re.sub(r"<.*?>", "", website)  # 모든 HTML 태그 제거
        operating_hours = re.sub(r"<br>", " ", operating_hours)  # <br>을 공백으로 변환
        operating_hours = re.sub(r"<.*?>", "", operating_hours).strip()  # 추가적인 HTML 태그 제거

        # 'nan' 값을 '정보 없음'으로 처리
        spot_name = "정보 없음" if spot_name.lower() == "nan" else spot_name
        location = "정보 없음" if location.lower() == "nan" else location
        phone = "정보 없음" if phone.lower() == "nan" else phone
        website = "정보 없음" if website.lower() == "nan" else website
        entrance_fee = "정보 없음" if entrance_fee.lower() == "nan" else entrance_fee
        operating_hours = "정보 없음" if operating_hours.lower() == "nan" else operating_hours

        # 리스트에 관광지 정보 추가
        result.append([spot_name, location, phone, website, entrance_fee, operating_hours])

        # 관광지 정보를 딕셔너리에 저장
        if spot_name != "정보 없음":
            tourist_spots[spot_name] = {
                "location": location,
                "phone": phone,
                "website": website,
                "entrance_fee": entrance_fee,
                "operating_hours": operating_hours
            }

    # Pandas 데이터프레임 생성
    df = pd.DataFrame(result, columns=["spot_name", "location", "phone", "website", "entrance_fee", "operating_hours"])

    return df, tourist_spots

def preprocess_query(query):
    """
    사용자의 질문에서 불필요한 텍스트를 제거하여 검색 최적화
    """
    query = re.sub(r"Q\.\s*", "", query)  # "Q. " 제거
    query = re.sub(r"(어디에 있나요\?|위치가 어디인가요\?|운영 시간은 어떻게 되나요\?|입장료는 얼마인가요\?)", "", query)  # 질문 패턴 제거
    query = query.strip()
    return query

def search_tourist_spot(tourist_spots, query):
    """
    사용자의 질문에서 관광지명을 추출하고 해당 정보를 검색하여 자연어 응답 생성
    """
    query = preprocess_query(query)  # 검색어 정제

    # 1차 검색 (정확한 명칭 포함 여부)
    matching_spots = [spot for spot in tourist_spots if query in spot]

    # 2차 검색 (부분 일치 허용)
    if not matching_spots:
        matching_spots = [spot for spot in tourist_spots if query.lower() in spot.lower()]

    if matching_spots:
        spot_name = matching_spots[0]  # 첫 번째 매칭된 결과 선택
        info = tourist_spots[spot_name]
        response = (
            f"주어진 정보에 따르면 {spot_name}은(는) {info['location']}에 위치해 있습니다.\n"
            f"📞 연락처: {info['phone']}\n"
            f"🌐 홈페이지: {info['website']}\n"
            f"💰 입장료: {info['entrance_fee']}\n"
            f"🕒 운영 시간: {info['operating_hours']}\n"
            f"더 자세한 정보는 공식 홈페이지에서 확인하세요!"
        )
        return response
    return "죄송합니다. 해당 관광지에 대한 정보를 찾을 수 없습니다."

# 실행 예제
file_path = "tour_site.txt"  # 파일명 설정
if not os.path.exists(file_path):
    print(f"❌ 오류: '{file_path}' 파일을 찾을 수 없습니다.")
else:
    df_tour_sites, tourist_spots = parse_tour_sites_from_txt(file_path)

    # 데이터프레임 출력
    print(df_tour_sites)

    # CSV 파일로 저장
    df_tour_sites.to_csv("tour_sites_clean.csv", index=False, encoding="utf-8-sig")
    print("✅ 관광지 데이터가 'tour_sites_clean.csv' 파일로 저장되었습니다.")

    # 예제 검색 실행
    user_query = "Q. 송도스포츠캠핑장이 어디에 있나요?"
    response = search_tourist_spot(tourist_spots, user_query)
    print(response)

    user_query = "Q. 송도스포츠 위치가 어디인가요?"
    response = search_tourist_spot(tourist_spots, user_query)
    print(response)

# 1. 관광지 정보 문제
# "만정캠핑장"은 어디에 위치해 있나요?
# "송도스포츠캠핑장"에서 텐트존의 주말 이용 요금은 얼마인가요?
# "함허동천(야영장)"의 공식 웹사이트 주소는 무엇인가요?
# "대이작도 부아산 하이킹"의 입장료는 얼마인가요?
# "강화나들길"의 운영 시간은 어떻게 되나요?
# 2. 예약 및 입장료 관련 문제
# "함허동천(야영장)"에서 1야영장을 3박 4일 이용할 경우 요금은 얼마인가요?
# "송도스포츠캠핑장"의 가족 피크닉존 요금은 청소년과 일반 이용자 간에 얼마나 차이가 나나요?
# "강화도 황청낚시터"의 입장료 정책은 어떻게 되나요?
# "선재도 어촌체험 휴양마을 해상낚시터"에서 어린이 입장료는 얼마인가요?
# "서포리 오토캠핑장"에서 4시간을 초과하여 머물 경우 추가 요금은 얼마인가요?
# 3. 운영 시간 및 방문 관련 문제
# "대이작도 생태탐방로"의 운영 시간은 언제인가요?
# "현대유람선(아라뱃길)"에서 뷔페크루즈는 주중과 주말에 각각 몇 시에 운영되나요?
# "선재도 트리캠핑장"의 입실 및 퇴실 시간은 언제인가요?
# "문라이트 캠핑장"은 어떤 요일에 운영되나요?
# "BMW 드라이빙 센터"의 여름철 운영 시간은 몇 시부터 몇 시까지인가요?
# 4. 특별한 관광 명소 관련 문제
# "계양산 둘레길"을 방문할 때 입장료는 얼마인가요?
# "강화도 황청낚시터"에서 특정 프로그램을 이용하려면 추가 요금이 발생하나요?
# "강화고인돌캠핑장"의 입장료는 어떤 기준으로 달라지나요?
# "두리생태공원캠핑장"은 현재 운영 중인가요?
# "교동도 난정저수지"에서 낚시를 할 경우 운영 시간이 어떻게 되나요?
# 5. 위치 및 교통 관련 문제
# "무의바다누리길"은 어느 구에 위치하고 있나요?
# "신도·시도·모도 해안누리길(인천 삼형제섬길)"의 정확한 주소는 무엇인가요?
# "선재오토캠핑장"의 공식 웹사이트 주소는 무엇인가요?
# "오크힐글램핑"의 입장료가 요일별로 어떻게 달라지나요?
# "덕산국민여가캠핑장"의 성수기 요금은 얼마인가요?