import pandas as pd
from sklearn import model_selection
from sklearn.linear_model import LinearRegression
import vetiver
from vetiver.pin_read_write import vetiver_pin_write
from pathlib import Path

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

path = "./examples/coffeeratings/"

model_board = board_folder(path=path, versioned=True, allow_pickle_read=True)
vetiver_pin_write(board=model_board, model=v)

myapp = vetiver.VetiverAPI(v, check_ptype = True)
api = myapp.app

# next, run myapp.run() to start API and see visual documentation
# create app.py file that includes pinned VetiverAPI to be deployed
vetiver.vetiver_write_app(model_board, "v", file = path+"app.py")

# automatically create requirements.txt
vetiver.load_pkgs(model=v, path=path)

# write Dockerfile
vetiver.vetiver_write_docker(path=path, host="0.0.0.0", port="80")

## to run Dockerfile, in CLI
# cd ./coffeeratings
# docker build -t myimage .
# docker run -d --name mycontainer -p 80:80 myimage
