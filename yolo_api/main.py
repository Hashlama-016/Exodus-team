from uvicorn import Server, Config
from conf import get_conf
from fastapi import FastAPI, File, UploadFile, HTTPException, APIRouter, Depends
from model.model import run_model_on_image, get_model_classes, run_model_on_s3_image
from pydantic import ValidationError
from model.input_model import ModelInput, ModelInputS3
from auth import handle_api_key

app = FastAPI()
public = APIRouter()
secure = APIRouter(dependencies=[Depends(handle_api_key)])


@public.get("/")
def read_root():
    return "ok status"


@secure.post("/model/run")
async def model_run(query: ModelInput = Depends()):
    try:
        result = run_model_on_image(query.file, classes=query.classes)
    except FileExistsError as e:
        raise HTTPException(status_code=500, detail="failed load model")
    except ValueError as e:
        raise HTTPException(status_code=422, detail="failed to open image")
    except Exception as e:
        raise HTTPException(status_code=500, detail="failed to run model on image")
    return result.to_json()


@secure.post("/model/run/s3/image")
async def model_from_s3_run(query: ModelInputS3 = Depends()):
    try:
        result = run_model_on_s3_image(query.s3_path, classes=query.classes)
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
    server = Server(Config(app, workers=4, host="0.0.0.0", port=port, lifespan="on"))
    server.run()
