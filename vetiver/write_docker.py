from vetiver.server import VetiverAPI
import sys

def vetiver_write_docker(app_file = "app.py",
    path = ".",
    rspm_env = True,
    host = "0.0.0.0",
    port = "80"):

    py_version = str(sys.version_info.major) + "." + str(sys.version_info.minor)

    if rspm_env:
        pass
    else:
        pass
    docker_pkgs = ["fastapi", "vetiver"]

    # pkgs = unique()

    docker_script = f"""
# #
# FROM python:{py_version}

# #
# WORKDIR /code


# #
# RUN pip freeze > /code/requirements.txt
# RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# #
# COPY . /code/app

# #
# CMD ["uvicorn", "app.app:api", "--host", {repr(host)}, "--port", {repr(port)}]
    """

    f = open("Dockerfile", "x")
    f.write(docker_script)
