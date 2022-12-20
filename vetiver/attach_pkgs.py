import tempfile
import os
from .vetiver_model import VetiverModel
from .meta import VetiverMeta


def load_pkgs(model: VetiverModel = None, packages: list = None, path=""):
    """Load packages necessary for predictions

    Args
    ----
        model: VetiverModel
            VetiverModel to extract packages from
        packages: list
            List of extra packages to include
        path: str
            Where to save output file
    """

    required_pkgs = ["vetiver"]
    if packages:
        required_pkgs = list(set(required_pkgs + packages))

    if isinstance(model.metadata, dict):
        model.metadata = VetiverMeta.from_dict(model.metadata)

    if model.metadata.required_pkgs:
        required_pkgs = list(set(required_pkgs + model.metadata.required_pkgs))

    tmp = tempfile.NamedTemporaryFile(suffix=".in", delete=False)
    tmp.close()

    with open(tmp.name, "a") as f:
        for package in required_pkgs:
            f.write(package + "\n")

    os.system(f"pip-compile {tmp.name} --output-file={path}requirements.txt")
    os.remove(tmp.name)
