import pytest
import vetiver
import pins
from pathlib import Path
from tempfile import TemporaryDirectory
import pandas as pd
import numpy as np

DOCKER_URL = "http://0.0.0.0:8080/predict"

# uses GitHub Actions to deploy model into Docker
# see vetiver-python/script/setup-docker for files


@pytest.mark.docker
def test_deployed_dockerfile():
    np.random.seed(500)

    X, y = vetiver.mock.get_mock_data()
    response = vetiver.predict(endpoint=DOCKER_URL, data=X)

    assert isinstance(response, pd.DataFrame), response
    assert response.iloc[0, 0] == 44.47
    assert len(response) == 100


@pytest.fixture()
def create_vetiver_model():
    X, y = vetiver.get_mock_data()
    model = vetiver.get_mock_model()

    return vetiver.VetiverModel(model.fit(X, y), "model", prototype_data=X)


@pytest.fixture(scope="module")
def test_warning_if_no_protocol(create_vetiver_model):
    with pytest.warns(UserWarning):
        board = pins.board_temp(allow_pickle_read=True)
        board.fs.protocol = "abc"

        vetiver.get_board_pkgs(board)


@pytest.mark.parametrize(
    "prot,output",
    [
        (["s3", "s3a"], "s3fs"),
        ("abfs", "adlfs"),
        (("gcs", "gs"), "gcsfs"),
    ],
)
@pytest.fixture(scope="module")
def test_get_board_pkgs(prot, output, create_vetiver_model):
    board = pins.board_temp(allow_pickle_read=True)
    board.fs.protocol = prot

    vetiver.vetiver_pin_write(board, create_vetiver_model)

    with TemporaryDirectory() as tempdir:
        vetiver.prepare_docker(board, "model", path=tempdir)
        file = Path(tempdir, "vetiver_requirements.txt")
        contents = open(file).read()
        assert f"{output}==" in contents
