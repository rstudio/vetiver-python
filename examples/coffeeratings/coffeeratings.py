import pandas as pd
from sklearn import model_selection
from sklearn.linear_model import LinearRegression
from vetiver import VetiverModel, VetiverAPI, vetiver_write_app, attach_pkgs, vetiver_write_docker

# Load training data
raw = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-07-07/coffee_ratings.csv')
df = pd.DataFrame(raw)
coffee = df[["total_cup_points", "aroma", "flavor", "sweetness", "acidity", \
    "body", "uniformity", "balance"]].dropna()

X_train, X_test, y_train, y_test = model_selection.train_test_split(coffee.iloc[:,1:],coffee['total_cup_points'],test_size=0.2)

lr_fit = LinearRegression().fit(X_train, y_train)

v = VetiverModel(lr_fit, save_ptype = False, ptype_data=X_train, model_name = "v")

from pins import board_folder

model_board = board_folder(path="/tmp/test", versioned=True)
model_board.pin_write(v, name="lr_model", title="", type="joblib")

myapp = VetiverAPI(coffee, check_ptype = False)

# next, run myapp.run() to start API and see visual documentation

path = "./examples/coffeeratings/"
# create app.py file that includes pinned VetiverAPI to be deployed
vetiver_write_app(model_board, "lr_model", file = path+"app.py")

# automatically create requirements.txt
attach_pkgs.load_pkgs(packages = v.metadata.get("required_pkgs"), path=path)

# write Dockerfile
vetiver_write_docker(app_file="app.py", path=path, host="0.0.0.0", port="80")
