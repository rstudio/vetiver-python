import pins
import vetiver
import pytest
from tempfile import TemporaryDirectory
from pathlib import Path


@pytest.fixture
def vetiver_model_creation():
    X_df, y = vetiver.get_mock_data()
    model = vetiver.get_mock_model().fit(X_df, y)
    return vetiver.VetiverModel(model, "model")


def test_write_app(vetiver_model_creation):
    with TemporaryDirectory() as tempdir:
        file = Path(tempdir, "app.py")
        model_board = pins.board_folder(path=tempdir, allow_pickle_read=True)
        vetiver.vetiver_pin_write(model_board, vetiver_model_creation)
        vetiver.write_app(model_board, "model", file=file)
        contents = open(file).read()
        version = model_board.pin_versions("model").sort_values(
            by="created", ascending=False
        )
        version = version.version[0]
        assert (
            contents
            == f"""from vetiver import VetiverModel
from dotenv import load_dotenv, find_dotenv
import vetiver
import pins

load_dotenv(find_dotenv())

b = pins.board_folder({repr(tempdir)}, allow_pickle_read=True)
v = VetiverModel.from_pin(b, 'model', version = {repr(version)})

vetiver_api = vetiver.VetiverAPI(v)
api = vetiver_api.app
"""
        )
