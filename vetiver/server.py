from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, ValidationError
import joblib
from joblib import dump
import uvicorn
import sklearn
import pandas as pd
from typing import List

# do we want to convert to joblib?
def _prepare_model(model):
    dump(model, 'vetiver_model.joblib')
    load_model = joblib.load("vetiver_model.joblib")
    return(load_model)


def _validate_data(data_base_model, pred_data):
    
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


def vetiver_serve(sk_model, data_base_model, host_addr = "127.0.0.1", port = 8000):
    
    served_model = _prepare_model(sk_model)

    # create a template for visual docs?

    app = FastAPI()
    @app.get("/")
    def vetiver_intro():
        return {"message": "go to /rapidoc or /docs"}

    @app.post("/predict")
    async def prediction(pred_data: data_base_model):
              
        served_data = _validate_data(data_base_model, pred_data)

        y = served_model.predict([served_data])

        return {'prediction': y[0]}

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

    uvicorn.run(app, host=host_addr, port=port)