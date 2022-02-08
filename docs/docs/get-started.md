# Get started

`vetiver` is intended to extend a data science workflow to deployment after a model has been created. It does not offer capabilities to train a machine learning model.

## Installation

`pip install vetiver`

To begin, initialize a `VetiverModel` with a trained model and an example of data (usually training data) to built a data prototype.

```python
my_model = VetiverModel(model = linear_reg, ptype_data = train_data)
```

Next, you can build a model-aware API and run it locally.

```python
my_app = VetiverServe(my_model)
my_app.run()
```
