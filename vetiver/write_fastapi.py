from vetiver.server import VetiverAPI

def vetiver_write_app(board, name,
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

    fastapi = f"""from vetiver import VetiverAPI
from pins import board_folder

b = board_folder(path = {repr(board.board)})

v = b.pin_read({repr(name)})

vetiver_api = VetiverAPI(v)
app = vetiver_api.app
"""

    f.write(fastapi)
