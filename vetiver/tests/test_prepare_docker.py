import pytest
import vetiver
import pandas as pd
import numpy as np

DOCKER_URL = "http://0.0.0.0:8080/predict"

pytestmark = pytest.mark.docker  # noqa
np.random.seed(500)


def test_predict_sklearn_df_check_ptype():

    X, y = vetiver.mock.get_mock_data()
    response = vetiver.predict(endpoint=DOCKER_URL, data=X)

    assert isinstance(response, pd.DataFrame), response
    assert response.iloc[0, 0] == 54.52
    assert len(response) == 100
