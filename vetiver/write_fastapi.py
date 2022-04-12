from vetiver.server import VetiverAPI
import pins

def vetiver_write_app(board: pins.BaseBoard, pin_name,
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

    app = f"""from vetiver import VetiverAPI
from pins import board_folder

b = board_folder(path = {repr(board.board)})

v = b.pin_read({repr(pin_name)})

vetiver_api = VetiverAPI(v)
app = vetiver_api.app
"""

    f.write(app)
