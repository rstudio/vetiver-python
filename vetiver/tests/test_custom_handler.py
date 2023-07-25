import sklearn
import pydantic
import pandas as pd

from vetiver import mock, VetiverModel, BaseHandler


class CustomHandler(BaseHandler):
    def __init__(self, model, prototype_data):
        super().__init__(model, prototype_data)

    model_type = staticmethod(lambda: sklearn.dummy.DummyRegressor)

    def handler_predict(self, input_data, check_ptype):
        if check_ptype is True:
            if isinstance(input_data, pd.DataFrame):
                prediction = self.model.predict(input_data)
            else:
                prediction = self.model.predict([input_data])
        else:
            if not isinstance(input_data, list):
                input_data = [input_data.split(",")]  # user delimiter ?
            prediction = self.model.predict(input_data)

        return prediction


def test_custom_vetiver_model():
    X, y = mock.get_mock_data()
    model = mock.get_mock_model().fit(X, y)
    custom_handler = CustomHandler(model, X)

    v = VetiverModel(
        model=custom_handler,
        prototype_data=X,
        model_name="my_model",
        versioned=None,
    )

    assert v.description == "A  DummyRegressor model"
    assert not v.metadata.required_pkgs
    assert isinstance(v.model, sklearn.dummy.DummyRegressor)
    # change to model_construct for pydantic v3
    assert isinstance(v.prototype.construct(), pydantic.BaseModel)


def test_custom_vetiver_model_no_ptype():
    X, y = mock.get_mock_data()
    model = mock.get_mock_model().fit(X, y)
    custom_handler = CustomHandler(model, None)

    v = VetiverModel(
        model=custom_handler,
        prototype_data=X,
        model_name="my_model",
        versioned=None,
        description="A regression model for testing purposes",
    )

    assert v.description == "A regression model for testing purposes"
    assert isinstance(v.model, sklearn.dummy.DummyRegressor)
    # change to model_construct for pydantic v3
    assert isinstance(v.prototype.construct(), pydantic.BaseModel)
