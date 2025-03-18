from pydantic import BaseModel, AfterValidator
from typing_extensions import Annotated
from fastapi import UploadFile


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


class ModelInput(BaseModel):
    file: UploadFile
    classes: Annotated[list, AfterValidator(is_integer_list)]
