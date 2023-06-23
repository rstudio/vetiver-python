from .base import BaseHandler
from ..prototype import vetiver_create_prototype
from ..helpers import api_data_to_frame

import pandas as pd

spacy_exists = True
try:
    import spacy
except ImportError:
    spacy_exists = False


class SpacyHandler(BaseHandler):
    """Handler class for creating VetiverModels with spacy.

    Parameters
    ----------
    model :
        a trained and fit spacy model
    """

    model_class = staticmethod(lambda: spacy.Language)

    if spacy_exists:
        pip_name = "spacy"

    def construct_prototype(self):
        """Create data prototype for a spacy model, which is one column of string data

        Returns
        -------
        prototype :
            Input data prototype for spacy model
        """
        if self.prototype_data is not None and not isinstance(
            self.prototype_data, (pd.Series, pd.DataFrame, dict)
        ):  # wrong type
            raise TypeError(
                "Spacy prototype must be a dict, pandas Series, or pandas DataFrame"
            )
        elif (
            isinstance(self.prototype_data, pd.DataFrame)
            and len(self.prototype_data.columns) != 1
        ):  # is dataframe, more than one column
            raise ValueError("Spacy prototype data must be a 1-column pandas DataFrame")
        elif (
            isinstance(self.prototype_data, dict) and len(self.prototype_data) != 1
        ):  # is dict, more than one key
            raise ValueError("Spacy prototype data must be a dictionary with 1 key")

        prototype = vetiver_create_prototype(self.prototype_data)

        return prototype

    def handler_predict(self, input_data, check_prototype):
        """
        Generates method for /predict endpoint in VetiverAPI

        The `handler_predict` function executes at each API call. Use this
        function for calling `predict()` and any other tasks that must be executed
        at each API call.

        Parameters
        ----------
        input_data:
            Test data. The SpacyHandler expects an input of a 1 column DataFrame with
            the same column names as the prototype data, or column name "text" if no
            prototype was given.

        Returns
        -------
        prediction
            Prediction from model
        """
        if not spacy_exists:
            raise ImportError("Cannot import `spacy`")

        response_body = []

        input_data = api_data_to_frame(input_data)

        for doc in self.model.pipe(input_data.iloc[:, 0]):
            response_body.append(doc.to_json())

        return pd.Series(response_body)
