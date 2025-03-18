import json
import logging
import re
import webbrowser
from textwrap import dedent
from typing import Callable, List, Union
from urllib.parse import urljoin
from warnings import warn

import httpx
import pandas as pd
import requests
import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from .helpers import api_data_to_frame, response_to_frame
from .handlers.sklearn import SKLearnHandler
from .meta import VetiverMeta
from .utils import _jupyter_nb, get_workbench_path
from .vetiver_model import VetiverModel
from .types import SklearnPredictionTypes


class VetiverAPI:
    """Create model aware API

    Parameters
    ----------
    model :  VetiverModel
        Model to be deployed in API
    show_prototype: bool = True
        Whether or not to show the data prototype in the API
    check_prototype : bool
        Determine if data prototype should be enforced
    app_factory :
        Type of API to be deployed
    **kwargs: dict
        Deprecated parameters.

    Examples
    -------
    ```{python}
    from vetiver import mock, VetiverModel, VetiverAPI
    X, y = mock.get_mock_data()
    model = mock.get_mock_model().fit(X, y)

    v = VetiverModel(model = model, model_name = "my_model", prototype_data = X)
    api = VetiverAPI(model = v, check_prototype = True)
    ```

    Notes
    -----
    This generates an API with 2-4 GET endpoints and 1 POST endpoint.

    ```
    ├──/ping (GET)
    ├──/metadata (GET)
    ├──/prototype (GET, if `show_prototype` is True)
    ├──/pin-url (GET, if VetiverModel metadata `url` field is not None)
    └──/predict (POST)
    ```

    Parameter `check_ptype` was changed to `check_prototype`. Handling of `check_ptype`
    will be removed in a future version.
    """

    app = None

    def __init__(
        self,
        model: VetiverModel,
        show_prototype: bool = True,
        check_prototype: bool = True,
        app_factory=FastAPI,
        **kwargs,
    ) -> None:
        self.model = model
        self.app_factory = app_factory
        self.app = app_factory()
        self.workbench_path = None

        if "check_ptype" in kwargs:
            check_prototype = kwargs.pop("check_ptype")
            warn(
                "argument for checking input data prototype has changed to "
                "check_prototype, from check_ptype",
                DeprecationWarning,
                stacklevel=2,
            )
        if hasattr(self.model, "ptype"):
            self.model.prototype = self.model.ptype
            delattr(self.model, "ptype")

        self.show_prototype = show_prototype
        self.check_prototype = check_prototype

        self._init_app()

    def _init_app(self):
        app = self.app
        app.openapi = self._custom_openapi

        @app.on_event("startup")
        async def startup_event():
            logger = logging.getLogger("uvicorn.error")
            if self.workbench_path:
                logger.info(f"VetiverAPI starting at {self.workbench_path}")
            else:
                logger.info("VetiverAPI starting...")

        @app.get("/", include_in_schema=False)
        def docs_redirect():
            redirect = "__docs__"

            return RedirectResponse(redirect)

        if isinstance(self.model.metadata, dict):
            self.model.metadata = VetiverMeta.from_dict(self.model.metadata)

        if self.model.metadata.url is not None:

            @app.get("/pin-url")
            def pin_url():
                return repr(self.model.metadata.url)

        @app.get("/ping", include_in_schema=True)
        async def ping():
            """Ping endpoint for health check"""
            return {"ping": "pong"}

        @app.get("/metadata")
        async def get_metadata():
            """Get metadata from model"""
            return self.model.metadata.to_dict()

        if self.show_prototype is True:

            @app.get("/prototype")
            async def get_prototype():
                # to handle pydantic<2 and >=2
                prototype_schema = getattr(
                    self.model.prototype,
                    "model_json_schema",
                    self.model.prototype.schema_json,
                )()
                # pydantic<2 returns a string, need to handle to json format
                if isinstance(prototype_schema, str):
                    prototype_schema = json.loads(prototype_schema)
                for key, value in prototype_schema["properties"].items():
                    value.pop("title", None)
                return prototype_schema

        self.vetiver_post(
            self.model.handler_predict, "predict", check_prototype=self.check_prototype
        )

        @app.get("/__docs__", response_class=HTMLResponse, include_in_schema=False)
        async def rapidoc():
            # save as html html.tpl, .format {spec_url}
            return f"""
                    <!doctype html>
                    <html>
                        <head>
                        <meta name="viewport"
                        content="width=device-width,minimum-scale=1,initial-scale=1,user-scalable=yes">
                        <title>RapiDoc</title>
                        <script type="module"
                        src="https://unpkg.com/rapidoc@9.3.3/dist/rapidoc-min.js"></script>
                        </script></head>
                        <body>
                            <rapi-doc spec-url="{self.app.openapi_url[1:]}"
                            id="thedoc"
                            render-style="read"
                            schema-style="tree"
                            show-components="true"
                            show-info="true"
                            show-header="true"
                            allow-search="true"
                            show-side-nav="false"
                            allow-authentication="false"
                            update-route="false"
                            match-type="regex"
                            theme="light"
                            header-color="#F2C6AC"
                            primary-color = "#8C2D2D">
                            <img
                            slot="logo"
                            width="55"
                            src="https://raw.githubusercontent.com/rstudio/hex-stickers/master/SVG/vetiver.svg"
                            </rapi-doc>
                        </body>
                    </html>
            """

        @app.exception_handler(RequestValidationError)
        async def validation_exception_handler(request, exc):
            return PlainTextResponse(str(exc), status_code=422)

        return app

    def vetiver_post(
        self,
        endpoint_fx: Union[Callable, SklearnPredictionTypes],
        endpoint_name: str = None,
        **kw,
    ):
        """Define a new POST endpoint that utilizes the model's input data.

        Parameters
        ----------
        endpoint_fx : Union[typing.Callable, Literal["predict", "predict_proba", "predict_log_proba"]]
            A callable function that specifies the custom logic to execute when the endpoint is called.
            This function should take input data (e.g., a DataFrame or dictionary) and return the desired output
            (e.g., predictions or transformed data). For scikit-learn models, endpoint_fx can also be one of
            "predict", "predict_proba", or "predict_log_proba" if the model supports these methods.

        endpoint_name : str
            The name of the endpoint to be created.

        Examples
        -------
        ```python
        from vetiver import mock, VetiverModel, VetiverAPI
        X, y = mock.get_mock_data()
        model = mock.get_mock_model().fit(X, y)

        v = VetiverModel(model=model, model_name="model", prototype_data=X)
        v_api = VetiverAPI(model=v, check_prototype=True)

        def sum_values(x):
            return x.sum()

        v_api.vetiver_post(sum_values, "sums")
        ```
        """

        if isinstance(endpoint_fx, SklearnPredictionTypes):
            if not isinstance(self.model, SKLearnHandler):
                raise ValueError(
                    "The 'endpoint_fx' parameter can only be a string when using scikit-learn models."
                )
            self.vetiver_post(
                self.model.handler_predict,
                SklearnPredictionTypes,
                check_prototype=self.check_prototype,
                prediction_type=endpoint_fx,
            )
            return

        endpoint_name = endpoint_name or endpoint_fx.__name__
        endpoint_doc = dedent(endpoint_fx.__doc__) if endpoint_fx.__doc__ else None

        @self.app.post(
            urljoin("/", endpoint_name),
            name=endpoint_name,
            description=endpoint_doc,
        )
        async def custom_endpoint(input_data: List[self.model.prototype]):
            if self.check_prototype:
                served_data = api_data_to_frame(input_data)
            else:
                served_data = await input_data.json()

            predictions = endpoint_fx(served_data, **kw)

            if isinstance(predictions, List):
                return {endpoint_name: predictions}
            else:
                return predictions

    def run(self, port: int = 8000, host: str = "127.0.0.1", quiet_open=False, **kw):
        """
        Start API

        Parameters
        ----------
        port : int
            An integer that indicates the server port that should be listened on.
        host : str
            A valid IPv4 or IPv6 address, which the application will listen on.
        quiet_open : bool
            If host is a localhost address, try to automatically open API in browser

        Examples
        -------

        ```python
        from vetiver import mock, VetiverModel, VetiverAPI
        X, y = mock.get_mock_data()
        model = mock.get_mock_model().fit(X, y)

        v = VetiverModel(model = model, model_name = "my_model", prototype_data = X)
        v_api = VetiverAPI(model = v, check_prototype = True)
        v_api.run()
        ```

        """
        _jupyter_nb()
        self.workbench_path = get_workbench_path(port)
        if port and host:
            try:
                if host == "127.0.0.1" and not quiet_open:
                    # quality of life for developing APIs locally
                    webbrowser.open(f"http://{host}:{port}")
            except Exception:
                pass
        if self.workbench_path:
            uvicorn.run(
                self.app, port=port, host=host, root_path=self.workbench_path, **kw
            )
        else:
            uvicorn.run(self.app, port=port, host=host, **kw)

    def _custom_openapi(self):
        import vetiver

        if self.app.openapi_schema:
            return self.app.openapi_schema
        openapi_schema = get_openapi(
            title=self.model.model_name + " model API",
            version=vetiver.__version__,
            description=self.model.description,
            routes=self.app.routes,
            servers=self.app.servers,
        )
        openapi_schema["info"]["x-logo"] = {"url": "../docs/figures/logo.svg"}
        self.app.openapi_schema = openapi_schema

        return self.app.openapi_schema


