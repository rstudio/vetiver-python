import pins
import pandas as pd
import warnings


def _choose_version(df: pd.DataFrame):
    """Choose pin version to load

    Args
    ----
    df: pd.DataFrame
        Available pins versions
    """
    if "active" in df.columns:
        version = df.active[0]
    elif "created" in df.columns:
        version_desc = df.sort_values(by="created", ascending=False)
        version = version_desc.version[0]
    else:
        version = df.version.max()
        warnings.warn(
            f"""Pinned vetiver model has no active version and no datetime on versions,
              Do you need to check your pinned model?
              Using version {version}"""
        )
    return version


def _glue_required_pkgs(required_pkgs: list):
    """Generate import statements

    Args
    ----
    required_pkgs: list
        Packages needed to run API
    """
    load_required_pkgs = ""
    if required_pkgs:
        for pkg in required_pkgs:
            load_required_pkgs = load_required_pkgs + f"import {pkg}\n"

    return load_required_pkgs


def vetiver_write_app(board, pin_name: str, version: str = None, file: str = "app.py"):

    warnings.warn(
        "vetiver_write_app will be replaced by write_app in v1.0.0", DeprecationWarning
    )

    return write_app(board=board, pin_name=pin_name, version=version, file=file)


def write_app(
    board, pin_name: str, version: str = None, file: str = "app.py", overwrite=False
):
    """Write VetiverAPI app to a file

    Parameters
    ----------
    board :
        API to be written
    pin_name : string
        Name of pin containing VetiverModel
    version :
        Pins version of VetiverModel
    file :
        Name of file

    Examples
    -------
    >>> import vetiver
    >>> import tempfile
    >>> import pins
    >>> tmp = tempfile.TemporaryDirectory()
    >>> board = pins.board_temp(allow_pickle_read=True)
    >>> X, y = vetiver.get_mock_data()
    >>> model = vetiver.get_mock_model().fit(X, y)
    >>> v = vetiver.VetiverModel(model, "my_model", prototype_data = X)
    >>> vetiver.vetiver_pin_write(board, v)
    >>> vetiver.write_app(board,
    ...     "my_model",
    ...     file = tmp.name + "/app.py")
    """

    if board.versioned:
        if not version:
            version = board.pin_versions(pin_name)
            version = _choose_version(version)
        pin_read = (
            f"v = VetiverModel.from_pin(b, {repr(pin_name)}, version = {repr(version)})"
        )

    else:
        pin_read = f"v = VetiverModel.from_pin(b, {repr(pin_name)})"

    infra_pkgs = ["vetiver", "pins"]

    load_board = pins.board_deparse(board)

    if overwrite:
        f = open(file, "w")
    elif not overwrite:
        f = open(file, "x")

    app = f"""from vetiver import VetiverModel
from dotenv import load_dotenv, find_dotenv
{_glue_required_pkgs(infra_pkgs)}
load_dotenv(find_dotenv())

b = pins.{load_board}
{pin_read}

vetiver_api = vetiver.VetiverAPI(v)
api = vetiver_api.app
"""

    f.write(app)
