import lyrics
import image_gen
import SunoAI
import mongo

#일기와 일기 분석 데이터를 받는다고 가정
dir_file_path= 'Diary/sample_dir.txt'
with open(dir_file_path, "r") as file:
    dir = file.read()
"""
lyrics = lyrics.generate_lyrics(dir)
print(lyrics)

song_id = mongo.save_lyrics_to_mongodb(lyrics)
print(song_id)
image_prompt = image_gen.get_image_prompt(song_id)
print(image_prompt)

image_url = image_gen.generate_image(image_prompt)
print(image_url)

image_s3_url = image_gen.download_and_upload_image_to_s3(song_id, image_url)
print(image_s3_url)
song_data = SunoAI.get_song_info_from_mongodb(song_id)
print(song_data)

music_url_data = SunoAI.generate_audio(song_data)
print(music_url_data)

music_s3_url = SunoAI.upload_audio_to_s3(music_url_data)
print(music_s3_url)
"""
song_id= "662867e46c02b91010a54654"
image_s3_url="https://arcadiaimage.s3.ap-northeast-2.amazonaws.com/662867e46c02b91010a54654.png"



music_s3_url = ['https://arcadiamusic.s3.ap-northeast-2.amazonaws.com/7bb058cc-08a0-43ad-8c3d-1704d93adc85.mp3', 'https://arcadiamusic.s3.ap-northeast-2.amazonaws.com/fee1679b-c5f8-4e4b-8685-2fe977b8a8c4.mp3']

dir_id = mongo.save_dir(dir, song_id, image_s3_url, music_s3_url)
print(dir_id)





"""
from fastapi import FastAPI
world = FastAPI()
@world.get("/")
async def root():

    return {"message" : "hello world"}

#uvicorn main:app
#https://www.youtube.com/watch?v=XnYYwcOfcn8&list=PLqAmigZvYxIL9dnYeZEhMoHcoP4zop8-p
"""