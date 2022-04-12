from vetiver.server import VetiverAPI
import sys

def vetiver_write_docker(app_file = "app.py",
    path = ".",
    rspm_env = True,
<<<<<<< HEAD
<<<<<<< HEAD
    host = "0.0.0.0",
    port = "80"):

    py_version = str(sys.version_info.major) + "." + str(sys.version_info.minor)

    # what is python value add for RSPM?

    # if rspm_env:
    #     pass
    # else:
    #     pass

    docker_script = f"""# #
FROM python:{py_version}

# #
WORKDIR /code

# #
COPY vetiver_requirements.txt /code/requirements.txt

# #
RUN pip install --no-cache-dir --upgrade -r /code/vetiver_requirements.txt

# #
COPY . /code/app

# #
CMD ["uvicorn", "app.app:api", "--host", "{host}", "--port", "{port}"]
    """

    f = open("Dockerfile", "x")
    f.write(docker_script)
=======
    host = 0.0.0.0,
    port = 80):
=======
    host = "0.0.0.0",
    port = "80"):
>>>>>>> 9979f1c (handle loading requirements for docker)

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
<<<<<<< HEAD
>>>>>>> b14210f (scaffolding to write docker)
=======

    f = open("Dockerfile", "x")
    f.write(docker_script)
>>>>>>> 9979f1c (handle loading requirements for docker)