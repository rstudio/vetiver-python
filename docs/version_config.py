from importlib_metadata import version as _version

v = f"""VERSION={_version('vetiver')}"""

f = open("_environment", "w")
f.write(v)
