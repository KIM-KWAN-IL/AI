import os
import time
import uuid

import boto3
import requests
from bson import ObjectId
from pymongo import MongoClient

from config import SUNO_ENDPOINT, AWS_ACCESSS_KEY_ID, AWS_SECRET_ACCESS_KEY, ATLAS_MONGO_URL

# replace your vercel domain
base_url = SUNO_ENDPOINT
lyrics_path= "Song/Lyrics.txt"
genre_path= "Song/Genre.txt"
gender_path= "Song/Gender.txt"
group_path= "Song/Group.txt"
title_path= "Song/Title.txt"
song_url_path="Song/"


"""

def generate_audio_by_prompt(payload):
    url = f"{base_url}/api/generate"
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    return response.json()



def get_quota_information():
    url = f"{base_url}/api/get_limit"
    response = requests.get(url)
    return response.json()
"""

def custom_generate_audio(payload):
    url = f"{base_url}api/custom_generate"
    print(url)
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    return response.json()

def get_audio_information(audio_ids):
    url = f"{base_url}/api/get?ids={audio_ids}"
    response = requests.get(url)
    return response.json()


def generate_audio(song_data):
    title = str(song_data.get("title"))
    genre = str(song_data.get("genre"))
    gender = str(song_data.get("gender"))
    group = str(song_data.get("group"))
    lyrics = str(song_data.get("lyrics"))

    print("title : " + title)
    print("genre : " + genre)
    print("gender : " + gender)
    print("group : " + group)
    print("lyrics : " + lyrics)

    data = custom_generate_audio({
        "prompt": lyrics,
        "make_instrumental": False,
        "tags": f"{genre} {gender} {group}",
        "title": title,
        "wait_audio": False
    })
    print(data)
    ids = [data[0]['id'], data[1]['id']]
    print(f"ids: {ids}")

    music_urls = []

    for _ in range(60):
        data = get_audio_information(','.join(ids))
        if data[0]["status"] == 'streaming':
            for audio_data in data:
                music_urls.append(audio_data['audio_url'])
            break
        # sleep 5s
        time.sleep(5)

    return data

def upload_audio_to_s3(audio_info_list):
    bucket_name = "arcadiamusic"
    # Initialize S3 client
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESSS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name="ap-northeast-2")

    # Upload each audio file to S3
    music_s3_url = []
    for audio_info in audio_info_list:
        audio_url = audio_info['audio_url']
        audio_id = audio_info['id']
        # Download the audio file
        response = requests.get(audio_url)
        if response.status_code == 200:
            # Generate a unique filename using UUID
            audio_name = f"{audio_id}.mp3"

            # Save the audio file locally
            with open(audio_name, 'wb') as f:
                f.write(response.content)

            # Upload the audio file to S3
            s3_key = f"{audio_name}"
            with open(audio_name, 'rb') as audio_file:
                s3.upload_fileobj(audio_file, bucket_name, s3_key)

            # Delete the local audio file
            os.remove(audio_name)

            # Append the S3 URL to the list
            music_s3_url.append(f"https://{bucket_name}.s3.ap-northeast-2.amazonaws.com/{s3_key}")

    return music_s3_url
"""
def upload_audio_to_s3(audio_urls):
    bucket_name = "arcadiamusic"
    # Initialize S3 client
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESSS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name="ap-northeast-2")

    # Upload each audio file to S3
    audio_file_urls = []
    for audio_url in audio_urls:
        # Download the audio file
        response = requests.get(audio_url)
        if response.status_code == 200:
            # Generate a unique filename using UUID
            audio_id = str(uuid.uuid4())
            audio_name = f"{audio_id}.mp3"

            # Save the audio file locally
            with open(audio_name, 'wb') as f:
                f.write(response.content)

            # Upload the audio file to S3
            s3_key = f"{audio_name}"
            with open(audio_name, 'rb') as audio_file:
                s3.upload_fileobj(audio_file, bucket_name, s3_key)

            # Delete the local audio file
            os.remove(audio_name)

            # Append the S3 URL to the list
            audio_file_urls.append(f"https://{bucket_name}.s3.ap-northeast-2.amazonaws.com/{s3_key}")

    return audio_file_urls
    
"""
def get_song_info_from_mongodb(song_id):
    db_client = MongoClient(ATLAS_MONGO_URL)
    db = db_client.Arcadia
    collection = db.Song
    song_id_obj = ObjectId(song_id)

    song_document = collection.find_one({"_id": song_id_obj})
    if song_document:
        return song_document
    else:
        return None