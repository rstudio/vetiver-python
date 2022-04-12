import pins

def vetiver_write_app(board: pins.BaseBoard, pin_name: str,
              file = "app.py"):
    """Write VetiverAPI app to a file

    Attributes
    ----------
    vetiver_api :  VetiverAPI
        API to be written
    name : string
        name of file
    """
    # board deparse https://github.com/machow/pins-python/issues/89
    f = open(file, "x")

    app = f"""from vetiver import VetiverAPI
from pins import board_folder

# affected by deparse 
b = board_folder(path = {board.board}, allow_pickle_read=True)

v = b.pin_read({pin_name})

vetiver_api = VetiverAPI(v)
app = vetiver_api.app
"""

    f.write(app)
