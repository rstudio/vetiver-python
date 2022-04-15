import pytest
import os
import pins
import vetiver

# Load data, model
X_df, y = vetiver.get_mock_data()
model = vetiver.get_mock_model().fit(X_df, y)

def test_vetiver_write_app():
    file = "app.py"
    v = vetiver.VetiverModel(model=model, ptype_data=X_df,
         model_name="model", versioned=None)
    model_board = pins.board_folder(path=".", versioned=True, allow_pickle_read=True)
    vetiver.vetiver_pin_write(board=model_board, model=v)
    vetiver.vetiver_write_app(model_board, "model", file = "app.py")
    contents = open(file).read()
    os.remove(file)
    version = model_board.pin_versions("model").sort_values(by='created', ascending=False)
    version = version.version[0]
    assert(contents == f"""import vetiver
import pins


b = pins.board_folder('.')
v = vetiver.vetiver_pin_read(b, 'model', version = '{version}')

vetiver_api = vetiver.VetiverAPI(v)
api = vetiver_api.app
""")
