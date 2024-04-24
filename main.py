import sentiment_analysis
import extract_key_phrase
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

app = FastAPI()

#CORS 설정 (HTTP 통신 원활히)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


### 데이터 유효성을 확인하는 프로세스라고 함. 일단 1차적으로 통신이 문제없는지 확인할 때는 우선순위에서 밀린다고 생각해서 생략
# from pydantic import BaseModel
# # 유저 역할
# class Role(str, Enum): 
#     admin = "admin"
#     user = "user"
#     student = "student"


# class User(BaseModel):
#     # Optional : 필수적으로 필요한 것은 아님
#     id : Optional[UUID] = uuid4() # UUID : 범용 공유 식별자(Universally unique indentifier)
#     first_name : str
#     last_name : str
#     middle_name : Optional[str]
#     gender : Gender # class로 정의되어 있음
#     roles : List[Role]

@app.get("/diary")
async def root(query: str = Query(None, description="Enter a test string")):
    # 응답으로 사용자로부터 받은 쿼리 파라미터 값을 반환
    if query is not None:
        try:
            result = sentiment_analysis.sample_classify_document_multi_label(query)
            # 반환된 결과를 JSON 응답으로 반환
            return result
        except Exception as e:
            return {"error": str(e)}
        
    else:
        return {"message": "Please provide a query parameter."}
    
    # db = SessionLocal()
    # create_diary_entry(db, reply=result)
    # db.close()

@app.get("/keyphrase")
async def root(query: str = Query(None, description="Enter a test string")):
    # 응답으로 사용자로부터 받은 쿼리 파라미터 값을 반환
    if query is not None:
        try:
            result = extract_key_phrase.sample_extract_key_phrases(query)
            # 반환된 결과를 JSON 응답으로 반환
            return result
        except Exception as e:
            return {"error": str(e)}
        
    else:
        return {"message": "Please provide a query parameter."}

# @app.get("/{name}")
# async def generate_id_for_name(name: str):
#     return JSONResponse({
#         'id': str(uuid.uuid4()),
#         'name': name
#     })


import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", log_level="info")