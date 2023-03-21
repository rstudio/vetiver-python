# Release notes


For full details, view the [commit logs](https://github.com/rstudio/vetiver-python/commits/).


## v0.2.0
### What's Changed

[**Full Changelog**](https://github.com/rstudio/vetiver-python/compare/v0.1.8...v0.2.0)

* DOC: Added missing `model_name` to `VetiverModel` in [GH128](https://github.com/rstudio/vetiver-python/pull/128)
* BUG, MAINT: Catch non 200 codes in [GH129](https://github.com/rstudio/vetiver-python/pull/129)
* DOC: fix `deploy_rsconnect` example in [GH1234](https://github.com/rstudio/vetiver-python/pull/134)
* ENH: Make `vetiver_post` extensible for all endpoints in [GH130](https://github.com/rstudio/vetiver-python/pull/130)
* TEST: ci testing to run generated dockerfile in [GH136](https://github.com/rstudio/vetiver-python/pull/136)
* MAINT: rsconnect-python>=1.8.0 in [GH132](https://github.com/rstudio/vetiver-python/pull/132)
* ENH: New `prepare_docker` function in [GH137](https://github.com/rstudio/vetiver-python/pull/137)
* DOC: refresh README and add to docs in [GH141](https://github.com/rstudio/vetiver-python/pull/141)
* TEST: Update weekly tests: only run necessary tests in [GH142](https://github.com/rstudio/vetiver-python/pull/142)
* MAINT: update `ptype_data` to `prototype_data` in [GH138](https://github.com/rstudio/vetiver-python/pull/138)
* ENH: Refactor metadata in [GH126](https://github.com/rstudio/vetiver-python/pull/126)
* MAINT: remove stars for explicit imports in [GH145](https://github.com/rstudio/vetiver-python/pull/145)
* DOC: Changing language from "Example" to "Examples" for docstrings in [GH146](https://github.com/rstudio/vetiver-python/pull/146)
* ENH: Added Python version to `vetiver_pin_write` in [GH127](https://github.com/rstudio/vetiver-python/pull/127)


## v0.1.8
### What's Changed

[**Full Changelog**](https://github.com/rstudio/vetiver-python/compare/v0.1.7...v0.1.8)

* TEST: pins<>vetiver compatibility test in [GH113](https://github.com/rstudio/vetiver-python/pull/113)
* TEST: Update weekly tests to include `rsconnect-python` in [GH117](https://github.com/rstudio/vetiver-python/pull/117)
* DOC: Missing whitespace in InvalidModelError in [GH120](https://github.com/rstudio/vetiver-python/pull/120)
* MAINT: Remove xfail from `test_rsconnect` in [GH119](https://github.com/rstudio/vetiver-python/pull/119)
* MAINT: Add httpx in [GH125](https://github.com/rstudio/vetiver-python/pull/125)
* ENH: Add pin URL to REST API and metadata in [GH123](https://github.com/rstudio/vetiver-python/pull/123)


## v0.1.7
### What's Changed

[**Full Changelog**](https://github.com/rstudio/vetiver-python/compare/v0.1.6...v0.1.7)

* ENH, DOC: have stable and latest docs in [GH93](https://github.com/rstudio/vetiver-python/pull/93)
* BUG: bug fix for load_pkgs function on Windows OS in [GH98](https://github.com/rstudio/vetiver-python/pull/98)
* MAINT: Update attach_pkgs.py in [GH99](https://github.com/rstudio/vetiver-python/pull/99)
* ENH: implement statsmodels handler in [GH100](https://github.com/rstudio/vetiver-python/pull/100)
* FEAT: xgboost handler in [GH101](https://github.com/rstudio/vetiver-python/pull/101)
* ENH: adding model card template in [GH106](https://github.com/rstudio/vetiver-python/pull/106)
* BUG: refactor pseudo version to pin_url in model card in [GH107](https://github.com/rstudio/vetiver-python/pull/107)
* DOC: adding docs, small refactoring in [GH108](https://github.com/rstudio/vetiver-python/pull/108)
* ENH, DOC: add examples to docstrings in [GH109](https://github.com/rstudio/vetiver-python/pull/109)


## v0.1.6
### What's Changed

[**Full Changelog**](https://github.com/rstudio/vetiver-python/compare/v0.1.5...v0.1.6)

* ENH: add `rsconnect_deploy` support for `board_folder` in [GH77](https://github.com/rstudio/vetiver-python/pull/77)
* ENH: model monitoring in [GH76](https://github.com/rstudio/vetiver-python/pull/76)
* DOC: add mini chicago dataset in [GH81](https://github.com/rstudio/vetiver-python/pull/81)
* MAINT: remove trailing slashes in API paths [GH](https://github.com/rstudio/vetiver-python/pull/83)
* ENH: explicitly add `n` to hover data in `plot_metrics` in [GH84](https://github.com/rstudio/vetiver-python/pull/84)
* ENH: initial vetiver_pin_metrics implementation in [GH82](https://github.com/rstudio/vetiver-python/pull/82)
* MAINT, ENH: Use setuptools_scm for tagged versioning in [GH86](https://github.com/rstudio/vetiver-python/pull/86)
* ENH: handlers to register themselves in [GH87](https://github.com/rstudio/vetiver-python/pull/87)
* BUG: coerce date var to datetime in [GH89](https://github.com/rstudio/vetiver-python/pull/89)
