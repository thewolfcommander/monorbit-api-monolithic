
import re
import os
import time
import boto3
import uuid
from datetime import datetime
from botocore.client import Config
from decouple import config as env_config


ACCESS_KEY = env_config('AWS_ACCESS_KEY_ID')
SECRET_KEY = env_config('AWS_SECRET_ACCESS_KEY')
BUCKET_NAME = env_config('S3_BUCKET_NAME')

def get_ext(file):
    m = re.search(r'\.[A-Za-z0-9]+$', file)
    return m.group(0) if m else ""

# print(get_ext("hello.gif"))

def get_file_name(file):
    random_file_name = '-'.join([str(uuid.uuid4().hex[:14]), file])
    return random_file_name

# print(get_file_name("myapp_models.png"))

def upload(file, filetype, name):
    """
    FIle type should be - IMG, VID, DOC, AUD
    """
    TYPES = {
        "images": [".jpg", ".png", ".webp", ".svg"], 
        "documents": [".docx", ".pdf", ".md", ".xlsx"], 
        "videos": [".mp4", ".mkv"], 
        "audios": [".mp3", ".wav", ".ogg"], 
    }

    data = file
    # print(file)

    s3 = boto3.resource(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        config=Config(signature_version='s3v4')
    )

    REGION='us-west-2'
    today = datetime.now()
    # try:
    file_ext = get_ext(name)

    if file_ext == "":
        file_ext = 'png'
    filename = "MONO-{}-{}{}{}{}{}{}{}{}".format(filetype, today.year, today.month, today.day, today.hour, today.minute, today.second, today.microsecond, file_ext)
    filepath = '{}/{}/{}/{}/{}/{}'.format(filetype, today.year, today.month, today.day, today.hour, filename)
    s3.Bucket(BUCKET_NAME).put_object(Key=filepath, Body=data,ContentType='image/jpeg')
    object_acl = s3.ObjectAcl(BUCKET_NAME, filepath)
    response = object_acl.put(ACL='public-read')
    url = 'https://{}.s3.{}.amazonaws.com/{}/{}/{}/{}/{}/{}'.format(str(BUCKET_NAME), str(REGION), str(filetype), str(today.year), str(today.month), str(today.day), str(today.hour), str(filename))

    return url, file_ext

# uploaded = upload('myapp_models.png', 'IMG')
# print(uploaded)