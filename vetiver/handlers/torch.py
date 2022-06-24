import numpy as np

from .base import VetiverHandler
from ..meta import vetiver_meta

torch_exists = True
try:
    import torch
except ImportError:
    torch_exists = False


class TorchHandler(VetiverHandler):
    """Handler class for creating VetiverModels with torch.

    Parameters
    ----------
    model : nn.Module
        a trained torch model
    """
    base_class = torch.nn.Module
    def __init__(self, model, ptype_data):
        super().__init__(model, ptype_data)

    def describe(self):
        """Create description for torch model
        """
        desc = f"Pytorch model of type {type(self.model)}"
        return desc

    def create_meta(
        user: list = None,
        version: str = None,
        url: str = None,
        required_pkgs: list = [],
    ):
        """Create metadata for torch model
        """
        required_pkgs = required_pkgs + ["torch"]
        meta = vetiver_meta(user, version, url, required_pkgs)

        return meta

    def handler_predict(self, input_data, check_ptype):
        """Generates method for /predict endpoint in VetiverAPI

        The `handler_predict` function executes at each API call. Use this
        function for calling `predict()` and any other tasks that must be executed
        at each API call.

        Parameters
        ----------
        input_data:
            Test data

        Returns
        -------
        prediction
            Prediction from model
        """
        if torch_exists:
            if check_ptype == True:
                input_data = np.array(input_data, dtype=np.array(self.ptype_data).dtype)
                prediction = self.model(torch.from_numpy(input_data))
            
            # do not check ptype
            else:    
                input_data = torch.tensor(input_data)
                prediction = self.model(input_data)

        else:
            raise ImportError("Cannot import `torch`.")

        return prediction
