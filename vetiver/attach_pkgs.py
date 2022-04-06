import tempfile
import os

def load_pkgs(packages: list):

    tmp = tempfile.NamedTemporaryFile(suffix='.in')

    with open(repr(tmp), 'a') as f:
        for package in packages:
            f.write(package + '\n')

    os.system(f"pip-compile {repr(f.name)} --output-file=vetiver_req.txt")
