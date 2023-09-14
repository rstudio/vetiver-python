import nest_asyncio
import warnings
import sys
import os
import subprocess
from types import SimpleNamespace

no_notebook = False
try:
    from IPython import get_ipython  # noqa
except ImportError:
    no_notebook = True


def _jupyter_nb():

    if not no_notebook:
        warnings.warn(
            "You may be running from a notebook environment. Jupyter Notebooks are "
            "not considered stable environments for production code"
        )
        nest_asyncio.apply()
    else:
        return False


modelcard_options = SimpleNamespace(quiet=False)


def inform(log, msg):
    if log is not None:
        log.info(msg)

    if not modelcard_options.quiet:
        print(msg, file=sys.stderr)


def get_workbench_path(port):
    # check to see if in Posit Workbench, pulled from FastAPI section of user guide
    # https://docs.posit.co/ide/server-pro/user/vs-code/guide/proxying-web-servers.html#running-fastapi-with-uvicorn # noqa

    if "RS_SERVER_URL" in os.environ and os.environ["RS_SERVER_URL"]:
        path = (
            subprocess.run(
                f"echo $(/usr/lib/rstudio-server/bin/rserver-url -l {port})",
                stdout=subprocess.PIPE,
                shell=True,
            )
            .stdout.decode()
            .strip()
        )
        # subprocess is run, new URL given
        return path
    else:
        return None
