from pymongo import MongoClient
from config import ATLAS_MONGO_URL
import ast
#실제로는 일기랑 분석 나누어서 받을 듯
def save_dir(dir, song_id, image_s3_url, music_s3_url):
    print("music_s3_url1" + music_s3_url[0])
    db_client = MongoClient(ATLAS_MONGO_URL)
    post={
        "diary": dir,
        "song": song_id,
        "image_s3_url" : image_s3_url,
        "music_s3_url1" : music_s3_url[0],
        "music_s3_url2": music_s3_url[1]

        # Add more variables as needed
    }
    collection = db_client.Arcadia.Dir
    insert_result = collection.insert_one(post)
    dir_id = insert_result.inserted_id
    return dir_id

def save_lyrics_to_mongodb(song):
    db_client = MongoClient(ATLAS_MONGO_URL)
    song_dict = ast.literal_eval(song)

    collection = db_client.Arcadia.Song
    insert_result = collection.insert_one(song_dict)
    song_id = insert_result.inserted_id
    return song_id