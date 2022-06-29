import vetiver
from sklearn.dummy import DummyRegressor
import pandas as pd


def test_dummy_model():
    assert isinstance(vetiver.mock.get_mock_model(), DummyRegressor)


def test_dummy_data():
    X, y = vetiver.mock.get_mock_data()
    assert isinstance(X, pd.DataFrame)
    assert isinstance(y, pd.Series)
