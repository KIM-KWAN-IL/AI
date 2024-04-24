import sentiment_analysis
import extract_key_phrase
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from pydantic import BaseModel


app = FastAPI()

#CORS 설정 (HTTP 통신 원활히)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# # 데이터베이스 세션 의존성 주입을 위한 함수 추가
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

### pydantic 정의
class DiaryRequest(BaseModel):
    
    member_id: int
    diary : str

@app.post("/diary/")
async def analyze_sentiment(request: DiaryRequest):
    # 응답으로 사용자로부터 받은 쿼리 파라미터 값을 반환
    if request.diary is not None:
        try:
            result = sentiment_analysis.sample_classify_document_multi_label(request.diary)
            # 반환된 결과를 JSON 응답으로 반환
            return result
        except Exception as e:
            return {"error": str(e)}
        
    else:
        return {"message": "Please provide a query parameter."}
    
    # db = SessionLocal()
    # create_diary_entry(db, reply=result)
    # db.close()

@app.post("/keyphrase/")
async def extract_phrases(request: DiaryRequest):
    # 응답으로 사용자로부터 받은 쿼리 파라미터 값을 반환
    if request.diary is not None:
        try:
            result = extract_key_phrase.sample_extract_key_phrases(request.diary)
            # 반환된 결과를 JSON 응답으로 반환
            return result
        except Exception as e:
            return {"error": str(e)}
        
    else:
        return {"message": "Please provide a query parameter."}


import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", log_level="info")