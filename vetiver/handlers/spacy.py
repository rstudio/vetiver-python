from .base import BaseHandler

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

    model_class = staticmethod(lambda: spacy.pipeline.Pipe)

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

        doc = spacy.tokens.Doc.from_json(input_data)

        # if not isinstance (doc, list):
        #     doc = [doc]
        # needs to be in doc format to make prediction
        # doc is not json serializable
        prediction = self.model.predict([doc])

        return prediction
