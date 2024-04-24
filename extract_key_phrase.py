import json
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

def sample_extract_key_phrases(query: str) -> tuple:
    json_file_path = "./config.json"
    document = [query]
    print(document)
    key_phrase_result = []

 # JSON 파일을 읽습니다.
    with open(json_file_path, "r") as file:
        config = json.load(file)

    # JSON 파일에서 키, 엔드포인트, 프로젝트 이름, 배포 이름.
    endpoint = config["endpoint"]
    key = config["key"]
    # project_name = config["project_name"]
    # deployment_name = config["deployment_name"]

    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    result = text_analytics_client.extract_key_phrases(document, language='ko')
    for idx, doc in enumerate(result):
        if not doc.is_error:
            key_phrase_result.append(doc.key_phrases)
    
    return key_phrase_result

if __name__ == '__main__':
    sample_extract_key_phrases(query='일이 하기 싫다. 오늘은 늦게 일어나서 지각을 할 뻔했지만 지각을 하지 않았다. 다행이다. 맨날 가기 싫다 가지말까 이고민하면서 지각하기 싫어서 열심히 씻고 준비하는 내가 너무 모순적이다. 코로나 바이러스 때문에 외출을 삼가하세요 여행가지마세요 하면서 왜 출근은 하라는거지? 출퇴근시간에 모든 사람을 다 만나느데 말이지')