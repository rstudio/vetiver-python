from importlib_resources import files as _files
import shutil
from pathlib import Path


def model_card(path="."):
    """
    Create a model card for documentation

    This model card template is generated as a Quarto document.
    Visit [the Quarto website](https://quarto.org/) for more info.

    Parameters
    ----------
    path : str
        Path to save model card

    Examples
    --------

    ```{python}
    import vetiver
    vetiver.model_card()
    ```
    """
    src_path = _files("vetiver") / "templates/model_card.qmd"

    return shutil.copy(src=src_path, dst=path)


def monitoring_dashboard(path: str = "."):
    """
    Generate a monitoring dashboard template

    This template is generated as a Quarto document.
    Visit [the Quarto website](https://quarto.org/) for more info.

    Parameters
    ----------
    path : str
        Path to save monitoring dashboard

    Examples
    --------

    ```{python}
    import vetiver
    vetiver.monitoring_dashboard()
    ```
    """
    p = Path(path)
    src_path = p / _files("vetiver") / "templates" / "monitoring_dashboard.qmd"

    return shutil.copy(src=src_path, dst=path)
