import pandas as pd
import sklearn

from .base import BaseHandler


class SKLearnHandler(BaseHandler):
    """Handler class for creating VetiverModels with sklearn.

    Parameters
    ----------
    model : sklearn.base.BaseEstimator
        a trained sklearn model
    """

    model_class = staticmethod(lambda: sklearn.base.BaseEstimator)

    def describe(self):
        """Create description for sklearn model"""
        desc = f"Scikit-learn {self.model.__class__} model"
        return desc

    def create_meta(
        self,
        user: dict = None,
        version: str = None,
        url: str = None,
        required_pkgs: list = [],
    ):
        """Create metadata for sklearn model"""
        if "scikit-learn" not in required_pkgs:
            required_pkgs = required_pkgs + ["scikit-learn"]
        meta = super().create_meta(user, version, url, required_pkgs)

        return meta

    def handler_predict(self, input_data, check_prototype):
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

        if not check_prototype or isinstance(input_data, pd.DataFrame):
            prediction = self.model.predict(input_data)
        else:
            prediction = self.model.predict([input_data])

        return prediction
