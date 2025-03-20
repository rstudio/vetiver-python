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
    pip_name = "scikit-learn"

    def handler_predict(self, input_data, check_prototype: bool, **kw):
        """
        Generates method for /predict endpoint in VetiverAPI

        The `handler_predict` function executes at each API call. Use this
        function for calling `predict()` and any other tasks that must be executed
        at each API call.

        Parameters
        ----------
        input_data:
            Test data
        check_prototype: bool
        prediction_type: str
            Type of prediction to make. One of "predict", "predict_proba",
            or "predict_log_proba". Default is "predict".

        Returns
        -------
        prediction:
            Prediction from model
        """
        prediction_type = kw.get("prediction_type", "predict")

        input_data = (
            [input_data]
            if check_prototype and not isinstance(input_data, pd.DataFrame)
            else input_data
        )

        if prediction_type in ["predict_proba", "predict_log_proba"]:
            return getattr(self.model, prediction_type)(input_data).tolist()

        return self.model.predict(input_data).to_list()
