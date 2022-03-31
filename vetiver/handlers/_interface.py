from vetiver.handlers import pytorch_vt, sklearn_vt
from torch import nn
import sklearn

class NoAvailableHandlerError(Exception):
    """
    Throw an error if we don't find a method
    available to create a handler for `model`
    """

    def __init__(
        self,
        message="Unsupported model type. Supported models are: sklearn, torch.",
    ):
        self.message = message
        super().__init__(self.message)

def create_translator(model, ptype_data, save_ptype):
    """check for model type to handle prediction

    Parameters
    ----------
    model
        Description of parameter `x`.

    Returns
    -------
    pytorch_vt.TorchHandler or sklearn_vt.SKLearnHandler
        Handler class for specified model type
    """

    if isinstance(model, nn.Module):
        return pytorch_vt.TorchHandler(model, ptype_data, save_ptype)

    elif isinstance(model, sklearn.base.BaseEstimator):
        return sklearn_vt.SKLearnHandler(model, ptype_data, save_ptype)

    else:
        NoAvailableHandlerError
