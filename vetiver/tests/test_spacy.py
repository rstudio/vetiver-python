import pytest

spacy = pytest.importorskip("spacy", reason="spacy library not installed")

import numpy as np  # noqa
import pandas as pd  # noqa
from fastapi.testclient import TestClient  # noqa

import vetiver  # noqa


@pytest.fixture
def spacy_model():
<<<<<<< HEAD
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

    return vetiver.VetiverModel(nlp, "animals")


@pytest.fixture
def vetiver_client(spacy_model):  # With check_prototype=True
    app = vetiver.VetiverAPI(spacy_model, check_prototype=True)
=======

    nlp = spacy.blank("en")
    sentencizer = nlp.add_pipe("sentencizer")

    return vetiver.VetiverModel(sentencizer, "sentencizer")


@pytest.fixture
def vetiver_client(spacy_model):  # With check_ptype=True
    app = vetiver.VetiverAPI(spacy_model, check_ptype=True)
>>>>>>> b600e38 (testing spacy)
    app.app.root_path = "/predict"
    client = TestClient(app.app)

    return client


@pytest.fixture
<<<<<<< HEAD
def vetiver_client_check_ptype_false(spacy_model):  # With check_prototype=False
    app = vetiver.VetiverAPI(spacy_model, check_prototype=True)
=======
def vetiver_client_check_ptype_false(spacy_model):  # With check_ptype=True
    app = vetiver.VetiverAPI(spacy_model, check_ptype=False)
>>>>>>> b600e38 (testing spacy)
    app.app.root_path = "/predict"
    client = TestClient(app.app)

    return client


<<<<<<< HEAD
def test_vetiver_post(vetiver_client):
    df = pd.DataFrame({"text": ["one", "my turtle is smarter than my dog"]})

    response = vetiver.predict(endpoint=vetiver_client, data=df)

    assert isinstance(response, pd.DataFrame), response
    assert response.to_dict() == {
        "predict": {
            0: {
                "text": "one",
                "ents": [],
                "sents": [{"start": 0, "end": 3}],
                "tokens": [{"id": 0, "start": 0, "end": 3}],
            },
            1: {
                "text": "my turtle is smarter than my dog",
                "ents": [
                    {"start": 3, "end": 9, "label": "ANIMAL"},
                    {"start": 29, "end": 32, "label": "ANIMAL"},
                ],
                "tokens": [
                    {"id": 0, "start": 0, "end": 2},
                    {"id": 1, "start": 3, "end": 9},
                    {"id": 2, "start": 10, "end": 12},
                    {"id": 3, "start": 13, "end": 20},
                    {"id": 4, "start": 21, "end": 25},
                    {"id": 5, "start": 26, "end": 28},
                    {"id": 6, "start": 29, "end": 32},
                ],
            },
        }
    }


# def test_serialize(spacy_model):
#     import pins

#     board = pins.board_temp(allow_pickle_read=True)
#     vetiver.vetiver_pin_write(board=board, model=spacy_model)
#     assert isinstance(
#         board.pin_read("animals"),
#         spacy.Language,
#     )
#     board.pin_delete("animals")
=======
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
>>>>>>> b600e38 (testing spacy)
