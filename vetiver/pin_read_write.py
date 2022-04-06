import pins
from .vetiver_model import VetiverModel
from .meta import vetiver_meta

def vetiver_pin_write(board, VetiverModel: VetiverModel):
    pins.pin_write(
        board = board,
        x = list(model = VetiverModel.model,
                    ptype = VetiverModel.ptype,
                    required_pkgs = VetiverModel.metadata.required_pkgs),
        name = VetiverModel.model,
        type = "joblib",
        description = VetiverModel.description,
        metadata = VetiverModel.metadata.user,
        versioned = VetiverModel.versioned
        )

    print("Create a Model Card for your published model.")
    print("Model Cards provide a framework for transparent, responsible reporting.")
    print("Use the vetiver `.Rmd` template as a place to start.")


def vetiver_pin_read(board, name, version = None):

    board = pins.board_folder()
    pinned = pins.pin_read(board = board, name = name, version = version)
    meta = pins.pin_meta(board = board, name = name, version = version)

    # vetivermodel can be read directly if saved as joblib? do we need to recreate?

    v = VetiverModel(model = pinned.model,
        model_name = name,
        description = meta.description,
        metadata = vetiver_meta(user = meta.user,
             version = meta$local$version,
             url = meta$local$url,
             required_pkgs = pinned$required_pkgs
             ),
        ptype = pinned,
        versioned = pinned.version
        )
