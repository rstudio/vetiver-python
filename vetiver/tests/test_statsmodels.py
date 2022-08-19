# import pytest

# sm = pytest.importorskip("statsmodels", reason="statsmodels library not installed")

# import numpy as np  # noqa
# from fastapi.testclient import TestClient  # noqa

# from vetiver.vetiver_model import VetiverModel  # noqa
# from vetiver import VetiverAPI  # noqa


# def _build_sm():

#     input_size = 1
#     output_size = 1

#     x_train = np.array(
#         [
#             [3.3],
#             [4.4],
#             [5.5],
#             [6.71],
#             [6.93],
#             [4.168],
#             [9.779],
#             [6.182],
#             [7.59],
#             [2.167],
#             [7.042],
#             [10.791],
#             [5.313],
#             [7.997],
#             [3.1],
#         ],
#         dtype=np.float32,
#     )

#     torch_model = sm.nn.Linear(input_size, output_size)
#     return x_train, torch_model


# def test_vetiver_build():

#     x_train, torch_model = _build_sm()

#     vt2 = VetiverModel(
#         model=torch_model,
#         ptype_data=x_train,
#         model_name="torch",
#         versioned=None,
#         description=None,
#         metadata=None,
#     )

#     assert vt2.model == torch_model


# def test_sm_predict_ptype():
#     torch.manual_seed(3)
#     x_train, torch_model = _build_sm()
#     v = VetiverModel(torch_model, model_name="torch", ptype_data=x_train)
#     v_api = VetiverAPI(v)

#     client = TestClient(v_api.app)
#     data = {"0": 3.3}
#     response = client.post("/predict", json=data)

#     assert response.status_code == 200, response.text
#     assert response.json() == {"prediction": [-4.060722351074219]}, response.text


# def test_sm_predict_ptype_batch():

#     x_train, torch_model = _build_sm()
#     v = VetiverModel(torch_model, model_name="torch", ptype_data=x_train)
#     v_api = VetiverAPI(v)

#     client = TestClient(v_api.app)
#     data = [{"0": 3.3}, {"0": 3.3}]
#     response = client.post("/predict", json=data)

#     assert response.status_code == 200, response.text
#     assert response.json() == {
#         "prediction": [[-4.060722351074219], [-4.060722351074219]]
#     }, response.text


# def test_sm_predict_ptype_error():

#     x_train, torch_model = _build_sm()
#     v = VetiverModel(torch_model, model_name="torch", ptype_data=x_train)
#     v_api = VetiverAPI(v)

#     client = TestClient(v_api.app)
#     data = {"0": "bad"}
#     response = client.post("/predict", json=data)

#     assert response.status_code == 422, response.text  # value is not a valid float


# def test_sm_predict_no_ptype_batch():

#     x_train, torch_model = _build_sm()
#     v = VetiverModel(torch_model, model_name="torch")
#     v_api = VetiverAPI(v, check_ptype=False)

#     client = TestClient(v_api.app)
#     data = [[3.3], [3.3]]
#     response = client.post("/predict", json=data)
#     assert response.status_code == 200, response.text
#     assert response.json() == {
#         "prediction": [[-4.060722351074219], [-4.060722351074219]]
#     }, response.text


# def test_sm_predict_no_ptype():

#     x_train, torch_model = _build_sm()
#     v = VetiverModel(torch_model, model_name="torch")
#     v_api = VetiverAPI(v, check_ptype=False)

#     client = TestClient(v_api.app)
#     data = [[3.3]]
#     response = client.post("/predict", json=data)
#     assert response.status_code == 200, response.text
#     assert response.json() == {"prediction": [[-4.060722351074219]]}, response.text

# def test_pin_sm():
