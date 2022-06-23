import pytest
import json
from pins.rsconnect.fs import RsConnectFs
from pins.boards import BoardRsConnect

RSC_SERVER_URL = "http://localhost:3939"
RSC_KEYS_FNAME = "vetiver/tests/rsconnect_api_keys.json"

pytestmark = pytest.mark.rsc_test  # noqa

def rsc_from_key(name):
    from pins.rsconnect.api import RsConnectApi

    with open(RSC_KEYS_FNAME) as f:
        api_key = json.load(f)[name]
        return RsConnectApi(RSC_SERVER_URL, api_key)

def rsc_fs_from_key(name):
    from pins.rsconnect.fs import RsConnectFs

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

    yield BoardRsConnect("", fs_susan, allow_pickle_read=True) #fs_susan.ls to list content

    rsc_delete_user_content(fs_susan.api)

from vetiver import VetiverModel, vetiver_pin_write, mock
import sklearn
# Load data, model
X_df, y = mock.get_mock_data()
model = mock.get_mock_model().fit(X_df, y)

def test_board_pin_write(rsc_short):
    v = VetiverModel(model=model, ptype_data=X_df,
        model_name="susan/model", versioned=None)
    vetiver_pin_write(board=rsc_short, model=v)
    assert isinstance(rsc_short.pin_read("susan/model"), sklearn.dummy.DummyRegressor)
