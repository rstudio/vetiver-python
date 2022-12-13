import vetiver
import pins
import numpy as np

np.random.seed(500)

X, y = vetiver.get_mock_data()
model = vetiver.get_mock_model().fit(X, y)

board = pins.board_folder("pinsboard", allow_pickle_read=True)

v = vetiver.VetiverModel(model, "mymodel", ptype_data=X)

vetiver.vetiver_pin_write(board, v)
<<<<<<< HEAD
<<<<<<< HEAD

vetiver.prepare_docker(board, "mymodel")
=======
vetiver.load_pkgs(
    v,
    packages=["git+https://github.com/rstudio/vetiver-python@metadata"],
    path="vetiver_",
)
=======
vetiver.load_pkgs(v, path="vetiver_")
>>>>>>> aa70c3e (always install latest vetiver in docker)
vetiver.write_app(board, "mymodel")
vetiver.write_docker()
>>>>>>> 875faf2 (install into docker from branch)
