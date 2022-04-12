import numpy as np
import tempfile
import os
from vetiver import VetiverModel

def load_pkgs(model: VetiverModel = None, packages: list = None, path=""):
    """_summary_

    Args
    ----
        model (VetiverModel, optional):
            VetiverModel to extract packages from. Defaults to None.
        packages (list, optional): 
            List of extra packages to include. Defaults to None.
        path (str, optional): 
            Where to save output file. Defaults to ".".
    """

    required_pkgs = ["fastapi", "vetiver", "pins"]
    if packages:
        required_pkgs = list(set(required_pkgs + packages))
    if model.metadata.get("required_pkgs"):
        required_pkgs = list(set(required_pkgs + model.metadata.get("required_pkgs")))


    tmp = tempfile.NamedTemporaryFile(suffix='.in')

    with open(tmp.name, 'a') as f:
        for package in required_pkgs:
            f.write(package + '\n')

    os.system(f"pip-compile {f.name} --output-file={path}vetiver_requirements.txt")
