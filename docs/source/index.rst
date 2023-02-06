vetiver
===================================
The goal of vetiver is to provide fluent tooling to version, share, deploy, and monitor a trained model. Functions handle both recording and checking the model’s input data prototype, and predicting from a remote API endpoint.
You can use vetiver with:

- `scikit-learn <https://scikit-learn.org/stable/>`_
- `pytorch <https://pytorch.org/>`_
- `statsmodels <https://www.statsmodels.org/>`_
- `xgboost <https://xgboost.readthedocs.io/>`_

You can install the released version of vetiver from `PyPI <https://pypi.org/project/vetiver/>`_:

.. code-block:: bash

   python -m pip install vetiver

And the development version from `GitHub <https://github.com/rstudio/vetiver-python>`_ with:

.. code-block:: bash

   python -m pip install git+https://github.com/rstudio/vetiver-python

This website documents the public API of Vetiver (for Python). See `vetiver.rstudio.com <https://vetiver.rstudio.com>`_ for
more on how to get started.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Version
==================

.. currentmodule:: vetiver

.. autosummary::
   :toctree: reference/
   :caption: Version

   ~VetiverModel
   ~vetiver_pin_write
   ~vetiver_create_ptype
   ~model_card

Deploy
==================

.. autosummary::
   :toctree: reference/
   :caption: Deploy

   ~VetiverAPI
   ~VetiverAPI.run
   ~VetiverAPI.vetiver_post
   ~vetiver_endpoint
   ~predict
   ~write_app
   ~write_docker
   ~load_pkgs
   ~prepare_docker
   ~deploy_rsconnect

Monitor
==================

.. autosummary::
   :toctree: reference/
   :caption: Monitor

   ~compute_metrics
   ~pin_metrics
   ~plot_metrics

Model Handlers
==================

.. autosummary::
   :toctree: reference/
   :caption: Model Handlers

   ~BaseHandler
   ~SKLearnHandler
   ~TorchHandler
   ~StatsmodelsHandler
   ~XGBoostHandler


.. toctree::
   advancedusage/custom_handler.md
   :caption: Advanced Usage

.. toctree::
   changelog/index.md
   :caption: Changelog
