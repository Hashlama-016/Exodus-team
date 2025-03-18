from ultralytics import YOLO
from PIL import Image

from conf import get_conf


def load_model():
    try:
        model = YOLO(get_conf()["model_file"])
    except Exception as e:
        raise FileExistsError("failed to load model") from e
    return model


def run_model_on_image(image, classes):
    try:
        im = Image.open(image.file)
    except Exception as e:
        raise ValueError("failed to open image") from e
    model = load_model()
    try:
        results = model(im, classes=classes)
    except Exception as e:
        raise Exception("failed to run model on image") from e
    return results[0]


def get_model_classes():
    model = load_model()
    return model.names
