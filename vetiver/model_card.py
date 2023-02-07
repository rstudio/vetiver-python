from importlib_resources import files as _files
import shutil


def model_card(path="."):
    """
    Create a model card for documentation

    Parameters
    ----------
    path : str
        Path to save model card

    Notes
    -----
    This model card is generated as a Quarto document. For more info on
    Quarto, visit https://quarto.org/
    """
    src_path = _files("vetiver") / "templates/model_card.qmd"

    return shutil.copy(src=src_path, dst=path)
