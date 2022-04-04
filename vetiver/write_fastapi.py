from vetiver.server import VetiverAPI

def write_app(board, name,
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


