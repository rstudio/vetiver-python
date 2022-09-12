import logging
from importlib_resources import files as _files
import shutil

_log = logging.getLogger(__name__)


def model_card(path="."):
    """Create a model card for documentation

    Parameters
    ----------
    path : str
       Path to save model card
    """
    src_path = _files("vetiver") / "templates/model_card.qmd"

    logging.info("Writing model card template:")

    return shutil.copy(src=src_path, dst=path)
