"""vetiver - Python parallel to R vetiver package"""
# Change to import.metadata when minimum python>=3.8
from importlib_metadata import version as _version

from .prototype import (  # noqa
    vetiver_create_prototype,  # noqa
    vetiver_create_ptype,  # noqa
    InvalidPTypeError,  # noqa
)  # noqa
from .vetiver_model import VetiverModel  # noqa
from .server import VetiverAPI, vetiver_endpoint, predict  # noqa
from .mock import get_mock_data, get_mock_model  # noqa
from .pin_read_write import vetiver_pin_write  # noqa
from .attach_pkgs import load_pkgs, get_board_pkgs  # noqa
from .meta import VetiverMeta  # noqa
from .write_docker import write_docker, prepare_docker  # noqa
from .write_fastapi import write_app, vetiver_write_app  # noqa
from .handlers.base import BaseHandler, create_handler, InvalidModelError  # noqa
from .handlers.sklearn import SKLearnHandler  # noqa
from .handlers.torch import TorchHandler  # noqa
from .handlers.statsmodels import StatsmodelsHandler  # noqa
from .handlers.xgboost import XGBoostHandler  # noqa
from .handlers.spacy import SpacyHandler  # noqa
from .helpers import api_data_to_frame  # noqa
from .rsconnect import deploy_rsconnect  # noqa
from .monitor import compute_metrics, pin_metrics, plot_metrics, _rolling_df  # noqa
from .templates import model_card, monitoring_dashboard  # noqa
from .types import create_prototype, Prototype  # noqa

__author__ = "Isabel Zimmerman <isabel.zimmerman@posit.co>"
__version__ = _version("vetiver")
del _version
