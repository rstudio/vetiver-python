from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
import uvicorn
from typing import Callable, List, Optional
from logging import warn
import requests
import numpy as np
import pandas as pd

from .vetiver_model import VetiverModel
from .utils import _jupyter_nb


class VetiverAPI:
    """Create model aware API

    Attributes
    ----------
    model :  VetiverModel
        Model to be deployed in API
    check_ptype : bool
        Determine if data prototype should be enforced
    port :  int
        Port for deployment
    host :
        Host address
    app_factory :
        Type of API to be deployed
    app :
        API that is deployed
    """

    app = None

    def __init__(
        self,
        model: VetiverModel,
        check_ptype: bool = True,
        port: Optional[int] = 8000,
        host="127.0.0.1",
        app_factory=FastAPI,
    ) -> None:
        self.model = model
        self.port = port
        self.host = host
        self.check_ptype = check_ptype
        self.app_factory = app_factory
        self.app = self._init_app()

    def _init_app(self):
        app = self.app_factory()

        @app.get("/")
        async def main_app():
            return {"msg": "root path"}

        # redirect to docs?
        # def docs_redirect():
        #     return RedirectResponse("/rapidoc")

        @app.get("/ping", include_in_schema=False)
        async def ping():
            return {"ping": "pong"}

        @app.get("/rapidoc", response_class=HTMLResponse)
        async def rapidoc():
            return f"""
                <!doctype html>
                <html>
                    <head>
                        <meta charset="utf-8">
                        <script
                            type="module"
                            src="https://unpkg.com/rapidoc@9.1.4/dist/rapidoc-min.js"
                        ></script>
                    </head>
                    <body>
                        <rapi-doc spec-url="{app.openapi_url}"></rapi-doc>
                    </body>
                </html>
            """

        if self.check_ptype == True:

            @app.post("/predict/")
            async def prediction(input_data: self.model.ptype):

                served_data = _prepare_data(input_data)

                y = self.model.handler_predict(served_data)

                return {"prediction": y.tolist()}

        else:

            @app.post("/predict/")
            async def prediction(input_data):

                input_data = input_data.split(" ")  # user delimiter ?
                input_data = np.asarray(input_data)
                reshape_data = input_data.reshape(1, -1)
                y = self.model.handler_predict(reshape_data)

                return {"prediction": y.tolist()}

        return app

    def vetiver_post(
        self, endpoint_fx: Callable, endpoint_name: str = "custom_endpoint"
    ):
        """Create new POST endpoint
        Parameters
        ----------
        endpoint_fx : typing.Callable
            Custom function to be run at endpoint
        endpoint_name : str
            Name of endpoint

        Returns
        -------
        dict
            Key: endpoint_name Value: Output of endpoint_fx, in list format
        """
        if self.check_ptype == True:

            @self.app.post("/" + endpoint_name + "/")
            async def custom_endpoint(input_data: self.model.ptype):
                served_data = _prepare_data(input_data)
                new = endpoint_fx(pd.Series(served_data))

                return {endpoint_name: new.tolist()}

        else:

            @self.app.post("/" + endpoint_name + "/")
            async def custom_endpoint(input_data):
                served_data = _prepare_data(input_data)
                new = endpoint_fx(served_data)

                return {endpoint_name: new.tolist()}

    def run(self):
        """Start API
        """
        _jupyter_nb()
        uvicorn.run(self.app, port=self.port, host=self.host)

def predict(endpoint, data: dict):
    """Make a prediction from model endpoint

    Parameters
    ----------
    endpoint :
        URI path to endpoint
    data : dict
        Name of endpoint

    Returns
    -------
    dict
        Key: endpoint_name Value: Output of endpoint_fx, in list format
    """
    response = requests.post(endpoint, json=data)

    return response.json()


def _prepare_data(pred_data):
    served_data = []
    for key, value in pred_data:
        served_data.append(value)
    return served_data


def vetiver_endpoint(url="http://127.0.0.1:8000/predict"):
    """Wrap url

        Parameters
        ----------
        url : str
            URI path to endpoint

        Returns
        -------
        url : str
            URI path to endpoint
     """
    return url
