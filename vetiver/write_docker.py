from vetiver.server import VetiverAPI
import sys

def vetiver_write_docker(app_file = "app.py",
    path = ".",
    rspm_env = True,
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
