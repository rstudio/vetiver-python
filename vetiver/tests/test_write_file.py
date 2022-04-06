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

vetiver_api = VetiverAPI(v)
app = vetiver_api.app
""")
