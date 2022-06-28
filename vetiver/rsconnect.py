import tempfile
from rsconnect.actions import deploy_python_fastapi
import typing

from .write_fastapi import write_app


def deploy_rsconnect(
    connect_server,
    board,
    pin_name,
    version = None,
    extra_files: typing.List[str] = None,
    new: bool = False,
    app_id: int = None,
    title: str = None,
    python: str = None,
    conda_mode: bool = False,
    force_generate: bool = False,
    log_callback: typing.Callable = None,
    image: str = None,
):
    with tempfile.TemporaryDirectory() as temp:
        tmp_app = temp + "/app.py"
        write_app(
            board=board,
            pin_name=pin_name,
            version=version,
            file=tmp_app,
            overwrite=False,
        )

        deploy_python_fastapi(
            connect_server=connect_server,
            directory=temp,
            extra_files=extra_files,
            excludes=None,
            entry_point="vetiver_api:api",
            new=new,
            app_id=app_id,
            title=title,
            python=python,
            conda_mode=conda_mode,
            force_generate=force_generate,
            log_callback=log_callback,
            image=image,
        )
