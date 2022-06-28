from ..ptype import vetiver_create_ptype
import pandas as pd
from ..meta import _model_meta
from .base import VetiverHandler

xgboost_exists = True
try:
    import xgboost
except ImportError:
    xgboost_exists = False


class XGBoostHandler(VetiverHandler):

    base_class = xgboost.Booster

    def describe(self):
        """Create description for sklearn model"""
        desc = f"Scikit-learn {self.model.__class__} model"
        return desc

    def construct_meta(
        user: list = None,
        version: str = None,
        url: str = None,
        required_pkgs: list = [],
    ):
        """Create metadata for xgboost model"""
        required_pkgs = required_pkgs + ["scikit-learn"]
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

        import xgboost

        if check_ptype == True:
            if isinstance(input_data, pd.DataFrame):
                real_input = xgboost.DMatrix(input_data)

                prediction = self.model.predict(real_input)
            else:
                prediction = self.model.predict(input_data)

        # NOTE: this code is copied from the sklearn handler
        # NOTE: how is this used?
        # do not check ptype
        else:
            if not isinstance(input_data, list):
                input_data = [input_data.split(",")]  # user delimiter ?

            dmat_data = xgboost.DMatrix(input_data, label=self.model.feature_names)
            prediction = self.model.predict(dmat_data)

        return prediction
