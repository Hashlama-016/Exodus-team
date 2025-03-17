from uvicorn import Server, Config
from conf import get_conf
from typing import Annotated
from fastapi import FastAPI, File, UploadFile
from model.model import run_model_on_image

# Load a COCO-pretrained YOLOv8n model

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/model/run")
def model_run(file: UploadFile = File(), classes: list = None, model: str = "yolov8x"):
    if classes is None:
        classes = [0]
    return run_model_on_image(file, classes=classes, model=model)


# Display model information (optional)

if __name__ == "__main__":
    port = get_conf()["port"]
    server = Server(Config(app, host="127.0.0.1", port=port, lifespan="on"))
    server.run()
