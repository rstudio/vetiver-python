from typing import Protocol
from vetiver.handlers import pytorch_vt, sklearn_vt


class ITranslator(Protocol):  # adapter?
    def __init__(self, model):
        model = self.model

    def create_description():
        ...

    def create_meta():
        ...

    def prepare_model():
        ...

    def ptype():
        ...

    def handler_startup():
        ...

    def handler_predict():
        ...


def create_translator(model):
    # import joblib
    # if isinstance(model, joblib):
    #     model = joblib.load(model)
    from torch import nn

    if isinstance(model, nn.Module):
        return pytorch_vt.TorchHandler(model)
    import sklearn

    if isinstance(model, sklearn.base.BaseEstimator):
        return sklearn_vt.SKLearnHandler(model)
