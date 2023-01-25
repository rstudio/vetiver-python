from vetiver import VetiverModel
import vetiver
import pins


b = pins.board_folder('pinsboard', allow_pickle_read=True)
v = VetiverModel.from_pin(b, 'mymodel', version = '20221212T191456Z-4f5e3')

vetiver_api = vetiver.VetiverAPI(v)
api = vetiver_api.app
