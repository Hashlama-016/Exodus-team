from uvicorn import Server, Config
from conf import get_conf
from fastapi import FastAPI, File, UploadFile, HTTPException, APIRouter, Depends
from model.model import run_model_on_image, get_model_classes
from pydantic import ValidationError
from model.input_model import ModelInput
from auth import handle_api_key

app = FastAPI()
public = APIRouter()
secure = APIRouter(dependencies=[Depends(handle_api_key)])


@public.get("/")
def read_root():
    return "🤖🦊🦒"


@secure.post("/model/run")
async def model_run(file: UploadFile = File(), classes: list = None):
    if classes is None:
        classes = [0]
    try:
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
