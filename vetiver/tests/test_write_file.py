import pytest
from vetiver.write_fastapi import vetiver_write_app
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
    board = pins.board_folder(path=".")
    
    vetiver_write_app(board=board, pin_name="test", file = file)
    contents = open(file).read()
    os.remove(file)
    assert(contents == """from vetiver import VetiverAPI
from pins import board_folder

b = board_folder(path = '.')

v = b.pin_read('test')

vetiver_api = VetiverAPI(v)
app = vetiver_api.app
""")
