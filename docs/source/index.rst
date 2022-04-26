vetiver 🏺
===================================
The goal of vetiver is to provide fluent tooling to version, share, deploy, and monitor a trained model. Functions handle both recording and checking the model’s input data prototype, and predicting from a remote API endpoint. 
You can use vetiver with:

- `scikit-learn <https://scikit-learn.org/stable/>`_
- `pytorch <https://pytorch.org/>`_

This website documents the public API of Vetiver (for Python). See the `main Vetiver website <https://juliasilge.github.io/vetiver.dev/>`_ for
a more holistic introduction to the API. The left-hand sidebar lists the full public
API, and the sections below (linked to the right-hand sidebar) break it into similar groups, based on task.

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
   ~pin_read_write.vetiver_pin_read
   ~pin_read_write.vetiver_pin_write

Deploy
==================

.. currentmodule:: vetiver

.. autosummary::
   :toctree: reference/
   :caption: Deploy

   ~VetiverAPI
   ~VetiverAPI.run
   ~VetiverAPI.vetiver_post
   ~vetiver_endpoint
   ~predict
   ~load_pkgs
   ~vetiver_write_app
   ~vetiver_write_docker
