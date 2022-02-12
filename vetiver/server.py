from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
import uvicorn
import joblib
from typing import List, Optional
from logging import warn
import requests
import numpy as np
import pandas as pd

from vetiver.vetiver_model import VetiverModel
from vetiver.utils import _jupyter_nb


class VetiverAPI(FastAPI):

    app = None

    def __init__(
        self,
        model: VetiverModel,
        check_ptype: bool = True,
        port: Optional[int] = 8000,
        host="127.0.0.1",
    ) -> None:
        self.model = model
        self.port = port
        self.host = host
        self.check_ptype = check_ptype
        self.app = self._init_app()

    def _init_app(self):

        ptype = self.model.ptype
        served_model = _prepare_model(self.model.model)

        app = FastAPI()

        @app.get("/", response_class=HTMLResponse, include_in_schema=False)
        def docs_redirect():
            return RedirectResponse("/rapidoc")

        @app.get("/ping", include_in_schema=False)
        def ping():
            return {"ping": "pong"}

        @app.get("/rapidoc", response_class=HTMLResponse, include_in_schema=False)
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
            async def prediction(input_data: ptype):

                served_data = _prepare_data(input_data)

                y = served_model.predict([served_data])

                return {"prediction": y[0]}

        else:

            @app.post("/predict/")
            async def prediction(input_data):

                input_data = input_data.split(" ")  # user delimiter ?
                input_data = np.asarray(input_data)
                reshape_data = input_data.reshape(1, -1)
                y = served_model.predict(reshape_data)

                return {"prediction": y[0]}

        return app

    def vetiver_post(self, endpoint_fx, endpoint_name):
        if self.check_ptype == True:

            @self.app.post("/" + endpoint_name + "/")
            def custom_endpoint(input_data: self.model.ptype):
                served_data = _prepare_data(input_data)
                new = endpoint_fx(pd.Series(served_data))
                return new

        else:

            @self.app.post("/" + endpoint_name + "/")
            def custom_endpoint(input_data):
                served_data = _prepare_data(input_data)
                new = endpoint_fx(served_data)
                return new

    def run(self):
        _jupyter_nb()
        uvicorn.run(self.app, port=self.port, host=self.host)

    def predict(self, data: dict, endpoint):
        response = requests.post(endpoint, json=data)

        return response.json()


def _prepare_model(model):
    joblib.dump(model, "vetiver_model.joblib")  # will eventually go
    load_model = joblib.load("vetiver_model.joblib")
    return load_model


def _prepare_data(pred_data):
    served_data = []
    for key, value in pred_data:
        served_data.append(value)
    return served_data


def vetiver_endpoint(url="http://127.0.0.1:8000/predict"):

    return url
