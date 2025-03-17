import requests
url = 'http://127.0.0.1:8081/model_run_model_run_post'
files = {'media': open('im1.jpg', 'rb')}
requests.post(url, json=data)