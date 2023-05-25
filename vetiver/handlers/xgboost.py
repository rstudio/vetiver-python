import pandas as pd

from .base import BaseHandler

xgb_exists = True
try:
    import xgboost
except ImportError:
    xgb_exists = False


class XGBoostHandler(BaseHandler):
    """Handler class for creating VetiverModels with xgboost.

    Parameters
    ----------
    model : xgboost.Booster
        a trained and fit xgboost model
    """

    model_class = staticmethod(lambda: xgboost.Booster)
    if xgb_exists:
        pip_name = "xgboost"

    def handler_predict(self, input_data, check_prototype):
        """
        Generates method for /predict endpoint in VetiverAPI

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

        if not xgb_exists:
            raise ImportError("Cannot import `xgboost`")

        if not isinstance(input_data, pd.DataFrame):
            try:
                input_data = pd.DataFrame(input_data)
            except ValueError:
                raise (f"Expected a dict or DataFrame, got {type(input_data)}")

        input_data = xgboost.DMatrix(input_data)

        prediction = self.model.predict(input_data)

        return prediction.tolist()
