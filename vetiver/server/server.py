from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi import Request


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


@app.get('/')
def get_root():

	return {'message': 'Welcome to the API'}

@app.get('/predict_query/')
async def predict_query(message: float):
	return predictions_model(model, message)

@app.get('/predict_path/{message}')
async def predict_path(message: float):
	return predictions_model(model, message)
