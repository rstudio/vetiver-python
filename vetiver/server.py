import re
import httpx
import json
import requests
import uvicorn
import logging
import pandas as pd
from fastapi import FastAPI, Request, testclient
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse
from textwrap import dedent
from warnings import warn
from urllib.parse import urljoin
from typing import Callable, List, Union

from .utils import _jupyter_nb, get_workbench_path
from .vetiver_model import VetiverModel
from .meta import VetiverMeta
from .helpers import api_data_to_frame, response_to_frame


class VetiverAPI:
    """Create model aware API

    Parameters
    ----------
    model :  VetiverModel
        Model to be deployed in API
    show_prototype: bool = True

    check_prototype : bool
        Determine if data prototype should be enforced
    app_factory :
        Type of API to be deployed
    **kwargs: dict
        Deprecated parameters.

    Examples
    -------
    >>> import vetiver as vt
    >>> X, y = vt.get_mock_data()
    >>> model = vt.get_mock_model().fit(X, y)
    >>> v = vt.VetiverModel(model = model, model_name = "my_model", prototype_data = X)
    >>> v_api = vt.VetiverAPI(model = v, check_prototype = True)

    Notes
    -----
    This generates an API with either 3 or 4 GET endpoints and 1 POST endpoint.

    ```
    ├──/ping (GET)
    ├──/metadata (GET)
    ├──/prototype (GET)
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

    def vetiver_post(self, endpoint_fx: Callable, endpoint_name: str = None, **kw):
        """Create new POST endpoint that is aware of model input data

        Parameters
        ----------
        endpoint_fx : typing.Callable
            Custom function to be run at endpoint
        endpoint_name : str
            Name of endpoint

        Examples
        -------
        >>> import vetiver as vt
        >>> X, y = vt.get_mock_data()
        >>> model = vt.get_mock_model().fit(X, y)
        >>> v = vt.VetiverModel(model = model, model_name = "model", prototype_data = X)
        >>> v_api = vt.VetiverAPI(model = v, check_prototype = True)
        >>> def sum_values(x):
        ...     return x.sum()
        >>> v_api.vetiver_post(sum_values, "sums")
        """
        if not endpoint_name:
            endpoint_name = endpoint_fx.__name__

        if endpoint_fx.__doc__ is not None:
            api_desc = dedent(endpoint_fx.__doc__)
        else:
            api_desc = None

        if self.check_prototype is True:

            @self.app.post(
                urljoin("/", endpoint_name),
                name=endpoint_name,
                description=api_desc,
            )
            async def custom_endpoint(input_data: List[self.model.prototype]):
                _to_frame = api_data_to_frame(input_data)
                predictions = endpoint_fx(_to_frame, **kw)
                if isinstance(predictions, List):
                    return {endpoint_name: predictions}
                else:
                    return predictions

        else:

            @self.app.post(urljoin("/", endpoint_name))
            async def custom_endpoint(input_data: Request):
                served_data = await input_data.json()
                predictions = endpoint_fx(served_data, **kw)

                if isinstance(predictions, List):
                    return {endpoint_name: predictions}
                else:
                    return predictions

    def run(self, port: int = 8000, host: str = "127.0.0.1", **kw):
        """
        Start API

        Parameters
        ----------
        port : int
            An integer that indicates the server port that should be listened on.
        host : str
            A valid IPv4 or IPv6 address, which the application will listen on.

        Examples
        -------
        >>> import vetiver as vt
        >>> X, y = vt.get_mock_data()
        >>> model = vt.get_mock_model().fit(X, y)
        >>> v = vt.VetiverModel(model = model, model_name = "model", prototype_data = X)
        >>> v_api = vt.VetiverAPI(model = v, check_prototype = True)
        >>> v_api.run()     # doctest: +SKIP
        """
        _jupyter_nb()
        self.workbench_path = get_workbench_path(port)

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
        Name of endpoint

    Returns
    -------
    dict
        Endpoint_name and list of endpoint_fx output

    Examples
    -------
    >>> import vetiver
    >>> X, y = vetiver.get_mock_data()
    >>> endpoint = vetiver.vetiver_endpoint(url='http://127.0.0.1:8000/predict')
    >>> vetiver.predict(endpoint, X)     # doctest: +SKIP
    """
    if isinstance(endpoint, testclient.TestClient):
        requester = endpoint
        endpoint = requester.app.root_path
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
    >>> import vetiver
    >>> endpoint = vetiver.vetiver_endpoint(url='http://127.0.0.1:8000/predict')
    """
    # remove trailing backslash, if it exists
    if url[-1] == "/":
        url = url[:-1]

    return url
