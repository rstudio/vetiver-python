import pytest
from vetiver import VetiverModel, mock
from vetiver import InvalidModelError


def test_not_implemented_error():
    X, y = mock.get_mock_data()

    with pytest.raises(InvalidModelError):
        VetiverModel(
            model=y,
            prototype_data=X,
            model_name="my_model",
            versioned=None,
            description="A regression model for testing purposes",
        )
