import requests
import dotenv
import os
import time
dotenv.load_dotenv()
url_model_run = os.getenv("url_model_run")
url_model_classes = os.getenv("url_model_classes")



data = {'classes': [0]}
while True:
    files = {'file': open(os.getenv("file"), 'rb')}
    response = requests.post(url_model_run, files=files, json=data, headers={'x-key': os.getenv("token_key")})
    print(response.json())
    response = requests.get(url_model_classes, files=files, json=data, headers={'x-key': os.getenv("token_key")})
    print(response.json())
    time.sleep(10)