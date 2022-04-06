from vetiver.server import VetiverAPI
<<<<<<< HEAD
import pins

def vetiver_write_app(board: pins.BaseBoard, pin_name,
=======

<<<<<<< HEAD
def write_app(board, name,
>>>>>>> b14210f (scaffolding to write docker)
=======
def vetiver_write_app(board, name,
>>>>>>> 9979f1c (handle loading requirements for docker)
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
=======
    fastapi = f"""from vetiver import VetiverAPI
from pins import board_folder
>>>>>>> 9979f1c (handle loading requirements for docker)

b = board_folder(path = {repr(board.board)})

v = b.pin_read({repr(name)})

vetiver_api = VetiverAPI(v)
app = vetiver_api.app
"""

    f.write(fastapi)
<<<<<<< HEAD


>>>>>>> b14210f (scaffolding to write docker)
=======
>>>>>>> 9979f1c (handle loading requirements for docker)
