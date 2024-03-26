import pytest
import numpy as np
import pandas as pd
from requests.exceptions import HTTPError
from vetiver import mock, VetiverModel
from vetiver.server import predict

np.random.seed(500)
X, y = mock.get_mock_data()


@pytest.fixture
def model() -> VetiverModel:
    np.random.seed(500)
    model = mock.get_mock_model().fit(X, y)
    v = VetiverModel(
        model=model,
        prototype_data=X,
        model_name="my_model",
        versioned=None,
        description="A regression model for testing purposes",
    )

    return v


@pytest.mark.parametrize(
    "data,expected_length",
    [
        ([{"B": 0, "C": 0, "D": 0}], 1),
        (pd.Series(data=[0, 0, 0], index=["B", "C", "D"]), 1),
        (X, 100),
    ],
)
def test_predict_sklearn_ptype(data, expected_length, client):
    response = predict(endpoint="/predict/", data=data, test_client=client)
    assert isinstance(response, pd.DataFrame), response
    assert response.iloc[0, 0] == 44.47
    assert len(response) == expected_length


@pytest.mark.parametrize(
    "data,length",
    [({"B": 0, "C": 0, "D": 0}, 1), (pd.Series(data=[0, 0, 0]), 1), (X, 100)],
)
def test_predict_sklearn_no_ptype(data, length, client_no_prototype):
    response = predict(endpoint="/predict/", data=data, test_client=client_no_prototype)

    assert isinstance(response, pd.DataFrame), response
    assert response.iloc[0, 0] == 44.47
    assert len(response) == length


@pytest.mark.parametrize("data", [(0), 0, 0.0, "0"])
def test_predict_sklearn_type_error(data, client):

    msg = str(
        "[{'type': 'list_type', 'loc': ('body',), 'msg': 'Input should be a valid list', \
        'input': '0', 'url': 'https://errors.pydantic.dev/2.0.3/v/list_type'}]"
    )

    with pytest.raises(TypeError, match=msg):
        predict(endpoint="/predict/", data=data, test_client=client)


def test_predict_server_error(client):

    with pytest.raises(HTTPError):
        predict(endpoint="/i_do_not_exists/", data=X, test_client=client)
