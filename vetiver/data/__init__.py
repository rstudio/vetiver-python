__all__ = [
    "mtcars",
    "chicago",
    "sacramento",
]


def __dir__():
    return __all__


def _load_data_csv(name):
    import pandas as pd
    import pkg_resources

    fname = pkg_resources.resource_filename("vetiver.data", f"{name}.csv")
    return pd.read_csv(fname)


def __getattr__(name):
    if name not in __all__:
        raise AttributeError(f"No dataset named: {name}")

    return _load_data_csv(name)
