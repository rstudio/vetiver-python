from importlib_resources import files as _files

sources = {
    "mtcars": _files("vetiver") / "data/mtcars.csv",
    "chicago": _files("vetiver") / "data/chicago.csv",
}


def __dir__():
    return list(sources)


def __getattr__(k):
    import pandas as pd

    f_path = sources.get(k)

    return pd.read_csv(f_path)
