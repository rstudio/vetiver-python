import vetiver
import pins

# edited to reflect Docker container path, and allow_pickle_read=True
b = pins.board_folder('/code/app', allow_pickle_read=True)
v = vetiver.vetiver_pin_read(b, 'v', version = '20220415T174503Z-06d9b')

vetiver_api = vetiver.VetiverAPI(v)
api = vetiver_api.app
