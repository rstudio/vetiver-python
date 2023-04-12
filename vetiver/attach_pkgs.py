from __future__ import annotations
import typing

import tempfile
import os
import warnings
from .vetiver_model import VetiverModel
from .meta import VetiverMeta

if typing.TYPE_CHECKING:
    from typing import Optional
    from pathlib import Path


def load_pkgs(
    model: VetiverModel, packages: Optional[list] = None, path: str | Path = ""
):
    """Load packages necessary for predictions

    Parameters
    ----------
    model: VetiverModel
        VetiverModel to extract packages from
    packages: list
        List of extra packages to include
    path: str
        Where to save output file
    """

    required_pkgs = ["vetiver"]
    if packages:
        required_pkgs += packages

    if isinstance(model.metadata, dict):
        model.metadata = VetiverMeta.from_dict(model.metadata)

    if model.metadata.required_pkgs:
        required_pkgs += model.metadata.required_pkgs

    tmp = tempfile.NamedTemporaryFile(suffix=".in", delete=False)
    tmp.close()

    with open(tmp.name, "a") as f:
        for package in required_pkgs:
            f.write(package + "\n")

    os.system(f"pip-compile {tmp.name} --output-file={path}requirements.txt")
    os.remove(tmp.name)


def get_board_pkgs(board) -> list[str]:
    """
    Extract packages required for pin board authorization

    Parameters
    ----------
    board:
        A pin board, created by `pins.board_folder()` or another `board_` function.

    Returns
    --------
    list[str]
    """
    prot = board.fs.protocol

    if prot == "rsc":
        return ["rsconnect-python"]
    elif prot == "file":
        return []
    elif prot == ["s3", "s3a"]:
        return ["s3fs"]
    elif prot == "abfs":
        return ["adlfs"]
    elif prot == ("gcs", "gs"):
        return ["gcsfs"]
    else:
        warnings.warn(
            f"required packages unknown for board protocol: {prot}, "
            "add to model's metadata to export",
            UserWarning,
        )
        return []
