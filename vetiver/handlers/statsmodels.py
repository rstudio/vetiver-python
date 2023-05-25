import pandas as pd

from .base import BaseHandler

sm_exists = True
try:
    import statsmodels.api
except ImportError:
    sm_exists = False


class StatsmodelsHandler(BaseHandler):
    """Handler class for creating VetiverModels with statsmodels.

    Parameters
    ----------
    model : statsmodels
        a trained and fit statsmodels model
    """

    model_class = staticmethod(lambda: statsmodels.base.wrapper.ResultsWrapper)
    if sm_exists:
        pip_name = "statsmodels"

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
        if not sm_exists:
            raise ImportError("Cannot import `statsmodels`")

        if isinstance(input_data, (list, pd.DataFrame)):
            prediction = self.model.predict(input_data)
        else:
            prediction = self.model.predict([input_data])

        return prediction.tolist()
