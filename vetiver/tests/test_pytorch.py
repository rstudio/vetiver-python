import pytest

torch = pytest.importorskip("torch", reason="torch library not installed")

import numpy as np  # noqa
import pandas as pd  # noqa
import requests  # noqa
from fastapi.testclient import TestClient  # noqa

from vetiver import VetiverModel, VetiverAPI, predict  # noqa
import vetiver  # noqa


@pytest.fixture
def build_torch():
    torch.manual_seed(3)

    input_size = 1
    output_size = 1

    x_train = np.array(
        [
            [3.3],
            [4.4],
            [5.5],
            [6.71],
            [6.93],
            [4.168],
            [9.779],
            [6.182],
            [7.59],
            [2.167],
            [7.042],
            [10.791],
            [5.313],
            [7.997],
            [3.1],
        ],
        dtype=np.float32,
    )

    torch_model = torch.nn.Linear(input_size, output_size)
    return x_train, torch_model


@pytest.fixture
def model(build_torch):

    x_train, torch_model = build_torch
    return VetiverModel(
        model=torch_model,
        prototype_data=x_train,
        model_name="torch",
        versioned=None,
        description=None,
        metadata=None,
    )


def test_required_pkgs(model):
    assert isinstance(model.model, torch.nn.Linear)
    assert model.metadata.required_pkgs == ["torch"]


def test_torch_predict_ptype(client: TestClient):
    torch.manual_seed(3)

    data = [{"0": 3.3}]
    response = predict(endpoint="/predict/", data=data, test_client=client)

    assert len(response) == 1, len(response)
    assert isinstance(response, pd.DataFrame)
    assert response.iloc[0, 0] == [-4.060722351074219], response.iloc[0, 0]


def test_torch_predict_ptype_batch(client: TestClient):

    data = [{"0": 3.3}, {"0": 3.3}]
    response = predict(endpoint="/predict/", data=data, test_client=client)

    assert len(response) == 2, len(response)
    assert isinstance(response, pd.DataFrame)
    assert response.iloc[0, 0] == [-4.060722351074219], response.iloc[0, 0]


def test_torch_predict_ptype_error(client: TestClient):

    data = {"0": "bad"}

    with pytest.raises(TypeError):
        predict(endpoint="/predict/", data=data, test_client=client)


def test_torch_predict_no_ptype_batch(client_no_prototype: TestClient):
    torch.manual_seed(3)

    data = [[3.3], [3.3]]
    response = predict(endpoint="/predict/", data=data, test_client=client_no_prototype)

    assert len(response) == 2, len(response)
    assert isinstance(response, pd.DataFrame)
    assert response.iloc[0, 0] == [-4.060722351074219], response.iloc[0, 0]


def test_torch_predict_no_ptype(client_no_prototype: TestClient):
    torch.manual_seed(3)

    data = [[3.3]]
    response = predict(endpoint="/predict/", data=data, test_client=client_no_prototype)

    assert len(response) == 1, len(response)
    assert isinstance(response, pd.DataFrame)
    assert response.iloc[0, 0] == [-4.060722351074219], response.iloc[0, 0]
