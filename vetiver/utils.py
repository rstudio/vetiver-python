import nest_asyncio
import warnings
import sys
from types import SimpleNamespace

no_notebook = False
try:
    from IPython import get_ipython  # noqa
except ImportError:
    no_notebook = True


def _jupyter_nb():

    if not no_notebook:
        warnings.warn(
            "WARNING: Jupyter Notebooks are not considered stable environments "
            "for production code"
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
