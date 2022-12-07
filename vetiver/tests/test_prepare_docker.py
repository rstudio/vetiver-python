import pytest
import vetiver
import pandas as pd
import numpy as np

DOCKER_URL = "http://0.0.0.0:8080/predict"

pytestmark = pytest.mark.docker  # noqa


def test_predict_sklearn_df_check_ptype():
    np.random.seed(500)

    X, y = vetiver.mock.get_mock_data()
    response = vetiver.predict(endpoint=DOCKER_URL, data=X)

    assert isinstance(response, pd.DataFrame), response
    assert response.iloc[0, 0] == 44.47
    assert len(response) == 100
