# Custom Handlers

There are two different ways that vetiver supports flexible handling for models that do not work automatically with the vetiver framework. The first way is with [new model types,](#new-model-type) where there is no current implementation for the type of model you would like to deploy. The second way is when you would like to implement a current handler, but [in a different way](#different-model-implementation). In either case, you *must* make a custom handler from the base `VetiverHandler`. A minimal custom handler could look like the following:

```python
from vetiver.handlers.base import VetiverHandler

class SampleCustomHandler(VetiverHandler):
    def __init__(model, ptype_data):
        super().__init__(model, ptype_data)
    
    def handler_predict(self, input_data, check_ptype):
        """
        handler_predict defines how to make predictions from your model
        """
        # your code here
```

## New model type
If your model type is not supported by vetiver, you should create and then register the handler using [single dispatch](https://docs.python.org/3/library/functools.html#functools.singledispatch). Once the new type is registered, you are able to use `VetiverModel()` as normal. Here is a template for such a function: 

```python    
from vetiver.handlers._interface import create_handler

@create_handler.register
def _(model: {_model_type}, ptype_data):
    return SampleCustomHandler(model, ptype_data)

VetiverModel(your_model, "your_model")
```

If your model is a common type, please consider [submitting a pull request](https://github.com/rstudio/vetiver-python/pulls).

## Different model implementation
If your model's prediction function is different than vetiver's, you should create a custom handler with a `handler_predict` method to make predictions. Then, initialize your handler with your model, and pass the object into `VetiverModel`.

```python    
new_model = SampleCustomHandler(your_model, your_ptype_data)

VetiverModel(new_model, "your_model")
```