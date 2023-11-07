# Release notes


For full details, view the [commit logs](https://github.com/rstudio/vetiver-python/commits/).

## v0.2.3
## What's Changed

[**Full Changelog**](https://github.com/rstudio/vetiver-python/compare/v0.2.2...v0.2.3)

* ENH: add `root_path` if user in Posit Workbench in [GH191](https://github.com/rstudio/vetiver-python/pull/191)


## v0.2.2
### What's Changed

[**Full Changelog**](https://github.com/rstudio/vetiver-python/compare/v0.2.1...v0.2.2)

* DOCS: add square logo in [GH173](https://github.com/rstudio/vetiver-python/pull/173)
* DOCS: add API structure documentation in [GH176](https://github.com/rstudio/vetiver-python/pull/176)
* DOCS: update docs to look less like vetiver.rstudio.com in [GH178](https://github.com/rstudio/vetiver-python/pull/178)
* BUG: remove __all__ in init in [GH182](https://github.com/rstudio/vetiver-python/pull/182)
* MAINT: require no less than pins 0.7.1 in [GH183](https://github.com/rstudio/vetiver-python/pull/183)
* ENH: endpoint_fx docstring as FastAPI description in [GH179](https://github.com/rstudio/vetiver-python/pull/179)
* MAINT: Update Pydantic usage for v2 compatibility in [GH185](https://github.com/rstudio/vetiver-python/pull/185)
* MAINT: Update model_card.qmd by in [GH186](https://github.com/rstudio/vetiver-python/pull/186)
* ENH: add `/GET` prototype endpoint in [GH174](https://github.com/rstudio/vetiver-python/pull/174)
* BUG: use max instead of first in [GH189](https://github.com/rstudio/vetiver-python/pull/189)

## v0.2.1
### What's Changed

[**Full Changelog**](https://github.com/rstudio/vetiver-python/compare/v0.2.0...v0.2.1)

* DOC: add changelog in [GH151](https://github.com/rstudio/vetiver-python/pull/151)
* FIX: None type handling for `python_version` in metadata [GH149](https://github.com/rstudio/)vetiver-python/pull/149
* Match GHA Python versions to Connect [GH157](https://github.com/rstudio/vetiver-python/pull/157)
* DOCS: move from sphinx to quartodoc [GH153](https://github.com/rstudio/vetiver-python/pull/153)
* BUG,CI: /latest not rendering correctly [GH158](https://github.com/rstudio/vetiver-python/pull/158)
* MAINT: spring cleaning [GH160](https://github.com/rstudio/vetiver-python/pull/160)
* DOCS: Add netlify docs preview [GH163](https://github.com/rstudio/vetiver-python/pull/163)
* MAINT: spring cleaning [GH164](https://github.com/rstudio/vetiver-python/pull/164)
* ENH: Refactor server handling [GH155](https://github.com/rstudio/vetiver-python/pull/155)
* FEAT: add required packages to authorize pins boards [GH166](https://github.com/rstudio/vetiver-python/)pull/166
* MAINT: start typing vetiver [GH168](https://github.com/rstudio/vetiver-python/pull/168)
* FEAT: add new `/metadata` GET endpoint [GH170](https://github.com/rstudio/vetiver-python/pull/170)
* FEAT: implement spacy models [GH143](https://github.com/rstudio/vetiver-python/pull/143)

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
