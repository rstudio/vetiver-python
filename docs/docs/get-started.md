`vetiver` is an MLOps framework intended to extend a data science workflow to deployment after a model has been created. It

## Installation

vetiver can be installed via pip with [PyPI](https://pypi.org/project/vetiver/).

`pip install vetiver`

You can also install the development version from GitHub.

`pip install git+https://github.com/isabelizimm/vetiver`

## Get started

Vetiver focuses on two main objects: `VetiverModel()` and `VetiverAPI()`. A **VetiverModel** collects all the information needed for deploying a trained model, while a **VetiverAPI** deploys the model to a REST endpoint. The example below shows a minimal deployment of an arbitrary model.

```python
from vetiver import dummy, VetiverModel, VetiverAPI

X, y = dummy.get_dummy_data()
model = dummy.get_dummy_model().fit(X, y)

v = VetiverModel(model, save_ptype= True, ptype_data=X)

my_api = VetiverAPI(v)
my_api.run()
```
_(This script is complete, it should run "as is")_
