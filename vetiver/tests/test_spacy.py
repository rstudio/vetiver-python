import pytest

spacy = pytest.importorskip("spacy", reason="spacy library not installed")

import numpy as np  # noqa
import pandas as pd  # noqa
from fastapi.testclient import TestClient  # noqa

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


@pytest.fixture
def spacy_model():

    nlp = spacy.load("en_core_web_sm")
    animals = list(nlp.pipe(["dog", "cat", "turtle"]))
    matcher = spacy.matcher.PhraseMatcher(nlp.vocab)
    matcher.add("ANIMAL", animals)
    nlp.add_pipe("animals", after="ner")

    return vetiver.VetiverModel(nlp, "animals")


@pytest.fixture
def vetiver_client(spacy_model):  # With check_prototype=True
    app = vetiver.VetiverAPI(spacy_model, check_prototype=True)
    app.app.root_path = "/predict"
    client = TestClient(app.app)

    return client


@pytest.fixture
def vetiver_client_check_ptype_false(spacy_model):  # With check_prototype=True
    app = vetiver.VetiverAPI(spacy_model, check_prototype=False)
    app.app.root_path = "/predict"
    client = TestClient(app.app)

    return client


def test_vetiver_build(vetiver_client):
    words = {
        "data": [{"text": "i have a dog"}, {"text": "my turtle is smarter than my dog"}]
    }

    response = vetiver.predict(endpoint=vetiver_client, data=words)

    assert response.to_dict() == [[True, False, False, False, False, False]]


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
