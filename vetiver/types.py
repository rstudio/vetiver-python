from pydantic import BaseModel, create_model
from typing import Literal

all = ["Prototype", "create_prototype"]


class Prototype(BaseModel):
    pass


SklearnPredictionTypes = Literal["predict", "predict_proba", "predict_log_proba"]


def create_prototype(**dict_data):
    return create_model("prototype", __base__=Prototype, **dict_data)
