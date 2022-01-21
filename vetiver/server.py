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
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter

def _validate_data(data_base_model, pred_data):

   # does this really validate type? 
    class Validate(BaseModel):
        df_dict: List[data_base_model]

    try:
        Validate(df_dict = pred_data.dict())
    except ValidationError as e:
        print(e.json())

    dict_data = pred_data
    served_data = []

    for key, value in dict_data:
        served_data.append(value)

    return served_data


def vetiver_serve(sk_model, ptype, host_addr = "127.0.0.1", port = 8000):

    '''
    Parameters
    ----------
    model :  
    ptype :  
    host_addr : 
    port :
    '''
    
    served_model = _prepare_model(sk_model)

    # create a template for visual docs?

    app = FastAPI()
    @app.get("/")
    def vetiver_intro():
        return {"message": "to view visual documentation, go to /rapidoc or /docs"}

    @app.post("/predict")
    async def prediction(pred_data: ptype):
              
        served_data = _validate_data(ptype, pred_data)

        y = served_model.predict([served_data])

        return {'prediction': y[0]}

    @app.post("/health")


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


    
    