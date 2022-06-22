import pins
import warnings
import json

from .vetiver_model import VetiverModel
from .meta import _model_meta
from .write_fastapi import _choose_version

def vetiver_pin_write(board, model: VetiverModel, versioned: bool=True):
    """
    Pin a trained VetiverModel along with other model metadata.
    
    Parameters
    ----------
    board:
        A pin board, created by `pins.board_folder()` or another `board_` function.
    model: vetiver.VetiverModel
        VetiverModel to be written to board
    versioned: bool
        Whether or not the pin should be versioned
    """
    if not board.allow_pickle_read:
        raise NotImplementedError # must be pickle-able

    board.pin_write(
        model.model,
        name = model.model_name,
        type = "joblib",
        description = model.description,
        metadata = {"required_pkgs": model.metadata.get("required_pkgs"),
                    "ptype": None if model.ptype == None else model.ptype().json()},
        versioned=versioned
    )

    # to do: Model card

    # message = """
    # Create a Model Card for your published model.
    # Model Cards provide a framework for transparent, responsible reporting.
    # Use the vetiver `.Rmd` template as a place to start."""

    # warnings.warn(message=message)


def vetiver_pin_read(board, name: str, version: str = None) -> VetiverModel:
    """
    Read pin and populate VetiverModel
    
    Parameters
    ----------
    board:
        A pin board, created by `pins.board_folder()` or another `board_` function.
    name: string
        Pin name
    version: str
        Retrieve a specific version of a pin. 

    Returns
    --------
    vetiver.VetiverModel

    Notes
    -----
    If reading a board from RSConnect, the `board` argument must be in "username/modelname" format.
    
    """

    raise DeprecationWarning("vetiver_pin_read is now a classmethod VetiverModel.from_pin()")

    version = version if version is not None else _choose_version(board.pin_versions(name))

    model = board.pin_read(name, version)
    meta = board.pin_meta(name)

    v = VetiverModel(model = model,
        model_name = name,
        description = meta.description,
        metadata = _model_meta(user = meta.user,
             version = version,
             url = meta.user.get("url"), # None all the time, besides Connect
             required_pkgs = meta.user.get("required_pkgs")
        ),
        ptype_data = json.loads(meta.user.get("ptype")) if meta.user.get("ptype") else None,
        versioned = True
        )
    
    return v
