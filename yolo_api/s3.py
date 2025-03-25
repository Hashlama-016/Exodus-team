import io
import boto3
from conf import get_conf
from PIL import Image


def get_s3_image(s3_path):
    s3 = boto3.resource('s3', endpoint_url=get_conf()["aws_endpoint_url"],
                        aws_access_key_id=get_conf()["aws_access_key_id"],
                        aws_secret_access_key=get_conf()["aws_secret_access_key"])
    my_bucket = s3.Bucket(get_conf()["bucket_name"])
    file_s3 = my_bucket.Object(key=s3_path)
    download_file_stream = io.BytesIO()
    file_s3.download_fileobj(download_file_stream)
    file = Image.open(download_file_stream)
    return file
