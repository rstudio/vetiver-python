from logging import warn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, ValidationError
import joblib
from joblib import dump
import uvicorn
import sklearn
from typing import List
import nest_asyncio
import warnings
import numpy as np
from vetiver import VetiverModel

# do we want to convert to joblib?
# get pinned somewhere, then joblib load on the pin
def _prepare_model(model):
    dump(model, 'vetiver_model.joblib') # will eventually go
    load_model = joblib.load("vetiver_model.joblib")
    return(load_model)


def _jupyter_nb():
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True # Jupyter notebook
        else:
            return False 
    except NameError:
        return False


def _prepare_data(pred_data):

    served_data = []
    for key, value in pred_data:
        served_data.append(value)

    return served_data


#def _make_app(model, ptype, check_ptype):


def vetiver_serve(vetiver_model: VetiverModel, check_ptype=True, host_addr = "127.0.0.1", port = 8000):

    '''
    Parameters
    ----------
    model :  
    ptype :  
    host_addr : 
    port :
    '''

    model = _prepare_model(vetiver_model.model[0])
    ptype = vetiver_model.ptype[0]

    app = FastAPI(docs_url="/")

    @app.get("/")
    def vetiver_intro():
        return {"message": "to view visual documentation, go to /rapidoc or /docs"}

    if (check_ptype == False):
        @app.post("/predict/")
        async def prediction(input_data):

            input_data = input_data.split(" ") # user delimiter ?
            input_data = np.asarray(input_data)
            reshape_data = input_data.reshape(1,-1) 
            y = model.predict(reshape_data)

            return {'prediction': y[0]}
    else:
        @app.post("/predict/")
        async def prediction(input_data: ptype):
                
            served_data = _prepare_data(input_data)

            y = model.predict([served_data])

            return {'prediction': y[0]} #what about models with multiple outputs

    @app.get("/rapidoc", response_class=HTMLResponse, include_in_schema=False)
    async def rapidoc():
        return f"""
            <!doctype html>
            <html>
                <head>
                    <meta charset="utf-8">
                    <script 
                        type="module" 
                        src="https://unpkg.com/rapidoc/dist/rapidoc-min.js"
                    ></script>
                </head>
                <body>
                    <rapi-doc spec-url="{app.openapi_url}"></rapi-doc>
                </body> 
            </html>
        """
    
    if _jupyter_nb() == True:
            warnings.warn("WARNING: Jupyter Notebooks are not considered stable environments for production code")
            nest_asyncio.apply()
    
    uvicorn.run(app, host=host_addr, port=port)
    