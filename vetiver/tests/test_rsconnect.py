import pytest
import json
import sklearn
import pins
import rsconnect
import pandas as pd
from pins.boards import BoardRsConnect
from pins.rsconnect.api import RsConnectApi
from pins.rsconnect.fs import RsConnectFs
from rsconnect.api import RSConnectServer, RSConnectClient

import vetiver

# Load data, model
X_df, y = vetiver.mock.get_mock_data()
model = vetiver.mock.get_mock_model().fit(X_df, y)

RSC_SERVER_URL = "http://localhost:3939"
RSC_KEYS_FNAME = "vetiver/tests/rsconnect_api_keys.json"

pytestmark = pytest.mark.rsc_test  # noqa


def server_from_key(name):
    with open(RSC_KEYS_FNAME) as f:
        api_key = json.load(f)[name]
        return RSConnectServer(RSC_SERVER_URL, api_key)


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


def test_board_pin_write(rsc_short):
    v = vetiver.VetiverModel(
        model=model, ptype_data=X_df, model_name="susan/model", versioned=None
    )
    vetiver.vetiver_pin_write(board=rsc_short, model=v)
    assert isinstance(rsc_short.pin_read("susan/model"), sklearn.dummy.DummyRegressor)


def test_deploy(rsc_short):
    v = vetiver.VetiverModel(
        model=model, ptype_data=X_df, model_name="susan/model", versioned=None
    )
    board = pins.board_rsconnect(
        server_url=RSC_SERVER_URL, api_key=get_key("susan"), allow_pickle_read=True
    )

    vetiver.vetiver_pin_write(board=board, model=v)
    connect_server = RSConnectServer(url=RSC_SERVER_URL, api_key=get_key("susan"))
    assert isinstance(board.pin_read("susan/model"), sklearn.dummy.DummyRegressor)

    # vetiver.deploy_rsconnect(
    #     connect_server=connect_server, board=board, pin_name="susan/model"
    # )

    vetiver.write_app(board, "susan/model")
    vetiver.load_pkgs(v)
    rsconnect.actions.deploy_python_fastapi(
        connect_server=connect_server,
        directory=".",
        extra_files=None,
        excludes=None,
        entry_point="app:api",
        new=True,
        app_id=None,
        title="testapi",
        python=None,
        conda_mode=False,
        force_generate=False,
        log_callback=None,
    )

    client = RSConnectClient(connect_server)
    dicts = client.content_search()
    rsc_api = list(filter(lambda x: x["title"] == "testapi", dicts))
    content_url = rsc_api[0].get("content_url")

    h = {"Authorization": f'Key {get_key("susan")}'}

    endpoint = vetiver.vetiver_endpoint(content_url + "/predict")
    response = vetiver.predict(endpoint, X_df, headers=h)

    assert isinstance(response, pd.DataFrame), response
    assert type(response.iloc[0, 0]) == float
    assert len(response) == 100
