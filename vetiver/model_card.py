from importlib_resources import files as _files
import shutil


def model_card(path="."):
    """Create a model card for documentation

    Parameters
    ----------
    path : str
       Path to save model card
    """
    src_path = _files("vetiver") / "templates/model_card.qmd"

    return shutil.copy(src=src_path, dst=path)
