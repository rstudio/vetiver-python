from vetiver import VetiverAPI
from pins import board_folder

b = board_folder(path = '.')

#v = b.pin_read('lr_model')

vetiver_api = VetiverAPI(v)
api = vetiver_api.app
