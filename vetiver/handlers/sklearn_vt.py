from ..ptype import _vetiver_create_ptype

import pandas as pd
import numpy as np

class SKLearnHandler:
    """Handler class for creating VetiverModels with sklearn.

    Parameters
    ----------
    model : sklearn.base.BaseEstimator
        a trained sklearn model
    """
    def __init__(self, model, ptype_data, save_ptype):
        self.model = model
        self.ptype_data = ptype_data
        self.save_ptype = save_ptype

    def create_description(self):
        """Create description for sklearn model
        """
        desc = f"Scikit-learn model of type {type(self.model)}"
        return desc

    def create_meta():
        """Create metadata for sklearn model
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
        if check_ptype == True:
            if isinstance(input_data, pd.DataFrame):
                prediction = self.model.predict(input_data)
            else:
               prediction = self.model.predict([input_data])

        # do not check ptype
        else:
            if not isinstance(input_data, list):
                input_data = [input_data.split(",")]  # user delimiter ?

            prediction = self.model.predict(input_data)

        return prediction
