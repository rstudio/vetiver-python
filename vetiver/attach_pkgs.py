import tempfile
import os
from vetiver import VetiverModel


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
    if model.metadata.get("required_pkgs"):
        required_pkgs = list(set(required_pkgs + model.metadata.get("required_pkgs")))

    tmp = tempfile.NamedTemporaryFile(suffix=".in")

    with open(tmp.name, "a") as f:
        for package in required_pkgs:
            f.write(package + "\n")

    os.system(f"pip-compile {f.name} --output-file={path}vetiver_requirements.txt")
