from ..ptype import vetiver_create_ptype
from ..meta import vetiver_meta

class VetiverHandler:
    """Base handler class for creating VetiverModel of different type.

    Parameters
    ----------
    model :
        a trained model
    ptype_data:
        An object with information (data) whose layout is to be determined.
    """

    def __init__(self, model, ptype_data):
        self.model = model
        self.ptype_data = ptype_data

    def create_description(self):
        """Create description for model"""
        desc = f"{self.model.__class__} model"
        return desc

    def vetiver_create_meta(
        user: list = None,
        version: str = None,
        url: str = None,
        required_pkgs: list = [],
    ):
        """Create metadata for sklearn model"""
        meta = vetiver_meta(user, version, url, required_pkgs)

        return meta

    def ptype(self):
        """Create data prototype for torch model

        Parameters
        ----------
        ptype_data : pd.DataFrame, np.ndarray, or None
            Training data to create ptype

        Returns
        -------
        ptype : pd.DataFrame or None
            Zero-row DataFrame for storing data types
        """
        ptype = vetiver_create_ptype(self.ptype_data)
        return ptype

    def handler_startup():
        """Include required packages for prediction

        The `handler_startup` function executes when the API starts. Use this
        function for tasks like loading packages.
        """
        ...


    def handler_predict(self, input_data, check_ptype):
        """Generates method for /predict endpoint in VetiverAPI

        The `handler_predict` function executes at each API call. Use this
        function for calling `predict()` and any other tasks that must be executed
        at each API call.

        Parameters
        ----------
        input_data:
            Data used to generate prediction
        check_ptype:
            If type should be checked against `ptype` or not

        Returns
        -------
        prediction
            Prediction from model
        """
        ...
