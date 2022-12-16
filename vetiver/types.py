from pydantic import BaseModel, create_model

all = ["Prototype", "create_prototype"]


class Prototype(BaseModel):
    pass


def create_prototype(**dict_data):
    return create_model("prototype", __base__=Prototype, **dict_data)
