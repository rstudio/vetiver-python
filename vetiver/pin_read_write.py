import pins
import warnings

from .vetiver_model import VetiverModel
from .meta import vetiver_meta

def vetiver_pin_write(board, model: VetiverModel, versioned: bool=True):
    """
    Write pin including VetiverModel
    
    Parameters
    ----------
    board: pins.BaseBoard
        location for pin to be saved
    model: vetiver.VetiverModel
        VetiverModel to be written to board
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


def vetiver_pin_read(board: pins.BaseBoard, name: str, version: str = None) -> VetiverModel:

    model = board.pin_read(name, version)
    meta = board.pin_meta(name)

    v = VetiverModel(model = model,
        model_name = name,
        description = meta.description,
        metadata = vetiver_meta(user = meta.user,
             version = version,
             url = meta.user.get("url"), # None all the time, besides Connect
             required_pkgs = meta.user.get("required_pkgs")
        ),
        ptype = meta.user.get("ptype"), #depends on if joblib or not
        versioned = True
        )
    
    return v
