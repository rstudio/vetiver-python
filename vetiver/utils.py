import nest_asyncio
import warnings

no_notebook = False
try:
    from IPython import get_ipython
except ImportError:
    no_notebook = True


def _jupyter_nb():

    if not no_notebook:
        warnings.warn(
            "WARNING: Jupyter Notebooks are not considered stable environments for production code"
        )
        nest_asyncio.apply()
    else:
        return False
