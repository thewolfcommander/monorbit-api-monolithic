import re
from decouple import config
import boto3
from datetime import datetime
from botocore.exceptions import NoCredentialsError, ClientError

ACCESS_KEY = config('AWS_ACCESS_KEY_ID')
SECRET_KEY = config('AWS_SECRET_ACCESS_KEY')
BUCKET_NAME = config('S3_BUCKET_NAME')


def get_ext(file):
    m = re.search(r'\.[A-Za-z0-9]+$', file)
    return m.group(0) if m else ""


def upload_file(file, filetype):
    s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    REGION='us-west-2'
    today = datetime.now()
    try:
        file_ext = get_ext(file)
    except:
        if filetype == 'IMG':
            file_ext = '.png'
        elif filetype == 'VID':
            file_ext = '.mp4'
        elif filetype == 'DOC':
            file_ext = '.pdf'
        elif filetype == 'AUD':
            file_ext = '.mp3'
        else:
            return False

    if file_ext == "":
        file_ext = 'png'
    filename = "MONO-{}-{}{}{}{}{}{}{}{}".format(filetype, today.year, today.month, today.day, today.hour, today.minute, today.second, today.microsecond, file_ext)
    try:
        # response = s3_client.upload_file(file, BUCKET_NAME, 'hello.png')

        with open(file, "rb") as f:
            response = s3_client.upload_fileobj(file, BUCKET_NAME, '{}/{}/{}/{}/{}/{}'.format(filetype, today.year, today.month, today.day, today.hour, filename))
        url = 'http://{}.s3.{}.amazonaws.com/{}/{}/{}/{}/{}/{}'.format(str(BUCKET_NAME), str(REGION), str(filetype), str(today.year), str(today.month), str(today.day), str(today.hour), str(filename))
        return url
    except ClientError as e:
        print(e)
        return False
    return True




# uploaded = upload_file('myapp_models.png', 'IMG')
# print(uploaded)