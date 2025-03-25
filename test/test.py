import requests
import dotenv
import os
import time
dotenv.load_dotenv()
url_model_run = os.getenv("url_model_run")
url_model_classes = os.getenv("url_model_classes")
url_model_s3_run = os.getenv("url_model_s3_run")


params = {'classes': [0]}

files = {'file': open(os.getenv("file"), 'rb')}
response = requests.post(url_model_run, files=files, params=params, headers={'x-key': os.getenv("token_key")})
print(response.json())
response = requests.get(url_model_classes, headers={'x-key': os.getenv("token_key")})
print(response.json())
params = {'classes': [0], 's3_path': os.getenv("s3_path")}
response = requests.post(url_model_s3_run, params=params, headers={'x-key': os.getenv("token_key")})
print(response.json())

