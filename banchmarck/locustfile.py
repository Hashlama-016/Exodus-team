import os
import requests
from dotenv import load_dotenv
from locust import HttpUser, task, between, constant

load_dotenv()
url_model_run = os.getenv("url_model_run")
url_model_classes = os.getenv("url_model_classes")
url_model_s3_run = os.getenv("url_model_s3_run")


class QuickstartUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.client.get(url_model_classes, headers={'x-key': os.getenv("token_key")})

    @task
    def image(self):
        param = {'classes': [0]}
        files = {'file': open(os.getenv("file"), 'rb')}
        res = self.client.post(url_model_run, params=param, files=files, headers={'x-key': os.getenv("token_key")})
        try:
            res.raise_for_status()
        except Exception as e:
            print(e)

    @task
    def image_s3(self):
        params = {'classes': [0], 's3_path': os.getenv("s3_path")}
        res = self.client.post(url_model_s3_run, params=params, headers={'x-key': os.getenv("token_key")})
        try:
            res.raise_for_status()
        except Exception as e:
            print(e)


# requests.get(url_model_classes, headers={'x-key': os.getenv("token_key")})
# data = {'classes': [0]}
# files = {'file': open(os.getenv("file"), 'rb')}
# res = requests.post(url_model_run, files=files, json=data, headers={'x-key': os.getenv("token_key")})
# try:
#     res.raise_for_status()
# except Exception as e:
#     print(e)
# data = {'classes': [0], 's3_path': os.getenv("s3_path")}
# res = requests.post(url_model_s3_run, json=data, headers={'x-key': os.getenv("token_key")})