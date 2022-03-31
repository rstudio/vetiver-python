from sklearn.dummy import DummyRegressor
import pandas as pd
import numpy as np


def get_mock_data():
    """Create mock data for testing

    Returns
    -------
    X : pd.DataFrame
        Arbitrary data for testing purposes
    y : pd.Series
        Arbitrary reponse variable for testing purposes
    """
    data = pd.DataFrame(np.random.randint(0, 100, size=(100, 4)), columns=list("ABCD"))
    X, y = data.iloc[:, 1:], data["A"]
    return X, y


def get_mock_model():
    """Create mock model for testing

    Returns
    -------
    model : sklearn.dummy.DummyRegressor
        Arbitrary model for testing purposes
    """
    model = DummyRegressor()
    return model
