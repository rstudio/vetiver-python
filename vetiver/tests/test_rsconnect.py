import pytest
import json
import sklearn
import pins
import pandas as pd
import numpy as np

from pins.boards import BoardRsConnect
from pins.rsconnect.api import RsConnectApi
from pins.rsconnect.fs import RsConnectFs
from rsconnect.api import RSConnectServer, RSConnectClient

import vetiver

RSC_SERVER_URL = "http://localhost:3939"
RSC_KEYS_FNAME = "vetiver/tests/rsconnect_api_keys.json"

pytestmark = pytest.mark.rsc_test  # noqa


def get_key(name):
    with open(RSC_KEYS_FNAME) as f:
        api_key = json.load(f)[name]
        return api_key


def rsc_from_key(name):
    with open(RSC_KEYS_FNAME) as f:
        api_key = json.load(f)[name]
        return RsConnectApi(RSC_SERVER_URL, api_key)


def rsc_fs_from_key(name):

    rsc = rsc_from_key(name)

    return RsConnectFs(rsc)


def rsc_delete_user_content(rsc):
    guid = rsc.get_user()["guid"]
    content = rsc.get_content(owner_guid=guid)
    for entry in content:
        rsc.delete_content_item(entry["guid"])


@pytest.fixture(scope="function")
def rsc_short():
    # tears down content after each test
    fs_susan = rsc_fs_from_key("susan")

    # delete any content that might already exist
    rsc_delete_user_content(fs_susan.api)

    yield BoardRsConnect(
        "", fs_susan, allow_pickle_read=True
    )  # fs_susan.ls to list content

    rsc_delete_user_content(fs_susan.api)


def test_deploy(rsc_short):
    np.random.seed(500)

    # Load data, model
    X_df, y = vetiver.mock.get_mock_data()
    model = vetiver.mock.get_mock_model().fit(X_df, y)

    v = vetiver.VetiverModel(model=model, prototype_data=X_df, model_name="susan/model")

    board = pins.board_rsconnect(
        server_url=RSC_SERVER_URL, api_key=get_key("susan"), allow_pickle_read=True
    )

    vetiver.vetiver_pin_write(board=board, model=v)
    connect_server = RSConnectServer(url=RSC_SERVER_URL, api_key=get_key("susan"))
    assert isinstance(board.pin_read("susan/model"), sklearn.dummy.DummyRegressor)

    vetiver.deploy_rsconnect(
        connect_server=connect_server,
        board=board,
        pin_name="susan/model",
        title="testapi",
        extra_files=["requirements.txt"],
    )

    # get url of where content lives
    client = RSConnectClient(connect_server)
    dicts = client.content_search()
    rsc_api = list(filter(lambda x: x["title"] == "testapi", dicts))
    content_url = rsc_api[0].get("content_url")

    h = {"Authorization": f'Key {get_key("susan")}'}

    endpoint = vetiver.vetiver_endpoint(content_url + "/predict")
    response = vetiver.predict(endpoint, X_df, headers=h)

    assert isinstance(response, pd.DataFrame), response
    assert response.iloc[0, 0] == 44.47
    assert len(response) == 100
