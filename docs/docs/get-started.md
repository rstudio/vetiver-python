# Overview

The goal of vetiver is to give data scientists and other model-builders the tools to deploy their model to a remote endpoint.

Key features include: - Simple: designed to fit into a data scientist's natural workflow - Robust: ability to check input data types to minimize type failures in a model - Advanced support: easily deploy multiple endpoints to handle pre- and post- processing - Based on [FastAPI](https://github.com/tiangolo/fastapi), using [OpenAPI](https://github.com/OAI/OpenAPI-Specification)

Source code: https://github.com/isabelizimm/vetiver-python

# Quickstart

`pip install vetiver`

To begin, initialize a `VetiverModel` with a trained model and an example of data (usually training data) to built a data prototype.

```python
my_model = VetiverModel(model = linear_reg, ptype_data = train_data)
```

Next, you can build a model-aware API and run it locally.

```python
my_app = VetiverServe(my_model)
my_app.run()
```
