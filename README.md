# vetiver 🏺

<!-- badges: start -->

[![Lifecycle:
experimental](https://img.shields.io/badge/lifecycle-experimental-orange.svg)](https://lifecycle.r-lib.org/articles/stages.html#experimental) [![codecov](https://codecov.io/gh/isabelizimm/vetiver-python/branch/main/graph/badge.svg?token=CW6JHVS6ZX)](https://codecov.io/gh/isabelizimm/vetiver-python)

<!-- badges: end -->

_Vetiver, the oil of tranquility, is used as a stabilizing ingredient in perfumery to preserve more volatile fragrances._

Python parallel to [R vetiver](https://github.com/tidymodels/vetiver) package.

## Usage

`vetiver` is used to deploy a trained model to predict from a remote endpoint.

Key features include:

- **Simple:** designed to fit into a data scientist's natural workflow
- **Robust:** ability to check input data types to minimize type failures in a model
- **Advanced support:** easily deploy multiple endpoints to handle pre- and post- processing
- Based on [FastAPI](https://github.com/tiangolo/fastapi), using [OpenAPI](https://github.com/OAI/OpenAPI-Specification)

## Get Started

`pip install vetiver`

To begin, initialize a `VetiverModel` with a trained model and an example of data (usually training data) to built a data prototype.

```python
my_model = VetiverModel(model = linear_reg, ptype_data = train_data)
```

Next, you can build a model-aware API and run it locally.

```python
my_app = VetiverAPI(my_model)
my_app.run()
```

To view more, see [this repo of examples](https://github.com/isabelizimm/vetiverpydemo).

## License

## Contributing

This project is released with a [Contributor Code of
Conduct](https://contributor-covenant.org/version/2/0/CODE_OF_CONDUCT.html).
By contributing to this project, you agree to abide by its terms.
