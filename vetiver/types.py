from pydantic import BaseModel, create_model

all = ["Prototype", "create_prototype"]


class Prototype(BaseModel):
    pass


class Config:
    arbitrary_types_allowed = True


def create_prototype(**dict_data):
    return create_model("prototype", __config__=Config, **dict_data)
