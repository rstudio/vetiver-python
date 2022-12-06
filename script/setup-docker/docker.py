import vetiver
import pins

X, y = vetiver.get_mock_data()
model = vetiver.get_mock_model().fit(X, y)

board = pins.board_folder("pinsboard", allow_pickle_read=True)

v = vetiver.VetiverModel(model, "mymodel", ptype_data=X)

vetiver.vetiver_pin_write(board, v)

vetiver.prepare_docker(board, "mymodel")
