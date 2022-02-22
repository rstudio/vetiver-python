from sklearn.dummy import DummyRegressor
import pandas as pd
import numpy as np


def get_mock_data():
    data = pd.DataFrame(np.random.randint(0, 100, size=(100, 4)), columns=list("ABCD"))
    X, y = data.iloc[:, 1:], data["A"]
    return X, y


def get_mock_model():
    model = DummyRegressor()
    return model
