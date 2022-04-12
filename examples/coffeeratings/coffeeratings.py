import pandas as pd
from sklearn import model_selection
from sklearn.linear_model import LinearRegression
import vetiver
from vetiver.pin_read_write import vetiver_pin_write

# Load training data
raw = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-07-07/coffee_ratings.csv')
df = pd.DataFrame(raw)
coffee = df[["total_cup_points", "aroma", "flavor", "sweetness", "acidity", \
    "body", "uniformity", "balance"]].dropna()

X_train, X_test, y_train, y_test = model_selection.train_test_split(coffee.iloc[:,1:],coffee['total_cup_points'],test_size=0.2)

# fit model
lr_fit = LinearRegression().fit(X_train, y_train)

# create vetiver model
v = vetiver.VetiverModel(lr_fit, save_ptype = True, ptype_data=X_train, model_name = "v")

# version model via pin
from pins import board_folder

model_board = board_folder(path=".", versioned=True, allow_pickle_read=True)
vetiver_pin_write(board=model_board, model=v)

myapp = vetiver.VetiverAPI(v, check_ptype = True)
api = myapp.app

# next, run myapp.run() to start API and see visual documentation

path = "./examples/coffeeratings/"
# create app.py file that includes pinned VetiverAPI to be deployed
vetiver.vetiver_write_app(model_board, "lr_model", file = path+"app.py")

# automatically create requirements.txt
vetiver.load_pkgs(model=v, path=path)

# write Dockerfile
vetiver.vetiver_write_docker(app_file="app.py", path=path, host="0.0.0.0", port="80")
