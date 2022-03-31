from ..ptype import _vetiver_create_ptype
import torch
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

    def create_meta():
        """Create metadata for torch model
        """
        ...

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
        """
        ...

    def handler_predict(self, input_data, argmax=False):
        """Generates method for /predict endpoint in VetiverAPI

        Parameters
        ----------
        input_data:
            Test data

        Returns
        -------
        prediction
            Prediction from model
        """
        dt = np.array(self.ptype_data).dtype
        input_data = np.array(input_data, dtype=dt)
        prediction = self.model(torch.from_numpy(input_data))

        if argmax:

            prediction = np.argmax(prediction)

        return prediction
