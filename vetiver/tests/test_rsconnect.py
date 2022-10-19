import pytest
import json
import sklearn
import pins
from pins.boards import BoardRsConnect
from pins.rsconnect.api import RsConnectApi
from pins.rsconnect.fs import RsConnectFs
from rsconnect.api import RSConnectServer
from rsconnect.actions import gather_server_details

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


def test_python_env(rsc_short):
    connect_server = RSConnectServer(url=RSC_SERVER_URL, api_key=get_key("susan"))

    server_details = gather_server_details(connect_server)

    assert server_details.get("python").get("versions") == ["3.8.10", "3.9.5"]


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
    #     connect_server=connect_server,
    #     board=board,
    #     pin_name="susan/model"
    # )
    import rsconnect

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
        title=None,
        python=None,
        conda_mode=False,
        force_generate=False,
        log_callback=None,
    )

    response = vetiver.predict(RSC_SERVER_URL + "/predict", X_df)
    assert response.status_code == 200, response.text
    assert response.json() == {"prediction": [44.47, 44.47]}, response.json()
