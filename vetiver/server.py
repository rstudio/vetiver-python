from logging import warn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, ValidationError
import joblib
from joblib import dump
import uvicorn
from typing import List, Optional
import nest_asyncio
import warnings
import numpy as np
import pandas as pd

from vetiver.vetiver_model import VetiverModel

class VetiverApp():
    
    app = None

    def __init__(
        self, 
        model: VetiverModel, 
        check_ptype: bool = True, 
        port: Optional[int]=8000, 
        host = "127.0.0.1"
    ) -> None:
        self.app = _init_app(model, check_ptype)
        self.port = port
        self.host = host

    def run(self):
        if _jupyter_nb() == True:
            warnings.warn(
                "WARNING: Jupyter Notebooks are not considered stable environments for production code")
            nest_asyncio.apply()   
        uvicorn.run(self.app, port=self.port, host=self.host)



def _init_app(vetiver_model, check_ptype):
    model = _prepare_model(vetiver_model.model[0])
    ptype = vetiver_model.ptype[0]

    app = FastAPI()

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
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

    if check_ptype == True:
        @app.post("/predict/")
        async def prediction(input_data: ptype):

            served_data = _prepare_data(input_data)

            y = model.predict([served_data])

            return {"prediction": y[0]}

    else:
        @app.post("/predict/")
        async def prediction(input_data):

            input_data = input_data.split(" ")  # user delimiter ?
            input_data = np.asarray(input_data)
            reshape_data = input_data.reshape(1, -1)
            y = model.predict(reshape_data)

            return {"prediction": y[0]}

    ## add another endpoint?

    return app

def _prepare_model(model):
    joblib.dump(model, "vetiver_model.joblib")  # will eventually go
    load_model = joblib.load("vetiver_model.joblib")
    return load_model


def _jupyter_nb():
    try:
        shell = get_ipython().__class__.__name__
        if shell == "ZMQInteractiveShell":
            return True  # Jupyter notebook
        else:
            return False
    except NameError:
        return False


def _prepare_data(pred_data):

    served_data = []
    for key, value in pred_data:
        served_data.append(value)

    return served_data


def vetiver_endpoint(url="http://127.0.0.1:8000/predict"):

    return url


def vetiver_predict(data):

    if isinstance(data, pd.DataFrame):
        data.to_json(orient="records")
