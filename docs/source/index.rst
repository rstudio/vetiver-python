.. vetiver documentation master file, created by
   sphinx-quickstart on Thu Mar  3 14:13:21 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

vetiver
===================================
The goal of vetiver is to provide fluent tooling to version, share, deploy, and monitor a trained model. Functions handle both recording and checking the model’s input data prototype, and predicting from a remote API endpoint. 
You can use vetiver with:

- scikit-learn
- pytorch

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Version
==================

.. currentmodule:: vetiver

.. autosummary::
   :toctree: api_doc/

   ~VetiverModel
   ~pin_read_write.vetiver_pin_read
   ~pin_read_write.vetiver_pin_write

Deploy
==================

.. currentmodule:: vetiver

.. autosummary::
   :toctree: api_doc/

   ~VetiverModel

Deploy
==================

.. currentmodule:: vetiver

.. autosummary::
   :toctree: api_doc/

   ~VetiverModel

   ~VetiverAPI
   ~VetiverAPI.run
   ~VetiverAPI.vetiver_post
   ~vetiver_endpoint
   ~load_pkgs
   ~vetiver_write_app
   ~vetiver_write_docker