from vetiver import VetiverAPI
from pins import board_folder

<<<<<<< HEAD
b = board_folder(path = '.')

#v = b.pin_read('lr_model')

vetiver_api = VetiverAPI(v)
api = vetiver_api.app
=======
# affected by deparse 
b = board_folder(path = '/app/coffeeratings/my_board/', allow_pickle_read=True)

v = b.pin_read('v')

vetiver_api = VetiverAPI(v)
app = vetiver_api.app

print(b.pin_meta("v"))
>>>>>>> 99f57e0 (updating path-type things)
