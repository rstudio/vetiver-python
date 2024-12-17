import pins

from dotenv import load_dotenv
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from vetiver.data import sacramento
from vetiver import VetiverModel, vetiver_pin_write

load_dotenv()

x = sacramento.drop(columns="price")
y = sacramento["price"]

ohe = OneHotEncoder().fit(x)
lm = LinearRegression().fit(ohe.transform(x), y)
pipeline = Pipeline([("ohe", ohe), ("linear_model", lm)])
v = VetiverModel(pipeline, "isabel.zimmerman/sacramento", x)
board = pins.board_connect(allow_pickle_read=True)
vetiver_pin_write(board=board, model=v)
