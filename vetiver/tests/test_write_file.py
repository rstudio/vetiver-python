<<<<<<< HEAD
<<<<<<< HEAD
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
    vetiver_write_app(board=board, pin_name="model", file = file)
    contents = open(file).read()
    os.remove(file)
    assert(contents == """from vetiver import VetiverAPI
from pins import board_folder

b = board_folder(path = '.')
<<<<<<< HEAD

v = b.pin_read('test')

vetiver_api = VetiverAPI(v)
app = vetiver_api.app
""")
=======
from vetiver.write_fastapi import write_app

# write_app(board="test", name="test", file = "app.py")
>>>>>>> b14210f (scaffolding to write docker)
=======
import pytest
from vetiver.write_fastapi import vetiver_write_app
import os

def test_vetiver_write_app():
    file = "app.py"
    vetiver_write_app(board="test", name="test", file = file)
    contents = open(file).read()
    os.remove(file)
    assert(contents == """
from vetiver import VetiverAPI
from pins import board_folder

b = board_folder(path = 'test')

v = b.pin_read('test')
=======

v = b.pin_read('model')
>>>>>>> e94bfec (adding tests)

vetiver_api = VetiverAPI(v)
app = vetiver_api.app
""")
>>>>>>> 9979f1c (handle loading requirements for docker)