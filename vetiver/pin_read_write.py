import pins
from torch import true_divide
from .vetiver_model import VetiverModel
from .meta import vetiver_meta

def vetiver_pin_write(board, model: VetiverModel):
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

    # """Create a Model Card for your published model.
    # Model Cards provide a framework for transparent, responsible reporting.
    # Use the vetiver `.Rmd` template as a place to start."""


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
