from .base import BaseHandler
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

    # what to do about prototypes?

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

        for doc in self.model.pipe(input_data.text):
            response_body.append(get_data(doc))

        return pd.Series(response_body)


def get_data(doc):
    ents = [
        {
            "label": ent.label_,
            "start": ent.start_char,
            "end": ent.end_char,
        }
        for ent in doc.ents
    ]
    return {"text": doc.text, "ents": ents}
