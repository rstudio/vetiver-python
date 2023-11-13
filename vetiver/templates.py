from importlib_resources import files as _files
import shutil
from pathlib import Path


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


def monitoring_dashboard(path: str = "."):
    """
    Generate a monitoring dashboard template

    Parameters
    ----------
    path : str
        Path to save monitoring dashboard

    Notes
    -----
    This model card is generated as a Quarto document. For more info on
    Quarto, visit https://quarto.org/
    """
    p = Path(path)
    src_path = p / _files("vetiver") / "templates" / "monitoring_dashboard.qmd"

    return shutil.copy(src=src_path, dst=path)
