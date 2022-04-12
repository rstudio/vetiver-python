from ..meta import vetiver_meta
from ..ptype import _vetiver_create_ptype
import numpy as np

class TorchHandler:
    """Handler class for creating VetiverModels with torch.

    Parameters
    ----------
    model : nn.Module
        a trained torch model
    """
    def __init__(self, model, ptype_data, save_ptype):
        self.model = model
        self.ptype_data = ptype_data
        self.save_ptype = save_ptype

    def create_description(self):
        """Create description for torch model
        """
        desc = f"Pytorch model of type {type(self.model)}"
        return desc

    def vetiver_create_meta(
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

    def ptype(self):
        """Create data prototype for torch model

        Parameters
        ----------
        ptype_data : pd.DataFrame, np.ndarray, or None
            Training data to create ptype
        save_ptype : bool

        Returns
        -------
        ptype : pd.DataFrame or None
            Zero-row DataFrame for storing data types
        """
        ptype = _vetiver_create_ptype(self.ptype_data, self.save_ptype)

        return ptype

    def handler_startup():
        """Include required packages for prediction

        The `handler_startup` function executes when the API starts. Use this
        function for tasks like loading packages.
        """
        ...

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
        import torch
        
        if check_ptype == True:
            input_data = np.array(input_data, dtype=np.array(self.ptype_data).dtype)
            prediction = self.model(torch.from_numpy(input_data))
        
        # do not check ptype
        else:
            batch = True
            if not isinstance(input_data, list):
                batch = False
                input_data = input_data.split(",")  # user delimiter ?
            input_data = np.array(input_data, dtype=np.array(self.ptype_data).dtype)
            if not batch:
                input_data = input_data.reshape(1, -1)
            prediction = self.model(torch.from_numpy(input_data))

        return prediction