def predict(endpoint, data: Union[dict, pd.DataFrame, pd.Series], **kw) -> pd.DataFrame:
    """Make a prediction from model endpoint

    Parameters
    ----------
    endpoint :
        URI path to endpoint
    data : Union[dict, pd.DataFrame, pd.Series]
        New data for making predictions, such as a data frame.

    Returns
    -------
    dict
        Endpoint_name and list of endpoint_fx output

    Examples
    -------
    ```python
    from vetiver import vetiver_endpoint, mock, predict
    X, y = mock.get_mock_data()
    endpoint = vetiver_endpoint(url='http://127.0.0.1:8000/predict')
    predict(endpoint, X)
    ```

    Notes
    -----
    To authorize a request to Posit Connect, pass in a
    dictionary of headers that includes your API key. For example:

    ```python
    h = { 'Authorization': f'Key {api_key}' }
    response = predict(data = data, endpoint = endpoint, headers=h)
    ```

    """
    if "test_client" in kw:
        requester = kw.pop("test_client")
    else:
        requester = requests

    # TO DO: arrow format
    # TO DO: dispatch

    if isinstance(data, pd.DataFrame):
        response = requester.post(
            endpoint, data=data.to_json(orient="records"), **kw
        )  # TO DO: httpx deprecating data in favor of content for TestClient
    elif isinstance(data, pd.Series):
        response = requester.post(endpoint, json=[data.to_dict()], **kw)
    elif isinstance(data, dict):
        response = requester.post(endpoint, json=[data], **kw)
    else:
        response = requester.post(endpoint, json=data, **kw)

    try:
        response.raise_for_status()
    except (requests.exceptions.HTTPError, httpx.HTTPStatusError) as e:
        if response.status_code == 422:
            raise TypeError(re.sub(r"\n", ": ", response.text))
        raise requests.exceptions.HTTPError(
            f"Could not obtain data from endpoint with error: {e}"
        )

    response_frame = response_to_frame(response)

    return response_frame


def vetiver_endpoint(url: str = "http://127.0.0.1:8000/predict") -> str:
    """Wrap url where VetiverModel will be deployed

    Parameters
    ----------
    url : str
        URI path to endpoint

    Returns
    -------
    url : str
        URI path to endpoint

    Examples
    -------
    ```{python}
    from vetiver import vetiver_endpoint
    endpoint = vetiver_endpoint(url='http://127.0.0.1:8000/predict')
    ```
    """
    # remove trailing backslash, if it exists
    if url[-1] == "/":
        url = url[:-1]

    return url
