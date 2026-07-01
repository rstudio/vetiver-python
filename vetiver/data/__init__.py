__all__ = [
    "mtcars",
    "chicago",
    "sacramento",
]


def __dir__():
    return __all__


def _load_data_csv(name):
    import pandas as pd
    from importlib.resources import files

    fname = files("vetiver.data").joinpath(f"{name}.csv")
    with fname.open("rb") as f:
        return pd.read_csv(f)


def __getattr__(name):
    if name not in __all__:
        raise AttributeError(f"No dataset named: {name}")

    return _load_data_csv(name)
