import os

import numpy as np
import pandas as pd
import pytest
import sklearn

import pins
from pins.boards import BoardRsConnect
from pins.rsconnect.api import RsConnectApi
from pins.rsconnect.fs import RsConnectFs
from rsconnect.api import RSConnectClient, RSConnectServer

import vetiver

RSC_SERVER_URL = os.environ.get("CONNECT_SERVER")
RSC_API_KEY = os.environ.get("CONNECT_API_KEY")

pytestmark = pytest.mark.rsc_test  # noqa


def _require_connect():
    if not RSC_SERVER_URL or not RSC_API_KEY:
        pytest.skip("CONNECT_SERVER and CONNECT_API_KEY must be set (run via with-connect)")


def _api():
    return RsConnectApi(RSC_SERVER_URL, RSC_API_KEY)


def rsc_delete_user_content(rsc):
    guid = rsc.get_user()["guid"]
    content = rsc.get_content(owner_guid=guid)
    for entry in content:
        rsc.delete_content_item(entry["guid"])


@pytest.fixture(scope="function")
def username():
    _require_connect()
    return _api().get_user()["username"]


@pytest.fixture(scope="function")
def rsc_admin():
    # tears down content after each test
    _require_connect()
    fs = RsConnectFs(_api())
    rsc_delete_user_content(fs.api)
    yield BoardRsConnect("", fs, allow_pickle_read=True)
    rsc_delete_user_content(fs.api)


def test_deploy(rsc_admin, username):
    np.random.seed(500)

    # Load data, model
    X_df, y = vetiver.mock.get_mock_data()
    model = vetiver.mock.get_mock_model().fit(X_df, y)

    pin_name = f"{username}/model"
    v = vetiver.VetiverModel(model=model, prototype_data=X_df, model_name=pin_name)

    board = pins.board_connect(
        server_url=RSC_SERVER_URL, api_key=RSC_API_KEY, allow_pickle_read=True
    )

    vetiver.vetiver_pin_write(board=board, model=v)
    connect_server = RSConnectServer(url=RSC_SERVER_URL, api_key=RSC_API_KEY)
    assert isinstance(board.pin_read(pin_name), sklearn.dummy.DummyRegressor)

    vetiver.deploy_connect(
        connect_server=connect_server,
        board=board,
        pin_name=pin_name,
        title="testapi",
        extra_files=["requirements.txt"],
        new=True,
    )

    # get url of where content lives
    client = RSConnectClient(connect_server)
    dicts = client.content_list()
    rsc_api = list(filter(lambda x: x["title"] == "testapi", dicts))
    content_url = rsc_api[0].get("content_url").rstrip("/")

    h = {"Authorization": f"Key {RSC_API_KEY}"}

    endpoint = vetiver.vetiver_endpoint(content_url + "/predict")
    response = vetiver.predict(endpoint, X_df, headers=h)

    assert isinstance(response, pd.DataFrame), response
    assert response.iloc[0, 0] == 44.47
    assert len(response) == 100
