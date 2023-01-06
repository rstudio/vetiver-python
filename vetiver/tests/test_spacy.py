import pytest

spacy = pytest.importorskip("spacy", reason="spacy library not installed")

import numpy as np  # noqa
import pandas as pd  # noqa
from fastapi.testclient import TestClient  # noqa

import vetiver  # noqa


@pytest.fixture
def spacy_model():

    nlp = spacy.blank("en")
    sentencizer = nlp.add_pipe("sentencizer")

    return vetiver.VetiverModel(sentencizer, "sentencizer")


@pytest.fixture
def vetiver_client(spacy_model):  # With check_ptype=True
    app = vetiver.VetiverAPI(spacy_model, check_ptype=True)
    app.app.root_path = "/predict"
    client = TestClient(app.app)

    return client


@pytest.fixture
def vetiver_client_check_ptype_false(spacy_model):  # With check_ptype=True
    app = vetiver.VetiverAPI(spacy_model, check_ptype=False)
    app.app.root_path = "/predict"
    client = TestClient(app.app)

    return client


def test_vetiver_build(vetiver_client):
    nlp = spacy.blank("en")
    words = ["This", "is", "a", "new", "Sentence", "."]
    doc = spacy.tokens.Doc(nlp.vocab, words=words)

    response = vetiver.predict(endpoint=vetiver_client, data=doc.to_json())

    assert response == [[True, False, False, False, False, False]]


def test_batch(vetiver_client):
    nlp = spacy.blank("en")
    words1 = ["This", "is", "a", "new", "Sentence", "."]
    doc1 = spacy.tokens.Doc(nlp.vocab, words=words1)
    words2 = ["Another", "one", "."]
    doc2 = spacy.tokens.Doc(nlp.vocab, words=words2)

    response = vetiver.predict(endpoint=vetiver_client, data=[doc1, doc2])

    assert response == [[True, False, False, False, False, False], [True, False, False]]


def test_no_ptype(vetiver_client_check_ptype_false):
    nlp = spacy.blank("en")
    words1 = ["This", "is", "a", "new", "Sentence", "."]
    doc1 = spacy.tokens.Doc(nlp.vocab, words=words1)
    words2 = ["Another", "one", "."]
    doc2 = spacy.tokens.Doc(nlp.vocab, words=words2)

    response = vetiver.predict(
        endpoint=vetiver_client_check_ptype_false, data=[doc1, doc2]
    )

    assert response == [[True, False, False, False, False, False], [True, False, False]]


def test_serialize(spacy_model):
    import pins

    board = pins.board_temp(allow_pickle_read=True)
    vetiver.vetiver_pin_write(board=board, model=spacy_model)
    assert isinstance(
        board.pin_read("sentencizer"),
        spacy.pipeline.sentencizer.Sentencizer,
    )
    board.pin_delete("sentencizer")
