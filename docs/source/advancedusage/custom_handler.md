# Custom Handlers

There are two different ways that vetiver supports flexible handling for models that do not work automatically with the vetiver framework. The first way is with new model types where there is no current implementation for the type of model you would like to deploy. The second way is when you would like to implement a current handler, but in a different way. In either case, you should create a custom handler from vetiver's `BaseHandler()`. At a minimum, you must give the type of your model via `model_type` how predictions should be made, via the method `handler_predict()`. Then, initialize your handler with your model, and pass the object into `VetiverModel`.

This example shows a custom handler of `newmodeltype` type.

```python
from vetiver.handlers.base import BaseHandler

class CustomHandler(BaseHandler):
    def __init__(self, model, ptype_data):
        super().__init__(model, ptype_data)

    model_type = staticmethod(lambda: newmodeltype)

    def handler_predict(self, input_data, check_ptype: bool):
        """
        Generates method for /predict endpoint in VetiverAPI

        The `handler_predict` function executes at each API call. Use this
        function for calling `predict()` and any other tasks that must be executed at each API call.

        Parameters
        ----------
        input_data:
            Test data
        check_ptype: bool
            Whether the ptype should be enforced

        Returns
        -------
        prediction
            Prediction from model
        """
        # your code here
        prediction = model.fancy_new_predict(input_data)

        return prediction

new_model = CustomHandler(model, ptype_data)

VetiverModel(new_model, "custom_model")
```

If your model is a common type, please consider [submitting a pull request](https://github.com/rstudio/vetiver-python/pulls).
