import tempfile
import typing
from rsconnect.actions import deploy_python_fastapi
import shutil
import os

from .write_fastapi import write_app


def deploy_rsconnect(
    connect_server,
    board,
    pin_name: str,
    version: str = None,
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
    """Deploy to RSConnect

    Parameters
    ----------
        connect_server: 
            RSConnect Server
        board: 
            Pins board
        pin_name: str
            Name of pin
        version: str
            Version of pin
        extra_files: typing.List[str]
            Any extra files to include in 
        new:
            Force as a new deploy
        app_id:
            ID of an existing application to deploy new files for.
        title: str
            Optional title for the deploy.
        python: str
            Optional name of a Python executable
        conda_mode: bool
            Use conda to build an environment.yml
        force_generate: bool    
            Force generating "requirements.txt" or "environment.yml"
        log_callback: typing.Callable
            Callback to use to write the log to
        image: str
            Docker image to be specified for off-host execution
    """
    if board.fs.protocol == "rsc":
        raise NotImplementedError()

    if not title:
        title = pin_name + "_vetiver"

    with tempfile.TemporaryDirectory() as temp:
        if extra_files is not None:
            new_files = []
            for file in extra_files:
                filename = os.path.basename(file)
                shutil.copyfile(file, os.path.join(temp, filename))
                new_files = new_files + [os.path.join(temp, filename)]
            extra_files = new_files
                
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
            entry_point="app:api",
            new=new,
            app_id=app_id,
            title=title,
            python=python,
            conda_mode=conda_mode,
            force_generate=force_generate,
            log_callback=log_callback,
            image=image,
        )
