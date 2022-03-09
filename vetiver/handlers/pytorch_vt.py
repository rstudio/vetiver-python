from numpy import float16
from ..ptype import vetiver_create_ptype


class TorchHandler:
    def __init__(self, model):
        self.model = model

    def create_description(self):
        desc = f"Pytorch model of type {type(self.model)}"
        return desc

    def create_meta():
        ...

    def prepare_model():
        ...

    def ptype(self, ptype_data, save_ptype):
        ptype = vetiver_create_ptype(ptype_data, save_ptype)

    def handler_startup():
        # add in required package
        ...

    def handler_predict(self, input_data, argmax=False):
        import torch
        import numpy as np

        input_data = np.array(input_data, dtype=np.float32)
        prediction = self.model(torch.from_numpy(input_data))

        if argmax:
            import numpy as np

            prediction = np.argmax(prediction)

        return prediction
