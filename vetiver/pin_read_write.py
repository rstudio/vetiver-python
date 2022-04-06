import pins
from .vetiver_model import VetiverModel
from .meta import vetiver_meta

def vetiver_pin_write(board, model: VetiverModel):
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
        title = "",
        metadata = {"required_pkgs": model.metadata.get("required_pkgs"),
                    "ptype": None if model.ptype == None else model.ptype().json()}
    )
    #return(print("create a model card for your published model"))

    # """Create a Model Card for your published model.
    # Model Cards provide a framework for transparent, responsible reporting.
    # Use the vetiver `.Rmd` template as a place to start."""


def vetiver_pin_read(board, name) -> VetiverModel:

    model = board.pin_read(repr(name))
    meta = board.pin_meta(repr(name))

    v = VetiverModel(model = model,
        model_name = name,
        description = board.pin_meta(repr(name)).description,
        metadata = vetiver_meta(user = meta.user,
             version = meta.pin_hash,
#             url = board.pin_meta(name)url, # currently not in pin_meta
             required_pkgs = meta.user.get("required_pkgs")
        ),
        ptype = meta.user.get("ptype"), #depends on if joblib or not
        versioned = True
        )
    
    return v
