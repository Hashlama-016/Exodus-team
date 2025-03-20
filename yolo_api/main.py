from uvicorn import Server, Config
from conf import get_conf
from fastapi import FastAPI, File, UploadFile, HTTPException, APIRouter, Depends
from model.model import run_model_on_image, get_model_classes
from pydantic import ValidationError
from model.input_model import ModelInput
from auth import handle_api_key
import requests

app = FastAPI()
public = APIRouter()
secure = APIRouter(dependencies=[Depends(handle_api_key)])


def fetch_image(image_url: str) -> bytes:
    """
    Fetches an image from a given URL and returns it as a byte array.

    :param image_url: URL of the image (Azure Blob URL)
    :return: Image content as bytes
    :raises ValueError: If the URL is empty
    :raises requests.exceptions.RequestException: For network-related errors
    """
    if not image_url:
        raise ValueError("Image URL cannot be empty")

    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()  # Raises an error for HTTP errors (4xx and 5xx)
        return response.content  # Return image as bytes

    except requests.exceptions.MissingSchema:
        raise ValueError("❌ Invalid URL format")
    except requests.exceptions.ConnectionError:
        raise ConnectionError("❌ Failed to connect to the server")
    except requests.exceptions.Timeout:
        raise TimeoutError("❌ The request timed out")
    except requests.exceptions.HTTPError as e:
        raise requests.exceptions.HTTPError(f"❌ HTTP Error: {e}")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"❌ Unexpected error: {e}")



@public.get("/")
def read_root():
    return "ok status"


@secure.post("/model/run")
async def model_run(file: UploadFile = File(), classes: list = None):
# async def model_run(image_url: str, classes: list = None):
    if classes is None:
        classes = [0]
    # try:
    #     image_url = "https://yourstorageaccount.blob.core.windows.net/container-name/image.jpg"
    #     image_data = fetch_image(image_url)
    #     print(f"✅ Image fetched successfully! Size: {len(image_data)} bytes")
    # except Exception as e:
    #     print(e)
    
    try:
        # input_model = ModelInput(file=image_data, classes=classes)
        input_model = ModelInput(file=file, classes=classes)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    try:
        result = run_model_on_image(input_model.file, classes=input_model.classes)
    except FileExistsError as e:
        raise HTTPException(status_code=500, detail="failed load model")
    except ValueError as e:
        raise HTTPException(status_code=422, detail="failed to open image")
    except Exception as e:
        raise HTTPException(status_code=500, detail="failed to run model on image")
    return result.to_json()


@secure.get("/model/classes")
async def model_classes():
    return get_model_classes()


if __name__ == "__main__":
    app.include_router(public)
    app.include_router(secure)
    port = get_conf()["port"]
    server = Server(Config(app, host="0.0.0.0", port=port, lifespan="on"))
    server.run()