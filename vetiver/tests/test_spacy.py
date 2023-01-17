import pytest

spacy = pytest.importorskip("spacy", reason="spacy library not installed")

import numpy as np  # noqa
import pandas as pd  # noqa
from fastapi.testclient import TestClient  # noqa

import vetiver  # noqa


@pytest.fixture
def spacy_model():
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
    df = pd.DataFrame({"text": ["i have a dog", "my turtle is smarter than my dog"]})

    return vetiver.VetiverModel(nlp, "animals", prototype_data=df)


@pytest.fixture
def vetiver_client(spacy_model):  # With check_prototype=True
    app = vetiver.VetiverAPI(spacy_model, check_prototype=True)
    app.app.root_path = "/predict"
    client = TestClient(app.app)

    return client


@pytest.fixture
def vetiver_client_check_ptype_false(spacy_model):  # With check_prototype=False
    app = vetiver.VetiverAPI(spacy_model, check_prototype=False)
    app.app.root_path = "/predict"
    client = TestClient(app.app)

    return client


def test_vetiver_build(spacy_model):

    df = pd.DataFrame({"text": ["i have a dog", "my turtle is smarter than my dog"]})

    response = spacy_model.handler_predict(df, True)

    assert isinstance(response, pd.Series)
    assert response.iloc[0].get("text") == "i have a dog"


def test_vetiver_post(vetiver_client):
    df = pd.DataFrame({"text": ["i have a dog", "my turtle is smarter than my dog"]})

    response = vetiver.predict(endpoint=vetiver_client, data=df)

    assert isinstance(response, pd.DataFrame), response
    assert response.to_dict() == {
        "predict": {
            0: {
                "text": "i have a dog",
                "ents": [{"label": "ANIMAL", "start": 9, "end": 12}],
            },
            1: {
                "text": "my turtle is smarter than my dog",
                "ents": [
                    {"label": "ANIMAL", "start": 3, "end": 9},
                    {"label": "ANIMAL", "start": 29, "end": 32},
                ],
            },
        }
    }


# def test_batch(vetiver_client):
#     nlp = spacy.blank("en")
#     words1 = "This is a new"
#     doc1 = spacy.tokens.Doc(nlp.vocab, words=words1)
#     words2 = ["Another", "one", "."]
#     doc2 = spacy.tokens.Doc(nlp.vocab, words=words2)

#     response = vetiver.predict(endpoint=vetiver_client, data=[doc1, doc2])

#     assert response == [[True, False, False, False, False, False], [True, False, False]]


# def test_no_ptype(vetiver_client_check_ptype_false):
#     nlp = spacy.blank("en")
#     words1 = ["This", "is", "a", "new", "Sentence", "."]
#     doc1 = spacy.tokens.Doc(nlp.vocab, words=words1)
#     words2 = ["Another", "one", "."]
#     doc2 = spacy.tokens.Doc(nlp.vocab, words=words2)

#     response = vetiver.predict(
#         endpoint=vetiver_client_check_ptype_false, data=[doc1, doc2]
#     )

#     assert response == [[True, False, False, False, False, False], [True, False, False]]


# def test_serialize(spacy_model):
#     import pins

#     board = pins.board_temp(allow_pickle_read=True)
#     vetiver.vetiver_pin_write(board=board, model=spacy_model)
#     assert isinstance(
#         board.pin_read("sentencizer"),
#         spacy.pipeline.sentencizer.Sentencizer,
#     )
#     board.pin_delete("sentencizer")
