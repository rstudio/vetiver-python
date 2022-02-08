import nest_asyncio
import warnings
from IPython import get_ipython


def _jupyter_nb():
    shell = get_ipython().__class__.__name__

    if shell == "ZMQInteractiveShell":
        warnings.warn(
            "WARNING: Jupyter Notebooks are not considered stable environments for production code"
        )
        nest_asyncio.apply()
    else:
        return False
