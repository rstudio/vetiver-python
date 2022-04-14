import vetiver
import pins


b = pins.board_folder('./examples/coffeeratings/')
v = vetiver.vetiver_pin_read(b, 'v', version = '20220414T132046Z-c5e63')

vetiver_api = vetiver.VetiverAPI(v)
app = vetiver_api.app
