from importlib_resources import files as _files

sources = {
    "mtcars": _files("vetiver") / "data/mtcars.csv",
    "chicago": _files("vetiver") / "data/chicago.csv",
    "sacramento": _files("vetiver") / "data/sacramento.csv",
}


def __dir__():
    return list(sources)


def __getattr__(k):
    import pandas as pd

    f_path = sources.get("mtcars")
    if k == "chicago":
        f_path = sources.get("chicago")
    elif k == "sacramento":
        f_path = sources.get("sacramento")
    return pd.read_csv(f_path)
