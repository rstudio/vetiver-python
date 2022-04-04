from vetiver.server import VetiverAPI
<<<<<<< HEAD
import pins

def vetiver_write_app(board: pins.BaseBoard, pin_name,
=======

def write_app(board, name,
>>>>>>> b14210f (scaffolding to write docker)
              file = "app.py"):
    """Write VetiverAPI app to a file

    Attributes
    ----------
    vetiver_api :  VetiverAPI
        API to be written
    name : string
        name of file
    """

    f = open(file, "x")

<<<<<<< HEAD
    app = f"""from vetiver import VetiverAPI
from pins import board_folder

b = board_folder(path = {repr(board.board)})

v = b.pin_read({repr(pin_name)})

vetiver_api = VetiverAPI(v)
app = vetiver_api.app
"""

    f.write(app)
=======
    fastapi = f"""
from vetiver import VetiverAPI
from pins import BaseBoard
import joblib

b = BaseBoard({board})
# read VetiverAPI in, saved as joblib
v = b.pin_read({name})

api = joblib.load(v)

    """


    f.write(fastapi)


>>>>>>> b14210f (scaffolding to write docker)
