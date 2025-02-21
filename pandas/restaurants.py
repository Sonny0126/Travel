import pandas as pd
import re
import os

def parse_restaurants_from_txt(file_path):
    """
    TXT 파일에서 레스토랑 정보를 읽고 Pandas 데이터프레임으로 변환하는 함수
    """
    with open(file_path, "r", encoding="utf-8") as file:
        data = file.read()
    
    # 레스토랑 정보를 저장할 리스트
    restaurants = []
    
    # 레스토랑 정보를 정규 표현식을 이용해 추출
    pattern = re.compile(r'이름: (.*?)\n주소: (.*?)\n평점: (.*?)\n주요 리뷰:(.*?)\n={20,}', re.DOTALL)
    
    matches = pattern.findall(data)
    
    for match in matches:
        name, address, rating, reviews = match
        
        # 개별 리뷰 정보 추출
        review_pattern = re.compile(r'작성자: (.*?)\n평점: (\d+)\n리뷰 내용: (.*?)\n', re.DOTALL)
        review_matches = review_pattern.findall(reviews)
        
        extracted_reviews = []
        for reviewer, score, content in review_matches:
            extracted_reviews.append(f"{reviewer}({score}점): {content.strip()}")

        review_text = " | ".join(extracted_reviews)
        
        # 리스트에 레스토랑 정보 추가
        restaurants.append([name, address, rating, review_text])
    
    # Pandas 데이터프레임 생성
    df = pd.DataFrame(restaurants, columns=["이름", "주소", "평점", "주요 리뷰"])
    
    return df

def preprocess_query(query):
    """
    사용자의 질문에서 레스토랑 이름을 추출하여 검색 최적화
    """
    query = re.sub(r"[^가-힣a-zA-Z0-9 ]", "", query)  # 특수문자 제거 (예: ?, !, @ 등)
    
    # 불필요한 질문 패턴 제거 (더 다양한 형태 지원)
    query = re.sub(r"(위치|주소|어디|정보|리뷰|평점).*", "", query).strip()
    
    return query

def search_restaurant(df_restaurants, query):
    """
    사용자 입력이 레스토랑 이름과 정확히 일치하면 해당 정보를 반환
    """
    query = preprocess_query(query)  # 검색어 정제

    # 1차 검색: 정확한 이름 포함 여부
    matching_rows = df_restaurants[df_restaurants["이름"].str.contains(query, case=False, na=False)]

    # 2차 검색: 부분 일치 허용 (예: "샐러디"만 입력해도 "샐러디 인천대점" 검색됨)
    if matching_rows.empty:
        matching_rows = df_restaurants[df_restaurants["이름"].apply(lambda x: query in x)]
    
    if not matching_rows.empty:
        row = matching_rows.iloc[0]  # 첫 번째 검색 결과 선택
        response = (
            f"{row['이름']}\n"
            f"📍 위치: {row['주소']}\n"
            f"⭐ 평점: {row['평점']}점\n"
            f"📝 주요 리뷰: {row['주요 리뷰']}"
        )
        return response
    return "❌ 해당 레스토랑 정보를 찾을 수 없습니다."

# 실행 예제
file_path = "restaurants.txt"  # 파일명 설정
if not os.path.exists(file_path):
    print(f"❌ 오류: '{file_path}' 파일을 찾을 수 없습니다.")
else:
    df_restaurants = parse_restaurants_from_txt(file_path)
    
    # 데이터프레임 출력
    print(df_restaurants)

    # CSV 파일로 저장
    output_file = "restaurants_clean.csv"
    df_restaurants.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"✅ 레스토랑 데이터가 '{output_file}' 파일로 저장되었습니다.")

    # 예제 검색 실행
    queries = ["샐러디 인천대점", "캡틴 루이"]
    for query in queries:
        response = search_restaurant(df_restaurants, query)
        print(response)

# Q1. 캡틴 루이의 위치가 어디인가요?
# Q2. 캡틴 루이의 주요 메뉴는 무엇인가요?
# Q3. 캡틴 루이의 분위기는 어떤가요?
# Q4. 캡틴 루이의 대표적인 리뷰는 무엇인가요?
# Q5. 캡틴 루이에서 추천하는 음식은 무엇인가요?
# 샐러디 인천대점

# Q6. 샐러디 인천대점의 위치가 어디인가요?
# Q7. 샐러디 인천대점의 평점은 몇 점인가요?
# Q8. 샐러디 인천대점의 야채 신선도는 어떤가요?
# Q9. 샐러디 인천대점에서 가장 인기가 많은 메뉴는 무엇인가요?
# Q10. 샐러디 인천대점 방문 시 주의할 점이 있나요?
# 번패티번 송도

# Q11. 번패티번 송도의 위치는 어디인가요?
# Q12. 번패티번 송도의 버거 맛은 어떤가요?
# Q13. 번패티번 송도의 가격대는 어느 정도인가요?
# Q14. 번패티번 송도의 고객 서비스는 어떤가요?
# Q15. 번패티번 송도의 대표적인 리뷰를 알려주세요.
# 오복솥뚜껑 송도점

# Q16. 오복솥뚜껑 송도점의 위치는 어디인가요?
# Q17. 오복솥뚜껑 송도점의 삼겹살 맛은 어떤가요?
# Q18. 오복솥뚜껑 송도점에서 추가 비용이 발생하는 항목은 무엇인가요?
# Q19. 오복솥뚜껑 송도점의 고객 서비스 평가는 어떤가요?
# Q20. 오복솥뚜껑 송도점의 대표적인 리뷰는 무엇인가요?
# 송도국제신도시 송도갈비

# Q21. 송도국제신도시 송도갈비의 위치는 어디인가요?
# Q22. 송도국제신도시 송도갈비에서 인기 있는 메뉴는 무엇인가요?
# Q23. 송도국제신도시 송도갈비의 가격대는 어떻게 되나요?
# Q24. 송도국제신도시 송도갈비의 주요 리뷰를 알려주세요.
# Q25. 송도국제신도시 송도갈비에서 직원들이 직접 고기를 구워주나요?