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
        prediction:
            Prediction from model
        """

        if not check_prototype or isinstance(input_data, pd.DataFrame):
            prediction = self.model.predict(input_data)
        else:
            prediction = self.model.predict([input_data])

        return prediction.tolist()
