from tempfile import tempdir
import rsconnect
import typing

from .write_fastapi import write_app

def deploy_rsconnect(
    connect_server,
    board,
    pin_name,
    version,
    directory: str,
    extra_files: typing.List[str],
    excludes: typing.List[str],
    entry_point: str,
    new: bool,
    app_id: int,
    title: str,
    python: str,
    conda_mode: bool,
    force_generate: bool,
    log_callback: typing.Callable,
    image: str = None,
):
    tmp = tempdir()

    write_app(board = board, pin_name = pin_name, version = version, file = tmp+"app.py", overwrite = False)

    rsconnect.actions.deploy_python_fastapi(
        connect_server = connect_server,
        directory = directory,
        extra_files = extra_files,
        excludes = excludes,
        entry_point = entry_point,
        new = new,
        app_id = app_id,
        title = title,
        python = python,
        conda_mode = conda_mode,
        force_generate = force_generate,
        log_callback = log_callback,
        image = image,
     )