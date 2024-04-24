import requests
import json

# 더미 데이터 생성
dummy_data = {
    "member_id": 456,
    "diary": """
    일이 하기 싫다. 오늘은 늦게 일어나서 지각을 할 뻔했지만 지각을 하지 않았다. 다행이다. 맨날 가기 싫다 가지말까 이고민하면서 지각하기 싫어서 열심히 씻고 준비하는 내가 너무 모순적이다. 코로나 바이러스 때문에 외출을 삼가하세요 여행가지마세요 하면서 왜 출근은 하라는거지? 출퇴근시간에 모든 사람을 다 만나는데 말이지
    """
}

# API 엔드포인트 URL
api_url = "http://127.0.0.1:8000/keyphrase/"

# API 요청 보내기
response = requests.post(api_url, json=dummy_data)

# 결과 확인
print(response.status_code)  # 응답 상태 코드 확인
print(response.json())       # 응답 데이터 확인