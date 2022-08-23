import pandas as pd

from ..meta import _model_meta
from .base import BaseHandler

xgb_exists = True
try:
    import xgboost
except ImportError:
    xgb_exists = False


class XGBoostHandler(BaseHandler):
    """Handler class for creating VetiverModels with statsmodels.

    Parameters
    ----------
    model : statsmodels
        a trained and fit statsmodels model
    """

    model_class = staticmethod(lambda: xgboost.Booster)

    def __init__(self, model, ptype_data):
        super().__init__(model, ptype_data)

    def describe(self):
        """Create description for xgboost model"""
        desc = f"Statsmodels {self.model.__class__} model."
        return desc

    def create_meta(
        user: list = None,
        version: str = None,
        url: str = None,
        required_pkgs: list = [],
    ):
        """Create metadata for statsmodel"""
        required_pkgs = required_pkgs + ["xgboost"]
        meta = _model_meta(user, version, url, required_pkgs)

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

        if xgb_exists:
            if not isinstance(input_data, xgboost.DMatrix):
                if isinstance(input_data, pd.DataFrame):
                    input_data = xgboost.DMatrix(input_data)
                else:
                    input_data = xgboost.DMatrix(
                        input_data, label=self.model.feature_names
                    )

            prediction = self.model.predict(input_data)
        else:
            raise ImportError("Cannot import `xgboost`")

        return prediction
