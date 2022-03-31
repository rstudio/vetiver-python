from ..ptype import _vetiver_create_ptype
import sklearn

class SKLearnHandler:
    """Handler class for creating VetiverModels with sklearn.

    Parameters
    ----------
    model : sklearn.base.BaseEstimator
        a trained sklearn model
    """
    def __init__(self, model, ptype_data, save_ptype):
        self.model = model
        self.ptype_data = ptype_data
        self.save_ptype = save_ptype

    def create_description(self):
        """Create description for sklearn model
        """
        desc = f"Scikit-learn model of type {type(self.model)}"
        return desc

    def create_meta():
        """Create metadata for sklearn model
        """
        ...

    def ptype(self):
        """Create data prototype for torch model

        Parameters
        ----------
        ptype_data : pd.DataFrame, np.ndarray, or None
            Training data to create ptype
        save_ptype : bool

        Returns
        -------
        ptype : pd.DataFrame or None
            Zero-row DataFrame for storing data types
        """
        ptype = _vetiver_create_ptype(self.ptype_data, self.save_ptype)
        return ptype

    def handler_startup():
        """Generates method for /predict endpoint in VetiverAPI

        Parameters
        ----------
        input_data:
            Test data

        Returns
        -------
        prediction
            Prediction from model
        """
        ...

    def handler_predict(self, input_data, predict_proba: bool = False):

        if predict_proba:
            prediction = self.model.predict_proba([input_data])

        prediction = self.model.predict([input_data])

        return prediction
