import pytest

spacy = pytest.importorskip("spacy", reason="spacy library not installed")

import numpy as np  # noqa
import pandas as pd  # noqa
from fastapi.testclient import TestClient  # noqa
from numpy import nan  # noqa
import vetiver  # noqa


@spacy.language.Language.component("animals")
def animal_component_function(doc):
    matches = matcher(doc)  # noqa
    spans = [
        spacy.tokens.Span(doc, start, end, label="ANIMAL")
        for match_id, start, end in matches
    ]
    doc.ents = spans
    return doc


nlp = spacy.blank("en")
animals = list(nlp.pipe(["dog", "cat", "turtle"]))
matcher = spacy.matcher.PhraseMatcher(nlp.vocab)
matcher.add("ANIMAL", animals)
nlp.add_pipe("animals")


@pytest.fixture
def spacy_model():
    return nlp


@pytest.fixture()
def vetiver_client_with_prototype(spacy_model):  # With check_prototype=True
    df = pd.DataFrame({"new_column": ["one", "two", "three"]})
    v = vetiver.VetiverModel(spacy_model, "animals", prototype_data=df)
    app = vetiver.VetiverAPI(v, check_prototype=True)
    app.app.root_path = "/predict"
    client = TestClient(app.app)

    return client


@pytest.fixture(scope="function")
def vetiver_client_with_prototype_series(spacy_model):  # With check_prototype=True
    df = pd.Series({"new_column": ["one", "two", "three"]})
    v = vetiver.VetiverModel(spacy_model, "animals", prototype_data=df)
    app = vetiver.VetiverAPI(v, check_prototype=True)
    app.app.root_path = "/predict"
    client = TestClient(app.app)
    return client


@pytest.fixture
def vetiver_client_no_prototype(spacy_model):  # With check_prototype=False
    v = vetiver.VetiverModel(spacy_model, "animals")
    app = vetiver.VetiverAPI(v, check_prototype=False)
    app.app.root_path = "/predict"
    client = TestClient(app.app)

    return client


@pytest.mark.parametrize("data", ["a", 1, [1, 2, 3]])
def test_bad_prototype_data(data, spacy_model):
    with pytest.raises(TypeError):
        vetiver.VetiverModel(spacy_model, "animals", prototype_data=data)


@pytest.mark.parametrize(
    "data",
    [
        {"col": ["1", "2"], "col2": [1, 2]},
        pd.DataFrame({"col": ["1", "2"], "col2": [1, 2]}),
    ],
)
def test_bad_prototype_shape(data, spacy_model):
    with pytest.raises(ValueError):
        vetiver.VetiverModel(spacy_model, "animals", prototype_data=data)


@pytest.mark.parametrize("data", [{"col": "1"}, pd.DataFrame({"col": ["1"]})])
def test_good_prototype_shape(data, spacy_model):
    v = vetiver.VetiverModel(spacy_model, "animals", prototype_data=data)

    assert v.prototype.construct().dict() == {"col": "1"}


def test_vetiver_predict_with_prototype(vetiver_client_with_prototype):
    df = pd.DataFrame({"new_column": ["turtles", "i have a dog"]})

    response = vetiver.predict(endpoint=vetiver_client_with_prototype, data=df)

    assert isinstance(response, pd.DataFrame), response
    assert response.to_dict() == {
        "0": {
            "text": "turtles",
            "ents": [],
            "sents": [{"start": 0, "end": 7}],
            "tokens": [{"id": 0, "start": 0, "end": 7}],
        },
        "1": {
            "text": "i have a dog",
            "ents": [{"start": 9, "end": 12, "label": "ANIMAL"}],
            "sents": nan,
            "tokens": [
                {"id": 0, "start": 0, "end": 1},
                {"id": 1, "start": 2, "end": 6},
                {"id": 2, "start": 7, "end": 8},
                {"id": 3, "start": 9, "end": 12},
            ],
        },
    }


def test_vetiver_predict_no_prototype(vetiver_client_no_prototype):
    df = pd.DataFrame({"uhhh": ["turtles", "i have a dog"]})

    response = vetiver.predict(endpoint=vetiver_client_no_prototype, data=df)

    assert isinstance(response, pd.DataFrame), response
    assert response.to_dict() == {
        "0": {
            "text": "turtles",
            "ents": [],
            "sents": [{"start": 0, "end": 7}],
            "tokens": [{"id": 0, "start": 0, "end": 7}],
        },
        "1": {
            "text": "i have a dog",
            "ents": [{"start": 9, "end": 12, "label": "ANIMAL"}],
            "sents": nan,
            "tokens": [
                {"id": 0, "start": 0, "end": 1},
                {"id": 1, "start": 2, "end": 6},
                {"id": 2, "start": 7, "end": 8},
                {"id": 3, "start": 9, "end": 12},
            ],
        },
    }


def test_serialize_no_prototype(spacy_model):
    import pins

    board = pins.board_temp(allow_pickle_read=True)
    v = vetiver.VetiverModel(spacy_model, "animals")
    vetiver.vetiver_pin_write(board=board, model=v)
    v2 = vetiver.VetiverModel.from_pin(board, "animals")
    assert isinstance(
        v2.model,
        spacy.lang.en.English,
    )


def test_serialize_prototype(spacy_model):
    import pins

    board = pins.board_temp(allow_pickle_read=True)
    v = vetiver.VetiverModel(
        spacy_model, "animals", prototype_data=pd.DataFrame({"text": ["text"]})
    )
    vetiver.vetiver_pin_write(board=board, model=v)
    v2 = vetiver.VetiverModel.from_pin(board, "animals")
    assert isinstance(
        v2.model,
        spacy.lang.en.English,
    )
