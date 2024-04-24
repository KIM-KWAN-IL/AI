# import os
import json
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

def sample_classify_document_multi_label(query: str) -> tuple:
    
    json_file_path = "./config.json"
    document = [query]
    print(document)

    with open(json_file_path, "r") as file:
        config = json.load(file)

    # JSON 파일에서 키, 엔드포인트, 프로젝트 이름, 배포 이름.
    endpoint = config["endpoint"]
    key = config["key"]
    project_name = config["project_name"]
    deployment_name = config["deployment_name"]

    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
    )

    poller = text_analytics_client.begin_multi_label_classify(
        document,
        project_name=project_name,
        deployment_name=deployment_name
    )

    return_result = {}
    document_results = poller.result()
    for doc, classification_result in zip(document, document_results):
        if classification_result.kind == "CustomDocumentClassification":
            classifications = classification_result.classifications
            print(f"\nSentence '{doc}'\n") ## 입력값 print
            for classification in classifications:

                print("'{}' with confidence score {}.".format(
                    classification.category, classification.confidence_score ## 작동 확인용. 지워도 됨
                ))

                return_result[classification.category] = classification.confidence_score
            
                
        elif classification_result.is_error is True:
            print("Document '{}' has an error with code '{}' and message '{}'".format(
                doc, classification_result.error.code, classification_result.error.message ## 에러코드, 이제 fastapi 코드 내에서 오류 코드 보여주니까 지워도 됨
            ))
    
    return return_result


if __name__ == "__main__":
    
    documents = [
        "나는 행복한데 불안하며 슬프면서 화난다",
    ] 
    sample_classify_document_multi_label(documents)
