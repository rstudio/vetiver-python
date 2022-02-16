# VetiverAPI

This tutorial shows you how to use `VetiverAPI()` with its core features, step by step.

## Minimal deployment

The simplest VetiverAPI deployment includes a trained model with a `predict` method, inside a **VetiverModel**.

``` {python}
from vetiver import dummy, VetiverModel, VetiverAPI

X, y = dummy.get_dummy_data()
model = dummy.get_dummy_model().fit(X, y)

v = VetiverModel(model = model, save_ptype = True, ptype_data = X)

my_api = VetiverAPI(v)
my_api.run()
```
_(This script is complete, it should run "as is")_

!!! note

    In this example, Vetiver is invoking a data prototype, or `ptype`, which requires sample data to create. This is an optional configuration, but it creates more verbose documentation within the API, as well as allows for some basic type-checking within the API itself. To turn this off, set `save_ptype = False`.

In the output, there will be a line with something similiar to:

```{bash}
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Follow the link to the API at [http://127.0.0.1:8000](http://127.0.0.1:8000). You will be redirected to the automatic API documentation provided by [Rapidoc](https://mrin9.github.io/RapiDoc/). From there, you can send requests to your model, see example `curl` commands, and interact with your API.

## Multiple endpoints

More advanced use cases may require multiple endpoints to be created for pre-processing or post-processing data. You can use `vetiver_post()` to create a new `POST` endpoint that implements a custom function. In the example below, the endpoint "new_endpoint" sums all the input data.

!!! note

    The method `vetiver_post()` currently handles all data as a [Series](https://pandas.pydata.org/docs/reference/api/pandas.Series.html) type.

```{python}
from vetiver import dummy, VetiverModel, VetiverAPI

X, y = dummy.get_dummy_data()
model = dummy.get_dummy_model().fit(X, y)

v = VetiverModel(model = model, save_ptype = True, ptype_data = X)

my_api = VetiverAPI(v)

# new endpoint
def sum_numbers(x):
    return x.sum()

my_api.vetiver_post(endpoint_fx = sum_numbers, endpoint_name = "new_endpoint")

my_api.run()
```
_(This script is complete, it should run "as is")_
