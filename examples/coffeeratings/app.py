from vetiver import VetiverAPI
from pins import board_folder

b = board_folder(path = '/tmp/test')

v = b.pin_read('lr_model')

vetiver_api = VetiverAPI(v)
app = vetiver_api.app
