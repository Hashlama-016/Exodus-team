from ultralytics import YOLO
from pydantic import BaseModel
from PIL import Image


def run_model_on_image(image, classes, model):
    im = Image.open(image.file)
    model = YOLO(f"{model}.pt")
    results = model(im, classes=classes)  # [0] return a list of Results objects
    return results[0]

# print(results)
# print(type(results[0]))
# # Process results list
# for result in results:
#     boxes = result.boxes  # Boxes object for bounding box outputs
#     masks = result.masks  # Masks object for segmentation masks outputs
#     keypoints = result.keypoints  # Keypoints object for pose outputs
#     probs = result.probs  # Probs object for classification outputs
#     obb = result.obb  # Oriented boxes object for OBB outputs
#     result.show()  # display to screen
#     result.save(filename="../result.jpg")
