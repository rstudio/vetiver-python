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
        if self.prototype_data is None:
            text_column_name = "text"

        else:
            if len(self.prototype_data.columns) != 1:
                raise TypeError("Expected 1 column of text data")

            text_column_name = self.prototype_data.columns[0]

        prototype = vetiver_create_prototype(pd.DataFrame({text_column_name: ["text"]}))

        return prototype

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
        if not spacy_exists:
            raise ImportError("Cannot import `spacy`")

        response_body = []

        input_data = api_data_to_frame(input_data)

        for doc in self.model.pipe(input_data.iloc[:, 0]):
            response_body.append(doc.to_json())

        return pd.Series(response_body)
