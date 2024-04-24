from openai import AzureOpenAI
from pymongo import MongoClient, DESCENDING
from config import AZURE_ENDPOINT, AZURE_API_KEY, ATLAS_MONGO_URL
import ast

model_gpt4turbo = "gachonkeagpt4turbo"
model_gpt35 = "gachonkeagpt35turbo"

dir_file_path = "Diary/sample_dir.txt"
lyrics_file_path = "Song/Song.json"
lyrics_path = "Song/Song.json"
genre_path = "Song/Genre.txt"
gender_path = "Song/Gender.txt"
group_path = "Song/Group.txt"
title_path = "Song/Title.txt"
song_url_path = "Song/"


def generate_lyrics(dir):
    client = AzureOpenAI(
        azure_endpoint=AZURE_ENDPOINT,
        api_key=AZURE_API_KEY,
        api_version="2024-02-15-preview"
    )
    persona_dict = {
        "genre": "힙합",
        "gender": "여성",
        "group": "솔로",
        "diary": [
            "종이 교과서가 사라진다면, 다른 글들처럼 글씨를 쓰지 않아도 되진 않을 것이다. 왜냐하면 손글씨를 쓴다는 것은 인간의 정서와 우리나라의 손글씨를 보존하는 것에 대부분 의의를 두기 때문이다."]
    }
    persona_dict_example = {
        "title": "손끝의 울림",
        "genre": "힙합",
        "gender": "여성",
        "group": "솔로",
        "image_prompt": "한 여성 래퍼가 무대 위에서 마이크를 잡고 강렬하게 랩을 하는 모습, 배경에는 디지털과 아날로그가 혼합된 아트워크가 표시되어 있음",
        "lyrics": [
            "[Verse 1]",
            "종이 교과서 사라져도 소멸되지 않지,",
            "손끝에서 태어난 글자들의 춤사위,",
            "키보드 위를 두드려도, 가슴 속엔 남아있어,",
            "손글씨의 온기가, 우리 정서의 증거니까.",

            "[Hook]",
            "글씨를 쓰지 않아도, 내 마음은 계속 뛰어,",
            "손으로 쓴 편지처럼, 감정은 더 진해져,",
            "손글씨의 의미를, 우리는 절대 잃지 않아,",
            "기술이 변해도, 손끝의 울림은 계속되니까.",

            "[Verse 2]",
            "손으로 쓴다는 건, 단순한 행위를 넘어서,",
            "우리나라의 정체성, 문화를 지키는 거야,",
            "역사 속에 새겨진, 수많은 이야기들,",
            "디지털 화면 속에도, 그 정신은 살아 숨 쉬어.",

            "[Hook]",
            "글씨를 쓰지 않아도, 내 마음은 계속 뛰어,",
            "손으로 쓴 편지처럼, 감정은 더 진해져,",
            "손글씨의 의미를, 우리는 절대 잃지 않아,",
            "기술이 변해도, 손끝의 울림은 계속되니까.",

            "[Bridge]",
            "잊지 마, 손글씨 하나하나에 담긴 무게를,",
            "우리의 정서와 문화, 그리고 영혼의 언어를,",
            "시대가 바뀌어도 변치 않는 가치를,",
            "이건 우리 모두의, 소중한 유산이니까.",

            "[Outro]",
            "종이 없어도 우리의 이야기는 계속 쓰여져,",
            "손으로 써내려간, 우리의 정서를 지키며,",
            "손끝의 울림으로, 문화를 이어가,",
            "우리나라의 손글씨, 영원히 보존될 거야."
        ]
    }
    # "ouput 값에는 '()' 표시가 존재해서는 안된다. 단순히 가사만 존재해야한다."
    persona = [{"role": "system", "content": "너는 사람들의 글의 내용을 바탕으로 장르에 맞게 lyrics와 title을 작성해주는 AI다."
                                             "한국어 가사를 작사하지만, 필요에 따라서는 가사에 외국어를 쓰기도 한다. 하지만 대부분 가사는 한국어로 이루어져 있다."
                                             "일기에 작성된 언어에 따라서 외국어로 작사해도 괜찮다."
                                             "최소 3분 이상의 가사를 작사해준다."
                                             "해당 글에 맞는 그림을 DALL-E3 Prompt에 지시할 내용을 알려준다."
                                             "너는 dict 형식으로 순서대로 title, genre, gender, group, image_prompt, lyrics를 반환한다."
                },
               {"role": "user", "content": str(persona_dict)},
               {"role": "assistant", "content": str(persona_dict_example)}]


    with open(genre_path, "r") as file:
        genre = file.read()
    with open(gender_path, "r") as file:
        gender = file.read()
    with open(group_path, "r") as file:
        group = file.read()
    text = {
        "genre": genre,
        "gender": gender,
        "group": group,
        "diary": dir
    }
    # Combine persona and input question
    message = persona + [{"role": "user", "content": str(text)}]

    # 속성값 수치 참고 자료
    # https://community.openai.com/t/cheat-sheet-mastering-temperature-and-top-p-in-chatgpt-api/172683
    completion = client.chat.completions.create(
        model=model_gpt4turbo,
        messages=message,
        temperature=0.7,
        max_tokens=4000,
        top_p=0.8,
        frequency_penalty=0,
        presence_penalty=0,
        # stop=None

        # gpt4-turbo 사용시에는 stop parameter 쓰면 안됨
    )
    return completion.choices[0].message.content



