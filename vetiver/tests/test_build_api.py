from vetiver import mock, VetiverModel, VetiverAPI
from fastapi import FastAPI


def _build_v():
    X, y = mock.get_mock_data()
    model = mock.get_mock_model().fit(X, y)
    v = VetiverModel(
        model=model,
        prototype_data=X,
        model_name="my_model",
        versioned=None,
        description="A regression model for testing purposes",
    )

    return v


def test_is_fastapi():

    v = _build_v()
    app = VetiverAPI(v)
    assert isinstance(app.app, FastAPI)


def test_is_v_model():

    v = _build_v()
    app = VetiverAPI(v)
    assert isinstance(app.model, VetiverModel)
