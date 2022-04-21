from importlib_resources import files as _files

sources = {
    "default_css": _files("vetiver") / "rapidoc/default.min.css",
    "highlight": _files("vetiver") / "rapidoc/highligh.min.js",
    "rapidoc": _files("vetiver") / "rapidoc/rapidoc-min.js",
}


def __dir__():
    return list(sources)


def __getattr__(k):
    f_path = sources.get(k)

    return f_path