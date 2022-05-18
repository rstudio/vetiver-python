from ..ptype import vetiver_create_ptype
import pandas as pd
from ..meta import vetiver_meta
import sklearn

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
        desc = f"Scikit-learn {self.model.__class__} model"
        return desc

    def vetiver_create_meta(
        user: list = None,
        version: str = None,
        url: str = None,
        required_pkgs: list = [],
    ):
        """Create metadata for sklearn model"""
        required_pkgs = required_pkgs + ["scikit-learn"]
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
        ptype = vetiver_create_ptype(self.ptype_data, self.save_ptype)
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
