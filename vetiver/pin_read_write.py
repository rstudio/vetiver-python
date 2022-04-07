import pins
from torch import true_divide
from .vetiver_model import VetiverModel
from .meta import vetiver_meta

def vetiver_pin_write(board, model: VetiverModel):
<<<<<<< HEAD
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
=======
    # option if saving pieces of model
    # pins.pin_write(
    #     board = board,
    #     x = list(model = VetiverModel.model,
    #             required_pkgs = VetiverModel.metadata.get("required_pkgs")
    #     ),
    #     name = VetiverModel.model_name,
    #     type = "joblib",
    #     description = VetiverModel.description,
    #     title = ""

    # )
    board = pins.board_local(board)
    board.pin_write(model, name=model.model_name, title="", type="joblib")
>>>>>>> 361d192 (use pins read/write)

    # """Create a Model Card for your published model.
    # Model Cards provide a framework for transparent, responsible reporting.
    # Use the vetiver `.Rmd` template as a place to start."""


<<<<<<< HEAD
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
=======
def vetiver_pin_read(board, name):

    board = pins.board_folder(board)
    board.pin_read(repr(name))

    # vetivermodel can be read directly if saved as joblib? maybe recreate?
#     v = VetiverModel(model = board.pin_read(name),
#         model_name = name,
#         description = board.pin_meta(name).description,
#         metadata = vetiver_meta(user = board.pin_meta(name).user,
#              version = board.pin_meta(name).pin_hash,
# #             url = board.pin_meta(name)url, # currently not in pin_meta
# #             required_pkgs = # come from pin? or elsewhere
#              ),
# #        ptype = , #depends on if joblib or not
#         versioned = True
#         )
>>>>>>> 361d192 (use pins read/write)
