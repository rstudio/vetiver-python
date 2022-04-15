import pytest 
from vetiver import VetiverModel, mock


def test_not_implemented_error():
    X, y = mock.get_mock_data()

    with pytest.raises(NotImplementedError):
        VetiverModel(
        model=y,
        save_ptype=True,
        ptype_data=X,
        model_name="my_model",
        versioned=None,
        description="A regression model for testing purposes",
    )
