from pydantic import BaseModel, AfterValidator, Field
from typing_extensions import Annotated
from fastapi import UploadFile, Query
from typing import List


def is_integer_list(value: list) -> list:
    if len(value) != len(set(value)):
        raise ValueError('List must contain unique values')
    for item in value:
        if item != int(item):
            raise ValueError('List must contain only integers')
    if max(value) > 79:
        raise ValueError('List must contain values less than 80')
    if min(value) < 0:
        raise ValueError('List must contain values more than -1')
    return value


def is_s3_path_to_image(value: str) -> str:
    if not value.endswith(".jpg"):
        raise ValueError('S3 path must end with .jpg')
    return value


class ModelInput(BaseModel):
    file: UploadFile
    classes: Annotated[List[int], AfterValidator(is_integer_list)] = Field(Query(...))


class ModelInputS3(BaseModel):
    s3_path: Annotated[str, AfterValidator(is_s3_path_to_image)]
    classes: Annotated[List[int], AfterValidator(is_integer_list)] = Field(Query(...))


