#pip install openai==1.1.1
#pip install openai --upgrade
from bson import ObjectId
from openai import AzureOpenAI
import json

from pymongo import MongoClient

from config import AZURE_ENDPOINT, AZURE_API_KEY, AWS_SECRET_ACCESS_KEY, AWS_ACCESSS_KEY_ID, ATLAS_MONGO_URL
import os
import boto3
import requests
def generate_image(prompt):
    client = AzureOpenAI(
        api_version="2024-02-01",
        azure_endpoint=AZURE_ENDPOINT,
        api_key=AZURE_API_KEY,
    )

    result = client.images.generate(
        model="gachonkeadalle3",
        prompt=prompt,
        n=1,
        quality="standard",
        size="1024x1024"
    )

    image_url = json.loads(result.model_dump_json())['data'][0]['url']
    return image_url


def download_and_upload_image_to_s3(Song_id, image_url):
    # 이미지 다운
    bucket_name = "arcadiaimage"
    response = requests.get(image_url)
    if response.status_code == 200:
        img_name = f'{Song_id}.png'  # Use /tmp directory in Lambda for temporary storage
        with open(img_name, 'wb') as f:
            f.write(response.content)
        # S3에 업로드
        s3 = boto3.client('s3', aws_access_key_id = AWS_ACCESSS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                          region_name="ap-northeast-2")
        with open(img_name, 'rb') as image:
            s3.upload_fileobj(image, bucket_name, img_name)
        # S3에 업로드 후에 이미지 삭제
        os.remove(img_name)
        s3_url = f"https://{bucket_name}.s3.ap-northeast-2.amazonaws.com/{img_name}"

        return s3_url
    else:
        return None

def get_image_prompt(song_id):
    db_client = MongoClient(ATLAS_MONGO_URL)
    # Access the database and collection
    collection = db_client.Arcadia.Song
    # Find the document by its _id

    song_id_obj = ObjectId(song_id)

    song_document = collection.find_one({"_id": song_id_obj})
    return song_document.get("image_prompt")




