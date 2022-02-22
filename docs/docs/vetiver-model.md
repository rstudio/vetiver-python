# VetiverModel

This tutorial shows you how to use `VetiverModel()` with its core features, step by step.

Users will start with any trained model. Currently, Vetiver supports [scikit-learn](https://scikit-learn.org/stable/) models, with other model support on its way.

```python
from vetiver import mock, VetiverModel, VetiverAPI

X, y = mock.get_mock_data()
model = mock.get_mock_model().fit(X, y)

v = VetiverModel(model, save_ptype = True, ptype_data = X)
```

The `save_ptype` and `ptype_data` arguments refer to an _input data prototype_, or `ptype`. This **ptype** is an automatically created [Pydantic BaseModel](https://pydantic-docs.helpmanual.io/usage/models/) that stores the types of the data that the API can expect when deployed. To enable this feature, set `save_ptype = True` and set `ptype_data` equal to training data. You can turn this feature off by setting `save_ptype = False` and not passing in any `ptype_data`.
